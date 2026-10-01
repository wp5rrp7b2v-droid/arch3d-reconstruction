# AF01-J01｜下六椽栿 × 柱头铺作 Joinery Pilot V0.1

- Date: 2026-10-01
- Status: CANDIDATE / EVIDENCE-BOUND / ENGINEERING NOT YET EXECUTED
- Base: `0ecc3416a53bc3fa062e57e6573fd859c36504a1`
- Scope: ONE column-head node + ONE 下六椽栿 instance only
- Master mutation: PROHIBITED
- Whole-frame generation: NOT AUTHORIZED

## 1. Purpose

Resolve the first real assembly problem exposed by AF-01 V001:

> Existing Masters are component-body geometry, not assembly-ready joinery geometry.

J01 does **not** attempt to reconstruct all historical mortise-and-tenon details.
It tests one bounded question only:

> How does one existing Lower-Six-Chuanfu Master physically enter / bear on the column-head bracket set without proxy blocks or gross interpenetration?

## 2. Same-building structural authority

The Wanfo Hall structural description establishes:

- 下六椽栿 is placed on the **second-jump 华栱** of the front/rear column-head puzuo.
- The lower six-chuanfu engages the column-head puzuo at the column line.
- Secondary same-building visual/structural description characterizes the over-column beam head as **华头子-like / wedged under the two true ang members**.
- 上六椽栿 is a different relation and is excluded from J01.

Therefore J01 must not simplify the node as:

`COLUMN → GENERIC BLOCK → LOWER SIX`

and must not assume that the correct remedy is “cut a rectangular slot in the 华栱”.

## 3. Existing Master facts retained

### Lower Six-Chuanfu Master

`CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER`

Current bounded outer-envelope reference:

- observed width / 广 reference: 493.5 mm
- observed maximum thickness: 444.0 mm
- observed tenon-area thickness: **375.0 mm**
- historical full length: UNKNOWN
- tenon-area location / longitudinal extent: UNKNOWN
- exact beam-head profile: UNKNOWN
- hidden joinery: UNKNOWN

Important:

> The 375.0 mm tenon-area thickness is DIRECT_PRIMARY evidence but is currently metadata only. It may constrain a future assembly-instance cut zone; it does not by itself locate that zone or define its cut length/profile.

### Huagong / Ang Masters

Existing Stage1 Masters retain:

- visible family geometry / bounded profile;
- role variants where locked;
- **unsupported joinery / local cuts / grooves remain deferred**.

Therefore no existing Master is authorized to be permanently boolean-cut for J01.

## 4. J01 architecture

J01 introduces an **instance-owned Joinery Layer**, not a new Master.

```
MASTER
  ↓ instantiate
ASSEMBLY INSTANCE
  ↓ place by source-supported node relation
UNMODIFIED COLLISION AUDIT
  ↓
INSTANCE-LOCAL JOINERY FEATURE
  ↓
ASSEMBLY-READY INSTANCE
```

The base Master SHA / geometry must remain unchanged.

## 5. Stage A｜Unmodified collision audit

Stage A uses only existing real Masters.

Required participants:

1. one column / column-head reference;
2. one column-head ludou;
3. the source-supported 华栱 / 昂 participants required at the lower-six contact node;
4. one `CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER` instance.

No proxy cubes.
No generic support fillers.
No Tuofeng.
No Upper-Six.
No Four-Chuanfu.
No roof system.

### Stage A outputs

For every participating pair:

- intersection volume;
- contact / gap status;
- collision bounding box;
- collision centroid;
- owner component IDs;
- whether the collision occurs inside the Lower-Six observed 375 mm tenon-thickness envelope;
- orthographic FRONT / SIDE / AXON diagnostic renders.

Stage A is diagnostic only.
It may not create historical joinery.

## 6. Stage B｜Candidate joinery feature boundary

Stage B is **NOT AUTHORIZED by this document**.

If Stage A proves that the Lower-Six beam head is the body requiring local reduction, the first candidate feature class shall be:

`LOWER_SIX_COLUMN_HEAD_BEAM_END_REDUCTION_CANDIDATE`

not:

`GENERIC_HUAGONG_SLOT`.

The future feature may use 375.0 mm only as a thickness constraint.

The following remain UNKNOWN until further evidence / collision geometry resolves them:

- longitudinal cut length;
- exact transition station;
- top/bottom offset distribution;
- taper / wedge angle;
- shoulder geometry;
- hidden tenon extension;
- whether any counterpart also requires a complementary cut.

No symmetric 34.5 + 34.5 mm reduction may be assumed merely from 444 → 375.

## 7. Hard fails

- `MASTER_GEOMETRY_MUTATED`
- `PROXY_SUPPORT_INSERTED`
- `GENERIC_RECTANGULAR_SLOT_ASSUMED`
- `TENON_375_USED_AS_CUT_LENGTH`
- `TENON_ZONE_LOCATION_INVENTED`
- `SYMMETRIC_REDUCTION_ASSUMED`
- `UPPER_SIX_SCOPE_LEAK`
- `WHOLE_FRAME_SCOPE_LEAK`
- `HISTORICAL_JOINERY_CLAIM_WITHOUT_SOURCE`
- `NO_COLLISION_REPORT`

## 8. PASS condition for J01 Stage A

PASS means only:

1. real Masters were used;
2. the lower-six node can be placed without proxy geometry;
3. all actual interpenetrations are machine-reported;
4. no Master is modified;
5. no historical cut is invented;
6. the result identifies the smallest component-local region that must be processed next.

A Stage A PASS does **not** mean the historical joint is solved.

## 9. Recovery significance

AF-01 V001 proved that numeric placement plus proxy fillers can pass machine validation while still failing architectural review.

J01 reverses that order:

> **real components first → expose collision → cut only where evidence + assembly necessity require it.**

This is the required recovery path before any second whole-frame proof.
