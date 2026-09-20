"""T-023 Dingfu Master builder / inspector / review renderer."""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy
from mathutils import Vector

def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stable_signature(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def pmap(d): return {x["key"]:x for x in d["parameters"]}

def clear_scene():
    for obj in list(bpy.data.objects): bpy.data.objects.remove(obj,do_unlink=True)
    for c in list(bpy.data.collections):
        if c != bpy.context.scene.collection: bpy.data.collections.remove(c)

def setup_scene():
    s=bpy.context.scene
    s.unit_settings.system="METRIC"; s.unit_settings.scale_length=0.001; s.unit_settings.length_unit="MILLIMETERS"
    s.render.engine="BLENDER_EEVEE_NEXT"; s.render.image_settings.file_format="PNG"; s.render.resolution_percentage=100
    s.world.use_nodes=True
    bg=next(n for n in s.world.node_tree.nodes if n.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.88,0.88,0.88,1); bg.inputs["Strength"].default_value=1
    return s

def validate_params(d):
    p=pmap(d)
    assert d["component_id"]=="CMP-FRAME-DINGFU-001"
    assert d["master_id"]=="CMP-FRAME-DINGFU-001_MASTER"
    assert d["master_version"]=="V001"
    assert d["geometry_mode"]=="BOUNDED_LONG_MEMBER_OUTER_ENVELOPE"
    assert d["role_variants"]==["UPPER","LOWER"]
    assert d["role_geometry_policy"]=="SHARED_CANONICAL_BODY"
    assert d["sample_to_instance_mapping"]=="UNKNOWN"
    assert len(d["measured_section_samples_mm"])==8
    assert p["historical_full_length_mm"]["value"] is None
    assert p["canonical_reference_length_mm"]["historical_claim"] is False
    assert d["groove_boundary"]["status"]=="DIRECT_EXISTENCE / GEOMETRY_DEFERRED"
    assert d["groove_boundary"]["stage1_cut_geometry"] is False
    assert d["unsupported_geometry"]==[]
    return p

def make_body(d,p,role):
    L=float(p["realization_length_mm"]["value"]); W=float(p["width_mm"]["value"]); H=float(p["thickness_mm"]["value"])
    verts=[(-L/2,-W/2,0),(L/2,-W/2,0),(L/2,W/2,0),(-L/2,W/2,0),
           (-L/2,-W/2,H),(L/2,-W/2,H),(L/2,W/2,H),(-L/2,W/2,H)]
    faces=[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
    mesh=bpy.data.meshes.new("CMP_FRAME_DINGFU_001_BODY_MESH"); mesh.from_pydata(verts,[],faces); mesh.update()
    col=bpy.data.collections.new("MASTER__CMP_FRAME_DINGFU_001"); bpy.context.scene.collection.children.link(col)
    obj=bpy.data.objects.new("MASTER__CMP_FRAME_DINGFU_001__BODY",mesh); col.objects.link(obj)
    obj["component_id"]=d["component_id"]; obj["master_id"]=d["master_id"]; obj["role"]=role
    obj["sample_to_instance_mapping"]="UNKNOWN"
    obj["groove_existence"]="DIRECT"; obj["groove_geometry"]="DEFERRED"
    obj["historical_full_length_state"]="UNKNOWN_NULL_DO_NOT_LOCK"
    obj["reference_length_hard_fail"]=d["assembly_length_rule"]["hard_fail_id"]
    return obj

def body_payload(obj):
    verts=[[round(float(v.co[i]),6) for i in range(3)] for v in obj.data.vertices]
    faces=[list(p.vertices) for p in obj.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]; maxs=[max(v[i] for v in verts) for i in range(3)]
    return {"name":obj.name,"vertex_count":len(verts),"face_count":len(faces),
            "local_transform":{"location":[float(x) for x in obj.location],"rotation":[float(x) for x in obj.rotation_euler],"scale":[float(x) for x in obj.scale]},
            "local_bbox_mm":{"min":mins,"max":maxs,"dimensions":[round(maxs[i]-mins[i],6) for i in range(3)]},
            "primitive":"closed_rectangular_bounded_outer_envelope_reference",
            "unsupported_detail_count":0,"groove_cut_count":0,
            "geometry_vertices_mm":verts,"geometry_faces":faces}

def emissive(name,shade):
    m=bpy.data.materials.new(name); m.use_nodes=True; n=m.node_tree.nodes; n.clear()
    e=n.new("ShaderNodeEmission"); e.inputs["Color"].default_value=(shade,shade,shade,1)
    o=n.new("ShaderNodeOutputMaterial"); m.node_tree.links.new(e.outputs[0],o.inputs["Surface"]); return m

def camera(target,pos,scale):
    data=bpy.data.cameras.new("T023_CAMERA"); c=bpy.data.objects.new("T023_CAMERA",data); bpy.context.scene.collection.objects.link(c)
    bpy.context.scene.camera=c; data.type="ORTHO"; data.clip_end=100000; data.ortho_scale=scale
    c.location=pos; c.rotation_euler=(Vector(target)-c.location).to_track_quat("-Z","Y").to_euler(); return c

def render_views(obj,p,review):
    review=Path(review); review.mkdir(parents=True,exist_ok=True); s=setup_scene()
    obj.data.materials.append(emissive("T023_BODY",0.58))
    L=float(p["realization_length_mm"]["value"]); W=float(p["width_mm"]["value"]); H=float(p["thickness_mm"]["value"]); ext=max(L,W,H)
    target=(0,0,H/2); cam=camera(target,(0,-ext*3,H/2),ext*1.5)
    views={"FRONT":((0,-ext*3,H/2),max(L,H)*1.4),"SIDE":((ext*3,0,H/2),max(W,H)*1.5),
           "TOP":((0,0,ext*3),max(L,W)*1.4),"AXON":((ext*2,-ext*2.4,ext*1.9),ext*1.8)}
    for name,(pos,scale) in views.items():
        cam.location=pos; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler(); cam.data.ortho_scale=scale
        s.render.resolution_x=1200; s.render.resolution_y=900; s.render.filepath=str(review/(name+".png")); bpy.ops.render.render(write_still=True)

def text_page(path,title,lines):
    clear_scene(); s=setup_scene(); s.render.resolution_x=1200; s.render.resolution_y=900; dark=emissive("T023_TEXT",0.08)
    for i,line in enumerate([title]+lines):
        curve=bpy.data.curves.new("TXT"+str(i),type="FONT"); curve.body=line; curve.align_x="LEFT"; curve.align_y="CENTER"; curve.size=0.42 if i==0 else 0.28
        o=bpy.data.objects.new("TXT"+str(i),curve); bpy.context.scene.collection.objects.link(o); o.data.materials.append(dark); o.location=(-7.4,5.5-i*0.95,0)
    camera((0,0,0),(0,0,20),17.5); s.render.filepath=str(path); bpy.ops.render.render(write_still=True)

def render_summaries(d,review):
    review=Path(review)
    text_page(review/"DIMENSION_PARAMETER_SUMMARY.png","T-023 DINGFU / DIMENSION PARAMETER SUMMARY",[
        "Canonical section: 331.6 x 200.9 mm / measured family mean",
        "Measured section samples: 8 / sample-to-instance mapping UNKNOWN",
        "Role variants: UPPER / LOWER / shared canonical body",
        "Canonical reference length: 1000 mm / NON-HISTORICAL",
        "Historical full length: UNKNOWN / null",
        "Groove: existence DIRECT / geometry DEFERRED"
    ])
    text_page(review/"EVIDENCE_UNCERTAINTY_SUMMARY.png","T-023 DINGFU / EVIDENCE + UNCERTAINTY",[
        "Source: SRC-ZG-WF-001 / PDF p81,p83 / printed p66,p68 / table 2-40",
        "Physical instances: 8",
        "UPPER/LOWER are assembly roles, not geometry variants",
        "Outboard/inboard interfaces are semantic only in Stage 1",
        "Groove exact dimensions/position/contour remain UNKNOWN",
        "D-077: Dingfu-only visual-review waiver; D-076 remains general rule",
        "No mortise, tenon, groove cut, end-profile or 963-design claim"
    ])

def build(params,role,asset,semantic,review=None):
    d=json.loads(Path(params).read_text(encoding="utf-8")); p=validate_params(d)
    assert role in ("UNASSIGNED","UPPER","LOWER")
    clear_scene(); setup_scene(); obj=make_body(d,p,role)
    asset=Path(asset); asset.parent.mkdir(parents=True,exist_ok=True); bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset),check_existing=False)
    body=body_payload(obj)
    sem={"task":"T-023","component_id":d["component_id"],"master_id":d["master_id"],"master_version":d["master_version"],
         "role":role,"blender_version":bpy.app.version_string,"geometry_mode":d["geometry_mode"],
         "resolved_parameters":{k:v["value"] for k,v in p.items()},
         "sample_to_instance_mapping":d["sample_to_instance_mapping"],"role_geometry_policy":d["role_geometry_policy"],
         "interface_contract":d["interface_contract"],"groove_boundary":d["groove_boundary"],
         "historical_state":d["historical_state"],"assembly_length_rule":d["assembly_length_rule"],
         "body":body,"semantic_geometry_signature":stable_signature({"vertices":body["geometry_vertices_mm"],"faces":body["geometry_faces"]}),
         "canonical_blend_sha256":sha256(asset)}
    Path(semantic).write_text(json.dumps(sem,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if review:
        render_views(obj,p,review); render_summaries(d,review)
    print("DINGFU_BUILD_OK",role,sem["semantic_geometry_signature"])

def inspect(expected,asset,output):
    e=json.loads(Path(expected).read_text(encoding="utf-8")); obj=bpy.data.objects.get("MASTER__CMP_FRAME_DINGFU_001__BODY")
    assert obj is not None; a=body_payload(obj); assert a==e["body"]
    assert obj.get("component_id")==e["component_id"] and obj.get("master_id")==e["master_id"]
    assert obj.get("sample_to_instance_mapping")=="UNKNOWN"
    assert obj.get("groove_existence")=="DIRECT" and obj.get("groove_geometry")=="DEFERRED"
    out={"status":"PASS","role":obj.get("role"),"body":a,
         "semantic_geometry_signature":stable_signature({"vertices":a["geometry_vertices_mm"],"faces":a["geometry_faces"]}),
         "blend_sha256":sha256(asset)}
    Path(output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("DINGFU_REOPEN_OK")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=("build","inspect"),required=True)
    for n in ("params","role","asset","semantic","review_dir","expected","output"): ap.add_argument("--"+n.replace("_","-"),dest=n)
    a=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    inspect(a.expected,a.asset,a.output) if a.mode=="inspect" else build(a.params,a.role,a.asset,a.semantic,a.review_dir)
if __name__=="__main__": main()
