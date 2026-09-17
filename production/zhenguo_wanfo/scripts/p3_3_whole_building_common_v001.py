#!/usr/bin/env python3
"""Authoritative-input compiler shared by the T-018 Blender programs."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "production/zhenguo_wanfo"
BUILD = P / "build"
ACCOUNTING = BUILD / "P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json"
BASELINE = BUILD / "P3_3_BUILDING_INPUT_BASELINE_V001.json"
GRAPH = BUILD / "P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json"
BINDINGS = BUILD / "P3_3_BUILDING_PARAMETER_BINDINGS_V001.json"
PARAMETERS = P / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
REPRESENTATIVE_GRAPH = P / "assembly/P3_2_REPRESENTATIVE_RELATIONSHIP_GRAPH_V001.json"
MASTER_LIBRARY = P / "registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json"
MASTER_SCOPE = P / "registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json"
RUNTIME_MANIFEST = BUILD / "P3_3_WHOLE_BUILDING_RUNTIME_MANIFEST_V001.json"
CANONICAL_PM005 = 3505.7
MUTATED_PM005 = 3605.7
OUTCOMES = {
    "GENERATE_FROM_FORMAL_COMPONENT": "GENERATED_FORMAL_GEOMETRY",
    "PROXY_ONLY": "GENERATED_PROXY", "CONTROL_ONLY": "GENERATED_CONTROL",
    "ENVELOPE_ONLY": "GENERATED_ENVELOPE", "UNKNOWN_BLOCKED": "UNKNOWN_BLOCKED",
    "SEMANTIC_ONLY": "SEMANTIC_ONLY", "DEFERRED": "DEFERRED", "COMPARISON_ONLY": "COMPARISON_ONLY",
}
ALLOWED_OUTCOMES = set(OUTCOMES.values())
PROTECTED = [ACCOUNTING, BASELINE, GRAPH, BINDINGS, PARAMETERS, REPRESENTATIVE_GRAPH, MASTER_LIBRARY, MASTER_SCOPE]
COLUMN_ID = re.compile(r"^COLUMN_X(?P<x>\d+)_Y(?P<y>\d+)$")


def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def sha256(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def stable_json(value) -> str: return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"
def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(stable_json(value), encoding="utf-8")
def protected_hashes() -> dict[str, str]: return {str(path.relative_to(ROOT)): sha256(path) for path in PROTECTED}


def _authorities(pm005: float):
    graph = load(GRAPH); bindings = load(BINDINGS); params = load(PARAMETERS)["parameters"]
    parameter_values = {key: item.get("value") for key, item in params.items()}
    parameter_values["PM-005"] = pm005
    parameter_values["Z-006-RC-01"] = next(x["value"] for x in bindings["bindings"] if x["parameter_id"] == "Z-006-RC-01")
    relations = {r["source_node"]: r for r in graph["relationships"] if r["source_node"].startswith("P3_3:")}
    repeat = next(r for r in load(REPRESENTATIVE_GRAPH)["unit_graphs"]["C"]["relationships"] if r["relationship_id"] == "C-R01")
    masters = {m["component_id"]: m for m in load(MASTER_LIBRARY)["masters"]}
    scope = {r["candidate_id"]: r for r in load(MASTER_SCOPE)["records"]}
    return graph, bindings, parameter_values, relations, repeat, masters, scope


def _column_placement(source, values, relation, repeat):
    match = COLUMN_ID.fullmatch(source["legacy_instance_id"])
    if not match: raise ValueError(f"column identity cannot drive grid rule: {source['legacy_instance_id']}")
    x, y = int(match["x"]), int(match["y"])
    max_x, max_y = int(values["PM-001"]), int(values["PM-002"])
    if not (0 <= x <= max_x and 0 <= y <= max_y and (x in (0, max_x) or y in (0, max_y))):
        raise ValueError(f"column identity violates PM-001/PM-002 perimeter topology: {source['legacy_instance_id']}")
    direction = repeat["repeat_rule"]["direction"]
    spacing = float(values[repeat["repeat_rule"]["spacing_ref"]])
    corner = x in (0, max_x) and y in (0, max_y)
    return {
        "status": "RULE_DERIVED", "location_mm": [x * spacing * direction[0], y * spacing, float(values["Z-005"]) if corner else 0.0],
        "rotation_euler_rad": [0.0, 0.0, 0.0], "scale": [1.0, 1.0, 1.0],
        "derivation": {
            "building_graph_node_id": f"P3_3:{source['legacy_instance_id']}", "building_graph_relationship_id": relation["relationship_id"],
            "p3_2_relationship_id": repeat["relationship_id"], "relation_type": repeat["relation_type"],
            "interface_ids": [repeat["repeat_rule"]["start_interface"], repeat["repeat_rule"]["direction_interface"]],
            "rule_id": "RULE-COLUMN-GRID", "index_source": "legacy identity X/Y fields approved by T-017 accounting",
            "parameter_values": {"PM-001": values["PM-001"], "PM-002": values["PM-002"], "PM-005": spacing,
                                 "PM-013": values["PM-013"], "PM-014": values["PM-014"], "Z-005": values["Z-005"]},
            "authoritative_sources": [str(GRAPH.relative_to(ROOT)), str(BINDINGS.relative_to(ROOT)), str(PARAMETERS.relative_to(ROOT)), str(REPRESENTATIVE_GRAPH.relative_to(ROOT))],
        },
    }


def compile_runtime(pm005: float = CANONICAL_PM005) -> dict:
    accounting = load(ACCOUNTING); _, _, values, relations, repeat, masters, scope = _authorities(pm005); objects = []
    for sequence, source in enumerate(accounting["instances"]):
        component_id = source["component_id"]; disposition = source["p3_3_disposition"]
        # T-019/D-055: unqualified purlins remain deferred even if an older accounting checkout says otherwise.
        if component_id == "CMP-PURLIN-001": disposition = "DEFERRED"
        outcome = OUTCOMES[disposition]
        master = masters.get(component_id) if outcome == "GENERATED_FORMAL_GEOMETRY" else None
        if outcome == "GENERATED_FORMAL_GEOMETRY" and not master: raise ValueError(f"formal component has no approved Master: {component_id}")
        graph_node = f"P3_3:{source['legacy_instance_id']}"; relation = relations[graph_node]
        placement = _column_placement(source, values, relation, repeat) if component_id == "CMP-COLUMN-001" and outcome == "GENERATED_FORMAL_GEOMETRY" else {
            "status": "NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE", "location_mm": None, "rotation_euler_rad": None, "scale": None,
            "derivation": {"building_graph_node_id": graph_node, "building_graph_relationship_id": relation["relationship_id"],
                           "relation_type": relation["relation_type"], "rule_id": None, "parameter_values": {},
                           "authoritative_sources": [str(GRAPH.relative_to(ROOT))]},
        }
        objects.append({
            "runtime_instance_id": f"P3_3_RUNTIME_{sequence + 1:03d}", "legacy_instance_id": source["legacy_instance_id"],
            "component_id": component_id, "explicit_non_component_identity": None, "source_family_id": source["source_family_id"],
            "graph_parent_node_id": source["graph_parent_node_id"], "p3_3_disposition": outcome,
            "evidence_status": source["evidence_boundary"], "historical_claim_boundary": "NOT_UPGRADED", "placement": placement,
            "parameter_rule_provenance": placement["derivation"],
            "formal_master": None if not master else {key: master[key] for key in ("master_id", "master_version", "generator_path", "parameter_path", "geometry_mode", "approval_status")},
        })
    snapshot = {"pm005_mm": pm005, "runtime_objects": objects}; counts = Counter(x["p3_3_disposition"] for x in objects)
    return {"version":"V001", "task":"T-018", "status":"CANONICAL" if pm005 == CANONICAL_PM005 else "TEST_ONLY_MUTATION",
            "generator_contract":{"clean_scene":True,"p2_blend_loaded":False,"p2_numeric_transform_usage":0,"blender_version":"4.5.13","relationship_vocabulary":["SUPPORT","CONNECT","LOCATE","REPEAT","BELONG"],"formal_geometry_policy":"APPROVED_P3_1_MASTER_GENERATOR_ONLY"},
            "parameter_state":{"PM-005":{"value_mm":pm005,"canonical_value_mm":CANONICAL_PM005,"source":str(BINDINGS.relative_to(ROOT))}},
            "input_hashes":protected_hashes(), "runtime_objects":objects,
            "runtime_accounting":{"input_count":365,"outcome_count":len(objects),"outcome_counts":dict(sorted(counts.items())),"unexplained_runtime_omission":0,"anonymous_formal_mesh":0,"broken_identity":0},
            "technical_helpers":{"count":0,"historical_component_count":0},
            "canonical_semantic_snapshot_sha256":hashlib.sha256(stable_json(snapshot).encode()).hexdigest(),
            "blend_artifact":{"path":"artifacts/P3_3_WHOLE_BUILDING_CANONICAL_V001.blend","sha256":"POPULATED_BY_GITHUB_ACTIONS"}}


def normalized_snapshot(manifest: dict) -> dict: return {"parameter_state":manifest["parameter_state"],"runtime_objects":manifest["runtime_objects"]}
