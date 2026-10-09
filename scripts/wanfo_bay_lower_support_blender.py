import bpy,json,sys,pathlib,hashlib
args=sys.argv[sys.argv.index('--')+1:];mode=args[0];root=pathlib.Path(args[1]);out=root/'output';out.mkdir(exist_ok=True)
payload=json.loads((root/'PILOT_GEOMETRY.json').read_text());path=out/'WANFO_BAY_LOWER_SUPPORT_FIRST_ARTICLE_V001.blend'
if mode=='build':
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1.
 bpy.context.scene['status']='FIRST_ARTICLE_NOT_APPROVED_NOT_COMPLETE_BAY'
 for record in payload['objects']:
  name=record['id'];me=bpy.data.meshes.new(name);me.from_pydata([[x*.001 for x in v] for v in record['vertices']],[],record['faces']);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o)
  for k,v in record.get('properties',{}).items():o[k]=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) or v is None else v
  mat=bpy.data.materials.new(name+'_material');mat.diffuse_color=(.9,.48,.1,1) if name.startswith('trial:') else (.48,.36,.23,1);o.data.materials.append(mat)
 bpy.ops.wm.save_as_mainfile(filepath=str(path))
else:
 bpy.ops.wm.open_mainfile(filepath=str(path));actual={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'};assert len(actual)==67
 maxd=0.
 for record in payload['objects']:
  o=actual[record['id']];assert len(o.data.vertices)==len(record['vertices']);assert [list(p.vertices) for p in o.data.polygons]==record['faces']
  for a,b in zip(o.data.vertices,record['vertices']):maxd=max(maxd,max(abs(a.co[i]*1000-b[i]) for i in range(3)))
 assert maxd<=.001,maxd
 r={'status':'PASS_SAVE_INDEPENDENT_REOPEN','entities':67,'max_coordinate_delta_mm':maxd,'complete_bay':False,'approved':False,'blender_version':bpy.app.version_string,'blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 (out/'BLENDER_REOPEN_VALIDATION.json').write_text(json.dumps(r,indent=2));print(r)
