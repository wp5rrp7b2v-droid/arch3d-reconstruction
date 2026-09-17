#!/usr/bin/env python3
"""Build T-018 from an empty Blender scene, or emit its canonical manifest."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

# Blender --python does not promise the script directory on sys.path.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path: sys.path.insert(0, str(SCRIPT_DIR))

from p3_3_whole_building_common_v001 import CANONICAL_PM005, RUNTIME_MANIFEST, compile_runtime, write_json


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument("--pm005", type=float, default=CANONICAL_PM005)
    p.add_argument("--manifest", type=Path, default=RUNTIME_MANIFEST)
    p.add_argument("--snapshot", type=Path)
    p.add_argument("--blend", type=Path)
    p.add_argument("--manifest-only", action="store_true")
    return p.parse_args(argv)


def build_blender(manifest, blend_path: Path):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"
    collections = {}
    colors = {
        "GENERATED_FORMAL_GEOMETRY": (0.33, 0.12, 0.04, 1), "GENERATED_PROXY": (0.8, 0.55, 0.12, 1),
        "GENERATED_CONTROL": (0.1, 0.35, 0.8, 1), "GENERATED_ENVELOPE": (0.1, 0.65, 0.55, 1), "UNKNOWN_BLOCKED": (0.75, 0.05, 0.15, 1),
        "DEFERRED": (0.35, 0.35, 0.35, 1), "SEMANTIC_ONLY": (0.55, 0.55, 0.55, 1), "COMPARISON_ONLY": (0.2, 0.2, 0.2, 1),
    }
    for outcome, color in colors.items():
        col = bpy.data.collections.new(outcome); bpy.context.scene.collection.children.link(col); collections[outcome] = col
        mat = bpy.data.materials.new(f"MAT_{outcome}"); mat.diffuse_color = color; mat["technical_role"] = "EVIDENCE_CLASSIFICATION"
        collections[outcome]["material_name"] = mat.name
    loaded_generators = {}
    def technical_mesh(record, material):
        """Visible review-only octahedron; its size is never a historical dimension."""
        size=float(record["representation"]["marker_geometry"]["display_radius_mm"])
        verts=[(size,0,0),(-size,0,0),(0,size,0),(0,-size,0),(0,0,size),(0,0,-size)]
        faces=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
        mesh=bpy.data.meshes.new(record["runtime_instance_id"]+"_TECHNICAL_MESH"); mesh.from_pydata(verts,[],faces); mesh.materials.append(material)
        obj=bpy.data.objects.new(record["runtime_instance_id"],mesh); obj["representation_class"]=record["representation"]["class"]
        obj["display_dimensions_policy"]="TECHNICAL_REVIEW_ONLY"; obj["non_historical_geometry"]=True; return obj
    for record in manifest["runtime_objects"]:
        outcome = record["p3_3_disposition"]
        if outcome == "GENERATED_FORMAL_GEOMETRY":
            master = record["formal_master"]
            generator_path = Path(master["generator_path"])
            params_path = Path(master["parameter_path"])
            key = str(generator_path)
            if key not in loaded_generators:
                spec = importlib.util.spec_from_file_location("t018_approved_master_generator", generator_path)
                module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); loaded_generators[key] = module
            module = loaded_generators[key]
            data = json.loads(params_path.read_text(encoding="utf-8")); _, diameter, height = module.resolve(data)
            collections_before = set(bpy.data.collections)
            obj = module.build_mesh(diameter, height)
            for c in list(obj.users_collection): c.objects.unlink(obj)
            collections[outcome].objects.link(obj)
            for temporary in set(bpy.data.collections) - collections_before:
                if not temporary.objects: bpy.data.collections.remove(temporary)
            obj.data.materials.append(bpy.data.materials[collections[outcome]["material_name"]])
            obj["formal_geometry_source"] = key
            obj["formal_geometry_mode"] = master["geometry_mode"]
        else:
            obj = technical_mesh(record, bpy.data.materials[collections[outcome]["material_name"]])
            collections[outcome].objects.link(obj)
        if record["placement"]["status"] == "RULE_DERIVED":
            obj.location = record["placement"]["location_mm"]
            obj.rotation_euler = record["placement"]["rotation_euler_rad"]
            obj.scale = record["placement"]["scale"]
        obj.name = record["runtime_instance_id"]
        for key in ("runtime_instance_id", "legacy_instance_id", "component_id", "family", "graph_parent_node_id", "p3_3_disposition", "historical_claim_boundary"):
            obj[key] = record[key]
        obj["evidence_status_json"] = json.dumps(record["evidence_status"], sort_keys=True)
        obj["parameter_rule_provenance_json"] = json.dumps(record["parameter_rule_provenance"], sort_keys=True)
        obj["placement_status"] = record["placement"]["status"]
        obj["datum_type"] = record["placement"]["datum_type"]
        obj["representation_json"] = json.dumps(record["representation"], sort_keys=True)
    bpy.context.scene["t018_manifest_json"] = json.dumps(manifest, ensure_ascii=False, sort_keys=True)
    bpy.context.scene["clean_state_generation"] = True
    blend_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path.resolve()))


def main():
    args = parse_args(); manifest = compile_runtime(args.pm005); write_json(args.manifest, manifest)
    if args.snapshot: write_json(args.snapshot, {"snapshot_sha256": manifest["canonical_semantic_snapshot_sha256"], "normalized": {"parameter_state": manifest["parameter_state"], "runtime_objects": manifest["runtime_objects"]}})
    if not args.manifest_only:
        if not args.blend: raise SystemExit("--blend is required for Blender generation")
        build_blender(manifest, args.blend)
    print(json.dumps({"status": "PASS", "objects": len(manifest["runtime_objects"]), "snapshot": manifest["canonical_semantic_snapshot_sha256"]}))


if __name__ == "__main__": main()
