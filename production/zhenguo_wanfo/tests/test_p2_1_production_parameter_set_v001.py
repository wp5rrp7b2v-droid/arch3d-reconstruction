"""Source-backed P2.1 checks and mutation tests. No Blender dependency."""

from __future__ import annotations

from copy import deepcopy
import sys
from pathlib import Path
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_p2_1_parameter_set as validation  # noqa: E402
from p2_1_production_preflight import evaluate  # noqa: E402
from read_parameter_set import load_parameter_set, render_rows  # noqa: E402


class P21ProductionParameterSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = validation.read_json(validation.SCHEMA)
        cls.mother = validation.source_rows(validation.P1_MOTHER)
        cls.locked = validation.source_rows(validation.P1_LOCKED)

    def setUp(self):
        self.parameters = validation.read_json(validation.PARAMETERS)
        self.matrix = validation.read_json(validation.DEPENDENCY)

    def check(self):
        return validation.validate_data(self.parameters, self.matrix, self.schema,
                                        self.mother, self.locked)

    def test_full_source_backed_validation_and_reader(self):
        errors, summary = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["parameter_count"], 85)
        self.assertEqual(summary["dependency_count"], 85)
        self.assertEqual(set(self.parameters["parameters"]), set(self.mother))
        self.assertEqual(set(self.matrix["entries"]), set(self.mother))
        self.assertEqual(summary["classification_counts"], validation.EXPECTED_COUNTS)
        self.assertEqual(summary["schema_validation"], "PASS")
        self.assertEqual(summary["three_layer_preservation"], "PASS")
        self.assertEqual(len(render_rows(load_parameter_set(validation.PARAMETERS))), 86)

    def test_missing_parameter_and_matrix_entry_are_detected(self):
        del self.parameters["parameters"]["PM-001"]
        del self.matrix["entries"]["PM-002"]
        errors, _ = self.check()
        self.assertTrue(any("formal parameter IDs differ" in item for item in errors))
        self.assertTrue(any("dependency IDs differ" in item for item in errors))

    def test_duplicate_parameter_key_is_detected(self):
        self.parameters["parameters"]["PM-002"]["parameter_key"] = self.parameters["parameters"]["PM-001"]["parameter_key"]
        errors, _ = self.check()
        self.assertTrue(any("duplicate parameter_key" in item for item in errors))

    def test_classification_and_semantic_layer_drift_are_detected(self):
        self.parameters["parameters"]["PM-003"]["classification"] = "HIGH_CONFIDENCE_INFERENCE"
        self.parameters["parameters"]["PM-003"]["time_layer"] = "reconstructed_963_candidate"
        errors, _ = self.check()
        self.assertTrue(any("classification counts changed" in item for item in errors))
        self.assertTrue(any("PM-003: classification drifted" in item for item in errors))
        self.assertTrue(any("PM-003: time_layer drifted" in item for item in errors))

    def test_schema_rejects_missing_required_field(self):
        del self.parameters["parameters"]["PM-001"]["source_ids"]
        errors, _ = self.check()
        self.assertTrue(any(item.startswith("schema ") for item in errors))

    def test_unknown_value_and_dependency_boundaries(self):
        self.assertEqual(self.parameters["parameters"]["Z-006"]["value"], None)
        self.assertEqual(self.matrix["entries"]["Z-006"]["unknown_dependency_status"], "BLOCKS_P2_2_GEOMETRY")
        self.assertEqual(self.matrix["entries"]["DG-114"]["unknown_dependency_status"], "BOUNDED_NON_BLOCKING")
        self.assertEqual(self.matrix["entries"]["HIS-002"]["unknown_dependency_status"], "METADATA_ONLY_BLOCK")
        self.parameters["parameters"]["Z-006"]["value"] = 3420
        self.matrix["entries"]["Z-006"]["unknown_dependency_status"] = "BOUNDED_NON_BLOCKING"
        errors, _ = self.check()
        self.assertTrue(any("UNKNOWN must have null value" in item for item in errors))
        self.assertTrue(any("Z-006: P2.2 UNKNOWN dependency boundary changed" in item for item in errors))

    def test_reasonable_completion_must_remain_replaceable(self):
        self.parameters["parameters"]["ROOF-010"]["is_replaceable"] = False
        errors, _ = self.check()
        self.assertTrue(any("reasonable completion must be replaceable" in item for item in errors))

    def test_three_layer_and_originality_policies(self):
        self.matrix["semantic_layer_policy"]["distinct_layers"][1] = "reconstructed_963_candidate"
        self.matrix["component_metadata_policy"]["default_originality_status"] = "963_confirmed"
        errors, _ = self.check()
        self.assertTrue(any("three-layer separation" in item for item in errors))
        self.assertTrue(any("component originality metadata" in item for item in errors))

    def test_source_value_and_unit_drift(self):
        self.parameters["parameters"]["PM-008"]["value"] = 14.6
        self.parameters["parameters"]["PM-008"]["unit"] = "mm"
        errors, _ = self.check()
        self.assertTrue(any("PM-008: value differs" in item for item in errors))
        self.assertTrue(any("PM-008: unit" in item for item in errors))

    def test_preflight_hold_is_data_driven(self):
        errors, summary = self.check()
        result = evaluate(errors, summary, self.matrix)
        self.assertEqual(result["machine_validation"], "PASS")
        self.assertEqual(result["production_preflight"], "HOLD")
        self.assertEqual(result["geometry_critical_unresolved_blocker_count"], 1)
        self.assertEqual(result["blockers"][0]["parameter_key"], "column_height_963_design_mm")
        synthetic = deepcopy(self.matrix)
        synthetic["entries"]["Z-006"]["unknown_dependency_status"] = "BOUNDED_NON_BLOCKING"
        self.assertEqual(evaluate([], summary, synthetic)["production_preflight"], "PASS")
        self.assertTrue(validation.validate_data(self.parameters, synthetic, self.schema,
                                                self.mother, self.locked)[0])

    def test_scripts_are_read_only_and_blender_free(self):
        self.assertEqual(validation.check_read_only_python(), [])


if __name__ == "__main__":
    unittest.main()
