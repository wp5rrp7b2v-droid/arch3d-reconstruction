"""Export the already validated 89-mesh WEST trial BLEND to a portable GLB.
Do not save the source .blend; attach portable display materials only in memory.
Validation imports the GLB in a separate Blender process and checks named geometry
bounds and triangulated faces. Geometry distances are in original millimetres;
exporter roundtrip permits 0.03 mm for float32 glTF precision.
"""
import bpy, sys, json, hashlib, math, struct
from pathlib import Path
from mathutils import Vector

args=sys.argv[sys.argv.index("--")+1:]
assert len(args)==2,("EXPECTED_MODE_AND_TASK_ROOT",args)
mode,rootpath=args
root=Path(rootpath).resolve()
out=root/"output"
source=out/"WANFO_WEST_SPACER_TRIAL_V001.blend"
asset=out/"WANFO_WEST_SPACER_89_TRIAL_V001.glb"
baseline=out/"GLB_EXPORT_BASELINE.json"
expected_source_sha="5c81c836cc7ca3a229eebe5ac9cb4c62a744b9a1eeb10b0e9683cf0ccd097f13"
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mesh_records():
 result={}
 for obj in bpy.context.scene.objects:
  if obj.type!="MESH":continue
  obj.data.calc_loop_triangles()
  verts=[obj.matrix_world @ v.co for v in obj.data.vertices]
  assert verts,("EMPTY_MESH",obj.name)
  mins=[min(v[k] for v in verts) for k in range(3)]
  maxs=[max(v[k] for v in verts) for k in range(3)]
  assert all(math.isfinite(x) for x in mins+maxs)
  result[obj.name]={
   "world_bounds_mm":[mins,maxs],
   "triangle_count":len(obj.data.loop_triangles),
   "source_vertex_count":len(obj.data.vertices)
  }
 return result
def file_header(path):
 with path.open("rb") as f:buf=f.read(12)
 assert len(buf)==12, "GLB_HEADER_TOO_SHORT"
 magic,version,size=struct.unpack("<4sII",buf)
 assert magic==b"glTF" and version==2 and size==path.stat().st_size,("INVALID_GLB_HEADER",magic,version,size)
 return {"magic":"glTF","glb_version":version,"byte_length":size}
if mode=="export":
 assert source.exists(),"MISSING_APPROVED_WORKING_SOURCE"
 assert sha(source)==expected_source_sha,("SOURCE_SHA_MISMATCH",sha(source))
 validation=json.loads((out/"WEST_SPACER_VALIDATION.json").read_text())
 assert validation["status"]=="PASS_ASSEMBLY_CANDIDATE_ONLY"
 assert validation["new_blend_sha256"]==expected_source_sha
 bpy.ops.wm.open_mainfile(filepath=str(source))
 objects=[o for o in bpy.context.scene.objects if o.type=="MESH"]
 assert len(objects)==89,("SOURCE_OBJECT_COUNT",len(objects))
 ids=[o.name for o in objects];assert len(set(ids))==89
 before=mesh_records()
 # Distinctive presentation materials in this transient export session only.
 palette={
  "west_new":(0.90,0.36,0.09,1),
  "west_old":(0.32,0.55,0.67,1),
  "east_old":(0.69,0.53,0.33,1),
  "purlins":(0.52,0.60,0.49,1)}
 mats={}
 for name,color in palette.items():
  mat=bpy.data.materials.new("GLB_REVIEW_"+name)
  mat.use_nodes=True
  shader=mat.node_tree.nodes.get("Principled BSDF")
  shader.inputs["Base Color"].default_value=color
  shader.inputs["Roughness"].default_value=0.88
  mat.diffuse_color=color
  mats[name]=mat
 for obj in objects:
  group=("west_new" if obj.name.startswith("trial:WEST_") else
         "west_old" if obj.name.startswith("west:") else
         "east_old" if obj.name.startswith("east:") else
         "purlins")
  obj.data.materials.clear()
  obj.data.materials.append(mats[group])
  obj["glb_preview_role"]=group
  obj["glb_approval_scope"]="TRIAL_NOT_PO_APPROVED_AS_WHOLE"
 # Strictly verify geometry unchanged while adding temporary materials.
 assert mesh_records()==before,"EXPORT_PREP_GEOMETRY_CHANGED"
 for o in bpy.context.scene.objects:o.select_set(o.type=="MESH")
 bpy.ops.export_scene.gltf(
  filepath=str(asset),export_format="GLB",
  use_selection=True,export_yup=True,export_extras=True,
  export_materials="EXPORT",export_cameras=False,export_lights=False,
  export_apply=False)
 assert asset.exists() and asset.stat().st_size>20000
 header=file_header(asset)
 baseline.write_text(json.dumps({
  "status":"EXPORT_SOURCE_VERIFIED",
  "input_blend_sha256":expected_source_sha,
  "glb_sha256":sha(asset),
  "glb_header":header,
  "record_count":89,
  "mesh_records":before,
  "display_colors_are_export_only":True,
  "source_blend_modified":False,
  "all_candidates_still_pending_PO_review":True,
  "geometry_units":"millimetres in construction coordinates",
  "max_allowed_roundtrip_extent_error_mm":0.03
 },ensure_ascii=False,indent=2)+"\n")
 print("GLB_EXPORTED",asset,header["byte_length"],"sha256",sha(asset))
elif mode=="validate":
 check=json.loads(baseline.read_text())
 assert check["input_blend_sha256"]==expected_source_sha
 assert sha(source)==expected_source_sha
 assert sha(asset)==check["glb_sha256"],"EXPORTED_GLB_CHANGED"
 header=file_header(asset)
 # Blender --factory-startup opens a default Cube: remove the startup scene before
 # GLB import, otherwise its default Cube is incorrectly counted as model geometry.
 bpy.ops.object.select_all(action="SELECT")
 bpy.ops.object.delete(use_global=False)
 assert len([o for o in bpy.context.scene.objects if o.type=="MESH"])==0,"DIRTY_VALIDATION_SCENE"
 bpy.ops.import_scene.gltf(filepath=str(asset))
 imported=mesh_records()
 original=check["mesh_records"]
 missing=set(original)-set(imported)
 extra=set(imported)-set(original)
 assert not missing and not extra,("GLB_OBJECT_IDENTITIES_MISMATCH",sorted(missing),sorted(extra))
 max_error=0.0;sum_triangles=0
 for name,src in original.items():
  dst=imported[name]
  assert dst["triangle_count"]==src["triangle_count"],(
   "GLB_TRIANGLES_CHANGED",name,dst["triangle_count"],src["triangle_count"])
  for a,b in zip(src["world_bounds_mm"],dst["world_bounds_mm"]):
   for x,y in zip(a,b):
    d=abs(float(y)-float(x));max_error=max(max_error,d)
    assert d<=0.03,("GLB_BOUNDS_EXCEEDED_FLOAT32_TOLERANCE",name,x,y,d)
  sum_triangles+=dst["triangle_count"]
 assert sum_triangles>0
 summary={
  "status":"PASS_GLTF_GLB_IMPORTED_GEOMETRY",
  "input_blend_sha256":expected_source_sha,
  "glb_sha256":sha(asset),
  "glb_bytes":header["byte_length"],
  "glb_header":header,
  "blender_version":bpy.app.version_string,
  "source_object_count":len(original),
  "reimported_object_count":len(imported),
  "all_89_named_meshes_retained":True,
  "all_triangulated_faces_retained":True,
  "triangle_total":sum_triangles,
  "max_world_bounds_error_mm":max_error,
  "max_allowed_world_bounds_error_mm":0.03,
  "source_blend_original_unchanged":True,
  "new_geometry_approval":"NO_NEW_APPROVAL",
  "historical_shape_and_strength_verified":False,
  "source_validation":"WEST_SPACER_VALIDATION.json"
 }
 (out/"GLB_EXPORT_VALIDATION.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(summary,ensure_ascii=False,indent=2))
else:raise ValueError(mode)
