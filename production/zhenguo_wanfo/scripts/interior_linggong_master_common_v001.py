"""T-043 Interior-frame Linggong Master first-article builder / inspector."""
import argparse, hashlib, json, sys
from pathlib import Path

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def file_sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def clear_scene():
    import bpy
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for c in list(bpy.data.collections):
        if c != bpy.context.scene.collection:
            bpy.data.collections.remove(c)

def setup_scene():
    import bpy
    s=bpy.context.scene
    s.unit_settings.system="METRIC"
    s.unit_settings.scale_length=0.001
    s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_WORKBENCH"
    s.render.resolution_percentage=100
    s.world.use_nodes=True
    bg=next(n for n in s.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.94,0.94,0.94,1)
    bg.inputs["Strength"].default_value=0.8
    return s

def material(name,color):
    import bpy
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    return m

def box_geometry(sx,sy,z0,z1):
    x=sx/2.0; y=sy/2.0
    verts=[(-x,-y,z0),(x,-y,z0),(x,y,z0),(-x,y,z0),
           (-x,-y,z1),(x,-y,z1),(x,y,z1),(-x,y,z1)]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    return verts,faces

def mesh_obj(name,zone,verts,faces):
    import bpy
    me=bpy.data.meshes.new(name+"_MESH")
    me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me)
    bpy.context.scene.collection.objects.link(ob)
    ob["component_id"]="CMP-FRAME-LINGGONG-INTERIOR-001"
    ob["master_id"]="CMP-FRAME-LINGGONG-INTERIOR-001_MASTER"
    ob["role_variant"]="LOWER_PINGLIANG_SUPPORT"
    ob["zone_id"]=zone
    ob["historical_metric_claim"]=False
    ob["building_dimension_claim"]=False
    ob["outer_eaves_profile_used"]=False
    ob["joinery_cut_count"]=0
    return ob

def obj_payload(ob):
    verts=[[round(float(v.co.x),6),round(float(v.co.y),6),round(float(v.co.z),6)] for v in ob.data.vertices]
    faces=[list(p.vertices) for p in ob.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
    return {
      "zone_id":ob["zone_id"],
      "vertex_count":len(verts),
      "face_count":len(faces),
      "bbox_mm":{"min":mins,"max":maxs,"dimensions":[round(maxs[i]-mins[i],6) for i in range(3)]},
      "geometry_signature":stable({"verts":verts,"faces":faces}),
      "historical_metric_claim":bool(ob["historical_metric_claim"]),
      "building_dimension_claim":bool(ob["building_dimension_claim"]),
      "outer_eaves_profile_used":bool(ob["outer_eaves_profile_used"]),
      "joinery_cut_count":int(ob["joinery_cut_count"])
    }

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def add_camera_light():
    import bpy
    cd=bpy.data.cameras.new("T043_CAMERA")
    cam=bpy.data.objects.new("T043_CAMERA",cd)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera=cam
    cd.type="ORTHO"; cd.clip_end=100000
    ld=bpy.data.lights.new("KEY","AREA"); ld.energy=900; ld.size=3000
    lo=bpy.data.objects.new("KEY",ld); bpy.context.scene.collection.objects.link(lo)
    lo.location=(2000,-2500,2200); look_at(lo,(0,0,150))
    return cam

def render(objects,review_dir,prefix):
    import bpy
    review=Path(review_dir); review.mkdir(parents=True,exist_ok=True)
    ext=max(max(float(o.dimensions.x),float(o.dimensions.y),float(o.dimensions.z)) for o in objects)
    total_h=max(float(v.co.z) for o in objects for v in o.data.vertices)
    cam=bpy.context.scene.camera
    s=bpy.context.scene
    s.render.resolution_x=800; s.render.resolution_y=600
    target=(0,0,total_h/2.0)
    views={
      "PROFILE":((0,-ext*3,total_h/2.0),max(ext,total_h)*1.45),
      "AXON":((ext*2.2,-ext*2.3,ext*1.65),ext*1.75)
    }
    for name,(pos,scale) in views.items():
        cam.location=pos; look_at(cam,target); cam.data.ortho_scale=scale
        s.render.filepath=str(review/f"{prefix}_{name}.png")
        bpy.ops.render.render(write_still=True)

def validate_params(fx):
    vals=["body_length","body_depth","body_height","seat_length","seat_depth","seat_height"]
    if any(float(fx[k])<=0 for k in vals):
        raise ValueError("NON_POSITIVE_FIXTURE_VALUE")
    if float(fx["seat_length"])>float(fx["body_length"]):
        raise ValueError("SEAT_EXCEEDS_BODY")
    if float(fx["seat_depth"])>float(fx["body_depth"]):
        raise ValueError("SEAT_EXCEEDS_BODY")

def build(definition_path,asset,semantic,review_dir,fixture_set):
    import bpy
    d=load(definition_path)
    fx=d["canonical_first_article_fixture"] if fixture_set=="A" else d["mutation_fixture"]
    validate_params(fx)
    clear_scene(); setup_scene(); add_camera_light()

    body_v,body_f=box_geometry(float(fx["body_length"]),float(fx["body_depth"]),0,float(fx["body_height"]))
    seat_v,seat_f=box_geometry(float(fx["seat_length"]),float(fx["seat_depth"]),float(fx["body_height"]),float(fx["body_height"])+float(fx["seat_height"]))
    body=mesh_obj("INTERIOR_LINGGONG__BODY_ZONE","BODY_ZONE",body_v,body_f)
    seat=mesh_obj("INTERIOR_LINGGONG__UPPER_BEARING_ZONE","UPPER_BEARING_ZONE",seat_v,seat_f)
    body.data.materials.append(material("BODY_MAT",(0.43,0.23,0.11)))
    seat.data.materials.append(material("SEAT_MAT",(0.53,0.30,0.14)))

    if review_dir:
        render([body,seat],review_dir,f"FIXTURE_{fixture_set}")

    Path(asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(asset).resolve()))
    zones=[obj_payload(body),obj_payload(seat)]
    geometry_inputs={k:fx[k] for k in ["body_length","body_depth","body_height","seat_length","seat_depth","seat_height"]}
    out={
      "status":"BUILT",
      "task_id":"T-043",
      "component_id":d["component_id"],
      "master_id":d["master_id"],
      "master_version":d["master_version"],
      "master_family_count":1,
      "role_variant_count":1,
      "role_variant":"LOWER_PINGLIANG_SUPPORT",
      "geometry_strategy":d["geometry_strategy"],
      "fixture_set":fixture_set,
      "fixture_classification":fx["classification"],
      "fixture_historical_claim":fx["historical_claim"],
      "fixture_building_dimension_claim":fx["building_dimension_claim"],
      "geometry_inputs":geometry_inputs,
      "zones":zones,
      "geometry_signature":stable({z["zone_id"]:z["geometry_signature"] for z in zones}),
      "historical_dimensions":"UNKNOWN",
      "historical_profile":"UNKNOWN",
      "historical_joinery":"UNKNOWN / DEFERRED",
      "outer_eaves_geometry_inherited":False,
      "outer_eaves_profile_used":False,
      "joinery_cut_count":0,
      "building_metric_envelope":"ASSEMBLY_OWNED",
      "definition_sha256":file_sha(definition_path),
      "blender_version":bpy.app.version_string
    }
    Path(semantic).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    out["blend_sha256"]=file_sha(asset)
    Path(semantic).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T043_BUILD_PASS",fixture_set,out["geometry_signature"])

def inspect(expected,output):
    import bpy
    exp=load(expected)
    objs=[o for o in bpy.data.objects if o.type=="MESH" and o.get("master_id")=="CMP-FRAME-LINGGONG-INTERIOR-001_MASTER"]
    zones=[obj_payload(o) for o in sorted(objs,key=lambda x:x.get("zone_id",""))]
    got={z["zone_id"]:z["geometry_signature"] for z in zones}
    want={z["zone_id"]:z["geometry_signature"] for z in exp["zones"]}
    out={"status":"PASS" if got==want else "FAIL","object_count":len(zones),"geometry_signatures":got,"expected":want}
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if out["status"]!="PASS":
        raise SystemExit("REOPEN_SIGNATURE_MISMATCH")
    print("T043_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("build","inspect"))
    ap.add_argument("--definition")
    ap.add_argument("--asset")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--fixture-set",choices=("A","B"),default="A")
    ap.add_argument("--expected")
    ap.add_argument("--output")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    a=ap.parse_args(argv)
    if a.mode=="build":
        build(a.definition,a.asset,a.semantic,a.review_dir,a.fixture_set)
    else:
        inspect(a.expected,a.output)

if __name__=="__main__":
    main()
