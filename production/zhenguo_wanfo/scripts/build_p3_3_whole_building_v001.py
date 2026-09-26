#!/usr/bin/env python3
"""Build T-018 from an empty Blender scene, or emit its canonical manifest."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

# Blender --python does not promise the script directory on sys.path.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path: sys.path.insert(0, str(SCRIPT_DIR))

from p3_3_whole_building_common_v001 import CANONICAL_PM005, RUNTIME_MANIFEST, compile_runtime, write_json

DISPLAY_LINE_WIDTH_MM = 24.0
REVIEW_GLYPH_RADIUS_MM = 70.0


def representation_spec(record, records):
    """Return review geometry from existing authoritative runtime anchors only."""
    family=record["family"]; ident=record["legacy_instance_id"]; anchor=record["placement"]["location_mm"]
    by_id={x["legacy_instance_id"]:x for x in records}; columns=[x for x in records if x["family"]=="COLUMN"]
    xmin,xmax=min(x["placement"]["location_mm"][0] for x in columns),max(x["placement"]["location_mm"][0] for x in columns)
    ymin,ymax=min(x["placement"]["location_mm"][1] for x in columns),max(x["placement"]["location_mm"][1] for x in columns)
    def point(key): return by_id[key]["placement"]["location_mm"]
    def roof_point(side,tier):
        key=f"ROOF_PURLIN_{side}_{tier:02d}"
        if key in by_id: return point(key),[key]
        mirror=f"ROOF_PURLIN_N_{tier:02d}"
        if side=="S" and mirror in by_id:
            p=point(mirror); return [p[0],ymax-p[1],p[2]],[mirror,"COLUMN_GRID_Y_MIRROR_RULE"]
        raise ValueError(f"missing authoritative roof control for {key}")
    sources=[]; points=[]; kind="LINE"
    if family=="GRID_CONTROL":
        axis=record["placement"]["derivation"]["identity_indices"]["axis"]; points=[[anchor[0],ymin,anchor[2]],[anchor[0],ymax,anchor[2]]] if axis=="X" else [[xmin,anchor[1],anchor[2]],[xmax,anchor[1],anchor[2]]]; sources=[ident,"COLUMN_GRID_BOUNDS"]
    elif family=="BRACKET_CONTACT":
        r=REVIEW_GLYPH_RADIUS_MM; points=[[anchor[0]-r,anchor[1],anchor[2]],[anchor[0]+r,anchor[1],anchor[2]],[anchor[0],anchor[1]-r,anchor[2]],[anchor[0],anchor[1]+r,anchor[2]]]; kind="DISCONNECTED_LINES"; sources=[ident,"REVIEW_GLYPH_RADIUS_MM"]
    elif family=="BRACKET_ARM":
        r=REVIEW_GLYPH_RADIUS_MM; points=[[anchor[0]-r,anchor[1],anchor[2]],[anchor[0],anchor[1]+r,anchor[2]],[anchor[0]+r,anchor[1],anchor[2]],[anchor[0],anchor[1]-r,anchor[2]],[anchor[0]-r,anchor[1],anchor[2]]]; kind="POLYLINE"; sources=[ident,"REVIEW_GLYPH_RADIUS_MM"]
    elif family in {"FRAME_CONTROL","FRAME_SUPPORT"}:
        prefix="SUPPORT_" if family=="FRAME_SUPPORT" else ""; core=ident.removeprefix(prefix)
        post=re.fullmatch(r"FRAME_POST_([NS])_(\d+)_X(\d+)_(LOW|UP)",core)
        if post:
            side,tier,x,_=post.groups(); keys=[f"{prefix}FRAME_POST_{side}_{tier}_X{x}_LOW",f"{prefix}FRAME_POST_{side}_{tier}_X{x}_UP"]
        else:
            tier=re.fullmatch(r"FRAME_TIER_([NS])_(\d+)",core)
            if not tier: raise ValueError(f"no authoritative frame peers for {ident}")
            side,level=tier.groups(); keys=[f"{prefix}FRAME_POST_{side}_{level}_X00_LOW",f"{prefix}FRAME_POST_{side}_{level}_X03_LOW"]
        if any(k not in by_id for k in keys): raise ValueError(f"missing authoritative frame peer for {ident}: {keys}")
        points=[point(k) for k in keys]; sources=keys
    elif family=="PRIMARY_FRAME":
        axis=record["placement"]["derivation"]["identity_indices"]["axis"]; points=[[anchor[0],ymin,anchor[2]],[anchor[0],ymax,anchor[2]]] if axis=="DEPTH_X" else [[xmin,anchor[1],anchor[2]],[xmax,anchor[1],anchor[2]]]; sources=[ident,"COLUMN_GRID_BOUNDS"]
    elif family=="GABLE_CONTROL":
        q=re.fullmatch(r"GABLE_([EW])_([NS])",ident); edge,side=q.groups(); controls=[roof_point(side,i) for i in range(4)]; points=[[anchor[0],p[0][1],p[0][2]] for p in controls]; sources=[s for _,refs in controls for s in refs]
    elif family=="PURLIN":
        points=[[xmin,anchor[1],anchor[2]],[xmax,anchor[1],anchor[2]]]; sources=[ident,"COLUMN_GRID_X_BOUNDS"]
    elif family=="RAFTER":
        q=re.fullmatch(r"ROOF_RAFTER_([NS])_X\d+_S(\d+)",ident); side,seg=q.group(1),int(q.group(2)); controls=[roof_point(side,seg),roof_point(side,seg+1)]; points=[[anchor[0],p[0][1],p[0][2]] for p in controls]; sources=[s for _,refs in controls for s in refs]
    elif family=="ROOF_ENVELOPE":
        q=re.fullmatch(r"ROOF_SURFACE_([NS])_(\d+)",ident); side,seg=q.group(1),int(q.group(2)); ca,cb=roof_point(side,seg),roof_point(side,seg+1); a,b=ca[0],cb[0]; points=[[xmin,a[1],a[2]],[xmax,a[1],a[2]],[xmax,b[1],b[2]],[xmin,b[1],b[2]]]; sources=ca[1]+cb[1]+["COLUMN_GRID_X_BOUNDS"]; kind="SURFACE"
    else: raise ValueError(f"no technical representation renderer for {family}")
    return {"geometry_class":record["representation"]["geometry_class"],"kind":kind,"world_points":points,"endpoint_source_ids":sources,"display_line_width_mm":DISPLAY_LINE_WIDTH_MM}


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
    def technical_geometry(record, material):
        spec=representation_spec(record,manifest["runtime_objects"]); anchor=record["placement"]["location_mm"]
        local=[tuple(float(p[i])-float(anchor[i]) for i in range(3)) for p in spec["world_points"]]
        if spec["kind"]=="SURFACE":
            mesh=bpy.data.meshes.new(record["runtime_instance_id"]+"_REVIEW_SURFACE"); mesh.from_pydata(local,[],[(0,1,2,3)]); mesh.materials.append(material); obj=bpy.data.objects.new(record["runtime_instance_id"],mesh)
        else:
            curve=bpy.data.curves.new(record["runtime_instance_id"]+"_REVIEW_WIRE",'CURVE'); curve.dimensions='3D'; curve.resolution_u=1; curve.bevel_depth=DISPLAY_LINE_WIDTH_MM/2; curve.bevel_resolution=0; curve.materials.append(material)
            groups=[local[i:i+2] for i in range(0,len(local),2)] if spec["kind"]=="DISCONNECTED_LINES" else [local]
            for group in groups:
                spline=curve.splines.new('POLY'); spline.points.add(len(group)-1)
                for p,co in zip(spline.points,group): p.co=(*co,1.0)
            obj=bpy.data.objects.new(record["runtime_instance_id"],curve)
        obj["representation_class"]=record["representation"]["class"]; obj["representation_geometry_class"]=spec["geometry_class"]
        obj["endpoint_source_ids_json"]=json.dumps(spec["endpoint_source_ids"],sort_keys=True); obj["not_evidence_upgraded"]=True
        obj["display_dimensions_policy"]="TECHNICAL_REVIEW_ONLY"; obj["non_historical_geometry"]=True
        obj["TECHNICAL_REVIEW_ONLY"]=True; obj["NON_HISTORICAL_GEOMETRY"]=True; obj["NOT_EVIDENCE_UPGRADED"]=True; return obj
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
            obj = technical_geometry(record, bpy.data.materials[collections[outcome]["material_name"]])
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
