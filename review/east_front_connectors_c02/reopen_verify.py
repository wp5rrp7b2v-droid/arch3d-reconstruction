"""C02 separate Blender process reimport of GLB (m) and saved connected BLEND (mm)."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
P=ROOT/'output'
src=json.loads((P/'C02_ACTUAL_MESHES.json').read_text())
assert len(src['objects'])==17
glb=P/'WANFO_EAST_FRONT_CONNECTED_C02_SEED.glb'
blend=P/'WANFO_EAST_FRONT_CONNECTED_C02_SEED.blend'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
objs={o.name:o for o in bpy.context.scene.objects if o.type=="MESH"}
assert len(objs)==17,(len(objs),list(objs))
res=[]
for r in src['objects']:
 obj=objs[r['id']]
 expected=r['bounds_mm']
 points=[obj.matrix_world@v.co for v in obj.data.vertices]
 found=[[min(p[i] for p in points)*1000 for i in range(3)],[max(p[i] for p in points)*1000 for i in range(3)]]
 error=max(abs(found[j][i]-expected[j][i]) for j in range(2) for i in range(3))
 assert error<.02,(r['id'],error)
 res.append(dict(name=r['id'],bounds_error_mm=error))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.open_mainfile(filepath=str(blend))
objs2=[x for x in bpy.context.scene.objects if x.type=="MESH"]
assert len(objs2)==17,(len(objs2),[x.name for x in objs2])
assert bpy.context.scene.get('PO_APPROVAL')=='NOT_APPROVED'
validation=json.loads((P/'C02_INTERFACE_VALIDATION.json').read_text())
report=dict(
 blender_version=bpy.app.version_string,model_count=17,
 independent_GLTF_import='PASS',independent_BLENDER_reopen='PASS',
 geometry_bounds_checks=res,blend_sha256=sha(blend),glb_sha256=sha(glb),
 file_source_changed=False,source_sha256=src['source_sha256'],
 structural_seed_gate=validation['status'],
 PO_visual_form='NOT_APPROVED',
 updated_gong_ang_installation='NOT_DONE')
(P/'C02_BINARY_REOPEN_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('C02_BINARY_REOPEN_PASS',len(res))
