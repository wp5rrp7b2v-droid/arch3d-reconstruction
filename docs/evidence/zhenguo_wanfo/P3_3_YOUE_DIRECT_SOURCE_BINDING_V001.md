# P3.3｜由额 Direct Source Binding V001

**状态：LOCKED / D-156 / 2026-09-26**  
**Component：由额**  
**资料主权：D-099 / RC-019**  
**视觉门：D-155 / D-076 PASS WITH HISTORICAL-ORIENTATION BOUNDARY**

## 1. A1 Primary Engineering Authority

Source:
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF:
- SHA-256: `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`
- PDF p86–88
- printed p71–73
- §2.3.1.6｜阑额、由额
- Table 2-43
- Fig. 2-46 / 2-47 / 2-49

A1 directly establishes:
- 万佛殿南立面明三间、北立面明间显露阑额与由额；其余各面各间仅显阑额；
- 由额 physical instances = 4;
- all 4 have directly measured width and thickness;
- historical repair retained/adjusted original members and flipped 由额 vertically to hide pre-existing mortise traces from normal view;
- the exposed upper surface retains traces associated with earlier joinery;
- current observed orientation is therefore a historical-repair state and must not be silently equated to original 963 top/bottom orientation.

## 2. Direct instance measurements

| Registry location | A1 label | width / 广 mm | thickness / 厚 mm | evidence status |
|---|---|---:|---:|---|
| 南立面西次间 | 南西次间 | 255 | 105 | DIRECT_MEASURED |
| 南立面明间 | 南明间 | 245 | 105 | DIRECT_MEASURED |
| 南立面东次间 | 南东次间 | 250 | 105 | DIRECT_MEASURED |
| 北立面明间 | 北明间 | 259 | 105 | DIRECT_MEASURED |

Locked:
- `WIDTH_MAPPING = DIRECT_LOCKED / 4 OF 4`
- `THICKNESS_MAPPING = DIRECT_LOCKED / 4 OF 4`
- `SECTION_PRODUCTION_COMPLETENESS = 4 OF 4`

## 3. Report statistics and derived project reference

A1 reports:
- south-facade 由额 width mean = **250.0 mm**, thickness = **105 mm**
- north center-bay 由额 width = **259 mm**, thickness = **105 mm**

Project arithmetic across all four direct width rows:
- (255 + 245 + 250 + 259) / 4 = **252.25 mm**

Locked classification:
- `252.25 mm = PROJECT_DERIVED_REFERENCE`
- `NOT_SOURCE_PUBLISHED_FAMILY_MEAN`

It may be used only for the canonical reference specimen and must not overwrite any direct instance width.

## 4. A2 same-building cross-check

山西文物数字博物馆·万佛殿专题 supports:
- no 普拍枋;
- intercolumn connection uses 阑额 and 由额;
- same-building column grid / eave visual context.

A2 does not provide:
- per-instance 由额 section dimensions;
- exact historical full timber length;
- exact historical end profile;
- hidden tenon / mortise dimensions;
- pre-repair original top/bottom orientation.

No direct A1/A2 conflict is identified. Numeric and location authority remains A1.

## 5. D-076 Visual/Form Gate｜D-155

Result:
**PASS WITH HISTORICAL-ORIENTATION BOUNDARY**

Visual/form conclusions:
- straight horizontal timber;
- rectangular bounded-envelope body is supported for Stage1;
- where present, 由额 is visually and structurally distinct from 阑额 and 额间板;
- no direct evidence supports decorative longitudinal curvature, taper, or a canonical exposed complex end profile;
- Fig. 2-49 historical traces are evidence of past intervention/joinery history, not permission to model exact canonical joinery.

## 6. Historical orientation boundary

Locked:
- `current_orientation_state = HISTORICAL_REPAIR_FLIPPED`
- `original_963_top_bottom_orientation = UNRESOLVED`
- `mortise_trace_existence = DIRECT_EVIDENCE`
- `mortise_trace_exact_geometry = UNRESOLVED`
- `mortise_trace_current_structural_function = UNRESOLVED`

The traces belong to historical-repair metadata unless later direct evidence supports exact geometric restoration.

## 7. Production implication

Stage1 may proceed with:
- one shared parametric Master;
- 4 direct-section instances;
- zero Geometry Variants solely from location/section/orientation history;
- a straight rectangular bounded envelope;
- simplified flat ends;
- non-historical canonical reference length;
- explicit unresolved connection geometry.

No T-task, branch, PR, or Blender execution is created by this binding alone.
