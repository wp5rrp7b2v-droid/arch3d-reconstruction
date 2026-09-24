#!/usr/bin/env python3
import json
from pathlib import Path

CAT=Path("production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json")
REG=Path("docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json")
SNAP=Path("docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json")

cat=json.loads(CAT.read_text(encoding="utf-8"))
assert cat["approved_master_count"]==15
assert not any(x.get("master_id")=="CMP-FRAME-DAJIAOLIANG-001_MASTER" for x in cat.get("new_masters",[]))
cat["task"]="T-030"
cat["status"]="SIXTEEN_APPROVED / T030 ACCEPTED / FORMALIZED ON PR #18 / MERGE PENDING"
cat["new_masters"].append({
  "component_id":"CMP-FRAME-DAJIAOLIANG-001",
  "master_id":"CMP-FRAME-DAJIAOLIANG-001_MASTER",
  "master_version":"V001",
  "approval_status":"PRODUCT_OWNER_APPROVED",
  "decision_id":"D-128",
  "formalization_authority":"D-129",
  "publication_status":"FORMALIZED / PR #18 MERGE PENDING",
  "canonical_asset_status":"ACTIONS_ARTIFACT / APPROVED / LOCAL ONLY / NOT GIT",
  "canonical_asset_sha256":"199e1dcf7274d732e26e430e80e171f9a2a4d0c55162fb6bb100fe51b681aa91",
  "semantic_sha256":"ef69a45735415c618bdfe995181d545e231674b12476af119f92b8d1da610617",
  "validation_sha256":"8ef4970b6b3b353c5b58a94248a6d978f5ac89e10e03e0ad82ebc9c155911062",
  "review_board_sha256":"2398bff3922f3a6373a7160642d787e1b797911c758c558acfc4a92e58679fff",
  "semantic_geometry_signature":"b38684fe6adac315a53e62c5d773f36c5eabb305b744e03627b1ac9814f32dc2",
  "canonical_section_mm":{"width":225,"thickness":200.5},
  "physical_instance_count":4,
  "distribution":"SE / NE / SW / NW = 1 EACH / DIRECT_LOCKED_LOCATION_SECTION",
  "source_artifact":{"actions_run_id":35977160199,"artifact_id":10800439343},
  "shared_regression_artifact_id":10801150421,
  "accepted_engineering_head":"a8f195822a96b05bc206cd463c057885c47e2bb1"
})
cat["approved_master_count"]=16
CAT.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

reg=json.loads(REG.read_text(encoding="utf-8"))
assert reg["schema_version"]=="V008"
rows=[x for x in reg["items"] if x.get("component")=="大角梁"]
assert len(rows)==4
expected_ids={"大角梁-东南角","大角梁-东北角","大角梁-西南角","大角梁-西北角"}
assert {x.get("id") for x in rows}==expected_ids
for x in rows:
    assert x.get("master_coverage_status")=="MASTER_REQUIRED_PENDING"
    x["master_coverage_status"]="APPROVED_MASTER_AVAILABLE"
    x["master_reference"]="CMP-FRAME-DAJIAOLIANG-001_MASTER"

p=reg["stage1_master_progress_summary"]
assert p["approved_master_count"]==15
assert p["master_covered_registry_record_count"]==123
p.update({
  "snapshot_date":"2026-09-24",
  "status":"PR #18 FORMALIZED CANDIDATE / D-128 DAJIAOLIANG ACCEPTED / D-129 MERGE AUTHORIZED AFTER FINAL PASS",
  "approved_master_count":16,
  "pending_master_object_type_count":12,
  "master_completion_percent":57.1,
  "master_covered_registry_record_count":127
})
if "大角梁" not in p["approved_master_components"]:
    p["approved_master_components"].append("大角梁")
p["progress_display_note"]="505 Registry records; Stage1 Master completion: 16 approved / 12 pending = 57.1%. T-030 Dajiao beam formalized candidate on PR #18; merge only after final regression/cross-check PASS."
assert sum(x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE" for x in reg["items"])==127
REG.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
SNAP.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("T030_BINDING_UPDATE_PASS")
