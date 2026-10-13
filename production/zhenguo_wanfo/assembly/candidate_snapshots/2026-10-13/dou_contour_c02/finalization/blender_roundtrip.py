import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Matrix,Quaternion
mode,rootarg=sys.argv[sys.argv.index('--')+1:];root=Path(rootarg).resolve();out=root/'output';out.mkdir(exist_ok=True)
data=json.loads((root/'INPUT_GEOMETRY.json').read_text());asset=out/'WANFO_DOU_CONTOUR_CANDIDATE_C02.blend'
if mode=='build':
 original=root/'BASE_APPROVED_V002.blend';assert hashlib.sha256(original.read_bytes()).hexdigest()==data['original_blend_sha256']
 bpy.ops.wm.open_mainfile(filepath=str(original));scene=bpy.context.scene;scene.name='WANFO_DOU_CONTOUR_C02'
 scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001;scene.unit_settings.length_unit='MILLIMETERS'
 scene['whole_model_approval']='NOT_APPROVED_AS_WHOLE / LOCAL_APPROVALS_ONLY';scene['capacity']='NOT_TESTED';scene['historic_joinery']='NOT_PROVEN';scene['formal_stage3_closed']=False;scene['source_v004_sha256']=data['source_model_sha256']
 scene['source_original_blend_sha256']=data['original_blend_sha256'];scene['full_upper6']='PENDING_PO_APPROVAL';scene['dou_contour_candidate']='C02_FORM_APPROVED_CLOUD_VALIDATION_PENDING';scene['dou_dimensions_authority']='A1_GROUP_MEAN_RECONSTRUCTED_DESIGN';scene['approved_objects_inherited']=72;scene['pending_objects']=10
 colors={'APPROVED_EXISTING':(.43,.39,.33,1),'APPROVED_REPAIRS':(.60,.32,.13,1),'PENDING_CANDIDATES':(.7,.28,.12,1)};colls={};mats={}
 for group,color in colors.items():
  colls[group]=bpy.data.collections.new(group);scene.collection.children.link(colls[group]);mats[group]=bpy.data.materials.new(group);mats[group].diffuse_color=color
 retained=set(data['unchanged_original_ids']);sources={o['id']:o for o in data['objects']}
 for obj in list(scene.objects):
  if obj.name not in retained:bpy.data.objects.remove(obj,do_unlink=True)
 for item in data['objects']:
  name=item['id'];status=item['effective_status'];group=item['display_group']
  if name in retained:obj=bpy.data.objects[name]
  else:
   mesh=bpy.data.meshes.new(name+'__REPAIRED_MESH');mesh.from_pydata(item['local_vertices'],[],item['faces']);mesh.update();obj=bpy.data.objects.new(name,mesh);obj.location=item['origin'];scene.collection.objects.link(obj)
  for col in list(obj.users_collection):col.objects.unlink(obj)
  colls[group].objects.link(obj);obj['effective_approval_status']=status;obj['approval_record']=item['approval_record'];obj['historical_claim']=False;obj['source_entity_id']=name
  if name not in retained:
   obj['source_properties_json']=json.dumps(item['properties'],ensure_ascii=False);obj.data.materials.clear();obj.data.materials.append(mats[group]);obj.color=colors[group]
 txt=bpy.data.texts.new('V003_STATUS_ZH');txt.write('两榀三道槫修复联合工作模型 V003，82实体。\n原批准V002保留；东前/东后隔架与叉手、脊斗局部修复已批准。柱头V004只记录获批7件字段/层高修正。\n通长上六椽栿及其余柱头候选保留待审，不把整个模型称为全部批准。\n单位毫米；共同Z、隐藏槽口、历史昂长与承载力未验证；不关闭Stage3。\n')
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':
    v=area.spaces.active;v.clip_end=100000;v.shading.type='SOLID';v.shading.color_type='MATERIAL';v.overlay.show_floor=False;v.region_3d.view_location=(2218.5,0,-1000);v.region_3d.view_distance=15000;v.region_3d.view_rotation=Quaternion((.820,.424,.175,.340)).normalized();v.region_3d.view_perspective='ORTHO'
 assert len(scene.objects)==82;bpy.ops.wm.save_as_mainfile(filepath=str(asset),compress=True);print('BUILD82_SAVED')
elif mode=='reopen':
 bpy.ops.wm.open_mainfile(filepath=str(asset));scene=bpy.context.scene;objects=[]
 for obj in sorted(scene.objects,key=lambda o:o.name):
  assert obj.type=='MESH' and not obj.modifiers and obj.parent is None;obj.data.calc_loop_triangles();matrix=[list(row) for row in obj.matrix_world];local=[list(v.co) for v in obj.data.vertices];verts=[[sum(matrix[i][j]*v[j] for j in range(3))+matrix[i][3] for i in range(3)] for v in local]
  assert all(math.isfinite(x) for v in verts for x in v);objects.append({'id':obj.name,'vertices':verts,'faces':[list(t.vertices) for t in obj.data.loop_triangles],'local_vertices':local,'matrix_world':matrix,'effective_status':obj['effective_approval_status'],'approval_record':obj['approval_record']})
 assert len(objects)==82
 (out/'REOPENED_C02_MESHES.json').write_text(json.dumps({'blender_version':bpy.app.version_string,'blend_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'objects':objects,'unit_scale':scene.unit_settings.scale_length},ensure_ascii=False,separators=(',',':'))+'\n');print('INDEPENDENT_REOPEN82')
else:raise ValueError(mode)
