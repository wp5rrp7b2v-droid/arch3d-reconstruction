import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(size,bold=False):
    candidates=[
      "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in candidates:
        if Path(p).exists():
            try: return ImageFont.truetype(p,size)
            except Exception: pass
    return ImageFont.load_default()

def bodies(d): return {x["variant_id"]:x for x in d["bodies"]}

def compose(a):
    c=load(a.canonical); m=load(a.mutation)
    pics={}
    for v in ("LOWER_SUPPORT","UPPER_RIDGE_SUPPORT"):
        for view in ("AXON","PROFILE"):
            p=Path(a.review_dir)/f"{v}_{view}.png"
            pics[f"{v}_{view}"]=Image.open(p).convert("RGB")
    W,H=2200,1500
    out=Image.new("RGB",(W,H),"white")
    dr=ImageDraw.Draw(out)
    ft=font(34,True); fh=font(22,True); fb=font(18); fs=font(15)
    dr.text((50,25),"T-042 驼峰 MASTER FIRST ARTICLE — REVIEW BOARD",font=ft,fill="black")
    dr.text((50,72),"Engineering test geometry only / historical metric dimensions remain UNKNOWN",font=fb,fill="black")
    boxes=[(50,120,700,650),(775,120,1425,650),(1500,120,2150,650),
           (50,705,700,1425),(775,705,1425,1425),(1500,705,2150,1425)]
    titles=["1 LOWER_SUPPORT","2 UPPER_RIDGE_SUPPORT","3 TWO ROLE VARIANTS",
            "4 PARAMETRIC MUTATION","5 SOURCE / RECONSTRUCTION BOUNDARY","6 UNKNOWN / MACHINE"]
    for b,t in zip(boxes,titles):
        dr.rectangle(b,outline="gray",width=2); dr.text((b[0]+14,b[1]+12),t,font=fh,fill="black")
    def paste(im,b,top=55):
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-top-20))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+top))
    paste(pics["LOWER_SUPPORT_AXON"],boxes[0])
    paste(pics["UPPER_RIDGE_SUPPORT_AXON"],boxes[1])
    y=boxes[2][1]+65
    for line in ["1 Master family / 2 role variants","LOWER: 四椽栿 -> 驼峰/令栱 -> 平梁","UPPER: 平梁 -> 驼峰 -> 蜀柱","Geometry identity is NOT collapsed","Whole-hall count = UNKNOWN"]:
        dr.text((boxes[2][0]+18,y),line,font=fb,fill="black"); y+=47
    cb=bodies(c); mb=bodies(m)
    y=boxes[3][1]+65
    for line in [
      "Canonical fixture A = ENGINEERING_TEST_ONLY",
      "Mutation fixture B = ENGINEERING_TEST_ONLY",
      "LOWER geometry changed: "+str(cb["LOWER_SUPPORT"]["geometry_signature"]!=mb["LOWER_SUPPORT"]["geometry_signature"]),
      "UPPER geometry changed: "+str(cb["UPPER_RIDGE_SUPPORT"]["geometry_signature"]!=mb["UPPER_RIDGE_SUPPORT"]["geometry_signature"]),
      "Identity + role stay unchanged",
      "Test dimensions are NOT building dimensions"
    ]:
        dr.text((boxes[3][0]+18,y),line,font=fb,fill="black"); y+=48
    y=boxes[4][1]+65
    for line in [
      "FACT: 驼峰 component identity",
      "FACT: two assembly roles",
      "A1 figures: same-building visual cross-check",
      "Candidate bodies: RECONSTRUCTED_DESIGN",
      "Final Wanfo metric envelope: ASSEMBLY_OWNED",
      "No test value is historical evidence"
    ]:
        dr.text((boxes[4][0]+18,y),line,font=fb,fill="black"); y+=48
    y=boxes[5][1]+65
    for line in [
      "Exact dimensions: UNKNOWN",
      "Exact historical profile: UNKNOWN",
      "Hidden joinery: UNKNOWN / DEFERRED",
      "Mortise/tenon/groove cuts: 0",
      "Canonical family sig: "+c["family_signature"][:20]+"…",
      "Blender: "+str(c["blender_version"])
    ]:
        dr.text((boxes[5][0]+18,y),line,font=fb,fill="black"); y+=48
    Path(a.board).parent.mkdir(parents=True,exist_ok=True)
    out.save(a.board)
    print("T042_REVIEW_BOARD_PASS")

def validate(a):
    d=load(a.definition); c=load(a.canonical); m=load(a.mutation); r=load(a.reopen); rs=load(a.restore); reg=load(a.registry)
    cb=bodies(c); mb=bodies(m); rb=bodies(rs)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    ck("01_task",d["task_id"]=="T-042" and c["task_id"]=="T-042")
    ck("02_authorized",d["execution_boundary"]["engineering_execution_authorized"] is True and d["execution_boundary"]["blender_execution_authorized"] is True)
    ck("03_family_architecture",d["family_architecture"]["master_family_count"]==1 and d["family_architecture"]["role_variant_count"]==2)
    ck("04_semantic_architecture",c["master_family_count"]==1 and c["role_variant_count"]==2 and set(c["role_variants"])=={"LOWER_SUPPORT","UPPER_RIDGE_SUPPORT"})
    ck("05_fixture_test_only",c["fixture_historical_claim"] is False and c["fixture_building_dimension_claim"] is False and "ENGINEERING_TEST_ONLY" in c["fixture_classification"])
    ck("06_unknown_dimensions",c["historical_dimensions"]=="UNKNOWN" and c["exact_historical_profile"]=="UNKNOWN")
    ck("07_joinery_unknown",c["historical_joinery"]=="UNKNOWN / DEFERRED" and all(x["joinery_cut_count"]==0 for x in c["bodies"]))
    ck("08_two_distinct_geometry",cb["LOWER_SUPPORT"]["geometry_signature"]!=cb["UPPER_RIDGE_SUPPORT"]["geometry_signature"])
    ck("09_mutation_lower",cb["LOWER_SUPPORT"]["geometry_signature"]!=mb["LOWER_SUPPORT"]["geometry_signature"])
    ck("10_mutation_upper",cb["UPPER_RIDGE_SUPPORT"]["geometry_signature"]!=mb["UPPER_RIDGE_SUPPORT"]["geometry_signature"])
    ck("11_mutation_identity",m["component_id"]==c["component_id"] and set(m["role_variants"])==set(c["role_variants"]))
    ck("12_reopen",r["status"]=="PASS" and r["geometry_signatures"]=={k:v["geometry_signature"] for k,v in cb.items()})
    ck("13_restore_lower",rb["LOWER_SUPPORT"]["geometry_signature"]==cb["LOWER_SUPPORT"]["geometry_signature"])
    ck("14_restore_upper",rb["UPPER_RIDGE_SUPPORT"]["geometry_signature"]==cb["UPPER_RIDGE_SUPPORT"]["geometry_signature"])
    lf=d["canonical_first_article_fixture"]["LOWER_SUPPORT"]
    ck("15_lower_seat_span",lf["seat_span_mm"]<=lf["base_span_mm"] and lf["seat_depth_mm"]<=lf["base_depth_mm"])
    prof=d["upper_normalized_profile_xz"]
    ck("16_upper_profile_symmetric",all(abs(prof[i][0]+prof[-1-i][0])<1e-9 and abs(prof[i][1]-prof[-1-i][1])<1e-9 for i in range(len(prof))))
    ck("17_assembly_owned",c["assembly_metric_envelope"]=="ASSEMBLY_OWNED")
    tf=[x for x in reg["items"] if x.get("component")=="驼峰"]
    ck("18_registry_family_record",len(tf)==1 and tf[0].get("count_status")=="FAMILY_UNKNOWN_COUNT")
    ck("19_registry_pending",tf[0].get("master_coverage_status")=="MASTER_REQUIRED_PENDING")
    ck("20_no_historical_flags",all(x["historical_metric_claim"] is False and x["building_dimension_claim"] is False for x in c["bodies"]))
    ck("21_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("22_binary_sha",c["blend_sha256"]==sha(a.asset))
    ck("23_board",Path(a.board).exists() and Path(a.board).stat().st_size>15000)
    n=24
    for v in ("LOWER_SUPPORT","UPPER_RIDGE_SUPPORT"):
      for view in ("AXON","PROFILE"):
        rp=Path(a.review_dir)/f"{v}_{view}.png"
        im=Image.open(rp).convert("L")
        ck(f"{n:02d}_render_{v.lower()}_{view.lower()}",rp.exists() and rp.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10); n+=1
    out={"status":"PASS","task_id":"T-042","master_id":d["master_id"],"check_count":len(checks),"checks":checks,
         "canonical_blend_sha256":sha(a.asset),"family_signature":c["family_signature"],
         "geometry_signatures":{k:v["geometry_signature"] for k,v in cb.items()},
         "mutation_signatures":{k:v["geometry_signature"] for k,v in mb.items()}}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T042_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    for n in ("definition","canonical","mutation","reopen","restore","registry","asset","review_dir","board","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)
if __name__=="__main__": main()
