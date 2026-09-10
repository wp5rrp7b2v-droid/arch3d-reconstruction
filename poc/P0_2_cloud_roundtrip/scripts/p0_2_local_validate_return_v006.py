"""T-003 V006 Local 3.6 return validator. It never repairs scene data."""

import bpy


REQUIRED_OBJECTS = (
    "ARCH3D_BASE",
    "ARCH3D_COLUMN_01",
    "ARCH3D_COLUMN_02",
    "ARCH3D_COLUMN_03",
    "ARCH3D_COLUMN_04",
    "ARCH3D_ROOF",
    "ARCH3D_CLOUD_MARKER",
)


def fail(message):
    print("ARCH3D_LOCAL_VALIDATION=FAIL")
    print(f"ARCH3D_LOCAL_ERROR={message}")
    raise RuntimeError(message)


if bpy.app.version[:2] != (3, 6):
    fail(f"LOCAL_BLENDER_MUST_BE_3_6_X;ACTUAL={bpy.app.version_string}")

missing = [name for name in REQUIRED_OBJECTS if bpy.data.objects.get(name) is None]
if missing:
    fail("MISSING_OBJECTS=" + ",".join(missing))

invalid = []
for name in REQUIRED_OBJECTS:
    obj = bpy.data.objects[name]
    if obj.type != "MESH" or len(obj.data.vertices) == 0:
        invalid.append(name)
if invalid:
    fail("INVALID_MESH_GEOMETRY=" + ",".join(invalid))

scene = bpy.context.scene
poc_value = scene.get("ARCH3D_CLOUD_POC")
cloud_version = scene.get("ARCH3D_CLOUD_BLENDER_VERSION")

if poc_value != "P0_2_V006":
    fail(f"ARCH3D_CLOUD_POC_INVALID={poc_value!r}")
if not isinstance(cloud_version, str) or not cloud_version:
    fail(f"ARCH3D_CLOUD_BLENDER_VERSION_UNREADABLE={cloud_version!r}")

print("ARCH3D_LOCAL_VALIDATION=PASS")
print("ARCH3D_REQUIRED_OBJECTS=" + ",".join(REQUIRED_OBJECTS))
print(f"ARCH3D_CLOUD_POC={poc_value}")
print(f"ARCH3D_CLOUD_BLENDER_VERSION={cloud_version}")
