# P3.3 Stage1｜T-038 慢栱族 Profile Control Set V0.1

Status: **LOCKED / PRODUCT OWNER APPROVED / D-201**
Date: 2026-09-27
Task: T-038｜P3_3_MANGONG_MASTER_V2_V001
Decision lineage: D-196 / D-198 / D-199 / D-200 / D-201

## 1. Purpose

This gate supplies the numeric Stage1 profile control set required by the locked T-038 Task Contract before engineering execution.

It does not claim recovery of the exact historical slow-gong curve.

## 2. Source role

Same-building source authority:
- SRC-ZG-WF-001 PDF p73–76
- outer-eaves bracket-set photographs
- sectional/measured drawings
- CAD / assembly relationship drawings

Source role:
`QUALITATIVE_FORM_AND_ENVELOPE_AUTHORITY`

Not claimed:
- metric pixel-to-mm trace
- exact historical curve
- direct historical control-point coordinates
- slow-gong-specific local joinery geometry

## 3. Candidate classification

Candidate id:
`MANGONG_PROFILE_CONTROL_SET_V001_C01`

Classification:
`SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`

Control-set signature:
`07d5d9172f25758f057c4bc0200fc35aa892a9a72ef15b40735fcc5c620e80c4`

The candidate is independently constructed for T-038. It does not reuse the T-037瓜子栱 13-point control polygon.

## 4. Normalized coordinate meaning

- x = fraction of full member length, centered at x=0
- z = fraction of full profile thickness, centered at z=0
- top envelope = z=+0.50
- deepest central underside = z=-0.50
- profile is bilaterally symmetric as a Stage1 simplification, not a historical asymmetry claim

## 5. Candidate 01 normalized polygon

```json
[
  [
    -0.5,
    0.5
  ],
  [
    0.5,
    0.5
  ],
  [
    0.5,
    0.12
  ],
  [
    0.475,
    0.02
  ],
  [
    0.435,
    -0.1
  ],
  [
    0.385,
    -0.22
  ],
  [
    0.315,
    -0.33
  ],
  [
    0.235,
    -0.41
  ],
  [
    0.13,
    -0.47
  ],
  [
    0.08,
    -0.5
  ],
  [
    -0.08,
    -0.5
  ],
  [
    -0.13,
    -0.47
  ],
  [
    -0.235,
    -0.41
  ],
  [
    -0.315,
    -0.33
  ],
  [
    -0.385,
    -0.22
  ],
  [
    -0.435,
    -0.1
  ],
  [
    -0.475,
    0.02
  ],
  [
    -0.5,
    0.12
  ]
]
```

Total points: **18**

## 6. Source-guided shape rationale

Candidate 01 deliberately preserves only broad form features that the same-building report supports visually:

- straight horizontal upper bearing envelope;
- short end drops;
- gradual lower-edge deepening toward the center;
- broad central low bearing zone rather than a single sharp point;
- bilateral symmetry for the Stage1 canonical family body;
- no carved micro-profile, groove, mortise, socket or cavity.

These are Stage1 reconstruction controls, not measured historical curve geometry.

## 7. Variant application

The same normalized control set is proposed for both variants:

### LARGE_MANGONG
- L = 1641 mm
- T = 156.9 mm candidate
- actual x = normalized_x × 1641
- actual z = normalized_z × 156.9

### SMALL_MANGONG
- L = 1607 mm
- T = 156.9 mm candidate
- actual x = normalized_x × 1607
- actual z = normalized_z × 156.9

W = 218.9 mm remains the shared report-inferred family design candidate.

This is **not** a global 3D uniform scale:
- L changes by variant;
- W/T stay independently fixed candidate values.

## 8. Visual review criteria

Product Owner review should check:

1. top edge reads as a stable horizontal bearing line;
2. underside transitions are smooth enough for a simplified canonical Stage1 body;
3. central underside is broad rather than needle-pointed;
4. end shoulders do not look excessively decorative or generic-template driven;
5. LARGE/SMALL difference reads only through length, not width/thickness scaling;
6. no feature suggests unsupported historical joinery/detail.

## 9. Current decision boundary

Candidate 01 is **LOCKED / PRODUCT OWNER APPROVED / D-201**.

The approved 18-point numeric set is now stored in the locked T-038 Definition.

This approval does not authorize:
- builder implementation;
- Blender generation;
- workflow execution;
- Draft PR creation;
- engineering execution.

Classification remains `SOURCE_GUIDED_SIMPLIFIED / REPLACEABLE / NOT_DIRECT_MEASUREMENT`.


## 10. Approval Result

- Product Owner approval: **PASS / D-201**
- Locked candidate: `MANGONG_PROFILE_CONTROL_SET_V001_C01`
- Locked control-set signature: `07d5d9172f25758f057c4bc0200fc35aa892a9a72ef15b40735fcc5c620e80c4`
- Point count: **18**
- Engineering execution: **NOT AUTHORIZED**
