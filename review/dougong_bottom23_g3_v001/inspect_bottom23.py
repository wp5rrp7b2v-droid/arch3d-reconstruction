#!/usr/bin/env python3
"""G3 bottom-23 mesh identification experiment.
Pinned museum source glTF/BIN are ephemeral only. Renders of 3P model retained
as short-lived artifacts; no museum mesh/texture or render enters public Git.
This is a visual identification aid, NOT a verified historical member map.
"""
from __future__ import annotations
import bpy, json, math, ssl, hashlib, urllib.request, urllib.parse, traceback, re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from mathutils import Vector

ROOT=Path(__file__).resolve().parent; OUT=ROOT/"output";TMP=ROOT/"_temporary_source";IMAGES=ROOT/"_temporary_23_thumbnails"
for d in (OUT,TMP,IMAGES):d.mkdir(parents=True,exist_ok=True)
HOST="szbwgvue.chwhyun.cn";URL="https://"+HOST+"/wanfodian/3d/dougong/"
EXPECTED={"dougong.gltf":"ac0687694715029a7b906bfdaa13578c578a01640e5cfeba1dbd29749dae6f1b",
"dougong.bin":"940224e259dfcce31f2a11aa58780422a38bcf0de869a2b1c72762321f0abc32"}
R={
 "status":"NOT_STARTED","method":"bottom 40 percent of whole model Z extent BY OBJECT BBOX CENTROID (G2 method)",
 "date_utc":datetime.now(timezone.utc).isoformat(),"source_url":URL+"dougong.gltf",
 "source_tls":"UNVERIFIED_DIAGNOSTIC_CERT_EXPIRED; SOURCE_HASHES_PINNED",
 "source_rights":"UNKNOWN; third-party mesh and derived views TEMPORARY only, not public Git",
 "source_exact_hash_verified":False,"source_files":[],"whole_meshes":0,"selected_count":0,
 "selected_rows":[],"possible_support_pairs":[],"possible_support_pairs_count":0,
 "crosscheck":{"A1_photo":"survey PDF73 (printed 58) fig 2-27 lower ang contact reference",
    "A1_matching_same_instance":"NOT_PROVEN",
    "A1_can_identify_polySurface_object":"NO",
    "memo":"A1 figure supports layering and lower-ang joint logic, not museum mesh IDs"},
 "gates":{"G3_inventory_23":False,"G3_distinct_object_views_23":False,
    "G3_positional_bounds":False,"G3_independent_id_ludou":False,
    "G3_independent_id_hua1":False,"G3_same_east_front_instance":False,
    "G3_actual_mesh_contact":False},
 "images":[],"errors":[]}
def n(x):return round(float(x),6)
def hashb(b):return hashlib.sha256(b).hexdigest()
def fetch(name):
    u=URL+name
    if name not in EXPECTED:raise ValueError("unexpected source")
    req=urllib.request.Request(u,headers={"User-Agent":"Wanfo Academic NonCommercial Research G3"})
    with urllib.request.urlopen(req,context=ssl._create_unverified_context(),timeout=25) as resp:
        p=urllib.parse.urlsplit(resp.geturl())
        if p.hostname!=HOST or p.scheme!="https":raise RuntimeError("forbidden redirect")
        b=resp.read(6_000_001)
    if len(b)>6_000_000 or hashb(b)!=EXPECTED[name]:raise RuntimeError("source changed or too large: "+name)
    path=TMP/name;path.write_bytes(b)
    R["source_files"].append({"filename":name,"bytes":len(b),"sha256":hashb(b),"exact_match_to_G1":True})
    return path
def write():
    f=OUT/"G3_BOTTOM23_OBJECT_REVIEW.json"
    f.write_text(json.dumps(R,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("G3_RESULT",R["status"],"SELECTED",R["selected_count"],"PAIRS",R["possible_support_pairs_count"])
try:
    raw=fetch("dougong.gltf"); fetch("dougong.bin")
    R["source_exact_hash_verified"]=True
    doc=json.loads(raw.read_text(encoding="utf8"))
    for mesh in doc["meshes"]:
        for prim in mesh.get("primitives",[]):prim.pop("material",None)
    doc["images"]=[];doc["textures"]=[];doc["materials"]=[]
    doc.pop("extensionsUsed",None);doc.pop("extensionsRequired",None)
    clean=TMP/"museum_geometric_only.gltf"
    clean.write_text(json.dumps(doc,ensure_ascii=False),encoding="utf8")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(clean))
    objs=sorted([o for o in bpy.context.scene.objects if o.type=="MESH"],key=lambda o:o.name)
    R["whole_meshes"]=len(objs)
    if len(objs)!=96:raise RuntimeError("expected 96 meshes")
    rows=[]
    for obj in objs:
        pts=[obj.matrix_world @ Vector(b) for b in obj.bound_box]
        lo=[min(v[i] for v in pts) for i in range(3)]
        hi=[max(v[i] for v in pts) for i in range(3)]
        ext=[hi[i]-lo[i] for i in range(3)]
        cent=[(hi[i]+lo[i])/2 for i in range(3)]
        long=max(ext[0],ext[1]);small=min(ext[0],ext[1])
        orient="X" if ext[0]>1.6*ext[1] else "Y" if ext[1]>1.6*ext[0] else "XY"
        shape="horizontal" if long>=max(.11,2.5*small) and long>1.65*ext[2] else ("vertical" if ext[2]>=max(.10,1.5*long) else ("compact" if max(ext)<=.13 else "mixed"))
        rows.append({"name":obj.name,"object":obj,"lo":lo,"hi":hi,"ext":ext,"cent":cent,
             "form":shape,"orientation":orient,"vertices":len(obj.data.vertices)})
    bounds_lo=[min(a["lo"][i] for a in rows) for i in range(3)]
    bounds_hi=[max(a["hi"][i] for a in rows) for i in range(3)]
    span=[bounds_hi[i]-bounds_lo[i] for i in range(3)]
    for row in rows:
        frac=(row["cent"][2]-bounds_lo[2])/span[2]
        row["band"]=max(1,min(5,1+int(5*frac)))
    chosen=sorted([row for row in rows if row["band"] in (1,2)],key=lambda z:(z["band"],z["cent"][2],z["name"]))
    R["selected_count"]=len(chosen)
    if len(chosen)!=23:raise RuntimeError("G2 bottom-band membership changed "+str(len(chosen)))
    # deterministic numbering is by relative height and then ID
    for index,row in enumerate(chosen,1):
        entry={"review_id":f"B{index:02d}","gltf_mesh_name":row["name"],
          "relative_band":row["band"],"orientation_envelope":row["orientation"],
          "form_envelope":row["form"],"bbox_center_source_units":[n(x) for x in row["cent"]],
          "bbox_extent_source_units":[n(x) for x in row["ext"]],
          "bbox_min_source_units":[n(x) for x in row["lo"]],
          "bbox_max_source_units":[n(x) for x in row["hi"]],
          "vertices":row["vertices"],"historical_member_name":"UNKNOWN",
          "same_specific_architectural_location_as_A1":"UNKNOWN"}
        R["selected_rows"].append(entry)
    R["gates"]["G3_inventory_23"]=True
    R["gates"]["G3_positional_bounds"]=all(all(x>0 for x in row["bbox_extent_source_units"]) for row in R["selected_rows"])
    # AABB neighborhood scan for selected pairs only: DOES NOT PROVE JOINERY OR PHYSICAL CONTACT.
    gap_eps=.015*span[2];min_area=.00012*span[0]*span[1]
    pairs=[]
    ids={x["name"]:f"B{i:02d}" for i,x in enumerate(chosen,1)}
    for a in chosen:
        for b in chosen:
            if a is b:continue
            gap=b["lo"][2]-a["hi"][2]
            if abs(gap)>gap_eps:continue
            x=max(0,min(a["hi"][0],b["hi"][0])-max(a["lo"][0],b["lo"][0]))
            y=max(0,min(a["hi"][1],b["hi"][1])-max(a["lo"][1],b["lo"][1]))
            A=x*y
            if A<=min_area:continue
            ratio=A/max(1e-12,min(a["ext"][0]*a["ext"][1],b["ext"][0]*b["ext"][1]))
            if ratio<.10:continue
            pairs.append({"lower":ids[a["name"]],"upper":ids[b["name"]],
              "lower_mesh":a["name"],"upper_mesh":b["name"],
              "bbox_area_overlap_ratio":n(ratio),"gap_as_model_height":n(gap/span[2]),
              "evidence_status":"INFERENCE_AABB_NOT_REAL_CONTACT"})
    pairs.sort(key=lambda x:(-x["bbox_area_overlap_ratio"],abs(x["gap_as_model_height"]),x["lower"],x["upper"]))
    R["possible_support_pairs"]=pairs
    R["possible_support_pairs_count"]=len(pairs)
    # Every object given a separate, automatically normalized thumbnail.
    # Normalization is ONLY for visibility, NOT component proportions or size comparison.
    scene=bpy.context.scene;scene.render.engine="BLENDER_WORKBENCH"
    scene.display.shading.light="STUDIO"
    scene.display.shading.color_type="MATERIAL"
    scene.display.shading.show_shadows=True
    scene.render.resolution_x=430;scene.render.resolution_y=310
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.render.film_transparent=False
    camdata=bpy.data.cameras.new("G3_MEMBER_CAMERA")
    cam=bpy.data.objects.new("G3_MEMBER_CAMERA",camdata)
    scene.collection.objects.link(cam)
    scene.camera=cam;camdata.type="ORTHO"
    directions={"axon":Vector((1.2,-1.4,.8)),"top":Vector((.01,-.005,2.0))}
    # Thumbnail from same camera direction; source geometry and axes unmodified.
    for entry,row in zip(R["selected_rows"],chosen):
        for q in objs:q.hide_render=q!=row["object"]
        camera=cam
        eye=Vector(row["cent"])+directions["axon"]*max(row["ext"])*2.5
        cam.location=eye
        cam.rotation_euler=(Vector(row["cent"])-eye).to_track_quat("-Z","Y").to_euler()
        camdata.ortho_scale=max(.055,max(row["ext"])*1.6)
        imgpath=IMAGES/(entry["review_id"]+"_"+entry["gltf_mesh_name"]+".png")
        scene.render.filepath=str(imgpath)
        bpy.ops.render.render(write_still=True)
        info={"review_id":entry["review_id"],"name":entry["gltf_mesh_name"],
              "filename":imgpath.name,"size_bytes":imgpath.stat().st_size,
              "sha256":hashb(imgpath.read_bytes()),"style":"solo normalized axon thumbnail; no comparison of absolute dimensions"}
        R["images"].append(info)
    for q in objs:q.hide_render=False
    R["gates"]["G3_distinct_object_views_23"]=len(R["images"])==23 and all(x["size_bytes"]>3500 for x in R["images"])
    # Separate in-situ low-band group view as context, from source, also temporary.
    for q in objs:q.hide_render=q.name not in ids
    all_pts=[Vector(row["lo"]) for row in chosen]+[Vector(row["hi"]) for row in chosen]
    c=Vector([sum(p[i] for p in all_pts)/len(all_pts) for i in range(3)])
    diam=max(max(row["hi"][i] for row in chosen)-min(row["lo"][i] for row in chosen) for i in range(3))
    cam.location=c+Vector((1.4,-1.6,.9))*diam*2.8
    cam.rotation_euler=(c-cam.location).to_track_quat("-Z","Y").to_euler()
    camdata.ortho_scale=diam*2.5
    scene.render.resolution_x=1250;scene.render.resolution_y=950
    path=IMAGES/"B00_BOTTOM23_CONTEXT.png"
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)
    R["images"].append({"review_id":"B00","filename":path.name,"size_bytes":path.stat().st_size,
                        "sha256":hashb(path.read_bytes()),"style":"all bottom 23 grouped view for context"})
    for q in objs:q.hide_render=False
    R["status"]="PASS_BOTTOM23_OBJECT_VIEWS__EXACT_MEMBERS_UNKNOWN"
except Exception as e:
    traceback.print_exc();R["errors"].append(type(e).__name__+": "+str(e)[:1000]);R["status"]="FAIL_G3_EXECUTION"
finally:write()
