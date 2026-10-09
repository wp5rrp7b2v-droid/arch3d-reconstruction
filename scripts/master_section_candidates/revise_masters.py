"""Isolated section-direction candidates. Never edits a canonical Master."""
import pathlib,json,hashlib,sys,importlib.util,ast,math
ROOT=pathlib.Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2))
def bounds(v):return [max(q[i] for q in v)-min(q[i] for q in v) for i in range(3)]
def closed(v,f):
 edges={}
 for poly in f:
  for a,b in zip(poly,poly[1:]+poly[:1]):edges[tuple(sorted((a,b)))]=edges.get(tuple(sorted((a,b))),0)+1
 assert all(n==2 for n in edges.values())
 assert len(v)-len(edges)+len(f)==2
def area(p):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))/2
def generate(source):
 S=source/'production/zhenguo_wanfo';result={'status':'CANDIDATE_NOT_APPROVED','candidate_revision':'SECTION_DIRECTION_V002','unit':'mm','coordinate_contract':{'X':'length','Y':'horizontal section thickness','Z':'vertical height'},'source_main':'cf5ff09f8c1190286f4833edc48e11b589969f50','unchanged':['source dimension values and classifications','reference lengths','locked gong normalized profiles','old V001 assets','approved63 assembly','formal catalog/registry'],'changed':['section axis mapping','candidate coordinate properties','gong profile-to-extrusion parameter assignment'],'not_proven':['historical full beam length','interior asymmetric end fit','hidden joinery','sandou dimensions','whole bay completion'],'families':[]}
 for family in ['HUAGONG','LINGGONG']:
  p=S/f'component_library/masters/CMP-GONG-{family}-001';dpath=p/f'CMP-GONG-{family}-001_{family}_DEFINITION_V001.json';bpath=p/f'build_{family.lower()}_master_v001.py';d=json.loads(dpath.read_text());spec=importlib.util.spec_from_file_location(family,bpath);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);pts=d['profile_contract']['normalized_points'];bodies=[]
  variants=d['length_assembly_contract']['reference_specimens'] if family=='HUAGONG' else {'LINGGONG':{k+'_mm':v for k,v in d['canonical_reference_geometry_mm'].items()}}
  for name,values in variants.items():
   L,G,T=[float(values[k+'_mm']) for k in ['length','width','thickness']];v,f=m.mesh_payload(L,T,G,pts);ov,of=m.mesh_payload(L,G,T,pts);closed(v,f);dims=bounds(v);assert all(abs(a-b)<1e-8 for a,b in zip(dims,[L,T,G]));volume=area(pts)*L*G*T;assert volume>0
   qv,qf=m.canonical_geometry(ov,of);original_dims={'length':L,'width':G,'thickness':T} if family=='HUAGONG' else d['canonical_reference_geometry_mm'];sig=m.stable({'body_id':name,'dimensions':original_dims,'vertices':qv,'faces':qf});expected=d['first_article_approval']['jump_1_geometry_signature' if name=='JUMP_1_HUAGONG' else 'jump_2_geometry_signature'] if family=='HUAGONG' else d['first_article_approval']['geometry_signature'];assert sig==expected
   bodies.append({'id':name,'vertices':v,'faces':f,'old_vertices':ov,'old_faces':of,'target_dimensions_xyz_mm':dims,'expected_volume_mm3':volume,'source_geometry_signature_match':True,'source_geometry_signature':sig,'profile_points_unchanged':pts,'profile_control_sha256':d['profile_contract']['control_set_sha256'],'length_status':'REFERENCE_SPECIMEN_ONLY' if family=='HUAGONG' else 'EXTERNAL_EAVES_OBSERVED_MEAN_NOT_PER_INSTANCE_EXACT'})
  result['families'].append({'master_id':d['master_id'],'source_master_version':d['master_version'],'source_definition_sha256':digest(dpath),'source_builder_sha256':digest(bpath),'source_evidence_properties':d.get('evidence_semantics',d.get('length_assembly_contract')),'bodies':bodies})
 p=S/'component_library/masters/CMP-FRAME-UPPER-SIX-CHUANFU-001/CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER_PARAMS_V001.json';d=json.loads(p.read_text());params={x['key']:x for x in d['parameters']};bpath=S/'scripts/six_chuanfu_master_common_v001.py';tree=ast.parse(bpath.read_text());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='make_mesh');f.body=f.body[:3]+[ast.Return(value=ast.Tuple(elts=[ast.Name(id='verts',ctx=ast.Load()),ast.Name(id='faces',ctx=ast.Load())],ctx=ast.Load()))];space={'GEOMETRY_KEYS':('realization_length_mm','width_mm','max_thickness_mm')};exec(compile(ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[])),str(bpath),'exec'),space);ov,faces=space['make_mesh'](d,params);G=params['width_mm']['value'];T=params['max_thickness_mm']['value'];L=params['realization_length_mm']['value'];v=[[x,z-T/2,-y+G/2] for x,y,z in ov];closed(v,faces);assert bounds(v)==[L,T,G]
 result['families'].append({'master_id':d['master_id'],'source_master_version':d['master_version'],'source_definition_sha256':digest(p),'source_builder_sha256':digest(bpath),'source_evidence_properties':d['parameters'],'bodies':[{'id':'UPPER6_REFERENCE_ONLY','vertices':v,'faces':faces,'old_vertices':ov,'old_faces':faces,'target_dimensions_xyz_mm':[L,T,G],'expected_volume_mm3':L*T*G,'transformation':'rigid longitudinal roll -90deg plus lower-plane rebase','length_status':'1000_REFERENCE_ONLY_HISTORICAL_FULL_LENGTH_NULL'}]})
 write(ROOT/'MASTER_SECTION_DIRECTION_CANDIDATE_V002.json',result);print('GENERATE_PASS: 3 families, 4 reference bodies; old gong signatures match; source dimensions unchanged')
def blender(mode):
 import bpy
 j=json.loads((ROOT/'MASTER_SECTION_DIRECTION_CANDIDATE_V002.json').read_text());out=ROOT/'output';out.mkdir(exist_ok=True);reports=[]
 for family in j['families']:
  path=out/(family['master_id']+'_SECTION_CANDIDATE_V002.blend')
  if mode=='build':
   bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1.;scene['approval_status']='CANDIDATE_NOT_APPROVED';scene['source_master_version']='V001';scene['candidate_revision']='SECTION_DIRECTION_V002';scene['coordinate_contract']='X length / Y horizontal thickness / Z vertical height'
   for body in family['bodies']:
    me=bpy.data.meshes.new(body['id']);me.from_pydata([[x*.001 for x in v] for v in body['vertices']],[],body['faces']);me.update();o=bpy.data.objects.new(body['id'],me);scene.collection.objects.link(o)
    for k,val in {'master_id':family['master_id'],'source_master_version':'V001','candidate_revision':'SECTION_DIRECTION_V002','approval_status':'CANDIDATE_NOT_APPROVED','length_status':body['length_status'],'source_definition_sha256':family['source_definition_sha256'],'source_profile_control_sha256':body.get('profile_control_sha256','NOT_APPLICABLE'),'source_evidence_properties':json.dumps(family['source_evidence_properties'],ensure_ascii=False),'axis_X':'length','axis_Y':'horizontal_thickness','axis_Z':'vertical_height'}.items():o[k]=val
    mat=bpy.data.materials.new(body['id']+'_MAT');mat.diffuse_color=(.65,.38,.16,1);o.data.materials.append(mat)
   bpy.ops.wm.save_as_mainfile(filepath=str(path.resolve()))
  else:
   bpy.ops.wm.open_mainfile(filepath=str(path.resolve()));actual={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'};assert len(actual)==len(family['bodies']);errs=[]
   for body in family['bodies']:
    o=actual[body['id']];v=[[q.co[i]*1000 for i in range(3)] for q in o.data.vertices];assert len(v)==len(body['vertices']);assert [list(p.vertices) for p in o.data.polygons]==body['faces'];delta=max(abs(a-b) for va,vb in zip(v,body['vertices']) for a,b in zip(va,vb));assert delta<=.001;dims=bounds(v);assert max(abs(a-b) for a,b in zip(dims,body['target_dimensions_xyz_mm']))<=.001
    assert o['axis_Z']=='vertical_height' and o['approval_status']=='CANDIDATE_NOT_APPROVED';closed(v,body['faces']);o.data.calc_loop_triangles();signed=0.
    for tri in o.data.loop_triangles:
     a,b,c=[o.data.vertices[i].co*1000 for i in tri.vertices];signed+=a.dot(b.cross(c))/6
    vol=abs(signed);assert abs(vol-body['expected_volume_mm3'])/body['expected_volume_mm3']<1e-5
    errs.append({'id':body['id'],'max_coordinate_delta_mm':delta,'dimensions_xyz_mm':dims,'closed_single_body_euler2':True,'triangulated_volume_mm3':vol,'analytic_volume_mm3':body['expected_volume_mm3'],'properties_reopened':True})
   reports.append({'master_id':family['master_id'],'status':'PASS_SAVE_INDEPENDENT_REOPEN','body_count':len(actual),'checks':errs,'blend_file':path.name,'blend_sha256':digest(path),'blender_version':bpy.app.version_string,'approved':False})
 if mode=='reopen':write(out/'MASTER_CANDIDATE_REOPEN_VALIDATION.json',reports);print('REOPEN_PASS',json.dumps(reports))
if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
 if args[0]=='generate':generate(pathlib.Path(args[1]).resolve())
 else:blender(args[0])
