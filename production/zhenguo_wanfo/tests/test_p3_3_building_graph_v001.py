import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "production/zhenguo_wanfo/scripts"
sys.path.insert(0, str(SCRIPTS))

from build_p3_3_building_graph_v001 import OUTPUTS, compile_assets  # noqa: E402
from validate_p3_3_building_graph_v001 import (  # noqa: E402
    CLASSIFICATIONS,
    HARD_FAILS,
    mutate,
    validate,
)


class BuildingGraphTests(unittest.TestCase):
    def setUp(self):
        self.assets = compile_assets()

    def assert_rejected_after(self, mutation, expected_failure):
        changed = copy.deepcopy(self.assets)
        mutation(changed)
        self.assertIn(expected_failure, validate(changed))

    def test_canonical_assets_validate(self):
        self.assertEqual(validate(self.assets), [])

    def test_accounting_is_complete(self):
        summary = self.assets["accounting"]["summary"]
        self.assertEqual((summary["families_accounted"], summary["variants_accounted"], summary["instances_accounted"]), (11, 40, 365))
        self.assertEqual((summary["unexplained_omissions"], summary["orphan_identities"]), (0, 0))

    def test_five_negative_fixtures_are_rejected(self):
        fixtures = sorted((ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3").glob("*.json"))
        for path in fixtures:
            fixture = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn(fixture["expected_hard_fail"], validate(mutate(self.assets, fixture)), path.name)
        self.assertEqual(len(fixtures), 5)

    def test_hf01_fixture_injects_true_six_chuanfu_reference_leak(self):
        fixture = json.loads((ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3/REFERENCE_LENGTH_LEAKS_INTO_BUILDING.json").read_text(encoding="utf-8"))
        injected = fixture["mutation"]["injected_dimension"]
        self.assertEqual((injected["source_parameter"], injected["value_mm"], injected["use"]), ("canonical_reference_length_mm", 1000, "ACTUAL_FULL_LENGTH"))
        self.assertIn(HARD_FAILS[0], validate(mutate(self.assets, fixture)))

    def test_hf03_fixture_injects_true_p2_numeric_transform(self):
        fixture = json.loads((ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3/BAKED_MANUAL_BUILDING.json").read_text(encoding="utf-8"))
        transform = fixture["mutation"]["injected_p2_transform"]
        self.assertEqual(set(transform), {"location_mm", "rotation_euler_rad", "scale"})
        self.assertIn(HARD_FAILS[2], validate(mutate(self.assets, fixture)))

    def test_all_four_input_classifications_are_required(self):
        self.assertEqual(set(self.assets["baseline"]["input_classifications"]), CLASSIFICATIONS)
        self.assert_rejected_after(lambda docs: docs["baseline"]["input_classifications"].pop("COMPARISON_ONLY"), "INPUT_CLASSIFICATION_INCOMPLETE")

    def test_required_authoritative_input_coverage_is_enforced(self):
        self.assert_rejected_after(
            lambda docs: docs["baseline"]["inputs"].__setitem__(
                slice(None),
                [item for item in docs["baseline"]["inputs"] if not item["path"].endswith("P3_2_INTERFACE_REGISTRY_V001.json")],
            ),
            "AUTHORITATIVE_INPUT_COVERAGE_INCOMPLETE",
        )

    def test_explicit_parameter_to_graph_rule_bindings_are_required(self):
        def weaken(docs):
            docs["bindings"]["bindings"][0]["binding_targets"] = {"graph_node_ids": [], "relationship_types": [], "rule_ids": []}

        self.assert_rejected_after(weaken, "PARAMETER_GRAPH_RULE_BINDING_INCOMPLETE")

    def test_building_and_assembly_organization_layer_is_required(self):
        def flatten(docs):
            relation = next(item for item in docs["graph"]["relationships"] if item["source_node"].startswith("P3_3:"))
            relation["target_node"] = "BUILDING_ROOT"

        self.assert_rejected_after(flatten, "BUILDING_ORGANIZATION_HIERARCHY_INVALID")

    def test_p3_2_traceability_is_required(self):
        self.assert_rejected_after(lambda docs: docs["graph"].pop("p3_2_foundation_reuse"), "P3_2_TRACEABILITY_INCOMPLETE")

    def test_stable_serialization_matches_committed_outputs(self):
        for name, value in self.assets.items():
            self.assertEqual(json.loads(OUTPUTS[name].read_text(encoding="utf-8")), value, name)

    def test_no_p2_numeric_transform_in_generated_assets(self):
        graph_text = json.dumps(self.assets["graph"], sort_keys=True)
        self.assertNotIn('"location_mm"', graph_text)
        self.assertNotIn('"rotation_euler_rad"', graph_text)
        self.assertNotIn('"scale"', graph_text)


if __name__ == "__main__":
    unittest.main()
