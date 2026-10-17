import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=0.1): return abs(float(a)-float(b))<=t

def font(size,bold=False):
    for p in [
      "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(p).exists():
            try:return ImageFont.truetype(p,size)
            except:pass
    return ImageFont.load_default()

def compose(a):
    c=load(a.canonical)
    rd=Path(a.review_dir)
    names=[
      "CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png",
      "CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png",
      "ORTHOGONAL_GONG_TOP_VIEW.png",
      "FRONT_NODE_DETAIL.png",
      "REAR_NODE_DETAIL.png",
      "FRONT_TUOJIAO_SIDE.png",
      "REAR_TUOJIAO_SIDE.png"
    ]
    ims=[Image.open(rd/n).convert("RGB") for n in names]
    W,H=2600,2000
    out=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(out)
    d.text((40,25),"MP-01B｜T-046 Tuojiao First Geometry Review Board",font=font(42,True),fill="black")
    d.text((40,82),"First-article diagonal envelopes only; exact historical endpoints, cuts and joinery remain UNKNOWN",font=font(19),fill="black")
    boxes=[
      (40,120,1260,650),(1340,120,2560,650),
      (40,690,850,1230),(895,690,1705,1230),(1750,690,2560,1230),
      (40,1270,1260,1830),(1340,1270,2560,1830)
    ]
    titles=["1 FRONT ELEVATION","2 AXONOMETRIC","3 TOP VIEW","4 FRONT NODE","5 REAR NODE","6 FRONT TUOJIAO","7 REAR TUOJIAO"]
    for b,t,im in zip(boxes,titles,ims):
        d.rectangle(b,outline="gray",width=2); d.text((b[0]+12,b[1]+10),t,font=font(22,True),fill="black")
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-60))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+52))
    tj=[x for x in c["objects"] if x["component_role"]=="TUOJIAO_FRAME_SUPPORT"]
    y=1860
    d.text((40,y),f"Tuojiao solids: {len(tj)} | Section: 237.1 × 153.7 mm family-mean completion | ΔY 1759.5 | ΔZ 933.3 | L 1991.705 | angle 27.943° | Z offset explicit/replacable",font=font(17),fill="black")
    Path(a.board).parent.mkdir(parents=True,exist_ok=True); out.save(a.board)
    print("MP01B_TUOJIAO_REVIEW_BOARD_PASS")

def validate(a):
    contract=load(a.contract); c=load(a.canonical); m=load(a.mutation); reopen=load(a.reopen); rebuild=load(a.rebuild)
    checks={}
    def ck(n,cond):
        if not cond: raise AssertionError(n)
        checks[n]="PASS"
    objs={x["logical_object_id"]:x for x in c["objects"]}
    mo={x["logical_object_id"]:x for x in m["objects"]}
    ck("01_task",c["task_id"]=="T-046")
    ck("02_object_count",c["rendered_physical_geometry_count"]==12 and len(objs)==12)
    ck("03_deferred_count",c["deferred_physical_participant_count"]==2)
    ids=["ASM-MP01B-TUOJIAO-FRONT-01","ASM-MP01B-TUOJIAO-REAR-01"]
    ck("04_tuojiao_ids",all(i in objs for i in ids))
    for side,i in zip(["FRONT","REAR"],ids):
        o=objs[i]; p=o["custom_properties"]
        ck(f"05_{side}_role",o["component_role"]=="TUOJIAO_FRAME_SUPPORT")
        ck(f"06_{side}_section",near(p["section_guang_mm"],237.1,0.01) and near(p["section_hou_mm"],153.7,0.01))
        ck(f"07_{side}_projection",near(p["horizontal_projection_mm"],1759.5,0.01))
        ck(f"08_{side}_rise",near(p["relative_rise_mm"],933.3,0.01))
        ck(f"09_{side}_length",near(p["centerline_length_mm"],1991.7050835904395,0.01))
        ck(f"10_{side}_angle",near(p["angle_deg"],27.943034423382937,0.001))
        ck(f"11_{side}_zoffset",near(p["z_offset_mm"],0,0.001) and "REPLACEABLE" in p["z_offset_classification"])
        ck(f"12_{side}_joinery",o["joinery_cut_count"]==0 and str(o["historical_joinery"]).startswith("UNKNOWN"))
        ck(f"13_{side}_historical_claim",o["historical_metric_claim"] is False and o["historical_full_length_claim"] is False)
    ck("14_relationship_counts",c["relationship_counts"]=={"SUPPORT":6,"LOCATE":12,"BELONG":4,"CONNECT":0})
    ck("15_no_connect",all(r["type"]!="CONNECT" for r in c["relationships"]))
    ck("16_reopen",reopen["status"]=="PASS" and reopen["logical_object_count"]==12)
    ck("17_rebuild",rebuild["assembly_signature"]==c["assembly_signature"])
    ck("18_mutation_z",all(near(mo[i]["custom_properties"]["z_offset_mm"],50,0.001) for i in ids))
    ck("19_mutation_tj_changes",all(mo[i]["world_geometry_signature"]!=objs[i]["world_geometry_signature"] for i in ids))
    invariant=[k for k in objs if k not in ids]
    ck("20_mutation_others_invariant",all(mo[k]["world_geometry_signature"]==objs[k]["world_geometry_signature"] for k in invariant))
    ck("21_joinery_global",c["joinery_cut_count"]==0 and c["historical_joinery"].startswith("UNKNOWN"))
    ck("22_no_whole_hall",c["whole_hall_claim"] is False and c["historical_exactness_claim"] is False)
    ck("23_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("24_blend_sha",c["blend_sha256"]==sha(a.asset))
    for idx,n in enumerate([
      "CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png","CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png",
      "ORTHOGONAL_GONG_TOP_VIEW.png","FRONT_NODE_DETAIL.png","REAR_NODE_DETAIL.png",
      "FRONT_TUOJIAO_SIDE.png","REAR_TUOJIAO_SIDE.png"],start=25):
        p=Path(a.review_dir)/n; im=Image.open(p).convert("L")
        ck(f"{idx:02d}_render",p.exists() and p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    ck("32_review_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)
    out={"status":"PASS","task_id":"T-046","check_count":len(checks),"checks":checks,
         "assembly_signature":c["assembly_signature"],"mutation_assembly_signature":m["assembly_signature"],
         "blend_sha256":sha(a.asset),"semantic_sha256":sha(a.canonical),"review_board_sha256":sha(a.board),
         "scope":"MP01B_TUOJIAO_FIRST_GEOMETRY_ONLY","historical_exactness_claim":False,
         "whole_frame_claim":False,"whole_hall_claim":False}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01B_TUOJIAO_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("compose-board","validate"))
    for n in ["contract","canonical","mutation","reopen","rebuild","asset","review_dir","board","output"]:
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    compose(a) if a.mode=="compose-board" else validate(a)

if __name__=="__main__": main()
