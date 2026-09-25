# P3.3｜子角梁 Direct Source Binding V001

**状态：LOCKED / D-142 / 2026-09-25**  
**Component：子角梁**  
**资料主权：D-099 / RC-019；生产解释：RC-020 + RC-023；连接层：RC-024**

## 1. A1 Primary Engineering Authority

Source:
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF:
- SHA-256: `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`
- PDF p88–89
- printed p73–74
- §2.3.1.7｜角梁
- Fig. 2-50
- actual angle-beam table: Table 2-44

A1 directly establishes:
- four corner locations each include 子角梁 / 大角梁 / 隐角梁 as distinct identities;
- 子角梁 physical instance count = 4;
- 东北 / 西北 子角梁 measurements differ markedly from the other two and the report attributes this to historical replacement;
- location-labelled extant-state section measurements exist for all four 子角梁.

## 2. Direct extant-state sections

| Location | A1 label | width / 广 mm | thickness / 厚 mm | source qualifier |
|---|---|---:|---:|---|
| 东南角 | 东南子角梁 | 220 | 150 | direct row |
| 东北角 | 东北子角梁 | 190 | 153 | source row contains “含” qualifier; preserve raw qualifier |
| 西南角 | 西南子角梁 | 213 | 153 | direct row |
| 西北角 | 西北子角梁 | 125 | 149 | source marks replacement/new condition; preserve raw qualifier |

These are **current/extant-state direct measurements**. They are not claims of untouched 963 original dimensions.

## 3. Published mean / aggregation ambiguity

The report publishes a 子角梁 family mean:
- width = **216.5 mm**
- thickness = **152 mm**

All-four-row arithmetic mean:
- width = **187.0 mm**
- thickness = **151.25 mm**

Observation:
- 216.5 mm equals the mean of the SE 220 and SW 213 width rows;
- 152 mm is consistent with rounding the SE/SW thickness mean 151.5 mm;
- because the text separately identifies NE/NW as historical replacements, the published mean is compatible with an unreplaced-pair aggregation;
- however, the report does **not** explicitly state the aggregation rule.

Locked classification:
- `SOURCE_AGGREGATION_METHOD_AMBIGUOUS = TRUE`
- `SILENT_MEAN_REINTERPRETATION = PROHIBITED`
- the published 216.5×152 may be used only as the **family reference specimen**;
- it must never overwrite the four direct location-labelled measurements.

This is not silently converted into a generic arithmetic-error claim.

## 4. Internal locator mismatch

The text references “表2-41” for the angle-beam data, while the actual adjacent angle-beam table is labelled **Table 2-44**.

Locked:
- `SOURCE_INTERNAL_REFERENCE_MISMATCH = TRUE`
- page / section / Fig.2-50 / actual Table 2-44 remain the locator authority.

## 5. A2 official same-building visual/form evidence

山西文物数字博物馆·万佛殿专题 establishes:
- the third inward jump of the corner bracket set supports the corner-beam system;
- the old/large corner-beam tail has the documented hidden-corner-member relationship;
- 万佛殿的套兽 is a dragon-head form installed at the **子角梁端头**, facing forward, functioning as weather protection at the eave corner.

A2 supports visual/form and attachment semantics only. It is **not** authority for:
- exact 子角梁 full length;
- exact slope / 45° building coordinates;
- exact end-cut geometry;
- exact 子角梁↔大角梁 hidden joinery;
- exact sleeve-beast socket dimensions.

## 6. D-076 Visual/Form Gate

Result: **PASS WITH GEOMETRY BOUNDARY**

Adequate for Stage1:
- identity / four-corner placement;
- long-member outer-envelope interpretation;
- distinction from 大角梁 / 隐角梁;
- outboard-end 套兽 attachment semantic;
- bounded parametric section treatment.

Not visually/evidentially closed:
- historical exact full length;
- exact longitudinal profile/taper;
- exact installation angle;
- exact end cuts;
- hidden mortise/tenon;
- exact relation surface between 子角梁 and 大角梁;
- replacement-era original-vs-replacement body-form differences.

Per RC-023, these missing historical-original fields are not blockers.

## 7. Connection Layer carry-forward｜RC-024

Stage1 interface metadata:
1. `OUTBOARD_END / TAOSHOU_ATTACHMENT`
   - other identity: 套兽
   - later connection kind: `PHYSICAL_CONNECTOR` / accessory attachment
   - existence/placement semantic: A2-backed
   - exact interface geometry: unresolved / replaceable
   - structural load-path claim: none

2. `INBOARD_CORNER_ASSEMBLY`
   - related family: 大角梁 / corner-beam assembly
   - exact connection kind: unresolved at Stage1
   - allowed future resolution: `JOINERY_FEATURE` or `CONTACT_INTERFACE` according to evidence/assembly closure
   - no hidden joint is invented now.

## 8. Modeling implication

Stage1 should use:
- one shared `CMP-FRAME-ZIJIAOLIANG-001_MASTER`;
- four location-locked instance sections;
- zero Geometry Variant solely from location/replacement status;
- 1000 mm non-historical reference length;
- endpoint-driven actual length/orientation;
- rectangular bounded-envelope body and simplified flat ends;
- explicit source/reconstruction boundary.

No Blender execution fact is created by this binding alone.
