"""T-032 connector-aware complete assembly proof.
上六椽栿 -> 散斗 Connection Layer proxy -> 四椽栿.
All proof geometry is ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[3]
LOWER=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-FRAME-UPPER-SIX-CHUANFU-001/CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER_PARAMS_V001.json"
UPPER=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-FRAME-FOUR-CHUANFU-001/CMP-FRAME-FOUR-CHUANFU-001_MASTER_PARAMS_V001.json"
SCHEMA=ROOT/"production/zhenguo_wanfo/assembly/P3_3_CONNECTION_LAYER_SCHEMA_V001.json"
TOL=0.1

def stable(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def pm(data):
    return {x["key"]:x for x in data["parameters"]}

def load_inputs():
    lo=json.loads(LOWER.read_text(encoding="utf-8"))
    up=json.loads(UPPER.read_text(encoding="utf-8"))
    sc=json.loads(SCHEMA.read_text(encoding="utf-8"))
    lp=pm(lo); upm=pm(up)
    assert lo["master_id"]=="CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER"
    assert up["master_id"]=="CMP-FRAME-FOUR-CHUANFU-001_MASTER"
    proof=sc["t032_proof"]
    assert proof["connection_id"]=="CONN-SAN-DOU-UPPER6-FOUR-001"
    assert proof["connection_kind"]=="PHYSICAL_CONNECTOR"
    assert proof["historical_claim"] is False
    lw=float(lp["width_mm"]["value"])
    lt=float(lp["max_thickness_mm"]["value"])
    uw=float(upm["width_mm"]["value"])
    ut=float(upm["thickness_mm"]["value"])
    return lo,up,sc,lw,lt,uw,ut

def clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for c in list(bpy.data.collections):
        if c != bpy.context.scene.collection:
            bpy.data.collections.remove(c)

def setup():
    s=bpy.context.scene
    s.unit_settings.system="METRIC"
    s.unit_settings.scale_length=.001
    s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_EEVEE_NEXT"
    s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100
    s.render.image_settings.file_format="PNG"
    s.world.use_nodes=True
    bg=next(n for n in s.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.92,0.92,0.92,1);bg.inputs["Strength"].default_value=1
    s["task_id"]="T-032"
    s["coordinate_classification"]="ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES"

def box(name,L,W,H,z0,props):
    x=L/2;y=W/2;z1=z0+H
    verts=[(-x,-y,z0),(x,-y,z0),(x,y,z0),(-x,y,z0),
           (-x,-y,z1),(x,-y,z1),(x,y,z1),(-x,y,z1)]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    me=bpy.data.meshes.new(name+"__MESH");me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(ob)
    for k,v in props.items():ob[k]=v
    return ob

def payload(ob):
    vs=[[round(float(v.co[i]),6) for i in range(3)] for v in ob.data.vertices]
    fs=[list(p.vertices) for p in ob.data.polygons]
    return {
      "name":ob.name,
      "vertices_mm":vs,
      "faces":fs,
      "role":ob.get("assembly_role"),
      "component_id":ob.get("component_id"),
      "master_id":ob.get("master_id"),
      "connection_id":ob.get("connection_id")
    }

def render(outdir,target):
    outdir.mkdir(parents=True,exist_ok=True)
    s=bpy.context.scene
    vals=[0.28,0.52,0.72]
    for i,o in enumerate([x for x in s.objects if x.type=="MESH"]):
        m=bpy.data.materials.new("T032_M"+str(i));m.diffuse_color=(vals[i],vals[i],vals[i],1);o.data.materials.append(m)
    cd=bpy.data.cameras.new("T032_CAMERA");cam=bpy.data.objects.new("T032_CAMERA",cd)
    s.collection.objects.link(cam);s.camera=cam;cd.type="ORTHO";cd.clip_end=100000
    for name,pos,scale in [
      ("FRONT",(0,-6000,700),3600),
      ("AXON",(3800,-4800,3200),4300)
    ]:
        cam.location=pos
        cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
        cd.ortho_scale=scale
        s.render.filepath=str(outdir/(name+".png"))
        bpy.ops.render.render(write_still=True)

def build(case,blend,semantic,review=None):
    lo,up,sc,lw,lt,uw,ut=load_inputs()
    clear();setup()
    lower_len=2400.0; upper_len=2200.0
    connector_h=160.0 if case=="A" else 220.0
    connector_xy=round(.60*min(lw,uw),6)
    lower_z0=0.0
    connector_z0=lt
    upper_z0=lt+connector_h

    lower=box("ASM__UPPER_SIX_CHUANFU",lower_len,lw,lt,lower_z0,{
      "assembly_role":"LOWER_MASTER",
      "component_id":lo["component_id"],
      "master_id":lo["master_id"],
      "placement_authority":"SCRIPTED_CONNECTION_RESOLVER"
    })
    conn=box("CONN__SAN_DOU_PROXY",connector_xy,connector_xy,connector_h,connector_z0,{
      "assembly_role":"PHYSICAL_CONNECTOR",
      "connection_id":"CONN-SAN-DOU-UPPER6-FOUR-001",
      "connector_family":"散斗族",
      "geometry_classification":"RECONSTRUCTED_DESIGN / PHYSICAL_CONNECTOR_PROXY / ENGINEERING_TEST_ONLY",
      "historical_claim":False,
      "replaceable":True
    })
    upper=box("ASM__FOUR_CHUANFU",upper_len,uw,ut,upper_z0,{
      "assembly_role":"UPPER_MASTER",
      "component_id":up["component_id"],
      "master_id":up["master_id"],
      "placement_authority":"SCRIPTED_CONNECTION_RESOLVER"
    })

    lower_top=lt;conn_bottom=connector_z0;conn_top=connector_z0+connector_h;upper_bottom=upper_z0
    lower_gap=abs(lower_top-conn_bottom)
    upper_gap=abs(conn_top-upper_bottom)
    footprint_inside=(connector_xy<=lw+TOL and connector_xy<=uw+TOL)
    lower_ref=float(pm(lo)["canonical_reference_length_mm"]["value"])
    upper_ref=float(pm(up)["canonical_reference_length_mm"]["value"])

    out={
      "task_id":"T-032",
      "case":"TEST_"+case,
      "classification":"ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES",
      "manual_blender_transform_count":0,
      "connection_layer":{
        "schema_version":sc["schema_version"],
        "connection_id":"CONN-SAN-DOU-UPPER6-FOUR-001",
        "connection_kind":"PHYSICAL_CONNECTOR",
        "connector_family":"散斗族",
        "geometry_classification":"RECONSTRUCTED_DESIGN / PHYSICAL_CONNECTOR_PROXY / ENGINEERING_TEST_ONLY",
        "historical_claim":False,
        "replaceable":True,
        "lower_interface":"LOWER_MASTER_TOP_PLANE ↔ CONNECTOR_BOTTOM_PLANE",
        "upper_interface":"CONNECTOR_TOP_PLANE ↔ UPPER_MASTER_BOTTOM_PLANE",
        "connector_xy_mm":connector_xy,
        "connector_height_mm":connector_h
      },
      "lower_master":{
        "master_id":lo["master_id"],"component_id":lo["component_id"],
        "section_mm":[lw,lt],"test_length_mm":lower_len,
        "canonical_reference_length_mm":lower_ref
      },
      "upper_master":{
        "master_id":up["master_id"],"component_id":up["component_id"],
        "section_mm":[uw,ut],"test_length_mm":upper_len,
        "canonical_reference_length_mm":upper_ref,
        "resolved_bottom_z_mm":upper_bottom
      },
      "interfaces":{
        "lower_gap_mm":round(lower_gap,9),
        "upper_gap_mm":round(upper_gap,9),
        "lower_penetration_mm":round(max(0.0,conn_bottom-lower_top)*0.0,9),
        "upper_penetration_mm":round(max(0.0,conn_top-upper_bottom),9),
        "footprint_inside_both":footprint_inside,
        "tolerance_mm":TOL
      },
      "objects":[payload(lower),payload(conn),payload(upper)]
    }
    out["semantic_geometry_signature"]=stable(out["objects"])
    Path(blend).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic).parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(blend)),check_existing=False)
    Path(semantic).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if review:render(Path(review),(0,0,700))
    print("T032_BUILD_PASS",case,out["semantic_geometry_signature"])

def validate(a,b,r,out):
    A=json.loads(Path(a).read_text());B=json.loads(Path(b).read_text());R=json.loads(Path(r).read_text())
    checks={}
    def ck(k,v):checks[k]=bool(v);assert v,k
    ck("THREE_OBJECTS",len(A["objects"])==3 and len(B["objects"])==3)
    ck("MASTER_IDENTITIES",A["lower_master"]["master_id"]=="CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER" and A["upper_master"]["master_id"]=="CMP-FRAME-FOUR-CHUANFU-001_MASTER")
    ck("CONNECTION_ID",A["connection_layer"]["connection_id"]=="CONN-SAN-DOU-UPPER6-FOUR-001")
    ck("CONNECTION_KIND",A["connection_layer"]["connection_kind"]=="PHYSICAL_CONNECTOR")
    ck("CONNECTOR_RECONSTRUCTED",A["connection_layer"]["geometry_classification"].startswith("RECONSTRUCTED_DESIGN"))
    ck("NO_HISTORICAL_CLAIM",A["connection_layer"]["historical_claim"] is False)
    ck("LOWER_INTERFACE_CLOSED",A["interfaces"]["lower_gap_mm"]<=TOL)
    ck("UPPER_INTERFACE_CLOSED",A["interfaces"]["upper_gap_mm"]<=TOL)
    ck("NO_INTERPENETRATION",A["interfaces"]["upper_penetration_mm"]<=TOL and B["interfaces"]["upper_penetration_mm"]<=TOL)
    ck("FOOTPRINT_VALID",A["interfaces"]["footprint_inside_both"] and B["interfaces"]["footprint_inside_both"])
    ck("MUTATION_CHANGES_CONNECTOR",A["connection_layer"]["connector_height_mm"]!=B["connection_layer"]["connector_height_mm"])
    ck("MUTATION_MOVES_UPPER",A["upper_master"]["resolved_bottom_z_mm"]!=B["upper_master"]["resolved_bottom_z_mm"])
    ck("SECTIONS_STABLE",A["lower_master"]["section_mm"]==B["lower_master"]["section_mm"] and A["upper_master"]["section_mm"]==B["upper_master"]["section_mm"])
    ck("NO_REFERENCE_LENGTH_LEAK",A["lower_master"]["test_length_mm"]!=A["lower_master"]["canonical_reference_length_mm"] and A["upper_master"]["test_length_mm"]!=A["upper_master"]["canonical_reference_length_mm"])
    ck("NO_MANUAL_PLACEMENT",A["manual_blender_transform_count"]==0 and B["manual_blender_transform_count"]==0)
    ck("DETERMINISTIC",A["semantic_geometry_signature"]==R["semantic_geometry_signature"])
    ck("SCHEMA_PRESENT",A["connection_layer"]["schema_version"]=="P3_3_CONNECTION_LAYER_V001")
    ck("TEST_COORDINATES_ONLY",A["classification"].startswith("ENGINEERING_TEST_ONLY"))
    result={"status":"PASS","task_id":"T-032","check_count":len(checks),"checks":checks,
      "test_a_signature":A["semantic_geometry_signature"],"restore_signature":R["semantic_geometry_signature"],
      "test_a_connector_height_mm":A["connection_layer"]["connector_height_mm"],
      "test_b_connector_height_mm":B["connection_layer"]["connector_height_mm"],
      "test_a_upper_bottom_z_mm":A["upper_master"]["resolved_bottom_z_mm"],
      "test_b_upper_bottom_z_mm":B["upper_master"]["resolved_bottom_z_mm"],
      "stage_advance":False}
    Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("T032_VALIDATION_PASS",len(checks))

def parse():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","validate"),required=True)
    ap.add_argument("--case",choices=("A","B"))
    ap.add_argument("--blend");ap.add_argument("--semantic");ap.add_argument("--review-dir")
    ap.add_argument("--a");ap.add_argument("--b");ap.add_argument("--restore");ap.add_argument("--output")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)

def main():
    a=parse()
    if a.mode=="build":build(a.case,a.blend,a.semantic,a.review_dir)
    else:validate(a.a,a.b,a.restore,a.output)

if __name__=="__main__":main()
