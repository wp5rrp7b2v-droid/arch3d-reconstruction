#!/usr/bin/env python3
"""Build T-018 from an empty Blender scene, or emit its canonical manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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
    collections = {}
    colors = {
        "GENERATED_FORMAL_GEOMETRY": (0.33, 0.12, 0.04, 1), "GENERATED_PROXY": (0.8, 0.55, 0.12, 1),
        "GENERATED_CONTROL": (0.1, 0.35, 0.8, 1), "GENERATED_ENVELOPE": (0.1, 0.65, 0.55, 1), "UNKNOWN_BLOCKED": (0.75, 0.05, 0.15, 1),
    }
    for outcome, color in colors.items():
        col = bpy.data.collections.new(outcome); bpy.context.scene.collection.children.link(col); collections[outcome] = col
        mat = bpy.data.materials.new(f"MAT_{outcome}"); mat.diffuse_color = color; mat["technical_role"] = "EVIDENCE_CLASSIFICATION"
        collections[outcome]["material_name"] = mat.name
    for record in manifest["runtime_objects"]:
        outcome = record["p3_3_disposition"]
        if outcome == "UNKNOWN_BLOCKED":
            obj = bpy.data.objects.new(record["runtime_instance_id"], None)
            obj.empty_display_type = 'CUBE'; obj.empty_display_size = 0.18
            collections[outcome].objects.link(obj)
            obj.location = record["placement"]["location_m"]
        else:
            bpy.ops.mesh.primitive_cube_add(size=1, location=record["placement"]["location_m"])
            obj = bpy.context.object
            for c in list(obj.users_collection): c.objects.unlink(obj)
            collections[outcome].objects.link(obj)
            obj.scale = (0.13, 0.13, 1.4 if record["source_family_id"] == "COLUMN" else 0.13)
            obj.data.materials.append(bpy.data.materials[collections[outcome]["material_name"]])
        obj.name = record["runtime_instance_id"]
        for key in ("runtime_instance_id", "legacy_instance_id", "component_id", "graph_parent_node_id", "p3_3_disposition", "historical_claim_boundary"):
            obj[key] = record[key]
        obj["evidence_status_json"] = json.dumps(record["evidence_status"], sort_keys=True)
        obj["parameter_rule_provenance_json"] = json.dumps(record["parameter_rule_provenance"], sort_keys=True)
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
