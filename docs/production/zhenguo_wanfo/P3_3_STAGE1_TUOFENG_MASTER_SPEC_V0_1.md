# P3.3 Stage1 驼峰 Master Spec V0.1

Status: **FORMALIZED / CATALOG+V008 BOUND / MERGE NOT AUTHORIZED**

## 1. Master identity

- component: 驼峰
- component_id: `CMP-FRAME-TUOFENG-001`
- master_id: `CMP-FRAME-TUOFENG-001_MASTER`
- master_version: `V0.1 CANDIDATE`
- Master family count: **1**
- proposed role variant count: **2**
- historical whole-hall physical instance count: **UNKNOWN**

This specification does not claim that all Wanfo Hall 驼峰 instances have identical geometry.

## 2. Source basis

### A1 primary engineering authority

Source:
- `SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct review:
- PDF p83 / printed p68 / §2.3.1.3 / Fig. 2-41
- PDF p106 / printed p91 / Fig. 2-71
- PDF p107 / printed p92 / Table 2-52 and associated height analysis
- PDF p109 / printed p94 / Fig. 2-73

A1 contribution:
- same-building visual and relative-position evidence for the Pingliang / ridge-support zone;
- whole-frame tier context;
- combined vertical-level analysis around the relevant beam/purlin system.

A1 boundary:
- no isolated 驼峰 measurement table has been bound;
- no exact isolated profile or hidden joint geometry is locked;
- no direct A1 label proves every visible hump-shaped block is 驼峰.

### A2 official same-building direct statement

Official Wanfo Hall digital presentation states:
- “四椽栿上用驼峰、令栱承平梁。”
- “平梁之上设驼峰、蜀柱、叉手。”

A2 contribution:
- component identity = 驼峰;
- two distinct assembly roles are directly supported.

A2 boundary:
- no exact dimensions;
- no profile control points;
- no whole-hall count;
- no hidden joinery.

## 3. Evidence classification

| Attribute | Classification | Production consequence |
|---|---|---|
| component identity | FACT / A2 DIRECT | Master family may exist |
| lower assembly role | FACT / A2 DIRECT | role variant required |
| upper ridge-support role | FACT / A2 DIRECT | role variant required |
| same-building visual correspondence | FACT / A1 FIGURES | profile may be source-guided |
| exact metric dimensions | UNKNOWN | no historical numeric lock |
| exact profile | UNKNOWN | simplified/reconstructable only |
| one identical geometry for both roles | UNKNOWN | must not force one geometry |
| whole-hall count | UNKNOWN | no count claim |
| per-instance mapping | UNKNOWN | no whole-hall instance generation |
| hidden joinery | UNKNOWN | not modeled as history |

## 4. Role-Variant Decision

### Decision

Use **one Master family with two role variants**.

#### Variant A — LOWER_SUPPORT

- variant_id: `LOWER_SUPPORT`
- semantic chain: `FOUR_CHUANFU -> TUOFENG / LINGGONG -> PINGLIANG`
- lower parent/support: 四椽栿
- upper supported assembly: 令栱 + 平梁
- direct basis: A2 statement “四椽栿上用驼峰、令栱承平梁”

#### Variant B — UPPER_RIDGE_SUPPORT

- variant_id: `UPPER_RIDGE_SUPPORT`
- semantic chain: `PINGLIANG -> TUOFENG -> SHUZHU / RIDGE_SUPPORT_GROUP`
- lower parent/support: 平梁
- upper supported member: 蜀柱 / ridge-support group
- direct basis: A2 statement “平梁之上设驼峰、蜀柱、叉手”

### Why two variants instead of one geometry

The two source-supported roles have different interface topology:
- LOWER_SUPPORT participates with 令栱 between 四椽栿 and 平梁;
- UPPER_RIDGE_SUPPORT sits above 平梁 in the central ridge-support group.

The sources do not prove that these two roles use identical dimensions or identical profile geometry.

Therefore:
- **one component identity / one Master family** is justified;
- **two role variants** are required to avoid silently asserting geometric identity.

This is a conservative data-model decision, not a claim that the historical pieces were necessarily different types.

## 5. Canonical geometry policy

### 5.1 Geometry class

For both variants:

`SOURCE_GUIDED_SIMPLIFIED / PARAMETRIC_ENVELOPE / REPLACEABLE / NOT_DIRECT_MEASUREMENT`

### 5.2 Shape semantics that may be retained

Based on same-building A1 visual material:
- timber support body with a broad base on the supporting beam;
- raised central upper support/seat region;
- side silhouette may be represented as a simplified hump / raised support profile;
- local body remains a single timber support object for modeling purposes.

These are visual-form constraints only.

### 5.3 What V0.1 does NOT lock

No canonical historical value is assigned yet for:
- length/span;
- width/depth;
- height;
- curve radii;
- exact side-profile control points;
- local cuts;
- mortise;
- tenon;
- groove;
- hidden cavities.

### 5.4 Production envelope rule

When a first article is generated, any numeric envelope required to make the geometry buildable must be:

1. derived from the local assembly envelope / neighboring locked components where possible;
2. explicitly classified as `RECONSTRUCTED_DESIGN` or `SECONDARY_CALCULATED`;
3. stored separately from historical/direct-measurement fields;
4. replaceable without changing component identity or relationship semantics.

No numeric completion may be promoted to historical fact merely because the model builds successfully.

## 6. Local axes and placement semantics

Shared axis policy:
- local Z = vertical/up direction;
- base support plane = Z0;
- top support/seat region = +Z;
- plan center aligns to the supported-member / support-chain centerline unless evidence later proves an offset;
- exact historical eccentricity = UNKNOWN.

Variant A:
- base plane attaches to 四椽栿 upper support region;
- top interface belongs to the 令栱 / 平梁 support chain;
- precise split of load/contact between 驼峰 and 令栱 = UNKNOWN.

Variant B:
- base plane attaches to 平梁 upper support region;
- top interface locates the 蜀柱 lower support region;
- exact hidden connection between 驼峰 / 平梁 / 蜀柱 = UNKNOWN.

## 7. Joinery policy

Stage1:
- `HISTORICAL_JOINERY = UNKNOWN / DEFERRED`
- no invented mortise/tenon;
- no groove or slot unless later directly supported;
- visible contact may be represented as planar/contact-envelope logic only.

Assembly relationship records may exist even when joint geometry is UNKNOWN.

## 8. Unknown-handling policy

UNKNOWN is a formal field state, not a blocker by default.

The Master may proceed when:
- identity is known;
- assembly role is known;
- placement relation can be resolved;
- missing geometry is explicitly bounded and replaceable.

The Master must stop only if:
- component identity becomes ambiguous;
- role assignment cannot be distinguished;
- a proposed geometry requires an unsupported historical claim.

## 9. Stage1 acceptance gate for this Spec

V0.1 may be approved if Product Owner accepts all of the following:

1. one Master family: `CMP-FRAME-TUOFENG-001_MASTER`;
2. two role variants: `LOWER_SUPPORT` and `UPPER_RIDGE_SUPPORT`;
3. no exact historical dimension claim;
4. no forced shared geometry between variants;
5. source-guided simplified body is allowed;
6. production dimensions, if needed, must be explicitly reconstructed/replaceable;
7. hidden joinery stays UNKNOWN;
8. whole-hall count and per-instance mapping stay UNKNOWN.

## 10. Approved next step

Product Owner approved proceeding on 2026-10-06 by instruction to start the next step.

> **驼峰 Candidate Geometry V0.1｜two role variants / source-guided simplified**

The next step will create the minimum buildable geometry for the two role variants and show the geometry/evidence boundary before any formal Master lock.


## 11. Formalization result

- First Article: PRODUCT OWNER APPROVED
- Master Library binding: COMPLETE
- V008/CURRENT binding: COMPLETE
- Exact historical dimensions: UNKNOWN
- Hidden joinery: UNKNOWN / DEFERRED
- Merge: NOT AUTHORIZED
