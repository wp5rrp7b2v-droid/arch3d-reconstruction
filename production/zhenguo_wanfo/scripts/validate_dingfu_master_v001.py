"""Validate T-023 Dingfu Master first article."""
import argparse, copy, hashlib, json
from pathlib import Path
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def near(a,b,t=1e-3): return abs(float(a)-float(b))<=t
def dims(s): return [float(x) for x in s["body"]["local_bbox_mm"]["dimensions"]]
def main():
    ap=argparse.ArgumentParser()
    for n in ("params","canonical","reopen","length","width","thickness","upper","lower","restore","asset","review_dir","registry","source_catalog","output","catalog","report"):
        ap.add_argument("--"+n.replace("_","-"),dest=n,required=True)
    a=ap.parse_args()
    p=load(a.params); c=load(a.canonical); r=load(a.reopen); lm=load(a.length); wm=load(a.width); tm=load(a.thickness); up=load(a.upper); lo=load(a.lower); rs=load(a.restore)
    reg=load(a.registry); source_catalog=load(a.source_catalog)
    P={x["key"]:x for x in p["parameters"]}; checks={}
    def ck(n,v):
        if not v: raise AssertionError(n)
        checks[n]="PASS"
    items=[x for x in reg["items"] if x.get("component")=="丁栿"]; ids={x["id"] for x in items}
    expected={"丁栿-东山-上丁栿-南","丁栿-东山-上丁栿-北","丁栿-东山-下丁栿-南","丁栿-东山-下丁栿-北",
              "丁栿-西山-上丁栿-南","丁栿-西山-上丁栿-北","丁栿-西山-下丁栿-南","丁栿-西山-下丁栿-北"}
    cd=dims(c); ld=dims(lm); wd=dims(wm); td=dims(tm); ud=dims(up); lod=dims(lo)
    ck("01_component_id",p["component_id"]=="CMP-FRAME-DINGFU-001"==c["component_id"])
    ck("02_master_id",p["master_id"]=="CMP-FRAME-DINGFU-001_MASTER"==c["master_id"])
    ck("03_registry_v008",reg["schema_version"]=="V008" and reg["item_count"]==505)
    ck("04_instance_count_8",len(items)==8)
    ck("05_exact_instance_ids",ids==expected)
    ck("06_samples_8",len(p["measured_section_samples_mm"])==8)
    ck("07_mapping_unknown",p["sample_to_instance_mapping"]=="UNKNOWN" and all(x["sample_to_instance_mapping"]=="UNKNOWN" for x in items))
    ck("08_width_mean",P["width_mm"]["value"]==331.6)
    ck("09_thickness_mean",P["thickness_mm"]["value"]==200.9)
    ck("10_report_metadata_only",p["report_analysis"]["geometry_use_count"]==0 and p["report_analysis"]["rounded_fen"]=={"width":22,"thickness":13})
    ck("11_historical_length_null",P["historical_full_length_mm"]["value"] is None)
    ck("12_reference_1000_nonhistorical",P["canonical_reference_length_mm"]["value"]==1000.0 and P["canonical_reference_length_mm"]["historical_claim"] is False)
    ck("13_roles",p["role_variants"]==["UPPER","LOWER"] and p["role_geometry_policy"]=="SHARED_CANONICAL_BODY")
    ck("14_interfaces",set(p["interface_contract"])=={"OUTBOARD_END","INBOARD_END"})
    ck("15_groove_direct",p["groove_boundary"]["status"]=="DIRECT_EXISTENCE / GEOMETRY_DEFERRED")
    ck("16_groove_not_cut",p["groove_boundary"]["stage1_cut_geometry"] is False and c["body"]["groove_cut_count"]==0)
    ck("17_bbox_x",near(cd[0],1000.0)); ck("18_bbox_y",near(cd[1],331.6)); ck("19_bbox_z",near(cd[2],200.9))
    ck("20_reopen",r["status"]=="PASS" and r["body"]==c["body"])
    ck("21_restore",rs["semantic_geometry_signature"]==c["semantic_geometry_signature"] and rs["body"]==c["body"])
    ck("22_length_mutation_x",not near(ld[0],cd[0]) and near(ld[1],cd[1]) and near(ld[2],cd[2]))
    ck("23_width_mutation_y",near(wd[0],cd[0]) and not near(wd[1],cd[1]) and near(wd[2],cd[2]))
    ck("24_thickness_mutation_z",near(td[0],cd[0]) and near(td[1],cd[1]) and not near(td[2],cd[2]))
    ck("25_role_upper_same_geometry",up["semantic_geometry_signature"]==c["semantic_geometry_signature"] and ud==cd)
    ck("26_role_lower_same_geometry",lo["semantic_geometry_signature"]==c["semantic_geometry_signature"] and lod==cd)
    ck("27_role_labels",up["role"]=="UPPER" and lo["role"]=="LOWER")
    ck("28_visual_waiver",p["visual_reference_gate"]["dingfu_waiver"]=="D-077" and p["visual_reference_gate"]["waiver_scope"]=="DINGFU_ONLY")
    ck("29_no_ref_length_leak",p["assembly_length_rule"]["default_to_canonical_reference_allowed"] is False)
    ck("30_no_silent_historicization",p["historical_state"]["historical_claim"] is False)
    ck("31_no_unsupported_geometry",p["unsupported_geometry"]==[] and c["body"]["unsupported_detail_count"]==0)
    ck("32_no_p2_proxy",p["p2_primary_frame_proxy_geometry_use_count"]==0)
    review=Path(a.review_dir); names=["FRONT.png","SIDE.png","TOP.png","AXON.png","DIMENSION_PARAMETER_SUMMARY.png","EVIDENCE_UNCERTAINTY_SUMMARY.png"]
    ck("33_review_6_complete",all((review/n).exists() and (review/n).stat().st_size>1000 for n in names))
    sha=digest(a.asset); ck("34_binary_sha",len(sha)==64)
    ck("35_blender_4_5_13",str(c["blender_version"]).startswith("4.5.13"))
    catalog=copy.deepcopy(source_catalog); records=list(catalog.get("new_masters",[]))
    existing=[x for x in records if x.get("component_id")==p["component_id"]]
    ck("36_catalog_no_duplicate",len(existing)==0)
    records.append({"component_id":p["component_id"],"master_id":p["master_id"],"master_version":"V001",
                    "role_variants":["UPPER","LOWER"],"approval_status":"ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
                    "canonical_asset_status":"ACTIONS_ARTIFACT","canonical_asset_sha256":sha,
                    "semantic_geometry_signature":c["semantic_geometry_signature"],
                    "groove_boundary":"DIRECT_EXISTENCE / GEOMETRY_DEFERRED"})
    catalog["task"]="T-023"; catalog["status"]="SOURCE_CATALOG_PLUS_DINGFU_ENGINEERING_COMPLETE_PENDING_REVIEW"; catalog["new_masters"]=records
    Path(a.catalog).write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    result={"task":"T-023","status":"PASS","approval_boundary":"ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
            "check_count":len(checks),"checks":checks,"blender_version":c["blender_version"],"canonical_blend_sha256":sha,
            "semantic_geometry_signature":c["semantic_geometry_signature"],"review_paths":names,
            "canonical_section_mm":[331.6,200.9],"role_variants":["UPPER","LOWER"],
            "groove_boundary":"DIRECT_EXISTENCE / GEOMETRY_DEFERRED"}
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    Path(a.report).write_text("# T-023｜丁栿 Master First Article｜Engineering Review\n\nStatus: **ENGINEERING PASS / PENDING CHATGPT + PRODUCT OWNER REVIEW**\n\n"
      +f"- Validation: {len(checks)}/{len(checks)} PASS\n- Blender: {c['blender_version']}\n- Binary SHA-256: {sha}\n"
      +f"- Semantic geometry signature: {c['semantic_geometry_signature']}\n- Section: 331.6 × 200.9 mm / measured family mean\n"
      +"- UPPER/LOWER: shared body geometry\n- Groove: DIRECT existence / geometry DEFERRED\n- Historical full length: UNKNOWN / null\n"
      +"- Canonical reference length: 1000 mm / non-historical only\n- Review images: 6/6\n- PR: DO NOT MERGE pending Product Owner review.\n",encoding="utf-8")
    print("T023_VALIDATION_PASS",sha,c["semantic_geometry_signature"])
if __name__=="__main__": main()
