# P3.3｜大角梁 Direct Source Binding V001

Status: **LOCKED / D-124**
Date: 2026-09-24
Component: 大角梁
Source authority: D-099 / RC-019

## 1. A1 canonical source

Source:
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Canonical PDF SHA-256:
`94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Direct locator:
- PDF p88–89
- printed p73–74
- §2.3.1.7｜角梁
- Fig. 2-50｜万佛殿檐角梁与大角梁尾
- Table 2-44｜万佛殿角梁实测与分析表

## 2. Direct measured instance mapping

A1 Table 2-44 directly labels four 大角梁 positions and dimensions:

| position | width / 广 mm | thickness / 厚 mm |
|---|---:|---:|
| 东南大角梁 | 240 | 210 |
| 东北大角梁 | 216 | 187 |
| 西南大角梁 | 218 | 206 |
| 西北大角梁 | 226 | 199 |

Report-published mean:
- width = 225 mm
- thickness = 200.5 mm

Independent recompute:
- width = (240+216+218+226)/4 = 225 mm
- thickness = (210+187+206+199)/4 = 200.5 mm

`SOURCE_INTERNAL_NUMERIC_CONFLICT = false`

Report analysis metadata:
- converted_fen = 14.7 × 13.1
- rounded_fen = 15 × 13

The fen values are report analysis metadata and are not a separate 963 direct-design measurement.

## 3. Mapping consequence

Unlike components whose measured samples cannot be mapped to specific building instances, the four A1 大角梁 rows are position-labeled.

Therefore:
- `sample_to_instance_mapping = DIRECT_LOCKED`
- four instance sections must remain individually traceable
- report mean 225 × 200.5 mm may be used as a family reference specimen only
- the family mean must not overwrite the four directly measured instance sections

## 4. Related corner-beam terms

A1 §2.3.1.7 distinguishes:
- 大角梁
- 子角梁
- 隐角梁

Current Registry likewise keeps these as separate production identities.

For 隐角梁, A1 records a measurement gap: width/广 cannot be directly measured; thickness is related to 大角梁. This does not authorize copying the 大角梁 body into 隐角梁.

## 5. A2 same-building structural semantics

Existing official same-building evidence records:
- the inner third jump supports the corner beam;
- the old corner-beam rear-tail construction is described with corner-tail support/contact semantics;
- exact 45° coordinates, exact length, exact slope and exact joinery remain unresolved.

Project evidence documents:
- `docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_03.md`
- `docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_04.md`
- `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md`

## 6. D-076 visual/form gate

PASS WITH GEOMETRY BOUNDARY.

Direct visual basis:
- A1 Fig. 2-50 shows the eaves corner-beam / large-corner-beam-tail relationship.

Allowed Stage1 claim:
- medium-precision outer-envelope Master
- rectangular section driven by direct measurement
- shared parametric Master with instance-specific measured sections
- assembly-derived length and orientation later

Not locked as historical exact geometry:
- full length
- 45° exact node coordinates
- exact slope / installation angle
- end cuts / mortise / tenon / grooves
- exact relationship to 隐衬角栿 / 隐角梁
- exact 963 originality

## 7. Production boundary

This binding authorizes the evidence basis for:
`CMP-FRAME-DAJIAOLIANG-001_MASTER V001`

It does not authorize Blender execution, production branch creation, PR creation, Catalog binding, V008 approved Master binding, Stage2, or T-018 resume.
