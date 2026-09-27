# 中国古建筑3D复原｜T-040｜P3_3_HUAGONG_MASTER_V2_V001

Status: **FORMALIZED + CATALOG/V008/CURRENT BOUND / D-238 / PR #36 DRAFT / MERGE NOT AUTHORIZED**
Date: 2026-09-27
Stage: P3.3 V002 Stage 1
Locked Master Spec: D-227｜P3_3_STAGE1_HUAGONG_MASTER_SPEC_V001
Task id: `T-040｜P3_3_HUAGONG_MASTER_V2_V001`
Branch: `NOT CREATED / ENGINEERING EXECUTION NOT AUTHORIZED`

> Governance boundary: D-229 creates and locks the T-040 engineering task identity and this Task Contract only. Engineering execution remains blocked until Gate A and Gate B are Product Owner approved and a separate Engineering Execution Authorization is issued.

## 1. Objective

T-040 shall, only after all pre-execution gates and a separate Engineering Execution Authorization, build and validate one reusable 华栱 Stage1 Master family covering the current V008 direction-explicit 正身 subset:

- JUMP_1_HUAGONG: **28** Registry records
- JUMP_2_HUAGONG: **28** Registry records
- total target: **56 LOCKED_SUBSET records**

Locked family architecture from D-227:

**ONE PARAMETRIC MASTER FAMILY / TWO INDEPENDENT JUMP VARIANT IDENTITIES / 56 SUBSET INSTANCE BINDINGS**

The future task produces Stage1 component-family reference geometry only.

It does not authorize:
- whole-hall 华栱 count closure;
- complete dougong/bracket-set assembly as a production asset;
- 56-instance building placement;
- Stage2;
- T-018 restart.

## 2. Identity Contract

Component id:

`CMP-GONG-HUAGONG-001`

Master id:

`CMP-GONG-HUAGONG-001_MASTER`

Master version:

`V001`

Task id:

`T-040｜P3_3_HUAGONG_MASTER_V2_V001`

Geometry variant identities:

- `JUMP_1_HUAGONG`
- `JUMP_2_HUAGONG`

Required Registry bindings:
- JUMP_1 = 28
- JUMP_2 = 28
- total = 56
- all remain `LOCKED_SUBSET`

Hard semantic boundary:

**56 is the current direction-explicit 正身 subset, not the historical whole-hall 华栱 total.**

Direction/location semantics remain instance/assembly metadata and may not create SOUTH/NORTH/EAST/WEST geometry variants.

## 3. Source Authority

Primary source:

`SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF SHA-256:

`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Locked evidence lineage:
- D-225: Source Readiness + D-076 = PASS WITH BOUNDARIES
- D-227: 华栱 Master Spec V0.1 = PRODUCT OWNER APPROVED / LOCKED

No secondary calculated value, generic Song template, 《营造法式》 template, or comparative-building geometry may override the same-building source boundary.

## 4. Variant Contract

Exactly:
- Master family count = **1**
- geometry variant count = **2**
- direction/location geometry variant count = **0**

Required:
- JUMP_1 and JUMP_2 keep independent variant identities;
- both are generated from one family architecture;
- each must have its own semantic/geometry signature after execution;
- each must consume its own locked future length/datum inputs;
- shared builder/validator infrastructure is allowed;
- shared evidence schema and profile-control methodology are allowed.

Forbidden:
- collapsing JUMP_1 and JUMP_2 into one body merely because direct standalone differences are unresolved;
- claiming distinct decorative/profile forms merely because jump roles differ;
- creating JUMP_2 by uniform/global scaling of a finished JUMP_1 mesh;
- creating JUMP_1 by uniform/global scaling of a finished JUMP_2 mesh;
- direction/location-specific variants without new evidence;
- per-instance duplicate Masters.

## 5. Length / Assembly Control Contract

Current executable length status:

### JUMP_1_HUAGONG
- direct standalone full length = `UNRESOLVED`
- Stage1 canonical/reconstruction reference length = **NOT LOCKED**

### JUMP_2_HUAGONG
- direct standalone full length = `UNRESOLVED`
- later calculated full length ≈ **1630 mm**
- later calculated centre length ≈ **1464.8 mm**
- classification = `SECONDARY_CALCULATED / REPLACEABLE / NOT_DIRECT_PRIMARY`
- Stage1 canonical/reconstruction reference length = **NOT LOCKED**

Direct assembly-level evidence:

第一、二跳总出跳:
- observed mean = **732.4 mm**
- min = **704 mm**
- max = **755 mm**
- variance = **115.61**
- n = **46**
- classification = `DIRECT_PRIMARY / OBSERVED_MEAN / ASSEMBLY_LEVEL_COMBINED_PROJECTION`

This value is not:
- JUMP_1 full member length;
- JUMP_2 full member length;
- JUMP_1 + JUMP_2 full-member-length sum;
- per-instance exact geometry;
- proven 963 original design.

### Mandatory pre-execution Gate A

Before any engineering execution can be authorized, a separate:

`HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V0.1`

must be Product Owner approved and locked.

It must define at minimum:

1. deterministic Stage1 JUMP_1 reconstruction reference length;
2. deterministic Stage1 JUMP_2 reconstruction reference length;
3. evidence classification and provenance for each selected length;
4. section width/thickness rule;
5. JUMP_1 local origin / assembly datum;
6. JUMP_2 local origin / assembly datum;
7. deterministic two-jump validation-fixture placement rule;
8. exact measurement definition for "第一、二跳总出跳";
9. proof that the validation fixture reproduces the locked **732.4 mm observed-mean combined projection constraint** within an explicitly declared deterministic tolerance;
10. separate retention of the report's **48分** ideal-model rule as `REPORT_INFERRED / REPORT_IDEAL_MODEL / REPLACEABLE`;
11. deterministic version/signature;
12. Product Owner approval.

Explicit prohibitions:
- `JUMP_1_FULL_LENGTH = 732.4`;
- `JUMP_2_FULL_LENGTH = 732.4`;
- `JUMP_1_FULL_LENGTH + JUMP_2_FULL_LENGTH = 732.4` by assumption;
- promotion of 1630 / 1464.8 mm to DIRECT_PRIMARY;
- invented hidden overlap used to force the 732.4 mm result;
- claiming 732.4 mm as a per-instance exact or 963-original value.

Until Gate A is locked:
- neither geometry variant is executable;
- no canonical body may be generated;
- no builder may freeze any member length, section, local datum or assembly fixture.

## 6. Section Control Contract

Current source-supported report envelope:
- material width band = **214.1–218.9 mm**
- material thickness band = **154.0–156.9 mm**
- report ideal model = **14分 width / 10分 thickness**
- Yingzao ruler used by report synthesis = **306 mm**

Current boundary:
- no 华栱-specific standalone direct width mean is locked;
- no 华栱-specific standalone direct thickness mean is locked.

The future Gate A must select deterministic Stage1 section values and classify them explicitly as:

`REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`

unless stronger component-specific direct evidence is established.

Forbidden:
- importing T-037 / T-038 / T-039 width or thickness as 华栱 authority;
- selecting an arbitrary value inside the report band without an explicit rule;
- relabeling report ideal-model values as direct 华栱 measurements.

## 7. Profile Control Contract

Current status:
- same-building visual/form evidence = sufficient for bounded Stage1 reconstruction;
- exact standalone historical profile = `UNRESOLVED`;
- exact numeric profile controls = `UNRESOLVED`;
- exact end shaping = `UNRESOLVED`;
- metric image calibration = `NOT PERFORMED / NOT CLAIMED`.

### Mandatory pre-execution Gate B

After Gate A is locked and before engineering execution can be authorized, a separate:

`HUAGONG_PROFILE_CONTROL_SET_V0.1`

must be Product Owner approved and locked.

It must provide at minimum:

1. explicit deterministic numeric control set;
2. coordinate meaning tied to the locked Gate A section/datum convention;
3. same-building source references;
4. human-reviewable comparison against the approved same-building form envelope;
5. explicit classification:
   `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
6. explicit statement that metric image calibration is not claimed unless actually performed;
7. explicit mapping rule for JUMP_1 and JUMP_2;
8. proof that neither variant is created by copying/scaling a finished mesh of the other;
9. deterministic version/signature;
10. Product Owner approval.

Default profile rule:
- JUMP_1 and JUMP_2 share the same profile-control **methodology** unless new evidence supports a difference;
- different member lengths alone do not establish different historical profile forms;
- the Profile Control Set must explicitly define how common/source-guided controls are applied independently to each variant after Gate A resolves dimensions.

Explicitly forbidden:
- copying T-037 瓜子栱 control points;
- copying T-038 慢栱 control points;
- copying T-039 令栱 control points;
- averaging / morphing prior gong control sets;
- generic Song / 《营造法式》 substitution;
- comparative-building geometry as Wanfo authority;
- aesthetic free-form invention presented as evidence.

## 8. Coordinate Contract

Family semantic axes remain:

- +X = 华栱 longitudinal / out-jump axis
- +Y = member width axis
- +Z = vertical / profile-thickness axis

The exact local origin and assembly reference datum are **not locked by this Task Contract Candidate**.

They must be locked by Gate A.

After Gate A:
- each variant shall use deterministic family-local coordinates;
- canonical body transforms shall be location = [0,0,0], rotation = [0,0,0], scale = [1,1,1] unless the locked Definition establishes an equivalent deterministic representation;
- building/world placement remains outside Master geometry.

No building placement may be baked into the canonical Master bodies.

## 9. Geometry Construction Contract

Only after:
1. Task Contract lock;
2. Gate A Length/Assembly Control Set lock;
3. Gate B Profile Control Set lock;
4. explicit Engineering Execution Authorization;

may implementation begin.

Future Stage1 construction must:
- generate JUMP_1 independently from its locked Definition;
- generate JUMP_2 independently from its locked Definition;
- preserve the one-family/two-variant identity architecture;
- consume locked section, length, datum and profile controls;
- avoid global-scale derivation of one finished variant from the other;
- avoid geometry reuse from T-037/T-038/T-039 as authority;
- keep all unsupported connection details absent.

## 10. First Article Contract

The future First Article shall contain exactly **two canonical production bodies**:

1. `JUMP_1_HUAGONG`
2. `JUMP_2_HUAGONG`

Additionally, validation shall build one:

`TWO_JUMP_ASSEMBLY_FIXTURE_VALIDATION_ONLY`

This fixture is:
- validation-only;
- non-canonical;
- not a third geometry variant;
- not a Catalog asset;
- not a Registry binding;
- not whole-bracket-set production geometry;
- not evidence of historical hidden connection geometry.

Its sole purposes are:
- place locked JUMP_1/JUMP_2 reference bodies using Gate A datums;
- make the combined-projection measurement explicit;
- prove the locked 732.4 mm observed-mean assembly constraint;
- expose any illegal use of full-member lengths as projection distances.

No 56-instance building placement is allowed before Product Owner First Article approval.

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

Review evidence shall expose the following domains independently. The implementation may combine domains into fewer panels only if each remains clearly readable:

1. `FAMILY_AND_56_SUBSET_SCOPE`
2. `JUMP_1_CANONICAL_BODY`
3. `JUMP_2_CANONICAL_BODY`
4. `TWO_VARIANT_DIMENSION_AND_IDENTITY_PROOF`
5. `TWO_JUMP_ASSEMBLY_FIXTURE_AND_732_4_PROJECTION_PROOF`
6. `SECTION_EVIDENCE_AND_REPORT_IDEAL_MODEL_BOUNDARY`
7. `PROFILE_PROVENANCE_AND_CONTROL_SET_CLASSIFICATION`
8. `SOURCE_VS_RECONSTRUCTION_BOUNDARY`
9. `UNKNOWN_DEFERRED_AND_NO_JOINERY_PROOF`

Review evidence must make it possible to detect:
- accidental JUMP_1/JUMP_2 collapse;
- uniform mesh scaling;
- invented JUMP_1 length;
- secondary JUMP_2 value marked direct;
- 732.4 treated as member length or sum of member lengths;
- 48分 treated as direct measurement;
- unsupported direction/location variants;
- profile reuse from prior gong Masters;
- unsupported end/joinery invention;
- blank or near-uniform renders.

## 12. Validation Contract

Future machine validation must verify at minimum:

### Registry / identity
- Registry schema = V008
- Registry total = 505
- target 华栱 subset records = 56
- count status = LOCKED_SUBSET
- JUMP_1 bindings = 28
- JUMP_2 bindings = 28
- direction distribution = each direction 7 JUMP_1 + 7 JUMP_2
- whole-hall count closed = false
- Master family count = 1
- geometry variant count = 2
- direction geometry variant count = 0

### Evidence semantics
- 732.4 mm classification remains DIRECT_PRIMARY / OBSERVED_MEAN / ASSEMBLY_LEVEL_COMBINED_PROJECTION / n=46
- 732.4 is not standalone member length
- 732.4 is not full-length sum
- per-instance exact claim = false
- original-963 fact claim = false
- sample-to-instance mapping = UNKNOWN
- 48分/14分/10分 remain REPORT_INFERRED / REPORT_IDEAL_MODEL / REPLACEABLE
- JUMP_2 1630/1464.8 remains SECONDARY_CALCULATED / REPLACEABLE / NOT_DIRECT_PRIMARY

### Pre-execution controls
- approved Gate A id/version/signature present
- approved JUMP_1 reconstruction reference length present
- approved JUMP_2 reconstruction reference length present
- approved section rule present
- approved local datums present
- approved 732.4 measurement rule present
- approved Gate B id/version/signature present
- profile classification remains SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT
- prior-gong profile reuse = false

### Geometry / reproducibility
- exactly two canonical bodies
- JUMP_1 and JUMP_2 separate semantic/geometry signatures
- neither canonical body is produced by uniform global scaling of the other
- validation fixture is tagged non-canonical
- validation fixture does not create Registry/Catalog identity
- combined-projection fixture result satisfies Gate A's locked tolerance around 732.4 mm
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

- `HUAGONG_SUBSET_COUNT_NOT_56`
- `WHOLE_HALL_COUNT_FALSE_CLOSURE`
- `JUMP_1_BINDING_COUNT_NOT_28`
- `JUMP_2_BINDING_COUNT_NOT_28`
- `DIRECTION_DISTRIBUTION_INVALID`
- `MASTER_FAMILY_COUNT_NOT_1`
- `GEOMETRY_VARIANT_COUNT_NOT_2`
- `DIRECTION_GEOMETRY_VARIANT_CREATED`
- `JUMP_ROLE_COLLAPSED_WITHOUT_EVIDENCE`
- `JUMP_1_LENGTH_NOT_LOCKED`
- `JUMP_2_LENGTH_NOT_LOCKED`
- `JUMP_1_LENGTH_INVENTED`
- `JUMP_2_SECONDARY_LENGTH_MARKED_DIRECT`
- `COMBINED_PROJECTION_USED_AS_MEMBER_LENGTH`
- `FULL_LENGTH_SUM_EQUATED_TO_732_4`
- `ASSEMBLY_PROJECTION_RULE_NOT_LOCKED`
- `ASSEMBLY_FIXTURE_732_4_CONSTRAINT_FAIL`
- `HIDDEN_OVERLAP_INVENTED_TO_FORCE_PROJECTION`
- `OBSERVED_MEAN_MARKED_PER_INSTANCE_EXACT`
- `OBSERVED_MEAN_MARKED_ORIGINAL_963_DESIGN`
- `SAMPLE_TO_INSTANCE_MAPPING_INVENTED`
- `REPORT_IDEAL_MODEL_MARKED_DIRECT`
- `SECTION_CONTROL_NOT_LOCKED`
- `SECTION_MARKED_DIRECT_WITHOUT_EVIDENCE`
- `LENGTH_ASSEMBLY_CONTROL_SET_NOT_PO_APPROVED`
- `LENGTH_ASSEMBLY_CONTROL_SIGNATURE_MISSING`
- `PROFILE_CONTROL_SET_NOT_PO_APPROVED`
- `PROFILE_CONTROL_SET_NOT_VERSIONED`
- `PROFILE_CONTROL_SIGNATURE_MISSING`
- `PROFILE_SOURCE_NOT_RECORDED`
- `PROFILE_MARKED_DIRECT_MEASUREMENT`
- `GUAZI_PROFILE_CONTROL_REUSE`
- `MANGONG_PROFILE_CONTROL_REUSE`
- `LINGGONG_PROFILE_CONTROL_REUSE`
- `PRIOR_GONG_GEOMETRY_REUSE_AS_AUTHORITY`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `COMPARATIVE_BUILDING_GEOMETRY_REUSE_AS_AUTHORITY`
- `JUMP_VARIANT_CREATED_BY_UNIFORM_MESH_SCALE`
- `UNSUPPORTED_END_SHAPE`
- `UNSUPPORTED_JOINERY_OR_LOCAL_CUTS`
- `VALIDATION_FIXTURE_PROMOTED_TO_CANONICAL_ASSET`
- `BUILDING_PLACEMENT_BAKED_INTO_MASTER`
- `REVIEW_RENDER_NEAR_UNIFORM`
- `SILENT_HISTORICIZATION`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 14. Deferred / Unsupported Geometry

Remain explicitly unresolved or deferred:
- exact historical JUMP_1 standalone full length;
- exact historical JUMP_2 standalone full length;
- exact hidden overlap;
- exact historical side profile;
- exact historical profile control dimensions;
- exact end shoulder/notch;
- mortise-tenon geometry;
- grooves;
- slots;
- cavities;
- hidden connection cuts;
- unmeasured chamfers;
- wear/damage/warp;
- per-instance deformation;
- per-instance originality/repair state;
- whole-hall 华栱 total count;
- sample-to-instance mapping.

Assembly convenience is not evidence.

## 15. Scope Protection

The future task must not:
- reactivate T-018;
- start Stage2;
- modify T-020 shared datum authority;
- modify approved T-037/T-038/T-039 canonical geometry;
- use prior gong control polygons as 华栱 authority;
- broaden the validation fixture into a production bracket-set assembly;
- create 56 building-placement instances as First Article output;
- formalize Catalog/V008 before Product Owner First Article approval and explicit formalization authorization;
- merge before post-formalization readiness PASS and explicit Product Owner Ready+Merge approval.

## 16. Locked Gate Sequence

1. Source Readiness + D-076 — **PASS / D-225**
2. Master Spec V0.1 — **LOCKED / D-227**
3. Task Contract — **LOCKED / PRODUCT OWNER APPROVED / D-229**
4. Length/Assembly Control Set V0.1 — **LOCKED / PRODUCT OWNER APPROVED / D-231**
5. Profile Control Set V0.1 — **LOCKED / PRODUCT OWNER APPROVED / D-233**
6. Engineering Execution Authorization — **AUTHORIZED / D-234**
7. First Article machine validation — **PASS / D-235 / 76 OF 76**
8. Product Owner First Article Approval — **APPROVED / D-236**
9. Formalization + Catalog/V008/CURRENT binding — **COMPLETE / D-238**
10. Derived Excel + latest-head/shared regressions + readiness — **NOT AUTHORIZED**
11. D-194 combined Draft→Ready + Merge — **NOT AUTHORIZED**
12. Formal Closure — **NOT AUTHORIZED**

Ordering rule:

**Gate A Length/Assembly Control must lock before Gate B Profile Control.**

Reason:
the profile-control application requires a stable section/datum/length architecture; reversing the order would create avoidable rework and could silently bind a profile to an unapproved scale or assembly datum.

## 17. Task Contract Lock｜D-229

Product Owner approved D-228 Candidate 01 without changing its technical architecture or evidence boundaries.

D-229 formally:
- locks this Task Contract as the canonical contract for `T-040｜P3_3_HUAGONG_MASTER_V2_V001`;
- creates/activates the T-040 engineering task identity;
- preserves one `CMP-GONG-HUAGONG-001_MASTER` family;
- preserves two independent variants `JUMP_1_HUAGONG` / `JUMP_2_HUAGONG`;
- preserves 28 + 28 = 56 V008 `LOCKED_SUBSET` bindings;
- preserves zero direction/location geometry variants;
- locks the mandatory pre-execution sequence:
  1. `HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V0.1`;
  2. `HUAGONG_PROFILE_CONTROL_SET_V0.1`;
  3. separate Engineering Execution Authorization.

Evidence boundaries remain unchanged:
- 732.4 mm / n=46 = `DIRECT_PRIMARY / OBSERVED_MEAN / ASSEMBLY_LEVEL_COMBINED_PROJECTION`;
- 732.4 mm is not either standalone member length and is not the sum of member full lengths;
- JUMP_1 standalone full length = `UNRESOLVED`;
- JUMP_2 direct standalone full length = `UNRESOLVED`;
- 1630 / 1464.8 mm = `SECONDARY_CALCULATED / REPLACEABLE / NOT_DIRECT_PRIMARY`;
- 48分 / 14分 / 10分 = `REPORT_INFERRED / REPORT_IDEAL_MODEL / REPLACEABLE`;
- exact profile/end/hidden overlap = `UNRESOLVED`;
- hidden joinery = `DEFERRED`;
- whole-hall 华栱 count remains `NOT CLOSED`;
- sample-to-instance mapping remains `UNKNOWN`.

D-229 does **not** authorize:
- production branch creation;
- PR creation;
- builder implementation;
- Length/Assembly Control Set adoption;
- Profile Control Set adoption;
- GitHub Actions / Blender execution;
- First Article generation;
- formalization;
- Catalog/V008/CURRENT binding;
- Derived Excel synchronization;
- Ready/Merge;
- closure;
- Stage2;
- T-018 resume.

Current status:

**T-040 TASK CONTRACT LOCKED / ENGINEERING TASK IDENTITY ACTIVE / ENGINEERING EXECUTION BLOCKED**

Next complete step:

**design HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V0.1 Candidate.**

## 18. Length / Assembly Control Set Candidate｜D-230

D-230 prepares `HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01` for Product Owner review. Candidate architecture separates Master reference-specimen lengths from unresolved per-instance historical full lengths. Proposed reference specimens: JUMP_1=898.8mm (2.8M secondary-hypothesis-guided / reference-only), JUMP_2=1630.0mm (SECONDARY_CALCULATED / reference-only); family section=214.2×153.0mm from report 14分/10分 ideal-model synthesis. The validation fixture uses D0=0, D1=366.2, D2=732.4mm; only D0→D2=732.4 is direct-primary, while the equal midpoint split is project/reconstruction guidance and not an observed per-jump fact. Report 48分=734.4mm remains a separate cross-check. Candidate is NOT LOCKED; instance full lengths remain UNRESOLVED and engineering execution remains blocked.

## 19. Length / Assembly Control Set Approval｜D-231

Product Owner approved and locked `HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01` without changing D-230 numerical controls or evidence semantics. Locked control SHA-256=`ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b`. Canonical Stage1 reference controls are JUMP_1 reference specimen 898.8mm, JUMP_2 reference specimen 1630.0mm, family section 214.2×153.0mm, and validation fixture D0/D1/D2=0/366.2/732.4mm. Only D0→D2=732.4mm remains DIRECT_PRIMARY assembly-level observed mean; D1 is reconstruction/project-fixture guidance. All 56 instance historical standalone full lengths remain UNRESOLVED. Gate A is now CLOSED/PASS. Gate B `HUAGONG_PROFILE_CONTROL_SET_V0.1` is next. Engineering execution, branch/PR, builder/Blender, First Article and formalization remain unauthorized.

## 20. Profile Control Set Candidate｜D-232

D-232 prepares `HUAGONG_PROFILE_CONTROL_SET_V001_C01` for Product Owner review. Candidate uses an independently constructed 16-point bilateral normalized profile with SHA `f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`, classification `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`, and same-building SRC-ZG-WF-001 p73–76 as qualitative form/envelope authority only. It does not copy, scale, average or morph the T-037/T-038/T-039 control polygons. Both JUMP_1 and JUMP_2 use the same normalized controls but are evaluated independently against locked Gate A reference envelopes 898.8×214.2×153.0mm and 1630.0×214.2×153.0mm; W/T do not scale by length ratio and no finished-mesh uniform scaling is permitted. Candidate is NOT LOCKED. Engineering execution remains blocked pending Product Owner Gate B approval plus a separate execution authorization.

## 21. Profile Control Set Approval｜D-233

Product Owner approved and locked `HUAGONG_PROFILE_CONTROL_SET_V001_C01` without changes to D-232 Candidate 01. Locked profile SHA-256=`f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`; point count=16; classification remains `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`. JUMP_1/JUMP_2 share the same normalized controls but must be evaluated independently against D-231 Gate A envelopes; W/T remain fixed and finished-mesh uniform scaling is prohibited. Gate B is CLOSED/PASS. Engineering execution remains a separate authorization gate and is still blocked; no branch/PR/builder/Blender/First Article/formalization is authorized by D-233.

## 22. Engineering Execution Authorization｜D-234

Product Owner authorized isolated T-040 engineering execution after Gate A D-231 and Gate B D-233 were both locked.

Authorized engineering scope:
- create/use production branch `codex/t040-p3-3-huagong-master-v2-v001`;
- implement one T-040 Definition consuming the locked Gate A + Gate B controls;
- implement builder / validator / GitHub Actions workflow;
- use Blender **4.5.13** for canonical generation;
- generate exactly two canonical First Article bodies:
  - `JUMP_1_HUAGONG`;
  - `JUMP_2_HUAGONG`;
- generate one `TWO_JUMP_ASSEMBLY_FIXTURE_VALIDATION_ONLY` non-canonical fixture;
- validate D0→D2 = **732.4 mm** within the locked Gate A machine tolerance;
- perform deterministic rebuild + independent reopen checks;
- generate review evidence covering all locked Task Contract domains;
- create a **Draft PR** for Product Owner review.

Locked inputs:
- Gate A: `HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01`
  - SHA `ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b`;
- Gate B: `HUAGONG_PROFILE_CONTROL_SET_V001_C01`
  - SHA `f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`.

Required canonical First Article envelopes:
- JUMP_1 reference specimen = **898.8 × 214.2 × 153.0 mm**;
- JUMP_2 reference specimen = **1630.0 × 214.2 × 153.0 mm**.

Required profile rule:
- both variants use the locked independent 16-point normalized 华栱 control set;
- each body is generated independently from the locked Definition;
- no finished-mesh uniform scaling;
- W/T must not scale with length ratio.

Required fixture rule:
- D0 = 0.0 mm;
- D1 = 366.2 mm, reconstruction/project-fixture guidance only;
- D2 = 732.4 mm;
- only D0→D2 is the DIRECT_PRIMARY assembly metric assertion;
- the fixture is not a third canonical asset and shall not bind Registry/Catalog.

D-234 does **not** authorize:
- Product Owner First Article acceptance;
- formalization;
- Catalog/V008/CURRENT binding;
- Derived Excel synchronization;
- Draft→Ready transition;
- merge;
- closure;
- Stage2;
- T-018 resume.

Current execution state:

**ENGINEERING EXECUTION AUTHORIZED / FIRST ARTICLE MACHINE VALIDATION NEXT**


### D-234 branch creation result

Production branch created successfully:

`codex/t040-p3-3-huagong-master-v2-v001`

Base commit:

`7c4dc0d88bc928ea1abe73a1109172a95a69c67a`

This branch creation does not itself start First Article generation or expand the D-234 authorization boundary.


## 23. First Article Machine Result｜D-235

Final machine run:

- Workflow: `T-040 Huagong Master First Article`
- Run ID: **36317889355**
- Run number: **3**
- execution head: `51fc6e2a506a5950dc14f52d5aac0378872a531d`
- result: **SUCCESS**
- machine checks: **76 / 76 PASS**
- Draft PR: **#36**
- artifact: `P3_3_T040_HUAGONG_MASTER_V2_FIRST_ARTICLE_V001`
- Artifact ID: **10930899677**
- artifact digest: `sha256:de25a9031bd096ff2313b4a37d14aa821c480c13e46372113cb40f647a21781f`
- artifact expiry: **2026-10-27**
- canonical .blend SHA-256: `0748069370c0c3eb4da6eec26038f2498b7eb2fc8defedb1ebd70486029efb2e`
- family semantic signature: `0052a572ff7b546ca89ab251a945ad54a1621e0139fb9cabb278a17c1a65ae77`
- JUMP_1 geometry signature: `565fcdef9335691e73dd0cbec5e5d98b561f3bdebdbd367951bcb7826dc8f19a`
- JUMP_2 geometry signature: `451511f0b131e36784baefa2011850a1f9381d3b2dc1fee629951b7f4099e001`
- Gate A signature verified: `ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b`
- Gate B signature verified: `f9a96a20466d523a91c13ad85f5678c085963f5b826a35047843fb3ee1d46e8e`
- fixture combined projection: **732.4 mm**
- Blender: **4.5.13 LTS**

Machine evidence confirms:
- exactly two canonical bodies;
- JUMP_1 = 898.8 × 214.2 × 153.0 mm reference specimen;
- JUMP_2 = 1630.0 × 214.2 × 153.0 mm reference specimen;
- separate deterministic geometry signatures;
- no finished-mesh uniform scaling;
- fixture remains non-canonical / non-Registry / non-Catalog;
- D0/D1/D2 = 0 / 366.2 / 732.4 mm;
- only D0→D2 = 732.4 mm carries DIRECT_PRIMARY assembly-level semantics;
- all 56 instance historical standalone full lengths remain UNRESOLVED;
- unsupported end/joinery details remain absent;
- deterministic reopen and restore signatures match;
- 9-domain Review Board and all six technical renders are nonblank.

Run history:
- Run #1 (36317398213): geometry/reopen/restore/Review Board passed; validator stopped at profile SHA numeric-serialization normalization.
- Run #2 (36317658877): geometry/reopen/restore passed; validation patch contained a literal-newline syntax defect.
- Run #3 (36317889355): normalization syntax corrected; **76/76 PASS**.

The two earlier failures did not change the locked Gate A/Gate B geometry controls.

D-235 is a machine-gate result only.

It does **not** constitute Product Owner First Article acceptance and does not authorize:
- formalization;
- Catalog/V008/CURRENT binding;
- Derived Excel synchronization;
- PR Draft→Ready;
- merge;
- closure;
- Stage2;
- T-018 resume.

Current status:

**FIRST ARTICLE MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**


## 24. First Article Product Owner Approval｜D-236

Product Owner formally approved the actual machine-generated T-040 First Article artifact package.

Accepted evidence:
- Run ID: 36317889355
- Artifact ID: 10930899677
- Artifact digest: sha256:de25a9031bd096ff2313b4a37d14aa821c480c13e46372113cb40f647a21781f
- canonical .blend SHA-256: 0748069370c0c3eb4da6eec26038f2498b7eb2fc8defedb1ebd70486029efb2e
- Semantic SHA-256: e3264826dce4d747aa4c73ddbaa2ec29a042859b9f3f611a35fca8b999ae2ef9
- Validation SHA-256: ccb7baaee7e1e3e7c7f69d474bd77d97b22491998c1973152273fd4a87b3ee81
- Review Board SHA-256: 54d4c79bd83e23c6ac31c330323fce70e0a83f7a1c2f2d1355c2e9d3f16af2f1
- family semantic signature: 0052a572ff7b546ca89ab251a945ad54a1621e0139fb9cabb278a17c1a65ae77
- JUMP_1 geometry signature: 565fcdef9335691e73dd0cbec5e5d98b561f3bdebdbd367951bcb7826dc8f19a
- JUMP_2 geometry signature: 451511f0b131e36784baefa2011850a1f9381d3b2dc1fee629951b7f4099e001

Approval covers the real Blender artifact only; illustrative review images are excluded from the canonical evidence chain.

Formalization / Catalog binding / PR Ready / merge remain NOT AUTHORIZED.


## 25. Formalization + Catalog/V008/CURRENT Binding Authorization｜D-237

Product Owner authorized formalization and Stage1 Catalog/V008/CURRENT binding after D-236.

Authorization target:
- verify accepted Artifact 10930899677 and D-236 accepted hashes;
- materialize formal Semantic / Validation / Review Board package;
- keep canonical .blend Actions-artifact/local-only/not-Git;
- add one approved Master family CMP-GONG-HUAGONG-001_MASTER with JUMP_1_HUAGONG + JUMP_2_HUAGONG;
- bind exactly 56 华栱 V008/CURRENT rows: 28 JUMP_1 + 28 JUMP_2;
- update coverage only after successful binding: 24/28 = 85.7%, 331 covered;
- preserve LOCKED_SUBSET / not-whole-hall and per-instance historical full-length UNRESOLVED semantics.

Derived Excel, readiness, PR Ready/Merge and closure remain NOT AUTHORIZED.

Current status:
**FORMALIZATION AUTHORIZED / EXECUTION PENDING**

## 26. Formalization Result｜D-238

D-238 records successful formalization under D-237. Catalog branch count = 24/28 = 85.7%; all 56 Huagong V008/CURRENT LOCKED_SUBSET rows are bound to CMP-GONG-HUAGONG-001_MASTER with JUMP_1/JUMP_2 28/28; master-covered records = 331; CURRENT==V008. Accepted canonical blend remains D-236 SHA 0748069370c0c3eb4da6eec26038f2498b7eb2fc8defedb1ebd70486029efb2e. The 898.8/1630.0 controls remain reference-specimen-only and do not close per-instance historical standalone lengths. Derived Excel sync, post-formalization regression/readiness, Ready/Merge and closure remain separate gates.

## 27. Post-Formalization Verification Authorization｜D-239

Product Owner authorized the complete post-formalization verification sequence after D-238:

- Derived Excel sync from synchronized CURRENT;
- Excel validation against 505 rows / 24 approved Masters / 331 covered;
- latest-head T-040 deterministic rebuild/reopen regression;
- accepted family + JUMP_1 + JUMP_2 geometry signature comparison against D-236;
- shared regressions: T-021 / T-022 / T-023 / T-024 / T-037 / T-038 / T-039;
- generic P3.3 route ownership check for dedicated T-040;
- PR #36 readiness review.

Regression-only generated .blend must not replace the D-236 accepted canonical .blend.

D-239 does **not** authorize:
- PR #36 Draft→Ready;
- merge;
- closure;
- Stage2;
- T-018 resume.

Current status:

**POST-FORMALIZATION VERIFICATION AUTHORIZED / EXECUTION IN PROGRESS**

## 28. Post-Formalization Verification Result｜D-240

D-240 records successful completion of the D-239 verification gate. Final run **36323489326** completed SUCCESS. Derived Excel is synchronized to 505 rows / 24 approved Masters / 331 covered records with SHA `53583e21d3d418c260b39fa7f44cb5eade02009081b494eecba0985d7d4b86aa`. T-040 latest-head rebuild/reopen/restore validation returned **76/76 PASS** and preserved the accepted family/JUMP_1/JUMP_2 geometry signatures; regenerated blend SHA `be9e386a289a64e35d8f14f47e6d88e6ef45cc697ab8474a69392e5222b42199` is regression-only and is not promoted to canonical. Shared regressions T-021/T-022/T-023/T-024/T-037/T-038/T-039 all PASS. The T-039 validator required a lifecycle-only Review Patch because its old first-article assertion still required merge/closure to be unauthorized; geometry and evidence semantics were unchanged. Generic P3.3 Master V2 exclusion for T-040 is PASS. Readiness is **READY_FOR_PRODUCT_OWNER_READY_MERGE_DECISION**. PR #36 remains Draft; Ready/Merge/Closure remain separate Product Owner gates.
