#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(".")
CAT=ROOT/"production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json"
REGS=[
    ROOT/"docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json",
    ROOT/"docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json",
]
TASK=ROOT/"docs/tasks/T-034_P3_3_LANE_MASTER_V2_V001.md"

MASTER_ID="CMP-FRAME-LANE-001_MASTER"
COMP_ID="CMP-FRAME-LANE-001"
COMP="阑额"

cat=json.loads(CAT.read_text(encoding="utf-8"))
assert cat["approved_master_count"]==17, cat["approved_master_count"]
assert not any(x.get("master_id")==MASTER_ID for x in cat.get("new_masters",[]))

entry={
  "component_id":COMP_ID,
  "master_id":MASTER_ID,
  "master_version":"V001",
  "approval_status":"PRODUCT_OWNER_APPROVED",
  "decision_id":"D-151",
  "formalization_authority":"D-152",
  "publication_status":"FORMALIZED / PR #30 OPEN",
  "canonical_asset_status":"ACTIONS_ARTIFACT / APPROVED / LOCAL ONLY / NOT GIT",
  "canonical_asset_sha256":"b3facc02fdef388f90ee38281b4bdc5f8d493dc71505b2de8b4308557f8e759d",
  "semantic_sha256":"a47651910a96543f1426cc3293ca787e8b373b47dc481056f45b4e198744e083",
  "validation_sha256":"ec554a490ca2a9f112be6146d013037f7b543f035127d4c7e9108c563ca0882f",
  "review_board_sha256":"29f24d066a258693dbeba080f8e46a56aa191be9f1bff76816f96e2661187cef",
  "semantic_geometry_signature":"d1117d15868e5f9df37fc679b9c7cc6b0732ef79bcfef6b5e15c4a91fff94ed5",
  "canonical_section_mm":{"width":265.6,"thickness":105},
  "physical_instance_count":12,
  "geometry_variant_count":0,
  "distribution":"12 LOCATION-LOCKED INSTANCES / 12 DIRECT WIDTHS / 4 DIRECT THICKNESSES / 8 PARAMETRIC_COMPLETION THICKNESSES",
  "thickness_evidence_policy":{
    "direct_measured_count":4,
    "unmeasured_count":8,
    "production_completion_mm":105,
    "completion_classification":"PARAMETRIC_COMPLETION / REPLACEABLE / HISTORICAL_CLAIM_FALSE"
  },
  "source_artifact":{
    "actions_run_id":36222778768,
    "artifact_id":10899808683,
    "artifact_zip_sha256":"8034aec4b79740d52b68b162bcf04c0a1ce0b81e2ddeff9cd352e32e11985e88"
  },
  "shared_regression_artifact_id":10899644135,
  "accepted_engineering_head":"7daedf91d161f26235dd69e095ff93291a1e9fb2",
  "assembly_span_rule":"COLUMN_CENTER_DISTANCE / TOPOLOGY_AND_PLACEMENT_CONTROL_ONLY",
  "historical_full_timber_length_mm":None,
  "canonical_reference_length_mm":1000,
  "corner_projection":"NONE / A2 SAME-BUILDING SEMANTIC",
  "joinery_boundary":"EXACT JOINERY / END PENETRATION DEFERRED",
  "minimal_sufficient_package":{
    "policy":"ADAPTIVE / NO UNIVERSAL FILE COUNT",
    "formal_repo_files":[
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LANE-001/CMP-FRAME-LANE-001_MASTER_DEFINITION_V001.json",
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LANE-001/CMP-FRAME-LANE-001_MASTER_SEMANTIC_V001.json",
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LANE-001/CMP-FRAME-LANE-001_MASTER_REVIEW_BOARD_V001.png",
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LANE-001/CMP-FRAME-LANE-001_MASTER_VALIDATION_V001.json",
      "docs/tasks/T-034_P3_3_LANE_MASTER_V2_V001.md"
    ],
    "canonical_blend":"ACTIONS_ARTIFACT + LOCAL ONLY / NOT GIT",
    "review_board_count":1,
    "required_review_panel_count":6
  }
}
cat["task"]="T-034"
cat["status"]="EIGHTEEN_APPROVED / T034 FORMALIZED / PR #30 OPEN"
cat["new_masters"].append(entry)
cat["approved_master_count"]=18
CAT.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

expected_ids={
"阑额-南立面-西次间","阑额-南立面-明间","阑额-南立面-东次间",
"阑额-北立面-西次间","阑额-北立面-明间","阑额-北立面-东次间",
"阑额-东山-北次间","阑额-东山-明间","阑额-东山-南次间",
"阑额-西山-北次间","阑额-西山-明间","阑额-西山-南次间",
}
for p in REGS:
    reg=json.loads(p.read_text(encoding="utf-8"))
    rows=[x for x in reg["items"] if x.get("component")==COMP]
    assert len(rows)==12, (p,len(rows))
    assert {x["id"] for x in rows}==expected_ids
    for x in rows:
        assert x.get("master_coverage_status")=="MASTER_REQUIRED_PENDING", (p,x["id"],x.get("master_coverage_status"))
        x["master_coverage_status"]="APPROVED_MASTER_AVAILABLE"
        x["master_reference"]=MASTER_ID
    pr=reg["stage1_master_progress_summary"]
    assert pr["registry_record_count"]==505
    assert pr["master_scope_object_type_count"]==28
    assert pr["approved_master_count"]==17
    assert pr["master_covered_registry_record_count"]==131
    pr["snapshot_date"]="2026-09-26"
    pr["status"]="PR #30 FORMALIZED CANDIDATE / D-151 ACCEPTED / D-152 FORMALIZATION AUTHORIZED / FINAL VALIDATION PENDING"
    pr["approved_master_count"]=18
    pr["pending_master_object_type_count"]=10
    pr["master_completion_percent"]=64.3
    cm=pr.setdefault("completed_master_components",[])
    assert COMP not in cm
    cm.append(COMP)
    pr["master_covered_registry_record_count"]=143
    pr["progress_display_note"]="505 Registry records; Stage1 Master completion: 18 approved / 10 pending = 64.3%. T-034 阑额 formalized candidate on PR #30; 12/12 阑额 rows bound to CMP-FRAME-LANE-001_MASTER; final regression and derived Excel sync required before merge."
    p.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

text=TASK.read_text(encoding="utf-8")
marker="## 24. D-152 formalization authorization"
if marker not in text:
    text += f"""\n\n{marker}\n\nProduct Owner authorized T-034 formalization + Catalog/V008 binding on 2026-09-26.\n\nFormalization rules:\n- materialize exact D-151 accepted Semantic / Validation / Review Board from Artifact 10899808683;\n- canonical .blend remains Actions Artifact + local only / not Git;\n- Catalog candidate becomes 18 approved Masters;\n- V008/CURRENT 阑额 binding = 12/12 to {MASTER_ID};\n- Stage1 candidate = 18/28 = 64.3%;\n- Master-covered Registry rows candidate = 143;\n- derived Excel sync and latest-head Master V2 regression are mandatory.\n\nStill not authorized:\n- PR #30 merge;\n- next component;\n- Stage2;\n- T-018 resume.\n"""
    TASK.write_text(text,encoding="utf-8")

print("T034_FORMALIZATION_CANDIDATE_READY",cat["approved_master_count"])
