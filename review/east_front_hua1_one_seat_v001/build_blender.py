"""East-front HUA1 single-seat engineering candidate. NOT an approved Master.
Input is PR76 appearance-direction candidate plus PR81 read-only *rejected* C02 mesh.
Only the LUDOU lower seat is tested; upper INTERACTIVE DOU is OUT OF SCOPE.
"""
import bpy, json, hashlib, subprocess, math
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
OUT=HERE/"output"
OUT.mkdir(parents=True,exist_ok=True)
CAND=REPO/"review/gong_ang_form_v001/geometry/JUMP_1_HUAGONG_candidate.json"
LEGACY=REPO/"review/east_front_connectors_c02/output/C02_ACTUAL_MESHES.json"
EXPECTED={
    CAND:"567b5336f3319a66ff292aee88c57831850bb8a6",
    LEGACY:"c5a2622065589ed3588c7099f289384686dcb3c5"}
for path,sha in EXPECTED.items():
    actual=subprocess.check_output(["git","hash-object",str(path)],text=True).strip()
    assert actual==sha, (str(path),actual,sha)
candidate=json.loads(CAND.read_text(encoding="utf-8"))
source=json.loads(LEGACY.read_text(encoding="utf-8"))
assert candidate["id"]=="JUMP_1_HUAGONG"
assert source["source_sha256"]=="5c81c836cc7ca3a229eebe5ac9cb4c62a744b9a1eeb10b0e9683cf0ccd097f13"
objs={o["id"]:o for o in source["objects"]}
ludou=objs["trial:EAST_FRONT_COLUMN_LUDOU"]
oldhua=objs["trial:EAST_FRONT_HUA1_LOCAL"]
assert len(ludou["triangles"])==134 and len(candidate["faces"])==268
# Seat is existing recorded lower support plane, not inferred historic z.
seat_z=float(oldhua["bounds_mm"][0][2])
assert abs(seat_z+297.93149)<0.01
assert any(all(abs(ludou["coordinates_mm"][i][2]-seat_z)<0.001 for i in tri) for tri in ludou["triangles"])
v=candidate["vertices"]
width=max(a[1] for a in v)-min(a[1] for a in v)
height=max(a[2] for a in v)-min(a[2] for a in v)
length=max(a[0] for a in v)-min(a[0] for a in v)
assert abs(width-214.2)<0.001 and abs(height-153)<0.001 and abs(length-898.8)<0.001
# EVIDENCE-CONSTRAINED ENGINEERING PROPOSAL (NOT a PO-approved revision):
# 10 fen material thickness -> across world X (153mm)
# 14 fen material width -> vertical world Z (214.2mm)
# Former PDF/A2 evidence is only an aggregate reference; instance classification still unproven.
# x-longitude => -Y and source y-extrusion => X; positive transform determinant.
mapped=[[p[1]*153.0/width, -p[0], seat_z+(p[2]-min(a[2] for a in v))*214.2/height] for p in v]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.name="镇国寺万佛殿_华栱与栌斗_单接口试验_V001"
scene.unit_settings.system="METRIC"
scene["STATUS"]="CANDIDATE_ONLY_PO_FORM_PENDING"
scene["SCOPE"]="ONE_LOWER_SEAT_ONLY_NOT_FULL_ASSEMBLY"
scene["INPUT_LUDOU"]="PR81_REJECTED_ASSEMBLY_MESH_READ_ONLY"
scene["INPUT_HUA1"]="PR76_VISUAL_DIRECTION_PASS_NOT_INSTALLED"
scene["SECTION_MAPPING"]="10FEN_THICKNESS_X_14FEN_HEIGHT_Z_INFERENCE_FOR_INSTANCE"
scene["SEAT_Z_MM"]=seat_z
scene["NO_MASTER_CHANGED"]=True
scene["NOT_HISTORIC_JOINERY"]=True

def create(name,verts,faces,color):
    mesh=bpy.data.meshes.new(name+"_geom")
    mesh.from_pydata([tuple(float(x)/1000.0 for x in row) for row in verts],[],faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    scene.collection.objects.link(ob)
    mat=bpy.data.materials.new("彩色_"+name)
    mat.diffuse_color=(*color,1)
    mat.use_nodes=True
    node=mat.node_tree.nodes.get("Principled BSDF")
    if node:node.inputs["Base Color"].default_value=(*color,1)
    mesh.materials.append(mat)
    return ob

ld=create("SOURCE_LUDOU_READONLY",ludou["coordinates_mm"],ludou["triangles"],(.73,.49,.23))
hg=create("HUA1_SECTION_MAP_CANDIDATE",mapped,candidate["faces"],(.18,.51,.43))
hg["STATUS"]="ENGINEERING_CANDIDATE_PO_VISUAL_PENDING"
hg["CONTROLS_MM"]="L898.8_THICK153_HEIGHT214.2"
hg["UNCHANGED_NORMALIZED_END_CURVE"]=True
hg["SILHOUETTE_ASPECT_RATIO_CHANGED"]=True
hg["GONG_SOURCE_GIT_BLOB"]=EXPECTED[CAND]
ld["SOURCE_GIT_BLOB"]=EXPECTED[LEGACY]

meta={
 "state":"ENGINEERING_CANDIDATE_NOT_APPROVED",
 "seat":"LUDOU_TO_HUA1_BOTTOM_ONLY",
 "former_failed_assembly_not_promoted":True,
 "source_git_blobs":{str(CAND.relative_to(REPO)):EXPECTED[CAND],str(LEGACY.relative_to(REPO)):EXPECTED[LEGACY]},
 "original_geometry_sha256":source["source_sha256"],
 "source_PR76_candidate_extent_mm":[length,width,height],
 "mapped_extent_mm":[153.0,length,214.2],
 "coordinate_map":{"world_x":"candidate_y * (153/214.2)","world_y":"-candidate_x","world_z":"seat_z+(candidate_z+76.5)*(214.2/153)"},
 "seat_z_mm":seat_z,
 "source_hua1_removed":True,
 "ludou_preserved":True,
 "silhouette_scale_explicitly_changed":True,
 "PO_visual_gate":"PENDING",
 "historical_joint_gate":"UNKNOWN",
 "upper_interface_gate":"NOT_TESTED",
 "material_class_for_this_instance":"WORKING_HYPOTHESIS_NOT_ORIGINAL_MEASUREMENT"
}
(OUT/"CANDIDATE_MAPPING.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

world=bpy.data.worlds.new("Wanfo neutral");scene.world=world;world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.82,.84,.86,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.8
scene.render.engine="CYCLES"
scene.cycles.device="CPU";scene.cycles.samples=12
scene.render.resolution_x=1280;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.film_transparent=False
target=Vector((0,0,-.25))
for i,pos in enumerate([(1.4,-1.1,.75),(.95,0,.3)]):
    lightdata=bpy.data.lights.new("Light"+str(i),"AREA")
    l=bpy.data.objects.new("Light"+str(i),lightdata);scene.collection.objects.link(l)
    l.location=pos; l.rotation_euler=(target-l.location).to_track_quat("-Z","Y").to_euler()
    lightdata.energy=350;lightdata.shape="DISK";lightdata.size=2.1
def camera(pos,look,name,scale):
    cd=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,cd);scene.collection.objects.link(o)
    o.location=Vector(pos);o.rotation_euler=(Vector(look)-o.location).to_track_quat("-Z","Y").to_euler()
    cd.type="ORTHO";cd.ortho_scale=scale;scene.camera=o
    scene.render.filepath=str(OUT/(name+".png"))
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(o,do_unlink=True)

camera((1.55,-1.8,.85),(0,0,-.25),"HUA1_SEAT_AXON_ZH",1.45)
camera((1.75,0,-.04),(0,0,-.3),"HUA1_SEAT_FRONT_ZH",1.15)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"WANFO_HUA1_ONE_SEAT_CANDIDATE_V001.blend"))
bpy.ops.object.select_all(action="DESELECT")
ld.select_set(True);hg.select_set(True)
bpy.context.view_layer.objects.active=hg
bpy.ops.export_scene.gltf(filepath=str(OUT/"WANFO_HUA1_ONE_SEAT_CANDIDATE_V001.glb"),export_format="GLB",use_selection=True,export_extras=True,export_yup=True)
print("HUA1_SINGLE_SEAT_MODEL_GENERATED",seat_z)
