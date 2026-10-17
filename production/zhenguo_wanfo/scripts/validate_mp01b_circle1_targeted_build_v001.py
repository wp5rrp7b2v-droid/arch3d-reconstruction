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
            except: pass
    return ImageFont.load_default()

def compose(a):
    c=load(a.canonical)
    rd=Path(a.review_dir)
    names=[
      "CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png",
      "CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png",
      "FRONT_NODE_DETAIL.png",
      "REAR_NODE_DETAIL.png",
      "FRONT_HUAGONG_PROFILE_DETAIL.png",
      "REAR_HUAGONG_PROFILE_DETAIL.png"
    ]
    ims=[Image.open(rd/n).convert("RGB") for n in names]
    W,H=2600,1880
    out=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(out)
    d.text((40,24),"MP-01B｜T-047 Circle 1 Targeted Build Review Board",font=font(42,True),fill="black")
    d.text((40,78),"Only interior-Huagong visible gong-head profile changed; T046 Tuojiao and all other geometry are frozen",font=font(19),fill="black")
    boxes=[
      (40,115,1260,620),(1340,115,2560,620),
      (40,660,1260,1160),(1340,660,2560,1160),
      (40,1200,1260,1760),(1340,1200,2560,1760)
    ]
    titles=["1 FRONT ELEVATION","2 AXONOMETRIC","3 FRONT NODE","4 REAR NODE","5 FRONT HUAGONG PROFILE","6 REAR HUAGONG PROFILE"]
    for b,t,im in zip(boxes,titles,ims):
        d.rectangle(b,outline="gray",width=2); d.text((b[0]+12,b[1]+10),t,font=font(22,True),fill="black")
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-60))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+52))
    hg=[x for x in c["objects"] if x["component_role"]=="INTERIOR_HUAGONG"]
    d.text((40,1800),f"Huagong solids: {len(hg)} | 900 mm total | 650 mm visible gong-head zone | 250 mm Tuojiao zone | joinery cuts 0 | Circle 2/3 remain OPEN",font=font(18),fill="black")
    Path(a.board).parent.mkdir(parents=True,exist_ok=True); out.save(a.board)
    print("MP01B_CIRCLE1_REVIEW_BOARD_PASS")

def validate(a):
    prep=load(a.prep); profile=load(a.profile); c=load(a.canonical); m=load(a.mutation); reopen=load(a.reopen); rebuild=load(a.rebuild)
    checks={}
    def ck(n,cond):
        if not cond: raise AssertionError(n)
        checks[n]="PASS"
    objs={x["logical_object_id"]:x for x in c["objects"]}
    mo={x["logical_object_id"]:x for x in m["objects"]}
    hgids=["ASM-MP01B-HUAGONG-FRONT-01","ASM-MP01B-HUAGONG-REAR-01"]
    ck("01_task",c["task_id"]=="T-047")
    ck("02_scope",prep["scope"]=="CIRCLE_1_INTERIOR_HUAGONG_VISIBLE_PROFILE_ONLY")
    ck("03_authorized",prep["product_owner_authorization"]["authorized"] is True and prep["blender_authorized"] is True)
    ck("04_profile_approved",profile["product_owner_approved"] is True and profile["candidate_id"]=="MP01B_INTERIOR_HUAGONG_VISIBLE_PROFILE_V001_C01")
    ck("05_object_count",c["rendered_physical_geometry_count"]==12 and len(objs)==12)
    ck("06_deferred_count",c["deferred_physical_participant_count"]==2)
    ck("07_huagong_ids",all(i in objs for i in hgids))
    ck("08_huagong_changed_from_t046",all(objs[i]["world_geometry_signature"]!=prep["huagong_baseline_signatures"][i] for i in hgids))
    for i in hgids:
        p=objs[i]["custom_properties"]
        ck("09_"+i+"_candidate",p["profile_candidate_id"]==profile["candidate_id"])
        ck("10_"+i+"_length",near(p["realization_length_mm"],900,0.001))
        ck("11_"+i+"_zones",near(p["inward_gonghead_reach_mm"],650,0.001) and near(p["outward_tuojiao_reach_mm"],250,0.001))
        ck("12_"+i+"_tip",near(p["tip_depth_fraction"],0.15,0.0001))
        ck("13_"+i+"_no_t040",p["t040_profile_reuse"] is False)
        ck("14_"+i+"_no_hist_curve",p["exact_historical_curve_claim"] is False)
        ck("15_"+i+"_joinery",objs[i]["joinery_cut_count"]==0)
    fh=objs[hgids[0]]; rh=objs[hgids[1]]
    ck("16_front_bbox",all(near(x,y,0.01) for x,y in zip(fh["world_bbox_mm"]["dimensions"],[153,900,221])))
    ck("17_rear_bbox",all(near(x,y,0.01) for x,y in zip(rh["world_bbox_mm"]["dimensions"],[156,900,210])))
    # Endpoints remain the existing T3 controls.
    ck("18_front_endpoints",near(fh["world_bbox_mm"]["min"][1],1186,0.01) and near(fh["world_bbox_mm"]["max"][1],2086,0.01))
    ck("19_rear_endpoints",near(rh["world_bbox_mm"]["min"][1],-2086,0.01) and near(rh["world_bbox_mm"]["max"][1],-1186,0.01))
    # Every non-Huagong world geometry signature must equal approved T046.
    frozen=prep["frozen_object_signatures"]
    ck("20_frozen_geometry",all(objs[k]["world_geometry_signature"]==sig for k,sig in frozen.items()))
    tuos=["ASM-MP01B-TUOJIAO-FRONT-01","ASM-MP01B-TUOJIAO-REAR-01"]
    ck("21_tuojiao_frozen",all(objs[k]["world_geometry_signature"]==frozen[k] for k in tuos))
    ck("22_reopen",reopen["status"]=="PASS" and reopen["logical_object_count"]==12)
    ck("23_rebuild",rebuild["assembly_signature"]==c["assembly_signature"])
    ck("24_mutation_profile",all(near(mo[i]["custom_properties"]["tip_depth_fraction"],0.25,0.0001) for i in hgids))
    ck("25_mutation_changes_huagong",all(mo[i]["world_geometry_signature"]!=objs[i]["world_geometry_signature"] for i in hgids))
    invariant=[k for k in objs if k not in hgids]
    ck("26_mutation_other_geometry_invariant",all(mo[k]["world_geometry_signature"]==objs[k]["world_geometry_signature"] for k in invariant))
    ck("27_relationship_counts",c["relationship_counts"]=={"SUPPORT":6,"LOCATE":12,"BELONG":4,"CONNECT":0})
    ck("28_joinery_global",c["joinery_cut_count"]==0 and c["historical_joinery"].startswith("UNKNOWN"))
    ck("29_no_exactness",c["historical_exactness_claim"] is False and c["whole_hall_claim"] is False)
    ck("30_profile_hash",c["profile_control_sha256"]==sha(a.profile))
    ck("31_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("32_blend_sha",c["blend_sha256"]==sha(a.asset))
    renders=[
      "CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png","CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png",
      "ORTHOGONAL_GONG_TOP_VIEW.png","FRONT_NODE_DETAIL.png","REAR_NODE_DETAIL.png",
      "FRONT_TUOJIAO_SIDE.png","REAR_TUOJIAO_SIDE.png","FRONT_HUAGONG_PROFILE_DETAIL.png","REAR_HUAGONG_PROFILE_DETAIL.png"
    ]
    for idx,n in enumerate(renders,start=33):
        p=Path(a.review_dir)/n; im=Image.open(p).convert("L")
        ck(f"{idx:02d}_render",p.exists() and p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    ck("42_review_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)
    ck("43_circle2_open",profile["circle_2_resolved"] is False)
    ck("44_circle3_open",profile["circle_3_resolved"] is False)
    out={
      "status":"PASS","task_id":"T-047","check_count":len(checks),"checks":checks,
      "assembly_signature":c["assembly_signature"],"mutation_assembly_signature":m["assembly_signature"],
      "blend_sha256":sha(a.asset),"semantic_sha256":sha(a.canonical),"review_board_sha256":sha(a.board),
      "scope":"CIRCLE_1_INTERIOR_HUAGONG_VISIBLE_PROFILE_ONLY",
      "circle_2_resolved":False,"circle_3_resolved":False,"mp01b_accepted":False,"merge_authorized":False
    }
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01B_CIRCLE1_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("compose-board","validate"))
    for n in ["prep","profile","canonical","mutation","reopen","rebuild","asset","review_dir","board","output"]:
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    compose(a) if a.mode=="compose-board" else validate(a)

if __name__=="__main__": main()
