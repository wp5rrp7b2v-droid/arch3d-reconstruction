"""T-041 Ang-family first-article review-board composer and fail-closed validator."""
import argparse, hashlib, json, math
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat

GATE_A_SIG="6c9b8c5b6ee6715292df5b23b7d8b8d9fdaaf4be7d1558631fea5883528b7096"
GATE_B_FAMILY_SIG="dc38ab72be1f5aef3192a48e11621a3288c422475545b56dc5e29fa0102e2ae5"
TOU_PROFILE_SIG="3e45e7732cf49012cbf8b5e480e76ad2fd986c4aa717dd650e3bf3f9831f7bb5"
ER_PROFILE_SIG="c4b935c9d445414831f16d949b02ff110f3e336f88c68dd68f58d514bd172778"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stable(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def point_sha(points):
    return stable(points)

def near(a,b,tol=1e-4):
    return abs(float(a)-float(b))<=tol

def manifold_edges(faces):
    c=Counter()
    for f in faces:
        for i in range(len(f)):
            a,b=int(f[i]),int(f[(i+1)%len(f)])
            c[tuple(sorted((a,b)))]+=1
    return bool(c) and all(v==2 for v in c.values())

def font(size,bold=False):
    candidates=[
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for p in candidates:
        if p and Path(p).exists():
            try: return ImageFont.truetype(p,size)
            except Exception: pass
    return ImageFont.load_default()

def compose(args):
    d=load(args.definition)
    c=load(args.canonical)
    imgs={}
    for vid in ("TOU_ANG","ER_ANG"):
        for view in ("PROFILE","AXON","END"):
            p=Path(args.review_dir)/(vid+"_"+view+".png")
            imgs[vid+"_"+view]=Image.open(p).convert("RGB")
    W,H=2400,1900
    out=Image.new("RGB",(W,H),"white")
    draw=ImageDraw.Draw(out)
    title=font(34,True); head=font(21,True); body=font(17); small=font(14)
    draw.text((50,28),"T-041 ANG MASTER FIRST ARTICLE — REVIEW BOARD",font=title,fill="black")
    draw.text((50,76),"Machine review artifact / source-vs-reconstruction boundaries explicit / PO acceptance not implied",font=body,fill="black")
    margin=50; gap=22
    col=(W-2*margin-4*gap)//5
    row=(H-150-2*gap)//2
    boxes=[]
    for r in range(2):
        for cc in range(5):
            x0=margin+cc*(col+gap); y0=120+r*(row+gap)
            boxes.append((x0,y0,x0+col,y0+row))
    labels=[
      "1 FAMILY + 32 DERIVED BINDINGS","2 TOU_ANG CANONICAL BODY","3 ER_ANG CANONICAL BODY",
      "4 VARIANT IDENTITY / DIMENSIONS","5 47:21 SLOPE + 719.5 CROSSCHECK",
      "6 SOURCE DIMENSION AXIS MAP","7 GATE-B PROFILE PROVENANCE","8 SOURCE vs RECONSTRUCTION",
      "9 UNKNOWN / DEFERRED / NO JOINERY","10 MACHINE SIGNATURES"
    ]
    for lab,box in zip(labels,boxes):
        draw.rectangle(box,outline=(170,170,170),width=2)
        draw.text((box[0]+12,box[1]+10),lab,font=head,fill="black")
    def paste(im,box,top=58):
        z=im.copy()
        z.thumbnail((box[2]-box[0]-22,box[3]-box[1]-top-18))
        out.paste(z,(box[0]+(box[2]-box[0]-z.width)//2,box[1]+top))
    # 1
    y=boxes[0][1]+62
    for line in ["1 Master family / 2 variants","TOU 16 + ER 16 = 32","LOCKED_DERIVED / not direct whole-hall count","Each direction = 4 per variant"]:
        draw.text((boxes[0][0]+16,y),line,font=body,fill="black"); y+=43
    # 2,3
    paste(imgs["TOU_ANG_AXON"],boxes[1])
    paste(imgs["ER_ANG_AXON"],boxes[2])
    # 4
    y=boxes[3][1]+62
    for line in ["TOU: 10-point / 187 → 278.4 → 187","ER: 6-point / 187 body → 2/3 taper","thickness V = 154.0 mm","control span U = 787.615706 mm","finished-mesh scaling = PROHIBITED"]:
        draw.text((boxes[3][0]+14,y),line,font=small,fill="black"); y+=38
    # 5 slope schematic
    b=boxes[4]; x0=b[0]+45; x1=b[2]-45; yy=b[3]-145; topy=b[1]+170
    draw.line((x0,yy,x1,yy),fill="black",width=4)
    draw.line((x1,yy,x1,topy),fill="black",width=4)
    draw.line((x0,yy,x1,topy),fill="black",width=4)
    draw.text((x0+40,yy+18),"run 719.1 = 47分",font=small,fill="black")
    draw.text((x1-145,topy-34),"rise 321.3 = 21分",font=small,fill="black")
    draw.text((b[0]+20,b[1]+75),"angle = 24.075498°",font=body,fill="black")
    draw.text((b[0]+20,b[1]+110),"direct observed 3rd+4th projection = 719.5",font=small,fill="black")
    draw.text((b[0]+20,b[1]+140),"delta = 0.4 mm / retained, not forced to zero",font=small,fill="black")
    # 6 axis
    y=boxes[5][1]+65
    for line in ["U = longitudinal centreline → Blender X","V = thickness → Blender Y = 154.0","W = guang/profile depth → Blender Z","278.4 / 187 are LOCAL-W, not generic Y width","V008 width_mm = historical field-name reuse"]:
        draw.text((boxes[5][0]+14,y),line,font=small,fill="black"); y+=39
    # 7
    y=boxes[6][1]+65
    for line in ["Gate B = SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE","TOU profile SHA: "+TOU_PROFILE_SIG[:16]+"…","ER profile SHA: "+ER_PROFILE_SIG[:16]+"…","metric source-image calibration = NOT CLAIMED","prior gong profile reuse = FALSE"]:
        draw.text((boxes[6][0]+14,y),line,font=small,fill="black"); y+=39
    paste(imgs["TOU_ANG_PROFILE"],(boxes[6][0]+20,boxes[6][1]+270,boxes[6][2]-20,boxes[6][3]-20),top=0)
    # 8
    y=boxes[7][1]+65
    for line in ["DIRECT: TOU广278.4 / ER+TOU单材广187 / 厚154","REPORT DESIGN: 47:21 / run719.1 / rise321.3","DIRECT ASSEMBLY: 719.5 third+fourth total projection","RECONSTRUCTION: U stations / taper / control span","CONTROL SPAN ≠ historical full timber length"]:
        draw.text((boxes[7][0]+14,y),line,font=small,fill="black"); y+=39
    # 9
    y=boxes[8][1]+65
    for line in ["full historical TOU length = UNRESOLVED","full historical ER length = UNRESOLVED","exact head/inner-end = UNRESOLVED","hidden overlap + mortise/tenon = DEFERRED","wear/asymmetry/per-instance deformation = DEFERRED","unsupported detail count = 0"]:
        draw.text((boxes[8][0]+14,y),line,font=small,fill="black"); y+=37
    # 10
    bodies={x["variant_id"]:x for x in c["canonical_bodies"]}
    y=boxes[9][1]+65
    siglines=[
      "Gate A: "+GATE_A_SIG[:18]+"…",
      "Gate B family: "+GATE_B_FAMILY_SIG[:18]+"…",
      "TOU geometry: "+bodies["TOU_ANG"]["semantic_geometry_signature"][:18]+"…",
      "ER geometry: "+bodies["ER_ANG"]["semantic_geometry_signature"][:18]+"…",
      "Family semantic: "+c["family_semantic_signature"][:18]+"…",
      "Blender: "+str(c["blender_version"])
    ]
    for line in siglines:
        draw.text((boxes[9][0]+14,y),line,font=small,fill="black"); y+=39
    Path(args.board).parent.mkdir(parents=True,exist_ok=True)
    out.save(args.board)
    print("T041_REVIEW_BOARD_PASS")

def validate(args):
    d=load(args.definition); c=load(args.canonical); ro=load(args.reopen); rs=load(args.restore)
    reg=load(args.registry); ga=load(args.gate_a); gb=load(args.gate_b)
    checks={}
    def ck(name,cond):
        if not cond: raise AssertionError(name)
        checks[name]="PASS"
    items=reg["items"]
    tou=[x for x in items if x.get("component")=="头昂"]
    er=[x for x in items if x.get("component")=="二昂"]
    def dirs(rows,prefix):
        return {k:sum(1 for x in rows if x.get("id","").startswith(prefix+"-"+k+"-")) for k in ("南","北","东","西")}
    bodies={b["variant_id"]:b for b in c["canonical_bodies"]}
    # identity / registry
    ck("01_task",d["task_id"]=="T-041" and c["task_id"]=="T-041")
    ck("02_registry_schema",reg.get("schema_version")=="V008")
    ck("03_registry_total",len(items)==505)
    ck("04_tou_count",len(tou)==16)
    ck("05_er_count",len(er)==16)
    ck("06_total_binding_count",len(tou)+len(er)==32)
    ck("07_locked_derived",all(x.get("count_status")=="LOCKED_DERIVED" for x in tou+er))
    ck("08_tou_direction_distribution",dirs(tou,"头昂")=={"南":4,"北":4,"东":4,"西":4})
    ck("09_er_direction_distribution",dirs(er,"二昂")=={"南":4,"北":4,"东":4,"西":4})
    ck("10_family_variant_count",c["master_family_count"]==1 and c["geometry_variant_count"]==2)
    ck("11_direction_variant_zero",c["direction_geometry_variant_count"]==0)
    ck("12_whole_hall_false",c["whole_hall_direct_inventory_claim"] is False)
    ck("13_sample_mapping_unknown",c["sample_to_instance_mapping"]=="UNKNOWN")
    # registry source dimensions
    ck("14_tou_registry_guang",all(near(x.get("width_mm"),278.4) for x in tou))
    ck("15_er_registry_guang",all(near(x.get("width_mm"),187.0) for x in er))
    ck("16_registry_thickness",all(near(x.get("thickness_mm"),154.0) for x in tou+er))
    # gate A
    ck("17_gate_a_status",ga["status"].startswith("LOCKED / PRODUCT_OWNER_APPROVED / D-250"))
    ck("18_gate_a_authorized",ga["engineering_execution_authorized"] is True and ga["engineering_execution_authorization_decision_id"]=="D-253")
    ck("19_gate_a_id",ga["control_id"]=="ANG_LENGTH_SLOPE_ASSEMBLY_CONTROL_SET_V001_C01")
    ck("20_gate_a_sig",ga["control_semantic_signature_sha256"]==GATE_A_SIG and d["gate_a_contract"]["semantic_signature_sha256"]==GATE_A_SIG)
    ck("21_gate_a_tou_guang",near(ga["source_dimensions"]["TOU_ANG_GUANG"]["value_mm"],278.4))
    ck("22_gate_a_er_guang",near(ga["source_dimensions"]["ER_ANG_OR_TOU_SINGLE_CAI_GUANG"]["value_mm"],187.0))
    ck("23_gate_a_thickness",near(ga["source_dimensions"]["ANG_THICKNESS"]["value_mm"],154.0))
    ck("24_thickness_source_conflict",ga["source_dimensions"]["ANG_THICKNESS"]["sample_count_status"]=="SOURCE_INTERNAL_CONFLICT" and ga["source_dimensions"]["ANG_THICKNESS"]["narrative_sample_count"]==34 and ga["source_dimensions"]["ANG_THICKNESS"]["table_sample_count"]==16)
    ck("25_er_source_category_not_n16",ga["source_dimensions"]["ER_ANG_OR_TOU_SINGLE_CAI_GUANG"]["n"]==32 and "COMBINED_SOURCE_CATEGORY" in ga["source_dimensions"]["ER_ANG_OR_TOU_SINGLE_CAI_GUANG"]["classification"])
    m=ga["source_dimension_axis_mapping"]["mappings"]
    ck("26_axis_thickness",m["ANG_THICKNESS_154"]=="local V -> Assembly Y")
    ck("27_axis_guang",m["TOU_ANG_GUANG_278_4"].startswith("local W") and m["ER_ANG_GUANG_187_0"].startswith("local W"))
    tri=ga["report_design_triangle"]
    ck("28_design_47_21",tri["horizontal_fen"]==47 and tri["rise_fen"]==21)
    ck("29_design_run_rise",near(tri["run_mm"],719.1) and near(tri["rise_mm"],321.3))
    ck("30_design_angle",near(tri["angle_deg"],24.075498255078834,1e-9))
    ck("31_design_span",near(tri["centreline_span_mm"],787.6157057855055,1e-9))
    ck("32_design_not_direct","REPORT_INFERRED" in tri["classification"] and tri["direct_per_member_slope_measurement"] is False)
    oc=ga["observed_assembly_crosscheck"]
    ck("33_observed_719_5",near(oc["third_fourth_total_projection_mean_mm"],719.5) and oc["third_fourth_n"]==22)
    ck("34_delta_retained",near(oc["ideal_vs_observed_delta_mm"],0.4))
    ck("35_projection_not_member_length",oc["member_full_length_authority"] is False)
    spans=ga["reference_control_spans"]
    ck("36_control_spans",near(spans["TOU_ANG"]["span_mm"],787.6157057855055) and near(spans["ER_ANG"]["span_mm"],787.6157057855055))
    ck("37_control_span_not_historical",spans["TOU_ANG"]["applies_to_historical_full_timber_length"] is False and spans["ER_ANG"]["applies_to_historical_full_timber_length"] is False)
    # gate B
    ck("38_gate_b_status",gb["status"].startswith("LOCKED / PRODUCT_OWNER_APPROVED / D-252"))
    ck("39_gate_b_authorized",gb["engineering_execution_authorized"] is True and gb["engineering_execution_authorization_decision_id"]=="D-253")
    ck("40_gate_b_id",gb["control_id"]=="ANG_LONGITUDINAL_PROFILE_CONTROL_SET_V001_C01")
    ck("41_gate_b_family_sig",gb["family_semantic_control_sha256"]==GATE_B_FAMILY_SIG and d["gate_b_contract"]["family_semantic_control_sha256"]==GATE_B_FAMILY_SIG)
    ck("42_tou_point_count",gb["TOU_ANG"]["point_count"]==10 and len(gb["TOU_ANG"]["control_points_uw_mm"])==10)
    ck("43_er_point_count",gb["ER_ANG"]["point_count"]==6 and len(gb["ER_ANG"]["control_points_uw_mm"])==6)
    ck("44_tou_point_sig",point_sha(gb["TOU_ANG"]["control_points_uw_mm"])==TOU_PROFILE_SIG)
    ck("45_er_point_sig",point_sha(gb["ER_ANG"]["control_points_uw_mm"])==ER_PROFILE_SIG)
    ck("46_profiles_independent",gb["variant_separation"]["identical_profile_prohibited"] is True and gb["variant_separation"]["finished_mesh_uniform_scaling_prohibited"] is True)
    ck("47_tou_deep_head",gb["variant_separation"]["TOU_has_deep_head_region"] is True and max(abs(p[1]) for p in gb["TOU_ANG"]["control_points_uw_mm"])==139.2)
    ck("48_er_no_deep_head",gb["variant_separation"]["ER_has_deep_head_region"] is False and max(abs(p[1]) for p in gb["ER_ANG"]["control_points_uw_mm"])==93.5)
    ck("49_er_taper",near(gb["ER_ANG"]["outboard_taper_ratio"],2/3) and "NOT_DIRECT_MEASUREMENT" in gb["ER_ANG"]["outboard_taper_ratio_classification"])
    audit=gb["prior_control_audit"]
    ck("50_prior_reuse_false",audit["huagong_reused"] is False and audit["mangong_reused"] is False and audit["linggong_reused"] is False and audit["generic_song_template_used"] is False)
    # canonical geometry
    ck("51_body_count",len(c["canonical_bodies"])==2 and set(bodies)=={"TOU_ANG","ER_ANG"})
    tou_b=bodies["TOU_ANG"]; er_b=bodies["ER_ANG"]
    ck("52_tou_profile_count_semantic",tou_b["profile_point_count"]==10 and tou_b["profile_control_points_sha256"]==TOU_PROFILE_SIG)
    ck("53_er_profile_count_semantic",er_b["profile_point_count"]==6 and er_b["profile_control_points_sha256"]==ER_PROFILE_SIG)
    ck("54_tou_bbox",near(tou_b["local_bbox_mm"]["dimensions"][0],787.6157057855055,1e-4) and near(tou_b["local_bbox_mm"]["dimensions"][1],154.0) and near(tou_b["local_bbox_mm"]["dimensions"][2],278.4))
    ck("55_er_bbox",near(er_b["local_bbox_mm"]["dimensions"][0],787.6157057855055,1e-4) and near(er_b["local_bbox_mm"]["dimensions"][1],154.0) and near(er_b["local_bbox_mm"]["dimensions"][2],187.0))
    ck("56_geometry_signatures_distinct",tou_b["semantic_geometry_signature"]!=er_b["semantic_geometry_signature"])
    ck("57_tou_manifold",manifold_edges(tou_b["geometry_faces"]))
    ck("58_er_manifold",manifold_edges(er_b["geometry_faces"]))
    ck("59_no_unsupported",tou_b["unsupported_detail_count"]==0 and er_b["unsupported_detail_count"]==0 and tou_b["joinery_cut_count"]==0 and er_b["joinery_cut_count"]==0)
    expected_transform={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]}
    ck("60_identity_transforms",tou_b["local_transform"]==expected_transform and er_b["local_transform"]==expected_transform)
    ck("61_not_historical_full_length",tou_b["historical_full_timber_length_closed"] is False and er_b["historical_full_timber_length_closed"] is False)
    # fixture
    vf=c["validation_fixture"]
    ck("62_fixture_id",vf["fixture_id"]=="DOUBLE_ANG_ASSEMBLY_FIXTURE_VALIDATION_ONLY")
    ck("63_fixture_noncanonical",vf["canonical_asset"] is False and vf["registry_binding"] is False and vf["catalog_asset"] is False)
    ck("64_fixture_run_rise",near(vf["run_mm"],719.1) and near(vf["rise_mm"],321.3))
    ck("65_fixture_observed",near(vf["observed_third_fourth_projection_mean_mm"],719.5) and near(vf["ideal_vs_observed_delta_mm"],0.4))
    ck("66_fixture_not_length_authority",vf["member_full_length_authority"] is False and vf["historical_joinery_claim"] is False)
    # reopen / restore
    ck("67_reopen_status",ro["status"]=="PASS")
    ck("68_reopen_fixture_count",ro["fixture_object_count"]>=5)
    ck("69_reopen_tou",ro["body_geometry_signatures"]["TOU_ANG"]==tou_b["semantic_geometry_signature"])
    ck("70_reopen_er",ro["body_geometry_signatures"]["ER_ANG"]==er_b["semantic_geometry_signature"])
    rb={b["variant_id"]:b for b in rs["canonical_bodies"]}
    ck("71_restore_family",rs["family_semantic_signature"]==c["family_semantic_signature"])
    ck("72_restore_tou",rb["TOU_ANG"]["semantic_geometry_signature"]==tou_b["semantic_geometry_signature"])
    ck("73_restore_er",rb["ER_ANG"]["semantic_geometry_signature"]==er_b["semantic_geometry_signature"])
    # binary / renders
    ck("74_blender_version",str(c["blender_version"]).startswith("4.5.13"))
    ck("75_binary_sha",c["canonical_blend_sha256"]==digest(args.asset))
    ck("76_definition_sha",c["definition_sha256"]==digest(args.definition))
    ck("77_board",Path(args.board).exists() and Path(args.board).stat().st_size>20000)
    n=78
    for name in ("TOU_ANG_PROFILE","TOU_ANG_AXON","TOU_ANG_END","ER_ANG_PROFILE","ER_ANG_AXON","ER_ANG_END"):
        im=Image.open(Path(args.review_dir)/(name+".png")).convert("L")
        ck(f"{n:02d}_render_"+name.lower(),ImageStat.Stat(im).var[0]>=80.0); n+=1
    # lifecycle / boundaries
    ex=d["execution_boundary"]
    ck("84_execution_authorized",ex["engineering_execution_authorized"] is True and ex["blender_execution_authorized"] is True and ex["production_builder_authorized"] is True and ex["validator_authorized"] is True)
    ck("85_po_not_approved",ex["first_article_product_owner_approved"] is False and ex["first_article_acceptance_authorized"] is False)
    ck("86_formalization_not_authorized",ex["formalization_authorized"] is False and ex["catalog_v008_binding_authorized"] is False)
    ck("87_merge_close_not_authorized",ex["merge_authorized"] is False and ex["closure_authorized"] is False and ex["ready_transition_authorized"] is False)
    ck("88_stage2_t018",ex["stage2_authorized"] is False and ex["t018_status"]=="HOLD")
    ck("89_first_article_contract",d["first_article_contract"]["canonical_body_count"]==2 and d["first_article_contract"]["validation_fixture_canonical_asset"] is False and d["first_article_contract"]["required_review_domain_count"]==10)
    required_deferred=["exact_historical_tou_ang_full_timber_length","exact_historical_er_ang_full_timber_length","exact_tou_ang_deep_head_transition_location","exact_outer_ang_head_shaping","hidden_overlap","mortise_tenon","grooves","slots","cavities","hidden_connection_cuts"]
    ck("90_deferred",all(x in d["deferred_geometry"] for x in required_deferred))
    out={
      "status":"PASS","task_id":"T-041","master_id":d["master_id"],"check_count":len(checks),"checks":checks,
      "canonical_blend_sha256":digest(args.asset),
      "family_semantic_signature":c["family_semantic_signature"],
      "geometry_signatures":{"TOU_ANG":tou_b["semantic_geometry_signature"],"ER_ANG":er_b["semantic_geometry_signature"]},
      "gate_a_signature":GATE_A_SIG,
      "gate_b_family_signature":GATE_B_FAMILY_SIG,
      "tou_profile_signature":TOU_PROFILE_SIG,
      "er_profile_signature":ER_PROFILE_SIG,
      "fixture":{"run_mm":vf["run_mm"],"rise_mm":vf["rise_mm"],"observed_projection_mm":vf["observed_third_fourth_projection_mean_mm"],"delta_mm":vf["ideal_vs_observed_delta_mm"]}
    }
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("T041_VALIDATION_PASS",len(checks))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("compose-board","validate"),required=True)
    for n in ("definition","canonical","reopen","restore","registry","gate_a","gate_b","asset","review_dir","board","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args()
    if a.mode=="compose-board":
        compose(a)
    else:
        validate(a)

if __name__=="__main__":
    main()
