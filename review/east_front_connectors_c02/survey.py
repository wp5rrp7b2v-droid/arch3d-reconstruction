"""Survey as-built PR75 east front known connections. READ ONLY.
Not a source of new historical facts; preserved source GLB byte SHA enforced.
"""
import bpy,json,hashlib,math,bmesh,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/'output';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=REPO/'production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WANFO_WEST_SPACER_89_TRIAL_V001.glb'
EXPECTED='ed686f2ed81dc0ad0139a320bdd0c99709419c1c401bc1dff3b3635867f5a151'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(SOURCE))
objs={o.name:o for o in bpy.context.scene.objects if o.type=="MESH"}
assert len(objs)==89
TARGET=[
 'trial:EAST_FRONT_COLUMN_CANDIDATE','trial:EAST_FRONT_COLUMN_LUDOU',
 'trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL',
 'trial:EAST_FRONT_HUA2_LOCAL','trial:EAST_FRONT_SANDOU_LEFT','trial:EAST_FRONT_SANDOU_RIGHT',
 'trial:EAST_FRONT_TRANSVERSE_MANGONG','trial:EAST_FRONT_NIDAO_GUAZI',
 'trial:EAST_FRONT_TOU_ANG_LOCAL','trial:EAST_FRONT_ER_ANG_LOCAL',
 'trial:EAST_FRONT_LOWER6_END_SEGMENT','trial:EAST_UPPER6_FULL_BEAM_CANDIDATE',
 'trial:EAST_FRONT_SPACER_HUAGONG','trial:EAST_FRONT_SPACER_LINGGONG',
 'trial:EAST_FRONT_SANDOU','east:FOUR_BEAM']
assert all(n in objs for n in TARGET)
def bbox(o):
 v=[o.matrix_world@p.co for p in o.data.vertices]
 return [[round(min(p[i] for p in v)*1000,4) for i in range(3)],
         [round(max(p[i] for p in v)*1000,4) for i in range(3)]]
def meshinfo(o):
 verts=[list(round(1000*x,4) for x in (o.matrix_world@v.co)) for v in o.data.vertices]
 return dict(name=o.name,vertices=len(o.data.vertices),faces=len(o.data.polygons),
   world_bbox_mm=bbox(o),world_transform=[[round(float(v),8) for v in row] for row in o.matrix_world],
   world_vertex_sha256=hashlib.sha256(json.dumps(sorted(verts),separators=(',',':')).encode()).hexdigest(),
   local_vertices_mm=[list(round(1000*x,3) for x in v.co) for v in o.data.vertices][:20])
allparts=[meshinfo(objs[n]) for n in TARGET]
# Historical model connectivity is not physical contact proof: classify bbox gap and booleans.
PAIRS=[
 ('trial:EAST_FRONT_COLUMN_CANDIDATE','trial:EAST_FRONT_COLUMN_LUDOU'),
 ('trial:EAST_FRONT_COLUMN_LUDOU','trial:EAST_FRONT_HUA1_LOCAL'),
 ('trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL'),
 ('trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL','trial:EAST_FRONT_HUA2_LOCAL'),
 ('trial:EAST_FRONT_HUA2_LOCAL','trial:EAST_FRONT_TOU_ANG_LOCAL'),
 ('trial:EAST_FRONT_HUA2_LOCAL','trial:EAST_FRONT_ER_ANG_LOCAL'),
 ('trial:EAST_FRONT_TOU_ANG_LOCAL','trial:EAST_FRONT_ER_ANG_LOCAL'),
 ('trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_NIDAO_GUAZI'),
 ('trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL','trial:EAST_FRONT_SANDOU_LEFT'),
 ('trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL','trial:EAST_FRONT_SANDOU_RIGHT'),
 ('trial:EAST_FRONT_SANDOU_LEFT','trial:EAST_FRONT_TRANSVERSE_MANGONG'),
 ('trial:EAST_FRONT_SANDOU_RIGHT','trial:EAST_FRONT_TRANSVERSE_MANGONG'),
 ('trial:EAST_FRONT_SPACER_HUAGONG','trial:EAST_FRONT_SPACER_LINGGONG'),
 ('trial:EAST_FRONT_SPACER_LINGGONG','trial:EAST_FRONT_SANDOU'),
 ('trial:EAST_UPPER6_FULL_BEAM_CANDIDATE','trial:EAST_FRONT_SANDOU'),
 ('trial:EAST_UPPER6_FULL_BEAM_CANDIDATE','trial:EAST_FRONT_SPACER_LINGGONG')]
contacts=[]
for a,b in PAIRS:
 A=bbox(objs[a]);B=bbox(objs[b]);sep=[max(0.,A[0][i]-B[1][i],B[0][i]-A[1][i]) for i in range(3)]
 overlap=[max(0.,min(A[1][i],B[1][i])-max(A[0][i],B[0][i])) for i in range(3)]
 contacts.append(dict(a=a,b=b,aabb_gap_mm=sep,aabb_overlap_mm=overlap,
  aabb_touching=max(sep)<0.01 and min(overlap)<0.01,
  NOTE='AABB alone cannot verify matching contact patch'))
# Embedded metadata is read only. No geometry edits.
output=dict(source_glb=SOURCE.as_posix().split("arch3d-reconstruction/")[-1],source_sha256=EXPECTED,
 imported_mesh_count=len(objs),input_types='PR75_WORKING_CANDIDATES_NOT_ALL_VISUALLY_APPROVED',
 target_objects=allparts,survey_pairs=contacts,
 conclusion='READ_ONLY_SURVEY_NOT_APPROVAL')
(OUT/'PR75_EAST_FRONT_INTERFACE_SURVEY.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print('SURVEY_READY',len(allparts),'parts',len(contacts),'pairs')
