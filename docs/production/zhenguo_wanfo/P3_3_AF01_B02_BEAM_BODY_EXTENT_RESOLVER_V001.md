# AF-01 / B02｜Four Horizontal Beam Body-Extent Resolver V001

- Date: **2026-09-30**
- Task: **AF01-B02**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: 下六椽栿 / 上六椽栿 / 四椽栿 / 平梁 visible execution body extents only

## 1. Problem

All four approved Masters intentionally retain:

- historical full length = `UNKNOWN / null`;
- 1000 mm canonical realization = `NON-HISTORICAL REFERENCE ONLY`;
- reference-length leakage into assembly/building = HARD FAIL.

AF-01 already has deterministic support-axis spans, but B02 still needs an explicit building-specific execution body extent.

## 2. Source boundary

Same-building source provides the following useful constraints:

- lower six-chuanfu enters the column-head puzuo and bears in the second-jump huagong region;
- upper six-chuanfu presses on the second lower-ang and **terminates at the column-center position**;
- Fig. 2-73 provides the report's idealized beam-frame method drawing with the same transverse control grid used by AF-01;
- Four-Chuanfu / Pingliang bodies are visually tied to their corresponding support tiers in the report drawings.

However the report does **not** publish a directly measured historical full-length table for these four beam instances.

Therefore B02 MUST NOT claim that the execution lengths below are measured historical timber lengths.

## 3. Minimal AF-01 body-extent rule

For the first-article assembly only:

> **The rectangular visible/execution body envelope terminates at its two locked support axes. Any hidden penetration, tenon, buried end, projection beyond the support axis, or local end reduction remains UNKNOWN and is omitted from the body envelope.**

This is the smallest deterministic rule that:

- prevents 1000 mm reference-length leakage;
- preserves all locked support geometry;
- does not invent hidden historical joinery;
- is replaceable if later direct end-length evidence becomes available.

Classification:

**REPORT_INFERRED / DRAWING_DERIVED / RECONSTRUCTED_DESIGN / AF01_LOCAL / REPLACEABLE**

## 4. Locked support-axis coordinates inherited by B02

AF-01 section plane:

- X = **+2218.5 mm**
- beam longitudinal direction = world Y

Support-axis endpoints:

| Beam | South end Y | North end Y | Axis span |
|---|---:|---:|---:|
| 下六椽栿 | -5355.0 | +5355.0 | 10710.0 mm |
| 上六椽栿 | -5355.0 | +5355.0 | 10710.0 mm |
| 四椽栿 | -3595.5 | +3595.5 | 7191.0 mm |
| 平梁 | -1836.0 | +1836.0 | 3672.0 mm |

These are execution-envelope endpoints, not historical full-member endpoints.

## 5. B02 candidate outputs

### 下六椽栿-东缝

- execution body Y range = `[-5355.0, +5355.0] mm`
- `REALIZATION_LENGTH_MM = 10710.0`
- source-specific boundary: the report says the beam enters the column-head puzuo; any additional buried penetration beyond the support-axis cutoff remains UNKNOWN and is not modeled.

### 上六椽栿-东缝

- execution body Y range = `[-5355.0, +5355.0] mm`
- `REALIZATION_LENGTH_MM = 10710.0`
- strongest source condition: report explicitly states termination at the column-center position.
- this candidate is therefore directly consistent with the support-axis cutoff.

### 四椽栿-东缝

- execution body Y range = `[-3595.5, +3595.5] mm`
- `REALIZATION_LENGTH_MM = 7191.0`
- ends are cut at the locked lower-purlin/support axes for the AF-01 envelope.
- any hidden end extension associated with Tuojiao/contact/joinery remains UNKNOWN.

### 平梁-东缝

- execution body Y range = `[-1836.0, +1836.0] mm`
- `REALIZATION_LENGTH_MM = 3672.0`
- ends are cut at the locked inner support / upper-purlin control axes for the AF-01 envelope.
- any hidden end extension or local end treatment remains UNKNOWN.

## 6. Installation transform

All four Masters use a local long-member convention.

AF-01 installation mapping:

- Master local longitudinal axis `+X` → world `+Y`;
- Master local `section_width / 广` → world `+Z`;
- Master local `thickness / 厚` → world `+X`.

The beam center is at:

- world `Y = 0`;
- world `X = +2218.5 mm`;
- world Z determined by the locked B01 support plane.

Runtime geometry MUST change the longitudinal realization length only. Section dimensions must not be scaled.

## 7. B01 + B02 deterministic placement table

| Beam | X mm | Y range mm | Support-plane Z mm | Execution length mm |
|---|---:|---:|---:|---:|
| 下六椽栿 | +2218.5 | -5355 → +5355 | 4360.5 | 10710.0 |
| 上六椽栿 | +2218.5 | -5355 → +5355 | 5003.1 | 10710.0 |
| 四椽栿 | +2218.5 | -3595.5 → +3595.5 | 5658.4 | 7191.0 |
| 平梁 | +2218.5 | -1836 → +1836 | 6406.2 | 3672.0 |

Implementation guard inherited from B01:

> After roll/orientation, align the transformed body bottom face to the support-plane Z. Do not assign the canonical Master object origin directly to support-plane Z.

## 8. What B02 does NOT resolve

B02 does not resolve:

- historical full timber length;
- buried insertion depth inside column-head puzuo;
- tenons or mortises;
- end-profile carving/reduction;
- camber;
- hidden local section changes;
- Tuojiao exact contact points;
- Shuzhu / Chashou endpoints.

Those remain outside B02.

## 9. Cross-check against report ideal-frame drawing

Fig. 2-73 uses the same transverse modular control lines:

- outer-column control at ±350 fen;
- lower-purlin/support control at ±235 fen;
- inner / upper-purlin control at ±120 fen.

With `MOD-002 = 15.3 mm/fen`:

- 700 fen = 10710.0 mm;
- 470 fen = 7191.0 mm;
- 240 fen = 3672.0 mm.

This matches the three existing AF-01 support-axis spans exactly.

Cross-check status:

**PASS / REPORT-IDEAL-DRAWING CONSISTENT / NOT DIRECT HISTORICAL FULL-LENGTH MEASUREMENT**

## 10. Gate

B02 Candidate:

- Lower Six execution length = **10710.0 mm**
- Upper Six execution length = **10710.0 mm**
- Four-Chuanfu execution length = **7191.0 mm**
- Pingliang execution length = **3672.0 mm**

- historical full lengths remain `UNKNOWN / null`;
- Master 1000 mm reference does not enter building geometry;
- Master mutation = NONE;
- Registry mutation = NONE;
- Blender = NOT AUTHORIZED;
- B03 = NOT STARTED;
- T-018 = HOLD.

If Product Owner approves:

**AF01-B02 closes. AF-01 will have only B03 remaining before engineering readiness review.**
