# 中国古建筑3D复原｜T-038｜P3_3_MANGONG_MASTER_V2_V001

Status: **ENGINEERING EXECUTION AUTHORIZED / D-202 / FIRST ARTICLE IN PROGRESS**
Stage: P3.3 V002 Stage 1
Branch: codex/t038-p3-3-mangong-master-v2-v001

## 1. Objective

Build and validate one reusable 慢栱 Master family covering:

- LARGE_MANGONG / 大型慢栱: 16 Registry records
- SMALL_MANGONG / 小型慢栱: 28 Registry records
- total: 44 Registry records

The task produces a Stage1 Master family only. It does not authorize a whole bracket-set assembly or any T-018 work.

## 2. Identity Contract

Family component id:
`CMP-GONG-MANGONG-001`

Master id:
`CMP-GONG-MANGONG-001_MASTER`

Master version:
`V001`

Registry source labels remain:
- 大型慢栱
- 小型慢栱

The family Master does not erase the two source component names and must not create per-location duplicate Masters.

## 3. Source Authority

Primary source:
`SRC-ZG-WF-001`｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》

Canonical PDF SHA-256:
`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Locked evidence lineage:
- D-196 Source Readiness + D-076 = PASS WITH BOUNDARIES
- D-198 Master Spec V0.1 = PRODUCT OWNER APPROVED / LOCKED

No secondary template may override the same-building source boundary.

## 4. Dimension Contract

### LARGE_MANGONG
- L = **1641.0 mm**
- evidence = `DIRECT_PRIMARY / OBSERVED_MEAN / n=16`
- W = **218.9 mm**
- evidence = `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`
- T = **156.9 mm**
- evidence = `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`

### SMALL_MANGONG
- L = **1607.0 mm**
- evidence = `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
- W = **218.9 mm**
- evidence = `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`
- T = **156.9 mm**
- evidence = `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`

Semantic protection:
- 1641 / 1607 are observed means, not 44 per-instance exact lengths.
- W/T are not slow-gong-specific raw observed means.
- W/T are not per-instance direct facts.
- no L/W/T value is automatically a proven 963 original-design dimension.
- W/T must remain replaceable in metadata and validation.

## 5. Profile Control Contract

Current profile status:
- same-building form/context evidence = sufficient for bounded Stage1 work
- exact historical standalone profile = `UNRESOLVED`
- exact historical control-point dimensions = `UNRESOLVED`
- numeric Stage1 control set = **NOT YET LOCKED**

### Mandatory pre-execution profile gate

Before engineering execution can be authorized, T-038 must complete a separate:

`PROFILE_CONTROL_SET_V0.1`

The profile gate must provide:
1. explicit numeric normalized control set;
2. deterministic coordinate meaning;
3. same-building source references;
4. visual overlay / side-by-side review against the report-supported form envelope;
5. explicit classification:
   `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
6. explicit statement that no metric source-image calibration is claimed unless actually performed;
7. Product Owner approval.

Until that gate passes:
- no Blender body may be generated;
- no builder implementation may freeze a profile;
- no engineering execution may be authorized.

Forbidden:
- generic Song-dynasty template substitution;
- aesthetic free-form profile design;
- copying the T-037瓜子栱 profile merely because both are 栱;
- silently reusing another component's control points;
- calling inferred control points “measured”.

## 6. Variant Contract

One family / two variants.

Required:
- LARGE and SMALL are generated independently from the same family rule;
- variant discriminator = length;
- shared W/T Stage1 candidates are applied explicitly as report-inferred family candidates;
- separate geometry/semantic signatures are required for LARGE and SMALL.

Forbidden:
- `SMALL = uniform_scale(LARGE,1607/1641)`;
- W/T scaling by length ratio;
- location-specific geometry variants without source evidence;
- distinct LARGE/SMALL profile shapes without evidence.

## 7. Coordinate Contract

Future locked Definition must use:
- +X = member length
- +Y = width / extrusion
- +Z = profile thickness / vertical
- deterministic family-local origin
- location = [0,0,0]
- rotation = [0,0,0]
- scale = [1,1,1]

Building placement transforms are outside the Master body.

## 8. First Article Contract

First Article contains exactly two canonical bodies:
- LARGE_MANGONG
- SMALL_MANGONG

No 44-instance placement/assembly before Product Owner first-article approval.

The first article must not include unsupported grooves, sockets, mortises, tenons, cavities, local connection cuts, wear or deformation.

## 9. Required Review Evidence

Minimum Review Board domains:

1. LARGE axonometric
2. SMALL axonometric
3. LARGE front/profile
4. SMALL front/profile
5. LARGE vs SMALL overlay / dimensional comparison
6. dimension + count proof
7. profile provenance / control-set classification
8. evidence / UNKNOWN / DEFERRED boundary

The Review Board must be human-readable and must hard-fail on blank or near-uniform geometry renders.

## 10. Validation Contract

Machine validation must verify at least:

- Registry schema = V008
- Registry total = 505
- target family records = 44
- LARGE count = 16
- SMALL count = 28
- one Master family
- exactly two geometry variants
- LARGE L = 1641
- SMALL L = 1607
- W = 218.9 with report-inferred/replaceable semantics
- T = 156.9 with report-inferred/replaceable semantics
- no per-instance direct W/T claim
- no original-963 fact upgrade
- approved profile control-set id/version/signature present
- profile semantics remain SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT
- no generic-template substitution
- no uniform global scale implementation
- separate LARGE/SMALL geometry signatures
- closed manifold mesh
- deterministic rebuild
- independent reopen
- canonical binary SHA
- no tracked .blend in Git
- Blender version locked by workflow
- Review Board nonblank/variance check

## 11. Hard Fails

The implementation/validator must fail closed on at least:

- `MANGONG_FAMILY_COUNT_NOT_44`
- `LARGE_COUNT_NOT_16`
- `SMALL_COUNT_NOT_28`
- `LARGE_LENGTH_NOT_1641`
- `SMALL_LENGTH_NOT_1607`
- `WIDTH_CANDIDATE_LOST`
- `THICKNESS_CANDIDATE_LOST`
- `WIDTH_MARKED_DIRECT_OBSERVATION`
- `THICKNESS_MARKED_DIRECT_OBSERVATION`
- `PER_INSTANCE_EXACT_CLAIM`
- `OBSERVED_MEAN_MARKED_ORIGINAL_963_DESIGN`
- `PROFILE_CONTROL_SET_NOT_PO_APPROVED`
- `PROFILE_CONTROL_SET_NOT_VERSIONED`
- `PROFILE_SOURCE_NOT_RECORDED`
- `PROFILE_DERIVATION_NOT_REPRODUCIBLE`
- `PROFILE_MARKED_DIRECT_MEASUREMENT`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `GUAZI_PROFILE_SILENT_REUSE`
- `SMALL_CREATED_BY_UNIFORM_SCALE`
- `WIDTH_THICKNESS_SCALED_BY_LENGTH_RATIO`
- `UNSUPPORTED_JOINERY_MODELED`
- `LOCATION_CREATES_FALSE_VARIANT`
- `DUPLICATE_MASTER_PER_INSTANCE`
- `REVIEW_RENDER_NEAR_UNIFORM`
- `SILENT_HISTORICIZATION`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 12. Deferred / Unsupported Geometry

Remain explicitly unresolved or deferred:
- exact historical standalone profile curve
- exact mortise-tenon geometry
- grooves
- hidden slots / cavities
- local connection cuts
- wear / damage / warp
- per-instance deformation
- unmeasured chamfers
- per-instance 963 originality

Assembly convenience is not evidence.

## 13. Scope Protection

T-038 must not:
- reactivate T-018 / PR #3 / PR #6;
- start Stage2;
- modify T-020 datum authority;
- modify approved T-037 guazi geometry;
- reuse T-037 profile controls as slow-gong authority;
- broaden into complete bracket-set assembly;
- formalize Catalog/V008 before Product Owner first-article approval;
- merge under D-194 until post-formalization readiness review has PASSed and Product Owner explicitly approves the combined Ready+Merge step.

## 14. Gate Sequence

Locked sequence:

1. Source Readiness + D-076 — **PASS / D-196**
2. Master Spec V0.1 — **LOCKED / D-198**
3. Task Contract — **LOCKED / D-199**
4. Profile Control Set V0.1 — **LOCKED / PRODUCT OWNER APPROVED / D-201**
5. Engineering Execution Authorization — **AUTHORIZED / D-202**
6. First Article — **IN PROGRESS**
7. Product Owner First Article Approval — **NOT AUTHORIZED**
8. Formalization + Catalog/V008 binding — **NOT AUTHORIZED**
9. Derived Excel + latest-head regression + readiness review — **NOT AUTHORIZED**
10. D-194 combined Ready+Merge — **NOT AUTHORIZED**
11. Closure — **NOT AUTHORIZED**

## 15. Current Authorization Boundary

D-199 authorizes and locks this Task Contract only.

D-199 does **not** authorize:
- numeric profile control-set adoption;
- builder implementation;
- Blender generation;
- workflow execution;
- Draft PR creation;
- first-article acceptance;
- formalization;
- Catalog/V008 binding;
- PR Ready/merge;
- closure;
- Stage2;
- T-018 resume.

## 16. Profile Control Set Candidate 01

D-200 records Product Owner authorization to enter the profile-control design/review gate. Candidate 01 is an independent 18-point same-building-source-guided Stage1 profile control set with signature `07d5d9172f25758f057c4bc0200fc35aa892a9a72ef15b40735fcc5c620e80c4`. It is not metrically traced, not a direct historical measurement, and does not reuse the T-037 guazi control polygon. Candidate 01 remains NOT LOCKED pending Product Owner visual review/approval; engineering execution remains blocked.


## 17. Profile Control Set Approval

D-201 records Product Owner approval of `MANGONG_PROFILE_CONTROL_SET_V001_C01`. The 18-point normalized control set is now locked in `production/zhenguo_wanfo/component_library/masters/CMP-GONG-MANGONG-001/CMP-GONG-MANGONG-001_MANGONG_DEFINITION_V001.json` with signature `07d5d9172f25758f057c4bc0200fc35aa892a9a72ef15b40735fcc5c620e80c4`. Classification remains SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT. This approval does not authorize builder implementation, Blender generation, workflow execution, Draft PR creation, first-article acceptance, formalization, Catalog/V008 binding, merge, Stage2 or T-018 resume.


## 18. Engineering Execution Authorization

D-202 authorizes T-038 isolated engineering execution: builder, validator and GitHub Actions workflow implementation; Blender 4.5.13 two-variant first article; deterministic rebuild/reopen validation; 8-domain Review Board generation; Draft PR creation. It does not authorize Product Owner first-article acceptance, formalization, Catalog/V008 binding, PR Ready/merge, closure, Stage2 or T-018 resume.
