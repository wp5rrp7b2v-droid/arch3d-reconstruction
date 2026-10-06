# P3.3 梁架承托令栱 Master Spec V0.1

Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
Date: 2026-10-06

## 1. Master identity

- component: 令栱（梁架承托）
- component_id: `CMP-FRAME-LINGGONG-INTERIOR-001`
- master_id: `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`
- master_version: `V0.1 CANDIDATE`
- Master family count: **1**
- role variant count: **1**
- role variant: `LOWER_PINGLIANG_SUPPORT`
- historical whole-hall instance count: **UNKNOWN**

## 2. Scope decision

This Master is evidence-bounded to:

`FOUR_CHUANFU -> TUOFENG / INTERIOR_LINGGONG -> PINGLIANG`

It is not an extension of the approved outer-eaves `CMP-GONG-LINGGONG-001_MASTER`.

The two Masters share the historical term “令栱”, but current evidence does not establish metric/profile equivalence.

## 3. Geometry strategy

Geometry class:

`NORMALIZED_NEUTRAL_HORIZONTAL_SUPPORT_ENVELOPE / ASSEMBLY_OWNED / REPLACEABLE`

V0.1 locks only:
- horizontal support-member semantics;
- symmetric family-local body;
- flat upper bearing zone;
- flat/controlled lower support zone;
- deterministic local axes;
- assembly-owned dimensions.

V0.1 does **not** lock:
- historical length;
- historical width/depth;
- historical height/thickness;
- exact gong curve;
- end shaping;
- mortise/tenon/groove/slot;
- insertion depth.

## 4. Why no outer-eaves profile reuse

The outer-eaves 14-point profile was explicitly created for the 28-instance external dougong family.

Reusing it here would silently assert a cross-context geometry equivalence that has not been demonstrated.

Therefore:
- copy of 897 × 217.4 × 155.6 mm = **PROHIBITED as historical input**;
- copy of the 14-point outer-eaves profile = **PROHIBITED**;
- scaling/morphing that profile = **PROHIBITED**.

## 5. Candidate normalized body

The first Candidate Geometry should use a deliberately neutral two-zone envelope:

1. `BODY_ZONE`
   - horizontal rectangular support body;
   - normalized length = 1.0;
   - normalized depth = 1.0;
   - normalized body height = 0.60 of total height.

2. `UPPER_BEARING_ZONE`
   - centered flat upper seat;
   - normalized seat length = 0.55 of body length;
   - normalized seat depth = 1.0;
   - normalized seat height = 0.40 of total height.

This is a **project modeling abstraction**, not a historical profile reconstruction.

If source imagery later supports a more specific interior profile, this topology is replaceable.

## 6. Assembly-owned metric envelope

The Master itself stores no canonical historical millimetre dimensions.

For MP-01B realization, assembly must provide:

- available footprint on 四椽栿 upper support region;
- relationship with the `TUOFENG::LOWER_SUPPORT` envelope;
- required Pingliang lower support footprint;
- available vertical gap between 四椽栿 and 平梁.

Derived dimensions must be classified:
- `RECONSTRUCTED_DESIGN`, or
- `SECONDARY_CALCULATED`.

If support constraints cannot be satisfied simultaneously:
- assembly must **FAIL**;
- the Master must not silently stretch into an implausible shape.

## 7. Local axes

- local X = member horizontal length axis;
- local Y = depth/extrusion axis;
- local Z = vertical;
- origin = deterministic family-local center;
- building/world placement = assembly-owned.

## 8. Joinery

`HISTORICAL_JOINERY = UNKNOWN / DEFERRED`

- mortise count = 0
- tenon count = 0
- groove/slot count = 0
- hidden cuts = 0

Support/contact semantics may exist without historical joint geometry.

## 9. UNKNOWN policy

The following remain formal UNKNOWN:
- whole-hall count;
- per-instance mapping;
- exact historical dimensions;
- exact historical profile;
- exact interface contact face;
- hidden joinery;
- equivalence to outer-eaves Linggong.

UNKNOWN does not block a Minimum Proof if:
- identity is known;
- role is known;
- assembly envelope is explicit and replaceable;
- no reconstructed value is promoted to history.

## 10. Approval gate

V0.1 may be approved if Product Owner accepts:

1. separate interior-role Master family;
2. one role variant `LOWER_PINGLIANG_SUPPORT`;
3. neutral normalized two-zone geometry;
4. no reuse of outer-eaves dimensions/profile;
5. assembly-owned production dimensions;
6. hidden joinery remains UNKNOWN;
7. whole-hall count/per-instance mapping remain UNKNOWN.

After approval:

> **MP-01B Gate C｜Interior Linggong Candidate Geometry V0.1**

No Blender assembly is authorized by this Spec alone.
