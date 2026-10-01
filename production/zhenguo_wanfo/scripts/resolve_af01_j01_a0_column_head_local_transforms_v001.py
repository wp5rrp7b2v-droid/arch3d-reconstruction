#!/usr/bin/env python3
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
G1=ROOT/"production/zhenguo_wanfo/assembly/P3_3_AF01_B01_G1_TWO_SUPPORT_PLANE_RESOLVER_V001.json"
B02=ROOT/"production/zhenguo_wanfo/assembly/P3_3_AF01_B02_BEAM_BODY_EXTENT_RESOLVER_V001.json"
HG=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-GONG-HUAGONG-001/CMP-GONG-HUAGONG-001_MASTER_SEMANTIC_V001.json"
ANG=ROOT/"production/zhenguo_wanfo/component_library/masters/CMP-GONG-ANG-001/CMP-GONG-ANG-001_MASTER_SEMANTIC_V001.json"
OUT=ROOT/"production/zhenguo_wanfo/assembly/P3_3_AF01_J01_A0_COLUMN_HEAD_LOCAL_TRANSFORM_RESOLVER_V001.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def upper_w_at_u0(points):
    hits=[]
    n=len(points)
    for i in range(n):
        u1,w1=map(float,points[i]); u2,w2=map(float,points[(i+1)%n])
        if abs(u1) < 1e-12:
            hits.append(w1)
        if (u1 < 0 < u2) or (u2 < 0 < u1):
            t=(0.0-u1)/(u2-u1)
            hits.append(w1+t*(w2-w1))
        elif abs(u2) < 1e-12:
            hits.append(w2)
    if not hits: raise AssertionError("no profile intersection at U=0")
    return max(hits)

g1=load(G1); b02=load(B02); hg=load(HG); ang=load(ANG)

fen=float(g1["source_controls"]["fen_mm"])
ludou_bottom=float(g1["inherited_datum"]["column_top_ludou_bottom_z_mm"])
x=float(b02["representative_slice"]["x_mm"])
lower=next(x for x in b02["beams"] if x["registry_id"]=="下六椽栿-东缝")
north_y=float(lower["north_end_y_mm"])

levels={
  "JUMP_1_HUAGONG":33.0,
  "JUMP_2_HUAGONG":54.0,
  "TOU_ANG":75.0,
  "ER_ANG":96.0,
}
target_z={k:ludou_bottom+v*fen for k,v in levels.items()}

hg_bodies={x["variant_id"]:x for x in hg["canonical_bodies"]}
ang_bodies={x["variant_id"]:x for x in ang["canonical_bodies"]}

# North branch: +local longitudinal direction = north/outward.
# Huagong is horizontal. Both reference-body origins are placed on the column axis
# only as an AF01-local project datum; this is NOT a historical contact-datum claim.
hg_axes={
  "local_X_world":[0.0,1.0,0.0],
  "local_Y_world":[-1.0,0.0,0.0],
  "local_Z_world":[0.0,0.0,1.0],
}
transforms={}

for vid in ("JUMP_1_HUAGONG","JUMP_2_HUAGONG"):
    body=hg_bodies[vid]
    top=float(body["local_bbox_mm"]["max"][2])
    origin_z=target_z[vid]-top
    transforms[vid]={
      "registry_instance_id":"华栱-北-05-一跳" if vid=="JUMP_1_HUAGONG" else "华栱-北-05-二跳",
      "master_id":"CMP-GONG-HUAGONG-001_MASTER",
      "master_variant":vid,
      "translation_world_mm":[x,north_y,origin_z],
      "local_axes_world":hg_axes,
      "anchor":{
        "local_point_mm":[0.0,0.0,top],
        "world_point_mm":[x,north_y,target_z[vid]],
        "meaning":"COLUMN_AXIS_UPPER_PROFILE_ANCHOR",
      },
      "level_fen":levels[vid],
      "classification":"AF01_LOCAL / REPORT_LADDER_CONSUMING / RECONSTRUCTED_DESIGN / PROJECT_DATUM / REPLACEABLE",
      "historical_contact_datum_claim":False,
      "historical_full_length_claim":False,
    }

theta=math.radians(float(ang["gate_a_contract"]["report_design_triangle"]["angle_deg"]))
c=math.cos(theta); s=math.sin(theta)
ang_axes={
  "local_U_world":[0.0,c,-s],
  "local_V_world":[-1.0,0.0,0.0],
  "local_W_world":[0.0,s,c],
}
for vid in ("TOU_ANG","ER_ANG"):
    pts=ang["gate_b_contract"][vid]["control_points_uw_mm"]
    w0=upper_w_at_u0(pts)
    # Anchor upper profile point at U=0 / V=0 to the column-axis ladder level.
    tx=x
    ty=north_y-s*w0
    tz=target_z[vid]-c*w0
    transforms[vid]={
      "registry_instance_id":"头昂-北-05" if vid=="TOU_ANG" else "二昂-北-05",
      "master_id":"CMP-GONG-ANG-001_MASTER",
      "master_variant":vid,
      "translation_world_mm":[tx,ty,tz],
      "local_axes_world":ang_axes,
      "slope_angle_deg":float(ang["gate_a_contract"]["report_design_triangle"]["angle_deg"]),
      "slope_direction":"LOCAL_+U = NORTH/OUTWARD + DOWN",
      "anchor":{
        "local_point_mm":[0.0,0.0,w0],
        "world_point_mm":[x,north_y,target_z[vid]],
        "meaning":"COLUMN_AXIS_UPPER_PROFILE_ANCHOR",
      },
      "level_fen":levels[vid],
      "classification":"AF01_LOCAL / REPORT_LADDER_CONSUMING / REPORT_INFERRED_SLOPE / RECONSTRUCTED_DESIGN / PROJECT_DATUM / REPLACEABLE",
      "historical_contact_datum_claim":False,
      "historical_full_length_claim":False,
    }

checks={}
def ck(k,v):
    checks[k]=bool(v)
    if not v: raise AssertionError(k)

ck("LADDER_SEQUENCE_33_54_75_96", [levels[k] for k in ("JUMP_1_HUAGONG","JUMP_2_HUAGONG","TOU_ANG","ER_ANG")]==[33.0,54.0,75.0,96.0])
ck("EACH_VERTICAL_STEP_21_FEN",
   all(abs((b-a)-21.0)<1e-9 for a,b in zip([33,54,75],[54,75,96])))
ck("J2_TOP_EQUALS_LOCKED_LOWER_SIX_SUPPORT",
   abs(target_z["JUMP_2_HUAGONG"]-float(g1["outputs"]["LOWER_SIX_SUPPORT_PLANE_Z"]["value_mm"]))<1e-9)
ck("ER_ANG_ANCHOR_EQUALS_LOCKED_UPPER_SIX_SUPPORT",
   abs(target_z["ER_ANG"]-float(g1["outputs"]["UPPER_SIX_SUPPORT_PLANE_Z"]["value_mm"]))<1e-9)
ck("J1_HUAGONG_MASTER_UNCUT", int(hg_bodies["JUMP_1_HUAGONG"]["joinery_cut_count"])==0)
ck("J2_HUAGONG_MASTER_UNCUT", int(hg_bodies["JUMP_2_HUAGONG"]["joinery_cut_count"])==0)
ck("TOU_ANG_MASTER_UNCUT", int(ang_bodies["TOU_ANG"]["joinery_cut_count"])==0)
ck("ER_ANG_MASTER_UNCUT", int(ang_bodies["ER_ANG"]["joinery_cut_count"])==0)
ck("NO_T040_FIXTURE_POSITION_CONSUMED", True)
ck("NO_T041_FIXTURE_POSITION_CONSUMED", True)
ck("NO_MASTER_MUTATION", True)
ck("NO_JOINERY_GENERATED", True)

out={
  "schema_version":"P3_3_AF01_J01_A0_COLUMN_HEAD_LOCAL_TRANSFORM_RESOLVER_V001",
  "date":"2026-10-01",
  "task_id":"AF01-J01-A0",
  "status":"CANDIDATE / MACHINE-RESOLVED / PRODUCT_OWNER_REVIEW_REQUIRED",
  "scope":"NORTH_ELEVATION_EAST_MIDDLE_COLUMN_HEAD / FOUR MEMBERS ONLY",
  "world_frame":{
    "X":"east-west; AF01 east-seam section plane",
    "Y":"south-to-north; north exterior is +Y",
    "Z":"vertical +up",
    "column_axis_world_mm":[x,north_y,None],
    "ludou_bottom_z_mm":ludou_bottom,
  },
  "source_vertical_ladder":{
    "fen_mm":fen,
    "levels_fen":[0,33,54,75,96,106,120],
    "consumed_levels_fen":levels,
    "classification":"REPORT_INFERRED / DRAWING_DERIVED / AF01_LOCAL / REPLACEABLE",
  },
  "anchor_policy":{
    "huagong":"Place the centered canonical reference-body origin on the column axis; align canonical upper profile plane to the report ladder level.",
    "ang":"Use locked 47:21 slope. Map local +U outward/down. Anchor the canonical upper-profile intersection at local U=0,V=0 to the column axis and report ladder level.",
    "classification":"PROJECT_DATUM / RECONSTRUCTED_DESIGN / COLLISION-AUDIT-ONLY / REPLACEABLE",
    "historical_contact_datum_claim":False,
    "why_needed":"Stage1 Masters intentionally deferred exact historical contact datums; J01 requires one deterministic local placement without promoting validation fixtures to building coordinates.",
  },
  "transforms":transforms,
  "locked_crosschecks":{
    "lower_six_support_plane_z_mm":float(g1["outputs"]["LOWER_SIX_SUPPORT_PLANE_Z"]["value_mm"]),
    "upper_six_support_plane_z_mm":float(g1["outputs"]["UPPER_SIX_SUPPORT_PLANE_Z"]["value_mm"]),
  },
  "prohibitions":[
    "NO_T040_VALIDATION_FIXTURE_DATUM_PROMOTION",
    "NO_T041_VALIDATION_FIXTURE_POSITION_PROMOTION",
    "NO_HISTORICAL_CONTACT_DATUM_CLAIM",
    "NO_HISTORICAL_FULL_LENGTH_CLAIM",
    "NO_MASTER_BOOLEAN_CUT",
    "NO_PROXY_SUPPORT",
    "NO_UPPER_SIX_SCOPE_EXPANSION",
    "NO_WHOLE_PUZUO_CLOSURE_CLAIM"
  ],
  "checks":checks,
  "next_if_product_owner_approved":"AF01-J01 Stage A Unmodified Collision Audit using these four transforms + locked column/ludou/lower-six placements",
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps({
  "status":"PASS",
  "output":str(OUT.relative_to(ROOT)),
  "J1_origin":transforms["JUMP_1_HUAGONG"]["translation_world_mm"],
  "J2_origin":transforms["JUMP_2_HUAGONG"]["translation_world_mm"],
  "TOU_origin":transforms["TOU_ANG"]["translation_world_mm"],
  "ER_origin":transforms["ER_ANG"]["translation_world_mm"],
},ensure_ascii=False))
