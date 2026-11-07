#!/usr/bin/env python3
"""Non-invasive museum dougong.gltf identity + views G1 proof (Blender 4.5.13).
Do not publish museum assets or generated renders in public Git. The GLTF/BIN and
views are temporary in Actions, retained only in a 7-day evidence artifact.
"""
import bpy
import hashlib
import json
import math
import os
import re
import shutil
import ssl
import tempfile
import traceback
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
TMP=ROOT/"_private_source_not_git"
SHOTS=ROOT/"_private_views_not_git"
for p in [OUT,TMP,SHOTS]:p.mkdir(parents=True,exist_ok=True)
URL="https://szbwgvue.chwhyun.cn/wanfodian/3d/dougong/dougong.gltf"
HOST="szbwgvue.chwhyun.cn"
CAP=22*1024*1024
trace={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"source_url":URL,
 "source_kind":"public_interactive_museum_exhibit_model",
 "source_https_identity":"UNVERIFIED_TLS_EXPIRED_FROM_G0",
 "third_party_license":"UNKNOWN_NOT_AUTHORIZED_FOR_PUBLIC_REDISTRIBUTION",
 "downloaded_external_source_in_git":False,
 "downloaded_external_source_in_artifact":False,
 "model_mesh_redistributed":False,
 "render_artifact_expiration_days":7,
 "A1_reference":"A1-p073.jpg (PDF73/print58), A1-p060.jpg (PDF60/print45), PR76 provenance",
 "A1_independent_same_member_correspondence":"NOT_PROVEN",
 "member_approval":"NOT_APPROVED","result":"NOT_TESTED","errors":[],
 "passes":{},"downloads":[],"node_metadata":{},
 "identity_classification":"UNKNOWN","views":[]}

def output():
    path=OUT/"DOUGONG_IDENTITY_PROOF.json"
    path.write_text(json.dumps(trace,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("WANFO_DOUGONG_G1_RESULT",trace["result"])
    print("WANFO_DOUGONG_G1_IDENTITY",trace["identity_classification"])
    print("WANFO_DOUGONG_G1_JSON",path)

def fetch(url,where):
    p=urllib.parse.urlsplit(url)
    if p.hostname!=HOST or p.scheme!="https":raise ValueError("Only specified museum HTTPS origin is allowed")
    # The test domain certificate expired on 2026-10-15. Diagnostic-only,
    # no cookies, no credentials, and do not promote assets as verified.
    ctx=ssl._create_unverified_context()
    req=urllib.request.Request(url,headers={"User-Agent":"WanfoAcademicReferenceFeasibility/0.1 (public research)"})
    with urllib.request.urlopen(req,timeout=30,context=ctx) as resp:
        actual=urllib.parse.urlsplit(resp.geturl())
        if actual.hostname!=HOST or actual.scheme!="https":
            raise ValueError("Cross-domain redirect forbidden")
        size=resp.headers.get("Content-Length")
        if size and int(size)>CAP:raise ValueError("Oversized source asset")
        b=resp.read(CAP+1)
        if len(b)>CAP:raise ValueError("Size cap exceeded")
        if resp.status!=200:raise RuntimeError("HTTP status "+str(resp.status))
        where.write_bytes(b)
        trace["downloads"].append({"url":url,"status":resp.status,"bytes":len(b),
                                  "sha256":hashlib.sha256(b).hexdigest(),"ephemeral_only":True})
    return b

try:
    raw=fetch(URL,TMP/"dougong.original.gltf")
    model=json.loads(raw.decode("utf-8"))
    assert str(model.get("asset",{}).get("version",""))=="2.0"
    nodes=model.get("nodes",[])
    meshes=model.get("meshes",[])
    trace["node_metadata"]["gltf_version"]="2.0"
    trace["node_metadata"]["source_node_count"]=len(nodes)
    trace["node_metadata"]["source_mesh_count"]=len(meshes)
    trace["node_metadata"]["scene_count"]=len(model.get("scenes",[]))
    trace["node_metadata"]["root_scenes"]=model.get("scene",0)
    trace["node_metadata"]["nodes_with_mesh"]=sum(isinstance(n,dict) and "mesh" in n for n in nodes)
    trace["node_metadata"]["node_name_counts"]={}
    labels=[(n.get("name",""),i) for i,n in enumerate(nodes)]
    trace["node_metadata"]["node_names_sample"]=[{"id":i,"name":name[:120]} for name,i in labels[:30]]
    generic=sum(bool(re.match(r"^(polySurface|pCube|mesh|Object)\d",name,re.I)) for name,i in labels)
    trace["node_metadata"]["generic_named_nodes"]=generic
    vocab={
      "ludou":["栌斗","lu dou","ludou"],
      "jump1":["第一跳","头跳","一跳","hua1","华栱001","华拱001"],
      "huagong":["华栱","华拱","huagong"],
      "dougong":["斗栱","斗拱","dougong"],
      "column":["柱","column"]
    }
    hits={}
    for k, terms in vocab.items():
        hits[k]=[{"node_index":i,"name":name[:120]} for name,i in labels if any(s.lower() in name.lower() for s in terms)]
    trace["node_metadata"]["semantic_hits"]=hits
    trace["node_metadata"]["notes"]="polySurface is an arbitrary DCC name, NOT a reliable historical component ID"
    trace["node_metadata"]["asset_up_axis"]=str(model.get("asset",{}).get("extras",{}).get("upAxis","UNKNOWN"))

    buffers=model.get("buffers",[])
    for n,buf in enumerate(buffers):
        uri=buf.get("uri","")
        if not uri or uri.startswith("data:"):raise RuntimeError("Unrecognized inline / missing buffer")
        u=urllib.parse.urljoin(URL,uri)
        up=urllib.parse.urlsplit(u)
        if up.hostname!=HOST:raise RuntimeError("Nonfirstparty buffer forbidden")
        local=TMP/("buffer_"+str(n)+".bin")
        fetch(u,local)
        buf["uri"]=local.name
    # Remove ONLY display materials/remote textures from an ephemeral import copy.
    # The geometric vertex/index buffer data are byte-for-byte unchanged.
    for m in meshes:
        for prim in m.get("primitives",[]):
            prim.pop("material",None)
    model["textures"]=[]
    model["images"]=[]
    model["materials"]=[]
    model.pop("extensionsUsed",None)
    model.pop("extensionsRequired",None)
    geometric=TMP/"dougong.geometry_only.gltf"
    geometric.write_text(json.dumps(model,ensure_ascii=False),encoding="utf-8")
    trace["passes"]["public_binary_geometry_retrieved"]=bool(buffers and meshes)
    trace["node_metadata"]["buffer_count"]=len(buffers)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(geometric))
    objects=[o for o in bpy.context.scene.objects if o.type=="MESH"]
    trace["node_metadata"]["blender_mesh_objects"]=len(objects)
    if not objects:raise RuntimeError("No mesh imported")
    # Deterministic all-mesh bbox, original source orientation; never claim historical axes.
    corners=[]
    bounds=[]
    for o in objects:
        pts=[o.matrix_world@Vector(v) for v in o.bound_box]
        corners.extend(pts)
        bb=[min(p[i] for p in pts) for i in range(3)]
        BB=[max(p[i] for p in pts) for i in range(3)]
        bounds.append({"source_object_name":o.name[:120],"local_index":len(bounds),
                       "mesh_vertices":len(o.data.vertices),"bbox_min":list(map(float,bb)),
                       "bbox_max":list(map(float,BB))})
    low=Vector([min(c[i] for c in corners) for i in range(3)])
    high=Vector([max(c[i] for c in corners) for i in range(3)])
    center=(low+high)/2
    ext=high-low
    trace["node_metadata"]["whole_bbox_min_gltf_unit"]=[float(x) for x in low]
    trace["node_metadata"]["whole_bbox_max_gltf_unit"]=[float(x) for x in high]
    trace["node_metadata"]["whole_bbox_extent_gltf_unit"]=[float(x) for x in ext]
    trace["node_metadata"]["whole_bbox_units_are_historically_calibrated"]=False
    trace["node_metadata"]["anonymous_mesh_bounding_summary"]=sorted(bounds,key=lambda x:x["bbox_min"][2])[:25]
    # No unsupportable name assignment: direct object names do not distinguish
    # lower LUDOU vs first-jump HUA1; A1 cannot validate a particular generic mesh ID.
    direct_identified=(len(hits["ludou"])>0 and len(hits["jump1"])>0)
    trace["identity_classification"]="NAMED_CANDIDATES_NEED_A1_CHECK" if direct_identified else "FAIL_EXACT_LUDOU_HUA1_IDENTITY_NOT_DERIVABLE_FROM_SOURCE_LABELS"
    trace["passes"]["semantic_identification_of_two_members"]=direct_identified
    trace["passes"]["same_east_front_physical_instance"]=False

    # Clay renders are diagnostic views only; model/texture bytes remain private.
    scene=bpy.context.scene
    scene.render.engine="CYCLES";scene.cycles.samples=12;scene.cycles.device="CPU"
    scene.render.resolution_x=1280;scene.render.resolution_y=960
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.film_transparent=False
    world=bpy.data.worlds.new("Neutral world");scene.world=world
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs["Color"].default_value=(.86,.88,.91,1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value=.75
    colors=[(.64,.39,.22),(.72,.52,.32),(.34,.52,.49),(.50,.55,.60),(.57,.45,.36)]
    for i,o in enumerate(objects):
        mat=bpy.data.materials.new("InspectionClay_%d"%i)
        mat.diffuse_color=(*colors[i%len(colors)],1.0)
        mat.use_nodes=True
        bsdf=mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:bsdf.inputs["Base Color"].default_value=(*colors[i%len(colors)],1.0)
        o.data.materials.clear();o.data.materials.append(mat)
    scene.camera=None
    size=max(float(ext[i]) for i in range(3))
    if not math.isfinite(size) or size<=0:raise RuntimeError("Bad source bbox")
    def camera(tag,direction):
        eye=center+Vector(direction)*size*2.2
        cd=bpy.data.cameras.new("CAM_"+tag)
        cam=bpy.data.objects.new("CAM_"+tag,cd)
        scene.collection.objects.link(cam)
        cam.location=eye;cam.rotation_euler=(center-eye).to_track_quat("-Z","Y").to_euler()
        cd.type="ORTHO";cd.ortho_scale=size*1.8
        scene.camera=cam
        scene.render.filepath=str(SHOTS/(tag+".png"))
        bpy.ops.render.render(write_still=True)
        pp=Path(scene.render.filepath)
        trace["views"].append({"filename":pp.name,"label":tag,"bytes":pp.stat().st_size,
            "sha256":hashlib.sha256(pp.read_bytes()).hexdigest(),"temporary_artifact_only":True,
            "purpose":"whole unlabelled gong assembly orientation view, NOT approved member evidence"})
        bpy.data.objects.remove(cam,do_unlink=True)
    for i,ofs in enumerate([(2,-3,3),(-3,-2,1),(0,3,1)]):
        l=bpy.data.lights.new("Light_%d"%i,"AREA")
        lo=bpy.data.objects.new("Light_%d"%i,l);scene.collection.objects.link(lo)
        lo.location=center+Vector(ofs)*size*1.4
        lo.rotation_euler=(center-lo.location).to_track_quat("-Z","Y").to_euler()
        l.energy=650;l.shape="DISK";l.size=max(.1,size*1.3)
    camera("MUSEUM_DOUGONG_ISOMETRIC", (1.35,-1.15,.85))
    camera("MUSEUM_DOUGONG_OPPOSITE",(-1.35,-1.15,.65))
    camera("MUSEUM_DOUGONG_SIDE",(0,1,.25))
    trace["passes"]["two_independent_views"]=len(trace["views"])>=2
    trace["passes"]["visual_member_evidence_sufficient"]=False
    trace["result"]="VIEWS_PASS_EXACT_IDENTITY_FAIL" if len(trace["views"])>=2 else "FAIL_VIEW_CREATION"
except Exception as e:
    trace["result"]="FAIL_DUE_TO_READ_OR_RENDER_ERROR"
    trace["errors"].append(type(e).__name__+": "+str(e)[:900])
    traceback.print_exc()
finally:
    output()
