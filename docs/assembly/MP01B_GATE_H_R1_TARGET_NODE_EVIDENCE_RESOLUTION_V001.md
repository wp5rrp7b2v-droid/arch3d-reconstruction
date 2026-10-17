# MP-01B Gate H-R1｜Target Node Evidence Resolution V001

Status: **PARTIAL PASS / TARGET COMPONENT SET + LINGGONG DIRECTION RESOLVED / CORRECTED BUILD NOT YET AUTHORIZED**  
Date: 2026-10-06

## 1. Scope

This gate rechecks only the two East-Seam support nodes at the ends of `平梁-东缝`.

It does not rebuild Blender geometry.

Authoritative source:
- `SRC-ZG-WF-001` detailed survey report;
- `SRC-ZG-WF-002 / S15` only as a secondary directionality cross-check;
- A2 official same-building description only for the named Tuofeng/Linggong support role.

## 2. Terminology correction

The previous Gate H evidence-recheck note used **柱斗** for the target interior dou.

That wording is incorrect.

The primary source consistently identifies the component as:

> **襻间 / 隔架用栌斗**

and, in the height decomposition:

> **襻间栌斗平欹**

Source:
- PDF p98–99 / printed p83–84 / Fig.2-63 / Table 2-49;
- PDF p107 / printed p92;
- Appendix 1-10 / PDF p347 / printed p332.

Therefore all future MP-01B work must use **襻间栌斗**, not 柱斗.

## 3. Target node identification

Drawing 11 places the two Pingliang endpoints on the two `上平槫` support lines.

Appendix 1-9 has exact East-Seam entries for:

- `东缝前上平槫下襻间`
- `东缝后上平槫下襻间`

These are the relevant target-node records for MP-01B.

The earlier ±1836 mm support stations are therefore retained as the two upper-purlin / Pingliang-end station candidates.

No inward shift is authorized by this recheck.

## 4. Direct target components from Appendix 1-9

### 4.1 East-Seam FRONT upper-purlin bracket

`东缝前上平槫下襻间`

Direct records:

- **进深华栱**
  - 广 = 221 mm
  - 厚 = 153 mm
  - 长 = descriptive: `一端栱头，一端至托脚`

- **顺身令栱**
  - 广 = 213 mm
  - 厚 = 149 mm
  - 长 = **1016 mm**

- **襻间枋**
  - 广 = 210 mm
  - 厚 = 152 mm
  - 长 / end form = `隐刻翼形`

### 4.2 East-Seam REAR upper-purlin bracket

`东缝后上平槫下襻间`

Direct records:

- **进深华栱**
  - 广 = 210 mm
  - 厚 = 156 mm
  - 长 = descriptive: `一端栱头，一端至托脚`

- **顺身令栱**
  - 广 = 217 mm
  - 厚 = 150 mm
  - 长 = **995 mm**

- **襻间枋**
  - 广 / 厚 = 未及
  - end form = `隐刻翼形`

## 5. Linggong direction is now resolved

Appendix 1-9 explicitly labels the target Linggong as:

> **顺身令栱**

and the target Huagong as:

> **进深华栱**

For the existing MP-01B assembly coordinate:

- assembly Y = transverse / front-back / 进深 direction;
- assembly X = East-Seam line / out-of-section / 顺身 direction.

Therefore:

> **Target Linggong long axis = assembly X, not assembly Y.**

The Gate G/H rule:

`Linggong local +X → assembly +Y / Rz +90°`

is superseded for the target nodes.

Corrected target rule:

`Linggong local +X → assembly X / Rz 0°`

Classification:

`DIRECT_PRIMARY / POSITION-LABELLED DIRECTION`

This is no longer merely a visual inference.

S15 supports the need to distinguish `横栱方向` and `华栱方向`, but S15 is not the authority for this target-node lock; Appendix 1-9 is.

## 6. The visible curved member in Drawing 11

Because Drawing 11 is a transverse / 进深 section:

- the **进深华栱** lies in the section plane and can appear as a long curved gong profile;
- the **顺身令栱** is out of the section plane and should not be interpreted as the long curved member visible in that section.

This resolves the earlier visual confusion.

The Gate H Review Board rendered the Linggong itself as the in-section long member; that representation is not consistent with the position-labelled source record.

## 7. Direct target Linggong dimensions supersede the analog envelope

Gate F/H used the same-building interior analog:

`893.3 × 153.6 × 215.0 mm`

for the target Linggong.

Appendix 1-9 now provides target-position direct values.

For MP-01B target instances:

### FRONT target Linggong

- length = **1016 mm**
- profile height / 广 = **213 mm**
- thickness / 厚 = **149 mm**

### REAR target Linggong

- length = **995 mm**
- profile height / 广 = **217 mm**
- thickness / 厚 = **150 mm**

Classification:

`DIRECT_PRIMARY / POSITION-SPECIFIC / OBSERVED_AS_MEASURED`

The 893.3 × 153.6 × 215.0 analog remains valid only as evidence for another interior Linggong context and must not control these two target instances.

## 8. Target 襻间栌斗 evidence

Appendix 1-10 directly records the `上平槫下` target locations.

### East-Seam FRONT upper-purlin Ludou

- 上宽 = 321 mm
- 下宽 = 221 mm
- 上深 = 355 mm
- 下深 = 未及
- 总高 = 未及
- 平高 = 未及
- 欹高 = 未及

### East-Seam REAR upper-purlin Ludou

- 上宽 = 320 mm
- 下宽 = 227 mm
- 上深 = 357 mm
- 下深 = 未及
- 总高 = **219 mm**
- 平高 = **45 mm**
- 欹高 = **65 mm**

This target family is not the existing exterior `柱头栌斗` Master.

A new interior `襻间/隔架用栌斗` family boundary is required before corrected engineering build.

## 9. Correct vertical decomposition

SRC-ZG-WF-001 PDF p107 / printed p92 states:

> 下平槫与上平槫之高差 = 61分；其中 **四椽栿、驼峰、襻间栌斗平欹共垫高40分**。

Therefore:

`40 fen = Four-Chuanfu + Tuofeng + Ludou flat/sloped contribution`

It does **not** include the Linggong as a simple additive full-height body.

At the report's `15.3 mm/fen` analytical scale:

- 40 fen = 612 mm;
- Four-Chuanfu design-analysis thickness = 20 fen = 306 mm;
- residual above Four-Chuanfu = 306 mm.

### East-Seam REAR candidate residual

Direct target Ludou:
- 平高 + 欹高 = 45 + 65 = **110 mm**.

Therefore a bounded assembly calculation gives:

`Tuofeng vertical contribution candidate = 306 - 110 = 196 mm`

Classification:

`SECONDARY_CALCULATED / REPORT_MODULAR_DECOMPOSITION + DIRECT_LOCATION_LUDOU / REPLACEABLE`

Historical exact Tuofeng height claim: **false**.

### East-Seam FRONT

Target Ludou 平高 / 欹高 are `未及`.

Therefore exact target-front Tuofeng vertical contribution remains:

`UNKNOWN`

Do not silently copy the rear 196 mm value to the front.

A future build may use an explicitly declared parametric completion, but that choice requires a separate gate.

## 10. Corrected target-node component set

The evidence-bounded target support node is no longer a three-member additive stack.

Minimum physical participants now are:

1. `四椽栿-东缝`
2. target `驼峰`
3. target `襻间栌斗`
4. target `进深华栱`
5. target `顺身令栱`
6. target `襻间枋`
7. `平梁-东缝`

The front and rear support nodes each have their own position-specific measurements.

A2's abbreviated statement `四椽栿上用驼峰、令栱承平梁` remains valid as role evidence, but it is not a complete component inventory of the bracket node.

## 11. Existing Master reuse decisions

### Existing outer-eaves Huagong Master

`CMP-GONG-HUAGONG-001_MASTER`

Scope is the 56-record outer-eaves first/second-jump subset.

Decision:

> **NO direct reuse as target interior Huagong geometry authority.**

The target `进深华栱` has separate position-labelled direct measurements and role.

### Existing column-head Ludou Master

`CMP-LUDOU-COLUMN-001_MASTER`

Scope is exterior column-head Ludou.

Decision:

> **NO direct reuse as target interior 襻间栌斗 geometry authority.**

The report explicitly treats 襻间/隔架用栌斗 as a separate measured interior group.

### Interior Linggong Master

`CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`

Family identity remains useful.

However the target instances must use the direct Appendix 1-9 measurement sets rather than the Gate F analog dimensions.

## 12. What is resolved

**RESOLVED / DIRECT PRIMARY**

- target node = East-Seam front/rear `上平槫下襻间`;
- Linggong is `顺身`;
- Huagong is `进深`;
- Linggong target long axis is out-of-section / assembly X;
- target FRONT Linggong = 1016 × 213 × 149 mm;
- target REAR Linggong = 995 × 217 × 150 mm;
- target Ludou location-specific dimensions as listed above;
- target node contains Huagong + Linggong + 襻间枋 + 襻间栌斗;
- 306 mm residual is not Linggong full height.

## 13. What remains unresolved

- target-front Ludou total / flat / sloped height;
- target-front Tuofeng vertical contribution;
- exact Tuofeng historical profile and dimensions;
- exact hidden slots / mortise / tenon / contact-face topology;
- exact full length of target 进深华栱 (source gives endpoint semantics, not a numeric length);
- exact hidden relationship of 襻间枋;
- whether a parametric completion should use family mean, mirrored counterpart, or assembly envelope for missing front Ludou heights.

These are not blockers to defining component identity and direction, but they block a corrected two-sided deterministic build contract until a completion rule is approved.

## 14. Gate result

**PARTIAL PASS**

The key directional and component-identity problem that invalidated Gate H is now resolved.

No Blender rebuild is authorized yet.

Next complete step:

> **MP-01B Gate H-R2｜Interior Huagong + Panjian Ludou Scope & Missing-Height Completion Rule**

Gate H-R2 must:
1. define the new interior Huagong family boundary;
2. define the new interior Panjian/Spacer Ludou family boundary;
3. choose one explicit, replaceable completion rule for the FRONT Ludou missing height fields;
4. preserve the REAR direct values unchanged;
5. prepare, but not yet execute, a corrected assembly contract.
