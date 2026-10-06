# P3.3 驼峰 Source Binding V001

## 1. Identity

- component: 驼峰
- planned component_id: `CMP-FRAME-TUOFENG-001`
- planned master_id: `CMP-FRAME-TUOFENG-001_MASTER`
- source authority rule: D-099 / RC-019
- review date: 2026-10-06
- status: **IDENTITY + ASSEMBLY ROLE BOUND / GEOMETRY UNRESOLVED**

## 2. A2 official same-building direct statement

Official source:
- 山西文物数字博物馆·万佛殿专题
- https://szbwgvue.chwhyun.cn/wanfodian/

Direct structural statement:
- “四椽栿上用驼峰、令栱承平梁。”
- “平梁之上设驼峰、蜀柱、叉手。”

What this directly supports:
1. **驼峰 is a named physical timber component used in Wanfo Hall.**
2. It participates in at least two assembly roles:
   - `FOUR_CHUANFU_TO_PINGLIANG_SUPPORT`
   - `PINGLIANG_TO_RIDGE_SUPPORT`
3. It must not remain an unregistered permanent proxy if the project goal is a structured component/assembly model.

What this source does **not** supply:
- whole-hall count;
- per-instance mapping;
- dimensions;
- exact profile;
- hidden joinery;
- proof that the two assembly roles use exactly the same geometry.

## 3. A1 primary engineering authority cross-check

Source:
- `SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`
- canonical PDF: 434 pages / exact-byte identity already registered in SOURCE_REGISTER

Targeted direct review locations:

### 3.1 PDF p83 / printed p68 / Fig. 2-41
- section: §2.3.1.3 平梁、丁栿、乳栿
- figure: 图2-41｜万佛殿平梁与斗栱交接关系
- same-building photograph clearly shows the Pingliang / upper ridge-support zone and the short-post/diagonal-support assembly.
- use: visual context and relative placement cross-check.
- boundary: the figure caption does not independently label the visible hump-shaped support as “驼峰”.

### 3.2 PDF p106 / printed p91 / Fig. 2-71
- figure: 图2-71｜万佛殿上平槫与脊槫之高差示意图
- the central ridge-support assembly is shown schematically above the Pingliang, including a short vertical member seated on a visibly raised support form.
- use: confirms the same-building relative geometry around Pingliang / short-post / ridge support.
- boundary: the figure does not provide an isolated 驼峰 dimension set or a component label pointing to that raised support.

### 3.3 PDF p109 / printed p94 / Fig. 2-73
- figure: 图2-73｜万佛殿梁架举折方法示意图
- use: whole-frame context showing the relative tier positions of the central ridge-support assembly and the lower beam system.
- boundary: not a component measurement drawing for 驼峰.

### 3.4 Appendix targeted check
- PDF p344 / printed p329 / Appendix 1-7 records 蜀柱 section measurements.
- PDF p344-345 / printed p329-330 / Appendix 1-8 to 1-9 record 替木 and inter-frame bracket measurements/positions.
- **No separate 驼峰 measurement row was found in this targeted relevant appendix check.**
- This is a bounded finding for the pages inspected, not a claim that the word never appears anywhere else in all 434 pages.

## 4. Evidence classification

| Attribute | Status | Basis |
|---|---|---|
| component identity = 驼峰 | **FACT** | A2 official same-building direct statement |
| used above 四椽栿 to help support 平梁 | **FACT** | A2 direct statement |
| used above 平梁 in ridge-support group with 蜀柱 / 叉手 | **FACT** | A2 direct statement |
| same-building visual correspondence in A1 figures | **FACT** | A1 Fig. 2-41 / 2-71 / 2-73 |
| visible raised/hump support in A1 figures is the named 驼峰 | **INFERENCE** | A1 visual + A2 terminology cross-check; A1 figure itself is not explicitly labeled |
| one shared geometry for both roles | **UNKNOWN** | no direct source proof |
| exact width / thickness / height / length | **UNKNOWN** | no direct locked measurement identified |
| whole-hall count | **UNKNOWN** | no closed count identified |
| exact per-instance location map | **UNKNOWN** | role known, instance mapping not closed |
| exact profile | **UNKNOWN** | visual form exists but no metric profile control set yet |
| hidden joinery | **UNKNOWN** | no direct dimensions/topology locked |

## 5. Master-family boundary

Current working boundary:

- one component family is justified: `CMP-FRAME-TUOFENG-001`;
- **do not yet lock one geometry** for every usage;
- the source already implies at least two assembly roles:
  1. lower support role: 四椽栿 → 驼峰 / 令栱 → 平梁;
  2. upper ridge-support role: 平梁 → 驼峰 → 蜀柱 / ridge-support group.

Therefore the next Master Spec must explicitly test:

> Can both roles be represented by one evidence-bounded geometry family, or are role variants required?

Until that check is complete:
- `geometry_variant_count = UNKNOWN`;
- no canonical dimensions;
- no canonical profile;
- no mortise/tenon geometry.

## 6. Current production readiness

Result:

**SOURCE BINDING = PASS for component identity and assembly role.**

**MASTER GEOMETRY READINESS = NOT YET PASS.**

Reason:
- we have enough evidence to keep 驼峰 in Master scope;
- we do **not** yet have enough evidence to lock its production geometry.

Next complete step:
- `驼峰 Master Spec V0.1｜Geometry Evidence & Role-Variant Decision`
- scope limited to the two directly supported assembly roles above;
- no whole-hall count exercise and no hidden-joinery reconstruction.
