"""Independent reopen inspection: run Blender with the saved .blend as input."""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


def main():
    args = cli()
    expected = json.loads(Path(args.expected).read_text())
    objects = list(bpy.data.objects)
    assert len(objects) == 1, [obj.name for obj in objects]
    body = objects[0]
    assert body.type == "MESH" and body.name == "MASTER__CMP_COLUMN_001__BODY"
    assert [c.name for c in bpy.data.collections] == ["MASTER__CMP_COLUMN_001"]
    assert bpy.context.scene.unit_settings.system == "METRIC"
    assert bpy.context.scene.unit_settings.length_unit == "MILLIMETERS"
    assert math.isclose(bpy.context.scene.unit_settings.scale_length, 0.001, abs_tol=1e-7)
    transform = {
        "location": [float(x) for x in body.location],
        "rotation": [float(x) for x in body.rotation_euler],
        "scale": [float(x) for x in body.scale],
    }
    assert transform == expected["body"]["local_transform"]
    assert transform == {"location": [0.0] * 3, "rotation": [0.0] * 3, "scale": [1.0] * 3}
    verts = [tuple(round(float(v.co[i]), 5) for i in range(3)) for v in body.data.vertices]
    faces = [tuple(p.vertices) for p in body.data.polygons]
    serialized = json.dumps({"vertices": verts, "faces": faces}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    signature = hashlib.sha256(serialized.encode()).hexdigest()
    assert signature == expected["semantic_geometry_signature"]
    mins = [min(v[i] for v in verts) for i in range(3)]
    maxs = [max(v[i] for v in verts) for i in range(3)]
    dimensions = [maxs[i] - mins[i] for i in range(3)]
    expected_dim = expected["body"]["local_bbox_mm"]["dimensions"]
    assert all(math.isclose(a, b, abs_tol=0.001) for a, b in zip(dimensions, expected_dim))
    assert math.isclose(mins[2], 0, abs_tol=0.001)
    radii = [math.hypot(v[0], v[1]) for v in verts]
    assert max(radii) - min(radii) < 0.001
    assert len(set(round(v[2], 3) for v in verts)) == 2
    assert len(verts) == 256 and len(faces) == 130
    result = {
        "status": "PASS",
        "loaded_blend": bpy.data.filepath,
        "blender_version": bpy.app.version_string,
        "object_count": len(objects),
        "mesh_count": 1,
        "collection_names": [c.name for c in bpy.data.collections],
        "local_transform": transform,
        "bbox_dimensions_mm": dimensions,
        "constant_radius": True,
        "unsupported_column_geometry_count": 0,
        "semantic_geometry_signature": signature,
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print("COLUMN_MASTER_REOPEN_OK", signature)


if __name__ == "__main__":
    main()
