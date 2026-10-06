# MP-01B Gate C｜Interior Linggong Candidate Geometry V0.1

Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED / NOT CANONICAL**
Date: 2026-10-06

## 1. Purpose

Convert the approved Interior Linggong Master Spec V0.1 into a minimum buildable geometry candidate without inventing historical dimensions or copying the outer-eaves Linggong family.

## 2. Candidate

Master:
`CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`

Role:
`LOWER_PINGLIANG_SUPPORT`

Geometry:
`NORMALIZED_NEUTRAL_TWO_ZONE_SUPPORT_ENVELOPE`

Two zones:

### BODY_ZONE
- normalized length = 1.00
- normalized depth = 1.00
- normalized height = 0.60
- purpose: neutral horizontal support body

### UPPER_BEARING_ZONE
- normalized length = 0.55
- normalized depth = 1.00
- normalized height = 0.40
- centered above BODY_ZONE
- purpose: explicit upper bearing region for Pingliang support

This is deliberately simple.

It is **not** claimed to be the historical gong curve/profile.

## 3. Evidence boundary

FACT:
- component identity = 令栱
- role in 四椽栿 → 平梁 support chain

RECONSTRUCTED_DESIGN:
- two-zone neutral envelope
- normalized proportions
- explicit upper bearing zone

UNKNOWN:
- historical length
- historical section
- historical curve/profile
- exact contact faces
- hidden joinery
- whole-hall count
- per-instance mapping
- equality with outer-eaves Linggong

## 4. Explicit non-inheritance

The Candidate does not use:
- 897 mm outer-eaves Linggong length
- 217.4 mm outer-eaves width
- 155.6 mm outer-eaves thickness
- outer-eaves 14-point profile
- any scaled/morphed version of that profile

## 5. Metric realization policy

Final MP-01B dimensions remain assembly-owned.

They must be resolved from:
- 四椽栿 upper support footprint
- 驼峰 LOWER_SUPPORT envelope
- Pingliang required lower support footprint
- Four-Chuanfu → Pingliang vertical gap

All resulting metric values must be:
`RECONSTRUCTED_DESIGN` or `SECONDARY_CALCULATED`

and remain replaceable.

## 6. Review question

Product Owner is asked to approve only the **geometry strategy**:

> Is this neutral two-zone body acceptable as the temporary, replaceable digital representation of the interior Linggong for MP-01B?

Approval does not assert historical shape accuracy.

## 7. Next step after approval

> **MP-01B Gate D｜Interior Linggong First Article Build Preparation**

No MP-01B Blender assembly is authorized yet.
