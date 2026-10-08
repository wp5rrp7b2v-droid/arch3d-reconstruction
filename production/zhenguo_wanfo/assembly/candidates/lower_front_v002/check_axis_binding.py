"""Read-only axis/length diagnostic; does not export a revised approved model."""
import ast, json, math, hashlib, warnings
from pathlib import Path
from functools import reduce
import numpy as np
import trimesh, manifold3d
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
for node in ast.parse((ROOT/'lower_front/check_lower_front.py').read_text()).body:
    if isinstance(node,ast.FunctionDef):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
g=json.loads((OUT/'GEOMETRY.json').read_text())
new={k:trimesh.Trimesh(v['vertices'],v['faces'],process=False) for k,v in g.items()}
bad=json.loads((OUT/'CHECKS.json').read_text())['bad_pairs']
results=[]; evidence=[]; hashes={}
for side,folder,file in [('east','east_v011','REOPENED_V11_MESHES.json'),('west','west_v002','REOPENED_WEST_V002_MESHES.json')]:
    path=ROOT/folder/file; raw=path.read_bytes(); hashes[str(path)]=hashlib.sha256(raw).hexdigest()
    obj=next(o for o in json.loads(raw)['objects'] if o['id']=='FOUR_BEAM')
    beam=trimesh.Trimesh(obj['vertices'],obj['faces'],process=False)
    beam.apply_translation([4437 if side=='east' else 0,0,0])
    evidence.append({'side':side,'mesh_evidence':obj.get('evidence'),'actual_length_mm':float(beam.extents[1]),'upper_axis_Y_mm':1836,'lower_trial_axis_Y_mm':3596,'length_class':'working hypothesis, not measured timber length'})
    failures=[p for p in bad if p['b']==side+':FOUR_BEAM']
    for length in [7192.,7000.,6600.,6000.,5000.,4400.,4200.]:
        # Analytical clipping copy only; unmeasured choices are not new candidate dimensions.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',RuntimeWarning)
            clip=box([1000,length,2000],[4437 if side=='east' else 0,0,-500])
            diagnostic=boolean64([beam,clip],'intersection')
            volumes=[{'object':p['a'],'overlap_mm3':vol(new[p['a']],diagnostic)} for p in failures]
        results.append({'side':side,'diagnostic_length_mm':length,'failed_of_original_five':sum(p['overlap_mm3']>1 for p in volumes),'overlaps':volumes})
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
baseline={p['a']:p['overlap_mm3'] for p in bad}
assert all(abs(p['overlap_mm3']-baseline[p['object']])<1 for c in results if c['diagnostic_length_mm']==7192 for p in c['overlaps'])
report={'status':'AXIS_LENGTH_BINDING_REVIEW_REQUIRED','scope':'14 length cases x 5 known failed pairs; not a full revised assembly feasibility test','pairs_checked':len(results)*5,'evidence':evidence,'cases':results,'approved_source_files_unchanged':True,'formal_candidate_exported':False,'source_review':{'PDF82':'four beam above upper six beam; gap single gong with scattered dou, no ludou','PDF287_292_293':'cross-sections place shorter upper beam at upper purlin group; lower purlin group at outer upper-six region; visual topology only, not scaled precise endpoints','PDF342':'four-beam measured sections, no total length','PDF105_106':'B is relative level difference, not independent model absolute elevation'},'boundary':'Reduction of these five known collisions by clipping only isolates length sensitivity; it does not validate a shorter beam, preserve all other brace contacts, or authorize changing approved geometry.'}
(OUT/'AXIS_BINDING_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pairs_checked':report['pairs_checked'],'cases':[{k:v for k,v in q.items() if k!='overlaps'} for q in results],'unchanged':True},ensure_ascii=False))
