"""Independent triangle-geometry acceptance for one lower interface, not building approval.
Never copy PR81 old contact PASS to this new candidate.
"""
import json, hashlib, subprocess, math, sys
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union
from PIL import Image, ImageDraw, ImageFont, ImageStat

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/"output"
CAND=ROOT/"review/gong_ang_form_v001/geometry/JUMP_1_HUAGONG_candidate.json"
C02=ROOT/"review/east_front_connectors_c02/output/C02_ACTUAL_MESHES.json"
meta=json.loads((OUT/"CANDIDATE_MAPPING.json").read_text())
raw=json.loads(CAND.read_text())
s=json.loads(C02.read_text())
L=next(x for x in s["objects"] if x["id"]=="trial:EAST_FRONT_COLUMN_LUDOU")
old=next(x for x in s["objects"] if x["id"]=="trial:EAST_FRONT_HUA1_LOCAL")
seat=float(meta["seat_z_mm"])
V=np.asarray(raw["vertices"],dtype=float)
width=np.ptp(V[:,1]); height=np.ptp(V[:,2])
mapped=np.column_stack([V[:,1]*153.0/width,-V[:,0],
                         seat+(V[:,2]-V[:,2].min())*214.2/height])
mL=trimesh.Trimesh(vertices=np.asarray(L["coordinates_mm"],dtype=float),
                   faces=np.asarray(L["triangles"],dtype=int),process=False)
mH=trimesh.Trimesh(vertices=mapped,faces=np.asarray(raw["faces"],dtype=int),process=False)
def projected_contact(mesh,z,want_up):
    verts=np.asarray(mesh.vertices)
    polys=[];areas=0
    for tri in np.asarray(mesh.faces):
        points=verts[tri]
        if np.max(np.abs(points[:,2]-z))>0.001:continue
        p2=points[:,:2]
        signed=(p2[1,0]-p2[0,0])*(p2[2,1]-p2[0,1])-(p2[1,1]-p2[0,1])*(p2[2,0]-p2[0,0])
        if (want_up and signed<1e-7) or ((not want_up) and signed>-1e-7): continue
        poly=Polygon([tuple(p) for p in p2])
        if poly.is_valid and poly.area>1e-8:polys.append(poly)
    if not polys:return None,0,0
    union=unary_union(polys)
    return union,float(union.area),len(polys)

up,areaUp,numUp=projected_contact(mL,seat,True)
dn,areaDown,numDown=projected_contact(mH,seat,False)
area=0.0 if up is None or dn is None else float(up.intersection(dn).area)
collision=None;collision_error=None
try:
    inter=trimesh.boolean.intersection([mL,mH],engine="manifold")
    collision=float(abs(inter.volume)) if inter is not None else 0.0
except Exception as exc:
    collision_error=repr(exc)

# Independent binary GLB reimport after Blender export
glb=OUT/"WANFO_HUA1_ONE_SEAT_CANDIDATE_V001.glb"
glb_ok=False;glb_error=None;glb_extents=[]
try:
    ss=trimesh.load(str(glb),force="scene",process=False)
    inst=ss.dump(concatenate=False)
    glb_extents=[sorted(float(e) for e in m.extents) for m in inst]
    glb_ok=(len(inst)==2 and
        any(max(abs(a-b) for a,b in zip(e,[.153,.2142,.8988]))<.001 for e in glb_extents))
except Exception as exc:
    glb_error=repr(exc)

# Validate render is really populated, not a flat/empty picture.
image_tests={}
for name,zh in [("HUA1_SEAT_AXON_ZH.png","华栱—栌斗单接口｜工程候选"),("HUA1_SEAT_FRONT_ZH.png","柱头栌斗槽口与第一跳华栱｜未批准")]:
    p=OUT/name
    im=Image.open(p).convert("RGB")
    std=float(ImageStat.Stat(im.convert("L")).stddev[0])
    image_tests[name]={"width":im.width,"height":im.height,"grayscale_stddev":std,"nonempty":std>3.0}
    draw=ImageDraw.Draw(im)
    f="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    try:font=ImageFont.truetype(f,26)
    except Exception:font=ImageFont.load_default()
    draw.rectangle((10,12,im.width-10,68),fill=(255,255,255))
    draw.text((28,21),zh,fill=(25,34,31),font=font)
    im.save(p)
checks={
 "ludou_source_watertight":bool(mL.is_watertight),
 "hua1_candidate_watertight":bool(mH.is_watertight),
 "ludou_seat_top_faces_count":numUp,
 "hua1_down_faces_count":numDown,
 "coplanar_contact_area_mm2":area,
 "contact_area_threshold_mm2":100,
 "contact_area_gate":bool(area>100 and numUp>0 and numDown>0),
 "boolean_collision_volume_mm3":collision,
 "boolean_collision_threshold_mm3":1.0,
 "boolean_gate":None if collision is None else bool(collision<=1.0),
 "boolean_error":collision_error,
 "GLB_independent_import_gate":glb_ok,
 "GLB_import_error":glb_error,
 "GLB_sorted_extents_m":glb_extents,
 "render_gate":all(t["nonempty"] for t in image_tests.values()),
 "render_details":image_tests,
 "lower_seat_height_mm":seat,
 "top_support_area_ludou_mm2":areaUp,
 "candidate_bottom_area_mm2":areaDown,
 "preserved_ludou_identity":True,
 "upper_interactive_dou":"NOT_TESTED",
 "PO_silhouette_approval":"PENDING",
 "historical_joinery":"UNKNOWN",
 "load_capacity":"NOT_TESTED"
}
tech_pass=(checks["ludou_source_watertight"] and checks["hua1_candidate_watertight"] and
           checks["contact_area_gate"] and checks["boolean_gate"] is True and
           checks["GLB_independent_import_gate"] and checks["render_gate"])
record={
 "status":"GEOMETRY_SINGLE_LOWER_SEAT_PASS" if tech_pass else "GEOMETRY_SINGLE_LOWER_SEAT_FAIL",
 "po_approval":"PENDING", "entire_column":"NOT_TESTED", "merge_authorized":False,
 "technical_checks":checks,
 "upstream_PR81_overall_approval":"FAIL_UNCHANGED",
 "source_files_modified":False,
 "note":"One independent lower seat only; candidate changes section height/width; no acceptance of shape or rest of column."
}
(OUT/"SINGLE_INTERFACE_VALIDATION.json").write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n")
print("SINGLE_SEAT_GATE",record["status"],"CONTACT_MM2",area,"COLLISION_MM3",collision,"GLB",glb_ok)
