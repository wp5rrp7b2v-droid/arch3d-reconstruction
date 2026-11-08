#!/usr/bin/env python3
"""Whole-hall MVP proof and candidate. Run ONLY in cloud Blender.
Approved 63-piece source geometry is read, never overwritten. All added geometry
is segregated as temporary / reconstructed design; no historical exactness claim.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path.cwd()
APPROVED = ROOT / "production/zhenguo_wanfo/assembly/approved_snapshots/2026-10-09/curved_gong_v002/WANFO_TWO_FRAMES_THREE_PURLINS_APPROVED_V002.blend"
EXPECTED_SHA = "fbcc8f4e025da9325fa5bf0d7b76f7c6267e796650eb19e651f0f27a58f70802"
OUTROOT = ROOT / "production/zhenguo_wanfo/mvp_v001"
PARAMS = ROOT / "production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
DATUM = ROOT / "production/zhenguo_wanfo/build/P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_V001.json"

def args():
    import sys
    argv = sys.argv
    argv = argv[argv.index("--")+1:] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["build", "check-blend", "check-glb"], required=True)
    parser.add_argument("--stage", choices=["proof", "full"], required=True)
    return parser.parse_args(argv)

def pval(table, k):
    if k == "Z-006-RC-01":
        return 3534.3   # approved replaceable rule, never a measured height
    return table["parameters"][k]["value"]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def new_col(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

def move_to(obj, col):
    for previous in list(obj.users_collection):
        previous.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    node = m.node_tree.nodes.get("Principled BSDF")
    if node:
        node.inputs["Base Color"].default_value = (*color, 1.0)
        node.inputs["Roughness"].default_value = 0.86
    return m

def register(obj, col, role, material):
    move_to(obj, col)
    obj["mvp_evidence_class"] = "TEMP_VISUAL_GEOMETRY_REPLACEABLE"
    obj["mvp_role"] = role
    obj["mvp_historical_accuracy"] = "NOT_VERIFIED"
    if material: obj.data.materials.append(material)
    return obj

def cube(name, center, size, col, role, material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj=bpy.context.object
    obj.name=name
    obj.dimensions=size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return register(obj,col,role,material)

def beam(name, start, end, thickness, col, role, material):
    start,end=Vector(start),Vector(end)
    direction=end-start
    obj=cube(name, (start+end)*0.5, (thickness,thickness,direction.length), col,role,material)
    obj.rotation_euler=direction.to_track_quat("Z","Y").to_euler()
    return obj

def column(name, x, y, z0, z1, radius, col, material):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=z1-z0, end_fill_type="NGON",
                                        location=(x,y,(z0+z1)/2))
    obj=bpy.context.object
    obj.name=name
    return register(obj,col,"PERIMETER_COLUMN_DESIGN_PROXY",material)

def roof_panel(name, verts, faces, col, material, role="ROOF_SHELL_XIESHAN_MASSING_PROXY"):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    ob["mvp_evidence_class"]="TEMP_VISUAL_GEOMETRY_REPLACEABLE"
    ob["mvp_historical_accuracy"]="NOT_VERIFIED"
    ob["mvp_role"]=role
    mesh.materials.append(material)
    return ob

def bounds(objects):
    pts=[o.matrix_world @ Vector(c) for o in objects for c in o.bound_box]
    return [[min(p[i] for p in pts) for i in range(3)],
            [max(p[i] for p in pts) for i in range(3)]]

def save_report(path, report):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def set_camera(scene, name, eye, target, orthoscale, camera_col):
    cam_data=bpy.data.cameras.new(name+"_DATA")
    cam=bpy.data.objects.new(name,cam_data)
    camera_col.objects.link(cam)
    cam.location=Vector(eye)
    delta=Vector(target)-cam.location
    cam.rotation_euler=delta.to_track_quat("-Z","Y").to_euler()
    cam.data.type="ORTHO"
    cam.data.ortho_scale=orthoscale
    cam.data.clip_end=200000
    scene.camera=cam
    return cam

def review_views(scene, roofcol, camcol, z0, ztop, stage):
    scene.render.engine="BLENDER_WORKBENCH"
    scene.display.shading.light="STUDIO"
    scene.display.shading.color_type="MATERIAL"
    scene.display.shading.show_shadows=True
    scene.render.resolution_x=1280
    scene.render.resolution_y=900
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    target_z=(z0+ztop)*0.5
    overview=[
        ("AXON",(19700,-21900,ztop+15000), (0,0,target_z),24000,False),
        ("EXTERIOR",(8000,-25500,ztop+5100),(0,0,target_z),20500,False)
    ]
    if stage=="full":
        overview.extend([
          ("INTERIOR",(12200,-18500,ztop+8000),(0,0,z0+4200),19000,True),
          ("ROOF",(16000,-14500,ztop+18000),(0,0,ztop-1000),21500,False)
        ])
    paths=[]
    for tag,eye,target,scale,hide_roof in overview:
        for obj in roofcol.objects:
            obj.hide_render=hide_roof
        set_camera(scene,"REVIEW_CAM_"+tag,eye,target,scale,camcol)
        path=OUTROOT/stage/(f"WANFO_{stage.upper()}_{tag}.png")
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        paths.append(str(path.relative_to(ROOT)))
    for obj in roofcol.objects: obj.hide_render=False
    return paths

def build(stage):
    assert APPROVED.exists(), "APPROVED_SOURCE_NOT_FOUND"
    actual=sha256(APPROVED)
    assert actual==EXPECTED_SHA, "APPROVED_SOURCE_SHA_MISMATCH"
    params=json.loads(PARAMS.read_text(encoding="utf-8"))
    datum=json.loads(DATUM.read_text(encoding="utf-8"))
    mm_per_chi=pval(params,"MOD-001")
    width=pval(params,"PM-011")
    depth=pval(params,"PM-012")
    side=pval(params,"PM-010")*mm_per_chi
    middle=pval(params,"PM-008")*mm_per_chi
    dep_side=pval(params,"PM-010")*mm_per_chi
    dep_middle=pval(params,"PM-009")*mm_per_chi
    assert abs(2*side+middle-width)<0.01, "GRID_X_NOT_CLOSED"
    assert abs(2*dep_side+dep_middle-depth)<0.01, "GRID_Y_NOT_CLOSED"
    assert pval(params,"PM-013")==12 and pval(params,"PM-014")==0
    assert datum["roof_control"]["shared_ridge_terminal"]=="ROOF_PURLIN_N_03"
    yE=abs(datum["roof_control"]["y_positions_mm"]["ROOF_PURLIN_N_00"])
    yShoulder=abs(datum["roof_control"]["y_positions_mm"]["ROOF_PURLIN_N_02"])
    assert abs(yE-6808.5)<0.01
    assert abs(yShoulder-3213)<0.01
    bpy.ops.wm.open_mainfile(filepath=str(APPROVED))
    src=[ob for ob in bpy.data.objects if ob.type=="MESH"]
    assert len(src)==63, f"APPROVED_SOURCE_OBJECT_COUNT_{len(src)}"
    src0=bounds(src)
    cx=(src0[0][0]+src0[1][0])/2
    cy=(src0[0][1]+src0[1][1])/2
    shift=[-cx,-cy,0.0]
    for ob in src:
        ob.location.x += shift[0]
        ob.location.y += shift[1]
        ob["mvp_evidence_class"]="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"
        ob["mvp_source_sha256"]=actual
        ob["mvp_scope"]="TWO_FRAMES_THREE_PURLINS_NOT_WHOLE_BUILDING"
        ob.hide_render=False
    bpy.context.view_layer.update()
    srcbox=bounds(src)
    span=[srcbox[1][i]-srcbox[0][i] for i in range(3)]
    assert 200 < max(span) < 25000, f"APPROVED_SOURCE_UNEXPECTED_SCALE_{span}"
    source_col=new_col("APPROVED_SOURCE_V002_63_ENTITIES")
    for ob in src: source_col.objects.link(ob)
    proxy_col=new_col("TEMP_STRUCTURE_PROXIES_NOT_APPROVED")
    dg_col=new_col("TEMP_BRACKET_PROXIES_NOT_APPROVED")
    roof_col=new_col("TEMP_ROOF_SHELL_NOT_APPROVED")
    roof_structure_col=new_col("TEMP_ROOF_SUPPORT_NOT_APPROVED")
    wall_col=new_col("TEMP_WALL_PANELS_NOT_APPROVED")
    cameras_col=new_col("MVP_REVIEW_CAMERAS")
    wood=mat("Warm timber / design proxy",(0.39,0.22,0.12))
    columnmat=mat("Column timber / design proxy",(0.30,0.18,0.10))
    bracketmat=mat("Bracket timber / NOT APPROVED",(0.48,0.30,0.15))
    roofmat=mat("Roof dark-grey / visual proxy",(0.20,0.29,0.29))
    gablemat=mat("Gable timber / visual proxy",(0.43,0.27,0.15))
    wallmat=mat("Masonry vermilion / visual proxy",(0.48,0.22,0.18))
    xgrid=[-width/2,-middle/2,middle/2,width/2]
    ygrid=[-depth/2,-dep_middle/2,dep_middle/2,depth/2]
    xy=[]
    for ix,x in enumerate(xgrid):
        for iy,y in enumerate(ygrid):
            if ix in (0,3) or iy in (0,3): xy.append((ix,iy,x,y))
    assert len(xy)==12
    column_top=srcbox[0][2]+150.0
    z0=column_top-pval(params,"Z-006-RC-01")
    dgheight=max(1200.0, min(2400.0,srcbox[1][2]-column_top+250.0))
    eave_z=max(column_top+dgheight,srcbox[1][2]+250)
    ridge_z=eave_z+pval(params,"ROOF-011")
    shoulder_z=eave_z+(pval(params,"ROOF-007")+pval(params,"ROOF-008"))*pval(params,"MOD-002")
    assert shoulder_z<ridge_z and eave_z<shoulder_z
    for ix,iy,x,y in xy:
        column(f"TMP_COLUMN_{ix}_{iy}",x,y,z0,column_top,
                pval(params,"Z-002")/2,proxy_col,columnmat)
        if stage=="full":
            cube(f"TMP_DG_DOU_{ix}_{iy}",(x,y,column_top+185),(550,550,260),dg_col,"DOU_BLOCK_PROXY",bracketmat)
            beam(f"TMP_DG_GONG_X_{ix}_{iy}",(x-650,y,column_top+410),(x+650,y,column_top+410),245,dg_col,"BRACKET_CROSS_ARM_X_PROXY",bracketmat)
            beam(f"TMP_DG_GONG_Y_{ix}_{iy}",(x,y-650,column_top+620),(x,y+650,column_top+620),245,dg_col,"BRACKET_CROSS_ARM_Y_PROXY",bracketmat)
            beam(f"TMP_DG_TOP_{ix}_{iy}",(x,y,column_top+730),(x,y,eave_z-100),220,dg_col,"BRACKET_VISUAL_SUPPORT_PROXY",bracketmat)
    if stage=="full":
        for i in (0,3):
            beam("TMP_RIM_X_"+str(i),(xgrid[0],ygrid[i],column_top),
                 (xgrid[3],ygrid[i],column_top),280,proxy_col,"PERIMETER_RIM_BEAM_PROXY",wood)
            beam("TMP_RIM_Y_"+str(i),(xgrid[i],ygrid[0],column_top),
                 (xgrid[i],ygrid[3],column_top),280,proxy_col,"PERIMETER_RIM_BEAM_PROXY",wood)
        for iy,y in enumerate(ygrid):
            beam("TMP_FRAME_X_"+str(iy),(xgrid[0],y,column_top+900),
                 (xgrid[3],y,column_top+900),280,proxy_col,"TRANSVERSE_BEAM_PROXY",wood)
        for ix,x in enumerate(xgrid):
            beam("TMP_FRAME_Y_"+str(ix),(x,ygrid[0],column_top+850),
                 (x,ygrid[3],column_top+850),240,proxy_col,"LONGITUDINAL_BEAM_PROXY",wood)
    xe=width/2+950.0
    xs=width/2-650.0
    xr=middle/2+1350.0
    # A deliberately simplified single-eave hip-and-gable volume. These panels
    # are design proxies; their eave corner curvature, tiles and hidden build-up
    # are not interpreted as measured geometry.
    for sn,label in [(-1,"N"),(1,"S")]:
        yout=sn*yE
        yin=sn*yShoulder
        verts=[(-xr,0,ridge_z),(xr,0,ridge_z),
               (xs,yin,shoulder_z),(-xs,yin,shoulder_z),
               (xe,yout,eave_z),(-xe,yout,eave_z)]
        roof_panel("TMP_ROOF_UPPER_"+label,verts,[(0,1,2,3)],roof_col,roofmat)
        roof_panel("TMP_ROOF_LOWER_"+label,verts,[(3,2,4,5)],roof_col,roofmat)
    for sign,label in [(-1,"W"),(1,"E")]:
        verts=[(sign*xr,0,ridge_z),(sign*xs,-yShoulder,shoulder_z),
               (sign*xs,yShoulder,shoulder_z),
               (sign*xe,-yE,eave_z),(sign*xe,yE,eave_z)]
        roof_panel("TMP_XIESHAN_GABLE_"+label,verts,[(0,1,2)],roof_col,gablemat,"UPPER_GABLE_PROXY")
        roof_panel("TMP_XIESHAN_HIP_"+label,verts,[(1,3,4,2)],roof_col,roofmat,"LOWER_HIP_PROXY")
    if stage=="full":
        beam("TMP_ROOF_RIDGE",(-xr,0,ridge_z+80),(xr,0,ridge_z+80),180,roof_structure_col,"RIDGE_PURLIN_PROXY",wood)
        for side,label in [(-1,"N"),(1,"S")]:
            for band, yy, zz in [(0,yShoulder,shoulder_z),(1,yE,eave_z)]:
                beam(f"TMP_PURLIN_{label}_{band}",(-xs,side*yy,zz-100),
                     (xs,side*yy,zz-100),165,roof_structure_col,"PURLIN_PROXY",wood)
            for i in range(17):
                x=-xs+(2*xs*i/16)
                beam(f"TMP_RAFTER_UP_{label}_{i}",(x,0,ridge_z-130),
                     (x,side*yShoulder,shoulder_z-130),110,roof_structure_col,"RAFTER_PROXY",wood)
                beam(f"TMP_RAFTER_LOW_{label}_{i}",(x,side*yShoulder,shoulder_z-130),
                     (x,side*yE,eave_z-130),110,roof_structure_col,"RAFTER_PROXY",wood)
        # Walls are intentionally incomplete and optional: model remains accessible
        # for interior review. No historical wall detail is asserted.
        for ix in range(3):
            xx=(xgrid[ix]+xgrid[ix+1])*0.5
            ww=xgrid[ix+1]-xgrid[ix]-340
            cube(f"TMP_REAR_WALL_{ix}",(xx,depth/2+60,z0+1000),
                 (ww,175,2000),wall_col,"WALL_PANEL_PROXY",wallmat)
        for iy in range(3):
            yy=(ygrid[iy]+ygrid[iy+1])*0.5
            hh=ygrid[iy+1]-ygrid[iy]-350
            for side in (-1,1):
                cube(f"TMP_SIDE_WALL_{side}_{iy}",(side*(width/2+40),yy,z0+1000),
                     (145,hh,2000),wall_col,"WALL_PANEL_PROXY",wallmat)
        # South front has an open middle bay (visitor entrance).
        for ix in (0,2):
            xx=(xgrid[ix]+xgrid[ix+1])*0.5
            ww=xgrid[ix+1]-xgrid[ix]-330
            cube(f"TMP_FRONT_WALL_{ix}",(xx,-depth/2-50,z0+900),
                 (ww,155,1800),wall_col,"FRONT_PANEL_PROXY",wallmat)
    output=OUTROOT/stage
    output.mkdir(parents=True,exist_ok=True)
    for ob in bpy.context.selected_objects: ob.select_set(False)
    bpy.context.view_layer.update()
    scene=bpy.context.scene
    scene.unit_settings.system="METRIC"
    scene.unit_settings.scale_length=0.001
    for ob in bpy.data.objects:
        if ob.type=="MESH": ob.hide_render=False
    scene["mvp_status"]="CANDIDATE_NOT_APPROVED"
    scene["mvp_stage"]=stage
    scene["source_sha256"]=actual
    scene["design_dim_mm"]=[width,depth]
    scene["roof_type"]="SINGLE_EAVE_XIESHAN_TEMP_VISUAL_PROXY"
    # Review images are rendered before saves, with final roof visibility restored.
    imgs=review_views(scene,roof_col,cameras_col,z0,ridge_z,stage)
    for ob in roof_col.objects: ob.hide_render=False
    blend=output/f"WANFO_{stage.upper()}_V001.blend"
    glb=output/f"WANFO_{stage.upper()}_V001.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False,compress=True)
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",export_extras=True)
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    report={
      "state":"BUILD_CREATED_REOPEN_PENDING",
      "stage":stage,"source_sha256":actual,"source_count":len(src),
      "source_origin_shift_mm":shift,"source_bbox_after_shift_mm":srcbox,
      "source_span_mm":span,"source_identity":"D-285 V002 / D-286",
      "approved_geometry_modified":False,
      "candidate_design_dimensions_mm":{"width":width,"depth":depth},
      "column_count":len(xy),"roof_type":"single_eave_xieshan_proxy",
      "component_counts":{"mesh_objects":len(meshes),"temporary_meshes":len(meshes)-len(src)},
      "datum":{"column_foot_z_mm":z0,"column_top_z_mm":column_top,
               "eave_z_mm":eave_z,"ridge_z_mm":ridge_z,
               "ridge_y_mm":0,"north_eave_y_mm":-yE,"south_eave_y_mm":yE},
      "unverified":["precise original 963 geometry","walls and tilework",
                    "all hidden joints","original common datum from approved local assembly",
                    "load capacity","detailed dougong identity"],
      "deliverables":{"blend":str(blend.relative_to(ROOT)),
                       "glb":str(glb.relative_to(ROOT)),"review_images":imgs},
      "hashes":{"blend":sha256(blend),"glb":sha256(glb)}
    }
    save_report(output/"BUILD_REPORT.json",report)
    print("MVP_BUILD_CREATED",stage,json.dumps(report,ensure_ascii=False))
    
def check_blend(stage):
    objs=[o for o in bpy.data.objects if o.type=="MESH"]
    source=[o for o in objs if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"]
    temp=[o for o in objs if o.get("mvp_evidence_class")=="TEMP_VISUAL_GEOMETRY_REPLACEABLE"]
    roles={o.get("mvp_role") for o in temp}
    assert len(source)==63,f"BLEND_SOURCE_COUNT_INVALID_{len(source)}"
    assert len(temp)>=24, f"BLEND_TEMP_COUNT_INVALID_{len(temp)}"
    assert any("ROOF" in str(r) for r in roles),"BLEND_MISSING_ROOF"
    assert len([o for o in temp if o.get("mvp_role")=="PERIMETER_COLUMN_DESIGN_PROXY"])==12
    assert bpy.context.scene.get("mvp_stage")==stage
    save_report(OUTROOT/stage/"BLEND_REOPEN_CHECK.json",
                {"status":"PASS","source_meshes":len(source),"temporary_meshes":len(temp),
                 "roof_present":True,"columns":12,"stage":stage})
    print("MVP_BLEND_REOPEN_PASS",stage,len(objs))

def check_glb(stage):
    filepath=OUTROOT/stage/f"WANFO_{stage.upper()}_V001.glb"
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(filepath))
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    sources=[o for o in meshes if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"]
    temps=[o for o in meshes if o.get("mvp_evidence_class")=="TEMP_VISUAL_GEOMETRY_REPLACEABLE"]
    assert len(meshes)>=90, f"GLB_TOO_FEW_OBJECTS_{len(meshes)}"
    assert len(sources)==63, f"GLB_SOURCE_COUNT_INVALID_{len(sources)}"
    assert len(temps)>=24, f"GLB_TEMP_COUNT_INVALID_{len(temps)}"
    assert all(len(o.data.vertices)>0 for o in meshes), "GLB_EMPTY_MESH"
    save_report(OUTROOT/stage/"GLB_REOPEN_CHECK.json",
                {"status":"PASS","mesh_count":len(meshes),"approved_mesh_count":len(sources),
                 "temporary_mesh_count":len(temps),"stage":stage})
    print("MVP_GLB_REOPEN_PASS",stage,len(meshes))

if __name__=="__main__":
    a=args()
    if a.mode=="build": build(a.stage)
    elif a.mode=="check-blend": check_blend(a.stage)
    else: check_glb(a.stage)
