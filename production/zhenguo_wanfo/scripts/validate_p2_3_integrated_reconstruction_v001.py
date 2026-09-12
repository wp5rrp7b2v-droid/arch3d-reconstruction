#!/usr/bin/env python3
"""Independent reopened-file QC for the T-008 integrated candidate."""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
CASE = ROOT / "production/zhenguo_wanfo"
MANIFEST = CASE / "build/P2_3_INTEGRATION_MANIFEST_V001.json"
RESULT = CASE / "validation/P2_3_MACHINE_VALIDATION_V001.json"
TOL = 0.01

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def near(a,b,tol=TOL): return abs(float(a)-float(b))<=tol

def validate(manifest_path, result_path):
    import bpy
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    baseline=json.loads((CASE/"build/P2_2_BUILD_MANIFEST_V001.json").read_text(encoding="utf-8"))
    formal=json.loads((CASE/"params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json").read_text(encoding="utf-8"))
    matrix=json.loads((CASE/"dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json").read_text(encoding="utf-8"))
    errors=[]
    checks={}
    def check(name, condition, detail=""):
        checks[name]=bool(condition)
        if not condition: errors.append(name+(": "+detail if detail else ""))
    blend=ROOT/manifest["output_blend"]["path"]
    check("output_hash",blend.exists() and sha(blend)==manifest["output_blend"]["sha256"])
    for name,entry in manifest["formal_inputs"].items():
        path=ROOT/entry["path"]
        check("formal_input_hash_"+name,path.exists() and sha(path)==entry["sha256"])
    check("baseline_hash",sha(CASE/"output/P2_2_STRUCTURAL_SKELETON_V001.blend")==manifest["p2_2_approved_baseline"]["sha256"])
    check("Z_006_boundary",formal["parameters"]["Z-006"]["value"] is None and formal["parameters"]["Z-006"]["classification"]=="UNKNOWN" and formal["parameters"]["Z-006"]["production_use"]=="DO_NOT_LOCK")
    check("DG_114_boundary",matrix["entries"]["DG-114"]["unknown_dependency_status"]=="BOUNDED_NON_BLOCKING")
    check("HIS_002_boundary",matrix["entries"]["HIS-002"]["geometry_dependency_role"]=="METADATA_ONLY")
    records=manifest["instances"]
    names=[r["instance_id"] for r in records]
    meshes={x.name:x for x in bpy.data.objects if x.type=="MESH"}
    check("stable_ids_unique",len(names)==len(set(names)))
    check("no_blender_name_drift",all(not name.endswith((".001",".002")) for name in names))
    check("instance_set",set(names)==set(meshes))
    check("instance_count",len(names)==manifest["semantic_summary"]["instance_count"])
    counts=Counter(r["family_id"] for r in records)
    check("family_counts",dict(sorted(counts.items()))==manifest["semantic_summary"]["family_counts"])
    check("required_families",{"COLUMN","PRIMARY_FRAME","FRAME_SUPPORT","BRACKET_ARM","BRACKET_CONTACT","PURLIN","RAFTER","ROOF_ENVELOPE"}.issubset(counts))
    check("variant_set",set(r["variant_id"] for r in records)==set(manifest["variants"]))
    check("variant_count",len(manifest["variants"])==manifest["semantic_summary"]["variant_count"])
    mesh_by_variant=defaultdict(set)
    placement_keys=set()
    for r in records:
        ob=meshes.get(r["instance_id"])
        if ob is None: continue
        ident=r["instance_id"]
        for key in ("instance_id","family_id","variant_id","historical_state_tag","time_layer","originality_status","parameter_ids","override_ids","evidence_class","source_layer","bounded_placeholder","presentation"):
            if key not in ob: errors.append("missing_metadata:"+ident+":"+key)
        if ob.get("instance_id")!=ident or ob.get("family_id")!=r["family_id"] or ob.get("variant_id")!=r["variant_id"]:
            errors.append("mapping_mismatch:"+ident)
        if ob.get("originality_status")!="unknown" or ob.get("historical_state_tag")!="reconstructed_963_candidate":
            errors.append("authenticity_boundary:"+ident)
        if set(ob.get("parameter_ids","").split(","))!=set(r["parameter_ids"]): errors.append("parameter_mapping:"+ident)
        if ob.get("override_ids","")!=",".join(r["override_ids"]): errors.append("override_mapping:"+ident)
        if ob.get("bounded_placeholder")!=r["bounded_placeholder"]: errors.append("placeholder_mapping:"+ident)
        if ob.get("presentation")!=r["presentation"]: errors.append("presentation_mapping:"+ident)
        for p in r["parameter_ids"]:
            if p!="Z-006-RC-01" and (p not in formal["parameters"] or matrix["entries"][p]["geometry_dependency_role"] not in ("DIRECT_GEOMETRY_INPUT","DERIVED_GEOMETRY_RULE")):
                errors.append("unapproved_parameter_role:"+ident+":"+p)
        if ob.data is None: errors.append("broken_mesh:"+ident)
        else: mesh_by_variant[r["variant_id"]].add(ob.data.name)
        values=list(ob.location)+list(ob.rotation_euler)+list(ob.scale)
        if not all(math.isfinite(v) for v in values) or any(abs(v)<1e-9 for v in ob.scale): errors.append("invalid_transform:"+ident)
        if any(not near(ob.location[i],r["transform"]["location_mm"][i]) for i in range(3)):
            errors.append("transform_manifest:"+ident)
        key=(r["family_id"],tuple(round(float(x),2) for x in ob.location),tuple(round(float(x),3) for x in ob.rotation_euler))
        if key in placement_keys and r["family_id"] not in ("BRACKET_CONTACT","ROOF_ENVELOPE"):
            errors.append("duplicate_placement:"+ident)
        placement_keys.add(key)
        root_name="P2_3_PRESENTATION" if r["presentation"] else "P2_3_DIAGNOSTIC"
        root=bpy.data.collections.get(root_name)
        if root is None or not any(ob.name in c.objects for c in root.children): errors.append("collection_mapping:"+ident)
    check("shared_prototypes",all(len(names)==1 for names in mesh_by_variant.values()))
    check("prototype_mesh_mapping",all(mesh_by_variant.get(variant)=={spec["mesh_data_name"]} for variant,spec in manifest["variants"].items()))
    check("instance_metadata",not any(e.startswith(("missing_metadata","mapping_mismatch","authenticity_boundary","parameter_mapping","override_mapping","placeholder_mapping","presentation_mapping","unapproved_parameter_role","broken_mesh","invalid_transform","transform_manifest","collection_mapping")) for e in errors))
    check("duplicate_placements",not any(e.startswith("duplicate_placement") for e in errors))
    check("presentation_excludes_diagnostic",all(not r["presentation"] for r in records if r["family_id"] in ("GRID_CONTROL","FRAME_CONTROL","GABLE_CONTROL")))
    key=manifest["semantic_summary"]["key_dimensions_mm"]
    check("P2_2_key_dimensions_regression",key==baseline["semantic_summary"]["key_dimensions_mm"])
    columns=[meshes[r["instance_id"]] for r in records if r["family_id"]=="COLUMN" and r["instance_id"] in meshes]
    check("perimeter_column_count",len(columns)==12 and counts.get("COLUMN")==12)
    # The approved P2.2 structural chain is retained exactly at its named controls.
    baseline_names={r["name"] for r in baseline["objects"]}
    check("P2_2_control_retention",baseline_names.issubset(meshes))
    check("principal_frame_count",counts.get("PRIMARY_FRAME")==8)
    check("frame_support_count",counts.get("FRAME_SUPPORT")==54)
    support_errors=[]
    for name,ob in meshes.items():
        if not name.startswith("SUPPORT_"): continue
        source=meshes.get(name.removeprefix("SUPPORT_"))
        if source is None or any(not near(ob["endpoint_a_mm"][i],source["endpoint_a_mm"][i]) or not near(ob["endpoint_b_mm"][i],source["endpoint_b_mm"][i]) for i in range(3)):
            support_errors.append(name)
    check("frame_to_roof_connector_trace",not support_errors,",".join(support_errors[:5]))
    check("bracket_chain",counts.get("BRACKET_ARM")==88 and counts.get("BRACKET_CONTACT")==88)
    contact_errors=[]
    for name,ob in meshes.items():
        if not name.startswith("CONTACT_"): continue
        arm=meshes.get("BRACKET_"+name.removeprefix("CONTACT_"))
        if arm is None or any(not near(ob.location[i],arm["endpoint_b_mm"][i]) for i in range(3)):
            contact_errors.append(name)
    check("bracket_contact_continuity",not contact_errors,",".join(contact_errors[:5]))
    roof_errors=[]
    for side in ("N","S"):
        for k in range(3):
            ob=meshes.get("ROOF_SURFACE_%s_%02d"%(side,k))
            if ob is None or len(ob.data.vertices)!=4: roof_errors.append("missing_strip_%s_%d"%(side,k)); continue
            if k:
                prev=meshes["ROOF_SURFACE_%s_%02d"%(side,k-1)]
                # Compare the seam by Y/Z rather than mesh vertex order or X.
                seam_prev={(round(v.co.y,2),round(v.co.z,2)) for v in prev.data.vertices}
                seam_here={(round(v.co.y,2),round(v.co.z,2)) for v in ob.data.vertices}
                if not seam_prev.intersection(seam_here): roof_errors.append("open_seam_%s_%d"%(side,k))
    check("roof_surface_continuity",not roof_errors,",".join(roof_errors))
    check("roof_families",counts.get("PURLIN")==7 and counts.get("RAFTER")==36 and counts.get("ROOF_ENVELOPE")==6)
    check("RC_01_not_baked_as_historical",near(manifest["enabled_approved_override"]["resolved_mm"],key["column_height"]) and manifest["enabled_approved_override"]["is_replaceable"] and all(x.get("originality_status")=="unknown" for x in records))
    check("no_unregistered_mesh",set(meshes)==set(names))
    result={"task":"T-008","status":"PASS" if not errors and all(checks.values()) else "FAIL",
            "checks":checks,"errors":sorted(set(errors)),"instance_count":len(records),
            "family_counts":dict(sorted(counts.items())),"variant_count":len(manifest["variants"]),
            "blend_sha256":sha(blend),"blender_version":bpy.app.version_string}
    result_path.parent.mkdir(parents=True,exist_ok=True)
    result_path.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("P2_3_QC_"+result["status"],json.dumps({"checks":len(checks),"errors":result["errors"][:10]},ensure_ascii=False))
    if result["status"]!="PASS": raise ValueError("P2.3 independent QC failed")

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--manifest",type=Path,default=MANIFEST)
    parser.add_argument("--result",type=Path,default=RESULT)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    validate(args.manifest.resolve(),args.result.resolve())
