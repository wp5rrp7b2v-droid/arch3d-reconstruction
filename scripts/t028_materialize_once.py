#!/usr/bin/env python3
import json
from pathlib import Path

CATALOG=Path("production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json")
REGISTRY=Path("docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json")
TASK=Path("docs/tasks/T-028_P3_3_CHASHOU_MASTER_V2_V001.md")
DASH_WF=Path(".github/workflows/project-dashboard-v2-sync.yml")

catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
assert catalog["approved_master_count"]==13
assert not any(x.get("master_id")=="CMP-FRAME-CHASHOU-001_MASTER" for x in catalog.get("new_masters",[]))

catalog["task"]="T-028"
catalog["status"]="FOURTEEN_APPROVED / T028 PRODUCT_OWNER_APPROVED / FORMALIZED ON PR #16 / MERGE PENDING"
catalog["new_masters"].append({
  "component_id":"CMP-FRAME-CHASHOU-001",
  "master_id":"CMP-FRAME-CHASHOU-001_MASTER",
  "master_version":"V001",
  "approval_status":"PRODUCT_OWNER_APPROVED",
  "decision_id":"D-111",
  "formalization_authority":"D-112",
  "publication_status":"FORMALIZED / PR #16 MERGE PENDING",
  "canonical_asset_status":"ACTIONS_ARTIFACT / APPROVED / LOCAL_RESTORE_PENDING",
  "canonical_asset_sha256":"25da16f9e69c930ff4b37523c23bb19ac7ef1f3c5dcf2ffcc7dcaf17f35eff25",
  "semantic_sha256":"28ccd0ea91f8935ebbeaa7c4c9be59ea1bd25c8acc790cbec53342477d86f05d",
  "validation_sha256":"e8cb259cb5fa9be474bce120c0984ae02c7159c1ad27bdc5d63deb457c4dcde6",
  "review_board_sha256":"07bf0761410b3db9c7bc00161a04a34027ca7711f38437978715f3807eda577f",
  "semantic_geometry_signature":"410a64eac567e256253e56b94ab44f8273ccac634fa01a1d211913ca1b0bd72e",
  "canonical_section_mm":{"width":230.5,"thickness":90.5},
  "source_internal_numeric_conflict":False,
  "historical_full_length_mm":None,
  "canonical_reference_length_mm":1000,
  "geometry_mode":"PARAMETRIC_ENDPOINT_DRIVEN_LONG_MEMBER",
  "physical_instance_count":8,
  "distribution":"INTERIOR_FRAME 4 / GABLE_FRAME 4",
  "geometry_variant_count":0,
  "endpoint_policy":"ACTUAL LENGTH / CENTER / ORIENTATION ARE ASSEMBLY-ENDPOINT-DERIVED",
  "historical_joinery":"UNRESOLVED_METADATA / STAGE1 SIMPLIFIED FLAT END",
  "source_artifact":{
    "actions_run_id":35825911214,
    "artifact_id":10735946772,
    "artifact_zip_sha256":"5c4a77a41291433b590911d4b1c6aa806a1b2dff579d2cecc80ca1bbd28b4151"
  },
  "minimal_sufficient_package":{
    "policy":"ADAPTIVE / NO UNIVERSAL FILE COUNT",
    "component_specific_formal_file_count":6,
    "formal_repo_files":[
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-CHASHOU-001/CMP-FRAME-CHASHOU-001_MASTER_DEFINITION_V001.json",
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-CHASHOU-001/CMP-FRAME-CHASHOU-001_MASTER_SEMANTIC_V001.json",
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-CHASHOU-001/CMP-FRAME-CHASHOU-001_MASTER_REVIEW_BOARD_V001.png",
      "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-CHASHOU-001/CMP-FRAME-CHASHOU-001_MASTER_VALIDATION_V001.json",
      "docs/tasks/T-028_P3_3_CHASHOU_MASTER_V2_V001.md"
    ],
    "canonical_blend":"ACTIONS_ARTIFACT + LOCAL ONLY / NOT GIT",
    "review_board_count":1,
    "required_review_panel_count":6
  },
  "accepted_engineering_head":"eba3b798f05de54713910549bd198dbb43110f26"
})
catalog["approved_master_count"]=14
CATALOG.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

reg=json.loads(REGISTRY.read_text(encoding="utf-8"))
assert reg["schema_version"]=="V008"
ch=[x for x in reg["items"] if x.get("component")=="叉手"]
assert len(ch)==8
assert all(x.get("master_coverage_status")=="MASTER_REQUIRED_PENDING" for x in ch)
for x in ch:
    x["master_coverage_status"]="APPROVED_MASTER_AVAILABLE"
    x["master_reference"]="CMP-FRAME-CHASHOU-001_MASTER"

addition=" D-111 approves the Chashou first article; D-112 formalizes the accepted outputs and binds all 8 叉手 records to CMP-FRAME-CHASHOU-001_MASTER on PR #16 pending merge."
if addition.strip() not in reg.get("generation_note",""):
    reg["generation_note"]=reg.get("generation_note","")+addition

p=reg["stage1_master_progress_summary"]
assert p["approved_master_count"]==13
assert p["master_covered_registry_record_count"]==111
p["snapshot_date"]="2026-09-23"
p["status"]="PR #16 FORMALIZED CANDIDATE / D-111 CHASHOU APPROVED / D-112 CATALOG+V008 BINDING / MERGE PENDING"
p["approved_master_count"]=14
p["pending_master_object_type_count"]=14
p["master_completion_percent"]=50.0
if "叉手" not in p["approved_master_components"]:
    p["approved_master_components"].append("叉手")
p["master_covered_registry_record_count"]=119
p["progress_display_note"]="505 is registry-record count, not a whole-building physical-piece total. Stage1 Master completion uses 28 Master-scope object types as denominator: 14 approved / 14 pending = 50.0%. This is a PR #16 formalized candidate until merge to main."
assert sum(1 for x in reg["items"] if x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE")==119
REGISTRY.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

task=TASK.read_text(encoding="utf-8").rstrip()
if "## 25. Formalization Attempt #1" not in task:
    task += """

## 25. Formalization Attempt #1｜Workflow parse failure / no mutation

Run 35835041762 failed during workflow parsing before any job was created.
Classification: WORKFLOW_YAML_PARSE_FAILURE.
No Artifact download, materialization, Catalog mutation, V008 mutation, or binary publication occurred.
The attempt is superseded; D-112 byte identities and authorization boundaries remain unchanged.
"""
if "## 26. D-112 exact materialization + Catalog/V008 binding" not in task:
    task += """

## 26. D-112 exact materialization + Catalog/V008 binding

Formalization executed from the D-111 accepted Artifact 10735946772 / Run 35825911214.

Exact bytes verified before publication:
- canonical .blend SHA-256: 25da16f9e69c930ff4b37523c23bb19ac7ef1f3c5dcf2ffcc7dcaf17f35eff25 — verified, NOT committed
- Semantic SHA-256: 28ccd0ea91f8935ebbeaa7c4c9be59ea1bd25c8acc790cbec53342477d86f05d
- Validation SHA-256: e8cb259cb5fa9be474bce120c0984ae02c7159c1ad27bdc5d63deb457c4dcde6
- Review Board SHA-256: 07bf0761410b3db9c7bc00161a04a34027ca7711f38437978715f3807eda577f

Formalized PR-branch candidate:
- Stage1 Catalog approved Masters: 14
- V008 Chashou binding: 8 / 8
- approved-Master-covered Registry records: 119
- Stage1 Master completion candidate: 14 / 28 = 50.0%
- next Master-scope target: 蜀柱

This state is not canonical on main until PR #16 merge.
PR #16 merge remains separately unauthorized.
"""
task="\n".join(line.rstrip() for line in task.splitlines()).rstrip()
TASK.write_text(task+"\n",encoding="utf-8")

s=DASH_WF.read_text(encoding="utf-8")
s=s.replace('grep -q "13 / 28" docs/project_control/dashboard.html','grep -q "14 / 28" docs/project_control/dashboard.html')
s=s.replace('grep -q "46.4%" docs/project_control/dashboard.html','grep -q "50.0%" docs/project_control/dashboard.html')
s=s.replace('grep -q "下一目标：叉手" docs/project_control/dashboard.html','grep -q "下一目标：蜀柱" docs/project_control/dashboard.html')
DASH_WF.write_text(s,encoding="utf-8")

print("T028_BINDING_UPDATE_PASS")
