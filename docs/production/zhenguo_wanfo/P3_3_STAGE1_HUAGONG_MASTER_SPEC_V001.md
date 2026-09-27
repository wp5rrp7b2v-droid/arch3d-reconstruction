# P3.3 Stage1｜华栱 Master Spec V0.1

Status: **CANDIDATE 01 / PRODUCT OWNER REVIEW REQUIRED / D-226**
Date: 2026-09-27
Stage: P3.3 V002 Stage 1
Source Gate: D-225｜Source Readiness + D-076 PASS WITH BOUNDARIES

## 1. Scope

Target component:
- 中文名：华栱
- V008 Registry target：**56 LOCKED_SUBSET records**
- subset distribution：
  - 南：JUMP_1 7 + JUMP_2 7
  - 北：JUMP_1 7 + JUMP_2 7
  - 东：JUMP_1 7 + JUMP_2 7
  - 西：JUMP_1 7 + JUMP_2 7
- total：**JUMP_1 28 + JUMP_2 28**
- Coverage Matrix priority：18
- Stage1 disposition：需新建Master
- historical whole-hall 华栱 total：**NOT CLOSED**

Hard scope boundary:

**The 56 Registry records are a direction-explicit 正身 subset, not a claim that the whole hall contains only 56 华栱.**

Proposed identity:
- component id：`CMP-GONG-HUAGONG-001`
- master id：`CMP-GONG-HUAGONG-001_MASTER`
- master version：V001
- master family count：**1**
- geometry variant identities：**2**
  - `JUMP_1_HUAGONG`
  - `JUMP_2_HUAGONG`

Proposed architecture:

**ONE PARAMETRIC MASTER FAMILY / TWO INDEPENDENT JUMP VARIANT IDENTITIES / 56 SUBSET INSTANCE BINDINGS**

The two variant identities are intentionally kept separate because:
1. the primary source and Registry distinguish first-jump and second-jump assembly positions;
2. the source does not prove that their standalone full geometry is identical;
3. collapsing them into one body now would silently assert equality that is not evidenced;
4. keeping separate variant identities does **not** claim that their historical profiles or every dimension differ—it only prevents unsupported forced equivalence.

Direction and location do not create additional geometry variants.

## 2. Primary source and evidence bindings

Primary authority:

`SRC-ZG-WF-001｜《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF SHA-256:

`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

### Direct assembly-level evidence

PDF p71 / printed p56 / §2.2.4.2 / Fig.2-25 / Table 2-33:

第一、二跳总出跳:
- observed mean = **732.4 mm**
- minimum = **704 mm**
- maximum = **755 mm**
- variance = **115.61**
- n = **46**
- classification = `DIRECT_PRIMARY / OBSERVED_MEAN / ASSEMBLY_LEVEL_COMBINED_PROJECTION`

This value is **not**:
- JUMP_1 full member length;
- JUMP_2 full member length;
- JUMP_1 + JUMP_2 full-member-length sum;
- per-instance exact geometry;
- proven 963 original design.

Sample-to-instance mapping:
`UNKNOWN`

### Report ideal-model evidence

PDF p72 / printed p57 / §2.2.4.4 / Table 2-35 and PDF p120 / printed p105:

- first+second total projection = **48分** in the report's ideal-model synthesis;
- single-material width tends toward **14分**;
- material thickness baseline = **10分**;
- report uses 营造尺 = **306 mm**;
- classification = `REPORT_INFERRED / REPORT_IDEAL_MODEL / REPLACEABLE`.

The report also presents measured/synthesized material bands:
- single-material width band = **214.1–218.9 mm**
- material thickness band = **154.0–156.9 mm**

No 华栱-specific standalone raw width/thickness mean is locked by this Master Spec.

## 3. Variant architecture

### JUMP_1_HUAGONG

Role:
- first-jump 华栱 identity
- Registry bindings = **28**

Current full-length status:
- direct standalone full length = **UNRESOLVED**
- canonical Stage1 full length = **NOT YET LOCKED**

### JUMP_2_HUAGONG

Role:
- second-jump 华栱 identity
- Registry bindings = **28**

Current full-length status:
- direct standalone full length = **UNRESOLVED**
- existing later/calculated full length ≈ **1630 mm**
- existing later/calculated centre length ≈ **1464.8 mm**
- classification of those later values = `SECONDARY_CALCULATED / REPLACEABLE / NOT_DIRECT_PRIMARY`
- canonical Stage1 full length = **NOT YET LOCKED**

### Sharing rule

The two variants may share:
- component-family identity;
- topology strategy;
- coordinate convention;
- source-guided profile method;
- section-control method;
- builder/validator infrastructure;
- evidence schema.

They may **not** be forced to share:
- standalone full length;
- assembly reference datum;
- hidden overlap;
- any dimension that future same-building control evidence shows to be role-specific.

They may not receive distinct decorative/profile forms unless evidence supports that distinction.

## 4. Length / assembly policy

A separate mandatory pre-engineering gate is required:

`HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V0.1`

It must lock, at minimum:
1. deterministic JUMP_1 standalone reference length;
2. deterministic JUMP_2 standalone reference length;
3. local assembly reference datum for each variant;
4. definition of how "总出跳" is measured in the future assembly fixture;
5. proof that the reconstructed two-jump assembly respects the direct **732.4 mm observed-mean combined projection** as an evidence constraint;
6. separate reporting of the report ideal-model **48分** rule;
7. explicit classification of every reconstructed length as `RECONSTRUCTED / REPLACEABLE / NOT_DIRECT_MEASUREMENT` unless a stronger direct source is established;
8. deterministic signature / versioning;
9. Product Owner approval.

Explicit prohibition:

**The control set may not set JUMP_1_length + JUMP_2_length = 732.4 mm merely because 732.4 mm is the combined projection.**

Full member length and assembly projection are different measurement boundaries.

The existing 1630 / 1464.8 mm JUMP_2 values may be used only as secondary calculated evidence and may not be promoted to direct measurement.

Until this gate is approved:
- neither variant has an executable canonical full length;
- no canonical Blender body may be generated;
- no builder may freeze a member length.

## 5. Section policy

This Master Spec does **not** promote a 华栱-specific direct section dimension.

Permitted evidence envelope:
- report material width band = **214.1–218.9 mm**
- report material thickness band = **154.0–156.9 mm**
- report ideal model = **14分 width / 10分 thickness**

Proposed Stage1 rule:
- section dimensions shall be resolved inside the Length/Assembly Control Set;
- the chosen section shall be explicitly classified `REPORT_INFERRED / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`;
- it shall not be described as a direct 华栱-specific observed mean unless a component-specific source table is established.

Forbidden:
- importing T-037 / T-038 / T-039 section values merely because they are all gong-family members;
- silently selecting a convenient value inside the band without a declared control rule.

## 6. Profile / form authority

Proposed:

`PROFILE_AUTHORITY = SAME_BUILDING_SOURCE_GUIDED_SIMPLIFIED / PROVISIONAL`

Same-building primary basis:
- PDF p73 / printed p58 / Fig.2-27 photograph + bracket-stack schematic;
- same-building outer-eaves dougong context and first/second jump relationships.

Evidence boundary:
- exact standalone historical side profile = `UNRESOLVED`
- exact numeric profile control dimensions = `UNRESOLVED`
- exact end shaping = `UNRESOLVED`
- source-image metric calibration = `NOT PERFORMED / NOT CLAIMED`

A separate mandatory pre-engineering gate is required:

`HUAGONG_PROFILE_CONTROL_SET_V0.1`

It must be:
- deterministic;
- versioned;
- visually reviewable;
- reproducible from locked numeric controls;
- explicitly `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
- grounded in approved same-building evidence.

Variant profile rule:
- JUMP_1 and JUMP_2 use the same profile-control method by default;
- a different profile shape between the two variants is prohibited unless evidence supports it;
- different lengths alone do not justify profile scaling.

Explicitly forbidden:
- copying T-037 瓜子栱 points;
- copying T-038 慢栱 points;
- copying T-039 令栱 points;
- averaging / morphing those prior control sets;
- generic Song / 《营造法式》 substitution;
- using 佛光寺、独乐寺、应县木塔、高平崇明寺 comparison geometry as Wanfo authority.

## 7. Coordinate / geometry convention

Future Definition must use a deterministic family-local coordinate system.

Proposed semantic axes:
- +X = 华栱 longitudinal / out-jump axis
- +Y = member width axis
- +Z = vertical / profile-thickness axis

However, the exact local origin / assembly datum is **not locked by this Candidate** because the hidden overlap and projection measurement boundary remain unresolved.

The Length/Assembly Control Set must lock:
- variant-local origin;
- assembly datum;
- forward projection reference;
- how the two variants are positioned in a deterministic test fixture.

No building world placement belongs inside the Stage1 Master geometry.

## 8. Registry binding rule

If later approved and formalized:
- `JUMP_1_HUAGONG` may bind only the 28 V008 一跳 records;
- `JUMP_2_HUAGONG` may bind only the 28 V008 二跳 records;
- north/south/east/west are assembly/instance semantics;
- no direction-specific geometry variants are permitted without evidence;
- no location-specific Master duplication is permitted;
- the 56-record binding must retain the `LOCKED_SUBSET` / not-whole-hall qualification.

Forbidden:
- claiming 56 is the whole-hall count;
- inventing unregistered extra bindings merely to make an assembly complete;
- mapping report n=46 samples to the 56 Registry rows.

## 9. Unsupported / deferred geometry

Explicitly UNRESOLVED / DEFERRED:
- exact historical JUMP_1 full length;
- exact historical JUMP_2 full length;
- exact hidden overlap;
- exact local assembly datum;
- exact historical side profile;
- exact profile control dimensions;
- exact end shoulder / notch;
- mortise-tenon geometry;
- grooves;
- slots;
- cavities;
- hidden connection cuts;
- unmeasured chamfers;
- wear / damage / warp;
- per-instance deformation;
- per-instance originality / repair state;
- whole-hall 华栱 total count;
- sample-to-instance mapping.

None may be filled for visual plausibility or modeling convenience.

## 10. First-Article review intent

A future first article must make at least these review domains independently visible:

1. `FAMILY_AND_SUBSET_SCOPE`
2. `JUMP_1_BODY`
3. `JUMP_2_BODY`
4. `TWO_VARIANT_DIMENSION_AND_ROLE_PROOF`
5. `LENGTH_ASSEMBLY_CONTROL_AND_732_4_PROJECTION_PROOF`
6. `SECTION_EVIDENCE_AND_REPORT_IDEAL_MODEL_BOUNDARY`
7. `PROFILE_PROVENANCE_AND_CONTROL_SET_CLASSIFICATION`
8. `SOURCE_VS_RECONSTRUCTION_UNKNOWN_DEFERRED`

Review must expose:
- accidental one/two-jump collapse;
- invented JUMP_1 length;
- secondary JUMP_2 value promoted to direct evidence;
- combined projection treated as member length;
- report ideal model treated as direct measurement;
- direction-specific duplication;
- prior-gong profile reuse;
- generic-template substitution;
- unsupported joinery;
- blank/near-uniform renders.

## 11. Proposed future hard fails

- `WRONG_REGISTRY_SUBSET_COUNT`
- `WHOLE_HALL_COUNT_FALSE_CLOSURE`
- `WRONG_JUMP_1_BINDING_COUNT`
- `WRONG_JUMP_2_BINDING_COUNT`
- `JUMP_ROLE_COLLAPSED_WITHOUT_EVIDENCE`
- `JUMP_1_LENGTH_INVENTED`
- `JUMP_2_SECONDARY_LENGTH_MARKED_DIRECT`
- `COMBINED_PROJECTION_USED_AS_MEMBER_LENGTH`
- `FULL_LENGTH_SUM_EQUATED_TO_732_4`
- `OBSERVED_MEAN_MARKED_PER_INSTANCE_EXACT`
- `ORIGINAL_963_FACT_UPGRADE`
- `REPORT_IDEAL_MODEL_MARKED_DIRECT`
- `SAMPLE_TO_INSTANCE_MAPPING_INVENTED`
- `DIRECTION_GEOMETRY_VARIANT_WITHOUT_EVIDENCE`
- `LOCATION_SPECIFIC_MASTER_DUPLICATION`
- `PRIOR_GONG_PROFILE_CONTROL_REUSE`
- `GENERIC_TEMPLATE_SUBSTITUTION`
- `COMPARATIVE_BUILDING_GEOMETRY_REUSE_AS_AUTHORITY`
- `PROFILE_CONTROL_SET_NOT_LOCKED`
- `LENGTH_ASSEMBLY_CONTROL_SET_NOT_LOCKED`
- `UNSUPPORTED_END_SHAPE`
- `UNSUPPORTED_JOINERY_OR_LOCAL_CUTS`
- `BUILDING_PLACEMENT_BAKED_INTO_MASTER`
- `MODEL_BEFORE_EXECUTION_AUTHORIZATION`

## 12. Candidate 01 decision boundary｜D-226

D-226 prepares this Master Spec V0.1 Candidate for Product Owner review.

Candidate architecture:
- one `CMP-GONG-HUAGONG-001_MASTER`;
- two independent variant identities: `JUMP_1_HUAGONG` / `JUMP_2_HUAGONG`;
- 28 + 28 = 56 subset instance bindings;
- zero direction/location variants;
- individual full lengths remain unresolved;
- combined first+second projection evidence remains 732.4 mm observed mean / n=46 at assembly level;
- 48分 remains report ideal-model evidence;
- exact profile/end/joinery remain unresolved/deferred;
- both Length/Assembly Control Set and Profile Control Set are mandatory before engineering execution.

Current status:

**CANDIDATE 01 / NOT LOCKED / PRODUCT OWNER REVIEW REQUIRED**

D-226 does **not** authorize:
- Master Spec lock;
- Task Contract creation/lock;
- engineering T-task;
- control-set approval;
- production branch / PR;
- Blender / GitHub Actions execution;
- first article;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.
