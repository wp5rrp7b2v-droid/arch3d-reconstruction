# MP-01A Gate C｜Assembly-Local Numeric Placement Resolver V001

Status: **PASS / MINIMUM NUMERIC INPUTS LOCKED FOR FIRST BUILD / BLENDER BUILD REQUIRES NEXT AUTHORIZATION**
Date: 2026-10-06

## 1. Purpose

Resolve only the minimum numeric values needed to generate the first actual 3D Minimum Proof for the East-Seam upper ridge-support subassembly:

`平梁-东缝 → 驼峰(UPPER_RIDGE_SUPPORT) → 蜀柱-东缝 + 叉手-东缝-南/北侧`

No value in this Gate is promoted beyond its stated evidence class.

## 2. Assembly-local coordinate system

Use an assembly-local coordinate system for MP-01A only:

- `X` = along the East-Seam frame-line longitudinal/out-of-section direction;
- `Y` = transverse section direction, South positive / North negative;
- `Z` = vertical upward.

Origin:

`O = center of Pingliang upper connection plane`

Therefore:

- Pingliang centerline in section: `Y = 0`
- Pingliang upper connection plane: `Z = 0`
- East-Seam frame plane: `X = 0`

This origin is a project assembly coordinate, not a historical survey coordinate.

## 3. Direct / locked component envelopes used

### Pingliang

Master:
`CMP-FRAME-PINGLIANG-001_MASTER / EW_SEAM`

Use:
- section width = **395.5 mm**
- section thickness = **280.5 mm**

Classification:
`DIRECT_PRIMARY / CONFIRMED_FAMILY_MEAN`

Historical full length remains UNKNOWN.

### Shuzhu

Master:
`CMP-FRAME-SHUZHU-001_MASTER`

Canonical production section:
- width = **218.75 mm**
- thickness = **157.5 mm**

Classification:
`DIRECT_MEASURED_REPORT_MEAN_WITH_MATCHING_RECOMPUTE`

East-Seam position-labelled source sample remains separately recorded as 218 × 158 mm; Gate C does not create a new geometry variant.

### Chashou

Master:
`CMP-FRAME-CHASHOU-001_MASTER`

Production section:
- width = **230.5 mm**
- thickness = **90.5 mm**

Classification:
`DIRECT_MEASURED_REPORT_MEAN_WITH_MATCHING_RECOMPUTE`

## 4. Vertical source calibration from Fig. 2-71

Primary source:
- PDF p106 / printed p91 / Fig. 2-71
- PDF p107 / printed p92 / Table 2-52

Direct East-Seam value:
- `东缝前 C = 1245 mm`
- `东缝后 C = 未及`

The 1245 mm value is a purlin-level rise and is **not** a direct Shuzhu length.

For the Minimum Proof only, Fig. 2-71 is used as a source-image calibration for the visible Pingliang → Tuofeng → Shuzhu / Chashou stack.

Calibration anchors on the preserved figure snapshot:
- lower C reference / Pingliang upper-interface line ≈ image row 293;
- upper C reference ≈ image row 155;
- span = 138 px = 1245 mm;
- vertical image scale ≈ **9.02 mm/px**.

This calibration is:
`RECONSTRUCTED_DESIGN / SOURCE_IMAGE_CALIBRATED / REPLACEABLE`

It is not direct measurement.

### Derived local vertical values

Visible Tuofeng upper seat:
- source-image rise ≈ 22 px
- calibrated ≈ 198.5 mm
- locked production candidate = **200 mm**

Visible Shuzhu / Chashou upper convergence region:
- source-image rise ≈ 98 px
- calibrated ≈ 884.1 mm
- locked production candidate = **885 mm**

Therefore:
- Tuofeng top seat datum = `Z = 200 mm`
- Shuzhu/Chashou upper target datum = `Z = 885 mm`
- endpoint-derived Shuzhu realization length = **685 mm**

Ridge-purlin source-reference level remains:
- `Z_ref = 1245 mm`

Difference between upper convergence target and ridge-purlin reference:
- **360 mm**

This 360 mm is not assigned to a named historical component in MP-01A.
It remains `UNRESOLVED RIDGE SUPPORT STACK`.

## 5. Horizontal / transverse placement

Existing report-derived project parameter:

`FR-006 = 1836 mm`

Meaning in the existing parameter set:
- third frame-depth design candidate;
- 6 chi;
- `HIGH_CONFIDENCE_INFERENCE / REPORT_INFERRED / REPLACEABLE`.

Fig. 2-71 source-image calibration independently places the visible Chashou lower anchors at approximately 1.82–1.84 m from the centerline.

Gate C therefore adopts:

- South Chashou lower anchor: `Y = +1836 mm`
- North Chashou lower anchor: `Y = -1836 mm`

Classification:

`RECONSTRUCTED_DESIGN / CROSS_CONSTRAINED_BY_REPORT_INFERENCE_AND_SOURCE_IMAGE`

This does not claim 1836 mm is a directly measured Chashou anchor coordinate.

## 6. Pingliang realization for MP-01A

Minimum required support span:

`2 × 1836 = 3672 mm`

For the first build only:

- Pingliang realization length = **3672 mm**
- center = `(0,0,-140.25)`
- top plane = `Z=0`
- bottom plane = `Z=-280.5`

Classification:

`RECONSTRUCTED_DESIGN / MINIMUM_SUPPORT_SPAN / REPLACEABLE`

This is **not** the historical full length.

## 7. Tuofeng UPPER_RIDGE_SUPPORT production envelope

Master:
`CMP-FRAME-TUOFENG-001_MASTER / UPPER_RIDGE_SUPPORT`

The first-article 1000 × 500 × 320 fixture is **not reused** as a building dimension.

Gate C resolves a new assembly-owned envelope:

- base span along Y = **1325 mm**
- depth along X = **395.5 mm**
- height = **200 mm**

Basis:
- span + height: `SOURCE_IMAGE_CALIBRATED / RECONSTRUCTED_DESIGN`;
- depth: `SECONDARY_CALCULATED / ASSEMBLY_FOOTPRINT_MATCH` to Pingliang width;
- all values replaceable;
- historical metric claim = false.

The approved normalized stepped-hump topology is preserved.

At 1325 mm base span, the normalized flat central seat is about 318 mm wide, sufficient to contain the 218.75 mm Shuzhu production width without changing the Master topology.

## 8. Endpoint resolver result

### Shuzhu

Lower:
`P_lower = (0, 0, 200)`

Upper:
`P_upper = (0, 0, 885)`

Resolved:
- length = **685 mm**
- direction = vertical

Classification:
`RECONSTRUCTED_DESIGN / ENDPOINT_DERIVED`

### South Chashou

Lower:
`P_lower = (0, +1836, 0)`

Upper:
`P_upper = (0, 0, 885)`

Resolved:
- length ≈ **2038.2 mm**
- rise angle ≈ **25.74° above horizontal**

### North Chashou

Lower:
`P_lower = (0, -1836, 0)`

Upper:
`P_upper = (0, 0, 885)`

Resolved:
- length ≈ **2038.2 mm**
- mirror direction
- rise angle ≈ **25.74° above horizontal**

Classification for both:
`RECONSTRUCTED_DESIGN / ENDPOINT_DERIVED / REPLACEABLE`

No historical fixed angle is claimed.

## 9. First-build object table

| Object | Numeric realization | Evidence class |
|---|---:|---|
| 平梁-东缝 | 3672 × 395.5 × 280.5 mm envelope | section DIRECT_PRIMARY; length RECONSTRUCTED_DESIGN |
| 驼峰 Upper | 1325 × 395.5 × 200 mm envelope | RECONSTRUCTED_DESIGN / SOURCE_IMAGE_CALIBRATED |
| 蜀柱-东缝 | section 218.75 × 157.5; length 685 mm | section DIRECT_PRIMARY mean; length ENDPOINT_DERIVED |
| 叉手-东缝-南侧 | section 230.5 × 90.5; length ≈2038.2 mm | section DIRECT_PRIMARY mean; length/angle ENDPOINT_DERIVED |
| 叉手-东缝-北侧 | same mirrored | same |
| Ridge target datum | (X=0,Y=0,Z=885) | RECONSTRUCTED_DESIGN assembly datum |
| Ridge-purlin reference level | Z_ref=1245 | 1245 DIRECT East-Seam-front C used as reference/calibration, not Shuzhu length |

## 10. UNKNOWN retained

The following remain explicitly UNKNOWN:

- historical Pingliang full length;
- exact historical Tuofeng dimensions/profile;
- exact Shuzhu historical full height;
- exact historical Chashou angle/full length;
- East-Seam rear C (`未及`);
- exact ridge-purlin segment-end owner;
- exact intermediate block(s) between Shuzhu/Chashou convergence and ridge purlin;
- all hidden joinery;
- exact contact faces.

## 11. Gate C PASS criteria

PASS because the first build now has:
1. one explicit local coordinate system;
2. no Stage1 test/reference length leaked into building placement;
3. direct component sections preserved;
4. every reconstructed number separately classified;
5. endpoint-driven Shuzhu / Chashou placement;
6. no UNKNOWN silently converted to historical fact;
7. deterministic numeric input sufficient for a first 3D assembly.

## 12. Next complete step

**MP-01A Gate D｜First Assembly Engineering Build**

Proposed execution:
- instantiate Pingliang;
- instantiate + scale Tuofeng Upper variant to the Gate C assembly envelope;
- endpoint-resolve Shuzhu;
- endpoint-resolve South/North Chashou;
- attach object-level metadata for Master ID / Instance ID / evidence class / relation;
- generate one assembly Review Board;
- machine-check coordinates, lengths, symmetry, provenance and deterministic rebuild.

Gate C does not itself authorize Blender execution.
