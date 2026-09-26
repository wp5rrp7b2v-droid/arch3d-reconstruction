#!/usr/bin/env python3
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path

ZIP = Path(sys.argv[1])
EXPECTED_ZIP = "d664456279065be2d7db01f373dbd60c9744f957e04d0f90636fb23d6731deb7"
EXPECTED = {
    "CMP-FRAME-YOUE-001_MASTER_V001.blend": "6d368d5f67a47c819b13a7f90e30515bee6ec640a9a1d570e68886e9be829e16",
    "CMP-FRAME-YOUE-001_MASTER_SEMANTIC_V001.json": "7e1d0a132f54680fab11b8d373461dba0931552f60e10e55356d9a86471d392a",
    "CMP-FRAME-YOUE-001_MASTER_REVIEW_BOARD_V001.png": "8c5e32edadf442a316daa7c120a1615f49ba13268824e0c91da754082adb2e62",
    "CMP-FRAME-YOUE-001_MASTER_VALIDATION_V001.json": "f7422adec32e98d51457f33c22128677704569bdf493ca76d8b2a9fd164a1fb8",
}
ROOT = Path(".")
MASTER_DIR = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-YOUE-001"
CATALOG = ROOT / "production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json"
CURRENT = ROOT / "docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json"
V008 = ROOT / "docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json"
TASK = ROOT / "docs/tasks/T-035_P3_3_YOUE_MASTER_V2_V001.md"
TMP = Path("/tmp/t035_accepted")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha256(ZIP) == EXPECTED_ZIP, (sha256(ZIP), EXPECTED_ZIP)
if TMP.exists():
    shutil.rmtree(TMP)
TMP.mkdir(parents=True)
with zipfile.ZipFile(ZIP) as z:
    z.extractall(TMP)

for name, digest in EXPECTED.items():
    p = TMP / name
    assert p.exists(), name
    assert sha256(p) == digest, (name, sha256(p), digest)

MASTER_DIR.mkdir(parents=True, exist_ok=True)
for name in (
    "CMP-FRAME-YOUE-001_MASTER_SEMANTIC_V001.json",
    "CMP-FRAME-YOUE-001_MASTER_REVIEW_BOARD_V001.png",
    "CMP-FRAME-YOUE-001_MASTER_VALIDATION_V001.json",
):
    shutil.copyfile(TMP / name, MASTER_DIR / name)
assert not (MASTER_DIR / "CMP-FRAME-YOUE-001_MASTER_V001.blend").exists()

cat = json.loads(CATALOG.read_text(encoding="utf-8"))
entry = {
    "component_id": "CMP-FRAME-YOUE-001",
    "master_id": "CMP-FRAME-YOUE-001_MASTER",
    "master_version": "V001",
    "approval_status": "PRODUCT_OWNER_APPROVED",
    "decision_id": "D-159",
    "formalization_authority": "D-160",
    "publication_status": "FORMALIZED / PR #31 OPEN",
    "canonical_asset_status": "ACTIONS_ARTIFACT / APPROVED / LOCAL ONLY / NOT GIT",
    "canonical_asset_sha256": EXPECTED["CMP-FRAME-YOUE-001_MASTER_V001.blend"],
    "semantic_sha256": EXPECTED["CMP-FRAME-YOUE-001_MASTER_SEMANTIC_V001.json"],
    "validation_sha256": EXPECTED["CMP-FRAME-YOUE-001_MASTER_VALIDATION_V001.json"],
    "review_board_sha256": EXPECTED["CMP-FRAME-YOUE-001_MASTER_REVIEW_BOARD_V001.png"],
    "semantic_geometry_signature": "4ba3601e1603697c03991c08c01c2edc5d2e5c00321bc4ec5a10ea1f4c5580b8",
    "canonical_section_mm": {"width": 252.25, "thickness": 105},
    "physical_instance_count": 4,
    "geometry_variant_count": 0,
    "distribution": "4 LOCATION-LOCKED INSTANCES / 4 DIRECT WIDTHS / 4 DIRECT THICKNESSES",
    "reference_width_policy": "252.25 = PROJECT_DERIVED_REFERENCE / NOT_SOURCE_PUBLISHED_FAMILY_MEAN",
    "historical_orientation_policy": {
        "current_orientation_state": "HISTORICAL_REPAIR_FLIPPED",
        "original_963_top_bottom_orientation": "UNRESOLVED",
        "geometry_variant_created": False,
    },
    "mortise_trace_policy": {
        "existence": "DIRECT_EVIDENCE",
        "exact_geometry": "UNRESOLVED",
        "current_structural_function": "UNRESOLVED",
        "canonical_body_cut": False,
    },
    "source_artifact": {
        "actions_run_id": 36231069458,
        "artifact_id": 10903011230,
        "artifact_zip_sha256": EXPECTED_ZIP,
    },
    "shared_regression_artifact_id": 10902682823,
    "shared_regression_artifact_zip_sha256": "531e2190c85dc62f3a17fa05e352dd9125c5fd960138319b1140d149b5e90dec",
    "accepted_engineering_head": "cab973375d6f88906d1815c06b3a10725a06ef87",
    "historical_full_timber_length_mm": None,
    "canonical_reference_length_mm": 1000,
    "assembly_span_rule": "ENDPOINT_DERIVED / ASSEMBLY_OWNED",
    "joinery_boundary": "COLUMN CONNECTION EXISTENCE KNOWN / EXACT JOINERY + PENETRATION DEFERRED",
    "minimal_sufficient_package": {
        "policy": "ADAPTIVE / NO UNIVERSAL FILE COUNT",
        "formal_repo_files": [
            "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-YOUE-001/CMP-FRAME-YOUE-001_MASTER_DEFINITION_V001.json",
            "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-YOUE-001/CMP-FRAME-YOUE-001_MASTER_SEMANTIC_V001.json",
            "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-YOUE-001/CMP-FRAME-YOUE-001_MASTER_REVIEW_BOARD_V001.png",
            "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-YOUE-001/CMP-FRAME-YOUE-001_MASTER_VALIDATION_V001.json",
            "docs/tasks/T-035_P3_3_YOUE_MASTER_V2_V001.md",
        ],
        "canonical_blend": "ACTIONS_ARTIFACT + LOCAL ONLY / NOT GIT",
        "review_board_count": 1,
        "required_review_panel_count": 6,
    },
}
arr = cat.setdefault("new_masters", [])
matches = [i for i, x in enumerate(arr) if x.get("master_id") == "CMP-FRAME-YOUE-001_MASTER"]
assert len(matches) <= 1
if matches:
    arr[matches[0]] = entry
else:
    arr.append(entry)
cat["approved_master_count"] = 19
cat["task"] = "T-035"
cat["status"] = "NINETEEN_APPROVED / T035 FORMALIZED / PR #31 OPEN"
CATALOG.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

expected_sections = {
    "由额-南立面-西次间": "255×105",
    "由额-南立面-明间": "245×105",
    "由额-南立面-东次间": "250×105",
    "由额-北立面-明间": "259×105",
}

def bind(path: Path) -> None:
    r = json.loads(path.read_text(encoding="utf-8"))
    rows = [x for x in r["items"] if x.get("component") == "由额"]
    assert len(rows) == 4
    for x in rows:
        assert x["id"] in expected_sections
        assert x.get("section_mm") == expected_sections[x["id"]]
        x["master_coverage_status"] = "APPROVED_MASTER_AVAILABLE"
        x["master_reference"] = "CMP-FRAME-YOUE-001_MASTER"
    p = r["stage1_master_progress_summary"]
    comps = list(p.get("approved_master_components", []))
    if "由额" not in comps:
        comps.append("由额")
    assert len(comps) == 19 and len(set(comps)) == 19
    p["approved_master_components"] = comps
    p["approved_master_count"] = 19
    p["pending_master_object_type_count"] = 9
    p["master_completion_percent"] = 67.9
    p["master_covered_registry_record_count"] = 147
    p["status"] = "FORMALIZED / D-160 / T-035 / PR #31 OPEN / 19 OF 28 MASTERS APPROVED"
    p["progress_display_note"] = (
        "505 Registry records; Stage1 Master completion: 19 approved / 9 pending = 67.9%. "
        "T-035 由额 formalized under D-160; 4/4 由额 rows bound to CMP-FRAME-YOUE-001_MASTER; "
        "Registry Excel Sync and final regression pending."
    )
    path.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

bind(CURRENT)
bind(V008)

t = TASK.read_text(encoding="utf-8")
if "## 23. D-160 formalization authorization" not in t:
    t += """
## 23. D-160 formalization authorization

Product Owner authorized the post-approval formalization step on 2026-09-26.

Authorized scope:
- exact-byte materialization of accepted Semantic / Review Board / Validation from Artifact `10903011230`;
- verify accepted canonical .blend SHA but keep .blend Actions Artifact + local-only / NOT GIT;
- register `CMP-FRAME-YOUE-001_MASTER` as Stage1 approved Master #19;
- bind all 4 由额 V008/CURRENT rows to the approved Master;
- Registry Excel Sync;
- latest-head final Master V2 regression.

Target progress after binding:
- Stage1 approved Masters = **19/28 = 67.9%**
- Master-covered Registry records = **147**
- 由额 bindings = **4/4**

Not authorized:
- PR #31 Ready/merge;
- T-035 closure;
- next component;
- Stage2;
- T-018 resume.
"""
    TASK.write_text(t, encoding="utf-8")

# Final local assertions before commit.
cat = json.loads(CATALOG.read_text(encoding="utf-8"))
assert cat["approved_master_count"] == 19
assert len([x for x in cat["new_masters"] if x.get("master_id") == "CMP-FRAME-YOUE-001_MASTER"]) == 1
for path in (CURRENT, V008):
    r = json.loads(path.read_text(encoding="utf-8"))
    rows = [x for x in r["items"] if x.get("component") == "由额"]
    assert len(rows) == 4
    assert all(x.get("master_coverage_status") == "APPROVED_MASTER_AVAILABLE" for x in rows)
    assert all(x.get("master_reference") == "CMP-FRAME-YOUE-001_MASTER" for x in rows)
    p = r["stage1_master_progress_summary"]
    assert p["approved_master_count"] == 19
    assert p["pending_master_object_type_count"] == 9
    assert p["master_completion_percent"] == 67.9
    assert p["master_covered_registry_record_count"] == 147
    assert len(p["approved_master_components"]) == 19
    assert "由额" in p["approved_master_components"]
print("T035_FORMALIZATION_BINDING_PASS")
