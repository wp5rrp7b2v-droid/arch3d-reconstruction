import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=0.1): return abs(float(a)-float(b))<=t

def font(size,bold=False):
    choices=[
      "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in choices:
        if Path(p).exists():
            try:return ImageFont.truetype(p,size)
            except:pass
    return ImageFont.load_default()

def wrap(draw,text,ft,maxw):
    words=text.split(" "); lines=[]; cur=""
    for w in words:
        cand=(cur+" "+w).strip()
        if cur and draw.textlength(cand,font=ft)>maxw:
            lines.append(cur); cur=w
        else: cur=cand
    if cur: lines.append(cur)
    return lines

def compose(a):
    c=load(a.canonical); m=load(a.mutation)
    rd=Path(a.review_dir)
    ims={
      "front":Image.open(rd/"CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png").convert("RGB"),
      "axon":Image.open(rd/"CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png").convert("RGB"),
      "top":Image.open(rd/"ORTHOGONAL_GONG_TOP_VIEW.png").convert("RGB"),
      "fnode":Image.open(rd/"FRONT_NODE_DETAIL.png").convert("RGB"),
      "rnode":Image.open(rd/"REAR_NODE_DETAIL.png").convert("RGB")
    }
    W,H=2600,1900
    out=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(out)
    ft=font(40,True); fh=font(23,True); fb=font(17); fs=font(15)
    d.text((45,25),"MP-01B Gate H-R4｜Corrected Lower Assembly Review Board",font=ft,fill="black")
    d.text((45,78),"Orthogonal bracket-node build / hidden cuts & joinery remain UNKNOWN",font=fb,fill="black")
    boxes=[
      (40,115,1255,650),(1345,115,2560,650),
      (40,690,850,1250),(895,690,1705,1250),(1750,690,2560,1250),
      (40,1290,860,1850),(900,1290,1700,1850),(1740,1290,2560,1850)
    ]
    titles=[
      "1 FRONT ELEVATION","2 AXONOMETRIC","3 ORTHOGONAL TOP VIEW",
      "4 FRONT NODE","5 REAR NODE","6 LUDOU / TUOFENG EVIDENCE",
      "7 HUAGONG ENDPOINT CONTROL","8 DEFERRED / UNKNOWN BOUNDARY"
    ]
    for b,t in zip(boxes,titles):
        d.rectangle(b,outline="gray",width=2)
        d.text((b[0]+12,b[1]+10),t,font=fh,fill="black")
    def paste(im,b):
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-60))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+52))
    paste(ims["front"],boxes[0]); paste(ims["axon"],boxes[1]); paste(ims["top"],boxes[2])
    paste(ims["fnode"],boxes[3]); paste(ims["rnode"],boxes[4])

    b=boxes[5]; y=b[1]+60
    lines=[
      "FRONT Ludou: top 321×355, bottom 221×255; bottom depth 255 = reconstructed equal-side-inset completion.",
      "REAR Ludou: top 320×357, bottom 227×264; bottom depth 264 = reconstructed completion.",
      "FRONT Tuofeng vertical contribution: 172.9 mm.",
      "REAR Tuofeng vertical contribution: 196 mm.",
      "Gong-seat reference: Z=306 mm at both nodes.",
      "Physical Ludou tops: FRONT 398 mm / REAR 415 mm."
    ]
    for line in lines:
        for q in wrap(d,line,fb,b[2]-b[0]-30):
            d.text((b[0]+15,y),q,font=fb,fill="black"); y+=29
        y+=8

    b=boxes[6]; y=b[1]+60
    lines=[
      "Huagong direction: 进深 / assembly Y.",
      "Realization length: 900 mm = source-image-calibrated PROJECT COMPLETION, not direct historical full length.",
      "FRONT: inner gong-head Y=+1186; outer Tuojiao control Y=+2086.",
      "REAR: inner gong-head Y=-1186; outer Tuojiao control Y=-2086.",
      "Mutation proof: 900→950 mm holds outer Tuojiao endpoint fixed and moves only the inner endpoint/midpoint."
    ]
    for line in lines:
        for q in wrap(d,line,fb,b[2]-b[0]-30):
            d.text((b[0]+15,y),q,font=fb,fill="black"); y+=29
        y+=8

    b=boxes[7]; y=b[1]+60
    lines=[
      "Rendered physical geometries: 10.",
      "Deferred physical participants: 2 Panjian Fang records; no fabricated solid geometry.",
      "Linggong = 顺身 / assembly X. Huagong = 进深 / assembly Y.",
      "Huagong/Linggong overlap = BRACKET_INTERLOCK_ZONE; exact cuts are UNKNOWN.",
      "Pingliang underside = Z521 with ±2 mm reconciliation against direct Linggong envelopes.",
      "No CONNECT relation; joinery cut count = 0.",
      "PASS does not establish historical exactness or whole-hall scalability."
    ]
    for line in lines:
        for q in wrap(d,line,fs,b[2]-b[0]-30):
            d.text((b[0]+15,y),q,font=fs,fill="black"); y+=26
        y+=6
    Path(a.board).parent.mkdir(parents=True,exist_ok=True)
    out.save(a.board)
    print("MP01B_GATE_H_R4_REVIEW_BOARD_PASS")

def validate(a):
    contract=load(a.contract); c=load(a.canonical); m=load(a.mutation); reopen=load(a.reopen); rebuild=load(a.rebuild)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    objs={x["logical_object_id"]:x for x in c["objects"]}
    mo={x["logical_object_id"]:x for x in m["objects"]}
    def dims(o): return o["world_bbox_mm"]["dimensions"]
    def wmin(o,i): return o["world_bbox_mm"]["min"][i]
    def wmax(o,i): return o["world_bbox_mm"]["max"][i]

    ck("01_task",c["task_id"]=="T-045")
    ck("02_object_count",c["rendered_physical_geometry_count"]==10 and len(objs)==10)
    ck("03_deferred_count",c["deferred_physical_participant_count"]==2)
    ck("04_deferred_no_geometry",all(x["geometry_generated"] is False for x in c["deferred_physical_participants"]))
    ck("05_support_stations",contract["coordinate_system"]["support_stations_y_mm"]=={"front":1836,"rear":-1836})

    fc=objs["四椽栿-东缝"]; pl=objs["平梁-东缝"]
    ck("06_fc_dims",all(near(x,y,0.01) for x,y in zip(dims(fc),[426.5,7192,302])))
    ck("07_pl_dims",all(near(x,y,0.01) for x,y in zip(dims(pl),[395.5,3672,280.5])))
    ck("08_fc_z",near(wmin(fc,2),-302,0.01) and near(wmax(fc,2),0,0.01))
    ck("09_pl_z",near(wmin(pl,2),521,0.01) and near(wmax(pl,2),801.5,0.01))
    ck("10_beam_hist_claims",fc["historical_full_length_claim"] is False and pl["historical_full_length_claim"] is False)

    fl=objs["ASM-MP01B-LINGGONG-FRONT-01"]; rl=objs["ASM-MP01B-LINGGONG-REAR-01"]
    ck("11_linggong_front_dims",all(near(x,y,0.01) for x,y in zip(dims(fl),[1016,149,213])))
    ck("12_linggong_rear_dims",all(near(x,y,0.01) for x,y in zip(dims(rl),[995,150,217])))
    ck("13_linggong_axis",fl["axis_semantics"]=="local X -> assembly X / 顺身" and rl["axis_semantics"]=="local X -> assembly X / 顺身")
    ck("14_no_893_3_leak",all(not near(v,893.3,0.001) for o in [fl,rl] for v in o["local_bbox_mm"]["dimensions"]))

    fh=objs["ASM-MP01B-HUAGONG-FRONT-01"]; rh=objs["ASM-MP01B-HUAGONG-REAR-01"]
    ck("15_huagong_front_dims",all(near(x,y,0.01) for x,y in zip(dims(fh),[153,900,221])))
    ck("16_huagong_rear_dims",all(near(x,y,0.01) for x,y in zip(dims(rh),[156,900,210])))
    ck("17_huagong_axis",fh["axis_semantics"]=="local X -> assembly Y / 进深" and rh["axis_semantics"]=="local X -> assembly Y / 进深")
    ck("18_huagong_not_direct","SOURCE_IMAGE_CALIBRATED_PROJECT_COMPLETION" in fh["evidence_class"] and "SOURCE_IMAGE_CALIBRATED_PROJECT_COMPLETION" in rh["evidence_class"])
    ck("19_huagong_endpoints",near(wmin(fh,1),1186,0.01) and near(wmax(fh,1),2086,0.01) and near(wmin(rh,1),-2086,0.01) and near(wmax(rh,1),-1186,0.01))
    ck("20_no_outer_huagong_master",all(o["master_id"]!="CMP-GONG-HUAGONG-001_MASTER" for o in [fh,rh]))

    ft=objs["ASM-MP01B-TUOFENG-FRONT-01"]; rt=objs["ASM-MP01B-TUOFENG-REAR-01"]
    ck("21_tuofeng_heights",near(dims(ft)[2],172.9,0.01) and near(dims(rt)[2],196,0.01))
    ck("22_tuofeng_front_plan",near(dims(ft)[0],426.5,0.01) and near(dims(ft)[1],355,0.01))
    ck("23_tuofeng_rear_plan",near(dims(rt)[0],426.5,0.01) and near(dims(rt)[1],357,0.01))

    fld=objs["ASM-MP01B-PANJIAN-LUDOU-FRONT-01"]; rld=objs["ASM-MP01B-PANJIAN-LUDOU-REAR-01"]
    ck("24_ludou_front_dims",all(near(x,y,0.01) for x,y in zip(dims(fld),[321,355,225.1])))
    ck("25_ludou_rear_dims",all(near(x,y,0.01) for x,y in zip(dims(rld),[320,357,219])))
    ck("26_ludou_bottom_depth_class",fld["geometry_basis"].endswith("COMPLETED_BOTTOM_DEPTH") and rld["geometry_basis"].endswith("COMPLETED_BOTTOM_DEPTH"))
    ck("27_no_column_head_ludou",all(o["master_id"]!="CMP-LUDOU-COLUMN-001_MASTER" for o in [fld,rld]))
    ck("28_ludou_bottom_z",near(wmin(fld,2),172.9,0.01) and near(wmin(rld,2),196,0.01))
    ck("29_ludou_top_z",near(wmax(fld,2),398,0.01) and near(wmax(rld,2),415,0.01))

    ck("30_gong_seat_front",near(wmin(fl,2),306,0.01) and near(wmin(fh,2),306,0.01))
    ck("31_gong_seat_rear",near(wmin(rl,2),306,0.01) and near(wmin(rh,2),306,0.01))
    ck("32_bearing_front",near(wmax(fl,2)-wmin(pl,2),-2,0.01))
    ck("33_bearing_rear",near(wmax(rl,2)-wmin(pl,2),2,0.01))

    def overlap(a,b):
        return all(min(wmax(a,i),wmax(b,i))>max(wmin(a,i),wmin(b,i)) for i in range(3))
    ck("34_interlock_front",overlap(fl,fh))
    ck("35_interlock_rear",overlap(rl,rh))
    ck("36_interlock_semantics","BRACKET_INTERLOCK" in c["bracket_interlock"])
    ck("37_joinery_unknown",c["historical_joinery"].startswith("UNKNOWN") and c["joinery_cut_count"]==0)
    ck("38_no_whole_hall",c["whole_hall_claim"] is False)

    rc=c["relationship_counts"]
    ck("39_relation_counts",rc=={"SUPPORT":6,"LOCATE":8,"BELONG":2,"CONNECT":0})
    ck("40_no_connect",all(r["type"]!="CONNECT" for r in c["relationships"]))

    ck("41_reopen",reopen["status"]=="PASS" and reopen["logical_object_count"]==10)
    ck("42_rebuild",rebuild["assembly_signature"]==c["assembly_signature"] and {x["logical_object_id"]:x["world_geometry_signature"] for x in rebuild["objects"]}=={x["logical_object_id"]:x["world_geometry_signature"] for x in c["objects"]})

    ck("43_mutation_len",near(m["huagong_realization_length_mm"],950,0.001))
    mfh=mo["ASM-MP01B-HUAGONG-FRONT-01"]; mrh=mo["ASM-MP01B-HUAGONG-REAR-01"]
    ck("44_mutation_outer_fixed",near(wmax(mfh,1),2086,0.01) and near(wmin(mrh,1),-2086,0.01))
    ck("45_mutation_inner_moves",near(wmin(mfh,1),1136,0.01) and near(wmax(mrh,1),-1136,0.01))
    ck("46_mutation_sections",near(dims(mfh)[0],153,0.01) and near(dims(mfh)[2],221,0.01) and near(dims(mrh)[0],156,0.01) and near(dims(mrh)[2],210,0.01))
    invariant=[k for k in objs if "HUAGONG" not in k]
    ck("47_mutation_others_invariant",all(mo[k]["world_geometry_signature"]==objs[k]["world_geometry_signature"] for k in invariant))
    ck("48_mutation_evidence_invariant",all(mo[k]["evidence_class"]==objs[k]["evidence_class"] for k in objs))
    ck("49_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("50_blend_sha",c["blend_sha256"]==sha(a.asset))

    for idx,n in enumerate([
      "CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION.png","CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC.png",
      "ORTHOGONAL_GONG_TOP_VIEW.png","FRONT_NODE_DETAIL.png","REAR_NODE_DETAIL.png"
    ],start=51):
        p=Path(a.review_dir)/n; im=Image.open(p).convert("L")
        ck(f"{idx:02d}_render",p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    ck("56_review_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)

    out={
      "status":"PASS","task_id":"T-045","check_count":len(checks),"checks":checks,
      "assembly_signature":c["assembly_signature"],
      "mutation_assembly_signature":m["assembly_signature"],
      "blend_sha256":sha(a.asset),"semantic_sha256":sha(a.canonical),
      "review_board_sha256":sha(a.board),
      "scope":"MP01B_CORRECTED_LOWER_SUPPORT_MINIMUM_PROOF_ONLY",
      "historical_exactness_claim":False,"whole_frame_claim":False,"whole_hall_claim":False
    }
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01B_GATE_H_R4_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("compose-board","validate"))
    for n in ["contract","canonical","mutation","reopen","rebuild","asset","review_dir","board","output"]:
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)

if __name__=="__main__":
    main()
