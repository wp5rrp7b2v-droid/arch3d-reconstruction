#!/usr/bin/env python3
"""Generate and validate the P0.3 parameter-driven architecture grey model.

Blender 3.6 usage:
  blender --background --python generate_parametric_arch_v001.py -- \
    --params PARAMS.json --blend-out MODEL.blend --png-out REVIEW.png

Reopen validation usage:
  blender --background MODEL.blend --python generate_parametric_arch_v001.py -- \
    --mode validate --params PARAMS.json
"""

import argparse
import hashlib
import json
import math
import os
import sys

import bpy
from mathutils import Vector


REQUIRED_PARAMS = {
    "bay_count_x": int,
    "bay_count_y": int,
    "bay_width": (int, float),
    "bay_depth": (int, float),
    "platform_margin": (int, float),
    "platform_height": (int, float),
    "column_height": (int, float),
    "column_radius": (int, float),
    "beam_height": (int, float),
    "beam_width": (int, float),
    "roof_eave_overhang": (int, float),
    "roof_height": (int, float),
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("build", "validate"), default="build")
    parser.add_argument("--params", required=True)
    parser.add_argument("--blend-out")
    parser.add_argument("--png-out")
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    return parser.parse_args(argv)


def load_params(path):
    with open(path, "r", encoding="utf-8") as handle:
        params = json.load(handle)
    unknown = sorted(set(params) - set(REQUIRED_PARAMS))
    missing = sorted(set(REQUIRED_PARAMS) - set(params))
    if missing or unknown:
        raise ValueError("parameter keys mismatch; missing=%s unknown=%s" % (missing, unknown))
    for key, expected_type in REQUIRED_PARAMS.items():
        if not isinstance(params[key], expected_type) or isinstance(params[key], bool):
            raise TypeError("invalid type for %s" % key)
        if params[key] <= 0:
            raise ValueError("%s must be greater than zero" % key)
    return params


def derived_values(p):
    width = p["bay_count_x"] * p["bay_width"]
    depth = p["bay_count_y"] * p["bay_depth"]
    roof_width = width + 2.0 * p["roof_eave_overhang"]
    roof_depth = depth + 2.0 * p["roof_eave_overhang"]
    platform_width = width + 2.0 * p["platform_margin"]
    platform_depth = depth + 2.0 * p["platform_margin"]
    columns = (p["bay_count_x"] + 1) * (p["bay_count_y"] + 1)
    beams_x = p["bay_count_y"] + 1
    beams_y = p["bay_count_x"] + 1
    major_objects = 2 + columns + beams_x + beams_y
    overall_height = (
        p["platform_height"]
        + p["column_height"]
        + p["beam_height"]
        + p["roof_height"]
    )
    return {
        "building_width": width,
        "building_depth": depth,
        "roof_width": roof_width,
        "roof_depth": roof_depth,
        "platform_width": platform_width,
        "platform_depth": platform_depth,
        "expected_columns": columns,
        "expected_beams_x": beams_x,
        "expected_beams_y": beams_y,
        "expected_major_objects": major_objects,
        "overall_width": max(roof_width, platform_width),
        "overall_depth": max(roof_depth, platform_depth),
        "overall_height": overall_height,
    }


def clean_scene():
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def make_material(name, color, roughness=0.8):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1.0)
    material.use_nodes = True
    bsdf = next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return material


def add_cube(name, location, dimensions, material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    return obj


def add_column(name, location, radius, height, material):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=radius,
        depth=height,
        end_fill_type="NGON",
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    return obj


def add_roof(name, width, depth, base_z, height, material):
    half_w = width / 2.0
    half_d = depth / 2.0
    # A six-vertex solid: rectangular eaves below, a centered ridge above.
    # Ridge length is derived from roof width/depth, never stored as coordinates.
    ridge_half = max(0.0, half_w - half_d)
    vertices = [
        (-half_w, -half_d, base_z),
        (half_w, -half_d, base_z),
        (half_w, half_d, base_z),
        (-half_w, half_d, base_z),
        (-ridge_half, 0.0, base_z + height),
        (ridge_half, 0.0, base_z + height),
    ]
    faces = [
        (0, 3, 2, 1),
        (0, 1, 5, 4),
        (3, 4, 5, 2),
        (0, 4, 3),
        (1, 2, 5),
    ]
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def point_camera(camera, target):
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


def add_camera_and_lights(d):
    span = max(d["overall_width"], d["overall_depth"], d["overall_height"])
    target_z = d["overall_height"] * 0.43
    camera_data = bpy.data.cameras.new("ARCH3D_CAMERA_DATA")
    camera = bpy.data.objects.new("ARCH3D_CAMERA", camera_data)
    bpy.context.collection.objects.link(camera)
    # A low three-quarter view keeps the 0.30 m beam band visible beneath eaves.
    camera.location = (span * 1.15, -span * 1.35, d["overall_height"] * 0.75)
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = max(d["overall_width"] * 1.3, d["overall_depth"] * 1.7, d["overall_height"] * 2.0)
    point_camera(camera, (0.0, 0.0, target_z))
    bpy.context.scene.camera = camera

    area_data = bpy.data.lights.new("ARCH3D_KEY_LIGHT_DATA", type="AREA")
    area_data.energy = 1100.0
    area_data.size = span
    area = bpy.data.objects.new("ARCH3D_KEY_LIGHT", area_data)
    bpy.context.collection.objects.link(area)
    area.location = (-span * 0.65, -span * 0.75, span * 1.5)
    area.rotation_euler = (Vector((0.0, 0.0, target_z)) - area.location).to_track_quat("-Z", "Y").to_euler()

    sun_data = bpy.data.lights.new("ARCH3D_FILL_LIGHT_DATA", type="SUN")
    sun_data.energy = 1.8
    sun = bpy.data.objects.new("ARCH3D_FILL_LIGHT", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(28.0), math.radians(-20.0), math.radians(145.0))


def configure_scene(params_path, d):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 3.0
    scene.eevee.gtao_factor = 1.25
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.055, 0.055, 0.055)
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    scene.display.shading.light = "STUDIO"
    scene["arch3d_schema"] = "P0_3_PARAMETRIC_ARCH_V001"
    scene["arch3d_param_file"] = os.path.abspath(params_path)
    for key, value in d.items():
        scene["arch3d_" + key] = value


def build_model(p, params_path):
    d = derived_values(p)
    clean_scene()
    structure_mat = make_material("ARCH3D_MAT_STRUCTURE", (0.39, 0.41, 0.43))
    beam_mat = make_material("ARCH3D_MAT_BEAM", (0.62, 0.64, 0.66))
    platform_mat = make_material("ARCH3D_MAT_PLATFORM", (0.53, 0.54, 0.55))
    roof_mat = make_material("ARCH3D_MAT_ROOF", (0.29, 0.31, 0.33))

    add_cube(
        "ARCH3D_PLATFORM",
        (0.0, 0.0, p["platform_height"] / 2.0),
        (d["platform_width"], d["platform_depth"], p["platform_height"]),
        platform_mat,
    )

    column_center_z = p["platform_height"] + p["column_height"] / 2.0
    for iy in range(p["bay_count_y"] + 1):
        y = (iy - p["bay_count_y"] / 2.0) * p["bay_depth"]
        for ix in range(p["bay_count_x"] + 1):
            x = (ix - p["bay_count_x"] / 2.0) * p["bay_width"]
            add_column(
                "ARCH3D_COLUMN_X%02d_Y%02d" % (ix, iy),
                (x, y, column_center_z),
                p["column_radius"],
                p["column_height"],
                structure_mat,
            )

    beam_center_z = p["platform_height"] + p["column_height"] + p["beam_height"] / 2.0
    for iy in range(p["bay_count_y"] + 1):
        y = (iy - p["bay_count_y"] / 2.0) * p["bay_depth"]
        add_cube(
            "ARCH3D_BEAM_X_Y%02d" % iy,
            (0.0, y, beam_center_z),
            (d["building_width"] + 2.0 * p["column_radius"], p["beam_width"], p["beam_height"]),
            beam_mat,
        )
    for ix in range(p["bay_count_x"] + 1):
        x = (ix - p["bay_count_x"] / 2.0) * p["bay_width"]
        add_cube(
            "ARCH3D_BEAM_Y_X%02d" % ix,
            (x, 0.0, beam_center_z),
            (p["beam_width"], d["building_depth"] + 2.0 * p["column_radius"], p["beam_height"]),
            beam_mat,
        )

    roof_base_z = p["platform_height"] + p["column_height"] + p["beam_height"]
    add_roof("ARCH3D_ROOF", d["roof_width"], d["roof_depth"], roof_base_z, p["roof_height"], roof_mat)
    add_camera_and_lights(d)
    configure_scene(params_path, d)
    return d


def core_objects():
    prefixes = ("ARCH3D_PLATFORM", "ARCH3D_COLUMN_", "ARCH3D_BEAM_", "ARCH3D_ROOF")
    return sorted(
        (obj for obj in bpy.data.objects if obj.name.startswith(prefixes)),
        key=lambda obj: obj.name,
    )


def object_signature(objects):
    records = []
    for obj in objects:
        records.append(
            "%s|%.6f,%.6f,%.6f|%.6f,%.6f,%.6f"
            % (obj.name, *obj.location, *obj.dimensions)
        )
    return hashlib.sha256("\n".join(records).encode("utf-8")).hexdigest()


def vector_close(actual, expected, tolerance=1.0e-5):
    return all(abs(float(a) - float(e)) <= tolerance for a, e in zip(actual, expected))


def validate_model(p, params_path):
    d = derived_values(p)
    names = {obj.name for obj in bpy.data.objects}
    required_names = {"ARCH3D_PLATFORM", "ARCH3D_ROOF"}
    required_names.update(
        "ARCH3D_COLUMN_X%02d_Y%02d" % (ix, iy)
        for iy in range(p["bay_count_y"] + 1)
        for ix in range(p["bay_count_x"] + 1)
    )
    required_names.update("ARCH3D_BEAM_X_Y%02d" % iy for iy in range(p["bay_count_y"] + 1))
    required_names.update("ARCH3D_BEAM_Y_X%02d" % ix for ix in range(p["bay_count_x"] + 1))
    missing = sorted(required_names - names)
    columns = [obj for obj in bpy.data.objects if obj.name.startswith("ARCH3D_COLUMN_")]
    beams_x = [obj for obj in bpy.data.objects if obj.name.startswith("ARCH3D_BEAM_X_")]
    beams_y = [obj for obj in bpy.data.objects if obj.name.startswith("ARCH3D_BEAM_Y_")]
    major = core_objects()
    platform = bpy.data.objects.get("ARCH3D_PLATFORM")
    roof = bpy.data.objects.get("ARCH3D_ROOF")
    column_center_z = p["platform_height"] + p["column_height"] / 2.0
    beam_center_z = p["platform_height"] + p["column_height"] + p["beam_height"] / 2.0
    geometry_checks = []
    if platform:
        geometry_checks.extend(
            [
                vector_close(platform.location, (0.0, 0.0, p["platform_height"] / 2.0)),
                vector_close(platform.dimensions, (d["platform_width"], d["platform_depth"], p["platform_height"])),
            ]
        )
    if roof:
        geometry_checks.append(vector_close(roof.dimensions, (d["roof_width"], d["roof_depth"], p["roof_height"])))
    for iy in range(p["bay_count_y"] + 1):
        y = (iy - p["bay_count_y"] / 2.0) * p["bay_depth"]
        beam_x = bpy.data.objects.get("ARCH3D_BEAM_X_Y%02d" % iy)
        if beam_x:
            geometry_checks.extend(
                [
                    vector_close(beam_x.location, (0.0, y, beam_center_z)),
                    vector_close(
                        beam_x.dimensions,
                        (d["building_width"] + 2.0 * p["column_radius"], p["beam_width"], p["beam_height"]),
                    ),
                ]
            )
        for ix in range(p["bay_count_x"] + 1):
            x = (ix - p["bay_count_x"] / 2.0) * p["bay_width"]
            column = bpy.data.objects.get("ARCH3D_COLUMN_X%02d_Y%02d" % (ix, iy))
            if column:
                geometry_checks.extend(
                    [
                        vector_close(column.location, (x, y, column_center_z)),
                        vector_close(column.dimensions, (2.0 * p["column_radius"], 2.0 * p["column_radius"], p["column_height"])),
                    ]
                )
    for ix in range(p["bay_count_x"] + 1):
        x = (ix - p["bay_count_x"] / 2.0) * p["bay_width"]
        beam_y = bpy.data.objects.get("ARCH3D_BEAM_Y_X%02d" % ix)
        if beam_y:
            geometry_checks.extend(
                [
                    vector_close(beam_y.location, (x, 0.0, beam_center_z)),
                    vector_close(
                        beam_y.dimensions,
                        (p["beam_width"], d["building_depth"] + 2.0 * p["column_radius"], p["beam_height"]),
                    ),
                ]
            )
    checks = [
        not missing,
        len(columns) == d["expected_columns"],
        len(beams_x) == d["expected_beams_x"],
        len(beams_y) == d["expected_beams_y"],
        len(major) == d["expected_major_objects"],
        bpy.context.scene.get("arch3d_schema") == "P0_3_PARAMETRIC_ARCH_V001",
        len(geometry_checks) > 0 and all(geometry_checks),
    ]
    result = "PASS" if all(checks) else "FAIL"
    print_summary(result, params_path, d, len(columns), len(major), object_signature(major))
    if missing:
        print("MISSING_OBJECTS=" + ",".join(missing))
    if result != "PASS":
        raise RuntimeError("ARCH3D validation failed")
    return d


def print_summary(result, params_path, d, actual_columns, major_count, signature):
    print("ARCH3D_PARAMETRIC_RESULT=" + result)
    print("PARAM_FILE=" + os.path.abspath(params_path))
    print("BAY_COUNT_X=%d" % (d["expected_beams_y"] - 1))
    print("BAY_COUNT_Y=%d" % (d["expected_beams_x"] - 1))
    print("EXPECTED_COLUMNS=%d" % d["expected_columns"])
    print("ACTUAL_COLUMNS=%d" % actual_columns)
    print("BUILDING_WIDTH=%.3f" % d["building_width"])
    print("BUILDING_DEPTH=%.3f" % d["building_depth"])
    print("OVERALL_WIDTH=%.3f" % d["overall_width"])
    print("OVERALL_DEPTH=%.3f" % d["overall_depth"])
    print("OVERALL_HEIGHT=%.3f" % d["overall_height"])
    print("OBJECT_COUNT=%d" % major_count)
    print("CORE_SIGNATURE=" + signature)


def main():
    args = parse_args()
    params_path = os.path.abspath(args.params)
    p = load_params(params_path)
    if args.mode == "validate":
        validate_model(p, params_path)
        return
    if not args.blend_out or not args.png_out:
        raise ValueError("build mode requires --blend-out and --png-out")
    blend_out = os.path.abspath(args.blend_out)
    png_out = os.path.abspath(args.png_out)
    os.makedirs(os.path.dirname(blend_out), exist_ok=True)
    os.makedirs(os.path.dirname(png_out), exist_ok=True)
    d = build_model(p, params_path)
    bpy.context.scene.render.filepath = png_out
    bpy.ops.wm.save_as_mainfile(filepath=blend_out, check_existing=False)
    bpy.ops.render.render(write_still=True)
    validate_model(p, params_path)
    print("BLEND_PATH=" + blend_out)
    print("PNG_PATH=" + png_out)


if __name__ == "__main__":
    main()
