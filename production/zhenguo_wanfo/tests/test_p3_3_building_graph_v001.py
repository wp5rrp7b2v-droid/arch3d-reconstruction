import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "production/zhenguo_wanfo/scripts"
sys.path.insert(0, str(SCRIPTS))

from build_p3_3_building_graph_v001 import OUTPUTS, compile_assets  # noqa: E402
from validate_p3_3_building_graph_v001 import HARD_FAILS, mutate, validate  # noqa: E402


class BuildingGraphTests(unittest.TestCase):
    def test_canonical_assets_validate(self):
        self.assertEqual(validate(compile_assets()), [])

    def test_accounting_is_complete(self):
        summary = compile_assets()["accounting"]["summary"]
        self.assertEqual((summary["families_accounted"], summary["variants_accounted"], summary["instances_accounted"]), (11, 40, 365))
        self.assertEqual((summary["unexplained_omissions"], summary["orphan_identities"]), (0, 0))

    def test_five_negative_fixtures_are_rejected(self):
        canonical = compile_assets()
        for fixture in sorted((ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3").glob("*.json")):
            spec = json.loads(fixture.read_text(encoding="utf-8"))
            self.assertIn(spec["expected_hard_fail"], validate(mutate(canonical, spec["mutation"])), fixture.name)
        self.assertEqual(len(list((ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3").glob("*.json"))), 5)

    def test_stable_serialization_matches_committed_outputs(self):
        compiled = compile_assets()
        for name, value in compiled.items():
            self.assertEqual(json.loads(OUTPUTS[name].read_text(encoding="utf-8")), value, name)

    def test_no_p2_numeric_transform_in_generated_assets(self):
        text = json.dumps(compile_assets(), sort_keys=True)
        self.assertNotIn('"location_mm"', text)
        self.assertNotIn('"rotation_euler_rad"', text)
        self.assertNotIn('"scale"', text)


if __name__ == "__main__":
    unittest.main()
