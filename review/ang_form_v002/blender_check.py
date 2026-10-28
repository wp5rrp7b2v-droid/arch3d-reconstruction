"""Cloud Blender export and separate-process reimport. Never opens production BLEND."""
import bpy,bmesh,json,sys,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
TASK=Path(__file__).resolve().parent;GEO=TASK/'geometry';mode=sys.argv[-1]
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
results=[]
for p in sorted(GEO.glob('*candidate.json')):
 d=json.loads(p.read_text());bpy.ops.wm.read_factory_settings(use_empty=True)
 if mode=='export':
  mesh=bpy.data.meshes.new(d['id']);mesh.from_pydata([[v*.001 for v in a] for a in d['vertices']],[],d['faces']);mesh.update()
  obj=bpy.data.objects.new(d['id'],mesh);bpy.context.collection.objects.link(obj)
  obj['status']='PENDING_PO_VISUAL_REVIEW';obj['historical_full_length']='UNKNOWN';obj['design_scope']='WORK_DESIGN_LENGTH' if d['work_design_length_only'] else 'MASTER_CONTROL_SPAN_NOT_FULL_LENGTH'
  mat=bpy.data.materials.new('V002候选');mat.diffuse_color=(.38,.52,.40,1);obj.data.materials.append(mat)
  bpy.ops.export_scene.gltf(filepath=str(p.with_suffix('.glb')),export_format='GLB',export_yup=True,export_extras=True)
 else:
  bpy.ops.import_scene.gltf(filepath=str(p.with_suffix('.glb')))
  objs=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(objs)==1
  obj=objs[0];assert obj.name==d['id'];verts=[obj.matrix_world@v.co for v in obj.data.vertices]
  bounds=[[min(v[i] for v in verts)*1000 for i in range(3)],[max(v[i] for v in verts)*1000 for i in range(3)]]
  expected=[[min(v[i] for v in d['vertices']) for i in range(3)],[max(v[i] for v in d['vertices']) for i in range(3)]]
  error=max(abs(bounds[j][i]-expected[j][i]) for j in range(2) for i in range(3));assert error<.001,(p,error)
  # Blender glTF splits normals/vertices; weld identical surface vertices before topology checks.
  bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bm.normal_update()
  assert all(e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True)*1e9;assert vol>0
  assert len(bm.verts)-len(bm.edges)+len(bm.faces)==2
  # Compare complete vertex-coordinate sets after glTF normal seam splits, not only bounds.
  src=[tuple(a) for a in d['vertices']];points=[tuple(v.co*1000) for v in bm.verts]
  import math
  haus=max(max(min(math.dist(a,b) for b in points) for a in src),max(min(math.dist(a,b) for b in src) for a in points));assert haus<.001
  expected_vol=abs(sum((d['vertices'][f[0]][0]*(d['vertices'][f[1]][1]*d['vertices'][f[2]][2]-d['vertices'][f[1]][2]*d['vertices'][f[2]][1])+d['vertices'][f[0]][1]*(d['vertices'][f[1]][2]*d['vertices'][f[2]][0]-d['vertices'][f[1]][0]*d['vertices'][f[2]][2])+d['vertices'][f[0]][2]*(d['vertices'][f[1]][0]*d['vertices'][f[2]][1]-d['vertices'][f[1]][1]*d['vertices'][f[2]][0]))/6 for f in d['faces']))
  assert abs(vol-expected_vol)/expected_vol<1e-5
  results.append(dict(file=p.with_suffix('.glb').name,sha256=hashlib.sha256(p.with_suffix('.glb').read_bytes()).hexdigest(),bytes=p.with_suffix('.glb').stat().st_size,bounds_error_mm=error,vertex_set_hausdorff_mm=haus,watertight=True,positive_volume_mm3=vol,volume_relative_error=abs(vol-expected_vol)/expected_vol,euler_number=2,independent_process_reimport='PASS'))
  bm.free()
if mode=='validate':write(TASK/'BLENDER_VALIDATION.json',dict(blender=bpy.app.version_string,gate='PASS',models=results,source_files_never_opened_for_write=True))
