"""Independent spatial test: 1-jump Huagong + Linggong + Touang C01 + Erang C01.
No source meshes are rewritten; rigid transforms only. Blender 4.5 cloud.
Four component *families*, four candidate objects, NOT complete Wanfo structural assembly.
Do not treat contact geometry or illustrative place of Linggong as historically proven.
"""
import bpy, json, math, hashlib, sys
from pathlib import Path
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
TASK=Path(__file__).resolve().parent
REPO=TASK.parents[1]
OUT=TASK/'output';OUT.mkdir(parents=True,exist_ok=True)
MODE=sys.argv[-1];assert MODE in ('build','verify')
NAMES=[
 ('HUA1','第一跳华栱',REPO/'review/gong_ang_form_v001/geometry/JUMP_1_HUAGONG_candidate.json',(0.78,0.54,0.28,1)),
 ('LING','令栱',REPO/'review/gong_ang_form_v001/geometry/LINGGONG_candidate.json',(0.25,0.62,0.55,1)),
 ('TOU','头昂 C01',REPO/'review/ang_form_c01/geometry/TOU_ANG_ILLUSTRATION_C01_candidate.json',(0.87,0.38,0.25,1)),
 ('ER','二昂 C01',REPO/'review/ang_form_c01/geometry/ER_ANG_ILLUSTRATION_C01_candidate.json',(0.43,0.48,0.81,1)),
]
# Local pilot coordinate; offsets from East-front PR75 work-model world bbox centers.
# Ling is *not* an East-front certified member: isolated candidate positioned at Hua1 top.
centers={
 'HUA1':(0.,0.,0.),
 'LING':(0.,0.,154.3),   # flat bottom at Hua top, if axes interpreted as in this pilot
 'TOU':(0.,434.5,657.63),
 'ER':(0.,608.0,805.83),
}
a=math.radians(24.075498255078834);c=math.cos(a);s=math.sin(a)
# No mesh scale. Tangentially oriented gongs; ANG axes rotated to PR75 sloping trial direction.
ROT={
 'HUA1':Matrix(((0.,-1.,0.),(1.,0.,0.),(0.,0.,1.))),
 'LING':Matrix(((1.,0.,0.),(0.,1.,0.),(0.,0.,1.))),
 'TOU':Matrix(((0.,-1.,0.),(c,0.,-s),(s,0.,c))),
 'ER':Matrix(((0.,-1.,0.),(c,0.,-s),(s,0.,c))),
}
assert all(abs(r.determinant()-1)<1e-5 for r in ROT.values()) # mathutils Matrix is float32
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mat4(name):
 r=ROT[name];v=centers[name]
 return Matrix(((r[0][0],r[0][1],r[0][2],v[0]),(r[1][0],r[1][1],r[1][2],v[1]),
                (r[2][0],r[2][1],r[2][2],v[2]),(0.,0.,0.,1.)))
def input_manifest():
 return [dict(code=k,name_zh=n,path=str(p.relative_to(REPO)),sha256=sha(p),dimensions_mm=json.loads(p.read_text())['dimensions_mm'],
      transform_world_from_source=[list(map(float,row)) for row in mat4(k)]) for k,n,p,_ in NAMES]
def init_scene():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH'
 scene.display.shading.light='STUDIO'
 scene.display.shading.color_type='MATERIAL'
 scene.display.shading.show_shadows=True
 scene.display.shading.show_cavity=True
 scene.display.shading.cavity_type='BOTH'
 scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG'
 scene.render.film_transparent=False
 scene.world.color=(0.85,0.85,0.83)
 scene.view_settings.view_transform='Standard'
 return scene
def place():
 obs={}
 for key,name,p,col in NAMES:
  d=json.loads(p.read_text())
  mesh=bpy.data.meshes.new(name);mesh.from_pydata([[v*.001 for v in row] for row in d['vertices']],[],d['faces']);mesh.update()
  obj=bpy.data.objects.new(key+'__'+name,mesh);bpy.context.collection.objects.link(obj)
  m=mat4(key);t=Matrix(((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)))
  for i in range(3):
   for j in range(3):t[i][j]=m[i][j]
   t[i][3]=m[i][3]*.001
  obj.matrix_world=t
  obj['CANDIDATE_ID']=key
  obj['PO_FORM_STATUS']='PASS_V001' if key in ('HUA1','LING') else 'C01_PENDING'
  obj['world_pose_source']='PR75_EAST_FRONT_BBOX_ANCHOR' if key!='LING' else 'ASSUMED_SCHEMATIC_CROSS'
  mat=bpy.data.materials.new('材料色_'+key);mat.diffuse_color=col;obj.data.materials.append(mat)
  obs[key]=obj
 return obs
def bb(obj):
 # Exact transformed mesh bounds; transforming an object-space AABB corner box
 # overestimates bounds on oblique asymmetric ANG and fails true vertex checks.
 w=[obj.matrix_world@v.co for v in obj.data.vertices]
 return [[min(v[i] for v in w)*1000 for i in range(3)],[max(v[i] for v in w)*1000 for i in range(3)]]
def pair_analysis(objs):
 out=[]
 deps=bpy.context.evaluated_depsgraph_get()
 for i,(a,an,_,_) in enumerate(NAMES):
  for b,bn,_,_ in NAMES[i+1:]:
   oa,ob=objs[a],objs[b]
   aa,ab=bb(oa),bb(ob)
   bbox_overlap=[max(0.,min(ab[1][t],aa[1][t])-max(ab[0][t],aa[0][t])) for t in range(3)]
   possible=all(t>0.001 for t in bbox_overlap)
   overlap_count=0
   overlap_volume_mm3=None
   error=None
   if possible:
    try:
     A=BVHTree.FromObject(oa,deps);B=BVHTree.FromObject(ob,deps)
     overlap_count=len(A.overlap(B))
    except Exception as e:error='BVH:'+str(e)
    # Real 3D Boolean INTERSECT on a temporary copy, no modification of model
    try:
     tmp=oa.copy();tmp.data=oa.data.copy();bpy.context.collection.objects.link(tmp)
     mod=tmp.modifiers.new('INTERSECTION_VOLUME_ONLY','BOOLEAN')
     mod.operation='INTERSECT';mod.solver='EXACT';mod.object=ob
     deps=bpy.context.evaluated_depsgraph_get()
     ev=tmp.evaluated_get(deps)
     bm=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=deps)
     # mesh is in tmp object's local coords; rigid world transform preserves volume
     import bmesh
     b=bmesh.new();b.from_mesh(bm)
     overlap_volume_mm3=abs(float(b.calc_volume(signed=True)))*1e9 if b.faces else 0.
     b.free();bpy.data.meshes.remove(bm)
     bpy.data.objects.remove(tmp,do_unlink=True)
    except Exception as e:
     error=(error+';' if error else '')+'BOOLEAN:'+str(e)
     if 'tmp' in locals() and tmp.name in bpy.data.objects:bpy.data.objects.remove(tmp,do_unlink=True)
   else:overlap_volume_mm3=0.
   out.append(dict(a=a,b=b,a_zh=an,b_zh=bn,bbox_overlap_dimensions_mm=bbox_overlap,
    bbox_possible_intersection=possible,surface_triangle_overlap_count=overlap_count,
    solid_boolean_intersection_mm3=overlap_volume_mm3,diagnostic_error=error))
 return out
def camera(scene,key):
 if key=='iso':pos=(2450,2800,2200);target=(0,450,450);scale=3200
 elif key=='side':pos=(3300,400,750);target=(0,450,450);scale=2900
 elif key=='front':pos=(200,3700,1100);target=(0,450,450);scale=2500
 else:raise ValueError(key)
 cdata=bpy.data.cameras.new('Camera_'+key);cam=bpy.data.objects.new('Camera_'+key,cdata)
 scene.collection.objects.link(cam);scene.camera=cam
 cam.location=Vector(pos)*.001;goal=Vector(target)*.001
 direction=goal-cam.location;cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
 cdata.type='ORTHO';cdata.ortho_scale=scale*.001
 return cam
def label_image(path,subtitle):
 from PIL import Image,ImageDraw,ImageFont
 im=Image.open(path).convert('RGB');w,h=im.size
 board=Image.new('RGB',(w,h+220),'#f3f3ef');board.paste(im,(0,135))
 d=ImageDraw.Draw(board)
 ft='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
 f=lambda z:ImageFont.truetype(ft,z)
 d.rectangle((0,0,w,130),fill='#243f47')
 d.text((35,20),'镇国寺万佛殿｜四类栱昂｜独立试搭 C01',font=f(42),fill='#ffffff')
 d.text((36,79),subtitle,font=f(24),fill='#d7e9e7')
 d.rectangle((0,h+135,w,h+220),fill='#f3f3ef')
 for x,color,txt in [(40,'#c78a47','第一跳华栱'),(350,'#429e8d','令栱（位置假设）'),
                     (750,'#d96040','头昂 C01'),(1130,'#6e79cf','二昂 C01')]:
  d.rectangle((x,h+153,x+38,h+185),fill=color)
  d.text((x+48,h+150),txt,font=f(24),fill='#243f47')
 d.text((35,h+196),'纯四件空间试排：缺少斗、栌斗、梁、连接构件；非完整万佛殿装配。',font=f(20),fill='#9a3e31')
 board.save(path)
def render_views(scene):
 for v,label in [('iso','等轴试搭视图｜所有颜色代表独立网格，保留原构件尺度'),
                 ('side','正身侧面视图｜外檐方向与上下斜昂层位（候选方向）'),
                 ('front','外檐正面视图｜令栱横向，华栱纵向；位置仅为试排')]:
  cam=camera(scene,v)
  path=OUT/(v+'_FOUR_COMPONENTS_ZH.png')
  scene.render.filepath=str(path)
  bpy.ops.render.render(write_still=True)
  bpy.data.objects.remove(cam,do_unlink=True)
  # Chinese headers and legends are applied by system Python / Pillow after Blender rendering.
  # Blender's isolated Python may not have Pillow installed.
def build():
 scene=init_scene();objs=place();pairs=pair_analysis(objs)
 for k,o in objs.items():
  bpy.context.view_layer.objects.active=o;o.select_set(True)
 # No unsupported "PASS" for collision/contacts.
 collision=sum(1 for p in pairs if p['solid_boolean_intersection_mm3'] is not None and p['solid_boolean_intersection_mm3']>1.)
 unresolved=sum(1 for p in pairs if p['solid_boolean_intersection_mm3'] is None)
 status='FAIL_OVERLAP' if collision else ('UNVERIFIED_BOOLEAN' if unresolved else 'NO_VOLUME_OVERLAP_DETECTED')
 data={'scope':'FOUR_FAMILY_SCHEMATIC_PLACEMENT_NO_SOURCE_REPLACEMENT',
   'origin_world_pr75_mm':[4437.,5355.,-2297.831485],
   'structure_note':'1x first jump Huagong + 1x Linggong + Touang C01 + Erang C01; excludes second jump and other actual load-bearing members',
   'posing':'HUA1/ANG anchored approximately to PR75 East Front bbox centers; LING hypothetical cross placement NOT real East Ling instance',
   'input_manifest':input_manifest(),
   'pairs':pairs,'collision_gate':status,'pairs_over_1mm3':collision,
   'unresolved_boolean_pairs':unresolved,
   'mechanical_support':'NOT_VALIDATED_MISSING_CUPS_BEAMS_AND_OTHER_BRACKET_MEMBERS',
   'linggong_type_instance_mapping':'UNCONFIRMED; V001 general approved shape is not East verified geometry',
   'PO_VISUAL':'PENDING','source_approved_meshes_not_changed':True,
   'interpretation':'Collision finding is about rigid uncut candidate meshes at pilot pose, not a proof of real historic joinery.'}
 (OUT/'ASSEMBLY_VALIDATION.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 scene.render.image_settings.file_format='PNG'
 render_views(scene)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'WANFO_FOUR_GONG_ANG_PILOT_C01.blend'))
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs.values():o.select_set(True)
 bpy.context.view_layer.objects.active=objs['TOU']
 bpy.ops.export_scene.gltf(filepath=str(OUT/'WANFO_FOUR_GONG_ANG_PILOT_C01.glb'),
   export_format='GLB',use_selection=True,export_extras=True,export_yup=True)
 print('C01_BUILD_COMPLETE',status,'model_count',len(objs))
def verify():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 glb=OUT/'WANFO_FOUR_GONG_ANG_PILOT_C01.glb'
 bpy.ops.import_scene.gltf(filepath=str(glb))
 obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
 assert len(obs)==4,[o.name for o in obs]
 orig=json.loads((OUT/'ASSEMBLY_VALIDATION.json').read_text())
 allowed=set(x['code'] for x in orig['input_manifest'])
 got=set(o.name.split('__')[0] for o in obs)
 assert got==allowed,(got,allowed)
 # GLSZ checks after applying source rigid matrices should preserve world BBoxes within 0.005mm
 checks=[]
 for o in obs:
  key=o.name.split('__')[0];ex=next(x for x in orig['input_manifest'] if x['code']==key)
  data=json.loads((REPO/ex['path']).read_text())
  mx=Matrix(ex['transform_world_from_source'])
  expected=[]
  for row in data['vertices']:
   v=mx @ Vector((row[0],row[1],row[2],1))
   expected.append(tuple(v[:3]))
  eb=[[min(p[i] for p in expected) for i in range(3)],[max(p[i] for p in expected) for i in range(3)]]
  actual=bb(o)
  err=max(abs(actual[j][i]-eb[j][i]) for j in range(2) for i in range(3))
  assert err<.01,(key,err)
  checks.append(dict(id=key,bbox_error_mm=err,source_sha256=ex['sha256']))
 blend=OUT/'WANFO_FOUR_GONG_ANG_PILOT_C01.blend'
 assert blend.exists() and blend.stat().st_size>10000
 report={'technical_import_gate':'PASS','blender_version':bpy.app.version_string,
  'model_count':4,'objects':checks,
  'blend_sha256':sha(blend),'glb_sha256':sha(glb),
  'no_replacement_of_any_source_mesh':True,
  'assembly_contact_and_collision':orig['collision_gate'],
  'historical_installation':'NOT_APPROVED'}
 (OUT/'BINARY_REOPEN_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('C01_INDEPENDENT_REOPEN_PASS',json.dumps(report,ensure_ascii=False))
if MODE=='build':build()
else:verify()
