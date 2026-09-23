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

    role_cfg=d.get("registry_role_counts")
    if role_cfg:
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

    rc=get_review_contract(d); panels=rc["required_panels"]; review=Path(a.review_dir)
    ck("26_required_panels_complete",all((review/(x+".png")).exists() and (review/(x+".png")).stat().st_size>1000 for x in panels))
    board=Path(a.board)
    ck("27_review_board_exists",board.exists() and board.stat().st_size>10000)
    im=Image.open(board)
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
        ck("EP90_fixture_lengths_differ",len({round(float(x),6) for x in lengths})==len(lengths))
        ck("EP91_fixture_directions_differ",len({tuple(round(float(v),6) for v in x) for x in directions})==len(directions))
        ck("EP92_reference_length_not_leaked",all(not near(x,gc["canonical_reference_length_mm"]) for x in lengths))
        ck("EP93_same_master_section",near(cd[1],w) and near(cd[2],h))
        ck("EP94_required_panel","PLACEMENT_AND_ENDPOINT_LOGIC" in panels)
        ck("EP95_reconstruction_boundary_panel","SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY" in panels)
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
