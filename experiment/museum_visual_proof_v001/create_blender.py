#!/usr/bin/env python3
"""Original, independent visual-arrangement proof, NOT measurement/engineering replica.
Museum use = qualitative layering inspiration only; no third-party mesh code or vertex copied.
"""
import bpy,math,json,hashlib,os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1.0
assemblage=[]
def mat(name,clr):
 m=bpy.data.materials.new(name);m.diffuse_color=(*clr,1)
 m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*clr,1)
 m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.75
 return m
wood=mat('PROTOTYPE_GONG',(0.67,.48,.29))
douwood=mat('PROTOTYPE_DOU',(0.79,.59,.35))
angwood=mat('PROTOTYPE_ANG',(0.45,.53,.51))
columnwood=mat('PROTOTYPE_COLUMN',(.69,.64,.54))
def box(name,loc,dims,m,kind):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
 o=bpy.context.object;o.name=name
 o.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(m)
 assemblage.append({'name':name,'kind':kind,'center_m':list(loc),'bbox_m':list(dims),'source':'ORIGINAL_WORKING_HYPOTHESIS'})
 return o
def prism(name,pts,axis,width,material,kind):
 # pts: (longitudinal coordinate, height), extruded across transverse width
 verts=[]
 for s in (-width/2,width/2):
  verts.extend([(t,s,z) if axis=='X' else (s,t,z) for t,z in pts])
 n=len(pts)
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
 for i in range(n):faces.append((i,(i+1)%n,(i+1)%n+n,i+n))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj)
 obj.data.materials.append(material)
 assemblage.append({'name':name,'kind':kind,'source':'ORIGINAL_WORKING_HYPOTHESIS','vertices':len(mesh.vertices)})
 return obj
def gong(name,axis,cross, length,z0,z1,material=wood):
 # Lower ends roll inward: gently stepped/relieved underside rather than PR83 semicircular cap.
 L=length/2
 profile=[(-L,z1),(-L,z0+.10),(-L+.03,z0+.06),(-L+.12,z0+.01),(-L+.18,z0),
          (L-.18,z0),(L-.12,z0+.01),(L-.03,z0+.06),(L,z0+.10),(L,z1)]
 o=prism(name,profile,axis,.165,material,'gong_candidate')
 if axis=='X':o.location.y=cross
 else:o.location.x=cross
 return o
# The following dimensions are intentionally NOT surveyed. Relative layout only.
# Goal: compare visual hierarchy and member type diversity with museum; no historical assertion.
box('PROOF_COLUMN',(0,0,-.51),(.31,.31,1.02),columnwood,'column_visual')
box('LUDOU_NECK',(0,0,.057),(.27,.27,.114),douwood,'dou_visual')
box('LUDOU_TOP',(0,0,.175),(.43,.41,.124),douwood,'dou_visual') # top .237
gong('HUA_1', 'X',0,1.12,.237,.410)
for sign,tag in [(-1,'A'),(1,'B')]:
 box('SANDOU_1_'+tag,(sign*.32,0,.469),(.18,.24,.118),douwood,'dou_visual') # .410-.528
 gong('TRANSVERSE_1_'+tag,'Y',sign*.32,.92,.528,.707)
gong('HUA_2','X',0,1.54,.707,.878)
for sign,tag in [(-1,'A'),(1,'B')]:
 box('SANDOU_2_'+tag,(0,sign*.29,.937),(.24,.18,.118),douwood,'dou_visual')
 gong('TRANSVERSE_2_'+tag,'X',sign*.29,1.74,.996,1.155)
# Individual angular members: demonstrate A1-style diagonal extension at rear; no asserted joint.
for sign,tag in [(-1,'A'),(1,'B')]:
 poly=[(-1.06,.42),(-1.00,.55),(.18,1.14),(.42,1.19),(.40,1.03),(.12,1.00)]
 o=prism('DIAGONAL_ANG_'+tag,poly,'X',.105,angwood,'ang_hypothesis')
 o.location.y=sign*.14
# Upper supporting sequence resembles museum's layered cross-grain hierarchy.
box('TOP_SUPPORT_A',(-.36,0,1.194),(.18,.36,.078),douwood,'dou_visual')
box('TOP_SUPPORT_B',(.36,0,1.194),(.18,.36,.078),douwood,'dou_visual')
gong('TOP_LONG_GONG','X',0,2.05,1.233,1.411)
box('TOP_SUPPORT_C',(0,0,1.466),(.30,.25,.11),douwood,'dou_visual')
gong('TOP_CROSS_MEMBER','Y',0,1.72,1.521,1.685)
# Validate elementary mesh integrity; do not mistake for real assembled contact verification.
for o in [o for o in scene.objects if o.type=='MESH']:
 assert len(o.data.vertices)>=8 and len(o.data.polygons)>=6, o.name
assert len(assemblage)>=14
# Exports
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'MUSEUM_REFERENCED_VISUAL_PROOF_V001.blend'))
bpy.ops.export_scene.gltf(filepath=str(OUT/'MUSEUM_REFERENCED_VISUAL_PROOF_V001.glb'),export_format='GLB',
    use_selection=False,export_apply=True)
scene.render.engine='CYCLES';scene.cycles.samples=16
scene.render.resolution_x=1120;scene.render.resolution_y=840;scene.render.resolution_percentage=100
world=bpy.data.worlds.new('WORLD');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.9,.91,.94,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.world=world
scene.render.image_settings.file_format='PNG'
def place_camera(name,offset):
 eye=Vector(offset);camd=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,camd)
 scene.collection.objects.link(cam);cam.location=eye
 focal=Vector((0,0,.56))
 cam.rotation_euler=(focal-eye).to_track_quat('-Z','Y').to_euler()
 camd.type='ORTHO';camd.ortho_scale=3.15;scene.camera=cam
 return cam
for i,offset in enumerate([(3,-4,6),(-4,2,5),(0,2,6)]):
 ld=bpy.data.lights.new('Area'+str(i),'AREA');light=bpy.data.objects.new('Area'+str(i),ld)
 scene.collection.objects.link(light);light.location=offset;ld.energy=450;ld.size=4.0
views=[]
for name,eye in [('ISOMETRIC',(3.4,-4.3,3.3)),('REVERSE',(-3.4,-3.9,3.2)),('SIDE',(0,-5.5,2.0))]:
 cam=place_camera('CAM_'+name,eye)
 p=OUT/('ORIGINAL_VISUAL_PROOF_'+name+'.png')
 scene.render.filepath=str(p)
 bpy.ops.render.render(write_still=True)
 views.append({'filename':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 bpy.data.objects.remove(cam,do_unlink=True)
report={
 'status':'CANDIDATE_VISUAL_ONLY',
 'gate':{'original_geometry_generated':True,'blender_blend_and_glb_generated':True,'three_views_created':len(views)==3,
         'A1_dimensions_verified':False,'real_contact_pass':False,'same_physical_instance_proven':False,
         'PO_visual_approval':False,'museum_model_reproduced':False},
 'source_kind':'original parametric geometry using visual composition inferred from museum and A1 2-27',
 'source_urls':['https://szbwgvue.chwhyun.cn/wanfodian/','A1 original survey PDF73 (printed p58), fig 2-27'],
 'museum_copyrighted_meshes_used':False,
 'all_dimensions':'temporary relative visual hypothesis, NOT historical measured dimensions',
 'component_count':len(assemblage),'components':assemblage,
 'views':views,
 'binaries':{},
 'status_note':'Do not mount into PR83 or master, no claim of historical correctness; requires PO visual gate and A1/A2 metric reconstruction.',
}
for name in ['MUSEUM_REFERENCED_VISUAL_PROOF_V001.blend','MUSEUM_REFERENCED_VISUAL_PROOF_V001.glb']:
 p=OUT/name
 report['binaries'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'PROOF_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('RESULT',report['status'],'OBJECTS',len(assemblage),'THREE_VIEWS',len(views))
