"""T-003 Part B: modify the P0.2 input using Blender 4.x only."""

from pathlib import Path
import sys

import bpy
from mathutils import Vector


REQUIRED_ORIGINAL_OBJECTS = (
    "ARCH3D_BASE",
    "ARCH3D_COLUMN_01",
    "ARCH3D_COLUMN_02",
    "ARCH3D_COLUMN_03",
    "ARCH3D_COLUMN_04",
    "ARCH3D_ROOF",
)
MARKER_NAME = "ARCH3D_CLOUD_MARKER"
POC_VALUE = "P0_2_V002"

SCRIPT_PATH = Path(__file__).resolve()
ROUNDTRIP_DIR = SCRIPT_PATH.parent.parent
OUTPUT_DIR = ROUNDTRIP_DIR / "cloud_output"
RENDER_PATH = OUTPUT_DIR / "P0_2_CLOUD_RENDER_V001.png"
BLEND_PATH = OUTPUT_DIR / "P0_2_CLOUD_RETURN_V001.blend"


def fail(message, code=1):
    print(f"ARCH3D_CLOUD_STATUS=FAIL")
    print(f"ARCH3D_CLOUD_ERROR={message}")
    raise SystemExit(code)


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


if bpy.app.version[0] != 4:
    fail(f"CLOUD_BLENDER_MAJOR_MUST_BE_4;ACTUAL={bpy.app.version_string}", 20)

missing = [name for name in REQUIRED_ORIGINAL_OBJECTS if bpy.data.objects.get(name) is None]
if missing:
    fail("MISSING_ORIGINAL_OBJECTS=" + ",".join(missing), 21)

invalid = []
for name in REQUIRED_ORIGINAL_OBJECTS:
    obj = bpy.data.objects[name]
    if obj.type != "MESH" or len(obj.data.vertices) == 0:
        invalid.append(name)
if invalid:
    fail("INVALID_ORIGINAL_GEOMETRY=" + ",".join(invalid), 22)

if bpy.data.objects.get(MARKER_NAME) is not None:
    fail("CLOUD_MARKER_ALREADY_EXISTS_IN_INPUT", 23)

# The 0.5 m cube sits beyond the base's +X edge and toward the camera.
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(4.75, -2.50, 0.25))
marker = bpy.context.object
marker.name = MARKER_NAME

marker_material = bpy.data.materials.get("ARCH3D_CLOUD_MARKER_MATERIAL")
if marker_material is None:
    marker_material = bpy.data.materials.new("ARCH3D_CLOUD_MARKER_MATERIAL")
marker_material.diffuse_color = (0.80, 0.12, 0.04, 1.0)
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
light.data.energy = 1300
light.data.shape = "DISK"
light.data.size = 6.0
look_at(light, (0.0, 0.0, 2.0))

scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.film_transparent = False
scene.render.filepath = str(RENDER_PATH)
scene.world.color = (0.045, 0.045, 0.045)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
bpy.ops.render.render(write_still=True)
if not RENDER_PATH.is_file() or RENDER_PATH.stat().st_size <= 0:
    fail("CLOUD_RENDER_NOT_CREATED", 24)

bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH), check_existing=False)
if not BLEND_PATH.is_file() or BLEND_PATH.stat().st_size <= 0:
    fail("CLOUD_BLEND_NOT_CREATED", 25)

print(f"ARCH3D_CLOUD_STATUS=PASS")
print(f"ARCH3D_CLOUD_BLENDER_VERSION={bpy.app.version_string}")
print(f"ARCH3D_CLOUD_MARKER={MARKER_NAME}")
print(f"ARCH3D_CLOUD_RENDER={RENDER_PATH}")
print(f"ARCH3D_CLOUD_BLEND={BLEND_PATH}")
