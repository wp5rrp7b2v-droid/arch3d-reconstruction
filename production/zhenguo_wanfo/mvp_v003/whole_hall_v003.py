#!/usr/bin/env python3
"""Whole-hall spatial coordination V003: one editable COMPLETE building candidate.
Based on archived V002; preserve all 63 approved source meshes and roof geometry.
No local C01-style individual-gate escalation; every hypothesis is visible/tagged.
Master vertex shapes are copied verbatim; proposed assembly placements are NOT approved.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
from collections import Counter
import bpy
from mathutils import Vector

ROOT=Path.cwd()
BASE=ROOT/"production/zhenguo_wanfo"
V002=BASE/"mvp_v002/full/WANFO_FULL_V002.blend"
V002_REPORT=BASE/"mvp_v002/full/BUILD_REPORT.json"
OUT=BASE/"mvp_v003/full"
HUA=BASE/"component_library/masters/CMP-GONG-HUAGONG-001/CMP-GONG-HUAGONG-001_MASTER_SEMANTIC_V001.json"
LING=BASE/"component_library/masters/CMP-GONG-LINGGONG-001/CMP-GONG-LINGGONG-001_MASTER_SEMANTIC_V001.json"
ANG=BASE/"component_library/masters/CMP-GONG-ANG-001/CMP-GONG-ANG-001_MASTER_SEMANTIC_V001.json"
DOU=BASE/"component_library/masters/CMP-LUDOU-COLUMN-001/CMP-LUDOU-COLUMN-001_MASTER_SEMANTIC_V001.json"
PARAMS=BASE/"params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
DATUM=BASE/"build/P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_V001.json"

def hashfile(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()
def load(path):
    return json.loads(path.read_text(encoding="utf-8"))
def dump(path,val):
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(val,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
def obj_hash(o):
    h=hashlib.sha256()
    # local geometry, face topology, world position (not Material) stable across save/reload
    for v in o.data.vertices:
        h.update(",".join(f"{float(k):.4f}" for k in v.co).encode())
        h.update(b";")
    for poly in o.data.polygons:
        h.update(("-".join(map(str,poly.vertices))+";").encode())
    for row in o.matrix_world:
        h.update((",".join(f"{float(x):.4f}" for x in row)+";").encode())
    return h.hexdigest()
def coll(name):
    c=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c
def mat(name,rgb):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*rgb,1)
    m.use_nodes=True
    n=m.node_tree.nodes.get("Principled BSDF")
    if n: n.inputs["Base Color"].default_value=(*rgb,1)
    return m
def mesh_master(name,body,pos,yaw,material,c,which,tilt=0):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(body["geometry_vertices_mm"],[],body["geometry_faces"])
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    c.objects.link(ob)
    ob.location=pos
    ob.rotation_euler=(0,tilt,yaw)
    ob.data.materials.append(material)
    ob["v003_kind"]="APPROVED_MASTER_REFERENCE_WITH_UNAPPROVED_PLACEMENT"
    ob["v003_origin_master"]=which
    ob["v003_master_signature"]=body["semantic_geometry_signature"]
    ob["v003_placement_status"]="RECONSTRUCTED_DESIGN_HYPOTHESIS_UNVERIFIED"
    return ob
def cube(name,xyz,size,c,material,role):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
    ob=bpy.context.object
    ob.name=name
    ob.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for prior in list(ob.users_collection):prior.objects.unlink(ob)
    c.objects.link(ob)
    ob.data.materials.append(material)
    ob["v003_kind"]="TEMP_VISUAL_STRUCTURE_REPLACEABLE"
    ob["v003_role"]=role
    ob["v003_historical_accuracy"]="NOT_VERIFIED"
    return ob
def beam(name,a,b,thick,c,material,role):
    a,b=Vector(a),Vector(b)
    d=b-a
    if d.length<.01:return None
    o=cube(name,(a+b)*.5,(thick,thick,d.length),c,material,role)
    o.rotation_euler=d.to_track_quat("Z","Y").to_euler()
    return o
def seat(name,loc,z0,z1,c,material,kind):
    dz=z1-z0
    assert dz>0
    return cube(name,(loc[0],loc[1],(z0+z1)*.5),(240,240,dz),c,material,kind)
def look_at(cam,target):
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
def review(name,eye,target,scale,hide_collections):
    for coll_name in hide_collections:
        for ob in bpy.data.collections[coll_name].objects:ob.hide_render=True
    camdata=bpy.data.cameras.new("V003_"+name)
    ca=bpy.data.objects.new("V003_CAM_"+name,camdata)
    bpy.context.scene.collection.objects.link(ca)
    ca.location=Vector(eye)
    look_at(ca,target)
    ca.data.type="ORTHO"
    ca.data.ortho_scale=scale
    ca.data.clip_end=150000
    bpy.context.scene.camera=ca
    scene=bpy.context.scene
    scene.render.filepath=str(OUT/("WANFO_V003_"+name+".png"))
    bpy.ops.render.render(write_still=True)
    for coll_name in hide_collections:
        for ob in bpy.data.collections[coll_name].objects:ob.hide_render=False

def build():
    assert V002.is_file(), "ARCHIVED_V002_BLENDER_MISSING"
    rpt=load(V002_REPORT)
    assert hashfile(V002)==rpt["hashes"]["blend"], "ARCHIVED_V002_SHA256_FAILURE"
    src={k:load(p) for k,p in (("hua",HUA),("ling",LING),("ang",ANG),("dou",DOU))}
    pvals=load(PARAMS)["parameters"]
    rules=load(DATUM)
    assert src["hua"]["master_id"]=="CMP-GONG-HUAGONG-001_MASTER"
    assert src["ling"]["master_id"]=="CMP-GONG-LINGGONG-001_MASTER"
    assert src["ang"]["master_id"]=="CMP-GONG-ANG-001_MASTER"
    assert src["dou"]["master_id"]=="CMP-LUDOU-COLUMN-001_MASTER"
    assert rules["roof_control"]["shared_ridge_terminal"]=="ROOF_PURLIN_N_03"
    width=pvals["PM-011"]["value"];depth=pvals["PM-012"]["value"]
    assert width==11475 and depth==10710
    bpy.ops.wm.open_mainfile(filepath=str(V002))
    approved=[o for o in bpy.data.objects if o.type=="MESH" and
              o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"]
    assert len(approved)==63
    bpy.context.view_layer.update()
    exact_before={o.name:obj_hash(o) for o in approved}
    # Delete V002 temporary schematic staircase, old simplistic framing/rafters,
    # not its roof shell, approved 63 bents, perimeter 12 columns, or wall proxy.
    removed=Counter()
    for o in list(bpy.data.objects):
        if o in approved or o.type!="MESH":continue
        remove=bool(o.get("v003_kind")) or o.name.startswith((
            "TMP_DG_","TMP_PURLIN_","TMP_RAFTER_","TMP_ROOF_RIDGE",
            "TMP_FRAME_","TMP_RIM_"))
        if remove:
            removed["bracket_and_frame_proxies"]+=1
            bpy.data.objects.remove(o,do_unlink=True)
    bpy.context.view_layer.update()
    assert {o.name:obj_hash(o) for o in approved}==exact_before, "SOURCE_INTEGRITY_AFTER_DELETE"
    roof=[o for o in bpy.data.objects if o.type=="MESH" and
          o.get("mvp_role")=="ROOF_STITCHED_CONTINUOUS_SURFACE_PROXY"]
    columns=[o for o in bpy.data.objects if o.type=="MESH" and o.name.startswith("TMP_COLUMN_")]
    assert len(roof)==1 and len(columns)==12
    roofcol=roof[0].users_collection[0].name

    mwood=mat("V003 / Master profile reference",(0.50,0.29,0.14))
    mdou=mat("V003 / Dou profile source",(0.33,0.24,0.15))
    mlink=mat("V003 / Replaceable bearing timber",(0.41,0.26,0.16))
    mroof=mat("V003 / Rafter purlin temp",(0.25,0.29,0.28))
    mmark=mat("V003 / Unverified spacer",(0.54,0.29,0.22))
    mcol=coll("V003_MASTER_REFERENCES_PLACEMENT_NOT_APPROVED")
    cbr=coll("V003_HALL_BRACKET_SYSTEM_VISUAL_HYPOTHESES")
    cbeam=coll("V003_HALL_FRAMES_GLOBAL_CONNECTIVITY_TRIAL")
    cpurl=coll("V003_ROOF_PURLIN_RAFTER_COORDINATION_TRIAL")
    cmarks=coll("V003_UNRESOLVED_STRUCTURAL_LINKS_RED")

    hua1=next(b for b in src["hua"]["canonical_bodies"] if b["body_id"]=="JUMP_1_HUAGONG")
    hua2=next(b for b in src["hua"]["canonical_bodies"] if b["body_id"]=="JUMP_2_HUAGONG")
    tou=next(b for b in src["ang"]["canonical_bodies"] if b["body_id"]=="TOU_ANG")
    er=next(b for b in src["ang"]["canonical_bodies"] if b["body_id"]=="ER_ANG")
    ling=src["ling"]["canonical_body"]
    dou=src["dou"]["body"]
    assert hua1["semantic_geometry_signature"]=="565fcdef9335691e73dd0cbec5e5d98b561f3bdebdbd367951bcb7826dc8f19a"
    assert hua2["semantic_geometry_signature"]=="451511f0b131e36784baefa2011850a1f9381d3b2dc1fee629951b7f4099e001"
    assert ling["semantic_geometry_signature"]=="e54e0521271ba8f74d66b9f3ac8eb6de9fa2121b20ca6a732725ff55417fac61"
    assert tou["semantic_geometry_signature"]=="61a2bbb85fa5fc07ed9c37ce610f2aee0360f280c09f8317614b7a62f7819250"
    assert er["semantic_geometry_signature"]=="b778edc208d788c5f9fad0a19849ca33f3334e7c4e2656721279386528979678"
    # Canonical master is outer-envelope-only. Does NOT contain real slots.
    assert len(dou["geometry_vertices_mm"])==8
    xg=[-width/2,-2218.5,2218.5,width/2]
    yg=[-depth/2,-1836,1836,depth/2]
    ztop=3534.3; zeave=5270; zridge=8870
    # Layered visible topology: 2 hua + 2 ang groups. Missing true sockets and
    # exact top bearings are marked unknown; no structural-contact PASS asserted.
    head=0; arms=0; infill=0
    placement_ids=[]
    for ix,x in enumerate(xg):
        for iy,y in enumerate(yg):
            if ix not in (0,3) and iy not in (0,3):continue
            head+=1
            mesh_master(f"V003_COLUMN_DOU_{ix}_{iy}",dou,(x,y,ztop),0,mdou,mcol,
                        "CMP-LUDOU-COLUMN-001")
            dirs=[]
            if ix==0: dirs.append((-1,0))
            if ix==3: dirs.append((1,0))
            if iy==0: dirs.append((0,-1))
            if iy==3: dirs.append((0,1))
            for dx,dy in dirs:
                arms+=1
                yaw=math.atan2(dy,dx)
                arm=f"{ix}_{iy}_{dx}_{dy}"
                anchor=(x,y)
                first=ztop+293.8
                hh=hua1["resolved_dimensions_mm"]["thickness"]
                mesh_master("V003_HUA1_"+arm,hua1,(x+dx*160,y+dy*160,first+hh/2),
                            yaw,mwood,mcol,"CMP-GONG-HUAGONG-001/JUMP1")
                seat("V003_SMALL_DOU1_"+arm,(x+dx*280,y+dy*280),first+hh,first+hh+110,
                     cbr,mdou,"SMALL_DOU_GEOMETRY_UNVERIFIED")
                second=first+hh+110
                hh2=hua2["resolved_dimensions_mm"]["thickness"]
                mesh_master("V003_HUA2_"+arm,hua2,(x+dx*285,y+dy*285,second+hh2/2),
                            yaw,mwood,mcol,"CMP-GONG-HUAGONG-001/JUMP2")
                seat("V003_SMALL_DOU2_"+arm,(x+dx*420,y+dy*420),second+hh2,second+hh2+100,
                     cbr,mdou,"SMALL_DOU_GEOMETRY_UNVERIFIED")
                # The two ang are profile-true master references but their
                # placement/angle belongs only to this whole-hall candidate.
                mesh_master("V003_TOU_ANG_"+arm,tou,
                    (x+dx*550,y+dy*550,second+hh2+195),
                    yaw,mwood,mcol,"CMP-GONG-ANG-001/TOU",
                    tilt=-math.radians(24.0755))
                mesh_master("V003_ER_ANG_"+arm,er,
                    (x+dx*690,y+dy*690,second+hh2+345),
                    yaw,mwood,mcol,"CMP-GONG-ANG-001/ER",
                    tilt=-math.radians(24.0755))
                # Upper trim: candidate only. Not claimed contact with the Ang
                # skins and not an exact historical bearer.
                beam("V003_TIE_TO_EAVE_"+arm,
                    (x+dx*650,y+dy*650,4710),
                    (x+dx*650,y+dy*650,zeave-310),185,cbr,mlink,
                    "GLOBAL_VISUAL_BEARING_PLACEHOLDER_NOT_APPROVED")
                placement_ids.append(arm)
    # Intercolumn: 3 per side (12). A visibly simpler 2-jump group; no
    # unsupported first-to-eave direct bearing assertion.
    for side in (-1,1):
        for k in range(3):
            xc=(xg[k]+xg[k+1])/2
            yc=(yg[k]+yg[k+1])/2
            for x,y,dx,dy,label in [
                (xc,side*depth/2,0,side,"N" if side>0 else "S"),
                (side*width/2,yc,side,0,"E" if side>0 else "W")
            ]:
                infill+=1
                t=f"{label}_{k}"
                yaw=math.atan2(dy,dx)
                cube("V003_INFILL_BEAM_BASE_"+t,(x,y,ztop+190),(570,340,240),
                     cbr,mlink,"INTERCOLUMN_LOCAL_BASE_NOT_SURVEYED")
                seat("V003_INFILL_DOU_"+t,(x,y),ztop+310,ztop+510,cbr,mdou,
                     "INTERCOLUMN_DOU_REPLACEABLE")
                mesh_master("V003_INFILL_HUA_"+t,hua1,
                            (x+dx*180,y+dy*180,ztop+510+76.5),
                            yaw,mwood,mcol,"HUAGONG_REFERENCE_VIZ_INFILL_NOT_EXACT")
                mesh_master("V003_INFILL_LING_"+t,ling,
                            (x,y,ztop+510+153+77.8),0,mwood,mcol,
                            "LINGGONG_REFERENCE_VIZ_INFILL_NOT_EXACT")
                beam("V003_INFILL_UPPER_TIE_"+t,(x,y,ztop+900),
                     (x,y,zeave-310),160,cbr,mlink,
                     "GLOBAL_INFILL_UPPER_PATH_REPLACEABLE")
    assert head==12 and arms==16 and infill==12

    # Put ring BEARING framework into the right roof / wall coordinates.
    # Roof EAVE (y±8295,x±8677.5,z=5270) is NOT over column lines.
    # Therefore direct vertical column-to-eave is *invalid*: the 2.94m
    # outboard eave is carried by extended rafters beyond a nearer line.
    ring_z=zeave-210
    for side,ylab in ((-1,"S"),(1,"N")):
        y=side*depth/2
        beam("V003_FRONT_BACK_RING_"+ylab,(-width/2,y,ring_z),
             (width/2,y,ring_z),260,cbeam,mlink,"PERIMETER_BEARING_RING_PROXY")
    for side,xlab in ((-1,"W"),(1,"E")):
        x=side*width/2
        beam("V003_SIDE_RING_"+xlab,(x,-depth/2,ring_z),
             (x,depth/2,ring_z),260,cbeam,mlink,"PERIMETER_BEARING_RING_PROXY")
    # Original source 63 holds middle two frames; only add outer frame
    # silhouettes, so not duplicate or alter the approved original geometry.
    for side,label in ((-1,"W"),(1,"E")):
        x=side*width/2
        beam("V003_OUTER_BENT_LOWER_"+label,(x,-depth/2,ztop+560),
             (x,depth/2,ztop+560),260,cbeam,mlink,"OUTER_FRAME_BEAM_DESIGN_PROXY")
        beam("V003_OUTER_BENT_RAFTER_N_"+label,(x,0,zridge-540),
             (x,4972.5,6700),160,cbeam,mroof,"OUTER_FRAME_SLOPING_DESIGN_PROXY")
        beam("V003_OUTER_BENT_RAFTER_S_"+label,(x,0,zridge-540),
             (x,-4972.5,6700),160,cbeam,mroof,"OUTER_FRAME_SLOPING_DESIGN_PROXY")

    # V002 roof is a continuous xieshan surface: keep original mesh untouched.
    # Add 7 project-datum purlin guide lines and tiered rafters below roof:
    # source D-284 purlin Y control (not true measured outer profile).
    yshoulder=3213.; yout=8295.; xs=3568.5; xe=width/2+2940
    zshoulder=zeave+(88+61)*15.3
    def roof_z(y):
        a=abs(y)
        if a<=yshoulder:
            return zridge-(zridge-zshoulder)*a/yshoulder
        return zshoulder-(zshoulder-zeave)*(a-yshoulder)/(yout-yshoulder)
    def roof_half_x(y):
        if abs(y)<=yshoulder:return xs
        return xs+(xe-xs)*(abs(y)-yshoulder)/(yout-yshoulder)
    control_y=[-6808.5,-4972.5,-3213.,0.,3213.,4972.5,6808.5]
    purlin_positions=[]
    for i,y in enumerate(control_y):
        span=roof_half_x(y)-200
        z=roof_z(y)-160
        beam("V003_PURLIN_%02d"%i,(-span,y,z),(span,y,z),
             185,cpurl,mroof,"DATUM_PURLIN_PROXY_Y_"+str(y))
        purlin_positions.append({"y_mm":y,"z_mm":z,"half_span_mm":span})
    # Rafters at 13 intervals per slope, genuinely reach the 2.94 m eave.
    # Hip corner rafters remain candidate; the continuous skin is unchanged.
    nraf=0
    for side in (-1,1):
        for i in range(17):
            x=xs*(-1+2*i/16)
            for a,b in zip([0.,3213.,4972.5,6808.5],
                           [3213.,4972.5,6808.5,8295.]):
                x0=x*(roof_half_x(a)/xs)
                x1=x*(roof_half_x(b)/xs)
                beam("V003_RAFTER_%s_%02d_%04d"%(("N" if side>0 else "S"),i,int(a)),
                    (x0,side*a,roof_z(a)-140),
                    (x1,side*b,roof_z(b)-140),
                    105,cpurl,mroof,"CONTINUOUS_ROOF_SUPPORT_VISUAL_PROXY")
                nraf+=1
    assert nraf==136
    # Two limits are explicitly unverified, not fabricated as completed joinery.
    # Instead of fake C01 1.13m filler, record a whole-hall support-path TODO
    # and structural intersections as hypothesis pending A1 confirmation.
    unresolved=[
      "Perimeter column-head upper bearer to inboard roof-purlin/roof-frame: local joinery unknown",
      "Full column-head seven-puzuo and intercolumn five-puzuo are visual/topological references only",
      "Approved 63 entity bents are preserved; their contacts to new proxy roof support unverified",
      "V002 roof elevations and 2.94m eave are provisional controls pending A1 direct comparison",
      "Corner assemblies and angled bearing cannot claim accurate historical geometry",
      "No loading, earthquake, deformation or hidden mortise-tenon structural proof"
    ]
    bpy.context.view_layer.update()
    assert {o.name:obj_hash(o) for o in approved}==exact_before, "SOURCE_MESH_OR_TRANSFORM_CHANGED"
    OUT.mkdir(parents=True,exist_ok=True)
    scene=bpy.context.scene
    scene["v003_status"]="CANDIDATE_ONLY_NOT_APPROVED"
    scene["v003_assembly_authority"]="WHOLE_HALL_MVP_3D_COORDINATION_ONLY"
    scene["v003_root_source_sha"]=hashfile(V002)
    scene["v003_structural_load_bearing_gate"]="UNKNOWN_NOT_TESTED"
    scene.render.engine="BLENDER_WORKBENCH"
    scene.display.shading.light="STUDIO"
    scene.display.shading.color_type="MATERIAL"
    scene.render.resolution_x=1400
    scene.render.resolution_y=1000
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    views=[
      ("AXON",(21500,-24500,20300),(0,0,4200),27000,[]),
      ("EXTERIOR",(10200,-23600,12700),(0,0,4400),22000,[]),
      ("FRONT",(0,-27000,5600),(0,0,4750),18700,[]),
      ("SIDE",(27500,0,5700),(0,0,4750),19400,[]),
      ("ROOF",(15500,-15000,24000),(0,0,7800),22300,[]),
      ("INTERIOR",(13000,-19500,11500),(0,0,4900),19000,[roofcol]),
      ("STRUCTURE",(17000,-22000,14100),(0,0,5450),22000,[roofcol]),
    ]
    for name,eye,target,scale,hide in views:review(name,eye,target,scale,hide)
    bpy.context.view_layer.update()
    for o in bpy.data.objects:
        if o.type=="CAMERA":o.hide_render=True
    blend=OUT/"WANFO_FULL_V003.blend"
    glb=OUT/"WANFO_FULL_V003.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True,check_existing=False)
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",export_extras=True)
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    counters=Counter(o.get("v003_kind") or o.get("mvp_evidence_class") or "UNCLASSIFIED" for o in meshes)
    evidence={
     "state":"WHOLE_HALL_CANDIDATE_CREATED_REOPEN_PENDING",
     "scope":"COMPLETE_HALL_ONLY_NO_INDEPENDENT_LOCAL_GATE",
     "v002_source_sha256":hashfile(V002),
     "v002_source_approved_count":63,
     "v002_source_approved_signatures_before_after_equal":True,
     "master_semantic_sha256":{k:hashfile(path) for k,path in (("hua",HUA),("ling",LING),("ang",ANG),("dou",DOU))},
     "design_axis":{"x_width_mm":width,"y_depth_mm":depth,"column_count":head},
     "whole_hall_bracket_topology":{"column_head_puzuo":"七铺作双杪双下昂 - simplified source profile geometries",
                                    "intercolumn_puzuo":"五铺作双杪偷心 - simplified placeholder",
                                    "column_head_count":head,
                                    "column_head_outward_arm_groups":arms,
                                    "intercolumn_sets":infill,
                                    "front_back_and_side_distribution_complete":True},
     "roof_support":{"datum_y_mm":control_y,"purlins":purlin_positions,
                     "rafter_segment_count":nraf,
                     "eave_y_mm":yout,
                     "column_front_y_mm":depth/2,
                     "eave_offset_from_column_mm":yout-depth/2,
                     "direct_column_to_eave_contact_claim":False,
                     "roof_shell_v002_untouched":True},
     "model_count":{"mesh_objects":len(meshes),"by_evidence_group":dict(counters)},
     "structural_verification":"NOT_COMPLETE_VISUAL_GLOBAL_TOPOLOGY_CANDIDATE",
     "unverified_structural_links":unresolved,
     "technical_checks":{"approved_preservation":"PASS","column_count":"PASS",
                         "bracket_distribution":"PASS","roof_y_datum":"PASS",
                         "roof_stitched_surface":"INHERITED_V002_TECHNICAL_PASS",
                         "visible_support_contact":"NOT_TESTED","loads":"NOT_TESTED"},
     "files":{"blend":str(blend.relative_to(ROOT)),"glb":str(glb.relative_to(ROOT)),
              "views":[str((OUT/("WANFO_V003_"+n+".png")).relative_to(ROOT)) for n,*_ in views]},
     "sha256":{"blend":hashfile(blend),"glb":hashfile(glb)}
    }
    dump(OUT/"BUILD_REPORT.json",evidence)
    print("V003_WHOLE_HALL_BUILD_CREATED",json.dumps({k:evidence[k] for k in ("model_count","design_axis","roof_support")},ensure_ascii=False))
def check_blend():
    r=load(OUT/"BUILD_REPORT.json")
    assert bpy.context.scene["v003_status"]=="CANDIDATE_ONLY_NOT_APPROVED"
    objs=[o for o in bpy.data.objects if o.type=="MESH"]
    assert len(objs)==r["model_count"]["mesh_objects"]
    assert len([o for o in objs if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"])==63
    assert len([o for o in objs if o.get("v003_origin_master")])>=60
    assert sum(1 for o in objs if o.name.startswith("V003_PURLIN_"))==7
    dump(OUT/"BLEND_REOPEN_CHECK.json",{"status":"PASS","mesh_count":len(objs),
                                    "source_approved":63,"master_reference_instanced":
                                        sum(1 for o in objs if o.get("v003_origin_master"))})
    print("V003_BLEND_REOPEN_PASS",len(objs))
def check_glb():
    f=OUT/"WANFO_FULL_V003.glb"
    bpy.ops.import_scene.gltf(filepath=str(f))
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    assert sum(1 for o in meshes if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN")==63
    assert sum(1 for o in meshes if o.name.startswith("V003_PURLIN_"))==7
    assert sum(1 for o in meshes if o.get("v003_origin_master"))>=60
    dump(OUT/"GLB_REOPEN_CHECK.json",{"status":"PASS","mesh_count":len(meshes),
                                   "source_approved":63})
    print("V003_GLB_REOPEN_PASS",len(meshes))
if __name__=="__main__":
    arg=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("build","check-blend","check-glb"))
    mode=ap.parse_args(arg).mode
    if mode=="build":build()
    elif mode=="check-blend":check_blend()
    else:check_glb()
