"""T-011 end-to-end validation, including mutation, rebuild and independent reopen.

Run outside the restricted macOS GPU sandbox with Python 3 and Blender 3.6.23.
"""

import copy
import hashlib
import json
import math
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
PARAMS = HERE / "CMP-COLUMN-001_MASTER_PARAMS_V001.json"
GENERATOR = HERE / "build_column_master_v001.py"
INSPECTOR = HERE / "inspect_column_master_v001.py"
ASSET = HERE / "asset/CMP-COLUMN-001_MASTER_V001.blend"
SEMANTIC = HERE / "CMP-COLUMN-001_MASTER_SEMANTIC_V001.json"
REVIEW = ROOT / "production/zhenguo_wanfo/review/P3_1/masters/CMP-COLUMN-001"
REVIEW_METADATA = REVIEW / "REVIEW_PACKAGE_V001.json"
REGISTRY = ROOT / "production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json"
VALIDATION = ROOT / "production/zhenguo_wanfo/validation/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json"
BASELINE = Path("/tmp/t011_p2_initial_hashes.json")
P2_PARAMS = ROOT / "production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
P2_OVERRIDE = ROOT / "production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json"
CONTRACT = ROOT / "production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V001.json"
IDENTITY = ROOT / "production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json"


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(ROOT))


def run_blender(command, marker):
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode or marker not in result.stdout or "Traceback" in result.stdout:
        raise RuntimeError(f"Blender operation failed: {marker}\n{result.stdout[-4000:]}")
    return result.stdout


def build(params, asset, semantic):
    return run_blender([
        str(BLENDER), "--background", "--python", str(GENERATOR), "--",
        "--params", str(params), "--asset", str(asset), "--semantic", str(semantic),
    ], "COLUMN_MASTER_BUILD_OK")


def check(condition, name, checks):
    checks[name] = "PASS" if condition else "FAIL"
    if not condition:
        raise AssertionError(name)


def main():
    data = read(PARAMS)
    p = {item["key"]: item for item in data["parameters"]}
    contract = read(CONTRACT)
    identity = read(IDENTITY)
    original = read(SEMANTIC)
    p2 = read(P2_PARAMS)["parameters"]
    override = read(P2_OVERRIDE)["overrides"]["Z-006-RC-01"]
    checks = {}
    check(data["component_id"] == "CMP-COLUMN-001" and data["master_id"] == "CMP-COLUMN-001_MASTER" and identity["records"][[r["candidate_id"] for r in identity["records"]].index("CMP-COLUMN-001")]["eligibility_status"] == "MASTER_REQUIRED", "unique_component_master_identity", checks)
    required = {"component_id", "master_version", "unit", "coordinate_convention", "origin_convention", "parameters", "geometry_mode", "known_unknowns", "interpretation_boundary", "historical_state", "originality_status", "reuse_scope", "variant_axes", "placement_only_attributes", "generator_path", "canonical_asset_path", "review_asset_paths"}
    common_fields = {"key", "value", "unit", "classification", "time_layer", "source_layer", "production_use", "source_ids", "replaceable"}
    check(required <= data.keys() and all(common_fields <= item.keys() for item in data["parameters"]), "required_asset_contract_fields", checks)
    column_contract = next(c for c in contract["master_components"] if c["component_id"] == "CMP-COLUMN-001")
    check(data["unit"] == "mm" and data["coordinate_convention"]["handedness"] == "right_handed" and column_contract["origin"] == "bottom_face_center", "unit_axes_origin_contract", checks)
    check(data["geometry_mode"] == column_contract["geometry_mode"] and data["geometry_lod"] == contract["global_convention"]["geometry_lod"], "geometry_mode_lod_contract", checks)
    check(p["diameter_source_mode"]["value"] == "OBSERVED_Z001" and p["height_source_mode"]["value"] == "RC_Z006_RC_01", "canonical_source_modes", checks)
    check(math.isclose(p["diameter_mm"]["value"], p2["Z-001"]["value"]) and p["diameter_mm"]["classification"] == p2["Z-001"]["classification"], "observed_diameter_reference", checks)
    check(p["historical_height_Z006_mm"]["value"] is None and p["historical_height_Z006_mm"]["classification"] == "UNKNOWN" and p["historical_height_Z006_mm"]["production_use"] == "DO_NOT_LOCK" and p2["Z-006"]["value"] is None, "z006_unknown_null_do_not_lock", checks)
    check(override["approval_decision_id"] == "D-023" and override["is_replaceable"] is True and override["formula"] == "11 * MOD-006" and p["height_mm"]["classification"] == "REASONABLE_COMPLETION" and math.isclose(p["height_mm"]["value"], override["multiplier"] * p2["MOD-006"]["value"], abs_tol=1e-6), "rc01_separate_replaceable_candidate", checks)
    check(p2["HIS-002"]["value"] is None and data["originality_status"] == "unknown", "his002_originality_unknown", checks)
    check(data["unsupported_geometry"] == [] and original["body"]["unsupported_column_geometry_count"] == 0, "unsupported_column_geometry_zero", checks)
    code = GENERATOR.read_text()
    forbidden = [str(p["diameter_mm"]["value"]), str(p["height_mm"]["value"]), str(p2["MOD-006"]["value"])]
    check(not any(re.search(r"(?<![\d.])" + re.escape(x) + r"(?![\d.])", code) for x in forbidden), "naked_historical_constant_scan", checks)
    check(not any(key in original for key in ("world_position", "grid_position", "bay_index", "instance_rotation")) and data["canonical_transform"] == contract["global_convention"]["canonical_transform"], "no_world_placement_leakage", checks)
    check(ASSET.exists() and original["canonical_blend_sha256"] == digest(ASSET), "canonical_binary_hash", checks)
    body = original["body"]
    dims = body["local_bbox_mm"]["dimensions"]
    check(body["local_transform"] == {"location": [0.0] * 3, "rotation": [0.0] * 3, "scale": [1.0] * 3} and original["object_count"] == 1 and original["mesh_count"] == 1, "transform_object_count", checks)
    check(all(math.isclose(dims[i], expected, abs_tol=0.001) for i, expected in enumerate((p["diameter_mm"]["value"], p["diameter_mm"]["value"], p["height_mm"]["value"]))) and body["local_bbox_mm"]["min"][2] == 0, "bounding_box_matches_parameters", checks)
    with tempfile.TemporaryDirectory(prefix="t011_column_") as temp:
        work = Path(temp)
        alternate_asset = work / "regeneration.blend"
        alternate_semantic = work / "regeneration.json"
        build(PARAMS, alternate_asset, alternate_semantic)
        alternate = read(alternate_semantic)
        stable = ("semantic_geometry_signature", "resolved_parameters", "evidence_classes", "geometry_mode", "known_unknowns", "body", "object_names", "collection_names", "unit")
        check(all(original[key] == alternate[key] for key in stable), "deterministic_semantic_regeneration", checks)
        mutated = copy.deepcopy(data)
        mp = {item["key"]: item for item in mutated["parameters"]}
        mp["height_mm"]["value"] = p["height_mm"]["value"] + 100.0
        mp["height_mm"]["classification"] = "ENGINEERING_TEST_ONLY"
        mp["height_mm"]["time_layer"] = "engineering_test"
        mp["height_mm"]["source_layer"] = "SYNTHETIC"
        mp["height_mm"]["production_use"] = "MUTATION_TEST_ONLY"
        mp["height_mm"]["source_ids"] = ["T-011-SYNTHETIC-MUTATION"]
        mp["height_source_mode"]["value"] = "ENGINEERING_TEST_ONLY"
        mp["height_source_mode"]["classification"] = "ENGINEERING_TEST_ONLY"
        mp["height_source_mode"]["time_layer"] = "engineering_test"
        mp["height_source_mode"]["source_layer"] = "SYNTHETIC"
        mp["height_source_mode"]["production_use"] = "MUTATION_TEST_ONLY"
        mp["height_source_mode"]["source_ids"] = ["T-011-SYNTHETIC-MUTATION"]
        mutation_params = work / "synthetic_params.json"
        mutation_asset = work / "synthetic.blend"
        mutation_semantic = work / "synthetic.json"
        write(mutation_params, mutated)
        canonical_hash_before_mutation = digest(ASSET)
        build(mutation_params, mutation_asset, mutation_semantic)
        mutation = read(mutation_semantic)
        check(mutation["semantic_geometry_signature"] != original["semantic_geometry_signature"] and math.isclose(mutation["body"]["local_bbox_mm"]["dimensions"][2] - dims[2], 100.0, abs_tol=0.001) and mutation["body"]["local_bbox_mm"]["dimensions"][:2] == dims[:2] and digest(ASSET) == canonical_hash_before_mutation and digest(PARAMS) == original["input_hashes"][rel(PARAMS)], "synthetic_mutation_isolated", checks)
        build(PARAMS, ASSET, SEMANTIC)
        rebuilt = read(SEMANTIC)
        check(all(original[key] == rebuilt[key] for key in stable) and rebuilt["canonical_blend_sha256"] == digest(ASSET), "canonical_rebuild_after_mutation", checks)
        reopened_path = work / "reopen.json"
        run_blender([str(BLENDER), "--background", str(ASSET), "--python", str(INSPECTOR), "--", "--expected", str(SEMANTIC), "--output", str(reopened_path)], "COLUMN_MASTER_REOPEN_OK")
        reopen = read(reopened_path)
        check(reopen["status"] == "PASS" and reopen["semantic_geometry_signature"] == rebuilt["semantic_geometry_signature"], "independent_reopen", checks)
        mutation_evidence = {
            "status": "PASS",
            "classification": "ENGINEERING_TEST_ONLY",
            "changed_parameter": "height_mm",
            "baseline_height_mm": p["height_mm"]["value"],
            "synthetic_height_mm": mp["height_mm"]["value"],
            "baseline_bbox_mm": dims,
            "synthetic_bbox_mm": mutation["body"]["local_bbox_mm"]["dimensions"],
            "baseline_signature": original["semantic_geometry_signature"],
            "synthetic_signature": mutation["semantic_geometry_signature"],
            "canonical_file_unchanged_during_mutation": True,
            "canonical_rebuild_restored": True,
            "not_a_historical_variant": True,
        }
    names = ["FRONT", "SIDE", "TOP", "AXON", "DIMENSION_PARAMETER_SUMMARY", "EVIDENCE_UNCERTAINTY_SUMMARY"]
    images = []
    for name in names:
        path = REVIEW / (name + ".png")
        with Image.open(path) as im:
            im.verify()
        images.append({"view": name, "path": rel(path), "sha256": digest(path)})
    check(len(images) == 6 and len({x["path"] for x in images}) == 6, "six_review_images", checks)
    write(REVIEW_METADATA, {
        "component_id": data["component_id"], "master_version": "V001",
        "status": "ENGINEERING_REVIEW_READY", "geometry_color": "neutral_grey",
        "orthographic_views": ["FRONT", "SIDE", "TOP", "AXON"],
        "render_source": "Blender 3.6.23 canonical parameter realization; temporary review-only camera/materials are not saved in the Master",
        "images": images,
        "interpretation_boundary": data["interpretation_boundary"],
    })
    registry = {
        "version": "V001", "phase": "P3.1", "task": "T-011", "status": "PILOT_ENGINEERING_COMPLETE_PENDING_PRODUCT_OWNER_REVIEW",
        "base_registry_path": "production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_V001.json",
        "masters": [{
            "component_id": data["component_id"], "master_id": data["master_id"], "master_version": data["master_version"],
            "canonical_asset_status": "LOCAL_ONLY_GENERATED", "canonical_asset_sha256": digest(ASSET),
            "generator_path": rel(GENERATOR), "parameter_path": rel(PARAMS), "semantic_snapshot_path": rel(SEMANTIC),
            "local_binary_path": rel(ASSET), "review_path": rel(REVIEW), "review_metadata_path": rel(REVIEW_METADATA),
            "geometry_mode": data["geometry_mode"], "reuse_scope": data["reuse_scope"],
            "evidence_references": data["evidence_references"], "originality_status": data["originality_status"],
            "known_unknowns": data["known_unknowns"], "variant_ids": [],
            "validation_status": "T011_ENGINEERING_PASS", "approval_status": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
        }],
    }
    write(REGISTRY, registry)
    entry = read(REGISTRY)["masters"][0]
    check(len(read(REGISTRY)["masters"]) == 1 and entry["component_id"] == "CMP-COLUMN-001" and entry["variant_ids"] == [] and all((ROOT / entry[key]).exists() for key in ("generator_path", "parameter_path", "semantic_snapshot_path", "local_binary_path", "review_metadata_path")), "registry_single_master_no_orphan", checks)
    # The first execution uses the pre-build local hash capture. Later audits can
    # reuse the committed before-hashes; this also detects a changed local P2 binary.
    before = read(BASELINE) if BASELINE.exists() else read(VALIDATION)["p2_frozen_baseline_sha256_before"]
    after = {path: digest(ROOT / path) for path in before}
    check(after == before, "p2_frozen_baseline_unchanged", checks)
    report = {
        "task": "T-011", "component_id": "CMP-COLUMN-001", "master_version": "V001", "status": "PASS",
        "blender_version": rebuilt["blender_version"], "canonical_blend_path": rel(ASSET),
        "canonical_blend_sha256": digest(ASSET), "semantic_snapshot_path": rel(SEMANTIC),
        "semantic_geometry_signature": rebuilt["semantic_geometry_signature"],
        "checks": checks, "check_count": len(checks), "review_count": len(images),
        "mutation_evidence": mutation_evidence, "independent_reopen_evidence": reopen,
        "p2_frozen_baseline_sha256_before": before, "p2_frozen_baseline_sha256_after": after,
        "requires_project_control_review": [], "unexplained_validation_errors": [],
        "approval_boundary": "T-011 engineering PASS only; Product Owner visual/Pilot approval and P3.1 gate remain pending.",
    }
    write(VALIDATION, report)
    print("T011_VALIDATION_PASS", len(checks), "checks", digest(ASSET))


if __name__ == "__main__":
    main()
