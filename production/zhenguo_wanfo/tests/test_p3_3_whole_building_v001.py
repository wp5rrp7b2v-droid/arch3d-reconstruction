import copy
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "production/zhenguo_wanfo/scripts"))
from p3_3_whole_building_common_v001 import CANONICAL_PM005, MUTATED_PM005, compile_runtime, normalized_snapshot, stable_json
from validate_p3_3_whole_building_v001 import (HARD_FAILS, failures, mutated_fixture, negative_results,
    valid_blender_version, validate_pr_head_binding)


class WholeBuildingTests(unittest.TestCase):
    def setUp(self): self.canonical = compile_runtime()

    def test_blender_style_entrypoints_bootstrap_sibling_imports(self):
        scripts = ROOT / "production/zhenguo_wanfo/scripts"
        build_script = scripts / "build_p3_3_whole_building_v001.py"
        validate_script = scripts / "validate_p3_3_whole_building_v001.py"
        original_cwd = Path.cwd()
        original_path = list(sys.path)
        original_common = sys.modules.get("p3_3_whole_building_common_v001")
        try:
            with tempfile.TemporaryDirectory() as td:
                os.chdir(td)
                sys.path[:] = [entry for entry in original_path if Path(entry or ".").resolve() != scripts.resolve()]
                sys.modules.pop("p3_3_whole_building_common_v001", None)
                build_ns = runpy.run_path(str(build_script))
                manifest = build_ns["compile_runtime"]()
                self.assertEqual(len(manifest["runtime_objects"]), 365)

                sys.path[:] = [entry for entry in original_path if Path(entry or ".").resolve() != scripts.resolve()]
                sys.modules.pop("p3_3_whole_building_common_v001", None)
                validate_ns = runpy.run_path(str(validate_script))
                self.assertEqual(validate_ns["report"](manifest)["status"], "PASS")
        finally:
            os.chdir(original_cwd)
            sys.path[:] = original_path
            if original_common is not None:
                sys.modules["p3_3_whole_building_common_v001"] = original_common

    def test_clean_contract_and_365_outcomes(self):
        self.assertFalse(failures(self.canonical)); self.assertEqual(len(self.canonical["runtime_objects"]), 365)
        self.assertEqual(sum(self.canonical["runtime_accounting"]["outcome_counts"].values()), 365)
        self.assertEqual(self.canonical["generator_contract"]["p2_numeric_transform_usage"], 0)

    def test_identity_metadata_complete(self):
        required={"runtime_instance_id","legacy_instance_id","component_id","graph_parent_node_id","p3_3_disposition","evidence_status","parameter_rule_provenance","historical_claim_boundary"}
        self.assertTrue(all(required <= set(x) for x in self.canonical["runtime_objects"]))

    def test_formal_geometry_is_approved_master_not_generic_cube(self):
        formal=[x for x in self.canonical["runtime_objects"] if x["p3_3_disposition"]=="GENERATED_FORMAL_GEOMETRY"]
        self.assertEqual(len(formal),12); self.assertTrue(all(x["component_id"]=="CMP-COLUMN-001" for x in formal))
        self.assertTrue(all(x["formal_master"]["generator_path"].endswith("build_column_master_v001.py") for x in formal))
        self.assertNotIn("primitive_cube_add", (ROOT/"production/zhenguo_wanfo/scripts/build_p3_3_whole_building_v001.py").read_text())

    def test_purlins_are_seven_of_seven_deferred(self):
        purlins=[x for x in self.canonical["runtime_objects"] if x["component_id"]=="CMP-PURLIN-001"]
        self.assertEqual(len(purlins),7); self.assertEqual({x["p3_3_disposition"] for x in purlins},{"DEFERRED"})

    def test_placement_is_authoritative_rule_traceable(self):
        derived=[x for x in self.canonical["runtime_objects"] if x["placement"]["status"]=="RULE_DERIVED"]
        self.assertEqual(len(derived),12)
        for item in derived:
            d=item["placement"]["derivation"]
            self.assertEqual((d["p3_2_relationship_id"],d["rule_id"]),("C-R01","RULE-COLUMN-GRID"))
            self.assertIn("PM-005",d["parameter_values"]); self.assertEqual(len(d["authoritative_sources"]),4)
        source=(ROOT/"production/zhenguo_wanfo/scripts/p3_3_whole_building_common_v001.py").read_text()
        self.assertNotIn("0.72",source); self.assertNotIn("0.42",source); self.assertNotIn("layouts =",source)

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
        self.assertTrue(changed); self.assertTrue(all("PM-005" in b["placement"]["derivation"]["parameter_values"] for _,b in changed))
        self.assertEqual(mutation["parameter_state"]["PM-005"]["value_mm"]-CANONICAL_PM005,100.0)

    def test_restore_and_stable_serialization(self):
        run_a=compile_runtime(); compile_runtime(MUTATED_PM005); run_d=compile_runtime()
        self.assertEqual(normalized_snapshot(run_a),normalized_snapshot(run_d)); self.assertEqual(stable_json(run_a),stable_json(run_d))

    def test_blender_version_is_strict_and_suffix_aware(self):
        self.assertTrue(valid_blender_version("Blender 4.5.13")); self.assertTrue(valid_blender_version("Blender 4.5.13 LTS"))
        for value in ("Blender 4.5.12","Blender 4.5.14","Blender 4.5.13 alpha","4.5.13"):
            self.assertFalse(valid_blender_version(value))

    def test_pr_head_sha_binding(self):
        sha="a"*40; self.assertTrue(validate_pr_head_binding({"pr_head_sha":sha},sha))
        self.assertFalse(validate_pr_head_binding({"pr_head_sha":"b"*40},sha)); self.assertFalse(validate_pr_head_binding({"pr_head_sha":sha},"not-a-sha"))

if __name__=="__main__": unittest.main()
