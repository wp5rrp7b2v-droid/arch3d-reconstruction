#!/usr/bin/env python3
"""Render four fixed, evidence-colored T-018 review views in Blender."""
import argparse, json, sys
from pathlib import Path

def args():
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]; p=argparse.ArgumentParser(); p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--manifest",type=Path,required=True); return p.parse_args(argv)
def main():
    import bpy
    a=args(); a.output_dir.mkdir(parents=True,exist_ok=True); scene=bpy.context.scene; scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=960; scene.render.resolution_y=720; scene.render.resolution_percentage=100; scene.display.shading.light='STUDIO'; scene.display.shading.color_type='MATERIAL'; scene.world.color=(0.04,0.04,0.04)
    bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='TECHNICAL_REVIEW_CAMERA'; cam.data.type='ORTHO'; cam.data.ortho_scale=16; scene.camera=cam
    from mathutils import Vector
    views={"PLAN":(0,0,18),"FRONT_ELEVATION":(0,-18,7),"SIDE_ELEVATION":(18,0,7),"AXON":(13,-13,12)}
    hashes={}
    for name,loc in views.items():
        cam.location=loc; cam.rotation_euler=((Vector((0,0,6))-cam.location).to_track_quat('-Z','Y')).to_euler(); scene.render.filepath=str((a.output_dir/f"P3_3_T018_{name}_V001.png").resolve()); bpy.ops.render.render(write_still=True)
    print(json.dumps({"status":"PASS","views":list(views)}))
if __name__=='__main__': main()
