# T-047｜MP-01B Circle 1 Targeted Build V001

Status: **ENGINEERING EXECUTION COMPLETE / MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED**
Date: 2026-10-06

## Goal
Implement only the Product-Owner-approved Circle 1 visible gong-head profile on the FRONT/REAR interior depthwise Huagong while preserving the approved T-046 Tuojiao geometry and every other MP-01B physical geometry.

## Approved Circle 1 control
- Candidate: `MP01B_INTERIOR_HUAGONG_VISIBLE_PROFILE_V001_C01`
- Total realization length: 900 mm
- Inward gong-head zone: 650 mm
- Outward Tuojiao zone: 250 mm
- FRONT section authority: 221 × 153 mm
- REAR section authority: 210 × 156 mm
- target-specific asymmetric visible gong-head profile
- T-040 outer-eaves Huagong geometry reuse: NO
- hidden contact / joinery: UNKNOWN / DEFERRED
- joinery cut count: 0

## Frozen baseline
Approved T-046:
- Run: 37472462998
- Artifact: 11416983796
- Tuojiao FRONT/REAR first articles are frozen and must remain geometry-identical.
- Four-Chuanfu, Pingliang, Tuofeng, Panjian Ludou and Linggong are frozen.
- Panjian Fang remains deferred.

## Required proof
- exactly 12 rendered physical geometries;
- exactly two interior Huagong solids receive the new profile;
- Huagong 900 / 650 / 250 length-zone controls unchanged;
- all non-Huagong T-046 geometry signatures unchanged;
- T-046 Tuojiao signatures unchanged;
- independent reopen PASS;
- deterministic rebuild PASS;
- profile-tip mutation 0.15 → 0.25 changes only the two Huagong meshes;
- nine engineering renders plus Review Board;
- Circle 2 remains OPEN;
- Circle 3 remains OPEN;
- MP-01B remains NOT APPROVED;
- PR #56 merge remains NOT AUTHORIZED.

## Product Owner authorization
Instruction: **开始 Circle 1 Targeted Build**

## Engineering result

- GitHub Actions Run: `37476995027`
- Artifact: `MP01B_T047_CIRCLE1_TARGETED_BUILD_V001`
- Artifact ID: `11418594641`
- Artifact digest: `sha256:5843070ebcafadc9c60cfa92d040f87a4d07fb52bf9141ad6bd251853a4d7567`
- Validation: **51 / 51 PASS**
- Independent reopen: PASS
- Deterministic rebuild: PASS
- Profile-tip mutation 0.15 → 0.25: PASS
- All non-Huagong T-046 geometry signatures frozen: PASS
- T-046 Tuojiao FRONT/REAR geometry frozen: PASS
- Canonical assembly signature: `6ce17c0a7af5b4ae7e5ae7b0ea33bee0656046383e060c48644bc1f5ed767786`
- Mutation assembly signature: `a1c333943d4e47b21914e12a649d7bc38a10d0fff99505c7224e1903cc94d303`
- Canonical .blend SHA-256: `f3138fd874ab316da1114fe4ad18de115be212fff362209d31b68ede277dfa0e`
- Review Board SHA-256: `03d50888181b48560df72ff0596bc8e180c8c87018e953a97e1fc4753f0d8889`
- Product Owner acceptance: REQUIRED
- Circle 2: OPEN
- Circle 3: OPEN
- MP-01B overall: NOT APPROVED
- PR #56 merge: NOT AUTHORIZED

Machine PASS proves only that the approved Circle 1 profile control was implemented deterministically and that the frozen T-046 geometry did not change.
