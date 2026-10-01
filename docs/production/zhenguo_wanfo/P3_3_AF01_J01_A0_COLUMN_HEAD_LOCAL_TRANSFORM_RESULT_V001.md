# AF01-J01-A0｜Column-Head Local Assembly Transform Resolver V001 — Result

- Date: 2026-10-01
- Status: **CANDIDATE / MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**
- Scope: 北立面东中柱柱头节点，仅四个构件
- Workflow Run: **36820874582**
- Workflow conclusion: **SUCCESS**
- Artifact: `AF01_J01_A0_COLUMN_HEAD_LOCAL_TRANSFORM_RESOLVER_V001`
- Artifact ID: **11143770943**
- Artifact digest: `sha256:0640041be31ee9ec39dc91da8c0692e626d1b024033386e7cc4d1dc97156bebd`
- Head commit: `c87a7587b7397b58ae477c16250aa9cf0a9911bb`

## 1. Node frame

AF-01 east-seam north column node:

- world X = **+2218.5 mm**
- world Y = **+5355.0 mm**
- column-head ludou bottom = **Z 3534.3 mm**
- +Y = north / outward
- +Z = up

The report-derived vertical ladder consumed by A0 is:

`0 → 33 → 54 → 75 → 96 → 106 → 120 fen`

with:

`1 fen = 15.3 mm`

A0 consumes only:

- JUMP_1_HUAGONG = 33 fen
- JUMP_2_HUAGONG = 54 fen
- TOU_ANG = 75 fen
- ER_ANG = 96 fen

The 54-fen and 96-fen endpoints already close against locked AF01-B01-G1 support planes.

## 2. Four resolved transforms

### A0-1｜一跳华栱

Registry:
`华栱-北-05-一跳`

Master:
`CMP-GONG-HUAGONG-001_MASTER / JUMP_1_HUAGONG`

Canonical Master top offset:
`+76.5 mm`

Target upper-profile level:

`3534.3 + 33 × 15.3 = 4039.2 mm`

Resolved Master origin:

`[X,Y,Z] = [2218.5, 5355.0, 3962.7] mm`

Orientation:
- local +X → world +Y / north-outward
- local +Y → world -X
- local +Z → world +Z

### A0-2｜二跳华栱

Registry:
`华栱-北-05-二跳`

Master:
`CMP-GONG-HUAGONG-001_MASTER / JUMP_2_HUAGONG`

Canonical Master top offset:
`+76.5 mm`

Target upper-profile level:

`3534.3 + 54 × 15.3 = 4360.5 mm`

Resolved Master origin:

`[X,Y,Z] = [2218.5, 5355.0, 4284.0] mm`

Cross-check:

`JUMP_2_HUAGONG upper profile Z = 4360.5 mm`

= locked:

`LOWER_SIX_SUPPORT_PLANE_Z = 4360.5 mm`

**MATCH**

### A0-3｜头昂

Registry:
`头昂-北-05`

Master:
`CMP-GONG-ANG-001_MASTER / TOU_ANG`

Locked slope:
- run = 47 fen = 719.1 mm
- rise = 21 fen = 321.3 mm
- angle = **24.0754982551°**

Installation direction:

`local +U = north / outward + downward`

Canonical upper-profile intersection at local `U=0,V=0`:

`W = 116.35 mm`

Target column-axis upper-profile level:

`3534.3 + 75 × 15.3 = 4681.8 mm`

Resolved Master origin:

`[X,Y,Z] = [2218.5, 5307.536174, 4575.571437] mm`

The local upper-profile anchor maps exactly to:

`[2218.5, 5355.0, 4681.8] mm`

### A0-4｜二昂

Registry:
`二昂-北-05`

Master:
`CMP-GONG-ANG-001_MASTER / ER_ANG`

Same locked 47:21 slope.

Canonical upper-profile intersection at local `U=0,V=0`:

`W = 93.5 mm`

Target column-axis upper-profile level:

`3534.3 + 96 × 15.3 = 5003.1 mm`

Resolved Master origin:

`[X,Y,Z] = [2218.5, 5316.857604, 4917.733686] mm`

The local upper-profile anchor maps exactly to:

`[2218.5, 5355.0, 5003.1] mm`

Cross-check:

`ER_ANG column-axis upper-profile Z = 5003.1 mm`

= locked:

`UPPER_SIX_SUPPORT_PLANE_Z = 5003.1 mm`

**MATCH**

## 3. Important classification boundary

The four transforms are **not** historical measured joint coordinates.

They are:

`AF01_LOCAL / REPORT_LADDER_CONSUMING / RECONSTRUCTED_DESIGN / PROJECT_DATUM / REPLACEABLE`

The key new A0 rule is deliberately minimal:

- Huagong: centered canonical reference-body origin placed on the column axis; its upper profile is aligned to the report ladder level.
- Ang: existing locked 47:21 slope is consumed; the canonical upper-profile point at local `U=0,V=0` is anchored to the column axis and report ladder level.

This rule exists only because Stage1 Masters intentionally deferred exact historical contact datums.

It must not be re-labelled as:
- direct survey position;
- exact 963 joint coordinate;
- exact hidden overlap;
- exact historical member-end position.

## 4. What A0 does not consume

A0 does **not** consume:
- T-040 D0/D1/D2 validation-fixture positions as building coordinates;
- T-041 O/RUN/RISE validation-fixture positions as building coordinates;
- historical full timber lengths;
- hidden joinery;
- mortise/tenon cuts;
- proxy blocks.

The approved Ang 47:21 slope rule is consumed as a geometry rule, not as fixture placement.

## 5. Machine gate

PASS checks include:

- 33/54/75/96 ladder order;
- each successive layer increment = 21 fen;
- J2 upper level = lower-six locked support Z;
- ER Ang upper anchor = upper-six locked support Z;
- all four Master joinery-cut counts remain zero;
- no T040/T041 fixture position promotion;
- no Master mutation;
- no joinery generation.

## 6. Gate

A0 numerical/local-transform resolution is complete.

Pending Product Owner decision:

**APPROVE A0 candidate → return to J01 Stage A Unmodified Collision Audit.**

If approved, Stage A may use these four transforms together with the already locked column / ludou / lower-six placements.

No Stage B joinery cut is authorized by A0.
