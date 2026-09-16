#!/usr/bin/env python3
"""Deterministically compile the T-017 building baseline and assembly graph."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "production/zhenguo_wanfo"
BUILD = P / "build"

PATHS = {
    "p2_manifest": BUILD / "P2_3_INTEGRATION_MANIFEST_V001.json",
    "p3_0_ontology": P / "registry/P3_0_COMPONENT_ONTOLOGY_V001.json",
    "p3_0_schema": P / "registry/P3_0_COMPONENT_REGISTRY_SCHEMA_V001.json",
    "registry": P / "registry/P3_0_COMPONENT_REGISTRY_V001.json",
    "migration": P / "registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json",
    "p3_1_identity": P / "registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json",
    "p3_1_scope": P / "registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json",
    "masters": P / "registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json",
    "p3_1_contract": P / "registry/P3_1_MASTER_ASSET_CONTRACT_V002.json",
    "assembly_schema": P / "assembly/P3_2_ASSEMBLY_SCHEMA_V001.json",
    "assembly_nodes": P / "assembly/P3_2_ASSEMBLY_NODE_REGISTRY_V001.json",
    "relationships": P / "assembly/P3_2_RELATIONSHIP_TYPES_V001.json",
    "interfaces": P / "assembly/P3_2_INTERFACE_REGISTRY_V001.json",
    "representative_assemblies": P / "assembly/P3_2_REPRESENTATIVE_ASSEMBLY_REGISTRY_V001.json",
    "representative_interfaces": P / "assembly/P3_2_REPRESENTATIVE_INTERFACE_EXTENSION_V001.json",
    "representative_graph": P / "assembly/P3_2_REPRESENTATIVE_RELATIONSHIP_GRAPH_V001.json",
    "parameters": P / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json",
    "overrides": P / "params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json",
    "dependency": P / "dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json",
    "evidence_schema": P / "schema/evidence_aware_parameter_schema_v001.json",
    "p3_2_validator": P / "scripts/validate_p3_2_relationship_foundation_v001.py",
    "p3_2_representative_validator": P / "scripts/validate_p3_2_representative_assembly_v001.py",
    "p3_2_tests": P / "tests/test_p3_2_relationship_foundation_v001.py",
    "p3_2_representative_tests": P / "tests/test_p3_2_representative_assembly_v001.py",
    "p3_2_validation": P / "validation/P3_2_RELATIONSHIP_FOUNDATION_VALIDATION_V001.json",
    "p3_2_representative_validation": P / "validation/P3_2_REPRESENTATIVE_ASSEMBLY_VALIDATION_V001.json",
}

OUTPUTS = {
    "baseline": BUILD / "P3_3_BUILDING_INPUT_BASELINE_V001.json",
    "bindings": BUILD / "P3_3_BUILDING_PARAMETER_BINDINGS_V001.json",
    "accounting": BUILD / "P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json",
    "graph": BUILD / "P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json",
    "validation": BUILD / "P3_3_BUILDING_GRAPH_VALIDATION_V001.json",
}

MASTER_INPUTS = sorted(
    list((P / "component_library/masters").glob("*/**/*_MASTER_PARAMS_V001.json"))
    + list((P / "component_library/masters").glob("*/**/*_MASTER_SEMANTIC_V001.json"))
)

AUTHORITATIVE_KEYS = set(PATHS) - {"p2_manifest", "migration"}
ORGANIZATIONS = {
    "BRACKET_ARM": "ORG-BRACKET-SYSTEM",
    "BRACKET_CONTACT": "ORG-BRACKET-SYSTEM",
    "COLUMN": "ORG-COLUMN-GRID",
    "GRID_CONTROL": "ORG-COLUMN-GRID",
    "FRAME_CONTROL": "ORG-FRAME-SYSTEM",
    "FRAME_SUPPORT": "ORG-FRAME-SYSTEM",
    "PRIMARY_FRAME": "ORG-FRAME-SYSTEM",
    "GABLE_CONTROL": "ORG-ROOF-SYSTEM",
    "PURLIN": "ORG-ROOF-SYSTEM",
    "RAFTER": "ORG-ROOF-SYSTEM",
    "ROOF_ENVELOPE": "ORG-ROOF-SYSTEM",
}

TARGET_BINDINGS = {
    "柱网与主要空间关系": (["ORG-COLUMN-GRID"], ["LOCATE", "REPEAT"], ["RULE-COLUMN-GRID"]),
    "设计模数与主要构件比例": (["ORG-BUILDING"], [], ["RULE-MODULAR-SYSTEM"]),
    "柱与屋架绝对Z控制": (["ORG-COLUMN-GRID", "ORG-FRAME-SYSTEM"], ["LOCATE"], ["RULE-MAJOR-ELEVATIONS"]),
    "斗栱拓扑骨架": (["ORG-BRACKET-SYSTEM"], ["LOCATE", "REPEAT"], ["RULE-BRACKET-TOPOLOGY"]),
    "主体梁架": (["ORG-FRAME-SYSTEM"], ["BELONG"], ["RULE-FRAME-SEMANTICS"]),
    "屋架水平控制": (["ORG-FRAME-SYSTEM"], ["LOCATE"], ["RULE-FRAME-DEPTHS"]),
    "屋顶山面控制几何": (["ORG-ROOF-SYSTEM"], ["LOCATE"], ["RULE-ROOF-OUTLINE"]),
    "屋顶Z向控制几何": (["ORG-ROOF-SYSTEM"], ["LOCATE"], ["RULE-ROOF-ELEVATIONS"]),
    "现状形变校核": (["ORG-BUILDING"], [], ["RULE-COMPARISON-ONLY-DEFORMATION"]),
    "构件历史元数据": (["ORG-BUILDING"], [], ["RULE-EVIDENCE-METADATA"]),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def serialize(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write(path: Path, value) -> None:
    path.write_text(serialize(value), encoding="utf-8")


QUALIFICATION_DISPOSITIONS = {
    "DEFERRED_INSUFFICIENT_EVIDENCE": "DEFERRED",
    "PROXY_ONLY": "PROXY_ONLY",
    "CONTROL_ONLY": "CONTROL_ONLY",
    "ENVELOPE_ONLY": "ENVELOPE_ONLY",
}


def direct_identity_qualifications(scope: dict, identity: dict) -> dict[str, str]:
    """Resolve P3.1 qualifications by explicit identity fields, never by family."""
    resolved: dict[str, set[str]] = {}
    for document in (scope, identity):
        for record in document.get("records", []):
            for key in ("candidate_id", "source_registry_id"):
                direct_id = record.get(key)
                if direct_id:
                    resolved.setdefault(direct_id, set()).add(record["eligibility_status"])
    conflicts = {key: values for key, values in resolved.items() if len(values) != 1}
    if conflicts:
        raise ValueError(f"ambiguous explicit P3.1 identity qualification: {conflicts}")
    return {key: next(iter(values)) for key, values in resolved.items()}


def disposition(role: str, ontology: str, qualification: str | None, approved_master: bool) -> str:
    if role == "CONTROL_OBJECT":
        role_disposition = "CONTROL_ONLY"
    elif role == "ENVELOPE_SURFACE":
        role_disposition = "ENVELOPE_ONLY"
    elif role == "GEOMETRIC_PROXY":
        role_disposition = "UNKNOWN_BLOCKED" if ontology == "UNKNOWN_UNRESOLVED_COMPONENT" else "PROXY_ONLY"
    else:
        role_disposition = "GENERATE_FROM_FORMAL_COMPONENT"
    if role_disposition != "GENERATE_FROM_FORMAL_COMPONENT":
        return role_disposition
    if qualification in QUALIFICATION_DISPOSITIONS:
        return QUALIFICATION_DISPOSITIONS[qualification]
    if qualification == "MASTER_REQUIRED" and not approved_master:
        return "DEFERRED"
    return role_disposition


def input_record(path: Path, classification, role: str, allowed_fields=None, prohibited_fields=None):
    return {
        "path": str(path.relative_to(ROOT)),
        "classifications": classification if isinstance(classification, list) else [classification],
        "role": role,
        "sha256": digest(path),
        "protection": "READ_ONLY",
        "allowed_fields": allowed_fields or ["ALL_CONTRACT_AUTHORIZED_FIELDS"],
        "prohibited_fields": prohibited_fields or [],
    }


def compile_assets() -> dict:
    manifest = load(PATHS["p2_manifest"])
    registry = load(PATHS["registry"])
    migration = load(PATHS["migration"])
    parameters = load(PATHS["parameters"])
    overrides = load(PATHS["overrides"])
    dependencies = load(PATHS["dependency"])["entries"]
    masters = load(PATHS["masters"])
    scope = load(PATHS["p3_1_scope"])
    identity = load(PATHS["p3_1_identity"])
    qualifications = direct_identity_qualifications(scope, identity)
    approved_component_ids = {item["component_id"] for item in masters["masters"]}
    relation_source = load(PATHS["relationships"])
    relation_types = [item["relation_type"] for item in relation_source["relationship_types"]]

    inventory = [
        input_record(
            PATHS["p2_manifest"],
            ["ACCOUNTING_REFERENCE_ONLY", "COMPARISON_ONLY"],
            "P2 frozen instance identity, coverage, evidence and comparison source only",
            ["instance_id", "family_id", "variant_id", "evidence metadata", "parameter references", "counts"],
            ["instances[].transform.location_mm", "instances[].transform.rotation_euler_rad", "instances[].transform.scale"],
        ),
        input_record(PATHS["migration"], "ACCOUNTING_REFERENCE_ONLY", "P3.0-approved P2 identity migration accounting"),
    ]
    inventory.extend(
        input_record(PATHS[key], "AUTHORITATIVE_GENERATIVE", key.upper())
        for key in sorted(AUTHORITATIVE_KEYS)
    )
    inventory.extend(
        input_record(path, "AUTHORITATIVE_GENERATIVE", "P3.1_APPROVED_MASTER_PARAMETER_OR_SEMANTIC_SNAPSHOT")
        for path in MASTER_INPUTS
    )
    prohibited = [
        {
            "classification": "PROHIBITED_AS_GENERATIVE_INPUT",
            "source_path": str(PATHS["p2_manifest"].relative_to(ROOT)),
            "field_path": field,
            "reason": "P2 numeric world transform is comparison/diagnostic evidence, never a P3.3 placement source.",
            "authoritative_generation_usage_count": 0,
        }
        for field in ("instances[].transform.location_mm", "instances[].transform.rotation_euler_rad", "instances[].transform.scale")
    ]
    baseline = {
        "version": "V001",
        "task": "T-017",
        "status": "CANONICAL",
        "input_classifications": {
            "AUTHORITATIVE_GENERATIVE": "May drive P3.3 rules within its evidence boundary.",
            "ACCOUNTING_REFERENCE_ONLY": "May establish identity and scope accounting only.",
            "COMPARISON_ONLY": "May be used for diagnostics/comparison, never generation.",
            "PROHIBITED_AS_GENERATIVE_INPUT": "Must never enter generation or placement paths.",
        },
        "inputs": inventory,
        "prohibited_inputs": prohibited,
        "protection_hashes": {item["path"]: item["sha256"] for item in inventory},
    }

    bindings = []
    for pid, record in sorted(parameters["parameters"].items()):
        dependency = dependencies[pid]
        node_ids, relation_ids, rule_ids = TARGET_BINDINGS[dependency["p2_2_target"]]
        bindings.append(
            {
                "parameter_id": pid,
                "parameter_key": record["parameter_key"],
                "value": record.get("value"),
                "unit": record.get("unit"),
                "classification": record["classification"],
                "source_layer": record["source_layer"],
                "time_layer": record["time_layer"],
                "production_use": record["production_use"],
                "replaceable": record["is_replaceable"],
                "source_ids": record["source_ids"],
                "building_role": dependency["p2_2_target"],
                "dependency_role": dependency["geometry_dependency_role"],
                "binding_targets": {
                    "graph_node_ids": node_ids,
                    "relationship_types": relation_ids,
                    "rule_ids": rule_ids,
                },
                "historical_claim_upgrade": False,
            }
        )
    override = overrides["overrides"]["Z-006-RC-01"]
    bindings.append(
        {
            "parameter_id": "Z-006-RC-01",
            "parameter_key": override["target_parameter_key"],
            "value": override["current_resolved_value"],
            "unit": override["unit"],
            "classification": override["classification"],
            "source_layer": "APPROVED_OVERRIDE",
            "time_layer": override["time_layer"],
            "production_use": override["production_use"],
            "replaceable": override["is_replaceable"],
            "source_ids": override["evidence_basis"] + [override["approval_decision_id"]],
            "building_role": "柱与屋架绝对Z控制",
            "dependency_role": "APPROVED_REPLACEABLE_RULE",
            "binding_targets": {
                "graph_node_ids": ["ORG-COLUMN-GRID", "ORG-FRAME-SYSTEM"],
                "relationship_types": ["LOCATE"],
                "rule_ids": ["RULE-MAJOR-ELEVATIONS"],
                "formula": override["formula"],
                "depends_on": override["depends_on"],
            },
            "historical_claim_boundary": override["historical_claim_boundary"],
            "historical_claim_upgrade": False,
        }
    )
    bindings_doc = {
        "version": "V001",
        "task": "T-017",
        "status": "CANONICAL",
        "p3_2_validated_dependencies": [
            {
                "parameter_id": "PM-005",
                "assembly_unit_id": "AU-COLUMN-GRID-001",
                "relationship_type": "REPEAT",
                "source": str(PATHS["representative_graph"].relative_to(ROOT)),
                "boundary": "P3.2 validated representative dependency; observed reference remains observed reference.",
            },
            {
                "parameter_id": "Z-006-RC-01",
                "assembly_unit_id": "AU-COLUMN-LUDOU-001",
                "relationship_type": "LOCATE",
                "source": str(PATHS["representative_graph"].relative_to(ROOT)),
                "boundary": "Approved replaceable candidate, not confirmed historical column height.",
            },
        ],
        "bindings": bindings,
        "mandatory_boundaries": {
            "Z-006": "UNKNOWN / null / DO_NOT_LOCK",
            "Z-006-RC-01": "REASONABLE_COMPLETION / replaceable / D-023",
            "DG-114": "UNKNOWN / no unified small-dou historical specification claim",
            "HIS-002": "component originality unknown",
            "six_chuanfu_historical_full_length": None,
            "canonical_reference_length_mm_usage": "NON_HISTORICAL_ENGINEERING_REFERENCE_ONLY",
        },
    }

    components = {item["component_id"]: item for item in registry["components"]}
    migration_instances = {item["p2_instance_id"]: item for item in migration["instances"]}
    accounting = []
    for source in sorted(manifest["instances"], key=lambda item: item["instance_id"]):
        mapped = migration_instances[source["instance_id"]]
        component = components[mapped["p3_component_id"]]
        accounting.append(
            {
                "legacy_instance_id": source["instance_id"],
                "source_family_id": source["family_id"],
                "source_variant_id": source["variant_id"],
                "component_id": component["component_id"],
                "semantic_class": component["ontology_type"],
                "asset_role": component["current_asset_role"],
                "p3_3_disposition": disposition(
                    component["current_asset_role"],
                    component["ontology_type"],
                    qualifications.get(component["component_id"]),
                    component["component_id"] in approved_component_ids,
                ),
                "evidence_boundary": {
                    "bounded_placeholder": source.get("bounded_placeholder", False),
                    "originality_status": source.get("originality_status", "unknown"),
                    "time_layer": source.get("time_layer"),
                    "historical_claim": "NOT_UPGRADED",
                },
                "graph_inclusion_status": "INCLUDED",
                "graph_parent_node_id": ORGANIZATIONS[source["family_id"]],
                "parameter_ids": source.get("parameter_ids", []),
                "provenance": [str(PATHS[key].relative_to(ROOT)) for key in ("p2_manifest", "migration", "registry")],
                "explanation": "Retained under its registry-qualified identity; P2 numeric transform is not copied.",
            }
        )
    accounting_doc = {
        "version": "V001",
        "task": "T-017",
        "status": "CANONICAL",
        "summary": {
            "families_accounted": len({item["source_family_id"] for item in accounting}),
            "families_expected": 11,
            "variants_accounted": len({item["source_variant_id"] for item in accounting}),
            "variants_expected": 40,
            "instances_accounted": len(accounting),
            "instances_expected": 365,
            "unexplained_omissions": 0,
            "orphan_identities": 0,
        },
        "instances": accounting,
    }

    approved = {
        item["component_id"]: {"master_id": item["master_id"], "approval_status": item["approval_status"]}
        for item in masters["masters"]
    }
    nodes = [
        {"node_id": "BUILDING_ROOT", "node_class": "ASSEMBLY_UNIT", "organizational_level": "ROOT", "label": "万佛殿 building root", "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"},
        {"node_id": "ORG-BUILDING", "node_class": "ASSEMBLY_UNIT", "organizational_level": "BUILDING", "label": "万佛殿 building organization", "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"},
        {"node_id": "ORG-COLUMN-GRID", "node_class": "ASSEMBLY_UNIT", "organizational_level": "ASSEMBLY", "label": "柱网组织", "p3_2_assembly_refs": ["AU-COLUMN-GRID-001", "AU-COLUMN-LUDOU-001"], "parameter_refs": ["PM-001", "PM-002", "PM-005", "PM-013", "PM-014", "Z-006-RC-01"], "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"},
        {"node_id": "ORG-BRACKET-SYSTEM", "node_class": "ASSEMBLY_UNIT", "organizational_level": "ASSEMBLY", "label": "斗栱系统组织", "parameter_refs": ["DG-001", "DG-002", "DG-110", "DG-111", "DG-112", "DG-113"], "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"},
        {"node_id": "ORG-FRAME-SYSTEM", "node_class": "ASSEMBLY_UNIT", "organizational_level": "ASSEMBLY", "label": "梁架系统组织", "p3_2_assembly_refs": ["AU-FRAME-TIER-001"], "parameter_refs": ["RF-001", "FR-004", "FR-005", "FR-006", "FR-007"], "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"},
        {"node_id": "ORG-ROOF-SYSTEM", "node_class": "ASSEMBLY_UNIT", "organizational_level": "ASSEMBLY", "label": "屋顶系统组织", "parameter_refs": ["OUT-003", "ROOF-004", "ROOF-005", "ROOF-006", "ROOF-010", "ROOF-011"], "p3_3_disposition": "SEMANTIC_ONLY", "historical_claim": "ORGANIZATIONAL_ONLY"},
    ]
    for item in accounting:
        nodes.append(
            {
                "node_id": "P3_3:" + item["legacy_instance_id"],
                "node_class": {"CONTROL_OBJECT": "CONTROL", "ENVELOPE_SURFACE": "ENVELOPE", "GEOMETRIC_PROXY": "PROXY"}.get(item["asset_role"], "FORMAL_COMPONENT"),
                "organizational_level": "RUNTIME",
                "component_id": item["component_id"],
                "legacy_instance_id": item["legacy_instance_id"],
                "master_qualification": approved.get(item["component_id"], "NOT_AN_APPROVED_P3_1_MASTER"),
                "parameter_refs": item["parameter_ids"],
                "placement_rule": {"source": "BUILDING_PARAMETERS_AND_P3_2_RELATIONSHIPS", "p2_numeric_transform_used": False, "status": "DEFERRED_OR_RULE_DRIVEN"},
                "p3_3_disposition": item["p3_3_disposition"],
                "evidence_status": item["evidence_boundary"],
                "historical_claim": "NOT_UPGRADED",
            }
        )
    relations = [
        {"relationship_id": "BELONG-BUILDING-ROOT", "relation_type": "BELONG", "source_node": "ORG-BUILDING", "target_node": "BUILDING_ROOT"},
        *[
            {"relationship_id": f"BELONG-{node_id}", "relation_type": "BELONG", "source_node": node_id, "target_node": "ORG-BUILDING"}
            for node_id in ("ORG-COLUMN-GRID", "ORG-BRACKET-SYSTEM", "ORG-FRAME-SYSTEM", "ORG-ROOF-SYSTEM")
        ],
    ]
    relations.extend(
        {"relationship_id": f"BELONG-RUNTIME-{index:04d}", "relation_type": "BELONG", "source_node": "P3_3:" + item["legacy_instance_id"], "target_node": item["graph_parent_node_id"]}
        for index, item in enumerate(accounting, 1)
    )
    for relation in relations:
        relation.update({"directionality": "DIRECTED", "provenance": [str(PATHS["relationships"].relative_to(ROOT)), "T-017 deterministic organization rule"], "parameter_refs": [], "evidence_status": "ORGANIZATIONAL_ONLY", "replaceability": True, "historical_claim": False})
    graph = {
        "version": "V001",
        "task": "T-017",
        "status": "CANONICAL",
        "building_root": "BUILDING_ROOT",
        "foundational_relation_vocabulary": relation_types,
        "relationship_definition_source": str(PATHS["relationships"].relative_to(ROOT)),
        "p3_2_foundation_reuse": {
            "assembly_registry": str(PATHS["representative_assemblies"].relative_to(ROOT)),
            "relationship_graph": str(PATHS["representative_graph"].relative_to(ROOT)),
            "interface_extension": str(PATHS["representative_interfaces"].relative_to(ROOT)),
            "reused_assembly_units": ["AU-COLUMN-LUDOU-001", "AU-FRAME-TIER-001", "AU-COLUMN-GRID-001"],
            "policy": "Reuse validated semantics and parameter dependencies; do not assert unsupported building-instance SUPPORT or CONNECT edges.",
        },
        "nodes": nodes,
        "relationships": relations,
        "unresolved_relationships": [{"scope": "45-degree corner, mortise, hidden-angle beam and unevidenced connections", "status": "UNKNOWN_BLOCKED", "reason": "No approved evidence; no sixth relationship type and no invented connector."}],
        "generation_contract": {"authoritative_placement_sources": ["formal parameter bindings", "P3.2 relationship foundation"], "p2_numeric_world_transforms": "PROHIBITED", "manual_baked_placement": False},
    }
    return {"baseline": baseline, "bindings": bindings_doc, "accounting": accounting_doc, "graph": graph}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed outputs differ from a clean deterministic compile")
    args = parser.parse_args()
    assets = compile_assets()
    if args.check:
        changed = [name for name, value in assets.items() if not OUTPUTS[name].is_file() or load(OUTPUTS[name]) != value]
        if changed:
            raise SystemExit("non-deterministic or stale outputs: " + ", ".join(changed))
        if serialize(compile_assets()) != serialize(assets):
            raise SystemExit("successive clean compilations are not stable")
        print("PASS: deterministic regeneration and stable serialization")
        return 0
    for name, value in assets.items():
        write(OUTPUTS[name], value)
    print("WROTE: " + ", ".join(str(OUTPUTS[name].relative_to(ROOT)) for name in assets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
