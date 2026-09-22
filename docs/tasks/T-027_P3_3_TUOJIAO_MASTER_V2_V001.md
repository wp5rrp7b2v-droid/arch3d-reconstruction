# 【中国古建筑3D复原｜T-027｜P3_3_TUOJIAO_MASTER_V2_V001｜托脚 Master 首件生产】

Status: **ENGINEERING EXECUTION AUTHORIZED / D-102 / FIRST ARTICLE IN PROGRESS**  
Execution architecture: **MASTER V2 / MINIMAL_SUFFICIENT / SHARED INFRASTRUCTURE**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-22  
Proposed branch: `codex/t027-p3-3-tuojiao-master-v2-v001`  
PR policy: **ONE TASK = ONE BRANCH = ONE PR / DO NOT CREATE UNTIL EXECUTION AUTHORIZED**

## 1. Objective

建立并验证一个托脚 canonical Master：

- component id: `CMP-FRAME-TUOJIAO-001`
- master id: `CMP-FRAME-TUOJIAO-001_MASTER`
- master version: `V001`

Stage1 只允许一个 shared canonical body。

Assembly / placement roles：
- `MAIN_FRAME` = 8
- `GABLE` = 4

Role 差异不得自动生成 geometry Variant。

## 2. Authoritative Inputs

### A1｜一级工程主权来源
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct binding：
- PDF p89–90 / printed p74–75
- §2.3.1.8｜托脚与叉手
- 表2-45
- cross-check: PDF p102 / printed p87 / 表2-50

Formal evidence record：
`docs/evidence/zhenguo_wanfo/P3_3_TUOJIAO_DIRECT_SOURCE_BINDING_V001.md`

### A2｜官方同建筑视觉/结构来源
山西文物数字博物馆·万佛殿专题。

锁定结构语义：
`SUPPORTS_ENDS_OF_FOUR_CHUANFU`

### Canonical project inputs
- `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json` / V008
- `docs/production/zhenguo_wanfo/P3_3_STAGE1_TUOJIAO_MASTER_SPEC_V001.md`
- `production/zhenguo_wanfo/registry/P3_3_STAGE1_TUOJIAO_MASTER_SPEC_V001.json`

Decision chain：
- D-076 visual gate
- D-099 / RC-019 source-authority priority
- D-100 Tuojiao Master Spec V001

SRC-ZG-WF-001 canonical PDF Git/LFS publication may remain pending during contract locking; it must not be used as a reason to downgrade already completed direct-page review.

## 3. Locked Measurement Boundary

Physical instances：
- total = **12**
- MAIN_FRAME = **8**
- GABLE = **4**

Table 2-45：
- rows = **11**
- complete visible measured rows = **10**
- unmeasured visible row = **1**

Visible complete samples, mm：
- 249×152
- 245×151
- 245×152
- 244×149
- 250×151
- 250×154
- 214×151
- 213×158
- 212×150
- 219×173

Report-published mean：
- width = **237.1 mm**
- thickness = **153.7 mm**

Visible-row arithmetic recompute：
- width = **234.1 mm**
- thickness = **154.1 mm**
- classification = `AUDIT_ONLY`

Locked source status：
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = TRUE`
- `SILENT_ARITHMETIC_CORRECTION = PROHIBITED`

Canonical section uses the report-published value:
**237.1 × 153.7 mm**

The recomputed value must remain visible in Definition / Review / Validation as an audit discrepancy and must never silently replace canonical geometry.

## 4. Geometry Contract

Geometry mode：
`BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`

Canonical body：
- X = **1000 mm**
- Y = **237.1 mm**
- Z = **153.7 mm**

Axes：
- +X longitudinal
- +Y width / 广
- +Z thickness / 厚

Origin：
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform：
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

1000 mm = `NON_HISTORICAL_REFERENCE_ONLY`.

Historical full length = `null / UNKNOWN`.  
Exact placement angle = `null / UNKNOWN`.

Real length and orientation are assembly-owned and must later derive from explicit assembly endpoints.

## 5. Role Policy

`MAIN_FRAME` and `GABLE` are semantic assembly / placement roles only.

They must not alter:
- canonical section
- canonical body signature
- end profile
- joinery
- canonical transform
- fixed angle

A future Variant split requires new A1 evidence proving stable body-geometry differences.

## 6. Assembly / Joinery Boundary

Allowed semantic:
- `member_type = DIAGONAL_FRAME_SUPPORT`
- `official_same_building_semantic = SUPPORTS_ENDS_OF_FOUR_CHUANFU`
- `exact_endpoint_contact_geometry = UNKNOWN / ASSEMBLY_ENDPOINT_TO_BE_RESOLVED`

Stage1 must not generate:
- four-chuanfu geometry
- purlin geometry
- building placement coordinates
- fixed installation angle
- exact contact faces
- mortise / tenon
- notch / groove
- hidden joint
- unsupported end cuts

Old P2 `FRAME_SUPPORT` proxy must not be renamed/reused as Tuojiao geometry.

## 7. Master V2 Architecture

T-027 must reuse the shared V2 infrastructure introduced and validated by T-025 / T-026:

- `production/zhenguo_wanfo/scripts/p3_3_master_v2_common.py`
- `production/zhenguo_wanfo/scripts/validate_p3_3_master_v2.py`
- `.github/workflows/p3_3_master_v2.yml`

Do not create Tuojiao-specific builder / validator / workflow unless a genuinely non-shareable requirement is discovered and formally recorded.

### Numeric-conflict extension rule

Current shared V2 infrastructure does not yet provide a generic source-internal numeric-conflict presentation/validation contract.

If T-027 execution requires an infrastructure extension, it must be **generic / Definition-driven**, supporting fields such as:
- source numeric conflict
- published mean
- recomputed audit mean
- silent-correction prohibition
- conflict-specific Review Board text

It must not be hard-coded only for Tuojiao.

Any shared-infrastructure change must run regression against approved V2 Masters:
- T-025 剳牵
- T-026 槫

No existing approved Master may be weakened or reinterpreted.

## 8. Adaptive Review Board

Formal review output:
one adaptive `MASTER_REVIEW_BOARD_V001.png`.

Required panels for Tuojiao:

1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION_ENVELOPE`
4. `DIMENSION_PARAMETER_SUMMARY`
5. `ROLE_ASSEMBLY_SEMANTICS`
6. `EVIDENCE_UNCERTAINTY_AND_NUMERIC_CONFLICT`

The final panel must visibly state:
- REPORT PUBLISHED MEAN = 237.1 × 153.7 mm
- VISIBLE-ROW RECOMPUTED MEAN = 234.1 × 154.1 mm
- SOURCE_INTERNAL_NUMERIC_CONFLICT = TRUE
- NO SILENT CORRECTION
- historical length UNKNOWN
- exact angle UNKNOWN
- endpoints UNKNOWN
- joinery/end geometry DEFERRED

Panel count is Definition-driven, not a universal project rule.

## 9. Minimal-sufficient Formal Package

Expected component-specific formal outputs:

1. `CMP-FRAME-TUOJIAO-001_MASTER_DEFINITION_V001.json`
2. `CMP-FRAME-TUOJIAO-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-TUOJIAO-001_MASTER_V001.blend` — Actions artifact + local-only, not Git
4. `CMP-FRAME-TUOJIAO-001_MASTER_REVIEW_BOARD_V001.png`
5. `CMP-FRAME-TUOJIAO-001_MASTER_VALIDATION_V001.json`
6. this lifecycle record

This is an expected minimal-sufficient result, not a fixed six-file rule.

Definition / Semantic / Validation must remain independent.

## 10. Validation Contract

Machine validation must be Definition-driven and check at least:

### Identity / registry
1. task/component/master/version identity
2. V008 schema/record authority
3. physical instances=12
4. MAIN_FRAME=8
5. GABLE=4

### A1 measurement
6. table rows=11
7. complete visible rows=10
8. unmeasured row=1
9. visible raw samples retained
10. sample-to-instance mapping=UNKNOWN
11. published width=237.1
12. published thickness=153.7
13. audit width=234.1
14. audit thickness=154.1
15. source internal numeric conflict=true
16. silent arithmetic correction prohibited
17. report fen metadata only / geometry_use_count=0

### Geometry
18. historical full length=null
19. canonical reference length=1000 / non-historical
20. exact angle=null
21. bbox=1000×237.1×153.7
22. canonical origin/transform
23. length mutation isolates X
24. width mutation isolates Y
25. thickness mutation isolates Z
26. MAIN_FRAME/GABLE role mutation preserves body geometry

### Assembly / uncertainty
27. A2 four-chuanfu support semantic retained
28. exact endpoints unresolved
29. joinery/end geometry deferred
30. no actual unsupported cuts
31. no P2 proxy reuse

### Reproducibility / evidence
32. independent reopen PASS
33. deterministic semantic restore
34. Definition↔Semantic identity
35. binary SHA recorded
36. Blender 4.5.13 LTS
37. all Definition-required Review Board panels complete
38. canonical .blend not tracked in Master directory
39. D-076 / D-099 / D-100 traceable

### Hard-fail guards
40. no `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
41. no `FIXED_MASTER_ANGLE`
42. no `FIXED_HISTORICAL_LENGTH_WITHOUT_A1_EVIDENCE`
43. no `SILENT_HISTORICIZATION`
44. no `SILENT_ARITHMETIC_CORRECTION`
45. no `UNDECLARED_PARAMETRIC_COMPLETION`
46. no `MASTER_WITHOUT_EVIDENCE_BINDING`

If shared V2 infrastructure is changed, T-025 and T-026 regression must also PASS before Tuojiao engineering may be considered complete.

Exact validation check count may exceed 46 if atomic checks are split further; no required information domain may be merged away merely to reduce the count.

## 11. Blender / Artifact Rule

- Blender pinned to **4.5.13 LTS**
- formal execution through GitHub Actions
- canonical .blend remains Actions Artifact + local-only
- no canonical Tuojiao .blend committed to Git
- exact Blender version unavailable = STOP

## 12. Protected Boundaries

T-027 must not modify/reactivate:
- T-018 / PR #3 / PR #6
- T-020
- RZ D-063
- FV D-064
- approved T-021–T-026 historical facts
- P2 frozen baseline

T-018 remains HOLD.

## 13. Authorization Boundary

D-101 locks this Task Contract only.

Current status:

`ENGINEERING_EXECUTION_AUTHORIZED = FALSE`  
`BLENDER_EXECUTION_AUTHORIZED = FALSE`  
`PRODUCTION_BRANCH_CREATION_AUTHORIZED = FALSE`  
`PR_CREATION_AUTHORIZED = FALSE`

To begin engineering, Product Owner must explicitly authorize:

> **开始 T-027**

Only then may the locked engineering Definition be created/finalized with execution=true, branch/PR be created, and GitHub Actions/Blender run.

Final Master approval and PR merge each remain separate Product Owner authorization boundaries.


## 14. Engineering execution authorization / D-102

Product Owner explicitly authorized **开始 T-027** on 2026-09-22.

Execution boundary now:
- engineering_execution_authorized = true
- Blender/GitHub Actions execution = authorized
- production branch = `codex/t027-p3-3-tuojiao-master-v2-v001`
- PR creation = authorized
- final first-article acceptance = still requires separate Product Owner approval
- PR merge = still requires separate Product Owner authorization

Engineering implementation must preserve all D-101 contract boundaries. Shared V2 infrastructure changes require T-025/T-026 regression before T-027 may be declared engineering-complete.


## 15. First-article engineering result｜Review Patch 01 final

**ENGINEERING COMPLETE / PRODUCT OWNER REVIEW REQUIRED**

Final reviewed engineering run:
- GitHub Actions Run: `35712113350`
- reviewed engineering commit: `86892ce6904075f0abc4813ee50bf6fd3c294f73`
- Blender: **4.5.13 LTS**
- T-027 machine validation: **56 / 56 PASS**
- canonical .blend SHA-256: `23ed48fba3bf63f58a690ab7b5f236435ffd5ce069e3b5d115f4b7bdaf6e6c3f`
- semantic geometry signature: `3c8f39d3b6eab08ad8d09651dce70dc07c1cb5c2a7a9387369416c1611911a2c`
- Semantic SHA-256: `cd28dc19cdfbeefa391298c9ae060341e4fe6e40341333bea539fe0e671084a6`
- Validation SHA-256: `69a289a2f449f68bad18d317ab65370359751accb1765e5f6d71fb38fe448655`
- Review Board SHA-256: `6bc5f05c212d07d08a0e9e1b48415718c17734dad5d8239a75b29198880b7c0f`
- formal first-article Artifact ID: `10689220649`
- Artifact ZIP SHA-256: `f255355b915c6c842b8d7e2d9a3090fce1787670d545f3d432ed8aa46f875749`
- Artifact size: 1,385,479 bytes
- Review Board: 6 Definition-required panels

Shared V2 regression after the generic numeric-conflict / role-support extension:
- T-025 剳牵: **44 / 44 PASS**
- T-026 槫: **47 / 47 PASS**
- shared-regression Artifact ID: `10689000813`
- shared-regression Artifact ZIP SHA-256: `2bb7111e739180e88ad689f65baef4411e9306a674bb617c27d2dd7747dd2419`

### Review Patch 01

Initial Run `35709735882` passed machine validation and shared regressions, but ChatGPT human review found one presentation defect in the Review Board:

- `DIMENSION_PARAMETER_SUMMARY` inherited Purlin-style distribution text and displayed `0 main / 0 E gable / 0 W gable`.
- This was a shared Review Board display defect only; canonical geometry, numeric-conflict preservation, Registry counts, role mutation, reopen, and machine validation were not affected.
- Patch commit `86892ce6904075f0abc4813ee50bf6fd3c294f73` changed the shared renderer to use Definition-driven `registry_role_counts` when present.
- Final Board now correctly displays `MAIN_FRAME 8 / GABLE 4`.
- Patch triggered a complete T-027 rerun plus T-025/T-026 regressions; all passed.

Initial Run `35709735882` is therefore **SUPERSEDED FOR HUMAN REVIEW** by final Run `35712113350`.

### Final engineering boundary

Verified:
- one shared Tuojiao canonical body;
- body reference bbox = 1000 × 237.1 × 153.7 mm;
- 1000 mm remains non-historical;
- MAIN_FRAME=8 / GABLE=4;
- role mutation preserves the canonical geometry signature;
- report-published 237.1×153.7 drives canonical section;
- visible-row recompute 234.1×154.1 remains AUDIT_ONLY;
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = TRUE`;
- `SILENT_ARITHMETIC_CORRECTION = PROHIBITED`;
- historical length / exact angle / endpoints / joinery remain UNKNOWN / DEFERRED;
- no unsupported joinery cuts;
- no P2 FRAME_SUPPORT proxy reuse;
- canonical .blend is Artifact/local-only and is not tracked in Git.

PR #14 static check at reviewed engineering head:
- branch behind main: **0**
- mergeable: **true**
- changed-file scope: exactly 5 T-027 / shared-V2 files
- PR remains **DRAFT**
- no merge authorization has been granted.

### Current authorization boundary

Engineering has reached:

`ENGINEERING_COMPLETE_PENDING_PRODUCT_OWNER_REVIEW`

Not yet authorized:
- Product Owner first-article acceptance;
- formal materialization / Catalog + Registry binding;
- PR #14 Ready/merge;
- Stage1 PASS;
- Stage2;
- T-018 resume.


## 16. Product Owner acceptance / D-103

**PRODUCT OWNER APPROVED / FIRST ARTICLE ACCEPTED / FORMAL DELIVERY AUTHORIZED**

Product Owner approved the final T-027 Tuojiao V2 first article after Review Patch 01.

Accepted evidence:
- final approved Run: `35712113350` / SUCCESS
- validation: **56 / 56 PASS**
- accepted engineering head: `86892ce6904075f0abc4813ee50bf6fd3c294f73`
- canonical .blend SHA-256: `23ed48fba3bf63f58a690ab7b5f236435ffd5ce069e3b5d115f4b7bdaf6e6c3f`
- semantic geometry signature: `3c8f39d3b6eab08ad8d09651dce70dc07c1cb5c2a7a9387369416c1611911a2c`
- Semantic SHA-256: `cd28dc19cdfbeefa391298c9ae060341e4fe6e40341333bea539fe0e671084a6`
- Validation SHA-256: `69a289a2f449f68bad18d317ab65370359751accb1765e5f6d71fb38fe448655`
- Review Board SHA-256: `6bc5f05c212d07d08a0e9e1b48415718c17734dad5d8239a75b29198880b7c0f`
- Artifact ID: `10689220649`
- Artifact ZIP SHA-256: `f255355b915c6c842b8d7e2d9a3090fce1787670d545f3d432ed8aa46f875749`

Accepted boundary:
- one shared canonical Master;
- 12 instances = MAIN_FRAME 8 + GABLE 4;
- canonical reference body = 1000 × 237.1 × 153.7 mm;
- 1000 mm remains non-historical;
- report-published 237.1 × 153.7 remains canonical;
- visible-row recompute 234.1 × 154.1 remains AUDIT_ONLY;
- SOURCE_INTERNAL_NUMERIC_CONFLICT remains explicit;
- historical full length / exact angle / endpoints / hidden joinery remain UNKNOWN / DEFERRED.

D-103 authorizes exact materialization, Catalog registration, V008/CURRENT binding, derived Excel synchronization, and final regression / pre-merge cross-check.

D-103 does **not** authorize PR #14 merge, Stage1 PASS, Stage2, or T-018 resume.

## 17. Formal materialization

**PASS / EXACT D-103 APPROVED ARTIFACT MATERIALIZED**

- publication workflow Run: `35716617847` = SUCCESS
- materialization commit: `4d588623fffa5e554d9b2c616ffb13bd34bd8ef1`
- source Artifact ID: `10689220649`
- exact-source SHA verification: PASS for .blend / Semantic / Validation / Review Board
- repository materialized files: Semantic / Validation / Review Board
- canonical .blend remains Actions Artifact + local-only / not tracked in Git
- approved Definition remained unchanged.

## 18. Catalog / Registry binding

**PASS / FINAL REGRESSION PENDING**

- Stage1 Catalog approved Master count: **13**
- V008/CURRENT Tuojiao binding: **12 / 12**
- Stage1 Master progress: **13 / 28 = 46.4%**
- approved-Master-covered Registry records: **111**
- pending Master object types: **15**
- derived Excel remains DERIVED_VIEW and must synchronize from JSON before merge.

Final regression and PR #14 pre-merge cross-check are required before requesting merge authorization.
