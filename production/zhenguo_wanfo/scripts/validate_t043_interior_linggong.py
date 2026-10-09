import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

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
    d=load(a.definition); c=load(a.canonical); m=load(a.mutation)
    ax=Image.open(Path(a.review_dir)/"FIXTURE_A_AXON.png").convert("RGB")
    pr=Image.open(Path(a.review_dir)/"FIXTURE_A_PROFILE.png").convert("RGB")
    mu=Image.open(Path(a.mutation_review_dir)/"FIXTURE_B_AXON.png").convert("RGB")
    W,H=2400,1600
    out=Image.new("RGB",(W,H),"white"); dr=ImageDraw.Draw(out)
    ft=font(38,True); fh=font(23,True); fb=font(17); fs=font(15)
    dr.text((45,25),"T-043｜梁架承托令栱 First Article Review Board",font=ft,fill="black")
    dr.text((45,75),"ENGINEERING TEST ONLY / NOT BUILDING DIMENSIONS / historical profile UNKNOWN",font=fb,fill="black")
    boxes=[(45,115,1165,720),(1235,115,2355,720),(45,770,790,1535),(830,770,1595,1535),(1635,770,2355,1535)]
    titles=["1 CANONICAL AXON","2 CANONICAL PROFILE","3 MUTATION PROOF","4 ROLE / NON-INHERITANCE","5 UNKNOWN BOUNDARY"]
    for b,t in zip(boxes,titles):
        dr.rectangle(b,outline="gray",width=2); dr.text((b[0]+12,b[1]+10),t,font=fh,fill="black")
    def paste(im,b):
        z=im.copy(); z.thumbnail((b[2]-b[0]-24,b[3]-b[1]-60))
        out.paste(z,(b[0]+(b[2]-b[0]-z.width)//2,b[1]+52))
    paste(ax,boxes[0]); paste(pr,boxes[1]); paste(mu,boxes[2])
    y=boxes[3][1]+60
    lines=[
      "Role: LOWER_PINGLIANG_SUPPORT",
      "System: 四椽栿 → 驼峰 / 令栱 → 平梁",
      "",
      "Fixture A: 1000 / 500 / 180 / 550 / 500 / 120",
      "Fixture B: 1260 / 620 / 210 / 660 / 620 / 140",
      "",
      "Outer-eaves Linggong NOT inherited:",
      "897 × 217.4 × 155.6 mm → prohibited",
      "14-point outer-eaves profile → prohibited",
      "",
      "Geometry = neutral two-zone digital abstraction",
      "Building dimensions = ASSEMBLY_OWNED"
    ]
    for line in lines:
        dr.text((boxes[3][0]+16,y),line,font=fb,fill="black"); y+=42
    y=boxes[4][1]+60
    for line in [
      "UNKNOWN retained:",
      "• whole-hall instance count",
      "• exact per-instance mapping",
      "• historical length / section",
      "• historical gong profile",
      "• exact contact faces",
      "• hidden joinery",
      "• equivalence to outer-eaves Linggong",
      "",
      "PASS means generator proof only.",
      "It does NOT prove historical form."
    ]:
        dr.text((boxes[4][0]+16,y),line,font=fb,fill="black"); y+=42
    Path(a.board).parent.mkdir(parents=True,exist_ok=True)
    out.save(a.board)
    print("T043_REVIEW_BOARD_PASS")

def validate(a):
    d=load(a.definition); c=load(a.canonical); m=load(a.mutation); r=load(a.reopen); rs=load(a.restore)
    reg=load(a.registry); cand=load(a.candidate)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    ck("01_task",c["task_id"]=="T-043")
    ck("02_family_count",c["master_family_count"]==1)
    ck("03_role_count",c["role_variant_count"]==1)
    ck("04_role",c["role_variant"]=="LOWER_PINGLIANG_SUPPORT")
    ck("05_fixture_A_class",c["fixture_classification"].startswith("ENGINEERING_TEST_ONLY"))
    ck("06_no_hist_claim",c["fixture_historical_claim"] is False and all(z["historical_metric_claim"] is False for z in c["zones"]))
    ck("07_no_building_claim",c["fixture_building_dimension_claim"] is False and all(z["building_dimension_claim"] is False for z in c["zones"]))
    ck("08_two_zones",set(z["zone_id"] for z in c["zones"])=={"BODY_ZONE","UPPER_BEARING_ZONE"})
    ck("09_seat_within_body",c["geometry_inputs"]["seat_length"]<=c["geometry_inputs"]["body_length"] and c["geometry_inputs"]["seat_depth"]<=c["geometry_inputs"]["body_depth"])
    ck("10_reopen",r["status"]=="PASS" and r["object_count"]==2)
    ck("11_mutation_changes",m["geometry_signature"]!=c["geometry_signature"])
    ck("12_identity_stable",m["component_id"]==c["component_id"] and m["master_id"]==c["master_id"] and m["role_variant"]==c["role_variant"])
    ck("13_restore",rs["geometry_signature"]==c["geometry_signature"])
    forbidden={897.0,217.4,155.6}
    actual={float(v) for v in c["geometry_inputs"].values()}
    ck("14_outer_eaves_dimensions_absent_from_geometry_inputs",forbidden.isdisjoint(actual))
    ck("15_outer_eaves_profile_not_used",c["outer_eaves_profile_used"] is False and c["outer_eaves_geometry_inherited"] is False and all(z["outer_eaves_profile_used"] is False for z in c["zones"]))
    ck("16_joinery_unknown",c["historical_joinery"]=="UNKNOWN / DEFERRED" and c["joinery_cut_count"]==0 and all(z["joinery_cut_count"]==0 for z in c["zones"]))
    ck("17_unknown_dimensions",c["historical_dimensions"]=="UNKNOWN" and c["historical_profile"]=="UNKNOWN")
    ck("18_assembly_owned",c["building_metric_envelope"]=="ASSEMBLY_OWNED")
    ck("19_candidate_approved",cand["status"].startswith("APPROVED_GEOMETRY_STRATEGY") and cand["approval"]["approved"] is True)
    rows=[x for x in reg["items"] if x.get("component")=="令栱（梁架承托）"]
    ck("20_registry_record",len(rows)==1 and rows[0]["master_coverage_status"]=="MASTER_REQUIRED_PENDING")
    ck("21_definition_source_boundary",d["geometry_authority"]["outer_eaves_master_geometry_authority"] is False and d["geometry_authority"]["historical_metric_geometry_authority"] is False)
    ck("22_source_binding_exists",Path(a.source_binding).exists())
    ck("23_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("24_blend_sha",c["blend_sha256"]==sha(a.asset))
    for i,n in enumerate(["FIXTURE_A_AXON.png","FIXTURE_A_PROFILE.png"],start=25):
        p=Path(a.review_dir)/n; im=Image.open(p).convert("L")
        ck(f"{i:02d}_canonical_render",p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    p=Path(a.mutation_review_dir)/"FIXTURE_B_AXON.png"; im=Image.open(p).convert("L")
    ck("27_mutation_render",p.stat().st_size>5000 and ImageStat.Stat(im).var[0]>10)
    ck("28_review_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)
    out={
      "status":"PASS","task_id":"T-043","check_count":len(checks),"checks":checks,
      "geometry_signature":c["geometry_signature"],"mutation_geometry_signature":m["geometry_signature"],
      "blend_sha256":sha(a.asset),"semantic_sha256":sha(a.canonical),"review_board_sha256":sha(a.board),
      "scope":"INTERIOR_LINGGONG_MASTER_GENERATOR_ONLY",
      "historical_exactness_claim":False,"mp01b_assembly_claim":False
    }
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T043_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",required=True,choices=("compose-board","validate"))
    for n in ["definition","canonical","mutation","reopen","restore","registry","candidate","source_binding","asset","review_dir","mutation_review_dir","board","output"]:
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)

if __name__=="__main__":
    main()
