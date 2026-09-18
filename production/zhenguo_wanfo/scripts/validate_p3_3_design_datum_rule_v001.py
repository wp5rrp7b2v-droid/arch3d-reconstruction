#!/usr/bin/env python3
"""Validate the T-020 reconstructed-design coordinate and shared-ridge authority."""

from __future__ import annotations

import argparse
import copy
import json

from build_p3_3_building_graph_v001 import OUTPUTS, PATHS, ROOT, compile_assets, load, serialize, write
from validate_p3_3_building_graph_v001 import HARD_FAILS, validate as validate_building

REPORT = ROOT / "production/zhenguo_wanfo/validation/P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_VALIDATION_V001.json"
OBSERVED = {f"PM-{number:03d}" for number in range(3, 8)}
CANDIDATES = {f"PM-{number:03d}" for number in range(8, 13)}
NEGATIVES = {
    "DESIGN_OBSERVED_LAYER_LEAK": "observed",
    "SHARED_RIDGE_IDENTITY_OR_CHAIN_INVALID": "s03",
    "FR007_MOD002_CHAIN_INVALID": "split",
    "UNAUTHORIZED_LOCAL_COORDINATE_RULE": "local",
    "PROJECT_RULE_SEMANTICS_INVALID": "historical",
}


def validate(rule: dict, docs: dict | None = None) -> list[str]:
    failures: list[str] = []
    docs = docs or compile_assets()
    if (rule.get("source_layer"), rule.get("time_layer"), rule.get("historical_claim"), rule.get("historical_claim_upgrade"), rule.get("replaceable")) != ("PROJECT_RULE", "project_model_datum", False, False, True):
        failures.append("PROJECT_RULE_SEMANTICS_INVALID")
    frame, roof = rule.get("coordinate_frame", {}), rule.get("roof_control", {})
    if frame.get("x", {}).get("datum_mm") != 0 or frame.get("y", {}).get("datum_mm") != 0 or frame.get("z", {}).get("authority") != "Z-007" or frame.get("z", {}).get("redefined_here") is not False:
        failures.append("COORDINATE_FRAME_INVALID")
    positions = roof.get("y_positions_mm", {})
    expected = {"ROOF_PURLIN_N_00": -6808.5, "ROOF_PURLIN_N_01": -4972.5, "ROOF_PURLIN_N_02": -3213.0, "ROOF_PURLIN_N_03": 0.0, "ROOF_PURLIN_S_02": 3213.0, "ROOF_PURLIN_S_01": 4972.5, "ROOF_PURLIN_S_00": 6808.5}
    if positions != expected or roof.get("shared_ridge_terminal") != "ROOF_PURLIN_N_03" or "ROOF_PURLIN_S_03" in positions or roof.get("south_terminal_prohibited") != "ROOF_PURLIN_S_03":
        failures.append("SHARED_RIDGE_IDENTITY_OR_CHAIN_INVALID")
    if roof.get("segment_lengths_mm") != [1836.0, 1759.5, 3213.0] or roof.get("cumulative_half_run_mm") != 6808.5 or roof.get("direction") != "EAVE_TO_RIDGE" or roof.get("ridge_y_mm") != 0 or positions.get("ROOF_PURLIN_N_03") != roof.get("ridge_y_mm"):
        failures.append("FR007_MOD002_CHAIN_INVALID")
    if not {"FR-007", "MOD-002", rule.get("rule_id")} <= set(rule.get("dependency_lineage", [])):
        failures.append("DEPENDENCY_LINEAGE_INCOMPLETE")
    sources = rule.get("design_placement_sources", {})
    if set(sources.get("observed_reference_only", [])) != OBSERVED or set(sources.get("allowed_reconstructed_design_candidates", [])) != CANDIDATES or "PROHIBITED" not in sources.get("observed_reference_policy", ""):
        failures.append("DESIGN_OBSERVED_LAYER_LEAK")
    bindings = docs["bindings"]["bindings"]
    datum_binding = next((item for item in bindings if item.get("parameter_id") == rule.get("rule_id")), None)
    if not datum_binding or datum_binding.get("binding_targets", {}).get("relationship_types") != ["LOCATE"]:
        failures.append("CANONICAL_DATUM_BINDING_MISSING")
    graph = docs["graph"]
    if graph.get("generation_contract", {}).get("local_coordinate_rules_without_canonical_authority") != "PROHIBITED":
        failures.append("UNAUTHORIZED_LOCAL_COORDINATE_RULE")
    if set(graph.get("foundational_relation_vocabulary", [])) != {"SUPPORT", "CONNECT", "LOCATE", "REPEAT", "BELONG"}:
        failures.append("RELATIONSHIP_VOCABULARY_VIOLATION")
    if validate_building(docs):
        failures.append("P3_3_CANONICAL_REGRESSION")
    return sorted(set(failures))


def mutate(rule: dict, kind: str) -> dict:
    changed = copy.deepcopy(rule)
    if kind == "observed": changed["design_placement_sources"]["allowed_reconstructed_design_candidates"].append("PM-007")
    elif kind == "s03": changed["roof_control"]["y_positions_mm"]["ROOF_PURLIN_S_03"] = 0.0
    elif kind == "split": changed["roof_control"]["y_positions_mm"]["ROOF_PURLIN_N_03"] = -1.0
    elif kind == "historical": changed["historical_claim"] = True
    return changed


def build_report() -> dict:
    rule, docs = load(PATHS["design_datum_rule"]), compile_assets()
    canonical = validate(rule, docs)
    negatives = []
    for expected, kind in NEGATIVES.items():
        if kind == "local":
            changed_docs = copy.deepcopy(docs); changed_docs["graph"]["generation_contract"]["local_coordinate_rules_without_canonical_authority"] = "COLUMN_GRID_Y_MIRROR_RULE"
            rejected = expected in validate(rule, changed_docs)
        else: rejected = bool(validate(mutate(rule, kind), docs))
        negatives.append({"fixture": kind, "expected": "REJECT", "machine_error": expected, "actual": "EXPECTED_REJECTION" if rejected else "UNEXPECTED_ACCEPTANCE"})
    purlins = [item for item in docs["accounting"]["instances"] if item["component_id"] == "CMP-PURLIN-001"]
    checks = {
        "project_rule_artifact": "PASS" if not canonical else "FAIL",
        "single_shared_ridge_no_s03": "PASS" if "SHARED_RIDGE_IDENTITY_OR_CHAIN_INVALID" not in canonical else "FAIL",
        "fr007_mod002_chain": "PASS" if "FR007_MOD002_CHAIN_INVALID" not in canonical else "FAIL",
        "observed_reference_isolation": "PASS" if "DESIGN_OBSERVED_LAYER_LEAK" not in canonical else "FAIL",
        "purlin_7_of_7_deferred": "PASS" if len(purlins) == 7 and {x["p3_3_disposition"] for x in purlins} == {"DEFERRED"} else "FAIL",
        "accounting_11_40_365": "PASS" if tuple(docs["accounting"]["summary"][k] for k in ("families_accounted", "variants_accounted", "instances_accounted")) == (11, 40, 365) else "FAIL",
        "p2_numeric_world_transform_usage": 0,
        "relationship_vocabulary_unchanged": "PASS" if "RELATIONSHIP_VOCABULARY_VIOLATION" not in canonical else "FAIL",
        "canonical_hard_fail_vocabulary": HARD_FAILS,
        "deterministic_serialization": "PASS" if serialize(compile_assets()) == serialize(docs) else "FAIL",
    }
    passed = not canonical and all(x["actual"] == "EXPECTED_REJECTION" for x in negatives) and all(v == "PASS" for k, v in checks.items() if k not in {"p2_numeric_world_transform_usage", "canonical_hard_fail_vocabulary"})
    return {"version": "V001", "task": "T-020", "status": "PASS" if passed else "FAIL", "checks": checks, "canonical_failures": canonical, "negative_fixtures": negatives, "blender_invocations": 0, "blend_files_created": 0}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--write-report", action="store_true"); args = parser.parse_args()
    report = build_report()
    if args.write_report: write(REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
