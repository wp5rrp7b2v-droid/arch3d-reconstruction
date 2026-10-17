"""Read-only Blender renders of byte-verified existing assets; never saves a BLEND."""
import bpy, json, hashlib, pathlib, sys, math
from mathutils import Vector
ROOT=pathlib.Path.cwd()
OUT=ROOT/'docs/component_atlas_v001/assets/models'
OUT.mkdir(parents=True,exist_ok=True)
jobs=json.loads((ROOT/'docs/component_atlas_v001/render_inputs.json').read_text())
report=[]
def mesh_digest(objects):
    payload=[]
    for o in sorted(objects,key=lambda x:x.name):
        payload.append([o.name,[list(v.co) for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],[list(r) for r in o.matrix_world]])
    return hashlib.sha256(json.dumps(payload).encode()).hexdigest()
for job in jobs:
    path=ROOT/job['path']
    if not path.exists():
        report.append(dict(job,status='BINARY_UNAVAILABLE'));continue
    original=hashlib.sha256(path.read_bytes()).hexdigest()
    if original!=job['sha256']:raise RuntimeError('Binary mismatch '+str(path))
    bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
    all_mesh=[o for o in bpy.context.scene.objects if o.type=='MESH']
    before=mesh_digest(all_mesh)
    # Keep canonical bodies only; fixture meshes remain hidden, never changed.
    body_names=job.get('body_names',[])
    selected=[o for o in all_mesh if o.name in body_names] if body_names else all_mesh
    if not selected:raise RuntimeError('Canonical body not found '+job['id'])
    for o in all_mesh:o.hide_render=o not in selected
    scene=bpy.context.scene
    scene.render.engine='BLENDER_WORKBENCH'
    scene.display.shading.light='STUDIO'
    scene.display.shading.color_type='SINGLE'
    scene.display.shading.single_color=(0.55,0.38,0.23)
    scene.display.shading.show_shadows=True
    scene.display.shading.show_cavity=True
    scene.display.shading.cavity_type='BOTH'
    scene.display.shading.background_type='WORLD'
    scene.world.color=(0.85,0.84,0.80)
    scene.render.resolution_x=1200;scene.render.resolution_y=850;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    groups=[[o] for o in selected] if job.get('individual',True) else [selected]
    images=[]
    for i,group in enumerate(groups):
        for o in all_mesh:o.hide_render=o not in group
        points=[o.matrix_world@Vector(c) for o in group for c in o.bound_box]
        lo=Vector([min(v[a] for v in points) for a in range(3)]);hi=Vector([max(v[a] for v in points) for a in range(3)])
        center=(lo+hi)/2;span=max(hi-lo)
        for view,direction in [('axon',(1.6,-2.7,1.8)),('front',(0,-1,0)),('side',(1,0,0))]:
            camera=bpy.data.objects.new('ATLAS_READONLY_CAMERA',bpy.data.cameras.new('ATLAS_READONLY_CAMERA'))
            scene.collection.objects.link(camera);camera.data.type='ORTHO';camera.data.ortho_scale=span*1.6
            camera.data.clip_start=max(span*.00001,.000001);camera.data.clip_end=span*100
            camera.location=center+Vector(direction).normalized()*span*6
            camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
            stem=job['id']+'--'+str(i)+'--'+view
            scene.render.filepath=str(OUT/(stem+'.png'));bpy.ops.render.render(write_still=True)
            images.append(dict(file=stem+'.png',object_names=[o.name for o in group],view=view))
            bpy.data.objects.remove(camera,do_unlink=True)
    after=mesh_digest(all_mesh)
    assert before==after
    assert hashlib.sha256(path.read_bytes()).hexdigest()==original
    report.append(dict(job,status='PASS_READONLY',blender=bpy.app.version_string,mesh_transform_unchanged=True,binary_unchanged=True,images=images))
(OUT/'RENDER_PROVENANCE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
