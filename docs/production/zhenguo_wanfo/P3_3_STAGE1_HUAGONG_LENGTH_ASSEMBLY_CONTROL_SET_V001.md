# P3.3 Stage1｜华栱 Length / Assembly Control Set V0.1

Status: **LOCKED / PRODUCT OWNER APPROVED / D-231**
Date: 2026-09-27
Task: `T-040｜P3_3_HUAGONG_MASTER_V2_V001`
Task Contract: **LOCKED / D-229**
Master Spec: **LOCKED / D-227**

## 1. Purpose

This Gate A Candidate defines the deterministic Stage1 **reference-specimen** length/section/assembly controls required before 华栱 profile construction.

It does **not** close the historical standalone full length of all 56 Registry instances.

The control set deliberately separates:

1. `MASTER_REFERENCE_SPECIMEN_LENGTH` — a deterministic, replaceable Stage1 construction control for the two First Article reference bodies;
2. `INSTANCE_HISTORICAL_FULL_LENGTH` — remains unresolved for the 56 Registry records;
3. `ASSEMBLY_COMBINED_PROJECTION` — the directly observed first+second total projection constraint;
4. `REPORT_IDEAL_MODEL` — report-inferred modular interpretation kept separate from direct observation.

This separation is mandatory because V008 JUMP_1/JUMP_2 records include column-head, intercolumn and corner-direction contexts, while available non-primary length studies do not establish one universal per-instance standalone length.

## 2. Registry scope

Target remains:

- JUMP_1_HUAGONG: **28**
- JUMP_2_HUAGONG: **28**
- total: **56 LOCKED_SUBSET**
- scope: direction-explicit 正身 subset / **NOT WHOLE-HALL TOTAL**

The 56 bindings are family/variant identity bindings only.

This Candidate does **not** assign an exact historical full length to any individual Registry row.

## 3. Evidence hierarchy

### 3.1 Direct primary assembly constraint

SRC-ZG-WF-001 / PDF p71 / printed p56 / §2.2.4.2 / Fig.2-25 / Table 2-33:

First+second jump total projection:
- mean = **732.4 mm**
- min = **704 mm**
- max = **755 mm**
- variance = **115.61**
- n = **46**
- classification = `DIRECT_PRIMARY / OBSERVED_MEAN / ASSEMBLY_LEVEL_COMBINED_PROJECTION`

Hard boundary:
- not JUMP_1 full member length;
- not JUMP_2 full member length;
- not the sum of two full member lengths;
- not per-instance exact;
- not proven 963 original design;
- sample-to-instance mapping = `UNKNOWN`.

### 3.2 Report ideal-model constraint

SRC-ZG-WF-001 / PDF p72 + p120 / printed p57 + p105:

- 营造尺 = **306 mm**
- 1分 = **15.3 mm**
- first+second total projection = **48分 = 734.4 mm**
- single-material width = **14分 = 214.2 mm**
- material thickness = **10分 = 153.0 mm**
- classification = `REPORT_INFERRED / REPORT_IDEAL_MODEL / REPLACEABLE`

Observed/report-synthesized bands retained as context:
- width band = **214.1–218.9 mm**
- thickness band = **154.0–156.9 mm**

The 734.4 mm ideal total differs from the direct observed mean 732.4 mm by **2.0 mm (~0.273%)**. The direct observed mean remains the validation target; the 48分 value remains a separate report-model cross-check.

### 3.3 Secondary length evidence

Existing canonical P1 bridge evidence:
- JUMP_2 full length ≈ **1630.0 mm**
- JUMP_2 centre length ≈ **1464.8 mm**
- classification = `SECONDARY_CALCULATED / REPLACEABLE / NOT_DIRECT_PRIMARY`

Registered secondary study:
肖旻，2024，《镇国寺大殿尺度规律研究》，《建筑史学刊》5(2):53–68, DOI 10.12329/20969368.2024.02006.

Its later design-hypothesis discussion uses 足材 `M ≈ 321 mm` and distinguishes lower-gong contexts:
- small-seat lower 华栱: full length **2.8M = 898.8 mm**, centre length **2.25M = 722.25 mm**;
- column-head lower gong context: full length **3.15M = 1011.15 mm**, centre length **2.6M = 834.6 mm**;
- upper / JUMP_2 design hypothesis: full length **5M = 1605.0 mm**, centre length **4.5M = 1444.5 mm**.

Classification:
`SECONDARY_HYPOTHESIS / RECONSTRUCTED_DESIGN_GUIDANCE / REPLACEABLE / NOT_DIRECT_PRIMARY`

These values demonstrate that one universal JUMP_1 per-instance full length is not established. They may guide a Stage1 reference specimen, but may not be mapped silently to all 28 JUMP_1 Registry rows.

## 4. Candidate Master reference-specimen lengths

### 4.1 JUMP_1_HUAGONG

Candidate Stage1 Master reference-specimen full length:

**898.8 mm**

Derivation:
`2.8 × 321.0 = 898.8 mm`

Classification:
`RECONSTRUCTED_DESIGN / SECONDARY_HYPOTHESIS_GUIDED / REFERENCE_SPECIMEN_ONLY / REPLACEABLE / NOT_DIRECT_MEASUREMENT`

Reason for choosing this value as the Master reference specimen:
- it is an explicit published small-seat lower-Huagong reconstruction rather than an invented convenience number;
- it provides a deterministic short-form JUMP_1 reference body distinct from JUMP_2;
- it is not promoted to a universal JUMP_1 instance length;
- the alternative column-head 3.15M hypothesis is retained as a conflict/context check rather than averaged or silently discarded.

Hard boundary:
- `JUMP_1_INSTANCE_HISTORICAL_FULL_LENGTH = UNRESOLVED`
- the 898.8 mm reference body must never be described as the exact length of all 28 JUMP_1 records.

### 4.2 JUMP_2_HUAGONG

Candidate Stage1 Master reference-specimen full length:

**1630.0 mm**

Classification:
`SECONDARY_CALCULATED / REFERENCE_SPECIMEN_ONLY / REPLACEABLE / NOT_DIRECT_PRIMARY`

Reason:
- this value already exists in the canonical project evidence chain as a report-derived later calculation;
- it has stronger project provenance than replacing it with the weaker 5M modular hypothesis solely for regularity;
- the 5M = 1605.0 mm value remains a secondary design-hypothesis cross-check only.

Retained cross-check:
- secondary calculated centre length = **1464.8 mm**
- modular hypothesis full length = **1605.0 mm**
- difference from 1630.0 mm = **25.0 mm (~1.53%)**
- modular hypothesis centre length = **1444.5 mm**
- difference from 1464.8 mm = **20.3 mm (~1.39%)**

Hard boundary:
- `JUMP_2_INSTANCE_HISTORICAL_FULL_LENGTH = UNRESOLVED`
- 1630.0 mm is not direct primary and not a claim for all 28 JUMP_2 instances.

## 5. Instance-length non-propagation rule

The two Master reference-specimen lengths are **not instance placement dimensions**.

Stage1 Catalog/V008 binding, if later authorized, shall mean only:

`Registry row → Master family / jump-variant identity`

It shall **not** mean:

`Registry row → exact standalone full length`

Required metadata:
- `reference_specimen_length_applies_to_instance = false`
- `instance_full_length_status = UNRESOLVED`
- `per_instance_exact = false`
- `sample_to_instance_mapping = UNKNOWN`

No building assembly may consume 898.8 or 1630.0 as an instance length without a later evidence-backed assembly rule.

## 6. Candidate section control

Candidate Stage1 family section:

- width = **214.2 mm**
- thickness = **153.0 mm**

Derivation:
- width = 14分 × 15.3 = 214.2 mm
- thickness = 10分 × 15.3 = 153.0 mm

Classification:
`REPORT_INFERRED / REPORT_IDEAL_MODEL / FAMILY_DESIGN_CANDIDATE / REPLACEABLE / NOT_DIRECT_HUAGONG_MEASUREMENT`

Application:
- same section candidate for both JUMP_1/JUMP_2 reference specimens;
- section does not scale with member length;
- no prior T-037/T-038/T-039 section value is imported as authority.

Evidence-boundary note:
- width 214.2 mm lies inside the report's 214.1–218.9 mm band;
- thickness 153.0 mm is **1.0 mm below** the lower edge of the 154.0–156.9 mm observed/synthesized band;
- this discrepancy is retained explicitly and is **not** clipped away;
- the Candidate favors the report's explicit 10分 ideal-model rule for the reconstruction reference specimen, not an invented midpoint.

## 7. Local coordinate / reference-datum rule

Canonical reference bodies:

- +X = longitudinal / out-jump direction
- +Y = width
- +Z = vertical / profile-thickness
- body geometric origin = centre of the Stage1 reference envelope
- location = [0,0,0]
- rotation = [0,0,0]
- scale = [1,1,1]

The body geometric origin is a **PROJECT MODEL DATUM**, not a historical joint/contact datum.

Exact historical:
- hidden overlap = `UNRESOLVED`
- mortise/tenon datum = `DEFERRED`
- actual bearing/contact planes = `UNRESOLVED`

No body end, notch or hidden overlap may be invented merely to make the assembly fixture touch visually.

## 8. Two-jump validation fixture

Fixture id:

`TWO_JUMP_ASSEMBLY_FIXTURE_VALIDATION_ONLY`

Status:
`NON_CANONICAL / VALIDATION_ONLY / NOT A THIRD VARIANT / NOT REGISTRY / NOT CATALOG`

### 8.1 Observed-mean control datums

Along fixture +X:

- `D0_ASSEMBLY_BASE = 0.0 mm`
- `D1_JUMP_MIDPOINT = 366.2 mm`
- `D2_TOTAL_PROJECTION = 732.4 mm`

Thus:
- interval 1 = 366.2 mm
- interval 2 = 366.2 mm
- total = 732.4 mm

The equal split is classified:

`RECONSTRUCTED_DESIGN / SECONDARY_HYPOTHESIS_GUIDED_EQUAL_JUMP_RULE / PROJECT_FIXTURE_ONLY / REPLACEABLE`

It is **not** a direct observation of individual jump lengths.

The only direct metric assertion remains:

`D2 - D0 = 732.4 mm`

### 8.2 Why the midpoint is permitted

The secondary 2024 study explicitly discusses an equal-real-jump tendency as part of its design interpretation. This is sufficient to propose a deterministic **validation fixture midpoint**, but not sufficient to upgrade 366.2 mm into an observed first-jump or second-jump fact.

Therefore:
- D1 is replaceable;
- D0→D2 is the primary source constraint;
- individual per-jump projection remains historically unresolved.

### 8.3 Body placement in the fixture

The fixture may display:
- one JUMP_1 reference body;
- one JUMP_2 reference body;
- D0/D1/D2 datum planes/markers.

Reference bodies are positioned using explicit project role anchors for visual review.

The fixture must never infer projection from:
- mesh end-to-end length;
- hidden overlap;
- invented sockets/notches;
- full-length subtraction.

The 732.4 proof is datum-to-datum, independent from standalone full-member lengths.

## 9. Report ideal-model cross-check

Separate non-authoritative cross-check:

- report total = 48分 × 15.3 = **734.4 mm**
- optional report-ideal midpoint = **367.2 mm**
- direct observed-mean target = **732.4 mm**
- delta = **+2.0 mm**
- relative delta ≈ **0.273%**

The 734.4 mm model:
- is not used as the canonical fixture total;
- is not used to overwrite the direct observed mean;
- is not a historical exactness claim.

## 10. Machine-control tolerance

For deterministic software validation only:

`ASSEMBLY_TOTAL_PROJECTION_MACHINE_TOLERANCE = ±0.1 mm`

Required check:

`abs((D2 - D0) - 732.4) <= 0.1`

This tolerance expresses numeric implementation control only.

It does **not** mean the historical building was constructed or measured to ±0.1 mm.

The observed source spread 704–755 mm remains evidence context and shall not generate undocumented per-instance variation.

## 11. Candidate signatures / versioning policy

Candidate control id:

`HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01`

Canonical signature shall be calculated only from the final locked machine-readable control payload.

Until Product Owner approval:
- signature status = `LOCKED`
- control set semantic SHA-256 = `ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b`
- signature scope = canonicalized semantic control payload excluding governance/status/signature fields
- signature canonicalization = UTF-8 JSON / recursively sorted object keys / compact separators
- the locked control payload may be consumed only after a separate Engineering Execution Authorization.
- no builder/Blender execution is authorized by the control-set lock itself.

## 12. Mandatory hard fails after future lock

Future validator must fail closed on at least:

- `REFERENCE_SPECIMEN_LENGTH_PROPAGATED_TO_INSTANCE`
- `JUMP_1_REFERENCE_MARKED_DIRECT`
- `JUMP_1_REFERENCE_MARKED_ALL_INSTANCES_EXACT`
- `JUMP_2_1630_MARKED_DIRECT_PRIMARY`
- `SECONDARY_HYPOTHESIS_MARKED_PRIMARY`
- `JUMP_1_LOCATION_CLASS_CONFLICT_HIDDEN`
- `SECTION_IDEAL_MODEL_MARKED_DIRECT`
- `SECTION_VALUE_SILENTLY_CLIPPED_TO_OBSERVED_BAND`
- `COMBINED_PROJECTION_USED_AS_MEMBER_LENGTH`
- `FULL_LENGTH_SUM_EQUATED_TO_732_4`
- `PER_JUMP_366_2_MARKED_DIRECT_OBSERVATION`
- `HIDDEN_OVERLAP_INVENTED_TO_FORCE_PROJECTION`
- `MESH_ENDS_USED_AS_UNSUPPORTED_PROJECTION_DATUM`
- `VALIDATION_FIXTURE_PROMOTED_TO_CANONICAL_ASSET`
- `REPORT_734_4_OVERWRITES_DIRECT_732_4`
- `OBSERVED_SPREAD_USED_TO_INVENT_INSTANCE_VARIANTS`
- `INSTANCE_FULL_LENGTH_FALSE_CLOSURE`

## 13. Unknown / deferred after this Candidate

Still unresolved/deferred:

- exact historical JUMP_1 full length by location;
- exact historical JUMP_2 full length by location;
- corner-direction standalone lengths;
- exact individual jump projections;
- exact hidden overlap;
- exact physical assembly contact datum;
- exact end geometry;
- mortise-tenon / grooves / slots / cavities / hidden cuts;
- per-instance deformation;
- per-instance originality / repair state;
- whole-hall 华栱 total count;
- n=46 sample-to-56-instance mapping.

## 14. Candidate 01 review decision

Recommended Candidate controls:

| Control | Candidate |
|---|---|
| JUMP_1 Master reference specimen L | **898.8 mm** |
| JUMP_2 Master reference specimen L | **1630.0 mm** |
| Family section W | **214.2 mm** |
| Family section T | **153.0 mm** |
| Direct combined projection target | **732.4 mm** |
| Fixture midpoint | **366.2 mm** |
| Report ideal total cross-check | **734.4 mm** |
| Machine tolerance | **±0.1 mm** |

Critical semantic rule:

**The two reference-specimen lengths close the Stage1 Master construction control only; they do not close any individual Registry instance's historical standalone full length.**

Current status:

**LOCKED / PRODUCT OWNER APPROVED / D-231**

D-231 locks this Length/Assembly Control Set but does not authorize:
- Profile Control Set lock;
- engineering execution;
- branch / PR;
- builder implementation;
- Blender / GitHub Actions;
- First Article;
- formalization;
- Catalog/V008 binding;
- Stage2;
- T-018 resume.


## 15. Product Owner Approval / Lock｜D-231

Product Owner approved D-230 Candidate 01 without changing any numerical control, evidence classification, or unresolved/deferred boundary.

D-231 formally locks:

- control id: `HUAGONG_LENGTH_ASSEMBLY_CONTROL_SET_V001_C01`;
- JUMP_1 Master reference specimen full length = **898.8 mm**;
- JUMP_2 Master reference specimen full length = **1630.0 mm**;
- family reference section = **214.2 × 153.0 mm**;
- validation fixture datums = **D0 0.0 / D1 366.2 / D2 732.4 mm**;
- report ideal-model cross-check = **734.4 mm / 48分**;
- machine implementation tolerance = **±0.1 mm**;
- semantic control SHA-256 = `ffacd94f5d6c2102a3a2378b3a1529a052a1c9b60d0ebc982d8c3b9c5dac201b`.

The SHA-256 covers the canonicalized semantic control payload only, excluding governance/status/signature fields, so approval metadata does not alter the control identity.

Evidence semantics remain unchanged:
- 898.8 mm = `RECONSTRUCTED_DESIGN / SECONDARY_HYPOTHESIS_GUIDED / REFERENCE_SPECIMEN_ONLY / REPLACEABLE / NOT_DIRECT_MEASUREMENT`;
- 1630.0 mm = `SECONDARY_CALCULATED / REFERENCE_SPECIMEN_ONLY / REPLACEABLE / NOT_DIRECT_PRIMARY`;
- 214.2 × 153.0 mm = `REPORT_INFERRED / REPORT_IDEAL_MODEL / FAMILY_DESIGN_CANDIDATE / REPLACEABLE`;
- D0→D2 = 732.4 mm remains the only direct-primary assembly metric assertion in the fixture;
- D1 = 366.2 mm remains reconstruction/project-fixture guidance, not an observed individual-jump fact;
- 56 Registry instance historical standalone full lengths remain `UNRESOLVED`;
- sample-to-instance mapping remains `UNKNOWN`.

D-231 does **not** authorize:
- production branch / PR;
- builder implementation;
- Profile Control Set adoption;
- GitHub Actions / Blender execution;
- First Article;
- formalization;
- Catalog/V008/CURRENT binding;
- Stage2;
- T-018 resume.

Next complete step:

**design `HUAGONG_PROFILE_CONTROL_SET_V0.1` Candidate.**
