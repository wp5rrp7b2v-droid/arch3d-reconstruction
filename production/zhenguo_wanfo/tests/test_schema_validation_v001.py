#!/usr/bin/env python3
"""Executable acceptance tests for T-005 P2.0 schema validation."""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


WANFO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = WANFO_ROOT / "schema" / "evidence_aware_parameter_schema_v001.json"
POSITIVE_PATH = WANFO_ROOT / "params" / "P2_0_MINIMAL_PARAMETER_SET_V001.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
NEGATIVE_UNKNOWN_PATH = FIXTURES / "P2_0_INVALID_UNKNOWN_HARD_LOCK_V001.json"
NEGATIVE_REASONABLE_PATH = (
    FIXTURES / "P2_0_INVALID_REASONABLE_COMPLETION_NON_REPLACEABLE_V001.json"
)
THREE_LAYER_PATH = FIXTURES / "P2_0_VALID_THREE_LAYER_COEXISTENCE_V001.json"
VALIDATOR_SCRIPT = WANFO_ROOT / "scripts" / "validate_parameter_set.py"
READER_SCRIPT = WANFO_ROOT / "scripts" / "read_parameter_set.py"


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class EvidenceAwareSchemaValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def run_validator(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR_SCRIPT), str(path)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_positive_minimal_set_covers_four_classes(self) -> None:
        instance = load_json(POSITIVE_PATH)
        self.assertEqual(list(self.validator.iter_errors(instance)), [])
        classifications = {
            item["classification"] for item in instance["parameters"].values()
        }
        self.assertEqual(
            classifications,
            {
                "CONFIRMED",
                "HIGH_CONFIDENCE_INFERENCE",
                "REASONABLE_COMPLETION",
                "UNKNOWN",
            },
        )
        result = self.run_validator(POSITIVE_PATH)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_negative_01_unknown_do_not_lock_rejects_number(self) -> None:
        instance = load_json(NEGATIVE_UNKNOWN_PATH)
        errors = list(self.validator.iter_errors(instance))
        target_errors = [
            error
            for error in errors
            if list(error.absolute_path) == ["parameters", "Z-006", "value"]
            and error.validator == "type"
        ]
        self.assertEqual(len(target_errors), 1, [error.message for error in errors])
        result = self.run_validator(NEGATIVE_UNKNOWN_PATH)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Z-006", result.stdout)
        self.assertIn("value", result.stdout)

    def test_negative_02_reasonable_completion_must_be_replaceable(self) -> None:
        instance = load_json(NEGATIVE_REASONABLE_PATH)
        errors = list(self.validator.iter_errors(instance))
        target_errors = [
            error
            for error in errors
            if list(error.absolute_path) == ["parameters", "Z-005", "is_replaceable"]
            and error.validator == "const"
        ]
        self.assertEqual(len(target_errors), 1, [error.message for error in errors])
        result = self.run_validator(NEGATIVE_REASONABLE_PATH)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Z-005", result.stdout)
        self.assertIn("is_replaceable", result.stdout)

    def test_reader_smoke_is_read_only_and_blender_free(self) -> None:
        tree = ast.parse(READER_SCRIPT.read_text(encoding="utf-8"))
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        self.assertNotIn("bpy", imported_roots)

        result = subprocess.run(
            [sys.executable, str(READER_SCRIPT), str(POSITIVE_PATH)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "ID\tparameter_key\tvalue\tclassification\ttime_layer\tproduction_use",
            result.stdout,
        )
        for parameter_id in ("PM-003", "PM-008", "Z-005", "Z-006"):
            self.assertIn(parameter_id, result.stdout)

    def test_three_layer_coexistence_fixture_validates(self) -> None:
        instance = load_json(THREE_LAYER_PATH)
        self.assertEqual(list(self.validator.iter_errors(instance)), [])
        result = self.run_validator(THREE_LAYER_PATH)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_three_layer_reader_preserves_exact_time_layers(self) -> None:
        spec = importlib.util.spec_from_file_location("p2_parameter_reader", READER_SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reader)

        data = reader.load_parameter_set(THREE_LAYER_PATH)
        expected_by_id = {
            "PM-TL-OBS": "observed_as_measured",
            "MOD-TL-IDEAL": "report_ideal_model",
            "Z-TL-963": "reconstructed_963_candidate",
        }
        actual_by_id = {
            parameter_id: parameter["time_layer"]
            for parameter_id, parameter in data["parameters"].items()
        }
        self.assertEqual(actual_by_id, expected_by_id)
        self.assertEqual(set(actual_by_id), set(expected_by_id))
        self.assertEqual(set(actual_by_id.values()), set(expected_by_id.values()))

        result = subprocess.run(
            [sys.executable, str(READER_SCRIPT), str(THREE_LAYER_PATH)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output_rows = {
            cells[0]: cells[4]
            for line in result.stdout.splitlines()[1:]
            if len(cells := line.split("\t")) == 6
        }
        self.assertEqual(output_rows, expected_by_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
