"""C02 connected structural seed from PR75 measured geometry.

DO NOT CALL THIS 'four approved new profiles installed'. Four profile classes have NOT
all passed PO visual form; this rebuild deliberately restores existing jointed
source geometry and real SANDOU before any new-shape replacement.
Source BLEND is read-only; exact 89-node hash is validated.
"""
import bpy,sys,math,hashlib,json,os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/'output';OUT.mkdir(exist_ok=True,parents=True)
SOURCE=REPO/'production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-20/west_spacer_v001/output/WANFO_WEST_SPACER_TRIAL_V001.blend'
SOURCE_SHA='5c81c836cc7ca3a229eebe5ac9cb4c62a744b9a1eeb10b0e9683cf0ccd097f13'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA
A=['trial:EAST_FRONT_COLUMN_CANDIDATE','trial:EAST_FRONT_COLUMN_LUDOU',
'trial:EAST_FRONT_HUA1_LOCAL','trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL',
'trial:EAST_FRONT_HUA2_LOCAL','trial:EAST_FRONT_SANDOU_LEFT','trial:EAST_FRONT_SANDOU_RIGHT',
'trial:EAST_FRONT_TRANSVERSE_MANGONG','trial:EAST_FRONT_NIDAO_GUAZI',
'trial:EAST_FRONT_TOU_ANG_LOCAL','trial:EAST_FRONT_ER_ANG_LOCAL',
'trial:EAST_FRONT_LOWER6_END_SEGMENT','trial:EAST_UPPER6_FULL_BEAM_CANDIDATE',
'trial:EAST_FRONT_SPACER_HUAGONG','trial:EAST_FRONT_SPACER_LINGGONG',
'trial:EAST_FRONT_SANDOU','east:FOUR_BEAM']
assert len(A)==17
COLOR={'柱':'#8b7053','斗':'#dfae66','栱':'#53a17d','华':'#479488','昂':'#d36a48','梁':'#85709e'}
C={k:tuple(int(v[i:i+2],16)/255 for i in (1,3,5)) for k,v in COLOR.items()}
def kind(n):
 if 'ANG_LOCAL' in n:return '昂'
 if 'SANDOU' in n or 'DOU' in n:return '斗'
 if 'COLUMN' in n:return '柱'
 if any(w in n for w in ('BEAM','UPPER6','LOWER6')):return '梁'
 if 'HUA' in n:return '华'
 return '栱'
def local_to_world(o):
 return [[float(x*1000) for x in (o.matrix_world @ v.co)] for v in o.data.vertices]
def bbox(o):
 v=[o.matrix_world@u.co for u in o.data.vertices]
 return [[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
def setup():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
 allobj=[x for x in bpy.context.scene.objects if x.type=="MESH"]
 assert len(allobj)==89
 expected=set(A)
 for o in allobj:
  if o.name not in expected:bpy.data.objects.remove(o,do_unlink=True)
 objs={o.name:o for o in bpy.context.scene.objects if o.type=="MESH"}
 assert set(objs)==expected
 # Source BLEND stores millimetre numeric coordinates in its original Z-up world frame.
 # Retain exact imported source vertex arrays, all face topology and local object rotations.
 origin=Vector((4437.,5355.,-2112.))
 source_hashes={}
 for o in objs.values():
  # Capture exact mesh before moving the whole component rigidly.
  import struct
  verts=b''.join(struct.pack('<fff',*(float(q) for q in v.co)) for v in o.data.vertices)
  faces=b''.join(struct.pack('<I',i) for f in o.data.polygons for i in f.vertices)
  source_hashes[o.name]=dict(vertex_hash=hashlib.sha256(verts).hexdigest(),
      polygon_stream_hash=hashlib.sha256(faces).hexdigest(),
      vertex_count=len(o.data.vertices),face_count=len(o.data.polygons))
  mat=o.matrix_world.copy();mat.translation=mat.translation-origin;o.matrix_world=mat
  tint=C[kind(o.name)]
  material=bpy.data.materials.new('构件_'+kind(o.name)+'_'+str(len(bpy.data.materials)))
  material.diffuse_color=(*tint,1)
  o.data.materials.clear();o.data.materials.append(material)
  o.color=(*tint,1)
  o['PR75_ORIGINAL_ID']=o.name
  o['SRC_SHA256']=SOURCE_SHA
  o['FORM']='PR75_LEGACY_NOT_PO_FORM_APPROVED'
 scene=bpy.context.scene
 scene.name='万佛殿东缝前柱及隔架__真实连接种子__C02'
 scene['MODE']='STRUCTURAL_CONNECTION_SEED_NOT_FINAL_FORM'
 scene['PO_APPROVAL']='NOT_APPROVED'
 scene['SOURCE_GLBSHA']=SOURCE_SHA
 scene['NO_C01_ANG_SUBSTITUTION']='TRUE_PENDING_INTERFACE_CALIBRATION'
 return scene,objs,source_hashes
def mesh_geometry_json(objs,h):
 from mathutils import Vector
 out=[]
 for o in objs.values():
  # Coordinates are numeric mm, not m; source original BLEND numeric mm, output meters only for GLB.
  world=[list(map(float,o.matrix_world@v.co)) for v in o.data.vertices]
  # triangulate by loop triangles, never overwrite original ngon meshes
  o.data.calc_loop_triangles()
  faces=[[int(i) for i in p.vertices] for p in o.data.loop_triangles]
  out.append(dict(id=o.name,coordinates_mm=world,triangles=faces,
       original_identity=h[o.name],bounds_mm=bbox(o),group=kind(o.name)))
 return out
def add_camera(scene,tag):
 if tag=='head':pos=Vector((3400,-1400,2600));look=Vector((0,100,50));size=3600
 elif tag=='spacer':pos=Vector((2200,-3800,2500));look=Vector((0,-1900,1250));size=3000
 elif tag=='overview':pos=Vector((5300,-600,3800));look=Vector((0,-750,550));size=7000
 else:raise ValueError(tag)
 camd=bpy.data.cameras.new(tag+'_CAM');cam=bpy.data.objects.new(tag+'_CAM',camd)
 scene.collection.objects.link(cam)
 cam.location=pos*0.001
 cam.rotation_euler=((look-pos)).to_track_quat('-Z','Y').to_euler()
 camd.type='ORTHO';camd.ortho_scale=size*0.001
 scene.camera=cam;return cam
def render(scene,objects):
 scene.render.engine='CYCLES'
 scene.cycles.device='CPU'
 scene.cycles.samples=16
 scene.render.image_settings.color_mode='RGBA'
 if scene.world is None:scene.world=bpy.data.worlds.new('C02 World')
 scene.world.use_nodes=True
 scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value=(0.82,0.84,0.83,1)
 scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=0.8
 for obj in objects.values():
  for mat in obj.data.materials:
   mat.use_nodes=True
   node=mat.node_tree.nodes.get('Principled BSDF')
   if node:node.inputs['Base Color'].default_value=tuple(mat.diffuse_color)
 for i,(xyz,power,sz) in enumerate([((2.2,-4.,4.),1700,6.),((-3.,1.,5.),1400,7.)]):
  ld=bpy.data.lights.new('Area'+str(i),'AREA');lo=bpy.data.objects.new('Area'+str(i),ld)
  scene.collection.objects.link(lo)
  lo.location=xyz;lo.rotation_euler=(Vector((0.,-0.7,0.4))-lo.location).to_track_quat('-Z','Y').to_euler()
  ld.energy=power;ld.shape='DISK';ld.size=sz
 scene.render.resolution_x=1600
 scene.render.resolution_y=1000
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG'
 scene.render.film_transparent=False
 if scene.world is None:scene.world=bpy.data.worlds.new('default')
 for tag in ['head','spacer','overview']:
  for o in objects.values():
   o.hide_render=False
   if tag=='head' and any(w in o.name for w in ['UPPER6_FULL_BEAM','FOUR_BEAM','SPACER_']):o.hide_render=True
   if tag=='spacer' and any(w in o.name for w in ['COLUMN','TOU_ANG','ER_ANG','HUA1_','HUA2_','NIDAO','TRANSVERSE_MANGONG','INTERACTIVE_DOU']):o.hide_render=True
  cam=add_camera(scene,tag)
  scene.render.filepath=str(OUT/(tag+'_CONNECTED_C02_ZH.png'))
  bpy.ops.render.render(write_still=True)
  bpy.data.objects.remove(cam,do_unlink=True)
 for o in objects.values():o.hide_render=False
def main():
 scene,objs,h=setup()
 # The PR75 verified interface members are deliberately included: they are not flat free-standing boxes.
 assert all(x in objs for x in ('trial:EAST_FRONT_INTERACTIVE_DOU_LOCAL',
 'trial:EAST_FRONT_SANDOU_LEFT','trial:EAST_FRONT_SANDOU_RIGHT','trial:EAST_FRONT_SANDOU'))
 (OUT/'C02_ACTUAL_MESHES.json').write_text(json.dumps(
   dict(status='STRUCTURAL_SEED',source_sha256=SOURCE_SHA,model_source='PR75_LEGACY_WORK_MESH',
       prototype_is_not_c01_approved_form=True,
       interface_members_present=['LUDOU','INTERACTIVE_DOU','SANDOU_LEFT','SANDOU_RIGHT','SPACER_SANDOU'],
       support_geometry_kind='REAL_OLD_MESHES_NO_FAKE_CONNECTIONS',
       original_mesh_exact=True,units='millimetres',objects=mesh_geometry_json(objs,h)),
   ensure_ascii=False,indent=2)+'\n')
 # Convert ONLY this independent candidate scene from source numeric mm to real metres.
 # This leaves input BLEND untouched, and makes both saved C02 BLEND and C02 GLB unit-correct.
 for o in objs.values():
  for v in o.data.vertices:v.co *=0.001
  m=o.matrix_world.copy();m.translation *=0.001;o.matrix_world=m
 render(scene,objs)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'WANFO_EAST_FRONT_CONNECTED_C02_SEED.blend'))
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs.values():o.select_set(True)
 bpy.context.view_layer.objects.active=next(iter(objs.values()))
 bpy.ops.export_scene.gltf(filepath=str(OUT/'WANFO_EAST_FRONT_CONNECTED_C02_SEED.glb'),
  export_format='GLB',use_selection=True,export_yup=True,export_extras=True)
 print('C02_CONNECTED_SEED_SAVED',len(objs))
if __name__=='__main__':main()
