# AF-01 / B02｜Visible Body Length / End Extent V001

- Date: **2026-09-30**
- Task: **AF01-B02**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: 下六椽栿 / 上六椽栿 / 四椽栿 / 平梁 visible main body only

## 1. Problem

The four approved Masters intentionally retain:

- historical full length = `UNKNOWN / null`;
- canonical/reference specimen length = 1000 mm;
- explicit hard fail against reference-length leakage into assembly/building.

AF-01 already has deterministic support-axis spans, but not historical end projections, hidden tenons, insertion depths, or end machining.

B02 must therefore provide a building-specific realization length without converting missing historical end details into invented fact.

## 2. Source / control geometry

The report's roof-frame method diagram provides a symmetric modular transverse control:

- column axes: `-350 / -120 / +120 / +350 fen`;
- roof control sequence includes `-445 / -350 / -235 / -120 / 0 / +120 / +235 / +350 / +445 fen`;
- `MOD-002 = 15.3 mm/fen`.

The existing AF-01 / T-020 controls therefore give:

- outer column axes = `Y ±5355.0 mm` = ±350 fen;
- lower-purlin / Four-Chuanfu support axes = `Y ±3595.5 mm` = ±235 fen;
- upper-purlin / Pingliang support axes = `Y ±1836.0 mm` = ±120 fen.

The report directly identifies the members as six-rafter / four-rafter / pingliang tiers, but does **not** publish the historical full timber end projection beyond those support/control axes.

## 3. B02 engineering rule

For the AF-01 first article only:

> **Visible main-body end planes are placed at the two locked functional support axes.**

This is the minimum deterministic body envelope necessary to assemble the frame.

It means:

- no historical tenon is invented;
- no unsupported overhang beyond the support axis is invented;
- no support-axis span is relabelled as historical full timber length;
- omitted end projection means **UNKNOWN / NOT MATERIALIZED**, not “historically absent”.

Classification:

**RECONSTRUCTED_DESIGN / AF01_LOCAL / MINIMUM_VISIBLE_BODY_EXTENT / REPLACEABLE**

Historical full length remains `UNKNOWN / null`.

## 4. Locked candidate extents

AF-01 slice axis:

`X = +2218.5 mm`

B01 support-plane Z values remain unchanged.

### 4.1 下六椽栿

- north end plane: `Y = -5355.0 mm`
- south end plane: `Y = +5355.0 mm`
- realization length: **10710.0 mm**
- modular cross-check: `700 fen × 15.3 = 10710.0 mm`

### 4.2 上六椽栿

- north end plane: `Y = -5355.0 mm`
- south end plane: `Y = +5355.0 mm`
- realization length: **10710.0 mm**
- modular cross-check: `700 fen × 15.3 = 10710.0 mm`

### 4.3 四椽栿

- north end plane: `Y = -3595.5 mm`
- south end plane: `Y = +3595.5 mm`
- realization length: **7191.0 mm**
- modular cross-check: `470 fen × 15.3 = 7191.0 mm`

### 4.4 平梁

- north end plane: `Y = -1836.0 mm`
- south end plane: `Y = +1836.0 mm`
- realization length: **3672.0 mm**
- modular cross-check: `240 fen × 15.3 = 3672.0 mm`

## 5. Combined AF-01 body placement controls

| Instance | X mm | Y end planes mm | support-plane Z mm | realization length mm |
|---|---:|---:|---:|---:|
| 下六椽栿-东缝 | +2218.5 | -5355.0 / +5355.0 | 4360.5 | 10710.0 |
| 上六椽栿-东缝 | +2218.5 | -5355.0 / +5355.0 | 5003.1 | 10710.0 |
| 四椽栿-东缝 | +2218.5 | -3595.5 / +3595.5 | 5658.4 | 7191.0 |
| 平梁-东缝 | +2218.5 | -1836.0 / +1836.0 | 6406.2 | 3672.0 |

These values define only the **visible rectangular main-body envelope** used by the approved Masters.

## 6. End-detail boundary

B02 explicitly does not materialize:

- hidden tenons;
- dovetails / mortises;
- beam-end reduction;
- insertion depth into bracket work;
- historical end projection beyond support axes;
- wear / deformation / nonuniform end profiles.

If later direct evidence proves an end projection or joint body beyond the support axis, the AF-01 body endpoint may be replaced without changing the support axes, B01 Z authority, or Master identity.

## 7. Master / builder implementation guard

The canonical Masters use a 1000 mm non-historical reference realization.

Future AF-01 builder must:

1. instantiate the approved Master identity;
2. apply the AF-01 installation orientation;
3. replace its longitudinal realization length with the B02 instance length;
4. center the body between the two explicit Y end planes;
5. after orientation, align the transformed body bottom face to the B01 support-plane Z.

Hard fail:

`REFERENCE_LENGTH_LEAKS_INTO_BUILDING`

must remain active.

## 8. Cross-check against report diagram

The report's method diagram shows the tier hierarchy and control-axis spans used above. It also visually shows beam-end details near support zones, but those drawn projections are not dimensioned as historical full-length measurements.

Therefore the drawing is used to validate:
- tier identity;
- support-axis relationship;
- symmetry;
- relative span.

It is **not** used to raster-measure an undocumented historical end projection.

## 9. B02 Gate

Candidate result:

- Lower Six visible main body = **10710.0 mm**
- Upper Six visible main body = **10710.0 mm**
- Four-Chuanfu visible main body = **7191.0 mm**
- Pingliang visible main body = **3672.0 mm**

Historical full lengths remain UNKNOWN.

No Master mutation.
No Registry mutation.
No Blender.
B03 remains open.
T-018 remains HOLD.

If Product Owner approves:

**B02 closes. AF-01 will then have only B03 remaining before first-article engineering readiness review.**
