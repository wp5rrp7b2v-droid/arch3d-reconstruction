"""Shared Blender geometry, semantic inspection and review rendering for T-012.

Only the measured rectangular end footprints and height drive the mesh.
The connecting linear loft is a replaceable engineering interpolation.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[3]
DIMENSIONS = ("bottom_width_mm", "bottom_depth_mm", "top_width_mm", "top_depth_mm", "total_height_mm")
STABLE = ("component_id", "master_id", "master_version", "unit", "object_count", "object_names", "mesh_count", "body", "sections_mm", "resolved_parameters", "evidence_classes", "geometry_mode", "geometry_lod", "known_unknowns", "originality_status", "historical_state", "semantic_geometry_signature")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    path = Path(path).resolve()
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def signature(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def names(component_id):
    base = "MASTER__" + component_id.replace("-", "_")
    return base, base + "__BODY"


def resolved(data):
    params = {item["key"]: item for item in data["parameters"]}
    assert len(params) == len(data["parameters"])
    assert all(float(params[key]["value"]) > 0 for key in DIMENSIONS)
    assert data["unit"] == "mm" and data["master_version"] == "V001"
    assert data["canonical_transform"] == {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]}
    assert data["origin_convention"] == "bottom_footprint_center"
    assert data["unsupported_geometry"] == []
    return params


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)


def make_mesh(component_id, values, data=None, curve_amount=None):
    bw, bd, tw, td, height = (float(values[key]) for key in DIMENSIONS)
    profile = (data or {}).get("profile_contract", {})
    profile_class = profile.get("profile_class", "LINEAR_OUTER_ENVELOPE")
    collection_name, body_name = names(component_id)

    if profile_class == "CURVED_QI_PROFILE":
        amount = float(profile.get("default_curve_amount", 0.5) if curve_amount is None else curve_amount)
        lo, hi = profile.get("legal_curve_amount_range", [0.0, 1.0])
        assert float(lo) <= amount <= float(hi)
        segments = int(profile.get("vertical_segments", 16))
        assert segments >= 4
        verts = []
        for i in range(segments + 1):
            t = i / segments
            smooth = 3.0 * t * t - 2.0 * t * t * t
            f = (1.0 - amount) * t + amount * smooth
            width = bw + (tw - bw) * f
            depth = bd + (td - bd) * f
            z = height * t
            verts.extend([
                (-width / 2, -depth / 2, z),
                ( width / 2, -depth / 2, z),
                ( width / 2,  depth / 2, z),
                (-width / 2,  depth / 2, z),
            ])
        faces = [(3, 2, 1, 0)]
        for i in range(segments):
            a = i * 4
            b = (i + 1) * 4
            faces.extend([
                (a + 0, a + 1, b + 1, b + 0),
                (a + 1, a + 2, b + 2, b + 1),
                (a + 2, a + 3, b + 3, b + 2),
                (a + 3, a + 0, b + 0, b + 3),
            ])
        top = segments * 4
        faces.append((top + 0, top + 1, top + 2, top + 3))
    else:
        amount = None
        verts = [(-bw / 2, -bd / 2, 0), (bw / 2, -bd / 2, 0), (bw / 2, bd / 2, 0), (-bw / 2, bd / 2, 0),
                 (-tw / 2, -td / 2, height), (tw / 2, -td / 2, height), (tw / 2, td / 2, height), (-tw / 2, td / 2, height)]
        faces = [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]

    mesh = bpy.data.meshes.new(body_name + "__MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    obj = bpy.data.objects.new(body_name, mesh)
    collection.objects.link(obj)
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)
    obj["component_id"] = component_id
    obj["master_version"] = "V001"
    obj["geometry_mode"] = (data or {}).get("geometry_mode", "MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE")
    obj["interpolation"] = (data or {}).get("interpolation", "PROJECT_RULE / REPLACEABLE_ENGINEERING_INTERPOLATION")
    obj["unit"] = "mm"
    obj["profile_class"] = profile_class
    if amount is not None:
        obj["curve_amount"] = amount
    return obj


def body_payload(obj):
    verts = [[round(float(v.co[i]), 5) for i in range(3)] for v in obj.data.vertices]
    faces = [list(p.vertices) for p in obj.data.polygons]
    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]
    transform = {"location": [float(x) for x in obj.location], "rotation": [float(x) for x in obj.rotation_euler], "scale": [float(x) for x in obj.scale]}
    profile_class = obj.get("profile_class", "LINEAR_OUTER_ENVELOPE")
    section = lambda ring: {"width": round(max(v[0] for v in ring) - min(v[0] for v in ring), 5), "depth": round(max(v[1] for v in ring) - min(v[1] for v in ring), 5)}
    if profile_class == "CURVED_QI_PROFILE":
        ring_count = len(verts) // 4
        bottom = verts[:4]
        top = verts[-4:]
        mid_start = (ring_count // 2) * 4
        mid = verts[mid_start:mid_start + 4]
        primitive = "closed_centered_rectangular_curved_qi_outer_envelope"
    else:
        bottom = verts[:4]
        top = verts[4:]
        mid = [[round((a[i] + b[i]) / 2, 5) for i in range(3)] for a, b in zip(bottom, top)]
        primitive = "closed_centered_rectangular_linear_outer_envelope"
    payload = {
        "body": {"name": obj.name, "vertex_count": len(verts), "face_count": len(faces), "local_transform": transform,
                 "local_bbox_mm": {"min": mins, "max": maxs, "dimensions": [round(maxs[i] - mins[i], 5) for i in range(3)]},
                 "primitive": primitive, "unsupported_detail_count": 0,
                 "geometry_vertices_mm": verts, "geometry_faces": faces},
        "sections_mm": {"bottom": section(bottom), "mid": section(mid), "top": section(top)},
        "semantic_geometry_signature": signature({"vertices": verts, "faces": faces}),
    }
    if profile_class == "CURVED_QI_PROFILE":
        payload["profile_geometry"] = {
            "profile_class": profile_class,
            "curve_amount": float(obj["curve_amount"]),
            "ring_count": len(verts) // 4,
            "monotonic_expected": True,
            "exact_curvature_claim": False,
        }
    return payload


def snapshot(data, params, obj, params_path, wrapper_path, asset_path):
    result = {
        "component_id": data["component_id"], "master_id": data["master_id"], "master_version": "V001", "unit": "mm",
        "object_count": 1, "object_names": [obj.name], "mesh_count": 1, "collection_names": [obj.users_collection[0].name],
        "non_mesh_auxiliary_objects": [], "resolved_parameters": {key: item["value"] for key, item in sorted(params.items())},
        "evidence_classes": {key: item["classification"] for key, item in sorted(params.items())},
        "geometry_mode": data["geometry_mode"], "geometry_lod": data["geometry_lod"],
        "interpolation": data["interpolation"], "known_unknowns": data["known_unknowns"],
        "originality_status": data["originality_status"], "historical_state": data["historical_state"],
        "dg114_geometry_use_count": 0, "generator_version": "V001", "blender_version": bpy.app.version_string,
        "input_hashes": {relative(params_path): digest(params_path), relative(wrapper_path): digest(wrapper_path), relative(__file__): digest(__file__)},
        "canonical_asset_path": relative(asset_path), "canonical_blend_sha256": digest(asset_path),
    }
    result.update(body_payload(obj))
    if obj.get("profile_class") == "CURVED_QI_PROFILE":
        result["profile_contract"] = data.get("profile_contract", {})
        result["evidence_depth_contract"] = data.get("evidence_depth_contract", {})
        result["profile_evidence"] = data.get("profile_evidence", {})
        result["registry_contract"] = data.get("registry_contract", {})
        result["deferred_geometry"] = data.get("deferred_geometry", [])
        result["historical_963_design_dimensions"] = data.get("historical_963_design_dimensions", "UNRESOLVED")
    return result


def setup_review():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 32
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.resolution_percentage = 100
    scene.world.use_nodes = True
    bg = next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (0.86, 0.86, 0.86, 1)
    bg.inputs["Strength"].default_value = 1
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    return scene


def materials(obj):
    for label, value in (("SIDE", 0.50), ("TOP", 0.66), ("BOTTOM", 0.38)):
        material = bpy.data.materials.new("REVIEW_GREY_" + label + "_TEMP")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        emission = nodes.new("ShaderNodeEmission")
        emission.inputs["Color"].default_value = (value, value, value, 1)
        output = nodes.new("ShaderNodeOutputMaterial")
        material.node_tree.links.new(emission.outputs[0], output.inputs["Surface"])
        obj.data.materials.append(material)
    for poly in obj.data.polygons:
        poly.material_index = 2 if poly.index == 0 else (1 if poly.index == 5 else 0)


def camera_at(target, position, scale):
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new("REVIEW_CAMERA_TEMP")
    camera = bpy.data.objects.new("REVIEW_CAMERA_TEMP", cam_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    cam_data.type = "ORTHO"
    cam_data.clip_end = 10000
    cam_data.ortho_scale = scale
    camera.location = position
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    return camera


def render_views(obj, values, review_dir):
    review_dir.mkdir(parents=True, exist_ok=True)
    scene = setup_review()
    materials(obj)
    width = float(values["top_width_mm"])
    depth = float(values["top_depth_mm"])
    height = float(values["total_height_mm"])
    extent = max(width, depth, height)
    target = (0, 0, height / 2)
    camera = camera_at(target, (0, -extent * 3, height / 2), extent * 1.6)
    views = {
        "FRONT": ((0, -extent * 3, height / 2), max(width, height) * 1.55),
        "SIDE": ((extent * 3, 0, height / 2), max(depth, height) * 1.55),
        "TOP": ((0, 0, extent * 3), max(width, depth) * 1.55),
        "AXON": ((extent * 2.0, -extent * 2.6, extent * 2.0), extent * 1.85),
    }
    for view, (position, scale) in views.items():
        camera.location = position
        camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
        camera.data.ortho_scale = scale
        scene.render.resolution_x = 1200
        scene.render.resolution_y = 1000
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
    assert all(actual[key] == expected[key] for key in ("body", "sections_mm", "semantic_geometry_signature"))
    assert obj.get("component_id") == expected["component_id"]
    assert obj.get("interpolation") == expected["interpolation"]
    assert digest(asset_path) == expected["canonical_blend_sha256"]
    output = {"status": "PASS", "component_id": expected["component_id"], "semantic_geometry_signature": actual["semantic_geometry_signature"], "blend_sha256": digest(asset_path)}
    Path(output_path).write_text(json.dumps(output, indent=2) + "\n")
    print("DOU_MASTER_REOPEN_OK", expected["component_id"])


def render_overview(asset_paths, output_path):
    clear_scene()
    scene = setup_review()
    positions = (-470.0, 85.0, 475.0)  # Review layout positions, not Master placement.
    for asset_path, xpos in zip(asset_paths, positions):
        with bpy.data.libraries.load(str(asset_path), link=False) as (source, destination):
            destination.objects = [name for name in source.objects if name.endswith("__BODY")]
        assert len(destination.objects) == 1
        obj = destination.objects[0]
        scene.collection.objects.link(obj)
        obj.location = (xpos, 0, 0)
        assert all(abs(x - 1.0) < 1e-9 for x in obj.scale)
        materials(obj)
    camera_at((0, 0, 120), (900, -1250, 1050), 1550)
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 1100
    scene.render.filepath = str(output_path)
    bpy.ops.render.render(write_still=True)
    print("DOU_OVERVIEW_OK")


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
    parser.add_argument("--curve-amount", type=float)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])
    if args.mode == "inspect":
        inspect(args.expected, args.asset, args.output)
        return
    if args.mode == "overview":
        render_overview(args.assets, args.output)
        return
    data = json.loads(Path(args.params).read_text())
    params = resolved(data)
    values = {key: item["value"] for key, item in params.items()}
    clear_scene()
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"
    obj = make_mesh(data["component_id"], values, data=data, curve_amount=args.curve_amount)
    asset_path = Path(args.asset).resolve()
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset_path), check_existing=False)
    semantic = snapshot(data, params, obj, args.params, sys.argv[sys.argv.index("--python") + 1], asset_path)
    semantic_path = Path(args.semantic)
    semantic_path.parent.mkdir(parents=True, exist_ok=True)
    semantic_path.write_text(json.dumps(semantic, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    if args.review_dir:
        render_views(obj, values, Path(args.review_dir))
    print("DOU_MASTER_BUILD_OK", data["component_id"], semantic["semantic_geometry_signature"])


if __name__ == "__main__":
    main()
