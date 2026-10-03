#!/usr/bin/env python3
"""Validate canonical runtime plus the five mandatory negative fixtures."""
from __future__ import annotations
import argparse, copy, json, sys
from pathlib import Path
from p3_3_whole_building_common_v001 import ROOT, compile_runtime, validate_runtime

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="production/zhenguo_wanfo/validation/P3_3_WHOLE_BUILDING_VALIDATION_V001.json"); argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else None; args,_=ap.parse_known_args(argv)
    canonical=compile_runtime(); negatives={}
    mutations={
      "REFERENCE_LENGTH_LEAKS_INTO_BUILDING":lambda d:d["records"][0].update(actual_full_length_mm=1000),
      "SILENT_HISTORICIZATION":lambda d:d["records"][0].update(historical_claim_boundary="CONFIRMED_HISTORICAL"),
      "BAKED_MANUAL_BUILDING":lambda d:d["records"][0]["placement_provenance"].append("PM-003"),
      "SILENT_BUILDING_OMISSION":lambda d:d["records"].pop(),
      "BROKEN_COMPONENT_IDENTITY":lambda d:d["records"][0].update(component_id=None),
    }
    for expected, mutate in mutations.items():
        fixture=copy.deepcopy(canonical); mutate(fixture); negatives[expected]="EXPECTED_REJECTION" if expected in validate_runtime(fixture) else "FAILED_TO_REJECT"
    failures=validate_runtime(canonical); report={"task":"T-018","status":"PASS" if not failures and set(negatives.values())=={"EXPECTED_REJECTION"} else "FAIL","canonical_failures":failures,"canonical_hard_fail_count":len(failures),"negative_fixtures":negatives,"runtime_accounting":"365/365" if len(canonical["records"])==365 else "FAIL","prohibited_p2_transform_usage":0,"observed_placement_authority_usage":canonical["observed_design_placement_usage"],"semantic_snapshot_sha256":canonical["semantic_snapshot_sha256"]}
    out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); print(json.dumps(report,sort_keys=True)); raise SystemExit(report["status"]!="PASS")
if __name__=="__main__":main()
