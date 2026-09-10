"""T-003 V006 Cloud modification and independent reopen verification."""

import argparse
from pathlib import Path
import sys

import bpy
from mathutils import Vector


EXPECTED_BLENDER_VERSION = (4, 5, 13)
REQUIRED_ORIGINAL_OBJECTS = (
    "ARCH3D_BASE",
    "ARCH3D_COLUMN_01",
    "ARCH3D_COLUMN_02",
    "ARCH3D_COLUMN_03",
    "ARCH3D_COLUMN_04",
    "ARCH3D_ROOF",
)
MARKER_NAME = "ARCH3D_CLOUD_MARKER"
POC_VALUE = "P0_2_V006"

SCRIPT_PATH = Path(__file__).resolve()
ROUNDTRIP_DIR = SCRIPT_PATH.parent.parent
OUTPUT_DIR = ROUNDTRIP_DIR / "cloud_output"
RENDER_PATH = OUTPUT_DIR / "P0_2_GHA_RENDER_V001.png"
RETURN_PATH = OUTPUT_DIR / "P0_2_GHA_RETURN_V001.blend"


def fail(message):
    print("ARCH3D_GHA_STATUS=FAIL")
    print(f"ARCH3D_GHA_ERROR={message}")
    raise RuntimeError(message)


def parse_mode():
    script_args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("modify", "reopen-check"), required=True)
    return parser.parse_args(script_args).mode


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def validate_mesh_objects(names):
    missing = [name for name in names if bpy.data.objects.get(name) is None]
    if missing:
        fail("MISSING_OBJECTS=" + ",".join(missing))

    invalid = []
    for name in names:
        obj = bpy.data.objects[name]
        if obj.type != "MESH" or len(obj.data.vertices) == 0:
            invalid.append(name)
    if invalid:
        fail("INVALID_MESH_GEOMETRY=" + ",".join(invalid))


def mesh_signature(obj):
    return (
        tuple(round(value, 9) for row in obj.matrix_world for value in row),
        tuple(tuple(round(value, 9) for value in vertex.co) for vertex in obj.data.vertices),
        tuple(tuple(edge.vertices) for edge in obj.data.edges),
        tuple(tuple(polygon.vertices) for polygon in obj.data.polygons),
    )


def validate_metadata():
    scene = bpy.context.scene
    poc_value = scene.get("ARCH3D_CLOUD_POC")
    cloud_version = scene.get("ARCH3D_CLOUD_BLENDER_VERSION")
    if poc_value != POC_VALUE:
        fail(f"ARCH3D_CLOUD_POC_INVALID={poc_value!r}")
    if not isinstance(cloud_version, str) or not cloud_version:
        fail(f"ARCH3D_CLOUD_BLENDER_VERSION_INVALID={cloud_version!r}")
    return poc_value, cloud_version


if bpy.app.version[:3] != EXPECTED_BLENDER_VERSION:
    fail(
        "BLENDER_VERSION_MUST_BE_4_5_13;"
        f"ACTUAL={bpy.app.version_string}"
    )

mode = parse_mode()
validate_mesh_objects(REQUIRED_ORIGINAL_OBJECTS)

if mode == "reopen-check":
    validate_mesh_objects((MARKER_NAME,))
    poc_value, cloud_version = validate_metadata()
    print("ARCH3D_CLOUD_REOPEN=PASS")
    print("ARCH3D_CLOUD_MARKER=PASS")
    print(f"ARCH3D_CLOUD_POC={poc_value}")
    print(f"ARCH3D_CLOUD_BLENDER_VERSION={cloud_version}")
else:
    if bpy.data.objects.get(MARKER_NAME) is not None:
        fail("CLOUD_MARKER_ALREADY_EXISTS_IN_INPUT")

    original_signatures = {
        name: mesh_signature(bpy.data.objects[name])
        for name in REQUIRED_ORIGINAL_OBJECTS
    }

    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(4.75, -2.50, 0.25))
    marker = bpy.context.object
    marker.name = MARKER_NAME

    marker_material = bpy.data.materials.new("ARCH3D_CLOUD_MARKER_MATERIAL")
    marker_material.use_nodes = True
    marker_material.diffuse_color = (0.80, 0.12, 0.04, 1.0)
    principled = marker_material.node_tree.nodes.get("Principled BSDF")
    if principled is not None:
        principled.inputs["Base Color"].default_value = (0.80, 0.12, 0.04, 1.0)
        principled.inputs["Roughness"].default_value = 0.45
    marker.data.materials.append(marker_material)

    scene = bpy.context.scene
    scene["ARCH3D_CLOUD_POC"] = POC_VALUE
    scene["ARCH3D_CLOUD_BLENDER_VERSION"] = bpy.app.version_string

    camera = bpy.data.objects.get("Camera")
    if camera is None or camera.type != "CAMERA":
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        camera.name = "Camera"
    camera.location = (11.5, -14.0, 9.5)
    camera.data.lens = 52
    look_at(camera, (0.3, -0.2, 2.4))
    scene.camera = camera

    light = bpy.data.objects.get("Light")
    if light is None or light.type != "LIGHT":
        bpy.ops.object.light_add(type="AREA")
        light = bpy.context.object
        light.name = "Light"
    light.data.type = "AREA"
    light.location = (4.0, -5.0, 10.0)
    light.data.energy = 1600
    light.data.shape = "DISK"
    light.data.size = 6.0
    look_at(light, (0.0, 0.0, 2.0))

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 16
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.filepath = str(RENDER_PATH)
    scene.world.color = (0.045, 0.045, 0.045)

    for name, signature in original_signatures.items():
        if mesh_signature(bpy.data.objects[name]) != signature:
            fail(f"ORIGINAL_GEOMETRY_CHANGED={name}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    bpy.ops.render.render(write_still=True)
    if not RENDER_PATH.is_file() or RENDER_PATH.stat().st_size <= 0:
        fail("CLOUD_RENDER_NOT_CREATED")

    bpy.ops.wm.save_as_mainfile(filepath=str(RETURN_PATH), check_existing=False)
    if not RETURN_PATH.is_file() or RETURN_PATH.stat().st_size <= 0:
        fail("CLOUD_RETURN_NOT_CREATED")

    print("ARCH3D_GHA_STATUS=PASS")
    print(f"ARCH3D_CLOUD_BLENDER_VERSION={bpy.app.version_string}")
    print(f"ARCH3D_CLOUD_RENDER={RENDER_PATH}")
    print(f"ARCH3D_CLOUD_RETURN={RETURN_PATH}")
