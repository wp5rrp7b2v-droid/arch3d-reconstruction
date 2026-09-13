#!/usr/bin/env python3
"""Deterministic P2 -> P3.0 semantic migration. Never opens or writes Blender files."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
BASE = Path("production/zhenguo_wanfo")
DOC = Path("docs/production/zhenguo_wanfo")
MANIFEST = BASE / "build/P2_3_INTEGRATION_MANIFEST_V001.json"
PARAMETERS = BASE / "params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
OVERRIDES = BASE / "params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json"
MATRIX = BASE / "dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json"
EVIDENCE_SCHEMA = BASE / "schema/evidence_aware_parameter_schema_v001.json"
ONTOLOGY_JSON = BASE / "registry/P3_0_COMPONENT_ONTOLOGY_V001.json"
SCHEMA_JSON = BASE / "registry/P3_0_COMPONENT_REGISTRY_SCHEMA_V001.json"
AUDIT_JSON = BASE / "registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json"
REGISTRY_JSON = BASE / "registry/P3_0_COMPONENT_REGISTRY_V001.json"
REPORT_JSON = BASE / "validation/P3_0_REGISTRY_VALIDATION_REPORT_V001.json"
ONTOLOGY_MD = DOC / "P3_0_COMPONENT_ONTOLOGY_V001.md"
AUDIT_MD = DOC / "P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md"
REPORT_MD = DOC / "P3_0_REGISTRY_VALIDATION_REPORT_V001.md"

SOURCE_REGISTER = "docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md"
DIRECT_REVIEW = "docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md"
P1_CLASSIFICATION = "docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md"
P1_GATE = "docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md"
P2_AUDIT = str(AUDIT_MD)
SOURCE_ID = "SRC-ZG-WF-001"
HISTORICAL_TERMS = {
    "COLUMN": ["柱", "檐柱", "角柱"],
    "PURLIN": ["槫", "撩风槫", "下平槫", "上平槫", "脊槫"],
    "RAFTER": ["椽", "檐椽", "飞椽"],
}

RELATIONS = [
    "supports", "supported_by", "connects_to", "inserted_into", "receives",
    "rests_on", "spans_between", "aligned_with", "repeated_in",
    "belongs_to_assembly", "located_at", "orientation",
]
ONTOLOGY_TYPES = [
    "HISTORICAL_COMPONENT", "ASSEMBLY_UNIT", "GEOMETRIC_PROXY",
    "CONTROL_OBJECT", "ENVELOPE_SURFACE", "UNKNOWN_UNRESOLVED_COMPONENT",
]

# These decisions are intentionally explicit and reviewable. No historical member is
# inferred from the shape of an engineering mesh.
FAMILIES = {
    "BRACKET_ARM": dict(id="PRX-BRACKET-JUMP-001", zh="未定铺作出跳代理", en="unresolved_bracket_jump_proxy", type="UNKNOWN_UNRESOLVED_COMPONENT", role="GEOMETRIC_PROXY", concept=False, real=None, change="保留代理；后续按实证拆分栱、昂及铺作组合，不把四跳均分网格当成构件。", function="表达斗栱出跳总体拓扑", structural="图示出跳，不代表单根受力构件", position="外檐铺作出跳", refs=[P1_CLASSIFICATION, DIRECT_REVIEW], unknown="DG-110～113 只控制总体出跳；45°构件、栱昂分件、榫卯未定。"),
    "BRACKET_CONTACT": dict(id="PRX-BRACKET-CONTACT-001", zh="铺作端点接触代理", en="bracket_endpoint_contact_proxy", type="GEOMETRIC_PROXY", role="GEOMETRIC_PROXY", concept=False, real=False, change="保留端点代理；不得重命名为小斗。", function="图示出跳端点的接触位置", structural="非已辨识斗类构件", position="铺作出跳端点", refs=[DIRECT_REVIEW, P1_CLASSIFICATION], unknown="DG-114 为 UNKNOWN / DO_NOT_LOCK；不能据此给散斗、齐心斗或交互斗统一规格。"),
    "COLUMN": dict(id="CMP-COLUMN-001", zh="柱", en="column", type="HISTORICAL_COMPONENT", role="RECONSTRUCTED_COMPONENT_CANDIDATE", concept=True, real=True, change="归入柱构件概念；位置和候选尺寸只作为建筑专属变体。", function="支承外檐铺作及上部木构", structural="竖向承重候选", position="外围檐柱柱网", refs=[DIRECT_REVIEW, P1_CLASSIFICATION], unknown="Z-006 963柱高 UNKNOWN；Z-006-RC-01 仅是 D-023 可替换生产候选；角柱生起为报告猜测。"),
    "FRAME_CONTROL": dict(id="CTL-FRAME-001", zh="梁架层位控制对象", en="frame_tier_control", type="CONTROL_OBJECT", role="CONTROL_OBJECT", concept=False, real=False, change="保留工程控制命名空间，不迁入历史构件目录。", function="定位与诊断梁架层位", structural="无历史结构身份", position="梁架控制坐标", refs=[P1_GATE], unknown="控制长度和位置不能解释为实体梁、枋或节点。"),
    "FRAME_SUPPORT": dict(id="PRX-FRAME-CONNECTOR-001", zh="梁架层位连接代理", en="frame_tier_connector_proxy", type="GEOMETRIC_PROXY", role="GEOMETRIC_PROXY", concept=False, real=False, change="保留代理；未来按确证梁架成员替换。", function="图示层位和柱/支点之间的连接", structural="非精确历史支承件或榫卯", position="梁架层位连接处", refs=[DIRECT_REVIEW, P1_GATE], unknown="端点与截面为中等 LOD；不能命名为托脚、蜀柱等具体历史构件。"),
    "GABLE_CONTROL": dict(id="CTL-GABLE-001", zh="山面轮廓控制对象", en="gable_guide_control", type="CONTROL_OBJECT", role="CONTROL_OBJECT", concept=False, real=False, change="保留诊断控制命名空间。", function="控制歇山山面轮廓", structural="无历史结构身份", position="山面轮廓", refs=[P1_GATE], unknown="山面控制线不能解释为博风板、角梁或其他实体构件。"),
    "GRID_CONTROL": dict(id="CTL-GRID-001", zh="柱网定位控制对象", en="bay_grid_control", type="CONTROL_OBJECT", role="CONTROL_OBJECT", concept=False, real=False, change="保留定位控制命名空间。", function="标示平面开间与进深控制线", structural="无历史结构身份", position="平面柱网", refs=[DIRECT_REVIEW], unknown="线段数不是柱数或历史构件数。"),
    "PRIMARY_FRAME": dict(id="UNR-PRIMARY-FRAME-001", zh="未分解主体梁架代理", en="unresolved_primary_frame_proxy", type="UNKNOWN_UNRESOLVED_COMPONENT", role="GEOMETRIC_PROXY", concept=False, real=None, change="保留集合代理；后续按证据拆分六椽栿、梁、枋等，不能把整个 family 命名为单件。", function="表达主要梁架跨度与层级", structural="集合性中等 LOD 占位", position="主体梁架", refs=[DIRECT_REVIEW, P1_CLASSIFICATION], unknown="六椽栿、阑额等术语有证据，但 P2 两种网格不能逐一等同具体历史成员。"),
    "PURLIN": dict(id="CMP-PURLIN-001", zh="槫类构件", en="purlin_type", type="HISTORICAL_COMPONENT", role="RECONSTRUCTED_COMPONENT_CANDIDATE", concept=True, real=True, change="以报告使用的槫为类名；具体撩风/下平/上平/脊槫分型暂不由 P2 单一 variant 锁定。", function="支承屋面椽架并控制屋架标高", structural="屋架横向支承类型候选", position="屋架各槫位", refs=[DIRECT_REVIEW, P1_CLASSIFICATION], unknown="当前 P2 截面、数量和排布为 roof-control 候选，不是逐根原构清单。"),
    "RAFTER": dict(id="CMP-RAFTER-001", zh="椽类构件", en="rafter_type", type="HISTORICAL_COMPONENT", role="GEOMETRIC_PROXY", concept=True, real=True, change="保留椽构件概念，P2 三种坡段仅作图示代理。", function="承托屋面并形成坡面", structural="屋面坡向构件类型", position="屋面各坡段", refs=[DIRECT_REVIEW, P1_CLASSIFICATION], unknown="P2 36 个图示段的间距、数量、翼角做法不能作为历史精确椽布置。"),
    "ROOF_ENVELOPE": dict(id="ENV-ROOF-001", zh="屋面连续形态包络", en="roof_surface_envelope", type="ENVELOPE_SURFACE", role="ENVELOPE_SURFACE", concept=False, real=False, change="保留零厚度包络层，不登记为瓦、望板或实体屋面构件。", function="表达檐至脊的连续屋面外形", structural="无实体构件身份", position="屋面外表", refs=[DIRECT_REVIEW, P1_GATE], unknown="六片平面条带无厚度、铺瓦及真实曲面构造主张。"),
}


def read_json(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def encode(obj: dict) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def parameter_evidence(pid: str, params: dict, overrides: dict) -> dict:
    if pid in params:
        p = params[pid]
        return {k: p[k] for k in ("classification", "time_layer", "source_layer", "production_use", "source_ids", "is_replaceable", "value")}
    if pid in overrides:
        p = overrides[pid]
        return {"classification": p["classification"], "time_layer": p["time_layer"], "source_layer": "APPROVED_OVERRIDE", "production_use": p["production_use"], "source_ids": p["evidence_basis"] + [p["approval_decision_id"]], "is_replaceable": p["is_replaceable"], "value": p["current_resolved_value"], "target_parameter_id": p["target_parameter_id"], "formula": p["formula"]}
    raise ValueError(f"Unknown parameter ID: {pid}")


def baseline_check(m: dict, params: dict, overrides: dict) -> None:
    families, variants, instances = m["component_families"], m["variants"], m["instances"]
    if set(families) != set(FAMILIES) or len(variants) != 40 or len(instances) != 365:
        raise ValueError("P2 frozen 11/40/365 baseline mismatch; stop without writing")
    summary = m["semantic_summary"]
    counts = dict(collections.Counter(i["family_id"] for i in instances))
    if summary["family_counts"] != counts or summary["variant_count"] != 40 or summary["instance_count"] != 365:
        raise ValueError("P2 summary counts differ from records; stop without writing")
    if set(summary["variant_ids"]) != set(variants) or set(summary["instance_ids"]) != {i["instance_id"] for i in instances}:
        raise ValueError("P2 summary IDs differ from records; stop without writing")
    if summary["historical_Z_006"] != {"classification": "UNKNOWN", "production_use": "DO_NOT_LOCK", "value": None}:
        raise ValueError("P2 Z-006 boundary mismatch; stop without writing")
    if params["Z-006"]["value"] is not None or params["DG-114"]["value"] is not None or params["HIS-002"]["value"] is not None:
        raise ValueError("P2 UNKNOWN boundary mismatch; stop without writing")
    rc = overrides["Z-006-RC-01"]
    if (rc["classification"], rc["is_replaceable"], rc["approval_decision_id"], rc["target_parameter_id"]) != ("REASONABLE_COMPLETION", True, "D-023", "Z-006"):
        raise ValueError("P2 RC override boundary mismatch; stop without writing")
    if set(i["variant_id"] for i in instances) - set(variants):
        raise ValueError("P2 orphan variant reference; stop without writing")
    for vid, v in variants.items():
        if v["family_id"] not in families or any(pid not in params and pid not in overrides for pid in v["parameter_ids"]):
            raise ValueError(f"P2 variant {vid} has invalid family or parameter; stop without writing")
    for i in instances:
        if i["family_id"] not in families or i["family_id"] != variants[i["variant_id"]]["family_id"]:
            raise ValueError(f"P2 instance {i['instance_id']} relation mismatch; stop without writing")


def make_ontology() -> dict:
    descriptions = {
        "HISTORICAL_COMPONENT": "有证据支持的构件类型概念；当前 P2 网格精度与历史原构数量另行判断。",
        "ASSEMBLY_UNIT": "多个构件的组合单元；P3.0 预留，不由 P2 family 自动生成。",
        "GEOMETRIC_PROXY": "证据或 LOD 受限时的替代几何，无精确历史构件身份。",
        "CONTROL_OBJECT": "参数化定位或诊断对象，不是历史构件。",
        "ENVELOPE_SURFACE": "连续外形包络或曲面，不是实体古建构件。",
        "UNKNOWN_UNRESOLVED_COMPONENT": "构件身份或集合拆分未获证据支持，保持未决。",
    }
    return {"version": "V001", "status": "T-009_IMPLEMENTED_PENDING_GATE_REVIEW", "types": descriptions, "identity_rule": "P2 engineering family and Blender mesh instance do not imply historical component type or count.", "asset_roles": ["RECONSTRUCTED_COMPONENT_CANDIDATE", "GEOMETRIC_PROXY", "CONTROL_OBJECT", "ENVELOPE_SURFACE"], "evidence_classes": ["CONFIRMED", "HIGH_CONFIDENCE_INFERENCE", "REASONABLE_COMPLETION", "UNKNOWN"], "semantic_layers": ["observed_as_measured", "report_ideal_model", "reconstructed_963_candidate"], "assembly_relationship_vocabulary": RELATIONS, "historical_count_rule": "P2 instances are machine placements; no historical component inventory count is derived in P3.0.", "source_references": [str(MANIFEST), DIRECT_REVIEW, P1_CLASSIFICATION, P1_GATE, "docs/production/zhenguo_wanfo/P3_0_DEFINITION_OF_DONE_V001.md"]}


def make_schema() -> dict:
    nonempty = {"type": "string", "minLength": 1}
    strings = {"type": "array", "items": nonempty}
    record_fields = ["component_id", "canonical_name_zh", "canonical_name_en", "aliases", "historical_terms", "category", "ontology_type", "function", "structural_role", "typical_position", "source_building", "period", "parameter_ids", "evidence_by_attribute", "source_references", "historical_state", "originality_status", "master_3d_asset", "variant_ids", "instance_ids", "assembly_relations", "applicability", "reuse_scope", "known_unknowns", "interpretation_boundary", "version", "status"]
    component_properties = {k: nonempty for k in record_fields}
    for k in ("aliases", "historical_terms", "parameter_ids", "source_references", "variant_ids", "instance_ids", "known_unknowns"):
        component_properties[k] = strings
    for k in ("evidence_by_attribute", "historical_state", "master_3d_asset", "applicability", "interpretation_boundary"):
        component_properties[k] = {"type": "object"}
    component_properties["assembly_relations"] = {"type": "array", "items": {"$ref": "#/$defs/relation"}}
    component_properties["ontology_type"] = {"enum": ONTOLOGY_TYPES}
    component_properties["historical_component_concept"] = {"type": "boolean"}
    component_properties["historical_component_statistics_policy"] = {"enum": ["CANDIDATE_PLACEMENT_ONLY", "EXCLUDED"]}
    component_properties["p2_family_id"] = nonempty
    component_properties["current_asset_role"] = {"enum": ["RECONSTRUCTED_COMPONENT_CANDIDATE", "GEOMETRIC_PROXY", "CONTROL_OBJECT", "ENVELOPE_SURFACE"]}
    component_properties["corresponds_to_real_historical_component"] = {"type": ["boolean", "null"]}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://example.local/arch3d/p3_0_component_registry_schema_v001.json", "title": "ARCH3D P3.0 Component Registry V001", "type": "object", "additionalProperties": False, "required": ["version", "status", "case_id", "input_sha256", "historical_boundaries", "parameter_evidence_catalog", "components", "variants", "instances", "assembly_relationship_vocabulary"], "properties": {"version": {"const": "V001"}, "status": nonempty, "case_id": nonempty, "input_sha256": {"type": "object", "minProperties": 5, "additionalProperties": nonempty}, "historical_boundaries": {"type": "object"}, "parameter_evidence_catalog": {"type": "object"}, "components": {"type": "array", "minItems": 11, "maxItems": 11, "items": {"$ref": "#/$defs/component"}}, "variants": {"type": "array", "minItems": 40, "maxItems": 40, "items": {"$ref": "#/$defs/variant"}}, "instances": {"type": "array", "minItems": 365, "maxItems": 365, "items": {"$ref": "#/$defs/instance"}}, "assembly_relationship_vocabulary": {"type": "array", "uniqueItems": True, "items": {"enum": RELATIONS}}}, "$defs": {"relation": {"type": "object", "additionalProperties": False, "required": ["relation", "target_id", "evidence_status"], "properties": {"relation": {"enum": RELATIONS}, "target_id": nonempty, "evidence_status": nonempty}}, "component": {"type": "object", "required": record_fields + ["p2_family_id", "current_asset_role", "historical_component_concept", "historical_component_statistics_policy", "corresponds_to_real_historical_component"], "properties": component_properties}, "variant": {"type": "object", "required": ["variant_id", "p2_variant_id", "component_id", "p2_family_id", "parameter_ids", "evidence_by_attribute", "p2_generator_parameters", "p2_mesh_data_name", "current_asset_role", "replaceability", "source_references", "version", "status"], "properties": {"variant_id": nonempty, "p2_variant_id": nonempty, "component_id": nonempty, "p2_family_id": nonempty, "parameter_ids": strings, "evidence_by_attribute": {"type": "object"}, "p2_generator_parameters": {"type": "object"}, "p2_mesh_data_name": nonempty, "current_asset_role": nonempty, "replaceability": {"type": "object"}, "source_references": strings, "version": nonempty, "status": nonempty}}, "instance": {"type": "object", "required": ["instance_id", "p2_instance_id", "component_id", "variant_id", "p2_family_id", "placement", "evidence_metadata", "parameter_ids", "historical_component_count_eligible", "source_references", "version", "status"], "properties": {"instance_id": nonempty, "p2_instance_id": nonempty, "component_id": nonempty, "variant_id": nonempty, "p2_family_id": nonempty, "placement": {"type": "object", "required": ["location_mm", "rotation_euler_rad", "scale"]}, "evidence_metadata": {"type": "object", "required": ["evidence_class", "source_layer", "time_layer", "historical_state_tag", "originality_status", "bounded_placeholder", "override_ids"]}, "parameter_ids": strings, "historical_component_count_eligible": {"type": "boolean"}, "source_references": strings, "version": nonempty, "status": nonempty}}}}


def build(m: dict, params: dict, overrides: dict, matrix: dict) -> tuple[dict, dict, dict, dict]:
    ontology = make_ontology()
    audit = {"version": "V001", "status": "COMPLETE_FOR_T009_PENDING_GATE_REVIEW", "input_manifest": str(MANIFEST), "input_manifest_sha256": sha256(MANIFEST), "families": [], "variants": [], "instances": []}
    catalog = {pid: parameter_evidence(pid, params, overrides) for pid in sorted(set(params) | set(overrides))}
    by_family_instances = collections.defaultdict(list)
    by_family_variants = collections.defaultdict(list)
    for item in m["instances"]:
        by_family_instances[item["family_id"]].append(item)
    for vid, item in m["variants"].items():
        by_family_variants[item["family_id"]].append(vid)
    components, variants, instances = [], [], []
    for fid in sorted(FAMILIES):
        spec = FAMILIES[fid]
        p2 = m["component_families"][fid]
        pids = sorted({pid for vid in by_family_variants[fid] for pid in m["variants"][vid]["parameter_ids"]})
        refs = sorted(set([str(MANIFEST), str(PARAMETERS), str(OVERRIDES), str(MATRIX), SOURCE_REGISTER] + spec["refs"]))
        audit_item = {"p2_family_id": fid, "p2_engineering_meaning": p2, "p3_component_id": spec["id"], "p3_ontology_type": spec["type"], "current_asset_role": spec["role"], "corresponds_to_real_historical_component": spec["real"], "split_merge_rename_decision": spec["change"], "diagnostic_control_only": spec["type"] == "CONTROL_OBJECT", "source_references": refs, "unresolved_boundary": spec["unknown"], "variant_count": len(by_family_variants[fid]), "instance_count": len(by_family_instances[fid])}
        audit["families"].append(audit_item)
        components.append({"component_id": spec["id"], "canonical_name_zh": spec["zh"], "canonical_name_en": spec["en"], "aliases": [fid] + (["檩类"] if fid == "PURLIN" else []), "historical_terms": HISTORICAL_TERMS.get(fid, []), "category": "WOODEN_ARCHITECTURE" if spec["concept"] else "ENGINEERING_MIGRATION", "ontology_type": spec["type"], "function": spec["function"], "structural_role": spec["structural"], "typical_position": spec["position"], "source_building": "ZG-WF-963-CANDIDATE", "period": "北汉天会七年（963）候选；现存构件年代未逐件确定", "parameter_ids": pids, "evidence_by_attribute": {pid: catalog[pid] for pid in pids}, "source_references": refs, "historical_state": {"model_layer": "reconstructed_963_candidate", "observed_as_measured": "separate in P1/P2 parameter record", "report_ideal_model": "separate; no automatic equivalence", "historical_claim": "candidate_only"}, "originality_status": "unknown", "master_3d_asset": {"path": None, "status": "NOT_YET_CREATED", "p2_canonical_blend": m["output_blend"]["path"]}, "variant_ids": sorted(by_family_variants[fid]), "instance_ids": sorted(i["instance_id"] for i in by_family_instances[fid]), "assembly_relations": [], "applicability": {"case_id": "ZG-WF-963-CANDIDATE", "future_buildings": "REQUIRES_EVIDENCE_REVIEW"}, "reuse_scope": "cross-building concept only; P2 dimensions and evidence are building-specific" if spec["concept"] else "P2 engineering lineage only", "known_unknowns": [spec["unknown"], "HIS-002: component originality unknown"], "interpretation_boundary": {"p2_family_is_historical_count": False, "p2_instances_are_historical_count": False, "current_asset_role": spec["role"], "claim": spec["change"]}, "version": "V001", "status": "MIGRATED_PENDING_GATE_REVIEW", "p2_family_id": fid, "current_asset_role": spec["role"], "historical_component_concept": spec["concept"], "historical_component_statistics_policy": "CANDIDATE_PLACEMENT_ONLY" if spec["concept"] else "EXCLUDED", "corresponds_to_real_historical_component": spec["real"]})
    for vid in sorted(m["variants"]):
        v = m["variants"][vid]
        spec = FAMILIES[v["family_id"]]
        variants.append({"variant_id": vid, "p2_variant_id": vid, "component_id": spec["id"], "p2_family_id": v["family_id"], "parameter_ids": v["parameter_ids"], "evidence_by_attribute": {pid: catalog[pid] for pid in v["parameter_ids"]}, "p2_generator_parameters": v["generator_parameters"], "p2_mesh_data_name": v["mesh_data_name"], "p2_explicit_unique": v["explicit_unique"], "current_asset_role": spec["role"], "replaceability": {"approved_override_ids": sorted(pid for pid in v["parameter_ids"] if pid in overrides), "is_p2_variant_rebuildable": True, "historical_component_master_created": False}, "source_references": [str(MANIFEST), str(PARAMETERS), str(OVERRIDES)], "version": "V001", "status": "MIGRATED_PENDING_GATE_REVIEW"})
        audit["variants"].append({"p2_variant_id": vid, "p2_family_id": v["family_id"], "p3_component_id": spec["id"], "p3_variant_id": vid, "ontology_type": spec["type"], "current_asset_role": spec["role"], "parameter_ids": v["parameter_ids"], "approved_override_ids": sorted(pid for pid in v["parameter_ids"] if pid in overrides), "evidence_catalog_ref": str(REGISTRY_JSON) + "#/parameter_evidence_catalog"})
    for i in sorted(m["instances"], key=lambda x: x["instance_id"]):
        spec = FAMILIES[i["family_id"]]
        meta = {k: i[k] for k in ("evidence_class", "source_layer", "time_layer", "historical_state_tag", "originality_status", "bounded_placeholder", "override_ids", "presentation")}
        instances.append({"instance_id": i["instance_id"], "p2_instance_id": i["instance_id"], "component_id": spec["id"], "variant_id": i["variant_id"], "p2_family_id": i["family_id"], "placement": i["transform"], "evidence_metadata": meta, "parameter_ids": i["parameter_ids"], "historical_component_count_eligible": False, "source_references": [str(MANIFEST), str(PARAMETERS), str(OVERRIDES)], "version": "V001", "status": "P2_MACHINE_PLACEMENT_MIGRATED"})
        audit["instances"].append({"p2_instance_id": i["instance_id"], "p2_family_id": i["family_id"], "p3_component_id": spec["id"], "p3_variant_id": i["variant_id"], "p3_instance_id": i["instance_id"], "placement": i["transform"], "evidence_metadata": meta, "historical_component_count_eligible": False})
    boundaries = {"Z-006": params["Z-006"], "Z-006-RC-01": overrides["Z-006-RC-01"], "DG-114": params["DG-114"], "HIS-002": params["HIS-002"], "corner_joinery_hidden_angle_beam": "45-degree corner, mortise and hidden-angle beam unresolved; no precision claim", "semantic_layers": matrix["semantic_layer_policy"]["distinct_layers"], "source_references": [DIRECT_REVIEW, P1_CLASSIFICATION, P1_GATE, "D-023", "D-028", "D-029", "D-030"]}
    registry = {"version": "V001", "status": "T009_COMPLETE_PENDING_PRODUCT_OWNER_GATE_REVIEW", "case_id": "ZG-WF-963-CANDIDATE", "input_sha256": {str(path): sha256(path) for path in [MANIFEST, PARAMETERS, OVERRIDES, MATRIX, EVIDENCE_SCHEMA]}, "historical_boundaries": boundaries, "parameter_evidence_catalog": catalog, "components": components, "variants": variants, "instances": instances, "assembly_relationship_vocabulary": RELATIONS}
    return ontology, audit, registry, make_schema()


def validate(ontology: dict, audit: dict, registry: dict, schema: dict, m: dict, params: dict, overrides: dict) -> dict:
    failures = []
    def check(name: str, condition: bool) -> None:
        if not condition:
            failures.append(name)
    schema_errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda e: str(e.path))
    check("schema", not schema_errors)
    component_ids = [x["component_id"] for x in registry["components"]]
    variant_ids = [x["variant_id"] for x in registry["variants"]]
    instance_ids = [x["instance_id"] for x in registry["instances"]]
    check("unique_component_ids", len(component_ids) == len(set(component_ids)))
    check("unique_variant_ids", len(variant_ids) == len(set(variant_ids)))
    check("unique_instance_ids", len(instance_ids) == len(set(instance_ids)))
    check("legal_ontology", all(c["ontology_type"] in ontology["types"] for c in registry["components"]))
    family_ids = {x["p2_family_id"] for x in audit["families"]}
    check("family_coverage", family_ids == set(m["component_families"]))
    check("variant_coverage", set(variant_ids) == set(m["variants"]))
    check("instance_coverage", set(instance_ids) == {i["instance_id"] for i in m["instances"]})
    check("audit_variant_coverage", {v["p2_variant_id"] for v in audit["variants"]} == set(m["variants"]))
    check("audit_instance_coverage", {i["p2_instance_id"] for i in audit["instances"]} == {i["instance_id"] for i in m["instances"]})
    cmap = {c["component_id"]: c for c in registry["components"]}
    vmap = {v["variant_id"]: v for v in registry["variants"]}
    imap = {i["instance_id"]: i for i in registry["instances"]}
    orphan_families = sorted(set(m["component_families"]) - family_ids)
    orphan_variants = sorted(vid for vid, v in m["variants"].items() if vid not in vmap or vmap[vid]["component_id"] not in cmap)
    orphan_instances = sorted(i["instance_id"] for i in m["instances"] if i["instance_id"] not in imap or imap[i["instance_id"]]["variant_id"] not in vmap)
    check("zero_orphans", not (orphan_families or orphan_variants or orphan_instances))
    check("component_backlinks", all(set(c["variant_ids"]) == {v["variant_id"] for v in registry["variants"] if v["component_id"] == c["component_id"]} and set(c["instance_ids"]) == {i["instance_id"] for i in registry["instances"] if i["component_id"] == c["component_id"]} for c in registry["components"]))
    check("component_semantics", all(c["ontology_type"] == FAMILIES[c["p2_family_id"]]["type"] and c["current_asset_role"] == FAMILIES[c["p2_family_id"]]["role"] and c["originality_status"] == "unknown" and c["evidence_by_attribute"] == {pid: registry["parameter_evidence_catalog"][pid] for pid in c["parameter_ids"]} for c in registry["components"]))
    check("audit_relations", all(x["p3_component_id"] == vmap[x["p2_variant_id"]]["component_id"] and x["p3_variant_id"] == x["p2_variant_id"] for x in audit["variants"]) and all(x["p3_component_id"] == imap[x["p2_instance_id"]]["component_id"] and x["p3_variant_id"] == imap[x["p2_instance_id"]]["variant_id"] and x["placement"] == imap[x["p2_instance_id"]]["placement"] and x["evidence_metadata"] == imap[x["p2_instance_id"]]["evidence_metadata"] for x in audit["instances"]))
    check("variant_provenance", all(vmap[vid]["p2_family_id"] == source["family_id"] and vmap[vid]["parameter_ids"] == source["parameter_ids"] and vmap[vid]["p2_generator_parameters"] == source["generator_parameters"] and vmap[vid]["evidence_by_attribute"] == {pid: registry["parameter_evidence_catalog"][pid] for pid in source["parameter_ids"]} for vid, source in m["variants"].items()))
    check("instance_provenance", all(imap[i["instance_id"]]["placement"] == i["transform"] and imap[i["instance_id"]]["parameter_ids"] == i["parameter_ids"] and imap[i["instance_id"]]["evidence_metadata"] == {k: i[k] for k in ("evidence_class", "source_layer", "time_layer", "historical_state_tag", "originality_status", "bounded_placeholder", "override_ids", "presentation")} for i in m["instances"]))
    check("parameter_evidence_preservation", all(registry["parameter_evidence_catalog"][pid] == parameter_evidence(pid, params, overrides) for pid in set(params) | set(overrides)))
    check("control_envelope_exclusion", all(not c["historical_component_concept"] and c["historical_component_statistics_policy"] == "EXCLUDED" for c in registry["components"] if c["ontology_type"] in ("CONTROL_OBJECT", "ENVELOPE_SURFACE", "GEOMETRIC_PROXY", "UNKNOWN_UNRESOLVED_COMPONENT")))
    check("machine_instances_not_historical_count", all(not i["historical_component_count_eligible"] for i in registry["instances"]))
    b = registry["historical_boundaries"]
    check("Z-006_boundary", b["Z-006"]["classification"] == "UNKNOWN" and b["Z-006"]["value"] is None and b["Z-006"]["production_use"] == "DO_NOT_LOCK")
    check("RC_boundary", b["Z-006-RC-01"]["classification"] == "REASONABLE_COMPLETION" and b["Z-006-RC-01"]["is_replaceable"] and b["Z-006-RC-01"]["approval_decision_id"] == "D-023")
    check("DG_HIS_boundary", all(b[pid]["classification"] == "UNKNOWN" and b[pid]["value"] is None for pid in ("DG-114", "HIS-002")))
    check("semantic_layers", b["semantic_layers"] == ["observed_as_measured", "report_ideal_model", "reconstructed_963_candidate"])
    check("assembly_vocabulary", set(RELATIONS) == set(registry["assembly_relationship_vocabulary"]))
    return {"version": "V001", "status": "PASS" if not failures else "FAIL", "family_coverage": f"{len(family_ids)}/11", "variant_coverage": f"{len(variant_ids)}/40", "instance_coverage": f"{len(instance_ids)}/365", "orphan_family": len(orphan_families), "orphan_variant": len(orphan_variants), "orphan_instance": len(orphan_instances), "orphan_ids": {"family": orphan_families, "variant": orphan_variants, "instance": orphan_instances}, "ontology_validation": "PASS" if "legal_ontology" not in failures else "FAIL", "registry_schema_validation": "PASS" if not schema_errors else "FAIL", "evidence_boundary_validation": "PASS" if all(x not in failures for x in ("parameter_evidence_preservation", "variant_provenance", "instance_provenance", "component_semantics", "audit_relations", "Z-006_boundary", "RC_boundary", "DG_HIS_boundary", "semantic_layers", "control_envelope_exclusion", "machine_instances_not_historical_count")) else "FAIL", "determinism": "PASS: sorted inputs and canonical JSON; --check byte comparison", "checks": {name: "FAIL" if name in failures else "PASS" for name in ["schema", "unique_component_ids", "unique_variant_ids", "unique_instance_ids", "legal_ontology", "family_coverage", "variant_coverage", "instance_coverage", "audit_variant_coverage", "audit_instance_coverage", "zero_orphans", "component_backlinks", "component_semantics", "audit_relations", "variant_provenance", "instance_provenance", "parameter_evidence_preservation", "control_envelope_exclusion", "machine_instances_not_historical_count", "Z-006_boundary", "RC_boundary", "DG_HIS_boundary", "semantic_layers", "assembly_vocabulary"]}, "schema_errors": [str(e) for e in schema_errors], "failures": failures, "source_manifest_sha256": sha256(MANIFEST), "gate_decision": "PENDING_PRODUCT_OWNER_REVIEW; NOT_P3_0_PASS"}


def markdown(ontology: dict, audit: dict, report: dict) -> dict[Path, bytes]:
    onto = ["# P3.0 Component Ontology V001｜构件本体与命名规则", "", "Status: **T-009 IMPLEMENTED / P3.0 GATE REVIEW PENDING**", "", "P2 engineering family、Blender object 与 mesh instance 均不自动等于历史构件或历史数量。构件身份与当前资产角色分别登记；证据等级不会因命名改变。", "", "## 本体类型", ""]
    for key, desc in ontology["types"].items(): onto.append(f"- `{key}`：{desc}")
    onto += ["", "## 命名与 ID", "", "- 中文名为概念名；英文 `canonical_name_en` 使用小写下划线键，跨建筑复用。报告原称与异名分别保存在 `historical_terms`、`aliases`，不能拿别名升级证据。", "- `CMP-*` 表示可辨识的历史构件**类型概念**，`PRX-*` 表示代理，`CTL-*` 表示工程控制，`ENV-*` 表示包络，`UNR-*` 表示未决集合。`ASM-*` 为未来组合单元保留。ID 不含万佛殿名。", "- 建筑专属 Variant ID 保留 P2 稳定 ID；新建筑可使用 `<CASE>-<COMPONENT>-V<序号>`。Instance ID 保留 P2 稳定放置 ID；新实例可用 `<CASE>-I<序号>`。Assembly ID 使用 `<CASE>-ASM-<序号>`。均不得以 ID 推断历史身份。", "- `component_id` 表示类型/代理登记；`variant_id` 表示参数化版本；`instance_id` 表示机器放置。当前没有独立 P3.1 Master，`master_3d_asset.path = null`。", "", "## 证据与统计", "", "- `observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate` 三层不互换。", "- `Z-006` 仍 `UNKNOWN / null / DO_NOT_LOCK`；`Z-006-RC-01` 仅为 D-023 批准的独立、可替换候选。", "- `DG-114` 仍 UNKNOWN，接触代理不是小斗；`HIS-002` 逐构件原真性仍 unknown。45°转角、榫卯、隐角梁仍未决。", "- 所有 365 个 P2 实例仅为机器放置；控制、代理与包络从历史构件统计排除。历史类型概念的 P2 放置也不能直接算作原构数量。", "", "## 组合关系词汇（P3.2 预留）", "", ", ".join(f"`{x}`" for x in RELATIONS) + "。关系记录使用 `relation / target_id / evidence_status`；本版不填未经核证的具体组合边。", "", "## 依据", "", f"- `{MANIFEST}`；`{DIRECT_REVIEW}`；`{P1_CLASSIFICATION}`；`{P1_GATE}`；D-023、D-028～D-030。", ""]
    aud = ["# P3.0 P2→P3 Component Migration Audit V001｜镇国寺万佛殿", "", "Status: **11/11 COMPLETE / T-009 VALIDATED / P3.0 GATE REVIEW PENDING**", "", f"P2 input: `{MANIFEST}`。完整 40 个 variant 与 365 个 instance 的逐条映射见 `{AUDIT_JSON}` 与 `{REGISTRY_JSON}`。", "", "| P2 family | P2 工程语义 | P3 类型 / 当前资产 | 对应真实历史构件 | 拆分 / 命名决策 | 控制/诊断专用 | 证据 | 未决边界 | Variant / Instance |", "|---|---|---|---|---|---|---|---|---|"]
    for x in audit["families"]:
        fid=x["p2_family_id"]; s=FAMILIES[fid]
        real={True:"类型概念成立；P2 实例非历史计数",False:"否",None:"未决"}[s["real"]]
        aud.append(f"| `{fid}` | {x['p2_engineering_meaning']['rule']} | `{s['type']}` / `{s['role']}` | {real} | {s['change']} | {'是' if x['diagnostic_control_only'] else '否'} | {', '.join('`'+p+'`' for p in s['refs'])} | {s['unknown']} | {x['variant_count']} / {x['instance_count']} |")
    aud += ["", "## 迁移与边界", "", "- 11 个 family 映射到 11 条 P3 登记记录；40 个 variant 与 365 个 instance 保留原 ID、参数、变换和证据元数据，orphan 为 0。", "- `COLUMN`、`PURLIN`、`RAFTER` 的历史**类型概念**有依据；当前网格仍按各自 asset role 解释，不能把 12/7/36 个放置当历史清单。", "- `BRACKET_ARM`、`PRIMARY_FRAME` 是未决集合/代理，待 P3.1 回证据拆分。`BRACKET_CONTACT` 不能解释为小斗。", "- `FRAME_CONTROL`、`GABLE_CONTROL`、`GRID_CONTROL` 是控制对象；`ROOF_ENVELOPE` 是零厚度包络；均不计历史构件。", "- `Z-006`、`Z-006-RC-01`、`DG-114`、`HIS-002` 和三层语义按原参数逐项保留。", ""]
    rep = ["# P3.0 Registry Validation Report V001", "", "Status: **T-009 MACHINE VALIDATION PASS / P3.0 GATE REVIEW PENDING**", "", "| 检查 | 结果 |", "|---|---|", f"| Family / Variant / Instance coverage | {report['family_coverage']} / {report['variant_coverage']} / {report['instance_coverage']} |", f"| Orphan family / variant / instance | {report['orphan_family']} / {report['orphan_variant']} / {report['orphan_instance']} |", f"| Ontology | {report['ontology_validation']} |", f"| Registry schema | {report['registry_schema_validation']} |", f"| Evidence boundary | {report['evidence_boundary_validation']} |", f"| Determinism | {report['determinism']} |", "", "## 机器检查", ""]
    rep += [f"- `{k}`: {v}" for k,v in report["checks"].items()]
    rep += ["", f"P2 manifest SHA256: `{report['source_manifest_sha256']}`。Schema 使用 JSON Schema Draft 2020-12。执行 `python3 production/zhenguo_wanfo/scripts/build_p3_0_component_registry_v001.py --check` 进行只读字节复验。", "", "本报告不批准 P3.0 Gate PASS；Product Owner / ChatGPT 后续按 D-030 做最终 Gate Review。", ""]
    return {ONTOLOGY_MD: ("\n".join(onto)).encode(), AUDIT_MD: ("\n".join(aud)).encode(), REPORT_MD: ("\n".join(rep)).encode()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate source and compare generated files byte-for-byte without writing")
    args = parser.parse_args()
    m, ps, os, matrix = (read_json(p) for p in (MANIFEST, PARAMETERS, OVERRIDES, MATRIX))
    read_json(EVIDENCE_SCHEMA)  # authoritative contract input; its hash is recorded
    params, overrides = ps["parameters"], os["overrides"]
    baseline_check(m, params, overrides)
    ontology, audit, registry, schema = build(m, params, overrides, matrix)
    report = validate(ontology, audit, registry, schema, m, params, overrides)
    if report["status"] != "PASS":
        raise SystemExit("Validation failed: " + ", ".join(report["failures"] + report["schema_errors"]))
    files = {ONTOLOGY_JSON: encode(ontology), AUDIT_JSON: encode(audit), REGISTRY_JSON: encode(registry), SCHEMA_JSON: encode(schema), REPORT_JSON: encode(report)}
    files.update(markdown(ontology, audit, report))
    if args.check:
        mismatch = [str(p) for p, content in files.items() if not (ROOT / p).exists() or (ROOT / p).read_bytes() != content]
        if mismatch:
            raise SystemExit("Determinism/coverage file mismatch: " + ", ".join(mismatch))
    else:
        for path, content in files.items():
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    print(f"{report['status']}: {report['family_coverage']} families; {report['variant_coverage']} variants; {report['instance_coverage']} instances; orphans {report['orphan_family']}/{report['orphan_variant']}/{report['orphan_instance']}; mode={'check' if args.check else 'write'}")


if __name__ == "__main__":
    main()
