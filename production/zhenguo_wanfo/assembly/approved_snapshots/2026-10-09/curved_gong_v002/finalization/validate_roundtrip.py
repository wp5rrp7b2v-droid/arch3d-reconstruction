import json, hashlib, sys, math
from pathlib import Path
import numpy as np
import trimesh
import boolean64
from contact import contact

root=Path(sys.argv[1]); out=root/'output'
source=json.loads((root/'APPROVED_GEOMETRY_V002.json').read_text())
raw=json.loads((out/'REOPENED_V002_MESHES.json').read_text())
expected={o['id']:o for o in source['objects']}; actual={o['id']:o for o in raw['objects']}
assert len(actual)==63 and set(actual)==set(expected)
assert abs(raw['unit_scale']-.001)<1e-9 and raw['scene_approval']=='D-285'
meshes={}; entities=[]
for name,o in actual.items():
 e=expected[name];v=np.asarray(o['vertices']);f=np.asarray(o['faces'])
 assert np.isfinite(v).all() and np.array_equal(f,e['faces'])
 delta=float(np.max(np.abs(v-np.asarray(e['vertices'])))); assert delta<=.001,(name,delta)
 assert o['collection']==[e['group']]
 for key,value in e['properties'].items():
  if key!='model_role': assert o['properties'][key]==value,(name,key)
 assert o['properties']['model_role']==e['group'] and o['properties']['approval']=='D-285'
 mesh=trimesh.Trimesh(v,f,process=False);assert mesh.is_volume and len(mesh.split(only_watertight=False))==1,name
 meshes[name]=mesh;entities.append({'id':name,'group':e['group'],'coordinate_delta_mm':delta,'closed_single_positive_solid':True,'source_properties_preserved':True})
def overlap(a,b):
 low=np.maximum(a.bounds[0],b.bounds[0]);high=np.minimum(a.bounds[1],b.bounds[1])
 if np.any(high-low<=0):return 0.
 center=(low+high)/2;a=a.copy();b=b.copy();a.apply_translation(-center);b.apply_translation(-center)
 q=trimesh.boolean.intersection([a,b],engine='manifold');v=abs(float(q.volume)) if not q.is_empty else 0.;assert math.isfinite(v);return v
interfaces=[]
for old in source['expected_baseline_validation']:
 a=meshes[old['seat']];b=meshes[old['rod']];c=contact(a,b);bounds=c['upward_contact_bounds_mm'];span=bounds[1][0]-bounds[0][0] if bounds else 0.;v=overlap(a,b)
 assert bounds and span>=old['seat_length_mm']-1 and c['connected_upward_patch_count']==1 and c['minimum_midinterval_projected_width_mm']>0 and v<=1,(old['seat'],c,v)
 interfaces.append({'seat':old['seat'],'rod':old['rod'],'status':'PASS','contact_span_mm':span,'overlap_mm3':v,'contact':c})
names=list(meshes);pairs=[]
for i,a in enumerate(names):
 for b in names[i+1:]:pairs.append({'a':a,'b':b,'overlap_mm3':overlap(meshes[a],meshes[b])})
bad=[p for p in pairs if p['overlap_mm3']>1];assert not bad,bad
groups={g:sum(e['group']==g for e in entities) for g in ['RETAINED_50','PROFILE_CORRECTED_4','PURLINS_3','RECONSTRUCTED_SEATS_6']}
assert list(groups.values())==[50,4,3,6]
report={'status':'PASS','approval':'D-285','blender_version':raw['blender_version'],'blend_sha256':raw['blend_sha256'],'input_sha256':hashlib.sha256((root/'APPROVED_GEOMETRY_V002.json').read_bytes()).hexdigest(),'approved_glb_sha256':source['approved_glb_sha256'],'independent_reopen':True,'entity_count':63,'groups':groups,'max_coordinate_difference_mm':max(e['coordinate_delta_mm'] for e in entities),'coordinate_tolerance_mm':.001,'six_interfaces':interfaces,'entity_pairs_checked':len(pairs),'max_pair_overlap_mm3':max(p['overlap_mm3'] for p in pairs),'intersection_threshold_mm3':1,'above_threshold':bad,'entities':entities,'all_pairs':pairs,'historical_geometry':'NOT_VERIFIED','structural_capacity':'NOT_TESTED','whole_building_closed':False,'physical_registry_binding':'UNRESOLVED'}
(out/'SAVE_REOPEN_V002_VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','entity_count','groups','max_coordinate_difference_mm','max_pair_overlap_mm3','blend_sha256']},indent=2))
