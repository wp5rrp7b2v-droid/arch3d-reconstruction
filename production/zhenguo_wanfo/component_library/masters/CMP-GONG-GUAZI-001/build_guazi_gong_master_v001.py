"""T-037 瓜子栱 family first-article builder / inspector.

Builds one Stage1 Master family containing LARGE and SMALL canonical variants.
The 2D profile is a deterministic SOURCE_DERIVED_PROFILE from the locked Definition.
Exact historical curve dimensions remain UNRESOLVED.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stable(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")).hexdigest()

def mesh_payload(length, width, thickness, normalized_points):
    pts=[(float(x)*length, float(z)*thickness) for x,z in normalized_points]
    n=len(pts); y0=-width/2.0; y1=width/2.0
    verts=[[x,y0,z] for x,z in pts] + [[x,y1,z] for x,z in pts]
    # caps + side quads; Blender n-gons are intentional and deterministic.
    faces=[list(range(n-1,-1,-1)), list(range(n,2*n))]
    for i in range(n):
        j=(i+1)%n
        faces.append([i,j,n+j,n+i])
    return verts,faces

def bbox(verts):
    xs=[v[0] for v in verts]; ys=[v[1] for v in verts]; zs=[v[2] for v in verts]
    return {
      "min":[min(xs),min(ys),min(zs)],
      "max":[max(xs),max(ys),max(zs)],
      "dimensions":[max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)]
    }

def setup_material(bpy,name,rgba):
    m=bpy.data.materials.new(name)
    m.diffuse_color=rgba
    m.roughness=0.58
    return m

def look_at(obj,target):
    from mathutils import Vector
    direction=Vector(target)-obj.location
    obj.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()

def setup_scene(bpy):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.resolution_x=900; scene.render.resolution_y=650; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.film_transparent=False
    scene.world.color=(0.94,0.94,0.94)
    # Groundless studio lighting, stable in headless mode.
    bpy.ops.object.light_add(type="AREA", location=(0,-700,900))
    key=bpy.context.object; key.data.energy=900; key.data.shape="DISK"; key.data.size=1000
    look_at(key,(0,0,0))
    bpy.ops.object.light_add(type="AREA", location=(700,400,500))
    fill=bpy.context.object; fill.data.energy=650; fill.data.size=800
    look_at(fill,(0,0,0))
    bpy.ops.object.camera_add(location=(0,-1600,0))
    cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.ortho_scale=1250
    look_at(cam,(0,0,0)); scene.camera=cam
    return scene,cam

def make_object(bpy,name,verts,faces,mat):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj["t037_variant"]=name
    return obj

def render_variant(bpy,scene,cam,objects,which,path,view):
    for key,obj in objects.items():
        obj.hide_render=(key!=which)
    if view=="FRONT":
        cam.location=(0,-1600,0); cam.data.ortho_scale=1200; look_at(cam,(0,0,0))
    else:
        cam.location=(1100,-1100,800); cam.data.ortho_scale=1350; look_at(cam,(0,0,0))
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def render_overlay(bpy,scene,cam,objects,path):
    for obj in objects.values(): obj.hide_render=False
    cam.location=(0,-1600,0); cam.data.ortho_scale=1200; look_at(cam,(0,0,0))
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def semantic_from_def(d, variant_payloads, blender_version):
    variants={}
    for v,p in variant_payloads.items():
        payload={
          "variant_id":v,
          "component_name_zh":p["component_name_zh"],
          "count":p["count"],
          "resolved_dimensions_mm":{"length":p["length"],"width":p["width"],"thickness":p["thickness"]},
          "local_bbox_mm":p["bbox"],
          "geometry_vertices_mm":p["verts"],
          "geometry_faces":p["faces"],
          "unsupported_detail_count":0,
          "joinery_cut_count":0,
          "local_transform":{"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]}
        }
        payload["semantic_geometry_signature"]=stable({
          "variant_id":v,
          "dimensions":payload["resolved_dimensions_mm"],
          "vertices":payload["geometry_vertices_mm"],
          "faces":payload["geometry_faces"]
        })
        variants[v]=payload
    return {
      "schema_version":"GUAZI_GONG_MASTER_SEMANTIC_V001",
      "task_id":"T-037",
      "component_family_id":d["component_family_id"],
      "master_id":d["master_id"],
      "master_version":d["master_version"],
      "master_family_count":1,
      "geometry_variant_count":2,
      "physical_instance_count":44,
      "profile_contract":d["profile_contract"],
      "evidence_semantics":d["evidence_semantics"],
      "deferred_geometry":d["deferred_geometry"],
      "variants":variants,
      "blender_version":blender_version
    }

def build(args):
    import bpy
    d=load(args.definition)
    assert d["task_id"]=="T-037"
    assert d["execution_boundary"]["engineering_execution_authorized"] is True
    assert d["profile_contract"]["authority"]=="SOURCE_DERIVED_PROFILE"
    assert d["profile_contract"]["exact_historical_curve"]=="UNRESOLVED"
    scene,cam=setup_scene(bpy)
    mats={
      "LARGE_GUAZI_GONG":setup_material(bpy,"LARGE_MAT",(0.30,0.19,0.10,1.0)),
      "SMALL_GUAZI_GONG":setup_material(bpy,"SMALL_MAT",(0.56,0.38,0.19,1.0))
    }
    objects={}; payloads={}
    points=d["profile_contract"]["normalized_points"]
    for v in d["variants"]:
        vid=v["variant_id"]
        verts,faces=mesh_payload(float(v["length_mm"]),float(v["width_mm"]),float(v["thickness_mm"]),points)
        obj=make_object(bpy,vid,verts,faces,mats[vid]); objects[vid]=obj
        payloads[vid]={
          "component_name_zh":v["component_name_zh"],"count":v["count"],
          "length":float(v["length_mm"]),"width":float(v["width_mm"]),"thickness":float(v["thickness_mm"]),
          "verts":verts,"faces":faces,"bbox":bbox(verts)
        }
    # Canonical first article contains only two overlapping-at-origin variant objects.
    for obj in objects.values():
        obj.hide_render=False
        obj.location=(0,0,0); obj.rotation_euler=(0,0,0); obj.scale=(1,1,1)
    scene["T037_MASTER_ID"]=d["master_id"]
    scene["T037_PROFILE_AUTHORITY"]="SOURCE_DERIVED_PROFILE"
    Path(args.asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.asset).resolve()))
    sem=semantic_from_def(d,payloads,bpy.app.version_string)
    sem["definition_sha256"]=digest(args.definition)
    sem["canonical_blend_sha256"]=digest(args.asset)
    sem["family_semantic_signature"]=stable({
      "master_id":sem["master_id"],
      "profile":sem["profile_contract"],
      "variants":{k:v["semantic_geometry_signature"] for k,v in sem["variants"].items()}
    })
    write(args.semantic,sem)
    if args.review_dir:
        r=Path(args.review_dir); r.mkdir(parents=True,exist_ok=True)
        render_variant(bpy,scene,cam,objects,"LARGE_GUAZI_GONG",r/"LARGE_AXON.png","AXON")
        render_variant(bpy,scene,cam,objects,"LARGE_GUAZI_GONG",r/"LARGE_FRONT.png","FRONT")
        render_variant(bpy,scene,cam,objects,"SMALL_GUAZI_GONG",r/"SMALL_AXON.png","AXON")
        render_variant(bpy,scene,cam,objects,"SMALL_GUAZI_GONG",r/"SMALL_FRONT.png","FRONT")
        render_overlay(bpy,scene,cam,objects,r/"OVERLAY_FRONT.png")
    print("T037_BUILD_PASS",sem["family_semantic_signature"])

def inspect(args):
    import bpy
    expected=load(args.expected)
    out={"status":"PASS","task_id":"T-037","master_id":expected["master_id"],"variants":{}}
    for vid,ev in expected["variants"].items():
        obj=bpy.data.objects.get(vid)
        if obj is None: raise AssertionError("missing object "+vid)
        verts=[[float(v.co.x),float(v.co.y),float(v.co.z)] for v in obj.data.vertices]
        faces=[[int(i) for i in p.vertices] for p in obj.data.polygons]
        sig=stable({"variant_id":vid,"dimensions":ev["resolved_dimensions_mm"],"vertices":verts,"faces":faces})
        if sig!=ev["semantic_geometry_signature"]:
            raise AssertionError("geometry signature mismatch "+vid)
        out["variants"][vid]={"semantic_geometry_signature":sig,"vertex_count":len(verts),"face_count":len(faces)}
    out["family_semantic_signature"]=expected["family_semantic_signature"]
    write(args.output,out)
    print("T037_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","inspect"),required=True)
    ap.add_argument("--definition"); ap.add_argument("--asset",required=True); ap.add_argument("--semantic")
    ap.add_argument("--review-dir"); ap.add_argument("--expected"); ap.add_argument("--output")
    a=ap.parse_args()
    if a.mode=="build":
        if not a.definition or not a.semantic: ap.error("build requires --definition --semantic")
        build(a)
    else:
        if not a.expected or not a.output: ap.error("inspect requires --expected --output")
        inspect(a)
if __name__=="__main__": main()
