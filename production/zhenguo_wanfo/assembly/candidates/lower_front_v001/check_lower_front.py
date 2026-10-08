import json,math,warnings,hashlib
from pathlib import Path
import numpy as np
import trimesh,manifold3d
from functools import reduce
ROOT=Path(__file__).resolve().parents[1]; OUT=Path(__file__).resolve().parent
TOL=.001;LIMIT=1.
s=(ROOT/'check_continuous_seat.py').read_text();exec(s[s.index('def contact('):s.index('original={}; source=[]')])
sd=s[s.index('def contact('):s.index('original={}; source=[]')].replace('def contact(','def contact_down(').replace('(seat.face_normals[:,2]>0.1)','(seat.face_normals[:,2]<-0.1)');exec(sd)
def boolean64(meshes,operation,check_volume=True,**kwargs):
 if check_volume and not all(m.is_volume for m in meshes):raise ValueError('non-volume input')
 ms=[manifold3d.Manifold(manifold3d.Mesh64(vert_properties=np.array(m.vertices,dtype=np.float64),tri_verts=np.array(m.faces,dtype=np.uint64))) for m in meshes]
 assert all(m.status()==manifold3d.Error.NoError for m in ms)
 q=reduce(lambda a,b:a^b,ms) if operation=='intersection' else reduce(lambda a,b:a+b,ms) if operation=='union' else ms[0]-reduce(lambda a,b:a+b,ms[1:])
 assert q.status()==manifold3d.Error.NoError
 r=q.to_mesh64();return trimesh.Trimesh(r.vert_properties,r.tri_verts,process=False)
trimesh.boolean._engines['manifold']=boolean64
def vol(a,b):
 lo=np.maximum(a.bounds[0],b.bounds[0]);hi=np.minimum(a.bounds[1],b.bounds[1])
 if np.any(hi-lo<=0):return 0.
 c=(lo+hi)/2;aa=a.copy();bb=b.copy();aa.apply_translation(-c);bb.apply_translation(-c)
 q=boolean64([aa,bb],'intersection');v=0. if q.is_empty else abs(float(q.volume));assert math.isfinite(v);return v
def box(ext,center):
 q=trimesh.creation.box(extents=ext);q.apply_translation(center);return q
def sig(m):return hashlib.sha256(m.vertices.tobytes()+m.faces.tobytes()).hexdigest()
rules={'scope':'front lower purlin, two reconstructed local support chains terminating at approved four-beam top; not historical proof or lower-six-beam closure','hypotheses':{'axis_spacing_mm':4437.,'common_four_beam_Z':0.,'Y_mm':3596.,'east_tiemu_mm':[1740,148,151],'east_tiemu_class':'borrowed west measured envelope, reconstructed design','west_tiemu_class':'PDF345 measured envelope','panjian_dimensions_class':'borrowed upper seat display envelope; lower panjian dimensions missing','dou_envelope_class':'PDF347 overall top widths and heights; other dimensions/profile borrowed upper dou; new slots reconstructed','purlin_class':'east upper purlin profile borrowed, lower instance not measured; diagnostic length only'},'pass':'8 support contacts, each finite area>0, one contiguous patch; tiemu/purlin full length minus1mm; overlap<=1mm3; positive closed one-piece solids; approved63 exact unchanged; reopened checks','historical_support_mapping':'four-beam top directly supports slotted new panjian is an exploratory candidate, not independently evidenced; no full-chain historical PASS'}
(OUT/'PREDECLARED_RULES.json').write_text(json.dumps(rules,ensure_ascii=False,indent=2)+'\n')
orig={};base={};targets={'TIEMU_FRONT','TIEMU_REAR','RIDGE_TIEMU','UPPER_PURLIN_FRONT','UPPER_PURLIN_REAR','RIDGE_PURLIN'}
for side,folder,file in [('east','east_v011','REOPENED_V11_MESHES.json'),('west','west_v002','REOPENED_WEST_V002_MESHES.json')]:
 raw=(ROOT/folder/file).read_bytes();man=json.loads((ROOT/folder/'APPROVED_SNAPSHOT_MANIFEST.json').read_text())['artifacts'][file];assert hashlib.sha256(raw).hexdigest()==man['sha256']
 orig[side]={o['id']:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for o in json.loads(raw)['objects']}
 for k,m in orig[side].items():
  if k in targets:continue
  q=m.copy();q.apply_translation([4437 if side=='east' else 0,0,0]);base[side+':'+k]=q
for k,o in json.loads((ROOT/'full_feasibility/PRIMARY_GEOMETRY.json').read_text()).items():
 if not k.endswith(':ORIGINAL'):base[k]=trimesh.Trimesh(o['vertices'],o['faces'],process=False)
assert len(base)==63;before={k:sig(m) for k,m in base.items()};new={};rawfail=[];contacts=[]
with warnings.catch_warnings(record=True) as ws:
 warnings.simplefilter('always')
 # Reject simple upper-group translation using the approved frame meshes.
 for side,B in [('east',612),('west',608)]:
  beam=base[side+':FOUR_BEAM'];off=np.array([4437 if side=='east' else 0,1760,-B])
  for k in ['CENTRE_DOU_FRONT','PANJIAN_FANG_FRONT']:
   q=orig[side][k].copy();q.apply_translation(off);rawfail.append({'side':side,'translated_upper_object':k,'beam_overlap_mm3':vol(q,beam)})
 # Actual exploratory support geometry: new panjian lower slot wraps the immutable four-beam end.
 for side,B,z,topwidth,height in [('east',612,223.,329.,223.),('west',608,238.,331.,220.)]:
  x=4437. if side=='east' else 0.;oldp=orig[side]['PANJIAN_FANG_FRONT'];pb=oldp.bounds[0,2]-B;pt=oldp.bounds[1,2]-B
  pan=box([1740.,oldp.extents[1],oldp.extents[2]],[x,3596.,(pb+pt)/2]);beam=base[side+':FOUR_BEAM']
  pan=boolean64([pan,beam],'difference');new[side+':LOWER_PANJIAN']=pan
  dou=orig[side]['UPPER_DOU_FRONT'].convex_hull;v=dou.vertices.copy();lo=v.min(0);hi=v.max(0);v[:,0]=(v[:,0]-(lo[0]+hi[0])/2)*topwidth/(hi[0]-lo[0])+x;v[:,1]+=(3596.-(lo[1]+hi[1])/2);v[:,2]=(v[:,2]-lo[2])*height/(hi[2]-lo[2])+pt;dou.vertices=v
  seat=box([1740.,148.,151.],[x,3596.,z+151/2]);dou=boolean64([dou,seat],'difference');new[side+':LOWER_DOU']=dou;new[side+':LOWER_TIEMU_BLANK']=seat
 ec=np.array([4437.,3596.,223+151-20+112.5]);wc=np.array([0.,3596.,238+151-20+112.5]);angle=math.atan2(wc[2]-ec[2],4437.);L=math.hypot(4437.,wc[2]-ec[2])+1740.
 rod=orig['east']['UPPER_PURLIN_FRONT'].copy();v=rod.vertices-rod.bounds.mean(0);v[:,0]=np.where(v[:,0]<0,-L/2,L/2);rod.vertices=v;rod.apply_transform(trimesh.transformations.rotation_matrix(angle,[0,1,0]));rod.apply_translation((ec+wc)/2);new['LOWER_PURLIN_FRONT']=rod
 conservation=[]
 for side in ['east','west']:
  blank=new.pop(side+':LOWER_TIEMU_BLANK');seat=boolean64([blank,rod],'difference');cut=boolean64([blank,rod],'intersection');new[side+':LOWER_TIEMU']=seat;conservation.append({'side':side,'error_mm3':abs(float(blank.volume-seat.volume-cut.volume))})
  pan=new[side+':LOWER_PANJIAN'];dou=new[side+':LOWER_DOU'];beam=base[side+':FOUR_BEAM']
  for label,a,b,down in [('槫—替木',seat,rod,False),('替木—斗',dou,seat,False),('斗—襻间枋',dou,pan,True),('襻间枋—四椽栿',pan,beam,True)]:
   c=(contact_down if down else contact)(a,b);bound=c['upward_contact_bounds_mm'];span=bound[1][0]-bound[0][0] if bound else 0.;ok=c['upward_area_mm2']>0 and c['connected_upward_patch_count']==1 and (label!='槫—替木' or span>=1739.)
   contacts.append({'side':side,'interface':label,'status':'PASS' if ok else 'FAIL','contact':c,'span_X_mm':span,'overlap_mm3':vol(a,b)})
 pairs=[]
 for k,m in new.items():
  for l,n in base.items():pairs.append({'a':k,'b':l,'overlap_mm3':vol(m,n)})
 keys=list(new)
 for i,k in enumerate(keys):
  for l in keys[i+1:]:pairs.append({'a':k,'b':l,'overlap_mm3':vol(new[k],new[l])})
 solids=[{'id':k,'is_volume':bool(m.is_volume),'components':len(m.split(only_watertight=False))} for k,m in new.items()]
 scene=trimesh.Scene()
 for k,m in {**base,**new}.items():
  q=m.copy();q.visual.face_colors=[214,155,54,255] if k in new else [130,143,150,255];c=q.bounds.mean(0);q.apply_translation(-c);T=np.eye(4);T[:3,3]=c;scene.add_geometry(q,node_name=k,geom_name=k,transform=T)
 path=OUT/'LOWER_FRONT_EXPLORATORY_TEST_ONLY.glb';path.write_bytes(scene.export(file_type='glb'));rr=trimesh.load(path,force='scene');assert len(rr.geometry)==70
 reopenmesh={k:rr.geometry[k].copy() for k in rr.geometry}
 for k,m in reopenmesh.items():m.apply_transform(rr.graph.get(k)[0])
 reopened=[]
 for side in ['east','west']:
  for label,a,b,down in [('槫—替木',side+':LOWER_TIEMU','LOWER_PURLIN_FRONT',False),('替木—斗',side+':LOWER_DOU',side+':LOWER_TIEMU',False),('斗—襻间枋',side+':LOWER_DOU',side+':LOWER_PANJIAN',True),('襻间枋—四椽栿',side+':LOWER_PANJIAN',side+':FOUR_BEAM',True)]:
   c=(contact_down if down else contact)(reopenmesh[a],reopenmesh[b]);bound=c['upward_contact_bounds_mm'];span=bound[1][0]-bound[0][0] if bound else 0.;ov=vol(reopenmesh[a],reopenmesh[b]);ok=c['upward_area_mm2']>0 and c['connected_upward_patch_count']==1 and ov<=LIMIT and (label!='槫—替木' or span>=1739.)
   reopened.append({'side':side,'interface':label,'status':'PASS' if ok else 'FAIL','overlap_mm3':ov,'contact':c,'span_X_mm':span})
 unchanged=all(sig(base[k])==before[k] for k in base);bad=[p for p in pairs if p['overlap_mm3']>LIMIT]
 passed=unchanged and not bad and all(c['status']=='PASS' and c['overlap_mm3']<=LIMIT for c in contacts+reopened) and all(s['is_volume'] and s['components']==1 for s in solids) and all(q['error_mm3']<=LIMIT for q in conservation)
 result={'status':'EXPLORATORY_LOCAL_GEOMETRY_PASS' if passed else 'FAIL','historical_support_chain_validated':False,'production_expansion_allowed':False,'raw_translation_intersections':rawfail,'contacts':contacts,'new_pairs_checked':len(pairs),'bad_pairs':bad,'all_pairs':pairs,'new_solids':solids,'conservation':conservation,'reopen_contacts':reopened,'reopened_entities':len(rr.geometry),'approved_63_exact_shape_unchanged':unchanged,'purlin_diagnostic_length_mm':L,'purlin_angle_deg':math.degrees(angle),'warnings':sorted(set(str(w.message) for w in ws))}
 (OUT/'LOWER_FRONT_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(OUT/'LOWER_FRONT_GEOMETRY.json').write_text(json.dumps({k:{'vertices':m.vertices.tolist(),'faces':m.faces.tolist()} for k,m in new.items()},ensure_ascii=False,indent=2)+'\n')

# Independent source-completeness gate after visual review of PDF90-92.
result.update({'source_completeness_status': 'FAIL_INCOMPLETE_SUPPORT_GROUP', 'overall_adoption_status': 'NOT_READY_FOR_ADOPTION', 'independent_source_review': {'pdf_pages': [90, 91, 92], 'fact': '原报告说明替木下有小斗；槫下襻间斗栱由进深及顺身方向构件组成，底部用栌斗，上下六椽栿之间隔架为例外。', 'finding': '试验直接以四椽栿顶承托新襻间枋，遗漏完整下平槫斗栱组。表中襻间枋斗总尺寸不能单独证明把借形斗放在襻间枋上方正确。', 'missing_representation': ['底部栌斗', '顺身令栱', '进深华栱', '替木下小斗'], 'interpretation': '构件表达不完整使候选不能采用；没有进行承载能力判断。已批准三道槫方案不受影响。'}})
(OUT/'LOWER_FRONT_CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','source_completeness_status','overall_adoption_status']},ensure_ascii=False))
