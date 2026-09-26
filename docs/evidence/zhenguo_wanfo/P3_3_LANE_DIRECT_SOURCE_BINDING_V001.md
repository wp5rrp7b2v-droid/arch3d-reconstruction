# P3.3｜阑额 Direct Source Binding V001

**状态：LOCKED / D-148 / 2026-09-26**  
**Component：阑额**  
**资料主权：D-099 / RC-019；生产解释：D-108 / RC-020；连接层：RC-024**

## 1. A1 Primary Engineering Authority

Source:
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF:
- SHA-256: `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`
- PDF p86–88
- printed p71–73
- §2.3.1.6｜阑额、由额
- Table 2-43
- Fig. 2-46 / 2-47 / 2-48 / 2-49

A1 directly establishes:
- 万佛殿柱间使用阑额；南立面明三间、北立面明间同时可见阑额与由额，其余各面各间仅显露阑额；
- Table 2-43 contains 12 location-labelled 阑额 width measurements;
- only 4 of the 12 locations have directly measurable thickness, all 105 mm; the other 8 are marked “未及”;
- the report publishes 阑额 mean width = 265.6 mm and thickness = 105 mm, converted to 17.36分 × 6.86分 and rounded to 17分 × 7分;
- the report discusses historical retention/adjustment of 阑额、由额; these extant measurements are not automatically 963 original-design dimensions.

## 2. Direct location-labelled measurements

| Registry location | A1 label | width / 广 mm | evidence thickness mm | thickness status |
|---|---|---:|---:|---|
| 南立面东次间 | 南东次间 | 269 | 105 | DIRECT_MEASURED |
| 南立面明间 | 南明间 | 264 | 105 | DIRECT_MEASURED |
| 南立面西次间 | 南西次间 | 268 | 105 | DIRECT_MEASURED |
| 北立面明间 | 北明间 | 264 | 105 | DIRECT_MEASURED |
| 北立面东次间 | 北东次间 | 269 | null | UNMEASURED / 未及 |
| 北立面西次间 | 北西次间 | 259 | null | UNMEASURED / 未及 |
| 东山南次间 | 东南次间 | 266 | null | UNMEASURED / 未及 |
| 东山明间 | 东明间 | 264 | null | UNMEASURED / 未及 |
| 东山北次间 | 东北次间 | 266 | null | UNMEASURED / 未及 |
| 西山南次间 | 西南次间 | 261 | null | UNMEASURED / 未及 |
| 西山明间 | 西明间 | 271 | null | UNMEASURED / 未及 |
| 西山北次间 | 西北次间 | 266 | null | UNMEASURED / 未及 |

Note: the Registry uses east/west gable north/center/south-bay labels. The A1 labels above map directly by orientation:
- 东南次间 → 东山南次间
- 东明间 → 东山明间
- 东北次间 → 东山北次间
- 西南次间 → 西山南次间
- 西明间 → 西山明间
- 西北次间 → 西山北次间

The stray “东山东次间?” line above is explicitly non-authoritative and is not part of the 12-instance mapping.

## 3. Published family statistics / arithmetic check

Report-published:
- width = **265.6 mm**
- thickness = **105 mm**

Independent width recompute across all 12 location-labelled width rows:
- (269+264+268+264+269+259+266+264+266+261+271+266)/12
- = **265.5833… mm**
- rounds to **265.6 mm**

Thickness:
- 4 directly measured rows = 105 / 105 / 105 / 105 mm
- 8 rows = 未及
- published 105 mm is consistent with the four measurable rows.

Locked:
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = false`
- `WIDTH_MAPPING = DIRECT_LOCKED / 12 OF 12`
- `THICKNESS_MAPPING = DIRECT_LOCKED / 4 OF 12`
- `UNMEASURED_THICKNESS = 8 OF 12`

## 4. A2 official same-building visual / structural semantics

山西文物数字博物馆·万佛殿专题 supports:
- 不设普拍枋；
- 柱间以阑额、由额连接；
- 阑额至角柱不出头；
- same-building visual/form reading of the exterior eave layer.

A2 is visual/form and structural-semantic authority only. It is not authority for:
- exact 阑额 thickness at the 8 unmeasured locations;
- exact timber full length;
- hidden tenon length or mortise depth;
- exact end-cut geometry;
- 963 original section dimensions.

## 5. D-076 Visual / Form Gate

Result: **PASS WITH GEOMETRY BOUNDARY / Product Owner accepted by approving Master Spec V0.1 on 2026-09-26.**

Adequate for Stage1:
- identity as a horizontal intercolumn timber;
- 12 location-locked instances;
- straight rectangular bounded-envelope interpretation;
- no projection beyond corner column as an exterior-form rule;
- one shared parametric Master with location-owned width parameters;
- partial direct thickness evidence with explicit production completion for unmeasured rows.

Not visually/evidentially closed:
- 963 original exact section;
- exact hidden end/tenon geometry;
- exact mortise geometry in columns;
- exact full timber length including concealed joints;
- current deformation/damage as canonical geometry.

## 6. Thickness production completion

For 4 directly measured locations:
- `evidence_thickness_mm = 105`
- `production_thickness_mm = 105`
- classification = `DIRECT_MEASURED`

For 8 unmeasured locations:
- `evidence_thickness_mm = null`
- `production_thickness_mm = 105`
- classification = `PARAMETRIC_COMPLETION`
- basis = `four directly measured specimens + report family reference`
- replaceable = true
- historical_claim = false

This dual-layer rule is mandatory. Production completion must never be rewritten as direct measurement.

## 7. Connection Layer carry-forward｜RC-024

Stage1 interface metadata:
1. `LEFT_END / COLUMN_CONNECTION`
2. `RIGHT_END / COLUMN_CONNECTION`

For both:
- related family: 柱
- connection existence: known
- exact kind/geometry: unresolved at Stage1
- later resolution restricted to evidence-backed `JOINERY_FEATURE` or `CONTACT_INTERFACE`
- hidden tenon/mortise dimensions are not invented.

Related identities kept separate:
- 由额
- 额间板
- 普拍枋
- 柱
- 斗栱

## 8. Modeling implication

Stage1 should use:
- one shared `CMP-FRAME-LANE-001_MASTER`;
- 12 location-locked instance width parameters;
- 4 direct thickness values;
- 8 explicit thickness production-completion values;
- zero Geometry Variant solely from location or section difference;
- 1000 mm non-historical canonical reference length;
- column-center topology as assembly span control, not as a claim of concealed historical timber full length;
- rectangular bounded-envelope body and simplified flat ends;
- explicit evidence/reconstruction boundary.

No Blender execution fact is created by this binding alone.
