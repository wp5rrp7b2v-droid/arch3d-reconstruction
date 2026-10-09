# MP-01B｜Tuojiao First Geometry Engineering Result V001

Status: **MACHINE PASS / PRODUCT OWNER APPROVED / TUOJIAO FIRST-ARTICLE ACCEPTED**
Date: 2026-10-06

## Run
- Task: T-046
- Run: 37472462998
- Artifact ID: 11416983796
- Artifact digest: sha256:d7a9065d07c5109bc18d6d28c92b8142a52edbfc9cb3478caa49ba0371d80eab
- Validation: 41/41 PASS

## Canonical geometry
Rendered physical geometries: 12.
New Tuojiao solids:
- ASM-MP01B-TUOJIAO-FRONT-01
- ASM-MP01B-TUOJIAO-REAR-01

Tuojiao first-article controls:
- section: 237.1 × 153.7 mm
- horizontal projection: 1759.5 mm
- relative rise: 933.3 mm
- centerline length: 1991.7050835904395 mm
- angle: 27.943034423382937°
- canonical Z offset: 0 mm, replaceable first-article assembly datum

## Validation
- independent reopen: PASS
- deterministic rebuild: PASS
- Z-offset mutation 0→50 mm: PASS
- only Tuojiao geometry changes under Z-offset mutation: PASS
- hidden joinery remains UNKNOWN
- joinery cut count: 0
- Panjian Fang remains deferred
- no whole-frame or whole-hall claim

## Signatures
- canonical assembly signature: 8001d642fa6cf67e474ef88534157ef74b46573d52c69363a64103ad9df18814
- mutation assembly signature: 9d6137200e213b43fbfa759f270d48206039ae55f67b25788a9ece6cfc091d57
- canonical blend SHA-256: 1a11598ef3af8ff2b0d2c5b2ca4b861ecf3af2f02fbafbcb9f210930a9e84a03
- semantic SHA-256: 7f6451c230996e8eded9504b25c86fab52b84ca41e8ee0ec18e031bef783ce6c
- Review Board SHA-256: 2ee3e441a13d022a81ad20bc94db4f300b7e723327c303694fe8937860c142cf

## Boundary
MACHINE PASS proves deterministic execution of the approved T3 first-article contract only.

It does not establish:
- exact historical Tuojiao endpoints;
- exact Huagong–Tuojiao contact coordinates;
- hidden mortise / tenon / groove geometry;
- historical FRONT/REAR symmetry;
- MP-01B acceptance;
- PR #56 merge authorization.

## Product Owner decision

**APPROVED — Tuojiao first article only.**

Approved baseline:
- `ASM-MP01B-TUOJIAO-FRONT-01`
- `ASM-MP01B-TUOJIAO-REAR-01`
- current evidence-bounded rectangular diagonal-envelope realization
- 237.1 × 153.7 mm family-mean section completion
- 1759.5 mm horizontal projection
- 933.3 mm relative rise
- 1991.7050835904395 mm centerline control
- 27.943034423382937° slope control

Still unresolved / not accepted:
- exact historical endpoints;
- exact Huagong–Tuojiao contact coordinates;
- hidden joinery;
- Circle 1 Huagong visible gong-head profile;
- Circle 2 remaining node incompleteness including deferred Panjian Fang / visible bracket-form issue;
- Circle 3 Tuofeng–Ludou visible-form gap;
- MP-01B overall acceptance;
- PR #56 merge.
