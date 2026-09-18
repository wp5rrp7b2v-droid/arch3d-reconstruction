import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "production/zhenguo_wanfo/scripts"))

from build_p3_3_building_graph_v001 import PATHS, compile_assets, load  # noqa: E402
from validate_p3_3_design_datum_rule_v001 import NEGATIVES, build_report, mutate, validate  # noqa: E402


class DesignDatumRuleTests(unittest.TestCase):
    def setUp(self):
        self.rule, self.docs = load(PATHS["design_datum_rule"]), compile_assets()

    def test_canonical_rule_validates(self): self.assertEqual(validate(self.rule, self.docs), [])
    def test_binding_consumes_canonical_value_without_self_dependency(self):
        binding = next(item for item in self.docs["bindings"]["bindings"] if item.get("parameter_id") == self.rule["rule_id"])
        self.assertEqual(binding["value"], {"plan_origin_mm": [self.rule["coordinate_frame"]["x"]["datum_mm"], self.rule["coordinate_frame"]["y"]["datum_mm"]], "ridge_y_mm": self.rule["roof_control"]["ridge_y_mm"]})
        self.assertEqual(binding["binding_targets"]["depends_on"], ["FR-007", "MOD-002"])
        self.assertNotIn(self.rule["rule_id"], self.rule["dependency_lineage"])

    def test_unrelated_locate_does_not_inherit_datum_metadata(self):
        docs = copy.deepcopy(self.docs)
        docs["graph"]["relationships"].append({"relationship_id": "LOCATE-UNRELATED", "relation_type": "LOCATE", "provenance": ["unrelated"], "parameter_refs": [], "evidence_status": "ORGANIZATIONAL_ONLY"})
        self.assertNotIn("DATUM_RELATION_SCOPE_INVALID", validate(self.rule, docs))

    def test_required_negatives_are_rejected(self):
        for expected, kind in NEGATIVES.items():
            if kind == "observed":
                docs = copy.deepcopy(self.docs)
                datum_binding = next(item for item in docs["bindings"]["bindings"] if item.get("parameter_id") == self.rule["rule_id"])
                datum_binding["binding_targets"]["depends_on"].append("PM-007")
                self.assertIn(expected, validate(self.rule, docs))
            elif kind == "local":
                docs = copy.deepcopy(self.docs); docs["graph"]["generation_contract"]["local_coordinate_rules_without_canonical_authority"] = "COLUMN_GRID_Y_MIRROR_RULE"
                self.assertIn(expected, validate(self.rule, docs))
            else: self.assertIn(expected, validate(mutate(self.rule, kind), self.docs), kind)
    def test_report_passes(self): self.assertEqual(build_report()["status"], "PASS")


if __name__ == "__main__": unittest.main()
