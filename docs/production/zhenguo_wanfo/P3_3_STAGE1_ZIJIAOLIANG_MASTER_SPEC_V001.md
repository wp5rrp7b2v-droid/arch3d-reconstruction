# P3.3 V002 Stage 1｜子角梁 Master Spec V001

**状态：LOCKED / PRODUCT OWNER AUTHORIZED / D-142**  
**日期：2026-09-25**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019**  
**复原：D-108 / RC-020 + D-137 / RC-023**  
**连接层：D-139 / RC-024**  
**视觉门：D-076 PASS WITH GEOMETRY BOUNDARY**

## 1. Identity

- 中文名：子角梁
- component id：`CMP-FRAME-ZIJIAOLIANG-001`
- master id：`CMP-FRAME-ZIJIAOLIANG-001_MASTER`
- version：`V001`
- physical instances：**4**
- locations：东北 / 东南 / 西南 / 西北
- family：角梁
- geometry variants：**0**

One shared parametric Master. Location and replacement history do not create separate Master identities without stable body-form evidence.

## 2. Authority

A1:
- PDF p88–89 / printed p73–74
- §2.3.1.7
- Fig.2-50
- actual Table 2-44
- binding: `docs/evidence/zhenguo_wanfo/P3_3_ZIJIAOLIANG_DIRECT_SOURCE_BINDING_V001.md`

A2:
- official same-building corner-beam / 套兽 visual semantics
- not dimensional authority.

Registry:
`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

## 3. Direct instance section contract

| registry id | location | width mm | thickness mm | status |
|---|---|---:|---:|---|
| 子角梁-东南角 | 东南角 | 220 | 150 | extant direct measured |
| 子角梁-东北角 | 东北角 | 190 | 153 | extant direct measured / historical replacement context |
| 子角梁-西南角 | 西南角 | 213 | 153 | extant direct measured |
| 子角梁-西北角 | 西北角 | 125 | 149 | extant direct measured / historical replacement context |

Rules:
- instance sections are direct current-state evidence;
- no family mean may overwrite them;
- no separate Master or Geometry Variant is created solely from section difference;
- replacement status is metadata unless body-form evidence proves a stable variant.

## 4. Family reference specimen

Report-published family mean:
- width **216.5 mm**
- thickness **152 mm**

Canonical Stage1 reference body:
**1000 × 216.5 × 152 mm**

Classification:
- 1000 = `RECONSTRUCTION_REFERENCE_LENGTH / NON_HISTORICAL / REPLACEABLE`
- 216.5×152 = `REPORT_PUBLISHED_FAMILY_MEAN / REFERENCE_SPECIMEN_ONLY / SOURCE_AGGREGATION_METHOD_AMBIGUOUS`

All-four arithmetic mean 187×151.25 is audit metadata only and does not silently replace the published family statistic.

## 5. Geometry

Mode:
`PARAMETRIC_ENDPOINT_DRIVEN_LONG_MEMBER_WITH_INSTANCE_SECTION_PARAMETERS`

Axes:
- +X longitudinal
- +Y width / 广
- +Z thickness / 厚

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

Stage1 representation:
- rectangular bounding-envelope proxy
- simplified flat ends
- no historical exact profile claim.

## 6. Endpoint-driven assembly

Actual building length/orientation are assembly-owned:
- `V=P_end-P_start`
- `L=||V||`
- local +X aligns to V
- center = midpoint.

Master must not contain:
- fixed historical full length;
- fixed 45° historical installation angle;
- final Wanfodian XYZ.

## 7. Related identities

Explicitly excluded:
- 大角梁
- 隐角梁
- 隐衬角栿 / 递角栿
- 翼角椽
- 套兽 geometry itself.

The 套兽 remains a separate physical/accessory identity even though its attachment semantic is registered here.

## 8. Connection Layer metadata｜RC-024

`OUTBOARD_END / TAOSHOU_ATTACHMENT`
- later kind: PHYSICAL_CONNECTOR / accessory attachment
- evidence: A2 direct same-building semantic
- exact fit/socket: unresolved
- no structural load-path claim.

`INBOARD_CORNER_ASSEMBLY`
- related family: 大角梁 / corner assembly
- exact kind: unresolved
- later resolution restricted to evidence-backed JOINERY_FEATURE or CONTACT_INTERFACE
- no invented mortise/tenon.

## 9. Historical replacement boundary

A1 states NE/NW are replacement-affected.

Therefore:
- extant measurements remain direct evidence for the modeled current/reliable-source building state;
- replacement history does not automatically create a Geometry Variant;
- no claim that NE/NW values represent 963 originals;
- no attempt to reconstruct unknown pre-replacement dimensions is required for Stage1.

## 10. Required Review Board

1. AXON
2. LONG_SIDE
3. END_SECTION
4. DIMENSION_AND_PARAMETRIC_LENGTH
5. PLACEMENT_AND_ENDPOINT_LOGIC
6. SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY

END_SECTION must show:
- family reference 216.5×152;
- SE 220×150;
- NE 190×153;
- SW 213×153;
- NW 125×149;
- family mean reference only;
- replacement status does not erase direct measurements.

## 11. Hard fails

- `INSTANCE_SECTION_COLLAPSED_TO_FAMILY_MEAN`
- `INSTANCE_SECTION_MAPPING_MISMATCH`
- `DUPLICATE_MASTER_PER_CORNER`
- `FALSE_GEOMETRY_VARIANT_FROM_REPLACEMENT_STATUS_ONLY`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `FIXED_MASTER_INSTALLATION_ANGLE`
- `FIXED_45_DEGREE_HISTORICAL_CLAIM`
- `SILENT_HISTORICIZATION`
- `PUBLISHED_MEAN_REINTERPRETED_AS_ALL_FOUR_ARITHMETIC_MEAN`
- `UNSUPPORTED_JOINERY_CLAIM`
- `RELATED_COMPONENT_IDENTITY_COLLAPSE`
- `MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`

Missing exact historical length/joinery/profile is **not** a hard fail under RC-023.

## 12. Locked production route

The next task is:
`T-033｜P3_3_ZIJIAOLIANG_MASTER_V2_V001`

Product Owner instruction “继续完成子角梁” authorizes continuation through engineering execution and closure subject to existing machine/human evidence gates. Stage2 and T-018 remain outside scope.
