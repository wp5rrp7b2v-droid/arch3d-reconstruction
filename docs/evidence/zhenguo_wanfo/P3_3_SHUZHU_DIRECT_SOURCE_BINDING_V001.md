# P3.3 蜀柱 Direct Source Binding V001

## 1. Identity

- component: 蜀柱
- proposed component_id: `CMP-FRAME-SHUZHU-001`
- source authority rule: D-099 / RC-019
- reconstruction rule: D-108 / RC-020

## 2. A1 primary engineering authority

Source:
- `SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`
- exact-byte canonical archive identity already locked by D-107

Direct review location:
- PDF p90-91 / printed p75-76
- §2.3.1.9
- Table 2-46 (蜀柱实测值及分析)
- Fig. 2-51 / Fig. 2-52 provide same-building visual reference for the upper Pingliang / ridge-support zone

Visible measurement rows, table order:
- 东缝: width 218 mm / thickness 158 mm
- 东山: width 220 mm / thickness 未及
- 西缝: width 220 mm / thickness 157 mm
- 西山: width 217 mm / thickness 未及

Published / recomputed mean:
- width: 218.75 mm
- thickness: 157.5 mm
- width recompute: (218 + 220 + 220 + 217) / 4 = 218.75 mm
- thickness recompute from measured interior-frame rows: (158 + 157) / 2 = 157.5 mm
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = FALSE`

Boundary:
- both gable thickness entries (东山 / 西山) are explicitly unmeasured (未及)
- sample-to-final-instance historical identity is not separately proven beyond the table/location labels
- exact historical full height, end profile and hidden joinery are not directly locked here

## 3. V008/CURRENT instance authority

Canonical Registry locks four physical instances:
1. `蜀柱-东缝` / 东缝平梁上
2. `蜀柱-西缝` / 西缝平梁上
3. `蜀柱-东山` / 东山平梁上
4. `蜀柱-西山` / 西山平梁上

Count status:
- `LOCKED_DERIVED`
- basis: 附件1-7实测位置 + 木结构测绘图闭合

Role grouping for Stage1:
- INTERIOR_FRAME = 2 (东缝 / 西缝)
- GABLE_FRAME = 2 (东山 / 西山)

Role grouping is placement metadata, not a Geometry Variant.

## 4. A2 official same-building cross-check

Official source:
- 山西文物数字博物馆·万佛殿专题
- `https://szbwgvue.chwhyun.cn/wanfodian/`

Official structural statement:
- 平梁之上设驼峰、蜀柱、叉手。

Use:
- confirms the structural layer and same-building component identity
- does not supply exact section dimensions, historical full height, endpoints or hidden joinery

## 5. D-076 visual/form gate

Result: **PASS**

Observed / source-consistent visual facts:
- 蜀柱 is a short vertical timber member in the Pingliang-above ridge-support system
- it is visually distinct from the diagonal 叉手
- a bounded rectangular timber representation is sufficient for Stage1 Master identity
- exact historical end/joint treatment is not visually/directly resolved to production certainty

Production boundary:
- canonical section uses the A1 published/recomputed mean 218.75 × 157.5 mm
- canonical reference length is non-historical and replaceable
- actual installed height is assembly-endpoint-derived
- flat/simplified ends are reconstructed-design representation, not historical claims

Hard boundary:
- no silent historical height
- no unsupported mortise/tenon claim
- no GABLE Geometry Variant solely because one thickness measurement is 未及
