# P3.3 V002 Stage 1｜由额 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-156**  
**日期：2026-09-26**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019**  
**复原方法：D-108 / RC-020｜Evidence-Constrained Reconstruction**  
**历史缺口规则：D-137 / RC-023**  
**连接层：RC-024**  
**视觉门：D-155 / D-076 PASS WITH HISTORICAL-ORIENTATION BOUNDARY**  
**任务性质：正式锁定规格；允许下一步设计 T-035 Task Contract；不等于工程执行授权**

## 1. Component Identity

- 中文名：由额
- component id：`CMP-FRAME-YOUE-001`
- master id：`CMP-FRAME-YOUE-001_MASTER`
- master version：V001
- physical instances：**4**
- family：额枋 / 柱间水平连接构件
- geometry variant count：**0**

Locked architecture:
**one shared parametric Master + four location-owned section instances + zero Geometry Variant.**

## 2. Authoritative Inputs

### A1
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Locator:
- PDF p86–88
- printed p71–73
- §2.3.1.6｜阑额、由额
- Table 2-43
- Fig. 2-46 / 2-47 / 2-49
- canonical PDF SHA-256 = `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Formal evidence:
`docs/evidence/zhenguo_wanfo/P3_3_YOUE_DIRECT_SOURCE_BINDING_V001.md`

### A2
山西文物数字博物馆·万佛殿专题。

Allowed use:
- no 普拍枋;
- 阑额 / 由额 intercolumn structural semantics;
- same-building visual/form cross-check.

A2 is not dimensional authority for hidden joinery, full timber length, or original pre-repair orientation.

### Registry
`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

V008/CURRENT locks 4 physical 由额 instances:
- 南立面西次间
- 南立面明间
- 南立面东次间
- 北立面明间

## 3. Direct Instance Section Contract

| Registry location | A1 label | width mm | thickness mm | classification |
|---|---|---:|---:|---|
| 南立面西次间 | 南西次间 | 255 | 105 | DIRECT_MEASURED |
| 南立面明间 | 南明间 | 245 | 105 | DIRECT_MEASURED |
| 南立面东次间 | 南东次间 | 250 | 105 | DIRECT_MEASURED |
| 北立面明间 | 北明间 | 259 | 105 | DIRECT_MEASURED |

Locked:
- `WIDTH_SAMPLE_TO_INSTANCE_MAPPING = DIRECT_LOCKED / 4 OF 4`
- `THICKNESS_SAMPLE_TO_INSTANCE_MAPPING = DIRECT_LOCKED / 4 OF 4`
- no section completion is required.

Direct instance values must never be collapsed to a reference mean.

## 4. Reference Statistics

A1 reports:
- south-facade 由额 width mean = 250.0 mm
- south-facade thickness = 105 mm
- north center-bay width = 259 mm
- north center-bay thickness = 105 mm

Project-derived all-four width reference:
- `(255+245+250+259)/4 = 252.25 mm`

Classification:
- `252.25 = PROJECT_DERIVED_REFERENCE`
- `NOT_SOURCE_PUBLISHED_FAMILY_MEAN`

## 5. Canonical Reference Specimen

Canonical Stage1 reference body:

**1000 × 252.25 × 105 mm**

Axes:
- +X = longitudinal
- +Y = width / 广
- +Z = thickness / 厚

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

1000 mm:
- `NON_HISTORICAL_REFERENCE_LENGTH`
- `MASTER_SPECIMEN_ONLY`
- replaceable
- must not leak into building placement.

252.25 mm:
- project-derived reference only;
- not a source-published family mean;
- must not overwrite 255 / 245 / 250 / 259 direct widths.

105 mm:
- directly measured at all four instances.

## 6. Length / Placement Contract

No direct historical full timber length is locked.

Therefore:
- `canonical_reference_length_mm = 1000`
- `actual_instance_length = ASSEMBLY_ENDPOINT_DERIVED`
- `historical_full_timber_length_mm = null / UNKNOWN`
- hidden end penetration = UNKNOWN

Later assembly may derive production span/length from explicit endpoints or column topology, but that result must not be relabelled as exact concealed historical timber full length.

## 7. Geometry Mode

`PARAMETRIC_HORIZONTAL_LONG_MEMBER_WITH_INSTANCE_SECTION_PARAMETERS`

Stage1 representation:
- straight rectangular bounded envelope;
- local +X longitudinal;
- local +Y width;
- local +Z thickness;
- simplified flat ends;
- no current sag/damage baked into canonical geometry;
- no decorative curvature/taper without direct evidence.

World placement/orientation remains assembly-owned.

## 8. Historical Repair / Orientation Contract

A1 establishes that current 由额 orientation was altered by historical repair.

Locked:
- `current_orientation_state = HISTORICAL_REPAIR_FLIPPED`
- `original_963_top_bottom_orientation = UNRESOLVED`

This is **semantic / historical-state metadata**, not a Geometry Variant.

Reason:
- Stage1 body is a rectangular bounded envelope;
- no asymmetric mortise/joinery detail is being restored;
- flipping the current rectangular body does not create a distinct canonical body form.

A future evidence-backed non-symmetric joinery restoration may require a more detailed state model, but V001 does not pre-claim it.

## 9. Historical Mortise Trace Contract

Locked:
- `mortise_trace_existence = DIRECT_EVIDENCE`
- `mortise_trace_exact_geometry = UNRESOLVED`
- `mortise_trace_current_structural_function = UNRESOLVED`
- `canonical_body_cut = false`

Stage1 must not cut Fig.2-49 traces into the canonical Master.

The traces remain:
`HISTORICAL_REPAIR_TRACE_METADATA`

## 10. Connection Layer｜RC-024

Interfaces:
1. `LEFT_END / COLUMN_CONNECTION`
2. `RIGHT_END / COLUMN_CONNECTION`

For both:
- related family = 柱
- connection existence = KNOWN
- exact connection geometry = DEFERRED
- end penetration depth = UNKNOWN
- tenon/mortise dimensions = UNKNOWN

The vertical relationship among 阑额 / 额间板 / 由额 is assembly placement semantics and is not converted into unsupported joinery in V001.

## 11. Related-component Isolation

This Master includes only 由额.

Explicitly excluded:
- 阑额
- 额间板
- 普拍枋
- 柱
- 斗栱

The visual stack must not be fused into one asset.

## 12. Historical-State Boundary

V001 must not claim:
- current section = exact 963 original section;
- current top/bottom orientation = original orientation;
- old mortise traces = current active joinery;
- assembly-derived length = exact historical full timber length.

Under RC-023, these unknowns do not block Stage1.

## 13. Review Board

Required six panels:
1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION`
4. `4_INSTANCE_SECTION_MAPPING`
5. `HISTORICAL_ORIENTATION_BOUNDARY`
6. `SOURCE_AND_RECONSTRUCTION_BOUNDARY`

Mandatory visible statements:
- 4/4 width direct;
- 4/4 thickness direct;
- 252.25 = project-derived reference only;
- current state = historically flipped;
- original top/bottom = unresolved;
- mortise traces observed;
- exact mortise geometry not modeled;
- 1000 mm = non-historical reference only.

## 14. Hard Fails

- `INSTANCE_SECTION_COLLAPSED_TO_REFERENCE_MEAN`
- `PROJECT_DERIVED_REFERENCE_MARKED_AS_SOURCE_PUBLISHED`
- `HISTORICAL_REPAIR_FLIP_IGNORED`
- `CURRENT_ORIENTATION_MARKED_AS_963_ORIGINAL`
- `OLD_MORTISE_TRACE_MODELED_AS_CANONICAL_JOINERY`
- `UNSUPPORTED_JOINERY_CLAIM`
- `DUPLICATE_MASTER_PER_LOCATION`
- `FALSE_GEOMETRY_VARIANT_FROM_SECTION_DIFFERENCE`
- `FALSE_GEOMETRY_VARIANT_FROM_HISTORICAL_ORIENTATION_METADATA`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `ASSEMBLY_LENGTH_MARKED_AS_HISTORICAL_FULL_TIMBER_LENGTH`
- `YOUE_LANE_IDENTITY_COLLAPSE`
- `YOUE_EJIANBAN_IDENTITY_COLLAPSE`
- `PU_PAIFANG_FALSELY_INTRODUCED`
- `SILENT_HISTORICIZATION`
- `MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`

## 15. Locked Decision｜D-156

Product Owner approved Master Spec V0.1 and locks it as V001.

Locked route:
- one `CMP-FRAME-YOUE-001_MASTER`;
- four direct-section instances;
- zero Geometry Variant;
- 1000 × 252.25 × 105 mm canonical reference specimen;
- 252.25 is project-derived reference only;
- instance length later assembly-derived;
- exact historical full length deferred;
- current orientation recorded as historical-repair flipped;
- original 963 top/bottom unresolved;
- old mortise traces recorded but not modeled;
- exact end/joinery geometry deferred.

Next allowed step:
- design/establish `T-035｜P3_3_YOUE_MASTER_V2_V001` Task Contract.

Not authorized by D-156:
- production branch;
- PR;
- Blender / GitHub Actions;
- first-article production;
- Catalog/V008 approved binding;
- Stage2;
- T-018 resume.
