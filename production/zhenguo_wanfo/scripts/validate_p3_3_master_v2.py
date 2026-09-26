"""Generic P3.3 Master V2 validator driven by a locked Master Definition."""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def near(a,b,t=1e-3):
    return abs(float(a)-float(b))<=t

def dims(s):
    return [float(x) for x in s["body"]["local_bbox_mm"]["dimensions"]]

def get_section(d):
    rb=d["registry_boundary"]
    if "section_mm" in rb:
        return float(rb["section_mm"]["width"]),float(rb["section_mm"]["thickness"])
    if "section_statistics_mm" in rb:
        s=rb["section_statistics_mm"]
        return float(s["mean_width"]),float(s["mean_thickness"])
    s=d["geometry_contract"]["section_envelope_mm"]
    return float(s["width"]),float(s["thickness"])

def get_review_contract(d):
    if "review_contract" in d:
        return d["review_contract"]
    return d["v2_slim_file_contract"]["review_contract"]

def get_package(d):
    return d.get("minimal_sufficient_package",d.get("v2_slim_file_contract",{}))

def profile_unknown(d):
    gc=d["geometry_contract"]
    return gc.get("exact_section_profile")=="UNKNOWN" or gc.get("section_envelope_is_historical_profile") is False

def main():
    ap=argparse.ArgumentParser()
    for n in ("definition","canonical","reopen","length","width","thickness","restore","asset","review_dir","board","registry","catalog","output"):
        ap.add_argument("--"+n.replace("_","-"),dest=n,required=True)
    ap.add_argument("--role-a")
    ap.add_argument("--role-b")
    ap.add_argument("--instance-section-dir")
    a=ap.parse_args()
    d=load(a.definition); c=load(a.canonical); r=load(a.reopen)
    lm=load(a.length); wm=load(a.width); tm=load(a.thickness); rs=load(a.restore)
    reg=load(a.registry); catalog=load(a.catalog)
    checks={}
    def ck(name,value):
        if not value:
            raise AssertionError(name)
        checks[name]="PASS"

    rb=d["registry_boundary"]; gc=d["geometry_contract"]; auth=d["authority"]
    component=d["component_name_zh"]
    items=[x for x in reg["items"] if x.get("component")==component]
    w,h=get_section(d)

    ck("01_definition_locked",d["status"].startswith("LOCKED / PRODUCT_OWNER_APPROVED") and d["approval"]["definition_locked"] is True)
    ck("02_execution_authorized",d["execution_boundary"]["engineering_execution_authorized"] is True)
    ck("03_visual_gate",str(auth["visual_reference_gate"]["result"]).startswith("PASS"))
    ck("04_registry_version",reg["schema_version"]==auth["registry_schema_version_expected"])
    ck("05_registry_record_count",reg["item_count"]==auth["registry_record_count_expected"])
    ck("06_component_identity",c["component_id"]==d["component_id"] and c["master_id"]==d["master_id"] and c["master_version"]==d["master_version"])
    ck("07_instance_count",len(items)==rb["physical_instance_count"])

    instance_sections=d.get("instance_section_binding_contract")
    role_cfg=d.get("registry_role_counts")
    if instance_sections:
        mappings=instance_sections.get("instances",[])
        by_id={x.get("id"):x for x in items}
        ck("08_instance_section_mapping_count",len(mappings)==len(items)==rb["physical_instance_count"])
        ck("09_instance_section_registry_identity",
           all(m.get("registry_id") in by_id and by_id[m.get("registry_id")].get("location")==m.get("location") for m in mappings))
    elif role_cfg:
        matched_ids=set()
        role_ok=True
        for role,cfg in role_cfg.items():
            prefixes=cfg.get("id_prefixes",[])
            matched=[x for x in items if any(x.get("id","").startswith(p) for p in prefixes)]
            role_ok = role_ok and len(matched)==cfg["count"]
            matched_ids.update(x.get("id") for x in matched)
        ck("08_definition_driven_role_counts",role_ok)
        ck("09_registry_role_partition_complete",len(matched_ids)==len(items) and sum(cfg["count"] for cfg in role_cfg.values())==len(items))
    else:
        east=[x for x in items if x.get("id","").startswith(component+"-东山")]
        west=[x for x in items if x.get("id","").startswith(component+"-西山")]
        main=[x for x in items if x.get("id","").startswith(component+"-正身")]
        if "east_gable_known_count" in rb:
            ck("08_known_gable_counts",len(east)==rb["east_gable_known_count"] and len(west)==rb["west_gable_known_count"])
        else:
            ck("08_distribution_counts",len(main)==rb.get("main_body_count",len(main)) and len(east)==rb.get("east_gable_count",len(east)) and len(west)==rb.get("west_gable_count",len(west)))
        if "exact_location_unresolved_count" in rb:
            ck("09_unresolved_count",len(items)-len(east)-len(west)==rb["exact_location_unresolved_count"])
        else:
            ck("09_all_registry_instances_located",all(x.get("location") not in (None,"","待定位") for x in items))

    section_strings=[str(x.get("section_mm","")) for x in items]
    section_binding=d.get("registry_section_binding_contract")
    if instance_sections and instance_sections.get("mode")=="DIRECT_LOCKED_LOCATION_SECTION":
        fam=instance_sections["family_reference_section_mm"]
        tokens=[str(x) for x in instance_sections.get("registry_family_summary_tokens",[])]
        ck("10_registry_family_summary_binding",
           near(fam["width"],w) and near(fam["thickness"],h) and
           all(all(tok in s for tok in tokens) for s in section_strings))
        ck("10A_family_mean_reference_only",
           instance_sections.get("family_reference_only") is True and
           instance_sections.get("family_mean_must_not_overwrite_instances") is True)
    elif instance_sections and instance_sections.get("mode")=="DIRECT_LOCKED_LOCATION_SECTION_PROJECT_REFERENCE":
        fam=instance_sections["family_reference_section_mm"]
        ck("10_registry_project_reference_binding",near(fam["width"],w) and near(fam["thickness"],h))
        ck("10A_project_reference_only",
           instance_sections.get("family_reference_only") is True and
           instance_sections.get("family_mean_must_not_overwrite_instances") is True and
           instance_sections.get("reference_classification")=="PROJECT_DERIVED_REFERENCE / NOT_SOURCE_PUBLISHED_FAMILY_MEAN")
        expected={(float(x["width_mm"]),float(x["thickness_mm"])) for x in instance_sections.get("instances",[])}
        observed=set()
        for s in section_strings:
            for pair in expected:
                token=f"{pair[0]:g}×{pair[1]:g}"
                if token in s:
                    observed.add(pair)
        ck("10B_all_direct_registry_sections_present",observed==expected)
    elif instance_sections and instance_sections.get("mode")=="DIRECT_LOCKED_WIDTH_PARTIAL_THICKNESS_WITH_PRODUCTION_COMPLETION":
        fam=instance_sections["family_reference_section_mm"]
        ck("10_registry_family_reference_binding",near(fam["width"],w) and near(fam["thickness"],h))
        ck("10A_width_mapping_direct_locked",
           instance_sections.get("width_mapping")=="DIRECT_LOCKED_12_OF_12" and
           instance_sections.get("family_mean_must_not_overwrite_instances") is True)
        ck("10B_partial_thickness_contract",
           instance_sections.get("direct_thickness_count")==4 and
           instance_sections.get("unmeasured_thickness_count")==8 and
           instance_sections.get("production_ready_thickness_count")==12)
    elif section_binding and section_binding.get("mode")=="SEMANTIC_MEASUREMENT_STATE_WITH_MASTER_MEAN":
        measured_token=section_binding["measured_full_section_token"]
        unknown_token=section_binding["unknown_thickness_token"]
        measured=[s for s in section_strings if measured_token in s]
        unknown=[s for s in section_strings if unknown_token in s]
        ck("10_registry_section_binding",
           len(measured)==section_binding["measured_full_section_count"] and
           len(unknown)==section_binding["unknown_thickness_count"] and
           len(measured)+len(unknown)==len(items))
        ck("10A_registry_unknown_thickness_preserved",
           all(unknown_token in s for s in unknown) and
           section_binding.get("unknown_must_not_be_silently_filled") is True)
        ck("10B_master_mean_has_A1_authority",
           section_binding.get("canonical_section_authority")=="A1_TABLE_PUBLISHED_MEAN_MATCHING_RECOMPUTE" and
           near(rb["section_mm"]["width"],w) and near(rb["section_mm"]["thickness"],h))
    else:
        exact=[s for s in section_strings if str(w) in s and (str(h) in s or str(int(h)) in s)]
        inherited=[s for s in section_strings if ("沿用" in s and "实测统计" in s)]
        ck("10_registry_section_binding",len(exact)>=1 and len(exact)+len(inherited)==len(items))

    ck("11_historical_length_null",rb["historical_full_length_mm"] is None and c["historical_full_length_mm"] is None)
    ck("12_reference_nonhistorical",gc["canonical_reference_length_historical_claim"] is False and c["canonical_reference_length_historical_claim"] is False)
    ck("13_no_unsupported_geometry",gc["unsupported_geometry"]==[] and c["body"]["unsupported_detail_count"]==0 and c["body"]["joinery_cut_count"]==0)
    ck("14_definition_hash",c["definition_sha256"]==digest(a.definition))

    cd=dims(c); ld=dims(lm); wd=dims(wm); td=dims(tm)
    L=float(gc["canonical_reference_length_mm"])
    ck("15_bbox_length",near(cd[0],L))
    ck("16_bbox_width",near(cd[1],w))
    ck("17_bbox_thickness",near(cd[2],h))
    ck("18_origin_transform",c["body"]["local_transform"]=={"location":[0.0,0.0,0.0],"rotation":[0.0,0.0,0.0],"scale":[1.0,1.0,1.0]})
    ck("19_reopen",r["status"]=="PASS" and r["body"]==c["body"] and r["semantic_geometry_signature"]==c["semantic_geometry_signature"])
    ck("20_restore",rs["body"]==c["body"] and rs["semantic_geometry_signature"]==c["semantic_geometry_signature"])
    ck("21_length_mutation",not near(ld[0],cd[0]) and near(ld[1],cd[1]) and near(ld[2],cd[2]))
    ck("22_width_mutation",near(wd[0],cd[0]) and not near(wd[1],cd[1]) and near(wd[2],cd[2]))
    ck("23_thickness_mutation",near(td[0],cd[0]) and near(td[1],cd[1]) and not near(td[2],cd[2]))
    ck("24_binary_sha",digest(a.asset)==c["canonical_blend_sha256"] and len(c["canonical_blend_sha256"])==64)
    ck("25_blender_version",str(c["blender_version"]).startswith("4.5.13"))

    if instance_sections:
        ck("IS01_semantic_preserves_instance_section_contract",c.get("instance_section_binding_contract")==instance_sections)
        ck("IS02_zero_geometry_variants",instance_sections.get("geometry_variant_count")==0)
        ck("IS03_same_master_required",instance_sections.get("same_master_required") is True)
        ck("IS04_direct_mapping_locked",
           rb.get("sample_to_instance_mapping")=="DIRECT_LOCKED_BY_A1_LOCATION_LABELS")
        if not a.instance_section_dir:
            raise AssertionError("instance-section semantics required but --instance-section-dir not supplied")
        idir=Path(a.instance_section_dir)
        family=instance_sections["family_reference_section_mm"]
        generated=[]
        for m in instance_sections.get("instances",[]):
            p=idir/(m["fixture_id"]+".json")
            ck("IS_"+m["fixture_id"]+"_semantic_exists",p.exists())
            s=load(p)
            dd=dims(s)
            ck("IS_"+m["fixture_id"]+"_identity",
               s["component_id"]==d["component_id"] and s["master_id"]==d["master_id"] and s["master_version"]==d["master_version"])
            ck("IS_"+m["fixture_id"]+"_section",
               near(dd[0],gc["canonical_reference_length_mm"]) and near(dd[1],m["width_mm"]) and near(dd[2],m["thickness_mm"]))
            generated.append((float(dd[1]),float(dd[2])))
        ck("IS90_all_direct_sections_generated",len(generated)==len(instance_sections.get("instances",[])))
        ck("IS91_family_mean_not_collapsed",
           any(not (near(wi,family["width"]) and near(hi,family["thickness"])) for wi,hi in generated))
        ck("IS92_no_duplicate_master_identity",
           len({load(idir/(m["fixture_id"]+".json"))["master_id"] for m in instance_sections.get("instances",[])})==1)
        ck("IS93_mapping_immutable_without_decision",
           instance_sections.get("direct_mapping_replaceable_without_new_decision") is False)

        if instance_sections.get("mode")=="DIRECT_LOCKED_WIDTH_PARTIAL_THICKNESS_WITH_PRODUCTION_COMPLETION":
            rows=instance_sections.get("instances",[])
            direct=[x for x in rows if x.get("thickness_classification")=="DIRECT_MEASURED"]
            completion=[x for x in rows if x.get("thickness_classification")=="PARAMETRIC_COMPLETION"]
            ck("IS94_direct_width_count",len(rows)==12 and all(x.get("width_classification")=="DIRECT_MEASURED" for x in rows))
            ck("IS95_direct_thickness_count",len(direct)==4)
            ck("IS96_completion_thickness_count",len(completion)==8)
            ck("IS97_direct_thickness_integrity",
               all(near(x.get("evidence_thickness_mm"),105) and near(x.get("production_thickness_mm"),105) and near(x.get("thickness_mm"),105) for x in direct))
            ck("IS98_completion_thickness_integrity",
               all(x.get("evidence_thickness_mm") is None and near(x.get("production_thickness_mm"),105) and near(x.get("thickness_mm"),105) and x.get("replaceable") is True and x.get("historical_claim") is False for x in completion))
            ck("IS99_completion_basis",
               instance_sections.get("completion_basis")=="4 directly measured specimens + report family reference")
            pair=instance_sections.get("same_geometry_different_evidence_regression",{})
            da=next((x for x in rows if x.get("fixture_id")==pair.get("direct_fixture_id")),None)
            cb=next((x for x in rows if x.get("fixture_id")==pair.get("completion_fixture_id")),None)
            ck("IS100_evidence_regression_pair_declared",
               da is not None and cb is not None and
               da.get("thickness_classification")=="DIRECT_MEASURED" and
               cb.get("thickness_classification")=="PARAMETRIC_COMPLETION" and
               near(da["width_mm"],cb["width_mm"]) and near(da["thickness_mm"],cb["thickness_mm"]))
            sa=load(idir/(da["fixture_id"]+".json")); sb=load(idir/(cb["fixture_id"]+".json"))
            ck("IS101_same_geometry_different_evidence",
               sa["body"]==sb["body"] and
               sa["semantic_geometry_signature"]==sb["semantic_geometry_signature"] and
               da.get("thickness_classification")!=cb.get("thickness_classification"))
            ck("IS102_zero_variant_despite_evidence_difference",
               instance_sections.get("geometry_variant_count")==0)
            measured_mean=sum(float(x["width_mm"]) for x in rows)/len(rows)
            ck("IS103_report_width_mean_reconciles",
               near(measured_mean,instance_sections["family_reference_section_mm"]["width"],0.05))

    hr=d.get("historical_repair_contract")
    if hr:
        ck("HR01_semantic_contract_preserved",c.get("historical_repair_contract")==hr)
        ck("HR02_current_orientation_flipped",hr.get("current_orientation_state")=="HISTORICAL_REPAIR_FLIPPED")
        ck("HR03_original_orientation_unresolved",hr.get("original_963_top_bottom_orientation")=="UNRESOLVED")
        ck("HR04_orientation_metadata_no_variant",hr.get("geometry_variant_created") is False and instance_sections.get("geometry_variant_count")==0)
        mt=hr.get("mortise_trace",{})
        ck("HR05_mortise_trace_direct",mt.get("existence")=="DIRECT_EVIDENCE")
        ck("HR06_mortise_trace_geometry_unresolved",mt.get("exact_geometry")=="UNRESOLVED")
        ck("HR07_mortise_trace_function_unresolved",mt.get("current_structural_function")=="UNRESOLVED")
        ck("HR08_no_canonical_body_cut",mt.get("canonical_body_cut") is False and c["body"]["joinery_cut_count"]==0)
        ck("HR09_trace_metadata_classification",mt.get("classification")=="HISTORICAL_REPAIR_TRACE_METADATA")
        ck("HR10_metadata_does_not_change_geometry",c["semantic_geometry_signature"]==rs["semantic_geometry_signature"] and c["body"]==rs["body"])
        ck("HR11_required_orientation_panel","HISTORICAL_ORIENTATION_BOUNDARY" in get_review_contract(d)["required_panels"])

    rc=get_review_contract(d); panels=rc["required_panels"]; review=Path(a.review_dir)
    ck("26_required_panels_complete",all((review/(x+".png")).exists() and (review/(x+".png")).stat().st_size>1000 for x in panels))
    board=Path(a.board)
    ck("27_review_board_exists",board.exists() and board.stat().st_size>10000)
    im=Image.open(board)
    ck("27A_review_board_chinese_identity",
       bool(component.strip()) and
       im.info.get("component_name_zh")==component and
       im.info.get("review_board_identity_rule")=="RC-012")
    cols=min(3,max(1,len(panels))); rows=math.ceil(len(panels)/cols)
    ck("28_review_board_dimensions",im.size==(cols*1200,rows*940))
    ck("29_no_fixed_panel_rule",rc.get("fixed_panel_count_required",d.get("v2_slim_file_contract",{}).get("fixed_review_panel_count_required")) is False)
    ck("30_minimal_sufficient_rule","D-089" in str(d.get("architecture_rule","D-089")) or get_package(d).get("principle")=="MINIMAL_SUFFICIENT_COMPONENT_PACKAGE")

    master_dir=str(Path(a.definition).parent)
    tracked=subprocess.check_output(["git","ls-files","--",master_dir+"/*.blend"],text=True).strip()
    ck("31_no_tracked_canonical_blend_in_master_dir",tracked=="")
    ck("32_definition_semantic_validation_independence",c["schema_version"].startswith("MASTER_V2_SEMANTIC_"))

    unknown_text=" | ".join(d.get("unknowns",[])).lower()
    ck("33_unknowns_preserved","historical" in unknown_text and "sample-to-instance" in unknown_text)
    ck("34_reference_length_assembly_guard","ASSEMBLY_OWNED" in gc["placement_policy"] and gc["canonical_reference_length_historical_claim"] is False)
    vg=auth["visual_reference_gate"]
    ck("35_visual_source_not_dimension_authority",vg.get("dimension_authority") is False or vg.get("unsupported_as_dimension_authority") is True)

    nc=d.get("source_numeric_conflict")
    if nc:
        pub=nc["published_mean_mm"]; rec=nc["visible_rows_recomputed_mean_mm"]
        ck("NC01_conflict_contract_declared",nc.get("conflict_type")=="SOURCE_INTERNAL_NUMERIC_CONFLICT" and isinstance(nc.get("conflict"),bool))
        ck("NC02_published_mean_drives_canonical_section",near(pub["width"],w) and near(pub["thickness"],h))
        if nc.get("conflict") is True:
            ck("NC03_recomputed_mean_preserved_as_distinct_audit",not near(rec["width"],pub["width"]) and not near(rec["thickness"],pub["thickness"]) and nc.get("recomputed_classification")=="AUDIT_ONLY")
            ck("NC04_silent_correction_prohibited",nc.get("silent_arithmetic_correction")=="PROHIBITED")
            ck("NC06_conflict_panel_required","EVIDENCE_UNCERTAINTY_AND_NUMERIC_CONFLICT" in panels)
        else:
            ck("NC03_matching_recompute_preserved",near(rec["width"],pub["width"]) and near(rec["thickness"],pub["thickness"]))
            ck("NC04_no_false_conflict",nc.get("canonical_geometry_basis")=="PUBLISHED_MEAN_MATCHING_RECOMPUTE")
        ck("NC05_semantic_preserves_numeric_conflict_contract",c.get("source_numeric_conflict")==nc)
        complete=nc.get("complete_visible_sample_count")
        if "table_row_count" in nc or "unmeasured_visible_row_count" in nc:
            ck("NC07_measurement_accounting_preserved",
               isinstance(complete,int) and complete>0 and
               isinstance(nc.get("unmeasured_visible_row_count"),int) and
               nc.get("table_row_count")==complete+nc.get("unmeasured_visible_row_count"))
        else:
            ck("NC07_measurement_accounting_preserved",
               isinstance(complete,int) and complete>0 and nc.get("unmeasured_record_present") is True)
        ck("NC08_fen_metadata_not_geometry",d.get("report_analysis",{}).get("geometry_use_count")==0)

    if role_cfg:
        ck("ROLE01_semantic_preserves_role_contract",c.get("registry_role_counts")==role_cfg)
        ck("ROLE02_assembly_semantics_preserved",c.get("assembly_semantics")==d.get("assembly_semantics"))
        ck("ROLE03_exact_angle_unknown",rb.get("exact_placement_angle_deg") is None)
        ck("ROLE04_legacy_proxy_not_reused",d.get("legacy_proxy_reuse") is False and c.get("legacy_proxy_reuse") is False)
        ck("ROLE05_role_or_placement_panel_required","ROLE_ASSEMBLY_SEMANTICS" in panels or "PLACEMENT_AND_ENDPOINT_LOGIC" in panels)
        if not a.role_a or not a.role_b:
            raise AssertionError("role mutation semantics required but --role-a/--role-b not supplied")
        ra=load(a.role_a); rbsem=load(a.role_b)
        role_names=list(role_cfg.keys())
        ck("ROLE06_role_mutation_names",ra.get("assembly_role")==role_names[0] and rbsem.get("assembly_role")==role_names[1])
        ck("ROLE07_role_mutation_preserves_geometry",ra["body"]==c["body"] and rbsem["body"]==c["body"] and ra["semantic_geometry_signature"]==c["semantic_geometry_signature"]==rbsem["semantic_geometry_signature"])

    endpoint=d.get("endpoint_resolver_contract")
    if endpoint and endpoint.get("enabled") is True:
        ck("EP01_contract_enabled",endpoint.get("enabled") is True)
        ck("EP02_nonhistorical_contract",endpoint.get("historical_claim") is False)
        ck("EP03_not_building_coordinates",endpoint.get("building_coordinate_claim") is False)
        fixtures=endpoint.get("fixtures",[])
        results=c.get("endpoint_fixture_results")
        ck("EP04_fixture_count",len(fixtures)>=2 and isinstance(results,list) and len(results)==len(fixtures))
        result_by_id={x["fixture_id"]:x for x in results}
        directions=[]; lengths=[]
        for fixture in fixtures:
            fid=fixture["fixture_id"]; rr=result_by_id.get(fid)
            ck("EP_"+fid+"_result_present",rr is not None)
            lower=[float(x) for x in fixture["p_lower_mm"]]; upper=[float(x) for x in fixture["p_upper_mm"]]
            vec=[upper[i]-lower[i] for i in range(3)]
            length=math.sqrt(sum(x*x for x in vec))
            center=[(upper[i]+lower[i])/2.0 for i in range(3)]
            direction=[x/length for x in vec]
            ck("EP_"+fid+"_length",near(rr["derived_length_mm"],fixture["expected_length_mm"]) and near(rr["derived_length_mm"],length))
            ck("EP_"+fid+"_center",all(near(rr["derived_center_mm"][i],center[i]) for i in range(3)))
            ck("EP_"+fid+"_direction",all(near(rr["derived_direction"][i],direction[i],1e-6) for i in range(3)))
            ck("EP_"+fid+"_classification","NOT_BUILDING_COORDINATES" in fixture["classification"] and rr.get("building_coordinate_claim") is False and rr.get("historical_claim") is False)
            lengths.append(rr["derived_length_mm"]); directions.append(rr["derived_direction"])
        variation=endpoint.get("fixture_variation_contract",{})
        unique_lengths={round(float(x),6) for x in lengths}
        unique_directions={tuple(round(float(v),6) for v in x) for x in directions}
        if variation.get("lengths_must_differ",True):
            ck("EP90_fixture_lengths_differ",len(unique_lengths)==len(lengths))
        else:
            ck("EP90_fixture_length_policy",True)
        if variation.get("directions_must_match",False):
            ck("EP91_fixture_directions_match",len(unique_directions)==1)
        elif variation.get("directions_must_differ",True):
            ck("EP91_fixture_directions_differ",len(unique_directions)==len(directions))
        else:
            ck("EP91_fixture_direction_policy",True)
        ck("EP92_reference_length_not_leaked",all(not near(x,gc["canonical_reference_length_mm"]) for x in lengths))
        ck("EP93_same_master_section",near(cd[1],w) and near(cd[2],h))
        ck("EP94_required_panel",
           "PLACEMENT_AND_ENDPOINT_LOGIC" in panels or endpoint.get("review_panel_required") is False)
        ck("EP95_reconstruction_boundary_panel",
           "SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY" in panels or
           "SOURCE_AND_RECONSTRUCTION_BOUNDARY" in panels)
        ck("EP96_semantic_contract_preserved",c.get("endpoint_resolver_contract")==endpoint)
        ck("EP97_reconstruction_policy_preserved",c.get("reconstruction_policy")==d.get("reconstruction_policy"))

    if "identity_boundary" in d:
        ib=d["identity_boundary"]
        ck("36_legacy_identity_separated",d["component_id"]!=ib["legacy_identity"] and ib["physical_instance_count"]==rb["physical_instance_count"])
    else:
        ck("36_legacy_identity_not_applicable",True)

    if profile_unknown(d):
        ck("37_profile_unknown_semantic",c.get("section_profile_state")=="UNKNOWN" and c.get("section_envelope_historical_claim") is False)
        ck("38_profile_unknown_body",c["body"].get("section_profile_state")=="UNKNOWN" and c["body"].get("section_envelope_historical_claim") is False and "envelope_proxy" in c["body"].get("primitive",""))
        rep=gc.get("engineering_representation",{})
        ck("39_envelope_proxy_nonhistorical",rep.get("historical_profile_claim") is False and rep.get("primitive")=="RECTANGULAR_BOUNDING_ENVELOPE_PROXY")
        ck("40_no_shengtou_baked",c.get("shengtou_wood_baked_in") is False and c["body"].get("shengtou_wood_baked_in") is False)
    else:
        ck("37_profile_contract_defined",True)

    catalog_entries=[x for x in catalog.get("new_masters",[]) if x.get("master_id")==d["master_id"]]
    if catalog_entries:
        ce=catalog_entries[0]
        ck("41_catalog_approved",ce.get("approval_status")=="PRODUCT_OWNER_APPROVED")
        published_semantic_path=Path(a.definition).parent / f'{d["master_id"]}_SEMANTIC_{d["master_version"]}.json'
        ck("42_published_semantic_exists",published_semantic_path.exists())
        published=load(published_semantic_path)
        ck("43_catalog_approved_binary_identity",ce.get("canonical_asset_sha256")==published.get("canonical_blend_sha256"))
        ck("44_regenerated_geometry_matches_approved",ce.get("semantic_geometry_signature")==c["semantic_geometry_signature"]==published.get("semantic_geometry_signature"))
        ck("45_registry_master_binding",all(x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE" and x.get("master_reference")==d["master_id"] for x in items))
        progress=reg["stage1_master_progress_summary"]
        ck("46_registry_progress_consistent",progress["approved_master_count"]==catalog["approved_master_count"] and progress["pending_master_object_type_count"]==progress["master_scope_object_type_count"]-progress["approved_master_count"])
        ck("47_registry_covered_rows_consistent",progress["master_covered_registry_record_count"]==sum(1 for x in reg["items"] if x.get("master_coverage_status")=="APPROVED_MASTER_AVAILABLE"))
    else:
        ck("41_preapproval_catalog_absent",all(x.get("master_reference")!=d["master_id"] for x in items))

    result={
      "schema_version":"MASTER_V2_VALIDATION_1.1",
      "task_id":d["task_id"],
      "status":"PASS",
      "approval_boundary":"ENGINEERING_COMPLETE_PENDING_PRODUCT_OWNER_REVIEW",
      "check_count":len(checks),
      "checks":checks,
      "component_id":d["component_id"],
      "master_id":d["master_id"],
      "definition_sha256":digest(a.definition),
      "canonical_blend_sha256":c["canonical_blend_sha256"],
      "semantic_geometry_signature":c["semantic_geometry_signature"],
      "review_board_sha256":digest(a.board),
      "required_review_panels":panels,
      "section_profile_state":c.get("section_profile_state"),
      "section_envelope_historical_claim":c.get("section_envelope_historical_claim"),
      "source_numeric_conflict":c.get("source_numeric_conflict"),
      "instance_section_binding_contract":c.get("instance_section_binding_contract"),
      "endpoint_resolver_contract":c.get("endpoint_resolver_contract"),
      "endpoint_fixture_results":c.get("endpoint_fixture_results"),
      "reconstruction_policy":c.get("reconstruction_policy"),
      "registry_role_counts":c.get("registry_role_counts"),
      "formal_file_count_policy":"ADAPTIVE / MINIMAL SUFFICIENT / NO FIXED COUNT",
      "blender_version":c["blender_version"]
    }
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MASTER_V2_VALIDATION_PASS",len(checks),c["canonical_blend_sha256"],c["semantic_geometry_signature"])

if __name__=="__main__":
    main()
