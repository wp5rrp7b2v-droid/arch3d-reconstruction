# MP-01B｜Circle 1 Targeted Build Engineering Result V001

Status: **MACHINE PASS / PRODUCT OWNER REVIEW REQUIRED / CIRCLE 1 NOT YET ACCEPTED**
Date: 2026-10-06

## Scope
Only the approved interior-Huagong visible gong-head profile was changed.

Frozen from approved T-046:
- FRONT/REAR Tuojiao;
- Four-Chuanfu;
- Pingliang;
- FRONT/REAR Tuofeng;
- FRONT/REAR Panjian Ludou;
- FRONT/REAR Linggong.

Circle 2 and Circle 3 remain open.

## Run
- Task: T-047
- Run: 37476995027
- Artifact ID: 11418594641
- Artifact digest: sha256:5843070ebcafadc9c60cfa92d040f87a4d07fb52bf9141ad6bd251853a4d7567
- Validation: 51/51 PASS

## Circle 1 geometry
- profile candidate: MP01B_INTERIOR_HUAGONG_VISIBLE_PROFILE_V001_C01
- total realization length: 900 mm
- inward gong-head zone: 650 mm
- outward Tuojiao zone: 250 mm
- FRONT direct section authority: 221 × 153 mm
- REAR direct section authority: 210 × 156 mm
- tip depth fraction: 0.15
- T-040 outer-eaves profile reuse: false
- joinery cut count: 0

## Machine proof
- independent reopen: PASS
- deterministic rebuild: PASS
- profile-tip mutation 0.15→0.25: PASS
- mutation changes only the two interior Huagong meshes: PASS
- all non-Huagong T-046 world geometry signatures unchanged: PASS
- approved T-046 Tuojiao geometry unchanged: PASS
- exact historical curve claim: false
- hidden joinery: UNKNOWN / DEFERRED

## Signatures
- canonical assembly signature: 6ce17c0a7af5b4ae7e5ae7b0ea33bee0656046383e060c48644bc1f5ed767786
- mutation assembly signature: a1c333943d4e47b21914e12a649d7bc38a10d0fff99505c7224e1903cc94d303
- blend SHA-256: f3138fd874ab316da1114fe4ad18de115be212fff362209d31b68ede277dfa0e
- semantic SHA-256: 7dcb7e85f76bc8b03a1f8963513633c148a1d413759f2742b76417a2907ffcfb
- Review Board SHA-256: 03d50888181b48560df72ff0596bc8e180c8c87018e953a97e1fc4753f0d8889

## Boundary
MACHINE PASS does not prove:
- historical exact gong-head curve;
- exact shoulder/end shaping;
- Huagong–Tuojiao hidden contact;
- Circle 2 resolution;
- Circle 3 resolution;
- MP-01B acceptance;
- PR #56 merge authorization.
