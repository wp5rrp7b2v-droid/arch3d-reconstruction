"""T-040 华栱 first-article validator and 9-domain Review Board composer."""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

PROFILE_SHA="f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e"
GATE_A_SHA="ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=1e-3): return abs(float(a)-float(b))<=t
def point_sha(points):
    normalized=[[float(x),float(z)] for x,z in points]
    return hashlib.sha256(json.dumps(normalized,ensure_ascii=False,separators=(",",":")).encode("utf-8")).hexdigest()
def font(size=24):
    for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def polygon_simple(points):
    def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def seg(a,b,c,d):
        o1,o2,o3,o4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
        return (o1*o2<0) and (o3*o4<0)
    n=len(points)
    for i in range(n):
        a,b=points[i],points[(i+1)%n]
        for j in range(i+1,n):
            if j in (i,(i+1)%n) or (j+1)%n in (i,(i+1)%n): continue
            if i==0 and j==n-1: continue
            if seg(a,b,points[j],points[(j+1)%n]): return False
    return True

def manifold_edges(faces):
    counts={}
    for f in faces:
        for i in range(len(f)):
            k=tuple(sorted((int(f[i]),int(f[(i+1)%len(f)]))))
            counts[k]=counts.get(k,0)+1
    return counts and all(v==2 for v in counts.values())

def compose(a):
    d=load(a.definition); c=load(a.canonical); r=Path(a.review_dir)
    image_names=["JUMP_1_HUAGONG_PROFILE","JUMP_1_HUAGONG_AXON","JUMP_2_HUAGONG_PROFILE","JUMP_2_HUAGONG_AXON","JUMP_1_HUAGONG_END","JUMP_2_HUAGONG_END"]
    imgs={}
    for n in image_names:
        p=r/(n+".png")
        if not p.exists(): raise AssertionError("missing "+str(p))
        im=Image.open(p).convert("RGB"); var=ImageStat.Stat(im.convert("L")).var[0]
        if var<100.0: raise AssertionError("REVIEW_RENDER_NEAR_UNIFORM "+n+" variance="+str(var))
        im.thumbnail((700,430)); imgs[n]=im.copy()
    W,H=2460,2240; out=Image.new("RGB",(W,H),"white"); draw=ImageDraw.Draw(out)
    title=font(33); head=font(22); small=font(18); tiny=font(16)
    draw.text((45,22),"T-040｜华栱 Master V001｜First Article Review Board",font=title,fill="black")
    boxes=[(30+c0*810,75+r0*710,800+c0*810,755+r0*710) for r0 in range(3) for c0 in range(3)]
    labels=[
      "1 FAMILY + 56 SUBSET SCOPE","2 JUMP_1 CANONICAL BODY","3 JUMP_2 CANONICAL BODY",
      "4 TWO-VARIANT DIMENSION / IDENTITY","5 TWO-JUMP FIXTURE / 732.4 PROOF","6 SECTION + REPORT IDEAL BOUNDARY",
      "7 PROFILE PROVENANCE / CONTROL","8 SOURCE vs RECONSTRUCTION","9 UNKNOWN / DEFERRED / NO JOINERY"
    ]
    for lab,box in zip(labels,boxes):
        draw.rectangle(box,outline=(180,180,180),width=2); draw.text((box[0]+14,box[1]+12),lab,font=head,fill="black")
    def paste(im,box,top=58):
        z=im.copy(); z.thumbnail((box[2]-box[0]-28,box[3]-box[1]-top-20))
        out.paste(z,(box[0]+(box[2]-box[0]-z.width)//2,box[1]+top))
    # Panel 1 text
    y=boxes[0][1]+72
    for line in ["1 Master family / 2 jump variants","JUMP_1 28 + JUMP_2 28 = 56","LOCKED_SUBSET / NOT whole-hall total","South/North/East/West each 7 per jump"]:
        draw.text((boxes[0][0]+24,y),line,font=small,fill="black"); y+=48
    paste(imgs["JUMP_1_HUAGONG_PROFILE"],boxes[1])
    paste(imgs["JUMP_2_HUAGONG_PROFILE"],boxes[2])
    # Dimension proof
    y=boxes[3][1]+70
    for line in ["JUMP_1 ref: 898.8 × 214.2 × 153.0 mm","JUMP_2 ref: 1630.0 × 214.2 × 153.0 mm",
                 "reference specimen only / NOT instance exact","independent body generation / distinct geometry SHA"]:
        draw.text((boxes[3][0]+20,y),line,font=small,fill="black"); y+=47
    # Fixture diagram
    box=boxes[4]; x0=box[0]+80; x2=box[2]-80; yy=box[1]+330
    draw.line((x0,yy,x2,yy),fill="black",width=4)
    for frac,name,val in [(0.0,"D0","0.0"),(0.5,"D1","366.2"),(1.0,"D2","732.4")]:
        xx=x0+(x2-x0)*frac; draw.line((xx,yy-70,xx,yy+70),fill="black",width=3)
        draw.text((xx-42,yy-110),name,font=head,fill="black"); draw.text((xx-50,yy+85),val+" mm",font=tiny,fill="black")
    draw.text((box[0]+28,box[1]+500),"DIRECT PRIMARY: D2-D0 = 732.4 mm / n=46 observed mean",font=tiny,fill="black")
    draw.text((box[0]+28,box[1]+536),"D1 = project/reconstruction fixture guidance, NOT direct jump measure",font=tiny,fill="black")
    # Section
    y=boxes[5][1]+70
    for line in ["W=214.2 mm / T=153.0 mm","REPORT_INFERRED / 14分 / 10分","report ideal total=734.4 mm / 48分","direct assembly mean remains 732.4 mm","no silent clipping to observed band"]:
        draw.text((boxes[5][0]+20,y),line,font=small,fill="black"); y+=45
    # Profile
    y=boxes[6][1]+68
    for line in ["HUAGONG_PROFILE_CONTROL_SET_V001_C01","16 normalized points",d["profile_contract"]["classification"],
                 "metric calibration = NOT PERFORMED","T037/T038/T039 reuse = FALSE"]:
        draw.text((boxes[6][0]+20,y),line,font=small,fill="black"); y+=44
    # Source/reconstruction
    y=boxes[7][1]+68
    for line in ["DIRECT: combined projection 732.4 mm","REPORT MODEL: section 14分/10分 + 48分 total",
                 "SECONDARY: JUMP_2 1630 mm","RECONSTRUCTION: JUMP_1 898.8 ref specimen",
                 "PROFILE: source-guided simplified, not direct"]:
        draw.text((boxes[7][0]+20,y),line,font=small,fill="black"); y+=44
    # Deferred
    y=boxes[8][1]+68
    for line in ["instance full lengths = UNRESOLVED","individual jump projections = UNRESOLVED","hidden overlap/contact datum = UNRESOLVED",
                 "end shoulder/notch = UNRESOLVED","mortise/tenon + grooves + slots = DEFERRED","unsupported detail count = 0"]:
        draw.text((boxes[8][0]+20,y),line,font=tiny,fill="black"); y+=41
    Path(a.board).parent.mkdir(parents=True,exist_ok=True); out.save(a.board)

def validate(a):
    d=load(a.definition); c=load(a.canonical); ro=load(a.reopen); rs=load(a.restore); reg=load(a.registry)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    items=reg["items"]; target=[x for x in items if x.get("component")=="华栱"]
    j1=[x for x in target if x.get("id","").endswith("一跳")]
    j2=[x for x in target if x.get("id","").endswith("二跳")]
    def dirs(rows):
        return {k:sum(1 for x in rows if ("华栱-"+k+"-") in x.get("id","")) for k in ("南","北","东","西")}
    bodies={b["variant_id"]:b for b in c["canonical_bodies"]}
    p=d["profile_contract"]["normalized_points"]
    la=d["length_assembly_contract"]; vf=c["validation_fixture"]
    ck("01_task",d["task_id"]=="T-040" and c["task_id"]=="T-040")
    ck("02_registry_schema",reg.get("schema_version")=="V008")
    ck("03_registry_total",len(items)==505)
    ck("04_target_count_56",len(target)==56)
    ck("05_locked_subset",all(x.get("count_status")=="LOCKED_SUBSET" for x in target))
    ck("06_jump_counts",len(j1)==28 and len(j2)==28)
    ck("07_direction_distribution_j1",dirs(j1)=={"南":7,"北":7,"东":7,"西":7})
    ck("08_direction_distribution_j2",dirs(j2)=={"南":7,"北":7,"东":7,"西":7})
    ck("09_whole_hall_false",d["registry_boundary"]["whole_hall_total_claim"] is False and c["whole_hall_total_claim"] is False)
    ck("10_family_variant_count",c["master_family_count"]==1 and c["geometry_variant_count"]==2)
    ck("11_physical_count",c["physical_instance_count"]==56)
    ck("12_direction_variant_zero",d["registry_boundary"]["direction_geometry_variant_count"]==0)
    ck("13_gate_a_id",la["control_id"]=="HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01")
    ck("14_gate_a_sha",la["control_set_sha256"]==GATE_A_SHA)
    ck("15_gate_b_id",d["profile_contract"]["candidate_id"]=="HUAGONG_PROFILE_CONTROL_SET_V001_C01")
    ck("16_gate_b_sha",d["profile_contract"]["control_set_sha256"]==PROFILE_SHA)
    ck("17_profile_point_count",d["profile_contract"]["point_count"]==16 and len(p)==16)
    ck("18_profile_sha_recomputed",point_sha(p)==PROFILE_SHA)
    ck("19_profile_classification",d["profile_contract"]["classification"]=="SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT")
    ck("20_profile_not_direct",d["profile_contract"]["normalized_points_are_direct_measurements"] is False)
    ck("21_metric_not_claimed",d["profile_contract"]["metric_scale_calibration"]=="NOT_PERFORMED / NOT_CLAIMED")
    pr=d["profile_contract"]["prior_control_reuse"]
    ck("22_prior_reuse_false",not any(pr.values()))
    ck("23_profile_simple",polygon_simple(p))
    ck("24_profile_extent",min(x for x,z in p)==-0.5 and max(x for x,z in p)==0.5 and min(z for x,z in p)==-0.5 and max(z for x,z in p)==0.5)
    ck("25_bilateral",d["profile_contract"]["bilateral_symmetry"] is True)
    s1=la["reference_specimens"]["JUMP_1_HUAGONG"]; s2=la["reference_specimens"]["JUMP_2_HUAGONG"]
    ck("26_gate_a_jump1_dims",near(s1["length_mm"],898.8) and near(s1["width_mm"],214.2) and near(s1["thickness_mm"],153.0))
    ck("27_gate_a_jump2_dims",near(s2["length_mm"],1630.0) and near(s2["width_mm"],214.2) and near(s2["thickness_mm"],153.0))
    ck("28_section_shared_not_scaled",near(s1["width_mm"],s2["width_mm"]) and near(s1["thickness_mm"],s2["thickness_mm"]))
    ck("29_body_count",len(c["canonical_bodies"])==2 and set(bodies)=={"JUMP_1_HUAGONG","JUMP_2_HUAGONG"})
    for idx,(vid,L) in enumerate((("JUMP_1_HUAGONG",898.8),("JUMP_2_HUAGONG",1630.0)),start=30):
        b=bodies[vid]; dims=b["resolved_dimensions_mm"]; bb=b["local_bbox_mm"]["dimensions"]
        ck(f"{idx:02d}_{vid.lower()}_semantic_dims",near(dims["length"],L) and near(dims["width"],214.2) and near(dims["thickness"],153.0))
        ck(f"{idx+2:02d}_{vid.lower()}_bbox",near(bb[0],L) and near(bb[1],214.2) and near(bb[2],153.0))
    ck("34_body_signatures_distinct",bodies["JUMP_1_HUAGONG"]["semantic_geometry_signature"]!=bodies["JUMP_2_HUAGONG"]["semantic_geometry_signature"])
    ck("35_no_unsupported",all(b["unsupported_detail_count"]==0 and b["joinery_cut_count"]==0 for b in bodies.values()))
    ck("36_manifold_j1",manifold_edges(bodies["JUMP_1_HUAGONG"]["geometry_faces"]))
    ck("37_manifold_j2",manifold_edges(bodies["JUMP_2_HUAGONG"]["geometry_faces"]))
    expected_transform={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]}
    ck("38_transforms",all(b["local_transform"]==expected_transform for b in bodies.values()))
    ck("39_fixture_id",vf["fixture_id"]=="TWO_JUMP_ASSEMBLY_FIXTURE_VALIDATION_ONLY")
    ck("40_fixture_noncanonical",vf["canonical_asset"] is False and vf["registry_binding"] is False and vf["catalog_asset"] is False)
    ck("41_fixture_datums",near(vf["datums_mm"]["D0"],0.0) and near(vf["datums_mm"]["D1"],366.2) and near(vf["datums_mm"]["D2"],732.4))
    ck("42_projection_tolerance",abs(float(vf["combined_projection_mm"])-732.4)<=float(vf["machine_tolerance_mm"]))
    ck("43_midpoint_not_direct",vf["individual_jump_projection_direct"] is False and "PROJECT_FIXTURE_ONLY" in vf["D1_classification"])
    pac=la["primary_assembly_constraint"]
    ck("44_primary_projection_semantics",near(pac["total_projection_mean_mm"],732.4) and pac["n"]==46 and pac["classification"]=="DIRECT_PRIMARY / OBSERVED_MEAN / ASSEMBLY_LEVEL_COMBINED_PROJECTION")
    ck("45_projection_not_member_length",pac["standalone_member_length"] is False and pac["full_length_sum"] is False)
    ck("46_projection_not_instance_or_963",pac["per_instance_exact"] is False and pac["original_963_design"] is False)
    ric=la["report_ideal_crosscheck"]
    ck("47_report_ideal_separate",near(ric["total_projection_mm"],734.4) and ric["classification"]=="REPORT_INFERRED / REPORT_IDEAL_MODEL / CROSSCHECK_ONLY / REPLACEABLE")
    ck("48_reference_not_instance",s1["applies_to_instance"] is False and s2["applies_to_instance"] is False)
    ck("49_historical_lengths_unresolved",s1["historical_instance_full_length_closed"] is False and s2["historical_instance_full_length_closed"] is False and d["registry_boundary"]["instance_historical_full_length_status"]=="UNRESOLVED")
    ck("50_sample_mapping_unknown",d["registry_boundary"]["sample_to_instance_mapping"]=="UNKNOWN" and c["sample_to_instance_mapping"]=="UNKNOWN")
    va=d["profile_contract"]["variant_application"]
    ck("51_no_uniform_mesh_scale",va["uniform_3d_scaling"] is False and va["independent_body_generation_required"] is True)
    ck("52_no_width_thickness_scale",va["width_thickness_scaled_by_length_ratio"] is False)
    ck("53_reopen_status",ro["status"]=="PASS" and ro["fixture_object_count"]==3)
    ck("54_reopen_j1",ro["body_geometry_signatures"]["JUMP_1_HUAGONG"]==bodies["JUMP_1_HUAGONG"]["semantic_geometry_signature"])
    ck("55_reopen_j2",ro["body_geometry_signatures"]["JUMP_2_HUAGONG"]==bodies["JUMP_2_HUAGONG"]["semantic_geometry_signature"])
    ck("56_reopen_fixture",all(near(ro["fixture_datums_mm"][k],vf["datums_mm"][k]) for k in ("D0","D1","D2")))
    rb={b["variant_id"]:b for b in rs["canonical_bodies"]}
    ck("57_restore_family",rs["family_semantic_signature"]==c["family_semantic_signature"])
    ck("58_restore_j1",rb["JUMP_1_HUAGONG"]["semantic_geometry_signature"]==bodies["JUMP_1_HUAGONG"]["semantic_geometry_signature"])
    ck("59_restore_j2",rb["JUMP_2_HUAGONG"]["semantic_geometry_signature"]==bodies["JUMP_2_HUAGONG"]["semantic_geometry_signature"])
    ck("60_blender",str(c["blender_version"]).startswith("4.5.13"))
    ck("61_binary_sha",c["canonical_blend_sha256"]==digest(a.asset))
    ck("62_definition_hash",c["definition_sha256"]==digest(a.definition))
    ck("63_board",Path(a.board).exists() and Path(a.board).stat().st_size>20000)
    n=64
    for name in ("JUMP_1_HUAGONG_PROFILE","JUMP_1_HUAGONG_AXON","JUMP_1_HUAGONG_END","JUMP_2_HUAGONG_PROFILE","JUMP_2_HUAGONG_AXON","JUMP_2_HUAGONG_END"):
        im=Image.open(Path(a.review_dir)/(name+".png")).convert("L")
        ck(f"{n:02d}_render_"+name.lower(),ImageStat.Stat(im).var[0]>=100.0); n+=1
    fa=d["first_article_contract"]
    ck("70_first_article_contract",fa["canonical_body_count"]==2 and fa["validation_fixture_canonical_asset"] is False and fa["registry_instance_assembly"] is False and fa["required_review_domain_count"]==9)
    ex=d["execution_boundary"]
    ck("71_execution_authorized",ex["engineering_execution_authorized"] is True and ex["blender_execution_authorized"] is True and ex["production_builder_authorized"] is True and ex["validator_authorized"] is True)
    ck("72_po_acceptance_lifecycle",ex["first_article_product_owner_approved"] is True and ex["first_article_acceptance_authorized"] is True)
    ck("73_formalization_lifecycle",ex["formalization_authorized"] is True and ex["catalog_v008_binding_authorized"] is True and ex.get("formalization_complete") is True and ex.get("catalog_v008_binding_complete") is True)
    ck("74_merge_close_not_authorized",ex["merge_authorized"] is False and ex["closure_authorized"] is False)
    ck("75_t018_stage2",ex["t018_status"]=="HOLD" and ex["stage2_authorized"] is False)
    ck("76_deferred",all(x in d["deferred_geometry"] for x in ["exact_hidden_overlap","historical_contact_datum","exact_end_notch_shoulder","mortise_tenon","grooves","slots","cavities","hidden_connection_cuts","exact_historical_profile_curve"]))
    out={"status":"PASS","task_id":"T-040","master_id":d["master_id"],"check_count":len(checks),"checks":checks,
         "canonical_blend_sha256":digest(a.asset),"family_semantic_signature":c["family_semantic_signature"],
         "geometry_signatures":{k:v["semantic_geometry_signature"] for k,v in bodies.items()},
         "profile_control_signature":d["profile_contract"]["control_set_sha256"],
         "length_assembly_control_signature":d["length_assembly_contract"]["control_set_sha256"],
         "fixture_combined_projection_mm":vf["combined_projection_mm"]}
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T040_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    for n in ("definition","canonical","reopen","restore","registry","asset","review_dir","board","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board": compose(a)
    else: validate(a)
if __name__=="__main__": main()
