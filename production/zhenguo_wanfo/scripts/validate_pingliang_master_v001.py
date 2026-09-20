"""Validate T-022 Pingliang Master first article and formal variants."""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pmap(data):
    return {x["key"]:x for x in data["parameters"]}


def vmap(data):
    return {x["variant_id"]:x for x in data["variants"]}


def near(a,b,tol=1e-3):
    return abs(float(a)-float(b)) <= tol


def same_dims(a,b,tol=1e-3):
    return len(a)==len(b) and all(near(x,y,tol) for x,y in zip(a,b))


def main():
    ap=argparse.ArgumentParser()
    names=[
        "params","ew","ew_reopen","gable","gable_reopen",
        "length","width","thickness","gable_completion",
        "restore_ew","restore_gable","ew_asset","gable_asset",
        "review_dir","registry","source_catalog","output","catalog","report"
    ]
    for name in names:
        ap.add_argument("--"+name.replace("_","-"),dest=name,required=True)
    a=ap.parse_args()

    p=load(a.params)
    gp=pmap(p)
    vs=vmap(p)
    ew=load(a.ew)
    ewr=load(a.ew_reopen)
    ga=load(a.gable)
    gar=load(a.gable_reopen)
    lm=load(a.length)
    wm=load(a.width)
    tm=load(a.thickness)
    gm=load(a.gable_completion)
    rew=load(a.restore_ew)
    rga=load(a.restore_gable)
    reg=load(a.registry)
    source_catalog=load(a.source_catalog)

    checks={}
    def ck(name,condition):
        if not condition:
            raise AssertionError(name)
        checks[name]="PASS"

    def dims(s):
        return [float(x) for x in s["body"]["local_bbox_mm"]["dimensions"]]

    ewv=vs["EW_SEAM"]
    gav=vs["GABLE"]
    ed=dims(ew); gd=dims(ga)
    ld=dims(lm); wd=dims(wm); td=dims(tm); gmd=dims(gm)
    items=[x for x in reg["items"] if x.get("component")=="平梁"]
    ids={x["id"] for x in items}
    byid={x["id"]:x for x in items}
    review=Path(a.review_dir)
    review_names=[
        "EW_SEAM_FRONT.png","EW_SEAM_SIDE.png","EW_SEAM_TOP.png","EW_SEAM_AXON.png",
        "GABLE_FRONT.png","GABLE_SIDE.png","GABLE_TOP.png","GABLE_AXON.png",
        "DIMENSION_PARAMETER_SUMMARY.png","EVIDENCE_UNCERTAINTY_SUMMARY.png"
    ]

    ck("01_component_id",p["component_id"]==ew["component_id"]==ga["component_id"]=="CMP-FRAME-PINGLIANG-001")
    ck("02_master_id",p["master_id"]==ew["master_id"]==ga["master_id"]=="CMP-FRAME-PINGLIANG-001_MASTER")
    ck("03_registry_v008_505",reg["schema_version"]=="V008" and reg["item_count"]==505)
    ck("04_pingliang_instance_count_4",len(items)==4)
    ck("05_exact_instance_ids",ids=={"平梁-东缝","平梁-西缝","平梁-东山","平梁-西山"})
    sb=p["source_binding"]
    ck("06_source_binding",sb["source_id"]=="SRC-ZG-WF-001" and sb["pdf_page"]==83 and sb["printed_page"]==68 and sb["table"]=="2-40" and sb["figure"]=="2-41")
    ck("07_two_stable_variants",set(vs)=={"EW_SEAM","GABLE"} and ewv["stable_variant_id"]=="CMP-FRAME-PINGLIANG-001__EW_SEAM" and gav["stable_variant_id"]=="CMP-FRAME-PINGLIANG-001__GABLE")
    es=ewv["observed_section_samples_mm"]
    ck("08_ew_sample_a",es[0]=={"width":390.0,"thickness":280.0})
    ck("09_ew_sample_b",es[1]=={"width":401.0,"thickness":281.0})
    ck("10_ew_mapping_unknown",ewv["sample_to_instance_mapping"]=="UNKNOWN" and all(byid[i]["sample_to_instance_mapping"]=="UNKNOWN" for i in ("平梁-东缝","平梁-西缝")))
    ck("11_ew_mean_width",ewv["production_section_mm"]["width"]==395.5)
    ck("12_ew_mean_thickness",ewv["production_section_mm"]["thickness"]==280.5)
    ck("13_ew_report_metadata_only",ewv["report_design_analysis"]["width_fen_rounded"]==26 and ewv["report_design_analysis"]["thickness_fen_rounded"]==18 and ewv["report_design_analysis"]["geometry_use_count"]==0)

    gs=gav["observed_section_samples_mm"]
    ck("14_gable_one_observed_sample",len(gs)==1 and gs[0]["width"]==346.0)
    ck("15_gable_observed_thickness_null",gs[0]["thickness"] is None and gav["observed_section_mm"]["thickness"] is None and all(byid[i]["thickness_mm"] is None for i in ("平梁-东山","平梁-西山")))
    ck("16_gable_mapping_unknown",gav["sample_to_instance_mapping"]=="UNKNOWN" and all(byid[i]["sample_to_instance_mapping"]=="UNKNOWN" for i in ("平梁-东山","平梁-西山")))
    ck("17_gable_production_width",gav["production_section_mm"]["width"]==346.0)
    ck("18_gable_production_thickness",gav["production_section_mm"]["thickness"]==245.4)
    calc=round(346.0*280.5/395.5,1)
    ck("19_gable_formula_rounds_245_4",calc==245.4 and gav["thickness_semantics"]["formula"]=="346 * 280.5 / 395.5")
    ck("20_gable_width_completion_class",gav["width_semantics"]["classification"]=="PARAMETRIC_COMPLETION")
    ck("21_gable_width_replaceable_nonhistorical",gav["width_semantics"]["replaceable"] is True and gav["width_semantics"]["historical_claim"] is False)
    ck("22_gable_thickness_completion_class",gav["thickness_semantics"]["classification"]=="PARAMETRIC_COMPLETION")
    ck("23_gable_thickness_replaceable_nonhistorical",gav["thickness_semantics"]["replaceable"] is True and gav["thickness_semantics"]["historical_claim"] is False)
    ck("24_gable_report_metadata_only",gav["report_design_analysis"]["width_fen_rounded"]==23 and gav["report_design_analysis"]["thickness_fen_rounded"] is None and gav["report_design_analysis"]["geometry_use_count"]==0)

    ck("25_historical_length_null",gp["historical_full_length_mm"]["value"] is None and ew["resolved_global_parameters"]["historical_full_length_mm"] is None and ga["resolved_global_parameters"]["historical_full_length_mm"] is None)
    ref=gp["canonical_reference_length_mm"]
    ck("26_reference_nonhistorical",ref["value"]==1000.0 and ref["classification"]=="PROJECT_RULE" and ref["production_use"]=="CANONICAL_REFERENCE_ONLY" and ref["historical_claim"] is False)
    ck("27_realization_derives_reference",gp["realization_length_mm"]["derives_from"]=="canonical_reference_length_mm" and gp["realization_length_mm"]["value"]==1000.0)
    ck("28_ew_x_extent",near(ed[0],1000.0))
    ck("29_ew_y_extent",near(ed[1],395.5))
    ck("30_ew_z_extent",near(ed[2],280.5))
    ck("31_gable_x_extent",near(gd[0],1000.0))
    ck("32_gable_y_extent",near(gd[1],346.0))
    ck("33_gable_z_extent",near(gd[2],245.4))
    ck("34_canonical_transforms",ew["body"]["local_transform"]==ga["body"]["local_transform"]=={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]})
    ck("35_unsupported_geometry_zero",ew["body"]["unsupported_detail_count"]==0 and ga["body"]["unsupported_detail_count"]==0 and ew["unsupported_geometry"]==[] and ga["unsupported_geometry"]==[])
    ck("36_p2_proxy_zero",p["p2_primary_frame_proxy_geometry_use_count"]==0)
    ck("37_independent_reopen_both",ewr["status"]=="PASS" and gar["status"]=="PASS" and ewr["body"]==ew["body"] and gar["body"]==ga["body"])
    ck("38_deterministic_restore_ew",rew["semantic_geometry_signature"]==ew["semantic_geometry_signature"] and rew["body"]==ew["body"])
    ck("39_deterministic_restore_gable",rga["semantic_geometry_signature"]==ga["semantic_geometry_signature"] and rga["body"]==ga["body"])
    ck("40_length_mutation_x_only",not near(ld[0],ed[0]) and same_dims(ld[1:],ed[1:]))
    ck("41_ew_width_mutation_y_only",not near(wd[1],ed[1]) and near(wd[0],ed[0]) and near(wd[2],ed[2]))
    ck("42_ew_thickness_mutation_z_only",not near(td[2],ed[2]) and same_dims(td[:2],ed[:2]))
    ck("43_gable_completion_mutation_z_only",not near(gmd[2],gd[2]) and same_dims(gmd[:2],gd[:2]))
    ck("44_gable_mutation_keeps_completion_semantics",gm["variant_semantics"]["thickness_semantics"]["classification"]=="PARAMETRIC_COMPLETION" and gm["variant_semantics"]["thickness_semantics"]["historical_claim"] is False)
    ck("45_review_ten_complete",all((review/n).exists() and (review/n).stat().st_size>1000 for n in review_names))

    ew_sha=digest(a.ew_asset); ga_sha=digest(a.gable_asset)
    ck("46_binary_sha_both",len(ew_sha)==64 and len(ga_sha)==64 and ew_sha!=ga_sha)
    ck("47_blend_artifact_only",str(a.ew_asset).startswith("artifacts/") and str(a.gable_asset).startswith("artifacts/"))
    ck("48_registry_completion_declared",all(byid[i]["modeling_disposition"].startswith("PARAMETRIC_COMPLETION") and byid[i]["parametric_completion"]["production_value_mm"]==245.4 for i in ("平梁-东山","平梁-西山")))
    ck("49_no_reference_length_leak",p["assembly_length_rule"]["hard_fail_id"]=="REFERENCE_LENGTH_LEAKS_INTO_BUILDING" and p["assembly_length_rule"]["default_to_canonical_reference_allowed"] is False)
    ck("50_no_silent_historicization",p["historical_state"]["historical_claim"] is False and p["historical_state"]["reconstructed_963_candidate"]=="not_inferred")
    ck("51_no_undeclared_parametric_completion",gav["width_semantics"]["classification"]=="PARAMETRIC_COMPLETION" and gav["thickness_semantics"]["classification"]=="PARAMETRIC_COMPLETION")
    ck("52_no_legacy_proxy_as_real_component",p["p2_primary_frame_proxy_geometry_use_count"]==0)
    ck("53_variant_ids_match_semantics",ew["variant_id"]=="EW_SEAM" and ga["variant_id"]=="GABLE" and ew["stable_variant_id"]==ewv["stable_variant_id"] and ga["stable_variant_id"]==gav["stable_variant_id"])
    ck("54_blender_4_5_13",str(ew["blender_version"]).startswith("4.5.13") and str(ga["blender_version"]).startswith("4.5.13"))

    catalog=copy.deepcopy(source_catalog)
    catalog["task"]="T-022"
    catalog["status"]="SOURCE_CATALOG_PLUS_PINGLIANG_ENGINEERING_COMPLETE_PENDING_REVIEW"
    records=list(catalog.get("new_masters",[]))
    ck("55_no_duplicate_pingliang_in_source_catalog",not any(x.get("component_id")==p["component_id"] for x in records))
    records.append({
        "component_id":p["component_id"],
        "master_id":p["master_id"],
        "master_version":"V001",
        "variant_ids":["EW_SEAM","GABLE"],
        "approval_status":"ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
        "canonical_asset_status":"ACTIONS_ARTIFACT",
        "canonical_asset_sha256":{"EW_SEAM":ew_sha,"GABLE":ga_sha},
        "parametric_completion":{"GABLE_thickness_mm":245.4,"replaceable":True,"historical_claim":False}
    })
    catalog["new_masters"]=records
    Path(a.catalog).write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ck("56_catalog_pingliang_pending_only",records[-1]["approval_status"]=="ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW")

    result={
        "task":"T-022",
        "status":"PASS",
        "approval_boundary":"ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW",
        "check_count":len(checks),
        "checks":checks,
        "blender_version":ew["blender_version"],
        "canonical_blend_sha256":{"EW_SEAM":ew_sha,"GABLE":ga_sha},
        "review_paths":review_names,
        "variants":{
            "EW_SEAM":{"section_mm":[395.5,280.5],"classification":"DIRECT_MEASURED_FAMILY_MEAN"},
            "GABLE":{"section_mm":[346.0,245.4],"classification":"PARAMETRIC_COMPLETION / REPLACEABLE / NON_HISTORICAL"}
        },
        "mutation_evidence":{
            "length":ld,
            "ew_width":wd,
            "ew_thickness":td,
            "gable_completion_thickness":gmd,
            "canonical_restored":True
        },
        "reopen_evidence":{"EW_SEAM":ewr,"GABLE":gar}
    }
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    Path(a.report).write_text(
        "# T-022｜平梁 Master First Article｜Engineering Review\n\n"
        "Status: **ENGINEERING PASS / PENDING CHATGPT + PRODUCT OWNER REVIEW**\n\n"
        f"- Validation: {len(checks)}/{len(checks)} PASS\n"
        f"- Blender: {ew['blender_version']}\n"
        f"- EW_SEAM binary SHA-256: {ew_sha}\n"
        f"- GABLE binary SHA-256: {ga_sha}\n"
        "- EW_SEAM section: 395.5 × 280.5 mm / measured family mean\n"
        "- GABLE section: 346 × 245.4 mm / explicit replaceable PARAMETRIC_COMPLETION\n"
        "- GABLE observed thickness: UNKNOWN / null\n"
        "- Historical full length: UNKNOWN / null\n"
        "- Canonical reference length: 1000 mm / non-historical only\n"
        "- Review images: 10/10\n"
        "- PR: DO NOT MERGE pending Product Owner review.\n",
        encoding="utf-8"
    )
    print("T022_VALIDATION_PASS",ew_sha,ga_sha)


if __name__=="__main__":
    main()
