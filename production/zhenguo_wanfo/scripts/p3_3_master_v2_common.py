"""P3.3 Master V2 shared builder / inspector / adaptive review-board composer.

Shared infrastructure. Component-specific facts must come from a locked Master Definition.
"""
import argparse, hashlib, json, math, re, shutil, sys
from pathlib import Path

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stable_signature(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load_definition(path):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    assert d["status"].startswith("LOCKED / PRODUCT_OWNER_APPROVED")
    assert d["approval"]["definition_locked"] is True
    assert d["execution_boundary"]["engineering_execution_authorized"] is True
    assert d["geometry_contract"]["canonical_reference_length_historical_claim"] is False
    assert d["registry_boundary"]["historical_full_length_mm"] is None
    assert d["geometry_contract"]["unsupported_geometry"]==[]
    return d

def get_review_contract(d):
    if "review_contract" in d:
        return d["review_contract"]
    return d["v2_slim_file_contract"]["review_contract"]

def get_section(d):
    rb=d["registry_boundary"]
    if "section_mm" in rb:
        return float(rb["section_mm"]["width"]),float(rb["section_mm"]["thickness"])
    if "section_statistics_mm" in rb:
        s=rb["section_statistics_mm"]
        return float(s["mean_width"]),float(s["mean_thickness"])
    s=d["geometry_contract"]["section_envelope_mm"]
    return float(s["width"]),float(s["thickness"])

def is_profile_unknown(d):
    gc=d["geometry_contract"]
    return gc.get("exact_section_profile")=="UNKNOWN" or gc.get("section_envelope_is_historical_profile") is False

def resolve_endpoint_fixture(fixture):
    lower=[float(x) for x in fixture["p_lower_mm"]]
    upper=[float(x) for x in fixture["p_upper_mm"]]
    vec=[upper[i]-lower[i] for i in range(3)]
    length=math.sqrt(sum(x*x for x in vec))
    if length<=0:
        raise ValueError("endpoint fixture must have non-zero length")
    center=[(upper[i]+lower[i])/2.0 for i in range(3)]
    direction=[x/length for x in vec]
    return {
      "fixture_id":fixture["fixture_id"],
      "classification":fixture["classification"],
      "building_coordinate_claim":bool(fixture.get("building_coordinate_claim",False)),
      "historical_claim":bool(fixture.get("historical_claim",False)),
      "p_lower_mm":lower,
      "p_upper_mm":upper,
      "derived_length_mm":round(length,6),
      "derived_center_mm":[round(x,6) for x in center],
      "derived_direction":[round(x,9) for x in direction]
    }

def resolve_endpoint_fixtures(d):
    contract=d.get("endpoint_resolver_contract")
    if not contract or contract.get("enabled") is not True:
        return None
    return [resolve_endpoint_fixture(x) for x in contract.get("fixtures",[])]

def safe_name(s):
    return re.sub(r"[^A-Za-z0-9_]+","_",s.replace("-","_"))

def clear_scene():
    import bpy
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj,do_unlink=True)
    for c in list(bpy.data.collections):
        if c != bpy.context.scene.collection:
            bpy.data.collections.remove(c)

def setup_scene():
    import bpy
    s=bpy.context.scene
    s.unit_settings.system="METRIC"
    s.unit_settings.scale_length=0.001
    s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_EEVEE_NEXT"
    s.render.image_settings.file_format="PNG"
    s.render.resolution_percentage=100
    s.world.use_nodes=True
    bg=next(n for n in s.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.88,0.88,0.88,1)
    bg.inputs["Strength"].default_value=1
    return s

def emissive(name,shade):
    import bpy
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    n=m.node_tree.nodes
    n.clear()
    e=n.new("ShaderNodeEmission")
    e.inputs["Color"].default_value=(shade,shade,shade,1)
    o=n.new("ShaderNodeOutputMaterial")
    m.node_tree.links.new(e.outputs[0],o.inputs["Surface"])
    return m

def camera(target,pos,scale,name="V2_CAMERA"):
    import bpy
    from mathutils import Vector
    data=bpy.data.cameras.new(name)
    c=bpy.data.objects.new(name,data)
    bpy.context.scene.collection.objects.link(c)
    bpy.context.scene.camera=c
    data.type="ORTHO"
    data.clip_end=100000
    data.ortho_scale=scale
    c.location=pos
    c.rotation_euler=(Vector(target)-c.location).to_track_quat("-Z","Y").to_euler()
    return c

def make_body(d,length_mm,width_mm,thickness_mm):
    import bpy
    L=float(length_mm); W=float(width_mm); H=float(thickness_mm)
    verts=[(-L/2,-W/2,0),(L/2,-W/2,0),(L/2,W/2,0),(-L/2,W/2,0),
           (-L/2,-W/2,H),(L/2,-W/2,H),(L/2,W/2,H),(-L/2,W/2,H)]
    faces=[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
    base=safe_name(d["component_id"])
    mesh=bpy.data.meshes.new(base+"_BODY_MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    col=bpy.data.collections.new("MASTER__"+base)
    bpy.context.scene.collection.children.link(col)
    obj=bpy.data.objects.new("MASTER__"+base+"__BODY",mesh)
    col.objects.link(obj)
    obj["component_id"]=d["component_id"]
    obj["master_id"]=d["master_id"]
    obj["master_version"]=d["master_version"]
    obj["historical_full_length_state"]="UNKNOWN_NULL_DO_NOT_LOCK"
    obj["canonical_reference_length_historical_claim"]=False
    obj["joinery_geometry"]="DEFERRED"
    obj["unsupported_geometry_count"]=0
    obj["section_profile_state"]="UNKNOWN" if is_profile_unknown(d) else "DEFINED_BY_DEFINITION"
    obj["section_envelope_historical_claim"]=False if is_profile_unknown(d) else True
    obj["shengtou_wood_baked_in"]=False
    return obj

def body_payload(obj):
    verts=[[round(float(v.co[i]),6) for i in range(3)] for v in obj.data.vertices]
    faces=[list(p.vertices) for p in obj.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
    primitive="rectangular_bounding_envelope_proxy_profile_unknown" if obj.get("section_profile_state")=="UNKNOWN" else "closed_rectangular_bounded_outer_envelope_reference"
    return {
      "name":obj.name,
      "vertex_count":len(verts),
      "face_count":len(faces),
      "local_transform":{
        "location":[float(x) for x in obj.location],
        "rotation":[float(x) for x in obj.rotation_euler],
        "scale":[float(x) for x in obj.scale]
      },
      "local_bbox_mm":{
        "min":mins,"max":maxs,
        "dimensions":[round(maxs[i]-mins[i],6) for i in range(3)]
      },
      "primitive":primitive,
      "section_profile_state":obj.get("section_profile_state"),
      "section_envelope_historical_claim":bool(obj.get("section_envelope_historical_claim")),
      "shengtou_wood_baked_in":bool(obj.get("shengtou_wood_baked_in")),
      "unsupported_detail_count":0,
      "joinery_cut_count":0,
      "geometry_vertices_mm":verts,
      "geometry_faces":faces
    }

def render_views(obj,d,review_dir):
    import bpy
    from mathutils import Vector
    review=Path(review_dir)
    review.mkdir(parents=True,exist_ok=True)
    s=setup_scene()
    obj.data.materials.append(emissive("V2_BODY",0.58))
    dims=obj.dimensions
    L=float(dims.x); W=float(dims.y); H=float(dims.z); ext=max(L,W,H)
    target=(0,0,H/2)
    cam=camera(target,(0,-ext*3,H/2),ext*1.5)
    views={
      "FRONT":((0,-ext*3,H/2),max(L,H)*1.4),
      "SIDE":((ext*3,0,H/2),max(W,H)*1.5),
      "TOP":((0,0,ext*3),max(L,W)*1.4),
      "AXON":((ext*2,-ext*2.4,ext*1.9),ext*1.8)
    }
    for name,(pos,scale) in views.items():
        cam.location=pos
        cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
        cam.data.ortho_scale=scale
        s.render.resolution_x=1200
        s.render.resolution_y=900
        s.render.filepath=str(review/(name+".png"))
        bpy.ops.render.render(write_still=True)
    # Semantic aliases: no duplicate Blender render cost.
    shutil.copyfile(review/"FRONT.png",review/"LONG_SIDE.png")
    shutil.copyfile(review/"SIDE.png",review/"END_SECTION_ENVELOPE.png")
    shutil.copyfile(review/"SIDE.png",review/"END_SECTION.png")

def text_page(path,title,lines):
    import bpy
    clear_scene()
    s=setup_scene()
    s.render.resolution_x=1200
    s.render.resolution_y=900
    dark=emissive("V2_TEXT",0.08)
    content=[title]+lines
    for i,line in enumerate(content):
        curve=bpy.data.curves.new("TXT_"+str(i),type="FONT")
        curve.body=str(line)
        curve.align_x="LEFT"
        curve.align_y="CENTER"
        curve.size=0.40 if i==0 else 0.25
        o=bpy.data.objects.new("TXT_"+str(i),curve)
        bpy.context.scene.collection.objects.link(o)
        o.data.materials.append(dark)
        o.location=(-7.5,5.5-i*0.90,0)
    camera((0,0,0),(0,0,20),17.5,name="V2_TEXT_CAMERA")
    s.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)

def render_summaries(d,review_dir,length_mm,width_mm,thickness_mm):
    review=Path(review_dir)
    rb=d["registry_boundary"]
    vg=d["authority"]["visual_reference_gate"]
    profile_unknown=is_profile_unknown(d)
    role_cfg=d.get("registry_role_counts")
    if role_cfg:
        location_line="Role distribution: " + " / ".join(
            f'{name} {cfg.get("count")}' for name,cfg in role_cfg.items()
        )
    elif "exact_location_unresolved_count" in rb:
        location_line=f'Exact-location unresolved: {rb["exact_location_unresolved_count"]}'
    else:
        location_line=f'Instance distribution: {rb.get("main_body_count",0)} main / {rb.get("east_gable_count",0)} E gable / {rb.get("west_gable_count",0)} W gable'
    section_label="BOUNDING ENVELOPE / PROFILE UNKNOWN" if profile_unknown else "CANONICAL SECTION"
    text_page(review/"DIMENSION_PARAMETER_SUMMARY.png","MASTER V2 / DIMENSION + PARAMETER",[
      f'Component: {d["component_id"]}',
      f'Section envelope: {width_mm:.1f} x {thickness_mm:.1f} mm',
      f'Section meaning: {section_label}',
      f'Reference length: {length_mm:.1f} mm / NON-HISTORICAL',
      f'Physical instances: {rb["physical_instance_count"]}',
      location_line,
      'Placement length/orientation: ASSEMBLY-OWNED'
    ])
    dimension_authority=(vg.get("dimension_authority") is True)
    text_page(review/"EVIDENCE_UNCERTAINTY_SUMMARY.png","MASTER V2 / EVIDENCE + UNCERTAINTY",[
      f'Registry authority: {d["authority"]["registry_schema_version_expected"]}',
      f'Visual gate: {vg["decision_id"]} / {vg["result"]}',
      f'Visual source dimension authority: {dimension_authority}',
      'Historical full length: UNKNOWN / null',
      f'Section profile: {"UNKNOWN / ENVELOPE NOT HISTORICAL" if profile_unknown else "DEFINED"}',
      f'Sample-to-instance mapping: {d.get("registry_boundary",{}).get("sample_to_instance_mapping","UNKNOWN")}',
      'Hidden joinery/end geometry: UNKNOWN / DEFERRED'
    ])
    required=set(get_review_contract(d)["required_panels"])
    if "INSTANCE_TOPOLOGY_33" in required:
        text_page(review/"INSTANCE_TOPOLOGY_33.png","PURLIN / 33-INSTANCE TOPOLOGY",[
          f'Total physical instances: {rb["physical_instance_count"]}',
          f'Main body: {rb["main_body_count"]} = 7 lines x 3 segments',
          f'East gable: {rb["east_gable_count"]} = 2 lines x 3 segments',
          f'West gable: {rb["west_gable_count"]} = 2 lines x 3 segments',
          'One shared Master; role/length/orientation are assembly-owned',
          'Legacy 7 engineering PURLIN objects are NOT the real count'
        ])
    if "ROLE_LAYER_DIAGRAM" in required:
        roles=d.get("assembly_roles",{})
        text_page(review/"ROLE_LAYER_DIAGRAM.png","PURLIN / ROLE + LAYER CONTRACT",[
          'Main: EAVE / LOWER / UPPER / RIDGE / UPPER / LOWER / EAVE',
          'Gables: 2 purlin lines per east/west gable',
          'Role difference alone does NOT create geometry variants',
          'Shengtou wood: separate roof-curvature/assembly control',
          'Corner-beam connection: existence known / geometry deferred',
          'All real segment lengths and orientations: assembly-owned'
        ])
    if "ROLE_ASSEMBLY_SEMANTICS" in required:
        role_cfg=d.get("registry_role_counts",{})
        sem=d.get("assembly_semantics",{})
        lines=[f'{name}: {cfg.get("count")} instances / shared canonical body'
               for name,cfg in role_cfg.items()]
        lines += [
          f'Member type: {sem.get("member_type","UNKNOWN")}',
          f'Official same-building semantic: {sem.get("official_same_building_semantic","UNKNOWN")}',
          f'Endpoint/contact geometry: {sem.get("exact_endpoint_contact_geometry","UNKNOWN")}',
          'Role difference alone does NOT create a geometry Variant'
        ]
        text_page(review/"ROLE_ASSEMBLY_SEMANTICS.png","MASTER V2 / ROLE + ASSEMBLY SEMANTICS",lines)
    if "EVIDENCE_UNCERTAINTY_AND_NUMERIC_CONFLICT" in required:
        nc=d.get("source_numeric_conflict")
        if not nc:
            raise ValueError("numeric-conflict review panel required but source_numeric_conflict is absent")
        pub=nc["published_mean_mm"]; rec=nc["visible_rows_recomputed_mean_mm"]
        text_page(review/"EVIDENCE_UNCERTAINTY_AND_NUMERIC_CONFLICT.png","MASTER V2 / EVIDENCE + NUMERIC CONFLICT",[
          f'REPORT PUBLISHED MEAN: {pub["width"]:.1f} x {pub["thickness"]:.1f} mm',
          f'VISIBLE-ROW RECOMPUTED MEAN: {rec["width"]:.1f} x {rec["thickness"]:.1f} mm / AUDIT ONLY',
          f'SOURCE_INTERNAL_NUMERIC_CONFLICT: {str(nc.get("conflict")).upper()}',
          f'SILENT ARITHMETIC CORRECTION: {nc.get("silent_arithmetic_correction")}',
          'Historical full length: UNKNOWN / null',
          'Exact placement angle: UNKNOWN / null',
          'Endpoints/contact faces: UNKNOWN',
          'Joinery/end geometry: DEFERRED'
        ])

    instance_sections=d.get("instance_section_binding_contract")
    if "END_SECTION" in required and instance_sections:
        fam=instance_sections["family_reference_section_mm"]
        lines=[
          f'FAMILY REFERENCE ONLY: {fam["width"]:.1f} x {fam["thickness"]:.1f} mm',
          'ONE SHARED MASTER / ZERO GEOMETRY VARIANT',
          'INSTANCE SECTIONS:'
        ]
        for x in instance_sections.get("instances",[]):
            ev=x.get("evidence_thickness_mm",x.get("thickness_mm"))
            prod=x.get("production_thickness_mm",x.get("thickness_mm"))
            cls=x.get("thickness_classification","DIRECT_MEASURED")
            ev_text="UNKNOWN/null" if ev is None else f'{float(ev):.1f} mm'
            lines.append(f'{x["fixture_id"]} / {x["location"]}: width {x["width_mm"]:.1f} / production thickness {float(prod):.1f} mm / {cls} / evidence thickness {ev_text}')
        lines += [
          'Family mean MUST NOT overwrite direct instance width measurements',
          'Rectangular outline is Stage1 bounded-envelope representation'
        ]
        text_page(review/"END_SECTION.png","MASTER V2 / END SECTION + INSTANCE SECTIONS",lines)

    if "4_INSTANCE_SECTION_MAPPING" in required:
        if not instance_sections:
            raise ValueError("4-instance section panel requires instance_section_binding_contract")
        fam=instance_sections["family_reference_section_mm"]
        lines=[
          f'PROJECT REFERENCE: {fam["width"]:.2f} x {fam["thickness"]:.1f} mm / REFERENCE ONLY',
          '4/4 WIDTH + THICKNESS DIRECT_MEASURED:',
        ]
        for x in instance_sections.get("instances",[]):
            lines.append(f'{x["fixture_id"]} / {x["location"]}: {x["width_mm"]:.1f} x {x["thickness_mm"]:.1f} mm / DIRECT_MEASURED')
        lines += [
          '252.25 mm = PROJECT_DERIVED_REFERENCE / NOT SOURCE-PUBLISHED FAMILY MEAN',
          'Direct instance sections MUST NOT collapse to project reference'
        ]
        text_page(review/"4_INSTANCE_SECTION_MAPPING.png","由额 / 4 INSTANCE SECTION MAPPING",lines)

    if "HISTORICAL_ORIENTATION_BOUNDARY" in required:
        hr=d.get("historical_repair_contract")
        if not hr:
            raise ValueError("historical-orientation panel requires historical_repair_contract")
        text_page(review/"HISTORICAL_ORIENTATION_BOUNDARY.png","由额 / HISTORICAL ORIENTATION BOUNDARY",[
          f'CURRENT STATE: {hr["current_orientation_state"]}',
          f'ORIGINAL 963 TOP/BOTTOM: {hr["original_963_top_bottom_orientation"]}',
          f'MORTISE TRACE EXISTENCE: {hr["mortise_trace"]["existence"]}',
          f'EXACT TRACE GEOMETRY: {hr["mortise_trace"]["exact_geometry"]}',
          f'CURRENT STRUCTURAL FUNCTION: {hr["mortise_trace"]["current_structural_function"]}',
          'CANONICAL BODY CUT: FALSE / old traces are metadata only',
          'Historical orientation metadata MUST NOT create a Geometry Variant'
        ])

    if "12_INSTANCE_WIDTH_MAPPING" in required:
        if not instance_sections:
            raise ValueError("12-instance width panel requires instance_section_binding_contract")
        fam=instance_sections["family_reference_section_mm"]
        lines=[
          f'FAMILY WIDTH REFERENCE: {fam["width"]:.1f} mm / REFERENCE ONLY',
          f'INSTANCE COUNT: {len(instance_sections.get("instances",[]))}',
          'DIRECT LOCATION-LABELLED WIDTHS:'
        ]
        for x in instance_sections.get("instances",[]):
            lines.append(f'{x["fixture_id"]} / {x["location"]}: {x["width_mm"]:.1f} mm')
        lines.append('Family mean MUST NOT overwrite instance widths')
        text_page(review/"12_INSTANCE_WIDTH_MAPPING.png","阑额 / 12 INSTANCE WIDTH MAPPING",lines)

    if "THICKNESS_EVIDENCE_BOUNDARY" in required:
        if not instance_sections:
            raise ValueError("thickness evidence panel requires instance_section_binding_contract")
        rows=instance_sections.get("instances",[])
        direct=[x for x in rows if x.get("thickness_classification","DIRECT_MEASURED")=="DIRECT_MEASURED"]
        completion=[x for x in rows if x.get("thickness_classification")=="PARAMETRIC_COMPLETION"]
        pair=instance_sections.get("same_geometry_different_evidence_regression",{})
        lines=[
          f'DIRECT THICKNESS: {len(direct)}/{len(rows)} / evidence=105 / production=105 mm',
          f'UNMEASURED THICKNESS: {len(completion)}/{len(rows)} / evidence=UNKNOWN/null',
          'PRODUCTION COMPLETION: 105 mm / PARAMETRIC_COMPLETION',
          'Completion is REPLACEABLE / historical_claim=false',
          'Geometry may match while evidence classification remains different',
          f'Regression pair: {pair.get("direct_fixture_id","N/A")} DIRECT vs {pair.get("completion_fixture_id","N/A")} COMPLETION'
        ]
        text_page(review/"THICKNESS_EVIDENCE_BOUNDARY.png","阑额 / THICKNESS EVIDENCE BOUNDARY",lines)

    if "SOURCE_AND_RECONSTRUCTION_BOUNDARY" in required:
        if d.get("component_name_zh")=="由额":
            text_page(review/"SOURCE_AND_RECONSTRUCTION_BOUNDARY.png","由额 / SOURCE + RECONSTRUCTION BOUNDARY",[
              'EVIDENCE LOCKED: identity / 4 locations / 4 direct sections',
              'EVIDENCE LOCKED: current historical-repair flip / old mortise trace existence',
              'PROJECT RULE: 1000 mm Master reference / 252.25 project-derived width reference',
              'ASSEMBLY RULE: production length endpoint-derived / historical full length UNKNOWN',
              'NOT CLAIMED: exact 963 section / original top-bottom orientation',
              'NOT CLAIMED: exact mortise-tenon / trace geometry / penetration depth'
            ])
        else:
            text_page(review/"SOURCE_AND_RECONSTRUCTION_BOUNDARY.png","阑额 / SOURCE + RECONSTRUCTION BOUNDARY",[
              'EVIDENCE LOCKED: identity / count / 12 direct widths / 4 direct thicknesses',
              'PRODUCTION COMPLETION: 8 thickness values = 105 mm / replaceable / non-historical',
              'A2 LOCKED: no pu-paifang / corner projection none',
              'PROJECT RULE: 1000 mm Master reference / column-center assembly span',
              'NOT CLAIMED: exact 963 section / concealed timber full length',
              'NOT CLAIMED: exact mortise-tenon / end cuts / penetration depth'
            ])

    endpoint_results=resolve_endpoint_fixtures(d)
    if "DIMENSION_AND_PARAMETRIC_LENGTH" in required:
        text_page(review/"DIMENSION_AND_PARAMETRIC_LENGTH.png","MASTER V2 / DIMENSION + PARAMETRIC LENGTH",[
          f'Component: {d["component_id"]}',
          f'Canonical section: {width_mm:.1f} x {thickness_mm:.1f} mm',
          f'Master specimen length: {length_mm:.1f} mm / RECONSTRUCTION REFERENCE ONLY',
          'Building instance length: ENDPOINT-DERIVED',
          'Building instance orientation: ENDPOINT-DERIVED',
          'REFERENCE LENGTH LEAKAGE: PROHIBITED'
        ])
    if "PLACEMENT_AND_ENDPOINT_LOGIC" in required:
        if not endpoint_results or len(endpoint_results)<2:
            raise ValueError("endpoint placement panel requires at least two endpoint fixtures")
        lines=['Same canonical Master / same section / endpoint-driven instances']
        role_cfg=d.get("registry_role_counts",{})
        if role_cfg:
            lines.append('Role distribution: ' + ' / '.join(f'{name} {cfg.get("count")}' for name,cfg in role_cfg.items()))
            lines.append('Role difference does NOT create a geometry Variant')
        for x in endpoint_results:
            lines += [
              f'{x["fixture_id"]}: {x["classification"]}',
              f'lower={x["p_lower_mm"]} upper={x["p_upper_mm"]}',
              f'length={x["derived_length_mm"]:.1f} mm center={x["derived_center_mm"]}',
              f'direction={x["derived_direction"]}'
            ]
        text_page(review/"PLACEMENT_AND_ENDPOINT_LOGIC.png","MASTER V2 / PLACEMENT + ENDPOINT LOGIC",lines)
    if "SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY" in required:
        boundary_lines=[
          'EVIDENCE LOCKED: identity / count / measured section / structural layer',
          'RECONSTRUCTED DESIGN: endpoint placement / derived length / orientation / simplified flat ends',
          'NOT CLAIMED: exact 963 full length / angle / historical-original joinery',
          'UNKNOWN historical metadata does NOT automatically block required production geometry',
          'Reconstructed design remains explicit, replaceable, and source-consistent'
        ]
        if instance_sections:
            boundary_lines.insert(1,'EVIDENCE LOCKED: location-specific instance sections remain direct and must not collapse to family mean')
            boundary_lines.append('RELATED IDENTITIES remain separate; this Master does not absorb adjacent component families')
        text_page(review/"SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY.png","MASTER V2 / SOURCE + RECONSTRUCTION BOUNDARY",boundary_lines)

def build(definition,asset,semantic,review_dir=None,length_mm=None,width_mm=None,thickness_mm=None,role=None):
    import bpy
    d=load_definition(definition)
    role_contract=d.get("registry_role_counts",{})
    if role is not None:
        assert role in role_contract, f"Unknown assembly role: {role}"
    rb=d["registry_boundary"]
    base_w,base_h=get_section(d)
    L=float(length_mm if length_mm is not None else d["geometry_contract"]["canonical_reference_length_mm"])
    W=float(width_mm if width_mm is not None else base_w)
    H=float(thickness_mm if thickness_mm is not None else base_h)
    clear_scene(); setup_scene()
    obj=make_body(d,L,W,H)
    asset=Path(asset); asset.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset),check_existing=False)
    body=body_payload(obj)
    sig=stable_signature({"vertices":body["geometry_vertices_mm"],"faces":body["geometry_faces"]})
    profile_unknown=is_profile_unknown(d)
    sem={
      "schema_version":"MASTER_V2_SEMANTIC_1.1",
      "task_id":d["task_id"],
      "component_id":d["component_id"],
      "master_id":d["master_id"],
      "master_version":d["master_version"],
      "definition_sha256":sha256(definition),
      "blender_version":bpy.app.version_string,
      "geometry_mode":d["geometry_contract"]["geometry_mode"],
      "resolved_dimensions_mm":{"length":L,"width":W,"thickness":H},
      "historical_full_length_mm":None,
      "canonical_reference_length_historical_claim":False,
      "placement_policy":d["geometry_contract"]["placement_policy"],
      "joinery_geometry":d["geometry_contract"]["joinery_geometry"],
      "section_profile_state":"UNKNOWN" if profile_unknown else "DEFINED_BY_DEFINITION",
      "section_envelope_historical_claim":False if profile_unknown else True,
      "engineering_representation":d["geometry_contract"].get("engineering_representation"),
      "shengtou_wood_baked_in":False,
      "unknowns":d["unknowns"],
      "assembly_role":role,
      "registry_role_counts":d.get("registry_role_counts"),
      "assembly_semantics":d.get("assembly_semantics"),
      "source_numeric_conflict":d.get("source_numeric_conflict"),
      "historical_repair_contract":d.get("historical_repair_contract"),
      "instance_section_binding_contract":d.get("instance_section_binding_contract"),
      "reconstruction_policy":d.get("reconstruction_policy"),
      "endpoint_resolver_contract":d.get("endpoint_resolver_contract"),
      "endpoint_fixture_results":resolve_endpoint_fixtures(d),
      "legacy_proxy_reuse":d.get("legacy_proxy_reuse"),
      "body":body,
      "semantic_geometry_signature":sig,
      "canonical_blend_sha256":sha256(asset)
    }
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if review_dir:
        render_views(obj,d,review_dir)
        render_summaries(d,review_dir,L,W,H)
    print("MASTER_V2_BUILD_OK",d["component_id"],sig)

def inspect(asset,expected,output):
    import bpy
    e=json.loads(Path(expected).read_text(encoding="utf-8"))
    obj=bpy.data.objects.get(e["body"]["name"])
    assert obj is not None
    body=body_payload(obj)
    assert body==e["body"]
    assert obj.get("component_id")==e["component_id"]
    assert obj.get("master_id")==e["master_id"]
    assert obj.get("historical_full_length_state")=="UNKNOWN_NULL_DO_NOT_LOCK"
    assert obj.get("canonical_reference_length_historical_claim") is False
    assert bool(obj.get("shengtou_wood_baked_in")) is False
    out={
      "status":"PASS",
      "body":body,
      "semantic_geometry_signature":stable_signature({"vertices":body["geometry_vertices_mm"],"faces":body["geometry_faces"]}),
      "blend_sha256":sha256(asset)
    }
    Path(output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("MASTER_V2_REOPEN_OK")

def compose_board(definition,review_dir,board):
    from PIL import Image,ImageDraw,ImageFont,PngImagePlugin
    d=load_definition(definition)
    panels=get_review_contract(d)["required_panels"]
    component_name_zh=str(d.get("component_name_zh","")).strip()
    if not component_name_zh:
        raise ValueError("RC-012 requires component_name_zh on every formal Review Board")
    font_path=Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    if not font_path.exists():
        raise FileNotFoundError(f"RC-012 CJK font missing: {font_path}")
    review=Path(review_dir)
    cols=min(3,max(1,len(panels)))
    rows=math.ceil(len(panels)/cols)
    iw,ih=1200,900
    label_h=40
    canvas=Image.new("RGB",(cols*iw,rows*(ih+label_h)),"white")
    draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype(str(font_path),22)
    for idx,panel in enumerate(panels):
        src=review/(panel+".png")
        if not src.exists():
            raise FileNotFoundError(src)
        im=Image.open(src).convert("RGB")
        if im.size!=(iw,ih):
            im=im.resize((iw,ih))
        x=(idx%cols)*iw; y=(idx//cols)*(ih+label_h)
        draw.text((x+12,y+6),f"{component_name_zh}｜{panel}",fill="black",font=font)
        canvas.paste(im,(x,y+label_h))
    out=Path(board); out.parent.mkdir(parents=True,exist_ok=True)
    meta=PngImagePlugin.PngInfo()
    meta.add_text("component_name_zh",component_name_zh)
    meta.add_text("review_board_identity_rule","RC-012")
    meta.add_text("review_board_label_format","{component_name_zh}｜{panel}")
    canvas.save(out,pnginfo=meta)
    print("MASTER_V2_REVIEW_BOARD_OK",len(panels),component_name_zh,out)

def parse_args():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("build","inspect","compose-board"),required=True)
    ap.add_argument("--definition")
    ap.add_argument("--asset")
    ap.add_argument("--semantic")
    ap.add_argument("--review-dir")
    ap.add_argument("--expected")
    ap.add_argument("--output")
    ap.add_argument("--board")
    ap.add_argument("--length-mm",type=float)
    ap.add_argument("--width-mm",type=float)
    ap.add_argument("--thickness-mm",type=float)
    ap.add_argument("--role")
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    return ap.parse_args(argv)

def main():
    a=parse_args()
    if a.mode=="build":
        build(a.definition,a.asset,a.semantic,a.review_dir,a.length_mm,a.width_mm,a.thickness_mm,a.role)
    elif a.mode=="inspect":
        inspect(a.asset,a.expected,a.output)
    else:
        compose_board(a.definition,a.review_dir,a.board)

if __name__=="__main__":
    main()
