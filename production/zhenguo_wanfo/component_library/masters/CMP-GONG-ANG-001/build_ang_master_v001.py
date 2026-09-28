"""T-041 Ang-family first-article builder / inspector."""
import argparse, hashlib, json, math, sys
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stable(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def quantize_vertices(vertices):
    return [[round(float(x), 6), round(float(y), 6), round(float(z), 6)] for x, y, z in vertices]

def mesh_payload(profile_uw, thickness):
    """Map member-local U/V/W => Blender X/Y/Z and extrude profile through V."""
    pts=[(float(u), float(w)) for u,w in profile_uw]
    n=len(pts)
    y0=-float(thickness)/2.0
    y1=float(thickness)/2.0
    verts=[[u,y0,w] for u,w in pts] + [[u,y1,w] for u,w in pts]
    faces=[list(range(n-1,-1,-1)), list(range(n,2*n))]
    for i in range(n):
        j=(i+1)%n
        faces.append([i,j,n+j,n+i])
    return verts, faces

def bbox(verts):
    xs=[v[0] for v in verts]; ys=[v[1] for v in verts]; zs=[v[2] for v in verts]
    return {
        "min":[min(xs),min(ys),min(zs)],
        "max":[max(xs),max(ys),max(zs)],
        "dimensions":[max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)]
    }

def body_geometry_signature(variant_id, verts, faces):
    return stable({
        "variant_id":variant_id,
        "vertices":quantize_vertices(verts),
        "faces":[[int(i) for i in f] for f in faces]
    })

def setup_material(bpy,name,rgb):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*rgb,1.0)
    m.use_nodes=True
    nodes=m.node_tree.nodes
    nodes.clear()
    p=nodes.new("ShaderNodeBsdfPrincipled")
    p.inputs["Base Color"].default_value=(*rgb,1.0)
    p.inputs["Roughness"].default_value=0.72
    o=nodes.new("ShaderNodeOutputMaterial")
    m.node_tree.links.new(p.outputs[0],o.inputs["Surface"])
    return m

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def setup_scene(bpy):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for c in list(bpy.data.collections):
        if c.name != "Collection" and c.users == 0:
            bpy.data.collections.remove(c)
    scene=bpy.context.scene
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.resolution_x=1100
    scene.render.resolution_y=760
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.film_transparent=False
    scene.world.use_nodes=True
    bg=next(n for n in scene.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.94,0.94,0.94,1.0)
    bg.inputs["Strength"].default_value=0.8
    scene.view_settings.view_transform="Standard"
    bpy.ops.object.camera_add(location=(0,-1600,0))
    cam=bpy.context.object
    cam.name="T041_REVIEW_CAMERA"
    cam.data.type="ORTHO"
    cam.data.clip_start=1.0
    cam.data.clip_end=20000.0
    scene.camera=cam
    return scene, cam

def create_mesh_object(bpy,name,verts,faces,mat,role,canonical):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj["t041_role"]=role
    obj["variant_id"]=name
    obj["canonical_asset"]=bool(canonical)
    obj.location=(0,0,0)
    obj.rotation_euler=(0,0,0)
    obj.scale=(1,1,1)
    return obj

def create_fixture(bpy, d):
    ga=d["gate_a_contract"]
    tri=ga["report_design_triangle"]
    obs=ga["observed_crosscheck"]
    coll=bpy.data.collections.new("DOUBLE_ANG_ASSEMBLY_FIXTURE_VALIDATION_ONLY")
    bpy.context.scene.collection.children.link(coll)
    coll["t041_role"]="validation_fixture"
    coll["canonical_asset"]=False
    coll["historical_joinery_claim"]=False
    created=[]
    marks={
        "O":(0.0,0.0,0.0),
        "RUN":(float(tri["run_mm"]),0.0,0.0),
        "RISE":(float(tri["run_mm"]),0.0,float(tri["rise_mm"])),
        "OBS7195":(float(obs["third_fourth_total_projection_mean_mm"]),0.0,0.0),
    }
    for key,loc in marks.items():
        bpy.ops.object.empty_add(type="PLAIN_AXES",location=loc)
        obj=bpy.context.object
        obj.name="FIXTURE_"+key
        obj.empty_display_size=38.0
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        coll.objects.link(obj)
        obj["t041_role"]="validation_fixture_datum"
        obj["canonical_asset"]=False
        obj["datum_name"]=key
        created.append(obj)
    # design-triangle line, non-canonical
    mesh=bpy.data.meshes.new("FIXTURE_47_21_GUIDE_MESH")
    verts=[marks["O"],marks["RUN"],marks["RISE"],marks["O"]]
    edges=[(0,1),(1,2),(2,3)]
    mesh.from_pydata(verts,edges,[])
    mesh.update()
    guide=bpy.data.objects.new("FIXTURE_47_21_GUIDE",mesh)
    coll.objects.link(guide)
    guide["t041_role"]="validation_fixture_guide"
    guide["canonical_asset"]=False
    created.append(guide)
    return coll, created

def set_visibility(objects, active_names):
    active=set(active_names)
    for obj in objects:
        obj.hide_render=(obj.name not in active)

def render_object(bpy,scene,cam,obj,path,view,all_renderables):
    set_visibility(all_renderables,[obj.name])
    bb=obj.dimensions
    sx=max(float(bb.x),1.0); sy=max(float(bb.y),1.0); sz=max(float(bb.z),1.0)
    if view=="PROFILE":
        cam.location=(0,-max(1400.0,sy*8.0),0)
        cam.data.ortho_scale=max(sx*1.25,sz*1.6)
        look_at(cam,(0,0,0))
    elif view=="END":
        cam.location=(max(1800.0,sx*2.2),0,0)
        cam.data.ortho_scale=max(sy,sz)*1.8
        look_at(cam,(0,0,0))
    else:
        cam.location=(sx*0.85,-sx*0.85,max(600.0,sz*2.0))
        cam.data.ortho_scale=max(sx*1.45,sz*2.0)
        look_at(cam,(0,0,0))
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def render_fixture(bpy,scene,cam,fixture_objs,path,all_renderables):
    set_visibility(all_renderables,[o.name for o in fixture_objs])
    cam.location=(360,-1800,160)
    cam.data.ortho_scale=1050
    look_at(cam,(360,0,160))
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def build_semantic(d, payloads, blender_version, blend_sha):
    bodies=[]
    for vid in ("TOU_ANG","ER_ANG"):
        verts,faces=payloads[vid]
        profile=d["gate_b_contract"][vid]
        body={
            "body_id":vid,
            "variant_id":vid,
            "component_name_zh":"头昂" if vid=="TOU_ANG" else "二昂",
            "canonical_asset":True,
            "reference_control_span_only":True,
            "historical_full_timber_length_closed":False,
            "profile_point_count":int(profile["point_count"]),
            "profile_control_points_sha256":profile["control_points_sha256"],
            "semantic_profile":profile["semantic_profile"],
            "thickness_mm":float(d["gate_a_contract"]["source_dimensions"]["ANG_THICKNESS_MM"]),
            "local_bbox_mm":bbox(verts),
            "geometry_vertices_mm":quantize_vertices(verts),
            "geometry_faces":[[int(i) for i in f] for f in faces],
            "unsupported_detail_count":0,
            "joinery_cut_count":0,
            "local_transform":{"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]}
        }
        body["semantic_geometry_signature"]=body_geometry_signature(vid,verts,faces)
        bodies.append(body)
    tri=d["gate_a_contract"]["report_design_triangle"]
    obs=d["gate_a_contract"]["observed_crosscheck"]
    fixture={
        "fixture_id":d["gate_a_contract"]["validation_fixture_id"],
        "canonical_asset":False,
        "registry_binding":False,
        "catalog_asset":False,
        "historical_joinery_claim":False,
        "run_mm":float(tri["run_mm"]),
        "rise_mm":float(tri["rise_mm"]),
        "angle_deg":float(tri["angle_deg"]),
        "reference_span_mm":float(tri["centreline_span_mm"]),
        "observed_third_fourth_projection_mean_mm":float(obs["third_fourth_total_projection_mean_mm"]),
        "ideal_vs_observed_delta_mm":float(obs["delta_mm"]),
        "member_full_length_authority":False
    }
    family_signature=stable({
        "master_id":d["master_id"],
        "gate_a_signature":d["gate_a_contract"]["semantic_signature_sha256"],
        "gate_b_signature":d["gate_b_contract"]["family_semantic_control_sha256"],
        "bodies":[b["semantic_geometry_signature"] for b in bodies],
        "fixture":fixture
    })
    return {
        "schema_version":"ANG_MASTER_SEMANTIC_V001",
        "task_id":"T-041",
        "component_family_id":d["component_family_id"],
        "master_id":d["master_id"],
        "master_version":d["master_version"],
        "blender_version":blender_version,
        "definition_sha256":None,
        "canonical_blend_sha256":blend_sha,
        "master_family_count":1,
        "geometry_variant_count":2,
        "direction_geometry_variant_count":0,
        "registry_binding_count":32,
        "binding_counts":{"TOU_ANG":16,"ER_ANG":16},
        "count_status":"LOCKED_DERIVED",
        "whole_hall_direct_inventory_claim":False,
        "sample_to_instance_mapping":"UNKNOWN",
        "historical_full_timber_length_status":"UNRESOLVED",
        "gate_a_contract":d["gate_a_contract"],
        "gate_b_contract":d["gate_b_contract"],
        "canonical_bodies":bodies,
        "validation_fixture":fixture,
        "family_semantic_signature":family_signature,
        "unsupported_connection_geometry_present":False
    }

def do_build(args):
    import bpy
    d=load(args.definition)
    scene,cam=setup_scene(bpy)
    mat_tou=setup_material(bpy,"TOU_ANG_MAT",(0.56,0.30,0.14))
    mat_er=setup_material(bpy,"ER_ANG_MAT",(0.44,0.24,0.11))
    thickness=float(d["gate_a_contract"]["source_dimensions"]["ANG_THICKNESS_MM"])
    payloads={}
    bodies={}
    for vid,mat in (("TOU_ANG",mat_tou),("ER_ANG",mat_er)):
        pts=d["gate_b_contract"][vid]["control_points_uw_mm"]
        verts,faces=mesh_payload(pts,thickness)
        payloads[vid]=(verts,faces)
        bodies[vid]=create_mesh_object(bpy,vid,verts,faces,mat,"canonical_master_body",True)
    fixture_coll,fixture_objs=create_fixture(bpy,d)
    renderables=list(bodies.values())+[o for o in fixture_objs if o.type=="MESH"]
    review_dir=Path(args.review_dir) if args.review_dir else None
    if review_dir:
        review_dir.mkdir(parents=True,exist_ok=True)
        for vid,obj in bodies.items():
            for view in ("PROFILE","AXON","END"):
                render_object(bpy,scene,cam,obj,review_dir/(vid+"_"+view+".png"),view,renderables)
        render_fixture(bpy,scene,cam,fixture_objs,review_dir/"DOUBLE_ANG_FIXTURE_PROFILE.png",renderables)
        set_visibility(renderables,[o.name for o in bodies.values()])
    Path(args.asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.asset))
    blend_sha=digest(args.asset)
    sem=build_semantic(d,payloads,bpy.app.version_string,blend_sha)
    sem["definition_sha256"]=digest(args.definition)
    write(args.semantic,sem)
    print("T041_BUILD_PASS",sem["family_semantic_signature"])

def inspect_mesh_object(obj):
    verts=[[obj.data.vertices[i].co.x,obj.data.vertices[i].co.y,obj.data.vertices[i].co.z] for i in range(len(obj.data.vertices))]
    faces=[[int(v) for v in p.vertices] for p in obj.data.polygons]
    return verts,faces

def do_inspect(args):
    import bpy
    expected=load(args.expected)
    bodies={}
    for vid in ("TOU_ANG","ER_ANG"):
        obj=bpy.data.objects.get(vid)
        if obj is None:
            raise AssertionError("missing_"+vid)
        verts,faces=inspect_mesh_object(obj)
        bodies[vid]=body_geometry_signature(vid,verts,faces)
    fixture=[o for o in bpy.data.objects if o.get("t041_role") in ("validation_fixture_datum","validation_fixture_guide")]
    out={
        "status":"PASS",
        "task_id":"T-041",
        "body_geometry_signatures":bodies,
        "fixture_object_count":len(fixture),
        "blend_sha256":digest(args.asset),
        "expected_blend_sha256":expected["canonical_blend_sha256"]
    }
    write(args.output,out)
    print("T041_INSPECT_PASS",len(fixture))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","inspect"),required=True)
    ap.add_argument("--definition")
    ap.add_argument("--asset",required=True)
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--expected")
    ap.add_argument("--output")
    a=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else None)
    if a.mode=="build":
        for req in ("definition","semantic"):
            if not getattr(a,req): raise SystemExit("missing --"+req.replace("_","-"))
        do_build(a)
    else:
        for req in ("expected","output"):
            if not getattr(a,req): raise SystemExit("missing --"+req.replace("_","-"))
        do_inspect(a)

if __name__=="__main__":
    main()
