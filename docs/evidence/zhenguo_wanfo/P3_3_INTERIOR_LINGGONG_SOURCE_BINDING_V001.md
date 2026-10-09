# P3.3 梁架承托令栱 Source Binding V001

Status: **IDENTITY + ASSEMBLY ROLE BOUND / METRIC GEOMETRY UNRESOLVED**
Date: 2026-10-06

## 1. Identity

- component_name_zh: 令栱（梁架承托）
- component_id: `CMP-FRAME-LINGGONG-INTERIOR-001`
- planned_master_id: `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`
- system: 主体梁架 / 梁架承托
- role: `FOUR_CHUANFU_TO_PINGLIANG_SUPPORT`

## 2. Direct same-building structural evidence

Canonical project evidence already records the official Wanfo Hall structural statement:

> “四椽栿上用驼峰、令栱承平梁。”

This directly supports:
1. a physical component identified as 令栱 participates in this interior beam-frame support chain;
2. its role is to help support 平梁 above 四椽栿 together with 驼峰.

It does not directly support:
- exact length;
- exact section;
- exact profile;
- whole-hall count;
- per-instance mapping;
- hidden joinery.

## 3. Boundary against the existing outer-eaves Linggong Master

Existing:
`CMP-GONG-LINGGONG-001_MASTER`

Bound source scope:
- 28 physical Registry records;
- system = 外檐斗栱;
- measured family reference envelope = 897 × 217.4 × 155.6 mm;
- 14-point profile = source-guided simplified outer-eaves family profile;
- sample-to-instance mapping = UNKNOWN.

No current bound evidence proves that the interior beam-frame Linggong has the same:
- 897 mm length;
- 217.4 mm width;
- 155.6 mm thickness;
- 14-point profile;
- interface topology.

Therefore no numeric/profile field from the outer-eaves Master may be copied as historical evidence.

## 4. Evidence classification

| Attribute | State |
|---|---|
| term / identity = 令栱 | **FACT / SAME-BUILDING DIRECT STATEMENT** |
| role in 四椽栿→平梁 support | **FACT / SAME-BUILDING DIRECT STATEMENT** |
| existence of outer-eaves 令栱 measured family | **FACT / A1 + V008** |
| equality of interior and outer-eaves geometry | **UNKNOWN / NOT ESTABLISHED** |
| exact interior count | **UNKNOWN** |
| exact East-Seam instance mapping | **UNKNOWN** |
| exact length | **UNKNOWN** |
| exact section | **UNKNOWN** |
| exact profile | **UNKNOWN** |
| hidden joinery | **UNKNOWN** |

## 5. Source-readiness result

**PASS for Master-scope admission.**

This source binding is sufficient to:
- create a separate interior-role family record;
- define a minimum replaceable Master strategy;
- proceed to Candidate Geometry later.

It is not sufficient to:
- assign historical millimetre dimensions;
- reuse the outer-eaves geometry;
- claim historical joint details.
