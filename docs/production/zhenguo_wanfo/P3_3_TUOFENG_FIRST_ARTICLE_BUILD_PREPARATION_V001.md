# 驼峰 First Article Build Preparation V001

Status: **DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED / ENGINEERING EXECUTION NOT AUTHORIZED**

## 1. Objective

Prepare the first buildable Master article for:

`CMP-FRAME-TUOFENG-001_MASTER`

with two approved role variants:

1. `LOWER_SUPPORT`
2. `UPPER_RIDGE_SUPPORT`

This step does **not** assign historical metric dimensions to 驼峰.

## 2. Key rule

The Master stores **shape logic + role semantics**.

Actual Wanfo Hall building dimensions are owned by later assembly interfaces.

Therefore:

> Master geometry must be scalable from explicit assembly envelopes; no reference/test dimension may leak into building placement.

## 3. Geometry builder contract

### 3.1 LOWER_SUPPORT

Primitive strategy:
- two-tier support envelope;
- lower broad body;
- centered raised seat;
- no curve claim;
- no joinery cuts.

Input parameters:

- `base_span_u`
- `base_depth_v`
- `base_height`
- `seat_span_u`
- `seat_depth_v`
- `seat_height`

Constraints:

- all values > 0;
- `seat_span_u <= base_span_u`;
- `seat_depth_v <= base_depth_v`;
- total height = `base_height + seat_height`.

Historical metric authority:
- **NONE**.

### 3.2 UPPER_RIDGE_SUPPORT

Primitive strategy:
- symmetric stepped-hump profile extruded in depth;
- broad base;
- stepped shoulders;
- raised flat center seat;
- no historical curve claim;
- no joinery cuts.

Input parameters:

- `base_span_u`
- `depth_v`
- `height`
- normalized XZ profile from approved Candidate Geometry V0.1.

Profile behavior:
- X coordinates scale by `base_span_u`;
- Z coordinates scale by `height`;
- Y extrusion scales by `depth_v`.

Historical metric authority:
- **NONE**.

## 4. Assembly-owned metric envelope rules

No building-specific millimetre value is frozen in the Master.

### LOWER_SUPPORT building realization

Required assembly inputs:

- `lower_support_region = FOUR_CHUANFU_UPPER_SUPPORT_REGION`
- `upper_support_region = LINGGONG_AND_PINGLIANG_SUPPORT_CHAIN`
- `available_vertical_gap`
- `available_support_footprint`
- `required_upper_seat_footprint`

Derived production envelope:

- base footprint must remain inside the available 四椽栿 support region;
- upper seat must satisfy the required support footprint of the 令栱 / 平梁 chain;
- total height is derived from the resolved vertical gap;
- if these constraints cannot be satisfied simultaneously, assembly must FAIL rather than silently distort the component.

### UPPER_RIDGE_SUPPORT building realization

Required assembly inputs:

- `lower_support_region = PINGLIANG_UPPER_SUPPORT_REGION`
- `upper_support_region = SHUZHU_LOWER_SUPPORT_REGION`
- `available_vertical_gap`
- `available_support_footprint`
- `required_shuzhu_footprint`

Derived production envelope:

- base footprint must remain inside the Pingliang support region;
- upper seat must contain/support the resolved Shuzhu lower footprint;
- total height is derived from the resolved Pingliang-top → Shuzhu-bottom gap;
- if the gap is non-positive or support footprints are incompatible, assembly must FAIL.

All derived values:
- classification = `RECONSTRUCTED_DESIGN` or `SECONDARY_CALCULATED`;
- historical_claim = false;
- replaceable = true.

## 5. First-article engineering fixtures

Fixtures exist only to prove the builder and scaling contract.

They are **NOT Wanfo Hall dimensions**.

### LOWER-A
- base span = 1000 test units
- base depth = 500
- base height = 180
- seat span = 420
- seat depth = 320
- seat height = 180

### LOWER-B mutation
- base span = 1250
- base depth = 620
- base height = 210
- seat span = 500
- seat depth = 360
- seat height = 220

Expected:
- identity unchanged;
- role unchanged;
- geometry signature changes;
- constraints remain valid.

### UPPER-A
- base span = 1000
- depth = 500
- height = 320

### UPPER-B mutation
- base span = 820
- depth = 410
- height = 270

Expected:
- same normalized profile topology;
- identity unchanged;
- role unchanged;
- geometry signature changes predictably.

All fixture units are engineering test values in the Blender millimetre workspace and have `historical_claim=false`.

## 6. First Article Review Board

Required panels:

1. BOTH_VARIANTS_AXON
2. LOWER_SUPPORT_PROFILE
3. UPPER_RIDGE_SUPPORT_PROFILE
4. PARAMETRIC_MUTATION_PROOF
5. ROLE_AND_INTERFACE_SEMANTICS
6. SOURCE_VS_RECONSTRUCTED_BOUNDARY
7. UNKNOWN_AND_DEFERRED_GEOMETRY

The board must visibly state:

- exact historical dimensions = UNKNOWN;
- test fixture dimensions = ENGINEERING_TEST_ONLY;
- hidden joinery = UNKNOWN / DEFERRED;
- building realization = ASSEMBLY-OWNED.

## 7. Machine validation

Must verify:

1. one Master family;
2. exactly two role variants;
3. LOWER and UPPER use different geometry strategies;
4. mutation changes geometry without changing identity;
5. no fixture is tagged as building coordinate/dimension;
6. no reference/test dimension is used as historical evidence;
7. joinery cut count = 0;
8. mortise/tenon/groove count = 0;
9. normalized UPPER profile remains symmetric;
10. LOWER seat remains within base footprint;
11. all assembly-owned metric fields remain unresolved in Stage1;
12. source binding record exists;
13. approved Candidate Geometry record exists.

## 8. Hard fails

- `TEST_DIMENSION_LEAKS_INTO_BUILDING`
- `TEST_DIMENSION_MARKED_HISTORICAL`
- `UNSUPPORTED_METRIC_LOCK`
- `UNSUPPORTED_JOINERY_CLAIM`
- `ROLE_VARIANTS_COLLAPSED_WITHOUT_EVIDENCE`
- `VARIANT_IDENTITY_SPLIT_INTO_TWO_MASTER_FAMILIES`
- `LOWER_SEAT_EXCEEDS_BASE`
- `UPPER_PROFILE_ASYMMETRY`
- `ASSEMBLY_ENVELOPE_BYPASSED`
- `UNKNOWN_SILENTLY_FILLED`

## 9. Implementation strategy

Preferred implementation:

- create a small dedicated `tuofeng_master_common_v001.py` builder/inspector;
- do **not** modify the existing long-member Master V2 shared builder, because 驼峰 is not a rectangular endpoint-driven long member;
- reuse common validation/report conventions where practical;
- Blender version follows existing project production runtime;
- one task = one branch = one PR.

## 10. Authorization boundary

Current state:

- Source Binding: PASS
- Master Spec V0.1: APPROVED
- Candidate Geometry V0.1: APPROVED
- First Article Build Preparation: **DESIGN COMPLETE**
- Engineering / Blender execution: **NOT YET AUTHORIZED**
- Canonical Master: NOT CREATED
- Catalog/V008 approved-master binding: NOT AUTHORIZED

Next decision:

> Product Owner approves / amends / rejects this Build Preparation.

After approval, create and run the first-article engineering task.
