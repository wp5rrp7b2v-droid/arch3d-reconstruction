import bpy, sys, json, hashlib, math
from pathlib import Path

mode, rootarg = sys.argv[sys.argv.index('--')+1:]
root = Path(rootarg).resolve(); out = root/'output'; out.mkdir(exist_ok=True)
source = json.loads((root/'INPUT_GEOMETRY.json').read_text())
comparison = json.loads((root/'PARENT_C02_COMPARISON.json').read_text())
target = 'trial:EAST_UPPER6_FULL_BEAM_CANDIDATE'
asset = out/'WANFO_UPPER6_FRONT_TENON_C01.blend'

def dump(path):
    bpy.ops.wm.open_mainfile(filepath=str(path)); objects=[]
    for obj in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        assert obj.type=='MESH' and not obj.modifiers and obj.parent is None
        obj.data.calc_loop_triangles(); matrix=[list(row) for row in obj.matrix_world]
        local=[list(v.co) for v in obj.data.vertices]
        vertices=[[sum(matrix[i][j]*v[j] for j in range(3))+matrix[i][3] for i in range(3)] for v in local]
        assert all(math.isfinite(x) for v in vertices for x in v)
        objects.append({'id':obj.name,'vertices':vertices,'faces':[list(t.vertices) for t in obj.data.loop_triangles],'local_vertices':local,'matrix_world':matrix,'effective_status':obj['effective_approval_status'],'approval_record':obj['approval_record']})
    assert len(objects)==82
    return {'objects':objects,'blender_version':bpy.app.version_string,'blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

baseline = root/'BASE_C02.blend'
assert hashlib.sha256(baseline.read_bytes()).hexdigest()==comparison['baseline_blend_sha256']
if mode=='baseline':
    (out/'BASE_C02_MESHES.json').write_text(json.dumps(dump(baseline),ensure_ascii=False,separators=(',',':')))
elif mode=='build':
    bpy.ops.wm.open_mainfile(filepath=str(baseline)); scene=bpy.context.scene
    item=next(o for o in source['objects'] if o['id']==target)
    old=bpy.data.objects[target]; collections=list(old.users_collection)
    bpy.data.objects.remove(old,do_unlink=True)
    mesh=bpy.data.meshes.new(target+'__FRONT_TENON_C01');mesh.from_pydata(item['local_vertices'],[],item['faces']);mesh.update()
    obj=bpy.data.objects.new(target,mesh);obj.location=item['origin']
    for col in collections:col.objects.link(obj)
    obj['effective_approval_status']=item['effective_status'];obj['approval_record']=item['approval_record'];obj['historical_claim']=False;obj['source_entity_id']=target;obj['source_properties_json']=json.dumps(item['properties'],ensure_ascii=False)
    material=bpy.data.materials.new('UPPER6_FRONT_TENON_C01_PENDING');material.diffuse_color=(.7,.28,.12,1);obj.data.materials.append(material);obj.color=(.7,.28,.12,1)
    scene.name='WANFO_UPPER6_FRONT_TENON_C01';scene['upper6_front_tenon']='CANDIDATE_FORM_PENDING';scene['baseline_C02_six_local_form_approved']=True;scene['whole_model_approval']='NOT_APPROVED_AS_WHOLE';scene['modified_entity_count']=1
    note=bpy.data.texts.new('UPPER6_FRONT_TENON_C01_ZH');note.write('只修改上六椽栿前端，81邻件与C02 BLEND基底保持。\n210mm榫厚取东缝测绘；261.292mm段长、居中与直肩为复原假设。\n公开上传与云端执行已授权，候选外形仍待PO审核，不合并main。\n')
    assert len(scene.objects)==82;bpy.ops.wm.save_as_mainfile(filepath=str(asset),compress=True);print('BUILD82_SAVED')
elif mode=='reopen':
    (out/'REOPENED_UPPER6_FRONT_TENON_C01_MESHES.json').write_text(json.dumps(dump(asset),ensure_ascii=False,separators=(',',':')));print('INDEPENDENT_REOPEN82')
else:
    raise ValueError(mode)
