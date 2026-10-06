# MP-01B Gate D｜Interior Linggong First Article Build Preparation V001

Status: **GATE E EXECUTED / MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**
Date: 2026-10-06

## 1. Objective

Prepare the first buildable Master article for:

`CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`

Role variant:

`LOWER_PINGLIANG_SUPPORT`

The first article validates the new interior-role Master as a deterministic, parameterized and provenance-bounded digital component.

It does **not** reconstruct historical metric geometry.

## 2. Locked evidence boundary

Known:
- identity = 令栱;
- structural role = participates with 驼峰 above 四椽栿 to support 平梁;
- outer-eaves Linggong Master is a separate evidence-bounded family and may not be silently reused.

Unknown:
- whole-hall count;
- exact per-instance mapping;
- historical length;
- historical section;
- historical profile;
- exact contact faces;
- hidden joinery;
- equivalence to outer-eaves Linggong.

## 3. Builder contract

Geometry strategy:

`NORMALIZED_NEUTRAL_TWO_ZONE_SUPPORT_ENVELOPE`

### BODY_ZONE
Parameters:
- `body_length`
- `body_depth`
- `body_height`

### UPPER_BEARING_ZONE
Parameters:
- `seat_length`
- `seat_depth`
- `seat_height`

Constraints:
- all values > 0;
- `seat_length <= body_length`;
- `seat_depth <= body_depth`;
- seat centered over BODY_ZONE;
- total height = `body_height + seat_height`.

No historical gong curve is encoded.

## 4. First Article engineering fixtures

Fixtures are **ENGINEERING_TEST_ONLY / NOT_BUILDING_DIMENSIONS / historical_claim=false**.

### Fixture A｜canonical first article

- body_length = 1000
- body_depth = 500
- body_height = 180
- seat_length = 550
- seat_depth = 500
- seat_height = 120

Purpose:
- preserve approved 1.00 / 0.55 length ratio;
- preserve 0.60 / 0.40 height split;
- provide a stable validation body.

### Fixture B｜mutation

- body_length = 1260
- body_depth = 620
- body_height = 210
- seat_length = 660
- seat_depth = 620
- seat_height = 140

Expected:
- identity unchanged;
- role unchanged;
- geometry signature changes;
- constraints remain valid;
- no value becomes a building/historical dimension.

## 5. Prohibited leakage

The First Article must machine-fail if any of the following appears as the source of its geometry:

- outer-eaves Linggong length = 897 mm;
- outer-eaves width = 217.4 mm;
- outer-eaves thickness = 155.6 mm;
- outer-eaves 14-point profile;
- scaled/morphed outer-eaves profile;
- any claim that the two Master families are historically identical.

## 6. Assembly-owned building realization

The First Article proves the Master generator only.

For later MP-01B assembly, the building realization must be supplied by:

- 四椽栿 upper support footprint;
- 驼峰 `LOWER_SUPPORT` envelope;
- Pingliang lower support footprint;
- Four-Chuanfu → Pingliang vertical gap.

The Master does not own these building dimensions.

If later assembly constraints conflict:
- MP-01B assembly must FAIL;
- the Master must not silently distort.

## 7. Joinery policy

`HISTORICAL_JOINERY = UNKNOWN / DEFERRED`

First Article:
- mortise count = 0
- tenon count = 0
- groove/slot count = 0
- hidden cut count = 0

## 8. First Article outputs

Required:

1. `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER_V001.blend` — Actions Artifact only
2. semantic JSON
3. validation JSON
4. Review Board PNG
5. canonical/mutation review renders

Review Board panels:

1. CANONICAL_AXON
2. CANONICAL_PROFILE
3. MUTATION_PROOF
4. ROLE_SEMANTICS
5. OUTER_EAVES_NON_INHERITANCE
6. UNKNOWN_BOUNDARY

## 9. Machine validation

Must verify:

1. Master family count = 1;
2. role variant count = 1;
3. role = `LOWER_PINGLIANG_SUPPORT`;
4. Fixture A geometry deterministic;
5. independent reopen reproduces geometry signature;
6. Fixture B changes geometry but not identity/role;
7. deterministic restore of Fixture A reproduces signature;
8. seat stays within body footprint;
9. all fixture values tagged ENGINEERING_TEST_ONLY;
10. historical metric claim = false;
11. building dimension claim = false;
12. outer-eaves dimensions are absent from canonical geometry provenance;
13. outer-eaves profile is not used;
14. hidden joinery remains UNKNOWN / DEFERRED;
15. joinery cut count = 0;
16. source-binding record exists;
17. approved Candidate Geometry record exists;
18. Review Board generated and non-empty.

## 10. Hard fails

- `OUTER_EAVES_DIMENSION_LEAK`
- `OUTER_EAVES_PROFILE_LEAK`
- `UNSUPPORTED_HISTORICAL_EQUIVALENCE`
- `TEST_DIMENSION_MARKED_HISTORICAL`
- `TEST_DIMENSION_MARKED_BUILDING`
- `UNSUPPORTED_JOINERY_CLAIM`
- `SEAT_EXCEEDS_BODY`
- `MUTATION_NO_EFFECT`
- `REOPEN_SIGNATURE_MISMATCH`
- `RESTORE_NONDETERMINISTIC`
- `UNKNOWN_SILENTLY_FILLED`

## 11. Implementation strategy

Use a dedicated compact-support builder:

`interior_linggong_master_common_v001.py`

Do not modify or reuse the existing outer-eaves Linggong builder as the geometry authority.

Shared utility patterns may be reused only for:
- file/JSON handling;
- deterministic hashing;
- rendering;
- validation infrastructure.

## 12. Authorization boundary

Current:

- Gate A scope decision: PASS
- Gate B registration/source binding/spec: COMPLETE
- Master Spec V0.1: APPROVED
- Gate C Candidate Geometry: APPROVED
- Gate D Build Preparation: **DESIGN COMPLETE**
- Engineering / Blender execution: **NOT AUTHORIZED**
- Master formalization: NOT AUTHORIZED
- V008 approved-master binding: NOT AUTHORIZED
- PR merge: NOT AUTHORIZED

Next decision:

> Product Owner approves / amends / rejects this Build Preparation.

After approval:
> **MP-01B Gate E｜Interior Linggong First Article Engineering Execution**


## 13. Gate E authorization

Product Owner instruction: **开始下一步**

Date: 2026-10-06

Authorized:
- T-043 first-article engineering execution;
- Blender canonical build;
- mutation build;
- independent reopen;
- deterministic restore;
- Review Board generation;
- machine validation;
- Actions Artifact publication.

Not authorized:
- Master formalization;
- V008 approved-master binding;
- MP-01B assembly build;
- PR #56 merge.


## 14. Gate E result

- Run `37424767731`: SUCCESS
- Artifact `11394896083`
- Machine validation: **28/28 PASS**
- First Article formalization remains NOT AUTHORIZED pending Product Owner review.
