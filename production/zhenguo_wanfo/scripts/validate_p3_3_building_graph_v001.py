#!/usr/bin/env python3
"""Mechanically validate canonical T-017 assets and its five Hard Fails."""

from __future__ import annotations

import argparse
import copy
import json

from build_p3_3_building_graph_v001 import (
    AUTHORITATIVE_KEYS,
    MASTER_INPUTS,
    OUTPUTS,
    PATHS,
    ROOT,
    compile_assets,
    direct_identity_qualifications,
    digest,
    load,
    serialize,
    write,
)

HARD_FAILS = [
    "REFERENCE_LENGTH_LEAKS_INTO_BUILDING",
    "SILENT_HISTORICIZATION",
    "BAKED_MANUAL_BUILDING",
    "SILENT_BUILDING_OMISSION",
    "BROKEN_COMPONENT_IDENTITY",
]
CLASSIFICATIONS = {
    "AUTHORITATIVE_GENERATIVE",
    "ACCOUNTING_REFERENCE_ONLY",
    "COMPARISON_ONLY",
    "PROHIBITED_AS_GENERATIVE_INPUT",
}
PROHIBITED_TRANSFORM_KEYS = {"location_mm", "rotation_euler_rad", "scale", "world_transform"}
DISPOSITION_CONFLICT = "MASTER_SCOPE_DISPOSITION_CONFLICT"


def contains_key(value, forbidden):
    if isinstance(value, dict):
        return bool(set(value) & forbidden) or any(contains_key(item, forbidden) for item in value.values())
    if isinstance(value, list):
        return any(contains_key(item, forbidden) for item in value)
    return False


def check_baseline(baseline):
    failures = []
    if set(baseline.get("input_classifications", {})) != CLASSIFICATIONS:
        failures.append("INPUT_CLASSIFICATION_INCOMPLETE")
    inventory = baseline.get("inputs", [])
    by_path = {item.get("path"): item for item in inventory}
    required_paths = {
        str(PATHS[key].relative_to(ROOT)) for key in AUTHORITATIVE_KEYS
    } | {str(path.relative_to(ROOT)) for path in MASTER_INPUTS}
    authoritative_paths = {
        path for path, item in by_path.items() if "AUTHORITATIVE_GENERATIVE" in item.get("classifications", [])
    }
    if not required_paths <= authoritative_paths:
        failures.append("AUTHORITATIVE_INPUT_COVERAGE_INCOMPLETE")
    p2_path = str(PATHS["p2_manifest"].relative_to(ROOT))
    if not {"ACCOUNTING_REFERENCE_ONLY", "COMPARISON_ONLY"} <= set(by_path.get(p2_path, {}).get("classifications", [])):
        failures.append("P2_MANIFEST_ROLE_INVALID")
    prohibited_fields = {
        "instances[].transform.location_mm",
        "instances[].transform.rotation_euler_rad",
        "instances[].transform.scale",
    }
    prohibited = baseline.get("prohibited_inputs", [])
    if {item.get("field_path") for item in prohibited} != prohibited_fields or any(item.get("classification") != "PROHIBITED_AS_GENERATIVE_INPUT" for item in prohibited):
        failures.append("PROHIBITED_INPUT_DECLARATION_INCOMPLETE")
    for path, expected in baseline.get("protection_hashes", {}).items():
        file_path = ROOT / path
        if not file_path.is_file() or digest(file_path) != expected:
            failures.append("PROTECTED_INPUT_CHANGED")
            break
    return failures


def check_bindings(bindings, graph):
    failures = []
    node_ids = {node["node_id"] for node in graph.get("nodes", [])}
    allowed_relations = set(graph.get("foundational_relation_vocabulary", []))
    required_roles = {
        "柱网与主要空间关系",
        "设计模数与主要构件比例",
        "柱与屋架绝对Z控制",
        "斗栱拓扑骨架",
        "主体梁架",
        "屋架水平控制",
        "屋顶山面控制几何",
        "屋顶Z向控制几何",
    }
    seen_roles = set()
    for binding in bindings.get("bindings", []):
        targets = binding.get("binding_targets", {})
        seen_roles.add(binding.get("building_role"))
        if not targets.get("graph_node_ids") or not targets.get("rule_ids"):
            failures.append("PARAMETER_GRAPH_RULE_BINDING_INCOMPLETE")
            break
        if not set(targets["graph_node_ids"]) <= node_ids or not set(targets.get("relationship_types", [])) <= allowed_relations:
            failures.append("PARAMETER_BINDING_TARGET_INVALID")
            break
        required_provenance = ("classification", "source_layer", "time_layer", "production_use", "source_ids")
        if any(key not in binding for key in required_provenance):
            failures.append("PARAMETER_PROVENANCE_INCOMPLETE")
            break
    if not required_roles <= seen_roles:
        failures.append("BUILDING_ROLE_COVERAGE_INCOMPLETE")
    p3_2 = bindings.get("p3_2_validated_dependencies", [])
    if not {item.get("parameter_id") for item in p3_2} >= {"PM-005", "Z-006-RC-01"}:
        failures.append("P3_2_PARAMETER_TRACEABILITY_INCOMPLETE")
    return failures


def validate(docs: dict) -> list[str]:
    failures = []
    baseline, bindings, accounting, graph = (docs[name] for name in ("baseline", "bindings", "accounting", "graph"))
    failures.extend(check_baseline(baseline))
    failures.extend(check_bindings(bindings, graph))

    qualifications = direct_identity_qualifications(load(PATHS["p3_1_scope"]), load(PATHS["p3_1_identity"]))
    approved = {item["component_id"] for item in load(PATHS["masters"])["masters"]}
    allowed = {
        "DEFERRED_INSUFFICIENT_EVIDENCE": {"DEFERRED", "PROXY_ONLY", "UNKNOWN_BLOCKED"},
        "PROXY_ONLY": {"PROXY_ONLY", "UNKNOWN_BLOCKED"},
        "CONTROL_ONLY": {"CONTROL_ONLY"},
        "ENVELOPE_ONLY": {"ENVELOPE_ONLY"},
    }
    accounting_by_id = {item["legacy_instance_id"]: item for item in accounting.get("instances", [])}
    runtime_nodes = {node["legacy_instance_id"]: node for node in graph.get("nodes", []) if node.get("legacy_instance_id")}
    for legacy_id, item in accounting_by_id.items():
        component_id = item.get("component_id")
        qualification = qualifications.get(component_id)
        expected = allowed.get(qualification)
        if qualification == "MASTER_REQUIRED":
            expected = {"GENERATE_FROM_FORMAL_COMPONENT"} if component_id in approved else {"DEFERRED"}
        dispositions = {item.get("p3_3_disposition"), runtime_nodes.get(legacy_id, {}).get("p3_3_disposition")}
        if expected is None:
            if "GENERATE_FROM_FORMAL_COMPONENT" in dispositions:
                failures.append(DISPOSITION_CONFLICT)
        elif not dispositions <= expected:
            failures.append(DISPOSITION_CONFLICT)

    realization_paths = graph.get("building_realization_dimensions", [])
    if any(
        item.get("source_component_id") in {"CMP-FRAME-LOWER-SIX-CHUANFU-001", "CMP-FRAME-UPPER-SIX-CHUANFU-001"}
        and item.get("source_parameter") == "canonical_reference_length_mm"
        and item.get("value_mm") == 1000
        and item.get("use") in {"ACTUAL_FULL_LENGTH", "BUILDING_REALIZATION_LENGTH"}
        for item in realization_paths
    ):
        failures.append(HARD_FAILS[0])

    unsafe = {"PROXY_ONLY", "CONTROL_ONLY", "ENVELOPE_ONLY", "DEFERRED", "UNKNOWN_BLOCKED", "SEMANTIC_ONLY"}
    if any(node.get("p3_3_disposition") in unsafe and node.get("historical_claim") in {"CONFIRMED", "HISTORICAL_CONFIRMED"} for node in graph.get("nodes", [])):
        failures.append(HARD_FAILS[1])

    generation = graph.get("generation_contract", {})
    runtime_placements = [node.get("placement_rule", {}) for node in graph.get("nodes", [])]
    if generation.get("manual_baked_placement") or generation.get("p2_numeric_world_transforms") != "PROHIBITED" or contains_key(generation, PROHIBITED_TRANSFORM_KEYS) or any(contains_key(item, PROHIBITED_TRANSFORM_KEYS) for item in runtime_placements):
        failures.append(HARD_FAILS[2])

    source_count = len(load(PATHS["p2_manifest"])["instances"])
    ids = [item["legacy_instance_id"] for item in accounting.get("instances", [])]
    if len(ids) != source_count or len(set(ids)) != source_count or accounting.get("summary", {}).get("unexplained_omissions") != 0:
        failures.append(HARD_FAILS[3])

    registry_ids = {item["component_id"] for item in load(PATHS["registry"])["components"]}
    graph_ids = {node.get("legacy_instance_id") for node in graph.get("nodes", []) if node.get("legacy_instance_id")}
    if any(item["component_id"] not in registry_ids for item in accounting.get("instances", [])) or graph_ids != set(ids):
        failures.append(HARD_FAILS[4])

    allowed_relations = {item["relation_type"] for item in load(PATHS["relationships"])["relationship_types"]}
    if set(graph.get("foundational_relation_vocabulary", [])) != allowed_relations or any(relation["relation_type"] not in allowed_relations for relation in graph.get("relationships", [])):
        failures.append("RELATIONSHIP_VOCABULARY_VIOLATION")

    expected_summary = {"families_accounted": 11, "families_expected": 11, "variants_accounted": 40, "variants_expected": 40, "instances_accounted": 365, "instances_expected": 365, "unexplained_omissions": 0, "orphan_identities": 0}
    if accounting.get("summary") != expected_summary:
        failures.append("ACCOUNTING_SUMMARY_MISMATCH")

    boundaries = bindings.get("mandatory_boundaries", {})
    if boundaries.get("six_chuanfu_historical_full_length") is not None or boundaries.get("Z-006") != "UNKNOWN / null / DO_NOT_LOCK" or any(item.get("historical_claim_upgrade") for item in bindings.get("bindings", [])):
        failures.append("EVIDENCE_BOUNDARY_VIOLATION")

    organization_nodes = {node["node_id"] for node in graph.get("nodes", []) if node.get("organizational_level") in {"BUILDING", "ASSEMBLY"}}
    runtime_parents = {relation["target_node"] for relation in graph.get("relationships", []) if relation.get("source_node", "").startswith("P3_3:")}
    if "ORG-BUILDING" not in organization_nodes or not {"ORG-COLUMN-GRID", "ORG-BRACKET-SYSTEM", "ORG-FRAME-SYSTEM", "ORG-ROOF-SYSTEM"} <= organization_nodes or not runtime_parents <= organization_nodes or "BUILDING_ROOT" in runtime_parents:
        failures.append("BUILDING_ORGANIZATION_HIERARCHY_INVALID")
    p3_2_reuse = graph.get("p3_2_foundation_reuse", {})
    if set(p3_2_reuse.get("reused_assembly_units", [])) != {"AU-COLUMN-LUDOU-001", "AU-FRAME-TIER-001", "AU-COLUMN-GRID-001"}:
        failures.append("P3_2_TRACEABILITY_INCOMPLETE")
    return sorted(set(failures))


def mutate(docs, fixture):
    result = copy.deepcopy(docs)
    code = fixture["expected_hard_fail"]
    mutation = fixture["mutation"]
    if code == HARD_FAILS[0]:
        result["graph"].setdefault("building_realization_dimensions", []).append(mutation["injected_dimension"])
    elif code == HARD_FAILS[1]:
        node = next(node for node in result["graph"]["nodes"] if node.get("p3_3_disposition") in {"PROXY_ONLY", "CONTROL_ONLY", "ENVELOPE_ONLY", "UNKNOWN_BLOCKED"})
        node["historical_claim"] = mutation["historical_claim"]
    elif code == HARD_FAILS[2]:
        node = next(node for node in result["graph"]["nodes"] if node.get("organizational_level") == "RUNTIME")
        node["placement_rule"]["authoritative_p2_world_transform"] = mutation["injected_p2_transform"]
        node["placement_rule"]["source"] = mutation["source"]
    elif code == HARD_FAILS[3]:
        result["accounting"]["instances"].pop()
    elif code == HARD_FAILS[4]:
        result["accounting"]["instances"][0]["component_id"] = mutation["component_id"]
    return result


def fixture_results(docs):
    results = []
    fixture_dir = ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3"
    for path in sorted(fixture_dir.glob("*.json")):
        fixture = load(path)
        code = fixture["expected_hard_fail"]
        rejected = code in validate(mutate(docs, fixture))
        results.append({"hard_fail": code, "fixture": str(path.relative_to(ROOT)), "expected": "REJECT", "actual": "EXPECTED_REJECTION" if rejected else "UNEXPECTED_ACCEPTANCE"})
    return results


def build_report():
    docs = compile_assets()
    canonical = validate(docs)
    negative = fixture_results(docs)
    disposition_regression = copy.deepcopy(docs)
    for item in disposition_regression["accounting"]["instances"]:
        if item["component_id"] == "CMP-PURLIN-001":
            item["p3_3_disposition"] = "GENERATE_FROM_FORMAL_COMPONENT"
    for node in disposition_regression["graph"]["nodes"]:
        if node.get("component_id") == "CMP-PURLIN-001":
            node["p3_3_disposition"] = "GENERATE_FROM_FORMAL_COMPONENT"
    disposition_rejected = DISPOSITION_CONFLICT in validate(disposition_regression)
    purlins = [item for item in docs["accounting"]["instances"] if item["component_id"] == "CMP-PURLIN-001"]
    required_present = all(path.is_file() for path in OUTPUTS.values())
    required_readable = required_present and all(isinstance(load(path), dict) for path in OUTPUTS.values())
    stable = all(OUTPUTS[name].is_file() and load(OUTPUTS[name]) == value for name, value in docs.items()) and serialize(compile_assets()) == serialize(docs)
    protected = "PROTECTED_INPUT_CHANGED" not in check_baseline(docs["baseline"])
    checks = {
        "required_outputs": {"present": sum(path.is_file() for path in OUTPUTS.values()), "expected": 5, "machine_readable": required_readable, "status": "PASS" if required_readable else "FAIL"},
        "input_baseline": "PASS" if not check_baseline(docs["baseline"]) else "FAIL",
        "accounting": docs["accounting"]["summary"],
        "identity_orphan": "PASS" if not ({HARD_FAILS[3], HARD_FAILS[4]} & set(canonical)) else "FAIL",
        "relationship_types": "5/5 PASS" if "RELATIONSHIP_VOCABULARY_VIOLATION" not in canonical else "FAIL",
        "parameter_provenance_bindings": "PASS" if not set(check_bindings(docs["bindings"], docs["graph"])) else "FAIL",
        "building_organization": "PASS" if "BUILDING_ORGANIZATION_HIERARCHY_INVALID" not in canonical else "FAIL",
        "p3_2_traceability": "PASS" if "P3_2_TRACEABILITY_INCOMPLETE" not in canonical else "FAIL",
        "prohibited_transform_scan": {"authoritative_generation_usage_count": 0 if HARD_FAILS[2] not in canonical else 1, "status": "PASS" if HARD_FAILS[2] not in canonical else "FAIL"},
        "evidence_boundary": "PASS" if "EVIDENCE_BOUNDARY_VIOLATION" not in canonical and HARD_FAILS[0] not in canonical and HARD_FAILS[1] not in canonical else "FAIL",
        "cross_layer_disposition_consistency": {
            "conflict_count": canonical.count(DISPOSITION_CONFLICT),
            "status": "PASS" if DISPOSITION_CONFLICT not in canonical else "FAIL",
        },
        "purlin_correction": {
            "component_id": "CMP-PURLIN-001",
            "deferred": sum(item["p3_3_disposition"] == "DEFERRED" for item in purlins),
            "expected": 7,
            "status": "PASS" if len(purlins) == 7 and all(item["p3_3_disposition"] == "DEFERRED" for item in purlins) else "FAIL",
        },
        "disposition_regression": {
            "expected": "REJECT",
            "machine_error": DISPOSITION_CONFLICT,
            "actual": "EXPECTED_REJECTION" if disposition_rejected else "UNEXPECTED_ACCEPTANCE",
        },
        "deterministic_regeneration_stable_serialization": "PASS" if stable else "FAIL",
        "protected_inputs_unchanged": protected,
    }
    report_pass = (
        not canonical
        and len(negative) == 5
        and all(item["actual"] == "EXPECTED_REJECTION" for item in negative)
        and checks["required_outputs"]["status"] == "PASS"
        and checks["input_baseline"] == "PASS"
        and checks["identity_orphan"] == "PASS"
        and checks["relationship_types"] == "5/5 PASS"
        and checks["parameter_provenance_bindings"] == "PASS"
        and checks["building_organization"] == "PASS"
        and checks["p3_2_traceability"] == "PASS"
        and checks["prohibited_transform_scan"]["status"] == "PASS"
        and checks["evidence_boundary"] == "PASS"
        and checks["cross_layer_disposition_consistency"]["status"] == "PASS"
        and checks["purlin_correction"]["status"] == "PASS"
        and disposition_rejected
        and checks["deterministic_regeneration_stable_serialization"] == "PASS"
        and checks["protected_inputs_unchanged"] is True
        and docs["accounting"]["summary"] == {
            "families_accounted": 11,
            "families_expected": 11,
            "variants_accounted": 40,
            "variants_expected": 40,
            "instances_accounted": 365,
            "instances_expected": 365,
            "unexplained_omissions": 0,
            "orphan_identities": 0,
        }
    )
    return {"version": "V001", "task": "T-017", "status": "PASS" if report_pass else "FAIL", "validations": checks, "canonical_hard_fail_count": len(set(canonical) & set(HARD_FAILS)), "canonical_failures": canonical, "negative_fixtures": negative, "blender_invocations": 0, "blend_files_created": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        write(OUTPUTS["validation"], report)
        report = build_report()
        write(OUTPUTS["validation"], report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
