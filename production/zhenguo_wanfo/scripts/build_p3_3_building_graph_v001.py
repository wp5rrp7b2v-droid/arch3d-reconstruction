#!/usr/bin/env python3
"""Deterministically compile the T-017 building input, accounting and graph assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "production/zhenguo_wanfo/build"
P = ROOT / "production/zhenguo_wanfo"

PATHS = {
    "p2_manifest": BUILD / "P2_3_INTEGRATION_MANIFEST_V001.json",
    "registry": P / "registry/P3_0_COMPONENT_REGISTRY_V001.json",
    "migration": P / "registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json",
    "masters": P / "registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json",
    "assembly_schema": P / "assembly/P3_2_ASSEMBLY_SCHEMA_V001.json",
    "relationships": P / "assembly/P3_2_RELATIONSHIP_TYPES_V001.json",
    "parameters": P / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json",
    "overrides": P / "params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json",
    "dependency": P / "dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json",
}

OUTPUTS = {
    "baseline": BUILD / "P3_3_BUILDING_INPUT_BASELINE_V001.json",
    "bindings": BUILD / "P3_3_BUILDING_PARAMETER_BINDINGS_V001.json",
    "accounting": BUILD / "P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json",
    "graph": BUILD / "P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json",
    "validation": BUILD / "P3_3_BUILDING_GRAPH_VALIDATION_V001.json",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def disposition(role: str, ontology: str) -> str:
    if role == "CONTROL_OBJECT":
        return "CONTROL_ONLY"
    if role == "ENVELOPE_SURFACE":
        return "ENVELOPE_ONLY"
    if role == "GEOMETRIC_PROXY":
        return "UNKNOWN_BLOCKED" if ontology == "UNKNOWN_UNRESOLVED_COMPONENT" else "PROXY_ONLY"
    return "GENERATE_FROM_FORMAL_COMPONENT"


def compile_assets() -> dict:
    manifest, registry, migration = load(PATHS["p2_manifest"]), load(PATHS["registry"]), load(PATHS["migration"])
    parameters, overrides = load(PATHS["parameters"]), load(PATHS["overrides"])
    masters, relation_source = load(PATHS["masters"]), load(PATHS["relationships"])
    relation_types = [item["relation_type"] for item in relation_source["relationship_types"]]
    protected = {str(path.relative_to(ROOT)): digest(path) for path in PATHS.values()}

    baseline = {
        "version": "V001", "task": "T-017", "status": "CANONICAL",
        "inputs": [
            {"path": str(PATHS[k].relative_to(ROOT)), "role": "ACCOUNTING_REFERENCE_ONLY" if k in {"p2_manifest", "migration"} else "AUTHORITATIVE_GENERATIVE", "sha256": protected[str(PATHS[k].relative_to(ROOT))], "protection": "READ_ONLY", "allowed_fields": (["instance_id", "family_id", "variant_id", "evidence metadata", "parameter references", "counts"] if k == "p2_manifest" else ["ALL_EXCEPT_PROHIBITED_FIELDS"]), "prohibited_fields": (["instances[].transform.location_mm", "instances[].transform.rotation_euler_rad", "instances[].transform.scale"] if k == "p2_manifest" else [])}
            for k in PATHS
        ],
        "prohibited_as_generative_input": {"source": str(PATHS["p2_manifest"].relative_to(ROOT)), "fields": ["transform.location_mm", "transform.rotation_euler_rad", "transform.scale"], "usage_count": 0},
        "protection_hashes": protected,
    }

    bindings = []
    for pid, record in sorted(parameters["parameters"].items()):
        bindings.append({"parameter_id": pid, "parameter_key": record["parameter_key"], "value": record.get("value"), "unit": record.get("unit"), "classification": record["classification"], "source_layer": record["source_layer"], "time_layer": record["time_layer"], "production_use": record["production_use"], "replaceable": record["is_replaceable"], "source_ids": record["source_ids"], "building_role": "FORMAL_BUILDING_PARAMETER", "graph_dependency": "RUNTIME_RULE_WHEN_REFERENCED", "historical_claim_upgrade": False})
    for pid, record in sorted(overrides["overrides"].items()):
        bindings.append({"parameter_id": pid, "parameter_key": record["target_parameter_key"], "value": record["current_resolved_value"], "unit": record["unit"], "classification": record["classification"], "source_layer": "APPROVED_OVERRIDE", "time_layer": record["time_layer"], "production_use": record["production_use"], "replaceable": record["is_replaceable"], "source_ids": record["evidence_basis"] + [record["approval_decision_id"]], "building_role": "REPLACEABLE_BUILDING_RULE", "graph_dependency": {"formula": record["formula"], "depends_on": record["depends_on"]}, "historical_claim_boundary": record["historical_claim_boundary"], "historical_claim_upgrade": False})
    bindings_doc = {"version": "V001", "task": "T-017", "status": "CANONICAL", "bindings": bindings, "mandatory_boundaries": {"Z-006": "UNKNOWN / null / DO_NOT_LOCK", "Z-006-RC-01": "REASONABLE_COMPLETION / replaceable / D-023", "DG-114": "UNKNOWN / no unified small-dou historical specification claim", "HIS-002": "component originality unknown", "six_chuanfu_historical_full_length": None, "canonical_reference_length_mm_usage": "NON_HISTORICAL_ENGINEERING_REFERENCE_ONLY"}}

    components = {x["component_id"]: x for x in registry["components"]}
    migration_instances = {x["p2_instance_id"]: x for x in migration["instances"]}
    accounting = []
    for source in sorted(manifest["instances"], key=lambda x: x["instance_id"]):
        mapped = migration_instances[source["instance_id"]]
        component = components[mapped["p3_component_id"]]
        disp = disposition(component["current_asset_role"], component["ontology_type"])
        accounting.append({"legacy_instance_id": source["instance_id"], "source_family_id": source["family_id"], "source_variant_id": source["variant_id"], "component_id": component["component_id"], "semantic_class": component["ontology_type"], "asset_role": component["current_asset_role"], "p3_3_disposition": disp, "evidence_boundary": {"bounded_placeholder": source.get("bounded_placeholder", False), "originality_status": source.get("originality_status", "unknown"), "time_layer": source.get("time_layer"), "historical_claim": "NOT_UPGRADED"}, "graph_inclusion_status": "INCLUDED", "parameter_ids": source.get("parameter_ids", []), "provenance": [str(PATHS["p2_manifest"].relative_to(ROOT)), str(PATHS["migration"].relative_to(ROOT)), str(PATHS["registry"].relative_to(ROOT))], "explanation": "Explicitly retained under its registry-qualified identity; P2 numeric transform is not copied."})
    accounting_doc = {"version": "V001", "task": "T-017", "status": "CANONICAL", "summary": {"families_accounted": len({x["source_family_id"] for x in accounting}), "families_expected": 11, "variants_accounted": len({x["source_variant_id"] for x in accounting}), "variants_expected": 40, "instances_accounted": len(accounting), "instances_expected": 365, "unexplained_omissions": 0, "orphan_identities": 0}, "instances": accounting}

    approved = {m["component_id"]: {"master_id": m["master_id"], "approval_status": m["approval_status"]} for m in masters["masters"]}
    nodes = [{"node_id": "BUILDING_ROOT", "node_class": "ASSEMBLY_UNIT", "label": "万佛殿 building root", "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"}]
    for item in accounting:
        nodes.append({"node_id": "P3_3:" + item["legacy_instance_id"], "node_class": ({"CONTROL_OBJECT": "CONTROL", "ENVELOPE_SURFACE": "ENVELOPE", "GEOMETRIC_PROXY": "PROXY"}.get(item["asset_role"], "FORMAL_COMPONENT")), "component_id": item["component_id"], "legacy_instance_id": item["legacy_instance_id"], "master_qualification": approved.get(item["component_id"], "NOT_AN_APPROVED_P3_1_MASTER"), "parameter_refs": item["parameter_ids"], "placement_rule": {"source": "BUILDING_PARAMETERS_AND_P3_2_RELATIONSHIPS", "p2_numeric_transform_used": False, "status": "DEFERRED_OR_RULE_DRIVEN"}, "p3_3_disposition": item["p3_3_disposition"], "evidence_status": item["evidence_boundary"], "historical_claim": "NOT_UPGRADED"})
    relations = [{"relationship_id": f"BELONG-{i:04d}", "relation_type": "BELONG", "source_node": node["node_id"], "target_node": "BUILDING_ROOT", "provenance": "P3.2_FOUNDATION+T017_ACCOUNTING", "parameter_refs": [], "evidence_status": "ORGANIZATIONAL_ONLY", "replaceability": True} for i, node in enumerate(nodes[1:], 1)]
    graph = {"version": "V001", "task": "T-017", "status": "CANONICAL", "building_root": "BUILDING_ROOT", "foundational_relation_vocabulary": relation_types, "relationship_definition_source": str(PATHS["relationships"].relative_to(ROOT)), "nodes": nodes, "relationships": relations, "unresolved_relationships": [{"scope": "45-degree corner, mortise, hidden-angle beam and unevidenced connections", "status": "UNKNOWN_BLOCKED", "reason": "No approved evidence; no sixth relationship type and no invented connector."}], "generation_contract": {"authoritative_placement_sources": ["formal parameter bindings", "P3.2 relationship foundation"], "p2_numeric_world_transforms": "PROHIBITED", "manual_baked_placement": False}}
    return {"baseline": baseline, "bindings": bindings_doc, "accounting": accounting_doc, "graph": graph}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed outputs differ from a clean deterministic compile")
    args = parser.parse_args()
    assets = compile_assets()
    if args.check:
        changed = [name for name, value in assets.items() if load(OUTPUTS[name]) != value]
        if changed:
            raise SystemExit("non-deterministic or stale outputs: " + ", ".join(changed))
        print("PASS: deterministic regeneration and stable serialization")
        return 0
    for name, value in assets.items():
        write(OUTPUTS[name], value)
    print("WROTE: " + ", ".join(str(OUTPUTS[x].relative_to(ROOT)) for x in assets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
