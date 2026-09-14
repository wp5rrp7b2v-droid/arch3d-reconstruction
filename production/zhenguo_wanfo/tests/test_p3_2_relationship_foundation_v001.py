"""T-015 negative fixtures: each invalid graph must be rejected with a stable code."""

import copy
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import validate_p3_2_relationship_foundation_v001 as v  # noqa: E402


class RelationshipFoundationNegativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema, cls.registry, cls.types, cls.interface_registry = [v.read(p) for p in (v.SCHEMA, v.NODES, v.TYPES, v.INTERFACES)]

    def setUp(self):
        self.graph = {"nodes": copy.deepcopy(self.registry["nodes"]), "interfaces": copy.deepcopy(self.interface_registry["interfaces"]), "relationships": [], "placements": [], "building_parameters": []}
        self.ids = [n["node_id"] for n in self.graph["nodes"]]

    def rejected(self, code):
        errors = v.validate_graph(self.graph, self.registry, self.interface_registry, self.types, self.schema)
        self.assertIn(code, {e["code"] for e in errors}, errors)

    def relation(self, kind="CONNECT", source=0, target=1):
        a, b = self.ids[source], self.ids[target]
        interface = lambda node: node + "__LOWER-PLANE"
        row = {"relationship_id": "REL-TEST-001", "relation_type": kind, "source_node": a, "target_node": b,
               "source_interface": interface(a), "target_interface": interface(b),
               "directionality": next(t["directionality"] for t in self.types["relationship_types"] if t["relation_type"] == kind),
               "evidence_status": "UNKNOWN", "evidence_basis": "TEST_ONLY_SYNTHETIC",
               "provenance": ["T-015 negative fixture"], "replaceability": True, "parameter_refs": [], "notes": "Synthetic validator fixture; no historical assertion."}
        self.graph["relationships"].append(row)
        return row

    def test_duplicate_formal_identity(self):
        n = copy.deepcopy(self.graph["nodes"][0]); n["node_id"] = "DUPLICATE-NODE"; self.graph["nodes"].append(n)
        self.rejected("DUPLICATE_COMPONENT_IDENTITY")

    def test_nonexistent_component(self):
        self.graph["nodes"][0]["component_id"] = "CMP-NOT-APPROVED-001"
        self.rejected("REGISTRY_OUTSIDE_FORMAL_NODE")

    def test_illegal_self_link(self):
        self.relation(source=0, target=0)
        self.rejected("ILLEGAL_SELF_LINK")

    def test_illegal_endpoint_type(self):
        n = {"node_id": "CTL-TEST-001", "component_id": None, "noncomponent_ref": "TEST-ONLY-CTL", "canonical_name_zh": "测试控制点", "node_class": "CONTROL", "historical_role": "NON_HISTORICAL_FORMAL", "qualification_status": "CONTROL_ONLY", "evidence_status": "PROJECT_RULE", "provenance": ["T-015 negative fixture"], "replaceability": True, "historical_claim": False}
        self.graph["nodes"].append(n)
        r = self.relation(); r["source_node"] = n["node_id"]; r["source_interface"] = None
        self.rejected("ILLEGAL_ENDPOINT_TYPE")

    def test_nonexistent_interface(self):
        self.relation()["source_interface"] = "IF-NOT-REGISTERED"
        self.rejected("NONEXISTENT_INTERFACE")

    def test_belong_hierarchy_cycle(self):
        for x in ("UNIT-A", "UNIT-B"):
            self.graph["nodes"].append({"node_id": x, "component_id": None, "canonical_name_zh": "测试单元", "node_class": "ASSEMBLY_UNIT", "historical_role": "ORGANIZATIONAL_UNIT", "qualification_status": "TEST_ONLY", "evidence_status": "PROJECT_RULE", "provenance": ["T-015 negative fixture"], "replaceability": True, "historical_claim": False})
        for idx, (a, b) in enumerate((("UNIT-A", "UNIT-B"), ("UNIT-B", "UNIT-A"))):
            self.graph["relationships"].append({"relationship_id": f"REL-TEST-{idx}", "relation_type": "BELONG", "source_node": a, "target_node": b, "directionality": "DIRECTED", "evidence_status": "PROJECT_RULE", "evidence_basis": "TEST_ONLY_SYNTHETIC", "provenance": ["T-015 negative fixture"], "replaceability": True, "parameter_refs": [], "notes": "Synthetic hierarchy"})
        self.rejected("BELONG_HIERARCHY_CYCLE")

    def test_belong_parent_conflict(self):
        for x in ("UNIT-A", "UNIT-B"):
            self.graph["nodes"].append({"node_id": x, "component_id": None, "canonical_name_zh": "测试单元", "node_class": "ASSEMBLY_UNIT", "historical_role": "ORGANIZATIONAL_UNIT", "qualification_status": "TEST_ONLY", "evidence_status": "PROJECT_RULE", "provenance": ["T-015 negative fixture"], "replaceability": True, "historical_claim": False})
            self.graph["relationships"].append({"relationship_id": "REL-" + x, "relation_type": "BELONG", "source_node": self.ids[0], "target_node": x, "directionality": "DIRECTED", "evidence_status": "PROJECT_RULE", "evidence_basis": "TEST_ONLY_SYNTHETIC", "provenance": ["T-015 negative fixture"], "replaceability": True, "parameter_refs": [], "notes": "Synthetic hierarchy"})
        self.rejected("HIERARCHY_PARENT_CONFLICT")

    def test_missing_evidence_provenance(self):
        r = self.relation(); r["provenance"] = []
        self.rejected("MISSING_EVIDENCE_PROVENANCE")

    def test_unknown_relation_silent_upgrade(self):
        r = self.relation(); r["prior_evidence_status"] = "UNKNOWN"; r["evidence_status"] = "CONFIRMED"; r["evidence_basis"] = "TEST_ONLY_SYNTHETIC"
        self.rejected("EVIDENCE_STATUS_UPGRADE")

    def test_nonhistorical_silent_upgrade(self):
        for cls in ("PROXY", "CONTROL", "ENVELOPE", "DEFERRED", "UNKNOWN"):
            with self.subTest(cls=cls):
                g = copy.deepcopy(self.graph)
                g["nodes"].append({"node_id": f"{cls}-TEST", "component_id": None, "noncomponent_ref": f"TEST-ONLY-{cls}", "canonical_name_zh": "测试对象", "node_class": cls, "historical_role": "HISTORICAL_COMPONENT", "qualification_status": "FORMAL_APPROVED_MASTER", "evidence_status": "CONFIRMED", "provenance": ["T-015 negative fixture"], "replaceability": False, "historical_claim": True, "engineering_use": "TEST_ONLY"})
                codes = {e["code"] for e in v.validate_graph(g, self.registry, self.interface_registry, self.types, self.schema)}
                self.assertIn("SILENT_HISTORICIZATION", codes)

    def test_six_chuanfu_reference_length_leak(self):
        self.graph["building_parameters"].append({"parameter_id": "SPAN-TEST", "component_id": "CMP-FRAME-LOWER-SIX-CHUANFU-001", "source_layer": "MASTER_REFERENCE", "evidence_status": "PROJECT_RULE", "provenance": ["canonical_reference_length_mm"], "replaceable": True, "historical_claim": False, "actual_length_mm": 1000, "derives_from": "canonical_reference_length_mm"})
        self.rejected("REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY")

    def test_world_coordinate_only_placement(self):
        self.graph["placements"].append({"node_id": self.ids[0], "interface_id": self.ids[0]+"__ORIGIN", "method": "MANUAL_WORLD_PLACEMENT", "rule_id": "", "coordinate_space": "WORLD", "parameter_refs": [], "world_result_mm": [100, 200, 300]})
        self.rejected("BAKED_MANUAL_ASSEMBLY")

    def test_world_only_interface(self):
        self.graph["interfaces"][0]["coordinate_space"] = "WORLD"
        self.rejected("BAKED_MANUAL_ASSEMBLY")

    def test_fabricated_formal_interface(self):
        self.graph["interfaces"][0]["interface_id"] = "UNREGISTERED-FORMAL-INTERFACE"
        self.rejected("NONEXISTENT_INTERFACE")

    def test_relation_evidence_not_inherited_from_component(self):
        r = self.relation(); r["evidence_status"] = "CONFIRMED"; r["evidence_basis"] = "INHERITED_FROM_COMPONENT"
        self.rejected("RELATION_EVIDENCE_NOT_INDEPENDENT")

    def test_unknown_joinery_not_confirmed(self):
        r = self.relation(); r["joinery_detail_status"] = "CONFIRMED"; r["joinery_detail_basis"] = "UNKNOWN"
        self.rejected("EVIDENCE_STATUS_UPGRADE")

    def test_support_cycle(self):
        self.relation("SUPPORT", 0, 1)
        r = self.relation("SUPPORT", 1, 0); r["relationship_id"] = "REL-TEST-002"
        self.rejected("UNEXPECTED_SUPPORT_CYCLE")

    def test_locate_cycle(self):
        self.relation("LOCATE", 0, 1)
        r = self.relation("LOCATE", 1, 0); r["relationship_id"] = "REL-TEST-002"
        self.rejected("UNEXPECTED_LOCATE_CYCLE")

    def test_isolated_formal_node(self):
        self.graph["require_connected"] = True
        self.rejected("ISOLATED_FORMAL_NODE")

    def test_required_relation_missing(self):
        self.graph["required_relation_types"] = ["SUPPORT"]
        self.rejected("REQUIRED_RELATION_MISSING")

    def test_repeat_without_parameters(self):
        r = self.relation("REPEAT"); r["source_interface"] = None; r["target_interface"] = None
        self.rejected("BAKED_MANUAL_ASSEMBLY")


if __name__ == "__main__":
    unittest.main()
