# 【中国古建筑3D复原｜T-024｜P3_3_RUFU_MASTER_FIRST_ARTICLE_V001｜乳栿 Master 首件生产】

Status: **CONTRACT LOCKED / EXECUTION NOT YET AUTHORIZED / D-083**  
Execution Mode: **CHATGPT_DIRECT_GITHUB_EXECUTION / GITHUB_ACTIONS_HEADLESS_BLENDER**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-20  
Branch: `codex/t024-p3-3-rufu-master-first-article-v001`  
PR: **REQUIRED / DO NOT MERGE WITHOUT PRODUCT OWNER APPROVAL**

## 1. Objective

建立并验证一个乳栿 canonical Master family：
- `CMP-FRAME-RUFU-001_MASTER`

Role semantics：
- vertical = `UPPER` / `LOWER`
- corner = `NE` / `SE` / `SW` / `NW`

所有 role 在 Stage 1 必须共享同一 canonical body geometry。

## 2. Authoritative Inputs

Canonical registry：
`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json` / V008

Locked Spec：
- `docs/production/zhenguo_wanfo/P3_3_STAGE1_RUFU_MASTER_SPEC_V001.md`
- `production/zhenguo_wanfo/registry/P3_3_STAGE1_RUFU_MASTER_SPEC_V001.json`

Visual gate：
- D-076 = ACTIVE governance rule
- D-082 = 乳栿 visual gate PASS
- direct reference = SRC-ZG-WF-001 PDF p84 / printed p69 / Fig.2-42

不得新增独立乳栿 evidence registration 文档。

## 3. Locked Measurement Boundary

- physical instances = 8
- Table2-40 rows = 8
- complete measured samples = 6
- unmeasured rows = 2
- complete samples = 331×185 / 337×186 / 323×193 / 342×185 / 325×188 / 325×186 mm
- family mean section = **330.5 × 187.2 mm**
- classification = DIRECT_MEASURED_FAMILY_MEAN
- sample_to_instance_mapping = UNKNOWN
- report fen 21.6×12.2 / rounded 22×12 = metadata only

## 4. Length / Angle Rule

- historical full length = null / UNKNOWN
- canonical reference length = 1000 mm / NON_HISTORICAL_REFERENCE_ONLY
- exact plan angle = null / UNKNOWN
- real orientation and real length derive later from explicit assembly endpoints

**Never hard-code 45° merely because the member is diagonal at a corner.**

Hard fail:
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `SILENT_45_DEGREE_ASSUMPTION`

## 5. Geometry Contract

Geometry mode = `BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`

Canonical body:
- X = 1000 mm
- Y = 330.5 mm
- Z = 187.2 mm

Axes:
- +X longitudinal
- +Y width
- +Z thickness

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform:
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

Diagonal placement is assembly-owned and must not be baked into the canonical Master.

## 6. Role Policy

`UPPER`, `LOWER`, `NE`, `SE`, `SW`, `NW` are assembly/placement roles only.

Role changes must not alter:
- body dimensions
- semantic geometry signature
- end profile
- groove geometry
- transform baseline

## 7. Assembly / Groove Boundary

Direct semantic metadata:
- bracket_end = 与斗栱交接
- opposite_end = UNKNOWN / assembly endpoint unresolved
- 丁栿与斜乳栿间距 = 一材一栔
- 垫单材栿一层

Groove:
- existence = DIRECT
- geometry = DEFERRED
- Stage1 body must contain **no actual groove cut**

No mortise/tenon, unsupported end profile, hidden joint, camber, damage, deformation bake, or assumed 45-degree cut.

## 8. Required Engineering Outputs

1. `production/zhenguo_wanfo/component_library/masters/CMP-FRAME-RUFU-001/CMP-FRAME-RUFU-001_MASTER_PARAMS_V001.json`
2. `build_rufu_master_v001.py`
3. `production/zhenguo_wanfo/scripts/rufu_master_common_v001.py`
4. `production/zhenguo_wanfo/scripts/validate_rufu_master_v001.py`
5. `.github/workflows/p3_3_t024_rufu_master.yml`
6. Actions artifact containing canonical .blend, semantic snapshot, reopen/mutation/role evidence, validation JSON, engineering review and SHA256 manifest
7. Review PNG minimum 6: FRONT / SIDE / TOP / AXON / DIMENSION_PARAMETER_SUMMARY / EVIDENCE_UNCERTAINTY_SUMMARY

## 9. Validation Contract

Must machine-check at least:
1. physical instances=8
2. UPPER=4 / LOWER=4
3. NE/SE/SW/NW each=2
4. table rows=8
5. complete samples=6
6. unmeasured rows=2
7. six samples retained
8. sample mapping=UNKNOWN
9. width=330.5
10. thickness=187.2
11. fen metadata only
12. historical length=null
13. 1000 reference non-historical
14. exact plan angle=null
15. no 45-degree assumption
16. UPPER/LOWER same geometry signature
17. all corner roles same geometry signature
18. bracket-end semantic present
19. opposite endpoint unresolved
20. 一材一栔 / 单材栿 semantics retained
21. groove existence DIRECT
22. groove geometry DEFERRED
23. no actual groove cut
24. bbox correctness
25. canonical origin/transform
26. length mutation only X
27. width mutation only Y
28. thickness mutation only Z
29. role mutations preserve geometry
30. independent reopen
31. deterministic semantic restore
32. D-076 / D-082 traceable
33. no REFERENCE_LENGTH_LEAKS_INTO_BUILDING
34. no SILENT_HISTORICIZATION
35. no SILENT_45_DEGREE_ASSUMPTION
36. no UNDECLARED_PARAMETRIC_COMPLETION
37. no MASTER_WITHOUT_EVIDENCE_BINDING
38. no .blend committed

## 10. Blender Rule

- Blender pinned to 4.5.13 LTS
- formal execution only via GitHub Actions
- .blend stays in Actions artifact, not Git
- exact version unavailable = STOP

## 11. Git / PR Rule

ONE TASK = ONE BRANCH = ONE PR.

PR title:
`T-024｜乳栿 Master First Article V001`

Engineering completion may only reach:
`ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`

No final Master approval and no PR merge without separate Product Owner authorization.

## 12. Protected Boundaries

T-024 must not modify/reactivate:
- T-018 / PR #3 / PR #6
- T-020
- RZ D-063
- FV D-064
- approved T-021 / T-022 / T-023 facts
- P2 frozen baseline

D-076 remains active for later new components.
T-018 remains HOLD.

## 13. Authorization Boundary

D-083 locks this task contract creation only.

**Engineering execution has NOT started.**

To start T-024, Product Owner must explicitly authorize:
`开始 T-024`.
