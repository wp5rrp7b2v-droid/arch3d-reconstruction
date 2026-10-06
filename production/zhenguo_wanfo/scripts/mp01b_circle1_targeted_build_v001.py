import argparse, hashlib, json, math, sys
from pathlib import Path

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def stable(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
def file_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def clear_scene():
    import bpy
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def scene_setup():
    import bpy
    s=bpy.context.scene
    s.unit_settings.system="METRIC"
    s.unit_settings.scale_length=0.001
    s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_WORKBENCH"
    s.display.shading.light="STUDIO"
    s.display.shading.color_type="MATERIAL"
    s.display.shading.show_shadows=True
    s.display.shading.show_cavity=True
    s.render.resolution_percentage=100
    s.world.color=(0.94,0.94,0.94)
    return s

def mat(name,c):
    import bpy
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color=(*c,1)
    return m

def mesh_obj(name, verts, faces, loc, rz_deg, props, material):
    import bpy
    me=bpy.data.meshes.new(name+"_MESH")
    me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location=tuple(float(v) for v in loc)
    ob.rotation_euler=(0,0,math.radians(float(rz_deg)))
    for k,v in props.items():
        if isinstance(v,(list,dict,tuple)):
            ob[k]=json.dumps(v,ensure_ascii=False,sort_keys=True)
        elif v is None:
            ob[k]="NULL"
        else:
            ob[k]=v
    if material: ob.data.materials.append(material)
    return ob

def box_geom(lx,ly,h,z0=0):
    x=lx/2; y=ly/2; z1=z0+h
    v=[(-x,-y,z0),(x,-y,z0),(x,y,z0),(-x,y,z0),
       (-x,-y,z1),(x,-y,z1),(x,y,z1),(-x,y,z1)]
    f=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    return v,f

def two_tier_geom(base_x,base_y,top_x,top_y,h1,h2):
    verts=[]; faces=[]
    for lx,ly,z0,h in [(base_x,base_y,0,h1),(top_x,top_y,h1,h2)]:
        v,f=box_geom(lx,ly,h,z0); off=len(verts)
        verts += v; faces += [tuple(i+off for i in q) for q in f]
    return verts,faces

def frustum_geom(bottom_x,bottom_y,top_x,top_y,h):
    bx=bottom_x/2; by=bottom_y/2; tx=top_x/2; ty=top_y/2
    v=[(-bx,-by,0),(bx,-by,0),(bx,by,0),(-bx,by,0),
       (-tx,-ty,h),(tx,-ty,h),(tx,ty,h),(-tx,ty,h)]
    f=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    return v,f

def prism_xz_geom(poly_xz, width_y):
    hy=float(width_y)/2.0
    n=len(poly_xz)
    verts=[(float(x),-hy,float(z)) for x,z in poly_xz] + [(float(x),hy,float(z)) for x,z in poly_xz]
    faces=[]
    faces.append(tuple(range(n-1,-1,-1)))
    faces.append(tuple(range(n,2*n)))
    for i in range(n):
        j=(i+1)%n
        faces.append((i,j,n+j,n+i))
    return verts,faces

def huagong_visible_profile_geom(profile, side_key, tip_depth_fraction_override=None):
    side=profile[side_key]
    H=float(side["guang_mm"])
    W=float(side["hou_mm"])
    inward=float(profile["existing_length_control"]["inward_gonghead_reach_mm"])
    outward=float(profile["existing_length_control"]["outward_tuojiao_reach_mm"])
    pts=[[float(a),float(b)] for a,b in profile["normalized_inward_underside"]]
    if tip_depth_fraction_override is not None:
        pts[-1][1]=float(tip_depth_fraction_override)
    controls=[]
    for xf,df in pts:
        x=xf*inward
        z=H-df*H
        controls.append((x,z))
    # profile coordinates are station-relative: outward=-250, station=0, inward=+650.
    poly=[(-outward,H),(inward,H)]
    for x,z in reversed(controls):
        poly.append((x,z))
    poly.append((-outward,0.0))
    return prism_xz_geom(poly,W),controls

def diagonal_prism_geom(lower_xyz, upper_xyz, x_thickness, inplane_width):
    x0,y0,z0=[float(v) for v in lower_xyz]
    x1,y1,z1=[float(v) for v in upper_xyz]
    dy=y1-y0; dz=z1-z0
    L=(dy*dy+dz*dz)**0.5
    if L<=0: raise ValueError("zero Tuojiao centerline")
    # in-plane normal to centerline in Y-Z section
    ny=-dz/L; nz=dy/L
    hx=float(x_thickness)/2.0; hw=float(inplane_width)/2.0
    verts=[]
    for x,y,z in [(x0,y0,z0),(x1,y1,z1)]:
        for sx,sw in [(-1,-1),(1,-1),(1,1),(-1,1)]:
            verts.append((x+sx*hx, y+sw*hw*ny, z+sw*hw*nz))
    faces=[
      (0,3,2,1),(4,5,6,7),
      (0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)
    ]
    return verts,faces

def add_empty(name,xyz,props=None):
    import bpy
    ob=bpy.data.objects.new(name,None)
    bpy.context.scene.collection.objects.link(ob)
    ob.empty_display_type="PLAIN_AXES"; ob.empty_display_size=120
    ob.location=tuple(float(v) for v in xyz)
    for k,v in (props or {}).items():
        ob[k]=v
    return ob

def object_payload(ob):
    import bpy
    bpy.context.view_layer.update()
    lv=[[round(float(v.co.x),6),round(float(v.co.y),6),round(float(v.co.z),6)] for v in ob.data.vertices]
    faces=[list(p.vertices) for p in ob.data.polygons]
    wv=[]
    for v in ob.data.vertices:
        co=ob.matrix_world @ v.co
        wv.append([round(float(co.x),6),round(float(co.y),6),round(float(co.z),6)])
    lmin=[min(v[i] for v in lv) for i in range(3)]; lmax=[max(v[i] for v in lv) for i in range(3)]
    wmin=[min(v[i] for v in wv) for i in range(3)]; wmax=[max(v[i] for v in wv) for i in range(3)]
    props={}
    for k in ob.keys():
        val=ob[k]
        if isinstance(val,str) and val and val[0] in "[{":
            try: props[k]=json.loads(val)
            except: props[k]=val
        else: props[k]=val
    return {
      "logical_object_id":props.get("logical_object_id"),
      "component_role":props.get("component_role"),
      "master_id":props.get("master_id"),
      "geometry_basis":props.get("geometry_basis"),
      "evidence_class":props.get("evidence_class"),
      "historical_metric_claim":bool(props.get("historical_metric_claim",False)),
      "historical_full_length_claim":bool(props.get("historical_full_length_claim",False)),
      "whole_hall_count_claim":bool(props.get("whole_hall_count_claim",False)),
      "historical_joinery":props.get("historical_joinery"),
      "joinery_cut_count":int(props.get("joinery_cut_count",0)),
      "axis_semantics":props.get("axis_semantics"),
      "translation_mm":[round(float(x),6) for x in ob.location],
      "rotation_z_deg":round(math.degrees(float(ob.rotation_euler.z)),6),
      "local_bbox_mm":{"min":lmin,"max":lmax,"dimensions":[round(lmax[i]-lmin[i],6) for i in range(3)]},
      "world_bbox_mm":{"min":wmin,"max":wmax,"dimensions":[round(wmax[i]-wmin[i],6) for i in range(3)]},
      "local_geometry_signature":stable({"v":lv,"f":faces}),
      "world_geometry_signature":stable({"v":wv,"f":faces}),
      "custom_properties":props
    }

def common_props(logical, role, master, basis, evidence, axis):
    return {
      "logical_object_id":logical,
      "component_role":role,
      "master_id":master,
      "geometry_basis":basis,
      "evidence_class":evidence,
      "historical_metric_claim":False,
      "historical_full_length_claim":False,
      "whole_hall_count_claim":False,
      "historical_joinery":"UNKNOWN / DEFERRED / NOT_MODELED",
      "joinery_cut_count":0,
      "axis_semantics":axis
    }

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def render_setup():
    import bpy
    cd=bpy.data.cameras.new("T47_CAMERA")
    cam=bpy.data.objects.new("T47_CAMERA",cd)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera=cam; cd.type="ORTHO"; cd.clip_end=100000
    ld=bpy.data.lights.new("T47_KEY","AREA"); ld.energy=1200; ld.size=6000
    li=bpy.data.objects.new("T47_KEY",ld); bpy.context.scene.collection.objects.link(li)
    li.location=(5000,-5000,6000); look_at(li,(0,0,300))
    return cam

def render(scene,cam,path,pos,target,ortho,res=(1500,950)):
    import bpy
    cam.location=pos; look_at(cam,target); cam.data.ortho_scale=ortho
    scene.render.resolution_x=res[0]; scene.render.resolution_y=res[1]
    scene.render.filepath=str(Path(path).resolve())
    bpy.ops.render.render(write_still=True)

def build(contract_path, profile_path, asset, semantic, review_dir=None, huagong_len_override=None, tuojiao_z_offset_override=None, gonghead_tip_depth_fraction_override=None):
    import bpy
    c=load(contract_path)
    profile=load(profile_path)
    clear_scene(); scene=scene_setup()
    mats={
      "fc":mat("FC",(0.30,0.15,0.07)),
      "pl":mat("PL",(0.38,0.20,0.09)),
      "tf":mat("TF",(0.52,0.31,0.12)),
      "ld":mat("LD",(0.64,0.43,0.19)),
      "hg":mat("HG",(0.45,0.28,0.12)),
      "lg":mat("LG",(0.58,0.37,0.15)),
      "tj":mat("TJ",(0.34,0.22,0.10))
    }
    objs=[]

    fc=c["four_chuanfu"]; pl=c["pingliang"]
    v,f=box_geom(fc["length_mm"],fc["width_mm"],fc["thickness_mm"])
    objs.append(mesh_obj("T47__FOUR_CHUANFU",v,f,[0,0,-fc["thickness_mm"]],90,
      common_props("四椽栿-东缝","FOUR_CHUANFU","CMP-FRAME-FOUR-CHUANFU-001_MASTER",
      "DIRECT_SECTION + REPORT_INFERRED_REALIZATION","DIRECT_PRIMARY_SECTION / REPORT_INFERRED_LENGTH","local X -> assembly Y"),mats["fc"]))

    v,f=box_geom(pl["length_mm"],pl["width_mm"],pl["thickness_mm"])
    objs.append(mesh_obj("T47__PINGLIANG",v,f,[0,0,pl["underside_z_mm"]],90,
      common_props("平梁-东缝","PINGLIANG","CMP-FRAME-PINGLIANG-001_MASTER",
      "DIRECT_SECTION + RECONSTRUCTED_MINIMUM_SPAN","DIRECT_PRIMARY_SECTION / RECONSTRUCTED_LENGTH_AND_BEARING","local X -> assembly Y"),mats["pl"]))

    for side,y in [("FRONT",1836.0),("REAR",-1836.0)]:
        tf=c["tuofeng"][side.lower()]
        v,f=two_tier_geom(tf["base_footprint_mm"]["x"],tf["base_footprint_mm"]["y"],
                          tf["upper_seat_footprint_mm"]["x"],tf["upper_seat_footprint_mm"]["y"],
                          tf["tier_heights_mm"][0],tf["tier_heights_mm"][1])
        objs.append(mesh_obj(f"T47__TUOFENG_{side}",v,f,[0,y,0],0,
          common_props(f"ASM-MP01B-TUOFENG-{side}-01","TUOFENG_LOWER_SUPPORT","CMP-FRAME-TUOFENG-001_MASTER",
          "TWO_TIER_ASSEMBLY_ENVELOPE","RECONSTRUCTED_DESIGN / REPLACEABLE","world X/Y aligned"),mats["tf"]))

        ld=c["ludou"][side.lower()]
        b=ld["bottom_plan_mm"]; t=ld["top_plan_mm"]
        v,f=frustum_geom(b[0],b[1],t[0],t[1],ld["total_height_mm"])
        p=common_props(f"ASM-MP01B-PANJIAN-LUDOU-{side}-01","PANJIAN_LUDOU","CMP-FRAME-LUDOU-PANJIAN-001_MASTER",
          "MEASURED_TARGET_ENVELOPE + COMPLETED_BOTTOM_DEPTH","DIRECT_TARGET + PARAMETRIC_COMPLETION","world X/Y aligned")
        p["bottom_depth_classification"]="RECONSTRUCTED_DESIGN / EQUAL_PLAN_SIDE_INSET / REPLACEABLE"
        objs.append(mesh_obj(f"T47__PANJIAN_LUDOU_{side}",v,f,[0,y,ld["bottom_z_mm"]],0,p,mats["ld"]))

    # Linggong direct target envelopes
    for side,key in [("FRONT","front_linggong"),("REAR","rear_linggong")]:
        g=c["gongs"][key]
        v,f=box_geom(g["length_mm"],g["thickness_mm"],g["height_guang_mm"])
        p=common_props(f"ASM-MP01B-LINGGONG-{side}-01","TARGET_LINGGONG","CMP-FRAME-LINGGONG-INTERIOR-001_MASTER",
          "POSITION_SPECIFIC_BOUNDED_ENVELOPE / PROFILE_DEFERRED",g["classification"],"local X -> assembly X / 顺身")
        objs.append(mesh_obj(f"T47__LINGGONG_{side}",v,f,[g["center_xy_mm"][0],g["center_xy_mm"][1],g["z_min_mm"]],0,p,mats["lg"]))

    # Circle 1 approved interior-Huagong visible gong-head profile
    canonical_len=float(c["huagong_image_calibration"]["deterministic_control"]["realization_length_mm"])
    hlen=canonical_len if huagong_len_override is None else float(huagong_len_override)
    if abs(hlen-canonical_len)>1e-9:
        raise ValueError("Circle1 build freezes Huagong realization length at 900 mm; use profile mutation only")
    for side,key in [("FRONT","front_huagong"),("REAR","rear_huagong")]:
        base=c["gongs"][key]
        ep=c["huagong_endpoints"][side.lower()]
        station=float(ep["station_y_mm"])
        (v,f),profile_controls=huagong_visible_profile_geom(
            profile,side.lower(),gonghead_tip_depth_fraction_override
        )
        p=common_props(
          f"ASM-MP01B-HUAGONG-{side}-01","INTERIOR_HUAGONG","CMP-FRAME-HUAGONG-INTERIOR-001_MASTER",
          "TARGET_DRAWING_GUIDED_SIMPLIFIED_VISIBLE_GONGHEAD / IMAGE_CALIBRATED_LENGTH",
          profile["classification"],
          "local X -> assembly Y / 进深"
        )
        p["realization_length_mm"]=canonical_len
        p["inward_gonghead_reach_mm"]=float(profile["existing_length_control"]["inward_gonghead_reach_mm"])
        p["outward_tuojiao_reach_mm"]=float(profile["existing_length_control"]["outward_tuojiao_reach_mm"])
        p["profile_candidate_id"]=profile["candidate_id"]
        p["profile_normalized_control"]=profile["normalized_inward_underside"]
        p["profile_metric_controls_xz"]=profile_controls
        p["tip_depth_fraction"]=float(profile["normalized_inward_underside"][-1][1]) if gonghead_tip_depth_fraction_override is None else float(gonghead_tip_depth_fraction_override)
        p["outer_tuojiao_y_mm"]=float(ep["tuojiao_outer_y_mm"])
        p["inner_gonghead_y_mm"]=float(ep["gonghead_inner_y_mm"])
        p["t040_profile_reuse"]=False
        p["exact_historical_curve_claim"]=False
        objs.append(mesh_obj(
          f"T47__HUAGONG_{side}",v,f,[0,station,base["z_min_mm"]],ep["rotation_z_deg"],p,mats["hg"]
        ))

    # Tuojiao first-article diagonal envelopes (T3 evidence-bounded control)
    tj=c["tuojiao"]
    sec=tj["section_mm"]; ctl=tj["centerline_control"]
    for side in ["FRONT","REAR"]:
        inst=tj[side.lower()]
        lo=list(inst["lower_xyz_mm"]); hi=list(inst["upper_xyz_mm"])
        zoff=float(tj["z_offset"]["canonical_mm"]) if tuojiao_z_offset_override is None else float(tuojiao_z_offset_override)
        lo[2]+=zoff; hi[2]+=zoff
        v,f=diagonal_prism_geom(lo,hi,sec["hou"],sec["guang"])
        p=common_props(
          f"ASM-MP01B-TUOJIAO-{side}-01","TUOJIAO_FRAME_SUPPORT","CMP-FRAME-TUOJIAO-001",
          "STRAIGHT_RECTANGULAR_DIAGONAL_ENVELOPE / FIRST_ARTICLE",
          "DIRECT_PRIMARY FAMILY MEAN + SOURCE_DRAWING_CALIBRATED PROJECT CONTROL / REPLACEABLE",
          "long axis in assembly Y-Z section / FRONT-REAR mirrored"
        )
        p["section_guang_mm"]=float(sec["guang"])
        p["section_hou_mm"]=float(sec["hou"])
        p["horizontal_projection_mm"]=float(ctl["horizontal_projection_mm"])
        p["relative_rise_mm"]=float(ctl["relative_rise_mm"])
        p["centerline_length_mm"]=float(ctl["centerline_length_mm"])
        p["angle_deg"]=float(ctl["angle_deg"])
        p["lower_xyz_mm"]=lo
        p["upper_xyz_mm"]=hi
        p["z_offset_mm"]=zoff
        p["z_offset_classification"]=tj["z_offset"]["classification"]
        p["exact_contact_xyz"]="UNKNOWN"
        objs.append(mesh_obj(f"T47__TUOJIAO_{side}",v,f,[0,0,0],0,p,mats["tj"]))

    controls=[]
    for d in c["controls"]:
        controls.append(add_empty(d["id"],d["xyz_mm"],{"logical_control":True,"physical":False}))

    bpy.context.view_layer.update()
    payloads=[object_payload(o) for o in sorted(objs,key=lambda x:x.get("logical_object_id",""))]

    deferred=[
      {"logical_object_id":"ASM-MP01B-PANJIAN-FANG-FRONT-01","record_type":"DEFERRED_PHYSICAL_PARTICIPANT","source_label":"东缝前上平槫下襻间枋","known_section_mm":[210,152],"full_length_mm":None,"geometry_generated":False,"reason":"numeric full length unresolved"},
      {"logical_object_id":"ASM-MP01B-PANJIAN-FANG-REAR-01","record_type":"DEFERRED_PHYSICAL_PARTICIPANT","source_label":"东缝后上平槫下襻间枋","known_section_mm":None,"full_length_mm":None,"geometry_generated":False,"reason":"section and numeric full length unresolved"}
    ]
    relationships=[
      {"id":"SUP-FC-TF-F","type":"SUPPORT","source":"四椽栿-东缝","target":"ASM-MP01B-TUOFENG-FRONT-01","evidence":"A2 role + reconstructed local placement"},
      {"id":"SUP-FC-TF-R","type":"SUPPORT","source":"四椽栿-东缝","target":"ASM-MP01B-TUOFENG-REAR-01","evidence":"A2 role + reconstructed local placement"},
      {"id":"SUP-TF-LD-F","type":"SUPPORT","source":"ASM-MP01B-TUOFENG-FRONT-01","target":"ASM-MP01B-PANJIAN-LUDOU-FRONT-01","evidence":"report modular decomposition + reconstructed footprint"},
      {"id":"SUP-TF-LD-R","type":"SUPPORT","source":"ASM-MP01B-TUOFENG-REAR-01","target":"ASM-MP01B-PANJIAN-LUDOU-REAR-01","evidence":"report modular decomposition + reconstructed footprint"},
      {"id":"SUP-LG-PL-F","type":"SUPPORT","source":"ASM-MP01B-LINGGONG-FRONT-01","target":"平梁-东缝","evidence":"A2 support role + target direct Linggong"},
      {"id":"SUP-LG-PL-R","type":"SUPPORT","source":"ASM-MP01B-LINGGONG-REAR-01","target":"平梁-东缝","evidence":"A2 support role + target direct Linggong"},
      {"id":"LOC-DAT-TF-F","type":"LOCATE","source":"DATUM-MP01B-FRONT-SUPPORT","target":"ASM-MP01B-TUOFENG-FRONT-01"},
      {"id":"LOC-DAT-TF-R","type":"LOCATE","source":"DATUM-MP01B-REAR-SUPPORT","target":"ASM-MP01B-TUOFENG-REAR-01"},
      {"id":"LOC-LD-HG-F","type":"LOCATE","source":"ASM-MP01B-PANJIAN-LUDOU-FRONT-01","target":"ASM-MP01B-HUAGONG-FRONT-01"},
      {"id":"LOC-LD-HG-R","type":"LOCATE","source":"ASM-MP01B-PANJIAN-LUDOU-REAR-01","target":"ASM-MP01B-HUAGONG-REAR-01"},
      {"id":"LOC-LD-LG-F","type":"LOCATE","source":"ASM-MP01B-PANJIAN-LUDOU-FRONT-01","target":"ASM-MP01B-LINGGONG-FRONT-01"},
      {"id":"LOC-LD-LG-R","type":"LOCATE","source":"ASM-MP01B-PANJIAN-LUDOU-REAR-01","target":"ASM-MP01B-LINGGONG-REAR-01"},
      {"id":"LOC-TJ-HG-F","type":"LOCATE","source":"DATUM-MP01B-FRONT-HUAGONG-TUOJIAO-CONTACT","target":"ASM-MP01B-HUAGONG-FRONT-01"},
      {"id":"LOC-TJ-HG-R","type":"LOCATE","source":"DATUM-MP01B-REAR-HUAGONG-TUOJIAO-CONTACT","target":"ASM-MP01B-HUAGONG-REAR-01"},
      {"id":"LOC-TJ-LOWER-F","type":"LOCATE","source":"DATUM-MP01B-FRONT-TUOJIAO-LOWER","target":"ASM-MP01B-TUOJIAO-FRONT-01"},
      {"id":"LOC-TJ-UPPER-F","type":"LOCATE","source":"DATUM-MP01B-FRONT-TUOJIAO-UPPER","target":"ASM-MP01B-TUOJIAO-FRONT-01"},
      {"id":"LOC-TJ-LOWER-R","type":"LOCATE","source":"DATUM-MP01B-REAR-TUOJIAO-LOWER","target":"ASM-MP01B-TUOJIAO-REAR-01"},
      {"id":"LOC-TJ-UPPER-R","type":"LOCATE","source":"DATUM-MP01B-REAR-TUOJIAO-UPPER","target":"ASM-MP01B-TUOJIAO-REAR-01"},
      {"id":"BEL-TJ-F","type":"BELONG","source":"ASM-MP01B-TUOJIAO-FRONT-01","target":"MP01B_FRONT_BRACKET_NODE"},
      {"id":"BEL-TJ-R","type":"BELONG","source":"ASM-MP01B-TUOJIAO-REAR-01","target":"MP01B_REAR_BRACKET_NODE"},
      {"id":"BEL-FANG-F","type":"BELONG","source":"ASM-MP01B-PANJIAN-FANG-FRONT-01","target":"MP01B_FRONT_BRACKET_NODE"},
      {"id":"BEL-FANG-R","type":"BELONG","source":"ASM-MP01B-PANJIAN-FANG-REAR-01","target":"MP01B_REAR_BRACKET_NODE"}
    ]
    sem={
      "schema_version":"MP01B_CIRCLE1_TARGETED_BUILD_SEMANTIC_1.0",
      "status":"BUILT / MACHINE_REVIEW_PENDING",
      "task_id":"T-047",
      "assembly_id":"MP01B_CIRCLE1_TARGETED_BUILD_EAST_SEAM",
      "contract_sha256":file_sha(contract_path),
      "profile_control_sha256":file_sha(profile_path),
      "circle1_profile_candidate_id":profile["candidate_id"],
      "blender_version":bpy.app.version_string,
      "huagong_realization_length_mm":hlen,
      "is_mutation":gonghead_tip_depth_fraction_override is not None,
      "profile_tip_depth_fraction":float(profile["normalized_inward_underside"][-1][1]) if gonghead_tip_depth_fraction_override is None else float(gonghead_tip_depth_fraction_override),
      "rendered_physical_geometry_count":len(payloads),
      "objects":payloads,
      "deferred_physical_participants":deferred,
      "deferred_physical_participant_count":len(deferred),
      "relationships":relationships,
      "relationship_counts":{
        "SUPPORT":sum(1 for r in relationships if r["type"]=="SUPPORT"),
        "LOCATE":sum(1 for r in relationships if r["type"]=="LOCATE"),
        "BELONG":sum(1 for r in relationships if r["type"]=="BELONG"),
        "CONNECT":sum(1 for r in relationships if r["type"]=="CONNECT")
      },
      "bracket_interlock":c["gongs"]["overlap_classification"],
      "historical_joinery":"UNKNOWN / DEFERRED / NOT_MODELED",
      "joinery_cut_count":0,
      "whole_hall_claim":False,
      "historical_exactness_claim":False
    }
    sem["assembly_signature"]=stable({
      "objects":[(x["logical_object_id"],x["world_geometry_signature"]) for x in payloads],
      "relationships":relationships,
      "deferred":deferred
    })
    Path(semantic).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    if review_dir:
        rd=Path(review_dir); rd.mkdir(parents=True,exist_ok=True)
        cam=render_setup()
        render(scene,cam,rd/"CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png",(7000,0,600),(0,0,300),5200)
        render(scene,cam,rd/"CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png",(5200,-6200,3600),(0,0,260),7200)
        render(scene,cam,rd/"ORTHOGONAL_GONG_TOP_VIEW.png",(0,0,9000),(0,0,300),5200,(1400,1100))
        render(scene,cam,rd/"FRONT_NODE_DETAIL.png",(4200,1836,800),(0,1836,420),2200,(1100,900))
        render(scene,cam,rd/"FRONT_HUAGONG_PROFILE_DETAIL.png",(4200,1500,720),(0,1500,410),1250,(1200,900))
        render(scene,cam,rd/"FRONT_TUOJIAO_SIDE.png",(4200,2700,1200),(0,2700,420),2600,(1200,900))
        render(scene,cam,rd/"REAR_NODE_DETAIL.png",(4200,-1836,800),(0,-1836,420),2200,(1100,900))
        render(scene,cam,rd/"REAR_HUAGONG_PROFILE_DETAIL.png",(4200,-1500,720),(0,-1500,410),1250,(1200,900))
        render(scene,cam,rd/"REAR_TUOJIAO_SIDE.png",(4200,-2700,1200),(0,-2700,420),2600,(1200,900))

    Path(asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(asset).resolve()))
    sem["blend_sha256"]=file_sha(asset)
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01B_CIRCLE1_TARGETED_BUILD_PASS",sem["assembly_signature"])

def inspect(expected,output):
    import bpy
    exp=load(expected)
    got=[object_payload(o) for o in bpy.data.objects if o.type=="MESH" and o.get("logical_object_id")]
    got=sorted(got,key=lambda x:x["logical_object_id"])
    gm={x["logical_object_id"]:x["world_geometry_signature"] for x in got}
    em={x["logical_object_id"]:x["world_geometry_signature"] for x in exp["objects"]}
    out={"status":"PASS" if gm==em else "FAIL","logical_object_count":len(got),"got":gm,"expected":em}
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if out["status"]!="PASS": raise SystemExit("REOPEN_SIGNATURE_MISMATCH")
    print("MP01B_CIRCLE1_TARGETED_BUILD_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("build","inspect"))
    ap.add_argument("--contract"); ap.add_argument("--profile-control"); ap.add_argument("--asset"); ap.add_argument("--semantic")
    ap.add_argument("--review-dir"); ap.add_argument("--huagong-length-mm",type=float); ap.add_argument("--tuojiao-z-offset-mm",type=float); ap.add_argument("--gonghead-tip-depth-fraction",type=float)
    ap.add_argument("--expected"); ap.add_argument("--output")
    args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    a=ap.parse_args(args)
    if a.mode=="build":
        build(a.contract,a.profile_control,a.asset,a.semantic,a.review_dir,a.huagong_length_mm,a.tuojiao_z_offset_mm,a.gonghead_tip_depth_fraction)
    else:
        inspect(a.expected,a.output)

if __name__=="__main__":
    main()
