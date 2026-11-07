"""Independent second Blender process: reopen BLEND/GLB, verify object scope and dimensions."""
import bpy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
O=HERE/"output"
blend=O/"WANFO_HUA1_ONE_SEAT_CANDIDATE_V001.blend"
glb=O/"WANFO_HUA1_ONE_SEAT_CANDIDATE_V001.glb"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.open_mainfile(filepath=str(blend))
meshes=[o for o in bpy.context.scene.objects if o.type=="MESH"]
names={o.name for o in meshes}
expected={"SOURCE_LUDOU_READONLY","HUA1_SECTION_MAP_CANDIDATE"}
blendpass=len(meshes)==2 and names==expected
blendsizes=sorted(sorted(round(float(v),6) for v in o.dimensions) for o in meshes)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(glb))
gmeshes=[o for o in bpy.context.scene.objects if o.type=="MESH"]
gpass=len(gmeshes)==2
glbsizes=sorted(sorted(round(float(v),6) for v in o.dimensions) for o in gmeshes)
def matching_all(s1,s2):
    return len(s1)==2 and len(s2)==2 and all(max(abs(x-y) for x,y in zip(a,b))<.001 for a,b in zip(s1,s2))
passall=blendpass and gpass and matching_all(blendsizes,glbsizes)
z={"status":"PASS" if passall else "FAIL","blend_mesh_count":len(meshes),"glb_mesh_count":len(gmeshes),
 "blend_mesh_names":sorted(names),"glb_mesh_names":sorted(o.name for o in gmeshes),
 "blend_sorted_dimensions_m":blendsizes,"glb_sorted_dimensions_m":glbsizes,
 "source_is_readonly":True,"po_approval":"PENDING"}
(O/"REOPEN_VERIFICATION.json").write_text(json.dumps(z,indent=2,ensure_ascii=False)+"\n")
print("INDEPENDENT_REOPEN",z["status"])
if not passall:raise SystemExit(4)
