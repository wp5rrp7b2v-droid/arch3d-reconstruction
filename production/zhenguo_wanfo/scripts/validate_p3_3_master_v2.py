"""Generic P3.3 Master V2 validator driven by a locked Master Definition."""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def near(a,b,t=1e-3):
    return abs(float(a)-float(b))<=t

def dims(s):
    return [float(x) for x in s["body"]["local_bbox_mm"]["dimensions"]]

def main():
    ap=argparse.ArgumentParser()
    for n in ("definition","canonical","reopen","length","width","thickness","restore","asset","review_dir","board","registry","catalog","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n,required=True)
    a=ap.parse_args()
    d=load(a.definition); c=load(a.canonical); r=load(a.reopen)
    lm=load(a.length); wm=load(a.width); tm=load(a.thickness); rs=load(a.restore)
    reg=load(a.registry)
    catalog=load(a.catalog)
    checks={}
    def ck(name,value):
        if not value:
            raise AssertionError(name)
        checks[name]="PASS"

    rb=d["registry_boundary"]
    gc=d["geometry_contract"]
    auth=d["authority"]
    component=d["component_name_zh"]
    items=[x for x in reg["items"] if x.get("component")==component]

    ck("01_definition_locked",d["status"].startswith("LOCKED / PRODUCT_OWNER_APPROVED") and d["approval"]["definition_locked"] is True)
    ck("02_execution_authorized",d["execution_boundary"]["engineering_execution_authorized"] is True)
    ck("03_visual_gate",auth["visual_reference_gate"]["result"]=="PASS")
    ck("04_registry_version",reg["schema_version"]==auth["registry_schema_version_expected"])
    ck("05_registry_record_count",reg["item_count"]==auth["registry_record_count_expected"])
    ck("06_component_identity",c["component_id"]==d["component_id"] and c["master_id"]==d["master_id"] and c["master_version"]==d["master_version"])
    ck("07_instance_count",len(items)==rb["physical_instance_count"])
    east=[x for x in items if x.get("id","").startswith(component+"-东山")]
    west=[x for x in items if x.get("id","").startswith(component+"-西山")]
    ck("08_known_gable_counts",len(east)==rb["east_gable_known_count"] and len(west)==rb["west_gable_known_count"])
    ck("09_unresolved_count",len(items)-len(east)-len(west)==rb["exact_location_unresolved_count"])
    w=float(rb["section_mm"]["width"]); h=float(rb["section_mm"]["thickness"])
    section_strings=[str(x.get("section_mm","")) for x in items]
    ck("10_registry_section_binding",all(str(w) in s and ("185" in s if near(h,185) else str(h) in s) for s in section_strings))
    ck("11_historical_length_null",rb["historical_full_length_mm"] is None and c["historical_full_length_mm"] is None)
    ck("12_reference_nonhistorical",gc["canonical_reference_length_historical_claim"] is False and c["canonical_reference_length_historical_claim"] is False)
    ck("13_no_unsupported_geometry",gc["unsupported_geometry"]==[] and c["body"]["unsupported_detail_count"]==0 and c["body"]["joinery_cut_count"]==0)
    ck("14_definition_hash",c["definition_sha256"]==digest(a.definition))

    cd=dims(c); ld=dims(lm); wd=dims(wm); td=dims(tm)
    L=float(gc["canonical_reference_length_mm"])
    ck("15_bbox_length",near(cd[0],L))
    ck("16_bbox_width",near(cd[1],w))
    ck("17_bbox_thickness",near(cd[2],h))
    ck("18_origin_transform",c["body"]["local_transform"]=={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]})
    ck("19_reopen",r["status"]=="PASS" and r["body"]==c["body"] and r["semantic_geometry_signature"]==c["semantic_geometry_signature"])
    ck("20_restore",rs["body"]==c["body"] and rs["semantic_geometry_signature"]==c["semantic_geometry_signature"])
    ck("21_length_mutation",not near(ld[0],cd[0]) and near(ld[1],cd[1]) and near(ld[2],cd[2]))
    ck("22_width_mutation",near(wd[0],cd[0]) and not near(wd[1],cd[1]) and near(wd[2],cd[2]))
    ck("23_thickness_mutation",near(td[0],cd[0]) and near(td[1],cd[1]) and not near(td[2],cd[2]))
    ck("24_binary_sha",digest(a.asset)==c["canonical_blend_sha256"] and len(c["canonical_blend_sha256"])==64)
    ck("25_blender_version",str(c["blender_version"]).startswith("4.5.13"))

    rc=d["v2_slim_file_contract"]["review_contract"]
    panels=rc["required_panels"]
    review=Path(a.review_dir)
    ck("26_required_panels_complete",all((review/(x+".png")).exists() and (review/(x+".png")).stat().st_size>1000 for x in panels))
    board=Path(a.board)
    ck("27_review_board_exists",board.exists() and board.stat().st_size>10000)
    im=Image.open(board)
    cols=min(3,max(1,len(panels))); rows=math.ceil(len(panels)/cols)
    ck("28_review_board_dimensions",im.size==(cols*1200,rows*940))
    ck("29_no_fixed_panel_rule",d["v2_slim_file_contract"]["fixed_review_panel_count_required"] is False)
    ck("30_minimal_sufficient_rule",d["v2_slim_file_contract"]["principle"]=="MINIMAL_SUFFICIENT_COMPONENT_PACKAGE")

    master_dir=str(Path(a.definition).parent)
    tracked=subprocess.check_output(["git","ls-files","--",master_dir+"/*.blend"],text=True).strip()
    ck("31_no_tracked_canonical_blend_in_master_dir",tracked=="")
    ck("32_definition_semantic_validation_independence",
       "MASTER_DEFINITION_V001.json" in " ".join(d["v2_slim_file_contract"]["zhaqian_current_package"]) and
       c["schema_version"]=="MASTER_V2_SEMANTIC_1.0")
    ck("33_unknowns_preserved",
       rb["exact_instance_endpoints"]=="UNKNOWN" and rb["sample_to_instance_mapping"]=="UNKNOWN" and
       any("historical full lengths" in x for x in d["unknowns"]))
    ck("34_reference_length_assembly_guard",
       "ASSEMBLY_OWNED" in gc["placement_policy"] and gc["canonical_reference_length_historical_claim"] is False)
    ck("35_visual_source_not_dimension_authority",auth["visual_reference_gate"]["dimension_authority"] is False)

    catalog_entries=[x for x in catalog.get("new_masters",[]) if x.get("master_id")==d["master_id"]]
    if catalog_entries:
        ce=catalog_entries[0]
        ck("36_catalog_approved",ce.get("approval_status")=="PRODUCT_OWNER_APPROVED")
        ck("37_catalog_binary_identity",ce.get("canonical_asset_sha256")==c["canonical_blend_sha256"])
        ck("38_registry_master_binding",all(x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE" and x.get("master_reference")==d["master_id"] for x in items))
        progress=reg["stage1_master_progress_summary"]
        ck("39_registry_progress_consistent",progress["approved_master_count"]==catalog["approved_master_count"] and progress["pending_master_object_type_count"]==progress["master_scope_object_type_count"]-progress["approved_master_count"])
        ck("40_registry_covered_rows_consistent",progress["master_covered_registry_record_count"]==sum(1 for x in reg["items"] if x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE"))
    else:
        ck("36_preapproval_catalog_absent",all(x.get("master_reference")!=d["master_id"] for x in items))

    result={
      "schema_version":"MASTER_V2_VALIDATION_1.0",
      "task_id":d["task_id"],
      "status":"PASS",
      "approval_boundary":"ENGINEERING_COMPLETE_PENDING_PRODUCT_OWNER_REVIEW",
      "check_count":len(checks),
      "checks":checks,
      "component_id":d["component_id"],
      "master_id":d["master_id"],
      "definition_sha256":digest(a.definition),
      "canonical_blend_sha256":c["canonical_blend_sha256"],
      "semantic_geometry_signature":c["semantic_geometry_signature"],
      "review_board_sha256":digest(a.board),
      "required_review_panels":panels,
      "formal_file_count_policy":"ADAPTIVE / MINIMAL SUFFICIENT / NO FIXED COUNT",
      "blender_version":c["blender_version"]
    }
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MASTER_V2_VALIDATION_PASS",len(checks),c["canonical_blend_sha256"],c["semantic_geometry_signature"])

if __name__=="__main__":
    main()
