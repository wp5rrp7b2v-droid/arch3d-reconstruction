# MP-01B Gate H-R2｜Interior Huagong + Panjian Ludou Scope & Missing-Height Completion Rule V001

Status: **DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED / NO BLENDER**
Date: 2026-10-06

## 1. Objective

Resolve exactly the two items left by Gate H-R1:

1. provenance / family boundary for the target interior `进深华栱` and `襻间/隔架用栌斗`;
2. an explicit replaceable completion rule for the missing FRONT upper-purlin Ludou height fields.

No Blender build is performed in this gate.

## 2. Interior Huagong family boundary

Proposed family:

- component id: `CMP-FRAME-HUAGONG-INTERIOR-001`
- master id: `CMP-FRAME-HUAGONG-INTERIOR-001_MASTER`
- name: `华栱（梁架襻间进深）`
- role: `PANJIAN_DEPTHWISE_SUPPORT`
- direction: `进深 / assembly Y`
- whole-hall count: UNKNOWN
- target subset: East-Seam FRONT/REAR `上平槫下襻间`

Direct target sections:
- FRONT = 广221 × 厚153 mm;
- REAR = 广210 × 厚156 mm.

Numeric full length remains UNKNOWN.

The source states only:
`一端栱头，一端至托脚`.

Therefore future realization length must be generated from explicit assembly endpoints, not copied from the exterior Huagong Master.

### Reuse decision

Existing:
`CMP-GONG-HUAGONG-001_MASTER`

= outer-eaves first/second-jump subset.

**DIRECT GEOMETRY REUSE = NO**

Builder/profile methods may be reused as software infrastructure only if no geometry/evidence values are inherited.

## 3. Panjian / Spacer Ludou family boundary

Proposed family:

- component id: `CMP-FRAME-LUDOU-PANJIAN-001`
- master id: `CMP-FRAME-LUDOU-PANJIAN-001_MASTER`
- name: `襻间/隔架用栌斗`
- system: `主体梁架`
- whole-hall count: UNKNOWN

Evidence:
- Table 2-49 provides same-family means;
- Appendix 1-10 provides target-position values.

Existing exterior column-head Ludou:
`CMP-LUDOU-COLUMN-001_MASTER`

**DIRECT GEOMETRY REUSE = NO**

The family separation is directly supported by the report's separate measurement treatment and materially different dimensions.

## 4. FRONT missing-height completion candidates considered

Target:
`东缝前上平槫下襻间栌斗`

Directly known:
- top width 321;
- bottom width 221;
- top depth 355;
- total / flat / sloped height = 未及.

Three possible completion strategies were considered.

### Candidate A｜copy the paired REAR upper-purlin target

Use:
- total 219;
- flat 45;
- sloped 65.

Rejected as the default.

Reason:
- it is spatially close, but it would silently assert FRONT = REAR for missing height fields;
- Appendix 1-10 demonstrates real observed variation between positions;
- the REAR sloped height 65 mm is notably below the broader family mean 88.1 mm.

The REAR values remain a cross-check, not the FRONT default.

### Candidate B｜same-family direct mean

Use Table 2-49:
- total height = **225.1 mm**
- flat height = **45.0 mm**
- sloped height = **88.1 mm**

Classification:
`PARAMETRIC_COMPLETION / SAME_FAMILY_DIRECT_MEAN / REPLACEABLE / NOT_TARGET_DIRECT_MEASUREMENT`

**Recommended.**

Reason:
- all three values come from the same explicitly measured interior Ludou family;
- it does not promote one specific REAR instance into the FRONT instance;
- it has a clear deterministic replacement rule if future position-specific evidence is found;
- it preserves the target FRONT plan dimensions unchanged.

### Candidate C｜derive an ideal value from fen rules

Rejected for current production.

Reason:
- it would move from observed current-condition data into report ideal-model interpretation;
- current MP-01B assembly is not authorized to replace missing observations with a historical ideal design layer.

## 5. Locked candidate if Product Owner approves

For the FRONT target Ludou:

### Direct target fields
- top width = 321 mm
- bottom width = 221 mm
- top depth = 355 mm

Classification:
`DIRECT_PRIMARY / POSITION_SPECIFIC`

### Completed height fields
- total height = **225.1 mm**
- flat height = **45.0 mm**
- sloped height = **88.1 mm**

Classification:
`PARAMETRIC_COMPLETION / SAME_FAMILY_DIRECT_MEAN / REPLACEABLE`

Historical target-specific measurement claim:
**false**

### Still UNKNOWN
- bottom depth.

No bottom-depth geometry completion is authorized in R2.

## 6. Vertical-support implication

Report modular decomposition retained:

`40 fen = 612 mm`

Four-Chuanfu report design-analysis thickness:

`20 fen = 306 mm`

Residual above Four-Chuanfu:

`306 mm`

### FRONT candidate

Using the proposed family-mean completion:

`45.0 + 88.1 = 133.1 mm`

Therefore:

`FRONT Tuofeng vertical contribution = 306 - 133.1 = 172.9 mm`

Classification:
`SECONDARY_CALCULATED / REPORT_MODULAR_DECOMPOSITION + PARAMETRIC_COMPLETION / REPLACEABLE`

Historical exact claim:
false.

### REAR direct target

Direct:
`45 + 65 = 110 mm`

Therefore:

`REAR Tuofeng vertical contribution = 306 - 110 = 196 mm`

Classification:
`SECONDARY_CALCULATED / REPORT_MODULAR_DECOMPOSITION + DIRECT_POSITION_LUDOU / REPLACEABLE`

Historical exact claim:
false.

## 7. Why FRONT and REAR are allowed to differ

This gate does not force symmetry in observed/completed vertical geometry.

The detailed report records position-to-position differences, and Table 2-49 states that the height dimensions are affected by concentrated compression and significant reduction.

Therefore:
- visual symmetry is not an evidence requirement;
- FRONT 172.9 and REAR 196 mm may coexist as current evidence-bounded production candidates;
- they must not be called original 963 design heights.

## 8. Target Linggong retained from R1

No change:

### FRONT
`顺身令栱`
- L = 1016
- 广 = 213
- 厚 = 149
- long axis = assembly X

### REAR
`顺身令栱`
- L = 995
- 广 = 217
- 厚 = 150
- long axis = assembly X

Both:
`DIRECT_PRIMARY / POSITION_SPECIFIC`

Gate F's 893.3 × 153.6 × 215 analog is no longer target geometry authority.

## 9. Corrected node structure for the next build-preparation gate

At each target support station the physical participant set is:

- Four-Chuanfu;
- Tuofeng;
- Panjian Ludou;
- depthwise Huagong;
- along-building Linggong;
- Panjian Fang;
- Pingliang.

This is a bracket node, not a simple serial stack.

The next build-preparation gate must not model every participant as vertically additive.

In particular:
- Linggong sits/interacts through the Ludou bracket zone;
- Huagong crosses the node in the depth direction;
- Linggong crosses in the along-building direction;
- exact hidden notches / slots remain UNKNOWN.

## 10. Still unresolved before corrected deterministic build

Two geometry controls remain genuinely unresolved:

1. **Panjian Ludou bottom depth**
   - direct target = 未及;
   - same-family mean = 未及.

2. **Interior Huagong numeric full length / endpoint coordinates**
   - source gives `一端栱头，一端至托脚`;
   - no direct numeric full length is currently bound.

Therefore Gate H-R2 does not authorize Blender.

## 11. Recommended next gate

After Product Owner approval:

> **MP-01B Gate H-R3｜Missing Geometry Controls + Corrected Build Preparation**

It should resolve only:
- a replaceable bottom-depth interpolation rule for Panjian Ludou;
- explicit Huagong endpoint placement / realization length;
- corrected orthogonal Huagong/Linggong transforms;
- corrected node relation graph;
- machine checks and Review Board design.

Then stop again before Blender execution.

## 12. Gate decision

**DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

Recommended approval:
- accept the two new provenance families;
- accept Candidate B for FRONT missing heights;
- preserve REAR direct values;
- proceed to R3;
- do not run Blender yet.
