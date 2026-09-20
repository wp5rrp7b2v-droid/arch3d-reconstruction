"""T-022 Blender builder, inspector and review renderer for Pingliang Master variants."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stable_signature(value):
    payload=json.dumps(value,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(payload).hexdigest()


def global_params(data):
    p={x["key"]:x for x in data["parameters"]}
    assert len(p)==len(data["parameters"])
    assert data["component_id"]=="CMP-FRAME-PINGLIANG-001"
    assert data["master_id"]=="CMP-FRAME-PINGLIANG-001_MASTER"
    assert data["master_version"]=="V001"
    assert data["unit"]=="mm"
    assert data["geometry_mode"]=="BOUNDED_LONG_MEMBER_OUTER_ENVELOPE"
    assert data["canonical_transform"]=={"location":[0,0,0],"rotation":[0,0,0],"scale":[1,1,1]}
    assert data["unsupported_geometry"]==[]
    assert data["p2_primary_frame_proxy_geometry_use_count"]==0
    assert p["historical_full_length_mm"]["value"] is None
    assert p["historical_full_length_mm"]["classification"]=="UNKNOWN"
    assert p["canonical_reference_length_mm"]["classification"]=="PROJECT_RULE"
    assert p["canonical_reference_length_mm"]["historical_claim"] is False
    assert p["realization_length_mm"]["derives_from"]=="canonical_reference_length_mm"
    assert float(p["realization_length_mm"]["value"])==float(p["canonical_reference_length_mm"]["value"])
    assert float(p["realization_length_mm"]["value"])>0
    return p


def variants(data):
    out={v["variant_id"]:v for v in data["variants"]}
    assert set(out)=={"EW_SEAM","GABLE"}
    assert len(out)==len(data["variants"])
    assert out["EW_SEAM"]["stable_variant_id"]=="CMP-FRAME-PINGLIANG-001__EW_SEAM"
    assert out["GABLE"]["stable_variant_id"]=="CMP-FRAME-PINGLIANG-001__GABLE"
    assert out["EW_SEAM"]["sample_to_instance_mapping"]=="UNKNOWN"
    assert out["GABLE"]["sample_to_instance_mapping"]=="UNKNOWN"
    assert out["GABLE"]["thickness_semantics"]["classification"]=="PARAMETRIC_COMPLETION"
    assert out["GABLE"]["thickness_semantics"]["replaceable"] is True
    assert out["GABLE"]["thickness_semantics"]["historical_claim"] is False
    return out


def names(variant_id):
    root="MASTER__CMP_FRAME_PINGLIANG_001__"+variant_id
    return root,root+"__BODY"


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj,do_unlink=True)
    for collection in list(bpy.data.collections):
        if collection != bpy.context.scene.collection:
            bpy.data.collections.remove(collection)


def make_mesh(data,p,v):
    length=float(p["realization_length_mm"]["value"])
    width=float(v["production_section_mm"]["width"])
    height=float(v["production_section_mm"]["thickness"])
    assert length>0 and width>0 and height>0
    verts=[
        (-length/2,-width/2,0),(length/2,-width/2,0),
        (length/2,width/2,0),(-length/2,width/2,0),
        (-length/2,-width/2,height),(length/2,-width/2,height),
        (length/2,width/2,height),(-length/2,width/2,height)
    ]
    faces=[(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
    collection_name,body_name=names(v["variant_id"])
    mesh=bpy.data.meshes.new(body_name+"__MESH")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    collection=bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    obj=bpy.data.objects.new(body_name,mesh)
    collection.objects.link(obj)
    obj.location=(0,0,0)
    obj.rotation_euler=(0,0,0)
    obj.scale=(1,1,1)
    obj["component_id"]=data["component_id"]
    obj["master_id"]=data["master_id"]
    obj["variant_id"]=v["variant_id"]
    obj["stable_variant_id"]=v["stable_variant_id"]
    obj["historical_full_length_state"]="UNKNOWN_NULL_DO_NOT_LOCK"
    obj["sample_to_instance_mapping"]="UNKNOWN"
    obj["reference_length_hard_fail"]=data["assembly_length_rule"]["hard_fail_id"]
    if v["variant_id"]=="GABLE":
        obj["thickness_classification"]="PARAMETRIC_COMPLETION"
        obj["thickness_historical_claim"]=False
    return obj


def body_payload(obj):
    verts=[[round(float(v.co[i]),6) for i in range(3)] for v in obj.data.vertices]
    faces=[list(poly.vertices) for poly in obj.data.polygons]
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
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
            "min":mins,
            "max":maxs,
            "dimensions":[round(maxs[i]-mins[i],6) for i in range(3)]
        },
        "primitive":"closed_rectangular_bounded_outer_envelope_reference",
        "unsupported_detail_count":0,
        "geometry_vertices_mm":verts,
        "geometry_faces":faces
    }


def setup_scene():
    scene=bpy.context.scene
    scene.unit_settings.system="METRIC"
    scene.unit_settings.scale_length=0.001
    scene.unit_settings.length_unit="MILLIMETERS"
    scene.render.engine="BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format="PNG"
    scene.render.film_transparent=False
    scene.render.resolution_percentage=100
    scene.world.use_nodes=True
    bg=next(node for node in scene.world.node_tree.nodes if node.type=="BACKGROUND")
    bg.inputs["Color"].default_value=(0.88,0.88,0.88,1)
    bg.inputs["Strength"].default_value=1
    scene.view_settings.look="AgX - Medium High Contrast"
    return scene


def emissive_material(name,shade):
    mat=bpy.data.materials.new(name)
    mat.use_nodes=True
    nodes=mat.node_tree.nodes
    nodes.clear()
    emission=nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value=(shade,shade,shade,1)
    out=nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(emission.outputs[0],out.inputs["Surface"])
    return mat


def camera(target,position,scale):
    data=bpy.data.cameras.new("T022_CAMERA")
    cam=bpy.data.objects.new("T022_CAMERA",data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera=cam
    data.type="ORTHO"
    data.clip_end=100000
    data.ortho_scale=scale
    cam.location=position
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
    return cam


def render_model_views(obj,p,v,review_dir):
    review_dir.mkdir(parents=True,exist_ok=True)
    scene=setup_scene()
    obj.data.materials.append(emissive_material("T022_REVIEW_BODY_"+v["variant_id"],0.58))
    length=float(p["realization_length_mm"]["value"])
    width=float(v["production_section_mm"]["width"])
    height=float(v["production_section_mm"]["thickness"])
    extent=max(length,width,height)
    target=(0,0,height/2)
    cam=camera(target,(0,-extent*3,height/2),extent*1.5)
    views={
        "FRONT":((0,-extent*3,height/2),max(length,height)*1.4),
        "SIDE":((extent*3,0,height/2),max(width,height)*1.5),
        "TOP":((0,0,extent*3),max(length,width)*1.4),
        "AXON":((extent*2,-extent*2.4,extent*1.9),extent*1.8)
    }
    for name,(position,scale) in views.items():
        cam.location=position
        cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
        cam.data.ortho_scale=scale
        scene.render.resolution_x=1200
        scene.render.resolution_y=900
        scene.render.filepath=str(review_dir/(v["variant_id"]+"_"+name+".png"))
        bpy.ops.render.render(write_still=True)


def render_text_page(path,title,lines):
    clear_scene()
    scene=setup_scene()
    scene.render.resolution_x=1200
    scene.render.resolution_y=900
    dark=emissive_material("T022_TEXT",0.08)
    for i,line in enumerate([title]+lines):
        curve=bpy.data.curves.new("TXT_"+str(i),type="FONT")
        curve.body=line
        curve.align_x="LEFT"
        curve.align_y="CENTER"
        curve.size=0.42 if i==0 else 0.28
        obj=bpy.data.objects.new("TXT_"+str(i),curve)
        bpy.context.scene.collection.objects.link(obj)
        obj.data.materials.append(dark)
        obj.location=(-7.4,5.5-i*0.95,0)
    camera((0,0,0),(0,0,20),17.5)
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)


def render_summaries(data,review_dir):
    vs=variants(data)
    ew=vs["EW_SEAM"]
    ga=vs["GABLE"]
    render_text_page(
        review_dir/"DIMENSION_PARAMETER_SUMMARY.png",
        "T-022 PINGLIANG / DIMENSION PARAMETER SUMMARY",
        [
            "EW_SEAM production section: 395.5 x 280.5 mm / measured family mean",
            "EW raw samples: 390 x 280; 401 x 281 mm / mapping UNKNOWN",
            "GABLE observed sample: width 346 mm / thickness UNKNOWN",
            "GABLE production section: 346 x 245.4 mm",
            "GABLE thickness: PARAMETRIC_COMPLETION / replaceable / non-historical",
            "Completion formula: 346 x 280.5 / 395.5 -> 245.4 mm",
            "Canonical reference length: 1000 mm / NON-HISTORICAL",
            "Historical full length: UNKNOWN / null"
        ]
    )
    render_text_page(
        review_dir/"EVIDENCE_UNCERTAINTY_SUMMARY.png",
        "T-022 PINGLIANG / EVIDENCE + UNCERTAINTY",
        [
            "Source: SRC-ZG-WF-001 / PDF p83 / printed p68 / table 2-40 / fig 2-41",
            "Physical instances: 4 / east-west seams 2 / gables 2",
            "EW sample-to-instance mapping: UNKNOWN",
            "GABLE sample-to-instance mapping: UNKNOWN",
            "GABLE thickness observed: UNKNOWN / null",
            "245.4 mm is project completion, NOT measured and NOT 963 design",
            "No mortise, tenon, groove, end-profile, camber or hidden-joint claim",
            "Building-specific length remains assembly-owned"
        ]
    )


def build(params_path,variant_id,asset_path,semantic_path,review_dir=None):
    data=json.loads(Path(params_path).read_text(encoding="utf-8"))
    p=global_params(data)
    vs=variants(data)
    assert variant_id in vs
    v=vs[variant_id]
    clear_scene()
    setup_scene()
    obj=make_mesh(data,p,v)
    asset_path=Path(asset_path)
    asset_path.parent.mkdir(parents=True,exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(asset_path),check_existing=False)
    body=body_payload(obj)
    semantic={
        "task":"T-022",
        "component_id":data["component_id"],
        "master_id":data["master_id"],
        "master_version":data["master_version"],
        "variant_id":variant_id,
        "stable_variant_id":v["stable_variant_id"],
        "blender_version":bpy.app.version_string,
        "geometry_mode":data["geometry_mode"],
        "geometry_lod":data["geometry_lod"],
        "geometry_semantics":data["geometry_semantics"],
        "resolved_global_parameters":{k:x["value"] for k,x in p.items()},
        "variant_semantics":v,
        "historical_state":data["historical_state"],
        "known_unknowns":data["known_unknowns"],
        "assembly_length_rule":data["assembly_length_rule"],
        "unsupported_geometry":data["unsupported_geometry"],
        "body":body,
        "semantic_geometry_signature":stable_signature({"vertices":body["geometry_vertices_mm"],"faces":body["geometry_faces"]}),
        "canonical_asset_path":str(asset_path),
        "canonical_blend_sha256":sha256(asset_path)
    }
    Path(semantic_path).parent.mkdir(parents=True,exist_ok=True)
    Path(semantic_path).write_text(json.dumps(semantic,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if review_dir:
        review_dir=Path(review_dir)
        render_model_views(obj,p,v,review_dir)
        render_summaries(data,review_dir)
    print("PINGLIANG_BUILD_OK",variant_id,semantic["semantic_geometry_signature"])


def inspect(expected_path,asset_path,output_path):
    expected=json.loads(Path(expected_path).read_text(encoding="utf-8"))
    _,body_name=names(expected["variant_id"])
    obj=bpy.data.objects.get(body_name)
    assert obj is not None and obj.type=="MESH"
    actual=body_payload(obj)
    assert actual==expected["body"]
    assert obj.get("component_id")==expected["component_id"]
    assert obj.get("master_id")==expected["master_id"]
    assert obj.get("variant_id")==expected["variant_id"]
    assert obj.get("stable_variant_id")==expected["stable_variant_id"]
    assert obj.get("historical_full_length_state")=="UNKNOWN_NULL_DO_NOT_LOCK"
    assert obj.get("sample_to_instance_mapping")=="UNKNOWN"
    if expected["variant_id"]=="GABLE":
        assert obj.get("thickness_classification")=="PARAMETRIC_COMPLETION"
        assert obj.get("thickness_historical_claim") is False
    out={
        "status":"PASS",
        "component_id":expected["component_id"],
        "master_id":expected["master_id"],
        "variant_id":expected["variant_id"],
        "stable_variant_id":expected["stable_variant_id"],
        "body":actual,
        "semantic_geometry_signature":stable_signature({"vertices":actual["geometry_vertices_mm"],"faces":actual["geometry_faces"]}),
        "blend_sha256":sha256(asset_path),
        "historical_full_length_mm":None
    }
    Path(output_path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PINGLIANG_REOPEN_OK",expected["variant_id"])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode",choices=("build","inspect"),required=True)
    parser.add_argument("--params")
    parser.add_argument("--variant")
    parser.add_argument("--asset")
    parser.add_argument("--semantic")
    parser.add_argument("--review-dir")
    parser.add_argument("--expected")
    parser.add_argument("--output")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    if args.mode=="inspect":
        inspect(args.expected,args.asset,args.output)
    else:
        build(args.params,args.variant,args.asset,args.semantic,args.review_dir)


if __name__=="__main__":
    main()
