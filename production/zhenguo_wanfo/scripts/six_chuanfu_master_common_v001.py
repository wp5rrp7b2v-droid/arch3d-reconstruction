"""T-013 shared Blender geometry, semantic snapshot, reopen and review renderer.

The mesh is solely a replaceable bounded outer-envelope reference specimen.
All member dimensions and the reference realization length come from params.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[3]
GEOMETRY_KEYS = ("realization_length_mm", "width_mm", "max_thickness_mm")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    path = Path(path).resolve()
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def signature(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def names(component_id):
    root = "MASTER__" + component_id.replace("-", "_")
    return root, root + "__BODY"


def resolved(data):
    params = {item["key"]: item for item in data["parameters"]}
    assert len(params) == len(data["parameters"])
    assert data["unit"] == "mm" and data["master_version"] == "V001"
    assert data["geometry_mode"] == "BOUNDED_LONG_MEMBER_OUTER_ENVELOPE"
    assert data["canonical_transform"] == {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}
    assert data["origin_convention"] == "longitudinal_midpoint_transverse_center_lower_reference_plane"
    assert data["unsupported_geometry"] == []
    assert params["historical_full_length_mm"]["value"] is None
    assert params["historical_full_length_mm"]["classification"] == "UNKNOWN"
    assert params["historical_full_length_mm"]["production_use"] == "DO_NOT_LOCK"
    assert params["canonical_reference_length_mm"]["classification"] == "PROJECT_RULE"
    assert params["canonical_reference_length_mm"]["source_layer"] == "ENGINEERING_REFERENCE"
    assert params["canonical_reference_length_mm"]["historical_claim"] is False
    assert params["realization_length_mm"]["derives_from"] == "canonical_reference_length_mm"
    assert params["realization_length_mm"]["role"] == "GEOMETRY_EXECUTION_VALUE"
    assert float(params["realization_length_mm"]["value"]) == float(params["canonical_reference_length_mm"]["value"])
    assert all(float(params[key]["value"]) > 0 for key in GEOMETRY_KEYS)
    assert float(params["tenon_area_thickness_mm"]["value"]) > 0
    assert params["tenon_area_thickness_mm"]["geometry_use_count"] == 0
    return params


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)


def make_mesh(data, params):
    length, width, height = (float(params[key]["value"]) for key in GEOMETRY_KEYS)
    verts = [(-length / 2, -width / 2, 0), (length / 2, -width / 2, 0),
             (length / 2, width / 2, 0), (-length / 2, width / 2, 0),
             (-length / 2, -width / 2, height), (length / 2, -width / 2, height),
             (length / 2, width / 2, height), (-length / 2, width / 2, height)]
    faces = [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 6, 5),
             (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]
    collection_name, body_name = names(data["component_id"])
    mesh = bpy.data.meshes.new(body_name + "__MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    obj = bpy.data.objects.new(body_name, mesh)
    collection.objects.link(obj)
    obj.location, obj.rotation_euler, obj.scale = (0, 0, 0), (0, 0, 0), (1, 1, 1)
    obj["component_id"] = data["component_id"]
    obj["master_version"] = data["master_version"]
    obj["geometry_mode"] = data["geometry_mode"]
    obj["geometry_semantics"] = data["geometry_semantics"]
    obj["historical_full_length_state"] = "UNKNOWN_NULL_DO_NOT_LOCK"
    obj["reference_length_assembly_rule"] = data["assembly_length_rule"]["hard_fail_id"]
    obj["unit"] = "mm"
    return obj


def body_payload(obj):
    verts = [[round(float(v.co[i]), 5) for i in range(3)] for v in obj.data.vertices]
    faces = [list(poly.vertices) for poly in obj.data.polygons]
    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]
    transform = {"location": [float(v) for v in obj.location],
                 "rotation": [float(v) for v in obj.rotation_euler],
                 "scale": [float(v) for v in obj.scale]}
    body = {"name": obj.name, "vertex_count": len(verts), "face_count": len(faces),
            "local_transform": transform,
            "local_bbox_mm": {"min": mins, "max": maxs,
                              "dimensions": [round(maxs[i] - mins[i], 5) for i in range(3)]},
            "primitive": "closed_centered_rectangular_bounded_outer_envelope_reference",
            "unsupported_detail_count": 0, "geometry_vertices_mm": verts, "geometry_faces": faces}
    return {"body": body, "semantic_geometry_signature": signature({"vertices": verts, "faces": faces})}


def snapshot(data, params, obj, params_path, wrapper_path, asset_path):
    result = {"component_id": data["component_id"], "master_id": data["master_id"],
              "master_version": data["master_version"], "unit": "mm", "object_count": 1,
              "object_names": [obj.name], "mesh_count": 1,
              "collection_names": [obj.users_collection[0].name], "non_mesh_auxiliary_objects": [],
              "resolved_parameters": {key: item["value"] for key, item in sorted(params.items())},
              "parameter_semantics": {key: item for key, item in sorted(params.items())},
              "evidence_classes": {key: item["classification"] for key, item in sorted(params.items())},
              "geometry_mode": data["geometry_mode"], "geometry_lod": data["geometry_lod"],
              "geometry_semantics": data["geometry_semantics"],
              "known_unknowns": data["known_unknowns"], "historical_state": data["historical_state"],
              "originality_status": data["originality_status"],
              "assembly_length_rule": data["assembly_length_rule"],
              "unsupported_geometry": data["unsupported_geometry"],
              "tenon_area_geometry_use_count": params["tenon_area_thickness_mm"]["geometry_use_count"],
              "generator_version": "V001", "blender_version": bpy.app.version_string,
              "input_hashes": {relative(params_path): digest(params_path),
                               relative(wrapper_path): digest(wrapper_path), relative(__file__): digest(__file__)},
              "canonical_asset_path": relative(asset_path), "canonical_blend_sha256": digest(asset_path)}
    result.update(body_payload(obj))
    return result


def setup_review():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 16
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    scene.world.use_nodes = True
    bg = next(node for node in scene.world.node_tree.nodes if node.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (0.86, 0.86, 0.86, 1)
    bg.inputs["Strength"].default_value = 1
    scene.view_settings.view_transform = "Standard"
    return scene


def materials(obj):
    for label, shade in (("SIDE", 0.55), ("TOP", 0.7), ("BOTTOM", 0.4)):
        mat = bpy.data.materials.new("REVIEW_GREY_" + label + "_TEMP")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        emission = nodes.new("ShaderNodeEmission")
        emission.inputs["Color"].default_value = (shade, shade, shade, 1)
        output = nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(emission.outputs[0], output.inputs["Surface"])
        obj.data.materials.append(mat)
    for poly in obj.data.polygons:
        poly.material_index = 2 if poly.index == 0 else (1 if poly.index == 5 else 0)


def camera(target, position, scale):
    cam_data = bpy.data.cameras.new("REVIEW_CAMERA_TEMP")
    cam = bpy.data.objects.new("REVIEW_CAMERA_TEMP", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam_data.type = "ORTHO"
    cam_data.clip_end = 10000
    cam_data.ortho_scale = scale
    cam.location = position
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    return cam


def render_views(obj, params, review_dir):
    review_dir.mkdir(parents=True, exist_ok=True)
    scene = setup_review()
    materials(obj)
    length, width, height = (float(params[key]["value"]) for key in GEOMETRY_KEYS)
    extent = max(length, width, height)
    target = (0, 0, height / 2)
    cam = camera(target, (0, -extent * 3, height / 2), extent * 1.5)
    views = {
        "FRONT": ((0, -extent * 3, height / 2), max(length, height) * 1.45),
        "SIDE": ((extent * 3, 0, height / 2), max(width, height) * 1.45),
        "TOP": ((0, 0, extent * 3), max(length, width) * 1.45),
        "AXON": ((extent * 2, -extent * 2.6, extent * 2), extent * 1.9),
    }
    for view, (position, scale) in views.items():
        cam.location = position
        cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.ortho_scale = scale
        scene.render.resolution_x, scene.render.resolution_y = 1200, 900
        scene.render.filepath = str(review_dir / (view + ".png"))
        bpy.ops.render.render(write_still=True)


def inspect(expected_path, asset_path, output_path):
    expected = json.loads(Path(expected_path).read_text())
    collection_name, body_name = names(expected["component_id"])
    objects = list(bpy.data.objects)
    obj = bpy.data.objects.get(body_name)
    assert obj is not None and len(objects) == 1 and obj.type == "MESH"
    assert collection_name in bpy.data.collections
    assert bpy.context.scene.unit_settings.system == "METRIC"
    assert abs(bpy.context.scene.unit_settings.scale_length - 0.001) < 1e-9
    actual = body_payload(obj)
    assert all(actual[key] == expected[key] for key in ("body", "semantic_geometry_signature"))
    assert obj.get("component_id") == expected["component_id"]
    assert obj.get("geometry_semantics") == expected["geometry_semantics"]
    assert obj.get("historical_full_length_state") == "UNKNOWN_NULL_DO_NOT_LOCK"
    assert obj.get("reference_length_assembly_rule") == expected["assembly_length_rule"]["hard_fail_id"]
    assert digest(asset_path) == expected["canonical_blend_sha256"]
    output = {"status": "PASS", "component_id": expected["component_id"],
              "semantic_geometry_signature": actual["semantic_geometry_signature"],
              "blend_sha256": digest(asset_path), "historical_full_length_mm": None}
    Path(output_path).write_text(json.dumps(output, indent=2) + "\n")
    print("SIX_CHUANFU_REOPEN_OK", expected["component_id"])


def render_overview(asset_paths, output_path, reference_length):
    clear_scene()
    scene = setup_review()
    loaded = []
    for asset_path in asset_paths:
        with bpy.data.libraries.load(str(asset_path), link=False) as (source, dest):
            dest.objects = [name for name in source.objects if name.endswith("__BODY")]
        assert len(dest.objects) == 1
        obj = dest.objects[0]
        scene.collection.objects.link(obj)
        assert all(abs(value - 1.0) < 1e-9 for value in obj.scale)
        loaded.append(obj)
        materials(obj)
    # Translation is review-only; neither source Master is saved here.
    spacing = max(obj.dimensions.y for obj in loaded) * 1.2
    for index, obj in enumerate(loaded):
        obj.location.y = (index - (len(loaded) - 1) / 2) * spacing
        assert abs(obj.dimensions.x - reference_length) < 1e-5
    cam = camera((0, 0, max(obj.dimensions.z for obj in loaded) / 2),
                 (reference_length * 1.7, -reference_length * 2.2, reference_length * 1.8),
                 reference_length * 2.2)
    scene.render.resolution_x, scene.render.resolution_y = 1800, 1100
    scene.render.filepath = str(output_path)
    bpy.ops.render.render(write_still=True)
    print("SIX_CHUANFU_OVERVIEW_OK")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("build", "inspect", "overview"), required=True)
    parser.add_argument("--params")
    parser.add_argument("--asset")
    parser.add_argument("--semantic")
    parser.add_argument("--review-dir")
    parser.add_argument("--expected")
    parser.add_argument("--output")
    parser.add_argument("--assets", nargs="*")
    parser.add_argument("--reference-length", type=float)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    if args.mode == "inspect":
        inspect(args.expected, args.asset, args.output)
        return
    if args.mode == "overview":
        render_overview(args.assets, args.output, args.reference_length)
        return
    data = json.loads(Path(args.params).read_text())
    params = resolved(data)
    clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"
    obj = make_mesh(data, params)
    asset_path = Path(args.asset).resolve()
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset_path), check_existing=False)
    wrapper = sys.argv[sys.argv.index("--python") + 1]
    semantic = snapshot(data, params, obj, args.params, wrapper, asset_path)
    semantic_path = Path(args.semantic)
    semantic_path.parent.mkdir(parents=True, exist_ok=True)
    semantic_path.write_text(json.dumps(semantic, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    if args.review_dir:
        render_views(obj, params, Path(args.review_dir))
    print("SIX_CHUANFU_BUILD_OK", data["component_id"], semantic["semantic_geometry_signature"])


if __name__ == "__main__":
    main()
