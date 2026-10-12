import json,sys,itertools,hashlib
from pathlib import Path
import numpy as np,trimesh,manifold3d as mf
from shapely.geometry import Polygon
root=Path(sys.argv[1]);out=root/'output';source=json.loads((root/'INPUT_GEOMETRY.json').read_text());actual=json.loads((out/'REOPENED_V003_MESHES.json').read_text());ss={o['id']:o for o in source['objects']};aa={o['id']:o for o in actual['objects']};assert set(ss)==set(aa) and len(aa)==82
meshes={k:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for k,o in aa.items()};sm={k:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for k,o in ss.items()};maxdelta=0
for k in ss:
 assert ss[k]['faces']==aa[k]['faces'];delta=float(np.max(abs(np.array(ss[k]['vertices'])-aa[k]['vertices'])));assert delta<.001,(k,delta);maxdelta=max(maxdelta,delta);assert aa[k]['effective_status']==ss[k]['effective_status'];assert meshes[k].is_volume and len(meshes[k].split(only_watertight=False))==1
base=json.loads((root/'BASE_REOPENED_V002.json').read_text());bb={o['id']:o for o in base['objects']}
for k in source['unchanged_original_ids']:
 assert aa[k]['local_vertices']==bb[k]['local_vertices'] and aa[k]['matrix_world']==bb[k]['matrix_world'] and aa[k]['faces']==bb[k]['faces'],k
def man(v,f):return mf.Manifold(mf.Mesh64(vert_properties=np.array(v,dtype='f8',order='C'),tri_verts=np.array(f,dtype='u8',order='C')))
pair_count=0;maximum=0;fails=[]
for a,b in itertools.combinations(meshes,2):
 x,y=meshes[a],meshes[b];lo=np.maximum(x.bounds[0],y.bounds[0]);hi=np.minimum(x.bounds[1],y.bounds[1]);vol=0.
 if np.all(hi>lo):
  c=(hi+lo)/2;vol=abs(float((man(x.vertices-c,x.faces)^man(y.vertices-c,y.faces)).volume()))
 pair_count+=1;maximum=max(maximum,vol)
 if vol>1:fails.append({'a':a,'b':b,'overlap_mm3':vol})
def surface(ma,mb,down=False):
 total=0
 for i,tr in enumerate(ma.triangles):
  n=ma.face_normals[i]
  if down and n[2]>=-1e-8:continue
  u=tr[1]-tr[0];u/=np.linalg.norm(u);v=np.cross(n,u);origin=tr[0];pa=Polygon(np.column_stack([(tr-origin)@u,(tr-origin)@v]))
  for k,t in enumerate(mb.triangles):
   if np.dot(n,mb.face_normals[k])>-1+1e-7 or np.max(abs((t-origin)@n))>.001:continue
   pb=Polygon(np.column_stack([(t-origin)@u,(t-origin)@v]));total+=pa.intersection(pb).area*(-n[2] if down else 1)
 return total
contacts=[]
for c in source['contacts']:
 a,b=c['a'],c['b'];area=surface(meshes[a],meshes[b]);ref=surface(sm[a],sm[b]);dp=surface(meshes[a],meshes[b],True) if c['downward_required'] else None;passed=area>100 and area>=ref*.99 and (dp is None or dp>100);contacts.append({'a':a,'b':b,'area_mm2':area,'source_area_mm2':ref,'downward_mm2':dp,'pass':passed})
status='PASS_LOCAL_REPAIRED_WORK_MODEL_WITH_PENDING_CANDIDATES' if not fails and all(c['pass'] for c in contacts) else 'FAIL_DO_NOT_PUBLISH'
result={'status':status,'blender_version':actual['blender_version'],'blend_sha256':actual['blend_sha256'],'entity_count':82,'unchanged_original_count':len(source['unchanged_original_ids']),'unchanged_original_local_mesh_and_transform_exact':True,'max_coordinate_delta_mm':maxdelta,'coordinate_tolerance_mm':.001,'pair_count':pair_count,'max_overlap_mm3':maximum,'intersection_threshold_mm3':1,'failed_pairs':fails,'contacts':contacts,'approved_and_pending_separate':True,'whole_model_approved':False,'strength':'NOT_TESTED','historic_joinery':'NOT_PROVEN'}
(out/'SAVE_REOPEN_V003_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False));assert status.startswith('PASS'),result
