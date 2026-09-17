#!/usr/bin/env python3
"""Render four fixed T-018 views and view-aware projection evidence."""
import argparse, json, sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR=Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path: sys.path.insert(0,str(SCRIPT_DIR))

def args():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--manifest",type=Path,required=True); return p.parse_args(argv)

def projected_evidence(scene, camera, runtime):
    from bpy_extras.object_utils import world_to_camera_view
    points=[]; included=[]
    for obj in runtime:
        projected=[world_to_camera_view(scene,camera,obj.matrix_world @ __import__('mathutils').Vector(corner)) for corner in obj.bound_box]
        if not projected: continue
        xs=[p.x for p in projected]; ys=[p.y for p in projected]; zs=[p.z for p in projected]; points.extend((p.x,p.y) for p in projected)
        if max(xs)>=0 and min(xs)<=1 and max(ys)>=0 and min(ys)<=1 and max(zs)>=0: included.append(obj)
    return {"projected_in_frame_count":len(included),
            "per_family_in_frame_count":dict(sorted(Counter(o.get('family') for o in included).items())),
            "per_disposition_in_frame_count":dict(sorted(Counter(o.get('p3_3_disposition') for o in included).items())),
            "representation_class_in_frame_count":dict(sorted(Counter(o.get('representation_geometry_class','APPROVED_P3_1_MASTER') for o in included).items())),
            "camera_bounds":{"normalized_x":[0.0,1.0],"normalized_y":[0.0,1.0],"clip_start":camera.data.clip_start,"clip_end":camera.data.clip_end,"ortho_scale":camera.data.ortho_scale},
            "model_projected_bounds":{"min_x":min(x for x,_ in points),"max_x":max(x for x,_ in points),"min_y":min(y for _,y in points),"max_y":max(y for _,y in points)}}

def non_background_coverage(image_path):
    import bpy
    image=bpy.data.images.load(str(image_path),check_existing=False); pixels=list(image.pixels); bg=(0.04,0.04,0.04)
    changed=sum(any(abs(pixels[i+j]-bg[j])>0.035 for j in range(3)) for i in range(0,len(pixels),4)); total=max(1,len(pixels)//4)
    bpy.data.images.remove(image); return round(changed/total,6)

def main():
    import bpy
    from mathutils import Vector
    a=args(); manifest=json.loads(a.manifest.read_text(encoding='utf-8')); a.output_dir.mkdir(parents=True,exist_ok=True); scene=bpy.context.scene
    scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=960; scene.render.resolution_y=720; scene.render.resolution_percentage=100; scene.display.shading.light='STUDIO'; scene.display.shading.color_type='MATERIAL'
    if scene.world is None: scene.world=bpy.data.worlds.new('T018_TECHNICAL_WORLD')
    scene.world.color=(0.04,0.04,0.04)
    coords=[x['placement']['location_mm'] for x in manifest['runtime_objects']]; center=tuple((min(c[i] for c in coords)+max(c[i] for c in coords))/2 for i in range(3)); span=max(max(c[i] for c in coords)-min(c[i] for c in coords) for i in range(3)); distance=max(18000,span*1.5)
    bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='TECHNICAL_REVIEW_CAMERA'; cam.data.type='ORTHO'; cam.data.ortho_scale=span*1.25; cam.data.clip_start=1.0; cam.data.clip_end=max(100000.0,distance*4); scene.camera=cam
    views={"PLAN":(center[0],center[1],center[2]+distance),"FRONT_ELEVATION":(center[0],center[1]-distance,center[2]),"SIDE_ELEVATION":(center[0]+distance,center[1],center[2]),"AXON":(center[0]+distance,center[1]-distance,center[2]+distance*.7)}
    runtime=[o for o in scene.objects if o.get('runtime_instance_id')]; evidence={}
    for name,loc in views.items():
        cam.location=loc; cam.rotation_euler=((Vector(center)-cam.location).to_track_quat('-Z','Y')).to_euler(); bpy.context.view_layer.update()
        path=(a.output_dir/f"P3_3_T018_{name}_V001.png").resolve(); scene.render.filepath=str(path); projection=projected_evidence(scene,cam,runtime); bpy.ops.render.render(write_still=True); projection['non_background_pixel_coverage']=non_background_coverage(path); evidence[name]=projection
    payload={'status':'PASS','count_semantics':'PROJECTED_IN_FRAME_NOT_OCCLUSION_VISIBLE','global_runtime_count':len(runtime),'views':evidence}
    (a.output_dir/'P3_3_T018_REVIEW_REPRESENTATION_COUNTS_V001.json').write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(payload))
if __name__=='__main__': main()
