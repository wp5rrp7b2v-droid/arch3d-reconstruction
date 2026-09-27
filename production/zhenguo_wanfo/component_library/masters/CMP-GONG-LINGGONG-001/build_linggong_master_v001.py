"""T-039 令栱 first-article builder / inspector."""
import argparse, hashlib, json, math, sys
from pathlib import Path

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write(path,value):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stable(value): return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
def canonical_geometry(vertices,faces):
    return [[round(float(x),4),round(float(y),4),round(float(z),4)] for x,y,z in vertices], [[int(i) for i in f] for f in faces]

def mesh_payload(length,width,thickness,points):
    pts=[(float(x)*length,float(z)*thickness) for x,z in points]
    n=len(pts); y0=-width/2.0; y1=width/2.0
    verts=[[x,y0,z] for x,z in pts]+[[x,y1,z] for x,z in pts]
    faces=[list(range(n-1,-1,-1)),list(range(n,2*n))]
    for i in range(n):
        j=(i+1)%n; faces.append([i,j,n+j,n+i])
    return verts,faces

def bbox(verts):
    xs=[v[0] for v in verts]; ys=[v[1] for v in verts]; zs=[v[2] for v in verts]
    return {"min":[min(xs),min(ys),min(zs)],"max":[max(xs),max(ys),max(zs)],
            "dimensions":[max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)]}

def setup_material(bpy):
    m=bpy.data.materials.new("LINGGONG_MAT"); m.diffuse_color=(0.43,0.27,0.13,1.0); m.use_nodes=True
    nodes=m.node_tree.nodes; nodes.clear()
    e=nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value=(0.43,0.27,0.13,1.0); e.inputs["Strength"].default_value=0.9
    o=nodes.new("ShaderNodeOutputMaterial"); m.node_tree.links.new(e.outputs[0],o.inputs["Surface"])
    return m

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def setup_scene(bpy):
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene; scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.resolution_x=900; scene.render.resolution_y=650; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"; scene.render.film_transparent=False
    scene.world.use_nodes=True
    bg=next(n for n in scene.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.96,0.96,0.96,1.0); bg.inputs["Strength"].default_value=1.0
    scene.view_settings.view_transform="Standard"
    bpy.ops.object.camera_add(location=(0,-1200,0))
    cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.clip_start=1.0; cam.data.clip_end=10000.0
    scene.camera=cam
    return scene,cam

def make_object(bpy,verts,faces,mat):
    mesh=bpy.data.meshes.new("LINGGONG_MESH"); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new("LINGGONG",mesh); bpy.context.collection.objects.link(obj); obj.data.materials.append(mat)
    obj["t039_role"]="canonical_master_body"
    return obj

def render(bpy,scene,cam,path,view):
    if view=="FRONT":
        cam.location=(0,-1200,0); cam.data.ortho_scale=1100; cam.rotation_euler=(math.radians(90.0),0.0,0.0)
    elif view=="END":
        cam.location=(1200,0,0); cam.data.ortho_scale=420; look_at(cam,(0,0,0))
    else:
        cam.location=(900,-900,650); cam.data.ortho_scale=1250; look_at(cam,(0,0,0))
    scene.render.filepath=str(path); bpy.ops.render.render(write_still=True)

def semantic_from_def(d,verts,faces,blender_version):
    qv,qf=canonical_geometry(verts,faces)
    dims=d["canonical_reference_geometry_mm"]
    body={
      "body_id":"LINGGONG",
      "component_name_zh":"令栱",
      "resolved_dimensions_mm":dims,
      "local_bbox_mm":bbox(verts),
      "geometry_vertices_mm":verts,
      "geometry_faces":faces,
      "unsupported_detail_count":0,
      "joinery_cut_count":0,
      "local_transform":{"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]}
    }
    body["semantic_geometry_signature"]=stable({"body_id":"LINGGONG","dimensions":dims,"vertices":qv,"faces":qf})
    sem={
      "schema_version":"LINGGONG_MASTER_SEMANTIC_V001","task_id":"T-039",
      "component_family_id":d["component_family_id"],"master_id":d["master_id"],"master_version":d["master_version"],
      "master_family_count":1,"geometry_variant_count":0,"physical_instance_count":28,
      "direction_distribution":d["registry_boundary"]["direction_distribution"],
      "sample_to_instance_mapping":"UNKNOWN",
      "profile_contract":d["profile_contract"],"evidence_semantics":d["evidence_semantics"],
      "deferred_geometry":d["deferred_geometry"],"canonical_body":body,"blender_version":blender_version
    }
    sem["family_semantic_signature"]=stable({"master_id":sem["master_id"],"profile":sem["profile_contract"],"body_signature":body["semantic_geometry_signature"]})
    return sem

def build(a):
    import bpy
    d=load(a.definition)
    assert d["task_id"]=="T-039" and d["execution_boundary"]["engineering_execution_authorized"] is True
    dims=d["canonical_reference_geometry_mm"]; p=d["profile_contract"]["normalized_points"]
    verts,faces=mesh_payload(float(dims["length"]),float(dims["width"]),float(dims["thickness"]),p)
    scene,cam=setup_scene(bpy); obj=make_object(bpy,verts,faces,setup_material(bpy))
    obj.location=(0,0,0); obj.rotation_euler=(0,0,0); obj.scale=(1,1,1)
    scene["T039_MASTER_ID"]=d["master_id"]; scene["T039_PROFILE_SIGNATURE"]=d["profile_contract"]["control_set_sha256"]
    Path(a.asset).parent.mkdir(parents=True,exist_ok=True); bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.asset).resolve()))
    sem=semantic_from_def(d,verts,faces,bpy.app.version_string)
    sem["definition_sha256"]=digest(a.definition); sem["canonical_blend_sha256"]=digest(a.asset); write(a.semantic,sem)
    if a.review_dir:
        r=Path(a.review_dir); r.mkdir(parents=True,exist_ok=True)
        render(bpy,scene,cam,r/"AXON.png","AXON"); render(bpy,scene,cam,r/"FRONT_PROFILE.png","FRONT"); render(bpy,scene,cam,r/"END_WIDTH.png","END")
    print("T039_BUILD_PASS",sem["family_semantic_signature"],sem["canonical_body"]["semantic_geometry_signature"])

def inspect(a):
    import bpy
    e=load(a.expected); obj=bpy.data.objects.get("LINGGONG")
    if obj is None: raise AssertionError("missing LINGGONG object")
    verts=[[float(v.co.x),float(v.co.y),float(v.co.z)] for v in obj.data.vertices]
    faces=[[int(i) for i in p.vertices] for p in obj.data.polygons]
    qv,qf=canonical_geometry(verts,faces)
    sig=stable({"body_id":"LINGGONG","dimensions":e["canonical_body"]["resolved_dimensions_mm"],"vertices":qv,"faces":qf})
    if sig!=e["canonical_body"]["semantic_geometry_signature"]: raise AssertionError("geometry signature mismatch")
    write(a.output,{"status":"PASS","task_id":"T-039","master_id":e["master_id"],
                    "semantic_geometry_signature":sig,"family_semantic_signature":e["family_semantic_signature"],
                    "vertex_count":len(verts),"face_count":len(faces)})
    print("T039_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("build","inspect"),required=True)
    ap.add_argument("--definition"); ap.add_argument("--asset",required=True); ap.add_argument("--semantic")
    ap.add_argument("--review-dir"); ap.add_argument("--expected"); ap.add_argument("--output")
    a=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if a.mode=="build":
        if not a.definition or not a.semantic: ap.error("build requires --definition --semantic")
        build(a)
    else:
        if not a.expected or not a.output: ap.error("inspect requires --expected --output")
        inspect(a)
if __name__=="__main__": main()
