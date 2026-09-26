# P3.3 V002 Stage 1｜补间铺作底斗 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-166**  
**日期：2026-09-26**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019**  
**复原方法：D-108 / RC-020**  
**历史缺口规则：D-137 / RC-023**  
**连接层：D-139 / RC-024**  
**Source Readiness：D-164 PASS WITH EXPLICIT GEOMETRY UNKNOWN**  
**视觉门：D-165 / D-076 PASS WITH EXPLICIT PROFILE / DEPTH BOUNDARY**

## 1. Component Identity

- 中文名：补间铺作底斗
- existing component id：CMP-DOU-BOTTOM-LONGKAI-001
- master id：CMP-DOU-BOTTOM-LONGKAI-001_MASTER
- master version：V001
- physical instances：12
- measured instances：9
- master family count：1
- geometry variant count：0

沿用 P3.1 已建立的 CMP-DOU-BOTTOM-LONGKAI-001 身份，不另建重复 component id。

## 2. Direct A1 Geometry

A1 = SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》

Direct locators:
- §2.2.3.2 长开斗
- PDF p65–66 / printed p50–51
- Table 2-28 / 2-29
- 附件测量表支持 12 个补间铺作位置
- canonical PDF SHA-256 = 94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472

Observed family means from 9 measurable bottom-dou samples:
- top / total width = 255.56 mm
- bottom width = 178.56 mm
- total height = 161.78 mm
- flat height = 38.333 mm
- qi / sloped height = 65.6 mm

Mandatory semantics:
- OBSERVED_AS_MEASURED_FAMILY_MEAN
- NOT 12 individual measurements
- NOT proven 963 original design dimensions

North-facade 3 physical instances exist but were not included in these bottom-dou measurements.

## 3. Profile Boundary

Locked:
- profile_class = CURVED_QI_PROFILE
- exact_curvature = UNKNOWN
- profile_source = RECONSTRUCTED_DESIGN / REPLACEABLE
- symmetry = LEFT_RIGHT_SYMMETRIC for Stage1 canonical body
- one curve-control parameter only

V001 must not be:
- a rectangular Box;
- a pure straight-sided trapezoid claimed as the historical form;
- a multi-segment invented profile derived from terminology alone.

Important:
flat_height_mm = 38.333 and qi_height_mm = 65.6 are direct measured profile evidence, but the source does not fully close all vertical segment boundaries. In V001 they are retained as direct evidence metadata and review constraints; they must not by themselves be converted into invented extra breakpoints, ears, steps or cavities.

## 4. Depth Completion

A1 bottom-dou total depth / lower depth = UNKNOWN.

For buildability only, D-166 permits:
- production top depth reference ≈ 240.0 mm
- production bottom depth reference ≈ 165.1 mm

Classification is mandatory:
- PARAMETRIC_COMPLETION
- RECONSTRUCTED_DESIGN
- REPLACEABLE
- NOT_A1_DIRECT
- HISTORICAL_CLAIM_FALSE

These values may not overwrite the A1 unknown fields.

## 5. Canonical Stage1 Geometry

Canonical envelope:
- top width 255.56 mm
- bottom width 178.56 mm
- total height 161.78 mm
- production top depth 240.0 mm
- production bottom depth 165.1 mm

Coordinate convention:
- +X = width
- +Y = depth
- +Z = gravity-up height
- origin = bottom footprint center
- transform = Location 0/0/0, Rotation 0/0/0, Scale 1/1/1

Geometry method:
- centered bottom footprint
- centered top footprint
- one smooth monotonic vertical interpolation profile
- same single normalized curve-control drives the bounded width/depth transition
- top and bottom footprints remain exact
- no overshoot outside the locked envelope
- no self-intersection

Exact curve value is engineering reconstruction, not historical evidence.

## 6. Deferred / Unsupported Geometry

V001 excludes:
- exact斗耳 profile / height / thickness
- exact top slots / cavities
- exact bottom mortise-tenon
- concealed joinery
- wear / cracking / compression deformation
- per-instance damage
- 963 exact profile
- position-based geometry variants

All remain UNKNOWN / UNRESOLVED / DEFERRED.

## 7. Connection Layer

Stage1 interfaces:
- BOTTOM_SUPPORT_INTERFACE：补间铺作底部泥道 / supporting layer
- TOP_BEARING_INTERFACE：upper bracket-stack bearing relationship

Connection existence / support role may be represented semantically.
Exact connection kind, penetration, mortise, tenon and cavity geometry remain DEFERRED.

## 8. Review / Validation Intent

Review must make visible:
- 12 physical / 9 measured / 3 north unmeasured
- direct width/height values
- A1 depth UNKNOWN
- 240.0 / 165.1 as reconstructed production completion only
- CURVED_QI_PROFILE
- exact curvature UNKNOWN
- curve parameter not historical
- flat / qi heights retained without invented segmentation
- 1 Master / 0 Variant
- unsupported ears / slots / joinery absent

## 9. Locked Decision｜D-166

Product Owner approved the V0.1 design and locks this V001.

Next authorized step:
design and lock T-036｜P3_3_BUJIAN_DIDOU_MASTER_V2_V001 Task Contract.

Not authorized by D-166:
- production branch
- PR
- GitHub Actions / Blender
- first-article production
- Catalog / V008 approved binding
- Stage2
- T-018 resume
