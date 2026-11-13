"""C01: focused column-head / intercolumn / eave minimum proof.
Only formal Master semantic vertices/faces are used for named Master silhouettes.
The 63-entity D-285 local frame is NOT a column-head and is not transplanted.
A visible unsupported interface means FAIL; never auto-promote to assembled.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path.cwd()
OUT=ROOT/"production/zhenguo_wanfo/mvp_detail_c01"
MASTER_ROOT=ROOT/"production/zhenguo_wanfo/component_library/masters"
COL=MASTER_ROOT/"CMP-LUDOU-COLUMN-001/CMP-LUDOU-COLUMN-001_MASTER_SEMANTIC_V001.json"
HUA=MASTER_ROOT/"CMP-GONG-HUAGONG-001/CMP-GONG-HUAGONG-001_MASTER_SEMANTIC_V001.json"
LING=MASTER_ROOT/"CMP-GONG-LINGGONG-001/CMP-GONG-LINGGONG-001_MASTER_SEMANTIC_V001.json"
SHA={"COL":"98d34a3d1de850106e8a7715dd75dd8d4a80a80680dbf7cc89de4858315aa56a",
     "HUA":"565fcdef9335691e73dd0cbec5e5d98b561f3bdebdbd367951bcb7826dc8f19a",
     "LING":"e54e0521271ba8f74d66b9f3ac8eb6de9fa2121b20ca6a732725ff55417fac61"}
def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for buf in iter(lambda:f.read(1024*1024),b""):h.update(buf)
    return h.hexdigest()
def load(path):
    return json.loads(path.read_text(encoding="utf-8"))
def save(name,value):
    path=OUT/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
def mat(name,rgb):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*rgb,1)
    m.use_nodes=True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*rgb,1)
    return m
def tagged(obj,status,origin):
    obj["component_status"]=status
    obj["source_reference"]=origin
    obj["historical_accuracy"]="NOT_VERIFIED"
    return obj
def mesh_object(name,body,location,orientation,material,origin):
    verts=body["geometry_vertices_mm"]; faces=body["geometry_faces"]
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update(calc_edges=True)
    o=bpy.data.objects.new(name,mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location=location
    o.rotation_euler[2]=orientation
    o.data.materials.append(material)
    o["canonical_master_body_signature"]=body["semantic_geometry_signature"] if "semantic_geometry_signature" in body else SHA["COL"]
    tagged(o,"APPROVED_MASTER_GEOMETRY_USED_AS_UNVERIFIED_ASSEMBLY_INSTANCE",origin)
    return o
def cube(name,xyz,size,material,role):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
    obj=bpy.context.object
    obj.name=name
    obj.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    obj.data.materials.append(material)
    tagged(obj,"TEMP_VISUAL_AND_CONNECTION_PROXY",role)
    return obj
def pole(name,x,y,z0,z1,r,material):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=z1-z0,location=(x,y,(z0+z1)/2))
    o=bpy.context.object; o.name=name
    o.data.materials.append(material)
    tagged(o,"TEMP_COLUMN_DIMENSIONAL_PROXY","Z-002 / Z-006-RC-01 / not historical exact")
    return o
def mesh_local_low_vertices(ob):
    bpy.context.view_layer.update()
    pts=[ob.matrix_world @ v.co for v in ob.data.vertices]
    bottom=min(p.z for p in pts)
    return [p for p in pts if abs(p.z-bottom)<.01],bottom
def bottom_seat_check(upper,lower,lower_top,tol=.02):
    foot,z=mesh_local_low_vertices(upper)
    bmin,bmax=lower_top
    inside=[p for p in foot if bmin[0]-tol<=p.x<=bmax[0]+tol and bmin[1]-tol<=p.y<=bmax[1]+tol]
    return {"foot_vertices":len(foot),"foot_vertices_inside_support_footprint":len(inside),
            "bottom_mm":z,"support_top_mm":lower,"support_delta_mm":z-lower,
            "pass": len(foot)>=4 and len(inside)>=4 and abs(z-lower)<=tol}
def look_at(o,target):
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
def camera(label,eye,target,scale):
    bpy.ops.object.camera_add(location=eye)
    o=bpy.context.object;o.name="CAM_"+label;look_at(o,target)
    o.data.type="ORTHO";o.data.ortho_scale=scale;o.data.clip_end=100000
    bpy.context.scene.camera=o
    return o
def render(name,eye,target,scale):
    camera(name,eye,target,scale)
    scene=bpy.context.scene
    scene.render.filepath=str(OUT/("C01_"+name+".png"))
    bpy.ops.render.render(write_still=True)
def verify_master(s):
    for key,expect in SHA.items():
        assert s["COL"]["semantic_geometry_signature"]==SHA["COL"] if key=="COL" else True
    assert s["HUA"]["canonical_bodies"][0]["semantic_geometry_signature"]==SHA["HUA"]
    assert s["LING"]["canonical_body"]["semantic_geometry_signature"]==SHA["LING"]
    assert s["HUA"]["master_id"]=="CMP-GONG-HUAGONG-001_MASTER"
    assert s["LING"]["master_id"]=="CMP-GONG-LINGGONG-001_MASTER"
    assert s["COL"]["master_id"]=="CMP-LUDOU-COLUMN-001_MASTER"
    return {k:digest(v) for k,v in (("COL",COL),("HUA",HUA),("LING",LING))}
def build():
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    src={k:load(p) for k,p in (("COL",COL),("HUA",HUA),("LING",LING))}
    shas=verify_master(src)
    wood=mat("Column / temporary",(0.36,0.21,0.11))
    master=mat("Approved Master profile / tentative position",(0.52,0.31,0.11))
    temp=mat("Unverified infill and eave",(0.30,0.36,0.37))
    marker=mat("Unresolved gap highlight",(0.68,0.24,0.18))
    xpost=-2218.5
    xnext=2218.5
    xinter=0.0
    yfront=-5355.0
    column_top=3534.3
    for x,label in ((xpost,"WEST"),(xnext,"EAST_CONTEXT")):
        pole("TMP_COLUMN_"+label,x,yfront,0,column_top,459/2,wood)
    ludou=mesh_object("COLUMN_LUDOU_MASTER_REF",src["COL"]["body"],
       (xpost,yfront,column_top),0,master,"CMP-LUDOU-COLUMN-001 / observed outer envelope")
    lu_height=float(src["COL"]["resolved_parameters"]["total_height_mm"])
    top_ludou=column_top+lu_height
    huabody=next(x for x in src["HUA"]["canonical_bodies"] if x["body_id"]=="JUMP_1_HUAGONG")
    hua_thick=float(huabody["resolved_dimensions_mm"]["thickness"])
    hua=mesh_object("COLUMN_HUAGONG_JUMP1_MASTER_REF",huabody,
       (xpost,yfront,top_ludou+hua_thick/2),1.5707963267948966,master,
       "CMP-GONG-HUAGONG-001 JUMP_1 / ref specimen, placement unverified")
    lbody=src["LING"]["canonical_body"]
    lthick=float(lbody["resolved_dimensions_mm"]["thickness"])
    ztop_hua=top_ludou+hua_thick
    ling=mesh_object("COLUMN_LINGGONG_MASTER_REF",lbody,
       (xpost,yfront,ztop_hua+lthick/2),0,master,
       "CMP-GONG-LINGGONG-001 / section reference")
    ztop_ling=ztop_hua+lthick
    # Infill trial only: cross-tie, a SMALL_DOU and a Linggong / upper arm
    # are explicitly temporary placement / geometry; no invented historical clearance.
    fang_top=3820.0
    cube("TEMP_FRONT_FANG",(xinter,yfront,fang_top-115),(4437,240,230),wood,"front framing proxy / no historic joinery")
    cube("TEMP_INTERCOLUMN_SMALL_DOU",(xinter,yfront,fang_top+72.5),
       (265,235,145),temp,"unified small-dou unknown, replaceable")
    infillbase=fang_top+145
    ling_i=mesh_object("INTERCOLUMN_LINGGONG_MASTER_REF",lbody,
       (xinter,yfront,infillbase+lthick/2),0,master,"CMP-GONG-LINGGONG-001 / infill trial")
    top_infill=infillbase+lthick
    # The eave is kept at V002 silhouette datum; structural contact to the
    # incomplete article is intentionally NOT artificially filled.
    eave_z=5270.0
    eave_y=-8295.0
    cube("TEMP_EAVE_PURLIN", (0,eave_y,eave_z-85), (5200,240,170),
         temp,"V002 eave section / placement only")
    roof=cube("TEMP_ROOF_PREVIEW_STRIP",(0,-6825,5485),(5200,2940,35),
              temp,"NOT full roof, silhouette context only")
    roof.rotation_euler.x=-0.16
    bpy.context.view_layer.update()
    low,lu_top_bbox = mesh_local_low_vertices(ludou)
    # LUDOU is not treated as a historic joint; HUAGONG central bottom
    # footprint is checked against the observed envelope.
    column_foot=mesh_local_low_vertices(ludou)[1]
    lu_support=([xpost-237.55,yfront-223.14999],[xpost+237.55,yfront+223.14999])
    seat_a=bottom_seat_check(hua,top_ludou,lu_support)
    hfoot=([xpost-huabody["resolved_dimensions_mm"]["width"]/2,yfront-huabody["resolved_dimensions_mm"]["length"]/2],
           [xpost+huabody["resolved_dimensions_mm"]["width"]/2,yfront+huabody["resolved_dimensions_mm"]["length"]/2])
    seat_b=bottom_seat_check(ling,ztop_hua,hfoot)
    infill_seat=bottom_seat_check(ling_i,infillbase,([xinter-132.5,yfront-117.5],[xinter+132.5,yfront+117.5]))
    gaps={"column_master_stack_to_eave_mm":eave_z-ztop_ling,
          "infill_master_stack_to_eave_mm":eave_z-top_infill}
    # The true acceptance condition for expanding into whole hall includes
    # a fully grounded support path. This C01 intentionally cannot PASS that.
    complete=(seat_a["pass"] and seat_b["pass"] and infill_seat["pass"]
              and all(abs(v)<=1 for v in gaps.values()))
    scene=bpy.context.scene;scene.unit_settings.system="METRIC";scene.unit_settings.scale_length=.001
    scene.render.engine="BLENDER_WORKBENCH"
    scene.display.shading.color_type="MATERIAL"
    scene.display.shading.light="STUDIO"
    scene.render.resolution_x=1200;scene.render.resolution_y=900
    scene.render.resolution_percentage=100;scene.render.image_settings.file_format="PNG"
    OUT.mkdir(parents=True,exist_ok=True)
    render("AXON",(10500,-14500,9600),(-200,-5900,4550),8600)
    render("FRONT",(0,-16000,4700),(0,-6000,4550),8000)
    render("SIDE",(-9500,-6300,4800),(-800,-6200,4570),7600)
    # Save without approval; BLEND is a separate editable trial.
    for obj in bpy.data.objects:
        if obj.type=="CAMERA":obj.hide_render=True
    scene["c01_status"]="INTERFACE_GATE_PASS" if complete else "STRUCTURAL_INTERFACE_GATE_FAIL"
    scene["c01_master_source_shas"]=json.dumps(shas,sort_keys=True)
    pathblend=OUT/"C01_BRACKET_EAVE_TRIAL.blend"
    pathglb=OUT/"C01_BRACKET_EAVE_TRIAL.glb"
    bpy.ops.wm.save_as_mainfile(filepath=str(pathblend),compress=True)
    bpy.ops.export_scene.gltf(filepath=str(pathglb),export_format="GLB",export_extras=True)
    report={
     "scope":"ONE_COLUMN_HEAD_AND_ONE_INTERCOLUMN_FIRST_ARTICLE_ONLY",
     "status":"PASS" if complete else "FAIL",
     "geometry_import_and_generation":"BUILT",
     "visual_assets":["C01_AXON.png","C01_FRONT.png","C01_SIDE.png"],
     "formal_master_semantic_sha256":shas,
     "source_silhouettes":["CMP-LUDOU-COLUMN-001","CMP-GONG-HUAGONG-001 / JUMP_1","CMP-GONG-LINGGONG-001"],
     "master_instance_placements":"WORKING_HYPOTHESIS_NOT_APPROVED",
     "physical_checks":{"ludou_to_huagong":seat_a,"huagong_to_linggong":seat_b,
                        "intercolumn_small_dou_to_linggong":infill_seat,
                        "unsupported_gaps_mm":gaps,
                        "fully_connected_to_eave":complete},
     "non_pass_meaning":"NO SCALE OUT, no historic load-bearing claim; trial only",
     "open_items":["historical column-head geometry beyond first local seat",
                  "source-correct intercolumn small-dou",
                  "upward and outward bearing path to purlin/eave",
                  "A1 original elevation/roof junction overlay not independently verified"],
     "archived_files":{"blend":{"path":str(pathblend.relative_to(ROOT)),"sha256":digest(pathblend)},
                       "glb":{"path":str(pathglb.relative_to(ROOT)),"sha256":digest(pathglb)}}}
    save("VALIDATION.json",report)
    print("C01_END_TO_END_TRIAL",json.dumps({"status":report["status"],"gaps":gaps,"seats":report["physical_checks"]},ensure_ascii=False))
def check_blend():
    assert bpy.context.scene["c01_status"] in ("STRUCTURAL_INTERFACE_GATE_FAIL","INTERFACE_GATE_PASS")
    names={o.name for o in bpy.data.objects if o.type=="MESH"}
    assert {"COLUMN_LUDOU_MASTER_REF","COLUMN_HUAGONG_JUMP1_MASTER_REF",
            "COLUMN_LINGGONG_MASTER_REF","INTERCOLUMN_LINGGONG_MASTER_REF","TEMP_EAVE_PURLIN"}<=names
    save("BLEND_REOPEN.json",{"status":"PASS","objects":len(names)})
    print("C01_BLEND_REOPEN_PASS")
def check_glb():
    p=OUT/"C01_BRACKET_EAVE_TRIAL.glb"
    bpy.ops.import_scene.gltf(filepath=str(p))
    names={o.name for o in bpy.data.objects if o.type=="MESH"}
    assert {"COLUMN_LUDOU_MASTER_REF","COLUMN_HUAGONG_JUMP1_MASTER_REF","INTERCOLUMN_LINGGONG_MASTER_REF"}<=names
    save("GLB_REOPEN.json",{"status":"PASS","objects":len(names)})
    print("C01_GLB_REOPEN_PASS")
if __name__=="__main__":
    args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=["build","check-blend","check-glb"],required=True)
    a=ap.parse_args(args)
    if a.mode=="build":build()
    elif a.mode=="check-blend":check_blend()
    else:check_glb()
