import ast,json,math,warnings,hashlib
from pathlib import Path
import numpy as np
import trimesh,manifold3d
from functools import reduce
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent
TOL=.001;LIMIT=1.
source=(ROOT/'lower_front/check_lower_front.py').read_text();tree=ast.parse(source)
for node in tree.body:
 if isinstance(node,ast.FunctionDef):exec(compile(ast.Module(body=[node],type_ignores=[]),'helpers','exec'))
s=(ROOT/'check_continuous_seat.py').read_text();chunk=s[s.index('def contact('):s.index('original={}; source=[]')];exec(chunk);exec(chunk.replace('def contact(','def contact_down(').replace('(seat.face_normals[:,2]>0.1)','(seat.face_normals[:,2]<-0.1)'))
trimesh.boolean._engines['manifold']=boolean64
rules={'version':'V002','scope':'front lower purlin two-end full role-presence candidate, not historical shape or structural proof','pass':'all required role objects; positive closed single solids; every proposed support interface area>0; no new overlaps>1mm3; approved63 unchanged; reopened interference gate repeated','hypotheses':{'common_four_beam_top_Z':0,'frame_spacing_mm':4437,'lower_axis_Y_mm':3596,'east_tiemu_envelope':'borrow west1740x148x151','purlin_profile':'borrow east upper purlin','small_dou_shape':'borrow approved upper dou, three inferred candidate positions','panjian_envelope':'borrow upper panjian; lower dimensions missing','upper_six_beam':'measured sections PDF342; test length10710, no historical full length claim','san_dou':'new test pads, no historical dimensions claim','gongs':'PDF346 sections and linggong lengths; huagong incomplete length borrowed upper display; new crossing slots reconstructed'},'hard_stop':'do not automatically carve approved four-beam; failed placement cannot be historicized; no expansion after FAIL'}
(OUT/'PREDECLARED_RULES.json').write_text(json.dumps(rules,ensure_ascii=False,indent=2)+'\n')
orig={};base={};targets={'TIEMU_FRONT','TIEMU_REAR','RIDGE_TIEMU','UPPER_PURLIN_FRONT','UPPER_PURLIN_REAR','RIDGE_PURLIN'}
for side,folder,file in [('east','east_v011','REOPENED_V11_MESHES.json'),('west','west_v002','REOPENED_WEST_V002_MESHES.json')]:
 raw=(ROOT/folder/file).read_bytes();manifest=json.loads((ROOT/folder/'APPROVED_SNAPSHOT_MANIFEST.json').read_text())['artifacts'][file];assert hashlib.sha256(raw).hexdigest()==manifest['sha256']
 orig[side]={o['id']:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for o in json.loads(raw)['objects']}
 for k,m in orig[side].items():
  if k in targets:continue
  q=m.copy();q.apply_translation([4437 if side=='east' else 0,0,0]);base[side+':'+k]=q
for k,o in json.loads((ROOT/'full_feasibility/PRIMARY_GEOMETRY.json').read_text()).items():
 if not k.endswith(':ORIGINAL'):base[k]=trimesh.Trimesh(o['vertices'],o['faces'],process=False)
assert len(base)==63;signatures={k:sig(m) for k,m in base.items()}
def resized(m,extents,xy,zbottom,hull=False):
 q=m.convex_hull if hull else m.copy();v=q.vertices.copy();lo=v.min(0);hi=v.max(0);v=(v-(lo+hi)/2)*np.array(extents)/(hi-lo);v+=np.array([xy[0],xy[1],zbottom+extents[2]/2]);q.vertices=v;return q
new={};specs=[];interfaces=[]
with warnings.catch_warnings(record=True) as ws:
 warnings.simplefilter('always')
 for side,B,z,hgH,hgW,lgL,lgH,lgW,luW,luH,plain,knee,beamH,beamW in [('east',612,223.,224.,153.,1015.,219.,150.,329.,223.,43.,85.,335.,240.),('west',608,238.,213.,151.,1007.,218.,154.,331.,220.,42.,86.,333.,241.)]:
  x=4437. if side=='east' else 0.;xy=[x,3596.];old=orig[side];oldp=old['PANJIAN_FANG_FRONT'];pb=oldp.bounds[0,2]-B;pt=oldp.bounds[1,2]-B
  centre_bearing=oldp.bounds[0,2]-old['LINGGONG_FRONT'].bounds[1,2]
  lgTop=pb-centre_bearing;gBase=lgTop-lgH;luBase=gBase-plain-knee
  pan=box([1740.,oldp.extents[1],oldp.extents[2]],[x,3596.,(pb+pt)/2]);new[side+':PANJIAN']=pan
  # Bottom ludou and crossing gongs are independent objects, not the former top substitute.
  lu=resized(old['LUDOU_FRONT'],[luW,354. if side=='east' else 350.,luH],xy,luBase,hull=True)
  lg=resized(old['LINGGONG_FRONT'],[lgL,lgW,lgH],xy,gBase)
  # Preserve borrowed upper huagong offset toward the inner tuojiao; actual lower end is unknown.
  off=old['HUAGONG_FRONT'].bounds.mean(0)[1]-1836.
  hg=resized(old['HUAGONG_FRONT'],[hgW,old['HUAGONG_FRONT'].extents[1],hgH],[x,3596.+off],gBase)
  hg=boolean64([hg,lg],'difference');lu=boolean64([lu,hg,lg],'difference')
  centre=resized(old['CENTRE_DOU_FRONT'],old['CENTRE_DOU_FRONT'].extents,xy,lgTop,hull=True);centre=boolean64([centre,pan,hg],'difference')
  new[side+':LUDOU']=lu;new[side+':HUAGONG']=hg;new[side+':LINGGONG']=lg;new[side+':CENTRE_DOU']=centre
  seat=box([1740.,148.,151.],[x,3596.,z+75.5]);new[side+':TIEMU_BLANK']=seat
  for tag,dx in [('LEFT',-lgL/2),('CENTRE',0.),('RIGHT',lgL/2)]:
   dou=resized(old['UPPER_DOU_FRONT'],old['UPPER_DOU_FRONT'].extents,[x+dx,3596.],pt,hull=True);dou=boolean64([dou,seat],'difference');new[side+':SMALL_DOU_'+tag]=dou
  beam=box([beamW,10710.,beamH],[x,0.,luBase-beamH/2]);new[side+':UPPER_SIX_TEST']=beam
  gap=float(base[side+':FOUR_BEAM'].bounds[0,2]-luBase);assert gap>0
  for tag,y in [('FRONT',1836.),('REAR',-1836.)]:new[side+':SAN_DOU_TEST_'+tag]=box([180.,180.,gap],[x,y,luBase+gap/2])
  specs.append({'side':side,'four_beam_bottom_mm':float(base[side+':FOUR_BEAM'].bounds[0,2]),'tiemu_bottom_mm':z,'panjian_bottom_mm':float(pb),'panjian_top_mm':float(pt),'gongs_bottom_mm':float(gBase),'linggong_top_mm':float(lgTop),'ludou_bottom_mm':float(luBase),'upper_six_top_mm':float(luBase),'sandou_test_height_mm':gap,'classification':'conditional solver using borrowed geometry, not measured elevations'})
 ec=np.array([4437.,3596.,223+151-20+112.5]);wc=np.array([0.,3596.,238+151-20+112.5]);angle=math.atan2(wc[2]-ec[2],4437.);L=math.hypot(4437.,wc[2]-ec[2])+1740.
 rod=orig['east']['UPPER_PURLIN_FRONT'].copy();v=rod.vertices-rod.bounds.mean(0);v[:,0]=np.where(v[:,0]<0,-L/2,L/2);rod.vertices=v;rod.apply_transform(trimesh.transformations.rotation_matrix(angle,[0,1,0]));rod.apply_translation((ec+wc)/2);new['LOWER_PURLIN_FRONT']=rod
 for side in ['east','west']:
  blank=new.pop(side+':TIEMU_BLANK');new[side+':TIEMU']=boolean64([blank,rod],'difference')
 pairs=[]
 for k,m in new.items():
  for l,n in base.items():pairs.append({'a':k,'b':l,'overlap_mm3':vol(m,n)})
 keys=list(new)
 for i,k in enumerate(keys):
  for l in keys[i+1:]:pairs.append({'a':k,'b':l,'overlap_mm3':vol(new[k],new[l])})
 def support(a,b,down=False):
  # First mesh selected so its smaller/newly generated contact facets can be classified.
  ma=({**base,**new})[a];mb=({**base,**new})[b];c=(contact_down if down else contact)(ma,mb)
  interfaces.append({'a':a,'b':b,'downward_first_face':down,'area_mm2':c['upward_area_mm2'],'patch_count':c['connected_upward_patch_count'],'status':'PASS' if c['upward_area_mm2']>0 else 'FAIL','overlap_mm3':vol(ma,mb)})
 for side in ['east','west']:
  p=side+':'
  support(p+'LUDOU',p+'UPPER_SIX_TEST',True);support(p+'LUDOU',p+'HUAGONG');support(p+'LUDOU',p+'LINGGONG');support(p+'CENTRE_DOU',p+'LINGGONG',True);support(p+'CENTRE_DOU',p+'PANJIAN')
  for tag in ['LEFT','CENTRE','RIGHT']:support(p+'SMALL_DOU_'+tag,p+'PANJIAN',True);support(p+'SMALL_DOU_'+tag,p+'TIEMU')
  support(p+'TIEMU','LOWER_PURLIN_FRONT')
  for tag in ['FRONT','REAR']:support(p+'SAN_DOU_TEST_'+tag,p+'UPPER_SIX_TEST',True);support(p+'SAN_DOU_TEST_'+tag,p+'FOUR_BEAM')
 bad=[p for p in pairs if p['overlap_mm3']>LIMIT];solids=[{'id':k,'positive_closed':bool(m.is_volume),'components':len(m.split(only_watertight=False))} for k,m in new.items()]
 scene=trimesh.Scene()
 for k,m in {**base,**new}.items():
  q=m.copy();q.visual.face_colors=[218,167,83,255] if k in new else [145,151,157,255];c=q.bounds.mean(0);q.apply_translation(-c);T=np.eye(4);T[:3,3]=c;scene.add_geometry(q,node_name=k,geom_name=k,transform=T)
 path=OUT/'COMPLETE_ROLE_GROUP_TEST_ONLY.glb';path.write_bytes(scene.export(file_type='glb'));rr=trimesh.load(path,force='scene');assert len(rr.geometry)==len(base)+len(new)
 reopened={k:rr.geometry[k].copy() for k in rr.geometry}
 for k,m in reopened.items():m.apply_transform(rr.graph.get(k)[0])
 # Repeat every failed diagnostic pair after reopen; positive failure is robust to export precision.
 reFail=[{'a':p['a'],'b':p['b'],'overlap_mm3':vol(reopened[p['a']],reopened[p['b']])} for p in bad]
 unchanged=all(sig(base[k])==signatures[k] for k in base)
 ok=not bad and unchanged and all(q['status']=='PASS' for q in interfaces) and all(q['positive_closed'] and q['components']==1 for q in solids)
 result={'version':'V002','status':'GEOMETRY_PASS' if ok else 'FAIL_CURRENT_POSITIONING','role_presence_status':'REQUIRED_ROLE_CATEGORIES_PRESENT','historical_geometry_claim':False,'production_expansion_allowed':False,'specs':specs,'new_objects':len(new),'total_entities':len(rr.geometry),'pairs_checked':len(pairs),'bad_pairs':bad,'all_pairs':pairs,'interfaces':interfaces,'new_solids':solids,'reopened_failed_pairs':reFail,'approved_63_unchanged':unchanged,'warnings':sorted(set(str(w.message) for w in ws)),'boundary':'FAIL of this borrowed profile/placement candidate; does not prove approved four-beam incorrect or need to carve it; photo and exact connection alignment still required'}
 (OUT/'CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(OUT/'GEOMETRY.json').write_text(json.dumps({k:{'vertices':m.vertices.tolist(),'faces':m.faces.tolist()} for k,m in new.items()},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','new_objects','total_entities','pairs_checked','bad_pairs','interfaces','approved_63_unchanged']},ensure_ascii=False))
