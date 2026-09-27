"""T-038 慢栱 family first-article builder / inspector.

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

def canonical_geometry(vertices, faces):
    # Blender stores mesh coordinates as float32. Quantize only for the semantic
    # signature so a save/reopen round-trip does not fail on harmless sub-micron
    # representation drift; dimensional validation remains independent.
    qverts=[[round(float(x),4),round(float(y),4),round(float(z),4)] for x,y,z in vertices]
    qfaces=[[int(i) for i in face] for face in faces]
    return qverts,qfaces

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
    # Review materials use emission so GitHub headless rendering cannot collapse
    # into a near-uniform dark frame because of lighting/EGL differences.
    m=bpy.data.materials.new(name)
    m.diffuse_color=rgba
    m.use_nodes=True
    nodes=m.node_tree.nodes
    nodes.clear()
    emission=nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value=rgba
    emission.inputs["Strength"].default_value=0.82
    output=nodes.new("ShaderNodeOutputMaterial")
    m.node_tree.links.new(emission.outputs[0],output.inputs["Surface"])
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
    scene.world.use_nodes=True
    bg=next(n for n in scene.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.96,0.96,0.96,1.0)
    bg.inputs["Strength"].default_value=1.0
    scene.view_settings.view_transform="Standard"
    bpy.ops.object.camera_add(location=(0,-1600,0))
    cam=bpy.context.object
    cam.data.type="ORTHO"
    cam.data.clip_start=1.0
    cam.data.clip_end=10000.0
    cam.data.ortho_scale=1900
    # Explicit front rotation: camera looks +Y and keeps +Z vertical.
    cam.rotation_euler=(math.radians(90.0),0.0,0.0)
    scene.camera=cam
    return scene,cam

def make_object(bpy,name,verts,faces,mat):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj["t038_variant"]=name
    return obj

def render_variant(bpy,scene,cam,objects,which,path,view):
    for key,obj in objects.items():
        obj.hide_render=(key!=which)
    if view=="FRONT":
        cam.location=(0,-1600,0)
        cam.data.ortho_scale=1900
        cam.rotation_euler=(math.radians(90.0),0.0,0.0)
    else:
        cam.location=(1500,-1500,1000)
        cam.data.ortho_scale=2000
        look_at(cam,(0,0,0))
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def render_overlay(bpy,scene,cam,objects,path):
    for obj in objects.values(): obj.hide_render=False
    cam.location=(0,-1600,0)
    cam.data.ortho_scale=1900
    cam.rotation_euler=(math.radians(90.0),0.0,0.0)
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
        qverts,qfaces=canonical_geometry(payload["geometry_vertices_mm"],payload["geometry_faces"])
        payload["semantic_geometry_signature"]=stable({
          "variant_id":v,
          "dimensions":payload["resolved_dimensions_mm"],
          "vertices":qverts,
          "faces":qfaces
        })
        variants[v]=payload
    return {
      "schema_version":"MANGONG_MASTER_SEMANTIC_V001",
      "task_id":"T-038",
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
    assert d["task_id"]=="T-038"
    assert d["execution_boundary"]["engineering_execution_authorized"] is True
    assert d["profile_contract"]["authority"]=="SAME_BUILDING_SOURCE_GUIDED_SIMPLIFIED"
    assert d["profile_contract"]["exact_historical_curve"]=="UNRESOLVED"
    scene,cam=setup_scene(bpy)
    mats={
      "LARGE_MANGONG":setup_material(bpy,"LARGE_MAT",(0.30,0.19,0.10,1.0)),
      "SMALL_MANGONG":setup_material(bpy,"SMALL_MAT",(0.56,0.38,0.19,1.0))
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
    scene["T038_MASTER_ID"]=d["master_id"]
    scene["T038_PROFILE_AUTHORITY"]="SAME_BUILDING_SOURCE_GUIDED_SIMPLIFIED"
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
        render_variant(bpy,scene,cam,objects,"LARGE_MANGONG",r/"LARGE_AXON.png","AXON")
        render_variant(bpy,scene,cam,objects,"LARGE_MANGONG",r/"LARGE_FRONT.png","FRONT")
        render_variant(bpy,scene,cam,objects,"SMALL_MANGONG",r/"SMALL_AXON.png","AXON")
        render_variant(bpy,scene,cam,objects,"SMALL_MANGONG",r/"SMALL_FRONT.png","FRONT")
        render_overlay(bpy,scene,cam,objects,r/"OVERLAY_FRONT.png")
    print("T038_BUILD_PASS",sem["family_semantic_signature"])

def inspect(args):
    import bpy
    expected=load(args.expected)
    out={"status":"PASS","task_id":"T-038","master_id":expected["master_id"],"variants":{}}
    for vid,ev in expected["variants"].items():
        obj=bpy.data.objects.get(vid)
        if obj is None: raise AssertionError("missing object "+vid)
        verts=[[float(v.co.x),float(v.co.y),float(v.co.z)] for v in obj.data.vertices]
        faces=[[int(i) for i in p.vertices] for p in obj.data.polygons]
        qverts,qfaces=canonical_geometry(verts,faces)
        sig=stable({"variant_id":vid,"dimensions":ev["resolved_dimensions_mm"],"vertices":qverts,"faces":qfaces})
        if sig!=ev["semantic_geometry_signature"]:
            raise AssertionError("geometry signature mismatch "+vid)
        out["variants"][vid]={"semantic_geometry_signature":sig,"vertex_count":len(verts),"face_count":len(faces)}
    out["family_semantic_signature"]=expected["family_semantic_signature"]
    write(args.output,out)
    print("T038_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","inspect"),required=True)
    ap.add_argument("--definition"); ap.add_argument("--asset",required=True); ap.add_argument("--semantic")
    ap.add_argument("--review-dir"); ap.add_argument("--expected"); ap.add_argument("--output")
    a=ap.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])
    if a.mode=="build":
        if not a.definition or not a.semantic: ap.error("build requires --definition --semantic")
        build(a)
    else:
        if not a.expected or not a.output: ap.error("inspect requires --expected --output")
        inspect(a)
if __name__=="__main__": main()
