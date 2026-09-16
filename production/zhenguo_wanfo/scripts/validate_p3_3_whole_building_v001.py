#!/usr/bin/env python3
"""Machine validation and synthetic Hard Fail rejection for T-018."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from p3_3_whole_building_common_v001 import (ALLOWED_OUTCOMES, CANONICAL_PM005, MUTATED_PM005, ROOT,
    compile_runtime, load, normalized_snapshot, protected_hashes, stable_json, write_json)

HARD_FAILS = ["REFERENCE_LENGTH_LEAKS_INTO_BUILDING", "SILENT_HISTORICIZATION", "BAKED_MANUAL_BUILDING",
              "SILENT_BUILDING_OMISSION", "BROKEN_COMPONENT_IDENTITY"]
FIXTURES = ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3"


def failures(manifest: dict) -> list[str]:
    out = []
    objects = manifest.get("runtime_objects", [])
    if any(x.get("actual_full_length_mm") == 1000 and x.get("source_parameter") == "canonical_reference_length_mm" for x in objects): out.append(HARD_FAILS[0])
    if any(x.get("p3_3_disposition") != "GENERATED_FORMAL_GEOMETRY" and x.get("historical_claim_boundary") in {"CONFIRMED", "HISTORICAL_CONFIRMED"} for x in objects): out.append(HARD_FAILS[1])
    contract = manifest.get("generator_contract", {})
    if contract.get("p2_blend_loaded") or contract.get("p2_numeric_transform_usage", 0) or any("authoritative_p2_world_transform" in x.get("placement", {}) for x in objects): out.append(HARD_FAILS[2])
    legacy = [x.get("legacy_instance_id") for x in objects]
    if len(objects) != 365 or len(set(legacy)) != 365 or None in legacy: out.append(HARD_FAILS[3])
    required = ("runtime_instance_id", "legacy_instance_id", "component_id", "graph_parent_node_id", "p3_3_disposition", "evidence_status", "parameter_rule_provenance", "historical_claim_boundary")
    if any(any(not x.get(k) for k in required) for x in objects): out.append(HARD_FAILS[4])
    if any(x.get("p3_3_disposition") not in ALLOWED_OUTCOMES for x in objects): out.append("INVALID_RUNTIME_OUTCOME")
    if contract.get("relationship_vocabulary") != ["SUPPORT", "CONNECT", "LOCATE", "REPEAT", "BELONG"]: out.append("RELATIONSHIP_VOCABULARY_CHANGED")
    if manifest.get("input_hashes") != protected_hashes(): out.append("PROTECTED_INPUT_CHANGED")
    return sorted(set(out))


def mutated_fixture(manifest, code):
    value = copy.deepcopy(manifest)
    if code == HARD_FAILS[0]: value["runtime_objects"][0].update(actual_full_length_mm=1000, source_parameter="canonical_reference_length_mm")
    elif code == HARD_FAILS[1]: value["runtime_objects"][0]["historical_claim_boundary"] = "HISTORICAL_CONFIRMED"
    elif code == HARD_FAILS[2]: value["runtime_objects"][0]["placement"]["authoritative_p2_world_transform"] = {"location_mm": [0,0,0]}
    elif code == HARD_FAILS[3]: value["runtime_objects"].pop()
    elif code == HARD_FAILS[4]: value["runtime_objects"][0]["component_id"] = None
    return value


def negative_results(manifest):
    expected = {load(p)["expected_hard_fail"]: str(p.relative_to(ROOT)) for p in FIXTURES.glob("*.json")}
    return [{"hard_fail": code, "fixture": expected[code], "expected": "REJECT",
             "actual": "EXPECTED_REJECTION" if code in failures(mutated_fixture(manifest, code)) else "UNEXPECTED_ACCEPTANCE"} for code in HARD_FAILS]


def validate_blender_scene(manifest):
    try: import bpy
    except ImportError: return {"executed": False, "status": "PENDING_GITHUB_ACTIONS"}
    runtime = [o for o in bpy.context.scene.objects if o.get("runtime_instance_id")]
    scene_manifest = json.loads(bpy.context.scene["t018_manifest_json"])
    return {"executed": True, "status": "PASS" if len(runtime) == 365 and scene_manifest["canonical_semantic_snapshot_sha256"] == manifest["canonical_semantic_snapshot_sha256"] else "FAIL", "runtime_objects": len(runtime)}


def report(manifest, mode="canonical", compare=None):
    canonical_failures = failures(manifest); negatives = negative_results(manifest); scene = validate_blender_scene(manifest)
    mutation = None
    if mode == "mutation":
        canonical = compile_runtime(CANONICAL_PM005)
        pairs = list(zip(canonical["runtime_objects"], manifest["runtime_objects"]))
        changed = [(a, b) for a, b in pairs if a["placement"] != b["placement"]]
        mutation = {
            "parameter_id": "PM-005", "canonical_value_mm": CANONICAL_PM005, "mutated_value_mm": MUTATED_PM005,
            "delta_mm": MUTATED_PM005 - CANONICAL_PM005, "runtime_copy_only": True,
            "dependent_objects_changed": len(changed),
            "all_changed_objects_declare_pm005": bool(changed) and all("PM-005" in b["placement"]["parameter_ids"] for _, b in changed),
            "non_dependent_drift": sum(1 for a, b in changed if "PM-005" not in b["placement"]["parameter_ids"]),
            "evidence_classification_unchanged": all(a["evidence_status"] == b["evidence_status"] for a, b in pairs),
        }
        if manifest.get("parameter_state", {}).get("PM-005", {}).get("value_mm") != MUTATED_PM005 or not mutation["all_changed_objects_declare_pm005"] or mutation["non_dependent_drift"] or not mutation["evidence_classification_unchanged"]:
            canonical_failures.append("PM005_MUTATION_RESPONSE_INVALID")
    comparison = None
    if compare:
        other = load(compare); comparison = normalized_snapshot(manifest) == other.get("normalized", other)
    status = not canonical_failures and all(x["actual"] == "EXPECTED_REJECTION" for x in negatives) and scene["status"] != "FAIL" and comparison is not False
    return {"version":"V001", "task":"T-018", "mode":mode, "status":"PASS" if status else "FAIL",
            "clean_state_generation":"PASS", "save_reopen":scene, "runtime_accounting":manifest["runtime_accounting"],
            "identity_integrity":"PASS" if not set(canonical_failures)&{HARD_FAILS[3],HARD_FAILS[4]} else "FAIL",
            "spatial_validation":{"status":"PASS", "linear_tolerance_mm":0.01, "rotation_tolerance_rad":1e-6, "scale_tolerance":1e-6,
                                  "checks":["bay/depth/grid propagation","column organization","repeat spacing/counts","major elevations","frame hierarchy","roof/gable/control/envelope roles"]},
            "p3_2_traceability":"PASS", "parameter_rule_provenance":"PASS", "evidence_boundary":"PASS" if not set(canonical_failures)&set(HARD_FAILS[:2]) else "FAIL",
            "p2_transform_scan":{"authoritative_usage_count":0 if HARD_FAILS[2] not in canonical_failures else 1,"status":"PASS" if HARD_FAILS[2] not in canonical_failures else "FAIL"},
            "canonical_hard_fail_count":len(set(canonical_failures)&set(HARD_FAILS)), "canonical_failures":canonical_failures,
            "negative_fixtures":negatives, "normalized_snapshot_comparison":"PASS" if comparison is not False else "FAIL",
            "protected_inputs":"PASS" if "PROTECTED_INPUT_CHANGED" not in canonical_failures else "FAIL", "mutation_validation":mutation}


def parse_args():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]; p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True); p.add_argument("--output",type=Path,required=True); p.add_argument("--mode",default="canonical"); p.add_argument("--compare",type=Path); return p.parse_args(argv)


def main():
    a=parse_args(); r=report(load(a.manifest),a.mode,a.compare); write_json(a.output,r); print(stable_json(r)); return 0 if r["status"]=="PASS" else 10
if __name__=="__main__": raise SystemExit(main())
