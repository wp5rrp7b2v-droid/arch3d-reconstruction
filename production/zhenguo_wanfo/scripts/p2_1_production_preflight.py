#!/usr/bin/env python3
"""Read-only P2.1 entry check with an independently approved candidate override."""

from __future__ import annotations

import argparse
import json

from validate_p2_1_parameter_set import DEPENDENCY, PARAMETERS, run, read_json
from validate_p2_1_approved_override import OVERRIDES, validate_override


def evaluate(errors: list[str], summary: dict, matrix: dict,
             parameter_set: dict | None = None, sidecar: dict | None = None,
             require_override: bool = False) -> dict:
    entries = matrix.get("entries", {}) if isinstance(matrix, dict) else {}
    entries = entries if isinstance(entries, dict) else {}
    historical_blockers = []
    for ident, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        if entry.get("unknown_dependency_status") == "BLOCKS_P2_2_GEOMETRY":
            historical_blockers.append({"id": ident, "parameter_key": entry.get("parameter_key"),
                                        "reason": entry.get("blocking_reason")})
    candidate_errors = []
    resolution = None
    if require_override or sidecar is not None:
        candidate_errors, resolution = validate_override(parameter_set or {}, matrix, sidecar)
    all_errors = errors + candidate_errors
    resolved_ids = ({resolution["target_parameter_id"]} if resolution is not None and not all_errors else set())
    unresolved = [item for item in historical_blockers if item["id"] not in resolved_ids]
    return {"production_preflight": "HOLD" if all_errors or unresolved else "PASS",
            "machine_validation": "FAIL" if all_errors else "PASS",
            "candidate_validation": "FAIL" if candidate_errors else "PASS" if resolution else "NOT_PROVIDED",
            "validation_errors": all_errors,
            "parameter_count": summary.get("parameter_count"),
            "classification_counts": summary.get("classification_counts"),
            "dependency_count": summary.get("dependency_count"),
            "unknown_ids": summary.get("unknown_ids"),
            "reasonable_completion_ids": summary.get("reasonable_completion_ids"),
            "schema_validation": summary.get("schema_validation"),
            "three_layer_preservation": summary.get("three_layer_preservation"),
            "geometry_critical_historical_unknown_count": len(historical_blockers),
            "approved_candidate_resolution_count": len(resolved_ids),
            "geometry_critical_unresolved_blocker_count": len(unresolved),
            "approved_candidate_resolution": resolution if resolved_ids else None,
            "historical_blockers": historical_blockers,
            "blockers": unresolved}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable preflight result")
    args = parser.parse_args()
    try:
        errors, summary = run()
        parameter_set = read_json(PARAMETERS)
        matrix = read_json(DEPENDENCY)
        sidecar = read_json(OVERRIDES) if OVERRIDES.exists() else None
        result = evaluate(errors, summary, matrix, parameter_set, sidecar, require_override=True)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"production_preflight": "HOLD", "machine_validation": "FAIL",
                  "candidate_validation": "FAIL", "validation_errors": [str(exc)],
                  "geometry_critical_historical_unknown_count": None,
                  "approved_candidate_resolution_count": 0,
                  "geometry_critical_unresolved_blocker_count": None,
                  "blockers": []}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["production_preflight"], json.dumps(result, ensure_ascii=False))
    return 0 if result["production_preflight"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
