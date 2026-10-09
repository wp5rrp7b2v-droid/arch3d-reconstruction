import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Quaternion
mode,rootarg=sys.argv[sys.argv.index('--')+1:];root=Path(rootarg).resolve();out=root/'output';out.mkdir(exist_ok=True)
data=json.loads((root/'APPROVED_GEOMETRY_V002.json').read_text());asset=out/'WANFO_TWO_FRAMES_THREE_PURLINS_APPROVED_V002.blend'
if mode=='build':
 bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.name='WANFO_TWO_FRAMES_THREE_PURLINS_APPROVED_V002'
 scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001;scene.unit_settings.length_unit='MILLIMETERS'
 for k,v in {'approval':'D-285','approval_scope':'LOCAL_VISIBLE_PROFILE_AND_GLB / BLEND_FINALIZATION','axis_spacing_mm':4437,'historical_common_z':'WORKING_HYPOTHESIS','historical_joinery':'NOT_VERIFIED','capacity':'NOT_TESTED','whole_building_closed':False,'physical_registry_mapping':'NOT_PROMOTED'}.items():scene[k]=v
 colors={'RETAINED_50':(.43,.39,.33,1),'PROFILE_CORRECTED_4':(.65,.37,.17,1),'PURLINS_3':(.05,.30,.56,1),'RECONSTRUCTED_SEATS_6':(.65,.36,.09,1)};colls={};mats={}
 for g,c in colors.items():
  colls[g]=bpy.data.collections.new(g);scene.collection.children.link(colls[g]);mats[g]=bpy.data.materials.new(g);mats[g].diffuse_color=c
 for item in data['objects']:
  verts=item['vertices'];origin=[(min(v[k] for v in verts)+max(v[k] for v in verts))/2 for k in range(3)]
  local=[[v[k]-origin[k] for k in range(3)] for v in verts]
  mesh=bpy.data.meshes.new(item['id']+'__MESH');mesh.from_pydata(local,[],item['faces']);mesh.update();obj=bpy.data.objects.new(item['id'],mesh);obj.location=origin;colls[item['group']].objects.link(obj);mesh.materials.append(mats[item['group']]);obj.color=colors[item['group']]
  for k,v in item['properties'].items():obj[k]=v
  obj['model_role']=item['group'];obj['approval']='D-285';obj['approved_entity_id']=item['id'];obj['historical_claim']=False
 txt=bpy.data.texts.new('README_ZH');txt.write('万佛殿两榀三道槫批准工作模型 V002\nPO外观批准D-285；四令栱弧线修正。63实体：50保留、4修正、3跨榀槫、6重建替木。\n单位毫米；西X0、东X4437。共同标高、历史槽形/木料拼接与承载能力未验证。\n不是整殿验收，不晋升Master，不覆盖原批准V011/V002独立榀快照。\n')
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':
    space=area.spaces.active;space.clip_end=100000;space.shading.type='SOLID';space.shading.color_type='MATERIAL';space.overlay.show_floor=False;space.region_3d.view_location=(2218.5,0,1050);space.region_3d.view_distance=11000;space.region_3d.view_rotation=Quaternion((.820,.424,.175,.340)).normalized();space.region_3d.view_perspective='ORTHO'
 assert len(scene.objects)==63;bpy.ops.wm.save_as_mainfile(filepath=str(asset),compress=True);print('SAVED_63_APPROVED_V002')
elif mode=='reopen':
 bpy.ops.wm.open_mainfile(filepath=str(asset));scene=bpy.context.scene;objects=[]
 for obj in sorted(scene.objects,key=lambda o:o.name):
  assert obj.type=='MESH' and not obj.modifiers and obj.parent is None;obj.data.calc_loop_triangles();matrix=[list(row) for row in obj.matrix_world];local=[list(v.co) for v in obj.data.vertices]
  vertices=[[sum(matrix[i][j]*v[j] for j in range(3))+matrix[i][3] for i in range(3)] for v in local]
  assert all(math.isfinite(x) for v in vertices for x in v)
  objects.append({'id':obj.name,'vertices':vertices,'faces':[list(t.vertices) for t in obj.data.loop_triangles],'local_vertices':local,'matrix_world':matrix,'properties':{k:obj[k] for k in obj.keys()},'collection':[c.name for c in obj.users_collection]})
 assert len(objects)==63
 r={'blender_version':bpy.app.version_string,'file_opened':bpy.data.filepath,'blend_sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'entity_count':len(objects),'unit_scale':scene.unit_settings.scale_length,'scene_approval':scene['approval'],'objects':objects}
 (out/'REOPENED_V002_MESHES.json').write_text(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n');print('INDEPENDENT_REOPEN_63')
else:raise ValueError(mode)
