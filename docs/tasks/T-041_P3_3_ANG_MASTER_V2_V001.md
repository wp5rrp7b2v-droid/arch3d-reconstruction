# 中国古建筑3D复原｜T-041｜P3_3_ANG_MASTER_V2_V001

Status: **ENGINEERING EXECUTION AUTHORIZED / D-253 / FIRST ARTICLE ENGINEERING ACTIVE**
Date: 2026-09-28
Stage: P3.3 V002 Stage 1
Locked Master Spec: D-246｜P3_3_STAGE1_ANG_MASTER_SPEC_V001
Task id: `T-041｜P3_3_ANG_MASTER_V2_V001`
Branch: `codex/t041-p3-3-ang-master-v2-v001`

> Governance boundary: D-248 creates and locks the T-041 engineering task identity and this Task Contract only. Engineering execution remains blocked until Gate A and Gate B are separately Product Owner approved and a separate Engineering Execution Authorization is issued.

## 1. Objective

T-041 shall, only after all pre-execution gates and a separate Engineering Execution Authorization, build and validate one reusable 昂族 Stage1 Master family covering the current V008 derived binding scope:

- `TOU_ANG` / 头昂: **16** Registry records
- `ER_ANG` / 二昂: **16** Registry records
- total target: **32 LOCKED_DERIVED records**

Locked family architecture from D-246:

**ONE MASTER FAMILY / TWO NON-COLLAPSIBLE VARIANTS / 32 V008 BINDINGS**

The future task produces Stage1 component-family reference geometry only.

It does not authorize:
- treating 32 as a directly inventoried historical whole-hall physical count;
- complete dougong/bracket-set production geometry;
- 32-instance building placement;
- Stage2;
- T-018 restart.

## 2. Identity Contract

Component family id:

`CMP-GONG-ANG-001`

Master id:

`CMP-GONG-ANG-001_MASTER`

Master version:

`V001`

Task id:

`T-041｜P3_3_ANG_MASTER_V2_V001`

Geometry variant identities:

- `TOU_ANG`
- `ER_ANG`

Required Registry bindings:
- TOU_ANG = 16
- ER_ANG = 16
- total = 32
- all remain `LOCKED_DERIVED`

Hard semantic boundary:

**32 is the current V008 derived binding scope. It is not a directly inventoried historical whole-hall Ang count.**

Direction/location semantics remain instance/assembly metadata and may not create SOUTH/NORTH/EAST/WEST geometry variants.

## 3. Source Authority

Primary source:

`SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF SHA-256:

`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Locked evidence lineage:
- D-244: Source Readiness + D-076 = PASS WITH GEOMETRY BOUNDARY
- D-246: 昂族 Master Spec V0.1 = PRODUCT OWNER APPROVED / LOCKED

No generic Song template, 《营造法式》 template, comparative-building geometry, or unsupported reconstruction convenience may override the same-building source boundary.

## 4. Variant Contract

Exactly:
- Master family count = **1**
- geometry variant count = **2**
- direction/location geometry variant count = **0**

Required:
- TOU_ANG and ER_ANG keep independent variant identities;
- both are generated within one family architecture;
- each must have its own semantic/geometry signature after execution;
- each must consume its own locked future reference-length/profile inputs;
- shared builder/validator infrastructure is allowed;
- shared evidence schema and coordinate methodology are allowed.

Forbidden:
- collapsing TOU_ANG and ER_ANG into one geometry body;
- deriving ER_ANG by uniform/global scaling of a finished TOU_ANG mesh;
- deriving TOU_ANG by uniform/global scaling of a finished ER_ANG mesh;
- direction/location-specific geometry variants without new evidence;
- per-instance duplicate Masters.

## 5. Direct Dimension Semantic Contract

Locked same-building source values:
- 头昂“广” = **278.4 mm**, `DIRECT_PRIMARY / OBSERVED_MEAN`
- 二昂“广” = **187.0 mm**, `DIRECT_PRIMARY / SOURCE_TABLE_VALUE`

The report also associates **187.0 mm** with the 头昂单材部分 relationship.

These values are not:
- per-instance exact dimensions;
- proof of identical complete geometry between TOU_ANG and ER_ANG;
- proof of 963 original-design dimensions.

### Mandatory semantic-axis protection

The source term **“广” MUST NOT be hard-mapped to a Master X/Y/Z axis by this Task Contract.**

Gate A must explicitly lock:

`SOURCE DIMENSION SEMANTIC -> MASTER AXIS MAPPING`

before either 278.4 or 187.0 may enter executable geometry.

## 6. Length / Slope / Assembly Control Contract

Current executable length status:

### TOU_ANG
- direct historical standalone full timber length = `UNRESOLVED`
- Stage1 reconstruction reference length = **NOT LOCKED**

### ER_ANG
- direct historical standalone full timber length = `UNRESOLVED`
- Stage1 reconstruction reference length = **NOT LOCKED**

Inherited assembly-level evidence boundary from D-244:
- 第一二跳总出跳 observed mean = **732.4 mm**
- 第三四跳总出跳 observed mean = **719.5 mm**

These are assembly-level combined projection statistics and MUST NOT be converted into:
- TOU_ANG full length;
- ER_ANG full length;
- TOU_ANG + ER_ANG full-length sum;
- per-instance exact dimensions.

Report design relation:
- horizontal = **47分**
- rise = **21分**
- classification = `REPORT_INFERRED / REPORT_DESIGN_LOGIC / REPLACEABLE`

It is not:
- direct per-member slope measurement;
- proven 963 original design;
- standalone member length.

### Mandatory pre-execution Gate A

Before any engineering execution can be authorized, a separate:

`ANG_LENGTH_SLOPE_ASSEMBLY_CONTROL_SET_V0.1`

must be Product Owner approved and locked.

It must define at minimum:

1. deterministic Stage1 TOU_ANG reconstruction reference length;
2. deterministic Stage1 ER_ANG reconstruction reference length;
3. evidence classification/provenance for each selected reference length;
4. explicit semantic-to-axis mapping for source “广” values 278.4 / 187.0;
5. reconciliation of current V008 `thickness_mm = 154` provenance and axis semantics;
6. deterministic 47:21 slope/rise-run implementation rule and tolerance;
7. TOU_ANG local origin / assembly datum;
8. ER_ANG local origin / assembly datum;
9. deterministic double-Ang validation-fixture placement rule;
10. explicit assembly measurement semantics that keep 732.4 / 719.5 separate from member full lengths;
11. deterministic version/signature;
12. Product Owner approval.

Explicit prohibitions:
- `TOU_ANG_FULL_LENGTH = 719.5`;
- `ER_ANG_FULL_LENGTH = 719.5`;
- any member full length derived directly from 732.4 or 719.5 without independent evidence;
- promotion of 47:21 to DIRECT_PRIMARY;
- promotion of 154 mm to Ang-specific DIRECT_PRIMARY before provenance reconciliation;
- invented hidden overlap used to force any assembly relation.

Until Gate A is locked:
- neither geometry variant is executable;
- no canonical body may be generated;
- no builder may freeze member length, source-dimension axis mapping, section thickness, local datum, slope rule, or assembly fixture.

## 7. Longitudinal Profile Control Contract

Current status:
- same-building visual/form evidence is sufficient for bounded Stage1 reconstruction;
- geometry mode = `LONGITUDINAL_PROFILE_DRIVEN`;
- exact historical TOU_ANG longitudinal profile = `UNRESOLVED`;
- exact historical ER_ANG longitudinal profile = `UNRESOLVED`;
- exact head/body transition position = `UNRESOLVED`;
- exact end shaping = `UNRESOLVED`;
- metric image calibration = `NOT PERFORMED / NOT CLAIMED`.

TOU_ANG must retain the locked semantic:

`DEEP_HEAD_REGION -> SINGLE_CAI_REGION`

ER_ANG must use an independent longitudinal profile definition.

### Mandatory pre-execution Gate B

After Gate A is locked and before engineering execution can be authorized, a separate:

`ANG_LONGITUDINAL_PROFILE_CONTROL_SET_V0.1`

must be Product Owner approved and locked.

It must provide at minimum:

1. explicit deterministic numeric control set for TOU_ANG;
2. explicit deterministic numeric control set for ER_ANG;
3. coordinate meaning tied to Gate A axis/datum conventions;
4. same-building source references;
5. human-reviewable profile diagrams/comparison;
6. TOU_ANG deep-head to single-cai semantic proof;
7. explicit classification `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE` for reconstructed controls;
8. explicit statement that metric image calibration is not claimed unless actually performed;
9. proof that neither variant is created by finished-mesh scaling of the other;
10. deterministic version/signatures;
11. Product Owner approval.

Explicitly forbidden:
- rectangular-prism-only Ang representation;
- copying/scaling a finished mesh between TOU_ANG and ER_ANG;
- copying prior 华栱/瓜子栱/慢栱/令栱 control polygons as Ang authority;
- generic Song / 《营造法式》 template substitution;
- comparative-building geometry as Wanfo authority;
- aesthetic free-form invention presented as source evidence.

## 8. Coordinate Contract

Family semantic axes remain provisionally:

- +X = longitudinal / out-jump axis
- +Y = transverse member axis
- +Z = vertical

However, source terms such as “广” are not automatically equivalent to any axis until Gate A locks the semantic mapping.

The exact local origin and assembly reference datum are not locked by this Task Contract.

After Gate A:
- each variant shall use deterministic family-local coordinates;
- canonical-body transforms shall be identity unless the locked Definition establishes an equivalent deterministic representation;
- building/world placement remains outside Master geometry.

No building placement may be baked into the canonical Master bodies.

## 9. Geometry Construction Contract

Only after:
1. Task Contract lock;
2. Gate A lock;
3. Gate B lock;
4. explicit Engineering Execution Authorization;

may implementation begin.

Future Stage1 construction must:
- generate TOU_ANG independently from its locked Definition;
- generate ER_ANG independently from its locked Definition;
- preserve one-family/two-variant identity architecture;
- consume locked reference length, dimension-axis, datum, slope and profile controls;
- use longitudinal-profile-driven geometry;
- preserve TOU_ANG deep-head to single-cai semantic;
- avoid global-scale derivation of one finished variant from the other;
- keep unsupported connection details absent.

## 10. First Article Contract

The future First Article shall contain exactly **two canonical production bodies**:

1. `TOU_ANG`
2. `ER_ANG`

Additionally, validation may build one:

`DOUBLE_ANG_ASSEMBLY_FIXTURE_VALIDATION_ONLY`

This fixture is:
- validation-only;
- non-canonical;
- not a third geometry variant;
- not a Catalog asset;
- not a Registry binding;
- not complete dougong production geometry;
- not evidence of historical hidden connection geometry.

Its sole purposes are:
- place the two locked reference bodies using Gate A datums;
- expose the locked 47:21 implementation;
- verify the two-level Ang relationship;
- expose any illegal conversion of assembly projection into member length;
- expose finished-mesh scaling/collapse.

No 32-instance building placement is allowed before Product Owner First Article approval.

The canonical bodies and validation fixture must exclude unsupported:
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

## 11. Required Review Evidence

Review evidence shall expose the following domains independently; panels may be combined only if all domains remain readable:

1. `FAMILY_AND_32_DERIVED_BINDING_SCOPE`
2. `TOU_ANG_CANONICAL_BODY_AND_PROFILE`
3. `ER_ANG_CANONICAL_BODY_AND_PROFILE`
4. `TWO_VARIANT_IDENTITY_PROOF`
5. `278_4_187_SOURCE_DIMENSION_SEMANTIC_AND_AXIS_PROOF`
6. `47_21_SLOPE_IMPLEMENTATION_PROOF`
7. `DOUBLE_ANG_ASSEMBLY_FIXTURE`
8. `154_PROVENANCE_AND_SECTION_BOUNDARY`
9. `SOURCE_VS_RECONSTRUCTION_BOUNDARY`
10. `UNKNOWN_DEFERRED_AND_NO_JOINERY_PROOF`

Review evidence must make it possible to detect:
- accidental TOU_ANG/ER_ANG collapse;
- uniform mesh scaling;
- loss of TOU_ANG deep-head semantic;
- 278.4/187 mapped to an axis without locked semantic authority;
- 154 marked as direct without provenance closure;
- 47:21 treated as direct measurement;
- 719.5/732.4 treated as member lengths;
- unsupported direction/location variants;
- unsupported end/joinery invention;
- blank or near-uniform renders.

## 12. Validation Contract

Future machine validation must verify at minimum:

### Registry / identity
- Registry schema = V008
- Registry total = 505
- target Ang records = 32
- count status = LOCKED_DERIVED
- TOU_ANG bindings = 16
- ER_ANG bindings = 16
- directly inventoried whole-hall count claim = false
- Master family count = 1
- geometry variant count = 2
- direction geometry variant count = 0

### Evidence semantics
- TOU_ANG 278.4 remains family/source-level and not per-instance exact
- ER_ANG 187.0 remains family/source-level and not per-instance exact
- sample-to-instance mapping = UNKNOWN
- 47:21 remains REPORT_INFERRED / REPORT_DESIGN_LOGIC / REPLACEABLE
- original-963 fact claim = false
- 154 provenance reconciliation completed before use as direct authority
- 732.4/719.5 remain assembly-level combined-projection evidence only
- historical standalone member lengths remain unresolved unless separately evidenced

### Pre-execution controls
- approved Gate A id/version/signature present
- approved TOU_ANG reconstruction reference length present
- approved ER_ANG reconstruction reference length present
- source “广” axis mapping present
- 154 provenance disposition present
- approved local datums present
- approved 47:21 implementation rule present
- approved Gate B id/version/signatures present
- independent profile controls present for both variants
- reconstructed profile classification retained

### Geometry / reproducibility
- exactly two canonical bodies
- TOU_ANG and ER_ANG have separate semantic/geometry signatures
- neither is produced by uniform global scaling of the other
- TOU_ANG deep-head to single-cai semantic is preserved
- longitudinal-profile-driven geometry is used
- rectangular-prism-only output rejected
- validation fixture tagged non-canonical
- validation fixture creates no Registry/Catalog identity
- unsupported joinery/local cuts absent
- closed manifold canonical meshes
- deterministic rebuild
- independent reopen
- deterministic semantic and geometry signatures
- canonical binary SHA-256
- no tracked .blend in Git
- Blender version locked by workflow
- Review Board nonblank / variance check

## 13. Hard Fails

Future implementation/validator must fail closed on at least:

- `ANG_BINDING_COUNT_NOT_32`
- `TOU_ANG_BINDING_COUNT_NOT_16`
- `ER_ANG_BINDING_COUNT_NOT_16`
- `LOCKED_DERIVED_MARKED_AS_DIRECT_INVENTORY`
- `MASTER_FAMILY_COUNT_NOT_1`
- `GEOMETRY_VARIANT_COUNT_NOT_2`
- `DIRECTION_GEOMETRY_VARIANT_CREATED`
- `TOU_ER_VARIANTS_COLLAPSED`
- `TOU_ANG_SCALED_FROM_ER_ANG`
- `ER_ANG_SCALED_FROM_TOU_ANG`
- `RECTANGULAR_PRISM_ONLY_ANG_GEOMETRY`
- `SOURCE_GUANG_AXIS_MAPPING_NOT_LOCKED`
- `278_4_OR_187_MARKED_AS_PER_INSTANCE_EXACT`
- `ANG_154_PROVENANCE_NOT_RECONCILED`
- `ANG_154_MARKED_DIRECT_WITHOUT_EVIDENCE`
- `REPORT_47_21_MARKED_DIRECT`
- `REPORT_47_21_MARKED_PROVEN_963_DESIGN`
- `TOU_ANG_REFERENCE_LENGTH_NOT_LOCKED`
- `ER_ANG_REFERENCE_LENGTH_NOT_LOCKED`
- `MEMBER_LENGTH_INVENTED`
- `ASSEMBLY_PROJECTION_USED_AS_MEMBER_LENGTH`
- `FULL_LENGTH_SUM_EQUATED_TO_719_5_OR_732_4`
- `TOU_ANG_PROFILE_CONTROL_NOT_LOCKED`
- `ER_ANG_PROFILE_CONTROL_NOT_LOCKED`
- `TOU_ANG_DEEP_HEAD_SEMANTIC_LOST`
- `PROFILE_MARKED_DIRECT_MEASUREMENT_WITHOUT_EVIDENCE`
- `PRIOR_GONG_PROFILE_CONTROL_REUSE`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `COMPARATIVE_BUILDING_GEOMETRY_REUSE_AS_AUTHORITY`
- `UNSUPPORTED_END_SHAPE`
- `UNSUPPORTED_JOINERY_OR_HIDDEN_CUTS`
- `VALIDATION_FIXTURE_PROMOTED_TO_CANONICAL_ASSET`
- `BUILDING_PLACEMENT_BAKED_INTO_MASTER`
- `REVIEW_RENDER_NEAR_UNIFORM`
- `SILENT_HISTORICIZATION`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 14. Deferred / Unsupported Geometry

Remain explicitly unresolved or deferred:
- exact historical TOU_ANG standalone full timber length;
- exact historical ER_ANG standalone full timber length;
- exact TOU_ANG deep-head to single-cai transition location;
- exact historical TOU_ANG longitudinal profile;
- exact historical ER_ANG longitudinal profile;
- exact outer Ang head shaping;
- exact inner-end length;
- hidden overlap;
- mortise-tenon geometry;
- grooves;
- slots;
- cavities;
- hidden connection cuts;
- unmeasured chamfers;
- wear/damage/warp;
- per-instance deformation;
- per-instance originality/repair state;
- sample-to-instance mapping;
- directly inventoried whole-hall Ang count.

Assembly convenience is not evidence.

## 15. Scope Protection

The future task must not:
- reactivate T-018;
- start Stage2;
- modify T-020 shared datum authority;
- modify approved T-037/T-038/T-039/T-040 canonical geometry;
- use prior gong profile controls as Ang authority;
- broaden the validation fixture into a production bracket-set assembly;
- create 32 building-placement instances as First Article output;
- formalize Catalog/V008 before Product Owner First Article approval and explicit formalization authorization;
- merge before post-formalization readiness PASS and explicit Product Owner Ready+Merge approval.

## 16. Locked Gate Sequence

1. Source Readiness + D-076 — **PASS / D-244**
2. Master Spec V0.1 — **LOCKED / D-246**
3. Task Contract — **LOCKED / PRODUCT OWNER APPROVED / D-248**
4. Length/Slope/Assembly Control Set V0.1 — **LOCKED / PRODUCT OWNER APPROVED / D-250**
5. Longitudinal Profile Control Set V0.1 — **LOCKED / PRODUCT OWNER APPROVED / D-252**
6. Engineering Execution Authorization — **AUTHORIZED / D-253**
7. First Article machine validation — **NOT AUTHORIZED**
8. Product Owner First Article Approval — **NOT AUTHORIZED**
9. Formalization + Catalog/V008/CURRENT binding — **NOT AUTHORIZED**
10. Derived Excel + latest-head/shared regressions + readiness — **NOT AUTHORIZED**
11. Draft→Ready + Merge — **NOT AUTHORIZED**
12. Formal Closure — **NOT AUTHORIZED**

Ordering rule:

**Gate A Length/Slope/Assembly Control must lock before Gate B Longitudinal Profile Control.**

Reason:
the profile-control application depends on stable reference lengths, source-dimension axis semantics, section/thickness disposition, slope implementation and local datum. Reversing the order would create avoidable rework and could silently bind profiles to unapproved scale/axis semantics.

## 17. Task Contract Lock｜D-248

Product Owner approved D-247 Candidate 01 without changing its technical architecture or evidence boundaries.

D-248 formally:
- locks this Task Contract as the canonical contract for `T-041｜P3_3_ANG_MASTER_V2_V001`;
- creates/activates the T-041 engineering task identity;
- preserves one `CMP-GONG-ANG-001_MASTER` family;
- preserves two independent variants `TOU_ANG` / `ER_ANG`;
- preserves 16 + 16 = 32 V008 `LOCKED_DERIVED` bindings;
- preserves zero direction geometry variants;
- preserves 278.4 / 187.0 source-dimension semantics without premature axis mapping;
- preserves 154 mm as provenance-reconciliation-required;
- preserves 47:21 as REPORT_INFERRED / replaceable;
- preserves all unresolved historical lengths/profile/end/joinery boundaries;
- makes Gate A then Gate B mandatory before engineering execution.

D-248 does **not** authorize:
- branch creation;
- PR creation;
- builder/validator implementation;
- Blender;
- First Article generation;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.

Next complete step:

`ANG_LENGTH_SLOPE_ASSEMBLY_CONTROL_SET_V0.1` design.


## 18. Gate A Lock｜D-250

Product Owner approved Gate A Candidate 01 unchanged.

Canonical control:

`production/zhenguo_wanfo/registry/P3_3_STAGE1_ANG_LENGTH_SLOPE_ASSEMBLY_CONTROL_SET_V001.json`

D-250 formally locks:

- TOU_ANG 广 = **278.4 mm** as `DIRECT_PRIMARY / OBSERVED_MEAN / FAMILY_SOURCE_VALUE`;
- ER_ANG / 头昂单材部分广 = **187.0 mm** as the report's combined source category, not an ER-only n=16 mean;
- 昂厚 = **154.0 mm** as `DIRECT_PRIMARY / OBSERVED_MEAN / ANG_FAMILY_COMMON_THICKNESS`;
- source-internal thickness sample-count conflict remains explicit: narrative **34** vs Table 2-11 **16**;
- member-local axes: U longitudinal centreline / V thickness / W guang;
- 154 mm maps to local V / Assembly Y;
- 278.4 / 187.0 map to local W in the Assembly X-Z plane, not generic Assembly Y width;
- report design triangle = **47分 run / 21分 rise**;
- design run = **719.1 mm**;
- design rise = **321.3 mm**;
- design angle = **24.075498255078834°**;
- synthetic reference centreline control span = **787.6157057855055 mm** for each variant;
- the equal synthetic control span does not establish equal historical full timber lengths;
- direct observed third/fourth combined projection = **719.5 mm** remains separate from the report-inferred 719.1 mm design run;
- their delta = **0.4 mm** and must not be forced to zero;
- DOUBLE_ANG_ASSEMBLY_FIXTURE remains validation-only and non-canonical.

D-250 does **not** resolve:
- historical complete TOU_ANG timber length;
- historical complete ER_ANG timber length;
- exact longitudinal profiles;
- TOU_ANG deep-head transition location;
- outer/end shaping;
- hidden overlap;
- joinery.

D-250 does **not** authorize:
- engineering branch creation;
- builder/validator implementation;
- Blender execution;
- First Article;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.

Next complete step:

`ANG_LONGITUDINAL_PROFILE_CONTROL_SET_V0.1` design.


## 19. Gate B Lock｜D-252

Product Owner approved Gate B Candidate 01 unchanged.

Canonical control:

`production/zhenguo_wanfo/registry/P3_3_STAGE1_ANG_LONGITUDINAL_PROFILE_CONTROL_SET_V001.json`

Review artifact:

`docs/production/zhenguo_wanfo/P3_3_STAGE1_ANG_LONGITUDINAL_PROFILE_CONTROL_SET_V001.svg`

D-252 formally locks:

### TOU_ANG
- profile point count = **10**
- semantic = `SINGLE_CAI_REGION -> DEEP_HEAD_REGION -> OUTBOARD_TAPER`
- direct source depths retained: **187.0 mm** single-cai and **278.4 mm** deep-head
- deterministic reconstructed stations:
  - U=-0.500 = inner reconstruction cut / 187.0
  - U=-0.125 = single-cai region end / 187.0
  - U=+0.125 = deep-head transition completed / 278.4
  - U=+0.375 = deep-head region end / 278.4
  - U=+0.500 = outboard reconstruction taper cut / 187.0
- control-point SHA-256 = `3e45e7732cf49012cbf8b5e480e76ad2fd986c4aa717dd650e3bf3f9831f7bb5`

### ER_ANG
- profile point count = **6**
- semantic = `CONSTANT_SINGLE_CAI_BODY -> OUTBOARD_TAPER`
- direct source body depth retained: **187.0 mm**
- deterministic reconstructed taper:
  - U=+0.375 = taper start
  - U=+0.500 = outboard reconstruction cut
  - taper ratio = **2/3**
- the 2/3 taper is `SOURCE_GUIDED_SIMPLIFIED / STAGE1_TAPER_CONTROL / REPLACEABLE / NOT_DIRECT_MEASUREMENT`
- control-point SHA-256 = `c4b935c9d445414831f16d949b02ff110f3e336f88c68dd68f58d514bd172778`

Family semantic-control SHA-256:

`dc38ab72be1f5aef3192a48e11621a3288c422475545b56dc5e29fa0102e2ae5`

D-252 preserves:
- Gate A reference span = **787.6157057855055 mm**
- common thickness = **154.0 mm**
- 47:21 design relation from Gate A
- exact historical TOU/ER profiles = unresolved
- exact TOU deep-head transition location = unresolved
- exact outer Ang head shaping = unresolved
- metric source-image calibration = not performed/not claimed
- historical asymmetry = unresolved
- hidden overlap/joinery = deferred

Both profiles are classified:

`SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_PROFILE_MEASUREMENT`

D-252 prohibits:
- TOU/ER profile collapse;
- finished-mesh scaling between variants;
- reuse of prior gong profile controls as Ang authority;
- generic Song/《营造法式》 substitution;
- reconstructed stations/taper presented as direct measurement;
- profile-gate invention of end joinery.

D-252 does **not** authorize:
- engineering branch creation;
- PR creation;
- builder/validator implementation;
- Blender execution;
- First Article;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.

Next complete gate:

`ENGINEERING_EXECUTION_AUTHORIZATION`.


## 20. Engineering Execution Authorization｜D-253

Product Owner explicitly authorized T-041 Engineering Execution after:

- Task Contract D-248 = LOCKED;
- Gate A D-250 = LOCKED;
- Gate B D-252 = LOCKED.

Authorized isolated production branch:

`codex/t041-p3-3-ang-master-v2-v001`

Authorized engineering scope:

1. implement canonical Ang Definition payloads bound only to D-250 + D-252;
2. implement independent TOU_ANG and ER_ANG builders;
3. implement fail-closed validator covering the Task Contract hard-fail set;
4. implement GitHub Actions workflow using the project-locked Blender runtime;
5. generate exactly two canonical First Article bodies:
   - `TOU_ANG`
   - `ER_ANG`
6. generate one non-canonical `DOUBLE_ANG_ASSEMBLY_FIXTURE_VALIDATION_ONLY`;
7. produce deterministic semantic/geometry signatures;
8. perform deterministic rebuild and independent reopen validation;
9. produce nonblank review evidence exposing identity, dimensions, 47:21 implementation, Gate-B profile controls, evidence boundaries, and no-joinery proof;
10. open a Draft PR after machine validation evidence is available.

Locked engineering inputs:

### Gate A
`ANG_LENGTH_SLOPE_ASSEMBLY_CONTROL_SET_V001_C01`

Semantic signature:

`6c9b8c5b6ee6715292df5b23b7d8b8d9fdaaf4be7d1558631fea5883528b7096`

### Gate B
`ANG_LONGITUDINAL_PROFILE_CONTROL_SET_V001_C01`

Family semantic-control signature:

`dc38ab72be1f5aef3192a48e11621a3288c422475545b56dc5e29fa0102e2ae5`

TOU profile signature:

`3e45e7732cf49012cbf8b5e480e76ad2fd986c4aa717dd650e3bf3f9831f7bb5`

ER profile signature:

`c4b935c9d445414831f16d949b02ff110f3e336f88c68dd68f58d514bd172778`

D-253 does not authorize:

- Product Owner First Article acceptance;
- formalization;
- Catalog/V008/CURRENT binding;
- derived Excel sync;
- Draft→Ready transition;
- merge;
- formal closure;
- Stage2;
- T-018 resume.

Next engineering gate:

`FIRST ARTICLE MACHINE VALIDATION`.


## 21. First Article Machine Gate｜D-254

T-041 First Article machine validation completed successfully on GitHub Actions.

Run ID:

`36373958970`

Head commit:

`e8e986101c0c8a64d29ecc589d0e4c5949c1d5ac`

Draft PR:

`#37`

Artifact:

- name: `P3_3_T041_ANG_MASTER_V2_FIRST_ARTICLE_V001`
- artifact id: `10950620532`
- artifact digest: `sha256:a042c6e48a753867a5a74b44c54d0af2750d0f37c33a5f950eb3d9daf4d99d0e`
- size: `3771783 bytes`

Machine result:

- `T041_VALIDATION_PASS 90`
- `T041_FIRST_ARTICLE_MACHINE_PASS 90`
- canonical body count = 2
- TOU_ANG geometry signature = `61a2bbb85fa5fc07ed9c37ce610f2aee0360f280c09f8317614b7a62f7819250`
- ER_ANG geometry signature = `b778edc208d788c5f9fad0a19849ca33f3334e7c4e2656721279386528979678`
- family semantic signature = `a8c3b3757d6f2defd88bcece3fe754979a2c02af4e0de59f3ecc94e9fb6d7a29`
- canonical blend SHA-256 = `7a8c2bcdde1fac1f9f7f06bd7c1894237a7bda02a2a38e2b329da4f4b719d0a8`
- review board SHA-256 = `a76a85cba9ece9617053107772226bc790d783134faf4dd508edb0a02102ab65`
- Blender = `4.5.13 LTS`

All 90 fail-closed checks passed, including:
- V008 identity/count/binding semantics;
- Gate A/B signature binding;
- 278.4 / 187 / 154 evidence semantics;
- 47:21 and 719.1/719.5 separation;
- TOU/ER profile independence;
- manifold geometry;
- unsupported joinery absence;
- independent reopen;
- deterministic restore;
- nonblank review renders;
- canonical binary not tracked in Git.

D-254 records the **machine gate only**.

D-254 does **not** constitute Product Owner First Article acceptance and does not authorize:
- formalization;
- Catalog/V008/CURRENT binding;
- Derived Excel sync;
- Draft→Ready;
- merge;
- closure;
- Stage2;
- T-018 resume.

Next gate:

`PRODUCT OWNER FIRST ARTICLE REVIEW / APPROVAL`.
