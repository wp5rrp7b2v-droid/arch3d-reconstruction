"""T-031 two-piece Micro Assembly Proof: 四椽栿 + 托脚.
Run only in Blender background mode. Test coordinates are ENGINEERING_TEST_ONLY.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
FOUR_PARAMS = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-FOUR-CHUANFU-001/CMP-FRAME-FOUR-CHUANFU-001_MASTER_PARAMS_V001.json"
TUOJIAO_DEF = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-TUOJIAO-001/CMP-FRAME-TUOJIAO-001_MASTER_DEFINITION_V001.json"

TOL = 0.1

def stable_sig(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load_inputs():
    f=json.loads(FOUR_PARAMS.read_text(encoding="utf-8"))
    t=json.loads(TUOJIAO_DEF.read_text(encoding="utf-8"))
    assert f["component_id"]=="CMP-FRAME-FOUR-CHUANFU-001"
    assert f["master_id"]=="CMP-FRAME-FOUR-CHUANFU-001_MASTER"
    assert t["component_id"]=="CMP-FRAME-TUOJIAO-001"
    assert t["master_id"]=="CMP-FRAME-TUOJIAO-001_MASTER"
    fp={x["key"]:x for x in f["parameters"]}
    fw=float(fp["width_mm"]["value"]); ft=float(fp["thickness_mm"]["value"])
    tw=float(t["geometry_contract"]["section_envelope_mm"]["width"])
    tt=float(t["geometry_contract"]["section_envelope_mm"]["thickness"])
    assert float(fp["canonical_reference_length_mm"]["value"])==1000
    assert float(t["geometry_contract"]["canonical_reference_length_mm"])==1000
    return f,t,fw,ft,tw,tt

def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for c in list(bpy.data.collections):
        if c != bpy.context.scene.collection:
            bpy.data.collections.remove(c)

def setup_scene():
    s=bpy.context.scene
    s.unit_settings.system="METRIC"
    s.unit_settings.scale_length=0.001
    s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_EEVEE_NEXT"
    s.render.resolution_x=1200
    s.render.resolution_y=900
    s.render.resolution_percentage=100
    s.render.image_settings.file_format="PNG"
    s.world.use_nodes=True
    bg=next(n for n in s.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.92,0.92,0.92,1)
    bg.inputs["Strength"].default_value=1.0
    s["proof_id"]="T-031"
    s["coordinate_classification"]="ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES"

def box_mesh(name, verts, component_id, master_id, role):
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    mesh=bpy.data.meshes.new(name+"__MESH")
    mesh.from_pydata([tuple(v) for v in verts],[],faces)
    mesh.update()
    obj=bpy.data.objects.new(name,mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj["component_id"]=component_id
    obj["master_id"]=master_id
    obj["assembly_role"]=role
    obj["placement_authority"]="SCRIPTED_ENGINEERING_TEST_ONLY"
    return obj

def axis_box_vertices(center, ex, ey, ez, length, width, thickness):
    c=Vector(center); ex=Vector(ex); ey=Vector(ey); ez=Vector(ez)
    out=[]
    for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
        p=c+ex*(sx*length/2)+ey*(sy*width/2)+ez*(sz*thickness/2)
        out.append([float(p.x),float(p.y),float(p.z)])
    return out

def solve_tangent_upper_center(lower, contact_target, thickness):
    lower=Vector(lower); target=Vector(contact_target)
    upper=target.copy()
    for _ in range(40):
        ex=(upper-lower).normalized()
        ey=Vector((0,1,0))
        ez=ex.cross(ey).normalized()
        if ez.z<0: ez=-ez
        nxt=target-ez*(thickness/2)
        if (nxt-upper).length<1e-9:
            upper=nxt
            break
        upper=nxt
    ex=(upper-lower).normalized()
    ey=Vector((0,1,0))
    ez=ex.cross(ey).normalized()
    if ez.z<0: ez=-ez
    return upper,ex,ey,ez

def geom_payload(obj):
    verts=[[round(float(v.co[i]),6) for i in range(3)] for v in obj.data.vertices]
    faces=[list(p.vertices) for p in obj.data.polygons]
    return {"name":obj.name,"vertices_mm":verts,"faces":faces,
            "component_id":obj["component_id"],"master_id":obj["master_id"],
            "assembly_role":obj["assembly_role"]}

def render_views(outdir, target):
    outdir.mkdir(parents=True,exist_ok=True)
    s=bpy.context.scene
    def mat(name,val):
        m=bpy.data.materials.new(name);m.diffuse_color=(val,val,val,1);return m
    for i,o in enumerate([x for x in s.objects if x.type=="MESH"]):
        o.data.materials.append(mat("M"+str(i),0.35+0.25*i))
    camd=bpy.data.cameras.new("T031_CAMERA")
    cam=bpy.data.objects.new("T031_CAMERA",camd)
    s.collection.objects.link(cam);s.camera=cam;camd.type="ORTHO";camd.clip_end=100000
    for name,pos,scale in [
        ("FRONT",(0,-6000,1200),4200),
        ("AXON",(4200,-5200,3600),4700),
    ]:
        cam.location=pos
        cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
        camd.ortho_scale=scale
        s.render.filepath=str(outdir/(name+".png"))
        bpy.ops.render.render(write_still=True)

def build(case, blend_path, semantic_path, review_dir=None):
    f,t,fw,ft,tw,tt=load_inputs()
    clear_scene();setup_scene()
    beam_len=2400.0
    beam_bottom=1200.0
    beam_center=(0.0,0.0,beam_bottom+ft/2)
    beam_verts=axis_box_vertices(beam_center,(1,0,0),(0,1,0),(0,0,1),beam_len,fw,ft)
    beam=box_mesh("ASM__FOUR_CHUANFU",beam_verts,f["component_id"],f["master_id"],"SUPPORTED_MEMBER")
    contact_x=-900.0 if case=="A" else -700.0
    lower=Vector((-1600.0,0.0,0.0))
    contact=Vector((contact_x,0.0,beam_bottom))
    upper,ex,ey,ez=solve_tangent_upper_center(lower,contact,tt)
    length=(upper-lower).length
    center=(upper+lower)/2
    tverts=axis_box_vertices(center,ex,ey,ez,length,tw,tt)
    tj=box_mesh("ASM__TUOJIAO",tverts,t["component_id"],t["master_id"],"SUPPORT")
    positive_end=[Vector(tverts[i]) for i in (1,2,5,6)]
    maxz=max(p.z for p in positive_end)
    contact_gap=abs(maxz-beam_bottom)
    penetration=max(0.0,maxz-beam_bottom)
    target_inside_beam=(-beam_len/2<=contact_x<=beam_len/2 and tw<=fw+TOL)
    payload={
      "proof_id":"T-031",
      "case":"TEST_"+case,
      "classification":"ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES",
      "manual_blender_transform_count":0,
      "four_chuanfu":{
        "component_id":f["component_id"],"master_id":f["master_id"],
        "section_mm":[fw,ft],"assembly_test_length_mm":beam_len,
        "canonical_reference_length_mm":1000,"reference_length_leaked":beam_len==1000,
        "bottom_plane_z_mm":beam_bottom
      },
      "tuojiao":{
        "component_id":t["component_id"],"master_id":t["master_id"],
        "section_mm":[tw,tt],"derived_length_mm":round(length,6),
        "derived_direction":[round(float(x),9) for x in ex],
        "lower_anchor_mm":[round(float(x),6) for x in lower],
        "upper_center_mm":[round(float(x),6) for x in upper],
        "support_target_mm":[round(float(x),6) for x in contact],
        "canonical_reference_length_mm":1000,
        "fixed_angle":False
      },
      "contact":{
        "gap_mm":round(contact_gap,9),
        "penetration_mm":round(penetration,9),
        "target_inside_beam":target_inside_beam,
        "tolerance_mm":TOL
      },
      "objects":[geom_payload(beam),geom_payload(tj)]
    }
    payload["semantic_geometry_signature"]=stable_sig(payload["objects"])
    blend_path=Path(blend_path);semantic_path=Path(semantic_path)
    blend_path.parent.mkdir(parents=True,exist_ok=True)
    semantic_path.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path),check_existing=False)
    semantic_path.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if review_dir: render_views(Path(review_dir),(0,0,1000))
    print("T031_BUILD_PASS",case,payload["semantic_geometry_signature"])

def validate(a,b,restore,out):
    A=json.loads(Path(a).read_text());B=json.loads(Path(b).read_text());R=json.loads(Path(restore).read_text())
    checks={}
    def ck(k,v): checks[k]=bool(v); assert v,k
    ck("A_TWO_OBJECTS",len(A["objects"])==2)
    ck("B_TWO_OBJECTS",len(B["objects"])==2)
    ck("IDENTITIES_PRESERVED",A["four_chuanfu"]["master_id"]=="CMP-FRAME-FOUR-CHUANFU-001_MASTER" and A["tuojiao"]["master_id"]=="CMP-FRAME-TUOJIAO-001_MASTER")
    ck("REFERENCE_LENGTH_NOT_LEAKED",not A["four_chuanfu"]["reference_length_leaked"] and A["tuojiao"]["derived_length_mm"]!=1000)
    ck("A_CONTACT_CLOSED",A["contact"]["gap_mm"]<=TOL and A["contact"]["penetration_mm"]<=TOL)
    ck("B_CONTACT_CLOSED",B["contact"]["gap_mm"]<=TOL and B["contact"]["penetration_mm"]<=TOL)
    ck("TARGETS_INSIDE_BEAM",A["contact"]["target_inside_beam"] and B["contact"]["target_inside_beam"])
    ck("MUTATION_CHANGES_TUOJIAO",A["tuojiao"]["derived_length_mm"]!=B["tuojiao"]["derived_length_mm"] or A["tuojiao"]["derived_direction"]!=B["tuojiao"]["derived_direction"])
    ck("SECTIONS_STABLE",A["four_chuanfu"]["section_mm"]==B["four_chuanfu"]["section_mm"] and A["tuojiao"]["section_mm"]==B["tuojiao"]["section_mm"])
    ck("NO_MANUAL_PLACEMENT",A["manual_blender_transform_count"]==0 and B["manual_blender_transform_count"]==0)
    ck("TEST_COORDINATES_ONLY",A["classification"].startswith("ENGINEERING_TEST_ONLY") and B["classification"].startswith("ENGINEERING_TEST_ONLY"))
    ck("DETERMINISTIC_REBUILD",A["semantic_geometry_signature"]==R["semantic_geometry_signature"])
    result={"status":"PASS","task_id":"T-031","check_count":len(checks),"checks":checks,
            "test_a_signature":A["semantic_geometry_signature"],"restore_signature":R["semantic_geometry_signature"],
            "test_a_tuijiao_length_mm":A["tuojiao"]["derived_length_mm"],
            "test_b_tuijiao_length_mm":B["tuojiao"]["derived_length_mm"],
            "stage_advance":False}
    Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("T031_VALIDATION_PASS",len(checks))

def args():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","validate"),required=True)
    ap.add_argument("--case",choices=("A","B"))
    ap.add_argument("--blend")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--a");ap.add_argument("--b");ap.add_argument("--restore");ap.add_argument("--output")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)

def main():
    a=args()
    if a.mode=="build":
        build(a.case,a.blend,a.semantic,a.review_dir)
    else:
        validate(a.a,a.b,a.restore,a.output)

if __name__=="__main__":
    main()
