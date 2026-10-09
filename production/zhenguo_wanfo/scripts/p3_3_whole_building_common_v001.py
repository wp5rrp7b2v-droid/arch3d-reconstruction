#!/usr/bin/env python3
"""Pure deterministic placement compiler for the T-018 Blender build.

Coordinates in this module are project-model coordinates, not surveyed positions.
In particular, roof Y coordinates may only come from the T-020 datum authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "production/zhenguo_wanfo"
ACCOUNTING = P / "build/P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json"
PARAMETERS = P / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
OVERRIDES = P / "params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json"
DATUM = P / "build/P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_V001.json"
DATUM_RULE_ID = "RULE-P3-3-RECONSTRUCTED-DESIGN-DATUM-001"
OBSERVED_PLACEMENT_IDS = {f"PM-{i:03d}" for i in range(3, 8)}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def stable(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value) -> str:
    return hashlib.sha256(stable(value).encode()).hexdigest()


def _inputs(parameter_values=None):
    params = {key: rec.get("value") for key, rec in load(PARAMETERS)["parameters"].items()}
    params.update(parameter_values or {})
    override = load(OVERRIDES)["overrides"]["Z-006-RC-01"]
    params["Z-006-RC-01"] = override["current_resolved_value"]
    datum = load(DATUM)
    if datum.get("status") != "CANONICAL" or datum.get("rule_id") != DATUM_RULE_ID:
        raise ValueError("T-020 reconstructed-design datum authority is not canonical")
    return params, datum


def _grid(params):
    # PM-008..010 are explicitly authorized reconstructed-design candidates.
    chi = params["MOD-001"]
    side = params["PM-010"] * chi
    x_center = params["PM-008"] * chi
    y_center = params["PM-009"] * chi
    return (
        [-x_center / 2 - side, -x_center / 2, x_center / 2, x_center / 2 + side],
        [-y_center / 2 - side, -y_center / 2, y_center / 2, y_center / 2 + side],
    )


def _roof_controls(params, datum):
    ys = datum["roof_control"]["y_positions_mm"]
    eave_z = params["Z-006-RC-01"]
    rises = [params[k] * params["MOD-002"] for k in ("ROOF-007", "ROOF-008", "ROOF-009")]
    north_ids = [f"ROOF_PURLIN_N_{i:02d}" for i in range(4)]
    south_ids = ["ROOF_PURLIN_S_00", "ROOF_PURLIN_S_01", "ROOF_PURLIN_S_02"]
    north_z = [eave_z, eave_z + rises[0], eave_z + sum(rises[:2]), eave_z + sum(rises)]
    south_z = north_z[:3]
    return {key: (float(ys[key]), z) for key, z in zip(north_ids + south_ids, north_z + south_z)}


def compile_runtime(parameter_values=None):
    params, datum = _inputs(parameter_values)
    accounting = load(ACCOUNTING)["instances"]
    xs, grid_ys = _grid(params)
    roof = _roof_controls(params, datum)
    roof_xs = [-(params["PM-011"] / 2 + params["OUT-003"] * params["MOD-002"])]
    roof_xs += [xs[0], xs[1], xs[2], xs[3]]
    roof_xs += [-roof_xs[0]]
    records = []

    for source in accounting:
        rec = {
            "runtime_instance_id": "RT-" + source["legacy_instance_id"],
            "legacy_instance_id": source["legacy_instance_id"],
            "component_id": source["component_id"],
            "source_family_id": source["source_family_id"],
            "graph_parent_node_id": source["graph_parent_node_id"],
            "p3_3_disposition": source["p3_3_disposition"],
            "evidence_boundary": source["evidence_boundary"],
            "parameter_ids": source["parameter_ids"],
            "historical_claim_boundary": "UNCHANGED_FROM_T017",
            "placement": {"kind": "SEMANTIC_MARKER", "point_mm": [0.0, 0.0, 0.0]},
            "placement_provenance": ["T-017_ACCOUNTING", "DETERMINISTIC_ID_RULE"],
        }
        ident = source["legacy_instance_id"]
        family = source["source_family_id"]
        if family in {"COLUMN", "GRID_CONTROL"}:
            matches = {k: int(v) for k, v in re.findall(r"([XY])(\d\d)", ident)}
            if family == "COLUMN":
                rec["placement"] = {"kind": "VERTICAL_MEMBER", "start_mm": [xs[matches["X"]], grid_ys[matches["Y"]], 0.0], "end_mm": [xs[matches["X"]], grid_ys[matches["Y"]], params["Z-006-RC-01"]]}
            else:
                axis = ident[5]
                value = (xs if axis == "X" else grid_ys)[int(ident[-2:])]
                rec["placement"] = {"kind": "GRID_CONTROL", "axis": axis, "coordinate_mm": value}
            rec["placement_provenance"] = ["PM-008", "PM-009", "PM-010", "MOD-001"]
        elif family == "PURLIN":
            y, z = roof[ident]
            rec["placement"] = {"kind": "DEFERRED_CONTROL", "point_mm": [0.0, y, z]}
            rec["placement_provenance"] = [DATUM_RULE_ID, "FR-007", "MOD-002", "ROOF-007", "ROOF-008", "ROOF-009", "Z-006-RC-01"]
        elif family == "RAFTER":
            side, xi, segment = re.fullmatch(r"ROOF_RAFTER_([NS])_X(\d\d)_S(\d\d)", ident).groups()
            chain = [f"ROOF_PURLIN_{side}_{i:02d}" for i in range(4 if side == "N" else 3)]
            # South's last segment terminates at the one shared N03 ridge; S03 is forbidden.
            if side == "S": chain.append("ROOF_PURLIN_N_03")
            a, b = roof[chain[int(segment)]], roof[chain[int(segment) + 1]]
            rec["placement"] = {"kind": "SEGMENT_PROXY", "start_mm": [roof_xs[int(xi)], a[0], a[1]], "end_mm": [roof_xs[int(xi)], b[0], b[1]]}
            rec["placement_provenance"] = [DATUM_RULE_ID, "FR-007", "MOD-002", "ROOF-007", "ROOF-008", "ROOF-009"]
        elif family == "ROOF_ENVELOPE":
            side, segment = re.fullmatch(r"ROOF_SURFACE_([NS])_(\d\d)", ident).groups()
            chain = [f"ROOF_PURLIN_{side}_{i:02d}" for i in range(4 if side == "N" else 3)]
            if side == "S": chain.append("ROOF_PURLIN_N_03")
            a, b = roof[chain[int(segment)]], roof[chain[int(segment) + 1]]
            rec["placement"] = {"kind": "ENVELOPE_QUAD", "corners_mm": [[roof_xs[0], a[0], a[1]], [roof_xs[-1], a[0], a[1]], [roof_xs[-1], b[0], b[1]], [roof_xs[0], b[0], b[1]]]}
            rec["placement_provenance"] = [DATUM_RULE_ID, "PM-011", "OUT-003", "FR-007", "MOD-002"]
        elif family == "GABLE_CONTROL":
            east_west, side = re.fullmatch(r"GABLE_([EW])_([NS])", ident).groups()
            chain = [f"ROOF_PURLIN_{side}_{i:02d}" for i in range(4 if side == "N" else 3)]
            if side == "S": chain.append("ROOF_PURLIN_N_03")
            x = roof_xs[-1] if east_west == "E" else roof_xs[0]
            rec["placement"] = {"kind": "GABLE_POLYLINE", "points_mm": [[x, roof[k][0], roof[k][1]] for k in chain]}
            rec["placement_provenance"] = [DATUM_RULE_ID, "PM-011", "OUT-003", "FR-007", "MOD-002"]
        elif family in {"FRAME_CONTROL", "FRAME_SUPPORT"} and re.search(r"_POST_[NS]_\d\d_X\d\d_(LOW|UP)$", ident):
            side, tier, xi, level = re.search(r"_POST_([NS])_(\d\d)_X(\d\d)_(LOW|UP)$", ident).groups()
            key = f"ROOF_PURLIN_{side}_{tier}"
            if key not in roof: key = "ROOF_PURLIN_N_03"
            y, top = roof[key]
            base = params["Z-006-RC-01"] if level == "LOW" else top - params["MOD-004"] * params["MOD-002"]
            rec["placement"] = {"kind": "FRAME_ENDPOINT", "start_mm": [xs[int(xi)], y, base], "end_mm": [xs[int(xi)], y, top]}
            rec["placement_provenance"] = [DATUM_RULE_ID, "FR-007", "MOD-002", "MOD-004", "Z-006-RC-01"]
        records.append(rec)

    counts = dict(sorted(Counter(r["p3_3_disposition"] for r in records).items()))
    snapshot = {"datum_rule_id": DATUM_RULE_ID, "records": records}
    return {
        "task": "T-018", "version": "V001", "status": "CANONICAL_RUNTIME_PLAN",
        "datum_authority": str(DATUM.relative_to(ROOT)),
        "observed_design_placement_usage": 0,
        "runtime_count": len(records), "disposition_counts": counts,
        "records": records, "semantic_snapshot_sha256": sha(snapshot),
    }


def validate_runtime(runtime):
    failures = []
    records = runtime.get("records", [])
    if len(records) != 365 or len({r.get("legacy_instance_id") for r in records}) != 365:
        failures.append("SILENT_BUILDING_OMISSION")
    for rec in records:
        required = ("runtime_instance_id", "component_id", "graph_parent_node_id", "p3_3_disposition", "evidence_boundary", "placement_provenance")
        if any(not rec.get(k) for k in required): failures.append("BROKEN_COMPONENT_IDENTITY")
        if rec.get("historical_claim_boundary") != "UNCHANGED_FROM_T017": failures.append("SILENT_HISTORICIZATION")
        if rec.get("actual_full_length_mm") == 1000: failures.append("REFERENCE_LENGTH_LEAKS_INTO_BUILDING")
        provenance = set(rec.get("placement_provenance", []))
        if provenance & OBSERVED_PLACEMENT_IDS:
            failures.append("BAKED_MANUAL_BUILDING")
    purlins = [r for r in records if r.get("source_family_id") == "PURLIN"]
    if len(purlins) != 7 or any(r["p3_3_disposition"] != "DEFERRED" for r in purlins):
        failures.append("PURLIN_EVIDENCE_BOUNDARY")
    if any(r["legacy_instance_id"] == "ROOF_PURLIN_S_03" for r in records):
        failures.append("SOUTH_RIDGE_TERMINAL_PROHIBITED")
    return sorted(set(failures))
