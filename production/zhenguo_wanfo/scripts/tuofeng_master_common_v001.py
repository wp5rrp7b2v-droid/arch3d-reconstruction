"""T-042 Tuofeng Master first-article builder / inspector."""
import argparse, hashlib, json, math, sys
from pathlib import Path

def stable(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

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
    s.render.engine="BLENDER_EEVEE_NEXT"
    s.render.resolution_percentage=100
    s.world.use_nodes=True
    bg=next(n for n in s.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.93,0.93,0.93,1)
    bg.inputs["Strength"].default_value=0.8
    return s

def material(name,color):
    import bpy
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    return m

def mesh_object(name,verts,faces,variant_id):
    import bpy
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj["variant_id"]=variant_id
    obj["component_id"]="CMP-FRAME-TUOFENG-001"
    obj["master_id"]="CMP-FRAME-TUOFENG-001_MASTER"
    obj["historical_metric_claim"]=False
    obj["building_dimension_claim"]=False
    obj["joinery_cut_count"]=0
    return obj

def box_geometry(sx,sy,z0,z1,offset=0):
    x=sx/2.0; y=sy/2.0
    verts=[(-x,-y,z0),(x,-y,z0),(x,y,z0),(-x,y,z0),
           (-x,-y,z1),(x,-y,z1),(x,y,z1),(-x,y,z1)]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    return verts,[tuple(i+offset for i in f) for f in faces]

def lower_geometry(p):
    v1,f1=box_geometry(p["base_span_mm"],p["base_depth_mm"],0,p["base_height_mm"],0)
    v2,f2=box_geometry(p["seat_span_mm"],p["seat_depth_mm"],p["base_height_mm"],p["base_height_mm"]+p["seat_height_mm"],8)
    return v1+v2,f1+f2

def upper_geometry(p,profile):
    span=float(p["base_span_mm"]); depth=float(p["depth_mm"]); height=float(p["height_mm"])
    pts=[(float(x)*span,float(z)/0.32*height) for x,z in profile]
    y=depth/2.0
    verts=[(x,-y,z) for x,z in pts]+[(x,y,z) for x,z in pts]
    n=len(pts)
    faces=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]
    for i in range(n):
        j=(i+1)%n
        faces.append((i,j,n+j,n+i))
    return verts,faces

def payload(obj):
    verts=[[round(float(v.co.x),6),round(float(v.co.y),6),round(float(v.co.z),6)] for v in obj.data.vertices]
    faces=[list(p.vertices) for p in obj.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
    g={"verts":verts,"faces":faces}
    return {
      "variant_id":obj["variant_id"],
      "vertex_count":len(verts),
      "face_count":len(faces),
      "bbox_mm":{"min":mins,"max":maxs,"dimensions":[round(maxs[i]-mins[i],6) for i in range(3)]},
      "geometry_signature":stable(g),
      "historical_metric_claim":bool(obj["historical_metric_claim"]),
      "building_dimension_claim":bool(obj["building_dimension_claim"]),
      "joinery_cut_count":int(obj["joinery_cut_count"])
    }

def look_at(camera,target):
    from mathutils import Vector
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat("-Z","Y").to_euler()

def add_camera():
    import bpy
    data=bpy.data.cameras.new("T042_CAMERA")
    cam=bpy.data.objects.new("T042_CAMERA",data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera=cam
    data.type="ORTHO"
    data.clip_end=100000
    return cam

def add_lights():
    import bpy
    data=bpy.data.lights.new("KEY","AREA")
    data.energy=900
    data.shape="DISK"
    data.size=3000
    obj=bpy.data.objects.new("KEY",data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location=(2000,-2500,2500)
    look_at(obj,(0,0,200))
    data2=bpy.data.lights.new("FILL","AREA")
    data2.energy=500
    data2.size=2500
    obj2=bpy.data.objects.new("FILL",data2)
    bpy.context.scene.collection.objects.link(obj2)
    obj2.location=(-1800,1800,1600)
    look_at(obj2,(0,0,200))

def render_variant(obj,other,review_dir,prefix):
    import bpy
    review=Path(review_dir); review.mkdir(parents=True,exist_ok=True)
    obj.hide_render=False; other.hide_render=True
    dims=obj.dimensions
    ext=max(float(dims.x),float(dims.y),float(dims.z),1.0)
    target=(0,0,float(dims.z)/2.0)
    cam=bpy.context.scene.camera
    s=bpy.context.scene
    s.render.resolution_x=1000; s.render.resolution_y=700
    views={
      "PROFILE":((0,-ext*3,float(dims.z)/2.0),max(float(dims.x),float(dims.z))*1.35),
      "AXON":((ext*2.2,-ext*2.4,ext*1.7),ext*1.7),
      "TOP":((0,0,ext*3),max(float(dims.x),float(dims.y))*1.35)
    }
    for name,(pos,scale) in views.items():
        cam.location=pos
        look_at(cam,target)
        cam.data.ortho_scale=scale
        s.render.filepath=str(review/f"{prefix}_{name}.png")
        bpy.ops.render.render(write_still=True)
    other.hide_render=False

def build(definition_path,asset,semantic,review_dir,fixture_set):
    import bpy
    d=load(definition_path)
    clear_scene(); setup_scene(); add_camera(); add_lights()
    fx=d["canonical_first_article_fixture"] if fixture_set=="A" else d["mutation_fixture"]
    lv,lf=lower_geometry(fx["LOWER_SUPPORT"])
    uv,uf=upper_geometry(fx["UPPER_RIDGE_SUPPORT"],d["upper_normalized_profile_xz"])
    lower=mesh_object("TUOFENG_LOWER_SUPPORT",lv,lf,"LOWER_SUPPORT")
    upper=mesh_object("TUOFENG_UPPER_RIDGE_SUPPORT",uv,uf,"UPPER_RIDGE_SUPPORT")
    lower.data.materials.append(material("LOWER_MAT",(0.45,0.25,0.12)))
    upper.data.materials.append(material("UPPER_MAT",(0.38,0.20,0.10)))
    if review_dir:
        render_variant(lower,upper,review_dir,"LOWER_SUPPORT")
        render_variant(upper,lower,review_dir,"UPPER_RIDGE_SUPPORT")
    Path(asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(asset).resolve()))
    bodies=[payload(lower),payload(upper)]
    out={
      "status":"BUILT",
      "task_id":d["task_id"],
      "component_id":d["component_id"],
      "master_id":d["master_id"],
      "master_version":d["master_version"],
      "fixture_set":fixture_set,
      "fixture_classification":fx["classification"],
      "fixture_historical_claim":fx["historical_claim"],
      "fixture_building_dimension_claim":fx["building_dimension_claim"],
      "master_family_count":1,
      "role_variant_count":2,
      "role_variants":["LOWER_SUPPORT","UPPER_RIDGE_SUPPORT"],
      "historical_dimensions":"UNKNOWN",
      "exact_historical_profile":"UNKNOWN",
      "historical_joinery":"UNKNOWN / DEFERRED",
      "assembly_metric_envelope":"ASSEMBLY_OWNED",
      "bodies":bodies,
      "family_signature":stable({b["variant_id"]:b["geometry_signature"] for b in bodies}),
      "definition_sha256":file_sha(definition_path),
      "blender_version":bpy.app.version_string
    }
    Path(semantic).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    out["blend_sha256"]=file_sha(asset)
    Path(semantic).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T042_BUILD_PASS",fixture_set,out["family_signature"])

def inspect(asset,expected,output):
    import bpy
    exp=load(expected)
    found=[]
    for obj in bpy.data.objects:
        if obj.type=="MESH" and obj.get("variant_id") in {"LOWER_SUPPORT","UPPER_RIDGE_SUPPORT"}:
            found.append(payload(obj))
    got={x["variant_id"]:x["geometry_signature"] for x in found}
    want={x["variant_id"]:x["geometry_signature"] for x in exp["bodies"]}
    out={"status":"PASS" if got==want else "FAIL","object_count":len(found),"geometry_signatures":got,"expected":want}
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if out["status"]!="PASS":
        raise SystemExit("REOPEN_SIGNATURE_MISMATCH")
    print("T042_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","inspect"),required=True)
    ap.add_argument("--definition")
    ap.add_argument("--asset")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--fixture-set",choices=("A","B"),default="A")
    ap.add_argument("--expected")
    ap.add_argument("--output")
    a=ap.parse_args()
    if a.mode=="build":
        build(a.definition,a.asset,a.semantic,a.review_dir,a.fixture_set)
    else:
        inspect(a.asset,a.expected,a.output)

if __name__=="__main__":
    main()
