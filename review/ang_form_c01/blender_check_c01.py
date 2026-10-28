"""GitHub Actions Blender C01: 2 candidate GLBs export and independent reimport.
Never opens or edits any production BLEND/GLB or Master file.
Run: blender -b --factory-startup --python blender_check_c01.py -- export|validate
"""
import bpy,bmesh,json,sys,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
GEO=ROOT/'geometry'
MODE=sys.argv[-1]
assert MODE in ('export','validate')
inputs=sorted(GEO.glob('*ILLUSTRATION_C01_candidate.json'))
assert len(inputs)==2,[p.name for p in inputs]
checks=[]
for json_path in inputs:
 d=json.loads(json_path.read_text(encoding='utf-8'))
 bpy.ops.wm.read_factory_settings(use_empty=True)
 glb=json_path.with_suffix('.glb')
 if MODE=='export':
  mesh=bpy.data.meshes.new(d['id'])
  mesh.from_pydata([[float(v)*0.001 for v in row] for row in d['vertices']],[],d['faces'])
  mesh.update()
  obj=bpy.data.objects.new(d['id'],mesh);bpy.context.collection.objects.link(obj)
  obj['source']='PO_CHOSEN_GENERATED_ILLUSTRATION_NOT_OFFICIAL_MEASURED'
  obj['status']='PENDING_PO_VISUAL_REVIEW'
  obj['historical_full_length']='UNKNOWN'
  obj['geometry_scope']='INDEPENDENT_VISUAL_CANDIDATE_NOT_INSTALLATION'
  mat=bpy.data.materials.new('木材_色参考_非实物材质')
  mat.diffuse_color=(.53,.33,.16,1.0);mesh.materials.append(mat)
  bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',
    export_yup=True,export_extras=True,export_materials='EXPORT')
 else:
  assert glb.exists(),glb
  bpy.ops.import_scene.gltf(filepath=str(glb))
  objs=[x for x in bpy.context.scene.objects if x.type=='MESH']
  assert len(objs)==1,[x.name for x in objs]
  obj=objs[0]
  assert obj.name==d['id'],(obj.name,d['id'])
  wverts=[obj.matrix_world@v.co for v in obj.data.vertices]
  expected=[[min(float(v[i]) for v in d['vertices']) for i in range(3)],
    [max(float(v[i]) for v in d['vertices']) for i in range(3)]]
  bounds=[[min(v[i] for v in wverts)*1000 for i in range(3)],
    [max(v[i] for v in wverts)*1000 for i in range(3)]]
  err=max(abs(bounds[j][i]-expected[j][i]) for j in range(2) for i in range(3))
  assert err<.002,(json_path.name,'bbox error',err)
  # Blender can split glTF vertices on hard normal edges; weld exact positions for manifold checks.
  unique={};indices=[];coords=[]
  for vertex in obj.data.vertices:
   key=tuple(float(q) for q in vertex.co)
   if key not in unique:
    unique[key]=len(coords);coords.append(key)
   indices.append(unique[key])
  bm=bmesh.new()
  bv=[bm.verts.new(c) for c in coords]
  for f in obj.data.polygons:
   vv=[bv[indices[i]] for i in f.vertices]
   if len(set(vv))<3:continue
   bm.faces.new(vv)
  bm.normal_update()
  edges_bad=[e for e in bm.edges if not e.is_manifold]
  assert not edges_bad,(json_path.name,'non-manifold',len(edges_bad))
  euler=len(bm.verts)-len(bm.edges)+len(bm.faces)
  assert euler==2,(json_path.name,'euler',euler)
  vol=bm.calc_volume(signed=True)*1e9
  assert vol>0,(json_path.name,'volume',vol)
  # Source coords versus reimported coords, compare complete set not only bounding box.
  from mathutils import Vector
  pts=[tuple(float(q)*1000 for q in v.co) for v in bm.verts]
  src=[tuple(float(q) for q in row) for row in d['vertices']]
  # nearest check by ordered indexing would fail if Blender reorders vertices.
  from math import dist
  max_source=max(min(dist(a,b) for b in pts) for a in src)
  max_import=max(min(dist(a,b) for b in src) for a in pts)
  haus=max(max_source,max_import)
  assert haus<.002,(json_path.name,'vertex error',haus)
  checks.append(dict(name=d['id'],file=glb.name,sha256=hashlib.sha256(glb.read_bytes()).hexdigest(),
    imported_object_count=1,source_vertex_count=len(src),welded_vertex_count=len(pts),
    dimensions_error_mm=err,vertex_hausdorff_mm=haus,watertight=True,euler_number=euler,
    volume_mm3=vol,status='PASS'))
  bm.free()
if MODE=='validate':
 (ROOT/'BLENDER_VALIDATION.json').write_text(json.dumps(dict(
  status='PASS_CLOUD_BLENDER_REIMPORT_ONLY_PO_PENDING',
  blender_version=bpy.app.version_string,models=checks,
  original_approved_assets='NOT_OPENED_OR_MODIFIED',
  historical_form='NOT_TESTED',assembly='NOT_TESTED'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('WANFO_C01_BLENDER',MODE,'PASS',len(inputs))
