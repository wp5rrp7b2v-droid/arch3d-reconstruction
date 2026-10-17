import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,tol=0.1): return abs(float(a)-float(b))<=tol

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

def compose(a):
    c=load(a.canonical); m=load(a.mutation)
    front=Image.open(Path(a.review_dir)/"LOWER_ASSEMBLY_FRONT_ELEVATION.png").convert("RGB")
    axon=Image.open(Path(a.review_dir)/"LOWER_ASSEMBLY_AXONOMETRIC.png").convert("RGB")
    detail=Image.open(Path(a.review_dir)/"SOUTH_SUPPORT_DETAIL.png").convert("RGB")
    mut=Image.open(Path(a.mutation_review_dir)/"MUTATION_306_TO_310.png").convert("RGB")
    W,H=2400,1800
    out=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(out)
    ft=font(38,True); fh=font(22,True); fb=font(17); fs=font(15)
    d.text((45,25),"MP-01B Gate H｜下部承托 First Engineering Build",font=ft,fill="black")
    d.text((45,76),"Minimum Proof / reconstructed support metrics remain replaceable / hidden joinery UNKNOWN",font=fb,fill="black")
    boxes=[
      (45,115,1165,690),(1235,115,2355,690),
      (45,735,780,1285),(830,735,1565,1285),
      (1615,735,2355,1285),(45,1330,2355,1750)
    ]
    titles=[
      "1 LOWER ASSEMBLY FRONT","2 LOWER ASSEMBLY AXONOMETRIC",
      "3 SOUTH SUPPORT DETAIL","4 MUTATION 306 → 310",
      "5 OBJECT / RELATION EVIDENCE","6 UNKNOWN / RECONSTRUCTION BOUNDARY"
    ]
    for b,t in zip(boxes,titles):
        d.rectangle(b,outline="gray",width=2); d.text((b[0]+12,b[1]+10),t,font=fh,fill="black")
    def paste(im,b):
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-58))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+52))
    paste(front,boxes[0]); paste(axon,boxes[1]); paste(detail,boxes[2]); paste(mut,boxes[3])

    b=boxes[4]; y=b[1]+55
    lines=[
      "Logical objects: 6",
      "V008: 四椽栿-东缝 / 平梁-东缝",
      "Reconstructed: 2 × Tuofeng + 2 × Interior Linggong",
      "SUPPORT relations: 6",
      "LOCATE relations: 4",
      "",
      "Contact planes:",
      "Z=0   Four-Chuanfu ↔ Tuofeng",
      "Z=91  Tuofeng ↔ Linggong",
      "Z=306 Linggong ↔ Pingliang",
      "",
      "Target Linggong analog ≠ direct target measurement."
    ]
    for line in lines:
        d.text((b[0]+14,y),line,font=fs,fill="black"); y+=34

    b=boxes[5]; y=b[1]+55
    lines=[
      "UNKNOWN retained: target Linggong exact dimensions/profile; Tuofeng historical dimensions/profile; exact contact-face shapes; hidden mortise/tenon/groove geometry; whole-hall support counts; mapping outside this Minimum Proof.",
      "",
      "RECONSTRUCTED / REPLACEABLE: 7192 & 3672 realization lengths; ±1836 support stations; 306 mm support clearance; target use of same-building interior Linggong analog; 91 mm Tuofeng residual; transforms and contact-plane decomposition.",
      "",
      "Mutation: clearance 306→310 changes only vertical dependency chain; Four-Chuanfu, member lengths, station Y, Linggong local envelope and Tuofeng plan footprint remain invariant.",
      "",
      "PASS here does not prove historical exactness, joinery, whole-frame completeness or whole-hall scalability."
    ]
    for line in lines:
        # simple wrap
        words=line.split(" "); cur=""
        for w in words:
            test=(cur+" "+w).strip()
            if d.textlength(test,font=fb)>2200 and cur:
                d.text((b[0]+18,y),cur,font=fb,fill="black"); y+=32; cur=w
            else: cur=test
        if cur:
            d.text((b[0]+18,y),cur,font=fb,fill="black"); y+=32
        y+=8
    Path(a.board).parent.mkdir(parents=True,exist_ok=True)
    out.save(a.board)
    print("MP01B_GATE_H_REVIEW_BOARD_PASS")

def validate(a):
    contract=load(a.contract); c=load(a.canonical); m=load(a.mutation); r=load(a.reopen); rb=load(a.rebuild)
    checks={}
    def ck(n,cond):
        if not cond: raise AssertionError(n)
        checks[n]="PASS"

    objs={x["logical_object_id"]:x for x in c["objects"]}
    ck("01_task",c["task_id"]=="T-044")
    ck("02_logical_object_count",c["logical_object_count"]==6 and len(objs)==6)
    phys={k for k,v in objs.items() if v["object_class"]=="V008_PHYSICAL_INSTANCE"}
    ck("03_v008_identities",phys=={"四椽栿-东缝","平梁-东缝"})
    tf=[v for v in objs.values() if v["master_id"]=="CMP-FRAME-TUOFENG-001_MASTER"]
    lg=[v for v in objs.values() if v["master_id"]=="CMP-FRAME-LINGGONG-INTERIOR-001_MASTER"]
    ck("04_two_tuofeng",len(tf)==2)
    ck("05_two_linggong",len(lg)==2)
    ck("06_no_whole_hall_count",all(v["whole_hall_count_claim"] is False for v in tf+lg))

    fc=objs["四椽栿-东缝"]; pl=objs["平梁-东缝"]
    def dims(o): return o["world_bbox_mm"]["dimensions"]
    ck("07_fc_envelope",all(near(x,y,0.01) for x,y in zip(dims(fc),[426.5,7192.0,302.0])))
    ck("08_pl_envelope",all(near(x,y,0.01) for x,y in zip(dims(pl),[395.5,3672.0,280.5])))
    ck("09_fc_z",near(fc["world_bbox_mm"]["min"][2],-302,0.01) and near(fc["world_bbox_mm"]["max"][2],0,0.01))
    ck("10_pl_z",near(pl["world_bbox_mm"]["min"][2],306,0.01) and near(pl["world_bbox_mm"]["max"][2],586.5,0.01))

    south_tf=objs["ASM-MP01B-TUOFENG-LOWER-SOUTH-01"]; north_tf=objs["ASM-MP01B-TUOFENG-LOWER-NORTH-01"]
    south_lg=objs["ASM-MP01B-LINGGONG-SOUTH-01"]; north_lg=objs["ASM-MP01B-LINGGONG-NORTH-01"]
    ck("11_support_stations",near(south_tf["translation_mm"][1],1836,0.001) and near(north_tf["translation_mm"][1],-1836,0.001) and near(south_lg["translation_mm"][1],1836,0.001) and near(north_lg["translation_mm"][1],-1836,0.001))
    ck("12_mirror_tf",near(south_tf["world_bbox_mm"]["min"][1],-north_tf["world_bbox_mm"]["max"][1],0.01) and near(south_tf["world_bbox_mm"]["max"][1],-north_tf["world_bbox_mm"]["min"][1],0.01))
    ck("13_mirror_lg",near(south_lg["world_bbox_mm"]["min"][1],-north_lg["world_bbox_mm"]["max"][1],0.01) and near(south_lg["world_bbox_mm"]["max"][1],-north_lg["world_bbox_mm"]["min"][1],0.01))
    ck("14_axis_mapping",all(v["axis_mapping"]=="LOCAL_X_TO_ASSEMBLY_Y / RZ_PLUS_90" and near(v["rotation_euler_deg"][2],90,0.001) for v in tf+lg))

    tol=float(contract["contact_planes"]["tolerance_mm"])
    def zmin(o): return o["world_bbox_mm"]["min"][2]
    def zmax(o): return o["world_bbox_mm"]["max"][2]
    for idx,(a1,a2,z) in enumerate([
      (fc,south_tf,0),(south_tf,south_lg,91),(south_lg,pl,306),
      (fc,north_tf,0),(north_tf,north_lg,91),(north_lg,pl,306)
    ],start=15):
        ck(f"{idx:02d}_contact",near(zmax(a1),z,tol) and near(zmin(a2),z,tol) and (zmax(a1)-zmin(a2))<=tol)

    ck("21_linggong_envelope",all(near(x,y,0.01) for x,y in zip(south_lg["world_bbox_mm"]["dimensions"],[153.6,893.3,215.0])) and all(near(x,y,0.01) for x,y in zip(north_lg["world_bbox_mm"]["dimensions"],[153.6,893.3,215.0])))
    ck("22_tuofeng_height",near(south_tf["world_bbox_mm"]["dimensions"][2],91,0.01) and near(north_tf["world_bbox_mm"]["dimensions"][2],91,0.01))

    forbidden_outer={897.0,217.4,155.6}
    canonical_numbers=set()
    for o in c["objects"]:
        canonical_numbers.update(round(float(x),3) for x in o["local_bbox_mm"]["dimensions"])
    ck("23_no_outer_eaves_leak",forbidden_outer.isdisjoint(canonical_numbers))
    forbidden_fixture={1000.0,500.0,180.0,550.0,120.0,1260.0,620.0,210.0,660.0,140.0}
    ck("24_no_first_article_fixture_leak",forbidden_fixture.isdisjoint(canonical_numbers))
    ck("25_reconstructed_not_historical",all(v["historical_metric_claim"] is False for v in tf+lg))
    ck("26_no_historical_full_length",fc["historical_full_length_claim"] is False and pl["historical_full_length_claim"] is False)
    ck("27_joinery_unknown",c["historical_joinery"].startswith("UNKNOWN") and c["joinery_cut_count"]==0 and all(str(v["historical_joinery"]).startswith("UNKNOWN") and v["joinery_cut_count"]==0 for v in objs.values()))
    ck("28_support_relations",c["support_relation_count"]==6 and sum(1 for x in c["relationships"] if x["type"]=="SUPPORT")==6)
    ck("29_locate_relations",c["locate_relation_count"]==4 and sum(1 for x in c["relationships"] if x["type"]=="LOCATE")==4)
    ck("30_relation_evidence",all(bool(x.get("evidence")) for x in c["relationships"]))
    ck("31_reopen",r["status"]=="PASS" and r["logical_object_count"]==6)
    ck("32_rebuild",rb["assembly_signature"]==c["assembly_signature"] and {x["logical_object_id"]:x["world_geometry_signature"] for x in rb["objects"]}=={x["logical_object_id"]:x["world_geometry_signature"] for x in c["objects"]})

    # Mutation / dependency propagation
    ck("33_mutation_clearance",near(m["clearance_mm"],310,0.001))
    ck("34_mutation_tuofeng_height",near(m["tuofeng_total_height_mm"],95,0.001))
    ck("35_mutation_linggong_z",near(m["linggong_bottom_z_mm"],95,0.001) and near(m["linggong_top_z_mm"],310,0.001))
    ck("36_mutation_pingliang_z",near(m["pingliang_bottom_z_mm"],310,0.001) and near(m["pingliang_top_z_mm"],590.5,0.001))
    mo={x["logical_object_id"]:x for x in m["objects"]}
    ck("37_mutation_fc_invariant",mo["四椽栿-东缝"]["world_geometry_signature"]==fc["world_geometry_signature"])
    ck("38_mutation_lengths_invariant",near(mo["四椽栿-东缝"]["local_bbox_mm"]["dimensions"][0],7192,0.001) and near(mo["平梁-东缝"]["local_bbox_mm"]["dimensions"][0],3672,0.001))
    ck("39_mutation_station_invariant",m["support_stations_y_mm"]==c["support_stations_y_mm"])
    ck("40_mutation_linggong_local_invariant",mo["ASM-MP01B-LINGGONG-SOUTH-01"]["local_geometry_signature"]==south_lg["local_geometry_signature"] and mo["ASM-MP01B-LINGGONG-NORTH-01"]["local_geometry_signature"]==north_lg["local_geometry_signature"])
    ck("41_mutation_tuofeng_plan_invariant",near(mo["ASM-MP01B-TUOFENG-LOWER-SOUTH-01"]["local_bbox_mm"]["dimensions"][0],south_tf["local_bbox_mm"]["dimensions"][0],0.001) and near(mo["ASM-MP01B-TUOFENG-LOWER-SOUTH-01"]["local_bbox_mm"]["dimensions"][1],south_tf["local_bbox_mm"]["dimensions"][1],0.001))
    ck("42_mutation_ids_invariant",set(mo)==set(objs))
    ck("43_mutation_evidence_invariant",all(mo[k]["evidence_class"]==objs[k]["evidence_class"] for k in objs))
    ck("44_mutation_joinery_invariant",m["historical_joinery"]==c["historical_joinery"]=="UNKNOWN / DEFERRED / NOT_MODELED")

    ck("45_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("46_blend_sha",c["blend_sha256"]==sha(a.asset))
    for idx,n in enumerate(["LOWER_ASSEMBLY_FRONT_ELEVATION.png","LOWER_ASSEMBLY_AXONOMETRIC.png","SOUTH_SUPPORT_DETAIL.png"],start=47):
        p=Path(a.review_dir)/n; im=Image.open(p).convert("L")
        ck(f"{idx:02d}_render",p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    p=Path(a.mutation_review_dir)/"MUTATION_306_TO_310.png"; im=Image.open(p).convert("L")
    ck("50_mutation_render",p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    ck("51_review_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)

    out={
      "status":"PASS",
      "task_id":"T-044",
      "assembly_id":c["assembly_id"],
      "check_count":len(checks),
      "checks":checks,
      "assembly_signature":c["assembly_signature"],
      "mutation_assembly_signature":m["assembly_signature"],
      "blend_sha256":sha(a.asset),
      "semantic_sha256":sha(a.canonical),
      "review_board_sha256":sha(a.board),
      "scope":"MP01B_LOWER_ASSEMBLY_MINIMUM_PROOF_ONLY",
      "historical_exactness_claim":False,
      "whole_frame_claim":False,
      "whole_hall_claim":False
    }
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MP01B_GATE_H_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("compose-board","validate"))
    for n in ["contract","canonical","mutation","reopen","rebuild","asset","review_dir","mutation_review_dir","board","output"]:
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)

if __name__=="__main__":
    main()
