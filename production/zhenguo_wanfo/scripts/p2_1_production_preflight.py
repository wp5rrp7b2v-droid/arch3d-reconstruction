#!/usr/bin/env python3
"""Read-only P2.1 entry check: structural validation PASS can still mean P2.2 HOLD."""

from __future__ import annotations

import argparse
import json

from validate_p2_1_parameter_set import DEPENDENCY, run, read_json


def evaluate(errors: list[str], summary: dict, matrix: dict) -> dict:
    entries = matrix.get("entries", {})
    blockers = []
    for ident, entry in entries.items():
        if entry.get("unknown_dependency_status") == "BLOCKS_P2_2_GEOMETRY":
            blockers.append({"id": ident, "parameter_key": entry.get("parameter_key"),
                             "reason": entry.get("blocking_reason")})
    return {"production_preflight": "HOLD" if errors or blockers else "PASS",
            "machine_validation": "FAIL" if errors else "PASS",
            "validation_errors": errors,
            "parameter_count": summary.get("parameter_count"),
            "classification_counts": summary.get("classification_counts"),
            "dependency_count": summary.get("dependency_count"),
            "unknown_ids": summary.get("unknown_ids"),
            "reasonable_completion_ids": summary.get("reasonable_completion_ids"),
            "schema_validation": summary.get("schema_validation"),
            "three_layer_preservation": summary.get("three_layer_preservation"),
            "geometry_critical_unresolved_blocker_count": len(blockers),
            "blockers": blockers}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable preflight result")
    args = parser.parse_args()
    try:
        errors, summary = run()
        result = evaluate(errors, summary, read_json(DEPENDENCY))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = evaluate([str(exc)], {}, {"entries": {}})
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["production_preflight"], json.dumps(result, ensure_ascii=False))
    return 0 if result["production_preflight"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
