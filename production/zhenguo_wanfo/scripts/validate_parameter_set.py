#!/usr/bin/env python3
"""Validate an evidence-aware parameter set without invoking Blender."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError:
    print("FAIL dependency: Python package 'jsonschema' is required", file=sys.stderr)
    raise SystemExit(2)


WANFO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = WANFO_ROOT / "schema" / "evidence_aware_parameter_schema_v001.json"


def load_json(path: Path) -> Any:
    """Load JSON from *path* without modifying it."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def format_path(parts: Iterable[object]) -> str:
    """Format a jsonschema path as a concise JSON-style location."""
    location = "$"
    for part in parts:
        if isinstance(part, int):
            location += f"[{part}]"
        elif str(part).replace("_", "").replace("-", "").isalnum():
            location += f".{part}"
        else:
            location += f"[{part!r}]"
    return location


def build_validator(schema_path: Path) -> Draft202012Validator:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_file(schema_path: Path, parameter_set_path: Path) -> list[str]:
    validator = build_validator(schema_path)
    instance = load_json(parameter_set_path)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [f"{format_path(error.absolute_path)}: {error.message}" for error in errors]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an Evidence-aware Parameter Schema parameter set."
    )
    parser.add_argument("parameter_set", type=Path, help="parameter-set JSON file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help=f"JSON Schema file (default: {DEFAULT_SCHEMA})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        errors = validate_file(args.schema, args.parameter_set)
    except FileNotFoundError as error:
        print(f"FAIL file: {error.filename}: not found", file=sys.stderr)
        return 2
    except json.JSONDecodeError as error:
        print(
            f"FAIL JSON: {error.msg} at line {error.lineno}, column {error.colno}",
            file=sys.stderr,
        )
        return 2
    except SchemaError as error:
        print(f"FAIL schema: {format_path(error.absolute_path)}: {error.message}", file=sys.stderr)
        return 2

    if errors:
        print(f"FAIL {args.parameter_set}: {len(errors)} validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS {args.parameter_set}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
