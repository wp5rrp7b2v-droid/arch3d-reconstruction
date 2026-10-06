# MP-01｜东缝核心梁架 Minimum Proof｜Assembly Start V001

Status: **ASSEMBLY DESIGN STARTED / GATE A COMPLETE / ENGINEERING BUILD NOT YET AUTHORIZED**
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

## 6. Next complete step

**MP-01A Gate B｜Ridge Support Target Datum Resolution**

Only this question is next:

> For the 东缝 upper-ridge subassembly, what geometry/evidence should own the Shuzhu and Chashou upper endpoint target?

Candidate owner to test:
- the relevant 正身脊槫 support region / ridge-support assembly geometry.

Do not start Blender assembly before Gate B is resolved.
