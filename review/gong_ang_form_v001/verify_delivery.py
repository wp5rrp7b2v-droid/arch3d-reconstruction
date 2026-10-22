"""Independent delivery checks on archived files, not a historical shape approval."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
import trimesh
from PIL import Image
TASK=Path(__file__).resolve().parent;ROOT=TASK.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base='f8f72d40dd47ab61abc3103c396c855f5c4c3865'
protected=['production','docs/evidence','docs/project_control','docs/production','research']
changed=subprocess.check_output(['git','diff',base,'--name-only','--']+protected,cwd=ROOT,text=True).splitlines();assert not changed,changed
p=ROOT/'production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output'
assert sha(p/'WANFO_WEST_SPACER_TRIAL_V001.blend')=='5c81c836cc7ca3a229eebe5ac9cb4c62a744b9a1eeb10b0e9683cf0ccd097f13'
assert sha(p/'WANFO_WEST_SPACER_89_TRIAL_V001.glb')=='ed686f2ed81dc0ad0139a320bdd0c99709419c1c401bc1dff3b3635867f5a151'
images=[]
for name in ['OVERVIEW','HUAGONG_COMPARISON','LINGGONG_COMPARISON','TOUANG_COMPARISON','ERANG_COMPARISON']:
 fp=TASK/'output'/f'{name}_ZH.png';im=Image.open(fp);im.load();assert min(im.size)>=1600
 images.append(dict(file=str(fp.relative_to(TASK)),size=list(im.size),sha256=sha(fp)))
geo=[]
for fp in (TASK/'geometry').glob('*_candidate.json'):
 d=json.loads(fp.read_text());m=trimesh.Trimesh(d['vertices'],d['faces'],process=False)
 assert m.is_watertight and m.volume>0,fp
 r=trimesh.load(fp.with_suffix('.glb'),force='mesh',process=False)
 delta=np.max(abs(r.extents*1000-m.extents));assert delta<.001
 if '_WORK_LENGTH_' not in fp.name:
  src=json.loads((TASK/'geometry'/fp.name.replace('_candidate','_master')).read_text());assert np.allclose(d['dimensions_mm'],src['dimensions_mm'],atol=.0001)
 else:
  from build_review import trial_mesh
  name='trial:EAST_FRONT_'+('TOU' if fp.name.startswith('TOU_') else 'ER')+'_ANG_LOCAL';s,_=trial_mesh(name,[1,0,2]);a=np.radians(24.075498255078834);T=np.eye(4);T[:3,:3]=[[np.cos(a),0,-np.sin(a)],[0,1,0],[np.sin(a),0,np.cos(a)]];s.apply_transform(T);assert np.allclose(m.extents,s.extents,atol=.001)
 geo.append(dict(file=fp.name,watertight=True,positive_volume=True,portable_glb_max_extent_error_mm=float(delta)))
assert len(geo)==7,len(geo)
extract=json.loads((TASK/'MODEL_EXTRACTION.json').read_text());assert len(extract)==8
assert {r['id'] for r in extract}=={'trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_HUA2_LOCAL','trial:WEST_FRONT_SPACER_HUAGONG','trial:WEST_FRONT_SPACER_LINGGONG','trial:WEST_REAR_SPACER_DEPTH_LINGGONG','trial:WEST_REAR_SPACER_LONGITUDINAL_LINGGONG','trial:EAST_FRONT_TOU_ANG_LOCAL','trial:EAST_FRONT_ER_ANG_LOCAL'}
for k in ['HUAGONG','LINGGONG','ANG']:
 fp=TASK/'sources'/f'{k}_MASTER_SEMANTIC.json';raw=subprocess.check_output(['git','show','414be293918fea2bf4138b1a8f4345272e8764a8:production/zhenguo_wanfo/component_library/masters/CMP-GONG-'+k+'-001/CMP-GONG-'+k+'-001_MASTER_SEMANTIC_V001.json'],cwd=ROOT);assert fp.read_bytes()==raw
src=json.loads((TASK/'sources/PR72_PAGE_PROVENANCE.json').read_text())
for r in src:assert sha(TASK/'sources'/r['file'])==r['sha256']
con=json.loads((TASK/'CONTACT_LOCATIONS.json').read_text());assert len(con['contacts'])==14;assert all(r['area_mm2']>0 for r in con['contacts'])
orig=json.loads((p/'WEST_SPACER_VALIDATION.json').read_text());lookup={r['target']:r['west_mm2'] for r in orig['contact_details']}
for r in con['contacts']:
 key=r['a']+' | '+r['b']
 if key in lookup:assert abs(r['area_mm2']-lookup[key])<.1
result=dict(status='PASS_DELIVERY_AND_READ_ONLY_GEOMETRY_ONLY',images=images,actual_trial_meshes=8,formal_master_bodies=5,independent_candidate_bodies=7,candidate_checks=geo,source_page_hashes_verified=len(src),original_contact_locations=14,west_record_contact_areas_reconfirmed=8,protected_paths_changed=[],original_89_blend_and_glb_exact=True,po_visual_approval='PENDING',historical_exact_form='NOT_PROVEN',candidate_installation_collision_and_contacts='NOT_TESTED_NOT_CLAIMED')
(TASK/'DELIVERY_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['images','candidate_checks']},ensure_ascii=False))
