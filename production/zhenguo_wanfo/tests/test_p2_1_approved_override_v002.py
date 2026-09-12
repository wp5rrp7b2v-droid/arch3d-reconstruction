"""D-023 candidate resolution and mutation checks; data only, no geometry."""

from __future__ import annotations

from copy import deepcopy
import sys
from pathlib import Path
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_p2_1_parameter_set as base  # noqa: E402
import validate_p2_1_approved_override as approved  # noqa: E402
from p2_1_production_preflight import evaluate  # noqa: E402


class ApprovedOverrideV002Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = base.read_json(base.SCHEMA)
        cls.mother = base.source_rows(base.P1_MOTHER)
        cls.locked = base.source_rows(base.P1_LOCKED)

    def setUp(self):
        self.parameters = base.read_json(base.PARAMETERS)
        self.matrix = base.read_json(base.DEPENDENCY)
        self.sidecar = base.read_json(approved.OVERRIDES)

    def preflight(self, sidecar=None, use_default=True):
        errors, summary = base.validate_data(self.parameters, self.matrix, self.schema,
                                             self.mother, self.locked)
        selected = self.sidecar if use_default else sidecar
        return evaluate(errors, summary, self.matrix, self.parameters, selected, require_override=True)

    def assert_hold(self, result):
        self.assertEqual(result["production_preflight"], "HOLD")
        self.assertEqual(result["approved_candidate_resolution_count"], 0)
        self.assertEqual(result["geometry_critical_unresolved_blocker_count"], 1)

    def test_approved_candidate_resolves_only_the_unresolved_count(self):
        result = self.preflight()
        self.assertEqual(result["production_preflight"], "PASS")
        self.assertEqual(result["machine_validation"], "PASS")
        self.assertEqual(result["candidate_validation"], "PASS")
        self.assertEqual(result["geometry_critical_historical_unknown_count"], 1)
        self.assertEqual(result["approved_candidate_resolution_count"], 1)
        self.assertEqual(result["geometry_critical_unresolved_blocker_count"], 0)
        self.assertEqual(result["approved_candidate_resolution"]["resolved_value"], 3534.3)
        self.assertEqual(self.parameters["parameters"]["Z-006"]["value"], None)
        self.assertEqual(self.matrix["entries"]["Z-006"]["unknown_dependency_status"], "BLOCKS_P2_2_GEOMETRY")
        self.assertNotIn("Z-006-RC-01", self.parameters["parameters"])
        self.assertEqual(len(self.parameters["parameters"]), 85)
        self.assertEqual(result["classification_counts"], base.EXPECTED_COUNTS)

    def test_missing_or_extra_override_holds(self):
        self.assert_hold(self.preflight(None, use_default=False))
        self.sidecar["overrides"]["UNAPPROVED"] = deepcopy(self.sidecar["overrides"]["Z-006-RC-01"])
        self.assert_hold(self.preflight())

    def test_historical_z006_mutations_hold(self):
        for field, altered in (("value", 3534.3), ("classification", "REASONABLE_COMPLETION"),
                               ("production_use", "DEFAULT_REPLACEABLE_CANDIDATE")):
            with self.subTest(field=field):
                original = self.parameters["parameters"]["Z-006"][field]
                self.parameters["parameters"]["Z-006"][field] = altered
                self.assert_hold(self.preflight())
                self.parameters["parameters"]["Z-006"][field] = original

    def test_dependency_mutation_cannot_clear_historical_blocker(self):
        self.matrix["entries"]["Z-006"]["unknown_dependency_status"] = "BOUNDED_NON_BLOCKING"
        result = self.preflight()
        self.assertEqual(result["production_preflight"], "HOLD")
        self.assertEqual(result["machine_validation"], "FAIL")
        self.assertEqual(result["approved_candidate_resolution_count"], 0)
        self.assertTrue(any("dependency" in item for item in result["validation_errors"]))

    def test_approval_and_candidate_identity_mutations_hold(self):
        changes = {
            "approval_decision_id": "D-022",
            "candidate_id": "Z-006",
            "target_parameter_id": "MOD-006",
            "target_parameter_key": "wrong_key",
            "classification": "CONFIRMED",
            "time_layer": "observed_as_measured",
            "production_use": "DO_NOT_LOCK",
            "is_replaceable": False,
            "status": "DRAFT",
        }
        for field, altered in changes.items():
            with self.subTest(field=field):
                sidecar = deepcopy(self.sidecar)
                sidecar["overrides"]["Z-006-RC-01"][field] = altered
                self.assert_hold(self.preflight(sidecar, use_default=False))

    def test_formula_dependency_and_multiplier_mutations_hold(self):
        for field, altered in (("formula", "11 * Z-006"), ("depends_on", ["Z-006"]),
                               ("multiplier", 12), ("multiplier", True)):
            with self.subTest(field=field, altered=altered):
                sidecar = deepcopy(self.sidecar)
                sidecar["overrides"]["Z-006-RC-01"][field] = altered
                self.assert_hold(self.preflight(sidecar, use_default=False))

    def test_changed_mod_requires_recomputed_cache_and_formal_review(self):
        self.parameters["parameters"]["MOD-006"]["value"] = 322.3
        override_errors, resolution = approved.validate_override(self.parameters, self.matrix, self.sidecar)
        self.assertIsNone(resolution)
        self.assertTrue(any("stale resolved value" in item and "3545.3" in item for item in override_errors))
        self.assert_hold(self.preflight())
        updated = deepcopy(self.sidecar)
        updated["overrides"]["Z-006-RC-01"]["current_resolved_value"] = 3545.3
        override_errors, resolution = approved.validate_override(self.parameters, self.matrix, updated)
        self.assertEqual(override_errors, [])
        self.assertEqual(resolution["resolved_value"], 3545.3)
        # A changed formal MOD-006 still needs its own source-backed review.
        self.assertEqual(self.preflight(updated, use_default=False)["production_preflight"], "HOLD")

    def test_cached_value_and_approval_evidence_mutations_hold(self):
        for field, altered in (("current_resolved_value", 3534.4),
                               ("current_resolved_value", "3534.3"),
                               ("evidence_basis", ["E-018", "D-023"]),
                               ("historical_claim_boundary", "963设计柱高已证实")):
            with self.subTest(field=field, altered=altered):
                sidecar = deepcopy(self.sidecar)
                sidecar["overrides"]["Z-006-RC-01"][field] = altered
                self.assert_hold(self.preflight(sidecar, use_default=False))

    def test_override_does_not_enter_historical_parameter_set(self):
        self.parameters["parameters"]["Z-006-RC-01"] = deepcopy(self.parameters["parameters"]["Z-006"])
        self.assert_hold(self.preflight())

    def test_read_only_scripts_have_no_blender_dependency(self):
        self.assertEqual(base.check_read_only_python(), [])


if __name__ == "__main__":
    unittest.main()
