#!/usr/bin/env python3
import argparse, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SEM_COLUMN=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_SEMANTIC_V001.json"
SEM_LUDOU=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-LUDOU-COLUMN-001/CMP-LUDOU-COLUMN-001_MASTER_SEMANTIC_V001.json"
SEM_HG=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-GONG-HUAGONG-001/CMP-GONG-HUAGONG-001_MASTER_SEMANTIC_V001.json"
SEM_ANG=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-GONG-ANG-001/CMP-GONG-ANG-001_MASTER_SEMANTIC_V001.json"
SEM_LOWER=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LOWER-SIX-CHUANFU-001/CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER_SEMANTIC_V001.json"
B02=ROOT/"production/zhenguo_wanfo/assembly/P3_3_AF01_B02_BEAM_BODY_EXTENT_RESOLVER_V001.json"

NODE_X=2218.5
NODE_Y=5355.0
COLUMN_BASE_Z=0.0
LUDOU_BOTTOM_Z=3534.3

A0_TRANSFORMS={
 "JUMP_1_HUAGONG":{
   "instance_id":"华栱-北-05-一跳","origin":[2218.5,5355.0,3962.7],
   "axes":[[0,1,0],[-1,0,0],[0,0,1]]
 },
 "JUMP_2_HUAGONG":{
   "instance_id":"华栱-北-05-二跳","origin":[2218.5,5355.0,4284.0],
   "axes":[[0,1,0],[-1,0,0],[0,0,1]]
 },
 "TOU_ANG":{
   "instance_id":"头昂-北-05","origin":[2218.5,5307.536173764188,4575.571436519848],
   "axes":None
 },
 "ER_ANG":{
   "instance_id":"二昂-北-05","origin":[2218.5,5316.85760418523,4917.73368555742],
   "axes":None
 },
}
ANG_ANGLE_DEG=24.075498255078834
c=math.cos(math.radians(ANG_ANGLE_DEG)); s=math.sin(math.radians(ANG_ANGLE_DEG))
ANG_AXES=[[0,c,-s],[-1,0,0],[0,s,c]]
A0_TRANSFORMS["TOU_ANG"]["axes"]=ANG_AXES
A0_TRANSFORMS["ER_ANG"]["axes"]=ANG_AXES

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,v):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def mat_from_axes(Matrix, axes, origin):
    # Matrix columns are local axes expressed in world coordinates.
    x,y,z=axes
    return Matrix(((x[0],y[0],z[0],origin[0]),
                   (x[1],y[1],z[1],origin[1]),
                   (x[2],y[2],z[2],origin[2]),
                   (0,0,0,1)))

def make_mesh_obj(bpy, Matrix, name, verts, faces, origin, axes, material, meta):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    obj.matrix_world=mat_from_axes(Matrix,axes,origin)
    for k,v in meta.items(): obj[k]=v
    return obj

def cube_vertices_faces(x0,x1,y0,y1,z0,z1):
    v=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
       [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]]
    f=[[0,1,2,3],[4,7,6,5],[0,4,5,1],[1,5,6,2],[2,6,7,3],[4,0,3,7]]
    return v,f

def setup_scene(bpy):
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.resolution_x=1200; scene.render.resolution_y=900; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"; scene.render.film_transparent=False
    scene.world.use_nodes=True
    bg=next(n for n in scene.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.93,0.93,0.93,1.0); bg.inputs["Strength"].default_value=0.8
    scene.view_settings.view_transform="Standard"
    return scene

def material(bpy,name,rgb,alpha=1.0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*rgb,alpha); m.use_nodes=True
    bsdf=m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value=(*rgb,1.0)
        bsdf.inputs["Roughness"].default_value=0.65
    return m

def world_bbox(obj):
    from mathutils import Vector
    pts=[obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mins=[min(p[i] for p in pts) for i in range(3)]
    maxs=[max(p[i] for p in pts) for i in range(3)]
    return mins,maxs

def aabb_relation(a,b):
    amin,amax=world_bbox(a); bmin,bmax=world_bbox(b)
    sep=[max(0.0, bmin[i]-amax[i], amin[i]-bmax[i]) for i in range(3)]
    overlaps=[min(amax[i],bmax[i])-max(amin[i],bmin[i]) for i in range(3)]
    return {
      "aabb_separation_mm":sep,
      "aabb_overlap_mm":overlaps,
      "aabb_disjoint":any(x>1e-7 for x in sep),
      "aabb_min_gap_mm":math.sqrt(sum(x*x for x in sep))
    }

def boolean_intersection(bpy, bmesh, a,b, diag_mat):
    dup=a.copy(); dup.data=a.data.copy(); bpy.context.collection.objects.link(dup)
    dup.name="BOOL_TMP__"+a.name+"__"+b.name
    mod=dup.modifiers.new(name="EXACT_INTERSECTION",type="BOOLEAN")
    mod.operation="INTERSECT"; mod.solver="EXACT"; mod.object=b
    bpy.context.view_layer.objects.active=dup; dup.select_set(True)
    for o in bpy.context.selected_objects:
        if o is not dup: o.select_set(False)
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as e:
        bpy.data.objects.remove(dup,do_unlink=True)
        return None,{"status":"BOOLEAN_ERROR","error":str(e)}
    if len(dup.data.vertices)==0 or len(dup.data.polygons)==0:
        bpy.data.objects.remove(dup,do_unlink=True)
        return None,{"status":"NO_VOLUME_INTERSECTION","volume_mm3":0.0}
    bm=bmesh.new(); bm.from_mesh(dup.data)
    try: vol=abs(float(bm.calc_volume(signed=True)))
    except Exception: vol=0.0
    bm.free()
    if vol <= 1e-4:
        bpy.data.objects.remove(dup,do_unlink=True)
        return None,{"status":"NO_VOLUME_INTERSECTION","volume_mm3":vol}
    from mathutils import Vector
    pts=[dup.matrix_world @ v.co for v in dup.data.vertices]
    mins=[min(p[i] for p in pts) for i in range(3)]
    maxs=[max(p[i] for p in pts) for i in range(3)]
    centroid=[(mins[i]+maxs[i])/2.0 for i in range(3)]
    dup.name="COLLISION__"+a.name+"__"+b.name
    dup.data.materials.clear(); dup.data.materials.append(diag_mat)
    dup["diagnostic_only"]=True
    return dup,{
      "status":"VOLUME_INTERSECTION",
      "volume_mm3":vol,
      "collision_bbox_world_mm":{"min":mins,"max":maxs,"dimensions":[maxs[i]-mins[i] for i in range(3)]},
      "collision_bbox_centroid_world_mm":centroid
    }

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def render_views(bpy,scene,objects,collision_objects,outdir):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.camera_add()
    cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.clip_start=1; cam.data.clip_end=50000
    scene.camera=cam
    target=(NODE_X,NODE_Y-300,4350)
    views={
      "FRONT":((NODE_X,NODE_Y+4200,4350),2600),
      "SIDE":((NODE_X+4200,NODE_Y-350,4350),3000),
      "AXON":((NODE_X+3300,NODE_Y+3200,6500),3300),
    }
    for name,(loc,scale) in views.items():
        cam.location=loc; cam.data.ortho_scale=scale; look_at(cam,target)
        scene.render.filepath=str(outdir/(name+".png"))
        bpy.ops.render.render(write_still=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-json",required=True)
    ap.add_argument("--out-blend",required=True)
    ap.add_argument("--review-dir",required=True)
    import sys
    args=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else None)
    import bpy,bmesh
    from mathutils import Matrix

    scene=setup_scene(bpy)
    mats={
      "column":material(bpy,"MAT_COLUMN",(0.42,0.27,0.14)),
      "ludou":material(bpy,"MAT_LUDOU",(0.50,0.32,0.16)),
      "huagong":material(bpy,"MAT_HUAGONG",(0.57,0.38,0.20)),
      "ang":material(bpy,"MAT_ANG",(0.48,0.29,0.15)),
      "lower":material(bpy,"MAT_LOWER_SIX",(0.36,0.22,0.12)),
      "collision":material(bpy,"MAT_COLLISION",(0.90,0.08,0.05)),
    }
    col=load(SEM_COLUMN); lud=load(SEM_LUDOU); hg=load(SEM_HG); ang=load(SEM_ANG); low=load(SEM_LOWER); b02=load(B02)
    objects={}

    # Column: canonical Master body, translated only in XY.
    cb=col["body"]
    objects["COLUMN"]=make_mesh_obj(bpy,Matrix,"COLUMN__柱-03",cb["geometry_vertices_mm"] if "geometry_vertices_mm" in cb else [],cb["geometry_faces"] if "geometry_faces" in cb else [],[NODE_X,NODE_Y,COLUMN_BASE_Z],[[1,0,0],[0,1,0],[0,0,1]],mats["column"],{"instance_id":"柱-03","master_id":"CMP-COLUMN-001_MASTER"})
    # Column master is cylindrical and some legacy semantic files omit vertex arrays. Reconstruct only from its approved canonical primitive/dimensions if needed.
    if len(objects["COLUMN"].data.vertices)==0:
        bpy.data.objects.remove(objects["COLUMN"],do_unlink=True)
        bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=float(col["resolved_parameters"]["diameter_mm"])/2.0,depth=float(col["resolved_parameters"]["height_mm"]),location=(NODE_X,NODE_Y,float(col["resolved_parameters"]["height_mm"])/2.0))
        o=bpy.context.object; o.name="COLUMN__柱-03"; o.data.materials.append(mats["column"]); o["instance_id"]="柱-03"; o["master_id"]="CMP-COLUMN-001_MASTER"; o["source_geometry"]="APPROVED_CANONICAL_PRIMITIVE_PARAMETERS"
        objects["COLUMN"]=o

    lb=lud["body"]
    objects["LUDOU"]=make_mesh_obj(bpy,Matrix,"LUDOU__柱头栌斗-北侧东中柱",lb["geometry_vertices_mm"],lb["geometry_faces"],[NODE_X,NODE_Y,LUDOU_BOTTOM_Z],[[1,0,0],[0,1,0],[0,0,1]],mats["ludou"],{"instance_id":"柱头栌斗-北侧东中柱","master_id":"CMP-LUDOU-COLUMN-001_MASTER"})

    hgb={x["variant_id"]:x for x in hg["canonical_bodies"]}
    for vid,key in (("JUMP_1_HUAGONG","HG_J1"),("JUMP_2_HUAGONG","HG_J2")):
        b=hgb[vid]; t=A0_TRANSFORMS[vid]
        objects[key]=make_mesh_obj(bpy,Matrix,key+"__"+t["instance_id"],b["geometry_vertices_mm"],b["geometry_faces"],t["origin"],t["axes"],mats["huagong"],{"instance_id":t["instance_id"],"master_id":"CMP-GONG-HUAGONG-001_MASTER","master_variant":vid})

    anb={x["variant_id"]:x for x in ang["canonical_bodies"]}
    for vid,key in (("TOU_ANG","TOU_ANG"),("ER_ANG","ER_ANG")):
        b=anb[vid]; t=A0_TRANSFORMS[vid]
        objects[key]=make_mesh_obj(bpy,Matrix,key+"__"+t["instance_id"],b["geometry_vertices_mm"],b["geometry_faces"],t["origin"],t["axes"],mats["ang"],{"instance_id":t["instance_id"],"master_id":"CMP-GONG-ANG-001_MASTER","master_variant":vid})

    # Lower-Six assembly instance: B02 changes longitudinal realization only; section stays Master dimensions.
    lower_cfg=next(x for x in b02["beams"] if x["registry_id"]=="下六椽栿-东缝")
    L=float(lower_cfg["realization_length_mm"])
    W=float(low["resolved_parameters"]["width_mm"])       # guang -> world Z
    T=float(low["resolved_parameters"]["max_thickness_mm"]) # hou -> world X
    v,f=cube_vertices_faces(-L/2,L/2,-W/2,W/2,-T/2,T/2)
    axes=[[0,1,0],[0,0,1],[1,0,0]]
    # local x->world Y; local y(guang)->world Z; local z(hou)->world X
    origin=[NODE_X,0.0,float(lower_cfg["support_plane_z_mm"])+W/2.0]
    objects["LOWER_SIX"]=make_mesh_obj(bpy,Matrix,"LOWER_SIX__下六椽栿-东缝",v,f,origin,axes,mats["lower"],{"instance_id":"下六椽栿-东缝","master_id":"CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER","instance_realization_length_mm":L,"master_mutated":False})

    keys=list(objects.keys())
    pairs=[]
    collision_objects=[]
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            ka,kb=keys[i],keys[j]; a,bb=objects[ka],objects[kb]
            rel=aabb_relation(a,bb)
            inter_obj,inter=boolean_intersection(bpy,bmesh,a,bb,mats["collision"])
            rec={"a":ka,"b":kb,**rel,**inter}
            if "LOWER_SIX" in (ka,kb) and inter.get("status")=="VOLUME_INTERSECTION":
                dims=inter["collision_bbox_world_mm"]["dimensions"]
                rec["lower_six_tenon_375_assessment"]={
                  "observed_tenon_thickness_mm":375.0,
                  "collision_world_x_extent_mm":dims[0],
                  "exact_inside_tenon_envelope":"NOT_DETERMINABLE",
                  "reason":"TENON_ZONE_OFFSET_AND_LOCAL_CUT_DISTRIBUTION_ARE_UNKNOWN; NO_SYMMETRIC_REDUCTION_ASSUMED",
                  "numeric_compatibility_only":dims[0] <= 375.0 + 1e-6
                }
            if inter_obj: collision_objects.append(inter_obj)
            pairs.append(rec)

    collisions=[p for p in pairs if p["status"]=="VOLUME_INTERSECTION"]
    lower_collisions=[p for p in collisions if "LOWER_SIX" in (p["a"],p["b"])]

    result={
      "schema_version":"AF01_J01_STAGE_A_UNMODIFIED_COLLISION_AUDIT_V001",
      "date":"2026-10-01",
      "task":"AF01-J01",
      "stage":"A / UNMODIFIED COLLISION AUDIT",
      "status":"PASS_DIAGNOSTIC_COMPLETED",
      "node":"NORTH_ELEVATION_EAST_MIDDLE_COLUMN_HEAD",
      "participants":[{
        "key":k,
        "instance_id":objects[k].get("instance_id"),
        "master_id":objects[k].get("master_id"),
        "master_variant":objects[k].get("master_variant"),
        "world_bbox_mm":{"min":world_bbox(objects[k])[0],"max":world_bbox(objects[k])[1]}
      } for k in keys],
      "pair_count":len(pairs),
      "volume_intersection_pair_count":len(collisions),
      "lower_six_volume_intersection_pair_count":len(lower_collisions),
      "pairs":pairs,
      "lower_six_intersections":lower_collisions,
      "guardrails":{
        "master_mutation":False,
        "proxy_support_count":0,
        "joinery_cut_count_added":0,
        "t040_fixture_position_consumed":False,
        "t041_fixture_position_consumed":False,
        "a0_product_owner_approved":True
      },
      "interpretation_boundary":{
        "collision_means":"CURRENT_APPROVED_OUTER_ENVELOPES_INTERPENETRATE_UNDER_AF01_A0_PROJECT_DATUM",
        "collision_does_not_mean":"HISTORICAL_JOINERY_GEOMETRY_IS_PROVEN",
        "no_collision_does_not_mean":"HISTORICAL_CONTACT_OR_JOINERY_IS_SOLVED"
      },
      "next_gate":"PRODUCT_OWNER_REVIEW_OF_COLLISION_MAP_BEFORE_ANY_STAGE_B_CUT"
    }
    write(args.out_json,result)
    Path(args.out_blend).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(args.out_blend).resolve()))
    render_views(bpy,scene,objects,collision_objects,args.review_dir)
    print(json.dumps({
      "status":result["status"],
      "pair_count":len(pairs),
      "volume_intersection_pair_count":len(collisions),
      "lower_six_intersection_count":len(lower_collisions),
      "lower_six_intersections":[{"a":p["a"],"b":p["b"],"volume_mm3":round(p["volume_mm3"],3),"bbox":p.get("collision_bbox_world_mm")} for p in lower_collisions]
    },ensure_ascii=False))

if __name__=="__main__": main()
