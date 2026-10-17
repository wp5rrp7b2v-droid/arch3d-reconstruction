# MP-01B Gate F｜Lower Assembly Local Metric Envelope + Placement Resolution V001

Status: **PASS / FIRST LOWER-ASSEMBLY NUMERIC CONTRACT RESOLVED / BLENDER NOT YET AUTHORIZED**
Date: 2026-10-06

## 1. Goal

Resolve the minimum assembly-owned numbers required for:

`四椽栿-东缝 → 驼峰 LOWER_SUPPORT / 梁架承托令栱 → 平梁-东缝`

without promoting reconstructed values to historical facts.

## 2. Source basis

### A1｜Direct component sections

Four-Chuanfu Master:
- width = **426.5 mm**
- thickness = **302.0 mm**
- historical full length = UNKNOWN

Pingliang EW Master:
- width = **395.5 mm**
- thickness = **280.5 mm**
- historical full length = UNKNOWN

### A1｜Roof-frame design drawing

Report Drawing 10 / PDF p291 / printed p276 gives the central transverse spacing sequence:

`1836 / 1836 / 1760 / 1760 ...`

For the Minimum Proof:
- Pingliang endpoints are resolved to the first symmetric purlin stations: `±1836 mm`;
- Four-Chuanfu endpoints are resolved to the next symmetric purlin stations: `±(1836+1760) = ±3596 mm`.

These are:
`REPORT_INFERRED / SOURCE_DRAWING_TOPOLOGY / REPLACEABLE`

They are not claimed as directly measured historical timber full lengths.

### A1｜Purlin-height decomposition

Table 2-52:
- East-Seam front `B = 612 mm`
- report mean `B = 602.3 mm`
- report rounded design = **40 fen**

The report's following conclusion states that the lower-to-upper purlin tier uses a **40-fen padding stack** in which Four-Chuanfu and its intermediate support system participate.

Four-Chuanfu design thickness is rounded to **20 fen** in Table 2-39.

Therefore the first assembly candidate for the clear support envelope above the Four-Chuanfu is:

`40 fen - 20 fen = 20 fen = 306 mm`

Classification:
`REPORT_INFERRED / MODULAR_DECOMPOSITION / REPLACEABLE`

Cross-check only:
- East-Seam-front B 612 mm
- minus observed Four-Chuanfu mean thickness 302 mm
- = 310 mm

Difference from the 306 mm design candidate = **4 mm**.

The 310 mm cross-check is not treated as a target-instance exact value because the Four-Chuanfu raw samples are not mapped to East/West seam instances.

### A1｜New same-building interior Linggong analog

Table 2-48:
- interior gong material pool: `广 215.0 mm`, `厚 153.6 mm`;
- `四六椽栿隔架令栱` mean length = **893.3 mm**, n=3.

This is a direct interior-frame analog, but not the exact MP-01B target role.

Use classification:

`SAME_BUILDING_INTERIOR_ANALOG / RECONSTRUCTED_ASSEMBLY_CANDIDATE / REPLACEABLE`

## 3. MP-01B local coordinate system

- X = East-Seam frame-line / out-of-section direction
- Y = transverse section direction; South positive / North negative
- Z = vertical up

Origin:

`O = center of Four-Chuanfu upper face`

Therefore:
- Four-Chuanfu top = `Z=0`
- Four-Chuanfu bottom = `Z=-302`

This is an assembly-local project coordinate, not a survey datum.

## 4. Beam realizations

### Four-Chuanfu

Instance:
`四椽栿-东缝`

Master:
`CMP-FRAME-FOUR-CHUANFU-001_MASTER`

Realization:
- length = **7192 mm**
- width = 426.5 mm
- thickness = 302.0 mm
- Y extent = `[-3596,+3596]`
- top Z = 0
- bottom Z = -302

Length classification:
`REPORT_INFERRED / SOURCE_DRAWING_TOPOLOGY / REPLACEABLE`

Historical full-length claim = false.

### Pingliang

Reuse the MP-01A accepted realization:

- length = **3672 mm**
- width = 395.5 mm
- thickness = 280.5 mm
- Y extent = `[-1836,+1836]`
- underside Z = **306 mm**
- top Z = **586.5 mm**

Length:
`RECONSTRUCTED_DESIGN / MINIMUM SUPPORT SPAN / REPLACEABLE`

Vertical placement:
`REPORT_INFERRED / MODULAR_DECOMPOSITION / REPLACEABLE`

## 5. Lower support stations

Create two Minimum-Proof assembly stations:

- `SUPPORT_SOUTH`: Y = **+1836 mm**
- `SUPPORT_NORTH`: Y = **-1836 mm**

These are aligned to the first symmetric purlin / Pingliang-end stations in Drawing 10.

Classification:
`REPORT_INFERRED / SOURCE_DRAWING_TOPOLOGY`

They do not establish exact hidden contact centers.

## 6. Interior Linggong assembly realization

Master:
`CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`

Role:
`LOWER_PINGLIANG_SUPPORT`

For this Minimum Proof, use the same-building interior analog envelope:

- body length = **893.3 mm**
- total height = **215.0 mm**
- depth = **153.6 mm**

Preserve the approved neutral two-zone topology:
- BODY_ZONE height = **129.0 mm** (60%)
- UPPER_BEARING_ZONE height = **86.0 mm** (40%)
- upper bearing length = **491.315 mm** (55% of 893.3)
- upper bearing depth = **153.6 mm**

Classification:
`SAME_BUILDING_INTERIOR_ANALOG / RECONSTRUCTED_ASSEMBLY_CANDIDATE / REPLACEABLE`

Historical target-role metric claim = false.

Create:
- `ASM-MP01B-LINGGONG-SOUTH-01`
- `ASM-MP01B-LINGGONG-NORTH-01`

These are Minimum-Proof reconstructed assembly instances and do not create a whole-hall physical count.

## 7. Tuofeng LOWER_SUPPORT assembly realization

Available support gap:

`306.0 - 215.0 = 91.0 mm`

Therefore Tuofeng total assembly height candidate:

**91.0 mm**

Preserve the approved LOWER_SUPPORT two-tier topology:
- base height = **45.5 mm**
- upper-seat height = **45.5 mm**

Assembly footprint:
- base span = **893.3 mm** — matched to Linggong analog body length
- base depth = **426.5 mm** — matched to Four-Chuanfu upper-face width
- upper-seat span = **375.186 mm** — 42% normalized Master rule
- upper-seat depth = **153.6 mm** — matched to Linggong analog depth

Classifications:
- height = `SECONDARY_CALCULATED / RESIDUAL_WITHIN_20_FEN_SUPPORT_ENVELOPE / REPLACEABLE`
- base span = `SECONDARY_CALCULATED / ASSEMBLY_FOOTPRINT_MATCH`
- base depth = `SECONDARY_CALCULATED / FOUR_CHUANFU_FOOTPRINT_MATCH`
- upper seat = `RECONSTRUCTED_DESIGN / MASTER_NORMALIZED_TOPOLOGY + LINGGONG_FOOTPRINT`

Historical metric claim = false.

Create:
- `ASM-MP01B-TUOFENG-LOWER-SOUTH-01`
- `ASM-MP01B-TUOFENG-LOWER-NORTH-01`

No whole-hall count claim.

## 8. Vertical stack

At each South/North station:

```text
Four-Chuanfu top          Z =   0.0
Tuofeng top               Z =  91.0
Interior Linggong top     Z = 306.0
Pingliang underside       Z = 306.0
Pingliang top             Z = 586.5
```

Relationship semantics:

`FOUR_CHUANFU → TUOFENG LOWER → INTERIOR LINGGONG → PINGLIANG`

This is a production assembly chain.

It is **not** a claim that the exact historical contact topology or hidden joinery has been recovered.

## 9. Retained UNKNOWN

Still UNKNOWN:
- exact East-Seam target Linggong dimensions;
- target Linggong profile;
- exact asymmetric end shape;
- exact support center/contact face;
- Tuofeng historical dimensions/profile;
- exact Tuofeng↔Linggong contact;
- exact Linggong↔Pingliang contact;
- hidden mortise/tenon/groove geometry;
- physical whole-hall counts for interior Linggong/Tuofeng;
- per-instance mapping outside this Minimum Proof.

## 10. Gate F result

**PASS**

The lower subassembly now has a deterministic, evidence-classified numeric contract sufficient for a first assembly build.

Important:
- direct component sections remain direct;
- beam lengths are assembly-derived;
- target-role Linggong metrics are not falsely called direct;
- Tuofeng dimensions are explicit reconstructed residuals;
- no outer-eaves Linggong dimensions/profile are used as the geometry authority;
- no hidden joint is invented.

## 11. Next complete step

> **MP-01B Gate G｜Lower Assembly First Build Preparation**

Gate G will lock:
- exact object list;
- placement transforms;
- relation metadata;
- machine checks;
- perturbation test;
- Review Board design.

Blender execution remains **NOT AUTHORIZED** at Gate F.
