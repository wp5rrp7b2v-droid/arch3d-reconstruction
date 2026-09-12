#!/usr/bin/env python3
"""Read and list parameter data. This module is intentionally Blender-free."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WANFO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARAMETER_SET = WANFO_ROOT / "params" / "P2_0_MINIMAL_PARAMETER_SET_V001.json"
FIELDS = (
    "parameter_key",
    "value",
    "classification",
    "time_layer",
    "production_use",
)


def load_parameter_set(path: Path) -> dict[str, Any]:
    """Load a parameter set in read-only mode."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("parameters"), dict):
        raise ValueError("root 'parameters' must be an object")
    return data


def render_rows(data: dict[str, Any]) -> list[str]:
    rows = ["ID\tparameter_key\tvalue\tclassification\ttime_layer\tproduction_use"]
    for parameter_id, parameter in data["parameters"].items():
        if not isinstance(parameter, dict):
            raise ValueError(f"parameter {parameter_id!r} must be an object")
        missing = [field for field in FIELDS if field not in parameter]
        if missing:
            raise ValueError(f"parameter {parameter_id!r} is missing: {', '.join(missing)}")
        value = json.dumps(parameter["value"], ensure_ascii=False, separators=(",", ":"))
        cells = [parameter_id, parameter["parameter_key"], value]
        cells.extend(parameter[field] for field in FIELDS[2:])
        rows.append("\t".join(str(cell) for cell in cells))
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read an evidence-aware parameter set.")
    parser.add_argument(
        "parameter_set",
        nargs="?",
        type=Path,
        default=DEFAULT_PARAMETER_SET,
        help=f"parameter-set JSON file (default: {DEFAULT_PARAMETER_SET})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = render_rows(load_parameter_set(args.parameter_set))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError) as error:
        print(f"FAIL reader: {error}", file=sys.stderr)
        return 1
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
