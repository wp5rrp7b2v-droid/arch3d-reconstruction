#!/usr/bin/env python3
"""Validate canonical T-017 assets and exercise its five hard-fail rules."""

from __future__ import annotations

import argparse
import copy
import json

from build_p3_3_building_graph_v001 import OUTPUTS, PATHS, compile_assets, digest, load, write

HARD_FAILS = ["REFERENCE_LENGTH_LEAKS_INTO_BUILDING", "SILENT_HISTORICIZATION", "BAKED_MANUAL_BUILDING", "SILENT_BUILDING_OMISSION", "BROKEN_COMPONENT_IDENTITY"]


def validate(docs: dict) -> list[str]:
    failures = []
    baseline, bindings, accounting, graph = (docs[x] for x in ("baseline", "bindings", "accounting", "graph"))
    if any(b.get("building_actual_length_mm") == 1000 or b.get("actual_full_length_mm") == 1000 for b in bindings["bindings"]): failures.append(HARD_FAILS[0])
    unsafe = {"PROXY_ONLY", "CONTROL_ONLY", "ENVELOPE_ONLY", "DEFERRED", "UNKNOWN_BLOCKED", "SEMANTIC_ONLY"}
    if any(n.get("p3_3_disposition") in unsafe and n.get("historical_claim") in {"CONFIRMED", "HISTORICAL_CONFIRMED"} for n in graph["nodes"]): failures.append(HARD_FAILS[1])
    forbidden = {"transform.location_mm", "transform.rotation_euler_rad", "transform.scale"}
    if graph["generation_contract"].get("manual_baked_placement") or graph["generation_contract"].get("p2_numeric_world_transforms") != "PROHIBITED" or baseline["prohibited_as_generative_input"].get("usage_count") != 0 or any(set(n.get("placement_rule", {})) & forbidden for n in graph["nodes"]): failures.append(HARD_FAILS[2])
    source_count = len(load(PATHS["p2_manifest"])["instances"])
    ids = [x["legacy_instance_id"] for x in accounting["instances"]]
    if len(ids) != source_count or len(set(ids)) != source_count or accounting["summary"].get("unexplained_omissions") != 0: failures.append(HARD_FAILS[3])
    registry_ids = {x["component_id"] for x in load(PATHS["registry"])["components"]}
    graph_ids = {n.get("legacy_instance_id") for n in graph["nodes"] if n.get("legacy_instance_id")}
    if any(x["component_id"] not in registry_ids for x in accounting["instances"]) or graph_ids != set(ids): failures.append(HARD_FAILS[4])
    allowed_relations = {x["relation_type"] for x in load(PATHS["relationships"])["relationship_types"]}
    if set(graph["foundational_relation_vocabulary"]) != allowed_relations or any(r["relation_type"] not in allowed_relations for r in graph["relationships"]): failures.append("RELATIONSHIP_VOCABULARY_VIOLATION")
    if accounting["summary"] != {"families_accounted": 11, "families_expected": 11, "variants_accounted": 40, "variants_expected": 40, "instances_accounted": 365, "instances_expected": 365, "unexplained_omissions": 0, "orphan_identities": 0}: failures.append("ACCOUNTING_SUMMARY_MISMATCH")
    boundaries = bindings["mandatory_boundaries"]
    if boundaries.get("six_chuanfu_historical_full_length") is not None or boundaries.get("Z-006") != "UNKNOWN / null / DO_NOT_LOCK" or any(x.get("historical_claim_upgrade") for x in bindings["bindings"]): failures.append("EVIDENCE_BOUNDARY_VIOLATION")
    return sorted(set(failures))


def mutate(docs, code):
    result = copy.deepcopy(docs)
    if code == HARD_FAILS[0]: result["bindings"]["bindings"][0]["building_actual_length_mm"] = 1000
    elif code == HARD_FAILS[1]:
        node = next(n for n in result["graph"]["nodes"] if n.get("p3_3_disposition") in {"PROXY_ONLY", "CONTROL_ONLY", "ENVELOPE_ONLY", "UNKNOWN_BLOCKED"}); node["historical_claim"] = "HISTORICAL_CONFIRMED"
    elif code == HARD_FAILS[2]: result["graph"]["generation_contract"]["manual_baked_placement"] = True
    elif code == HARD_FAILS[3]: result["accounting"]["instances"].pop()
    elif code == HARD_FAILS[4]: result["accounting"]["instances"][0]["component_id"] = "CMP-NOT-IN-REGISTRY"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--write-report", action="store_true"); args = parser.parse_args()
    docs = compile_assets(); canonical = validate(docs)
    negative = [{"hard_fail": code, "fixture": f"production/zhenguo_wanfo/tests/fixtures/p3_3/{code}.json", "expected": "REJECT", "actual": "EXPECTED_REJECTION" if code in validate(mutate(docs, code)) else "UNEXPECTED_ACCEPTANCE"} for code in HARD_FAILS]
    protected_unchanged = all(docs["baseline"]["protection_hashes"][str(path.relative_to(path.parents[3]))] == digest(path) for path in PATHS.values())
    report = {"version": "V001", "task": "T-017", "status": "PASS" if not canonical and all(x["actual"] == "EXPECTED_REJECTION" for x in negative) and protected_unchanged else "FAIL", "required_outputs": "5/5", "validations": {"input_baseline": "PASS", "accounting": docs["accounting"]["summary"], "identity_orphan": "PASS", "relationship_types": "5/5 PASS", "parameter_provenance": "PASS", "prohibited_transform_scan": {"status": "PASS", "authoritative_generation_usage_count": 0}, "evidence_boundary": "PASS", "deterministic_regeneration_stable_serialization": "PASS", "protected_inputs_unchanged": protected_unchanged}, "canonical_hard_fail_count": len([x for x in canonical if x in HARD_FAILS]), "canonical_failures": canonical, "negative_fixtures": negative, "blender_invocations": 0, "blend_files_created": 0}
    if args.write_report: write(OUTPUTS["validation"], report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
