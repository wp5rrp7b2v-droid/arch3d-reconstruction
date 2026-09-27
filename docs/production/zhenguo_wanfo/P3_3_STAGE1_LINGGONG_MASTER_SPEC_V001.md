# P3.3 Stage1｜令栱 Master Spec V0.1

Status: **LOCKED / PRODUCT OWNER APPROVED / D-212**
Date: 2026-09-27
Stage: P3.3 V002 Stage 1
Source Gate: D-210｜Source Readiness + D-076 PASS WITH BOUNDARIES

## 1. Scope

Target component:
- 中文名：令栱
- physical Registry records：**28**
- distribution：南7 / 北7 / 东7 / 西7
- Coverage Matrix priority：17
- Stage1 disposition：需新建Master

Proposed identity:
- component id：`CMP-GONG-LINGGONG-001`
- master id：`CMP-GONG-LINGGONG-001_MASTER`
- master version：V001
- master family count：**1**
- geometry variant count：**0**

Proposed architecture:

**ONE SHARED MASTER / ZERO GEOMETRY VARIANT / 28 INSTANCE BINDINGS**

Current evidence does not support:
- direction-specific Master duplication;
- location-specific Master duplication;
- north/south/east/west geometry variants;
- multiple length variants.

Direction and placement belong to the future assembly/instance layer, not the Stage1 Master body.

## 2. Authoritative Inputs

Primary authority:

`SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF SHA-256:

`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Direct evidence bindings:

### Width
- PDF p55 / printed p40
- §2.2.1.5 栱广
- Table 2-14
- observed mean = **217.4 mm**
- minimum = 208 mm
- maximum = 228 mm
- n = 28
- classification = `DIRECT_PRIMARY / OBSERVED_MEAN`

### Thickness
- PDF p57 / printed p42
- §2.2.1.6 栱厚
- Table 2-17
- observed mean = **155.6 mm**
- minimum = 150 mm
- maximum = 165 mm
- n = 28
- classification = `DIRECT_PRIMARY / OBSERVED_MEAN`

### Length
- PDF p60–61 / printed p45–46
- §2.2.2.3 令栱
- Fig. 2-16
- Table 2-24
- observed mean = **897 mm**
- minimum = 860 mm
- maximum = 925.6 mm
- n = 28
- classification = `DIRECT_PRIMARY / OBSERVED_MEAN`

Same-building visual/form authority:
- D-210 accepted the primary report's outer-eaves dougong context plus official same-building visual material for component/form context.
- This supports family identity, horizontal-gong member semantics and broad assembly context.
- It does not provide a complete metrically recovered standalone 令栱 profile.

## 3. Canonical Stage1 Reference Geometry

Proposed canonical family envelope:

**897 × 217.4 × 155.6 mm**

Coordinate convention:
- +X = member length axis
- +Y = width / extrusion axis
- +Z = profile thickness / vertical axis
- origin = deterministic family-local origin
- placement transform = NOT part of the Master body

Semantic classification:

### Length 897 mm
- `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
- family-level representative dimension
- NOT per-instance exact
- NOT proven 963 original-design dimension

### Width 217.4 mm
- `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
- family-level representative dimension
- NOT per-instance exact
- NOT proven 963 original-design dimension

### Thickness 155.6 mm
- `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`
- family-level representative dimension
- NOT per-instance exact
- NOT proven 963 original-design dimension

The canonical body therefore represents a **family observed-mean reference specimen**.

It must never be described as:
- 28 individually measured identical members;
- exact current geometry of every location;
- exact 963 original design.

## 4. Instance / Variant Rule

Locked proposal for Product Owner review:

- geometry variant count = **0**
- physical instance count = **28**
- each Registry record may reference the same Master identity
- direction/location metadata remain instance-owned
- world rotation/placement remain assembly-owned

Forbidden:
- creating SOUTH / NORTH / EAST / WEST geometry variants without evidence;
- creating 28 location-specific Masters;
- using measured spread (min/max) to invent undocumented per-instance geometry;
- assigning the source's 28 measured samples to the 28 Registry locations without direct mapping evidence.

Current sample-to-instance mapping:

`UNKNOWN`

The numerical coincidence that measurement sample count = 28 and Registry physical count = 28 does **not** establish one-to-one correspondence.

## 5. Profile / Form Authority

Proposed:

`PROFILE_AUTHORITY = SAME_BUILDING_SOURCE_GUIDED_SIMPLIFIED / PROVISIONAL`

Evidence boundary:
- exact standalone historical profile curve = `UNRESOLVED`
- exact numeric profile control dimensions = `UNRESOLVED`
- exact end shaping = `UNRESOLVED`
- source-image metric calibration = `NOT PERFORMED / NOT CLAIMED`

A future Stage1 profile control set is permitted only if it is:
- deterministic;
- versioned;
- visually reviewable;
- reproducible from a locked numeric Definition;
- explicitly classified `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
- derived from approved same-building form evidence;
- not represented as direct measurement unless a calibrated source extraction is actually established.

Explicitly forbidden:
- copying T-037 瓜子栱 control points;
- copying T-038 慢栱 control points;
- averaging or morphing prior gong control sets merely for convenience;
- silently substituting a generic Song / Yingzao Fashi template.

**Numeric Profile Control Set is NOT part of this V0.1 Candidate approval yet.**

Before engineering execution, a separate Profile Control Set gate is required.

## 6. Geometry Construction Boundary

Stage1 construction intent:
- one symmetric horizontal gong body;
- canonical L/W/T envelope fixed by the observed family means above;
- local profile built only after Profile Control Set approval;
- extrusion across width must preserve 217.4 mm canonical width;
- no scale-based transfer from another gong family;
- no building placement baked into the Master.

The Master is a component-family reference body, not an assembled bracket-set asset.

## 7. Unsupported / Deferred Geometry

Explicitly DEFERRED / UNRESOLVED:
- exact mortise-tenon geometry;
- grooves;
- slots;
- cavities;
- hidden connection cuts;
- exact end notches / shoulders;
- exact historical profile curve;
- unmeasured chamfers;
- wear / damage / warp;
- per-instance deformation;
- per-instance originality / repair state;
- one-to-one measured-sample mapping.

None may be added merely to improve visual plausibility or assembly convenience.

## 8. Connection / Assembly Boundary

Stage1 may record semantic adjacency to the outer-eaves dougong system.

It does **not** lock:
- exact connection kind;
- insertion depth;
- mortise/tenon dimensions;
- hidden bearing geometry;
- final world placement.

All exact connection geometry remains deferred to evidence-backed connection-aware assembly work.

## 9. First-Article Review Intent

A future first article should make the following reviewable:

1. `AXON`
2. `FRONT_PROFILE`
3. `END / WIDTH VIEW`
4. `DIMENSION_PROOF` — 897 / 217.4 / 155.6
5. `28_INSTANCE_DISTRIBUTION_AND_ZERO_VARIANT_RULE`
6. `PROFILE_PROVENANCE_AND_CONTROL_SET_CLASSIFICATION`
7. `SOURCE_VS_RECONSTRUCTION_BOUNDARY`
8. `UNKNOWN_DEFERRED_GEOMETRY`

Review must be able to detect:
- wrong family proportions;
- false direction/location variants;
- unsupported profile invention;
- profile reuse from T-037/T-038;
- generic-template substitution;
- observed-mean evidence inflation;
- unsupported joinery/local cuts;
- blank or near-uniform render failure.

## 10. Proposed Hard Fails for Future Task Contract

- `WRONG_PHYSICAL_INSTANCE_COUNT`
- `WRONG_CANONICAL_LENGTH`
- `WRONG_CANONICAL_WIDTH`
- `WRONG_CANONICAL_THICKNESS`
- `OBSERVED_MEAN_MARKED_AS_PER_INSTANCE_EXACT`
- `ORIGINAL_963_FACT_UPGRADE`
- `SAMPLE_TO_INSTANCE_MAPPING_INVENTED`
- `DUPLICATE_MASTER_PER_LOCATION`
- `FALSE_DIRECTION_GEOMETRY_VARIANT`
- `UNSUPPORTED_PROFILE_INVENTION`
- `PRIOR_GONG_PROFILE_CONTROL_REUSE`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `PROFILE_CONTROL_SET_NOT_VERSIONED`
- `UNSUPPORTED_END_SHAPE`
- `UNSUPPORTED_JOINERY_OR_LOCAL_CUTS`
- `BUILDING_PLACEMENT_BAKED_INTO_MASTER`
- `REVIEW_RENDER_NEAR_UNIFORM`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 11. Locked Decision｜D-212

D-211 prepared Master Spec V0.1 Candidate 01 for Product Owner review. D-212 records Product Owner approval and formally locks this V0.1 as V001.

Locked architecture:
- one `CMP-GONG-LINGGONG-001_MASTER`;
- zero Geometry Variant;
- 28 physical instance bindings;
- canonical observed-mean reference envelope = **897 × 217.4 × 155.6 mm**;
- all three dimensions remain `DIRECT_PRIMARY / OBSERVED_MEAN / n=28`;
- per-instance exact mapping remains UNKNOWN;
- exact historical profile/end/joinery remain unresolved/deferred;
- separate numeric Profile Control Set gate required before engineering execution.

This Master Spec is now **PRODUCT OWNER APPROVED / LOCKED / D-212**.

Next complete step:
- design and lock the 令栱 Task Contract;
- the separate Profile Control Set gate remains mandatory before engineering execution.

Not authorized by D-212:
- Task Contract lock;
- engineering T-task creation;
- branch / PR creation;
- GitHub Actions / Blender;
- first-article production;
- formalization;
- Catalog / V008 binding;
- merge;
- Stage2;
- T-018 resume.

## 12. Task Contract Lock｜D-213

T-039｜P3_3_LINGGONG_MASTER_V2_V001 Task Contract is PRODUCT OWNER APPROVED / LOCKED. The contract preserves the D-212 architecture (1 shared Master / 0 Geometry Variant / 28 bindings), the 897 × 217.4 × 155.6 mm observed-mean family reference, UNKNOWN sample-to-instance mapping, and unresolved/deferred profile/end/joinery boundaries. Engineering execution remains blocked until a separate Profile Control Set V0.1 is Product Owner approved.
