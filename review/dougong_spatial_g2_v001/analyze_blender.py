#!/usr/bin/env python3
"""G2: inspect museum dougong's anonymous 96 mesh scene without replicating mesh assets.

SOURCE CONTENT IS SHORT-LIVED AND NEVER COMMITTED.
Only orientation classes, pair candidates, coarse layer statistics and source hash
may be stored. AABB candidates are NOT geometric mating/contact proof.
"""
from __future__ import annotations
import bpy
import hashlib
import json
import math
import os
import re
import ssl
import traceback
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
PRIVATE=ROOT/"_temporary_original_museum_mesh"
VIEWS=ROOT/"_temporary_review_images"
for p in [OUT,PRIVATE,VIEWS]:p.mkdir(exist_ok=True,parents=True)
BASE="https://szbwgvue.chwhyun.cn/wanfodian/3d/dougong/"
EXPECTED={"dougong.gltf":"ac0687694715029a7b906bfdaa13578c578a01640e5cfeba1dbd29749dae6f1b",
          "dougong.bin":"940224e259dfcce31f2a11aa58780422a38bcf0de869a2b1c72762321f0abc32"}
report={
 "status":"NOT_RUN","date_utc":datetime.now(timezone.utc).isoformat(),
 "test":"G2 museum anonymous dougong mesh topology, relative strata and adjacency",
 "source_url":BASE+"dougong.gltf",
 "source_cert_validation":"BYPASSED_AFTER_KNOWN_CERT_EXPIRY_FOR_DIAGNOSTIC_ONLY",
 "source_hash_pinned_to_previous_G1":False,
 "source_reuse_permission":"UNKNOWN; NOT COPYING SOURCE MESHES TO GITHUB",
 "source_instance_correspondence_to_east_seam":"UNKNOWN",
 "data_categories":{"FACT":"geometry bounds, orientation and count of loaded anonymous meshes, pinned hashes",
                   "INFERENCE":"relative layer clusters and bbox potential support candidate pair",
                   "UNKNOWN":"ludou/first jump mapping, actual contact, tenon, dimensions, construction date accuracy"},
 "files":{},"geometry":{},"layers":[],"orientation_counts":{},"form_counts":{},
 "contact_candidate_count":0,"contact_candidates":[],"crosscheck":{},
 "views":[],"errors":[],"gates":{}
}
def sha(data):return hashlib.sha256(data).hexdigest()
def get_file(name):
    if name not in EXPECTED:raise ValueError("unexpected source filename")
    u=BASE+name
    pr=urllib.parse.urlsplit(u)
    if pr.hostname!="szbwgvue.chwhyun.cn" or pr.scheme!="https":raise ValueError("unknown source")
    # G0 established site certificate expired 2026-10-15. This is a non-authoritative
    # diagnostic against previously-recorded fixed SHA values, never a secure identity check.
    req=urllib.request.Request(u,headers={"User-Agent":"Wanfo-Geometry-Research-G2/0.1"})
    with urllib.request.urlopen(req,context=ssl._create_unverified_context(),timeout=30) as response:
        final=urllib.parse.urlsplit(response.geturl())
        if final.hostname!=pr.hostname or final.scheme!="https":raise RuntimeError("cross-origin redirect")
        raw=response.read(6_000_001)
    if len(raw)>6_000_000:raise RuntimeError("source larger than cap")
    h=sha(raw)
    if h!=EXPECTED[name]:raise RuntimeError("SOURCE_HASH_CHANGED: "+name)
    p=PRIVATE/name
    p.write_bytes(raw)
    report["files"][name]={"bytes":len(raw),"sha256":h,"pinned_match":True,"stored_only_in_ephemeral_runner":True}
    return p
def wjson():
    (OUT/"G2_SPATIAL_PROOF.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("G2_STATUS",report["status"])
    print("G2_POSSIBLE_CONNECTIONS",report["contact_candidate_count"])
    print("G2_SOURCE_PINNED",report["source_hash_pinned_to_previous_G1"])
    print("G2_UNPROVEN_INSTANCE",report["source_instance_correspondence_to_east_seam"])
def num(x):return round(float(x),6)
try:
    src=get_file("dougong.gltf")
    buf=get_file("dougong.bin")
    report["source_hash_pinned_to_previous_G1"]=True
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Geometry-only import copy in temporary runner. Original vertex/index buffers
    # remain unchanged; no external textures or third-party material downloads.
    doc=json.loads(src.read_text(encoding="utf-8"))
    for mesh in doc.get("meshes",[]):
        for prim in mesh.get("primitives",[]):prim.pop("material",None)
    doc["images"]=[];doc["textures"]=[];doc["materials"]=[]
    doc.pop("extensionsUsed",None);doc.pop("extensionsRequired",None)
    safe=PRIVATE/"dougong.geometry_only.gltf"
    safe.write_text(json.dumps(doc,ensure_ascii=False),encoding="utf-8")
    # Keep source external binaries temporary. Do not export source material.
    bpy.ops.import_scene.gltf(filepath=str(safe))
    objs=sorted([o for o in bpy.context.scene.objects if o.type=="MESH"],key=lambda o:o.name)
    if len(objs)!=96:raise RuntimeError("Unexpected mesh count: "+str(len(objs)))
    mesh_rows=[]
    for o in objs:
        bb=[o.matrix_world@Vector(c) for c in o.bound_box]
        low=[min(v[k] for v in bb) for k in range(3)]
        high=[max(v[k] for v in bb) for k in range(3)]
        ext=[high[k]-low[k] for k in range(3)]
        ctr=[(high[k]+low[k])/2 for k in range(3)]
        xy_l=max(ext[0],ext[1]);xy_s=min(ext[0],ext[1])
        axis="X" if ext[0]>ext[1]*1.6 else "Y" if ext[1]>ext[0]*1.6 else "XY/MIXED"
        if xy_l>=max(.11,2.5*xy_s) and xy_l>1.65*ext[2]:
            broad="elongated horizontal envelope"
        elif ext[2]>=max(.1,1.5*xy_l):
            broad="vertically extended envelope"
        elif max(ext)<=.13:
            broad="compact envelope"
        else:
            broad="other/mixed envelope"
        row={"o":o,"id":o.name,"lo":low,"hi":high,"ext":ext,"ctr":ctr,
             "direction":axis,"form":broad,"verts":len(o.data.vertices)}
        mesh_rows.append(row)
    world_low=[min(x["lo"][k] for x in mesh_rows) for k in range(3)]
    world_high=[max(x["hi"][k] for x in mesh_rows) for k in range(3)]
    world_ext=[world_high[k]-world_low[k] for k in range(3)]
    if world_ext[2]<=0:raise RuntimeError("Invalid vertical extent")
    report["geometry"]={
      "object_count":len(objs),
      "vertex_count":sum(x["verts"] for x in mesh_rows),
      "object_name_example":[x["id"] for x in mesh_rows[:6]],
      "generic_names_count":sum(bool(re.match(r"^polySurface\d+$",x["id"],re.I)) for x in mesh_rows),
      "extent_source_units":[num(x) for x in world_ext],
      "historically_calibrated_units":False,
      "axis_note":"Blender glTF imported Z treated as display up; actual architecture orientation not authenticated",
      "mesh_data_exported":False
    }
    report["orientation_counts"]=dict(Counter(x["direction"] for x in mesh_rows))
    report["form_counts"]=dict(Counter(x["form"] for x in mesh_rows))
    # Dividing the source scene into 5 equal vertical bands is explicitly a
    # visualization convention, NOT original architectural 5-level classification.
    for r in mesh_rows:
        band=max(0,min(4,int(5*(r["ctr"][2]-world_low[2])/world_ext[2])))
        r["band"]=band
    report["layers"]=[
       {"display_band":i+1,"height_range_fraction":[i/5,(i+1)/5],
        "mesh_centroid_count":sum(r["band"]==i for r in mesh_rows),
        "directions":dict(Counter(r["direction"] for r in mesh_rows if r["band"]==i)),
        "forms":dict(Counter(r["form"] for r in mesh_rows if r["band"]==i))}
       for i in range(5)
    ]
    # Bounding envelope proximity only. It is NOT a true contact computation.
    near=[]
    z_eps=world_ext[2]*.015
    xy_base=(world_ext[0]*world_ext[1])*.00012
    for a in mesh_rows:
        for b in mesh_rows:
            if a is b:continue
            gap=b["lo"][2]-a["hi"][2]
            if abs(gap)>z_eps:continue
            overlap_x=max(0,min(a["hi"][0],b["hi"][0])-max(a["lo"][0],b["lo"][0]))
            overlap_y=max(0,min(a["hi"][1],b["hi"][1])-max(a["lo"][1],b["lo"][1]))
            overlap=overlap_x*overlap_y
            if overlap<=xy_base:continue
            min_area=min(a["ext"][0]*a["ext"][1],b["ext"][0]*b["ext"][1])
            ratio=overlap/max(1e-10,min_area)
            if ratio<.10:continue
            near.append({"lower_name":a["id"],"upper_name":b["id"],
                         "xy_bbox_overlap_ratio":num(ratio),
                         "z_top_to_bottom_gap_as_height_fraction":num(gap/world_ext[2]),
                         "classification":"AABB_POTENTIAL_ONLY"})
    near.sort(key=lambda x:(-x["xy_bbox_overlap_ratio"],abs(x["z_top_to_bottom_gap_as_height_fraction"])))
    report["contact_candidate_count"]=len(near)
    report["contact_candidates"]=near[:55]
    report["gates"]["source_geometry_exact_hashes_pass"]=True
    report["gates"]["96_nodes_mesh_instances_pass"]=len(objs)==96
    report["gates"]["relative_layer_map_pass"]=sum(x["mesh_centroid_count"] for x in report["layers"])==96
    report["gates"]["candidate_envelope_adjacency_computed"]=True
    report["gates"]["real_mesh_contact_or_mortise_pass"]=False
    report["gates"]["named_ludou_and_first_hua_gong"]=False
    report["gates"]["A1_same_east_front_instance_proven"]=False
    report["crosscheck"]={
      "A1_original_page":"精细测绘报告 PDF73 印刷第58页 图2-27",
      "A1_caption":"万佛殿下昂部位交接关系参考示意图",
      "A1_evidence":"实物照片+示意图可核对下昂与层间斗栱的相对交接关系",
      "A1_missing":"没有直接列出博物馆网页中 polySurfaceXXXX 对应的部件索引，不能证明同一柱头实体",
      "independent_licensing":"UNKNOWN",
      "status":"A1_RELATIVE_ARCHITECTURAL_LOGIC_ONLY"
    }
    # Aggregate chart in SVG (not 3P meshes), publishable as metadata plot.
    W,H=1050,600
    cc=["#a1c5b6","#c6b884","#ddb79c","#b5b5db","#9cb4d1"]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="600" viewBox="0 0 1050 600">',
         '<rect width="1050" height="600" fill="#f7f7f4"/>',
         '<text x="50" y="62" font-family="sans-serif" font-size="27" font-weight="bold" fill="#242c2d">数字博物馆斗栱：相对高度分布（96个匿名网格）</text>',
         '<text x="50" y="100" font-family="sans-serif" font-size="16" fill="#485459">高度分为5等份，仅为可复核的统计分组，不代表五层真实铺作</text>']
    for i,band in enumerate(report["layers"]):
        n=band["mesh_centroid_count"]
        y=148+i*77
        svg.extend([f'<text x="53" y="{y+38}" font-family="sans-serif" font-size="18" fill="#273c42">位置组 {i+1}</text>',
                    f'<rect x="190" y="{y+8}" width="{min(640,max(4,n*19))}" height="46" rx="5" fill="{cc[i]}"/>',
                    f'<text x="{210+min(640,max(4,n*19))}" y="{y+39}" font-family="sans-serif" font-size="20" fill="#273c42">{n}件</text>'])
    svg.extend(['<text x="50" y="560" font-family="sans-serif" font-size="13" fill="#60656c">只归纳模型相对空间关系；未通过具体构件身份、历史尺寸、真实接触面积验证。</text>',
                '</svg>'])
    (OUT/"G2_RELATIVE_LAYER_COUNTS.svg").write_text("\n".join(svg),encoding="utf-8")
    # Render grouped anonymous geometry only for ephemeral review, not public git.
    scene=bpy.context.scene
    mat_colors=[(.62,.77,.70),(.80,.70,.52),(.82,.62,.51),(.65,.66,.82),(.56,.70,.84)]
    for o in objs:
        band=next(r["band"] for r in mesh_rows if r["id"]==o.name)
        col=mat_colors[band]
        mat=bpy.data.materials.new("RELATIVE_BAND_"+str(band)+"_"+o.name)
        mat.use_nodes=True
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*col,1)
        mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value=.7
        o.data.materials.clear()
        o.data.materials.append(mat)
    # Material selection and lighting can visualize strata but do not change mesh geometry.
    sz=max(world_ext)
    focus=Vector([(world_low[i]+world_high[i])/2 for i in range(3)])
    scene.render.engine="CYCLES";scene.cycles.samples=16;scene.cycles.device="CPU"
    scene.render.resolution_x=1365;scene.render.resolution_y=960
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    world=bpy.data.worlds.new("G2_MATTE_WORLD");world.use_nodes=True
    world.node_tree.nodes["Background"].inputs["Color"].default_value=(.90,.92,.94,1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value=.75
    scene.world=world
    for i,ofs in enumerate([(2.2,-3.0,2.7),(-3.2,1.5,2.9)]):
        light=bpy.data.lights.new("G2_LIGHT_"+str(i),"AREA")
        o=bpy.data.objects.new("G2_LIGHT_"+str(i),light)
        scene.collection.objects.link(o)
        o.location=focus+Vector(ofs)*sz
        light.energy=550
        light.size=max(1,sz*2.5)
    # review cameras. The 3rd isolates only lower-most centroid group for inspectability.
    def render(name,direction,limit_band=None):
        # Hide higher levels only in isolated preview and restore immediately.
        if limit_band is not None:
            for row in mesh_rows:row["o"].hide_render=row["band"]>limit_band
        camd=bpy.data.cameras.new("G2_CAM_"+name)
        cam=bpy.data.objects.new("G2_CAM_"+name,camd);scene.collection.objects.link(cam)
        eye=focus+Vector(direction)*sz*2.7
        cam.location=eye
        cam.rotation_euler=(focus-eye).to_track_quat("-Z","Y").to_euler()
        camd.type="ORTHO";camd.ortho_scale=sz*2.45
        scene.camera=cam
        path=VIEWS/("MUSEUM_G2_"+name+".png")
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        report["views"].append({"name":name,"filename":path.name,"sha256":sha(path.read_bytes()),
                                 "bytes":path.stat().st_size,
                                 "source_model_view":True,
                                 "retention_days":7,
                                 "distribute_in_public_git":False})
        bpy.data.objects.remove(cam,do_unlink=True)
        for row in mesh_rows:row["o"].hide_render=False
    render("AXON_LAYER_COLORS",(1.4,-1.8,1.15))
    render("SIDE_LAYER_COLORS",(0,-2.5,.52))
    render("LOWER_TWO_GROUPS_ONLY",(1.4,-1.8,1.15),limit_band=1)
    report["gates"]["three_nonempty_renders"]=len(report["views"])==3 and all(v["bytes"]>30000 for v in report["views"])
    report["status"]="PASS_RELATIVE_TOPOLOGY_ONLY_MEMBER_IDENTITY_UNPROVEN"
except Exception as e:
    report["status"]="FAIL_G2_PROCEDURE"
    report["errors"].append(type(e).__name__+": "+str(e)[:800])
    traceback.print_exc()
finally:
    wjson()
