#!/usr/bin/env python3
import json, shutil
from pathlib import Path
CAT=Path("production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json")
REG=Path("docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json")
SNAP=Path("docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json")
cat=json.loads(CAT.read_text()); assert cat["approved_master_count"]==14
cat["task"]="T-029"; cat["status"]="FIFTEEN_APPROVED / T029 ACCEPTED / FORMALIZED ON PR #17 / MERGE PENDING"
cat["new_masters"].append({"component_id":"CMP-FRAME-SHUZHU-001","master_id":"CMP-FRAME-SHUZHU-001_MASTER","master_version":"V001","approval_status":"PRODUCT_OWNER_APPROVED","decision_id":"D-118","formalization_authority":"D-116","publication_status":"FORMALIZED / PR #17 MERGE PENDING","canonical_asset_status":"ACTIONS_ARTIFACT / APPROVED / LOCAL ONLY / NOT GIT","canonical_asset_sha256":"becf3323c0ff02606abdbb04e15be550f7c5d4dd74a8d5b9f4bd9adef53c10b6","semantic_sha256":"3327a95918d61c0ed830fb49a46042c88cb9be2b36a64b958e29918529d2cd93","validation_sha256":"5cfe4c5086d847e7c1f34b6ff7ea6488b20b7f9381d55e0c5fb063b5cfe6a5cb","review_board_sha256":"8fc89aed2ad0f0329bceb890e9a5350bac6d2aea22de2d92d34d935fa3db7d64","semantic_geometry_signature":"301e5a8ecf45cdc586d701571be7415aa3eb9e3e0d02bbb8a6b82ebef3a64a40","canonical_section_mm":{"width":218.75,"thickness":157.5},"physical_instance_count":4,"distribution":"INTERIOR_FRAME 2 / GABLE_FRAME 2","source_artifact":{"actions_run_id":35847859509,"artifact_id":10744639697},"accepted_engineering_head":"46eead003019dc30e9fc15439f16f4ba2f94f83c"})
cat["approved_master_count"]=15; CAT.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n")
reg=json.loads(REG.read_text()); assert reg["schema_version"]=="V008"
rows=[x for x in reg["items"] if x.get("component")=="蜀柱"]; assert len(rows)==4
for x in rows:
 assert x.get("master_coverage_status")=="MASTER_REQUIRED_PENDING"
 x["master_coverage_status"]="APPROVED_MASTER_AVAILABLE"; x["master_reference"]="CMP-FRAME-SHUZHU-001_MASTER"
p=reg["stage1_master_progress_summary"]; assert p["approved_master_count"]==14 and p["master_covered_registry_record_count"]==119
p.update({"snapshot_date":"2026-09-23","status":"PR #17 FORMALIZED CANDIDATE / D-118 SHUZHU ACCEPTED / MERGE PENDING","approved_master_count":15,"pending_master_object_type_count":13,"master_completion_percent":53.6,"master_covered_registry_record_count":123})
if "蜀柱" not in p["approved_master_components"]: p["approved_master_components"].append("蜀柱")
p["progress_display_note"]="505 Registry records; Stage1 Master completion: 15 approved / 13 pending = 53.6%. PR #17 candidate until merge."
assert sum(x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE" for x in reg["items"])==123
REG.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n"); SNAP.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n")
print("T029_BINDING_UPDATE_PASS")
