#!/usr/bin/env python3
"""Full T-008 clean rebuild, independent reopen, and test-only mutations."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[3]
CASE=ROOT/"production/zhenguo_wanfo"
GEN=CASE/"scripts/generate_p2_3_integrated_reconstruction_v001.py"
QC=CASE/"scripts/validate_p2_3_integrated_reconstruction_v001.py"
BLENDER=Path("/Applications/Blender.app/Contents/MacOS/Blender")
EVIDENCE=CASE/"validation/P2_3_REBUILD_MUTATION_EVIDENCE_V001.json"

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def run(*args):
    proc=subprocess.run([str(x) for x in args],cwd=ROOT,capture_output=True,text=True,timeout=180)
    if proc.returncode:
        raise AssertionError("Command failed (%d): %s\n%s\n%s"%(proc.returncode,args,proc.stdout[-2000:],proc.stderr[-2000:]))
    return proc

class IntegratedReconstructionTests(unittest.TestCase):
    def test_clean_rebuild_reopen_and_mutation(self):
        self.assertTrue(BLENDER.is_file())
        formal_path=CASE/"params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
        override_path=CASE/"params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json"
        library_path=CASE/"components/P2_3_COMPONENT_LIBRARY_V001.json"
        original_hashes={str(p.relative_to(ROOT)):digest(p) for p in (formal_path,override_path,library_path)}
        with tempfile.TemporaryDirectory(prefix="p2_3_t008_") as raw:
            temp=Path(raw)
            def build(label,extra=()):
                out=temp/(label+".blend")
                manifest=temp/(label+"_manifest.json")
                summary=temp/(label+"_summary.json")
                run(BLENDER,"--background","--factory-startup","--python-exit-code","10","--python",GEN,
                    "--","--no-review","--output",out,"--manifest",manifest,"--summary",summary,*extra)
                return json.loads(summary.read_text()),out,manifest
            first,first_blend,first_manifest=build("clean_1")
            second,second_blend,second_manifest=build("clean_2")
            self.assertEqual(first,second)
            reopen=[]
            for label,blend,manifest in (("clean_1",first_blend,first_manifest),("clean_2",second_blend,second_manifest)):
                result=temp/(label+"_qc.json")
                run(BLENDER,"--background",blend,"--python-exit-code","10","--python",QC,"--","--manifest",manifest,"--result",result)
                evidence=json.loads(result.read_text())
                self.assertEqual(evidence["status"],"PASS")
                reopen.append({"label":label,"status":evidence["status"],"checks":len(evidence["checks"])})
            formal=json.loads(formal_path.read_text())
            overrides=json.loads(override_path.read_text())
            # Synthetic replacement: the approved 11 x MOD-006 formula is kept;
            # its modular source and the sidecar cache change only under /tmp.
            fen=formal["parameters"]["MOD-002"]["value"]
            formal["parameters"]["MOD-005"]["value"]+=1
            new_cai=round(formal["parameters"]["MOD-005"]["value"]*fen,5)
            formal["parameters"]["MOD-006"]["value"]=new_cai
            overrides["overrides"]["Z-006-RC-01"]["current_resolved_value"]=round(11*new_cai,5)
            mut_params=temp/"params_mutation.json"
            mut_overrides=temp/"overrides_mutation.json"
            mut_params.write_text(json.dumps(formal,ensure_ascii=False))
            mut_overrides.write_text(json.dumps(overrides,ensure_ascii=False))
            rc,_,_=build("rc_mutation",("--params",mut_params,"--overrides",mut_overrides))
            self.assertIsNone(formal["parameters"]["Z-006"]["value"])
            self.assertEqual(rc["historical_Z_006"],first["historical_Z_006"])
            self.assertNotEqual(rc["candidate_RC_01_mm"],first["candidate_RC_01_mm"])
            self.assertEqual(rc["candidate_RC_01_mm"],round(11*new_cai,5))
            self.assertEqual(rc["instance_ids"],first["instance_ids"])
            self.assertEqual(rc["family_counts"],first["family_counts"])
            # Every column endpoint and roof control follows the RC source.
            self.assertNotEqual(rc["key_dimensions_mm"]["roof_control_z"],first["key_dimensions_mm"]["roof_control_z"])
            library=json.loads(library_path.read_text())
            library["graphic_only_rules"]["contact_block_fraction"]=0.6
            mut_library=temp/"library_mutation.json"
            mut_library.write_text(json.dumps(library,ensure_ascii=False))
            variant,_,_=build("variant_mutation",("--library",mut_library))
            changed={name for name in first["mapping"] if first["mapping"][name]!=variant["mapping"][name]}
            self.assertEqual(changed,{name for name in first["mapping"] if name.startswith("CONTACT_")})
            self.assertEqual(len(changed),88)
            self.assertEqual(variant["instance_ids"],first["instance_ids"])
            self.assertEqual(variant["family_counts"],first["family_counts"])
            self.assertEqual(original_hashes,{str(p.relative_to(ROOT)):digest(p) for p in (formal_path,override_path,library_path)})
            evidence={"task":"T-008","status":"PASS","clean_builds":2,"semantic_equal":True,
                      "semantic_sha256":hashlib.sha256(json.dumps(first,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
                      "independent_reopens":reopen,
                      "RC_mutation":{"test_only":True,"source":"MOD-005 -> MOD-006 -> Z-006-RC-01",
                                     "before_mm":first["candidate_RC_01_mm"],"after_mm":rc["candidate_RC_01_mm"],
                                     "instances_retained":len(rc["instance_ids"]),"historical_Z_006_unchanged":True,
                                     "roof_control_changed":True},
                      "variant_mutation":{"test_only":True,"family":"BRACKET_CONTACT","graphic_fraction_before":0.5,
                                          "graphic_fraction_after":0.6,"changed_instances":len(changed),"unrelated_mapping_stable":True},
                      "formal_input_hashes_unchanged":original_hashes}
            EVIDENCE.parent.mkdir(parents=True,exist_ok=True)
            EVIDENCE.write_text(json.dumps(evidence,ensure_ascii=False,sort_keys=True,indent=2)+"\n")

if __name__=="__main__": unittest.main()
