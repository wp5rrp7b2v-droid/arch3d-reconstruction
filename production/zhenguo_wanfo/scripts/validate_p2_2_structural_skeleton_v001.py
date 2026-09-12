#!/usr/bin/env python3
"""Independent in-Blender geometry check for a reopened T-007 candidate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve()
sys.path.insert(0,str(HERE.parent))
from generate_p2_2_structural_skeleton_v001 import FormalInputs, geometry_plan, roof_height_at_y, MACHINE_TOLERANCE_MM, PARAMS, OVERRIDES, DECISIONS, sha


def near(actual,expected,what,errors,tol=MACHINE_TOLERANCE_MM):
    if abs(float(actual)-float(expected))>tol:
        errors.append("%s: actual %s, expected %s"%(what,actual,expected))


def point(actual,expected,what,errors):
    if len(actual)!=len(expected):
        errors.append(what+": coordinate length mismatch")
    else:
        for k,(a,b) in enumerate(zip(actual,expected)):
            near(a,b,what+"[%d]"%k,errors)


def validate(blend_path,manifest_path,params=None,overrides=None):
    import bpy
    errors=[]
    manifest=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    inputs=FormalInputs(params=params or PARAMS,overrides=overrides or OVERRIDES)
    plan=geometry_plan(inputs)
    expected=manifest["semantic_summary"]
    for key,path in inputs.paths.items():
        if manifest["inputs"][key]["sha256"]!=sha(path):
            errors.append(key+": input hash differs from manifest")
    if manifest["approval_boundary"]["sha256"]!=sha(DECISIONS):
        errors.append("Approval decision log hash differs from manifest")
    if manifest["output_blend"]["sha256"]!=sha(blend_path):
        errors.append("Blend hash differs from manifest")
    if manifest["blender_version"]!=bpy.app.version_string:
        errors.append("Blender version differs from manifest")
    names=set(expected["object_names"])
    objects={name:bpy.data.objects.get(name) for name in names}
    if len(names)!=expected["object_count"]:
        errors.append("Manifest name/count mismatch")
    if any(obj is None for obj in objects.values()):
        errors.append("Missing saved structural objects: "+",".join(n for n,o in objects.items() if o is None))
    actual_structural={o.name for o in bpy.data.objects if o.type=="MESH"}
    if actual_structural!=names:
        errors.append("Saved mesh object name set differs from manifest")
    for name,obj in objects.items():
        if obj is None: continue
        for field in ("historical_state_tag","evidence_class","source_layer","originality_status",
                      "parameter_ids","override_ids","reasonable_completion_ids","bounded_placeholder","topology_type"):
            if field not in obj:
                errors.append(name+": missing metadata "+field)
        if obj.get("originality_status")!="unknown":
            errors.append(name+": originality upgraded")
        if ".001" in name or ".002" in name:
            errors.append(name+": unstable Blender suffix")
        for ident in obj.get("parameter_ids","").split(","):
            if not ident: continue
            if ident=="Z-006-RC-01": continue
            if ident not in inputs.entries or inputs.entries[ident]["geometry_dependency_role"] not in ("DIRECT_GEOMETRY_INPUT","DERIVED_GEOMETRY_RULE"):
                errors.append(name+": non-geometric parameter reference "+ident)
        if name.startswith("BRACKET_") or name.startswith("GABLE_"):
            if not obj.get("bounded_placeholder"):
                errors.append(name+": unresolved topology lacks placeholder tag")
    for record in manifest["objects"]:
        obj=objects.get(record["name"])
        if obj is None: continue
        for field in ("historical_state_tag","evidence_class","source_layer","originality_status",
                      "override_ids","reasonable_completion_ids","bounded_placeholder","topology_type"):
            if obj.get(field)!=record[field]:
                errors.append(record["name"]+": manifest metadata mismatch "+field)
        if obj.get("parameter_ids")!=",".join(record["parameter_ids"]):
            errors.append(record["name"]+": manifest parameter IDs mismatch")
    def endpoint(name,a,b):
        ob=objects.get(name)
        if ob:
            if "endpoint_a_mm" not in ob or "endpoint_b_mm" not in ob:
                errors.append(name+": endpoints missing")
            else:
                point(ob["endpoint_a_mm"],a,name+" A",errors)
                point(ob["endpoint_b_mm"],b,name+" B",errors)
    xs,ys=plan["xs"],plan["ys"]
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            name="COLUMN_X%02d_Y%02d"%(i,j)
            corner=i in (0,3) and j in (0,3)
            perimeter=i in (0,3) or j in (0,3)
            ob=objects.get(name)
            if perimeter and ob:
                height=plan["column_height"]+(plan["corner_rise"] if corner else 0)
                point(ob.location,(x,y,plan["datum_z"]+height/2),name+" center",errors)
                near(ob.dimensions.z,height,name+" height",errors)
                near(ob.dimensions.x,plan["diameter"],name+" diameter",errors)
                if ob.get("override_ids")!="Z-006-RC-01":
                    errors.append(name+": RC trace missing")
            elif perimeter:
                errors.append(name+": perimeter column missing")
            elif ob:
                errors.append(name+": unexpected interior column")
    for j,y in enumerate(ys):
        endpoint("GRID_Y%02d"%j,(xs[0],y,plan["datum_z"]),(xs[-1],y,plan["datum_z"]))
    for i,x in enumerate(xs):
        endpoint("GRID_X%02d"%i,(x,ys[0],plan["datum_z"]),(x,ys[-1],plan["datum_z"]))
    zframe=plan["datum_z"]+plan["column_height"]+plan["lower_ang_rise"]
    for i,x in enumerate(xs):
        endpoint("FRAME_DEPTH_X%02d"%i,(x,ys[0],zframe),(x,ys[-1],zframe))
    for j,y in enumerate(ys):
        endpoint("FRAME_WIDTH_Y%02d"%j,(xs[0],y,zframe),(xs[-1],y,zframe))
    for side in (-1,1):
        for k,distance in enumerate(plan["frame_y"][1:],1):
            y=side*distance;z=plan["frame_tier_z"][k-1]
            endpoint("FRAME_TIER_%s_%02d"%("N" if side<0 else "S",k),(xs[0],y,z),(xs[-1],y,z))
            for i,x in enumerate(xs):
                base="FRAME_POST_%s_%02d_X%02d"%("N" if side<0 else "S",k,i)
                endpoint(base+"_LOW",(x,y,zframe),(x,y,z))
                endpoint(base+"_UP",(x,y,z),(x,y,roof_height_at_y(plan,y)))
    # Exact aggregate projected reach, with individual steps identified as bounded markers.
    for name,ob in objects.items():
        if ob is None or not name.startswith("BRACKET_"): continue
        topology=ob.get("topology_type")
        if topology not in ("head_4_jumps","intercolumn_2_jumps"):
            errors.append(name+": bracket topology type invalid")
        step=int(name.rsplit("J",1)[-1])
        if topology=="intercolumn_2_jumps" and step>2:
            errors.append(name+": intercolumn jump exceeds 2")
        if topology=="head_4_jumps" and step>4:
            errors.append(name+": head jump exceeds 4")
        if "endpoint_a_mm" in ob and "endpoint_b_mm" in ob:
            a,b=ob["endpoint_a_mm"],ob["endpoint_b_mm"]
            projected=((b[0]-a[0])**2+(b[1]-a[1])**2)**0.5
            expected_length=(plan["jump_a"] if step<=2 else plan["jump_b"])/2
            near(projected,expected_length,name+" projected jump",errors)
            expected_rise=plan["lower_ang_rise"]/4 if topology=="head_4_jumps" else 0
            near(b[2]-a[2],expected_rise,name+" jump rise",errors)
    run=plan["roof_sequence"]
    roof_xs=[xs[0]-plan["gable"]]+xs+[xs[-1]+plan["gable"]]
    for side in (-1,1):
        for k,(r,z) in enumerate(zip(run,plan["roof_z"])):
            if k==len(run)-1 and side==1:continue
            y=side*(run[-1]-r)
            endpoint("ROOF_PURLIN_%s_%02d"%("N" if side<0 else "S",k),
                     (roof_xs[0],y,z),(roof_xs[-1],y,z))
        for i,x in enumerate(roof_xs):
            for k in range(len(run)-1):
                endpoint("ROOF_RAFTER_%s_X%02d_S%02d"%("N" if side<0 else "S",i,k),
                         (x,side*(run[-1]-run[k]),plan["roof_z"][k]),
                         (x,side*(run[-1]-run[k+1]),plan["roof_z"][k+1]))
    for side,x in (("W",roof_xs[0]),("E",roof_xs[-1])):
        for sign in (-1,1):
            endpoint("GABLE_%s_%s"%(side,"N" if sign<0 else "S"),
                     (x,sign*run[-1],plan["roof_z"][0]),(x,0,plan["roof_z"][-1]))
    counts={}
    for name,ob in objects.items():
        if ob:
            family=next((c.name.removeprefix("P2_2_") for c in ob.users_collection if c.name.startswith("P2_2_")),None)
            counts[family]=counts.get(family,0)+1
    if counts!=expected["family_counts"]:
        errors.append("Family counts mismatch: "+repr(counts))
    if manifest["approved_override"]["resolved_value_mm"]!=plan["column_height"]:
        errors.append("Manifest RC resolution mismatch")
    if manifest["approved_override"]["historical_Z_006"]!={"classification":"UNKNOWN","value":None,"production_use":"DO_NOT_LOCK","dependency":"BLOCKS_P2_2_GEOMETRY"}:
        errors.append("Manifest historical UNKNOWN boundary mismatch")
    if manifest["output_blend"]["path"]!=str(Path(blend_path).resolve()):
        errors.append("Manifest blend path mismatch")
    if manifest["geometry_input_snapshot"]!=inputs.snapshot():
        errors.append("Manifest geometry-input snapshot mismatch")
    return {"result":"PASS" if not errors else "FAIL","errors":errors,"checked_mesh_objects":len(actual_structural),
            "family_counts":counts,"machine_tolerance_mm":MACHINE_TOLERANCE_MM,
            "column_height_mm":plan["column_height"],"roof_ridge_z_mm":plan["roof_z"][-1]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--blend",required=True)
    parser.add_argument("--manifest",required=True)
    parser.add_argument("--result",type=Path)
    parser.add_argument("--params",type=Path)
    parser.add_argument("--overrides",type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    result=validate(args.blend,args.manifest,args.params,args.overrides)
    if args.result:
        args.result.parent.mkdir(parents=True,exist_ok=True)
        args.result.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("P2_2_GEOMETRY_"+result["result"],json.dumps(result,ensure_ascii=False))
    if result["errors"]:
        raise SystemExit(1)


if __name__=="__main__":main()
