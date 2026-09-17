import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "production/zhenguo_wanfo/scripts"))
from p3_3_whole_building_common_v001 import CANONICAL_PM005, MUTATED_PM005, compile_runtime, normalized_snapshot, stable_json
from build_p3_3_whole_building_v001 import representation_spec
from validate_p3_3_whole_building_v001 import (HARD_FAILS, failures, mutated_fixture, negative_results,
    representation_audit, spatial_audit, valid_blender_version, validate_pr_head_binding)


class WholeBuildingTests(unittest.TestCase):
    def setUp(self): self.canonical = compile_runtime()

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
        self.assertEqual(len(derived),365)
        for item in derived:
            d=item["placement"]["derivation"]
            self.assertTrue(d["rule_ids"]); self.assertTrue(d["relationship_types"]); self.assertTrue(d["parameter_values"]); self.assertTrue(d["identity_indices"]); self.assertEqual(len(d["authoritative_sources"]),4)
        rules={r for x in derived for r in x["placement"]["derivation"]["rule_ids"]}
        self.assertTrue({"RULE-COLUMN-GRID","RULE-BRACKET-TOPOLOGY","RULE-FRAME-DEPTHS","RULE-FRAME-SEMANTICS","RULE-ROOF-OUTLINE","RULE-ROOF-ELEVATIONS","RULE-MAJOR-ELEVATIONS"} <= rules)
        self.assertEqual(self.canonical["runtime_accounting"]["not_realized_no_approved_placement_rule"],0)
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
        self.assertGreater(len(changed),12)
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

    def test_spatial_audit_has_real_family_measurements(self):
        audit=spatial_audit(self.canonical); self.assertEqual(audit["status"],"PASS"); self.assertEqual(audit["realized_count"],365)
        self.assertEqual(set(audit["per_family"]),{"COLUMN","GRID_CONTROL","BRACKET_CONTACT","BRACKET_ARM","FRAME_CONTROL","FRAME_SUPPORT","PRIMARY_FRAME","GABLE_CONTROL","PURLIN","RAFTER","ROOF_ENVELOPE"})
        self.assertTrue(all(x["measurements"] and x["status"]=="PASS" for x in audit["per_family"].values()))

    def test_false_positive_spatial_mutations_are_rejected(self):
        cases=[]
        def alter(family, edit):
            m=copy.deepcopy(self.canonical); item=next(x for x in m["runtime_objects"] if x["family"]==family); edit(item); return m
        cases += [alter("COLUMN",lambda x:x["placement"]["location_mm"].__setitem__(0,x["placement"]["location_mm"][0]+1)),
                  alter("FRAME_CONTROL",lambda x:x["placement"]["location_mm"].__setitem__(2,x["placement"]["location_mm"][2]+1)),
                  alter("FRAME_CONTROL",lambda x:x["placement"]["derivation"]["identity_indices"].__setitem__("tier",99)),
                  alter("PURLIN",lambda x:x["placement"]["location_mm"].__setitem__(2,x["placement"]["location_mm"][2]+1)),
                  alter("ROOF_ENVELOPE",lambda x:x["placement"]["location_mm"].__setitem__(1,x["placement"]["location_mm"][1]+1)),
                  alter("BRACKET_ARM",lambda x:x["placement"]["derivation"].pop("rule_ids")),
                  alter("RAFTER",lambda x:x["placement"]["derivation"]["parameter_ids"].remove("FR-007")),
                  alter("BRACKET_ARM",lambda x:x.__setitem__("historical_claim_boundary","HISTORICAL_CONFIRMED")),
                  alter("PURLIN",lambda x:x.__setitem__("p3_3_disposition","GENERATED_FORMAL_GEOMETRY"))]
        missing=copy.deepcopy(self.canonical); missing["runtime_objects"].pop(); cases.append(missing)
        bracket_count=copy.deepcopy(self.canonical); bracket_count["runtime_objects"].pop(next(i for i,x in enumerate(bracket_count["runtime_objects"]) if x["family"]=="BRACKET_CONTACT")); cases.append(bracket_count)
        for index,case in enumerate(cases):
            with self.subTest(case_index=index): self.assertTrue(failures(case))

    def test_family_specific_engineering_representation_geometry(self):
        audit=representation_audit(self.canonical); self.assertEqual(audit["status"],"PASS"); self.assertEqual(audit["technical_count"],353); self.assertEqual(audit["generic_octahedron_count"],0)
        specs={}
        for record in self.canonical["runtime_objects"]:
            if record["family"]!="COLUMN": specs.setdefault(record["family"],representation_spec(record,self.canonical["runtime_objects"]))
        self.assertEqual(len({x["geometry_class"] for x in specs.values()}),10)
        self.assertEqual(specs["ROOF_ENVELOPE"]["kind"],"SURFACE")
        self.assertEqual(specs["PURLIN"]["geometry_class"],"DEFERRED_PURLIN_DATUM")
        self.assertEqual(specs["RAFTER"]["endpoint_source_ids"][:2],["ROOF_PURLIN_N_00","ROOF_PURLIN_N_01"])
        self.assertTrue(all(len(x["world_points"])>=2 and x["endpoint_source_ids"] for x in specs.values()))

    def test_representation_boundary_mutations_are_rejected(self):
        cases=[]
        for family,bad_class in (("FRAME_CONTROL","POINT_ONLY"),("FRAME_SUPPORT","MISSING_CONNECTOR"),("RAFTER","SYNTHETIC_LENGTH"),("ROOF_ENVELOPE","POINT_ONLY"),("BRACKET_ARM","SOLID_HISTORIC_MEMBER"),("PURLIN","BEAM_CYLINDER")):
            value=copy.deepcopy(self.canonical); item=next(x for x in value["runtime_objects"] if x["family"]==family); item["representation"]["geometry_class"]=bad_class; cases.append(value)
        identity=copy.deepcopy(self.canonical); next(x for x in identity["runtime_objects"] if x["family"]=="FRAME_CONTROL")["runtime_instance_id"]=""; cases.append(identity)
        for value in cases: self.assertTrue(representation_audit(value)["errors"] or failures(value))

    def test_review_counts_are_view_aware_not_global_copies(self):
        source=(ROOT/"production/zhenguo_wanfo/scripts/render_p3_3_whole_building_review_v001.py").read_text(encoding="utf-8")
        self.assertIn("projected_in_frame_count",source); self.assertIn("per_family_in_frame_count",source); self.assertIn("model_projected_bounds",source)
        self.assertNotIn("formal_visible_count",source); self.assertNotIn("proxy_visible_represented_count",source)

if __name__=="__main__": unittest.main()
