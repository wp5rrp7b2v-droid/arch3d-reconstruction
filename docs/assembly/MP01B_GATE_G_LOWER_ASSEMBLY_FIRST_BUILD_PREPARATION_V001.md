# MP-01B Gate G｜Lower Assembly First Build Preparation V001

Status: **PRODUCT OWNER APPROVED / GATE H ENGINEERING EXECUTION AUTHORIZED**
Date: 2026-10-06

## 1. Objective

Prepare the first deterministic 3D build for:

`四椽栿-东缝 → 驼峰 LOWER_SUPPORT / 梁架承托令栱 → 平梁-东缝`

using only the Gate F numeric contract.

Gate G locks:
- logical object list;
- local-to-assembly transforms;
- support/control datums;
- relation metadata;
- machine checks;
- dependency perturbation;
- Review Board layout.

Gate G does **not** execute Blender.

## 2. Authoritative input

Numeric authority:

`production/zhenguo_wanfo/assembly/MP01B_GATE_F_LOWER_ASSEMBLY_LOCAL_METRIC_ENVELOPE_V001.json`

No Gate G value may override Gate F evidence classification.

## 3. Coordinate system

Use `MP01B_ASSEMBLY_LOCAL`:

- X = East-Seam frame-line / out-of-section direction;
- Y = transverse section; South positive / North negative;
- Z = vertical up;
- origin = center of Four-Chuanfu upper face.

This is a project assembly coordinate system, not a survey datum.

## 4. Logical assembly object list

Exactly **6 logical assembly objects**:

1. `四椽栿-东缝`
   - Master: `CMP-FRAME-FOUR-CHUANFU-001_MASTER`
   - V008 physical identity preserved.

2. `平梁-东缝`
   - Master: `CMP-FRAME-PINGLIANG-001_MASTER`
   - variant: `EW_SEAM`
   - V008 physical identity preserved.

3. `ASM-MP01B-TUOFENG-LOWER-SOUTH-01`
   - Master: `CMP-FRAME-TUOFENG-001_MASTER`
   - variant: `LOWER_SUPPORT`
   - reconstructed Minimum-Proof assembly instance.

4. `ASM-MP01B-TUOFENG-LOWER-NORTH-01`
   - same Master / variant;
   - reconstructed Minimum-Proof assembly instance.

5. `ASM-MP01B-LINGGONG-SOUTH-01`
   - Master: `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`
   - role: `LOWER_PINGLIANG_SUPPORT`
   - reconstructed Minimum-Proof assembly instance.

6. `ASM-MP01B-LINGGONG-NORTH-01`
   - same Master / role;
   - reconstructed Minimum-Proof assembly instance.

The four reconstructed support instances do **not** create a whole-hall physical-count claim.

## 5. Control-only datums

Two non-physical controls:

- `DATUM-MP01B-SUPPORT-SOUTH` = `(0,+1836,0)`
- `DATUM-MP01B-SUPPORT-NORTH` = `(0,-1836,0)`

They are assembly controls only.

They do not assert exact historical hidden contact-center coordinates.

## 6. Transform convention

### Common axis rule

The source Masters for Four-Chuanfu, Pingliang and Interior Linggong store their member length on local +X.

For this East-Seam transverse section build:

> local +X → assembly +Y

Use:

`Rz = +90°`

for Four-Chuanfu, Pingliang and both Interior Linggong realizations.

Tuofeng LOWER_SUPPORT Candidate uses its normalized support-span axis as local +X. For the same assembly convention, use:

`Tuofeng local +X → assembly +Y`

with `Rz = +90°`.

This orientation is a **PROJECT_ASSEMBLY_RULE / REPLACEABLE**.

It is not a claim that an unobserved historical local coordinate system is known.

## 7. Locked canonical transforms

All translations in mm.

### Four-Chuanfu

Local body:
- local length X = 7192
- local width/depth Y = 426.5
- local height Z = 302

Transform:
- rotation = `(0,0,+90°)`
- translation = `(0,0,-302)`

World envelope:
- X = `[-213.25,+213.25]`
- Y = `[-3596,+3596]`
- Z = `[-302,0]`

### Pingliang

Local body:
- local length X = 3672
- local width/depth Y = 395.5
- local height Z = 280.5

Transform:
- rotation = `(0,0,+90°)`
- translation = `(0,0,+306)`

World envelope:
- X = `[-197.75,+197.75]`
- Y = `[-1836,+1836]`
- Z = `[306,586.5]`

### South Tuofeng LOWER_SUPPORT

Transform:
- rotation = `(0,0,+90°)`
- translation = `(0,+1836,0)`

Envelope parameters:
- span along assembly Y = 893.3
- depth along assembly X = 426.5
- total Z = 91.0
- base Z = 0
- top Z = 91.0

### North Tuofeng LOWER_SUPPORT

Same geometry.

Transform:
- rotation = `(0,0,+90°)`
- translation = `(0,-1836,0)`

### South Interior Linggong

Transform:
- rotation = `(0,0,+90°)`
- translation = `(0,+1836,+91)`

Envelope:
- length along assembly Y = 893.3
- depth along assembly X = 153.6
- total Z = 215.0
- top Z = 306.0

Two-zone realization:
- BODY_ZONE = Z `[91,220]`
- UPPER_BEARING_ZONE = Z `[220,306]`
- upper bearing length along Y = 491.315

### North Interior Linggong

Same geometry.

Transform:
- rotation = `(0,0,+90°)`
- translation = `(0,-1836,+91)`

## 8. Contact-plane contract

Machine build must resolve the following plane equalities within **0.1 mm**:

At South:
- Four-Chuanfu top Z=0 = Tuofeng bottom Z=0
- Tuofeng top Z=91 = Linggong bottom Z=91
- Linggong top Z=306 = Pingliang underside Z=306

At North:
- same three Z equalities.

These are **production contact planes**.

They are not evidence that exact historical contact-face geometry or joinery has been recovered.

Penetration deeper than 0.1 mm between successive logical bodies is a FAIL.

## 9. Relationship records

Relationship types use the existing P3.2 semantics.

### South chain

1. `REL-MP01B-S-FC-TF-001`
   - type: `SUPPORT`
   - source: `四椽栿-东缝`
   - target: `ASM-MP01B-TUOFENG-LOWER-SOUTH-01`
   - evidence: structural chain FACT + metric realization reconstructed.

2. `REL-MP01B-S-TF-LG-001`
   - type: `SUPPORT`
   - source: South Tuofeng
   - target: South Interior Linggong
   - evidence: reconstructed production decomposition;
   - exact historical contact topology NOT CLAIMED.

3. `REL-MP01B-S-LG-PL-001`
   - type: `SUPPORT`
   - source: South Interior Linggong
   - target: `平梁-东缝`
   - evidence: target support role FACT + contact realization reconstructed.

### North chain

Mirror the three records:
- `REL-MP01B-N-FC-TF-001`
- `REL-MP01B-N-TF-LG-001`
- `REL-MP01B-N-LG-PL-001`

### Location controls

- `DATUM-MP01B-SUPPORT-SOUTH → South Tuofeng / South Linggong` = `LOCATE`
- `DATUM-MP01B-SUPPORT-NORTH → North Tuofeng / North Linggong` = `LOCATE`

No `CONNECT` relation is used to imply known joinery.

## 10. Historical / reconstructed boundary

### FACT retained
- component identities of Four-Chuanfu and Pingliang;
- direct observed family sections;
- existence/role of Tuofeng and Linggong in the Four-Chuanfu→Pingliang support system;
- same-building interior Linggong analog measurements.

### REPORT_INFERRED / SECONDARY_CALCULATED / RECONSTRUCTED
- 7192 Four-Chuanfu realization length;
- 3672 Pingliang realization length;
- ±1836 support stations;
- 306 mm support envelope;
- target Linggong use of the 893.3 × 153.6 × 215.0 analog;
- Tuofeng 91 mm residual height;
- exact object transforms;
- sequential contact-plane decomposition;
- local-axis mapping.

### UNKNOWN / DEFERRED
- exact target-role Linggong dimensions/profile;
- exact Tuofeng historical dimensions/profile;
- exact contact face shapes;
- hidden mortise/tenon/groove geometry;
- whole-hall physical count;
- instance mapping outside this Minimum Proof.

## 11. Machine validation contract

First build must PASS all of the following:

1. logical assembly object count = **6**;
2. physical V008 identities preserved for Four-Chuanfu and Pingliang;
3. exactly two Tuofeng reconstructed instances;
4. exactly two Interior Linggong reconstructed instances;
5. no reconstructed support instance creates whole-hall count;
6. Four-Chuanfu world envelope matches Gate F;
7. Pingliang world envelope matches Gate F;
8. South/North support stations = `±1836 mm`;
9. support groups are mirror-symmetric about Y=0;
10. all four support instances use the locked +90° axis mapping;
11. South contact planes close at Z=0 / 91 / 306 within 0.1 mm;
12. North contact planes close at Z=0 / 91 / 306 within 0.1 mm;
13. no >0.1 mm penetration between successive support bodies;
14. Linggong candidate envelope = 893.3 × 153.6 × 215.0 mm;
15. Tuofeng height = 91.0 mm;
16. outer-eaves Linggong dimensions/profile are absent from geometry provenance;
17. Stage1 test-fixture dimensions are absent as building geometry authorities;
18. reconstructed metrics carry historical_claim=false;
19. beam realization lengths carry historical_full_length_claim=false;
20. hidden joinery remains UNKNOWN / DEFERRED;
21. joinery cut count = 0;
22. six SUPPORT records exist;
23. four LOCATE records exist;
24. relationship evidence classes remain explicit;
25. independent reopen reproduces object signatures;
26. clean deterministic rebuild reproduces assembly signature;
27. Review Board is generated and non-empty.

## 12. Dependency perturbation / V5-like test

Controlled mutation:

`support_clearance = 306 → 310 mm`

The 310 mm value is the existing Gate F observed-family cross-check, used here only as a dependency test.

Expected to change:
- Tuofeng total height: `91 → 95 mm`;
- Tuofeng top: `91 → 95 mm`;
- both Linggong base/top Z: `91/306 → 95/310 mm`;
- Pingliang underside/top Z: `306/586.5 → 310/590.5 mm`.

Expected to remain invariant:
- Four-Chuanfu geometry and placement;
- Four-Chuanfu/Pingliang realization lengths;
- support station Y values;
- Linggong 893.3 × 153.6 × 215.0 envelope;
- Tuofeng plan footprint;
- Master IDs / instance IDs;
- evidence classifications;
- hidden joinery UNKNOWN state.

Mutation PASS proves only dependency propagation for this tested MP-01B subset.

## 13. Review Board

Required six panels:

1. `LOWER_ASSEMBLY_FRONT_ELEVATION`
2. `LOWER_ASSEMBLY_AXONOMETRIC`
3. `SOUTH_SUPPORT_DETAIL`
4. `MUTATION_306_TO_310`
5. `OBJECT_RELATION_EVIDENCE_TABLE`
6. `UNKNOWN_AND_RECONSTRUCTION_BOUNDARY`

The Review Board must make it visually obvious that:
- there are two support groups;
- the Pingliang is supported at the two ±1836 stations;
- contact planes close without visible floating/penetration;
- reconstructed support bodies are not historical-shape claims.

## 14. Hard FAIL

- `WRONG_LOGICAL_OBJECT_COUNT`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `OUTER_EAVES_LINGGONG_GEOMETRY_LEAK`
- `FIRST_ARTICLE_FIXTURE_LEAKS_INTO_BUILDING`
- `SUPPORT_STATION_MISMATCH`
- `MIRROR_SYMMETRY_FAIL`
- `AXIS_MAPPING_MISMATCH`
- `CONTACT_PLANE_GAP`
- `UNINTENDED_PENETRATION`
- `TARGET_ANALOG_MARKED_DIRECT_MEASUREMENT`
- `TUOFENG_RECONSTRUCTION_MARKED_HISTORICAL`
- `HISTORICAL_FULL_LENGTH_FALSE_CLAIM`
- `UNSUPPORTED_JOINERY_CLAIM`
- `WHOLE_HALL_COUNT_FALSE_CLAIM`
- `MUTATION_DEPENDENCY_FAIL`
- `REOPEN_SIGNATURE_MISMATCH`
- `REBUILD_NONDETERMINISTIC`
- `REVIEW_BOARD_MISSING_OR_EMPTY`

## 15. Gate G result

**DESIGN COMPLETE**

The lower assembly now has a complete first-build contract.

Not yet authorized:
- Blender execution;
- Gate H engineering build;
- MP-01B Product Owner acceptance;
- combining MP-01A + MP-01B into a larger frame;
- PR #56 merge.

Next decision:

> Product Owner approves / amends / rejects Gate G Build Preparation.

After approval:

> **MP-01B Gate H｜Lower Assembly First Engineering Build**


## 16. Product Owner authorization

Instruction: **下一步：MP-01B Gate H**

Date: 2026-10-06

Authorized:
- Gate H Blender first build;
- canonical build;
- 306 → 310 mm dependency mutation;
- independent reopen;
- deterministic rebuild;
- Review Board;
- machine validation;
- Actions Artifact publication.

Not authorized:
- MP-01B Product Owner acceptance before review;
- combining MP-01A + MP-01B;
- PR #56 merge.
