"""T-013 staged first-article and independent six-chuanfu Master acceptance."""

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
COMMON = HERE / "six_chuanfu_master_common_v001.py"
CONTRACT = ROOT / "production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json"
TASK = ROOT / "docs/tasks/T-013_P3_1_SIX_CHUANFU_MASTER_BATCH_V002.md"
REGISTRY = ROOT / "production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json"
T011 = ROOT / "production/zhenguo_wanfo/validation/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json"
VALIDATION = ROOT / "production/zhenguo_wanfo/validation"
GATE = VALIDATION / "P3_1_SIX_CHUANFU_FIRST_ARTICLE_VALIDATION_V001.json"
BATCH = VALIDATION / "P3_1_SIX_CHUANFU_MASTER_BATCH_VALIDATION_V001.json"
FONT = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
IDS = ("CMP-FRAME-LOWER-SIX-CHUANFU-001", "CMP-FRAME-UPPER-SIX-CHUANFU-001")
VIEWS = ("FRONT", "SIDE", "TOP", "AXON", "DIMENSION_PARAMETER_SUMMARY", "EVIDENCE_UNCERTAINTY_SUMMARY")
STABLE = ("component_id", "master_id", "master_version", "unit", "object_count", "object_names", "mesh_count", "body", "resolved_parameters", "parameter_semantics", "evidence_classes", "geometry_mode", "geometry_lod", "geometry_semantics", "known_unknowns", "historical_state", "assembly_length_rule", "semantic_geometry_signature")


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
    return {"base": base, "params": base / (component_id + "_MASTER_PARAMS_V001.json"),
            "wrapper": base / "build_six_chuanfu_master_v001.py",
            "asset": base / "asset" / (component_id + "_MASTER_V001.blend"),
            "semantic": base / (component_id + "_MASTER_SEMANTIC_V001.json"),
            "review": review, "review_metadata": review / "REVIEW_PACKAGE_V001.json",
            "validation": VALIDATION / (component_id + "_MASTER_VALIDATION_V001.json")}


def ensure(condition, label, checks):
    checks[label] = "PASS" if condition else "FAIL"
    if not condition:
        raise AssertionError(label)


def git_head_bytes(path):
    return subprocess.check_output(["git", "show", "HEAD:" + rel(path)], cwd=ROOT)


def protected_check():
    tracked = subprocess.check_output(["git", "ls-files", "production/zhenguo_wanfo/component_library/masters",
                                       "production/zhenguo_wanfo/review/P3_1/masters",
                                       "production/zhenguo_wanfo/validation/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json",
                                       "production/zhenguo_wanfo/validation/P3_1_DOU_MASTER_BATCH_VALIDATION_V001.json",
                                       "production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json",
                                       "docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md",
                                       "docs/tasks/T-013_P3_1_SIX_CHUANFU_MASTER_BATCH_V002.md"], cwd=ROOT, text=True).splitlines()
    mismatches = [name for name in tracked if not (ROOT / name).exists() or (ROOT / name).read_bytes() != git_head_bytes(ROOT / name)]
    baseline = read(T011)["p2_frozen_baseline_sha256_after"]
    p2_mismatches = [name for name, sha in baseline.items() if not (ROOT / name).exists() or digest(ROOT / name) != sha]
    registry = read(REGISTRY)
    approved = registry["masters"][:4]
    approved_head = read_from_head(REGISTRY)["masters"][:4]
    binary_mismatches = [row["component_id"] for row in approved_head if not (ROOT / row["local_binary_path"]).exists() or digest(ROOT / row["local_binary_path"]) != row["canonical_asset_sha256"]]
    if mismatches or p2_mismatches or approved != approved_head or binary_mismatches:
        raise RuntimeError("PROTECTED_HASH_MISMATCH " + json.dumps({"tracked": mismatches, "p2": p2_mismatches,
                                                                       "approved_registry": approved != approved_head,
                                                                       "approved_binaries": binary_mismatches}))
    return {"status": "PASS", "protected_tracked_count": len(tracked), "p2_count": len(baseline), "approved_master_count": len(approved_head)}


def read_from_head(path):
    return json.loads(git_head_bytes(path))


def contract_entries():
    contract = read(CONTRACT)
    assert contract["version"] == "V002" and contract["contract_approval_decision"] == "D-036"
    assert contract["status"] == "LOCKED_PRODUCT_OWNER_APPROVED"
    entries = {item["component_id"]: item for item in contract["master_components"]}
    assert all(entries[component_id]["geometry_mode"] == "BOUNDED_LONG_MEMBER_OUTER_ENVELOPE" for component_id in IDS)
    return entries


def parameter_data(component_id, entry, reference_length):
    p = paths(component_id)
    measured = entry["authorized_inputs_mm"]
    assert measured["length"] is None
    assert reference_length > 0
    def parameter(key, value, classification, time_layer, source_layer, production_use, source_ids, replaceable, **extra):
        return {"key": key, "value": value, "unit": "mm", "classification": classification,
                "time_layer": time_layer, "source_layer": source_layer,
                "production_use": production_use, "source_ids": source_ids,
                "replaceable": replaceable, **extra}
    params = [
        parameter("historical_full_length_mm", None, "UNKNOWN", "historical_full_length_unknown", "EVIDENCE_GAP", "DO_NOT_LOCK", ["D-009", "HIS-002"], True, historical_claim=False),
        parameter("canonical_reference_length_mm", reference_length, "PROJECT_RULE", "NON_HISTORICAL_REFERENCE_REALIZATION", "ENGINEERING_REFERENCE", "CANONICAL_REFERENCE_ONLY", ["D-038", "T-013"], True, historical_claim=False),
        parameter("realization_length_mm", reference_length, "PROJECT_RULE", "NON_HISTORICAL_REFERENCE_REALIZATION", "ENGINEERING_EXECUTION", "GEOMETRY_EXECUTION_VALUE", ["D-038", "T-013"], True, historical_claim=False, role="GEOMETRY_EXECUTION_VALUE", derives_from="canonical_reference_length_mm"),
        parameter("width_mm", measured["width"], "CONFIRMED", "observed_as_measured", "DIRECT_PRIMARY", "OBSERVED_REFERENCE_OUTER_ENVELOPE", ["D-009", "SRC-ZG-WF-001"], False),
        parameter("max_thickness_mm", measured["maximum_thickness"], "CONFIRMED", "observed_as_measured", "DIRECT_PRIMARY", "OBSERVED_MAXIMUM_BOUND_ONLY", ["D-009", "SRC-ZG-WF-001"], False),
        parameter("tenon_area_thickness_mm", measured["tenon_area_thickness"], "CONFIRMED", "observed_as_measured", "DIRECT_PRIMARY", "EVIDENCE_METADATA_ONLY", ["D-009", "SRC-ZG-WF-001"], False, geometry_use_count=0),
    ]
    return {"component_id": component_id, "master_id": component_id + "_MASTER", "master_version": "V001",
            "contract_version": "P3_1_MASTER_ASSET_CONTRACT_V002", "contract_decision_id": "D-036", "task_decision_id": "D-038",
            "canonical_name_zh": entry["canonical_name_zh"], "unit": "mm",
            "coordinate_convention": {"handedness": "right_handed", "+X": "member_longitudinal",
                                      "+Y": "section_width", "+Z": "vertical_thickness"},
            "origin_convention": entry["origin"], "canonical_transform": {"location": [0, 0, 0], "rotation": [0, 0, 0], "scale": [1, 1, 1]},
            "geometry_mode": entry["geometry_mode"], "geometry_lod": "EVIDENCE_BOUNDED_MEDIUM_LOD",
            "geometry_semantics": "PROJECT_RULE / BOUNDED_OUTER_ENVELOPE_REFERENCE / REPLACEABLE",
            "parameters": params, "historical_state": {"model_layer": "observed_as_measured_section_plus_non_historical_reference_length",
                                                 "historical_full_length_mm": None, "historical_claim": False,
                                                 "reconstructed_963_candidate": "not_inferred", "report_ideal_model": "separate_not_inferred"},
            "originality_status": "unknown", "originality_parameter_id": "HIS-002",
            "known_unknowns": ["HIS-002: 963 component originality UNKNOWN", "Historical full length UNKNOWN / null",
                               "Maximum thickness is an observed bound, not a proven uniform full-length section",
                               "Tenon-area location/extent, camber, end profile, joinery and hidden connections are not evidenced"],
            "interpretation_boundary": ["Present measured section data are not proven 963 original design.",
                                        "Reference and realization length are non-historical engineering values.",
                                        "Bounded outer envelope does not claim uniform historical section along full member.",
                                        "Tenon-area thickness is metadata only and drives no geometry."],
            "assembly_length_rule": {"hard_fail_id": "REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY",
                                     "requires_explicit_building_specific_approved_length": True,
                                     "default_to_canonical_reference_allowed": False,
                                     "historical_full_length_remains_null": True},
            "unsupported_geometry": [], "p2_primary_frame_proxy_geometry_use_count": 0,
            "reuse_scope": "Replaceable bounded long-member outer-envelope reference; assembly requires separately approved building-specific length.",
            "variant_axes": entry["variant_axes"], "placement_only_attributes": entry["placement_only"],
            "evidence_references": ["docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md",
                                    "docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md", rel(CONTRACT), rel(TASK)],
            "generator_path": rel(p["wrapper"]), "shared_generator_path": rel(COMMON),
            "canonical_asset_path": rel(p["asset"]), "semantic_snapshot_path": rel(p["semantic"]),
            "review_asset_paths": [rel(p["review"] / (view + ".png")) for view in VIEWS]}


def prepare(component_id, entry, reference_length):
    p = paths(component_id)
    p["base"].mkdir(parents=True, exist_ok=True)
    write(p["params"], parameter_data(component_id, entry, reference_length))
    p["wrapper"].write_text('"""Independent ' + component_id + ' T-013 Master build entrypoint."""\n'
                            'import sys\nfrom pathlib import Path\n'
                            'sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))\n'
                            'from six_chuanfu_master_common_v001 import main\n'
                            'if __name__ == "__main__":\n    main()\n')
    return p


def blender(args, marker, loaded_asset=None):
    command = [str(BLENDER), "--background"]
    if loaded_asset:
        command.append(str(loaded_asset))
    command += ["--python", str(args[0]), "--"] + [str(item) for item in args[1:]]
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode or marker not in result.stdout or "Traceback" in result.stdout:
        raise RuntimeError("Blender " + marker + " failed: " + result.stdout[-5000:])
    return result.stdout


def build(p, params=None, asset=None, semantic=None, render=False):
    args = [p["wrapper"], "--mode", "build", "--params", params or p["params"],
            "--asset", asset or p["asset"], "--semantic", semantic or p["semantic"]]
    if render:
        args += ["--review-dir", p["review"]]
    blender(args, "SIX_CHUANFU_BUILD_OK")


def image_font(size):
    return ImageFont.truetype(str(FONT), size)


def annotated_review(p, data):
    p["review"].mkdir(parents=True, exist_ok=True)
    params = {item["key"]: item["value"] for item in data["parameters"]}
    info = PngImagePlugin.PngInfo()
    info.add_text("component_id", data["component_id"])
    info.add_text("geometry_semantics", data["geometry_semantics"])
    info.add_text("historical_full_length_mm", "null")
    info.add_text("canonical_reference_length_mm", str(params["canonical_reference_length_mm"]))
    info.add_text("assembly_length_hard_fail", data["assembly_length_rule"]["hard_fail_id"])
    records = []
    for view in VIEWS:
        output = p["review"] / (view + ".png")
        if view in VIEWS[:4]:
            with Image.open(output) as source:
                im = source.convert("RGB")
            draw = ImageDraw.Draw(im)
            draw.rectangle((0, 0, im.width, 120), fill="#f7f7f5")
            draw.text((25, 16), data["component_id"] + "  /  MASTER V001  /  " + view, font=image_font(28), fill="#202020")
            draw.text((25, 60), "BOUNDED OUTER ENVELOPE REFERENCE  |  NON-HISTORICAL LENGTH", font=image_font(23), fill="#353535")
            draw.rectangle((0, im.height - 86, im.width, im.height), fill="#f7f7f5")
            draw.text((25, im.height - 70), f'L={params["realization_length_mm"]:g} mm reference | W={params["width_mm"]:g} mm | max Z={params["max_thickness_mm"]:g} mm', font=image_font(22), fill="#333333")
            draw.text((25, im.height - 39), "No camber / end detail / local thickness / joinery modeled", font=image_font(19), fill="#555555")
        else:
            im = Image.new("RGB", (1200, 900), "#f7f7f5")
            draw = ImageDraw.Draw(im)
            draw.text((55, 45), data["component_id"], font=image_font(29), fill="#202020")
            draw.text((55, 98), data["canonical_name_zh"] + "  /  MASTER V001  /  " + view, font=image_font(27), fill="#222222")
            if view == "DIMENSION_PARAMETER_SUMMARY":
                lines = [f'Width (measured): {params["width_mm"]:g} mm',
                         f'Max thickness (observed bound): {params["max_thickness_mm"]:g} mm',
                         f'Tenon-area thickness (metadata only): {params["tenon_area_thickness_mm"]:g} mm',
                         f'Canonical reference length: {params["canonical_reference_length_mm"]:g} mm',
                         f'Realization length: {params["realization_length_mm"]:g} mm',
                         'Historical full length: UNKNOWN / null',
                         'Reference length: PROJECT_RULE / ENGINEERING_REFERENCE',
                         'Tenon-area thickness geometry use: 0']
            else:
                lines = ["DIRECT SOURCE: D-009, PDF p81 / printed p66, table 2-38",
                         "Present measured section != proven 963 original design",
                         "HIS-002 component originality: UNKNOWN",
                         "Historical full length: UNKNOWN / null",
                         "Reference specimen length is NON-HISTORICAL / REPLACEABLE",
                         "Maximum thickness is an observed upper bound",
                         "No end profile, camber, local thinning, cavity or joinery",
                         "Assembly requires explicit approved building-specific length"]
            for index, line in enumerate(lines):
                draw.text((65, 190 + index * 70), line, font=image_font(25), fill="#303030")
        im.save(output, pnginfo=info)
        with Image.open(output) as check:
            assert check.info.get("component_id") == data["component_id"] and check.info.get("historical_full_length_mm") == "null"
            assert check.size[0] >= 1200 and check.size[1] >= 900
            check.verify()
        records.append({"view": view, "path": rel(output), "sha256": digest(output), "status": "PASS"})
    write(p["review_metadata"], {"component_id": data["component_id"], "master_version": "V001",
                                  "status": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW", "assets": records,
                                  "geometry_semantics": data["geometry_semantics"],
                                  "historical_full_length_mm": None,
                                  "canonical_reference_length_mm": params["canonical_reference_length_mm"]})
    return records


def validate_one(component_id, entry, p):
    checks = {}
    try:
        data, snap = read(p["params"]), read(p["semantic"])
        values = {item["key"]: item for item in data["parameters"]}
        measured = entry["authorized_inputs_mm"]
        length = float(values["realization_length_mm"]["value"])
        width = float(values["width_mm"]["value"])
        height = float(values["max_thickness_mm"]["value"])
        bbox = snap["body"]["local_bbox_mm"]
        ensure(component_id in IDS and data["component_id"] == snap["component_id"] == entry["component_id"] and data["master_id"] == component_id + "_MASTER", "unique_component_master_id", checks)
        ensure(data["contract_version"] == "P3_1_MASTER_ASSET_CONTRACT_V002" and data["contract_decision_id"] == "D-036" and data["task_decision_id"] == "D-038", "authoritative_contract", checks)
        ensure(all(math.isclose(values[key]["value"], measured[source], abs_tol=1e-5) for key, source in (("width_mm", "width"), ("max_thickness_mm", "maximum_thickness"), ("tenon_area_thickness_mm", "tenon_area_thickness"))) and all("D-009" in values[key]["source_ids"] for key in ("width_mm", "max_thickness_mm", "tenon_area_thickness_mm")), "d009_measured_section_trace", checks)
        ensure(values["historical_full_length_mm"]["value"] is None and snap["resolved_parameters"]["historical_full_length_mm"] is None and snap["historical_state"]["historical_full_length_mm"] is None, "historical_length_null_all_layers", checks)
        ensure(values["historical_full_length_mm"]["classification"] == "UNKNOWN" and values["historical_full_length_mm"]["production_use"] == "DO_NOT_LOCK", "historical_length_unknown_not_locked", checks)
        task_text = TASK.read_text()
        match = re.search(r"canonical_reference_length_mm\s*=\s*([0-9]+(?:\.[0-9]+)?)", task_text)
        ensure(match is not None and values["canonical_reference_length_mm"]["value"] == float(match.group(1)), "approved_reference_length_from_contract", checks)
        ensure(values["canonical_reference_length_mm"]["classification"] == "PROJECT_RULE" and values["canonical_reference_length_mm"]["source_layer"] == "ENGINEERING_REFERENCE" and values["canonical_reference_length_mm"]["time_layer"] == "NON_HISTORICAL_REFERENCE_REALIZATION" and values["canonical_reference_length_mm"]["production_use"] == "CANONICAL_REFERENCE_ONLY" and values["canonical_reference_length_mm"]["historical_claim"] is False, "nonhistorical_reference_semantics", checks)
        ensure(values["realization_length_mm"]["value"] == values["canonical_reference_length_mm"]["value"] and values["realization_length_mm"]["derives_from"] == "canonical_reference_length_mm" and values["realization_length_mm"]["role"] == "GEOMETRY_EXECUTION_VALUE", "realization_explicitly_derived", checks)
        ensure(values["realization_length_mm"]["historical_claim"] is False and data["historical_state"]["historical_claim"] is False and data["historical_state"]["reconstructed_963_candidate"] == "not_inferred", "no_reference_as_historical_claim", checks)
        ensure(bbox["min"] == [-length / 2, -width / 2, 0] and bbox["max"] == [length / 2, width / 2, height] and bbox["dimensions"] == [length, width, height], "bbox_extents_origin_axes", checks)
        ensure(snap["body"]["local_transform"] == data["canonical_transform"] and snap["object_count"] == snap["mesh_count"] == 1, "unit_transform_single_body", checks)
        ensure(snap["body"]["vertex_count"] == 8 and snap["body"]["face_count"] == 6 and snap["body"]["unsupported_detail_count"] == 0 and snap["unsupported_geometry"] == [], "unsupported_geometry_zero", checks)
        ensure(values["max_thickness_mm"]["production_use"] == "OBSERVED_MAXIMUM_BOUND_ONLY" and "not a proven uniform full-length section" in data["known_unknowns"][2], "max_thickness_bound_not_uniform_claim", checks)
        ensure(values["tenon_area_thickness_mm"]["production_use"] == "EVIDENCE_METADATA_ONLY" and values["tenon_area_thickness_mm"]["geometry_use_count"] == snap["tenon_area_geometry_use_count"] == 0, "tenon_metadata_only", checks)
        ensure(data["p2_primary_frame_proxy_geometry_use_count"] == 0 and "P2" not in json.dumps(snap["input_hashes"]), "p2_proxy_geometry_nonuse", checks)
        ensure(data["assembly_length_rule"]["hard_fail_id"] == "REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY" and data["assembly_length_rule"]["requires_explicit_building_specific_approved_length"] is True and data["assembly_length_rule"]["default_to_canonical_reference_allowed"] is False, "assembly_length_leak_hard_fail_carried_forward", checks)
        ensure(data["geometry_semantics"] == "PROJECT_RULE / BOUNDED_OUTER_ENVELOPE_REFERENCE / REPLACEABLE", "bounded_reference_semantics", checks)
        ensure(digest(p["asset"]) == snap["canonical_blend_sha256"] and snap["input_hashes"][rel(p["params"])] == digest(p["params"]), "canonical_hashes", checks)
        source = COMMON.read_text()
        naked = [str(value) for value in measured.values() if value is not None and re.search(r"(?<![\d.])" + re.escape(str(value)) + r"(?![\d.])", source)]
        naked += [str(values["canonical_reference_length_mm"]["value"])] if re.search(r"(?<![\d.])" + re.escape(str(values["canonical_reference_length_mm"]["value"])) + r"(?![\d.])", source) else []
        ensure(not naked, "no_component_or_reference_naked_constants_in_shared_geometry", checks)
        with tempfile.TemporaryDirectory(prefix="t013_" + component_id + "_") as temp:
            work = Path(temp)
            before_hash = digest(p["asset"])
            build(p, asset=work / "regenerated.blend", semantic=work / "regenerated.json")
            regenerated = read(work / "regenerated.json")
            ensure(all(regenerated[key] == snap[key] for key in STABLE) and digest(p["asset"]) == before_hash, "deterministic_regeneration_semantic", checks)
            reopened_path = work / "reopen.json"
            blender([p["wrapper"], "--mode", "inspect", "--asset", p["asset"], "--expected", p["semantic"], "--output", reopened_path], "SIX_CHUANFU_REOPEN_OK", loaded_asset=p["asset"])
            reopen = read(reopened_path)
            ensure(reopen["status"] == "PASS" and reopen["historical_full_length_mm"] is None and reopen["semantic_geometry_signature"] == snap["semantic_geometry_signature"], "independent_reopen", checks)
            mutant = copy.deepcopy(data)
            m = {item["key"]: item for item in mutant["parameters"]}
            alternate_length = length * 1.1
            for key in ("canonical_reference_length_mm", "realization_length_mm"):
                m[key]["value"] = alternate_length
                m[key]["production_use"] = "MUTATION_TEST_ONLY"
                m[key]["source_ids"] = ["T-013-SYNTHETIC-MUTATION"]
            mutation_params = work / "length_params.json"
            write(mutation_params, mutant)
            build(p, params=mutation_params, asset=work / "length.blend", semantic=work / "length.json")
            length_snap = read(work / "length.json")
            length_bbox = length_snap["body"]["local_bbox_mm"]
            ensure(length_snap["resolved_parameters"]["historical_full_length_mm"] is None and length_snap["historical_state"]["historical_full_length_mm"] is None and length_bbox["dimensions"] == [alternate_length, width, height] and length_bbox["min"][0] == -alternate_length / 2 and length_bbox["max"][0] == alternate_length / 2 and length_bbox["min"][1:] == bbox["min"][1:] and length_bbox["max"][1:] == bbox["max"][1:] and length_snap["semantic_geometry_signature"] != snap["semantic_geometry_signature"] and digest(p["asset"]) == before_hash, "length_mutation_x_only_historical_null", checks)
            mutant = copy.deepcopy(data)
            m = {item["key"]: item for item in mutant["parameters"]}
            m["tenon_area_thickness_mm"]["value"] = float(m["tenon_area_thickness_mm"]["value"]) * 1.1
            m["tenon_area_thickness_mm"]["source_layer"] = "SYNTHETIC_TEST"
            m["tenon_area_thickness_mm"]["production_use"] = "MUTATION_TEST_ONLY"
            mutation_params = work / "tenon_params.json"
            write(mutation_params, mutant)
            build(p, params=mutation_params, asset=work / "tenon.blend", semantic=work / "tenon.json")
            tenon_snap = read(work / "tenon.json")
            ensure(tenon_snap["resolved_parameters"]["tenon_area_thickness_mm"] != snap["resolved_parameters"]["tenon_area_thickness_mm"] and tenon_snap["semantic_geometry_signature"] == snap["semantic_geometry_signature"] and tenon_snap["body"] == snap["body"] and tenon_snap["resolved_parameters"]["historical_full_length_mm"] is None and digest(p["asset"]) == before_hash, "tenon_metadata_mutation_geometry_unchanged", checks)
            build(p)
            rebuilt = read(p["semantic"])
            ensure(all(rebuilt[key] == snap[key] for key in STABLE) and rebuilt["canonical_blend_sha256"] == digest(p["asset"]) and read(p["params"]) == data, "canonical_rebuild_after_both_mutations", checks)
            mutation = {"classification": "ENGINEERING_TEST_ONLY", "length": {"baseline_mm": length, "mutated_mm": alternate_length, "x_only": True, "historical_null": True}, "tenon": {"baseline_mm": values["tenon_area_thickness_mm"]["value"], "mutated_mm": m["tenon_area_thickness_mm"]["value"], "geometry_unchanged": True}, "canonical_rebuilt": True, "not_historical_variant": True}
        images = annotated_review(p, data)
        ensure(len(images) == 6 and all(digest(ROOT / item["path"]) == item["sha256"] for item in images), "six_review_assets_machine_checked", checks)
        ensure(not subprocess.check_output(["git", "ls-files", "--", rel(p["asset"])], cwd=ROOT, text=True).strip(), "blend_local_only", checks)
        report = {"task": "T-013", "component_id": component_id, "status": "PASS", "checks": checks,
                  "check_count": len(checks), "review_count": len(images), "blender_version": rebuilt["blender_version"],
                  "canonical_blend_path": rel(p["asset"]), "canonical_blend_sha256": digest(p["asset"]),
                  "semantic_snapshot_path": rel(p["semantic"]), "semantic_geometry_signature": rebuilt["semantic_geometry_signature"],
                  "mutation_evidence": mutation, "reopen_evidence": reopen,
                  "approval_boundary": "ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW"}
        write(p["validation"], report)
        print("SIX_CHUANFU_ASSET_PASS", component_id, len(checks), "checks")
        return report
    except Exception as exc:
        write(p["validation"], {"task": "T-013", "component_id": component_id, "status": "FAIL", "checks": checks, "error": str(exc)})
        raise


def overview():
    first, second = (paths(component_id) for component_id in IDS)
    first_data, second_data = read(first["params"]), read(second["params"])
    first_values = {item["key"]: item["value"] for item in first_data["parameters"]}
    second_values = {item["key"]: item["value"] for item in second_data["parameters"]}
    length = first_values["canonical_reference_length_mm"]
    assert second_values["canonical_reference_length_mm"] == length
    output = ROOT / "production/zhenguo_wanfo/review/P3_1/batches/SIX_CHUANFU_MASTER_BATCH_V001_OVERVIEW.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    blender([COMMON, "--mode", "overview", "--assets", first["asset"], second["asset"],
             "--output", output, "--reference-length", length], "SIX_CHUANFU_OVERVIEW_OK")
    with Image.open(output) as source:
        im = source.convert("RGB")
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, im.width, 135), fill="#f7f7f5")
    draw.text((35, 15), "SIX CHUANFU MASTER BATCH / SAME AXES / TRUE RELATIVE SECTION SCALE", font=image_font(29), fill="#202020")
    draw.text((35, 65), f"LENGTH NORMALIZED TO {length:g} mm — NON-HISTORICAL", font=image_font(31), fill="#202020")
    draw.rectangle((0, im.height - 130, im.width, im.height), fill="#f7f7f5")
    draw.text((35, im.height - 115), "RELATIVE SECTION SCALE IS MEANINGFUL; MEMBER LENGTH IS NOT", font=image_font(31), fill="#202020")
    draw.text((35, im.height - 65), "Lower: W {0:g} / Zmax {1:g} mm     Upper: W {2:g} / Zmax {3:g} mm".format(first_values["width_mm"], first_values["max_thickness_mm"], second_values["width_mm"], second_values["max_thickness_mm"]), font=image_font(25), fill="#404040")
    info = PngImagePlugin.PngInfo()
    info.add_text("component_ids", ",".join(IDS))
    info.add_text("reference_length_mm", str(length))
    info.add_text("relative_scale", "TRUE_1_TO_1_MESH_DIMENSIONS")
    info.add_text("historical_full_lengths", "null,null")
    im.save(output, pnginfo=info)
    with Image.open(output) as check:
        assert check.info.get("component_ids") == ",".join(IDS) and check.info.get("historical_full_lengths") == "null,null"
        assert check.size == (1800, 1100)
        check.verify()
    return {"path": rel(output), "sha256": digest(output), "status": "PASS", "reference_length_mm": length,
            "relative_section_scale": "TRUE_1_TO_1_MESH_DIMENSIONS"}


def register(reports):
    registry = read(REGISTRY)
    approved_head = read_from_head(REGISTRY)["masters"]
    assert registry["masters"] == approved_head and len(approved_head) == 4
    for report in reports:
        component_id = report["component_id"]
        p, data = paths(component_id), read(paths(component_id)["params"])
        registry["masters"].append({"component_id": component_id, "master_id": data["master_id"],
                                    "master_version": "V001", "canonical_asset_status": "LOCAL_ONLY_GENERATED",
                                    "canonical_asset_sha256": report["canonical_blend_sha256"],
                                    "generator_path": rel(p["wrapper"]), "shared_generator_path": rel(COMMON),
                                    "parameter_path": rel(p["params"]), "semantic_snapshot_path": rel(p["semantic"]),
                                    "local_binary_path": rel(p["asset"]), "review_path": rel(p["review"]),
                                    "review_metadata_path": rel(p["review_metadata"]),
                                    "geometry_mode": data["geometry_mode"], "reuse_scope": data["reuse_scope"],
                                    "evidence_references": data["evidence_references"],
                                    "originality_status": "unknown", "known_unknowns": data["known_unknowns"],
                                    "variant_ids": [], "validation_status": "T013_ENGINEERING_PASS",
                                    "approval_status": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW"})
    registry["task"] = "T-013"
    registry["status"] = "FOUR_APPROVED_TWO_FRAME_ENGINEERING_COMPLETE_PENDING_REVIEW"
    # Preserve the approved four records byte-for-byte in the tracked Registry.
    original = git_head_bytes(REGISTRY).decode()
    anchor = '    }\n  ],\n  "phase":'
    assert original.count(anchor) == 1
    additions = []
    for row in registry["masters"][4:]:
        additions.append("\n".join("    " + line for line in json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2).splitlines()))
    updated = original.replace(anchor, '    },\n' + ',\n'.join(additions) + '\n  ],\n  "phase":')
    updated = updated.replace('"status": "COLUMN_D035_DOU_BATCH_D037_APPROVED_4_OF_6"',
                              '"status": "FOUR_APPROVED_TWO_FRAME_ENGINEERING_COMPLETE_PENDING_REVIEW"')
    updated = updated.replace('"task": "T-012"', '"task": "T-013"')
    REGISTRY.write_text(updated)
    actual = read(REGISTRY)
    assert actual["masters"][:4] == approved_head
    assert [row["component_id"] for row in actual["masters"][4:]] == list(IDS)
    assert len({row["component_id"] for row in actual["masters"]}) == len(actual["masters"]) == 6
    assert all(row["approval_status"] == "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW" for row in actual["masters"][4:])
    assert all((ROOT / row[key]).exists() for row in actual["masters"][4:] for key in ("generator_path", "parameter_path", "semantic_snapshot_path", "local_binary_path", "review_metadata_path"))
    return "PASS"


def first_article(entries, reference_length):
    before = protected_check()
    assert len(read(REGISTRY)["masters"]) == 4
    assert not paths(IDS[1])["base"].exists()
    p = prepare(IDS[0], entries[IDS[0]], reference_length)
    build(p, render=True)
    report = validate_one(IDS[0], entries[IDS[0]], p)
    protected_check()
    write(GATE, {"status": "PASS", "component_id": IDS[0], "per_asset_report": rel(p["validation"]),
                 "check_count": report["check_count"], "review_count": report["review_count"],
                 "canonical_blend_sha256": report["canonical_blend_sha256"], "stage_c_authorized": True,
                 "protected_preflight": before})
    print("SIX_CHUANFU_FIRST_ARTICLE_GATE_PASS", IDS[0])


def batch(entries):
    gate = read(GATE)
    assert gate["status"] == "PASS" and gate["component_id"] == IDS[0] and gate["stage_c_authorized"] is True
    first = read(paths(IDS[0])["validation"])
    assert first["status"] == "PASS" and digest(paths(IDS[0])["asset"]) == gate["canonical_blend_sha256"]
    protected_check()
    first_data = read(paths(IDS[0])["params"])
    reference_length = next(item["value"] for item in first_data["parameters"] if item["key"] == "canonical_reference_length_mm")
    p = prepare(IDS[1], entries[IDS[1]], reference_length)
    build(p, render=True)
    second = validate_one(IDS[1], entries[IDS[1]], p)
    assert digest(paths(IDS[0])["asset"]) == gate["canonical_blend_sha256"]
    review = overview()
    registration = register([first, second])
    protection = protected_check()
    assert len({digest(paths(component_id)["asset"]) for component_id in IDS}) == 2
    assert all(read(paths(component_id)["semantic"])["canonical_blend_sha256"] == digest(paths(component_id)["asset"]) for component_id in IDS)
    assert all(read(paths(component_id)["validation"])["status"] == "PASS" for component_id in IDS)
    assert sum(len(read(paths(component_id)["review_metadata"])["assets"]) for component_id in IDS) == 12
    write(BATCH, {"status": "PASS", "task": "T-013", "execution_contract": "P3_1_SIX_CHUANFU_MASTER_BATCH_V002",
                  "contract": "P3_1_MASTER_ASSET_CONTRACT_V002 / D-036", "execution_mode": "CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL + LEAN_PRODUCTION_MODE_V001",
                  "first_article": "PASS", "shared_pipeline": "PASS", "blender_execution_mode": "CLI_BACKGROUND",
                  "blender_version": first["blender_version"],
                  "components": [{"component_id": item["component_id"], "validation_path": rel(paths(item["component_id"])["validation"]),
                                  "canonical_blend_path": item["canonical_blend_path"],
                                  "canonical_blend_sha256": item["canonical_blend_sha256"],
                                  "semantic_snapshot_path": item["semantic_snapshot_path"],
                                  "check_count": item["check_count"], "review_count": item["review_count"]} for item in (first, second)],
                  "review_count": 12, "overview": review, "registry_registration": registration,
                  "protected_hashes": protection, "approved_four_preserved": True,
                  "p2_frozen_baseline_preserved": True, "contract_v002_preserved": True,
                  "extra_masters_produced": False, "unexplained_validation_errors": [],
                  "approval_boundary": "PENDING_CHATGPT_PRODUCT_OWNER_REVIEW; not P3.1 PASS"})
    print("SIX_CHUANFU_BATCH_PASS", "2 masters 12 reviews + overview")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("first-article", "batch"))
    parser.add_argument("--reference-length-mm", type=float)
    args = parser.parse_args()
    assert BLENDER.exists() and COMMON.exists() and FONT.exists()
    entries = contract_entries()
    if args.stage == "first-article":
        assert args.reference_length_mm is not None
        first_article(entries, args.reference_length_mm)
    else:
        batch(entries)


if __name__ == "__main__":
    main()
