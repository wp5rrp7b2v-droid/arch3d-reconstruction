import copy
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from p3_3_whole_building_common_v001 import DATUM_RULE_ID, compile_runtime, validate_runtime


class WholeBuildingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runtime = compile_runtime()

    def test_accounting_identity_and_evidence(self):
        self.assertEqual(365, self.runtime["runtime_count"])
        self.assertEqual([], validate_runtime(self.runtime))
        self.assertEqual(7, self.runtime["disposition_counts"]["DEFERRED"])
        self.assertTrue(all(r["p3_3_disposition"] == "DEFERRED" for r in self.runtime["records"] if r["source_family_id"] == "PURLIN"))

    def test_shared_ridge_datum_derives_roof(self):
        by_id = {r["legacy_instance_id"]: r for r in self.runtime["records"]}
        self.assertNotIn("ROOF_PURLIN_S_03", by_id)
        self.assertEqual([0.0, 0.0, 7068.6], by_id["ROOF_PURLIN_N_03"]["placement"]["point_mm"])
        south_last = by_id["ROOF_RAFTER_S_X00_S02"]
        self.assertEqual(0.0, south_last["placement"]["end_mm"][1])
        for family in ("PURLIN", "RAFTER", "ROOF_ENVELOPE", "GABLE_CONTROL"):
            self.assertTrue(all(DATUM_RULE_ID in r["placement_provenance"] for r in self.runtime["records"] if r["source_family_id"] == family))

    def test_observed_pm_values_never_place_objects(self):
        forbidden = {f"PM-{i:03d}" for i in range(3, 8)}
        self.assertTrue(all(not (forbidden & set(r["placement_provenance"])) for r in self.runtime["records"]))

    def test_all_five_hard_fails_reject(self):
        cases = {
            "REFERENCE_LENGTH_LEAKS_INTO_BUILDING": lambda d: d["records"][0].update(actual_full_length_mm=1000),
            "SILENT_HISTORICIZATION": lambda d: d["records"][0].update(historical_claim_boundary="CONFIRMED_HISTORICAL"),
            "BAKED_MANUAL_BUILDING": lambda d: d["records"][0]["placement_provenance"].append("PM-003"),
            "SILENT_BUILDING_OMISSION": lambda d: d["records"].pop(),
            "BROKEN_COMPONENT_IDENTITY": lambda d: d["records"][0].update(component_id=None),
        }
        for expected, mutate in cases.items():
            with self.subTest(expected):
                fixture = copy.deepcopy(self.runtime); mutate(fixture)
                self.assertIn(expected, validate_runtime(fixture))

    def test_pm005_mutation_is_non_authoritative_for_placement_and_restores(self):
        mutated = compile_runtime({"PM-005": 3605.7})
        restored = compile_runtime()
        self.assertEqual(self.runtime["semantic_snapshot_sha256"], restored["semantic_snapshot_sha256"])
        self.assertEqual(self.runtime["semantic_snapshot_sha256"], mutated["semantic_snapshot_sha256"])


if __name__ == "__main__": unittest.main()
