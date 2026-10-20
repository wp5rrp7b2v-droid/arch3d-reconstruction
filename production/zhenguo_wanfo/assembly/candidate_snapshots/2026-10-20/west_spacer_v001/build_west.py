"""Build WEST six-chuanfu + two spacer stations as non-approved trial geometry.
Source is the exact PO-approved upper6 front C01 working BLEND (82 meshes).
Only copies existing EAST trial geometry. No historical equivalence is claimed.
"""
import bpy, sys, json, hashlib, math
from pathlib import Path
from mathutils import Vector
root = Path(sys.argv[sys.argv.index("--")+2]).resolve()
out = root / "output"
out.mkdir(parents=True,exist_ok=True)
base = root / "BASE_APPROVED_FRONT_C01.blend"
expected = "baf43fc29fd9a769c89a0edc5cd4137d107133bf20239677105dde9baaa06e54"
assert hashlib.sha256(base.read_bytes()).hexdigest() == expected, "WRONG_PARENT_BASE"
pairs = {
 "trial:EAST_UPPER6_FULL_BEAM_CANDIDATE": "trial:WEST_UPPER6_FULL_BEAM_CANDIDATE",
 "trial:EAST_FRONT_SPACER_HUAGONG": "trial:WEST_FRONT_SPACER_HUAGONG",
 "trial:EAST_FRONT_SPACER_LINGGONG": "trial:WEST_FRONT_SPACER_LINGGONG",
 "trial:EAST_FRONT_SANDOU": "trial:WEST_FRONT_SANDOU",
 "trial:EAST_REAR_SPACER_DEPTH_LINGGONG": "trial:WEST_REAR_SPACER_DEPTH_LINGGONG",
 "trial:EAST_REAR_SPACER_LONGITUDINAL_LINGGONG": "trial:WEST_REAR_SPACER_LONGITUDINAL_LINGGONG",
 "trial:EAST_REAR_SANDOU": "trial:WEST_REAR_SANDOU",
}
def record(obj):
 obj.data.calc_loop_triangles()
 matrix = [list(row) for row in obj.matrix_world]
 local = [list(v.co) for v in obj.data.vertices]
 world = [[sum(matrix[i][j]*v[j] for j in range(3))+matrix[i][3] for i in range(3)] for v in local]
 assert all(math.isfinite(n) for p in world for n in p), obj.name
 return {"id":obj.name,"local":local,"matrix":matrix,"vertices":world,
         "faces":[list(t.vertices) for t in obj.data.loop_triangles]}
def all_meshes():
 return [record(o) for o in sorted(bpy.context.scene.objects,key=lambda a:a.name) if o.type=="MESH"]
def bounds(obj):
 points=[obj.matrix_world @ v.co for v in obj.data.vertices]
 return [[min(v[i] for v in points) for i in range(3)],[max(v[i] for v in points) for i in range(3)]]
def load(path):
 bpy.ops.wm.open_mainfile(filepath=str(path))
 assert len([o for o in bpy.context.scene.objects if o.type=="MESH"]) in (82,89)
if sys.argv[sys.argv.index("--")+2]=="build":
 load(base)
 original=all_meshes()
 assert len(original)==82
 (out/"BASELINE82.json").write_text(json.dumps({"objects":original},ensure_ascii=False,separators=(",",":")))
 scene=bpy.context.scene
 eb,wb = bounds(bpy.data.objects["east:FOUR_BEAM"]), bounds(bpy.data.objects["west:FOUR_BEAM"])
 delta=Vector((((wb[0][0]+wb[1][0])-(eb[0][0]+eb[1][0]))/2,
               ((wb[0][1]+wb[1][1])-(eb[0][1]+eb[1][1]))/2,wb[0][2]-eb[0][2]))
 assert abs(delta.x+4437)<1 and abs(delta.y)<1 and abs(delta.z+27)<1, \
        ("UNEXPECTED_WEST_FRAME_DATUM",tuple(delta),eb,wb)
 for src_name,dst_name in pairs.items():
  assert dst_name not in bpy.data.objects and src_name in bpy.data.objects
  src=bpy.data.objects[src_name]
  dst=src.copy()
  dst.data=src.data.copy()
  dst.name=dst_name
  for col in src.users_collection: col.objects.link(dst)
  matrix=src.matrix_world.copy()
  matrix.translation+=delta
  dst.matrix_world=matrix
  dst["effective_approval_status"]="PENDING_WEST_SPACER_V001_REVIEW"
  dst["approval_record"]="NO_NEW_PO_FORM_APPROVAL / COPY_FOR_ASSEMBLY_TEST_ONLY"
  dst["source_east_trial"]=src_name
  dst["historical_claim"]=False
  dst["material_equivalence"]="WORKING_HYPOTHESIS"
  dst["placement_method"]="EAST_TO_WEST_FOUR_BEAM_XY_CENTRE_AND_LOWER_FACE_Z"
  dst.color=(0.92,0.40,0.13,1)
 assert len([o for o in scene.objects if o.type=="MESH"])==89
 scene.name="WANFO_EAST_WEST_TWO_FRAMES_89_TRIAL"
 scene["whole_model_approval"]="NOT_APPROVED_AS_WHOLE"
 scene["new_west_candidate_count"]=7
 scene["canonical_master_change"]="NONE"
 scene["west_placement_hypothesis"]="mirror family geometry only; x/y beam centre, z underside shift; requires contact test"
 note=bpy.data.texts.new("WEST_SPACER_TRIAL_SCOPE_ZH")
 note.write("西缝上六椽栿及前后隔架：仅将东缝7件试装几何按两榀四椽栿中轴和底面关系转移。\n原82件不修改；西缝7件均为新候选，不自动批准。\n不得把东西缝同形当作历史实测，不得把当前模型中的其余待审件升级批准。\n")
 (out/"BUILD_INPUT_REPORT.json").write_text(json.dumps(
  {"baseline_sha256":expected,"source_count":82,"added_count":7,
   "total_meshes":89,"delta_mm":list(delta),
   "beam_east_bounds_mm":eb,"beam_west_bounds_mm":wb,
   "copy_map":pairs,"evidence_class":"ENGINEERING_TRIAL_NOT_HISTORICAL_GEOMETRY"},
  ensure_ascii=False,indent=2)+"\n")
 target=out/"WANFO_WEST_SPACER_TRIAL_V001.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
 print("WEST_TRIAL_89_SAVED",str(target))
 # Generate an actual headless Blender Workbench preview. Visual approval is separate.
 try:
  def view(name,loc,aim,scale):
   cam_data=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,cam_data);scene.collection.objects.link(cam)
   cam.location=loc;cam.rotation_euler=(Vector(aim)-cam.location).to_track_quat("-Z","Y").to_euler()
   cam_data.type="ORTHO";cam_data.ortho_scale=scale;scene.camera=cam
   scene.render.engine="BLENDER_WORKBENCH";scene.display.shading.light="STUDIO"
   scene.display.shading.color_type="OBJECT"
   scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
   scene.render.image_settings.file_format="PNG";scene.render.filepath=str(out/name+".png")
   bpy.ops.render.render(write_still=True)
   bpy.data.objects.remove(cam,do_unlink=True)
  view("WEST_SPACER_DETAIL",(-5500,-8500,3400),(0,0,-600),12000)
  view("TWO_FRAME_OVERVIEW",(-8500,-14000,8500),(1800,0,-200),19000)
 except Exception as exc:
  (out/"RENDER_FAILURE.txt").write_text(type(exc).__name__+": "+str(exc))
  print("PREVIEW_RENDER_FAILED",str(exc))
elif sys.argv[sys.argv.index("--")+2]=="reopen":
 load(out/"WANFO_WEST_SPACER_TRIAL_V001.blend")
 (out/"REOPENED89.json").write_text(json.dumps(
   {"objects":all_meshes(),"blend_sha256":hashlib.sha256((out/"WANFO_WEST_SPACER_TRIAL_V001.blend").read_bytes()).hexdigest(),
    "blender":bpy.app.version_string},ensure_ascii=False,separators=(",",":")))
 print("WEST_TRIAL_89_REOPENED")
else:
 raise ValueError("Expected build or reopen")
