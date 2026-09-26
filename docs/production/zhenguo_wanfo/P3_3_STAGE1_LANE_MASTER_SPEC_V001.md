# P3.3 V002 Stage 1｜阑额 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-148**  
**日期：2026-09-26**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019**  
**复原方法：D-108 / RC-020｜Evidence-Constrained Reconstruction**  
**连接层：RC-024**  
**视觉门：D-076 PASS WITH GEOMETRY BOUNDARY**  
**任务性质：正式锁定规格；允许下一步建立 T-034 Task Contract；不等于工程执行授权**

## 1. Component Identity

- 中文名：阑额
- component id：`CMP-FRAME-LANE-001`
- master id：`CMP-FRAME-LANE-001_MASTER`
- master version：V001
- physical instances：**12**
- family：额枋 / 柱间水平连接构件
- geometry variant count：**0**

锁定一个 shared parametric Master。

四面及明间/次间的位置差异不建立独立 Master；位置实测截面差异由 instance parameters 表达。

## 2. Authoritative Inputs

### A1
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct locator:
- PDF p86–88
- printed p71–73
- §2.3.1.6｜阑额、由额
- Table 2-43
- Fig. 2-46 / 2-47 / 2-48 / 2-49
- canonical PDF SHA-256 = `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Formal evidence:
`docs/evidence/zhenguo_wanfo/P3_3_LANE_DIRECT_SOURCE_BINDING_V001.md`

### A2
山西文物数字博物馆·万佛殿专题及既有同建筑 evidence records。

Allowed use:
- 不设普拍枋；
- 柱间阑额/由额连接关系；
- 阑额至角柱不出头；
- same-building visual/form cross-check.

A2 is not dimensional authority for hidden joinery, full timber length, or the 8 unmeasured thicknesses.

### Registry
`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

V008/CURRENT locks 12 阑额 physical instances and the assembly control rule “长度按柱心距离”.

## 3. Direct Width Instance Contract

A1 gives 12/12 location-labelled widths:

| Registry location | A1 label | width mm |
|---|---|---:|
| 南立面西次间 | 南西次间 | 268 |
| 南立面明间 | 南明间 | 264 |
| 南立面东次间 | 南东次间 | 269 |
| 北立面西次间 | 北西次间 | 259 |
| 北立面明间 | 北明间 | 264 |
| 北立面东次间 | 北东次间 | 269 |
| 东山北次间 | 东北次间 | 266 |
| 东山明间 | 东明间 | 264 |
| 东山南次间 | 东南次间 | 266 |
| 西山北次间 | 西北次间 | 266 |
| 西山明间 | 西明间 | 271 |
| 西山南次间 | 西南次间 | 261 |

Report-published mean width:
- **265.6 mm**

Independent recompute:
- **265.5833… mm**
- rounded to one decimal = **265.6 mm**

Locked:
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = false`
- `WIDTH_SAMPLE_TO_INSTANCE_MAPPING = DIRECT_LOCKED / 12 OF 12`

The family mean must never overwrite the 12 direct instance widths.

## 4. Thickness Evidence / Production Contract

A1 directly measures thickness at only 4 locations:
- 南东次间 = 105 mm
- 南明间 = 105 mm
- 南西次间 = 105 mm
- 北明间 = 105 mm

The other 8 rows are explicitly `未及`.

Report-published thickness:
- **105 mm**

Locked dual-layer rule:

### Four directly measured instances
- `evidence_thickness_mm = 105`
- `production_thickness_mm = 105`
- classification = `DIRECT_MEASURED`
- replaceable = false unless new primary evidence supersedes it

### Eight unmeasured instances
- `evidence_thickness_mm = null`
- `production_thickness_mm = 105`
- classification = `PARAMETRIC_COMPLETION`
- basis = `4 directly measured specimens + report family reference`
- replaceable = true
- historical_claim = false

Therefore:
- evidence completeness = 4/12 for thickness
- production geometry completeness = 12/12
- no production blocker is created
- no evidence inflation is permitted.

## 5. Family Reference Specimen

Stage1 canonical reference body:

**1000 × 265.6 × 105 mm**

Axes:
- +X = longitudinal
- +Y = 广 / width
- +Z = 厚 / thickness

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform:
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

1000 mm:
- `NON_HISTORICAL_REFERENCE_LENGTH`
- `MASTER_SPECIMEN_ONLY`
- replaceable
- must not leak into building placement.

265.6 mm:
- report family mean width / reference specimen only.

105 mm:
- report family thickness based on four measurable rows;
- canonical specimen value only;
- must not be presented as direct measurement for all 12 instances.

## 6. Assembly Span / Full-Length Boundary

Registry rule:
- `assembly_control_span_rule = COLUMN_CENTER_DISTANCE`

This is a topology/placement control rule.

It is **not** a claim that the concealed historical timber full length equals the column-center distance.

Locked:
- `historical_full_timber_length_mm = null / UNKNOWN`
- hidden tenon extension = UNKNOWN
- exact end penetration into columns = UNKNOWN

Later assembly may resolve visible/control span from column topology. Stage1 Master keeps a non-historical 1000 mm reference body.

## 7. Geometry Mode

Geometry mode:
`PARAMETRIC_HORIZONTAL_LONG_MEMBER_WITH_INSTANCE_SECTION_PARAMETERS`

Stage1 representation:
- straight rectangular bounded envelope;
- local +X longitudinal;
- local +Y width / 广;
- local +Z thickness / 厚;
- simplified flat ends;
- no current sag/deformation/damage baked into canonical geometry.

World placement/orientation remains assembly-owned.

## 8. Corner Rule

A2 same-building evidence:
- 阑额至角柱不出头.

Locked semantic:
- `CORNER_PROJECTION = NONE`

This controls visible exterior projection only.

It does not lock:
- hidden tenon length;
- mortise depth;
- exact shoulder cut;
- exact stop plane inside the column.

## 9. Connection Layer｜RC-024

Interfaces:
1. `LEFT_END / COLUMN_CONNECTION`
2. `RIGHT_END / COLUMN_CONNECTION`

For both:
- related family = 柱
- connection existence = KNOWN
- exact geometry = DEFERRED
- future kind = evidence-backed `JOINERY_FEATURE` or `CONTACT_INTERFACE`
- Stage1 creates no unsupported mortise/tenon.

## 10. Related-component Isolation

This Master includes only 阑额.

Explicitly excluded:
- 由额
- 额间板
- 普拍枋
- 柱
- 斗栱

In particular:
- 万佛殿“不设普拍枋” must remain explicit;
- the visual combination “阑额 + 由额 + 额间板” must not be fused into one Master.

## 11. Historical-State Boundary

A1 measurements are extant-state measurements.

V001 must not claim:
- 265.6 × 105 mm = exact 963 original design section;
- eight unmeasured thicknesses = direct evidence;
- current repairs/deformation = original geometry.

Historical originality remains component-level metadata and cannot be inferred from a measured current section alone.

## 12. Review Board

Required six panels:
1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION`
4. `12_INSTANCE_WIDTH_MAPPING`
5. `THICKNESS_EVIDENCE_BOUNDARY`
6. `SOURCE_AND_RECONSTRUCTION_BOUNDARY`

Mandatory visible statements:
- 12/12 width = direct location-labelled measurement;
- 4/12 thickness = direct measurement;
- 8/12 evidence thickness = UNKNOWN;
- 8/12 production thickness = 105 mm `PARAMETRIC_COMPLETION`;
- family mean does not overwrite instance width;
- 1000 mm is non-historical reference only;
- exact joinery/full timber length are not claimed.

## 13. Hard Fails

- `INSTANCE_WIDTH_COLLAPSED_TO_FAMILY_MEAN`
- `INSTANCE_WIDTH_MAPPING_MISMATCH`
- `UNMEASURED_THICKNESS_MARKED_AS_DIRECT`
- `PARAMETRIC_COMPLETION_WITHOUT_EVIDENCE_LABEL`
- `UNKNOWN_THICKNESS_SILENTLY_HISTORICIZED`
- `DUPLICATE_MASTER_PER_LOCATION`
- `FALSE_GEOMETRY_VARIANT_FROM_LOCATION_OR_SECTION_ONLY`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `COLUMN_CENTER_SPAN_MISREPRESENTED_AS_HISTORICAL_FULL_TIMBER_LENGTH`
- `CORNER_PROJECTION_INVENTED`
- `UNSUPPORTED_JOINERY_CLAIM`
- `LANE_YOUE_IDENTITY_COLLAPSE`
- `PU_PAIFANG_FALSELY_INTRODUCED`
- `SILENT_HISTORICIZATION`
- `MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`

Missing exact historical joinery/full timber length or 8 direct thickness measurements is **not** a Stage1 hard fail because the uncertainty is explicitly isolated and production-completed.

## 14. Locked Decision｜D-148

Product Owner approved the revised Master Spec V0.1 and locks it as V001.

Locked route:
- one `CMP-FRAME-LANE-001_MASTER`;
- 12 location-locked width parameters from A1;
- 4 directly measured thicknesses;
- 8 evidence-UNKNOWN thicknesses with explicit 105 mm replaceable production completion;
- zero Geometry Variants solely from location/section difference;
- 1000 mm non-historical canonical reference length;
- column-center distance retained as assembly control span, not historical concealed timber length;
- corner projection none;
- exact end/joinery geometry deferred.

Next allowed step:
- design/establish `T-034｜P3_3_LANE_MASTER_V2_V001` Task Contract.

Not authorized by D-148:
- production execution branch;
- PR;
- GitHub Actions / Blender;
- first-article production;
- Catalog/V008 approved binding;
- Stage2;
- T-018 resume.
