# MP-01B｜Circle 1 Interior Huagong Visible Gong-Head Profile Resolution V001

Status: **PREVIOUSLY PRODUCT OWNER APPROVED / T-047 ACTUAL BUILD FALSIFIED PROFILE-EXTENT ASSUMPTION / REOPENED / NO BLENDER**
Date: 2026-10-06

## 1. Scope

Resolve only the original Product Owner Circle 1 issue:

> the East-Seam FRONT/REAR interior depthwise Huagong is currently a rectangular bounded envelope and does not visibly express the source-described gong-head end.

This document does not resolve Circle 2 or Circle 3.

## 2. Baseline retained

Target family:
- `CMP-FRAME-HUAGONG-INTERIOR-001`
- name: 华栱（梁架襻间进深）
- system: 主体梁架 / 襻间承托
- axis: assembly Y / 进深

Direct target section evidence from Appendix 1-9:
- FRONT: 广 221 × 厚 153 mm
- REAR: 广 210 × 厚 156 mm
- length wording: `一端栱头，一端至托脚`

Existing R3 project-completion length control remains:
- total realization length = 900 mm
- inward gong-head reach = 650 mm
- outward Tuojiao reach = 250 mm
- classification = SOURCE_IMAGE_CALIBRATED_PROJECT_COMPLETION / REPLACEABLE

No change is made to those length/end-zone controls in Circle 1.

## 3. Outer-eaves Huagong reuse decision

Existing outer-eaves master:
`CMP-GONG-HUAGONG-001_MASTER`

has an approved T-040 profile control set, but the current MP-01B source binding explicitly says:

**DIRECT GEOMETRY REUSE = NO**

Therefore Circle 1 does not copy, scale, average or morph the T-040 16-point polygon.

T-040 may remain software-method precedent only.

## 4. Target Drawing-11 observation

Drawing 11 / 明间东缝结构横剖面推算—点云对比 shows both upper-purlin bracket nodes in the same transverse section.

At both target nodes:
- the interior Huagong is visible longitudinally in section;
- the inner side presents a short terminal gong-head with a rising/curved underside;
- the body is deepest near the bracket station;
- the source-visible gong-head occupies the previously locked inward 650 mm zone;
- the outward 250 mm zone terminates toward / into the Tuojiao region and is partly obscured by the support system.

This supports an asymmetric target realization:
- one visible gong-head end;
- one neutral Tuojiao-end body;
- no bilateral-symmetry claim.

## 5. Candidate profile control

Candidate id:
`MP01B_INTERIOR_HUAGONG_VISIBLE_PROFILE_V001_C01`

Classification:
`TARGET_DRAWING_GUIDED_SIMPLIFIED / SOURCE_IMAGE_CALIBRATED_PROJECT_COMPLETION / REPLACEABLE / NOT_DIRECT_MEASUREMENT`

Local longitudinal coordinate:
- station = x 0
- outward toward Tuojiao = x -250 mm
- inward toward gong-head = x +650 mm
- top bearing line = z 0
- downward = negative z

### Neutral outward region

From x -250 to x 0:
- retain full target section depth;
- no invented shoulder / notch / curve;
- purpose: preserve the source wording “至托脚” without fabricating the hidden contact geometry.

### Inward visible gong-head normalized underside

The Drawing-11 FRONT and REAR silhouettes were read independently and reduced to one coarse target-specific piecewise-linear visible-envelope control.

Normalized control pairs:
- x fraction is fraction of the 650 mm inward gong-head reach from station;
- depth fraction is fraction of the target direct 广 value below the top bearing line.

```json
[
  [0.00, 1.00],
  [0.20, 1.00],
  [0.45, 0.94],
  [0.65, 0.80],
  [0.85, 0.43],
  [1.00, 0.15]
]
```

Metric longitudinal control stations:
- 0 mm
- 130 mm
- 292.5 mm
- 422.5 mm
- 552.5 mm
- 650 mm

FRONT target underside depths below top line (H=221):
- 221.0
- 221.0
- 207.7
- 176.8
- 95.0
- 33.2 mm

REAR target underside depths below top line (H=210):
- 210.0
- 210.0
- 197.4
- 168.0
- 90.3
- 31.5 mm

These are reconstruction-control values, not historical measured curve coordinates.

## 6. Candidate polygon rule

For each FRONT/REAR target:
1. top edge remains straight from x=-250 to +650;
2. at x=+650 the visible gong-head terminates with the short target drop defined above;
3. underside follows the six target-specific control stations back toward x=0;
4. x=0 to x=-250 remains a neutral full-depth body;
5. extrusion thickness remains the direct target 厚:
   - FRONT 153 mm
   - REAR 156 mm.

No end notch, slot, mortise, tenon, hidden overlap or contact cut is introduced.

## 7. Evidence boundary

FACT:
- target identity = 进深华栱;
- FRONT/REAR direct target sections;
- source wording = 一端栱头，一端至托脚;
- Drawing 11 visibly shows a non-rectangular gong-head silhouette at the target nodes.

PROJECT COMPLETION:
- 900 mm realization length;
- 650 / 250 endpoint-zone control;
- six-point piecewise visible-profile approximation;
- same normalized visible-profile method applied to FRONT/REAR.

UNKNOWN / DEFERRED:
- exact historical curve;
- exact terminal shoulder;
- exact Tuojiao-side hidden shape;
- exact Huagong–Tuojiao cut/contact;
- mortise-tenon;
- slots / grooves / cavities;
- per-instance deformation / repair asymmetry.

## 8. Required machine checks if later authorized

- exactly two interior Huagong target solids remain;
- total longitudinal realization remains 900 mm;
- inward gong-head zone remains 650 mm;
- outward Tuojiao zone remains 250 mm;
- FRONT section remains 221 × 153 mm;
- REAR section remains 210 × 156 mm;
- candidate normalized control set matches exactly;
- profile is asymmetric;
- T-040 outer-eaves profile hash/points are not inherited;
- Huagong endpoint datums are unchanged;
- Tuojiao approved T-046 geometry is unchanged;
- Linggong / Ludou / Tuofeng / Pingliang / Four-Chuanfu geometry is unchanged;
- joinery cut count remains 0;
- Circle 2 and Circle 3 remain open.

## 9. Decision

Circle 1 evidence resolution is sufficient for a targeted build **if Product Owner approves this candidate**.

No Blender execution is authorized by this document.

## 10. Product Owner decision

Decision: **APPROVED**

Approved scope:
- Candidate `MP01B_INTERIOR_HUAGONG_VISIBLE_PROFILE_V001_C01`;
- target-specific asymmetric visible gong-head treatment;
- existing 900 mm total realization length retained;
- inward 650 mm gong-head zone retained;
- outward 250 mm Tuojiao zone retained;
- FRONT 221 × 153 mm and REAR 210 × 156 mm direct target sections retained;
- six-point target Drawing-11-guided visible-profile control;
- exact historical curve / shoulder / hidden contact / joinery remain UNKNOWN / DEFERRED.

Not approved by this decision:
- Blender execution;
- Circle 2;
- Circle 3;
- MP-01B overall acceptance;
- MP-01A + MP-01B combination;
- PR #56 merge.

Next gate:
**Circle 1 Targeted Build Authorization**


## 11. T-047 actual-build falsification / reopened status

T-047 executed the approved Candidate deterministically (51/51 MACHINE PASS) but Product Owner visual review **FAILED**.

Invalidated assumption:
- `650 mm inward endpoint reach == 650 mm shaped gong-head extent`.

The 650 mm value is retained only as an endpoint/placement reach unless later evidence disproves it.

The visible gong-head shaping extent is reopened and must be localized near the terminal end rather than spread across the full 650 mm.

### New Product Owner visual observations to carry into the next evidence check

1. Drawing 11 shows multiple gong heads with a repeated/localized terminal form.  
   This suggests a same-building repeated visible-form rule may exist, but exact metric equivalence is not yet established.

2. A distinct small dou-shaped physical element is visible above multiple gong-head terminals.  
   Working identification: **possibly 散斗**.

Evidence boundary:
- existence of a separate small dou-like physical participant at the visible gong-head location = **visual FACT candidate requiring target-location source confirmation**;
- identification as `散斗` = **INFERENCE / NOT YET LOCKED**;
- it must not be silently substituted with 齐心斗, 交互斗, generic small-dou geometry, or the old BRACKET_CONTACT proxy;
- DG-114 unified-small-dou rule remains UNKNOWN / DO_NOT_LOCK.

### Next work, not authorized tonight

**MP-01B｜Gonghead Repetition + Small-Dou Identity Check**

Scope only:
- compare multiple same-building gong-head terminals in Drawing 11 / relevant photographs;
- estimate only the localized shaping extent if source resolution permits;
- identify the small dou above the target gong head from primary source terminology/position;
- determine whether it must become a new independent physical participant.

No new Blender build is authorized until this check closes.
