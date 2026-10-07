import bpy,json
from pathlib import Path
r=Path(__file__).resolve().parent;d=json.loads((r/'WEST_SEAM_V002_MESHES.json').read_text());expected={o['id']:o for o in d['objects']};obs=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or not ob.get('logical_object_id'):continue
 id=ob['logical_object_id'];ob.data.calc_loop_triangles();rec=dict(expected[id]);rec['vertices']=[list(ob.matrix_world@v.co) for v in ob.data.vertices];rec['faces']=[list(t.vertices) for t in ob.data.loop_triangles];obs.append(rec)
d['objects']=obs;d['verification']='EXPORTED_FROM_INDEPENDENTLY_REOPENED_SAVED_BLEND';(r/'REOPENED_WEST_V002_MESHES.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));print('Reopened',len(obs),'physical meshes')
