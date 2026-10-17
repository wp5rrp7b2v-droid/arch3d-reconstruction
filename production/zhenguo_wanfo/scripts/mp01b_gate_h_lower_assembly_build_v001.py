import argparse, hashlib, json, math, sys
from pathlib import Path

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def stable(o):
    return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def file_sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

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

def material(name,color):
    import bpy
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    return m

def box_vertices_faces(sx,sy,z0,z1,offset=0):
    x=sx/2.0; y=sy/2.0
    verts=[
      (-x,-y,z0),(x,-y,z0),(x,y,z0),(-x,y,z0),
      (-x,-y,z1),(x,-y,z1),(x,y,z1),(-x,y,z1)
    ]
    faces=[
      (0,1,2,3),(4,7,6,5),(0,4,5,1),
      (1,5,6,2),(2,6,7,3),(3,7,4,0)
    ]
    return verts,[tuple(i+offset for i in f) for f in faces]

def multi_box_object(name,boxes,meta,material_obj,translation,rotation_deg):
    import bpy
    verts=[]; faces=[]
    for sx,sy,z0,z1 in boxes:
        v,f=box_vertices_faces(float(sx),float(sy),float(z0),float(z1),len(verts))
        verts.extend(v); faces.extend(f)
    me=bpy.data.meshes.new(name+"_MESH")
    me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location=tuple(float(x) for x in translation)
    ob.rotation_euler=tuple(math.radians(float(x)) for x in rotation_deg)
    for k,v in meta.items():
        if isinstance(v,(list,dict,tuple)):
            ob[k]=json.dumps(v,ensure_ascii=False,sort_keys=True)
        elif v is None:
            ob[k]="NULL"
        else:
            ob[k]=v
    if material_obj:
        ob.data.materials.append(material_obj)
    return ob

def add_datum(name,xyz):
    import bpy
    ob=bpy.data.objects.new(name,None)
    bpy.context.scene.collection.objects.link(ob)
    ob.empty_display_type="PLAIN_AXES"
    ob.empty_display_size=120
    ob.location=tuple(float(x) for x in xyz)
    ob["logical_control"]=True
    ob["physical"]=False
    return ob

def local_payload(ob):
    verts=[[round(float(v.co.x),6),round(float(v.co.y),6),round(float(v.co.z),6)] for v in ob.data.vertices]
    faces=[list(p.vertices) for p in ob.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
    return verts,faces,mins,maxs

def object_payload(ob):
    import bpy
    bpy.context.view_layer.update()
    lverts,faces,lmins,lmaxs=local_payload(ob)
    wverts=[]
    for v in ob.data.vertices:
        co=ob.matrix_world @ v.co
        wverts.append([round(float(co.x),6),round(float(co.y),6),round(float(co.z),6)])
    wmins=[min(v[i] for v in wverts) for i in range(3)]
    wmaxs=[max(v[i] for v in wverts) for i in range(3)]
    props={}
    for k in ob.keys():
        val=ob[k]
        try:
            if isinstance(val,str) and val and val[0] in "[{":
                props[k]=json.loads(val)
            else:
                props[k]=val
        except Exception:
            props[k]=val
    return {
      "logical_object_id":props.get("logical_object_id"),
      "object_class":props.get("object_class"),
      "master_id":props.get("master_id"),
      "variant_or_role":props.get("variant_or_role"),
      "whole_hall_count_claim":bool(props.get("whole_hall_count_claim",False)),
      "historical_metric_claim":bool(props.get("historical_metric_claim",False)),
      "historical_full_length_claim":bool(props.get("historical_full_length_claim",False)),
      "historical_joinery":props.get("historical_joinery"),
      "joinery_cut_count":int(props.get("joinery_cut_count",0)),
      "evidence_class":props.get("evidence_class"),
      "axis_mapping":props.get("axis_mapping"),
      "translation_mm":[round(float(x),6) for x in ob.location],
      "rotation_euler_deg":[round(math.degrees(float(x)),6) for x in ob.rotation_euler],
      "local_bbox_mm":{
        "min":lmins,"max":lmaxs,
        "dimensions":[round(lmaxs[i]-lmins[i],6) for i in range(3)]
      },
      "world_bbox_mm":{
        "min":wmins,"max":wmaxs,
        "dimensions":[round(wmaxs[i]-wmins[i],6) for i in range(3)]
      },
      "vertex_count":len(lverts),
      "face_count":len(faces),
      "local_geometry_signature":stable({"verts":lverts,"faces":faces}),
      "world_geometry_signature":stable({"verts":wverts,"faces":faces})
    }

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def camera_light():
    import bpy
    cd=bpy.data.cameras.new("MP01B_CAMERA")
    cam=bpy.data.objects.new("MP01B_CAMERA",cd)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera=cam
    cd.type="ORTHO"; cd.clip_end=100000
    ld=bpy.data.lights.new("KEY","AREA"); ld.energy=1100; ld.size=6000
    light=bpy.data.objects.new("KEY",ld)
    bpy.context.scene.collection.objects.link(light)
    light.location=(5000,-5000,5000); look_at(light,(0,0,100))
    return cam

def render(scene,cam,path,pos,target,ortho,res=(1400,900)):
    import bpy
    cam.location=pos; look_at(cam,target); cam.data.ortho_scale=ortho
    scene.render.resolution_x=res[0]; scene.render.resolution_y=res[1]
    scene.render.filepath=str(Path(path).resolve())
    bpy.ops.render.render(write_still=True)

def build(contract_path,asset,semantic,review_dir,clearance_override=None):
    import bpy
    c=load(contract_path)
    canonical_clearance=float(c["mutation_test"]["canonical_mm"])
    clearance=canonical_clearance if clearance_override is None else float(clearance_override)
    lg=c["geometry_inputs"]["interior_linggong"]
    tf=c["geometry_inputs"]["tuofeng_lower"]
    fc=c["geometry_inputs"]["four_chuanfu"]
    pl=c["geometry_inputs"]["pingliang"]
    lg_h=float(lg["total_height_mm"])
    tf_h=clearance-lg_h
    if tf_h<=0:
        raise ValueError("NEGATIVE_TUOFENG_RESIDUAL_HEIGHT")
    tf_base_h=tf_h/2.0
    tf_seat_h=tf_h-tf_base_h

    clear_scene(); scene=scene_setup()
    mats={
      "fc":material("FOUR_CHUANFU_MAT",(0.30,0.16,0.08)),
      "pl":material("PINGLIANG_MAT",(0.39,0.21,0.10)),
      "tf":material("TUOFENG_MAT",(0.49,0.27,0.12)),
      "lg":material("LINGGONG_MAT",(0.58,0.34,0.16))
    }
    rz=[0,0,90]
    common_unknown="UNKNOWN / DEFERRED / NOT_MODELED"

    objs=[]
    objs.append(multi_box_object(
      "MP01B__FOUR_CHUANFU_EAST_SEAM",
      [(fc["length_mm"],fc["width_mm"],0,fc["height_mm"])],
      {
        "logical_object_id":"四椽栿-东缝","object_class":"V008_PHYSICAL_INSTANCE",
        "master_id":"CMP-FRAME-FOUR-CHUANFU-001_MASTER","variant_or_role":"EAST_SEAM",
        "historical_metric_claim":False,"historical_full_length_claim":False,
        "whole_hall_count_claim":False,"historical_joinery":common_unknown,"joinery_cut_count":0,
        "evidence_class":"DIRECT_SECTION + REPORT_INFERRED_REALIZATION_LENGTH",
        "axis_mapping":"LOCAL_X_TO_ASSEMBLY_Y / RZ_PLUS_90"
      },mats["fc"],[0,0,-float(fc["height_mm"])],rz))

    objs.append(multi_box_object(
      "MP01B__PINGLIANG_EAST_SEAM",
      [(pl["length_mm"],pl["width_mm"],0,pl["height_mm"])],
      {
        "logical_object_id":"平梁-东缝","object_class":"V008_PHYSICAL_INSTANCE",
        "master_id":"CMP-FRAME-PINGLIANG-001_MASTER","variant_or_role":"EW_SEAM",
        "historical_metric_claim":False,"historical_full_length_claim":False,
        "whole_hall_count_claim":False,"historical_joinery":common_unknown,"joinery_cut_count":0,
        "evidence_class":"DIRECT_SECTION + RECONSTRUCTED_MINIMUM_SUPPORT_SPAN + REPORT_INFERRED_VERTICAL_PLACEMENT",
        "axis_mapping":"LOCAL_X_TO_ASSEMBLY_Y / RZ_PLUS_90"
      },mats["pl"],[0,0,clearance],rz))

    for side,y in [("SOUTH",1836.0),("NORTH",-1836.0)]:
        tf_id=f"ASM-MP01B-TUOFENG-LOWER-{side}-01"
        objs.append(multi_box_object(
          f"MP01B__TUOFENG_LOWER_{side}",
          [
            (tf["base_span_mm"],tf["base_depth_mm"],0,tf_base_h),
            (tf["upper_seat_span_mm"],tf["upper_seat_depth_mm"],tf_base_h,tf_h)
          ],
          {
            "logical_object_id":tf_id,"object_class":"RECONSTRUCTED_ASSEMBLY_INSTANCE",
            "master_id":"CMP-FRAME-TUOFENG-001_MASTER","variant_or_role":"LOWER_SUPPORT",
            "historical_metric_claim":False,"historical_full_length_claim":False,
            "whole_hall_count_claim":False,"historical_joinery":common_unknown,"joinery_cut_count":0,
            "evidence_class":"SECONDARY_CALCULATED_RESIDUAL + RECONSTRUCTED_MASTER_TOPOLOGY / REPLACEABLE",
            "axis_mapping":"LOCAL_X_TO_ASSEMBLY_Y / RZ_PLUS_90"
          },mats["tf"],[0,y,0],rz))

        lg_id=f"ASM-MP01B-LINGGONG-{side}-01"
        body_h=float(lg["body_zone_height_mm"])
        objs.append(multi_box_object(
          f"MP01B__INTERIOR_LINGGONG_{side}",
          [
            (lg["length_mm"],lg["depth_mm"],0,body_h),
            (lg["upper_bearing_length_mm"],lg["depth_mm"],body_h,lg_h)
          ],
          {
            "logical_object_id":lg_id,"object_class":"RECONSTRUCTED_ASSEMBLY_INSTANCE",
            "master_id":"CMP-FRAME-LINGGONG-INTERIOR-001_MASTER","variant_or_role":"LOWER_PINGLIANG_SUPPORT",
            "historical_metric_claim":False,"historical_full_length_claim":False,
            "whole_hall_count_claim":False,"historical_joinery":common_unknown,"joinery_cut_count":0,
            "evidence_class":"SAME_BUILDING_INTERIOR_ANALOG / RECONSTRUCTED_ASSEMBLY_CANDIDATE / REPLACEABLE",
            "axis_mapping":"LOCAL_X_TO_ASSEMBLY_Y / RZ_PLUS_90"
          },mats["lg"],[0,y,tf_h],rz))

    add_datum("DATUM-MP01B-SUPPORT-SOUTH",[0,1836,0])
    add_datum("DATUM-MP01B-SUPPORT-NORTH",[0,-1836,0])
    bpy.context.view_layer.update()

    payloads=[object_payload(o) for o in sorted(objs,key=lambda x:x.get("logical_object_id",""))]
    relationships=[]
    for r in c["relationships"]:
        q=dict(r)
        q["replaceable"]=True
        q["historical_joinery_claim"]=False
        if "evidence" not in q:
            q["evidence"]="PROJECT_ASSEMBLY_CONTROL / REPLACEABLE"
        relationships.append(q)

    sem={
      "schema_version":"MP01B_GATE_H_LOWER_ASSEMBLY_SEMANTIC_1.0",
      "status":"BUILT / PRODUCT_OWNER_REVIEW_REQUIRED",
      "task_id":"T-044",
      "assembly_id":"MP-01B-LOWER-PINGLIANG-SUPPORT-EAST-SEAM",
      "scope":"MINIMUM_PROOF_ONLY",
      "coordinate_system":c["coordinate_system"],
      "clearance_mm":clearance,
      "canonical_clearance_mm":canonical_clearance,
      "is_mutation":abs(clearance-canonical_clearance)>1e-9,
      "tuofeng_total_height_mm":tf_h,
      "tuofeng_base_height_mm":tf_base_h,
      "tuofeng_upper_seat_height_mm":tf_seat_h,
      "linggong_bottom_z_mm":tf_h,
      "linggong_top_z_mm":clearance,
      "pingliang_bottom_z_mm":clearance,
      "pingliang_top_z_mm":clearance+float(pl["height_mm"]),
      "support_stations_y_mm":[1836.0,-1836.0],
      "logical_object_count":len(payloads),
      "objects":payloads,
      "controls":c["controls"],
      "relationships":relationships,
      "support_relation_count":sum(1 for r in relationships if r["type"]=="SUPPORT"),
      "locate_relation_count":sum(1 for r in relationships if r["type"]=="LOCATE"),
      "historical_joinery":"UNKNOWN / DEFERRED / NOT_MODELED",
      "joinery_cut_count":0,
      "whole_hall_claim":False,
      "historical_exactness_claim":False,
      "contract_sha256":file_sha(contract_path),
      "blender_version":bpy.app.version_string
    }
    sem["assembly_signature"]=stable({
      "clearance_mm":clearance,
      "objects":[(x["logical_object_id"],x["local_geometry_signature"],x["world_geometry_signature"]) for x in payloads],
      "relationships":relationships
    })
    Path(semantic).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    if review_dir:
        review=Path(review_dir); review.mkdir(parents=True,exist_ok=True)
        cam=camera_light()
        target=(0,0,120)
        render(scene,cam,review/"LOWER_ASSEMBLY_FRONT_ELEVATION.png",(8000,0,400),target,5000)
        render(scene,cam,review/"LOWER_ASSEMBLY_AXONOMETRIC.png",(5200,-6200,3300),target,7000)
        render(scene,cam,review/"SOUTH_SUPPORT_DETAIL.png",(3500,1836,500),(0,1836,150),1500,(1100,900))
        if sem["is_mutation"]:
            render(scene,cam,review/"MUTATION_306_TO_310.png",(8000,0,400),target,5000)

    Path(asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(asset).resolve()))
    sem["blend_sha256"]=file_sha(asset)
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01B_GATE_H_BUILD_PASS",clearance,sem["assembly_signature"])

def inspect(expected,output):
    import bpy
    exp=load(expected)
    objs=[o for o in bpy.data.objects if o.type=="MESH" and o.get("logical_object_id")]
    got=[object_payload(o) for o in sorted(objs,key=lambda x:x.get("logical_object_id",""))]
    got_map={x["logical_object_id"]:x["world_geometry_signature"] for x in got}
    want_map={x["logical_object_id"]:x["world_geometry_signature"] for x in exp["objects"]}
    out={
      "status":"PASS" if got_map==want_map else "FAIL",
      "logical_object_count":len(got),
      "world_geometry_signatures":got_map,
      "expected":want_map
    }
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if out["status"]!="PASS":
        raise SystemExit("REOPEN_SIGNATURE_MISMATCH")
    print("MP01B_GATE_H_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("build","inspect"))
    ap.add_argument("--contract")
    ap.add_argument("--asset")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--clearance-mm",type=float)
    ap.add_argument("--expected")
    ap.add_argument("--output")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    a=ap.parse_args(argv)
    if a.mode=="build":
        build(a.contract,a.asset,a.semantic,a.review_dir,a.clearance_mm)
    else:
        inspect(a.expected,a.output)

if __name__=="__main__":
    main()
