#!/usr/bin/env python3
"""Build the canonical T-018 plan, and a Blender scene when run by Blender."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from p3_3_whole_building_common_v001 import ROOT, compile_runtime

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="production/zhenguo_wanfo/build/P3_3_WHOLE_BUILDING_RUNTIME_MANIFEST_V001.json"); ap.add_argument("--blend"); ap.add_argument("--pm005",type=float)
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else None
    args,_=ap.parse_known_args(argv); values={"PM-005":args.pm005} if args.pm005 is not None else None
    runtime=compile_runtime(values); out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(runtime,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    try: import bpy
    except ImportError: return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for rec in runtime["records"]:
        p=rec["placement"]; point=p.get("point_mm") or p.get("start_mm")
        if point:
            bpy.ops.mesh.primitive_cube_add(size=.12, location=tuple(v/1000 for v in point)); obj=bpy.context.object; obj.name=rec["runtime_instance_id"]
            for key in ("runtime_instance_id","legacy_instance_id","component_id","graph_parent_node_id","p3_3_disposition","historical_claim_boundary"): obj[key]=rec[key]
    bpy.context.scene["p3_3_semantic_snapshot_sha256"]=runtime["semantic_snapshot_sha256"]
    if args.blend: bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/args.blend))
if __name__=="__main__": main()
