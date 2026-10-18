#!/usr/bin/env python3
"""Render fixed orthographic T-018 review views from the current Blender scene."""
import argparse,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[3]
VIEWS={"PLAN":((0,0,32),(0,0,0)),"FRONT_ELEVATION":((0,-32,8),(1.5708,0,0)),"SIDE_ELEVATION":((32,0,8),(1.5708,0,1.5708)),"AXON":((24,-24,20),(1.0472,0,0.7854))}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output-dir",default="production/zhenguo_wanfo/review/P3_3_T018");argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else None;args,_=ap.parse_known_args(argv); out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=True)
 bpy.ops.object.camera_add();cam=bpy.context.object;bpy.context.scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=34
 scene=bpy.context.scene;scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
 for name,(loc,rot) in VIEWS.items(): cam.location=loc;cam.rotation_euler=rot;scene.render.filepath=str(out/f"P3_3_T018_{name}_V001.png");bpy.ops.render.render(write_still=True)
if __name__=="__main__":main()
