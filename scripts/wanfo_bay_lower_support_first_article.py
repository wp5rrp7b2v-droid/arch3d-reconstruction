import json,copy,math,pathlib,hashlib,sys
import numpy as np,trimesh,manifold3d as mf
ROOT=pathlib.Path(__file__).resolve().parent;BASE=ROOT.parent
baseline=json.loads((BASE/'blend_finalize/output/REOPENED_V002_MESHES.json').read_text())
objects=copy.deepcopy(baseline['objects']);meshes={o['id']:trimesh.Trimesh(o['vertices'],o['faces'],process=False) for o in objects}
def man(m):return mf.Manifold(mf.Mesh64(vert_properties=np.array(m.vertices,dtype=np.float64,order="C",copy=True),tri_verts=np.array(m.faces,dtype=np.uint64,order="C",copy=True)))
def mesh(a):
 assert a.status()==mf.Error.NoError
 b=a.to_mesh64();return trimesh.Trimesh(b.vert_properties,b.tri_verts,process=False)
def box(ext,c):
 m=trimesh.creation.box(extents=ext);m.apply_translation(c);return m
def vol(a,b):
 lo=np.maximum(a.bounds[0],b.bounds[0]);hi=np.minimum(a.bounds[1],b.bounds[1])
 if np.any(hi<=lo):return 0.
 c=(lo+hi)/2;aa=a.copy();bb=b.copy();aa.apply_translation(-c);bb.apply_translation(-c)
 return abs(float((man(aa)^man(bb)).volume()))
rules={'status':'PREDECLARED_BEFORE_GENERATION','scope':'ONE EAST FRONT LOWER CONNECTION FIRST ARTICLE; NOT COMPLETE BAY','baseline_entities_fixed':63,'coordinate_tolerance_mm':.001,'overlap_threshold_mm3':1,'source_direct':'PDF82 support semantics; PDF346 east-front HG 220x155x894; LG 210x153; upper-six section PDF81 mean334/max240.5','project_parameters':{'site_y_mm':3496,'site_basis':'trial 100mm inboard of approved four-beam end; not surveyed support centre','gong_base_z_mm':-753,'upper6_segment_length_mm':1800,'segment_basis':'CUT_DIAGNOSTIC_PATCH_ONLY; not full beam and not Master reference1000','linggong_length_mm':900,'linggong_length_basis':'explicit replaceable trial value; not taken from HG894 and not historical','sandou_body_height_mm':130,'sandou_top_xy_mm':[355,240],'sandou_foot_xy_mm':[140,120],'sandou_ears_height_mm':20,'sandou_basis':'SOURCE_GUIDED_RECONSTRUCTED_DESIGN; no borrowed LUDOU or unified dou-family dimensions'},'fail':'change baseline or above-threshold overlap or broken closed solids; no batch expansion until source and PO shape review','not_claimed':['complete bay','historic dimensions of reconstructed connectors','full upper-six length','Blender reopen before separate execution','structural strength']}
(ROOT/'PREDECLARED_RULES.json').write_text(json.dumps(rules,ensure_ascii=False,indent=2))
X=4437.;Y=3496.;Z=-753.
def gong(L,H,W,along):
 # Visible rounded head; opposed sloping tail is a replaceable source-guided trial.
 flat=145.;theta=np.linspace(0,math.pi/2,49)
 xx=-L/2+(L/2-flat)*(1-np.cos(theta));zz=.68*H*(1-np.sin(theta))
 lower=list(zip(xx,zz))+[(flat,0),(L/2,.85*H)]
 poly=[[-L/2,H],[L/2,H]]+[[float(a),float(b)] for a,b in lower[::-1]]
 q=mf.CrossSection([np.array(poly)],mf.FillRule.NonZero).extrude(W)
 if along=='Y':q=q.transform(np.array([[0,0,1,X-W/2],[1,0,0,Y],[0,1,0,Z]],float))
 else:q=q.transform(np.array([[1,0,0,X],[0,0,1,Y-W/2],[0,1,0,Z]],float))
 return mesh(q)
hg=gong(894,220,155,'Y');lg=gong(900,210,153,'X')
# Matching crossed housing, owned by this trial assembly; no historical joinery claim.
hg=mesh(man(hg)-man(box([157,153,117],[X,Y,Z+105+117/2])))
lg=mesh(man(lg)-man(box([155,155,107],[X,Y,Z-2+107/2])))
upper=box([240.5,1800,334],[X,Y,Z-167])
z0=Z+210;z1=-413
v=[]
for z,sx,sy in [(z0,140,120),(z1,355,240)]:
 for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]:v.append([X+a*sx/2,Y+b*sy/2,z])
f=[[0,2,1],[0,3,2],[4,5,6],[4,6,7]]
for i in range(4):a=i;b=(i+1)%4;f.extend([[a,b,b+4],[a,b+4,a+4]])
sd=trimesh.Trimesh(v,f,process=False)
for sign in [-1,1]:sd=mesh(man(sd)+man(box([30,240,20],[X+sign*162.5,Y,-403])))
new={'trial:EAST_FRONT_UPPER6_PATCH':upper,'trial:EAST_FRONT_SPACER_HUAGONG':hg,'trial:EAST_FRONT_SPACER_LINGGONG':lg,'trial:EAST_FRONT_SANDOU':sd}
for k,m in new.items():
 assert m.is_volume and len(m.split(only_watertight=False))==1,(k,m.is_volume)
 props={'assembly_status':'FIRST_ARTICLE_NOT_APPROVED','historical_claim':False,'source_pages':[81,82,346],'physical_registry_id':None,'parameter_status':'DIRECT_SECTION_AND_RECONSTRUCTED_DESIGN','role':'DIAGNOSTIC_CUT_PATCH' if 'PATCH' in k else 'SOURCE_GUIDED_TRIAL_CONNECTOR'}
 objects.append({'id':k,'vertices':m.vertices.tolist(),'faces':m.faces.tolist(),'properties':props});meshes[k]=m
# Four actual interfaces: two gong feet to patch, crossed housing, sandou to LG, sandou to four-beam.
contacts=[]
for a,b,desc in [('trial:EAST_FRONT_UPPER6_PATCH','trial:EAST_FRONT_SPACER_HUAGONG','HG base'),('trial:EAST_FRONT_UPPER6_PATCH','trial:EAST_FRONT_SPACER_LINGGONG','LG feet'),('trial:EAST_FRONT_SPACER_HUAGONG','trial:EAST_FRONT_SPACER_LINGGONG','crossed half housing'),('trial:EAST_FRONT_SPACER_LINGGONG','trial:EAST_FRONT_SANDOU','dou bottom'),('trial:EAST_FRONT_SANDOU','east:FOUR_BEAM','four-beam seat')]:
 ma=meshes[a];mb=meshes[b]; dist=float(min(trimesh.proximity.closest_point_naive(mb,ma.vertices)[1].min(),trimesh.proximity.closest_point_naive(ma,mb.vertices)[1].min()));assert dist<=.001,(a,b,dist)
 contacts.append({'a':a,'b':b,'description':desc,'minimum_surface_distance_mm':dist,'note':'surface meeting only; not strength or area certification'})
bad=[];maxv=0;checked=0
names=list(meshes)
for i,a in enumerate(names):
 for b in names[i+1:]:
  if a not in new and b not in new:continue
  value=vol(meshes[a],meshes[b]);checked+=1;maxv=max(maxv,value)
  if value>1:bad.append({'a':a,'b':b,'volume_mm3':value})
assert not bad,bad
payload={'status':'FIRST_ARTICLE_DIAGNOSTIC_CANDIDATE_NOT_APPROVED','unit':'mm','objects':objects,'new_ids':list(new),'rules':rules}
(ROOT/'PILOT_GEOMETRY.json').write_text(json.dumps(payload,ensure_ascii=False))
scene=trimesh.Scene()
for name,m in meshes.items():
 mm=m.copy();mm.visual.face_colors=[231,158,47,255] if name in new else [153,145,130,255]
 if name in ['RIDGE_PURLIN','UPPER_PURLIN_FRONT','UPPER_PURLIN_REAR']:mm.visual.face_colors=[40,132,175,255]
 mm.apply_scale(.001);mm.apply_transform(np.array([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]],float));c=mm.bounds.mean(0);mm.apply_translation(-c);t=np.eye(4);t[:3,3]=c
 scene.add_geometry(mm,node_name=name,geom_name=name,transform=t)
out=BASE/'deliverables/WANFO_BAY_LOWER_SUPPORT_FIRST_ARTICLE_V001.glb';out.write_bytes(scene.export(file_type='glb'))
r=trimesh.load(out,force='scene');assert len(r.geometry)==67
errs=[]
for node in r.graph.nodes_geometry:
 t,g=r.graph[node];m=r.geometry[g].copy();m.apply_transform(t);v=m.vertices[:,[0,2,1]].copy();v[:,1]*=-1;v*=1000
 assert np.array_equal(m.faces,meshes[node].faces);delta=float(np.max(np.abs(v-meshes[node].vertices)));assert delta<=.001;(errs.append(delta))
assert objects[:63]==baseline['objects']
result={'status':'PASS_BOUNDED_TRIAL_GEOMETRY; SOURCE_AND_PO_REVIEW_PENDING','entity_count':67,'baseline_unchanged':63,'new_trial_entities':4,'new_affected_pairs_checked':checked,'baseline_pairs_reused_not_rerun':1953,'max_new_overlap_mm3':maxv,'overlaps_above_threshold':bad,'contact_checks':contacts,'glb_reopened_entities':67,'max_roundtrip_coordinate_delta_mm':max(errs),'blender_saved_reopened':False,'complete_bay':False,'input_blend_sha256':baseline['blend_sha256'],'candidate_glb_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(ROOT/'PILOT_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False))
