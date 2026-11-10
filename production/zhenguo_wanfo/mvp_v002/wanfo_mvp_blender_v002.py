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
OUTROOT = ROOT / "production/zhenguo_wanfo/mvp_v002"
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


def stitched_xieshan_roof(xridge, xeave, yshoulder, yeave, zridge, zshoulder, zeave,
                          roof_col, roof_material, gable_material):
    """Connected hip-and-gable roof skin with a shared vertex graph.
    Explicitly a source-guided *temporary* visual reconstruction, not A1 exact.
    Outer boundary is the four-eave rectangle, with 180mm corner rise.
    """
    points, faces, face_mats, index = [], [], [], {}
    upper_segs, lower_segs, cross_segs, hip_segs = 6, 8, 20, 20
    corner_rise = 180.0

    def vid(p):
        key = tuple(round(float(v), 6) for v in p)
        if key not in index:
            index[key] = len(points)
            points.append(list(key))
        return index[key]

    def face(poly, mat=0):
        ids = [vid(p) for p in poly]
        if len(set(ids)) < 3:
            return
        faces.append(ids)
        face_mats.append(mat)

    def strips(rows, mat=0):
        for a, b in zip(rows[:-1],rows[1:]):
            for j in range(len(a)-1):
                face((a[j],a[j+1],b[j+1],b[j]),mat)

    # Two long roof planes, with matching side boundaries and raised corners.
    for side in (-1,1):
        rows=[]
        for k in range(upper_segs+1):
            t=k/upper_segs
            y=side*yshoulder*t
            z=zridge+(zshoulder-zridge)*t
            rows.append([(xridge*(-1+2*j/cross_segs),y,z) for j in range(cross_segs+1)])
        for k in range(1,lower_segs+1):
            t=k/lower_segs
            half=xridge+(xeave-xridge)*t
            y=side*(yshoulder+(yeave-yshoulder)*t)
            rows.append([(half*(-1+2*j/cross_segs),y,
                          zshoulder*(1-t)+t*(zeave+corner_rise*abs(-1+2*j/cross_segs)**4))
                         for j in range(cross_segs+1)])
        strips(rows)

    # Hip planes close east and west ends. At inner edge, they share exactly
    # the gable base line; at both side edges, they share the long roof skin.
    for side in (-1,1):
        rows=[]
        for i in range(lower_segs+1):
            t=i/lower_segs
            x=side*(xridge+(xeave-xridge)*t)
            half_y=yshoulder+(yeave-yshoulder)*t
            rows.append([(x,half_y*(-1+2*j/hip_segs),
                          zshoulder*(1-t)+t*(zeave+corner_rise*abs(-1+2*j/hip_segs)**4))
                         for j in range(hip_segs+1)])
        strips(rows)

        # Triangulated gable fan shares *all* exact boundary vertices with the
        # adjacent long roof and hip meshes (no T-junction at the shoulder).
        perimeter=[]
        for i in range(upper_segs,-1,-1):
            t=i/upper_segs
            perimeter.append((side*xridge,-yshoulder*t,
                              zridge+(zshoulder-zridge)*t))
        for i in range(1,upper_segs+1):
            t=i/upper_segs
            perimeter.append((side*xridge,yshoulder*t,
                              zridge+(zshoulder-zridge)*t))
        for j in range(hip_segs-1,0,-1):
            u=-1+2*j/hip_segs
            perimeter.append((side*xridge,yshoulder*u,zshoulder))
        center=(side*xridge,0,zshoulder+430.0)
        for i in range(len(perimeter)):
            face((center,perimeter[i],perimeter[(i+1)%len(perimeter)]),mat=1)

    mesh=bpy.data.meshes.new("TMP_XIESHAN_STITCHED_V002_MESH")
    mesh.from_pydata(points,[],faces)
    mesh.update(calc_edges=True)
    mesh.materials.append(roof_material)
    mesh.materials.append(gable_material)
    for poly,mat_index in zip(mesh.polygons,face_mats):
        poly.material_index=mat_index
    ob=bpy.data.objects.new("TMP_XIESHAN_STITCHED_SURFACE_V002",mesh)
    roof_col.objects.link(ob)
    ob["mvp_evidence_class"]="TEMP_VISUAL_GEOMETRY_REPLACEABLE"
    ob["mvp_historical_accuracy"]="NOT_VERIFIED"
    ob["mvp_role"]="ROOF_STITCHED_CONTINUOUS_SURFACE_PROXY"
    ob["mvp_eave_x_mm"]=xeave
    ob["mvp_eave_y_mm"]=yeave
    ob["mvp_corner_rise_proxy_mm"]=corner_rise
    ob["mvp_source_note"]="External silhouette references pending A1 sheet comparison"
    return ob

def validate_roof_topology(ob):
    mesh=ob.data
    uses={}
    for poly in mesh.polygons:
        verts=list(poly.vertices)
        for a,b in zip(verts,verts[1:]+verts[:1]):
            e=tuple(sorted((a,b)))
            uses[e]=uses.get(e,0)+1
    overused=[edge for edge,n in uses.items() if n>2]
    assert not overused,f"ROOF_NONMANIFOLD_OVERUSED_EDGES_{len(overused)}"
    boundary=[e for e,n in uses.items() if n==1]
    assert boundary,"ROOF_BOUNDARY_NOT_FOUND"
    xlim=float(ob["mvp_eave_x_mm"])
    ylim=float(ob["mvp_eave_y_mm"])
    tolerance=.01
    for a,b in boundary:
        va=mesh.vertices[a].co
        vb=mesh.vertices[b].co
        on_perimeter=lambda v: abs(abs(v.x)-xlim)<tolerance or abs(abs(v.y)-ylim)<tolerance
        assert on_perimeter(va) and on_perimeter(vb), "ROOF_UNEXPECTED_INTERNAL_SEAM"
    assert len(boundary)==80, f"ROOF_EAVE_BOUNDARY_COUNT_{len(boundary)}_EXPECTED_80"
    return {"status":"PASS","roof_vertices":len(mesh.vertices),
            "roof_faces":len(mesh.polygons),"eave_boundary_edges":len(boundary),
            "non_manifold_overused_edges":len(overused),
            "unintended_open_internal_seams":0}

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
    original_roof_y_eave=abs(datum["roof_control"]["y_positions_mm"]["ROOF_PURLIN_N_00"])
    # V002 isolated visual override: external reference projection from column line.
    # DO NOT edit T-020 design datum or assert that this is A1 exact.
    visual_eave_projection_mm=2940.0
    yE=depth/2+visual_eave_projection_mm
    yShoulder=abs(datum["roof_control"]["y_positions_mm"]["ROOF_PURLIN_N_02"])
    assert abs(original_roof_y_eave-6808.5)<0.01 and abs(yE-8295.0)<0.01
    assert abs(yShoulder-3213)<0.01
    bpy.ops.wm.open_mainfile(filepath=str(APPROVED))
    src=[ob for ob in bpy.data.objects if ob.type=="MESH"]
    assert len(src)==63, f"APPROVED_SOURCE_OBJECT_COUNT_{len(src)}"
    src0=bounds(src)
    cx=(src0[0][0]+src0[1][0])/2
    cy=(src0[0][1]+src0[1][1])/2
    shift=[-cx,-cy,pval(params,"Z-006-RC-01")-(src0[0][2]+150.0)]
    for ob in src:
        ob.location.x += shift[0]
        ob.location.y += shift[1]
        ob.location.z += shift[2]
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
    assert abs(z0) < 0.001, "PROJECT_COLUMN_FOOT_DATUM_NOT_ZERO"
    # Independent, replaceable V002 visual controls, pending direct A1 comparison.
    # Important: cannot be promoted to canonical historical measured coordinates.
    eave_z=5270.0
    ridge_z=8870.0
    shoulder_z=eave_z+(pval(params,"ROOF-007")+pval(params,"ROOF-008"))*pval(params,"MOD-002")
    assert abs(column_top-3534.3)<0.01
    assert abs(eave_z-column_top-1735.7)<0.01
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
    xe=width/2+visual_eave_projection_mm
    xs=middle/2+1350.0
    xr=xs
    roof_obj=stitched_xieshan_roof(xs,xe,yShoulder,yE,ridge_z,shoulder_z,eave_z,
                                   roof_col,roofmat,gablemat)
    roof_check=validate_roof_topology(roof_obj)
    if stage=="full":
        beam("TMP_ROOF_RIDGE",(-xr,0,ridge_z+80),(xr,0,ridge_z+80),180,roof_structure_col,"RIDGE_PURLIN_PROXY",wood)
        for side,label in [(-1,"N"),(1,"S")]:
            for band, yy, zz in [(0,yShoulder,shoulder_z),(1,yE,eave_z)]:
                beam(f"TMP_PURLIN_{label}_{band}",(-xe if band else -xs,side*yy,zz-100),
                     (xe if band else xs,side*yy,zz-100),165,roof_structure_col,"PURLIN_PROXY",wood)
            for i in range(17):
                x=-xs+(2*xs*i/16)
                beam(f"TMP_RAFTER_UP_{label}_{i}",(x,0,ridge_z-130),
                     (x,side*yShoulder,shoulder_z-130),110,roof_structure_col,"RAFTER_PROXY",wood)
                beam(f"TMP_RAFTER_LOW_{label}_{i}",(x,side*yShoulder,shoulder_z-130),
                     (x*xe/xs,side*yE,eave_z-130+180.0*abs(x/xs)**4),110,roof_structure_col,"RAFTER_PROXY",wood)
        # Temporary enclosed wall massing. Front and rear CENTER BAYS are
        # open-door bays per museum; surface detail is not a historic claim.
        wall_bottom=z0+140
        wall_top=column_top-140
        door_height=2550
        wall_height=wall_top-wall_bottom
        for facade,yy in (("FRONT",-depth/2-40),("REAR",depth/2+40)):
            for ix in range(3):
                centerx=(xgrid[ix]+xgrid[ix+1])*0.5
                baywidth=xgrid[ix+1]-xgrid[ix]-330
                if ix in (0,2):
                    cube(f"TMP_{facade}_WALL_{ix}",(centerx,yy,(wall_top+wall_bottom)/2),
                         (baywidth,160,wall_height),wall_col,"WALL_PANEL_PROXY",wallmat)
                else:
                    # Leave central door opening clear, with side jambs and lintel.
                    opening_width=2150.0
                    jambw=(baywidth-opening_width)/2
                    assert jambw>100
                    for side in (-1,1):
                        jambx=centerx+side*(opening_width/2+jambw/2)
                        cube(f"TMP_{facade}_DOOR_JAMB_{side}",(jambx,yy,(wall_top+wall_bottom)/2),
                             (jambw,160,wall_height),wall_col,"DOOR_WALL_JAMB_PROXY",wallmat)
                    headerheight=wall_top-door_height
                    assert headerheight>250
                    cube(f"TMP_{facade}_DOOR_HEADER",(centerx,yy,door_height+headerheight/2),
                         (opening_width,160,headerheight),wall_col,"DOOR_HEADER_PROXY",wallmat)
        for iy in range(3):
            yy=(ygrid[iy]+ygrid[iy+1])*0.5
            baylen=ygrid[iy+1]-ygrid[iy]-350
            for side in (-1,1):
                cube(f"TMP_SIDE_WALL_{side}_{iy}",(side*(width/2+40),yy,
                     (wall_top+wall_bottom)/2),(165,baylen,wall_height),
                     wall_col,"WALL_PANEL_PROXY",wallmat)
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
    blend=output/f"WANFO_{stage.upper()}_V002.blend"
    glb=output/f"WANFO_{stage.upper()}_V002.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False,compress=True)
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",export_extras=True)
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    report={
      "state":"BUILD_CREATED_REOPEN_PENDING",
      "roof_seam_check":roof_check,
      "visual_design_controls":{"eave_projection_from_column_mm":visual_eave_projection_mm,"eave_height_candidate_mm":eave_z,"ridge_height_candidate_mm":ridge_z,"control_source":"EXTERNAL_VISUAL_REFERENCE_PENDING_A1_DIRECT_VALIDATION","t020_canonical_eave_y_mm":original_roof_y_eave,"temporary_override":True},
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
    assert len(temp)>=(13 if stage=="proof" else 24), f"BLEND_TEMP_COUNT_INVALID_{len(temp)}"
    assert any("ROOF" in str(r) for r in roles),"BLEND_MISSING_ROOF"
    roofs=[o for o in temp if o.get("mvp_role")=="ROOF_STITCHED_CONTINUOUS_SURFACE_PROXY"]
    assert len(roofs)==1,"BLEND_MISSING_STITCHED_ROOF"
    roof_check=validate_roof_topology(roofs[0])
    assert len([o for o in temp if o.get("mvp_role")=="PERIMETER_COLUMN_DESIGN_PROXY"])==12
    assert bpy.context.scene.get("mvp_stage")==stage
    save_report(OUTROOT/stage/"BLEND_REOPEN_CHECK.json",
                {"status":"PASS","roof_seam_check":roof_check,"source_meshes":len(source),"temporary_meshes":len(temp),
                 "roof_present":True,"columns":12,"stage":stage})
    print("MVP_BLEND_REOPEN_PASS",stage,len(objs))

def check_glb(stage):
    filepath=OUTROOT/stage/f"WANFO_{stage.upper()}_V002.glb"
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(filepath))
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    sources=[o for o in meshes if o.get("mvp_evidence_class")=="APPROVED_63_ENTITY_RECONSTRUCTED_DESIGN"]
    temps=[o for o in meshes if o.get("mvp_evidence_class")=="TEMP_VISUAL_GEOMETRY_REPLACEABLE"]
    assert len(meshes)>=(76 if stage=="proof" else 90), f"GLB_TOO_FEW_OBJECTS_{len(meshes)}"
    assert len(sources)==63, f"GLB_SOURCE_COUNT_INVALID_{len(sources)}"
    assert len(temps)>=(13 if stage=="proof" else 24), f"GLB_TEMP_COUNT_INVALID_{len(temps)}"
    assert all(len(o.data.vertices)>0 for o in meshes), "GLB_EMPTY_MESH"
    assert len([o for o in temps if o.get("mvp_role")=="ROOF_STITCHED_CONTINUOUS_SURFACE_PROXY"])==1,"GLB_STITCHED_ROOF_NOT_FOUND"
    save_report(OUTROOT/stage/"GLB_REOPEN_CHECK.json",
                {"status":"PASS","mesh_count":len(meshes),"approved_mesh_count":len(sources),
                 "temporary_mesh_count":len(temps),"stage":stage})
    print("MVP_GLB_REOPEN_PASS",stage,len(meshes))

if __name__=="__main__":
    a=args()
    if a.mode=="build": build(a.stage)
    elif a.mode=="check-blend": check_blend(a.stage)
    else: check_glb(a.stage)
