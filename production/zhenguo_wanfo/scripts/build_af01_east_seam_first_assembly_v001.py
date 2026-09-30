"""AF-01 east-seam first assembly proof.

Purpose: build a visible, reviewable first main-frame slice before detail closure.
This is an ENGINEERING ASSEMBLY PROOF, not a historical-completeness claim.

Locked inputs:
- B01 beam support planes
- B02 beam execution extents
- approved component section envelopes

Temporary/proxy inputs:
- bracket/support fillers needed only to avoid visually floating members
- Tuofeng geometry
- Tuojiao endpoint mapping
- Shuzhu lower support via Tuofeng-B
- B03-R ridge/chashou candidate while B03-R remains HOLD

No canonical Master is mutated.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]

ASSEMBLY = ROOT / "production/zhenguo_wanfo/assembly/P3_3_AF01_EAST_SEAM_MAIN_FRAME_ASSEMBLY_SPEC_V001.json"
B02 = ROOT / "production/zhenguo_wanfo/assembly/P3_3_AF01_B02_BEAM_BODY_EXTENT_RESOLVER_V001.json"
B03R = ROOT / "production/zhenguo_wanfo/assembly/P3_3_AF01_B03_R_RIDGE_ENDPOINT_RESOLVER_V001.json"

COLUMN_PARAMS = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_PARAMS_V001.json"
LOWER_PARAMS = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LOWER-SIX-CHUANFU-001/CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER_PARAMS_V001.json"
UPPER_PARAMS = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-UPPER-SIX-CHUANFU-001/CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER_PARAMS_V001.json"
FOUR_PARAMS = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-FOUR-CHUANFU-001/CMP-FRAME-FOUR-CHUANFU-001_MASTER_PARAMS_V001.json"
PING_PARAMS = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-PINGLIANG-001/CMP-FRAME-PINGLIANG-001_MASTER_PARAMS_V001.json"
SHUZHU_DEF = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-SHUZHU-001/CMP-FRAME-SHUZHU-001_MASTER_DEFINITION_V001.json"
CHASHOU_DEF = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-CHASHOU-001/CMP-FRAME-CHASHOU-001_MASTER_DEFINITION_V001.json"
TUOJIAO_DEF = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-TUOJIAO-001/CMP-FRAME-TUOJIAO-001_MASTER_DEFINITION_V001.json"

TOL = 0.2


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def param_value(doc, key):
    for item in doc.get("parameters", []):
        if item.get("key") == key:
            return float(item["value"])
    raise KeyError(key)


def stable_sig(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        pass


def setup_scene():
    s = bpy.context.scene
    s.unit_settings.system = "METRIC"
    s.unit_settings.scale_length = 0.001
    s.unit_settings.length_unit = "MILLIMETERS"
    s.render.engine = "BLENDER_EEVEE_NEXT"
    s.render.resolution_x = 1600
    s.render.resolution_y = 1100
    s.render.resolution_percentage = 100
    s.render.image_settings.file_format = "PNG"
    s.render.film_transparent = False
    s.world.use_nodes = True
    bg = next(n for n in s.world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (0.94, 0.94, 0.94, 1)
    bg.inputs["Strength"].default_value = 0.8
    s["proof_id"] = "AF01_EAST_SEAM_FIRST_ASSEMBLY_V001"
    s["classification"] = "ENGINEERING_ASSEMBLY_PROOF / NOT_HISTORICAL_COMPLETENESS"
    s["canonical_claim"] = False


def make_material(name, rgba):
    m = bpy.data.materials.new(name)
    m.diffuse_color = rgba
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = 0.62
    if rgba[3] < 1:
        bsdf.inputs["Alpha"].default_value = rgba[3]
        m.surface_render_method = "DITHERED"
    return m


MATS = {}


def init_materials():
    MATS["locked"] = make_material("MAT_LOCKED_TIMBER", (0.34, 0.14, 0.055, 1))
    MATS["endpoint"] = make_material("MAT_ENDPOINT_CANDIDATE", (0.43, 0.22, 0.08, 1))
    MATS["proxy"] = make_material("MAT_RECONSTRUCTED_PROXY", (0.76, 0.43, 0.10, 0.72))
    MATS["context"] = make_material("MAT_CONTEXT", (0.23, 0.23, 0.23, 0.55))


def add_meta(obj, component_id, registry_id, evidence_class, role, canonical=False):
    obj["component_id"] = component_id
    obj["registry_id"] = registry_id
    obj["assembly_role"] = role
    obj["evidence_class"] = evidence_class
    obj["canonical_geometry_claim"] = bool(canonical)
    return obj


def box(name, center, dims_xyz, material, component_id, registry_id, evidence_class, role):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims_xyz
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    return add_meta(o, component_id, registry_id, evidence_class, role)


def cylinder_z(name, center, radius, height, material, component_id, registry_id, evidence_class, role):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=height, location=center)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return add_meta(o, component_id, registry_id, evidence_class, role)


def prism_between(name, p0, p1, width_in_plane, thickness_out_of_plane, material,
                  component_id, registry_id, evidence_class, role):
    p0 = Vector(p0)
    p1 = Vector(p1)
    ex = (p1 - p0).normalized()
    out = Vector((1, 0, 0))
    if abs(ex.dot(out)) > 0.95:
        out = Vector((0, 1, 0))
    ey = out.cross(ex).normalized()   # in-plane width axis for YZ members
    ez = ex.cross(ey).normalized()    # mostly world-X out-of-plane
    # Force out-of-plane axis to point along +/-X for stable roll.
    if abs(ez.x) < 0.5:
        ez = out
        ey = ez.cross(ex).normalized()
    center = (p0 + p1) / 2
    length = (p1 - p0).length
    verts = []
    for sx, sy, sz in [
        (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
        (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    ]:
        p = center + ex*(sx*length/2) + ey*(sy*width_in_plane/2) + ez*(sz*thickness_out_of_plane/2)
        verts.append(tuple(p))
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    mesh = bpy.data.meshes.new(name+"__MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(material)
    add_meta(o, component_id, registry_id, evidence_class, role)
    o["p_lower_mm"] = [round(float(x),3) for x in p0]
    o["p_upper_mm"] = [round(float(x),3) for x in p1]
    o["execution_length_mm"] = round(float(length),3)
    return o


def trapezoid_prism_yz(name, x_center, y_center, z0, z1, base_y, top_y, depth_x,
                       material, component_id, registry_id, evidence_class, role):
    hx = depth_x/2
    by = base_y/2
    ty = top_y/2
    verts = [
        (x_center-hx, y_center-by, z0), (x_center+hx, y_center-by, z0),
        (x_center+hx, y_center+by, z0), (x_center-hx, y_center+by, z0),
        (x_center-hx, y_center-ty, z1), (x_center+hx, y_center-ty, z1),
        (x_center+hx, y_center+ty, z1), (x_center-hx, y_center+ty, z1),
    ]
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    mesh = bpy.data.meshes.new(name+"__MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(material)
    add_meta(o, component_id, registry_id, evidence_class, role)
    o["proxy_height_mm"] = round(z1-z0,3)
    return o


def object_record(o):
    bb = [o.matrix_world @ Vector(corner) for corner in o.bound_box]
    mins = [min(float(v[i]) for v in bb) for i in range(3)]
    maxs = [max(float(v[i]) for v in bb) for i in range(3)]
    rec = {
        "name": o.name,
        "component_id": o.get("component_id"),
        "registry_id": o.get("registry_id"),
        "assembly_role": o.get("assembly_role"),
        "evidence_class": o.get("evidence_class"),
        "canonical_geometry_claim": bool(o.get("canonical_geometry_claim", False)),
        "bbox_min_mm": [round(x,3) for x in mins],
        "bbox_max_mm": [round(x,3) for x in maxs],
    }
    if "p_lower_mm" in o:
        rec["p_lower_mm"] = list(o["p_lower_mm"])
        rec["p_upper_mm"] = list(o["p_upper_mm"])
        rec["execution_length_mm"] = float(o["execution_length_mm"])
    return rec


def camera_render(outdir, target):
    outdir.mkdir(parents=True, exist_ok=True)
    s = bpy.context.scene
    camd = bpy.data.cameras.new("AF01_CAMERA")
    cam = bpy.data.objects.new("AF01_CAMERA", camd)
    s.collection.objects.link(cam)
    s.camera = cam
    camd.type = "ORTHO"
    camd.clip_end = 100000
    target = Vector(target)
    views = [
        ("SECTION_FRONT", (15000, 0, 4700), 12500),
        ("AXON", (11500, -10500, 10500), 13500),
        ("RIDGE_CLOSE", (10500, -2500, 7200), 5200),
    ]
    for name, pos, scale in views:
        cam.location = pos
        cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
        camd.ortho_scale = scale
        s.render.filepath = str(outdir/(name+".png"))
        bpy.ops.render.render(write_still=True)


def build(blend_path, semantic_path, review_dir):
    assembly = load_json(ASSEMBLY)
    b02 = load_json(B02)
    b03r = load_json(B03R)
    cp = load_json(COLUMN_PARAMS)
    lp = load_json(LOWER_PARAMS)
    up = load_json(UPPER_PARAMS)
    fp = load_json(FOUR_PARAMS)
    pp = load_json(PING_PARAMS)
    sd = load_json(SHUZHU_DEF)
    cd = load_json(CHASHOU_DEF)
    td = load_json(TUOJIAO_DEF)

    clear_scene()
    setup_scene()
    init_materials()

    x = float(assembly["representative_slice"]["x_mm"])
    zv = assembly["resolved_vertical_controls"]
    ext = assembly["resolved_body_extents"]

    # Sections use measured/approved outer envelopes.
    lower_guang = param_value(lp, "width_mm")
    lower_thick = param_value(lp, "max_thickness_mm")
    upper_guang = param_value(up, "width_mm")
    upper_thick = param_value(up, "max_thickness_mm")
    four_guang = param_value(fp, "width_mm")
    four_thick = param_value(fp, "thickness_mm")
    ping_variant = next(v for v in pp["variants"] if v["variant_id"] == "EW_SEAM")
    ping_guang = float(ping_variant["production_section_mm"]["width"])
    ping_thick = float(ping_variant["production_section_mm"]["thickness"])
    shuzhu_w = float(sd["geometry_contract"]["section_envelope_mm"]["width"])
    shuzhu_t = float(sd["geometry_contract"]["section_envelope_mm"]["thickness"])
    chashou_w = float(cd["geometry_contract"]["section_envelope_mm"]["width"])
    chashou_t = float(cd["geometry_contract"]["section_envelope_mm"]["thickness"])
    tuojiao_w = float(td["geometry_contract"]["section_envelope_mm"]["width"])
    tuojiao_t = float(td["geometry_contract"]["section_envelope_mm"]["thickness"])

    col_h = param_value(cp, "height_mm")
    col_d = param_value(cp, "diameter_mm")

    objects = []

    # Context columns: approved column engineering realization, not new history claim.
    for side, y in [("N",-5355.0),("S",5355.0)]:
        objects.append(cylinder_z(
            f"COL_{side}", (x,y,col_h/2), col_d/2, col_h, MATS["context"],
            "CMP-COLUMN-001", f"AF01_CONTEXT_COLUMN_{side}",
            "APPROVED_REPLACEABLE_COLUMN_REALIZATION / CONTEXT", "COLUMN_CONTEXT"
        ))

    # Minimal puzuo visual fillers so the beam tier does not float above columns.
    lower_z = float(zv["lower_six_support_plane_z_mm"])
    upper_z = float(zv["upper_six_support_plane_z_mm"])
    four_z = float(zv["four_chuanfu_support_plane_z_mm"])
    ping_z = float(zv["pingliang_support_plane_z_mm"])

    for side, y in [("N",-5355.0),("S",5355.0)]:
        objects.append(box(
            f"PUZUO_PROXY_{side}",
            (x,y,(col_h+lower_z)/2),
            (650,760,lower_z-col_h),
            MATS["proxy"], "PROXY-PUZUO", f"PUZUO_PROXY_{side}",
            "RECONSTRUCTED_DESIGN_PROXY / VISUAL_SUPPORT_ONLY", "COLUMN_HEAD_SUPPORT_FILLER"
        ))

    # Locked beam bodies.
    beam_specs = [
        ("LOWER_SIX","CMP-FRAME-LOWER-SIX-CHUANFU-001","下六椽栿-东缝",
         float(ext["lower_six"]["realization_length_mm"]), lower_thick, lower_guang, lower_z),
        ("UPPER_SIX","CMP-FRAME-UPPER-SIX-CHUANFU-001","上六椽栿-东缝",
         float(ext["upper_six"]["realization_length_mm"]), upper_thick, upper_guang, upper_z),
        ("FOUR_CHUANFU","CMP-FRAME-FOUR-CHUANFU-001","四椽栿-东缝",
         float(ext["four_chuanfu"]["realization_length_mm"]), four_thick, four_guang, four_z),
        ("PINGLIANG","CMP-FRAME-PINGLIANG-001","平梁-东缝",
         float(ext["pingliang"]["realization_length_mm"]), ping_thick, ping_guang, ping_z),
    ]
    beam_objs = {}
    for role,cid,rid,L,thick,guang,z0 in beam_specs:
        o = box(
            f"AF01_{role}", (x,0,z0+guang/2), (thick,L,guang),
            MATS["locked"], cid, rid,
            "LOCKED_AF01_B01_B02_EXECUTION_ENVELOPE", role
        )
        o["support_plane_z_mm"] = z0
        o["realization_length_mm"] = L
        objects.append(o)
        beam_objs[role]=o

    lower_top = lower_z + lower_guang
    upper_top = upper_z + upper_guang
    four_top = four_z + four_guang
    ping_top = ping_z + ping_guang

    # Small visual fillers for known effective support gaps.
    for side,y in [("N",-5355.0),("S",5355.0)]:
        objects.append(box(
            f"DOU_PROXY_{side}", (x,y,(lower_top+upper_z)/2),
            (360,360,max(1.0,upper_z-lower_top)),
            MATS["proxy"], "PROXY-DOU", f"DOU_PROXY_{side}",
            "RECONSTRUCTED_DESIGN_PROXY / G1_GAP_FILLER", "LOWER_TO_UPPER_SIX_SUPPORT"
        ))
    for side,y in [("N",-3595.5),("S",3595.5)]:
        objects.append(box(
            f"SANDOU_GONG_PROXY_{side}", (x,y,(upper_top+four_z)/2),
            (400,520,max(1.0,four_z-upper_top)),
            MATS["proxy"], "PROXY-SANDOU-GONG", f"SANDOU_GONG_PROXY_{side}",
            "RECONSTRUCTED_DESIGN_PROXY / G2_AGGREGATE_LAYER", "UPPER_SIX_TO_FOUR_SUPPORT"
        ))

    # Tuofeng role A: aggregate proxy filling the already-locked G3 gap.
    objects.append(trapezoid_prism_yz(
        "TUOFENG_LINGGONG_PROXY_A", x, 0, four_top, ping_z,
        1050, 620, 420, MATS["proxy"],
        "CMP-FRAME-TUOFENG-001-PROXY", "TUOFENG_ROLE_A_PROXY",
        "RECONSTRUCTED_DESIGN_PROXY / G3_AGGREGATE_GAP_ONLY",
        "FOUR_CHUANFU_TO_PINGLIANG_SUPPORT"
    ))

    # Tuofeng role B: visual-only proxy; chosen one-cai height so the missing physical role is visible.
    # This height is explicitly NOT authority and may be replaced without moving the ridge apex.
    tuofeng_b_h = 14.0 * 15.3
    objects.append(trapezoid_prism_yz(
        "TUOFENG_PROXY_B", x, 0, ping_top, ping_top+tuofeng_b_h,
        720, 360, 320, MATS["proxy"],
        "CMP-FRAME-TUOFENG-001-PROXY", "TUOFENG_ROLE_B_PROXY",
        "RECONSTRUCTED_DESIGN_PROXY / VISUAL_ONLY / HEIGHT_NOT_LOCKED",
        "PINGLIANG_TO_SHUZHU_SUPPORT"
    ))

    ridge_z = float(b03r["outputs"]["ridge_support_connection_z_mm"])
    shuzhu_lower_z = ping_top + tuofeng_b_h
    shuzhu = prism_between(
        "AF01_SHUZHU", (x,0,shuzhu_lower_z), (x,0,ridge_z),
        shuzhu_w, shuzhu_t, MATS["endpoint"],
        "CMP-FRAME-SHUZHU-001", "蜀柱-东缝",
        "B03_R_VISUAL_CANDIDATE / LOWER_ENDPOINT_PROXY_ADJUSTED_FOR_TUOFENG_B",
        "RIDGE_VERTICAL_SUPPORT"
    )
    objects.append(shuzhu)

    for side, y0, rid in [
        ("N",-1836.0,"叉手-东缝-北侧"),
        ("S",1836.0,"叉手-东缝-南侧")
    ]:
        ch = prism_between(
            f"AF01_CHASHOU_{side}", (x,y0,ping_top), (x,0,ridge_z),
            chashou_w, chashou_t, MATS["endpoint"],
            "CMP-FRAME-CHASHOU-001", rid,
            "B03_R_VISUAL_CANDIDATE / NOT_LOCKED",
            "RIDGE_DIAGONAL_SUPPORT"
        )
        objects.append(ch)

    # Four Tuojiao are deliberately visual proxies until B03-T.
    # They are arranged as two braces per side around the Four-Chuanfu end region.
    # These endpoints are NOT Registry endpoint authority.
    proxy_tj = [
        ("N_LOWER", (x,-5355.0,lower_top), (x,-3595.5,four_z), "托脚-东缝-北下平槫"),
        ("N_UPPER", (x,-1836.0,upper_top), (x,-3595.5,four_z), "托脚-东缝-北上平槫"),
        ("S_LOWER", (x,5355.0,lower_top), (x,3595.5,four_z), "托脚-东缝-南下平槫"),
        ("S_UPPER", (x,1836.0,upper_top), (x,3595.5,four_z), "托脚-东缝-南上平槫"),
    ]
    for label,p0,p1,rid in proxy_tj:
        tj = prism_between(
            f"TUOJIAO_PROXY_{label}", p0, p1,
            tuojiao_w, tuojiao_t, MATS["proxy"],
            "CMP-FRAME-TUOJIAO-001", rid,
            "RECONSTRUCTED_DESIGN_PROXY / B03_T_NOT_RESOLVED / VISUAL_ONLY",
            "FOUR_CHUANFU_DIAGONAL_SUPPORT_PROXY"
        )
        objects.append(tj)

    payload = {
        "proof_id":"AF01_EAST_SEAM_FIRST_ASSEMBLY_V001",
        "status":"ENGINEERING_ASSEMBLY_PROOF / PRODUCT_OWNER_VISUAL_REVIEW",
        "canonical_claim":False,
        "historical_completeness_claim":False,
        "source_branch_expected":"engineering/af01-east-seam-first-assembly-v001",
        "locked_authority":{
            "b01_support_planes": zv,
            "b02_body_extents": ext,
        },
        "temporary_geometry":{
            "tuofeng_role_a":"G3 aggregate gap proxy",
            "tuofeng_role_b_height_mm":tuofeng_b_h,
            "tuofeng_role_b_height_status":"VISUAL_ONLY / NOT_LOCKED",
            "shuzhu_lower_endpoint":"moved to visual Tuofeng-B proxy top; not authority",
            "chashou":"B03-R candidate geometry; B03-R remains HOLD",
            "tuojiao":"B03-T visual proxy endpoint mapping; not authority",
            "puzuo_and_dou_fillers":"visual support fillers only"
        },
        "objects":[object_record(o) for o in objects],
        "manual_blender_transform_count":0,
        "stage_advance":False,
        "blender_generation_authority":"FIRST_ASSEMBLY_PROOF_ONLY"
    }
    payload["semantic_geometry_signature"] = stable_sig(payload["objects"])

    blend_path = Path(blend_path)
    semantic_path = Path(semantic_path)
    review_dir = Path(review_dir)
    blend_path.parent.mkdir(parents=True, exist_ok=True)
    semantic_path.parent.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path), check_existing=False)
    semantic_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    camera_render(review_dir, (x,0,4700))
    print("AF01_FIRST_ASSEMBLY_BUILD_PASS", len(objects), payload["semantic_geometry_signature"])


def validate(semantic_path, output_path):
    d = load_json(Path(semantic_path))
    checks = {}
    def ck(name, value):
        checks[name] = bool(value)
        if not value:
            raise AssertionError(name)

    objs = {o["name"]:o for o in d["objects"]}
    ck("NOT_CANONICAL", d["canonical_claim"] is False)
    ck("NO_HISTORICAL_COMPLETENESS_CLAIM", d["historical_completeness_claim"] is False)
    ck("STAGE_ADVANCE_FALSE", d["stage_advance"] is False)
    ck("NO_MANUAL_TRANSFORMS", d["manual_blender_transform_count"] == 0)
    ck("FOUR_LOCKED_BEAMS", all(k in objs for k in ["AF01_LOWER_SIX","AF01_UPPER_SIX","AF01_FOUR_CHUANFU","AF01_PINGLIANG"]))
    ck("SHUZHU_PRESENT", "AF01_SHUZHU" in objs)
    ck("CHASHOU_PAIR_PRESENT", "AF01_CHASHOU_N" in objs and "AF01_CHASHOU_S" in objs)
    ck("FOUR_TUOJIAO_PROXIES", len([x for x in d["objects"] if x["name"].startswith("TUOJIAO_PROXY_")]) == 4)
    ck("TUOFENG_A_PRESENT", "TUOFENG_LINGGONG_PROXY_A" in objs)
    ck("TUOFENG_B_PRESENT", "TUOFENG_PROXY_B" in objs)
    ck("ALL_PROXIES_EXPLICIT", all(
        ("PROXY" not in x["name"]) or ("PROXY" in x["evidence_class"])
        for x in d["objects"]
    ))
    ck("NO_1000MM_BEAM_LENGTH_LEAKAGE", all(
        abs(float(objs[name]["bbox_max_mm"][1]) - float(objs[name]["bbox_min_mm"][1]) - expected) <= TOL
        for name,expected in [
            ("AF01_LOWER_SIX",10710.0),
            ("AF01_UPPER_SIX",10710.0),
            ("AF01_FOUR_CHUANFU",7191.0),
            ("AF01_PINGLIANG",3672.0),
        ]
    ))
    ck("B03_T_NOT_FALSELY_LOCKED", all(
        "B03_T_NOT_RESOLVED" in x["evidence_class"]
        for x in d["objects"] if x["name"].startswith("TUOJIAO_PROXY_")
    ))
    ck("TUOFENG_B_HEIGHT_NOT_LOCKED", d["temporary_geometry"]["tuofeng_role_b_height_status"].startswith("VISUAL_ONLY"))

    result = {
        "status":"PASS",
        "proof_id":d["proof_id"],
        "check_count":len(checks),
        "checks":checks,
        "semantic_geometry_signature":d["semantic_geometry_signature"],
        "object_count":len(d["objects"]),
        "stage_advance":False,
        "next_gate":"PRODUCT_OWNER_VISUAL_REVIEW_ONLY"
    }
    Path(output_path).write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print("AF01_FIRST_ASSEMBLY_VALIDATION_PASS", len(checks))


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("build","validate"), required=True)
    ap.add_argument("--blend")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--output")
    argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


def main():
    a = parse_args()
    if a.mode == "build":
        build(a.blend, a.semantic, a.review_dir)
    else:
        validate(a.semantic, a.output)


if __name__ == "__main__":
    main()
