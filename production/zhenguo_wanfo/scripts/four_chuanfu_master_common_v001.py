"""T-021 shared Blender builder, inspector and review renderer for four-chuanfu Master."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
GEOMETRY_KEYS = ("realization_length_mm", "width_mm", "thickness_mm")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path):
    path = Path(path).resolve()
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def stable_signature(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def param_map(data):
    values = {item["key"]: item for item in data["parameters"]}
    assert len(values) == len(data["parameters"])
    assert data["component_id"] == "CMP-FRAME-FOUR-CHUANFU-001"
    assert data["master_id"] == "CMP-FRAME-FOUR-CHUANFU-001_MASTER"
    assert data["master_version"] == "V001"
    assert data["geometry_mode"] == "BOUNDED_LONG_MEMBER_OUTER_ENVELOPE"
    assert data["unit"] == "mm"
    assert data["unsupported_geometry"] == []
    assert data["p2_primary_frame_proxy_geometry_use_count"] == 0
    assert data["sample_to_instance_mapping"] == "UNKNOWN"
    assert data["report_design_analysis"]["geometry_use_count"] == 0
    assert values["historical_full_length_mm"]["value"] is None
    assert values["historical_full_length_mm"]["classification"] == "UNKNOWN"
    assert values["canonical_reference_length_mm"]["classification"] == "PROJECT_RULE"
    assert values["canonical_reference_length_mm"]["historical_claim"] is False
    assert values["realization_length_mm"]["derives_from"] == "canonical_reference_length_mm"
    assert float(values["realization_length_mm"]["value"]) == float(values["canonical_reference_length_mm"]["value"])
    assert all(float(values[key]["value"]) > 0 for key in GEOMETRY_KEYS)
    return values


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        if collection != bpy.context.scene.collection:
            bpy.data.collections.remove(collection)


def names():
    root = "MASTER__CMP_FRAME_FOUR_CHUANFU_001"
    return root, root + "__BODY"


def make_mesh(data, values):
    length, width, height = (float(values[key]["value"]) for key in GEOMETRY_KEYS)
    verts = [
        (-length / 2, -width / 2, 0), (length / 2, -width / 2, 0),
        (length / 2, width / 2, 0), (-length / 2, width / 2, 0),
        (-length / 2, -width / 2, height), (length / 2, -width / 2, height),
        (length / 2, width / 2, height), (-length / 2, width / 2, height)
    ]
    faces = [(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
    collection_name, body_name = names()
    mesh = bpy.data.meshes.new(body_name + "__MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    obj = bpy.data.objects.new(body_name, mesh)
    collection.objects.link(obj)
    obj.location = (0,0,0)
    obj.rotation_euler = (0,0,0)
    obj.scale = (1,1,1)
    obj["component_id"] = data["component_id"]
    obj["master_id"] = data["master_id"]
    obj["master_version"] = data["master_version"]
    obj["historical_full_length_state"] = "UNKNOWN_NULL_DO_NOT_LOCK"
    obj["sample_to_instance_mapping"] = "UNKNOWN"
    obj["reference_length_hard_fail"] = data["assembly_length_rule"]["hard_fail_id"]
    return obj


def body_payload(obj):
    verts = [[round(float(v.co[i]), 6) for i in range(3)] for v in obj.data.vertices]
    faces = [list(poly.vertices) for poly in obj.data.polygons]
    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]
    body = {
        "name": obj.name,
        "vertex_count": len(verts),
        "face_count": len(faces),
        "local_transform": {
            "location": [float(v) for v in obj.location],
            "rotation": [float(v) for v in obj.rotation_euler],
            "scale": [float(v) for v in obj.scale],
        },
        "local_bbox_mm": {
            "min": mins,
            "max": maxs,
            "dimensions": [round(maxs[i]-mins[i], 6) for i in range(3)]
        },
        "primitive": "closed_rectangular_bounded_outer_envelope_reference",
        "unsupported_detail_count": 0,
        "geometry_vertices_mm": verts,
        "geometry_faces": faces,
    }
    return body


def setup_scene():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    scene.world.use_nodes = True
    bg = next(node for node in scene.world.node_tree.nodes if node.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (0.88,0.88,0.88,1)
    bg.inputs["Strength"].default_value = 1
    scene.view_settings.look = "AgX - Medium High Contrast"
    return scene


def emissive_material(name, shade):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (shade,shade,shade,1)
    out = nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(emission.outputs[0], out.inputs["Surface"])
    return mat


def camera(target, position, scale):
    data = bpy.data.cameras.new("T021_CAMERA")
    cam = bpy.data.objects.new("T021_CAMERA", data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    data.type = "ORTHO"
    data.clip_end = 100000
    data.ortho_scale = scale
    cam.location = position
    cam.rotation_euler = (Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
    return cam


def render_model_views(obj, values, review_dir):
    review_dir.mkdir(parents=True, exist_ok=True)
    scene = setup_scene()
    mat = emissive_material("T021_REVIEW_BODY", 0.58)
    obj.data.materials.append(mat)
    length, width, height = (float(values[key]["value"]) for key in GEOMETRY_KEYS)
    extent = max(length,width,height)
    target=(0,0,height/2)
    cam=camera(target,(0,-extent*3,height/2),extent*1.5)
    views={
        "FRONT":((0,-extent*3,height/2),max(length,height)*1.4),
        "SIDE":((extent*3,0,height/2),max(width,height)*1.5),
        "TOP":((0,0,extent*3),max(length,width)*1.4),
        "AXON":((extent*2,-extent*2.4,extent*1.9),extent*1.8),
    }
    for name,(position,scale) in views.items():
        cam.location=position
        cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
        cam.data.ortho_scale=scale
        scene.render.resolution_x=1200
        scene.render.resolution_y=900
        scene.render.filepath=str(review_dir/(name+".png"))
        bpy.ops.render.render(write_still=True)


def render_text_page(path, title, lines):
    clear_scene()
    scene=setup_scene()
    scene.render.resolution_x=1200
    scene.render.resolution_y=900
    dark=emissive_material("T021_TEXT",0.08)
    for i,line in enumerate([title]+lines):
        curve=bpy.data.curves.new("TXT_"+str(i), type="FONT")
        curve.body=line
        curve.align_x="LEFT"
        curve.align_y="CENTER"
        curve.size=0.42 if i==0 else 0.30
        obj=bpy.data.objects.new("TXT_"+str(i), curve)
        bpy.context.scene.collection.objects.link(obj)
        obj.data.materials.append(dark)
        obj.location=(-7.3, 5.4-i*1.15, 0)
    cam=camera((0,0,0),(0,0,20),17.5)
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)


def render_review(obj, data, values, review_dir):
    render_model_views(obj, values, review_dir)
    p={k:v["value"] for k,v in values.items()}
    render_text_page(
        review_dir/"DIMENSION_PARAMETER_SUMMARY.png",
        "T-021 FOUR CHUANFU / DIMENSION PARAMETER SUMMARY",
        [
            "Observed mean section width: %.1f mm" % p["width_mm"],
            "Observed mean thickness: %.1f mm" % p["thickness_mm"],
            "Canonical reference length: %.1f mm / NON-HISTORICAL" % p["canonical_reference_length_mm"],
            "Historical full length: UNKNOWN / null",
            "Sample A: 413 x 295 mm",
            "Sample B: 440 x 309 mm",
            "Sample-to-east/west mapping: UNKNOWN",
            "Report 28 fen x 20 fen: metadata only / geometry use 0",
        ],
    )
    render_text_page(
        review_dir/"EVIDENCE_UNCERTAINTY_SUMMARY.png",
        "T-021 FOUR CHUANFU / EVIDENCE + UNCERTAINTY",
        [
            "Source: SRC-ZG-WF-001 / PDF p82 / printed p67 / table 2-39",
            "Physical instances: 2 / east seam 1 / west seam 1",
            "Geometry: bounded outer envelope only",
            "No mortise, tenon, slot, camber or end-profile claim",
            "Historical full length remains UNKNOWN",
            "1000 mm is engineering reference only",
            "Assembly support coordinates remain ASSEMBLY_OWNED / UNKNOWN",
            "HIS-002 individual originality remains UNKNOWN",
        ],
    )


def build(params_path, asset_path, semantic_path, review_dir=None):
    data=json.loads(Path(params_path).read_text())
    values=param_map(data)
    clear_scene()
    setup_scene()
    obj=make_mesh(data, values)
    asset_path=Path(asset_path)
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset_path), check_existing=False)
    body=body_payload(obj)
    semantic={
        "task":"T-021",
        "component_id":data["component_id"],
        "master_id":data["master_id"],
        "master_version":data["master_version"],
        "blender_version":bpy.app.version_string,
        "geometry_mode":data["geometry_mode"],
        "geometry_lod":data["geometry_lod"],
        "geometry_semantics":data["geometry_semantics"],
        "resolved_parameters":{k:v["value"] for k,v in values.items()},
        "parameter_semantics":values,
        "historical_state":data["historical_state"],
        "known_unknowns":data["known_unknowns"],
        "originality_status":data["originality_status"],
        "sample_to_instance_mapping":data["sample_to_instance_mapping"],
        "measured_section_samples_mm":data["measured_section_samples_mm"],
        "report_design_analysis":data["report_design_analysis"],
        "interface_contract":data["interface_contract"],
        "assembly_length_rule":data["assembly_length_rule"],
        "unsupported_geometry":data["unsupported_geometry"],
        "body":body,
        "semantic_geometry_signature":stable_signature({"vertices":body["geometry_vertices_mm"],"faces":body["geometry_faces"]}),
        "canonical_asset_path":str(asset_path),
        "canonical_blend_sha256":sha256(asset_path),
    }
    Path(semantic_path).parent.mkdir(parents=True, exist_ok=True)
    Path(semantic_path).write_text(json.dumps(semantic,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    if review_dir:
        render_review(obj,data,values,Path(review_dir))
    print("FOUR_CHUANFU_BUILD_OK", semantic["semantic_geometry_signature"])


def inspect(expected_path, asset_path, output_path):
    expected=json.loads(Path(expected_path).read_text())
    _, body_name=names()
    obj=bpy.data.objects.get(body_name)
    assert obj is not None and obj.type=="MESH"
    actual=body_payload(obj)
    assert actual==expected["body"]
    assert obj.get("component_id")==expected["component_id"]
    assert obj.get("master_id")==expected["master_id"]
    assert obj.get("historical_full_length_state")=="UNKNOWN_NULL_DO_NOT_LOCK"
    assert obj.get("sample_to_instance_mapping")=="UNKNOWN"
    out={
        "status":"PASS",
        "component_id":expected["component_id"],
        "master_id":expected["master_id"],
        "body":actual,
        "semantic_geometry_signature":stable_signature({"vertices":actual["geometry_vertices_mm"],"faces":actual["geometry_faces"]}),
        "blend_sha256":sha256(asset_path),
        "historical_full_length_mm":None,
    }
    Path(output_path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("FOUR_CHUANFU_REOPEN_OK")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode",choices=("build","inspect"),required=True)
    parser.add_argument("--params")
    parser.add_argument("--asset")
    parser.add_argument("--semantic")
    parser.add_argument("--review-dir")
    parser.add_argument("--expected")
    parser.add_argument("--output")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if args.mode=="inspect":
        inspect(args.expected,args.asset,args.output)
    else:
        build(args.params,args.asset,args.semantic,args.review_dir)


if __name__=="__main__":
    main()
