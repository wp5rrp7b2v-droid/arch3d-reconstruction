# AF-01 / B03-R0｜驼峰 Evidence Reconciliation V001

- Date: **2026-09-30**
- Task: **AF01-B03-R0**
- Status: **INVESTIGATION COMPLETE / PRODUCT OWNER REVIEW REQUIRED**
- Scope: 万佛殿正身东缝中与 AF-01 directly relevant 的驼峰角色
- Engineering generation: **NOT AUTHORIZED**

## 1. Why this reconciliation was opened

AF01-B03-R Candidate temporarily placed Shuzhu P_lower on the Pingliang execution top surface and explicitly marked it as a simplified surrogate because a hump/support component had not been materialized.

A same-building official source explicitly identifies 驼峰 in the relevant structural layers. Therefore the omission must be reconciled before B03-R can be locked.

## 2. A2 official same-building authority｜CONFIRMED

Official source:
- 山西文物数字博物馆｜镇国寺·万佛殿
- URL: https://szbwgvue.chwhyun.cn/wanfodian/

The official structure description explicitly states:

1. **四椽栿上用驼峰、令栱承平梁。**
2. **平梁、四椽栿、六椽栿之间由隔架铺作承托。**
3. **平梁之上设驼峰、蜀柱、叉手。**

Therefore two AF-01-relevant hump roles are directly confirmed at same-building level:

- `TUOFENG_ROLE_A = FOUR_CHUANFU_TO_PINGLIANG_SUPPORT`
- `TUOFENG_ROLE_B = PINGLIANG_TO_SHUZHU_RIDGE_SUPPORT`

Status:
**DIRECT_SAME_BUILDING_OFFICIAL_STRUCTURAL_SEMANTIC**

The official page does not supply exact hump dimensions, exact end-contact XYZ, or a historical full 3D profile.

## 3. A1 measured-report review｜VISUAL CORROBORATION / NO DIMENSION TABLE

Primary source:
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

### PDF p83 / printed p68 / Fig.2-41

- section title: 平梁、丁栿、乳栿;
- Fig.2-41 caption: `万佛殿平梁与斗栱交接关系`;
- the photograph visibly records the Pingliang-above ridge-support zone and a discrete shaped support body at the Shuzhu base.

This visual form is consistent with the official same-building `平梁之上设驼峰、蜀柱、叉手` statement.

Classification:
**DIRECT_PRIMARY_VISUAL_CORROBORATION / COMPONENT_LABEL_FROM_A2 / NOT_DIMENSIONAL_AUTHORITY**

### PDF p90-91 / printed p75-76 / §2.3.1.9

The measured report section is titled:

`蜀柱、襻间与替木`

The text and tables measure/document:
- 蜀柱;
- 襻间 / 襻间枋;
- 替木;
- related dou/gong support relations.

Fig.2-51 directly shows `万佛殿蜀柱与替木`; the Shuzhu base is visibly supported by a shaped timber body consistent with the official hump description.

However this section does **not** provide:
- an independent 驼峰 measurement table;
- hump width / thickness / height statistics;
- a hump historical full-profile drawing;
- exact hump-to-Shuzhu contact XYZ.

Therefore:

`TUOFENG_DIRECT_DIMENSIONAL_EVIDENCE = NOT FOUND IN REVIEWED REPORT PAGES`

## 4. Secondary technical cross-check

Secondary structural-history descriptions of Wanfo Hall independently describe:
- beam/fu tiers using hump + bracket-set support;
- Pingliang above using hump to carry the Shuzhu/ridge-support system.

These are useful corroboration only.

They do not override A1/A2 and do not provide AF-01 exact geometry authority.

## 5. Current repository gap｜CONFIRMED

Repository search on the current AF-01 working branch returns no component or formal record for:
- `驼峰`
- `TUOFENG`
- `HUMP`
- `CAMEL_HUMP`

The current Registry / approved Master chain therefore omits a source-confirmed physical component role.

This is a **component-coverage omission**, not proof that a historical hump body can be dimensioned from current evidence.

## 6. Impact on AF01-B03-R

### Ridge apex

The candidate shared ridge-support apex derived from the report's relative 120-fen run / 82-fen rise method is not contradicted by the hump discovery.

Therefore:
- `RIDGE_SUPPORT_CONNECTION_Z = 8056.3 mm` may remain a **candidate geometric apex authority**.

### Chashou

Locked Master semantics already place Chashou P_lower in the Pingliang upper connection region and P_upper in the ridge-support connection region.

The official hump statement does not establish that Chashou must start on the hump.

Therefore:
- the north/south Chashou endpoint candidates are **not disproven**;
- exact historical contact-face geometry remains unresolved.

### Shuzhu

The official source explicitly places a hump in the Pingliang-above ridge-support group.

Therefore:
- `Shuzhu P_lower = bare Pingliang top surface` cannot be locked as final;
- the current `P_lower Z=6801.7 mm` is only a temporary surrogate;
- actual AF-01 Shuzhu lower endpoint must resolve to a `TUOFENG_B_UPPER_SUPPORT_INTERFACE`.

Consequence:

**AF01-B03-R MAY NOT BE LOCKED AS CURRENTLY WRITTEN.**

## 7. Impact on locked G3｜Four-Chuanfu → Pingliang

D-293 G3 currently uses one 21-fen effective spacer/support rise as the AF-01 local reconstructed-design completion.

The official source now establishes that the actual same-building support composition includes:

`FOUR_CHUANFU → TUOFENG + LINGGONG / INTERMEDIATE PUZUO → PINGLIANG`

Therefore:

- G3's numeric `PINGLIANG_SUPPORT_PLANE_Z=6406.2 mm` is **not directly disproven**;
- but its existing 21-fen support-layer interpretation is **insufficiently reconciled with the newly confirmed hump role**;
- it must not be treated as generation-ready authority until a narrow review determines whether 21 fen is a valid aggregate effective rise for `Tuofeng + Linggong`, or whether the G3 Z must change.

Recommended status:

**G3 = LOCKED HISTORICAL DECISION RECORD / GENERATION USE HOLD PENDING REVIEW PATCH 02**

No G3 file or D-293 decision is mutated by this R0 investigation.

## 8. Minimal remediation path

Do not reopen Stage1 or build a whole new research program.

Create only one missing component family identity:

`CMP-FRAME-TUOFENG-001`

with two assembly roles:
1. `FOUR_TO_PINGLIANG_SUPPORT`
2. `PINGLIANG_TO_SHUZHU_SUPPORT`

Initial evidence contract:
- physical role/existence: `DIRECT_SAME_BUILDING_OFFICIAL`
- visual form: `DIRECT_PRIMARY_VISUAL_CORROBORATION`
- exact dimensions: `UNKNOWN`
- exact historical profile: `UNKNOWN`
- geometry for AF-01, if needed: `RECONSTRUCTED_DESIGN / ENDPOINT_OR_GAP_DRIVEN / REPLACEABLE`

Do not invent decorative profile from general Song/Yingzao Fashi examples.

## 9. Decision recommendation

Before continuing B03-R, execute one bounded correction step:

**AF01-TF01｜Tuofeng Minimal Component + Two-Role Assembly Contract**

That step should:
- register the missing physical component family;
- define no unsupported historical dimensions;
- resolve Role A first against G3;
- resolve Role B only enough to provide the Shuzhu lower support interface.

Then:
- Review Patch G3 only if its Z changes or its aggregate-height authority needs correction;
- return to B03-R;
- B03-T remains untouched.

## 10. Gate

Investigation result:

- Tuofeng existence in Wanfo Hall: **CONFIRMED**
- Four-Chuanfu→Pingliang hump role: **CONFIRMED**
- Pingliang→Shuzhu hump role: **CONFIRMED**
- direct hump dimensions in reviewed measured report: **NOT FOUND**
- current Registry/Master coverage: **MISSING**
- B03-R lock readiness: **HOLD**
- G3 generation-use readiness: **REVIEW REQUIRED**
- Blender: **NOT AUTHORIZED**
