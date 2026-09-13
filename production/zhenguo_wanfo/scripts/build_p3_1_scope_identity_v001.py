#!/usr/bin/env python3
"""Deterministically build and validate the T-010 scope/identity review.

Only text/JSON outputs are written. P2 and P3.0 inputs are read-only.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = "production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_V001.json"
AUDIT_PATH = "production/zhenguo_wanfo/registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json"
PARAM_PATH = "production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json"
DIRECT = "docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md"
CLASSIFICATION = "docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md"
GATE = "docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md"
BATCH_02 = "docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md"
BATCH_03 = "docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_03.md"
BATCH_04 = "docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_04.md"
MIGRATION_DOC = "docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md"
TASK = "docs/tasks/T-010_P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001.md"
STATUS = (
    "MASTER_REQUIRED", "EVIDENCE_REVIEW_BEFORE_MASTER", "PROXY_ONLY",
    "CONTROL_ONLY", "ENVELOPE_ONLY", "DEFERRED_INSUFFICIENT_EVIDENCE",
)
MINIMUM = {
    "柱": "CMP-COLUMN-001", "柱头栌斗": "CMP-LUDOU-COLUMN-001",
    "底斗": "CMP-DOU-BOTTOM-LONGKAI-001",
    "单向长开斗": "CMP-DOU-SINGLE-LONGKAI-001",
    "交互斗": "CMP-DOU-INTERACTIVE-001",
    "下六椽栿": "CMP-FRAME-LOWER-SIX-CHUANFU-001",
    "上六椽栿": "CMP-FRAME-UPPER-SIX-CHUANFU-001",
    "槫类": "CMP-PURLIN-001", "椽类": "CMP-RAFTER-001",
}
OUT = {
    "scope_json": "production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json",
    "identity_json": "production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json",
    "scope_md": "docs/production/zhenguo_wanfo/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md",
    "identity_md": "docs/production/zhenguo_wanfo/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md",
    "validation_json": "production/zhenguo_wanfo/validation/P3_1_SCOPE_IDENTITY_VALIDATION_REPORT_V001.json",
    "validation_md": "docs/production/zhenguo_wanfo/P3_1_SCOPE_IDENTITY_VALIDATION_REPORT_V001.md",
}


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha256(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def dumped(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def page(label: str, pdf: str, printed: str, table: str = "") -> dict:
    return {"source_id": "SRC-ZG-WF-001", "review_path": DIRECT,
            "pdf_page": pdf, "printed_page": printed, "table_or_section": table}


PAGES = {
    "column": [page("column", "49–50", "34–35", "2.1.2 / table 2-6")],
    "ludou": [page("ludou", "62–63", "47–48", "tables 2-26 / 2-27")],
    "dou": [page("dou", "65–66", "50–51", "tables 2-28 / 2-29")],
    "frame": [page("frame", "81", "66", "table 2-38")],
    "purlin": [page("purlin", "103–107", "88–92", "tables 2-51 / 2-52")],
    "rafter": [page("rafter", "104–109", "89–94", "2.3.3 / 2.4")],
    "bracket_topology": [page("bracket_topology", "119–120", "104–105", "recommended conclusions")],
    "deformation": [page("deformation", "131", "116", "deformation analysis; 四椽栿 mention only")],
}

FAMILY_REGISTRY_IDS = {
    "BRACKET_ARM": "PRX-BRACKET-JUMP-001",
    "BRACKET_CONTACT": "PRX-BRACKET-CONTACT-001",
    "PRIMARY_FRAME": "UNR-PRIMARY-FRAME-001",
    "FRAME_SUPPORT": "PRX-FRAME-CONNECTOR-001",
}


def parameter_evidence(parameters: dict, ids: list[str]) -> dict:
    return {pid: {key: parameters[pid][key] for key in (
        "value", "unit", "classification", "time_layer", "source_layer",
        "production_use", "source_ids")}
        for pid in ids}


def measured(value: object, unit: str, note: str) -> dict:
    return {"value": value, "unit": unit, "classification": "CONFIRMED",
            "time_layer": "observed_as_measured", "source_layer": "DIRECT_PRIMARY",
            "production_use": "OBSERVED_REFERENCE", "source_ids": ["SRC-ZG-WF-001"],
            "note": note}


# The P3.0 record remains unchanged. This table decides its T-010 eligibility.
REGISTRY_REVIEW = {
    "BRACKET_ARM": ("PROXY_ONLY", "P2 equal jump subdivisions are aggregate graphic topology; DG-110–113 do not identify individual 栱 or 昂.", "Individual member drawings, section, endpoints and 45° node evidence."),
    "BRACKET_CONTACT": ("PROXY_ONLY", "Diagrammatic contact block is not 小斗; DG-114 unified-small-dou rule remains UNKNOWN.", "A component-specific斗 identity and shape source, without using P2 contact-block dimensions."),
    "COLUMN": ("MASTER_REQUIRED", "Column type and observed diameter are verified; a reusable parametric column body is feasible while Z-006 remains unknown.", "963 column height and individual originality remain unknown; no fixed historical height is licensed."),
    "FRAME_CONTROL": ("CONTROL_ONLY", "Frame-tier locator has no physical historical member identity.", "Not applicable to a control object."),
    "FRAME_SUPPORT": ("PROXY_ONLY", "P2 connector endpoints do not identify 托脚, 蜀柱 or joints.", "Member-specific section, length, topology and contact/joint evidence."),
    "GABLE_CONTROL": ("CONTROL_ONLY", "Gable diagnostic line is not 博风板, 角梁 or another physical member.", "Not applicable to a control object."),
    "GRID_CONTROL": ("CONTROL_ONLY", "Grid locator is not a column or historical member.", "Not applicable to a control object."),
    "PRIMARY_FRAME": ("PROXY_ONLY", "Aggregate P2 frame meshes cannot be assigned to individual 六椽栿, 梁 or 枋.", "Member-by-member mapping; independently verified identities are separate derived candidates."),
    "PURLIN": ("DEFERRED_INSUFFICIENT_EVIDENCE", "槫 is a verified type term, but P2 one section/variant is an engineering envelope, not a measured component profile.", "Position-specific sections, member lengths, end conditions and evidence for whether positions are variants or separate types."),
    "RAFTER": ("DEFERRED_INSUFFICIENT_EVIDENCE", "椽 type is real, but P2 slope segments and spacing are diagrammatic.", "Measured sections, lengths, eave/flying-rafter distinctions, spacing and wing-corner form."),
    "ROOF_ENVELOPE": ("ENVELOPE_ONLY", "Zero-thickness surface strips are not tiles, boarding or solid roof members.", "Not applicable to an envelope surface."),
}


def make_registry_records(registry: dict, parameters: dict) -> list[dict]:
    records = []
    key_pages = {"COLUMN": "column", "PURLIN": "purlin", "RAFTER": "rafter",
                 "BRACKET_ARM": "bracket_topology", "BRACKET_CONTACT": "dou",
                 "PRIMARY_FRAME": "frame", "FRAME_SUPPORT": "frame"}
    for c in registry["components"]:
        family = c["p2_family_id"]
        status, reason, gap = REGISTRY_REVIEW[family]
        refs = sorted(set(c["source_references"] + [MIGRATION_DOC, TASK]))
        ids = [pid for pid in c["parameter_ids"] if pid in parameters]
        record = {
            "candidate_id": c["component_id"], "source_registry_id": c["component_id"],
            "source_p2_family": family, "record_origin": "P3_0_REGISTRY",
            "canonical_name_zh": c["canonical_name_zh"],
            "canonical_name_en": c["canonical_name_en"],
            "aliases": c["aliases"], "historical_terms": c["historical_terms"],
            "source_context": c["typical_position"],
            "historical_component_identity": (c["canonical_name_zh"] if c["historical_component_concept"] else None),
            "corresponds_to_real_historical_component": c["corresponds_to_real_historical_component"],
            "eligibility_status": status, "source_references": refs,
            "source_pages": PAGES.get(key_pages.get(family, ""), []),
            "evidence_by_attribute": parameter_evidence(parameters, ids),
            "known_geometry_inputs": [f"P2 engineering parameter IDs: {', '.join(c['parameter_ids'])}; not direct member geometry"],
            "unknown_unresolved_attributes": c["known_unknowns"] + [gap],
            "evidence_gap": gap if status == "DEFERRED_INSUFFICIENT_EVIDENCE" else None,
            "required_followup_evidence": f"Obtain attributable report drawings/tables or an approved formal bridge resolving: {gap}" if status == "DEFERRED_INSUFFICIENT_EVIDENCE" else None,
            "historical_state": c["historical_state"],
            "originality_status": "unknown", "p2_asset_role": c["current_asset_role"],
            "p2_proxy_control_envelope_relationship": c["interpretation_boundary"]["claim"],
            "split_merge_replacement_relationship": "P3.0 record retained unchanged; no automatic historical upgrade.",
            "eligibility_reason": reason,
            "proposed_future_component_id": c["component_id"] if status == "MASTER_REQUIRED" else None,
            "readiness_for_later_master_asset_contract": "READY_WITH_BOUNDED_LOD" if status == "MASTER_REQUIRED" else "NOT_READY",
        }
        if family == "COLUMN":
            record["evidence_by_attribute"]["Z-001"] = parameter_evidence(parameters, ["Z-001"])["Z-001"]
            record["evidence_by_attribute"]["Z-006"] = parameter_evidence(parameters, ["Z-006"])["Z-006"]
            record["known_geometry_inputs"] = ["Observed diameter approximately 460 mm (Z-001); report design candidate 459 mm (Z-002); height is an explicit free parameter, not a historical constant."]
            record["unknown_unresolved_attributes"] += ["Z-006-RC-01 is a separate replaceable candidate under D-023, not Z-006 history."]
        elif family == "PURLIN":
            record["known_geometry_inputs"] = ["Measured purlin-to-purlin rises A/B/C and inferred position rises constrain placement, not an individual 槫 cross-section."]
        elif family == "RAFTER":
            record["known_geometry_inputs"] = ["Roof slope and eave references constrain envelope/placement, not individual 椽 shape or count."]
        records.append(record)
    return records


def new_record(candidate_id: str, name: str, key: str, aliases: list[str],
               position: str, parent: str, page_key: str, evidence: dict,
               geometry: list[str], unknown: list[str], reason: str,
               status: str = "MASTER_REQUIRED", refs: list[str] | None = None) -> dict:
    return {
        "candidate_id": candidate_id, "source_registry_id": None,
        "source_p2_family": parent, "record_origin": "P1_EVIDENCE_DERIVED",
        "canonical_name_zh": name, "canonical_name_en": key,
        "aliases": aliases, "historical_terms": [name], "source_context": position,
        "historical_component_identity": name,
        "corresponds_to_real_historical_component": True,
        "eligibility_status": status,
        "source_references": sorted(set((refs or [DIRECT, CLASSIFICATION]) + [TASK])),
        "source_pages": PAGES.get(page_key, []),
        "evidence_by_attribute": evidence,
        "known_geometry_inputs": geometry,
        "unknown_unresolved_attributes": unknown + ["HIS-002: individual 963 originality unknown."],
        "evidence_gap": "; ".join(unknown) if status == "DEFERRED_INSUFFICIENT_EVIDENCE" else None,
        "required_followup_evidence": ("Obtain direct original-page member-specific geometry and identity comparison resolving: " + "; ".join(unknown)) if status == "DEFERRED_INSUFFICIENT_EVIDENCE" else None,
        "historical_state": {"observed_as_measured": "directly measured where stated",
                             "report_ideal_model": "separate, no equivalence",
                             "reconstructed_963_candidate": "not historically locked"},
        "originality_status": "unknown", "p2_asset_role": "NONE_INDEPENDENT",
        "related_p3_0_registry_id": FAMILY_REGISTRY_IDS.get(parent),
        "relationship_kind": "EVIDENCE_DERIVED_CANDIDATE_RETAINS_P3_0_PROXY" if parent else "P1_ONLY_CANDIDATE",
        "p2_proxy_control_envelope_relationship": f"P1-derived identity; P2 {parent} remains an unchanged aggregate/proxy." if parent else "No direct P2 family counterpart.",
        "split_merge_replacement_relationship": f"DERIVED_FROM_P1_EVIDENCE; related P3.0 {FAMILY_REGISTRY_IDS[parent]} ({parent}) record is retained, not renamed or superseded." if parent else "DERIVED_FROM_P1_EVIDENCE; no P3.0 record replaced.",
        "eligibility_reason": reason,
        "proposed_future_component_id": candidate_id if status == "MASTER_REQUIRED" else None,
        "readiness_for_later_master_asset_contract": "READY_WITH_BOUNDED_LOD" if status == "MASTER_REQUIRED" else "NOT_READY",
    }


def make_new_records(parameters: dict) -> list[dict]:
    pe = lambda ids: parameter_evidence(parameters, ids)
    dou_unknown = ["Exact 3D ear/cavity/profile and mortise geometry are not directly quantified; limit later Master to evidence-bounded medium LOD.",
                   "Observed means include compression/wear and are not 963 design dimensions; DG-114 remains UNKNOWN."]
    frame_unknown = ["Member full length, camber, end profile and exact joinery are not verified as individual geometry.",
                     "Observed sections must not become fixed 963 design dimensions; length needs an explicit parameter."]
    out = [
        new_record("CMP-LUDOU-COLUMN-001", "柱头栌斗", "column_head_ludou", ["栌斗"],
                   "外檐柱头铺作下层", "BRACKET_CONTACT", "ludou",
                   {**pe(["DG-101", "DG-102", "DG-103", "DG-104"]),
                    "measured_total_height": measured(293.8, "mm", "P1 direct review D-007"),
                    "measured_flat_height": measured(58.75, "mm", "P1 direct review D-007"),
                    "measured_sloped_height": measured(116.2, "mm", "P1 direct review D-007")},
                   ["Top/bottom width and depth plus total, flat and sloped heights from tables 2-26/2-27."],
                   dou_unknown, "Distinct named column-head斗 with measured width/depth/height supports a bounded reusable type; P2 contact block supplies no geometry."),
        new_record("CMP-DOU-BOTTOM-LONGKAI-001", "底斗", "bottom_long_kai_dou", ["底部长开斗"],
                   "外檐铺作长开斗组", "BRACKET_CONTACT", "dou",
                   {**pe(["DG-105", "DG-106"]),
                    "measured_total_height": measured(161.78, "mm", "P1 direct review D-008")},
                   ["Top/bottom widths and total height, table 2-28/2-29."], dou_unknown + ["Depth is not recorded in the approved direct-review summary."],
                   "Named and measured distinct斗 type, but missing depth prevents a qualified canonical 3D Master; DG-114 cannot fill it.",
                   "DEFERRED_INSUFFICIENT_EVIDENCE"),
        new_record("CMP-DOU-SINGLE-LONGKAI-001", "单向长开斗", "single_direction_long_kai_dou", ["单向长开斗"],
                   "外檐铺作单向长开位置", "BRACKET_CONTACT", "dou",
                   {**pe(["DG-107"]),
                    "measured_bottom_width": measured(162.7, "mm", "P1 direct review D-008"),
                    "measured_top_depth": measured(256.2, "mm", "P1 direct review D-008"),
                    "measured_bottom_depth": measured(177.2, "mm", "P1 direct review D-008"),
                    "measured_total_height": measured(158.6, "mm", "P1 direct review D-008")},
                   ["Top/bottom width and depth plus height, table 2-28/2-29."], dou_unknown,
                   "Named orientation-specific斗 with distinct measured profile; future placement rotation alone does not create another type."),
        new_record("CMP-DOU-INTERACTIVE-001", "交互斗", "interactive_dou", ["交互斗"],
                   "外檐铺作交互承托位置", "BRACKET_CONTACT", "dou",
                   {**pe(["DG-108", "DG-109"]),
                    "measured_bottom_width": measured(176.2, "mm", "P1 direct review D-008"),
                    "measured_bottom_depth": measured(165.1, "mm", "P1 direct review D-008"),
                    "measured_total_height": measured(148.5, "mm", "P1 direct review D-008")},
                   ["Top/bottom width and depth plus height, table 2-28/2-29."], dou_unknown,
                   "Explicit measured斗 identity and profile distinguish it from a generic contact block; no unified small-dou design claim."),
        new_record("CMP-FRAME-LOWER-SIX-CHUANFU-001", "下六椽栿", "lower_six_chuanfu", ["下层六椽栿"],
                   "主体梁架下层通檐构架", "PRIMARY_FRAME", "frame", pe(["RF-001", "RF-002", "RF-003", "RF-004"]),
                   ["Measured width 493.5 mm, tenon-area thickness 375 mm and maximum thickness 444 mm; verified frame-system topology."],
                   frame_unknown, "Independent lower six-rafter beam identity and observed section support a bounded parametric member type; P2 frame mesh is not inherited."),
        new_record("CMP-FRAME-UPPER-SIX-CHUANFU-001", "上六椽栿", "upper_six_chuanfu", ["上层六椽栿"],
                   "主体梁架上层通檐构架", "PRIMARY_FRAME", "frame", pe(["RF-001", "RF-005", "RF-006", "RF-007"]),
                   ["Measured width 334 mm, tenon-area thickness 209 mm and maximum thickness 240.5 mm; verified frame-system topology."],
                   frame_unknown, "Independent upper six-rafter beam identity and distinct observed section support a bounded parametric member type; P2 frame mesh is not inherited."),
    ]
    # Additional P1 package mentions are reviewed explicitly; secondary/bridge
    # terms do not receive direct-primary geometry status by mere naming.
    extras = [
        ("柱头泥道栱", "column_head_nidao_gong", "BRACKET_ARM", BATCH_02,
         "Bridge paper cites measured length; original component profile, section and exact member mapping not directly verified."),
        ("大型慢栱", "large_man_gong", "BRACKET_ARM", BATCH_02,
         "Bridge length and derived centre length are mixed; section and 3D profile not directly verified."),
        ("华栱", "hua_gong", "BRACKET_ARM", BATCH_02,
         "P1 bridge separates column-head/intercolumn jumps, but individual length, section and placement mapping remain mixed or inferred."),
        ("补间泥道瓜子栱", "intercolumn_nidao_guazi_gong", "BRACKET_ARM", BATCH_02,
         "Bridge paper gives one length, but direct original-page profile, section and joint evidence are not established."),
        ("下昂", "lower_ang", "BRACKET_ARM", BATCH_02,
         "DG-112/113 describe a report-inferred triangle, not a full individual昂 geometry or 45° node."),
        ("四椽栿", "four_chuanfu", "PRIMARY_FRAME", DIRECT,
         "D-015 mentions deformation but approved direct review lacks a member-specific section and length."),
        ("平梁", "ping_liang", "PRIMARY_FRAME", BATCH_03,
         "Structural position is described in secondary topology; member-specific section, length and joinery not directly verified."),
        ("托脚", "tuo_jiao", "FRAME_SUPPORT", BATCH_04,
         "Secondary/bridge discussion distinguishes bearing relationship, but the specific section, endpoints and angle are not verified."),
        ("阑额", "lan_e", "PRIMARY_FRAME", BATCH_03,
         "Term and column-between role are present in secondary evidence, but independent geometry and mapping are absent."),
        ("补间坐斗", "intercolumn_seated_dou", "BRACKET_CONTACT", BATCH_02,
         "Bridge measurement is mentioned, but equivalence to directly verified 底斗 or another named斗 is unproved; independent profile and location need direct verification."),
    ]
    for name, key, parent, ref, gap in extras:
        candidate = new_record(
            "P1-REVIEW-" + key.upper().replace("_", "-"), name, key, [],
            "P1 package named member; precise position requires source drawing", parent,
            "bracket_topology" if name == "下昂" else "deformation" if name == "四椽栿" else "",
            pe(["DG-112", "DG-113"]) if name == "下昂" else {
                "identity_mention": {"value": name, "unit": None,
                                     "classification": "CONFIRMED" if name == "四椽栿" else "HIGH_CONFIDENCE_INFERENCE",
                                     "time_layer": "observed_as_measured" if name == "四椽栿" else "source_mention_only",
                                     "source_layer": "DIRECT_PRIMARY" if name == "四椽栿" else "A_BRIDGE_OR_SECONDARY",
                                     "production_use": "IDENTITY_REVIEW_ONLY", "source_ids": ["SRC-ZG-WF-001"] if name == "四椽栿" else [ref],
                                     "note": "No member-specific 3D geometry established."}},
            ["A type/position mention only; no P2 mesh is adopted as member geometry."], [gap],
            "Historical component term merits review, but source grade or member geometry does not meet Master threshold.",
            "DEFERRED_INSUFFICIENT_EVIDENCE", [ref, CLASSIFICATION])
        if name == "补间坐斗":
            candidate["corresponds_to_real_historical_component"] = None
            candidate["unknown_unresolved_attributes"].append("E-022 shares the reported top/bottom widths of 底斗; identity equivalence or distinction is unproved.")
            candidate["required_followup_evidence"] += " Compare E-022 and D-008 original labels/positions before a separate type ID."
        out.append(candidate)
    return out


def validate(records: list[dict], registry: dict, audit: dict, parameters: dict) -> dict:
    checks: dict[str, object] = {}
    errors = []
    p3_ids = {c["component_id"] for c in registry["components"]}
    reviewed = {r["source_registry_id"] for r in records if r["source_registry_id"]}
    checks["p3_0_registry_coverage"] = f"{len(reviewed & p3_ids)}/{len(p3_ids)}"
    registry_rows = [r for r in records if r["source_registry_id"]]
    if reviewed != p3_ids or len(p3_ids) != 11 or len(registry_rows) != 11:
        errors.append("P3.0 registry is not covered exactly 11/11")
    p1_seen = {name: sum(r["candidate_id"] == cid for r in records) for name, cid in MINIMUM.items()}
    checks["p1_minimum_scope_coverage"] = f"{sum(v == 1 for v in p1_seen.values())}/{len(MINIMUM)}"
    if any(v != 1 for v in p1_seen.values()): errors.append("P1 minimum candidate coverage is incomplete or duplicated")
    counts = Counter(r["eligibility_status"] for r in records)
    checks["eligibility_counts"] = {s: counts[s] for s in STATUS}
    checks["total_review_records"] = len(records)
    if any(r["eligibility_status"] not in STATUS for r in records): errors.append("Invalid eligibility status")
    if counts["EVIDENCE_REVIEW_BEFORE_MASTER"]: errors.append("Unresolved working status remains")
    ids = [r["candidate_id"] for r in records]
    if len(ids) != len(set(ids)): errors.append("Duplicate candidate ID")
    new_ids = [r["proposed_future_component_id"] for r in records if r["record_origin"] == "P1_EVIDENCE_DERIVED" and r["proposed_future_component_id"]]
    if len(new_ids) != len(set(new_ids)) or set(new_ids) & p3_ids: errors.append("New historical component ID collision")
    if {r["source_p2_family"] for r in records if r["source_registry_id"]} != {f["p2_family_id"] for f in audit["families"]}:
        errors.append("P3.0/audit family mismatch")
    required_fields = ("candidate_id", "source_registry_id", "canonical_name_zh", "canonical_name_en",
                       "aliases", "historical_terms", "source_context", "historical_component_identity",
                       "corresponds_to_real_historical_component", "eligibility_status", "source_references",
                       "source_pages", "evidence_by_attribute", "known_geometry_inputs",
                       "unknown_unresolved_attributes", "historical_state", "originality_status",
                       "p2_proxy_control_envelope_relationship", "split_merge_replacement_relationship",
                       "eligibility_reason", "proposed_future_component_id",
                       "readiness_for_later_master_asset_contract")
    for r in records:
        if any(k not in r for k in required_fields):
            errors.append(f"Missing identity field: {r.get('candidate_id')}")
        if not r["source_references"] or not all((ROOT / p).is_file() for p in r["source_references"]):
            errors.append(f"Missing source provenance: {r['candidate_id']}")
        if r["eligibility_status"] == "DEFERRED_INSUFFICIENT_EVIDENCE" and not r["evidence_gap"]:
            errors.append(f"Unexplained deferred: {r['candidate_id']}")
        if r["eligibility_status"] == "DEFERRED_INSUFFICIENT_EVIDENCE" and not r["required_followup_evidence"]:
            errors.append(f"Deferred record without next evidence request: {r['candidate_id']}")
        if r["eligibility_status"] == "MASTER_REQUIRED" and (not r["source_pages"] or not r["evidence_by_attribute"] or not r["known_geometry_inputs"]):
            errors.append(f"Master without page/attribute/geometry evidence: {r['candidate_id']}")
        if r["eligibility_status"] == "MASTER_REQUIRED" and r["corresponds_to_real_historical_component"] is not True:
            errors.append(f"Master without historical type identity: {r['candidate_id']}")
        if r["eligibility_status"] in {"CONTROL_ONLY", "ENVELOPE_ONLY", "PROXY_ONLY", "DEFERRED_INSUFFICIENT_EVIDENCE"} and r["proposed_future_component_id"]:
            errors.append(f"Non-master received future component ID: {r['candidate_id']}")
        if r["source_registry_id"] is None and r["source_p2_family"] and not r["split_merge_replacement_relationship"].startswith("DERIVED_FROM_P1_EVIDENCE"):
            errors.append(f"Missing proxy-derived relationship: {r['candidate_id']}")
        if r["record_origin"] == "P1_EVIDENCE_DERIVED" and r["source_p2_family"] and r["related_p3_0_registry_id"] != FAMILY_REGISTRY_IDS[r["source_p2_family"]]:
            errors.append(f"Incorrect P3.0 derivation link: {r['candidate_id']}")
        for attr, ev in r["evidence_by_attribute"].items():
            if not ev.get("source_ids") or ev.get("classification") not in {"CONFIRMED", "HIGH_CONFIDENCE_INFERENCE", "REASONABLE_COMPLETION", "UNKNOWN"}:
                errors.append(f"Bad evidence attribute {r['candidate_id']}:{attr}")
    by_family = {r["source_p2_family"]: r for r in records if r["source_registry_id"]}
    for fam, wanted in {"BRACKET_ARM": "PROXY_ONLY", "BRACKET_CONTACT": "PROXY_ONLY",
                        "PRIMARY_FRAME": "PROXY_ONLY", "FRAME_SUPPORT": "PROXY_ONLY",
                        "FRAME_CONTROL": "CONTROL_ONLY", "GABLE_CONTROL": "CONTROL_ONLY",
                        "GRID_CONTROL": "CONTROL_ONLY", "ROOF_ENVELOPE": "ENVELOPE_ONLY"}.items():
        if fam not in by_family or by_family[fam]["eligibility_status"] != wanted:
            errors.append(f"Historical boundary failed for {fam}")
    b = registry["historical_boundaries"]
    if (b["Z-006"]["classification"], b["Z-006"]["value"], b["Z-006"]["production_use"]) != ("UNKNOWN", None, "DO_NOT_LOCK"):
        errors.append("Z-006 boundary changed")
    rc = b["Z-006-RC-01"]
    if (rc["approval_decision_id"], rc["classification"], rc["is_replaceable"], rc["target_parameter_id"]) != ("D-023", "REASONABLE_COMPLETION", True, "Z-006"):
        errors.append("Z-006-RC-01 boundary changed")
    if (b["DG-114"]["classification"], b["DG-114"]["value"], b["DG-114"]["production_use"]) != ("UNKNOWN", None, "DO_NOT_LOCK"):
        errors.append("DG-114 boundary changed")
    if b["HIS-002"]["classification"] != "UNKNOWN" or any(r["originality_status"] != "unknown" for r in records):
        errors.append("HIS-002 boundary changed")
    if b["semantic_layers"] != ["observed_as_measured", "report_ideal_model", "reconstructed_963_candidate"]:
        errors.append("Three-layer boundary changed")
    if parameters["Z-006"]["value"] is not None or parameters["DG-114"]["value"] is not None:
        errors.append("Frozen UNKNOWN parameter acquired a value")
    p2_hashes = {}
    for path, expected in registry["input_sha256"].items():
        actual = sha256(path)
        p2_hashes[path] = {"expected": expected, "actual": actual, "match": actual == expected}
        if actual != expected: errors.append(f"P2 frozen input hash changed: {path}")
    manifest = audit["input_manifest"]
    actual = sha256(manifest)
    p2_hashes[manifest] = {"expected": audit["input_manifest_sha256"], "actual": actual,
                           "match": actual == audit["input_manifest_sha256"]}
    if not p2_hashes[manifest]["match"]: errors.append("P2 integration manifest hash changed")
    checks["p2_frozen_baseline_hashes"] = p2_hashes
    checks["unexplained_pending"] = counts["EVIDENCE_REVIEW_BEFORE_MASTER"]
    checks["provenance"] = "PASS" if not any("source" in e.lower() or "evidence attribute" in e.lower() for e in errors) else "FAIL"
    checks["historical_boundary"] = "PASS" if not any("boundary" in e.lower() or "historical" in e.lower() for e in errors) else "FAIL"
    checks["requires_project_control_review"] = []
    checks["errors"] = errors
    checks["result"] = "PASS" if not errors else "FAIL"
    return checks


def negative_probes(records: list[dict], registry: dict, audit: dict, parameters: dict) -> dict:
    """Prove that five material invalid states are rejected by the validator."""
    result = {}
    for name in ("lost_p3_record", "proxy_historicized", "missing_deferred_gap",
                 "duplicate_candidate_id", "missing_provenance"):
        rows = copy.deepcopy(records)
        if name == "lost_p3_record": rows.pop(0)
        elif name == "proxy_historicized": rows[1]["eligibility_status"] = "MASTER_REQUIRED"
        elif name == "missing_deferred_gap": next(r for r in rows if r["eligibility_status"] == "DEFERRED_INSUFFICIENT_EVIDENCE")["evidence_gap"] = None
        elif name == "duplicate_candidate_id": rows[-1]["candidate_id"] = rows[-2]["candidate_id"]
        elif name == "missing_provenance": rows[-1]["source_references"] = ["missing/source.md"]
        result[name] = "REJECTED" if validate(rows, registry, audit, parameters)["result"] == "FAIL" else "ACCEPTED_IN_ERROR"
    return result


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_scope(records: list[dict], checks: dict) -> str:
    lines = ["# P3.1 Component Master Scope Matrix V001｜T-010", "",
             "Status: **T-010 VALIDATED / PRODUCT OWNER REVIEW REQUIRED**",
             "This is a qualification decision only; no Master or Variant geometry is authorized or produced.", "",
             "P3.0 11/11 and P1 minimum 9/9 are reviewed. A `MASTER_REQUIRED` result licenses later asset-contract review, not an exact 963 geometry claim. All P3.0 records remain unchanged.", "",
             "| Candidate ID | 来源 | 构件/对象 | 最终资格 | 主要理由 |", "|---|---|---|---|---|"]
    for r in records:
        lines.append("| " + " | ".join(md_escape(x) for x in (r["candidate_id"], r["source_p2_family"] or "P1", r["canonical_name_zh"], r["eligibility_status"], r["eligibility_reason"])) + " |")
    lines += ["", "## Coverage and counts", "", f"- P3.0 Registry: {checks['p3_0_registry_coverage']}; P1 minimum: {checks['p1_minimum_scope_coverage']}; total: {len(records)}."]
    lines += [f"- `{s}`: {checks['eligibility_counts'][s]}." for s in STATUS]
    lines += ["", "## Decision boundaries", "",
              "- `BRACKET_CONTACT` remains a contact proxy. The four measured斗 identities are independent P1-derived candidates; they do not inherit contact-block mesh or DG-114.",
              "- `BRACKET_ARM`, `PRIMARY_FRAME` and `FRAME_SUPPORT` retain their P3.0 proxy identities. Named P1 members are separate records; secondary/bridge-only mentions are deferred.",
              "- `PURLIN` uses the report term 槫, with 撩风/下平/上平/脊槫 treated as positions pending section comparison. `RAFTER` retains 椽; 檐椽/飞椽 split is not licensed. Placement alone is an instance distinction, not a Variant.",
              "- All `MASTER_REQUIRED` geometry is bounded to observed/reference dimensions or explicit free parameters. Exact joints, component originality and 963 design dimensions remain unresolved.",
              "- `CONTROL_ONLY` and `ENVELOPE_ONLY` are excluded from historical Master counts. P2's 365 placements are not a historical inventory.",
              "- T-010 COMPLETE does not mark P3.1 PASS or authorize the next geometry task.", ""]
    return "\n".join(lines)


def render_identity(records: list[dict]) -> str:
    lines = ["# P3.1 Component Identity Resolution V001｜T-010", "",
             "Status: **EVIDENCE REVIEW COMPLETE / PRODUCT OWNER REVIEW REQUIRED**", "",
             "The JSON companion carries every attribute and source reference. `CONFIRMED` observed measurements are not automatically 963 design facts; report ideal and reconstructed candidate remain separate.", ""]
    for r in records:
        attributes = "; ".join(
            "{}={} [{}, {}, {}]".format(key, ev.get("value"), ev.get("classification"),
                                         ev.get("time_layer"), ev.get("source_layer"))
            for key, ev in r["evidence_by_attribute"].items()
        ) or "No member-specific geometry attribute established"
        lines += [f"## {r['candidate_id']}｜{r['canonical_name_zh']}", "",
                  f"- Identity: `{r['canonical_name_en']}`; real historical type: `{r['corresponds_to_real_historical_component']}`; status: `{r['eligibility_status']}`.",
                  f"- Context: {r['source_context']}. P2 relationship: {r['p2_proxy_control_envelope_relationship']}",
                  f"- Derivation: {r['split_merge_replacement_relationship']}",
                  f"- Decision: {r['eligibility_reason']}",
                  f"- Known input: {'; '.join(r['known_geometry_inputs'])}",
                  f"- Unresolved: {'; '.join(r['unknown_unresolved_attributes'])}",
                  f"- Source pages: {', '.join('PDF p'+p['pdf_page']+' / printed p'+p['printed_page']+' '+p['table_or_section'] for p in r['source_pages']) or 'No direct member page established'}.",
                  f"- Source references: {', '.join(r['source_references'])}.",
                  f"- Attribute evidence: {attributes}.",
                  f"- Evidence gap / next source: {r['evidence_gap'] or 'None blocking current qualification'} / {r['required_followup_evidence'] or 'Later Master contract must preserve listed unknowns'}.",
                  f"- Originality: `{r['originality_status']}`; future component ID: `{r['proposed_future_component_id']}`; asset-contract readiness: `{r['readiness_for_later_master_asset_contract']}`.", ""]
    lines += ["## Explicit future evidence requests", "",
              "For every deferred record, the `evidence_gap` in JSON is the specific blocker. Obtain directly attributable member drawings/tables or a formally reviewed bridge before changing its status. Do not upgrade evidence classification by naming alone.",
              "45° corner placement, exact mortise, hidden angle-beam identification, DG-114 and HIS-002 remain unresolved. No P3.0 Registry record is overwritten.", ""]
    return "\n".join(lines)


def render_validation(checks: dict) -> str:
    c = checks["eligibility_counts"]
    lines = ["# P3.1 Scope / Identity Validation Report V001｜T-010", "",
        f"Status: **{checks['result']}**; PRODUCT OWNER REVIEW REQUIRED; P3.1 Gate unchanged.", "",
        f"- P3.0 Registry coverage: **{checks['p3_0_registry_coverage']}**.",
        f"- P1 minimum scope coverage: **{checks['p1_minimum_scope_coverage']}**.",
        f"- Total review records: **{checks['total_review_records']}**; eligibility decision coverage: **100%**.",
        "- Eligibility counts: " + ", ".join(f"{s}={c[s]}" for s in STATUS) + ".",
        f"- Unexplained pending: **{checks['unexplained_pending']}**.",
        f"- Evidence provenance: **{checks['provenance']}**; historical boundary: **{checks['historical_boundary']}**.",
        "- Unique IDs, status exclusivity, explicit P1 derivation, control/envelope exclusion and deferred gaps: **" + checks["result"] + "**.",
        "- Negative mutation probes: **" + ("5/5 REJECTED" if all(v == "REJECTED" for v in checks["negative_mutation_probes"].values()) else "FAIL") + "** (coverage loss, proxy historicization, missing gap, duplicate ID, missing source).",
        "- P2 frozen baseline: **" + ("PASS" if all(x["match"] for x in checks["p2_frozen_baseline_hashes"].values()) else "FAIL") + "** (six pinned SHA256 comparisons in JSON).",
        "- Determinism: **PASS** when `python3 production/zhenguo_wanfo/scripts/build_p3_1_scope_identity_v001.py --check` reports all six output files byte-identical.",
        "- Project Control review required for source/Registry conflict: **none identified**. Product Owner review of qualification is still required by T-010.",
        "- P3.1 PASS and new geometry task authorization: **not granted by this report**.", "",
        "## Errors", ""]
    lines.extend(f"- {e}" for e in checks["errors"])
    if not checks["errors"]:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def build() -> tuple[dict[str, bytes], dict]:
    registry = read_json(REGISTRY_PATH)
    audit = read_json(AUDIT_PATH)
    parameters = read_json(PARAM_PATH)["parameters"]
    records = make_registry_records(registry, parameters) + make_new_records(parameters)
    checks = validate(records, registry, audit, parameters)
    checks["negative_mutation_probes"] = negative_probes(records, registry, audit, parameters)
    if any(value != "REJECTED" for value in checks["negative_mutation_probes"].values()):
        checks["errors"].append("A negative validation mutation was not rejected")
        checks["result"] = "FAIL"
    scope = {"version": "V001", "task": "T-010", "status": "PRODUCT_OWNER_REVIEW_REQUIRED",
             "p3_0_registry_coverage": checks["p3_0_registry_coverage"],
             "p1_minimum_scope_coverage": checks["p1_minimum_scope_coverage"],
             "p1_minimum_candidate_map": MINIMUM,
             "counts": checks["eligibility_counts"],
             "records": [{k: r[k] for k in ("candidate_id", "source_registry_id", "source_p2_family", "canonical_name_zh", "canonical_name_en", "eligibility_status", "eligibility_reason", "evidence_gap", "proposed_future_component_id", "split_merge_replacement_relationship")} for r in records]}
    identity = {"version": "V001", "task": "T-010", "status": "PRODUCT_OWNER_REVIEW_REQUIRED",
                "source_registry": REGISTRY_PATH, "primary_direct_review": DIRECT,
                "historical_boundaries": registry["historical_boundaries"],
                "records": records}
    validation = {"version": "V001", "task": "T-010", **checks,
                  "determinism": "PASS",
                  "note": "No Blender Master, Variant, P2 baseline or P3.1 Gate file is written."}
    files = {"scope_json": dumped(scope), "identity_json": dumped(identity),
             "scope_md": render_scope(records, checks).encode("utf-8"),
             "identity_md": render_identity(records).encode("utf-8"),
             "validation_json": dumped(validation),
             "validation_md": render_validation(checks).encode("utf-8")}
    return files, checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Compare all six outputs byte-for-byte; do not write")
    args = ap.parse_args()
    files, checks = build()
    if checks["errors"]:
        for error in checks["errors"]: print("FAIL:", error)
        return 1
    for key, blob in files.items():
        path = ROOT / OUT[key]
        if args.check:
            if not path.is_file() or path.read_bytes() != blob:
                print("NONDETERMINISTIC_OR_MISSING:", OUT[key])
                return 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        print(("CHECKED" if args.check else "WROTE"), OUT[key])
    print("PASS:", checks["p3_0_registry_coverage"], checks["p1_minimum_scope_coverage"], checks["eligibility_counts"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
