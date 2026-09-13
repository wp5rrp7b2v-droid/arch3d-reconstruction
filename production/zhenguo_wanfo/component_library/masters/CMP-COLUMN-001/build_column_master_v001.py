"""Build the evidence-bounded CMP-COLUMN-001 body in Blender 3.6.23.

Usage: blender --background --python this_file -- --params FILE --asset FILE
       --semantic FILE [--review-dir DIR]
All historical dimensions are resolved from the parameter JSON, never from code.
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


GENERATOR_VERSION = "V001"
BODY_NAME = "MASTER__CMP_COLUMN_001__BODY"
COLLECTION_NAME = "MASTER__CMP_COLUMN_001"
SIDES = 128  # Resolution only; this is not a historical dimension.
REPO_ROOT = Path(__file__).resolve().parents[5]


def args_from_blender():
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", required=True)
    parser.add_argument("--asset", required=True)
    parser.add_argument("--semantic", required=True)
    parser.add_argument("--review-dir")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def display_path(path):
    path = Path(path).resolve()
    return str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path)


def resolve(data):
    assert data["component_id"] == "CMP-COLUMN-001"
    assert data["master_version"] == "V001"
    assert data["unit"] == "mm"
    assert data["geometry_mode"] == "PARAMETRIC_CIRCULAR_COLUMN_BODY"
    assert data["origin_convention"] == "column_body_bottom_face_center"
    assert data["canonical_transform"] == {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}
    params = {item["key"]: item for item in data["parameters"]}
    assert len(params) == len(data["parameters"])
    for key in ("diameter_mm", "height_mm", "diameter_source_mode", "height_source_mode", "historical_height_Z006_mm"):
        assert key in params, key
    unknown = params["historical_height_Z006_mm"]
    assert unknown["value"] is None and unknown["classification"] == "UNKNOWN" and unknown["production_use"] == "DO_NOT_LOCK"
    assert data["originality_status"] == "unknown"
    assert data["unsupported_geometry"] == []
    diameter = float(params["diameter_mm"]["value"])
    height = float(params["height_mm"]["value"])
    assert math.isfinite(diameter) and diameter > 0
    assert math.isfinite(height) and height > 0
    assert params["diameter_source_mode"]["value"] == "OBSERVED_Z001"
    height_mode = params["height_source_mode"]["value"]
    if height_mode == "RC_Z006_RC_01":
        candidate = data["height_candidate"]
        assert candidate["candidate_id"] == "Z-006-RC-01" and candidate["replaceable"] is True
        assert candidate["classification"] == "REASONABLE_COMPLETION" and candidate["approval_decision_id"] == "D-023"
        assert candidate["formula"] == "11 * MOD-006"
        assert math.isclose(height, float(candidate["multiplier"]) * float(candidate["resolved_mod_006_mm"]), abs_tol=1e-6)
        assert math.isclose(height, float(candidate["current_resolved_value_mm"]), abs_tol=1e-6)
        assert params["height_mm"]["classification"] == "REASONABLE_COMPLETION"
    else:
        assert height_mode == "ENGINEERING_TEST_ONLY"
        assert params["height_mm"]["classification"] == "ENGINEERING_TEST_ONLY"
        assert params["height_mm"]["production_use"] == "MUTATION_TEST_ONLY"
    return params, diameter, height


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)


def build_mesh(diameter, height):
    radius = diameter / 2.0
    vertices = []
    for z in (0.0, height):
        for i in range(SIDES):
            angle = 2.0 * math.pi * i / SIDES
            vertices.append((radius * math.cos(angle), radius * math.sin(angle), z))
    faces = [tuple(reversed(range(SIDES)))]
    faces += [(i, (i + 1) % SIDES, SIDES + (i + 1) % SIDES, SIDES + i) for i in range(SIDES)]
    faces.append(tuple(range(SIDES, 2 * SIDES)))
    mesh = bpy.data.meshes.new(BODY_NAME + "__MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)
    body = bpy.data.objects.new(BODY_NAME, mesh)
    collection.objects.link(body)
    body.location = (0.0, 0.0, 0.0)
    body.rotation_euler = (0.0, 0.0, 0.0)
    body.scale = (1.0, 1.0, 1.0)
    body["component_id"] = "CMP-COLUMN-001"
    body["master_version"] = "V001"
    body["geometry_mode"] = "PARAMETRIC_CIRCULAR_COLUMN_BODY"
    body["unit"] = "mm"
    return body


def semantic_payload(data, params, body, params_path, asset_path):
    verts = [tuple(round(float(v.co[i]), 5) for i in range(3)) for v in body.data.vertices]
    faces = [tuple(p.vertices) for p in body.data.polygons]
    geometry_signature = hashlib.sha256(canonical_json({"vertices": verts, "faces": faces}).encode()).hexdigest()
    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]
    return {
        "component_id": data["component_id"],
        "master_id": data["master_id"],
        "master_version": data["master_version"],
        "unit": "mm",
        "collection_names": [COLLECTION_NAME],
        "object_names": [BODY_NAME],
        "object_count": 1,
        "mesh_count": 1,
        "non_mesh_auxiliary_objects": [],
        "body": {
            "name": BODY_NAME,
            "vertex_count": len(verts),
            "face_count": len(faces),
            "local_transform": {
                "location": [float(x) for x in body.location],
                "rotation": [float(x) for x in body.rotation_euler],
                "scale": [float(x) for x in body.scale],
            },
            "local_bbox_mm": {"min": mins, "max": maxs, "dimensions": [round(maxs[i] - mins[i], 5) for i in range(3)]},
            "primitive": "closed_constant_radius_circular_column_body",
            "unsupported_column_geometry_count": 0,
        },
        "resolved_parameters": {key: item["value"] for key, item in sorted(params.items())},
        "evidence_classes": {key: item["classification"] for key, item in sorted(params.items())},
        "geometry_mode": data["geometry_mode"],
        "geometry_lod": data["geometry_lod"],
        "known_unknowns": data["known_unknowns"],
        "originality_status": data["originality_status"],
        "historical_state": data["historical_state"],
        "generator_version": GENERATOR_VERSION,
        "input_hashes": {display_path(params_path): sha256(params_path), "generator": sha256(__file__)},
        "blender_version": bpy.app.version_string,
        "canonical_asset_path": display_path(asset_path),
        "canonical_blend_sha256": sha256(asset_path),
        "semantic_geometry_signature": geometry_signature,
    }


def render_views(body, diameter, height, review_dir):
    review_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 32
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    scene.render.resolution_x = 900
    scene.render.resolution_y = 1200
    scene.world.use_nodes = True
    background = next(node for node in scene.world.node_tree.nodes if node.type == "BACKGROUND")
    background.inputs["Color"].default_value = (0.84, 0.84, 0.84, 1)
    background.inputs["Strength"].default_value = 1.0
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    for label, grey in (("SIDE", 0.52), ("TOP", 0.68), ("BOTTOM", 0.40)):
        material = bpy.data.materials.new("REVIEW_NEUTRAL_GREY_" + label + "_TEMPORARY")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        emission = nodes.new("ShaderNodeEmission")
        emission.inputs["Color"].default_value = (grey, grey, grey, 1)
        output = nodes.new("ShaderNodeOutputMaterial")
        material.node_tree.links.new(emission.outputs[0], output.inputs["Surface"])
        body.data.materials.append(material)
    for polygon in body.data.polygons:
        polygon.material_index = 2 if polygon.index == 0 else (1 if polygon.index == len(body.data.polygons) - 1 else 0)
    camera_data = bpy.data.cameras.new("REVIEW_CAMERA_TEMPORARY")
    camera = bpy.data.objects.new("REVIEW_CAMERA_TEMPORARY", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera_data.type = "ORTHO"
    camera_data.clip_end = height * 10.0
    target = Vector((0, 0, height / 2))
    views = {
        "FRONT": ((0, -height * 1.5, height / 2), height * 1.18, (900, 1200)),
        "SIDE": ((height * 1.5, 0, height / 2), height * 1.18, (900, 1200)),
        "TOP": ((0, 0, height * 1.5), diameter * 1.65, (900, 900)),
        "AXON": ((height * 0.9, -height * 1.2, height * 0.9), height * 1.46, (900, 1200)),
    }
    for name, (position, scale, resolution) in views.items():
        camera.location = position
        camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera_data.ortho_scale = scale
        scene.render.resolution_x, scene.render.resolution_y = resolution
        scene.render.filepath = str(review_dir / (name + ".png"))
        bpy.ops.render.render(write_still=True)


def main():
    args = args_from_blender()
    params_path = Path(args.params).resolve()
    asset_path = Path(args.asset).resolve()
    semantic_path = Path(args.semantic).resolve()
    data = json.loads(params_path.read_text())
    params, diameter, height = resolve(data)
    clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"
    body = build_mesh(diameter, height)
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    semantic_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset_path), check_existing=False)
    semantic = semantic_payload(data, params, body, params_path, asset_path)
    semantic_path.write_text(json.dumps(semantic, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    if args.review_dir:
        render_views(body, diameter, height, Path(args.review_dir).resolve())
    print("COLUMN_MASTER_BUILD_OK", semantic["semantic_geometry_signature"], semantic["canonical_blend_sha256"])


if __name__ == "__main__":
    main()
