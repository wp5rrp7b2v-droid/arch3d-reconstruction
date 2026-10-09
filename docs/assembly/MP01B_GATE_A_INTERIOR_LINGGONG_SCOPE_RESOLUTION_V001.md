# MP-01B Gate A｜Interior Linggong Scope Resolution V001

Status: **PASS / EXISTING OUTER-EAVES MASTER REUSE REJECTED / NEW INTERIOR ROLE MASTER REQUIRED**
Date: 2026-10-06

## 1. Question

Can the current approved Master:

`CMP-GONG-LINGGONG-001_MASTER`

be used directly for the Linggong in:

`四椽栿 → 驼峰 / 令栱 → 平梁` ?

## 2. Decision

**No. Direct reuse is rejected.**

The existing Master is evidence-bounded to:
- system: **外檐斗栱**
- 28 physical Registry bindings
- distribution: 南7 / 北7 / 东7 / 西7
- canonical reference envelope: 897 × 217.4 × 155.6 mm
- sample-to-instance mapping: UNKNOWN

Its locked Master Spec explicitly states that the family reference was derived from the 28 measured outer-eaves Linggong samples and that direction/location are assembly-owned.

That scope does **not** establish that an interior core-frame Linggong between 四椽栿 and 平梁 has:
- the same length;
- the same section;
- the same profile;
- the same interface topology;
- the same historical construction detail.

Therefore:

> `OUTER_EAVES_LINGGONG_MASTER == INTERIOR_FRAME_LINGGONG`

remains **NOT ESTABLISHED**.

## 3. Evidence for the interior Linggong identity

Same-building official structural description directly states:

> “四椽栿上用驼峰、令栱承平梁。”

This is sufficient to classify:

- component identity “令栱” in the lower core-frame support chain = **FACT / A2 DIRECT**
- role “helps support Pingliang above Four-Chuanfu” = **FACT / A2 DIRECT**

It is not sufficient to classify:
- dimensions = historical FACT;
- profile = historical FACT;
- exact joint = historical FACT.

The Wanfo Hall targeted source review also confirms that the report's rear appendix contains position-specific Linggong measurements in the outer-eaves/dougong dataset, but the currently registered 28-instance Master remains explicitly bound to that outer-eaves family. Existing source review does not establish a one-to-one metric equivalence with the interior beam-frame role.

## 4. Master-family decision

Create a **separate interior-role Master family** rather than widening the existing locked outer-eaves Master.

Proposed identity:

- component_name_zh: `令栱（梁架承托）`
- component_id: `CMP-FRAME-LINGGONG-INTERIOR-001`
- master_id: `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`
- system: `主体梁架 / 梁架承托`
- role: `FOUR_CHUANFU_TO_PINGLIANG_SUPPORT`

Reason:
1. same historical term, but different evidence-bounded system role;
2. current outer-eaves Master scope is already locked and approved;
3. no evidence proves metric/profile identity across the two contexts;
4. separate family prevents silent inheritance of 897 × 217.4 × 155.6 mm into MP-01B;
5. if future direct evidence proves equivalence, the two families may later be reconciled without corrupting provenance.

This is a **data-model separation**, not a claim that medieval craftsmen necessarily treated them as different named component types.

## 5. Initial evidence classification for proposed interior Master

| Attribute | State |
|---|---|
| component term = 令栱 | FACT / A2 DIRECT |
| role in 四椽栿→平梁 support | FACT / A2 DIRECT |
| lower support context | FACT at structural-role level |
| exact count | UNKNOWN |
| exact East-Seam instance mapping | UNKNOWN |
| exact length | UNKNOWN |
| exact width/depth | UNKNOWN |
| exact profile | UNKNOWN |
| exact joinery | UNKNOWN |
| equality to outer-eaves Linggong | UNKNOWN / NOT ESTABLISHED |

## 6. Geometry policy

The new interior Master must **not** copy the outer-eaves Master dimensions or 14-point profile merely because both are called 令栱.

Allowed first-stage geometry class:

`SOURCE_GUIDED_SIMPLIFIED / ASSEMBLY_ENVELOPE_OWNED / REPLACEABLE`

Allowed to inherit only:
- semantic concept of a horizontal gong-type support member;
- generic project axis conventions if useful.

Not allowed to inherit as historical evidence:
- 897 mm length;
- 217.4 mm width;
- 155.6 mm thickness;
- outer-eaves 14-point profile;
- any outer-eaves instance mapping.

## 7. V008 / Master-scope consequence

The interior Linggong is **not currently a registered V008 physical instance**.

For MP-01B, before Blender assembly:
- register a family-level record for the interior-role Linggong;
- add it to Master scope as `MASTER_REQUIRED_PENDING`;
- build a minimum usable evidence-bounded Master;
- keep whole-hall count and exact per-instance mapping UNKNOWN.

This is analogous to the recently completed Tuofeng correction: a missing participating component family should be made explicit rather than represented by an unrelated existing Master.

## 8. Gate A result

**PASS**

The blocker is now classified rather than ambiguous:

- existing outer-eaves Linggong Master: **DO NOT REUSE**
- interior Linggong identity/role: **SUFFICIENT TO ENTER MASTER SCOPE**
- interior metric geometry: **UNKNOWN**
- next action: **create/register interior Linggong Master scope record**

## 9. Next complete step

> **MP-01B Gate B｜Register Interior Linggong + Master Spec V0.1**

Scope:
1. add `CMP-FRAME-LINGGONG-INTERIOR-001` to Master scope;
2. update V008/CURRENT with one family-level UNKNOWN-count record;
3. define source binding and Master Spec;
4. decide a minimum replaceable geometry strategy;
5. do not yet run Blender assembly.
