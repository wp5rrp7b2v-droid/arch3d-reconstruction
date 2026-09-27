"""T-040 华栱 two-variant first-article builder / inspector."""
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

def setup_material(bpy,name,rgb):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,1.0); m.use_nodes=True
    nodes=m.node_tree.nodes; nodes.clear()
    e=nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value=(*rgb,1.0); e.inputs["Strength"].default_value=0.9
    o=nodes.new("ShaderNodeOutputMaterial"); m.node_tree.links.new(e.outputs[0],o.inputs["Surface"])
    return m

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def setup_scene(bpy):
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene; scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.resolution_x=1000; scene.render.resolution_y=700; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"; scene.render.film_transparent=False
    scene.world.use_nodes=True
    bg=next(n for n in scene.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.96,0.96,0.96,1.0); bg.inputs["Strength"].default_value=1.0
    scene.view_settings.view_transform="Standard"
    bpy.ops.object.camera_add(location=(0,-1500,0))
    cam=bpy.context.object; cam.name="T040_REVIEW_CAMERA"; cam.data.type="ORTHO"; cam.data.clip_start=1.0; cam.data.clip_end=20000.0
    scene.camera=cam
    return scene,cam

def make_body(bpy,variant_id,verts,faces,mat):
    mesh=bpy.data.meshes.new(variant_id+"_MESH"); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(variant_id,mesh); bpy.context.collection.objects.link(obj); obj.data.materials.append(mat)
    obj["t040_role"]="canonical_master_body"; obj["variant_id"]=variant_id; obj["canonical_asset"]=True
    obj.location=(0,0,0); obj.rotation_euler=(0,0,0); obj.scale=(1,1,1)
    return obj

def make_fixture(bpy,d):
    coll=bpy.data.collections.new("TWO_JUMP_ASSEMBLY_FIXTURE_VALIDATION_ONLY")
    bpy.context.scene.collection.children.link(coll)
    datums=d["length_assembly_contract"]["validation_fixture"]["datums_mm"]
    created=[]
    for name in ("D0","D1","D2"):
        bpy.ops.object.empty_add(type="PLAIN_AXES",location=(float(datums[name]),0.0,0.0))
        obj=bpy.context.object; obj.name="FIXTURE_"+name; obj.empty_display_size=45.0
        for c in list(obj.users_collection): c.objects.unlink(obj)
        coll.objects.link(obj)
        obj["t040_role"]="validation_fixture_datum"; obj["canonical_asset"]=False; obj["datum_name"]=name
        created.append(obj)
    coll["t040_role"]="validation_fixture"; coll["canonical_asset"]=False
    coll["direct_primary_assertion"]="D2-D0 = 732.4 mm"
    return coll,created

def set_body_visibility(bodies,active):
    for k,o in bodies.items():
        o.hide_render=(k!=active)
        o.hide_viewport=False

def render_body(bpy,scene,cam,obj,path,view,length,width,thickness,bodies):
    active=obj.name; set_body_visibility(bodies,active)
    if view=="PROFILE":
        cam.location=(0,-max(1300.0,width*7.0),0); cam.data.ortho_scale=length*1.18; look_at(cam,(0,0,0))
    elif view=="END":
        cam.location=(max(2200.0,length*2.0),0,0); cam.data.ortho_scale=max(width,thickness)*1.8; look_at(cam,(0,0,0))
    else:
        cam.location=(length*0.82,-length*0.82,max(600.0,length*0.48)); cam.data.ortho_scale=length*1.45; look_at(cam,(0,0,0))
    scene.render.filepath=str(path); bpy.ops.render.render(write_still=True)

def body_semantic(variant_id,dims,verts,faces):
    qv,qf=canonical_geometry(verts,faces)
    body={
      "body_id":variant_id,"variant_id":variant_id,"component_name_zh":"华栱",
      "resolved_dimensions_mm":dims,"reference_specimen_only":True,"applies_to_registry_instance_exact":False,
      "local_bbox_mm":bbox(verts),"geometry_vertices_mm":verts,"geometry_faces":faces,
      "unsupported_detail_count":0,"joinery_cut_count":0,
      "local_transform":{"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]}
    }
    body["semantic_geometry_signature"]=stable({"body_id":variant_id,"dimensions":dims,"vertices":qv,"faces":qf})
    return body

def semantic_from_def(d,payloads,blender_version):
    bodies=[]
    for variant_id in ("JUMP_1_HUAGONG","JUMP_2_HUAGONG"):
        dims=d["length_assembly_contract"]["reference_specimens"][variant_id]
        clean={"length":float(dims["length_mm"]),"width":float(dims["width_mm"]),"thickness":float(dims["thickness_mm"])}
        verts,faces=payloads[variant_id]
        bodies.append(body_semantic(variant_id,clean,verts,faces))
    vf=d["length_assembly_contract"]["validation_fixture"]
    dat={k:float(v) for k,v in vf["datums_mm"].items()}
    fixture={
      "fixture_id":vf["fixture_id"],"canonical_asset":False,"registry_binding":False,"catalog_asset":False,
      "datums_mm":dat,"combined_projection_mm":dat["D2"]-dat["D0"],
      "midpoint_interval_1_mm":dat["D1"]-dat["D0"],"midpoint_interval_2_mm":dat["D2"]-dat["D1"],
      "D1_classification":vf["D1_classification"],"direct_assertion":vf["direct_assertion"],
      "individual_jump_projection_direct":False,"mesh_end_measurement_authority":False,"hidden_overlap_used":False,
      "machine_tolerance_mm":float(vf["machine_tolerance_mm"])
    }
    sem={
      "schema_version":"HUAGONG_MASTER_SEMANTIC_V001","task_id":"T-040",
      "component_family_id":d["component_family_id"],"master_id":d["master_id"],"master_version":d["master_version"],
      "master_family_count":1,"geometry_variant_count":2,"physical_instance_count":56,
      "jump_binding_counts":{"JUMP_1_HUAGONG":28,"JUMP_2_HUAGONG":28},
      "direction_distribution_each_jump":d["registry_boundary"]["direction_distribution_each_jump"],
      "whole_hall_total_claim":False,"sample_to_instance_mapping":"UNKNOWN","instance_historical_full_length_status":"UNRESOLVED",
      "length_assembly_contract":d["length_assembly_contract"],"profile_contract":d["profile_contract"],
      "deferred_geometry":d["deferred_geometry"],"canonical_bodies":bodies,"validation_fixture":fixture,
      "blender_version":blender_version
    }
    sem["family_semantic_signature"]=stable({
      "master_id":sem["master_id"],"profile_signature":d["profile_contract"]["control_set_sha256"],
      "length_assembly_signature":d["length_assembly_contract"]["control_set_sha256"],
      "body_signatures":[x["semantic_geometry_signature"] for x in bodies],
      "fixture":fixture
    })
    return sem

def build(a):
    import bpy
    d=load(a.definition)
    assert d["task_id"]=="T-040" and d["execution_boundary"]["engineering_execution_authorized"] is True
    p=d["profile_contract"]["normalized_points"]
    scene,cam=setup_scene(bpy)
    mats={
      "JUMP_1_HUAGONG":setup_material(bpy,"HUAGONG_JUMP1_MAT",(0.47,0.30,0.14)),
      "JUMP_2_HUAGONG":setup_material(bpy,"HUAGONG_JUMP2_MAT",(0.34,0.23,0.12))
    }
    payloads={}; bodies={}
    for variant_id in ("JUMP_1_HUAGONG","JUMP_2_HUAGONG"):
        spec=d["length_assembly_contract"]["reference_specimens"][variant_id]
        verts,faces=mesh_payload(float(spec["length_mm"]),float(spec["width_mm"]),float(spec["thickness_mm"]),p)
        payloads[variant_id]=(verts,faces); bodies[variant_id]=make_body(bpy,variant_id,verts,faces,mats[variant_id])
    make_fixture(bpy,d)
    scene["T040_MASTER_ID"]=d["master_id"]
    scene["T040_GATE_A_SIGNATURE"]=d["length_assembly_contract"]["control_set_sha256"]
    scene["T040_GATE_B_SIGNATURE"]=d["profile_contract"]["control_set_sha256"]
    Path(a.asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.asset).resolve()))
    sem=semantic_from_def(d,payloads,bpy.app.version_string)
    sem["definition_sha256"]=digest(a.definition); sem["canonical_blend_sha256"]=digest(a.asset); write(a.semantic,sem)
    if a.review_dir:
        r=Path(a.review_dir); r.mkdir(parents=True,exist_ok=True)
        for variant_id in ("JUMP_1_HUAGONG","JUMP_2_HUAGONG"):
            spec=d["length_assembly_contract"]["reference_specimens"][variant_id]
            obj=bodies[variant_id]; L=float(spec["length_mm"]); W=float(spec["width_mm"]); T=float(spec["thickness_mm"])
            render_body(bpy,scene,cam,obj,r/(variant_id+"_PROFILE.png"),"PROFILE",L,W,T,bodies)
            render_body(bpy,scene,cam,obj,r/(variant_id+"_AXON.png"),"AXON",L,W,T,bodies)
            render_body(bpy,scene,cam,obj,r/(variant_id+"_END.png"),"END",L,W,T,bodies)
        for o in bodies.values(): o.hide_render=False
    print("T040_BUILD_PASS",sem["family_semantic_signature"],*[x["semantic_geometry_signature"] for x in sem["canonical_bodies"]])

def inspect(a):
    import bpy
    e=load(a.expected)
    sigs={}
    for body in e["canonical_bodies"]:
        variant_id=body["variant_id"]; obj=bpy.data.objects.get(variant_id)
        if obj is None: raise AssertionError("missing "+variant_id)
        verts=[[float(v.co.x),float(v.co.y),float(v.co.z)] for v in obj.data.vertices]
        faces=[[int(i) for i in p.vertices] for p in obj.data.polygons]
        qv,qf=canonical_geometry(verts,faces)
        sig=stable({"body_id":variant_id,"dimensions":body["resolved_dimensions_mm"],"vertices":qv,"faces":qf})
        if sig!=body["semantic_geometry_signature"]: raise AssertionError("geometry signature mismatch "+variant_id)
        sigs[variant_id]=sig
    datums={}
    for name in ("D0","D1","D2"):
        obj=bpy.data.objects.get("FIXTURE_"+name)
        if obj is None: raise AssertionError("missing fixture datum "+name)
        if bool(obj.get("canonical_asset",True)): raise AssertionError("fixture datum marked canonical "+name)
        datums[name]=float(obj.location.x)
    write(a.output,{"status":"PASS","task_id":"T-040","master_id":e["master_id"],
                    "body_geometry_signatures":sigs,"family_semantic_signature":e["family_semantic_signature"],
                    "fixture_datums_mm":datums,"fixture_object_count":3})
    print("T040_REOPEN_PASS")

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
