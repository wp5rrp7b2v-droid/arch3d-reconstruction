# 中国古建筑3D复原｜T-039｜P3_3_LINGGONG_MASTER_V2_V001

Status: **TASK CONTRACT LOCKED / PRODUCT OWNER APPROVED / D-213 / ENGINEERING EXECUTION NOT AUTHORIZED**
Stage: P3.3 V002 Stage 1
Future branch: `codex/t039-p3-3-linggong-master-v2-v001`
Branch creation status: **NOT AUTHORIZED / NOT CREATED**

## 1. Objective

Build and validate one reusable 令栱 Stage1 Master covering:

- 令栱 physical Registry records: **28**
- distribution: South 7 / North 7 / East 7 / West 7
- one shared Master family
- zero Geometry Variant

The task produces one Stage1 component-family Master only.

It does not authorize:
- whole dougong assembly;
- 28-instance building placement;
- Stage2;
- T-018 restart.

## 2. Identity Contract

Component id:

`CMP-GONG-LINGGONG-001`

Master id:

`CMP-GONG-LINGGONG-001_MASTER`

Master version:

`V001`

Task id:

`T-039｜P3_3_LINGGONG_MASTER_V2_V001`

Locked architecture:

**ONE SHARED MASTER / ZERO GEOMETRY VARIANT / 28 INSTANCE BINDINGS**

Required:
- all 28 Registry rows retain their location/direction identities;
- one Master identity is reused;
- location/direction is instance/assembly metadata;
- no location-specific duplicate Master.

## 3. Source Authority

Primary source:

`SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF SHA-256:

`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Locked lineage:
- D-210: Source Readiness + D-076 = PASS WITH BOUNDARIES
- D-212: Master Spec V0.1 = PRODUCT OWNER APPROVED / LOCKED
- D-213: this Task Contract = PRODUCT OWNER APPROVED / LOCKED

No secondary or generic template may override same-building evidence boundaries.

## 4. Dimension Contract

Canonical family observed-mean reference specimen:

- Length = **897.0 mm**
  - evidence = `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
  - observed range = 860–925.6 mm

- Width = **217.4 mm**
  - evidence = `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
  - observed range = 208–228 mm

- Thickness = **155.6 mm**
  - evidence = `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
  - observed range = 150–165 mm

Mandatory semantic protection:
- 897 / 217.4 / 155.6 are family observed means;
- they are not 28 per-instance exact values;
- they are not proven 963 original-design dimensions;
- observed min/max ranges may not be used to fabricate undocumented location-specific dimensions.

Sample count and Registry physical count are both 28, but:

`SAMPLE_TO_INSTANCE_MAPPING = UNKNOWN`

Therefore:
- no one-to-one source sample assignment may be invented;
- no Registry row may be assigned a specific source measurement without explicit evidence.

## 5. Profile Control Contract

Current profile status:
- same-building form/context evidence = sufficient for bounded Stage1 reconstruction;
- exact historical standalone profile = `UNRESOLVED`;
- exact historical control-point dimensions = `UNRESOLVED`;
- exact end shaping = `UNRESOLVED`;
- metric image calibration = `NOT PERFORMED / NOT CLAIMED`;
- numeric Stage1 Profile Control Set = **NOT YET LOCKED**.

### Mandatory pre-execution gate

Before engineering execution can be authorized, T-039 must complete a separate:

`PROFILE_CONTROL_SET_V0.1`

The gate must provide at minimum:

1. explicit numeric normalized control points;
2. deterministic coordinate meaning;
3. same-building source references;
4. visual comparison against the approved same-building form envelope;
5. explicit classification:
   `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
6. explicit statement that metric source-image calibration is not claimed unless actually performed;
7. deterministic signature / hash of the control set;
8. Product Owner approval.

Until this gate passes:
- no canonical Blender body may be generated;
- no builder may freeze a profile;
- no engineering execution may be authorized.

Explicitly forbidden:
- copying T-037 瓜子栱 control points;
- copying T-038 慢栱 control points;
- averaging/morphing T-037 and T-038 control sets;
- generic Song / Yingzao Fashi template substitution;
- aesthetic free-form profile invention;
- describing reconstructed points as direct measurements.

## 6. Variant Contract

Geometry Variant count is locked at:

**0**

Required:
- one canonical body rule;
- direction/location handled outside the Master geometry;
- world rotation/placement handled by assembly.

Forbidden:
- SOUTH/NORTH/EAST/WEST geometry variants;
- location-specific geometry variants;
- 28 per-instance Masters;
- false variants created from observed measurement spread;
- hidden direction-dependent scale or deformation.

Any future variant proposal requires new evidence and a formal specification change before implementation.

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

## 8. Geometry Construction Contract

After Profile Control Set approval, Stage1 geometry must:

- use the locked 897 × 217.4 × 155.6 mm family envelope;
- build one deterministic profile-driven body;
- preserve canonical width during extrusion;
- contain exactly one canonical 令栱 body in the First Article;
- remain independent from world/building placement;
- avoid global scale reuse from another gong family.

The geometry may not silently reuse the T-037 or T-038 mesh, profile polygon, or Blender object as authority.

## 9. First Article Contract

First Article contains exactly:

**1 canonical 令栱 Master body**

No 28-instance placement or bracket-set assembly is allowed before Product Owner First Article approval.

The First Article must exclude unsupported:
- grooves;
- sockets;
- mortises;
- tenons;
- slots;
- cavities;
- hidden local cuts;
- invented end shoulders/notches;
- wear;
- damage;
- warp;
- per-instance deformation.

## 10. Required Review Evidence

Minimum Review Board domains:

1. `AXON`
2. `FRONT_PROFILE`
3. `END_WIDTH_VIEW`
4. `DIMENSION_PROOF`
5. `28_INSTANCE_DISTRIBUTION_AND_ZERO_VARIANT_RULE`
6. `PROFILE_PROVENANCE_AND_CONTROL_SET_CLASSIFICATION`
7. `SOURCE_VS_RECONSTRUCTION_BOUNDARY`
8. `UNKNOWN_DEFERRED_GEOMETRY`

The Review Board must be human-readable and make visible:
- 897 / 217.4 / 155.6;
- 28 Registry rows;
- one Master / zero Variant;
- family observed-mean semantics;
- sample-to-instance mapping UNKNOWN;
- profile-control classification;
- unresolved/deferred detail;
- absence of unsupported joinery.

Blank or near-uniform review renders must fail.

## 11. Validation Contract

Machine validation must verify at minimum:

- Registry schema = V008
- Registry total = 505
- target 令栱 records = 28
- direction distribution = 7 / 7 / 7 / 7
- Master family count = 1
- Geometry Variant count = 0
- canonical length = 897.0 mm
- canonical width = 217.4 mm
- canonical thickness = 155.6 mm
- L/W/T semantics = DIRECT_PRIMARY / OBSERVED_MEAN / n=28
- per-instance exact claim = false
- original-963 fact claim = false
- sample-to-instance mapping = UNKNOWN
- approved Profile Control Set id/version/signature present
- profile classification remains SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT
- T-037/T-038 profile-control reuse = false
- generic-template substitution = false
- unsupported joinery/local cuts absent
- one canonical body only
- closed manifold mesh
- deterministic rebuild
- independent reopen
- deterministic geometry signature
- canonical binary SHA-256
- no tracked .blend in Git
- Blender version locked by workflow
- Review Board nonblank / variance check

## 12. Hard Fails

Implementation / validator must fail closed on at least:

- `LINGGONG_RECORD_COUNT_NOT_28`
- `DIRECTION_DISTRIBUTION_NOT_7_7_7_7`
- `MASTER_FAMILY_COUNT_NOT_1`
- `GEOMETRY_VARIANT_COUNT_NOT_0`
- `CANONICAL_LENGTH_NOT_897`
- `CANONICAL_WIDTH_NOT_217_4`
- `CANONICAL_THICKNESS_NOT_155_6`
- `OBSERVED_MEAN_MARKED_PER_INSTANCE_EXACT`
- `OBSERVED_MEAN_MARKED_ORIGINAL_963_DESIGN`
- `SAMPLE_TO_INSTANCE_MAPPING_INVENTED`
- `DUPLICATE_MASTER_PER_LOCATION`
- `FALSE_DIRECTION_GEOMETRY_VARIANT`
- `PROFILE_CONTROL_SET_NOT_PO_APPROVED`
- `PROFILE_CONTROL_SET_NOT_VERSIONED`
- `PROFILE_CONTROL_SIGNATURE_MISSING`
- `PROFILE_SOURCE_NOT_RECORDED`
- `PROFILE_DERIVATION_NOT_REPRODUCIBLE`
- `PROFILE_MARKED_DIRECT_MEASUREMENT`
- `GUAZI_PROFILE_CONTROL_REUSE`
- `MANGONG_PROFILE_CONTROL_REUSE`
- `PRIOR_GONG_GEOMETRY_REUSE_AS_AUTHORITY`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `UNSUPPORTED_PROFILE_INVENTION`
- `UNSUPPORTED_END_SHAPE`
- `UNSUPPORTED_JOINERY_OR_LOCAL_CUTS`
- `BUILDING_PLACEMENT_BAKED_INTO_MASTER`
- `MULTIPLE_CANONICAL_BODIES`
- `REVIEW_RENDER_NEAR_UNIFORM`
- `SILENT_HISTORICIZATION`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 13. Deferred / Unsupported Geometry

Remain explicitly unresolved or deferred:

- exact historical standalone profile curve;
- exact mortise-tenon geometry;
- grooves;
- slots;
- cavities;
- hidden local connection cuts;
- exact end notches / shoulders;
- unmeasured chamfers;
- wear / damage / warp;
- per-instance deformation;
- per-instance originality / repair state;
- one-to-one source sample mapping.

Assembly convenience is not evidence.

## 14. Scope Protection

T-039 must not:

- reactivate T-018 or its held route;
- start Stage2;
- modify T-020 datum authority;
- modify approved T-037瓜子栱 or T-038慢栱 geometry;
- reuse T-037/T-038 profile controls as 令栱 authority;
- broaden into complete bracket-set assembly;
- bind Catalog/V008 before Product Owner First Article approval and formalization authorization;
- merge under D-194 before post-formalization readiness review PASS plus explicit Product Owner Ready+Merge approval.

## 15. Gate Sequence

Locked sequence:

1. Source Readiness + D-076 — **PASS / D-210**
2. Master Spec V0.1 — **LOCKED / D-212**
3. Task Contract — **LOCKED / D-213**
4. Profile Control Set V0.1 — **NEXT GATE / NOT YET PREPARED**
5. Engineering Execution Authorization — **NOT AUTHORIZED**
6. First Article machine validation — **NOT STARTED**
7. Product Owner First Article Approval — **NOT AUTHORIZED**
8. Formalization + Catalog/V008/CURRENT binding — **NOT AUTHORIZED**
9. Derived Excel + latest-head regression + readiness review — **NOT AUTHORIZED**
10. D-194 combined Draft→Ready + Merge — **NOT AUTHORIZED**
11. Formal Closure — **NOT AUTHORIZED**

## 16. Current Authorization Boundary

D-213 authorizes and locks this Task Contract only.

D-213 does **not** authorize:

- Profile Control Set adoption;
- builder implementation;
- production branch creation;
- GitHub Actions workflow execution;
- Blender generation;
- Draft PR creation;
- First Article acceptance;
- formalization;
- Catalog/V008/CURRENT binding;
- Derived Excel synchronization;
- PR Ready / merge;
- closure;
- Stage2;
- T-018 resume.

Next complete step:

**prepare 令栱 PROFILE_CONTROL_SET_V0.1 Candidate 01 for Product Owner review.**

## 17. Profile Control Set Candidate 01｜D-214

D-214 records preparation of `LINGGONG_PROFILE_CONTROL_SET_V001_C01` for Product Owner review. Candidate 01 is an independent 14-point normalized same-building-source-guided profile control set with signature `0a3081110d36fea812739a942eca1522a510810f5ea52ee3b4c9ebaa51c1c1a7`. It does not reuse, scale, average or morph the T-037瓜子栱 13-point or T-038慢栱 18-point control polygons. Classification remains SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT. Metric source-image calibration is NOT PERFORMED / NOT CLAIMED. Candidate remains NOT LOCKED; engineering execution remains blocked pending Product Owner approval.
