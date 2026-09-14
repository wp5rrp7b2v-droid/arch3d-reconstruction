#!/usr/bin/env python3
"""T-015 deterministic assembly foundation validator. No Blender or geometry writes."""

import argparse
import hashlib
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
BASE = Path("production/zhenguo_wanfo")
ASSEMBLY = BASE / "assembly"
SCHEMA = ASSEMBLY / "P3_2_ASSEMBLY_SCHEMA_V001.json"
NODES = ASSEMBLY / "P3_2_ASSEMBLY_NODE_REGISTRY_V001.json"
TYPES = ASSEMBLY / "P3_2_RELATIONSHIP_TYPES_V001.json"
INTERFACES = ASSEMBLY / "P3_2_INTERFACE_REGISTRY_V001.json"
REPORT = BASE / "validation/P3_2_RELATIONSHIP_FOUNDATION_VALIDATION_V001.json"
P30 = BASE / "registry/P3_0_COMPONENT_REGISTRY_V001.json"
SCOPE = BASE / "registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json"
LIBRARY = BASE / "registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json"
CONTRACT = BASE / "registry/P3_1_MASTER_ASSET_CONTRACT_V002.json"
SOURCE_DOCS = (
    Path("docs/production/zhenguo_wanfo/P3_2_DEFINITION_OF_DONE_V001.md"),
    Path("docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_DESIGN_V001.md"),
    Path("docs/tasks/T-015_P3_2_RELATIONSHIP_FOUNDATION_V001.md"),
)
EXPECTED_TYPES = ("SUPPORT", "CONNECT", "LOCATE", "REPEAT", "BELONG")
HARD_FAILS = ("REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY", "SILENT_HISTORICIZATION", "BAKED_MANUAL_ASSEMBLY")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def git_bytes(path):
    return subprocess.run(["git", "show", f"HEAD:{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def error(code, detail):
    return {"code": code, "detail": detail}


def has_cycle(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    visiting, done = set(), set()

    def visit(node):
        if node in visiting:
            return True
        if node in done:
            return False
        visiting.add(node)
        if any(visit(child) for child in graph.get(node, [])):
            return True
        visiting.remove(node)
        done.add(node)
        return False

    return any(visit(node) for node in graph)


def validate_graph(graph, node_registry, interface_registry, type_registry, schema):
    """Validate future assembly records without inferring historical relationships."""
    errors = []
    for issue in Draft202012Validator(schema).iter_errors(graph):
        errors.append(error("SCHEMA_INVALID", issue.message))
    if not isinstance(graph, dict) or any(not isinstance(graph.get(key), list) or any(not isinstance(row, dict) for row in graph[key]) for key in ("nodes", "relationships", "interfaces", "placements", "building_parameters")):
        return errors or [error("SCHEMA_INVALID", "assembly graph collections must be arrays of objects")]
    nodes = graph.get("nodes", [])
    relations = graph.get("relationships", [])
    interfaces = graph.get("interfaces", [])
    node_by_id = {n.get("node_id"): n for n in nodes if isinstance(n, dict)}
    interface_by_id = {i.get("interface_id"): i for i in interfaces if isinstance(i, dict)}
    approved = {n["component_id"]: n for n in node_registry["nodes"]}
    known_nonformal = {r["candidate_id"]: r for r in read(SCOPE)["records"] if r["eligibility_status"] != "MASTER_REQUIRED"}
    rules = node_registry["nonhistorical_qualification_rules"]
    classes = {t["relation_type"]: t for t in type_registry["relationship_types"]}
    if len(node_by_id) != len(nodes) or len([n.get("component_id") for n in nodes if n.get("node_class") == "FORMAL_COMPONENT"]) != len(set(n.get("component_id") for n in nodes if n.get("node_class") == "FORMAL_COMPONENT")):
        errors.append(error("DUPLICATE_COMPONENT_IDENTITY", "node_id or formal component_id repeated"))
    if len({r.get("relationship_id") for r in relations}) != len(relations):
        errors.append(error("DUPLICATE_RELATIONSHIP_ID", "relationship_id repeated"))
    if len(interface_by_id) != len(interfaces):
        errors.append(error("DUPLICATE_INTERFACE_ID", "interface_id repeated"))

    for n in nodes:
        cls = n.get("node_class")
        cid = n.get("component_id")
        if cls == "FORMAL_COMPONENT":
            expected = approved.get(cid)
            if expected is None or n.get("node_id") != cid:
                errors.append(error("REGISTRY_OUTSIDE_FORMAL_NODE", str(cid)))
            elif any(n.get(k) != expected.get(k) for k in ("canonical_name_zh", "historical_role", "qualification_status", "evidence_status", "replaceability")):
                errors.append(error("EVIDENCE_STATUS_UPGRADE", str(cid)))
        elif cls in rules:
            rule = rules[cls]
            scope_row = known_nonformal.get(cid)
            if cid is not None and (scope_row is None or scope_row["eligibility_status"] != rule["qualification_status"]):
                errors.append(error("REGISTRY_OUTSIDE_NONFORMAL_NODE", str(cid)))
            if cid is None and not n.get("noncomponent_ref"):
                errors.append(error("NONCOMPONENT_REFERENCE_MISSING", n.get("node_id")))
            if n.get("historical_role") != rule["historical_role"] or n.get("qualification_status") != rule["qualification_status"] or n.get("evidence_status") == "CONFIRMED" or n.get("historical_claim") is True:
                errors.append(error("SILENT_HISTORICIZATION", n.get("node_id")))
            if cls == "DEFERRED" and not n.get("engineering_use"):
                errors.append(error("DEFERRED_USE_NOT_DECLARED", n.get("node_id")))
        elif cls == "ASSEMBLY_UNIT":
            if cid is not None or n.get("historical_role") != "ORGANIZATIONAL_UNIT" or n.get("historical_claim") is True:
                errors.append(error("ILLEGAL_ASSEMBLY_UNIT", n.get("node_id")))
        else:
            errors.append(error("ILLEGAL_NODE_CLASS", str(cls)))
        if n.get("evidence_status") == "UNKNOWN" and n.get("historical_claim") is True:
            errors.append(error("SILENT_HISTORICIZATION", n.get("node_id")))
        if not n.get("provenance"):
            errors.append(error("MISSING_EVIDENCE_PROVENANCE", n.get("node_id")))

    for i in interfaces:
        owner = node_by_id.get(i.get("owner_node"))
        if owner is None:
            errors.append(error("ILLEGAL_INTERFACE_OWNER", i.get("interface_id")))
        if owner is not None and owner.get("node_class") == "FORMAL_COMPONENT":
            official = {r["interface_id"]: r for r in interface_registry["interfaces"]}.get(i.get("interface_id"))
            if official is None or any(i.get(k) != official.get(k) for k in ("owner_node", "interface_type", "coordinate_space", "local_datum", "primary_direction", "allowed_relation_types")):
                errors.append(error("NONEXISTENT_INTERFACE", i.get("interface_id")))
        if i.get("coordinate_space") != "MASTER_LOCAL" or not i.get("local_datum") or not i.get("primary_direction"):
            errors.append(error("BAKED_MANUAL_ASSEMBLY", i.get("interface_id")))
        if not i.get("provenance") or not i.get("evidence_status"):
            errors.append(error("MISSING_EVIDENCE_PROVENANCE", i.get("interface_id")))
        if i.get("evidence_status") == "CONFIRMED" and i.get("historical_claim") is True:
            errors.append(error("EVIDENCE_STATUS_UPGRADE", i.get("interface_id")))

    parameter_by_id = {p.get("parameter_id"): p for p in graph.get("building_parameters", [])}
    if len(parameter_by_id) != len(graph.get("building_parameters", [])):
        errors.append(error("DUPLICATE_BUILDING_PARAMETER", "parameter_id repeated"))
    support_edges, locate_edges, belong_edges = [], [], []
    used_nodes = set()
    for r in relations:
        kind = r.get("relation_type")
        spec = classes.get(kind)
        if spec is None:
            errors.append(error("ILLEGAL_RELATION_TYPE", str(kind)))
            continue
        source, target = node_by_id.get(r.get("source_node")), node_by_id.get(r.get("target_node"))
        if source is None or target is None:
            errors.append(error("ILLEGAL_ENDPOINT", r.get("relationship_id")))
            continue
        if source["node_id"] == target["node_id"] and not spec["self_link_allowed"]:
            errors.append(error("ILLEGAL_SELF_LINK", r.get("relationship_id")))
        if source["node_class"] not in spec["source_node_classes"] or target["node_class"] not in spec["target_node_classes"]:
            errors.append(error("ILLEGAL_ENDPOINT_TYPE", r.get("relationship_id")))
        for endpoint, key in ((source, "source_interface"), (target, "target_interface")):
            value = r.get(key)
            if key in spec["required_interface_fields"] and not value:
                errors.append(error("MISSING_INTERFACE", r.get("relationship_id")))
            if value:
                interface = interface_by_id.get(value)
                if interface is None or interface.get("owner_node") != endpoint["node_id"] or kind not in interface.get("allowed_relation_types", []):
                    errors.append(error("NONEXISTENT_INTERFACE", str(value)))
        if not r.get("evidence_status") or not r.get("provenance"):
            errors.append(error("MISSING_EVIDENCE_PROVENANCE", r.get("relationship_id")))
        if r.get("evidence_status") == "CONFIRMED" and r.get("evidence_basis") in (None, "INHERITED_FROM_COMPONENT"):
            errors.append(error("RELATION_EVIDENCE_NOT_INDEPENDENT", r.get("relationship_id")))
        if r.get("evidence_status") == "CONFIRMED" and r.get("prior_evidence_status") == "UNKNOWN":
            errors.append(error("EVIDENCE_STATUS_UPGRADE", r.get("relationship_id")))
        if r.get("joinery_detail_status") == "CONFIRMED" and r.get("joinery_detail_basis") in (None, "UNKNOWN"):
            errors.append(error("EVIDENCE_STATUS_UPGRADE", r.get("relationship_id")))
        if r.get("directionality") != spec["directionality"]:
            errors.append(error("ILLEGAL_DIRECTIONALITY", r.get("relationship_id")))
        if any(ref not in parameter_by_id for ref in r.get("parameter_refs", [])):
            errors.append(error("INVALID_PARAMETER_REFERENCE", r.get("relationship_id")))
        if kind == "REPEAT":
            p = r.get("repeat_rule", {})
            if not all(k in p for k in ("count_ref", "direction", "spacing_ref", "start_interface", "parameter_source")):
                errors.append(error("BAKED_MANUAL_ASSEMBLY", r.get("relationship_id")))
            elif p["start_interface"] not in interface_by_id or p["count_ref"] not in r.get("parameter_refs", []) or p["spacing_ref"] not in r.get("parameter_refs", []):
                errors.append(error("INVALID_REPEAT_RULE", r.get("relationship_id")))
        if kind == "SUPPORT":
            support_edges.append((source["node_id"], target["node_id"]))
        if kind == "LOCATE":
            locate_edges.append((source["node_id"], target["node_id"]))
        if kind == "BELONG":
            belong_edges.append((source["node_id"], target["node_id"]))
        used_nodes.update((source["node_id"], target["node_id"]))
    if has_cycle(support_edges):
        errors.append(error("UNEXPECTED_SUPPORT_CYCLE", "SUPPORT graph has cycle"))
    if has_cycle(locate_edges):
        errors.append(error("UNEXPECTED_LOCATE_CYCLE", "LOCATE graph has cycle"))
    if has_cycle(belong_edges):
        errors.append(error("BELONG_HIERARCHY_CYCLE", "BELONG graph has cycle"))
    parents = {}
    for child, parent in belong_edges:
        if child in parents and parents[child] != parent:
            errors.append(error("HIERARCHY_PARENT_CONFLICT", child))
        parents[child] = parent
    if graph.get("require_connected") and any(n.get("node_class") == "FORMAL_COMPONENT" and n.get("node_id") not in used_nodes for n in nodes):
        errors.append(error("ISOLATED_FORMAL_NODE", "formal graph contains unused node"))
    if any(req not in {r.get("relation_type") for r in relations} for req in graph.get("required_relation_types", [])):
        errors.append(error("REQUIRED_RELATION_MISSING", "required relation type absent"))

    for p in graph.get("placements", []):
        if p.get("node_id") not in node_by_id or p.get("interface_id") not in interface_by_id or interface_by_id.get(p.get("interface_id"), {}).get("owner_node") != p.get("node_id"):
            errors.append(error("NONEXISTENT_INTERFACE", p.get("node_id")))
        if p.get("method") != "INTERFACE_PARAMETER_RULE" or not p.get("rule_id") or not p.get("parameter_refs") or p.get("coordinate_space") != "MASTER_LOCAL":
            errors.append(error("BAKED_MANUAL_ASSEMBLY", p.get("node_id")))
        if any(ref not in parameter_by_id for ref in p.get("parameter_refs", [])):
            errors.append(error("INVALID_PARAMETER_REFERENCE", p.get("node_id")))
        if "SIX-CHUANFU" in str(p.get("node_id")) and not any(ref in parameter_by_id and parameter_by_id[ref].get("component_id") == p.get("node_id") and parameter_by_id[ref].get("actual_length_mm") is not None for ref in p.get("parameter_refs", [])):
            errors.append(error("BUILDING_LENGTH_REQUIRED", p.get("node_id")))
    for p in graph.get("building_parameters", []):
        if p.get("source_layer") == "MASTER_REFERENCE" or p.get("derives_from") in ("canonical_reference_length_mm", "realization_length_mm"):
            errors.append(error("REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY", p.get("parameter_id")))
        if p.get("historical_claim") is True and p.get("evidence_status") in ("UNKNOWN", "PROJECT_RULE", "REASONABLE_COMPLETION"):
            errors.append(error("EVIDENCE_STATUS_UPGRADE", p.get("parameter_id")))
    return errors


def canonical_checks():
    schema, nodes, types, interfaces = [read(p) for p in (SCHEMA, NODES, TYPES, INTERFACES)]
    library, scope, contract, p30 = [read(p) for p in (LIBRARY, SCOPE, CONTRACT, P30)]
    checks = {}

    def check(name, condition, code):
        checks[name] = {"status": "PASS" if condition else "FAIL", "error_code": None if condition else code}

    Draft202012Validator.check_schema(schema)
    check("assembly_schema_valid", True, "SCHEMA_INVALID")
    node_validator = Draft202012Validator({"$ref": "#/$defs/node", "$defs": schema["$defs"]})
    interface_validator = Draft202012Validator({"$ref": "#/$defs/interface", "$defs": schema["$defs"]})
    check("node_schema_records", all(node_validator.is_valid(n) for n in nodes["nodes"]), "SCHEMA_INVALID")
    check("interface_schema_records", all(interface_validator.is_valid(i) for i in interfaces["interfaces"]), "SCHEMA_INVALID")
    expected = {m["component_id"] for m in library["masters"]}
    actual = {n["component_id"] for n in nodes["nodes"]}
    check("approved_master_mapping_6_of_6", len(library["masters"]) == len(nodes["nodes"]) == len(actual) == 6 and actual == expected and all(m["approval_status"].startswith("PRODUCT_OWNER_APPROVED") for m in library["masters"]), "DUPLICATE_COMPONENT_IDENTITY")
    scope_ids = {r["candidate_id"] for r in scope["records"] if r["eligibility_status"] == "MASTER_REQUIRED"}
    check("scope_registry_identity", scope_ids == actual and all(n["node_id"] == n["component_id"] for n in nodes["nodes"]), "REGISTRY_OUTSIDE_FORMAL_NODE")
    check("five_relation_types_only", tuple(t["relation_type"] for t in types["relationship_types"]) == EXPECTED_TYPES, "ILLEGAL_RELATION_TYPE")
    check("relationship_type_contract", all(t.get("directionality") and t.get("required_fields") and t.get("source_node_classes") and t.get("target_node_classes") and isinstance(t.get("self_link_allowed"), bool) and t.get("cycle_policy") for t in types["relationship_types"]), "RELATION_TYPE_INCOMPLETE")
    check("six_interface_owners", {i["owner_node"] for i in interfaces["interfaces"]} == actual and all(i["coordinate_space"] == "MASTER_LOCAL" and i["local_datum"] for i in interfaces["interfaces"]), "BAKED_MANUAL_ASSEMBLY")
    check("interface_unique_ids", len({i["interface_id"] for i in interfaces["interfaces"]}) == len(interfaces["interfaces"]), "DUPLICATE_INTERFACE_ID")
    check("nonhistorical_rules", set(nodes["nonhistorical_qualification_rules"]) == {"PROXY", "CONTROL", "ENVELOPE", "DEFERRED", "UNKNOWN"} and all(r["historical_role"] == "NON_HISTORICAL_FORMAL" and r["qualification_status"] != "FORMAL_APPROVED_MASTER" for r in nodes["nonhistorical_qualification_rules"].values()), "SILENT_HISTORICIZATION")
    check("separate_evidence_fields", "evidence_status" in schema["$defs"]["relationship"]["required"] and "evidence_status" in schema["$defs"]["node"]["required"] and "evidence_basis" in schema["$defs"]["relationship"]["properties"], "RELATION_EVIDENCE_NOT_INDEPENDENT")
    check("building_parameter_isolation", schema["$defs"]["building_parameter"]["properties"]["source_layer"]["enum"] == ["BUILDING_LEVEL_APPROVED", "BUILDING_LEVEL_REPLACEABLE"], "REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY")
    for cid in sorted(actual):
        master = next(m for m in library["masters"] if m["component_id"] == cid)
        params, semantic = read(Path(master["parameter_path"])), read(Path(master["semantic_snapshot_path"]))
        node = next(n for n in nodes["nodes"] if n["component_id"] == cid)
        check("master_identity_" + cid, node["master_id"] == master["master_id"] == params["master_id"] == semantic["master_id"] and node["canonical_name_zh"] == next(c["canonical_name_zh"] for c in contract["master_components"] if c["component_id"] == cid) and semantic["originality_status"] == "unknown", "PROTECTED_BASELINE_MUTATION")
        check("master_binary_hash_" + cid, (ROOT / master["local_binary_path"]).exists() and digest(Path(master["local_binary_path"])) == master["canonical_asset_sha256"], "PROTECTED_BASELINE_MUTATION")
        if "SIX-CHUANFU" in cid:
            values = {p["key"]: p for p in params["parameters"]}
            check("six_chuanfu_reference_boundary_" + cid, values["canonical_reference_length_mm"]["value"] == 1000 and values["canonical_reference_length_mm"]["classification"] == "PROJECT_RULE" and values["historical_full_length_mm"]["value"] is None and values["historical_full_length_mm"]["classification"] == "UNKNOWN" and params["assembly_length_rule"]["default_to_canonical_reference_allowed"] is False, "REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY")
    input_hashes = p30["input_sha256"]
    check("p2_frozen_baseline", all(digest(Path(path)) == expected for path, expected in input_hashes.items()), "PROTECTED_BASELINE_MUTATION")
    frozen_19 = read(BASE / "validation/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json")["p2_frozen_baseline_sha256_after"]
    check("p2_frozen_19_asset_hashes", len(frozen_19) == 19 and all((ROOT / path).exists() and digest(Path(path)) == expected for path, expected in frozen_19.items()), "PROTECTED_BASELINE_MUTATION")
    protected = [P30, SCOPE, LIBRARY, CONTRACT]
    protected += [Path(m[k]) for m in library["masters"] for k in ("parameter_path", "semantic_snapshot_path")]
    check("p3_1_tracked_assets_unchanged", all((ROOT / path).read_bytes() == git_bytes(path) for path in protected), "PROTECTED_BASELINE_MUTATION")
    check("hard_fail_codes_present", all(code in schema["x-hard-fail-codes"] for code in HARD_FAILS), "HARD_FAIL_CONTRACT_WEAKENED")
    empty_graph = {"nodes": nodes["nodes"], "interfaces": interfaces["interfaces"], "relationships": [], "placements": [], "building_parameters": []}
    check("empty_foundation_graph_valid", not validate_graph(empty_graph, nodes, interfaces, types, schema), "FOUNDATION_GRAPH_INVALID")
    master_inputs = [Path(m[k]) for m in library["masters"] for k in ("parameter_path", "semantic_snapshot_path")]
    return checks, {str(p): digest(p) for p in (SCHEMA, NODES, TYPES, INTERFACES, P30, SCOPE, LIBRARY, CONTRACT, *SOURCE_DOCS, *master_inputs)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true", help="run negative tests and write final report")
    parser.add_argument("--graph", type=Path, help="validate an external assembly graph JSON")
    args = parser.parse_args()
    if args.graph:
        errors = validate_graph(json.loads(args.graph.read_text(encoding="utf-8")), read(NODES), read(INTERFACES), read(TYPES), read(SCHEMA))
        print(json.dumps({"status": "FAIL" if errors else "PASS", "errors": errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    checks, hashes = canonical_checks()
    tests = {"passed": 0, "total": 0, "status": "NOT_RUN"}
    if args.report:
        suite = unittest.defaultTestLoader.discover(str(ROOT / BASE / "tests"), pattern="test_p3_2_relationship_foundation_v001.py")
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
        tests = {"passed": result.testsRun - len(result.failures) - len(result.errors), "total": result.testsRun, "status": "PASS" if result.wasSuccessful() else "FAIL"}
    hard_fail_examples = {"REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY": "test_six_chuanfu_reference_length_leak", "SILENT_HISTORICIZATION": "test_nonhistorical_silent_upgrade", "BAKED_MANUAL_ASSEMBLY": "test_world_coordinate_only_placement"}
    hard_fails_canonical = sorted({c["error_code"] for c in checks.values() if c["status"] == "FAIL" and c["error_code"] in HARD_FAILS})
    report = {"task": "T-015", "version": "V001", "status": "PASS" if all(c["status"] == "PASS" for c in checks.values()) and tests["status"] in ("PASS", "NOT_RUN") else "FAIL", "checks": checks, "check_pass_count": sum(c["status"] == "PASS" for c in checks.values()), "check_total": len(checks), "negative_tests": tests, "hard_fail_trigger_tests": hard_fail_examples, "hard_fails_canonical": hard_fails_canonical, "input_sha256": hashes, "gate_status": "ENGINEERING_COMPLETE_REVIEW_REQUIRED_NOT_P3_2_PASS"}
    if args.report:
        (ROOT / REPORT).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "check_pass_count", "check_total", "negative_tests")}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
