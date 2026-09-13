"""T-012 V002 first-article gate and shared, independent dou Master acceptance."""

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BLENDER = Path("/Applications/Blender.app/Contents/MacOS/Blender")
COMMON = HERE / "dou_master_common_v001.py"
CONTRACT = ROOT / "production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json"
REGISTRY = ROOT / "production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json"
REPORT_DIR = ROOT / "production/zhenguo_wanfo/validation"
FIRST_GATE = REPORT_DIR / "P3_1_DOU_FIRST_ARTICLE_VALIDATION_V001.json"
BATCH_REPORT = REPORT_DIR / "P3_1_DOU_MASTER_BATCH_VALIDATION_V001.json"
BASELINE = Path("/tmp/t012_protected_before.json")
T011 = REPORT_DIR / "P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json"
FONT = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
IDS = ("CMP-LUDOU-COLUMN-001", "CMP-DOU-SINGLE-LONGKAI-001", "CMP-DOU-INTERACTIVE-001")
NUMERIC = ("top_width_mm", "bottom_width_mm", "top_depth_mm", "bottom_depth_mm", "total_height_mm")
VIEWS = ("FRONT", "SIDE", "TOP", "AXON", "DIMENSION_PARAMETER_SUMMARY", "EVIDENCE_UNCERTAINTY_SUMMARY")
STABLE = ("component_id", "master_id", "master_version", "unit", "object_count", "object_names", "mesh_count", "body", "sections_mm", "resolved_parameters", "evidence_classes", "geometry_mode", "geometry_lod", "known_unknowns", "originality_status", "historical_state", "semantic_geometry_signature")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path):
    return str(Path(path).relative_to(ROOT))


def paths(component_id):
    base = ROOT / "production/zhenguo_wanfo/component_library/masters" / component_id
    review = ROOT / "production/zhenguo_wanfo/review/P3_1/masters" / component_id
    return {
        "base": base, "params": base / (component_id + "_MASTER_PARAMS_V001.json"),
        "wrapper": base / "build_dou_master_v001.py", "asset": base / "asset" / (component_id + "_MASTER_V001.blend"),
        "semantic": base / (component_id + "_MASTER_SEMANTIC_V001.json"),
        "review": review, "review_metadata": review / "REVIEW_PACKAGE_V001.json",
        "validation": REPORT_DIR / (component_id + "_MASTER_VALIDATION_V001.json"),
    }


def required_contract():
    contract = read(CONTRACT)
    assert contract["version"] == "V002" and contract["contract_approval_decision"] == "D-036"
    assert contract["status"] == "LOCKED_PRODUCT_OWNER_APPROVED"
    entries = {entry["component_id"]: entry for entry in contract["master_components"]}
    assert all(component_id in entries for component_id in IDS)
    return contract, entries


def parameter_data(component_id, entry):
    base = paths(component_id)
    direct = {"CMP-LUDOU-COLUMN-001": "D-007", "CMP-DOU-SINGLE-LONGKAI-001": "D-008", "CMP-DOU-INTERACTIVE-001": "D-008"}[component_id]
    item_params = []
    for field, value in entry["authorized_inputs_mm"].items():
        key = field + "_mm"
        metadata = key in ("flat_height_mm", "sloped_height_mm")
        item_params.append({
            "key": key, "value": value, "unit": "mm", "classification": "CONFIRMED",
            "time_layer": "observed_as_measured", "source_layer": "DIRECT_PRIMARY",
            "production_use": "EVIDENCE_METADATA_ONLY_FOR_CURRENT_ENVELOPE" if metadata else "OBSERVED_REFERENCE_OUTER_ENVELOPE",
            "source_ids": [direct, "SRC-ZG-WF-001"], "replaceable": False,
        })
    reviews = [rel(base["review"] / (view + ".png")) for view in VIEWS]
    data = {
        "component_id": component_id, "master_id": component_id + "_MASTER", "master_version": "V001",
        "contract_version": "P3_1_MASTER_ASSET_CONTRACT_V002", "contract_decision_id": "D-036",
        "canonical_reference_status": "CURRENT_MEASURED_REFERENCE_REALIZATION_FOR_REVIEW",
        "canonical_name_zh": entry["canonical_name_zh"], "unit": "mm",
        "coordinate_convention": {"handedness": "right_handed", "+X": "canonical_width", "+Y": "canonical_depth", "+Z": "gravity_up_height"},
        "origin_convention": "bottom_footprint_center",
        "canonical_transform": {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]},
        "geometry_mode": entry["geometry_mode"], "geometry_lod": "EVIDENCE_BOUNDED_MEDIUM_LOD",
        "interpolation": "PROJECT_RULE / REPLACEABLE_ENGINEERING_INTERPOLATION",
        "parameters": item_params,
        "historical_state": {"model_layer": "observed_as_measured", "historical_claim": "not_proven_963_design",
                             "report_ideal_model": "separate_not_inferred", "reconstructed_963_candidate": "not_inferred"},
        "originality_status": "unknown", "originality_parameter_id": "HIS-002",
        "dg114_status": "UNKNOWN_NO_UNIFIED_SMALL_DOU_RULE", "dg114_geometry_use_count": 0,
        "known_unknowns": ["HIS-002: 963 component originality unknown", "DG-114: unified small-dou rule UNKNOWN and unused",
                           "Current measurements can include replacement, compression, wear and deformation",
                           "Ears, notches, cavities, mortise-tenon and hidden connections lack quantified evidence"],
        "interpretation_boundary": ["Current measured dimensions are not proven 963 original design.",
                                    "Linear outer envelope loft is replaceable engineering interpolation, not a historical profile claim.",
                                    "No name-driven slots, ears, cavities or joinery are modeled."],
        "unsupported_geometry": [], "reuse_scope": "Evidence-bounded measured dou outer-envelope reference; replace upon stronger evidence.",
        "variant_axes": entry["variant_axes"], "placement_only_attributes": entry["placement_only"],
        "evidence_references": ["docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md",
                                "docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md",
                                rel(CONTRACT)],
        "generator_path": rel(base["wrapper"]), "shared_generator_path": rel(COMMON),
        "canonical_asset_path": rel(base["asset"]), "semantic_snapshot_path": rel(base["semantic"]),
        "review_asset_paths": reviews,
    }
    return data


def prepare(component_id, entry):
    p = paths(component_id)
    p["base"].mkdir(parents=True, exist_ok=True)
    data = parameter_data(component_id, entry)
    write(p["params"], data)
    p["wrapper"].write_text('"""Independent entrypoint for ' + component_id + '; shared T-012 dou pipeline."""\n'
                            'import sys\nfrom pathlib import Path\n'
                            'sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))\n'
                            'from dou_master_common_v001 import main\n'
                            'if __name__ == "__main__":\n    main()\n')
    return p


def blender(args, marker, loaded_asset=None):
    command = [str(BLENDER), "--background"]
    if loaded_asset:
        command.append(str(loaded_asset))
    command += ["--python", str(args[0]), "--"] + [str(x) for x in args[1:]]
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode or marker not in result.stdout or "Traceback" in result.stdout:
        raise RuntimeError("Blender " + marker + " failed: " + result.stdout[-4500:])
    return result.stdout


def build(p, params=None, asset=None, semantic=None, render=False):
    params = params or p["params"]
    asset = asset or p["asset"]
    semantic = semantic or p["semantic"]
    args = [p["wrapper"], "--mode", "build", "--params", params, "--asset", asset, "--semantic", semantic]
    if render:
        args += ["--review-dir", p["review"]]
    blender(args, "DOU_MASTER_BUILD_OK")


def ensure(condition, label, checks):
    checks[label] = "PASS" if condition else "FAIL"
    if not condition:
        raise AssertionError(label)


def font(size):
    return ImageFont.truetype(str(FONT), size)


def png_info(component_id, view):
    info = PngImagePlugin.PngInfo()
    info.add_text("component_id", component_id)
    info.add_text("master_version", "V001")
    info.add_text("view", view)
    return info


def label_view(path, component_id, view, data):
    with Image.open(path) as source:
        im = source.convert("RGB")
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, im.width, 95), fill="#f7f7f5")
    draw.text((36, 22), component_id + "  /  MASTER V001  /  " + view, font=font(28), fill="#242424")
    draw.rectangle((0, im.height - 82, im.width, im.height), fill="#f7f7f5")
    vals = {item["key"]: item["value"] for item in data["parameters"]}
    line = f'TOP {vals["top_width_mm"]:.1f} × {vals["top_depth_mm"]:.1f}  |  BOTTOM {vals["bottom_width_mm"]:.1f} × {vals["bottom_depth_mm"]:.1f}  |  H {vals["total_height_mm"]:.1f} mm'
    draw.text((35, im.height - 60), line, font=font(23), fill="#323232")
    im.save(path, pnginfo=png_info(component_id, view))


def text_sheet(data, view, path):
    component_id = data["component_id"]
    im = Image.new("RGB", (1400, 1000), "#f7f7f5")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1400, 18), fill="#626262")
    d.text((78, 54), component_id + "  /  MASTER V001", font=font(29), fill="#575757")
    title = "尺寸与参数 / DIMENSIONS" if view == "DIMENSION_PARAMETER_SUMMARY" else "证据与不确定性 / EVIDENCE"
    d.text((78, 122), title, font=font(47), fill="#252525")
    d.line((78, 220, 1320, 220), fill="#c9c9c9", width=3)
    vals = {item["key"]: item["value"] for item in data["parameters"]}
    if view == "DIMENSION_PARAMETER_SUMMARY":
        lines = [
            f'TOP / 上口: width {vals["top_width_mm"]:.1f} mm   depth {vals["top_depth_mm"]:.1f} mm',
            f'BOTTOM / 下口: width {vals["bottom_width_mm"]:.1f} mm   depth {vals["bottom_depth_mm"]:.1f} mm',
            f'HEIGHT / 总高: {vals["total_height_mm"]:.1f} mm',
            "Local origin: bottom footprint center, Z = 0",
            "+X width  /  +Y depth  /  +Z height",
            "Location (0,0,0)  /  Rotation (0,0,0)  /  Scale (1,1,1)",
            "Outer envelope: centered rectangular linear loft, replaceable",
        ]
        if "flat_height_mm" in vals:
            lines.insert(3, f'Flat {vals["flat_height_mm"]:.2f} mm / sloped {vals["sloped_height_mm"]:.1f} mm: metadata only')
    else:
        lines = [
            "D-007 / D-008: present measured dimensions, DIRECT_VERIFIED",
            "CURRENT MEASURED does not prove the original 963 design.",
            "HIS-002: component originality UNKNOWN.",
            "DG-114: unified small-dou rule UNKNOWN; geometry use = 0.",
            "Replacement, compression, wear or deformation may affect sizes.",
            "Linear loft = replaceable engineering interpolation.",
            "No invented ears, notches, cavities, slots or mortise-tenon.",
            "Observed, report-ideal and reconstructed layers remain separate.",
        ]
    for index, line in enumerate(lines):
        y = 285 + index * 75
        d.rounded_rectangle((78, y - 12, 1320, y + 55), radius=12, fill="white", outline="#ddddda", width=2)
        d.text((104, y), line, font=font(27), fill="#353535")
    d.text((78, 938), "P3_1_MASTER_ASSET_CONTRACT_V002 / D-036  ·  T-012", font=font(23), fill="#777777")
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, pnginfo=png_info(component_id, view))


def review_package(p, data):
    for view in VIEWS[:4]:
        label_view(p["review"] / (view + ".png"), data["component_id"], view, data)
    for view in VIEWS[4:]:
        text_sheet(data, view, p["review"] / (view + ".png"))
    images = []
    for view in VIEWS:
        path = p["review"] / (view + ".png")
        with Image.open(path) as im:
            assert im.info.get("component_id") == data["component_id"] and im.info.get("view") == view
            width, height = im.size
            im.verify()
        assert width >= 900 and height >= 900
        images.append({"view": view, "path": rel(path), "width": width, "height": height, "sha256": digest(path)})
    write(p["review_metadata"], {"component_id": data["component_id"], "master_version": "V001", "status": "ENGINEERING_REVIEW_READY",
                                  "geometry_color": "neutral_grey", "orthographic_views": list(VIEWS[:4]),
                                  "visual_review_status": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW", "images": images,
                                  "interpretation_boundary": data["interpretation_boundary"]})
    return images


def validate_one(component_id, entry, p):
    checks = {}
    try:
        data = read(p["params"])
        original = read(p["semantic"])
        params = {item["key"]: item for item in data["parameters"]}
        values = {key: params[key]["value"] for key in NUMERIC}
        authoritative = {key + "_mm": value for key, value in entry["authorized_inputs_mm"].items()}
        registry_ids = [read(REGISTRY)["masters"][0]["component_id"]] + list(IDS)
        ensure(len(set(registry_ids)) == len(registry_ids) and data["component_id"] == component_id and data["master_id"] == component_id + "_MASTER", "unique_component_master_identity", checks)
        ensure(data["contract_version"] == "P3_1_MASTER_ASSET_CONTRACT_V002" and data["contract_decision_id"] == "D-036", "contract_v002_d036", checks)
        required = {"component_id", "master_id", "master_version", "unit", "coordinate_convention", "origin_convention", "canonical_transform", "parameters", "geometry_mode", "known_unknowns", "interpretation_boundary", "historical_state", "originality_status", "reuse_scope", "variant_axes", "placement_only_attributes", "generator_path", "canonical_asset_path", "review_asset_paths"}
        item_required = {"key", "value", "unit", "classification", "time_layer", "source_layer", "production_use", "source_ids", "replaceable"}
        ensure(required <= data.keys() and all(item_required <= item.keys() for item in data["parameters"]) and all(key in params for key in NUMERIC), "required_fields_complete", checks)
        ensure(data["unit"] == "mm" and data["coordinate_convention"] == {"handedness": "right_handed", "+X": "canonical_width", "+Y": "canonical_depth", "+Z": "gravity_up_height"} and data["origin_convention"] == "bottom_footprint_center", "unit_axes_origin", checks)
        ensure(data["canonical_transform"] == {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]} and original["body"]["local_transform"] == {"location": [0.0]*3, "rotation": [0.0]*3, "scale": [1.0]*3}, "transform_scale_one", checks)
        ensure(original["object_count"] == 1 and original["mesh_count"] == 1 and original["body"]["vertex_count"] == 8 and original["body"]["face_count"] == 6, "one_simple_closed_body", checks)
        ensure(not any(key in data or key in original for key in ("world_position", "grid_position", "bay_index", "instance_rotation", "world_rotation")), "no_world_placement", checks)
        ensure(all(math.isclose(params[key]["value"], authoritative[key], abs_tol=1e-8) for key in authoritative) and set(authoritative) == set(params), "contract_dimension_mapping", checks)
        if component_id == IDS[0]:
            ensure(values["bottom_width_mm"] == authoritative["bottom_width_mm"] and values["top_depth_mm"] == authoritative["top_depth_mm"] and values["bottom_width_mm"] != values["top_depth_mm"], "ludou_v002_field_mapping", checks)
            ensure(params["flat_height_mm"]["production_use"] == "EVIDENCE_METADATA_ONLY_FOR_CURRENT_ENVELOPE" and params["sloped_height_mm"]["production_use"] == "EVIDENCE_METADATA_ONLY_FOR_CURRENT_ENVELOPE", "flat_sloped_metadata_only", checks)
        sections = original["sections_mm"]
        ensure(math.isclose(sections["bottom"]["width"], values["bottom_width_mm"], abs_tol=0.001) and math.isclose(sections["bottom"]["depth"], values["bottom_depth_mm"], abs_tol=0.001), "bottom_section", checks)
        ensure(math.isclose(sections["top"]["width"], values["top_width_mm"], abs_tol=0.001) and math.isclose(sections["top"]["depth"], values["top_depth_mm"], abs_tol=0.001), "top_section", checks)
        ensure(math.isclose(sections["mid"]["width"], (values["bottom_width_mm"] + values["top_width_mm"])/2, abs_tol=0.001) and math.isclose(sections["mid"]["depth"], (values["bottom_depth_mm"] + values["top_depth_mm"])/2, abs_tol=0.001), "mid_linear_section", checks)
        bbox = original["body"]["local_bbox_mm"]
        ensure(all(math.isclose(bbox["dimensions"][i], target, abs_tol=0.001) for i, target in enumerate((values["top_width_mm"], values["top_depth_mm"], values["total_height_mm"]))) and bbox["min"][2] == 0, "bbox_total_height", checks)
        ensure(data["canonical_reference_status"] == "CURRENT_MEASURED_REFERENCE_REALIZATION_FOR_REVIEW" and data["historical_state"]["historical_claim"] == "not_proven_963_design" and all(params[key]["time_layer"] == "observed_as_measured" for key in NUMERIC), "current_measured_not_proven_963", checks)
        ensure(data["originality_status"] == "unknown" and data["originality_parameter_id"] == "HIS-002", "his002_originality_unknown", checks)
        ensure(data["dg114_geometry_use_count"] == 0 and original["dg114_geometry_use_count"] == 0 and data["dg114_status"] == "UNKNOWN_NO_UNIFIED_SMALL_DOU_RULE", "dg114_non_use", checks)
        ensure(data["unsupported_geometry"] == [] and original["body"]["unsupported_detail_count"] == 0 and original["body"]["primitive"] == "closed_centered_rectangular_linear_outer_envelope", "unsupported_detail_zero", checks)
        ensure(data["interpolation"] == "PROJECT_RULE / REPLACEABLE_ENGINEERING_INTERPOLATION" and original["interpolation"] == data["interpolation"], "name_independent_replaceable_loft", checks)
        code = COMMON.read_text() + p["wrapper"].read_text() + Path(__file__).read_text()
        naked = [str(value) for value in authoritative.values() if re.search(r"(?<![\d.])" + re.escape(str(value)) + r"(?![\d.])", code)]
        ensure(not naked, "naked_historical_constant_scan", checks)
        ensure(p["asset"].exists() and original["canonical_blend_sha256"] == digest(p["asset"]), "canonical_binary_hash", checks)
        ensure(original["input_hashes"][rel(p["params"])] == digest(p["params"]) and original["input_hashes"][rel(p["wrapper"])] == digest(p["wrapper"]) and original["input_hashes"][rel(COMMON)] == digest(COMMON), "input_hashes", checks)
        with tempfile.TemporaryDirectory(prefix="t012_dou_") as temporary:
            work = Path(temporary)
            regen_asset, regen_semantic = work / "regen.blend", work / "regen.json"
            build(p, asset=regen_asset, semantic=regen_semantic)
            regen = read(regen_semantic)
            ensure(all(regen[key] == original[key] for key in STABLE), "deterministic_regeneration", checks)
            mutated = copy.deepcopy(data)
            mutable = {item["key"]: item for item in mutated["parameters"]}
            mutable["top_width_mm"]["value"] += 10.0
            mutable["top_width_mm"]["classification"] = "ENGINEERING_TEST_ONLY"
            mutable["top_width_mm"]["time_layer"] = "engineering_test"
            mutable["top_width_mm"]["source_layer"] = "SYNTHETIC"
            mutable["top_width_mm"]["production_use"] = "MUTATION_TEST_ONLY"
            mutable["top_width_mm"]["source_ids"] = ["T-012-SYNTHETIC-MUTATION"]
            mutated["canonical_reference_status"] = "ENGINEERING_TEST_ONLY"
            mutation_params, mutation_asset, mutation_semantic = work / "mutation_params.json", work / "mutation.blend", work / "mutation.json"
            write(mutation_params, mutated)
            before_hash = digest(p["asset"])
            build(p, params=mutation_params, asset=mutation_asset, semantic=mutation_semantic)
            mutation = read(mutation_semantic)
            ensure(mutation["semantic_geometry_signature"] != original["semantic_geometry_signature"] and math.isclose(mutation["sections_mm"]["top"]["width"] - sections["top"]["width"], 10.0, abs_tol=0.001) and mutation["sections_mm"]["bottom"] == sections["bottom"] and digest(p["asset"]) == before_hash and digest(p["params"]) == original["input_hashes"][rel(p["params"])], "synthetic_mutation_isolated", checks)
            build(p)
            rebuilt = read(p["semantic"])
            ensure(all(rebuilt[key] == original[key] for key in STABLE) and rebuilt["canonical_blend_sha256"] == digest(p["asset"]), "canonical_rebuild_after_mutation", checks)
            reopen_output = work / "reopen.json"
            blender([p["wrapper"], "--mode", "inspect", "--asset", p["asset"], "--expected", p["semantic"], "--output", reopen_output], "DOU_MASTER_REOPEN_OK", loaded_asset=p["asset"])
            reopened = read(reopen_output)
            ensure(reopened["status"] == "PASS" and reopened["component_id"] == component_id and reopened["semantic_geometry_signature"] == rebuilt["semantic_geometry_signature"], "independent_reopen", checks)
            mutation_evidence = {"classification": "ENGINEERING_TEST_ONLY", "parameter": "top_width_mm", "baseline_mm": values["top_width_mm"], "mutated_mm": mutable["top_width_mm"]["value"], "baseline_signature": original["semantic_geometry_signature"], "mutated_signature": mutation["semantic_geometry_signature"], "canonical_unchanged_during_mutation": True, "canonical_rebuilt": True, "not_historical_variant": True}
        images = review_package(p, data)
        ensure(len(images) == 6 and all(image["sha256"] == digest(ROOT / image["path"]) for image in images), "six_review_assets_machine_checked", checks)
        ensure(not subprocess.check_output(["git", "ls-files", "--", rel(p["asset"])], cwd=ROOT, text=True).strip(), "blend_local_only", checks)
        report = {"task": "T-012", "contract": "P3_1_MASTER_ASSET_CONTRACT_V002 / D-036", "component_id": component_id, "status": "PASS", "blender_version": rebuilt["blender_version"], "canonical_blend_path": rel(p["asset"]), "canonical_blend_sha256": digest(p["asset"]), "semantic_snapshot_path": rel(p["semantic"]), "semantic_geometry_signature": rebuilt["semantic_geometry_signature"], "checks": checks, "check_count": len(checks), "review_count": len(images), "mutation_evidence": mutation_evidence, "reopen_evidence": reopened, "approval_boundary": "ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW"}
        write(p["validation"], report)
        print("DOU_ASSET_PASS", component_id, len(checks), "checks")
        return report
    except Exception as exc:
        write(p["validation"], {"task": "T-012", "component_id": component_id, "status": "FAIL", "checks": checks, "error": str(exc)})
        raise


def protected_check():
    before = read(BASELINE)
    mismatches = [path for path, hash_value in before.items() if not (ROOT / path).exists() or digest(ROOT / path) != hash_value]
    t011 = read(T011)
    p2 = t011["p2_frozen_baseline_sha256_after"]
    p2_mismatches = [path for path, hash_value in p2.items() if not (ROOT / path).exists() or digest(ROOT / path) != hash_value]
    if mismatches or p2_mismatches:
        raise RuntimeError("PROTECTED_HASH_MISMATCH: " + json.dumps({"protected": mismatches, "p2": p2_mismatches}))
    return {"protected_count": len(before), "p2_count": len(p2), "status": "PASS"}


def overview():
    output = ROOT / "production/zhenguo_wanfo/review/P3_1/batches/DOU_MASTER_BATCH_V001_OVERVIEW.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    assets = [paths(component_id)["asset"] for component_id in IDS]
    blender([COMMON, "--mode", "overview", "--assets", *assets, "--output", output], "DOU_OVERVIEW_OK")
    with Image.open(output) as source:
        im = source.convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1800, 100), fill="#f7f7f5")
    d.text((42, 28), "DOU MASTER BATCH V001  /  SAME AXES + TRUE RELATIVE SCALE", font=font(30), fill="#252525")
    d.rectangle((0, 950, 1800, 1100), fill="#f7f7f5")
    labels = [(60, IDS[0]), (625, IDS[1]), (1170, IDS[2])]
    for xpos, label in labels:
        d.text((xpos, 975), label, font=font(22), fill="#333333")
    d.text((60, 1030), "Measured outer envelopes  ·  linear interpolation replaceable  ·  no proven 963 profile", font=font(23), fill="#555555")
    info = PngImagePlugin.PngInfo()
    info.add_text("component_ids", ",".join(IDS))
    info.add_text("relative_scale", "TRUE_1_TO_1_MESH_DIMENSIONS")
    im.save(output, pnginfo=info)
    with Image.open(output) as check:
        assert check.size == (1800, 1100) and check.info.get("component_ids") == ",".join(IDS)
        check.verify()
    return {"path": rel(output), "sha256": digest(output), "status": "PASS"}


def register(reports):
    registry = read(REGISTRY)
    column = copy.deepcopy(registry["masters"][0])
    assert column["component_id"] == "CMP-COLUMN-001" and len(registry["masters"]) == 1
    for report in reports:
        component_id = report["component_id"]
        p = paths(component_id)
        data = read(p["params"])
        registry["masters"].append({
            "component_id": component_id, "master_id": data["master_id"], "master_version": "V001",
            "canonical_asset_status": "LOCAL_ONLY_GENERATED", "canonical_asset_sha256": report["canonical_blend_sha256"],
            "generator_path": rel(p["wrapper"]), "shared_generator_path": rel(COMMON),
            "parameter_path": rel(p["params"]), "semantic_snapshot_path": rel(p["semantic"]),
            "local_binary_path": rel(p["asset"]), "review_path": rel(p["review"]),
            "review_metadata_path": rel(p["review_metadata"]), "geometry_mode": data["geometry_mode"],
            "reuse_scope": data["reuse_scope"], "evidence_references": data["evidence_references"],
            "originality_status": "unknown", "known_unknowns": data["known_unknowns"], "variant_ids": [],
            "validation_status": "T012_ENGINEERING_PASS", "approval_status": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
        })
    registry["task"] = "T-012"
    registry["status"] = "COLUMN_APPROVED_D035_DOU_BATCH_ENGINEERING_COMPLETE_PENDING_REVIEW"
    write(REGISTRY, registry)
    actual = read(REGISTRY)
    assert actual["masters"][0] == column
    assert [row["component_id"] for row in actual["masters"]] == ["CMP-COLUMN-001", *IDS]
    assert all(row["approval_status"] == "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW" for row in actual["masters"][1:])
    assert all((ROOT / row[key]).exists() for row in actual["masters"][1:] for key in ("generator_path", "parameter_path", "semantic_snapshot_path", "local_binary_path", "review_metadata_path"))
    return "PASS"


def first_article(entries):
    protected_check()
    p = prepare(IDS[0], entries[IDS[0]])
    build(p, render=True)
    result = validate_one(IDS[0], entries[IDS[0]], p)
    protected_check()
    write(FIRST_GATE, {"status": "PASS", "component_id": IDS[0], "per_asset_report": rel(p["validation"]), "check_count": result["check_count"], "review_count": result["review_count"], "canonical_blend_sha256": result["canonical_blend_sha256"], "stage_c_authorized": True})
    print("FIRST_ARTICLE_GATE_PASS", IDS[0])


def batch(entries):
    gate = read(FIRST_GATE)
    assert gate["status"] == "PASS" and gate["component_id"] == IDS[0] and gate["stage_c_authorized"] is True
    first = read(paths(IDS[0])["validation"])
    assert first["status"] == "PASS" and digest(paths(IDS[0])["asset"]) == gate["canonical_blend_sha256"]
    protected_check()
    reports = [first]
    for component_id in IDS[1:]:
        p = prepare(component_id, entries[component_id])
        build(p, render=True)
        reports.append(validate_one(component_id, entries[component_id], p))
    assert digest(paths(IDS[0])["asset"]) == gate["canonical_blend_sha256"]
    review = overview()
    registered = register(reports)
    protection = protected_check()
    assert all(read(paths(component_id)["validation"])["status"] == "PASS" for component_id in IDS)
    assert all(read(paths(component_id)["semantic"])["canonical_blend_sha256"] == digest(paths(component_id)["asset"]) for component_id in IDS)
    assert len({digest(paths(component_id)["asset"]) for component_id in IDS}) == 3
    assert not any((ROOT / "production/zhenguo_wanfo/component_library/masters" / item).exists() for item in ("CMP-FRAME-LOWER-SIX-CHUANFU-001", "CMP-FRAME-UPPER-SIX-CHUANFU-001"))
    result = {"status": "PASS", "task": "T-012", "execution_contract": "P3_1_DOU_MASTER_BATCH_V002", "contract": "P3_1_MASTER_ASSET_CONTRACT_V002 / D-036", "execution_mode": "LEAN_PRODUCTION_MODE_V001", "first_article": "PASS", "shared_pipeline": "PASS", "blender_execution_mode": "CLI_BACKGROUND", "blender_version": reports[0]["blender_version"], "components": [{"component_id": item["component_id"], "validation_path": rel(paths(item["component_id"])["validation"]), "canonical_blend_path": item["canonical_blend_path"], "canonical_blend_sha256": item["canonical_blend_sha256"], "semantic_snapshot_path": item["semantic_snapshot_path"], "check_count": item["check_count"], "review_count": item["review_count"]} for item in reports], "review_count": 18, "overview": review, "registry_registration": registered, "protected_hashes": protection, "approved_column_preserved": True, "frame_masters_produced": False, "unexplained_validation_errors": [], "approval_boundary": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW; not P3.1 PASS"}
    write(BATCH_REPORT, result)
    print("DOU_BATCH_PASS", len(reports), "masters", result["review_count"], "review PNGs + overview")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("first-article", "batch"))
    stage = parser.parse_args().stage
    assert BLENDER.exists() and COMMON.exists() and BASELINE.exists()
    _, entries = required_contract()
    if stage == "first-article":
        first_article(entries)
    else:
        batch(entries)


if __name__ == "__main__":
    main()
