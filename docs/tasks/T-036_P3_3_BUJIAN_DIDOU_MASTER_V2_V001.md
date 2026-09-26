# 【中国古建筑3D复原｜T-036｜P3_3_BUJIAN_DIDOU_MASTER_V2_V001｜补间铺作底斗 Master】

Status: **TASK CONTRACT LOCKED / D-167 / ENGINEERING EXECUTION NOT AUTHORIZED**  
Think Level: HIGH  
Architecture: **MASTER V2 / MINIMAL_SUFFICIENT / EVIDENCE-BOUNDED CURVED PROFILE / SINGLE-PARAMETER PROFILE / EXPLICIT DEPTH COMPLETION / CONNECTION-AWARE**  
Stage: P3.3 V002 Stage 1  
Proposed branch: codex/t036-p3-3-bujian-didou-master-v2-v001

## 1. Objective

Build and validate one reusable canonical Master for:
- component id: CMP-DOU-BOTTOM-LONGKAI-001
- master id: CMP-DOU-BOTTOM-LONGKAI-001_MASTER
- version: V001
- physical instances: 12
- measured instances: 9
- geometry variants: 0

Core objective:
preserve the A1-measured bottom-dou envelope, produce a stable curved Stage1 body without pretending the exact historical curvature is known, explicitly separate reconstructed depth from direct evidence, and prove that all 12 registry instances remain one Master family.

T-036 does not restore exact斗耳、槽口、空腔、底部榫卯、磨损形变或963原始曲线。

## 2. Authoritative Inputs

Primary:
SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》
- PDF p65–66 / printed p50–51
- §2.2.3.2
- Table 2-28 / 2-29
- canonical SHA-256 94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472

Supporting project evidence:
- docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md
- docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md
- production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json
- docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json

Locked Spec:
- docs/production/zhenguo_wanfo/P3_3_STAGE1_BUJIAN_DIDOU_MASTER_SPEC_V001.md
- production/zhenguo_wanfo/registry/P3_3_STAGE1_BUJIAN_DIDOU_MASTER_SPEC_V001.json

Decision chain:
D-099 / RC-019 → D-108 / RC-020 → D-137 / RC-023 → D-139 / RC-024 → D-164 Source Readiness → D-165 D-076 → D-166 Master Spec → D-167 Task Contract.

## 3. Locked Registry / Identity Contract

V008/CURRENT physical instances = 12:
- 南立面：西次间 / 明间 / 东次间
- 北立面：西次间 / 明间 / 东次间
- 东山：北次间 / 明间 / 南次间
- 西山：北次间 / 明间 / 南次间

Locked:
- one component identity
- one Master
- zero Geometry Variant
- north / south / east / west placement does not create a Variant
- measured vs unmeasured status does not create a Variant

Existing P3.1 component identity CMP-DOU-BOTTOM-LONGKAI-001 must be reused. No duplicate BUJIAN-only component id may be introduced.

## 4. Direct A1 Dimension Contract

A1 bottom-dou observed family means from 9 measured instances:
- top_width_mm = 255.56
- bottom_width_mm = 178.56
- total_height_mm = 161.78
- flat_height_mm = 38.333
- qi_height_mm = 65.6

Mandatory semantics:
- DIRECT_PRIMARY / OBSERVED_AS_MEASURED_FAMILY_MEAN
- measured sample count = 9
- physical instance count = 12
- north-facade 3 bottom-dou dimensions = UNMEASURED
- values are not 12 per-instance direct measurements
- values are not proven 963 design dimensions

The validator must reject any representation that silently promotes these means to exact 963 design values or per-instance direct values.

## 5. Flat / Qi Height Boundary

flat_height_mm and qi_height_mm are direct source data and must be preserved.

However:
- they do not sum to total height;
- A1 does not close every remaining vertical segment boundary;
- therefore V001 must not invent additional named stages, ears, steps or cavities merely to force a complete segmented profile.

Locked use:
- evidence metadata
- review annotation
- profile plausibility boundary

Forbidden:
- direct conversion into unsupported extra Z breakpoints
- invented ear height = total - flat - qi
- invented cavity/slot geometry from the residual height

## 6. Depth Evidence / Production Completion Contract

A1 bottom-dou:
- top_depth_mm = UNKNOWN
- bottom_depth_mm = UNKNOWN

D-166 allows buildability references:
- production_top_depth_mm = 240.0
- production_bottom_depth_mm = 165.1

Mandatory classification:
PARAMETRIC_COMPLETION / RECONSTRUCTED_DESIGN / REPLACEABLE / NOT_A1_DIRECT / HISTORICAL_CLAIM_FALSE.

Source trail:
P1_2_CORE_EVIDENCE_BATCH_02 / E-022 secondary report-derived organization.

Hard rule:
the Definition and Semantic outputs must keep separate fields for A1 historical/evidence depth UNKNOWN and production depth completion values. One may never overwrite the other.

## 7. Geometry Mode

geometry_mode = EVIDENCE_BOUNDED_CURVED_QI_PROFILE_WITH_RECONSTRUCTED_DEPTH

Canonical envelope:
- bottom centered footprint = 178.56 × 165.1 mm
- top centered footprint = 255.56 × 240.0 mm
- total height = 161.78 mm

Axes:
- +X width
- +Y depth
- +Z height
- origin = bottom footprint center
- Location 0/0/0
- Rotation 0/0/0
- Scale 1/1/1

Profile rule:
- one smooth monotonic interpolation from bottom footprint to top footprint;
- one normalized curve_amount production parameter only;
- exact curve = RECONSTRUCTED_DESIGN / REPLACEABLE;
- curve_amount is not evidence and must never be presented as historical;
- no overshoot beyond top/bottom bounded envelope;
- no inward reversal;
- no self-intersection;
- closed manifold body.

Do not introduce multiple tangent controls, radii, spline families or a new global RC rule in T-036.

## 8. Curve Mutation / Stability Proof

The engineering Definition must establish one deterministic default curve_amount.

Validation must also test at least two legal non-default curve_amount values around the default.

Required result:
- all variants build successfully;
- top/bottom dimensions remain exact;
- total height remains exact;
- mesh remains manifold;
- no self-intersection;
- Master identity remains unchanged;
- geometry variant count remains 0;
- mutation outputs are ENGINEERING_TEST_ONLY and never enter Registry.

This proves the curve mechanism is stable without turning curve_amount into a historical claim.

## 9. Existing Dou Pipeline Reuse

Reuse before rebuilding:
production/zhenguo_wanfo/scripts/dou_master_common_v001.py

Existing legacy dou users include:
- CMP-LUDOU-COLUMN-001
- CMP-DOU-SINGLE-LONGKAI-001
- CMP-DOU-INTERACTIVE-001

Current shared builder is linear-envelope based. If T-036 execution requires a curved profile, the preferred path is a minimal backward-compatible, Definition-driven extension:
- legacy records with no curved profile declaration retain the existing linear geometry path unchanged;
- T-036 explicitly requests CURVED_QI_PROFILE;
- no second T-036-only geometry framework unless the shared extension is demonstrably unsafe.

If shared dou infrastructure changes, mandatory regressions:
- CMP-LUDOU-COLUMN-001 PASS
- CMP-DOU-SINGLE-LONGKAI-001 PASS
- CMP-DOU-INTERACTIVE-001 PASS
- their locked dimensions / evidence semantics / semantic geometry signatures must not regress.

If a clean backward-compatible extension cannot be achieved within scope, execution must STOP and report the blocker rather than broaden architecture.

T-036 must not modify the general P3.3 frame Master V2 infrastructure unless separately justified and authorized.

## 10. Unsupported Detail Contract

Canonical V001 body must not contain:
- inferred斗耳
- name-driven openings
- long-kai slot guessed from naming
- top cavity
- bottom cavity
- mortise / tenon
- hidden connector geometry
- damage / wear / compression deformation
- per-instance asymmetry

Unsupported detail count must remain zero.

## 11. Connection Layer｜RC-024

Stage1 semantic interfaces:
1. BOTTOM_SUPPORT_INTERFACE
   - related context = 补间铺作底部泥道 / supporting layer
   - support relationship = KNOWN
   - exact joint geometry = DEFERRED

2. TOP_BEARING_INTERFACE
   - role = support / receive upper bracket-stack member
   - exact counterpart identity / connection kind = UNRESOLVED where not directly locked
   - exact cavity / tenon / penetration = DEFERRED

Connection semantics do not authorize invented mesh cuts.

## 12. Required Review Board

Formal Review Board:
CMP-DOU-BOTTOM-LONGKAI-001_MASTER_REVIEW_BOARD_V001.png

Required six panels:
1. AXON
2. FRONT_PROFILE
3. SIDE_PROFILE_AND_DEPTH_BOUNDARY
4. TOP_BOTTOM_FOOTPRINTS
5. EVIDENCE_VS_COMPLETION
6. PROFILE_STABILITY

Mandatory visible statements:
- 12 physical / 9 measured / 3 north unmeasured
- 255.56 / 178.56 / 161.78 = A1 observed family means
- 38.333 / 65.6 retained as direct profile evidence
- A1 top/bottom depth = UNKNOWN
- 240.0 / 165.1 = reconstructed production completion only
- CURVED_QI_PROFILE
- exact curvature = UNKNOWN
- curve_amount = engineering reconstruction
- one Master / zero Variant
- unsupported ears / slots / joinery not modeled

## 13. Minimal-Sufficient Formal Package

After separate execution authorization, expected outputs:
1. CMP-DOU-BOTTOM-LONGKAI-001_MASTER_DEFINITION_V001.json
2. CMP-DOU-BOTTOM-LONGKAI-001_MASTER_SEMANTIC_V001.json
3. CMP-DOU-BOTTOM-LONGKAI-001_MASTER_V001.blend — Actions Artifact + local-only / NOT GIT
4. CMP-DOU-BOTTOM-LONGKAI-001_MASTER_REVIEW_BOARD_V001.png
5. CMP-DOU-BOTTOM-LONGKAI-001_MASTER_VALIDATION_V001.json
6. T-036 lifecycle record

No per-location binaries. No duplicate evidence cache.

## 14. First-Article Validation Domains

At minimum validate:

Identity / Registry:
- component / master / version
- 12 physical instances
- 9 measured instances
- 12 location traceability
- one shared Master
- zero Geometry Variant
- no duplicate component id

Direct evidence:
- top width 255.56
- bottom width 178.56
- total height 161.78
- flat height 38.333
- qi height 65.6
- observed-family-mean semantics preserved
- north 3 unmeasured preserved
- no 963 exact-design claim

Depth dual layer:
- A1 top depth null / UNKNOWN
- A1 bottom depth null / UNKNOWN
- production top depth 240.0
- production bottom depth 165.1
- completion classification correct
- historical_claim false
- production values do not overwrite evidence fields

Profile:
- profile_class CURVED_QI_PROFILE
- exact_curvature UNKNOWN
- one curve parameter only
- default deterministic
- two non-default mutation tests PASS
- top/bottom dimensions invariant
- total height invariant
- monotonic profile
- no envelope overshoot
- no self-intersection
- manifold mesh
- no invented segment from residual height
- no simple Box / unsupported straight-only historical claim

Unsupported details:
- ears = absent
- slots/cavities = absent
- mortise/tenon = absent
- damage deformation = absent
- unsupported_detail_count = 0

Reproducibility:
- Blender 4.5.13 LTS
- independent reopen PASS
- deterministic semantic restore
- Definition↔Semantic identity PASS
- geometry signature recorded
- canonical .blend not tracked in Git

Shared regression:
- three legacy dou Masters PASS if shared dou infrastructure changes

Exact atomic count may exceed this list; no domain may be dropped solely to reduce count.

## 15. Hard Fails

- BOTTOM_DOU_DUPLICATE_COMPONENT_ID
- PHYSICAL_COUNT_NOT_12
- MEASURED_COUNT_NOT_9
- FAMILY_MEAN_MARKED_AS_12_DIRECT_INSTANCE_VALUES
- OBSERVED_MEAN_MARKED_AS_963_DESIGN
- A1_DEPTH_FALSELY_MARKED_DIRECT
- PARAMETRIC_DEPTH_MARKED_HISTORICAL
- DEPTH_EVIDENCE_AND_COMPLETION_FIELDS_COLLAPSED
- PROFILE_CLASS_LOST
- EXACT_CURVATURE_FALSELY_CLAIMED
- CURVE_PARAMETER_MARKED_AS_HISTORICAL
- MULTI_PARAMETER_CURVE_COMPLEXITY_CREEP
- FLAT_QI_HEIGHT_USED_TO_INVENT_UNSUPPORTED_SEGMENTS
- CURVE_OVERSHOOT
- CURVE_REVERSAL_OR_SELF_INTERSECTION
- NON_MANIFOLD_BODY
- UNSUPPORTED_DOU_EARS_OR_SLOT
- NAME_DRIVEN_LONG_KAI_SLOT
- UNSUPPORTED_JOINERY_CLAIM
- DUPLICATE_MASTER_PER_LOCATION
- FALSE_GEOMETRY_VARIANT_FROM_LOCATION
- LEGACY_DOU_SHARED_REGRESSION_FAILURE
- SILENT_HISTORICIZATION
- MODEL_BEFORE_EXECUTION_AUTHORIZATION

Missing exact historical curvature, depth, ears or joinery is explicitly NOT a Stage1 Hard Fail when retained as UNKNOWN and production completion is explicit.

## 16. Protected Boundaries

T-036 must not:
- reactivate T-018 / PR #3 / PR #6
- start Stage2
- reopen P2
- alter T-020 / RZ / FV authority
- rewrite A1 source facts
- convert E-022 depth completion into A1 direct evidence
- create a new global curve rule unless later separately approved
- create location-specific Masters
- modify approved legacy dou geometry semantics
- broaden into full bracket-set assembly

T-018 remains HOLD.

## 17. Authorization Boundary｜D-167

Product Owner instruction “设计并锁定 T-036 Task Contract” authorizes this contract design and lock only.

Locked:
- TASK_CONTRACT_LOCKED = true
- ENGINEERING_EXECUTION_AUTHORIZED = false
- BLENDER_EXECUTION_AUTHORIZED = false
- PRODUCTION_BRANCH_CREATION_AUTHORIZED = false
- PR_CREATION_AUTHORIZED = false

No production branch or PR is created by D-167.

To begin engineering, Product Owner must separately authorize:

**开始 T-036 工程执行**

Only then may:
- branch codex/t036-p3-3-bujian-didou-master-v2-v001 be created;
- Draft PR be opened;
- Definition be finalized;
- GitHub Actions / Blender 4.5.13 run;
- the minimal backward-compatible shared dou profile extension be implemented if needed;
- first-article evidence be generated.

First-article acceptance, formalization, Catalog/V008 binding, PR merge, Stage2 and T-018 resume remain separate authorization boundaries.
