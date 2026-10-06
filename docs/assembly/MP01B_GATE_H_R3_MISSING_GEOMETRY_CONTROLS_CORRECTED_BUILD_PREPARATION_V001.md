# MP-01B Gate H-R3｜Missing Geometry Controls + Corrected Build Preparation V001

Status: **PRODUCT OWNER APPROVED / GATE H-R4 READY / CORRECTED BLENDER BUILD NOT YET STARTED**  
Date: 2026-10-06

## 1. Objective

Resolve the two geometry controls left by approved Gate H-R2 and prepare the corrected lower-support build contract:

1. Panjian / Spacer Ludou bottom depth;
2. target Interior Huagong numeric endpoint controls.

This gate also rewrites the Gate H build-preparation geometry/relations so the corrected build is an **orthogonal bracket node**, not the invalid serial stack.

No Blender execution occurs in R3.

## 2. Locked coordinate system

Use the existing MP-01B local assembly frame:

- X = 顺身 / East-Seam line / out-of-section;
- Y = 进深 / transverse section;
- South / FRONT = +Y;
- North / REAR = -Y;
- Z = up;
- origin = center of Four-Chuanfu upper face.

Retained support stations:

- FRONT / South upper-purlin node = `Y=+1836 mm`;
- REAR / North upper-purlin node = `Y=-1836 mm`.

These remain report/drawing-topology assembly controls, not hidden-contact center claims.

## 3. Panjian Ludou bottom-depth completion

### 3.1 Problem

For the Panjian/Spacer Ludou family:
- target top depths are direct;
- target bottom depths are `未及`;
- Table 2-49 family bottom depth is also `未及`.

No direct bottom-depth measurement is available.

### 3.2 Candidate rule

Use an **equal side-inset rule** in plan:

> `top_depth - bottom_depth = top_width - bottom_width`

Rationale:
- the known width direction directly gives the target's top-to-bottom plan inset;
- applying the same absolute side inset to the depth direction is a minimal frustum-envelope interpolation;
- it does not borrow exterior column-head Ludou dimensions;
- it is deterministic and directly replaceable.

Classification:

`RECONSTRUCTED_DESIGN / EQUAL_PLAN_SIDE_INSET / REPLACEABLE / NOT_HISTORICAL_MEASUREMENT`

### 3.3 Result

FRONT:
- top width = 321
- bottom width = 221
- full width reduction = 100
- top depth = 355
- **bottom depth candidate = 255 mm**

REAR:
- top width = 320
- bottom width = 227
- full width reduction = 93
- top depth = 357
- **bottom depth candidate = 264 mm**

Family-mean cross-check only:
- top width 332.1 - bottom width 230.0 = 102.1;
- top depth 353.6 - 102.1 = 251.5 mm.

The target candidates are of the same order but are not replaced by the family cross-check value.

## 4. Interior Huagong endpoint completion

### 4.1 Direct facts

Appendix 1-9:

FRONT `东缝前上平槫下襻间`
- 进深华栱
- 广221
- 厚153
- length note: `一端栱头，一端至托脚`

REAR `东缝后上平槫下襻间`
- 进深华栱
- 广210
- 厚156
- length note: `一端栱头，一端至托脚`

Direction is direct:
- long axis = assembly Y / 进深.

Numeric full length is not directly measured.

### 4.2 Drawing 11 calibration

Drawing 11 provides a section-plane image of the target upper-purlin bracket nodes.

Calibration control:
- visible Pingliang-end / upper-purlin station spacing ≈ 530 px;
- assembly station spacing = 3672 mm;
- image scale ≈ **6.93 mm/px**.

The visible in-plane Huagong-like span is approximately:
- total ≈ 130 px ≈ 901 mm;
- inward gong-head reach ≈ 94 px ≈ 651 mm;
- outward reach to Tuojiao ≈ 36 px ≈ 249 mm.

Image edges overlap with Tuojiao / bracket lines, so this is not treated as a direct survey measurement.

### 4.3 Deterministic project control

Round the source-image calibration to:

- total realization length = **900 mm**;
- inward gong-head reach from support station = **650 mm**;
- outward reach to Tuojiao contact datum = **250 mm**.

Classification:

`SOURCE_IMAGE_CALIBRATED_PROJECT_COMPLETION / REPLACEABLE / NOT_DIRECT_MEASUREMENT / NOT_HISTORICAL_FULL_LENGTH`

Expected uncertainty:
`±50 mm`

This is intentionally less precise than the direct Appendix measurements.

### 4.4 Endpoint controls

FRONT / South:
- support station = +1836
- inward gong-head endpoint = `Y=+1186`
- outward Tuojiao-contact endpoint = `Y=+2086`
- member midpoint = `Y=+1636`
- local +X points from outer Tuojiao side toward center
- local +X → assembly -Y
- Rz = -90°

REAR / North:
- support station = -1836
- inward gong-head endpoint = `Y=-1186`
- outward Tuojiao-contact endpoint = `Y=-2086`
- member midpoint = `Y=-1636`
- local +X points from outer Tuojiao side toward center
- local +X → assembly +Y
- Rz = +90°

These endpoint controls are a project reconstruction of the direct statement `一端栱头，一端至托脚`.

They do not claim exact historical end coordinates.

## 5. Corrected Tuofeng local envelopes

The old Gate F/H plan footprint was tied to the invalid Linggong analog and is superseded for corrected-build use.

At each node the Tuofeng remains:
`CMP-FRAME-TUOFENG-001_MASTER / LOWER_SUPPORT`

### FRONT
- total vertical contribution = 172.9 mm;
- base footprint:
  - X = Four-Chuanfu width = 426.5 mm;
  - Y = target Ludou top depth = 355 mm;
- upper seat footprint:
  - X = target Ludou bottom width = 221 mm;
  - Y = completed Ludou bottom depth = 255 mm;
- two-tier vertical split = 86.45 + 86.45 mm.

### REAR
- total vertical contribution = 196.0 mm;
- base footprint:
  - X = 426.5 mm;
  - Y = 357 mm;
- upper seat footprint:
  - X = 227 mm;
  - Y = 264 mm;
- two-tier vertical split = 98.0 + 98.0 mm.

Plan footprints are:
`ASSEMBLY_FOOTPRINT_MATCH / RECONSTRUCTED_DESIGN / REPLACEABLE`.

Exact historical Tuofeng profile remains UNKNOWN.

## 6. Corrected Ludou placement

### FRONT
- center = `(0,+1836)`
- bottom Z = 172.9
- direct/completed total height = 225.1
- physical envelope top Z = **398.0**
- flat+sloped contribution = 45.0+88.1 = 133.1
- gong-seat reference Z = **306.0**

Plan:
- top = 321 × 355
- bottom = 221 × 255
- bottom depth 255 = reconstructed completion.

### REAR
- center = `(0,-1836)`
- bottom Z = 196.0
- direct total height = 219
- physical envelope top Z = **415.0**
- flat+sloped contribution = 45+65 = 110
- gong-seat reference Z = **306.0**

Plan:
- top = 320 × 357
- bottom = 227 × 264
- bottom depth 264 = reconstructed completion.

Important:

> The physical Ludou top is above the `gong-seat reference Z=306`.

This is expected. `平+欹` is the report's vertical padding contribution; it is not the Ludou's full physical height.

## 7. Corrected orthogonal gong placement

Both target gongs use the common gong-seat reference:

`Z_BASE = 306 mm`

This is a production reference plane, not a claim that all hidden cut bottoms are identical.

### FRONT Linggong
- direct target dimensions = `L1016 × 广213 × 厚149`
- long axis = assembly X / 顺身
- center = `(0,+1836)`
- rotation = 0°
- envelope Z = 306 → **519**

### REAR Linggong
- direct target dimensions = `L995 × 广217 × 厚150`
- long axis = assembly X / 顺身
- center = `(0,-1836)`
- rotation = 0°
- envelope Z = 306 → **523**

### FRONT Huagong
- realization L = 900, project completion
- 广 = 221 direct
- 厚 = 153 direct
- long axis = assembly Y / 进深
- midpoint = `(0,+1636)`
- Rz = -90°
- envelope Z = 306 → **527**

### REAR Huagong
- realization L = 900, project completion
- 广 = 210 direct
- 厚 = 156 direct
- long axis = assembly Y / 进深
- midpoint = `(0,-1636)`
- Rz = +90°
- envelope Z = 306 → **516**

Huagong and Linggong are orthogonal participants inside one bracket node.

Their envelope intersection is intentional:

`BRACKET_INTERLOCK_ZONE / HIDDEN_CUT_GEOMETRY_UNKNOWN`

It must not be reported as an unintended mesh penetration.

## 8. Pingliang bearing reconciliation

A2 directly states that Linggong participates in supporting Pingliang.

The two observed target Linggong envelope tops differ:
- FRONT = 519;
- REAR = 523.

A single rigid Pingliang needs one production underside plane.

R3 chooses:

`Pingliang underside Z = 521 mm`

= midpoint of the two position-specific envelope tops.

Result:
- FRONT local difference = +2 mm;
- REAR local difference = -2 mm.

Classification:

`RECONSTRUCTED_ASSEMBLY_RECONCILIATION / OBSERVED_POSITION_VARIATION / REPLACEABLE`

Allowed support reconciliation tolerance:

`±2 mm`

This does not invent a shim, notch or historical leveling operation.

Pingliang envelope:
- realization length = 3672 mm;
- X section width = 395.5 mm;
- Z thickness = 280.5 mm;
- Y endpoints = ±1836;
- Z = **521 → 801.5**.

## 9. Four-Chuanfu retained

No R3 change:
- realization length = 7192 mm;
- X width = 426.5;
- Z thickness = 302;
- Y endpoints = ±3596;
- Z = -302 → 0.

Historical full-length claim remains false.

## 10. Panjian Fang handling

Appendix 1-9 confirms the physical `襻间枋` at the target node.

However:
- FRONT has section 210 × 152 but no numeric full length;
- REAR section is 未及;
- exact hidden relation is unresolved.

Corrected first build therefore includes two **DEFERRED_PHYSICAL_PARTICIPANT** records:
- FRONT Panjian Fang;
- REAR Panjian Fang.

They are present in the semantic node graph but not rendered as fabricated solid geometry in the next first build.

This prevents another silent omission while avoiding unsupported geometry.

## 11. Corrected build object contract

### Rendered physical geometry = 10 objects

1. Four-Chuanfu East Seam
2. Pingliang East Seam
3. FRONT Tuofeng
4. REAR Tuofeng
5. FRONT Panjian Ludou
6. REAR Panjian Ludou
7. FRONT Interior Huagong
8. REAR Interior Huagong
9. FRONT target Linggong
10. REAR target Linggong

### Deferred physical participants = 2 records
11. FRONT Panjian Fang
12. REAR Panjian Fang

### Controls
- FRONT support station
- REAR support station
- FRONT Huagong Tuojiao-contact datum
- REAR Huagong Tuojiao-contact datum

No whole-hall count claim is created by these local Minimum-Proof instances.

## 12. Relationship graph

Use existing P3.2 relationship types only.

### SUPPORT
- Four-Chuanfu → FRONT Tuofeng
- Four-Chuanfu → REAR Tuofeng
- FRONT Tuofeng → FRONT Panjian Ludou
- REAR Tuofeng → REAR Panjian Ludou
- FRONT Linggong → Pingliang
- REAR Linggong → Pingliang

### LOCATE
- FRONT support station → FRONT Tuofeng
- REAR support station → REAR Tuofeng
- FRONT Panjian Ludou → FRONT Huagong
- REAR Panjian Ludou → REAR Huagong
- FRONT Panjian Ludou → FRONT Linggong
- REAR Panjian Ludou → REAR Linggong
- FRONT Tuojiao-contact datum → FRONT Huagong outer endpoint
- REAR Tuojiao-contact datum → REAR Huagong outer endpoint

### BELONG
- FRONT Panjian Fang → FRONT bracket node
- REAR Panjian Fang → REAR bracket node

No CONNECT relation is used to claim a known mortise/tenon or slot.

## 13. Future machine checks

The corrected engineering build must at minimum verify:

1. rendered geometry object count = 10;
2. deferred physical participant count = 2;
3. support stations remain ±1836;
4. target Linggong directions = assembly X;
5. target Linggong direct dimensions = 1016×213×149 and 995×217×150;
6. target Huagong directions = assembly Y;
7. Huagong direct sections = 221×153 and 210×156;
8. Huagong full length 900 is marked project completion, not direct;
9. Huagong endpoints exactly follow 650/250 control;
10. no outer-eaves Huagong geometry authority;
11. no Gate-F 893.3 Linggong analog leakage into target instances;
12. Panjian Ludou top/bottom plan values match R3;
13. bottom depths 255/264 are marked reconstructed;
14. no column-head Ludou geometry leakage;
15. FRONT Tuofeng height =172.9;
16. REAR Tuofeng height =196;
17. both gong-seat reference planes =306;
18. physical Ludou tops =398/415;
19. Pingliang underside =521;
20. Linggong-to-Pingliang local reconciliation = ±2;
21. Huagong/Linggong overlap classified as BRACKET_INTERLOCK_ZONE;
22. hidden cuts/joinery remain UNKNOWN;
23. joinery cut count =0;
24. Panjian Fang geometry not silently invented;
25. Four-Chuanfu/Pingliang historical full-length claims=false;
26. no whole-hall count claim;
27. independent reopen;
28. deterministic rebuild;
29. evidence classes preserved;
30. Review Board non-empty.

## 14. Dependency perturbation for future build

Controlled engineering mutation:

`Huagong realization length 900 → 950 mm`

Hold the outward Tuojiao-contact endpoint fixed.

Expected:
- inward gong-head endpoint moves 50 mm toward building center;
- Huagong midpoint moves 25 mm inward;
- Huagong section unchanged;
- Ludou, Linggong, Tuofeng, Pingliang and Four-Chuanfu unchanged;
- evidence classifications unchanged.

This tests the replaceable endpoint-completion dependency only.

## 15. Review Board design

Required panels:

1. `CORRECTED_LOWER_ASSEMBLY_FRONT_ELEVATION`
2. `CORRECTED_LOWER_ASSEMBLY_AXONOMETRIC`
3. `ORTHOGONAL_GONG_TOP_VIEW`
4. `FRONT_NODE_VERTICAL_DECOMPOSITION`
5. `REAR_NODE_VERTICAL_DECOMPOSITION`
6. `LUDOU_COMPLETION_AND_EVIDENCE`
7. `HUAGONG_IMAGE_CALIBRATION_AND_ENDPOINTS`
8. `DEFERRED_PANJIAN_FANG_AND_UNKNOWN_JOINERY`

## 16. Hard FAIL

- old Gate H serial stack reused;
- Linggong local +X mapped to assembly Y;
- target Linggong uses 893.3 analog;
- Huagong uses outer-eaves Master dimensions/profile as target authority;
- Panjian Ludou uses exterior column-head Ludou geometry;
- bottom depth marked direct measurement;
- Huagong 900 marked historical/direct;
- FRONT/REAR Tuofeng forced equal;
- Ludou total height substituted for 平+欹 contribution;
- Pingliang underside returned to 306 without new evidence;
- Huagong/Linggong interlock treated as accidental penetration and removed by arbitrary displacement;
- Panjian Fang geometry fabricated;
- hidden joinery generated;
- whole-hall count extrapolated.

## 17. Gate result

**DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

R3 resolves enough geometry controls to prepare a corrected deterministic first build.

Not authorized:
- Blender corrected build;
- corrected build execution task;
- MP-01B acceptance;
- MP-01A + MP-01B combination;
- PR #56 merge.

After Product Owner approval:

> **MP-01B Gate H-R4｜Corrected Lower Assembly Engineering Build**


## 18. Product Owner decision

Date: 2026-10-06

Decision: **APPROVED**

Approved:
- Panjian Ludou bottom-depth completion: FRONT 255 mm / REAR 264 mm;
- Huagong 900 mm source-image-calibrated project realization;
- 650 mm inward + 250 mm outward endpoint control;
- corrected orthogonal node: Linggong = assembly X / Huagong = assembly Y;
- FRONT/REAR Tuofeng candidates 172.9 / 196 mm;
- Panjian Ludou placement and gong-seat reference;
- Pingliang underside reconciliation Z=521 mm with ±2 mm tolerance;
- 10 rendered physical objects + 2 deferred Panjian Fang records;
- R4 corrected engineering build may be prepared/executed as the next gate.

Not approved:
- historical exactness upgrade;
- hidden joinery geometry;
- whole-frame/whole-hall extrapolation;
- PR #56 merge.

Current execution state:
**R4 ready; Blender corrected build not yet started in this approval turn.**
