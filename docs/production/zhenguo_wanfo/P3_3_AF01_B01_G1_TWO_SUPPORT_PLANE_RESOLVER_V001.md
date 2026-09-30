# AF-01 / B01-G1｜Two Support-Plane Resolver V001

- Date: **2026-09-30**
- Task: **AF01-B01-G1**
- Status: **CANDIDATE / SOURCE-CLOSED FOR TWO OUTPUTS / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: lower-six + upper-six support planes only

## 1. Existing inherited datum

AF-01 does not create a new global vertical datum.

Inherited project engineering datum:

- column-foot design plane = `Z 0`;
- column top / column-head ludou lower support plane = **Z 3534.3 mm**;
- provenance = `Z-006-RC-01 / REASONABLE_COMPLETION / replaceable`;
- this is not a confirmed historical column-height claim.

## 2. Primary report evidence

The Wanfo Hall report states:

- east and west seams each use lower + upper six-chuanfu stacked vertically;
- **lower six-chuanfu enters the column-head puzuo and is placed above the second-jump huagong**;
- **upper six-chuanfu presses on the second lower-ang at the column-center position**.

The report's Wanfo puzuo dimensional synthesis gives:

- `1 fen = 15.3 mm`;
- material thickness baseline = 10 fen;
- single-cai guang = 14 fen;
- first/second total out-jump = 48 fen;
- third/fourth lower-ang design rise = 21 fen;
- from ludou bottom to eave-purlin bottom = 106 fen;
- to eave-purlin back/top design reference = 120 fen.

Figure 2-27 expresses the vertical control ladder from the ludou bottom as:

`0 → 33 → 54 → 75 → 96 → 106 → 120 fen`

For AF-01 only, the minimum structural-layer mapping is:

- second-jump huagong upper support level = **54 fen** above ludou bottom;
- second lower-ang column-center upper support level = **96 fen** above ludou bottom.

Classification:

**REPORT_INFERRED / DRAWING_DERIVED / RECONSTRUCTED_DESIGN / AF01_LOCAL / REPLACEABLE**

This is not a direct field-survey absolute-Z claim.

## 3. Resolver outputs

Using `MOD-002 = 15.3 mm/fen`:

### LOWER_SIX_SUPPORT_PLANE_Z

`3534.3 + 54 × 15.3 = 4360.5 mm`

**Result: 4360.5 mm**

### UPPER_SIX_SUPPORT_PLANE_Z

`3534.3 + 96 × 15.3 = 5003.1 mm`

**Result: 5003.1 mm**

North and south ends of the AF-01 east-seam first article use the same reconstructed-design support-plane Z values. Current observed puzuo settlement is not propagated into this design placement.

## 4. Independent numerical cross-check

Support-plane separation:

`96 - 54 = 42 fen = 642.6 mm`

Measured lower-six-chuanfu mean guang:

`493.5 mm ≈ 32.3 fen`

Remaining vertical interval above the measured lower-six body:

`642.6 - 493.5 = 149.1 mm ≈ 9.75 fen`

This independently falls in the report's small-dou / 10-fen order of magnitude and is consistent with the report's statement that the upper/lower six-chuanfu are separated by an intermediate dou/support layer.

Cross-check status:

**PASS / CONSISTENT / NOT USED AS PRIMARY AUTHORITY**

No specific hidden connector geometry is inferred from this numerical agreement.

## 5. Evidence boundary

The two outputs mean only:

- where the lower surface/support plane of the lower-six body is placed;
- where the lower surface/support plane of the upper-six body is placed.

They do not claim:

- exact historical 963 absolute elevations;
- current deformed/as-measured elevations;
- exact mortise/tenon geometry;
- complete column-head puzuo topology closure;
- exact support-face machining;
- that every puzuo instance has zero settlement;
- that the report's ideal model equals an as-built 963 state.

## 6. Existing Master compatibility

No Master geometry is mutated.

For the AF-01 east-seam instances:

- lower-six measured mean guang remains **493.5 mm**;
- upper-six measured mean guang remains **334.0 mm**;
- historical/full member length remains unresolved under B02;
- placement uses these support planes only.

## 7. G1 Gate

- `LOWER_SIX_SUPPORT_PLANE_Z`: **RESOLVED CANDIDATE = 4360.5 mm**
- `UPPER_SIX_SUPPORT_PLANE_Z`: **RESOLVED CANDIDATE = 5003.1 mm**
- whole puzuo network closure: **NOT REQUIRED / NOT PERFORMED**
- Blender: **NOT AUTHORIZED**
- Master mutation: **NONE**
- Registry mutation: **NONE**
- T-018: **HOLD**

If Product Owner approves this candidate:

**G1 closes and B01 advances only to G2｜Upper-Six → San-Dou/Intermediate Support → Four-Chuanfu vertical increment.**
