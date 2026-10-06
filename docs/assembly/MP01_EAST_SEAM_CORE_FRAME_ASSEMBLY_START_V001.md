# MP-01｜东缝核心梁架 Minimum Proof｜Assembly Start V001

Status: **MP-01A APPROVED / MP-01B GATE H MACHINE PASS BUT EVIDENCE FAIL / REVISION REQUIRED / MERGE NOT AUTHORIZED**
Date: 2026-10-06
Base: main @ `57bacb9ecdf8fa20371b5cb7f2f32bf04dd79763`

## 1. Goal

Test whether the current Wanfo Hall component system can produce one evidence-bounded, queryable and regenerable architectural assembly without inventing hidden joinery.

Project working label in chat: “明间东缝”.

Canonical V008 location label used here: **东缝**.

No claim is made yet that the registry label itself encodes “明间”.

## 2. Full intended Minimum Proof scope

Target chain:

`四椽栿 → 驼峰 / 令栱 → 平梁 → 驼峰 → 蜀柱 / 叉手`

This is split into two subassemblies so that unresolved identity/interface questions do not contaminate the whole test.

### MP-01A｜Upper Ridge Support

Proposed physical/assembly participants:

1. `平梁-东缝`
   - Master: `CMP-FRAME-PINGLIANG-001_MASTER`
   - variant: `EW_SEAM`

2. `ASM-MP01A-TUOFENG-UPPER-01`
   - Master: `CMP-FRAME-TUOFENG-001_MASTER`
   - variant: `UPPER_RIDGE_SUPPORT`
   - classification: `RECONSTRUCTED_ASSEMBLY_INSTANCE / NO_WHOLE_HALL_COUNT_CLAIM`
   - this does not create a new V008 physical-count claim

3. `蜀柱-东缝`
   - Master: `CMP-FRAME-SHUZHU-001_MASTER`

4. `叉手-东缝-南侧`
   - Master: `CMP-FRAME-CHASHOU-001_MASTER`

5. `叉手-东缝-北侧`
   - Master: `CMP-FRAME-CHASHOU-001_MASTER`

6. `RIDGE_SUPPORT_TARGET_DATUM`
   - non-physical assembly datum
   - purpose: resolve Shuzhu / Chashou upper endpoints
   - physical owner / exact ridge-purlin binding: **UNRESOLVED**

### MP-01B｜Lower Pingliang Support

Intended participants:

- `四椽栿-东缝`
- `CMP-FRAME-TUOFENG-001_MASTER / LOWER_SUPPORT`
- 令栱
- `平梁-东缝`

Current status: **DESIGN BLOCKED ONLY AT LINGGONG ROLE BINDING**.

## 3. Gate A findings

### Finding A1｜Upper-ridge component identities are usable

The following V008 instances are already explicit:
- `平梁-东缝`
- `蜀柱-东缝`
- `叉手-东缝-南侧`
- `叉手-东缝-北侧`

The Tuofeng Master is formalized and may supply an assembly-owned, replaceable `UPPER_RIDGE_SUPPORT` body.

### Finding A2｜Existing Stage2-C relation records are useful but not sufficient for final placement

Existing locked family semantics already state:
- Shuzhu rises from the Pingliang ridge-support system.
- Chashou lower endpoints belong to the Pingliang upper ridge-support system.

But those records explicitly defer:
- exact plan anchor;
- world coordinates;
- exact contact geometry;
- historical joinery.

Therefore they are relationship authority, not final placement coordinates.

### Finding A3｜Tuofeng insertion must not rewrite evidence

The Tuofeng `UPPER_RIDGE_SUPPORT` variant is a **reconstructed, replaceable assembly representation**.

For MP-01A:
- Pingliang → Tuofeng → Shuzhu may be used as a production support chain;
- this must not be relabeled as directly measured historical contact topology;
- if later evidence contradicts the intermediary placement, the Tuofeng envelope/placement is replaceable without changing Pingliang/Shuzhu identities.

### Finding A4｜A ridge target datum is required before actual Blender placement

Shuzhu and both Chashou Masters are endpoint-driven.

Their upper endpoints require a common ridge-support target region.

Current Stage2-C semantics do not lock its final building XYZ.

Therefore the next design step must bind `RIDGE_SUPPORT_TARGET_DATUM` to the relevant ridge-support geometry/evidence before MP-01A can be executed.

### Finding A5｜The current Linggong Master cannot be silently reused for MP-01B

Current `CMP-GONG-LINGGONG-001_MASTER` was scoped and measured from **28 outer-eaves dougong Linggong instances**:
- south 7
- north 7
- east 7
- west 7

Its locked Master Spec explicitly describes outer-eaves dougong context.

The lower core-frame statement uses “令栱” in the Four-Chuanfu → Pingliang support system.

No current V008 record explicitly maps an interior-frame Linggong instance to the existing 28-instance outer-eaves family.

Therefore:

> `OUTER_EAVES_LINGGONG_MASTER == INTERIOR_FRAME_LINGGONG` is **NOT ESTABLISHED**.

MP-01B must not use the existing Linggong Master until this identity/family-scope question is resolved.

This is a local blocker only; it does not block MP-01A.

## 4. Relationship classification for MP-01A

| From | To | Relationship used in model | Evidence state |
|---|---|---|---|
| 平梁-东缝 | upper support zone | LOCATE / SUPPORT REGION | FACT at structural-layer level |
| 平梁 support zone | Tuofeng Upper Variant | LOCATE / SUPPORT | RECONSTRUCTED_DESIGN / replaceable |
| Tuofeng Upper Variant | 蜀柱-东缝 | SUPPORT / SEAT | INFERENCE + RECONSTRUCTED_DESIGN / replaceable |
| 平梁 upper system | 叉手南/北 lower endpoints | LOCATE / CONTACT REGION | FACT structural layer; exact anchor UNKNOWN |
| ridge target datum | 蜀柱 upper endpoint | LOCATE | assembly datum; physical binding pending |
| ridge target datum | 叉手南/北 upper endpoints | LOCATE | assembly datum; physical binding pending |

No relation in MP-01A claims:
- exact historical mortise/tenon;
- exact contact face;
- exact historical angle;
- exact original full length.

## 5. PASS / FAIL for first actual assembly build

MP-01A will PASS only if:

1. all four registered physical members retain their V008 identities;
2. Tuofeng remains an explicitly reconstructed assembly instance;
3. Shuzhu and Chashou lengths/orientations are endpoint-derived, never copied from Stage1 reference fixtures;
4. ridge target datum is explicitly evidence-bound or explicitly reconstructed with provenance;
5. no hidden joinery is invented;
6. the same input record deterministically rebuilds the same geometry;
7. every object exposes Master ID + instance ID + relation records + evidence classification.

Hard FAIL:
- using Stage1 reference lengths as building lengths;
- silently choosing a Chashou angle;
- silently inventing a ridge target XYZ;
- calling Tuofeng reconstructed dimensions historical;
- using the outer-eaves Linggong Master for MP-01B without a scope decision;
- treating surface contact as proof of historical joinery.

## 6. Gate B result

**PASS** — upper endpoint owner resolved as `DATUM-MP01A-RIDGE-SUPPORT-EAST-SEAM`, semantically owned by `RIDGE_PURLIN role × EAST_SEAM frame plane`.

Exact global XYZ/contact face remain unresolved.

## 7. Gate C result

**PASS** — minimum deterministic local numeric inputs are locked with explicit evidence classes. No historical UNKNOWN has been silently filled.

## 8. Next complete step

**MP-01A Gate D｜First Assembly Engineering Build**

Only this question is next:

> For the 东缝 upper-ridge subassembly, what geometry/evidence should own the Shuzhu and Chashou upper endpoint target?

Candidate owner to test:
- the relevant 正身脊槫 support region / ridge-support assembly geometry.

Do not start Blender assembly before Gate B is resolved.


## 9. Gate D result

**MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**

- Run: `37420838311`
- Artifact: `11393212103`
- Validation: **31/31 PASS**
- First actual 3D assembly generated: 平梁 + 上部驼峰 + 蜀柱 + 南/北叉手
- Independent reopen: PASS
- Deterministic rebuild: PASS
- Controlled dependency perturbation: PASS
- Historical joinery: remains UNKNOWN / NOT MODELED
- MP-01B: not included; Linggong scope blocker remains

Next decision:
> Product Owner reviews Gate D Review Board and decides acceptance / rework.


## 10. Product Owner decision

- MP-01A Gate D: **APPROVED**
- MP-01A Minimum Proof: **PASS**
- Scope proven: upper ridge-support subset only
- PR #56 merge: **NOT AUTHORIZED**
- Next unresolved work: **MP-01B｜四椽栿 → 驼峰 / 令栱 → 平梁**


## 11. MP-01B Gate A

**PASS**

Decision:
- existing outer-eaves `CMP-GONG-LINGGONG-001_MASTER`: **DO NOT REUSE**
- proposed interior-role Master: `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`
- identity/role: FACT
- metric geometry/profile/joinery: UNKNOWN
- next: MP-01B Gate B｜register + Master Spec V0.1


## 12. MP-01B Gate B

**COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

- V008/CURRENT：added `令栱（梁架承托）-族边界UNKNOWN`
- Proposed Master：`CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`
- Source Binding：PASS for identity + role
- Master Spec V0.1：CANDIDATE
- Master-scope coverage：29/30 = 96.7%
- Approved Master families：26
- Blender assembly：NOT AUTHORIZED

Next:
> Product Owner review of Interior Linggong Master Spec V0.1.


## 13. MP-01B Gate C

- Interior Linggong Master Spec V0.1: **PRODUCT OWNER APPROVED**
- Candidate Geometry V0.1: **GENERATED / PRODUCT OWNER REVIEW REQUIRED**
- Geometry: neutral normalized two-zone support envelope
- Outer-eaves dimensions/profile: not inherited
- MP-01B Blender assembly: NOT AUTHORIZED


## 14. MP-01B Gate D

- Candidate Geometry V0.1: **PRODUCT OWNER APPROVED**
- First Article Build Preparation V001: **DESIGN COMPLETE**
- Engineering test fixtures: defined, non-historical
- Outer-eaves dimensions/profile leakage: machine-fail condition
- Engineering / Blender execution: **NOT AUTHORIZED**
- Next: MP-01B Gate E｜Interior Linggong First Article Engineering Execution


## 15. MP-01B Gate E

**MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**

- T-043 Run: `37424767731` — SUCCESS
- Artifact: `11394896083`
- Validation: **28/28 PASS**
- Independent reopen / mutation / deterministic restore: PASS
- Outer-eaves geometry inheritance: NONE
- Historical dimensions/profile/joinery: remain UNKNOWN
- Next: Product Owner First Article review


## 16. T-043 Formalization

- Product Owner: **APPROVED**
- `CMP-FRAME-LINGGONG-INTERIOR-001_MASTER`: **FORMALIZED**
- V008/CURRENT: **APPROVED_MASTER_AVAILABLE**
- Master-scope coverage: **30/30 = 100%**
- Approved Master families: **27**
- Historical dimensions/profile/joinery and whole-hall mapping remain UNKNOWN.
- Next: MP-01B assembly-local metric envelope / placement resolution.


## 17. MP-01B Gate F

**PASS**

Resolved for first lower-assembly build:
- 四椽栿 realization length: **7192 mm**
- 平梁 realization length: **3672 mm**
- lower support stations: **Y = ±1836 mm**
- clear support envelope above 四椽栿: **306 mm**
- interior Linggong assembly candidate: **893.3 × 153.6 × 215.0 mm**
- Tuofeng LOWER_SUPPORT residual height: **91.0 mm**

Evidence boundary:
- 893.3 × 153.6 × 215.0 mm is a same-building interior analog, not a direct target-role measurement;
- Tuofeng metric values remain reconstructed / replaceable;
- hidden joinery and exact contact faces remain UNKNOWN.

Next:
> MP-01B Gate G｜Lower Assembly First Build Preparation

Blender execution remains NOT AUTHORIZED.


## 18. MP-01B Gate G

**DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

Locked:
- 6 logical assembly objects;
- 2 control datums;
- common +90° local-X→assembly-Y axis mapping;
- exact canonical transforms;
- 6 SUPPORT + 4 LOCATE records;
- contact planes at Z=0 / 91 / 306;
- 27 machine checks;
- mutation test: support clearance 306 → 310 mm;
- six-panel Review Board.

Important:
- local-axis mapping is PROJECT_ASSEMBLY_RULE / REPLACEABLE;
- exact historical contact faces and hidden joinery remain UNKNOWN;
- Blender execution is NOT AUTHORIZED.

Next:
> MP-01B Gate H｜Lower Assembly First Engineering Build


## 19. MP-01B Gate H

**MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**

- T-044 Run: `37432149756` — SUCCESS
- Artifact: `11397412125`
- Validation: **51/51 PASS**
- Reopen / deterministic rebuild / 306→310 mutation: PASS
- Review note: support groups visibly straddle the ±1836 Pingliang end stations because of the approved replaceable Gate G axis/station rule.
- Next: Product Owner accepts or requests a local orientation/placement revision.


## 20. MP-01B Gate H evidence recheck

Primary-source recheck invalidated the Gate F/G vertical-stack interpretation.

Key correction:
- 306 mm must not be decomposed as `Tuofeng + Linggong`.
- Report p107/printed p92 explicitly includes `四椽栿、驼峰、襻间柱斗平欹` in the relevant 40-fen vertical padding.
- Report p99/printed p84 directly measures an interior `襻间/隔架用柱斗` family.
- Gate H machine proof is archived; MP-01B is **NOT APPROVED**.
- No support-center shift or Linggong rotation is authorized merely from visual appearance.
