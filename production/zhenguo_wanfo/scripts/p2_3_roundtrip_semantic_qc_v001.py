#!/usr/bin/env python3
"""Cross-version semantic snapshot and cloud/local returned-file comparison."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

def canonical(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def vector(v): return [round(float(x),3) for x in v]

def snapshot():
    import bpy
    objects=[]
    for ob in sorted((x for x in bpy.data.objects if x.type=="MESH"),key=lambda x:x.name):
        verts=ob.data.vertices
        bounds=[[round(min(v.co[i] for v in verts),3),round(max(v.co[i] for v in verts),3)] for i in range(3)]
        objects.append({"instance_id":ob.get("instance_id"),"name":ob.name,"family_id":ob.get("family_id"),
            "variant_id":ob.get("variant_id"),"mesh_data":ob.data.name,"vertices":len(verts),"faces":len(ob.data.polygons),
            "local_bounds_mm":bounds,"location_mm":vector(ob.location),"rotation_rad":vector(ob.rotation_euler),
            "scale":vector(ob.scale),"historical_state_tag":ob.get("historical_state_tag"),"time_layer":ob.get("time_layer"),
            "evidence_class":ob.get("evidence_class"),"source_layer":ob.get("source_layer"),
            "originality_status":ob.get("originality_status"),"parameter_ids":ob.get("parameter_ids"),
            "override_ids":ob.get("override_ids"),"bounded_placeholder":ob.get("bounded_placeholder"),
            "presentation":ob.get("presentation")})
    cameras=[{"name":ob.name,"location_mm":vector(ob.location),"rotation_rad":vector(ob.rotation_euler),
              "type":ob.data.type,"ortho_scale":round(float(ob.data.ortho_scale),3)}
             for ob in sorted((x for x in bpy.data.objects if x.type=="CAMERA"),key=lambda x:x.name)]
    return {"contract":"P2_3_ROUNDTRIP_SEMANTIC_V001","objects":objects,"cameras":cameras,
            "instance_count":len(objects),"variant_ids":sorted(set(x["variant_id"] for x in objects)),
            "family_counts":{f:sum(x["family_id"]==f for x in objects) for f in sorted(set(x["family_id"] for x in objects))},
            "collections":sorted(c.name for c in bpy.data.collections if c.name.startswith("P2_3_"))}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("snapshot","cloud-save","compare"),required=True)
    p.add_argument("--reference",type=Path)
    p.add_argument("--output",type=Path)
    p.add_argument("--result",type=Path)
    a=p.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    now=snapshot()
    if a.reference:
        expected=json.loads(a.reference.read_text(encoding="utf-8"))
        match=now==expected
    else: match=True
    result={"contract":now["contract"],"mode":a.mode,"status":"PASS" if match else "FAIL",
            "blender_version":__import__("bpy").app.version_string,
            "instance_count":now["instance_count"],"variant_count":len(now["variant_ids"]),
            "semantic_sha256":hashlib.sha256(canonical(now).encode()).hexdigest(),
            "reference_semantic_sha256":hashlib.sha256(canonical(expected).encode()).hexdigest() if a.reference else None}
    if a.mode=="snapshot":
        if not a.output: raise ValueError("snapshot requires --output")
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(now,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    elif a.mode=="cloud-save":
        if not a.output: raise ValueError("cloud-save requires --output")
        if not match: raise ValueError("Cloud input semantic mismatch")
        import bpy
        bpy.context.preferences.filepaths.save_version=0
        bpy.ops.wm.save_as_mainfile(filepath=str(a.output.resolve()))
    if a.result:
        a.result.parent.mkdir(parents=True,exist_ok=True)
        a.result.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("P2_3_ROUNDTRIP_"+result["status"],canonical(result))
    if not match: raise ValueError("Core geometry or metadata changed")

if __name__=="__main__": main()
