# P3.3 Stage1｜慢栱族 Master Spec V0.1

Status: **DRAFT / PRODUCT OWNER REVIEW REQUIRED / D-197**
Date: 2026-09-27
Stage: P3.3 V002 Stage 1
Task: T-038｜P3_3_MANGONG_MASTER_V2_V001

## 1. Scope

One shared Master family is proposed to cover:
- 大型慢栱: 16
- 小型慢栱: 28
- total Registry records: 44

Proposed architecture:
- one reusable Master family: `CMP-GONG-MANGONG-001`
- one Master: `CMP-GONG-MANGONG-001_MASTER`
- two geometry variants:
  - `LARGE_MANGONG`
  - `SMALL_MANGONG`
- no per-location Master duplication

This family structure follows Coverage Matrix priority 16 and V008's shared-parametric-family disposition.

## 2. Primary source and evidence bindings

Primary source:
`SRC-ZG-WF-001`｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》

Canonical PDF SHA-256:
`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Direct slow-gong length evidence:
- PDF p60 / printed p45 / §2.2.2.2 慢栱:
  - 大型慢栱 observed mean length = **1641 mm**, n=16
  - 小型慢栱 observed mean length = **1607 mm**, n=28

Visual/form evidence:
- PDF p73–76: same-building outer-eaves bracket-set photographs, sectional/measured drawings and CAD/assembly relationships.
- These support slow-gong orientation, bracket-set context, horizontal-arm form language and broad envelope.
- They do not directly provide a complete standalone metric slow-gong profile curve or local joinery specification.

## 3. Dimension policy

### LARGE_MANGONG

- length = **1641.0 mm**
  - classification: `DIRECT_PRIMARY / OBSERVED_MEAN`
  - sample count: `n=16`
  - variant-specific direct measurement statistic: YES

- width = **218.9 mm**
  - classification: `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`
  - slow-gong-specific raw observed mean verified: NO
  - per-instance direct claim: NO

- thickness = **156.9 mm**
  - classification: `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`
  - slow-gong-specific raw observed mean verified: NO
  - per-instance direct claim: NO

### SMALL_MANGONG

- length = **1607.0 mm**
  - classification: `DIRECT_PRIMARY / OBSERVED_MEAN`
  - sample count: `n=28`
  - variant-specific direct measurement statistic: YES

- width = **218.9 mm**
  - classification: `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`
  - slow-gong-specific raw observed mean verified: NO
  - per-instance direct claim: NO

- thickness = **156.9 mm**
  - classification: `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`
  - slow-gong-specific raw observed mean verified: NO
  - per-instance direct claim: NO

### Required semantic boundary

- 1641 / 1607 are observed means, not 44 per-instance exact lengths.
- 218.9 / 156.9 are not to be relabeled as slow-gong-specific direct observations.
- 218.9 / 156.9 are Stage1 family design candidates carried from report synthesis / V008 and must remain replaceable.
- No value above is automatically a proven 963 original-design dimension.

## 4. Profile / form authority

Proposed:
`PROFILE_AUTHORITY = SAME_BUILDING_SOURCE_GUIDED_SIMPLIFIED / PROVISIONAL`

Current evidence supports a bounded Stage1 form strategy but does **not** support a metrically recovered historical profile.

Locked draft boundary:
- same-building PDF p73–76 is the only allowed visual/form basis for Stage1 slow-gong profile work;
- exact historical standalone profile curve = `UNRESOLVED`;
- exact historical profile control-point dimensions = `UNRESOLVED`;
- no generic Song-dynasty template may silently replace same-building evidence;
- no control points may be described as direct measurements unless an explicit source table / calibrated extraction establishes them;
- any future normalized profile control set must be:
  - deterministic,
  - versioned,
  - visibly reviewable,
  - explicitly `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE`,
  - reproducible from its locked numeric Definition,
  - not represented as metrically re-extracted from the report unless that calibration is actually performed.

**V0.1 does not yet lock a numeric profile control set.**
That control set must be designed and visually reviewed before engineering execution.

## 5. Variant rule

Allowed sharing:
- family topology
- coordinate convention
- profile derivation method
- builder / validator logic
- evidence schema
- width/thickness Stage1 candidate values

Variant discriminator:
- LARGE length = 1641 mm
- SMALL length = 1607 mm

Forbidden:
- `SMALL = uniform_scale(LARGE, 1607/1641)`
- scaling width or thickness by the length ratio
- creating location-specific geometry variants without evidence
- inventing a distinct LARGE/SMALL profile shape without evidence
- upgrading width/thickness candidate values to direct-measurement facts

## 6. Coordinate / geometry convention

For a future T-038 Definition:
- X = member length axis
- Y = member width / extrusion axis
- Z = profile thickness / vertical axis
- geometry origin = deterministic family-local origin
- LARGE and SMALL must be generated independently from the same family rule with their own locked length input

No building placement transform is part of the Master geometry itself.

## 7. Unsupported / deferred detail

Explicitly deferred:
- exact mortise-tenon geometry
- grooves
- hidden slots / cavities
- local connection cuts
- exact historical profile curve
- wear / damage / warp
- per-instance deformation
- unmeasured chamfers or decorative cleanup
- per-instance 963 originality

These must not be added merely to make assembly visually convenient.

## 8. Required first-article evidence package

Before any Product Owner first-article approval, T-038 must provide at minimum:

1. LARGE axonometric render
2. SMALL axonometric render
3. LARGE front/profile render
4. SMALL front/profile render
5. LARGE vs SMALL overlay / dimensional comparison
6. dimension proof for L/W/T and variant counts
7. profile provenance / control-set classification panel
8. evidence-boundary / unknown-deferred panel

The review package must make it visually possible to detect:
- wrong family proportions,
- unintended uniform scaling,
- unsupported profile invention,
- width/thickness evidence overclaim,
- local detail invention,
- render failure / near-uniform blank output.

## 9. Proposed hard fails for Task Contract

A future T-038 Task Contract should hard-fail at least:

- `WRONG_LARGE_COUNT`
- `WRONG_SMALL_COUNT`
- `WRONG_LARGE_LENGTH`
- `WRONG_SMALL_LENGTH`
- `WIDTH_THICKNESS_EVIDENCE_OVERCLAIM`
- `PER_INSTANCE_EXACT_CLAIM`
- `ORIGINAL_963_FACT_UPGRADE`
- `SMALL_UNIFORM_SCALED_FROM_LARGE`
- `UNSUPPORTED_PROFILE_INVENTION`
- `PROFILE_CONTROL_SET_NOT_VERSIONED`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `UNSUPPORTED_JOINERY_OR_LOCAL_CUTS`
- `REVIEW_RENDER_NEAR_UNIFORM`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 10. Gate lineage

- D-195: T-038 start / Source Readiness authorized
- D-196: Source Readiness + D-076 PASS WITH BOUNDARIES
- D-197: Master Spec V0.1 DRAFT prepared / Product Owner review required

Current gate:
- Master Spec V0.1 = **DRAFT / NOT LOCKED**
- Task Contract = **NOT AUTHORIZED**
- engineering execution = **NOT AUTHORIZED**
- Blender generation = **NOT AUTHORIZED**
- formalization = **NOT AUTHORIZED**
- Catalog/V008 binding = **NOT AUTHORIZED**
- PR creation / merge = **NOT AUTHORIZED**
- Stage2 = **NOT AUTHORIZED**
- T-018 = **HOLD**
