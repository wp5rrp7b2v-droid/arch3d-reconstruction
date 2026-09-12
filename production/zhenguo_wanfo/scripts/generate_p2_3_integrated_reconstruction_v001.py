#!/usr/bin/env python3
"""T-008: integrate the approved P2.2 skeleton with a traceable component system.

All coordinates are mm. New forms are diagrammatic and derived from approved
control geometry; they do not establish missing historical member dimensions.
Run with Blender 3.6: blender -b --factory-startup --python THIS_FILE [-- args].
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
CASE = ROOT / "production/zhenguo_wanfo"
BASE = CASE / "output/P2_2_STRUCTURAL_SKELETON_V001.blend"
BASE_MANIFEST = CASE / "build/P2_2_BUILD_MANIFEST_V001.json"
LIBRARY = CASE / "components/P2_3_COMPONENT_LIBRARY_V001.json"
ROUNDTRIP_SCRIPT = CASE / "scripts/p2_3_roundtrip_semantic_qc_v001.py"
ROUNDTRIP_WORKFLOW = ROOT / ".github/workflows/p2_3_integrated_roundtrip.yml"
OUTPUT = CASE / "output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend"
MANIFEST = CASE / "build/P2_3_INTEGRATION_MANIFEST_V001.json"
REVIEW = CASE / "review"
P2_SCRIPT = CASE / "scripts/generate_p2_2_structural_skeleton_v001.py"
PREFIX = "P2_3_INTEGRATED_RECONSTRUCTION_V001"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def vec(values):
    return [round(float(x), 5) for x in values]


def load_p2():
    spec = importlib.util.spec_from_file_location("p2_2_approved", P2_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(args):
    import bpy
    from mathutils import Vector
    p2 = load_p2()
    baseline = read(BASE_MANIFEST)
    if sha(BASE) != baseline["output_blend"]["sha256"]:
        raise ValueError("Approved P2.2 local baseline hash mismatch")
    if sha(P2_SCRIPT) != baseline["generation_script"]["sha256"]:
        raise ValueError("Approved P2.2 generator hash mismatch")
    inputs = p2.FormalInputs(args.params or p2.PARAMS, args.overrides or p2.OVERRIDES, p2.MATRIX)
    plan = p2.geometry_plan(inputs)
    library_path = args.library or LIBRARY
    library = read(library_path)
    # Rebuild the approved P2.2 rule set from clean formal inputs. The approved
    # saved baseline is hash-checked above and used as the regression reference;
    # regeneration is what lets RC and variant replacements propagate.
    p2_records, p2_counters = p2.create_model(inputs, plan)
    p2_summary = p2.semantic_summary(plan, p2_records, p2_counters, inputs)
    scene = bpy.context.scene
    scene.render.filepath = ""
    for ob in list(bpy.data.objects):
        if ob.type == "CAMERA":
            bpy.data.objects.remove(ob, do_unlink=True)
    pres = bpy.data.collections.new("P2_3_PRESENTATION")
    diag = bpy.data.collections.new("P2_3_DIAGNOSTIC")
    scene.collection.children.link(pres)
    scene.collection.children.link(diag)
    families = {}
    def collection(family, presentation):
        key = (family, presentation)
        if key not in families:
            c = bpy.data.collections.new("P2_3_" + family)
            (pres if presentation else diag).children.link(c)
            families[key] = c
        return families[key]
    # Explicitly remove the old P2.2 collection structure after relinking.
    variant_meshes = {}
    variants = {}
    instances = []
    colors = {
        "COLUMN": (0.46, 0.25, 0.11, 1), "PRIMARY_FRAME": (0.27, 0.36, 0.47, 1),
        "BRACKET_ARM": (0.63, 0.31, 0.09, 1), "BRACKET_CONTACT": (0.78, 0.48, 0.14, 1),
        "PURLIN": (0.18, 0.37, 0.38, 1), "RAFTER": (0.28, 0.49, 0.46, 1),
        "ROOF_ENVELOPE": (0.34, 0.49, 0.49, 1), "FRAME_CONTROL": (0.47, 0.32, 0.60, 1),
        "GRID_CONTROL": (0.3, 0.3, 0.3, 1), "GABLE_CONTROL": (0.5, 0.28, 0.55, 1),
        "FRAME_SUPPORT": (0.48, 0.42, 0.56, 1)
    }
    def register(ob, family, ids, variant_parameters, presentation, placeholder=False):
        if family not in library["component_families"]:
            raise ValueError("Undeclared family " + family)
        if any(x not in inputs.parameters and x != "Z-006-RC-01" for x in ids):
            raise ValueError("Undeclared parameter ID")
        key = {"family": family, "generator_parameters": variant_parameters}
        variant_id = family + "_V" + hashlib.sha256(canonical(key).encode()).hexdigest()[:12].upper()
        for c in tuple(ob.users_collection):
            c.objects.unlink(ob)
        collection(family, presentation).objects.link(ob)
        ob["instance_id"] = ob.name
        ob["family_id"] = family
        ob["variant_id"] = variant_id
        ob["historical_state_tag"] = "reconstructed_963_candidate"
        ob["time_layer"] = "reconstructed_963_candidate"
        ob["originality_status"] = "unknown"
        ob["parameter_ids"] = ",".join(ids)
        ob["override_ids"] = "Z-006-RC-01" if "Z-006-RC-01" in ids else ""
        sources = [inputs.parameters[x] for x in ids if x in inputs.parameters]
        ob["evidence_class"] = "+".join(sorted({x["classification"] for x in sources})) or "REASONABLE_COMPLETION"
        ob["source_layer"] = "+".join(sorted({x["source_layer"] for x in sources})) or "D-023_APPROVED_OVERRIDE"
        ob["bounded_placeholder"] = bool(placeholder)
        ob["presentation"] = bool(presentation)
        ob.color = colors[family]
        if variant_id in variant_meshes:
            ob.data = variant_meshes[variant_id]
        else:
            ob.data.name = "MESH_" + variant_id
            variant_meshes[variant_id] = ob.data
        if variant_id not in variants:
            variants[variant_id] = {"family_id": family, "generator_parameters": variant_parameters,
                                    "mesh_data_name": ob.data.name, "parameter_ids": ids,
                                    "explicit_unique": False}
        rec = {"instance_id": ob.name, "family_id": family, "variant_id": variant_id,
               "transform": {"location_mm": vec(ob.location), "rotation_euler_rad": vec(ob.rotation_euler),
                             "scale": vec(ob.scale)},
               "parameter_ids": ids, "override_ids": ["Z-006-RC-01"] if "Z-006-RC-01" in ids else [],
               "historical_state_tag": ob["historical_state_tag"], "time_layer": ob["time_layer"],
               "evidence_class": ob["evidence_class"], "source_layer": ob["source_layer"],
               "originality_status": "unknown", "bounded_placeholder": bool(placeholder),
               "presentation": bool(presentation)}
        instances.append(rec)
        return rec
    def dims(ob):
        # Mesh-local extents define a shareable prototype. World-space bounding
        # boxes differ with rotation and cannot safely identify a beam variant.
        return [round(max(v.co[i] for v in ob.data.vertices)-min(v.co[i] for v in ob.data.vertices),5) for i in range(3)]
    baseline_records = {r["name"]: r for r in baseline["objects"]}
    for name in sorted(baseline_records):
        ob = bpy.data.objects.get(name)
        if ob is None or ob.type != "MESH":
            raise ValueError("Missing baseline mesh " + name)
        record = baseline_records[name]
        old_family = record["family"]
        if old_family == "COLUMN": family, show = "COLUMN", True
        elif old_family == "GRID": family, show = "GRID_CONTROL", False
        elif old_family == "GABLE": family, show = "GABLE_CONTROL", False
        elif old_family == "BRACKET": family, show = "BRACKET_ARM", True
        elif old_family == "ROOF": family, show = ("PURLIN" if name.startswith("ROOF_PURLIN") else "RAFTER"), True
        elif old_family == "FRAME":
            family, show = ("PRIMARY_FRAME", True) if name.startswith(("FRAME_DEPTH", "FRAME_WIDTH")) else ("FRAME_CONTROL", False)
        else: raise ValueError("Unknown baseline family")
        ids = list(dict.fromkeys(record["parameter_ids"]))
        parameters = {"source_role": record.get("topology_type", ""), "shape": "cylinder" if family == "COLUMN" else "beam",
                      "dimensions_mm": dims(ob)}
        register(ob, family, ids, parameters, show, record["bounded_placeholder"] or family in ("BRACKET_ARM", "RAFTER", "GABLE_CONTROL", "FRAME_CONTROL"))
    # These are new, explicitly bounded P2.3 connector instances. The original
    # P2.2 frame controls stay diagnostic; no control object is presented as an
    # authenticated historical component.
    for source in sorted((x for x in bpy.data.objects if x.name.startswith(("FRAME_TIER_","FRAME_POST_")) and x.type=="MESH"),key=lambda x:x.name):
        rec=baseline_records[source.name]
        ob=source.copy()
        ob.data=source.data.copy()
        ob.name="SUPPORT_"+source.name
        scene.collection.objects.link(ob)
        register(ob,"FRAME_SUPPORT",list(dict.fromkeys(rec["parameter_ids"])),
                 {"source_role":rec.get("topology_type",""),"shape":"diagrammatic_connector","dimensions_mm":dims(ob)},True,True)
    # Contact blocks are graphic topology markers at approved bracket-arm endpoints.
    # Their envelope is derived solely from the P2.2 module section, never DG-114.
    width, depth, height = plan["section_width"], plan["section_depth"], plan["section_height"]
    contact_ids = ["DG-001", "DG-002", "DG-110", "DG-111", "MOD-002", "MOD-003", "MOD-004", "MOD-005", "Z-006-RC-01"]
    contact_fraction = float(library["graphic_only_rules"]["contact_block_fraction"])
    if not 0 < contact_fraction <= 1:
        raise ValueError("Diagrammatic contact fraction must be in (0,1]")
    contact_dims = (width * contact_fraction, depth * contact_fraction, height * contact_fraction)
    def box_mesh(name, dimensions):
        x, y, z = (d / 2 for d in dimensions)
        verts = [(a*x,b*y,c*z) for a,b,c in ((-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1))]
        faces = [(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        return mesh
    for arm in sorted((x for x in bpy.data.objects if x.name.startswith("BRACKET_") and x.type == "MESH"), key=lambda x:x.name):
        endpoint = list(arm["endpoint_b_mm"])
        ob = bpy.data.objects.new("CONTACT_" + arm.name.removeprefix("BRACKET_"), box_mesh("CONTACT_TMP", contact_dims))
        scene.collection.objects.link(ob)
        ob.location = endpoint
        register(ob, "BRACKET_CONTACT", contact_ids,
                 {"shape": "diagrammatic_contact", "dimensions_mm": vec(contact_dims), "source_role": "arm_endpoint"}, True, True)
    # Piecewise planar strips span the approved P2.2 eave-to-ridge controls.
    roof_x = [plan["xs"][0]-plan["gable"], plan["xs"][-1]+plan["gable"]]
    roof_y = [plan["roof_sequence"][-1]-r for r in plan["roof_sequence"]]
    roof_ids = ["FR-007","ROOF-007","ROOF-008","ROOF-009","ROOF-010","ROOF-011","OUT-003","Z-006-RC-01","MOD-002"]
    for side in (-1, 1):
        for k in range(3):
            y0, y1 = side*roof_y[k], side*roof_y[k+1]
            z0, z1 = plan["roof_z"][k:k+2]
            points = [(roof_x[0],y0,z0),(roof_x[1],y0,z0),(roof_x[1],y1,z1),(roof_x[0],y1,z1)]
            mesh = bpy.data.meshes.new("ROOF_SURFACE_TMP")
            mesh.from_pydata(points, [], [(0,1,2,3)])
            mesh.update()
            ob = bpy.data.objects.new("ROOF_SURFACE_%s_%02d" % ("N" if side<0 else "S", k), mesh)
            scene.collection.objects.link(ob)
            register(ob, "ROOF_ENVELOPE", roof_ids,
                     {"shape":"zero_thickness_strip", "side": "N" if side<0 else "S", "interval": k,
                      "run_mm": round(abs(y0-y1),5), "rise_mm": round(z1-z0,5),
                      "span_mm": round(roof_x[1]-roof_x[0],5)}, True, True)
    for c in list(bpy.data.collections):
        if c.name.startswith("P2_2_"):
            bpy.data.collections.remove(c)
    bpy.context.view_layer.update()
    ids = [x["instance_id"] for x in instances]
    if len(ids) != len(set(ids)) or any(name.endswith((".001", ".002")) for name in ids):
        raise ValueError("Duplicate or drifting instance ID")
    counts = dict(sorted(Counter(x["family_id"] for x in instances).items()))
    summary = {"instance_ids": sorted(ids), "instance_count": len(instances),
               "family_counts": counts, "variant_ids": sorted(variants), "variant_count": len(variants),
               "mapping": {x["instance_id"]: x["variant_id"] for x in instances},
               "metadata_counts": [{"evidence_class": a, "originality_status": b, "presentation": c, "count": n}
                                   for (a,b,c),n in sorted(Counter((x["evidence_class"],x["originality_status"],x["presentation"]) for x in instances).items())],
               "key_dimensions_mm": p2_summary["key_dimensions_mm"],
               "historical_Z_006": {"classification":"UNKNOWN", "value":None, "production_use":"DO_NOT_LOCK"},
               "candidate_RC_01_mm": plan["column_height"]}
    review_paths = [] if args.no_review else render_reviews(scene, plan, args.review_dir or REVIEW, PREFIX)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output))
    commit = subprocess.run(["git","rev-parse","HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    input_paths = {"formal_parameter_set": inputs.paths["formal_parameter_set"], "approved_overrides": inputs.paths["approved_overrides"],
                   "geometry_dependency_matrix": p2.MATRIX, "evidence_schema": p2.SCHEMA}
    manifest = {"task":"T-008", "version":"V001", "source_commit": commit,
       "formal_inputs": {key:{"path":str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path), "sha256":sha(path)} for key,path in input_paths.items()},
       "p2_2_approved_baseline": {"path":str(BASE.relative_to(ROOT)), "sha256":sha(BASE), "size_bytes":BASE.stat().st_size,
                                  "build_manifest_path":str(BASE_MANIFEST.relative_to(ROOT)), "build_manifest_sha256":sha(BASE_MANIFEST),
                                  "generation_script_path":str(P2_SCRIPT.relative_to(ROOT)), "generation_script_sha256":sha(P2_SCRIPT),
                                  "canonical_commit":baseline["generation_script"]["source_commit"]},
       "p2_3_scripts": {"generator":{"path":str(HERE.relative_to(ROOT)),"sha256":sha(HERE)},
                        "component_library":{"path":str(library_path.relative_to(ROOT)) if library_path.is_relative_to(ROOT) else str(library_path),"sha256":sha(library_path)},
                        "roundtrip_validator":{"path":str(ROUNDTRIP_SCRIPT.relative_to(ROOT)),"sha256":sha(ROUNDTRIP_SCRIPT)},
                        "roundtrip_workflow":{"path":str(ROUNDTRIP_WORKFLOW.relative_to(ROOT)),"sha256":sha(ROUNDTRIP_WORKFLOW)}},
       "environment":{"blender_version":bpy.app.version_string,"python_version":sys.version.split()[0]},
       "component_families":library["component_families"], "variants":variants,
       "instances":sorted(instances,key=lambda x:x["instance_id"]), "semantic_summary":summary,
       "used_parameter_ids":sorted(inputs.used), "derived_rules":inputs.rules,
       "enabled_approved_override":{"id":"Z-006-RC-01","formula":inputs.sidecar["overrides"]["Z-006-RC-01"]["formula"],
                                    "is_replaceable":True,"approval_decision_id":"D-023","resolved_mm":plan["column_height"]},
       "bounded_unknowns":["Z-006 historical column height remains UNKNOWN / null / DO_NOT_LOCK", "DG-114 is not a unified small-dou specification", "HIS-002 component originality unknown", "45-degree joints, mortises and hidden-angle beam unresolved"],
       "collection_mapping":{"presentation":"P2_3_PRESENTATION", "diagnostic":"P2_3_DIAGNOSTIC"},
       "output_blend":{"path":str(args.output.relative_to(ROOT)) if args.output.is_relative_to(ROOT) else str(args.output),
                       "sha256":sha(args.output),"size_bytes":args.output.stat().st_size},
       "review_images":[{"path":str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),"sha256":sha(p)} for p in review_paths],
       "roundtrip":{"status":"PENDING", "artifact_path":None, "validation_path":None}}
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("P2_3_BUILD_OK",canonical({"instances":len(instances),"variants":len(variants),"families":counts,"blend_sha256":sha(args.output)}))


def render_reviews(scene, plan, directory, prefix):
    import bpy
    from mathutils import Vector
    directory.mkdir(parents=True, exist_ok=True)
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "P2_3_REVIEW_CAMERA"
    camera.data.type = "ORTHO"
    camera.data.clip_end = 1000000
    scene.camera = camera
    roof = bpy.data.collections["P2_3_ROOF_ENVELOPE"]
    diagnostic = bpy.data.collections["P2_3_DIAGNOSTIC"]
    zmid = plan["roof_z"][-1]/2
    w = plan["width"]+2*plan["gable"]
    d = 2*plan["roof_sequence"][-1]
    views = {
      "PLAN": ((0,0,30000),(0,0,0),max(w,d*1.4)*1.18,False,False),
      "ELEVATION": ((30000,0,zmid),(0,0,zmid),max(d,plan["roof_z"][-1]*1.4)*1.2,False,False),
      "AXON": ((23000,-26000,20000),(0,0,zmid),max(w,d)*1.7,False,False),
      "EXTERIOR_3Q": ((20000,-24000,12500),(0,0,zmid),max(w,d)*1.58,False,False),
      "STRUCTURE_DETAIL": ((7500,-7800,1500),(3500,-4300,4200),max(w,d)*0.65,True,False),
      "EVIDENCE_DIAGNOSTIC": ((22000,-24000,18000),(0,0,zmid),max(w,d)*1.7,False,True)
    }
    paths=[]
    for label,(position,target,scale,hide_roof,show_diag) in views.items():
        roof.hide_render = hide_roof
        diagnostic.hide_render = not show_diag
        camera.location = position
        camera.rotation_euler = (Vector(target)-camera.location).to_track_quat("-Z","Y").to_euler()
        camera.data.ortho_scale = scale
        if show_diag:
            for ob in bpy.data.objects:
                if ob.type == "MESH":
                    ob.color = (0.20,0.56,0.20,1) if ob["evidence_class"] == "CONFIRMED" else (0.86,0.55,0.13,1) if not ob["bounded_placeholder"] else (0.75,0.23,0.34,1)
        path = directory / (prefix+"_"+label+".png")
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        paths.append(path)
    roof.hide_render=False
    diagnostic.hide_render=True
    camera.hide_render=True
    return paths


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=OUTPUT)
    parser.add_argument("--manifest",type=Path,default=MANIFEST)
    parser.add_argument("--summary",type=Path)
    parser.add_argument("--review-dir",type=Path)
    parser.add_argument("--no-review",action="store_true")
    parser.add_argument("--params",type=Path)
    parser.add_argument("--overrides",type=Path)
    parser.add_argument("--library",type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    args.output=args.output.resolve()
    args.manifest=args.manifest.resolve()
    build(args)

if __name__=="__main__": main()
