"""Read-only independent cross-check V001 extracts against actual original repository inputs."""
from pathlib import Path
import subprocess,json,hashlib,ast,math
import trimesh,numpy as np
R=Path(__file__).resolve().parents[2];T=Path(__file__).resolve().parent;O=R/'review/gong_ang_form_v001'
def raw(ref,path):return subprocess.check_output(['git','show',ref+':'+path],cwd=R)
main='414be293918fea2bf4138b1a8f4345272e8764a8';pr75='f8f72d40dd47ab61abc3103c396c855f5c4c3865'
masterpath='production/zhenguo_wanfo/component_library/masters/CMP-GONG-ANG-001/CMP-GONG-ANG-001_MASTER_SEMANTIC_V001.json'
b=raw(main,masterpath);assert b==(O/'sources/ANG_MASTER_SEMANTIC.json').read_bytes()
s=json.loads(b);out=[]
for body in s['canonical_bodies']:
 d=json.loads((O/'geometry'/(body['body_id']+'_master.json')).read_text())
 assert np.allclose(np.sort(np.array(body['geometry_vertices_mm']),axis=0),np.sort(np.array(d['vertices']),axis=0),atol=1e-9)
path='production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WANFO_WEST_SPACER_89_TRIAL_V001.glb'
b=raw(pr75,path);h=hashlib.sha256(b).hexdigest();assert h=='ed686f2ed81dc0ad0139a320bdd0c99709419c1c401bc1dff3b3635867f5a151'
import io
scene=trimesh.load(io.BytesIO(b),file_type='glb',force='scene',process=False);assert len(scene.graph.nodes_geometry)==89
for k in ['TOU','ER']:
 name='trial:EAST_FRONT_'+k+'_ANG_LOCAL';tf,g=scene.graph[name];m=scene.geometry[g].copy();m.apply_transform(tf)
 v=m.vertices[:,[0,2,1]]*np.array([1,-1,1]);v=v[:,[1,0,2]];v[:,1]*=-1;v-=(v.max(0)+v.min(0))/2
 d=json.loads((O/'geometry'/('EAST_FRONT_'+k+'_ANG_LOCAL_trial.json')).read_text());a=np.array(d['vertices']);assert np.max(abs(v-a))<1e-8;assert np.array_equal(m.faces,np.array(d['faces']))
 out.append(dict(id=name,vertices_exact=True,faces_exact=True,source_sha256=h))
(T/'INPUT_MODEL_VERIFICATION.json').write_text(json.dumps(dict(status='PASS',main=main,PR75=pr75,master_semantic_byte_exact=True,master_vertices_exact=True,actual_89_glb_hash=h,actual_89_meshes=89,trial_extracts=out,method='Original Git blobs read; actual GLB node transforms and V001 observation transform independently reapplied'),ensure_ascii=False,indent=2)+'\n')
print('Original master and actual PR75 GLB extracts PASS')
