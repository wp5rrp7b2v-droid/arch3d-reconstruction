"""C02 independent contact & collision audit against actual 17 source meshes."""
from pathlib import Path
import numpy as np,json,itertools,hashlib
import trimesh,manifold3d as mf
from shapely.geometry import Polygon
P=Path(__file__).resolve().parent/'output'
d=json.loads((P/'C02_ACTUAL_MESHES.json').read_text())
assert d['original_mesh_exact'] and len(d['objects'])==17
M={};invalid_topology=[]
for o in d['objects']:
 mesh=trimesh.Trimesh(vertices=np.asarray(o['coordinates_mm'],dtype=np.float64),
   faces=np.asarray(o['triangles'],dtype=np.int64),process=False)
 # Preserve explicit distinct coincident interface vertices. Geometric welding here
 # falsely makes 4-face edges at the real interactive-dou seat. Its source topology
 # has exactly two uses for every indexed edge before welding; checked separately.
 mesh.fix_normals()
 if not mesh.is_watertight or not mesh.is_volume:
  from collections import Counter
  cnt=Counter(tuple(sorted(pair)) for face in mesh.faces for pair in ((face[0],face[1]),(face[1],face[2]),(face[2],face[0])))
  bad=[e for e,num in cnt.items() if num!=2]
  edge_samples=[{'a':mesh.vertices[e[0]].round(4).tolist(),'b':mesh.vertices[e[1]].round(4).tolist(),'uses':cnt[e]} for e in bad[:120]]
  invalid_topology.append(dict(id=o['id'],watertight=bool(mesh.is_watertight),volume=float(mesh.volume),bad_edges_count=len(bad),bad_edge_samples=edge_samples))
 M[o['id']]=mesh
def boolean(a,b):
 A,B=M[a],M[b]
 if not A.is_watertight or not B.is_watertight:return None
 lo=np.maximum(A.bounds[0],B.bounds[0]);hi=np.minimum(A.bounds[1],B.bounds[1])
 if np.any(hi<=lo):return 0.
 centre=(hi+lo)/2.
 def manifold(m):
  return mf.Manifold(mf.Mesh64(vert_properties=np.asarray(m.vertices-centre,dtype='f8',order='C'),
                 tri_verts=np.asarray(m.faces,dtype='u4',order='C')))
 return abs(float((manifold(A)^manifold(B)).volume()))
def surface(a,b):
 ma,mb=M[a],M[b];result=0.
 for i,tri in enumerate(ma.triangles):
  normal=ma.face_normals[i];ax=tri[1]-tri[0];n=np.linalg.norm(ax)
  if n<1e-6:continue
  ax=ax/n;other=np.cross(normal,ax);origin=tri[0]
  pa=Polygon(np.column_stack([(tri-origin)@ax,(tri-origin)@other]))
  for j,t in enumerate(mb.triangles):
   if np.dot(normal,mb.face_normals[j])>-1+1e-7 or np.max(np.abs((t-origin)@normal))>.001:continue
   pb=Polygon(np.column_stack([(t-origin)@ax,(t-origin)@other]))
   result+=float(pa.intersection(pb).area)
 return result
pairs=[];unknown=[]
for a,b in itertools.combinations(M,2):
 try:vol=boolean(a,b)
 except Exception as e:vol=None;unknown.append(dict(a=a,b=b,error=str(e)))
 if vol is None:unknown.append(dict(a=a,b=b,error='SOURCE_NON_MANIFOLD_NO_BOOLEAN'))
 pairs.append(dict(a=a,b=b,overlap_mm3=vol))
declared=[
 ('trial:EAST_UPPER6_FULL_BEAM_CANDIDATE','trial:EAST_FRONT_SPACER_HUAGONG'),
 ('trial:EAST_UPPER6_FULL_BEAM_CANDIDATE','trial:EAST_FRONT_SPACER_LINGGONG'),
 ('trial:EAST_FRONT_SPACER_HUAGONG','trial:EAST_FRONT_SPACER_LINGGONG'),
 ('trial:EAST_FRONT_SPACER_LINGGONG','trial:EAST_FRONT_SANDOU'),
 ('trial:EAST_FRONT_SANDOU','east:FOUR_BEAM')]
head=[
 ('trial:EAST_FRONT_COLUMN_CANDIDATE','trial:EAST_FRONT_COLUMN_LUDOU'),
 ('trial:EAST_FRONT_COLUMN_LUDOU','trial:EAST_FRONT_HUA1_LOCAL'),
 ('trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL'),
 ('trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL','trial:EAST_FRONT_HUA2_LOCAL'),
 ('trial:EAST_FRONT_HUA2_LOCAL','trial:EAST_FRONT_TOU_ANG_LOCAL'),
 ('trial:EAST_FRONT_TOU_ANG_LOCAL','trial:EAST_FRONT_ER_ANG_LOCAL'),
 ('trial:EAST_FRONT_SANDOU_LEFT','trial:EAST_FRONT_TRANSVERSE_MANGONG'),
 ('trial:EAST_FRONT_SANDOU_RIGHT','trial:EAST_FRONT_TRANSVERSE_MANGONG')]
contact=[]
for a,b in declared+head:
 try:area=surface(a,b);err=None
 except Exception as e:area=None;err=str(e)
 contact.append(dict(a=a,b=b,area_mm2=area,threshold_mm2=100.,
  classification='PR75_ALREADY_VERIFIED_SPACER' if (a,b) in declared else 'NEW_MEASURE_HEAD_UNVERIFIED_PRIOR',
  pass_area=bool(area is not None and area>100),error=err))
strict=[x for x in contact if x['classification']=='PR75_ALREADY_VERIFIED_SPACER']
excess=[x for x in pairs if x['overlap_mm3'] is not None and x['overlap_mm3']>1.]
collision='PASS' if not unknown and not excess else 'FAIL' if excess else 'UNVERIFIED'
contact_gate='PASS_FIVE_PRIOR_SPACER_SEATS' if all(x['pass_area'] for x in strict) else 'FAIL'
result=dict(
 status='PASS_CONNECTED_SPACER_SEED_ONLY' if collision=='PASS' and contact_gate.startswith('PASS') and not invalid_topology else 'FAIL',
 input_sha=d['source_sha256'],object_count=len(M),pair_count=len(pairs),
 collision_gate=collision,excess_overlap_pairs=excess,unknown_boolean_pairs=unknown,
 invalid_topology=invalid_topology,
 max_overlap_mm3=max((x['overlap_mm3'] or 0 for x in pairs),default=0),
 all_pairs=pairs,measured_contacts=contact,confirmed_spacer_seats=sum(x['pass_area'] for x in strict),
 spacer_contact_gate=contact_gate,
 full_column_support_chain='NOT_YET_PROVEN',
 visual_form_gate='NOT_APPROVED_SOURCE_LEGACY_VERSUS_PR76_AND_C01',
 real_notched_meshes_present=True,scatter_dou_instances_present=True,
 new_C01_ANG_NOT_INSTALLED=True,
 note='Reconstructed a connected-as-built joint seed from PR75 work geometry. Does not install V001 corrected gongs or C01 ang. No historical joint authenticity or mechanical capacity validation.'
)
(P/'C02_INTERFACE_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('all_pairs','measured_contacts','excess_overlap_pairs','unknown_boolean_pairs')},ensure_ascii=False,indent=2))
if result['status'] != 'PASS_CONNECTED_SPACER_SEED_ONLY': print('C02_GATE_FAILED_RETAINED_FOR_DIAGNOSIS')
# Explicit FAIL is archived; never promoted to approved assembly.
