#!/usr/bin/env python3
"""Wanfo Hall V003 whole-hall C02 evidence-aware comparative correction.

Inputs: immutable V003 candidate BLEND + its exact SHA256 and A1/P3.3 datum.
This program does not export or copy the museum's third-party 3D geometry.
No stand-alone component tests, no changes to approved Masters or Stage 1.
All new geometry is a visual design *candidate*, not proven historic joinery.

Reference:
A1 scanned report, PDF pages 75-77 (roof/bracket relation),
106 (roof frame/叉手 diagrams), 153 and 155 (whole-hall roof sections).
Museum: https://szbwgvue.chwhyun.cn/wanfodian/
Distinguish source FACT from inferred placement in BUILD_REPORT.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
from collections import Counter
import bpy
from mathutils import Vector

ROOT=Path.cwd()
BASE=ROOT/"production/zhenguo_wanfo"
SOURCE=BASE/"mvp_v003/full/WANFO_FULL_V003.blend"
SOURCE_REPORT=BASE/"mvp_v003/full/BUILD_REPORT.json"
OUT=BASE/"mvp_v003_c02/full"
DATUM=BASE/"build/P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_V001.json"
PARAMS=BASE/"params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
HUA=BASE/"component_library/masters/CMP-GONG-HUAGONG-001/CMP-GONG-HUAGONG-001_MASTER_SEMANTIC_V001.json"
ANG=BASE/"component_library/masters/CMP-GONG-ANG-001/CMP-GONG-ANG-001_MASTER_SEMANTIC_V001.json"

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for data in iter(lambda:f.read(1024*1024),b""):h.update(data)
    return h.hexdigest()
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def write(path,obj):
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def object_digest(o):
    h=hashlib.sha256()
    for v in o.data.vertices:
        h.update(",".join(f"{float(k):.4f}" for k in v.co).encode());h.update(b";")
    for poly in o.data.polygons:
        h.update(("-".join(map(str,poly.vertices))+";").encode())
    for row in o.matrix_world:
        h.update((",".join(f"{float(x):.4f}" for x in row)+";").encode())
    return h.hexdigest()
def mat(name,rgb):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*rgb,1)
    m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    if p:p.inputs["Base Color"].default_value=(*rgb,1)
    return m
def collection(name):
    c=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c
def tag(o,role,authority="VISUAL_RECONSTRUCTION_DESIGN_NOT_SURVEYED"):
    o["c02_status"]="TEMP_REPLACEABLE_CANDIDATE"
    o["c02_role"]=role
    o["c02_geometry_authority"]=authority
    o["c02_historical_accuracy"]="NOT_VERIFIED"
    o["c02_structural_load_capacity"]="NOT_VERIFIED"
    return o
def cuboid(name,center,size,c,material,role):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    ob=bpy.context.object
    ob.name=name
    ob.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for prev in list(ob.users_collection):prev.objects.unlink(ob)
    c.objects.link(ob)
    if material:ob.data.materials.append(material)
    return tag(ob,role)
def beam(name,start,end,section,c,material,role):
    a,b=Vector(start),Vector(end)
    d=b-a
    assert d.length>0.1,(name,"ZERO_BEAM")
    ob=cuboid(name,(a+b)*0.5,(section,section,d.length),c,material,role)
    ob.rotation_euler=d.to_track_quat("Z","Y").to_euler()
    return ob
def master_instance(name,body,xyz,yaw,c,material,provenance,tilt=0):
    mesh=bpy.data.meshes.new(name+"_CANONICAL_PROFILE")
    mesh.from_pydata(body["geometry_vertices_mm"],[],body["geometry_faces"])
    mesh.update(calc_edges=True)
    o=bpy.data.objects.new(name,mesh)
    c.objects.link(o)
    o.location=xyz
    o.rotation_euler=(0,tilt,yaw)
    mesh.materials.append(material)
    tag(o,"MASTER_PROFILE_WITH_UNVERIFIED_ASSEMBLY_PLACEMENT",
        "CANONICAL_MASTER_PROFILE_VERTICES__ASSEMBLY_PLACEMENT_HYPOTHESIS")
    o["c02_master_source"]=provenance
    o["c02_master_signature"]=body["semantic_geometry_signature"]
    return o
def roof_delta(x,y):
    """Subtle gable/eave curvature candidate, not a measured 963 roof profile."""
    t=min(1.0,abs(y)/8295.0)
    xr=min(1.0,abs(x)/8677.5)
    return 90.0*math.sin(math.pi*t)**2 + 80.0*xr**4*t**3
def roof_surface(x,y):
    ya=abs(y)
    zridge=8870.0
    zshoulder=5270.0+(88+61)*15.3
    if ya<=3213:
        zz=zridge+(zshoulder-zridge)*ya/3213
    else:
        t=(ya-3213)/(8295-3213)
        half=3568.5+(8677.5-3568.5)*t
        zz=zshoulder*(1-t)+t*(5270+180*(abs(x)/half)**4)
    return zz+roof_delta(x,y)
def roof_topology(mesh):
    usage=Counter()
    for poly in mesh.polygons:
        verts=list(poly.vertices)
        for a,b in zip(verts,verts[1:]+verts[:1]):
            usage[tuple(sorted((a,b)))]+=1
    overused=[e for e,c in usage.items() if c>2]
    boundary=[e for e,c in usage.items() if c==1]
    assert not overused,("OVERUSED_ROOF_EDGES",len(overused))
    assert len(boundary)==80,("UNEXPECTED_ROOF_BOUNDARY_COUNT",len(boundary))
    # Roof single connected component in graph.
    adjacency={}
    for a,b in usage:
        adjacency.setdefault(a,set()).add(b)
        adjacency.setdefault(b,set()).add(a)
    seen=set();remaining=set(adjacency)
    while remaining:
        start=min(remaining);pending=[start];group=set()
        while pending:
            p=pending.pop()
            if p in group:continue
            group.add(p);pending.extend(adjacency[p]-group)
        seen.add(start);remaining-=group
        assert not remaining, "UNCONNECTED_ROOF_COMPONENT"
    return {"mesh_vertices":len(mesh.vertices),"mesh_faces":len(mesh.polygons),
            "eave_boundary_edges":len(boundary),"internal_open_seams":0,
            "excess_edge_multiplicity":0,"connected_components":1}
def render(name,eye,target,scale,hidden):
    scene=bpy.context.scene
    camd=bpy.data.cameras.new("C02_"+name+"_CAM")
    cam=bpy.data.objects.new("C02_"+name+"_CAM",camd)
    scene.collection.objects.link(cam)
    cam.location=Vector(eye)
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
    cam.data.type="ORTHO";cam.data.ortho_scale=scale;cam.data.clip_end=120000
    scene.camera=cam
    scene.render.filepath=str(OUT/f"WANFO_C02_{name}.png")
    for o in hidden:o.hide_render=True
    bpy.ops.render.render(write_still=True)
    for o in hidden:o.hide_render=False
def build():
    rpt=read(SOURCE_REPORT)
    assert SOURCE.is_file() and digest(SOURCE)==rpt["sha256"]["blend"], "SOURCE_V003_HASH_MISMATCH"
    param=read(PARAMS)["parameters"]
    datum=read(DATUM)
    assert param["PM-011"]["value"]==11475
    assert param["PM-012"]["value"]==10710
    assert datum["roof_control"]["shared_ridge_terminal"]=="ROOF_PURLIN_N_03"
    hua=read(HUA);ang=read(ANG)
    hua1=next(x for x in hua["canonical_bodies"] if x["body_id"]=="JUMP_1_HUAGONG")
    hua2=next(x for x in hua["canonical_bodies"] if x["body_id"]=="JUMP_2_HUAGONG")
    tou=next(x for x in ang["canonical_bodies"] if x["body_id"]=="TOU_ANG")
    er=next(x for x in ang["canonical_bodies"] if x["body_id"]=="ER_ANG")
    assert hua1["semantic_geometry_signature"]=="565fcdef9335691e73dd0cbec5e5d98b561f3bdebdbd367951bcb7826dc8f19a"
    assert hua2["semantic_geometry_signature"]=="451511f0b131e36784baefa2011850a1f9381d3b2dc1fee629951b7f4099e001"
    assert tou["semantic_geometry_signature"]=="61a2bbb85fa5fc07ed9c37ce610f2aee0360f280c09f8317614b7a62f7819250"
    assert er["semantic_geometry_signature"]=="b778edc208d788c5f9fad0a19849ca33f3334e7c4e2656721279386528979678"
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    bpy.context.view_layer.update()
    approved=[o for o in bpy.data.objects if o.type=="MESH" and o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"]
    assert len(approved)==63,"APPROVED_SOURCE_COUNT_CHANGED"
    approved_before={o.name:object_digest(o) for o in approved}
    roof=[o for o in bpy.data.objects if o.type=="MESH" and o.get("mvp_role")=="ROOF_STITCHED_CONTINUOUS_SURFACE_PROXY"]
    assert len(roof)==1,"EXPECTED_ONE_EXISTING_COMPLETE_ROOF_SURFACE"
    roof=roof[0];old_roof=roof_topology(roof.data)
    assert old_roof["mesh_vertices"]==953 and old_roof["mesh_faces"]==944
    coords_old=[tuple(v.co) for v in roof.data.vertices]
    for v in roof.data.vertices:
        v.co.z+=roof_delta(v.co.x,v.co.y)
    roof.data.update()
    new_roof=roof_topology(roof.data)
    roof["c02_status"]="TEMP_REPLACEABLE_CANDIDATE"
    roof["c02_role"]="C02_WHOLE_HALL_CURVED_ROOF_SILHOUETTE_CANDIDATE"
    roof["c02_change_mm"]="90mm sinusoidal roof sweep + 80mm outer-corner enhancement"
    assert len(coords_old)==len(roof.data.vertices)
    max_delta=max(roof_delta(v.co.x,v.co.y) for v in roof.data.vertices)
    assert 90 <= max_delta <= 180, "ROOF_CURVE_STRENGTH_OUT_OF_RANGE"
    ccorner=collection("C02_CORNER_45_DEGREES_NOT_APPROVED")
    cframe=collection("C02_WHOLE_HALL_DOUBLE_SIX_BEAM_LAYER_VISUAL_GUIDE")
    croof=collection("C02_HIP_RIDGE_FASCIA_DESIGN_GUIDES")
    mbr=mat("C02 corner Master silhouettes only",(0.44,0.28,0.13))
    mwood=mat("C02 whole-hall timber layout candidate",(0.37,0.21,0.11))
    mroof=mat("C02 roof fascia hypothetical",(0.21,0.27,0.27))
    mtemp=mat("C02 support placeholders not approved",(0.49,0.32,0.15))
    corners=[];corner_master_count=0;hipbeams=0
    sqrt2=math.sqrt(0.5)
    for sx in (-1,1):
        for sy in (-1,1):
            x=sx*11475/2;y=sy*10710/2
            dx=sx*sqrt2;dy=sy*sqrt2
            label=("W" if sx<0 else "E")+("S" if sy<0 else "N")
            theta=math.atan2(dy,dx)
            corners.append({"name":label,"column_xy_mm":[x,y],"outward_direction":[round(dx,6),round(dy,6)]})
            cbase=3534.3+293.8
            h1=hua1["resolved_dimensions_mm"]["thickness"]
            h2=hua2["resolved_dimensions_mm"]["thickness"]
            for step,body,reach,z in (
                (1,hua1,190,cbase+h1/2),
                (2,hua2,525,cbase+h1+160+h2/2),
                (3,tou,790,cbase+h1+300),
                (4,er,1030,cbase+h1+480)
            ):
                master_instance(f"C02_CORNER_{label}_{step}",body,
                    (x+dx*reach,y+dy*reach,z),theta,ccorner,mbr,
                    "CMP-GONG-HUAGONG-001" if step<=2 else "CMP-GONG-ANG-001",
                    tilt=0 if step<=2 else -math.radians(17))
                corner_master_count+=1
            # Visual link from corner to the roof edge through a cantilever.
            tip=(sx*8677.5,sy*8295.0,roof_surface(sx*8677.5,sy*8295.0)-115)
            inner=(x,y,4950.0)
            beam("C02_CORNER_EAVE_GUIDE_"+label,inner,tip,160,
                 ccorner,mtemp,"CORNER_EAVE_GLOBAL_GUIDE_NOT_TRUE_JOINT")
    assert corner_master_count==16 and len(corners)==4

    # A1/museum topology: two SIX_CHUANFU layers with FOUR_CHUANFU and
    # PINGLIANG above in main transverse frames. These new items are shape
    # guides and do not replace the existing approved 63-object bent.
    # Crucial unresolved datum: original approved local assembly has a
    # different vertical relationship to V002 roof controls.
    frame_x=(-2218.5,2218.5)
    layers={
      "LOWER_SIX_CHUANFU":{"z":4200.0,"half_run":5355.0,"size":305},
      "UPPER_SIX_CHUANFU":{"z":4700.0,"half_run":5355.0,"size":285},
      "FOUR_CHUANFU":{"z":6120.0,"half_run":3213.0,"size":250},
      "PINGLIANG":{"z":7480.0,"half_run":1500.0,"size":220}
    }
    assert 3534.3<layers["LOWER_SIX_CHUANFU"]["z"]<layers["UPPER_SIX_CHUANFU"]["z"]<layers["FOUR_CHUANFU"]["z"]<layers["PINGLIANG"]["z"]<8870
    records=[]
    for ix,x in enumerate(frame_x):
        label="W" if x<0 else "E"
        for key,v in layers.items():
            z=v["z"];run=v["half_run"]
            beam(f"C02_BENT_{label}_{key}",(x,-run,z),(x,run,z),
                 v["size"],cframe,mwood,
                 f"A1_MUSEUM_LAYER_{key}_SPATIAL_PREVIEW_NOT_MEASURED")
            records.append({"bent":label,"type":key,"z_center_mm":z,"end_y_mm":[-run,run]})
        # This is NOT a surveyed 3D frame; its connecting struts are
        # displayed only as a working arrangement. No joinery/contact PASS.
        for side in (-1,1):
            beam(f"C02_{label}_TUOFENG_SUPPORT_{side}",
                 (x,side*3150,4830),(x,side*3150,6000),
                 145,cframe,mtemp,"VERTICAL_SUPPORT_CONJECTURE_TO_BE_REPLACED")
            beam(f"C02_{label}_PING_SUPPORT_{side}",
                 (x,side*1320,6270),(x,side*1320,7350),
                 125,cframe,mtemp,"PINGLEVEL_SUPPORT_CONJECTURE_TO_BE_REPLACED")
            beam(f"C02_{label}_CHASHOU_{side}",
                 (x,side*1120,7590),(x,0,8660),
                 130,cframe,mwood,"RIDGE_CHASHOU_DESIGN_CANDIDATE")
        beam(f"C02_{label}_SHUZHU",(x,0,7600),(x,0,8600),
             155,cframe,mwood,"SHUZHU_VISUAL_HYPOTHESIS")
    assert len(records)==8
    # Four diagonal hip edges and front/back curved eave fascia segment
    # samples. The original roof is one continuous 953-vertex skin.
    for sx in (-1,1):
        for sy in (-1,1):
            prev=None
            for i in range(12):
                t=i/11
                y=sy*(3213+(8295-3213)*t)
                x=sx*(3568.5+(8677.5-3568.5)*t)
                p=(x,y,roof_surface(x,y)+35)
                if prev is not None:
                    beam(f"C02_HIP_{sx}_{sy}_{i}",prev,p,90,croof,mroof,
                         "HIP_RIDGE_PROFILE_TRIAL_UNAPPROVED")
                    hipbeams+=1
                prev=p
    for side in (-1,1):
        prev=None
        for i in range(25):
            x=-8677.5+(17355*i/24)
            p=(x,side*8295,roof_surface(x,side*8295)-18)
            if prev:
                beam(f"C02_EAVE_EDGE_{side}_{i}",prev,p,90,croof,mroof,
                     "CURVED_EAVE_FASCIA_PROFILE_TRIAL")
            prev=p
    assert hipbeams==44
    # Draw roof-shape boundary and whole-hall structure with the SAME scene,
    # not separate component demonstrations.
    bpy.context.view_layer.update()
    assert {o.name:object_digest(o) for o in approved}==approved_before, "SOURCE_APPROVED_ENTITY_CHANGED"
    rootroofbbox=[[min(o.matrix_world @ Vector(c)[i] for o in [roof] for c in o.bound_box) for i in (0,1,2)],
                  [max(o.matrix_world @ Vector(c)[i] for o in [roof] for c in o.bound_box) for i in (0,1,2)]]
    # Report what is actually validated rather than claiming complete bearing.
    failures=[
      "A1 does not yet provide a numeric calibrated overlay in this candidate",
      "63 approved local source entities are kept, but their contacts with C02 frame guides are NOT validated",
      "Two six-chuanfu layers are visible as provisional global frame geometry; exact elevations remain design hypotheses",
      "Corner 45-degree Master silhouettes are true Master profile meshes at unapproved placement / tilt",
      "Intercolumn 5-puzuo contacts and all hidden mortise-tenon, loading and shear were NOT tested",
      "Roof curvature is a small visual improvement candidate, not a surveyed roof deformation"
    ]
    OUT.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    scene["c02_status"]="WHOLE_HALL_REVIEW_CANDIDATE_NOT_APPROVED"
    scene["c02_visual_source"]="A1 scanned PDF page 75,76,77,106,153,155; Shanxi Digital Museum"
    scene["c02_geometry_basis"]="V003 + replaceable C02 geometry, no third-party mesh copied"
    scene["c02_structural_interface_status"]="NOT_TESTED_AND_NOT_APPROVED"
    scene.render.engine="BLENDER_WORKBENCH"
    scene.display.shading.light="STUDIO"
    scene.display.shading.color_type="MATERIAL"
    scene.render.resolution_x=1400;scene.render.resolution_y=1000
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.view_settings.view_transform="Standard"
    views=[
      ("EXTERIOR",(10200,-23600,12700),(0,0,4400),22000,[]),
      ("AXON",(21500,-24500,20300),(0,0,4200),27000,[]),
      ("FRONT_ELEVATION",(0,-27000,5600),(0,0,4750),18700,[]),
      ("SIDE_ELEVATION",(27500,0,5700),(0,0,4750),19400,[]),
      ("ROOF",(15500,-15000,24000),(0,0,7800),22300,[]),
      ("STRUCTURE",(17000,-22000,14100),(0,0,5450),22000,[roof]),
      ("CROSS_SECTION",(18000,0,7200),(0,0,6100),17500,[roof]),
      ("LONG_SECTION",(0,-18000,7200),(0,0,6100),18000,[roof])
    ]
    for name,eye,target,scale,hidden in views:render(name,eye,target,scale,hidden)
    for obj in bpy.data.objects:
        if obj.type=="CAMERA":obj.hide_render=True
    for o in roof.parent.children if roof.parent else []:
        o.hide_render=False
    blend=OUT/"WANFO_V003_C02_FULL.blend"
    glb=OUT/"WANFO_V003_C02_FULL.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True,check_existing=False)
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",export_extras=True)
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    src_masters=[o for o in meshes if o.get("v003_origin_master")]
    c02=[o for o in meshes if o.get("c02_status")=="TEMP_REPLACEABLE_CANDIDATE"]
    assert len([o for o in meshes if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"])==63
    assert len(src_masters)>=100 and len(c02)>100
    report={
      "candidate_id":"WANFO_V003_WHOLE_HALL_COMPARE_C02",
      "state":"GENERATED_REOPEN_PENDING__PO_VISUAL_UNAPPROVED",
      "source_V003_sha256":digest(SOURCE),
      "approved_source_count":len(approved),
      "approved_entity_mesh_and_transform_sha256_unchanged":True,
      "A1_basis":{"file_name":"A1_山西平遥镇国寺万佛殿与天王殿精细测绘报告_刘畅_廖慧农_李树盛.pdf",
                  "A1_pdf_pages_visually_checked":[75,76,77,106,153,155],
                  "A1_raster_source_text_layer_available":False,
                  "direct_scaled_overlay":"NOT_CALIBRATED_OR_PASSED",
                  "A1_primary_document_used_as_qualitative_constraints_only":True},
      "museum_reference":{"url":"https://szbwgvue.chwhyun.cn/wanfodian/",
           "facts":["三间面阔三间进深无内柱","单檐歇山顶","柱头七铺作双杪双下昂","补间五铺作双杪偷心",
                    "四角转角铺作45度出角华栱","上下六椽栿叠置","平梁上设蜀柱和叉手"],
           "third_party_mesh_copied":False},
      "roof":{"previous_topology":old_roof,"updated_topology":new_roof,
             "max_added_vertical_sweep_mm":max_delta,
             "roof_geometry_accuracy":"NON_MEASURED_SHAPE_CANDIDATE",
             "true_gable_and_eave_dimensions_validated_against_A1":False},
      "whole_hall_coordinate_basis":{"width_design_candidate_mm":11475,
             "depth_design_candidate_mm":10710,"roof_ridge_design_candidate_mm":8870,
             "eave_reference_y_mm":8295},
      "corner":{"count":len(corners),"master_reference_instances":corner_master_count,
                "corners":corners,"45_degree_dirs_all":True,
                "historical_connection_validated":False},
      "frame":{"layer_records":records,"layer_set_names":list(layers),
               "two_six_levels_present_in_global_structure":True,
               "qualified_as_historical_model":False},
      "purlins_from_V003":{"expected_count":7,"preserved":True},
      "objects":{"mesh_count":len(meshes),"approved_existing":63,
                 "V003_master_reference_instances":len(src_masters),
                 "C02_replaceable_meshes":len(c02)},
      "files":{"blend":str(blend.relative_to(ROOT)),
               "glb":str(glb.relative_to(ROOT)),
               "images":[str((OUT/f"WANFO_C02_{name}.png").relative_to(ROOT)) for name,*_ in views]},
      "binary_sha256":{"blend":digest(blend),"glb":digest(glb)},
      "technical_tests":{"roof_mesh_connected":"PASS",
             "roof_internal_open_seam":"PASS","candidate_object_inventory":"PASS",
             "approved_source_preserved":"PASS",
             "real_contact_geometry":"NOT_TESTED",
             "A1_pixel_aligned_similarity":"NOT_TESTED",
             "structural_or_historical_fidelity":"NOT_APPROVED"},
      "known_limitations":failures
    }
    write(OUT/"BUILD_REPORT.json",report)
    print("C02_GENERATED",json.dumps({"objects":report["objects"],
       "roof":report["roof"]["updated_topology"],
       "corner_count":report["corner"]["count"],"double_six_levels":True},ensure_ascii=False))
def reopen_blend():
    r=read(OUT/"BUILD_REPORT.json")
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    assert bpy.context.scene.get("c02_status")=="WHOLE_HALL_REVIEW_CANDIDATE_NOT_APPROVED"
    assert len(meshes)==r["objects"]["mesh_count"]
    assert len([o for o in meshes if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"])==63
    assert len([o for o in meshes if o.name.startswith("C02_CORNER_") and o.get("c02_master_source")])==16
    assert len([o for o in meshes if o.name.startswith("C02_BENT_")])==8
    roof=[o for o in meshes if o.get("c02_role")=="C02_WHOLE_HALL_CURVED_ROOF_SILHOUETTE_CANDIDATE"]
    assert len(roof)==1
    shape=roof_topology(roof[0].data)
    write(OUT/"BLEND_REOPEN.json",{"status":"PASS","mesh_objects":len(meshes),"roof":shape,
         "original_approved_source_objects":63,"corner_master_references":16})
    print("C02_BLEND_REOPEN_PASS",len(meshes))
def reopen_glb():
    bpy.ops.import_scene.gltf(filepath=str(OUT/"WANFO_V003_C02_FULL.glb"))
    mesh=[o for o in bpy.data.objects if o.type=="MESH"]
    approved=[o for o in mesh if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"]
    corners=[o for o in mesh if o.name.startswith("C02_CORNER_") and o.get("c02_master_source")]
    assert len(approved)==63,("GLB_MISSING_APPROVED_SOURCE",len(approved))
    assert len(corners)==16,("GLB_MISSING_CORNER_REFERENCE",len(corners))
    assert sum(1 for o in mesh if o.name.startswith("C02_BENT_"))==8
    assert all(len(o.data.vertices)>0 for o in mesh)
    write(OUT/"GLB_REOPEN.json",{"status":"PASS","mesh_objects":len(mesh),
                                 "approved_source_objects":len(approved),
                                 "corner_master_references":len(corners)})
    print("C02_GLB_REOPEN_PASS",len(mesh))
if __name__=="__main__":
    v=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser()
    p.add_argument("--mode",required=True,choices=("build","check-blend","check-glb"))
    a=p.parse_args(v)
    if a.mode=="build":build()
    elif a.mode=="check-blend":reopen_blend()
    else:reopen_glb()
