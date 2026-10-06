# 中国古建筑3D复原｜T-042｜P3_3_TUOFENG_MASTER_V001

Status: **TASK CONTRACT LOCKED / PRODUCT OWNER AUTHORIZED / ENGINEERING EXECUTION ACTIVE**
Date: 2026-10-06
Stage: P3.3 V002 Stage 1 reopened for 驼峰
Task id: `T-042｜P3_3_TUOFENG_MASTER_V001`
Branch: `codex/t042-p3-3-tuofeng-master-v001`
Stacked base: `governance/v008-tuofeng-master-scope-patch-v001`

## 1. Objective

Build and machine-validate one reusable Master family:

`CMP-FRAME-TUOFENG-001_MASTER V001`

with exactly two role variants:

- `LOWER_SUPPORT`
- `UPPER_RIDGE_SUPPORT`

The task tests whether explicit UNKNOWN historical dimensions can coexist with deterministic, replaceable production geometry.

## 2. Locked evidence boundary

Direct assembly roles:

- 四椽栿上用驼峰、令栱承平梁。
- 平梁之上设驼峰、蜀柱、叉手。

A1 same-building visual cross-check:
- PDF p83 / printed p68 / Fig. 2-41
- PDF p106 / printed p91 / Fig. 2-71
- PDF p109 / printed p94 / Fig. 2-73

Still UNKNOWN:
- whole-hall instance count;
- exact per-instance mapping;
- historical width/depth/height;
- exact profile;
- hidden joinery.

## 3. Geometry contract

Master family count = 1.

Role variant count = 2.

### LOWER_SUPPORT

Engineering-test canonical fixture A:
- base span = 1000 mm
- base depth = 500 mm
- base height = 180 mm
- seat span = 420 mm
- seat depth = 320 mm
- seat height = 180 mm

These are **ENGINEERING_TEST_ONLY** values.

Geometry:
- broad lower body;
- centered raised seat;
- no historical curve claim;
- no joint cuts.

### UPPER_RIDGE_SUPPORT

Engineering-test canonical fixture A:
- base span = 1000 mm
- depth = 500 mm
- height = 320 mm

Geometry:
- symmetric stepped hump profile;
- broad base;
- raised flat center seat;
- source-guided visual abstraction only.

All fixture values:
- historical_claim = false
- building_dimension_claim = false
- replaceable = true

## 4. Mutation contract

Fixture B must prove deterministic parameterization:

LOWER_B:
- 1250 / 620 / 210 / 500 / 360 / 220 mm

UPPER_B:
- 820 / 410 / 270 mm

Expected:
- component and variant identities unchanged;
- geometry signatures change;
- no unsupported historical claim appears.

## 5. Assembly ownership

Master owns:
- identity;
- role variant;
- shape logic;
- normalized/profile topology.

Assembly owns:
- final Wanfo Hall metric envelope;
- placement;
- resolved support footprints;
- vertical gaps;
- final contact regions.

If future assembly constraints are incompatible, assembly must FAIL rather than silently distort the Master.

## 6. Joinery boundary

- historical joinery = UNKNOWN / DEFERRED
- mortise count = 0
- tenon count = 0
- groove/slot count = 0
- hidden cavity count = 0

## 7. First Article package

Required:
1. `CMP-FRAME-TUOFENG-001_MASTER_V001.blend` — Actions Artifact only
2. `CMP-FRAME-TUOFENG-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-TUOFENG-001_MASTER_REVIEW_BOARD_V001.png`
4. `CMP-FRAME-TUOFENG-001_MASTER_VALIDATION_V001.json`
5. variant review renders

## 8. Hard fails

- TEST_DIMENSION_LEAKS_INTO_BUILDING
- TEST_DIMENSION_MARKED_HISTORICAL
- UNSUPPORTED_METRIC_LOCK
- UNSUPPORTED_JOINERY_CLAIM
- ROLE_VARIANTS_COLLAPSED_WITHOUT_EVIDENCE
- VARIANT_IDENTITY_SPLIT_INTO_TWO_MASTER_FAMILIES
- LOWER_SEAT_EXCEEDS_BASE
- UPPER_PROFILE_ASYMMETRY
- UNKNOWN_SILENTLY_FILLED
- REOPEN_SIGNATURE_MISMATCH
- RESTORE_NONDETERMINISTIC
- MUTATION_NO_EFFECT

## 9. Authorization

Product Owner explicitly authorized:

> 开始驼峰 First Article Engineering Execution

This authorizes:
- engineering implementation;
- GitHub Actions / Blender execution;
- first-article generation;
- machine validation;
- review artifact generation.

It does **not** pre-authorize:
- Product Owner first-article acceptance;
- formal Catalog/V008 approved-master binding;
- merge to main;
- historical metric claims.
