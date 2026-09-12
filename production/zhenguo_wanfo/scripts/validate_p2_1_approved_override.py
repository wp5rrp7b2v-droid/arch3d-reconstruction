#!/usr/bin/env python3
"""Validate D-023's separate, formula-driven production override without geometry."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

import validate_p2_1_parameter_set as base


OVERRIDES = base.CASE / "params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json"
DECISIONS = base.ROOT / "docs/project_control/decision_log.md"
EVIDENCE = base.ROOT / "docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md"
HIGH_RISK = base.ROOT / "docs/evidence/zhenguo_wanfo/P1_3_HIGH_RISK_CLASSIFICATION_V001.md"
CANDIDATE_ID = "Z-006-RC-01"
CLAIM_BOUNDARY = "仅为reconstructed_963_candidate的可替换生产解析值，不是已证实的963年原设计柱高。"
EXPECTED_FIELDS = {
    "candidate_id": CANDIDATE_ID,
    "target_parameter_id": "Z-006",
    "target_parameter_key": "column_height_963_design_mm",
    "classification": "REASONABLE_COMPLETION",
    "time_layer": "reconstructed_963_candidate",
    "production_use": "DEFAULT_REPLACEABLE_CANDIDATE",
    "formula": "11 * MOD-006",
    "depends_on": ["MOD-006"],
    "unit": "mm",
    "is_replaceable": True,
    "approval_decision_id": "D-023",
    "status": "APPROVED_FOR_P2_2_CANDIDATE_USE",
    "historical_claim_boundary": CLAIM_BOUNDARY,
}


def check_approval_sources() -> list[str]:
    """Make sure the sidecar's three cited anchors still exist and say what it claims."""
    errors = []
    decision_lines = DECISIONS.read_text(encoding="utf-8").splitlines()
    decision = next((line for line in decision_lines if line.startswith("| **D-023** |")), "")
    if not all(token in decision for token in ("Product Owner 批准", "11 × MOD-006", "3534.3mm",
                                                "REASONABLE_COMPLETION", "ACTIVE")):
        errors.append("D-023 approval text missing or inconsistent with the candidate")
    evidence = EVIDENCE.read_text(encoding="utf-8")
    e018 = evidence.split("### E-018", 1)[-1].split("### E-019", 1)[0]
    if "### E-018" not in evidence or "11足材" not in e018 or "作者假说" not in e018:
        errors.append("E-018 hypothesis boundary missing")
    high_risk = HIGH_RISK.read_text(encoding="utf-8")
    hr01a = high_risk.split("### HR-01A", 1)[-1].split("### HR-01B", 1)[0]
    if "### HR-01A" not in high_risk or "UNKNOWN" not in hr01a or "null / unknown" not in hr01a:
        errors.append("HR-01A historical UNKNOWN boundary missing")
    return errors


def validate_override(parameter_set: dict, matrix: dict, sidecar: dict | None) -> tuple[list[str], dict | None]:
    """Return errors and a resolution only after every approval and formula check passes."""
    errors = check_approval_sources()
    parameters = parameter_set.get("parameters", {}) if isinstance(parameter_set, dict) else {}
    entries = matrix.get("entries", {}) if isinstance(matrix, dict) else {}
    parameters = parameters if isinstance(parameters, dict) else {}
    entries = entries if isinstance(entries, dict) else {}
    historical = parameters.get("Z-006", {})
    dependency = entries.get("Z-006", {})
    historical = historical if isinstance(historical, dict) else {}
    dependency = dependency if isinstance(dependency, dict) else {}
    if (historical.get("classification"), historical.get("value"), historical.get("production_use"),
            historical.get("parameter_key")) != ("UNKNOWN", None, "DO_NOT_LOCK", "column_height_963_design_mm"):
        errors.append("Z-006 must remain UNKNOWN / null / DO_NOT_LOCK")
    if (dependency.get("unknown_dependency_status") != "BLOCKS_P2_2_GEOMETRY"
            or dependency.get("parameter_key") != "column_height_963_design_mm"):
        errors.append("Z-006 historical geometry dependency must remain blocking")
    if sidecar is None:
        return errors + ["approved override sidecar missing"], None
    if not isinstance(sidecar, dict) or sidecar.get("override_set_version") != "V001":
        return errors + ["invalid override sidecar root/version"], None
    overrides = sidecar.get("overrides")
    if not isinstance(overrides, dict) or set(overrides) != {CANDIDATE_ID}:
        return errors + ["sidecar must contain only Z-006-RC-01"], None
    candidate = overrides[CANDIDATE_ID]
    if not isinstance(candidate, dict):
        return errors + ["Z-006-RC-01 must be an object"], None
    if CANDIDATE_ID in parameters:
        errors.append("Z-006-RC-01 was merged into the historical 85 parameters")
    for field, expected in EXPECTED_FIELDS.items():
        if candidate.get(field) != expected or (field == "is_replaceable" and type(candidate.get(field)) is not bool):
            errors.append(f"Z-006-RC-01: invalid {field}")
    if type(candidate.get("multiplier")) is not int or candidate["multiplier"] != 11:
        errors.append("Z-006-RC-01: multiplier must be the D-023 integer 11")
    basis = candidate.get("evidence_basis")
    if (not isinstance(basis, list) or not all(isinstance(item, str) for item in basis)
            or len(basis) != len(set(basis)) or not {"E-018", "HR-01A", "D-023"}.issubset(set(basis))):
        errors.append("Z-006-RC-01: evidence_basis must cite E-018, HR-01A, and D-023")
    mod = parameters.get("MOD-006", {})
    mod = mod if isinstance(mod, dict) else {}
    mod_value = mod.get("value")
    if (mod.get("parameter_key") != "full_cai_height_mm" or mod.get("unit") != "mm"
            or type(mod_value) not in (int, float)):
        return errors + ["MOD-006 must provide a numeric full_cai_height_mm in mm"], None
    try:
        input_value = Decimal(str(mod_value))
        resolved = Decimal("11") * input_value
        cached = candidate.get("current_resolved_value")
        if type(cached) not in (int, float):
            raise InvalidOperation("cached value is not numeric")
        cached_decimal = Decimal(str(cached))
        if not input_value.is_finite() or not cached_decimal.is_finite() or cached_decimal != resolved:
            errors.append(f"Z-006-RC-01: stale resolved value; 11 * MOD-006 = {resolved} mm")
    except (InvalidOperation, ValueError):
        return errors + ["Z-006-RC-01: invalid numeric resolution"], None
    if errors:
        return errors, None
    return [], {"candidate_id": CANDIDATE_ID, "target_parameter_id": "Z-006",
                "target_parameter_key": "column_height_963_design_mm", "mod_006_value": float(input_value),
                "resolved_value": float(resolved), "unit": "mm"}


def run() -> tuple[list[str], dict, dict | None]:
    base_errors, summary = base.run()
    parameter_set = base.read_json(base.PARAMETERS)
    matrix = base.read_json(base.DEPENDENCY)
    sidecar = base.read_json(OVERRIDES) if OVERRIDES.exists() else None
    override_errors, resolution = validate_override(parameter_set, matrix, sidecar)
    errors = base_errors + override_errors
    return errors, summary, resolution if not errors else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        errors, summary, resolution = run()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors, summary, resolution = [str(exc)], {}, None
    result = {"validation": "FAIL" if errors else "PASS", "errors": errors,
              "candidate_resolution": resolution, **summary}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["validation"], json.dumps(result, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
