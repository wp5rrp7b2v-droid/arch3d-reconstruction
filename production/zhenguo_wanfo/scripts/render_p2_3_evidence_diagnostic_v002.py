#!/usr/bin/env python3
"""Read-only T-008 V004 evidence diagnostic from the frozen V001 blend + manifest.

The host process verifies frozen inputs, asks Blender to color the already saved
objects in memory, and adds a legible four-category legend to the rendered PNG.
It never calls Blender's save-as operator or rebuilds model geometry.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[3]
CASE = ROOT / "production/zhenguo_wanfo"
SCRIPT = Path(__file__).resolve()
BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
BLEND = CASE / "output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend"
MANIFEST = CASE / "build/P2_3_INTEGRATION_MANIFEST_V001.json"
OUTPUT = CASE / "review/P2_3_INTEGRATED_RECONSTRUCTION_V001_EVIDENCE_DIAGNOSTIC_V002.png"
SIDECAR = CASE / "validation/P2_3_EVIDENCE_DIAGNOSTIC_V002_QC.json"
EXPECTED_BLEND_SHA256 = "ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512"

UNKNOWN = "UNKNOWN / PLACEHOLDER"
COMPLETION = "REASONABLE COMPLETION"
INFERENCE = "HIGH CONFIDENCE INFERENCE"
CONFIRMED = "CONFIRMED"
PRIORITY = (UNKNOWN, COMPLETION, INFERENCE, CONFIRMED)
LEGEND = (CONFIRMED, INFERENCE, COMPLETION, UNKNOWN)
COLORS = {
    CONFIRMED: (45, 188, 119),
    INFERENCE: (61, 144, 242),
    COMPLETION: (245, 171, 45),
    UNKNOWN: (216, 72, 126),
}
KNOWN_EVIDENCE_TOKENS = {
    "CONFIRMED", "HIGH_CONFIDENCE_INFERENCE", "REASONABLE_COMPLETION",
    "UNKNOWN", "UNRESOLVED", "UNKNOWN_PLACEHOLDER", "UNRESOLVED_PLACEHOLDER",
}
UNKNOWN_TOKENS = {"UNKNOWN", "UNRESOLVED", "UNKNOWN_PLACEHOLDER", "UNRESOLVED_PLACEHOLDER"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def evidence_tokens(record: dict) -> set[str]:
    raw = record.get("evidence_class", "")
    values = raw if isinstance(raw, list) else str(raw).split("+")
    tokens = {str(value).strip().upper() for value in values if str(value).strip()}
    if not tokens or tokens - KNOWN_EVIDENCE_TOKENS:
        raise ValueError(f"Unclassified evidence metadata for {record.get('instance_id')}: {raw!r}")
    return tokens


def classify(record: dict) -> str:
    """Use manifest evidence, with the most uncertain applicable class winning."""
    tokens = evidence_tokens(record)
    overrides = record.get("override_ids", [])
    if not isinstance(overrides, list):
        raise ValueError(f"override_ids is not a list: {record.get('instance_id')}")
    placeholder_status = str(record.get("placeholder_status", "")).upper()
    if (record.get("bounded_placeholder") is True
            or record.get("unresolved_placeholder") is True
            or tokens & UNKNOWN_TOKENS
            or placeholder_status.startswith(("UNKNOWN", "UNRESOLVED"))):
        return UNKNOWN
    if overrides or "REASONABLE_COMPLETION" in tokens:
        return COMPLETION
    if "HIGH_CONFIDENCE_INFERENCE" in tokens:
        return INFERENCE
    if "CONFIRMED" in tokens:
        return CONFIRMED
    raise ValueError(f"Evidence class has no mapping: {record.get('instance_id')}")


def classification_self_check() -> None:
    cases = (
        ({"evidence_class": "CONFIRMED", "override_ids": []}, CONFIRMED),
        ({"evidence_class": "CONFIRMED+HIGH_CONFIDENCE_INFERENCE", "override_ids": []}, INFERENCE),
        ({"evidence_class": "HIGH_CONFIDENCE_INFERENCE+REASONABLE_COMPLETION", "override_ids": []}, COMPLETION),
        ({"evidence_class": "CONFIRMED", "override_ids": ["Z-006-RC-01"]}, COMPLETION),
        ({"evidence_class": "CONFIRMED", "override_ids": ["Z-006-RC-01"], "bounded_placeholder": True}, UNKNOWN),
        ({"evidence_class": "UNKNOWN+CONFIRMED", "override_ids": []}, UNKNOWN),
        ({"evidence_class": "CONFIRMED", "override_ids": [], "originality_status": "unknown"}, CONFIRMED),
    )
    for record, expected in cases:
        assert classify(record) == expected


def records_and_classes(manifest: dict) -> tuple[dict[str, dict], dict[str, str]]:
    records = manifest["instances"]
    by_id = {record["instance_id"]: record for record in records}
    if len(records) != len(by_id) or len(records) != 365:
        raise ValueError("Expected 365 unique stable instance IDs")
    if len(manifest["component_families"]) != 11 or len(manifest["variants"]) != 40:
        raise ValueError("Frozen family/variant counts changed")
    if len({record["family_id"] for record in records}) != 11:
        raise ValueError("Manifest instance family count changed")
    classes = {instance_id: classify(record) for instance_id, record in by_id.items()}
    if set(classes.values()) - set(PRIORITY):
        raise ValueError("Unrecognized display category")
    return by_id, classes


def worker(manifest_path: Path, raw_path: Path, worker_qc_path: Path) -> None:
    import bpy

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records, classes = records_and_classes(manifest)
    meshes = {ob.name: ob for ob in bpy.data.objects if ob.type == "MESH"}
    if len(meshes) != 365 or set(meshes) != set(records):
        raise ValueError("Opened blend mesh IDs do not match authoritative manifest")
    for instance_id, record in records.items():
        ob = meshes[instance_id]
        if (ob.get("instance_id") != instance_id
                or ob.get("family_id") != record["family_id"]
                or ob.get("variant_id") != record["variant_id"]):
            raise ValueError(f"Saved-object mapping differs from manifest: {instance_id}")
        rgb = COLORS[classes[instance_id]]
        ob.color = (*(component / 255 for component in rgb), 1.0)
        ob.hide_render = False

    scene = bpy.context.scene
    camera = bpy.data.objects.get("P2_3_REVIEW_CAMERA")
    diagnostic = bpy.data.collections.get("P2_3_DIAGNOSTIC")
    roof = bpy.data.collections.get("P2_3_ROOF_ENVELOPE")
    if camera is None or camera.type != "CAMERA" or diagnostic is None or roof is None:
        raise ValueError("Frozen review camera or diagnostic collections are missing")
    scene.camera = camera  # V001 saved this camera in its diagnostic view.
    camera.hide_render = False
    diagnostic.hide_render = False
    roof.hide_render = False
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.render.filepath = str(raw_path)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.render.render(write_still=True)
    if not raw_path.is_file():
        raise ValueError("Blender did not write the diagnostic render")
    result = {
        "blender_version": bpy.app.version_string,
        "rendered_mesh_count": len(meshes),
        "manifest_mapping": "PASS: all 365 displayed mesh IDs unique and family/variant metadata matched",
        "camera": camera.name,
        "presentation_blend_saved": False,
    }
    worker_qc_path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def font(size: int):
    from PIL import ImageFont

    candidates = (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def add_legend(raw_path: Path, output_path: Path, counts: Counter) -> None:
    from PIL import Image, ImageDraw

    render = Image.open(raw_path).convert("RGB")
    if render.size != (1400, 1000):
        raise ValueError(f"Unexpected Blender render size: {render.size}")
    canvas = Image.new("RGB", (1400, 1190), (34, 39, 46))
    canvas.paste(render, (0, 190))
    draw = ImageDraw.Draw(canvas)
    draw.text((36, 12), "EVIDENCE DIAGNOSTIC  /  T-008 V004", font=font(31), fill=(245, 247, 250))
    draw.text((37, 52), "Manifest-led classification  |  most uncertain evidence wins  |  365 stable instances", font=font(18), fill=(181, 191, 204))
    labels = {
        CONFIRMED: ("CONFIRMED",),
        INFERENCE: ("HIGH CONFIDENCE", "INFERENCE"),
        COMPLETION: ("REASONABLE", "COMPLETION / RC"),
        UNKNOWN: ("UNKNOWN /", "PLACEHOLDER"),
    }
    for index, category in enumerate(LEGEND):
        x = 36 + index * 340
        draw.rounded_rectangle((x, 82, x + 324, 174), radius=10, fill=(50, 57, 67))
        draw.rectangle((x + 12, 95, x + 46, 155), fill=COLORS[category])
        for line_number, line in enumerate(labels[category]):
            draw.text((x + 57, 91 + line_number * 23), line, font=font(18), fill=(245, 247, 250))
        draw.text((x + 57, 141), f"{counts[category]} instances", font=font(16), fill=(190, 202, 217))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--raw", type=Path)
    parser.add_argument("--worker-qc", type=Path)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--sidecar", type=Path, default=SIDECAR)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    args = parser.parse_args(argv)
    if args.worker:
        if args.raw is None or args.worker_qc is None:
            raise ValueError("Worker requires --raw and --worker-qc")
        worker(args.manifest.resolve(), args.raw.resolve(), args.worker_qc.resolve())
        return

    classification_self_check()
    if not BLENDER.is_file():
        raise FileNotFoundError(BLENDER)
    frozen = [
        BLEND, MANIFEST,
        CASE / "components/P2_3_COMPONENT_LIBRARY_V001.json",
        CASE / "scripts/generate_p2_3_integrated_reconstruction_v001.py",
        CASE / "validation/P2_3_V003_ROUNDTRIP_QC_V001.json",
    ] + [CASE / f"review/P2_3_INTEGRATED_RECONSTRUCTION_V001_{name}.png"
         for name in ("PLAN", "ELEVATION", "AXON", "EXTERIOR_3Q", "STRUCTURE_DETAIL")]
    frozen_before = {str(path.relative_to(ROOT)): sha256(path) for path in frozen}
    if sha256(BLEND) != EXPECTED_BLEND_SHA256:
        raise ValueError("Frozen V001 canonical blend SHA256 changed")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    records, classes = records_and_classes(manifest)
    counts = Counter(classes.values())
    for category in PRIORITY:
        counts.setdefault(category, 0)
    with tempfile.TemporaryDirectory(prefix="p2_3_v004_diagnostic_") as temp:
        raw = Path(temp) / "raw.png"
        worker_qc_path = Path(temp) / "worker_qc.json"
        command = [str(BLENDER), "--background", str(BLEND), "--python-exit-code", "10",
                   "--python", str(SCRIPT), "--", "--worker", "--manifest", str(args.manifest),
                   "--raw", str(raw), "--worker-qc", str(worker_qc_path)]
        run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
        if run.returncode:
            raise RuntimeError(f"Blender diagnostic failed ({run.returncode}):\n{run.stdout[-3000:]}\n{run.stderr[-3000:]}")
        worker_qc = json.loads(worker_qc_path.read_text(encoding="utf-8"))
        if worker_qc["rendered_mesh_count"] != len(records):
            raise ValueError("Worker and manifest instance counts differ")
        add_legend(raw, args.output, counts)
    frozen_after = {str(path.relative_to(ROOT)): sha256(path) for path in frozen}
    if frozen_before != frozen_after:
        raise ValueError("A frozen model, engineering evidence file or approved review image changed")
    result = {
        "task": "T-008 V004",
        "status": "PASS",
        "authoritative_source": "Integration Manifest V001 instance records by stable instance ID",
        "input_manifest_path": str(args.manifest.relative_to(ROOT)),
        "input_manifest_sha256": sha256(args.manifest),
        "canonical_blend_sha256_before": frozen_before[str(BLEND.relative_to(ROOT))],
        "canonical_blend_sha256_after": frozen_after[str(BLEND.relative_to(ROOT))],
        "frozen_input_sha256_before_after_equal": True,
        "frozen_input_sha256": frozen_after,
        "component_family_count": len(manifest["component_families"]),
        "variant_count": len(manifest["variants"]),
        "stable_instance_count": len(records),
        "category_priority_most_uncertain_first": list(PRIORITY),
        "category_counts": {category: counts[category] for category in LEGEND},
        "instance_classification": dict(sorted(classes.items())),
        "rc_override_instance_count": sum(bool(record["override_ids"]) for record in records.values()),
        "rc_override_without_placeholder_count": sum(bool(record["override_ids"]) and classes[instance_id] == COMPLETION for instance_id, record in records.items()),
        "rc_override_superseded_by_unknown_count": sum(bool(record["override_ids"]) and classes[instance_id] == UNKNOWN for instance_id, record in records.items()),
        "legend_categories_all_embedded": list(LEGEND),
        "legend_zero_count_categories_retained": [category for category in LEGEND if counts[category] == 0],
        "rendered_mesh_manifest_mapping": worker_qc["manifest_mapping"],
        "worker_blender_version": worker_qc["blender_version"],
        "worker_camera": worker_qc["camera"],
        "geometry_changed": False,
        "canonical_blend_saved": False,
        "diagnostic_png_path": str(args.output.relative_to(ROOT)),
        "diagnostic_png_sha256": sha256(args.output),
    }
    args.sidecar.parent.mkdir(parents=True, exist_ok=True)
    args.sidecar.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("P2_3_EVIDENCE_DIAGNOSTIC_V002_PASS", json.dumps({
        "counts": result["category_counts"],
        "png_sha256": result["diagnostic_png_sha256"],
        "sidecar_sha256": sha256(args.sidecar),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
