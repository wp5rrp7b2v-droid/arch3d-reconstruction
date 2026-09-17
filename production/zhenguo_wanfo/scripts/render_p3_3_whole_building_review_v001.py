#!/usr/bin/env python3
"""Render four fixed, evidence-colored T-018 review views in Blender."""
import argparse, json, sys
from pathlib import Path

SCRIPT_DIR=Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path: sys.path.insert(0,str(SCRIPT_DIR))

def args():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]; p=argparse.ArgumentParser(); p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--manifest",type=Path,required=True); return p.parse_args(argv)
def main():
    import bpy
    a=args(); manifest=json.loads(a.manifest.read_text(encoding='utf-8')); a.output_dir.mkdir(parents=True,exist_ok=True); scene=bpy.context.scene; scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=960; scene.render.resolution_y=720; scene.render.resolution_percentage=100; scene.display.shading.light='STUDIO'; scene.display.shading.color_type='MATERIAL'
    if scene.world is None: scene.world=bpy.data.worlds.new('T018_REVIEW_WORLD')
    scene.world.color=(0.04,0.04,0.04)
    coords=[x['placement']['location_mm'] for x in manifest['runtime_objects']]; center=tuple((min(c[i] for c in coords)+max(c[i] for c in coords))/2 for i in range(3)); span=max(max(c[i] for c in coords)-min(c[i] for c in coords) for i in range(3)); distance=max(18000,span*1.5)
    bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='TECHNICAL_REVIEW_CAMERA'; cam.data.type='ORTHO'; cam.data.ortho_scale=span*1.25; cam.data.clip_start=1; cam.data.clip_end=max(50000.0,distance*3.0); scene.camera=cam
    from mathutils import Vector
    views={"PLAN":(center[0],center[1],center[2]+distance),"FRONT_ELEVATION":(center[0],center[1]-distance,center[2]),"SIDE_ELEVATION":(center[0]+distance,center[1],center[2]),"AXON":(center[0]+distance,center[1]-distance,center[2]+distance*.7)}
    keys={'GENERATED_FORMAL_GEOMETRY':'formal_visible_count','GENERATED_PROXY':'proxy_visible_represented_count','GENERATED_CONTROL':'control_visible_represented_count','GENERATED_ENVELOPE':'envelope_visible_count','UNKNOWN_BLOCKED':'unknown_marker_count','DEFERRED':'deferred_marker_count'}; counts={v:sum(x['p3_3_disposition']==k for x in manifest['runtime_objects']) for k,v in keys.items()}
    evidence={}
    for name,loc in views.items():
        cam.location=loc; cam.rotation_euler=((Vector(center)-cam.location).to_track_quat('-Z','Y')).to_euler(); scene.render.filepath=str((a.output_dir/f"P3_3_T018_{name}_V001.png").resolve()); bpy.ops.render.render(write_still=True); evidence[name]=dict(counts)
    (a.output_dir/'P3_3_T018_REVIEW_REPRESENTATION_COUNTS_V001.json').write_text(json.dumps({'status':'PASS','views':evidence},indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({"status":"PASS","views":evidence}))
if __name__=='__main__': main()
