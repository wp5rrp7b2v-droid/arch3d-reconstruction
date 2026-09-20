"""Validate T-024 Rufu Master first article."""
import argparse, copy, hashlib, json
from pathlib import Path

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=1e-3): return abs(float(a)-float(b))<=t
def dims(s): return [float(x) for x in s["body"]["local_bbox_mm"]["dimensions"]]

def main():
    ap=argparse.ArgumentParser()
    for n in ("params","canonical","reopen","length","width","thickness","upper","lower","ne","se","sw","nw","restore","asset","review_dir","registry","source_catalog","output","catalog","report"):
        ap.add_argument("--"+n.replace("_","-"),dest=n,required=True)
    a=ap.parse_args()
    p=load(a.params); c=load(a.canonical); r=load(a.reopen); lm=load(a.length); wm=load(a.width); tm=load(a.thickness)
    up=load(a.upper); lo=load(a.lower); ne=load(a.ne); se=load(a.se); sw=load(a.sw); nw=load(a.nw); rs=load(a.restore)
    reg=load(a.registry); source_catalog=load(a.source_catalog)
    P={x["key"]:x for x in p["parameters"]}; checks={}
    def ck(n,v):
        if not v: raise AssertionError(n)
        checks[n]="PASS"

    items=[x for x in reg["items"] if x.get("component")=="乳栿"]; ids={x["id"] for x in items}
    expected={"乳栿-东北角-上斜乳栿","乳栿-东北角-下斜乳栿","乳栿-东南角-上斜乳栿","乳栿-东南角-下斜乳栿",
              "乳栿-西南角-上斜乳栿","乳栿-西南角-下斜乳栿","乳栿-西北角-上斜乳栿","乳栿-西北角-下斜乳栿"}
    role_docs={"UPPER":up,"LOWER":lo,"NE":ne,"SE":se,"SW":sw,"NW":nw}
    cd=dims(c); ld=dims(lm); wd=dims(wm); td=dims(tm)

    ck("01_component_id",p["component_id"]=="CMP-FRAME-RUFU-001"==c["component_id"])
    ck("02_master_id",p["master_id"]=="CMP-FRAME-RUFU-001_MASTER"==c["master_id"])
    ck("03_registry_v008",reg["schema_version"]=="V008" and reg["item_count"]==505)
    ck("04_instance_count_8",len(items)==8)
    ck("05_exact_instance_ids",ids==expected)
    ck("06_vertical_role_counts",sum(x["role_semantics"]["vertical_role"]=="UPPER" for x in items)==4 and sum(x["role_semantics"]["vertical_role"]=="LOWER" for x in items)==4)
    ck("07_corner_role_counts",all(sum(x["role_semantics"]["corner"]==k for x in items)==2 for k in ("NE","SE","SW","NW")))
    ck("08_table_rows_8",p["measurement_table_row_count"]==8 and all(x["measurement_table_row_count"]==8 for x in items))
    ck("09_complete_samples_6",p["complete_measured_sample_count"]==6 and len(p["measured_section_samples_mm"])==6 and all(x["complete_measured_sample_count"]==6 for x in items))
    ck("10_unmeasured_rows_2",p["unmeasured_table_row_count"]==2 and all(x["unmeasured_table_row_count"]==2 for x in items))
    ck("11_samples_retained",p["measured_section_samples_mm"]==[{"width":331,"thickness":185},{"width":337,"thickness":186},{"width":323,"thickness":193},{"width":342,"thickness":185},{"width":325,"thickness":188},{"width":325,"thickness":186}])
    ck("12_mapping_unknown",p["sample_to_instance_mapping"]=="UNKNOWN" and all(x["sample_to_instance_mapping"]=="UNKNOWN" for x in items))
    ck("13_width_mean",P["width_mm"]["value"]==330.5 and all(x["width_mm"]==330.5 for x in items))
    ck("14_thickness_mean",P["thickness_mm"]["value"]==187.2 and all(x["thickness_mm"]==187.2 for x in items))
    ck("15_report_metadata_only",p["report_analysis"]["geometry_use_count"]==0 and p["report_analysis"]["rounded_fen"]=={"width":22,"thickness":12})
    ck("16_historical_length_null",P["historical_full_length_mm"]["value"] is None and all(x["historical_full_length_mm"] is None for x in items))
    ck("17_reference_1000_nonhistorical",P["canonical_reference_length_mm"]["value"]==1000 and P["canonical_reference_length_mm"]["historical_claim"] is False)
    ck("18_exact_plan_angle_null",P["exact_plan_angle_deg"]["value"] is None and all(x["placement_rule"]["exact_plan_angle_deg"] is None for x in items))
    ck("19_no_45_default",p["angle_rule"]["default_to_45_deg_allowed"] is False and all("do not bake 45 degrees" in x["placement_rule"]["rule"] for x in items))
    ck("20_roles_locked",p["role_variants"]==["UPPER","LOWER","NE","SE","SW","NW"] and p["role_geometry_policy"].endswith("SHARED_CANONICAL_BODY"))
    ck("21_interfaces",set(p["interface_contract"])=={"BRACKET_END","OPPOSITE_END"} and p["interface_contract"]["BRACKET_END"]["semantic"]=="与斗栱交接")
    ck("22_assembly_semantics",p["assembly_semantics"]["dingfu_rufu_spacing"]=="一材一栔" and p["assembly_semantics"]["pad_member"]=="垫单材栿一层")
    ck("23_groove_direct",p["groove_boundary"]["status"]=="DIRECT_EXISTENCE / GEOMETRY_DEFERRED" and all(x["groove_boundary"]["status"]=="DIRECT_EXISTENCE / GEOMETRY_DEFERRED" for x in items))
    ck("24_groove_not_cut",p["groove_boundary"]["stage1_cut_geometry"] is False and c["body"]["groove_cut_count"]==0)
    ck("25_bbox_x",near(cd[0],1000)); ck("26_bbox_y",near(cd[1],330.5)); ck("27_bbox_z",near(cd[2],187.2))
    ck("28_reopen",r["status"]=="PASS" and r["body"]==c["body"])
    ck("29_restore",rs["semantic_geometry_signature"]==c["semantic_geometry_signature"] and rs["body"]==c["body"])
    ck("30_length_mutation_x",not near(ld[0],cd[0]) and near(ld[1],cd[1]) and near(ld[2],cd[2]))
    ck("31_width_mutation_y",near(wd[0],cd[0]) and not near(wd[1],cd[1]) and near(wd[2],cd[2]))
    ck("32_thickness_mutation_z",near(td[0],cd[0]) and near(td[1],cd[1]) and not near(td[2],cd[2]))
    ck("33_all_roles_same_geometry",all(v["semantic_geometry_signature"]==c["semantic_geometry_signature"] and dims(v)==cd for v in role_docs.values()))
    ck("34_role_labels",all(v["role"]==k for k,v in role_docs.items()))
    ck("35_visual_gate",p["visual_reference_gate"]["general_rule"]=="D-076" and p["visual_reference_gate"]["rufu_pass_decision"]=="D-082" and p["visual_reference_gate"]["status"]=="PASS")
    ck("36_no_ref_length_leak",p["assembly_length_rule"]["default_to_canonical_reference_allowed"] is False)
    ck("37_no_silent_historicization",p["historical_state"]["historical_claim"] is False)
    ck("38_no_unsupported_geometry",p["unsupported_geometry"]==[] and c["body"]["unsupported_detail_count"]==0)
    ck("39_no_p2_proxy",p["p2_primary_frame_proxy_geometry_use_count"]==0)

    review=Path(a.review_dir); names=["FRONT.png","SIDE.png","TOP.png","AXON.png","DIMENSION_PARAMETER_SUMMARY.png","EVIDENCE_UNCERTAINTY_SUMMARY.png"]
    ck("40_review_6_complete",all((review/n).exists() and (review/n).stat().st_size>1000 for n in names))
    sha=digest(a.asset); ck("41_binary_sha",len(sha)==64)
    ck("42_blender_4_5_13",str(c["blender_version"]).startswith("4.5.13"))

    catalog=copy.deepcopy(source_catalog); records=list(catalog.get("new_masters",[]))
    existing=[x for x in records if x.get("component_id")==p["component_id"]]
    ck("43_catalog_rufu_unique_or_absent",len(existing)<=1)
    if existing:
        ru=existing[0]
        ck("44_catalog_rufu_existing_identity",ru.get("master_id")==p["master_id"])
    else:
        records.append({"component_id":p["component_id"],"master_id":p["master_id"],"master_version":"V001",
                        "role_variants":["UPPER","LOWER","NE","SE","SW","NW"],
                        "approval_status":"ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
                        "canonical_asset_status":"ACTIONS_ARTIFACT","canonical_asset_sha256":sha,
                        "semantic_geometry_signature":c["semantic_geometry_signature"],
                        "canonical_section_mm":{"width":330.5,"thickness":187.2},"exact_plan_angle_deg":None,
                        "groove_boundary":"DIRECT_EXISTENCE / GEOMETRY_DEFERRED"})
    catalog["task"]="T-024"; catalog["status"]="SOURCE_CATALOG_PLUS_RUFU_ENGINEERING_COMPLETE_PENDING_REVIEW"; catalog["new_masters"]=records
    Path(a.catalog).write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    result={"task":"T-024","status":"PASS","approval_boundary":"ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
            "check_count":len(checks),"checks":checks,"blender_version":c["blender_version"],"canonical_blend_sha256":sha,
            "semantic_geometry_signature":c["semantic_geometry_signature"],"review_paths":names,"canonical_section_mm":[330.5,187.2],
            "role_variants":["UPPER","LOWER","NE","SE","SW","NW"],"historical_full_length_mm":None,"exact_plan_angle_deg":None,
            "groove_boundary":"DIRECT_EXISTENCE / GEOMETRY_DEFERRED"}
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    Path(a.report).write_text("# T-024｜乳栿 Master First Article｜Engineering Review\n\nStatus: **ENGINEERING PASS / PENDING CHATGPT + PRODUCT OWNER REVIEW**\n\n"
      +f"- Validation: {len(checks)}/{len(checks)} PASS\n- Blender: {c['blender_version']}\n- Binary SHA-256: {sha}\n"
      +f"- Semantic geometry signature: {c['semantic_geometry_signature']}\n- Section: 330.5 × 187.2 mm / measured family mean\n"
      +"- UPPER/LOWER/NE/SE/SW/NW: shared body geometry\n- Exact plan angle: UNKNOWN / no 45-degree assumption\n"
      +"- Groove: DIRECT existence / geometry DEFERRED\n- Historical full length: UNKNOWN / null\n"
      +"- Canonical reference length: 1000 mm / non-historical only\n- Review images: 6/6\n- PR: DO NOT MERGE pending Product Owner review.\n",encoding="utf-8")
    print("T024_VALIDATION_PASS",sha,c["semantic_geometry_signature"])

if __name__=="__main__": main()
