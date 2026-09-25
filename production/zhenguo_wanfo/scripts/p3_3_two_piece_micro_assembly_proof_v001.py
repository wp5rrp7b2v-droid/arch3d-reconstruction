"""P3.3 two-piece micro assembly proof: Four-Chuanfu + Tuojiao.

Validation-only proof. It does not claim Stage 2/3 completion, building coordinates,
historical endpoint geometry, or joinery.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stable_hash(value):
    payload=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def r6(x):
    return round(float(x),6)


def vec_payload(v):
    return [r6(v[i]) for i in range(3)]


def contract_inputs(contract):
    a=contract["authority"]
    four=load_json(a["four_chuanfu_params"])
    four_sem=load_json(a["four_chuanfu_semantic"])
    tuo=load_json(a["tuojiao_definition"])
    tuo_sem=load_json(a["tuojiao_semantic"])

    locked=contract["locked_identity"]
    assert four["component_id"]==locked["four_chuanfu"]["component_id"]
    assert four["master_id"]==locked["four_chuanfu"]["master_id"]
    assert four_sem["canonical_blend_sha256"]==locked["four_chuanfu"]["canonical_blend_sha256"]
    assert tuo["component_id"]==locked["tuojiao"]["component_id"]
    assert tuo["master_id"]==locked["tuojiao"]["master_id"]
    assert tuo_sem["canonical_blend_sha256"]==locked["tuojiao"]["canonical_blend_sha256"]
    assert tuo_sem["assembly_semantics"]["official_same_building_semantic"]==locked["tuojiao"]["required_official_semantic"]

    params={x["key"]:x for x in four["parameters"]}
    four_dims={
        "width_mm":float(params["width_mm"]["value"]),
        "thickness_mm":float(params["thickness_mm"]["value"]),
        "canonical_reference_length_mm":float(params["canonical_reference_length_mm"]["value"])
    }
    sec=tuo["geometry_contract"]["section_envelope_mm"]
    tuo_dims={
        "width_mm":float(sec["width"]),
        "thickness_mm":float(sec["thickness"]),
        "canonical_reference_length_mm":float(tuo["geometry_contract"]["canonical_reference_length_mm"])
    }
    return four,four_sem,tuo,tuo_sem,four_dims,tuo_dims


def solve_upper_center_z(lower_x,lower_z,upper_x,beam_bottom_z,thickness):
    dx=float(upper_x)-float(lower_x)
    if abs(dx)<1e-9:
        raise ValueError("proof fixture requires non-zero horizontal offset")
    z=float(beam_bottom_z)
    for _ in range(100):
        dz=z-float(lower_z)
        length=math.sqrt(dx*dx+dz*dz)
        z2=float(beam_bottom_z)-(float(thickness)/2.0)*abs(dx/length)
        if abs(z2-z)<1e-10:
            return z2
        z=z2
    return z


def clear_scene():
    import bpy
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj,do_unlink=True)
    for mesh in list(bpy.data.meshes):
        if mesh.users==0:
            bpy.data.meshes.remove(mesh)


def make_local_box(name,length,width,thickness):
    import bpy
    L=float(length); W=float(width); H=float(thickness)
    verts=[
        (-L/2,-W/2,0),(L/2,-W/2,0),(L/2,W/2,0),(-L/2,W/2,0),
        (-L/2,-W/2,H),(L/2,-W/2,H),(L/2,W/2,H),(-L/2,W/2,H)
    ]
    faces=[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def place_centerline_member(obj,p0,p1,thickness):
    from mathutils import Matrix,Vector
    p0=Vector(p0); p1=Vector(p1)
    xhat=(p1-p0).normalized()
    yseed=Vector((0.0,1.0,0.0))
    if abs(xhat.dot(yseed))>0.999:
        raise ValueError("proof fixture axis degeneracy")
    zhat=xhat.cross(yseed).normalized()
    yhat=zhat.cross(xhat).normalized()
    R=Matrix((
        (xhat.x,yhat.x,zhat.x,0.0),
        (xhat.y,yhat.y,zhat.y,0.0),
        (xhat.z,yhat.z,zhat.z,0.0),
        (0.0,0.0,0.0,1.0)
    ))
    center=(p0+p1)/2.0
    origin_world=center-zhat*(float(thickness)/2.0)
    obj.matrix_world=Matrix.Translation(origin_world) @ R
    return vec_payload(xhat),vec_payload(yhat),vec_payload(zhat)


def world_vertices(obj):
    return [[r6((obj.matrix_world @ v.co)[i]) for i in range(3)] for v in obj.data.vertices]


def material(name,color):
    import bpy
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value=(*color,1.0)
        bsdf.inputs["Roughness"].default_value=0.55
    return m


def add_render_setup(target,render_path):
    import bpy
    from mathutils import Vector
    scene=bpy.context.scene
    scene.unit_settings.system="METRIC"
    scene.unit_settings.scale_length=0.001
    scene.unit_settings.length_unit="MILLIMETERS"
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.resolution_x=1400
    scene.render.resolution_y=1000
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.world.color=(0.05,0.05,0.05)

    data=bpy.data.cameras.new("PROOF_CAMERA")
    cam=bpy.data.objects.new("PROOF_CAMERA",data)
    scene.collection.objects.link(cam)
    scene.camera=cam
    data.type="ORTHO"
    data.ortho_scale=3600.0
    cam.location=(500.0,-5200.0,-250.0)
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()

    ldata=bpy.data.lights.new("PROOF_KEY","AREA")
    ldata.energy=1800.0
    ldata.shape="DISK"
    ldata.size=2600.0
    light=bpy.data.objects.new("PROOF_KEY",ldata)
    scene.collection.objects.link(light)
    light.location=(-700.0,-2200.0,2800.0)
    light.rotation_euler=(Vector(target)-light.location).to_track_quat("-Z","Y").to_euler()

    scene.render.filepath=str(render_path)
    bpy.ops.render.render(write_still=True)


def build(contract_path,fixture_id,asset,semantic,render_path):
    import bpy
    from mathutils import Vector

    contract=load_json(contract_path)
    four,four_sem,tuo,tuo_sem,four_dims,tuo_dims=contract_inputs(contract)
    fixture_cfg=next(x for x in contract["engineering_fixture"]["fixtures"] if x["fixture_id"]==fixture_id)
    ef=contract["engineering_fixture"]
    beam_cfg=ef["four_chuanfu"]
    contact=ef["support_contact"]
    tol=float(ef["tolerance_mm"])

    beam_L=float(beam_cfg["derived_instance_length_mm"])
    beam_W=four_dims["width_mm"]
    beam_H=four_dims["thickness_mm"]
    beam_cx=float(beam_cfg["center_x_mm"])
    beam_cy=float(beam_cfg["center_y_mm"])
    beam_bottom=float(beam_cfg["bottom_z_mm"])
    beam_p0=(beam_cx-beam_L/2.0,beam_cy,beam_bottom+beam_H/2.0)
    beam_p1=(beam_cx+beam_L/2.0,beam_cy,beam_bottom+beam_H/2.0)

    lower=[float(x) for x in fixture_cfg["p_lower_centerline_mm"]]
    upper_x=float(contact["beam_support_x_mm"])
    upper_y=float(contact["beam_support_y_mm"])
    upper_z=solve_upper_center_z(lower[0],lower[2],upper_x,float(contact["beam_underside_z_mm"]),tuo_dims["thickness_mm"])
    upper=[upper_x,upper_y,upper_z]
    support_L=math.sqrt(sum((upper[i]-lower[i])**2 for i in range(3)))

    clear_scene()
    beam=make_local_box("PROOF__FOUR_CHUANFU",beam_L,beam_W,beam_H)
    support=make_local_box("PROOF__TUOJIAO",support_L,tuo_dims["width_mm"],tuo_dims["thickness_mm"])
    beam_axes=place_centerline_member(beam,beam_p0,beam_p1,beam_H)
    support_axes=place_centerline_member(support,lower,upper,tuo_dims["thickness_mm"])

    beam["component_id"]=four["component_id"]
    beam["master_id"]=four["master_id"]
    beam["fixture_classification"]=ef["classification"]
    beam["manual_transform_used"]=False
    support["component_id"]=tuo["component_id"]
    support["master_id"]=tuo["master_id"]
    support["fixture_classification"]=ef["classification"]
    support["manual_transform_used"]=False
    support["assembly_semantic"]=tuo_sem["assembly_semantics"]["official_same_building_semantic"]

    beam.data.materials.append(material("MAT_FOUR_CHUANFU",(0.52,0.30,0.15)))
    support.data.materials.append(material("MAT_TUOJIAO",(0.25,0.13,0.07)))

    bverts=world_vertices(beam)
    sverts=world_vertices(support)
    max_support_z=max(v[2] for v in sverts)
    min_support_z=min(v[2] for v in sverts)
    beam_minx=min(v[0] for v in bverts); beam_maxx=max(v[0] for v in bverts)
    beam_miny=min(v[1] for v in bverts); beam_maxy=max(v[1] for v in bverts)
    tangent=[v for v in sverts if abs(v[2]-beam_bottom)<=tol]
    contact_inside=bool(tangent) and all(
        beam_minx-tol<=v[0]<=beam_maxx+tol and beam_miny-tol<=v[1]<=beam_maxy+tol
        for v in tangent
    )
    contact_tangent=abs(max_support_z-beam_bottom)<=tol
    no_penetration=max_support_z<=beam_bottom+tol

    Path(render_path).parent.mkdir(parents=True,exist_ok=True)
    add_render_setup((250.0,0.0,-450.0),render_path)
    Path(asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(asset))

    source_hashes={
        "four_chuanfu_params_sha256":sha256_file(contract["authority"]["four_chuanfu_params"]),
        "four_chuanfu_semantic_sha256":sha256_file(contract["authority"]["four_chuanfu_semantic"]),
        "tuojiao_definition_sha256":sha256_file(contract["authority"]["tuojiao_definition"]),
        "tuojiao_semantic_sha256":sha256_file(contract["authority"]["tuojiao_semantic"])
    }

    beam_payload={
        "component_id":four["component_id"],
        "master_id":four["master_id"],
        "section_mm":[beam_W,beam_H],
        "derived_instance_length_mm":r6(beam_L),
        "canonical_reference_length_mm":four_dims["canonical_reference_length_mm"],
        "p0_centerline_mm":vec_payload(Vector(beam_p0)),
        "p1_centerline_mm":vec_payload(Vector(beam_p1)),
        "axes":{"x":beam_axes[0],"y":beam_axes[1],"z":beam_axes[2]},
        "world_vertices_mm":bverts
    }
    support_payload={
        "component_id":tuo["component_id"],
        "master_id":tuo["master_id"],
        "section_mm":[tuo_dims["width_mm"],tuo_dims["thickness_mm"]],
        "derived_instance_length_mm":r6(support_L),
        "canonical_reference_length_mm":tuo_dims["canonical_reference_length_mm"],
        "p_lower_centerline_mm":[r6(x) for x in lower],
        "p_upper_centerline_mm":[r6(x) for x in upper],
        "derived_direction":support_axes[0],
        "axes":{"x":support_axes[0],"y":support_axes[1],"z":support_axes[2]},
        "world_vertices_mm":sverts,
        "official_same_building_semantic":tuo_sem["assembly_semantics"]["official_same_building_semantic"]
    }
    beam_sig=stable_hash(beam_payload["world_vertices_mm"])
    support_sig=stable_hash(support_payload["world_vertices_mm"])
    geometry_sig=stable_hash({"beam":beam_payload["world_vertices_mm"],"support":support_payload["world_vertices_mm"]})
    local_checks={
        "contact_tangent":contact_tangent,
        "no_volume_penetration":no_penetration,
        "contact_inside_beam_footprint":contact_inside,
        "contact_vertex_count":len(tangent),
        "max_support_z_mm":r6(max_support_z),
        "min_support_z_mm":r6(min_support_z),
        "beam_bottom_z_mm":r6(beam_bottom),
        "all_local_checks_pass":bool(contact_tangent and no_penetration and contact_inside)
    }
    out={
        "schema_version":"P3_3_MICRO_ASSEMBLY_SEMANTIC_1.0",
        "proof_id":contract["proof_id"],
        "fixture_id":fixture_id,
        "fixture_classification":ef["classification"],
        "status":"PASS" if local_checks["all_local_checks_pass"] else "FAIL",
        "source_hashes":source_hashes,
        "historical_claim":False,
        "building_coordinate_claim":False,
        "joinery_claim":False,
        "manual_transform_used":False,
        "beam":beam_payload,
        "support":support_payload,
        "beam_geometry_signature":beam_sig,
        "support_geometry_signature":support_sig,
        "geometry_only_signature":geometry_sig,
        "local_checks":local_checks,
        "blend_sha256":sha256_file(asset)
    }
    Path(semantic).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("P3_3_2PIECE_BUILD",fixture_id,out["status"],geometry_sig)


def inspect(expected_path,output):
    import bpy
    expected=load_json(expected_path)
    beam=bpy.data.objects.get("PROOF__FOUR_CHUANFU")
    support=bpy.data.objects.get("PROOF__TUOJIAO")
    assert beam is not None and support is not None
    geom=stable_hash({"beam":world_vertices(beam),"support":world_vertices(support)})
    ok=(geom==expected["geometry_only_signature"])
    out={"status":"PASS" if ok else "FAIL","geometry_only_signature":geom,"expected_geometry_only_signature":expected["geometry_only_signature"]}
    Path(output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if not ok:
        raise SystemExit(3)
    print("P3_3_2PIECE_REOPEN_PASS",geom)


def validate(contract_path,baseline_path,mutation_path,repeat_path,reopen_path,output):
    contract=load_json(contract_path)
    b=load_json(baseline_path)
    m=load_json(mutation_path)
    r=load_json(repeat_path)
    o=load_json(reopen_path)
    checks=[]

    def add(name,cond,detail=None):
        checks.append({"name":name,"pass":bool(cond),"detail":detail})
        if not cond:
            print("FAIL",name,detail)

    add("baseline_local_pass",b["status"]=="PASS")
    add("mutation_local_pass",m["status"]=="PASS")
    add("repeat_local_pass",r["status"]=="PASS")
    add("independent_reopen_pass",o["status"]=="PASS")
    add("baseline_repeat_deterministic",b["geometry_only_signature"]==r["geometry_only_signature"])
    add("reopen_matches_baseline",o["geometry_only_signature"]==b["geometry_only_signature"])
    add("beam_geometry_preserved_under_mutation",b["beam_geometry_signature"]==m["beam_geometry_signature"])
    add("support_geometry_changes_under_mutation",b["support_geometry_signature"]!=m["support_geometry_signature"])
    add("support_length_changes",abs(b["support"]["derived_instance_length_mm"]-m["support"]["derived_instance_length_mm"])>1.0)
    add("support_orientation_changes",b["support"]["derived_direction"]!=m["support"]["derived_direction"])
    add("baseline_contact_tangent",b["local_checks"]["contact_tangent"])
    add("mutation_contact_tangent",m["local_checks"]["contact_tangent"])
    add("baseline_no_penetration",b["local_checks"]["no_volume_penetration"])
    add("mutation_no_penetration",m["local_checks"]["no_volume_penetration"])
    add("baseline_contact_in_footprint",b["local_checks"]["contact_inside_beam_footprint"])
    add("mutation_contact_in_footprint",m["local_checks"]["contact_inside_beam_footprint"])
    add("beam_reference_length_not_leaked",b["beam"]["derived_instance_length_mm"]!=b["beam"]["canonical_reference_length_mm"])
    add("support_reference_length_not_leaked_baseline",abs(b["support"]["derived_instance_length_mm"]-b["support"]["canonical_reference_length_mm"])>1.0)
    add("support_reference_length_not_leaked_mutation",abs(m["support"]["derived_instance_length_mm"]-m["support"]["canonical_reference_length_mm"])>1.0)
    required=contract["locked_identity"]["tuojiao"]["required_official_semantic"]
    add("official_support_semantic_retained",b["support"]["official_same_building_semantic"]==required and m["support"]["official_same_building_semantic"]==required)
    add("no_manual_transform",not b["manual_transform_used"] and not m["manual_transform_used"])
    add("not_building_coordinates",not b["building_coordinate_claim"] and not m["building_coordinate_claim"])
    add("not_historical_claim",not b["historical_claim"] and not m["historical_claim"])
    add("no_joinery_claim",not b["joinery_claim"] and not m["joinery_claim"])

    passed=sum(1 for x in checks if x["pass"])
    out={
        "schema_version":"P3_3_MICRO_ASSEMBLY_VALIDATION_1.0",
        "proof_id":contract["proof_id"],
        "status":"PASS" if passed==len(checks) else "FAIL",
        "pass_count":passed,
        "total_count":len(checks),
        "checks":checks,
        "scope_result":"2-PIECE MICRO ASSEMBLY PROOF ONLY / NOT STAGE2 OR STAGE3 PASS"
    }
    Path(output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("P3_3_2PIECE_VALIDATION",out["status"],f"{passed}/{len(checks)}")
    if out["status"]!="PASS":
        raise SystemExit(4)


def parse_args():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("build","inspect","validate"))
    ap.add_argument("--contract")
    ap.add_argument("--fixture")
    ap.add_argument("--asset")
    ap.add_argument("--semantic")
    ap.add_argument("--render")
    ap.add_argument("--expected")
    ap.add_argument("--baseline")
    ap.add_argument("--mutation")
    ap.add_argument("--repeat")
    ap.add_argument("--reopen")
    ap.add_argument("--output")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)


def main():
    a=parse_args()
    if a.mode=="build":
        build(a.contract,a.fixture,a.asset,a.semantic,a.render)
    elif a.mode=="inspect":
        inspect(a.expected,a.output)
    else:
        validate(a.contract,a.baseline,a.mutation,a.repeat,a.reopen,a.output)


if __name__=="__main__":
    main()
