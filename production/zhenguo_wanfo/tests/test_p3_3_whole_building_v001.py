import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "production/zhenguo_wanfo/scripts"))
from p3_3_whole_building_common_v001 import CANONICAL_PM005, MUTATED_PM005, compile_runtime, normalized_snapshot, stable_json
from validate_p3_3_whole_building_v001 import HARD_FAILS, failures, mutated_fixture, negative_results


class WholeBuildingTests(unittest.TestCase):
    def setUp(self): self.canonical = compile_runtime()

    def test_clean_contract_and_365_outcomes(self):
        self.assertFalse(failures(self.canonical)); self.assertEqual(len(self.canonical["runtime_objects"]), 365)
        self.assertEqual(sum(self.canonical["runtime_accounting"]["outcome_counts"].values()), 365)
        self.assertEqual(self.canonical["generator_contract"]["p2_numeric_transform_usage"], 0)

    def test_identity_metadata_complete(self):
        required={"runtime_instance_id","legacy_instance_id","component_id","graph_parent_node_id","p3_3_disposition","evidence_status","parameter_rule_provenance","historical_claim_boundary"}
        self.assertTrue(all(required <= set(x) for x in self.canonical["runtime_objects"]))

    def test_locked_relationship_vocabulary(self):
        self.assertEqual(self.canonical["generator_contract"]["relationship_vocabulary"],["SUPPORT","CONNECT","LOCATE","REPEAT","BELONG"])

    def test_evidence_and_six_chuanfu_boundary(self):
        text=stable_json(self.canonical); self.assertNotIn('"actual_full_length_mm": 1000',text)
        self.assertTrue(all(x["historical_claim_boundary"]=="NOT_UPGRADED" for x in self.canonical["runtime_objects"]))

    def test_five_hard_fails_rejected(self):
        result=negative_results(self.canonical); self.assertEqual(len(result),5); self.assertTrue(all(x["actual"]=="EXPECTED_REJECTION" for x in result))
        for code in HARD_FAILS: self.assertIn(code,failures(mutated_fixture(self.canonical,code)))

    def test_pm005_mutation_only_moves_declared_dependants(self):
        mutation=compile_runtime(MUTATED_PM005); changed=[]
        for a,b in zip(self.canonical["runtime_objects"],mutation["runtime_objects"]):
            if a["placement"] != b["placement"]: changed.append((a,b))
            self.assertEqual(a["evidence_status"],b["evidence_status"])
        self.assertTrue(changed); self.assertTrue(all("PM-005" in b["placement"]["parameter_ids"] for _,b in changed))
        self.assertEqual(mutation["parameter_state"]["PM-005"]["value_mm"]-CANONICAL_PM005,100.0)

    def test_restore_and_stable_serialization(self):
        run_a=compile_runtime(); compile_runtime(MUTATED_PM005); run_d=compile_runtime()
        self.assertEqual(normalized_snapshot(run_a),normalized_snapshot(run_d)); self.assertEqual(stable_json(run_a),stable_json(run_d))

if __name__=="__main__": unittest.main()
