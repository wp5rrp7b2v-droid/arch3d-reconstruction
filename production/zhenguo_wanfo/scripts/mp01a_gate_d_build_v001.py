import argparse, hashlib, json, math, sys
from pathlib import Path

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def stable(o):
    return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def file_sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def clear():
    import bpy
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes,bpy.data.curves,bpy.data.materials,bpy.data.cameras,bpy.data.lights):
        pass

def scene_setup():
    import bpy
    s=bpy.context.scene
    s.unit_settings.system="METRIC"
    s.unit_settings.scale_length=0.001
    s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_WORKBENCH"
    s.display.shading.light="STUDIO"
    s.display.shading.show_shadows=True
    s.display.shading.show_cavity=True
    s.render.resolution_percentage=100
    s.world.color=(0.95,0.95,0.95)
    return s

def mat(name,color):
    import bpy
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    return m

def make_mesh(name,verts,faces,meta,material=None):
    import bpy
    me=bpy.data.meshes.new(name+"_MESH")
    me.from_pydata(verts,[],faces)
    me.update()
    ob=bpy.data.objects.new(name,me)
    bpy.context.scene.collection.objects.link(ob)
    for k,v in meta.items():
        if isinstance(v,(dict,list,tuple)):
            ob[k]=json.dumps(v,ensure_ascii=False,sort_keys=True)
        elif v is None:
            ob[k]="NULL"
        else:
            ob[k]=v
    if material:
        ob.data.materials.append(material)
    return ob

def box_axis_aligned(name,dx,dy,dz,cx,cy,cz,meta,material):
    x=dx/2; y=dy/2; z=dz/2
    verts=[
      (cx-x,cy-y,cz-z),(cx+x,cy-y,cz-z),(cx+x,cy+y,cz-z),(cx-x,cy+y,cz-z),
      (cx-x,cy-y,cz+z),(cx+x,cy-y,cz+z),(cx+x,cy+y,cz+z),(cx-x,cy+y,cz+z)
    ]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    return make_mesh(name,verts,faces,meta,material)

def vec_sub(a,b): return tuple(a[i]-b[i] for i in range(3))
def vec_add(a,b): return tuple(a[i]+b[i] for i in range(3))
def vec_mul(a,s): return tuple(x*s for x in a)
def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a,a))
def unit(a):
    n=norm(a)
    if n<=1e-9: raise ValueError("ZERO_LENGTH_ENDPOINT_VECTOR")
    return tuple(x/n for x in a)

def endpoint_prism(name,p0,p1,section_a,section_b,meta,material):
    # u = member axis. For MP-01A all member axes lie in YZ; use global X as one stable cross axis.
    u=unit(vec_sub(p1,p0))
    v=(1.0,0.0,0.0)
    if abs(dot(u,v))>0.95:
        v=(0.0,1.0,0.0)
    v=unit(vec_sub(v,vec_mul(u,dot(v,u))))
    w=unit(cross(u,v))
    ha=section_a/2.0
    hb=section_b/2.0
    def ring(p):
        return [
          vec_add(vec_add(p,vec_mul(v,-ha)),vec_mul(w,-hb)),
          vec_add(vec_add(p,vec_mul(v, ha)),vec_mul(w,-hb)),
          vec_add(vec_add(p,vec_mul(v, ha)),vec_mul(w, hb)),
          vec_add(vec_add(p,vec_mul(v,-ha)),vec_mul(w, hb))
        ]
    verts=ring(tuple(p0))+ring(tuple(p1))
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    meta=dict(meta)
    meta["p_lower_mm"]=list(p0); meta["p_upper_mm"]=list(p1)
    meta["resolved_length_mm"]=norm(vec_sub(p1,p0))
    meta["resolved_direction"]=list(u)
    return make_mesh(name,verts,faces,meta,material)

TUOFENG_PROFILE=[
 [-0.50,0.00],[-0.42,0.07],[-0.34,0.07],[-0.34,0.13],
 [-0.25,0.13],[-0.25,0.20],[-0.16,0.20],[-0.12,0.32],
 [0.12,0.32],[0.16,0.20],[0.25,0.20],[0.25,0.13],
 [0.34,0.13],[0.34,0.07],[0.42,0.07],[0.50,0.00]
]

def tuofeng(name,span_y,depth_x,height_z,base_z,meta,material):
    # approved profile is scaled into assembly YZ, extruded along X
    pts=[(float(y)*span_y, float(z)/0.32*height_z+base_z) for y,z in TUOFENG_PROFILE]
    hx=depth_x/2.0
    verts=[(-hx,y,z) for y,z in pts]+[(hx,y,z) for y,z in pts]
    n=len(pts)
    faces=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]
    for i in range(n):
        j=(i+1)%n
        faces.append((i,j,n+j,n+i))
    return make_mesh(name,verts,faces,meta,material)

def datum_line(name,p0,p1,meta):
    import bpy
    cu=bpy.data.curves.new(name+"_CURVE","CURVE")
    cu.dimensions="3D"; cu.bevel_depth=8; cu.bevel_resolution=2
    sp=cu.splines.new("POLY"); sp.points.add(1)
    sp.points[0].co=(*p0,1); sp.points[1].co=(*p1,1)
    ob=bpy.data.objects.new(name,cu); bpy.context.scene.collection.objects.link(ob)
    for k,v in meta.items(): ob[k]=v if not isinstance(v,(dict,list)) else json.dumps(v,ensure_ascii=False)
    return ob

def object_payload(ob):
    if ob.type!="MESH": return None
    verts=[]
    for v in ob.data.vertices:
        co=ob.matrix_world @ v.co
        verts.append([round(float(co.x),6),round(float(co.y),6),round(float(co.z),6)])
    faces=[list(p.vertices) for p in ob.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
    return {
      "object_name":ob.name,
      "instance_id":ob.get("instance_id"),
      "master_id":ob.get("master_id"),
      "variant_id":ob.get("variant_id"),
      "record_type":ob.get("record_type"),
      "evidence_class":ob.get("evidence_class"),
      "historical_metric_claim":bool(ob.get("historical_metric_claim",False)),
      "historical_joinery":ob.get("historical_joinery"),
      "vertex_count":len(verts),
      "face_count":len(faces),
      "bbox_mm":{"min":mins,"max":maxs,"dimensions":[round(maxs[i]-mins[i],6) for i in range(3)]},
      "geometry_signature":stable({"verts":verts,"faces":faces})
    }

def look_at(obj,target):
    from mathutils import Vector
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()

def camera_light():
    import bpy
    cd=bpy.data.cameras.new("MP01A_CAMERA")
    cam=bpy.data.objects.new("MP01A_CAMERA",cd); bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera=cam; cd.type="ORTHO"; cd.clip_end=100000
    ld=bpy.data.lights.new("KEY","AREA"); ld.energy=1000; ld.size=5000
    light=bpy.data.objects.new("KEY",ld); bpy.context.scene.collection.objects.link(light)
    light.location=(5000,-5000,4500); look_at(light,(0,0,300))
    return cam

def render(scene,cam,path,pos,target,ortho,res=(1200,900)):
    cam.location=pos; look_at(cam,target); cam.data.ortho_scale=ortho
    scene.render.resolution_x,resy=res
    scene.render.resolution_y=resy
    scene.render.filepath=str(Path(path).resolve())
    bpy=__import__("bpy")
    bpy.ops.render.render(write_still=True)

def build(contract_path,asset,semantic,review_dir):
    import bpy
    c=load(contract_path)
    clear(); scene=scene_setup()
    review=Path(review_dir); review.mkdir(parents=True,exist_ok=True)

    m_ping=mat("PINGLIANG_MAT",(0.33,0.18,0.09))
    m_tuo=mat("TUOFENG_MAT",(0.47,0.26,0.12))
    m_shu=mat("SHUZHU_MAT",(0.40,0.22,0.11))
    m_cha=mat("CHASHOU_MAT",(0.29,0.15,0.08))

    b=c["building_realization"]
    p=b["pingliang"]
    ping=box_axis_aligned(
      "MP01A__PINGLIANG_EAST_SEAM",
      p["width_mm"],p["length_mm"],p["thickness_mm"],
      0,0,(p["top_z_mm"]+p["bottom_z_mm"])/2,
      {"instance_id":p["instance_id"],"master_id":p["master_id"],"variant_id":p["variant"],
       "record_type":"V008_PHYSICAL_INSTANCE","evidence_class":p["length_classification"],
       "historical_metric_claim":False,"historical_joinery":"UNKNOWN / NOT_MODELED"},
      m_ping)

    t=b["tuofeng_upper"]
    tuo=tuofeng("MP01A__TUOFENG_UPPER",t["base_span_y_mm"],t["depth_x_mm"],t["height_z_mm"],t["base_z_mm"],
      {"instance_id":t["instance_id"],"master_id":t["master_id"],"variant_id":t["variant"],
       "record_type":"RECONSTRUCTED_ASSEMBLY_INSTANCE","evidence_class":json.dumps(t["classification"],ensure_ascii=False),
       "historical_metric_claim":False,"whole_hall_count_claim":False,"historical_joinery":"UNKNOWN / DEFERRED"},
      m_tuo)

    s=b["shuzhu"]
    shu=endpoint_prism("MP01A__SHUZHU_EAST_SEAM",s["lower_endpoint_mm"],s["upper_endpoint_mm"],
      c["direct_component_envelopes"]["shuzhu"]["thickness_mm"],
      c["direct_component_envelopes"]["shuzhu"]["width_mm"],
      {"instance_id":s["instance_id"],"master_id":s["master_id"],"variant_id":"INTERIOR_FRAME",
       "record_type":"V008_PHYSICAL_INSTANCE","evidence_class":s["classification"],
       "historical_metric_claim":False,"historical_joinery":"UNKNOWN / NOT_MODELED"},m_shu)

    for key,label in [("chashou_south","SOUTH"),("chashou_north","NORTH")]:
        q=b[key]
        endpoint_prism(f"MP01A__CHASHOU_{label}",q["lower_endpoint_mm"],q["upper_endpoint_mm"],
          c["direct_component_envelopes"]["chashou"]["thickness_mm"],
          c["direct_component_envelopes"]["chashou"]["width_mm"],
          {"instance_id":q["instance_id"],"master_id":q["master_id"],"variant_id":"INTERIOR_FRAME",
           "record_type":"V008_PHYSICAL_INSTANCE","evidence_class":q["classification"],
           "historical_metric_claim":False,"historical_joinery":"UNKNOWN / NOT_MODELED"},m_cha)

    # non-physical controls
    zt=b["ridge_target_datum"]["xyz_mm"][2]
    zr=b["ridge_purlin_reference"]["z_mm"]
    datum_line("DATUM__RIDGE_TARGET",(-300,0,zt),(300,0,zt),{"record_type":"NON_PHYSICAL_ASSEMBLY_DATUM","datum_id":b["ridge_target_datum"]["datum_id"]})
    datum_line("DATUM__RIDGE_PURLIN_REFERENCE",(-300,0,zr),(300,0,zr),{"record_type":"NON_PHYSICAL_REFERENCE_LEVEL","historical_contact_claim":False})

    physical=[o for o in bpy.data.objects if o.type=="MESH"]
    payloads=[object_payload(o) for o in sorted(physical,key=lambda x:x.name)]
    relations=[
      {"from":"平梁-东缝","to":"ASM-MP01A-TUOFENG-UPPER-01","relation":"SUPPORT/LOCATE","class":"RECONSTRUCTED_DESIGN / REPLACEABLE"},
      {"from":"ASM-MP01A-TUOFENG-UPPER-01","to":"蜀柱-东缝","relation":"SUPPORT/SEAT","class":"INFERENCE + RECONSTRUCTED_DESIGN"},
      {"from":"平梁-东缝","to":"叉手-东缝-南侧","relation":"CONTACT_REGION/LOCATE","class":"FACT structural layer + endpoint reconstruction"},
      {"from":"平梁-东缝","to":"叉手-东缝-北侧","relation":"CONTACT_REGION/LOCATE","class":"FACT structural layer + endpoint reconstruction"},
      {"from":"DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM","to":"蜀柱-东缝","relation":"ENDPOINT_TARGET","class":"PROJECT_ASSEMBLY_RULE"},
      {"from":"DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM","to":"叉手-东缝-南侧","relation":"ENDPOINT_TARGET","class":"PROJECT_ASSEMBLY_RULE"},
      {"from":"DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM","to":"叉手-东缝-北侧","relation":"ENDPOINT_TARGET","class":"PROJECT_ASSEMBLY_RULE"}
    ]
    sem={
      "schema_version":"MP01A_GATE_D_ASSEMBLY_SEMANTIC_1.0",
      "status":"BUILT / PRODUCT_OWNER_REVIEW_REQUIRED",
      "assembly_id":"MP-01A-UPPER-RIDGE-SUPPORT-EAST-SEAM",
      "scope":"MINIMUM_PROOF_ONLY",
      "coordinate_system":c["coordinate_system"],
      "contract_sha256":file_sha(contract_path),
      "objects":payloads,
      "relations":relations,
      "ridge_target_datum":b["ridge_target_datum"],
      "ridge_purlin_reference":b["ridge_purlin_reference"],
      "retained_unknowns":c["retained_unknowns"],
      "historical_joinery":"UNKNOWN / NOT_MODELED",
      "whole_hall_claim":False,
      "mp01b_status":"NOT_INCLUDED / LINGGONG_SCOPE_BLOCKER_REMAINS",
      "blender_version":bpy.app.version_string,
      "assembly_signature":stable({"objects":[(x["instance_id"],x["geometry_signature"]) for x in payloads],"relations":relations})
    }
    Path(semantic).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    cam=camera_light()
    target=(0,0,250)
    render(scene,cam,review/"MP01A_FRONT_ELEVATION.png",(-6500,0,700),target,4700,(1400,900))
    render(scene,cam,review/"MP01A_AXON.png",(4200,-5200,3300),target,5000,(1400,900))
    Path(asset).parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(asset).resolve()))
    sem["blend_sha256"]=file_sha(asset)
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01A_GATE_D_BUILD_PASS",sem["assembly_signature"])

def inspect(asset,expected,out):
    import bpy
    exp=load(expected)
    current=[object_payload(o) for o in sorted([x for x in bpy.data.objects if x.type=="MESH"],key=lambda x:x.name)]
    got={x["instance_id"]:x["geometry_signature"] for x in current}
    want={x["instance_id"]:x["geometry_signature"] for x in exp["objects"]}
    result={"status":"PASS" if got==want else "FAIL","object_count":len(current),"geometry_signatures":got,"expected":want}
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    Path(out).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if result["status"]!="PASS": raise SystemExit("MP01A_REOPEN_MISMATCH")
    print("MP01A_GATE_D_REOPEN_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("build","inspect"))
    ap.add_argument("--contract")
    ap.add_argument("--asset")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--expected")
    ap.add_argument("--output")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    a=ap.parse_args(argv)
    if a.mode=="build": build(a.contract,a.asset,a.semantic,a.review_dir)
    else: inspect(a.asset,a.expected,a.output)
if __name__=="__main__": main()
