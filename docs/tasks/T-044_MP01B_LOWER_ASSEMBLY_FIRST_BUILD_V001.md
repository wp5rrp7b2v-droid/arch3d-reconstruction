# T-044｜MP-01B Lower Assembly First Engineering Build V001

Status: **ENGINEERING EXECUTION COMPLETE / MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**
Date: 2026-10-06

## Goal

Build and validate the first deterministic lower assembly:

`四椽栿-东缝 → 驼峰 LOWER_SUPPORT / 梁架承托令栱 → 平梁-东缝`

## Authority

- MP-01B Gate F numeric contract: PASS
- MP-01B Gate G Build Preparation: Product Owner approved
- Product Owner instruction: `下一步：MP-01B Gate H`

## Locked build scope

Six logical assembly objects:
1. 四椽栿-东缝
2. 平梁-东缝
3. South LOWER_SUPPORT Tuofeng
4. North LOWER_SUPPORT Tuofeng
5. South Interior Linggong
6. North Interior Linggong

Two control datums:
- Y=+1836 mm
- Y=-1836 mm

## Required proof

- canonical deterministic build;
- independent reopen;
- clean deterministic rebuild;
- 306→310 mm dependency mutation;
- 6 SUPPORT / 4 LOCATE semantic records;
- contact-plane closure at Z=0 / 91 / 306;
- no unsupported historical metric or joinery claim;
- Review Board;
- machine validation;
- Actions Artifact.

## Boundary

Gate H may prove only this MP-01B Minimum-Proof subset.

Not authorized:
- historical exactness claim;
- whole-frame / whole-hall extrapolation;
- combining MP-01A + MP-01B before later authorization;
- PR #56 merge.


## Engineering result

- Run: `37432149756` — **SUCCESS**
- Artifact: `11397412125`
- Validation: **51/51 PASS**
- Independent reopen: PASS
- Deterministic rebuild: PASS
- 306→310 dependency mutation: PASS
- Product Owner acceptance: REQUIRED
- Combine with MP-01A: NOT AUTHORIZED
- PR #56 merge: NOT AUTHORIZED
