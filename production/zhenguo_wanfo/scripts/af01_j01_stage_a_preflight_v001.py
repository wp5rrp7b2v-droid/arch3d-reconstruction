#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json"
IFACE = ROOT / "production/zhenguo_wanfo/assembly/P3_2_INTERFACE_REGISTRY_V001.json"
HUAGONG = ROOT / "production/zhenguo_wanfo/registry/P3_3_STAGE1_HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001.json"
ANG = ROOT / "production/zhenguo_wanfo/registry/P3_3_STAGE1_ANG_LENGTH_SLOPE_ASSEMBLY_CONTROL_SET_V001.json"
LOWER = ROOT / "production/zhenguo_wanfo/component_library/masters/CMP-FRAME-LOWER-SIX-CHUANFU-001/CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER_PARAMS_V001.json"

OUT = ROOT / "production/zhenguo_wanfo/validation/AF01_J01_STAGE_A_PREFLIGHT_V001.json"

required_instances = [
    ("柱-03", "CMP-COLUMN-001_MASTER"),
    ("柱头栌斗-北侧东中柱", "CMP-LUDOU-COLUMN-001_MASTER"),
    ("华栱-北-05-一跳", "CMP-GONG-HUAGONG-001_MASTER"),
    ("华栱-北-05-二跳", "CMP-GONG-HUAGONG-001_MASTER"),
    ("头昂-北-05", "CMP-GONG-ANG-001_MASTER"),
    ("二昂-北-05", "CMP-GONG-ANG-001_MASTER"),
    ("下六椽栿-东缝", "CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER"),
]

reg = json.loads(REG.read_text(encoding="utf-8"))
iface = json.loads(IFACE.read_text(encoding="utf-8"))
hg = json.loads(HUAGONG.read_text(encoding="utf-8"))
ang = json.loads(ANG.read_text(encoding="utf-8"))
lower = json.loads(LOWER.read_text(encoding="utf-8"))

items = {x["id"]: x for x in reg["items"]}
checks = {}
resolved = []

for iid, mid in required_instances:
    exists = iid in items
    master_ok = exists and items[iid].get("master_reference") == mid
    checks[f"INSTANCE_EXISTS::{iid}"] = exists
    checks[f"MASTER_BINDING::{iid}"] = master_ok
    if exists:
        resolved.append({
            "instance_id": iid,
            "component": items[iid].get("component"),
            "location": items[iid].get("location"),
            "master_reference": items[iid].get("master_reference"),
            "master_variant": items[iid].get("master_variant"),
            "count_status": items[iid].get("count_status"),
        })

iface_owners = {x.get("owner_node") for x in iface.get("interfaces", [])}
checks["HUAGONG_BUILDING_INTERFACE_MISSING"] = "CMP-GONG-HUAGONG-001" not in iface_owners
checks["ANG_BUILDING_INTERFACE_MISSING"] = "CMP-GONG-ANG-001" not in iface_owners
checks["HUAGONG_FIXTURE_NOT_REGISTRY_BOUND"] = hg["validation_fixture"]["registry_binding"] is False
checks["HUAGONG_FIXTURE_NOT_CANONICAL_ASSET"] = hg["validation_fixture"]["canonical_asset"] is False
checks["ANG_FIXTURE_NOT_CANONICAL_ASSET"] = ang["validation_fixture"]["canonical_asset"] is False
checks["ANG_BUILDING_PLACEMENT_NOT_IN_MASTER"] = ang["local_coordinate_and_datum"]["building_world_placement_in_master"] is False
checks["ANG_FIXTURE_NO_HISTORICAL_JOINERY"] = ang["validation_fixture"]["historical_joinery_claim"] is False

p = {x["key"]: x for x in lower["parameters"]}
checks["LOWER_SIX_TENON_THICKNESS_375_DIRECT"] = (
    float(p["tenon_area_thickness_mm"]["value"]) == 375.0
    and p["tenon_area_thickness_mm"]["source_layer"] == "DIRECT_PRIMARY"
)
checks["LOWER_SIX_TENON_THICKNESS_GEOMETRY_UNUSED"] = (
    int(p["tenon_area_thickness_mm"].get("geometry_use_count", 0)) == 0
)

instance_transform_keys = {
    iid: sorted(set(items[iid].keys()) & {
        "world_position", "world_rotation", "transform", "location_mm",
        "rotation_deg", "matrix_world", "assembly_transform"
    })
    for iid, _ in required_instances if iid in items
}
checks["NO_PER_INSTANCE_TRANSFORMS_IN_V008_FOR_J01"] = all(not v for v in instance_transform_keys.values())

identity_ready = all(
    checks[f"INSTANCE_EXISTS::{iid}"] and checks[f"MASTER_BINDING::{iid}"]
    for iid, _ in required_instances
)
placement_authority_ready = not (
    checks["HUAGONG_BUILDING_INTERFACE_MISSING"]
    or checks["ANG_BUILDING_INTERFACE_MISSING"]
    or checks["NO_PER_INSTANCE_TRANSFORMS_IN_V008_FOR_J01"]
)

stage_a_state = "READY_FOR_UNMODIFIED_COLLISION_AUDIT" if placement_authority_ready else "BLOCKED_BEFORE_COLLISION"
blocking_reason = None if placement_authority_ready else (
    "REAL_MASTER_IDENTITIES_EXIST_BUT_BUILDING_INSTANCE_LOCAL_TRANSFORMS_FOR_COLUMN_HEAD_HUAGONG_ANG_ARE_NOT_LOCKED; "
    "VALIDATION_FIXTURES_ARE_EXPLICITLY_NONCANONICAL_AND_NOT_REGISTRY_BOUND"
)

result = {
    "schema_version": "AF01_J01_STAGE_A_PREFLIGHT_V001",
    "task": "AF01-J01",
    "stage": "A / UNMODIFIED COLLISION AUDIT",
    "node": "NORTH_ELEVATION_EAST_MIDDLE_COLUMN_HEAD",
    "identity_readiness": identity_ready,
    "placement_authority_readiness": placement_authority_ready,
    "stage_a_state": stage_a_state,
    "collision_audit_executed": False,
    "collision_volume_claim": None,
    "blocking_reason": blocking_reason,
    "required_instances": resolved,
    "instance_transform_keys_found": instance_transform_keys,
    "lower_six_direct_constraint": {
        "max_thickness_mm": float(p["max_thickness_mm"]["value"]),
        "tenon_area_thickness_mm": float(p["tenon_area_thickness_mm"]["value"]),
        "tenon_area_geometry_use_count": int(p["tenon_area_thickness_mm"].get("geometry_use_count", 0)),
        "tenon_zone_location": "UNKNOWN",
        "tenon_zone_longitudinal_extent": "UNKNOWN",
    },
    "prohibited_substitutions": [
        "HUAGONG_VALIDATION_FIXTURE_AS_BUILDING_PLACEMENT",
        "ANG_VALIDATION_FIXTURE_AS_BUILDING_PLACEMENT",
        "GENERIC_PROXY_SUPPORT",
        "INVENTED_WORLD_OR_LOCAL_TRANSFORM",
        "MASTER_BOOLEAN_CUT",
    ],
    "checks": checks,
    "next_required_closure": (
        "AF01-J01-A0 COLUMN_HEAD LOCAL ASSEMBLY TRANSFORM RESOLVER "
        "(Huagong J1/J2 + Tou-Ang/Er-Ang relative to Ludou/Lower-Six support node only)"
        if not placement_authority_ready else None
    ),
    "historical_joinery_claim": False,
    "master_mutation": False,
}

if not all(checks.values()):
    bad = [k for k,v in checks.items() if not v]
    raise SystemExit("PREFLIGHT_CHECK_FAILED: " + ", ".join(bad))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({
    "preflight": "PASS",
    "stage_a_state": stage_a_state,
    "identity_readiness": identity_ready,
    "placement_authority_readiness": placement_authority_ready,
    "next_required_closure": result["next_required_closure"],
}, ensure_ascii=False))
