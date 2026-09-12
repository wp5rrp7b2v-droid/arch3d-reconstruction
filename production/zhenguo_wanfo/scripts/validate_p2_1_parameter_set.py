#!/usr/bin/env python3
"""Read-only validation of the P2.1 production data against locked P1 inputs."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from importlib.metadata import version
import json
from pathlib import Path
import re
import sys

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CASE = ROOT / "production/zhenguo_wanfo"
PARAMETERS = CASE / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
DEPENDENCY = CASE / "dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json"
SCHEMA = CASE / "schema/evidence_aware_parameter_schema_v001.json"
P1_LOCKED = ROOT / "docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md"
P1_MOTHER = ROOT / "docs/evidence/zhenguo_wanfo/P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md"
EXPECTED_COUNTS = {"CONFIRMED": 46, "HIGH_CONFIDENCE_INFERENCE": 32,
                   "REASONABLE_COMPLETION": 4, "UNKNOWN": 3}
ROLES = {"DIRECT_GEOMETRY_INPUT", "DERIVED_GEOMETRY_RULE", "VALIDATION_REFERENCE",
         "METADATA_ONLY", "NOT_USED_IN_P2_2"}
UNKNOWN_STATUSES = {"BLOCKS_P2_2_GEOMETRY", "BOUNDED_NON_BLOCKING", "METADATA_ONLY_BLOCK"}
THREE_LAYERS = ["observed_as_measured", "report_ideal_model", "reconstructed_963_candidate"]
REQUIRED_METADATA_FIELDS = ["historical_state_tag", "evidence_class", "source_layer", "originality_status"]
RANGES = {"Z-003", "DEF-001", "DEF-002", "DEF-003", "DEF-004", "DEF-005", "DEF-006"}
TEXT_VALUES = {"DG-001", "DG-002", "RF-001", "HIS-001"}
UNKNOWN_IDS = {"Z-006", "DG-114", "HIS-002"}


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def source_rows(path: Path) -> dict[str, list[str]]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| (?:PM|MOD|Z|DG|RF|FR|OUT|ROOF|DEF|HIS)-\d+ \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] in result:
            raise ValueError(f"duplicate locked source ID: {cells[0]}")
        result[cells[0]] = cells
    return result


def source_value(ident: str, cell: str):
    raw = cell.replace("**", "").strip()
    if ident in UNKNOWN_IDS:
        return None
    if ident == "Z-007":
        return "Z = 0; abstract column-foot design plane"
    if ident in RANGES:
        match = re.fullmatch(r"(\d+(?:\.\d+)?)[–-](\d+(?:\.\d+)?)", raw)
        if not match:
            raise ValueError(f"unreadable source range: {ident}: {raw}")
        return [float(item) if "." in item else int(item) for item in match.groups()]
    if ident == "FR-007":
        if raw != "120 / 115 / 210":
            raise ValueError(f"changed source sequence: {ident}: {raw}")
        return [120, 115, 210]
    if ident in TEXT_VALUES:
        return raw
    match = re.fullmatch(r"≈?(\d+(?:\.\d+)?)(?:尺|分)?", raw)
    if not match:
        raise ValueError(f"unreadable source value: {ident}: {raw}")
    item = match.group(1)
    return float(item) if "." in item else int(item)


def validate_data(parameter_set: dict, matrix: dict, schema: dict,
                  mother: dict[str, list[str]], locked: dict[str, list[str]]) -> tuple[list[str], dict]:
    errors: list[str] = []
    Draft202012Validator.check_schema(schema)
    for error in Draft202012Validator(schema).iter_errors(parameter_set):
        errors.append(f"schema {list(error.absolute_path)}: {error.message}")
    parameters = parameter_set.get("parameters", {})
    entries = matrix.get("entries", {})
    if not isinstance(parameters, dict) or not isinstance(entries, dict):
        return errors + ["parameters and entries must be objects"], {}
    source_ids = set(mother)
    if len(source_ids) != 85 or set(locked) != source_ids:
        errors.append("authoritative P1 ID lists are not identical 85-item sets")
    if len(parameters) != 85 or set(parameters) != source_ids:
        errors.append(f"formal parameter IDs differ from locked 85 IDs: missing={sorted(source_ids-set(parameters))}, extra={sorted(set(parameters)-source_ids)}")
    if len(entries) != 85 or set(entries) != source_ids:
        errors.append(f"dependency IDs differ from locked 85 IDs: missing={sorted(source_ids-set(entries))}, extra={sorted(set(entries)-source_ids)}")
    keys = [p.get("parameter_key") for p in parameters.values() if isinstance(p, dict)]
    if len(keys) != len(set(keys)):
        errors.append("duplicate parameter_key")
    counts = Counter(p.get("classification") for p in parameters.values() if isinstance(p, dict))
    if dict(counts) != EXPECTED_COUNTS:
        errors.append(f"classification counts changed: {dict(counts)}")
    for ident in sorted(source_ids & set(parameters)):
        p = parameters[ident]
        if not isinstance(p, dict):
            errors.append(f"{ident}: parameter must be an object")
            continue
        m, q = mother[ident], locked[ident]
        expected = {"parameter_key": m[1].strip("`"), "classification": q[1],
                    "production_use": q[2].strip("`"),
                    "time_layer": "observed_current_topology" if q[3].strip("`") == "observed/current topology" else q[3].strip("`"),
                    "source_layer": q[4].strip("`"), "blocking_level": q[5].replace("*", "")}
        for field, value in expected.items():
            if p.get(field) != value:
                errors.append(f"{ident}: {field} drifted from locked P1/V002")
        if ident == "Z-007":
            # The V002 unknown was explicitly resolved by P1.3 HR-01B.
            if p.get("value") != source_value(ident, m[3]):
                errors.append("Z-007: project coordinate rule differs from P1.3 HR-01B")
        elif p.get("value") != source_value(ident, m[3]):
            errors.append(f"{ident}: value differs from V002 candidate")
        unit = next((value for suffix, value in (("_mm", "mm"), ("_fen", "fen"), ("_chi", "chi"))
                     if expected["parameter_key"].endswith(suffix)), None)
        if p.get("unit") != unit:
            errors.append(f"{ident}: unit does not match the locked parameter key")
        if not p.get("source_ids"):
            errors.append(f"{ident}: missing source_ids")
        if p.get("classification") == "UNKNOWN" and p.get("value") is not None:
            errors.append(f"{ident}: UNKNOWN must have null value")
        if p.get("classification") == "REASONABLE_COMPLETION" and p.get("is_replaceable") is not True:
            errors.append(f"{ident}: reasonable completion must be replaceable")
        if ident in {"Z-001", "MOD-006", "ROOF-011"} and "约" not in p.get("notes", ""):
            errors.append(f"{ident}: approximate source semantics lost")
    for ident in sorted(source_ids & set(entries)):
        e = entries[ident]
        p = parameters.get(ident, {})
        if not isinstance(e, dict) or not isinstance(p, dict):
            errors.append(f"{ident}: dependency or parameter is not an object")
            continue
        for field in ("parameter_key", "geometry_dependency_role", "p2_2_target", "requires_numeric_value",
                      "unknown_dependency_status", "blocking_reason", "resolution_required_before_p2_2", "notes"):
            if field not in e:
                errors.append(f"{ident}: missing dependency field {field}")
        if e.get("parameter_key") != p.get("parameter_key"):
            errors.append(f"{ident}: dependency parameter_key mismatch")
        role = e.get("geometry_dependency_role")
        if role not in ROLES:
            errors.append(f"{ident}: illegal dependency role")
        if not isinstance(e.get("requires_numeric_value"), bool) or not isinstance(e.get("resolution_required_before_p2_2"), bool):
            errors.append(f"{ident}: dependency flags must be boolean")
        if not isinstance(e.get("p2_2_target"), str) or not e.get("p2_2_target"):
            errors.append(f"{ident}: missing P2.2 target")
        if p.get("classification") == "UNKNOWN":
            status = e.get("unknown_dependency_status")
            if status not in UNKNOWN_STATUSES or not e.get("blocking_reason"):
                errors.append(f"{ident}: UNKNOWN needs legal dependency status and reason")
            if status == "BLOCKS_P2_2_GEOMETRY" and (role not in {"DIRECT_GEOMETRY_INPUT", "DERIVED_GEOMETRY_RULE"} or not e.get("resolution_required_before_p2_2")):
                errors.append(f"{ident}: geometry blocker must be a required geometry input")
            if status == "METADATA_ONLY_BLOCK" and role != "METADATA_ONLY":
                errors.append(f"{ident}: metadata blocker must have metadata role")
        elif e.get("unknown_dependency_status") is not None or e.get("blocking_reason") is not None:
            errors.append(f"{ident}: non-UNKNOWN has fabricated UNKNOWN status")
    # These decisions follow the approved P2.2 scope and P1.3 high-risk boundaries.
    required_unknown_decisions = {
        "Z-006": ("DIRECT_GEOMETRY_INPUT", "BLOCKS_P2_2_GEOMETRY", True, True),
        "DG-114": ("NOT_USED_IN_P2_2", "BOUNDED_NON_BLOCKING", False, False),
        "HIS-002": ("METADATA_ONLY", "METADATA_ONLY_BLOCK", False, False),
    }
    for ident, expected in required_unknown_decisions.items():
        entry = entries.get(ident, {})
        actual = (entry.get("geometry_dependency_role"), entry.get("unknown_dependency_status"),
                  entry.get("requires_numeric_value"), entry.get("resolution_required_before_p2_2"))
        if actual != expected:
            errors.append(f"{ident}: P2.2 UNKNOWN dependency boundary changed")
    policy = matrix.get("semantic_layer_policy", {})
    if policy.get("distinct_layers") != THREE_LAYERS or policy.get("report_ideal_model_parameter_ids") != [ident for ident,p in parameters.items() if isinstance(p,dict) and p.get("time_layer")=="report_ideal_model"]:
        errors.append("three-layer separation policy missing or relabelled")
    metadata = matrix.get("component_metadata_policy", {})
    if metadata.get("required_fields") != REQUIRED_METADATA_FIELDS or metadata.get("default_originality_status") != "unknown" or metadata.get("prohibited_automatic_status") != "963_confirmed":
        errors.append("component originality metadata rule missing or unsafe")
    blockers = [ident for ident, e in entries.items() if isinstance(e, dict) and e.get("unknown_dependency_status") == "BLOCKS_P2_2_GEOMETRY"]
    summary = {"parameter_count": len(parameters), "classification_counts": dict(counts),
               "dependency_count": len(entries), "unknown_ids": sorted(ident for ident,p in parameters.items() if isinstance(p,dict) and p.get("classification")=="UNKNOWN"),
               "reasonable_completion_ids": sorted(ident for ident,p in parameters.items() if isinstance(p,dict) and p.get("classification")=="REASONABLE_COMPLETION"),
               "geometry_critical_unresolved_blockers": sorted(blockers),
               "schema_validation": "PASS" if not list(Draft202012Validator(schema).iter_errors(parameter_set)) else "FAIL",
               "three_layer_preservation": "PASS" if not any("layer" in x or "time_layer" in x for x in errors) else "FAIL"}
    return errors, summary


def check_read_only_python() -> list[str]:
    errors = []
    for path in (CASE / "scripts/validate_p2_1_parameter_set.py", CASE / "scripts/p2_1_production_preflight.py",
                 CASE / "scripts/validate_p2_1_approved_override.py"):
        if not path.exists():
            errors.append(f"missing read-only script: {path.name}")
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                if any(name == "bpy" or name.startswith("bpy.") or name in {"subprocess", "blendfile"} for name in names):
                    errors.append(f"{path.name}: Blender execution/import dependency")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"write_text", "write_bytes", "mkdir", "touch", "unlink"}:
                errors.append(f"{path.name}: write operation in read-only script")
    return errors


def run() -> tuple[list[str], dict]:
    parameter_set, matrix, schema = read_json(PARAMETERS), read_json(DEPENDENCY), read_json(SCHEMA)
    errors, summary = validate_data(parameter_set, matrix, schema, source_rows(P1_MOTHER), source_rows(P1_LOCKED))
    errors.extend(check_read_only_python())
    summary["python_version"] = sys.version.split()[0]
    summary["jsonschema_version"] = version("jsonschema")
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable validation result")
    args = parser.parse_args()
    try:
        errors, summary = run()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors, summary = [str(exc)], {}
    result = {"validation": "FAIL" if errors else "PASS", "errors": errors, **summary}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["validation"], json.dumps(result, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
