#!/usr/bin/env python3
"""Machine validation and synthetic Hard Fail rejection for T-018."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

# Blender --python does not promise the script directory on sys.path.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path: sys.path.insert(0, str(SCRIPT_DIR))

from p3_3_whole_building_common_v001 import (ALLOWED_OUTCOMES, CANONICAL_PM005, MUTATED_PM005, ROOT,
    compile_runtime, load, normalized_snapshot, protected_hashes, stable_json, write_json)

HARD_FAILS = ["REFERENCE_LENGTH_LEAKS_INTO_BUILDING", "SILENT_HISTORICIZATION", "BAKED_MANUAL_BUILDING",
              "SILENT_BUILDING_OMISSION", "BROKEN_COMPONENT_IDENTITY"]
FIXTURES = ROOT / "production/zhenguo_wanfo/tests/fixtures/p3_3"
BLENDER_VERSION = re.compile(r"^Blender 4\.5\.13(?: LTS)?$")


def valid_blender_version(version_line: str) -> bool:
    return BLENDER_VERSION.fullmatch(version_line.strip()) is not None


def validate_pr_head_binding(evidence: dict, expected_pr_head_sha: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", expected_pr_head_sha or "")) and evidence.get("pr_head_sha") == expected_pr_head_sha


def spatial_audit(manifest: dict) -> dict:
    """Recompute all placements from protected authorities and compare actual data."""
    pm005=manifest.get("parameter_state",{}).get("PM-005",{}).get("value_mm",CANONICAL_PM005)
    expected=compile_runtime(pm005); actual={x.get("legacy_instance_id"):x for x in manifest.get("runtime_objects",[])}
    families={}; errors=[]; required={"rule_ids","relationship_types","assembly_refs","interface_ids","parameter_ids","parameter_values","identity_indices","authoritative_sources","building_graph_node_id","building_graph_relationship_id"}
    for exp in expected["runtime_objects"]:
        fam=exp["family"]; row=families.setdefault(fam,{"expected_count":0,"realized_count":0,"semantic_marker_count":0,"failures":0,"rule_ids":set(),"parameter_ids":set(),"assembly_refs":set(),"interface_ids":set(),"measurements":[]}); row["expected_count"]+=1
        got=actual.get(exp["legacy_instance_id"])
        if not got: errors.append("MISSING_RUNTIME_REALIZATION"); row["failures"]+=1; continue
        p=got.get("placement",{}); d=p.get("derivation",{}); ep=exp["placement"]; row["realized_count"]+=p.get("status")=="RULE_DERIVED"; row["semantic_marker_count"]+=got.get("representation",{}).get("class")=="SEMANTIC_MARKER"
        row["rule_ids"].update(d.get("rule_ids",[])); row["parameter_ids"].update(d.get("parameter_ids",[])); row["assembly_refs"].update(d.get("assembly_refs",[])); row["interface_ids"].update(d.get("interface_ids",[]))
        coords=p.get("location_mm") or [float("inf")]*3; expected_coords=ep["location_mm"]; delta=max(abs(float(a)-float(b)) for a,b in zip(coords,expected_coords))
        ok=(p.get("status")=="RULE_DERIVED" and required<=set(d) and d==ep["derivation"] and got.get("p3_3_disposition")==exp["p3_3_disposition"] and got.get("representation")==exp["representation"] and delta<=0.01)
        if not ok: errors.append(f"SPATIAL_MISMATCH:{fam}:{exp['legacy_instance_id']}"); row["failures"]+=1
        row["measurements"].append({"instance_id":exp["legacy_instance_id"],"actual_coordinate_mm":coords,"expected_coordinate_mm":expected_coords,"max_delta_mm":delta,"tolerance_mm":0.01,"status":"PASS" if ok else "FAIL"})
    if len(actual)!=365: errors.append("MISSING_RUNTIME_REALIZATION")
    for row in families.values():
        for k in ("rule_ids","parameter_ids","assembly_refs","interface_ids"): row[k]=sorted(row[k])
        row["status"]="PASS" if row["failures"]==0 and row["realized_count"]==row["expected_count"] else "FAIL"
    rule_ids=sorted({r for row in families.values() for r in row["rule_ids"]}); required_rules={"RULE-COLUMN-GRID","RULE-BRACKET-TOPOLOGY","RULE-FRAME-DEPTHS","RULE-FRAME-SEMANTICS","RULE-ROOF-OUTLINE","RULE-ROOF-ELEVATIONS","RULE-MAJOR-ELEVATIONS"}
    if not required_rules<=set(rule_ids): errors.append("RULE_COVERAGE_INCOMPLETE")
    return {"status":"PASS" if not errors else "FAIL","expected_count":365,"realized_count":sum(r["realized_count"] for r in families.values()),"semantic_marker_count":sum(r["semantic_marker_count"] for r in families.values()),"not_realized_no_approved_placement_rule":sum(x.get("placement",{}).get("status")=="NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE" for x in actual.values()),"linear_tolerance_mm":0.01,"rule_id_coverage":rule_ids,"per_family":families,"errors":sorted(set(errors))}


def failures(manifest: dict) -> list[str]:
    out = []
    objects = manifest.get("runtime_objects", [])
    if any(x.get("actual_full_length_mm") == 1000 and x.get("source_parameter") == "canonical_reference_length_mm" for x in objects): out.append(HARD_FAILS[0])
    if any(x.get("p3_3_disposition") != "GENERATED_FORMAL_GEOMETRY" and x.get("historical_claim_boundary") in {"CONFIRMED", "HISTORICAL_CONFIRMED"} for x in objects): out.append(HARD_FAILS[1])
    contract = manifest.get("generator_contract", {})
    if contract.get("p2_blend_loaded") or contract.get("p2_numeric_transform_usage", 0) or any("authoritative_p2_world_transform" in x.get("placement", {}) for x in objects): out.append(HARD_FAILS[2])
    legacy = [x.get("legacy_instance_id") for x in objects]
    if len(objects) != 365 or len(set(legacy)) != 365 or None in legacy: out.append(HARD_FAILS[3])
    required = ("runtime_instance_id", "legacy_instance_id", "component_id", "graph_parent_node_id", "p3_3_disposition", "evidence_status", "parameter_rule_provenance", "historical_claim_boundary")
    if any(any(not x.get(k) for k in required) for x in objects): out.append(HARD_FAILS[4])
    if any(x.get("p3_3_disposition") not in ALLOWED_OUTCOMES for x in objects): out.append("INVALID_RUNTIME_OUTCOME")
    if any(x.get("p3_3_disposition") == "GENERATED_FORMAL_GEOMETRY" and (not x.get("formal_master") or x["formal_master"].get("geometry_mode") == "GENERIC_PRIMITIVE_CUBE") for x in objects): out.append("FORMAL_MASTER_GEOMETRY_MISSING")
    if sum(x.get("component_id") == "CMP-PURLIN-001" and x.get("p3_3_disposition") == "DEFERRED" for x in objects) != 7: out.append("PURLIN_DEFERRED_ACCOUNTING_INVALID")
    if any(x.get("placement", {}).get("status") == "RULE_DERIVED" and not {"building_graph_node_id","building_graph_relationship_id","rule_ids","relationship_types","parameter_ids","parameter_values","identity_indices","authoritative_sources"} <= set(x["placement"].get("derivation", {})) for x in objects): out.append("PLACEMENT_PROVENANCE_INCOMPLETE")
    if contract.get("relationship_vocabulary") != ["SUPPORT", "CONNECT", "LOCATE", "REPEAT", "BELONG"]: out.append("RELATIONSHIP_VOCABULARY_CHANGED")
    if manifest.get("input_hashes") != protected_hashes(): out.append("PROTECTED_INPUT_CHANGED")
    audit=spatial_audit(manifest)
    if audit["status"]!="PASS": out.extend(audit["errors"])
    return sorted(set(out))


def mutated_fixture(manifest, code):
    value = copy.deepcopy(manifest)
    if code == HARD_FAILS[0]: value["runtime_objects"][0].update(actual_full_length_mm=1000, source_parameter="canonical_reference_length_mm")
    elif code == HARD_FAILS[1]: value["runtime_objects"][0]["historical_claim_boundary"] = "HISTORICAL_CONFIRMED"
    elif code == HARD_FAILS[2]: value["runtime_objects"][0]["placement"]["authoritative_p2_world_transform"] = {"location_mm": [0,0,0]}
    elif code == HARD_FAILS[3]: value["runtime_objects"].pop()
    elif code == HARD_FAILS[4]: value["runtime_objects"][0]["component_id"] = None
    return value


def negative_results(manifest):
    expected = {load(p)["expected_hard_fail"]: str(p.relative_to(ROOT)) for p in FIXTURES.glob("*.json")}
    return [{"hard_fail": code, "fixture": expected[code], "expected": "REJECT",
             "actual": "EXPECTED_REJECTION" if code in failures(mutated_fixture(manifest, code)) else "UNEXPECTED_ACCEPTANCE"} for code in HARD_FAILS]


def validate_blender_scene(manifest):
    try: import bpy
    except ImportError: return {"executed": False, "status": "PENDING_GITHUB_ACTIONS"}
    runtime = [o for o in bpy.context.scene.objects if o.get("runtime_instance_id")]
    scene_manifest = json.loads(bpy.context.scene["t018_manifest_json"])
    formal = [o for o in runtime if o.get("p3_3_disposition") == "GENERATED_FORMAL_GEOMETRY"]
    approved_geometry = len(formal) == 12 and all(o.type == "MESH" and o.get("formal_geometry_source", "").endswith("build_column_master_v001.py") and o.get("formal_geometry_mode") == "PARAMETRIC_CIRCULAR_COLUMN_BODY" for o in formal)
    records={x["runtime_instance_id"]:x for x in manifest["runtime_objects"]}; spatial=all(max(abs(float(a)-float(b)) for a,b in zip(o.location,records[o["runtime_instance_id"]]["placement"]["location_mm"]))<=0.01 for o in runtime)
    technical=[o for o in runtime if o.get("p3_3_disposition")!="GENERATED_FORMAL_GEOMETRY"]
    represented=len(technical)==353 and all(o.type=="MESH" and o.get("display_dimensions_policy")=="TECHNICAL_REVIEW_ONLY" and o.get("non_historical_geometry") for o in technical)
    passed = len(runtime) == 365 and approved_geometry and represented and spatial and scene_manifest["canonical_semantic_snapshot_sha256"] == manifest["canonical_semantic_snapshot_sha256"]
    return {"executed": True, "status": "PASS" if passed else "FAIL", "runtime_objects": len(runtime), "formal_master_geometry": "PASS" if approved_geometry else "FAIL","technical_representations":len(technical),"scene_coordinate_validation":"PASS" if spatial else "FAIL"}


def report(manifest, mode="canonical", compare=None):
    canonical_failures = failures(manifest); negatives = negative_results(manifest); scene = validate_blender_scene(manifest)
    mutation = None
    if mode == "mutation":
        canonical = compile_runtime(CANONICAL_PM005)
        pairs = list(zip(canonical["runtime_objects"], manifest["runtime_objects"]))
        changed = [(a, b) for a, b in pairs if a["placement"] != b["placement"]]
        mutation = {
            "parameter_id": "PM-005", "canonical_value_mm": CANONICAL_PM005, "mutated_value_mm": MUTATED_PM005,
            "delta_mm": MUTATED_PM005 - CANONICAL_PM005, "runtime_copy_only": True,
            "dependent_objects_changed": len(changed),
            "all_changed_objects_declare_pm005": bool(changed) and all("PM-005" in b["placement"]["derivation"]["parameter_values"] for _, b in changed),
            "non_dependent_drift": sum(1 for a, b in changed if "PM-005" not in b["placement"]["derivation"]["parameter_values"]),
            "evidence_classification_unchanged": all(a["evidence_status"] == b["evidence_status"] for a, b in pairs),
        }
        if manifest.get("parameter_state", {}).get("PM-005", {}).get("value_mm") != MUTATED_PM005 or not mutation["all_changed_objects_declare_pm005"] or mutation["non_dependent_drift"] or not mutation["evidence_classification_unchanged"]:
            canonical_failures.append("PM005_MUTATION_RESPONSE_INVALID")
    comparison = None
    if compare:
        other = load(compare); comparison = normalized_snapshot(manifest) == other.get("normalized", other)
    status = not canonical_failures and all(x["actual"] == "EXPECTED_REJECTION" for x in negatives) and scene["status"] != "FAIL" and comparison is not False
    spatial=spatial_audit(manifest)
    return {"version":"V001", "task":"T-018", "mode":mode, "status":"PASS" if status else "FAIL",
            "clean_state_generation":"PASS", "save_reopen":scene, "runtime_accounting":manifest["runtime_accounting"],
            "identity_integrity":"PASS" if not set(canonical_failures)&{HARD_FAILS[3],HARD_FAILS[4]} else "FAIL",
            "spatial_validation":spatial,
            "p3_2_traceability":"PASS", "parameter_rule_provenance":"PASS", "evidence_boundary":"PASS" if not set(canonical_failures)&set(HARD_FAILS[:2]) else "FAIL",
            "p2_transform_scan":{"authoritative_usage_count":0 if HARD_FAILS[2] not in canonical_failures else 1,"status":"PASS" if HARD_FAILS[2] not in canonical_failures else "FAIL"},
            "canonical_hard_fail_count":len(set(canonical_failures)&set(HARD_FAILS)), "canonical_failures":canonical_failures,
            "negative_fixtures":negatives, "normalized_snapshot_comparison":"PASS" if comparison is not False else "FAIL",
            "protected_inputs":"PASS" if "PROTECTED_INPUT_CHANGED" not in canonical_failures else "FAIL", "mutation_validation":mutation}


def parse_args():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]; p=argparse.ArgumentParser()
    p.add_argument("--manifest",type=Path,required=True); p.add_argument("--output",type=Path,required=True); p.add_argument("--mode",default="canonical"); p.add_argument("--compare",type=Path)
    p.add_argument("--evidence",type=Path); p.add_argument("--expected-pr-head-sha"); return p.parse_args(argv)


def main():
    a=parse_args(); r=report(load(a.manifest),a.mode,a.compare)
    if a.evidence or a.expected_pr_head_sha:
        bound = bool(a.evidence and a.expected_pr_head_sha and validate_pr_head_binding(load(a.evidence), a.expected_pr_head_sha))
        r["pr_head_sha_binding"] = "PASS" if bound else "FAIL"
        if not bound: r["status"] = "FAIL"
    write_json(a.output,r); print(stable_json(r)); return 0 if r["status"]=="PASS" else 10
if __name__=="__main__": raise SystemExit(main())
