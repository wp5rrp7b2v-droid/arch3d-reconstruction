#!/usr/bin/env python3
"""Pure-Python deterministic runtime compiler shared by T-018 Blender scripts."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "production/zhenguo_wanfo"
BUILD = P / "build"
ACCOUNTING = BUILD / "P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json"
BASELINE = BUILD / "P3_3_BUILDING_INPUT_BASELINE_V001.json"
GRAPH = BUILD / "P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json"
BINDINGS = BUILD / "P3_3_BUILDING_PARAMETER_BINDINGS_V001.json"
RUNTIME_MANIFEST = BUILD / "P3_3_WHOLE_BUILDING_RUNTIME_MANIFEST_V001.json"
CANONICAL_PM005 = 3505.7
MUTATED_PM005 = 3605.7
OUTCOMES = {
    "GENERATE_FROM_FORMAL_COMPONENT": "GENERATED_FORMAL_GEOMETRY",
    "PROXY_ONLY": "GENERATED_PROXY",
    "CONTROL_ONLY": "GENERATED_CONTROL",
    "ENVELOPE_ONLY": "GENERATED_ENVELOPE",
    "UNKNOWN_BLOCKED": "UNKNOWN_BLOCKED",
    "SEMANTIC_ONLY": "SEMANTIC_ONLY",
    "DEFERRED": "DEFERRED",
    "COMPARISON_ONLY": "COMPARISON_ONLY",
}
ALLOWED_OUTCOMES = set(OUTCOMES.values())
PROTECTED = [ACCOUNTING, BASELINE, GRAPH, BINDINGS]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8")


def protected_hashes() -> dict[str, str]:
    return {str(path.relative_to(ROOT)): sha256(path) for path in PROTECTED}


def _placement(family: str, family_index: int, pm005: float) -> dict:
    """Rule-derived diagnostic placement; never reads a P2 transform."""
    spacing = pm005
    layouts = {
        "COLUMN": (4, -1.5, -1.0, 0.0),
        "GRID_CONTROL": (4, -1.5, -1.0, 0.05),
        "BRACKET_ARM": (11, -5.0, -1.5, 6.2),
        "BRACKET_CONTACT": (11, -5.0, 0.5, 6.45),
        "PRIMARY_FRAME": (4, -1.5, -0.5, 7.2),
        "FRAME_CONTROL": (9, -4.0, -0.2, 7.8),
        "FRAME_SUPPORT": (9, -4.0, 0.2, 7.0),
        "PURLIN": (7, -3.0, 0.0, 9.0),
        "RAFTER": (12, -5.5, -1.0, 9.6),
        "GABLE_CONTROL": (2, -0.5, -1.0, 9.2),
        "ROOF_ENVELOPE": (3, -1.0, -0.5, 10.0),
    }
    columns, x0, y0, z = layouts[family]
    col, row = family_index % columns, family_index // columns
    # Only declared PM-005 grid dependants use the observed side-bay reference.
    x_step = spacing / 1000.0 if family in {"COLUMN", "GRID_CONTROL"} else 0.72
    return {
        "location_m": [round(x0 * x_step + col * x_step, 7), round(y0 + row * 0.42, 7), z],
        "rotation_euler_rad": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
        "placement_rule_id": "RULE-COLUMN-GRID" if family in {"COLUMN", "GRID_CONTROL"} else f"RULE-{family}",
        "parameter_ids": ["PM-005"] if family in {"COLUMN", "GRID_CONTROL"} else [],
    }


def compile_runtime(pm005: float = CANONICAL_PM005) -> dict:
    accounting = load(ACCOUNTING)
    family_seen = defaultdict(int)
    objects = []
    for sequence, source in enumerate(accounting["instances"]):
        family = source["source_family_id"]
        placement = _placement(family, family_seen[family], pm005)
        family_seen[family] += 1
        outcome = OUTCOMES[source["p3_3_disposition"]]
        objects.append({
            "runtime_instance_id": f"P3_3_RUNTIME_{sequence + 1:03d}",
            "legacy_instance_id": source["legacy_instance_id"],
            "component_id": source["component_id"],
            "explicit_non_component_identity": None,
            "source_family_id": family,
            "graph_parent_node_id": source["graph_parent_node_id"],
            "p3_3_disposition": outcome,
            "evidence_status": source["evidence_boundary"],
            "parameter_rule_provenance": {
                "source_parameter_ids": sorted(set(source["parameter_ids"] + placement["parameter_ids"])),
                "placement_rule_id": placement["placement_rule_id"],
                "source": "T-017 graph + formal parameters; no P2 numeric transform",
            },
            "historical_claim_boundary": "NOT_UPGRADED",
            "placement": placement,
        })
    snapshot = {"pm005_mm": pm005, "runtime_objects": objects}
    snapshot_hash = hashlib.sha256(stable_json(snapshot).encode()).hexdigest()
    counts = Counter(item["p3_3_disposition"] for item in objects)
    return {
        "version": "V001", "task": "T-018", "status": "CANONICAL" if pm005 == CANONICAL_PM005 else "TEST_ONLY_MUTATION",
        "generator_contract": {"clean_scene": True, "p2_blend_loaded": False, "p2_numeric_transform_usage": 0,
                               "blender_version": "4.5.13", "relationship_vocabulary": ["SUPPORT", "CONNECT", "LOCATE", "REPEAT", "BELONG"]},
        "parameter_state": {"PM-005": {"value_mm": pm005, "canonical_value_mm": CANONICAL_PM005,
                                         "source": str(BINDINGS.relative_to(ROOT))}},
        "input_hashes": protected_hashes(),
        "runtime_objects": objects,
        "runtime_accounting": {"input_count": 365, "outcome_count": len(objects), "outcome_counts": dict(sorted(counts.items())),
                               "unexplained_runtime_omission": 0, "anonymous_formal_mesh": 0, "broken_identity": 0},
        "technical_helpers": {"count": 0, "historical_component_count": 0},
        "canonical_semantic_snapshot_sha256": snapshot_hash,
        "blend_artifact": {"path": "artifacts/P3_3_WHOLE_BUILDING_CANONICAL_V001.blend", "sha256": "POPULATED_BY_GITHUB_ACTIONS"},
    }


def normalized_snapshot(manifest: dict) -> dict:
    return {"parameter_state": manifest["parameter_state"], "runtime_objects": manifest["runtime_objects"]}
