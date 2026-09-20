# 【中国古建筑3D复原｜T-023｜P3_3_DINGFU_MASTER_FIRST_ARTICLE_V001｜丁栿 Master 首件生产】

Status: **CONTRACT LOCKED / EXECUTION NOT YET AUTHORIZED / D-078**  
Execution Mode: **CHATGPT_DIRECT_GITHUB_EXECUTION / GITHUB_ACTIONS_HEADLESS_BLENDER**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-20  
Branch: `codex/t023-p3-3-dingfu-master-first-article-v001`  
PR: **REQUIRED / DO NOT MERGE WITHOUT PRODUCT OWNER APPROVAL**

## 1. Objective

建立并验证一个丁栿 canonical Master family：

- `CMP-FRAME-DINGFU-001_MASTER`
- assembly-role = `UPPER` / `LOWER`

两种 role 共用同一 canonical body geometry，不得静默产生不同截面或不同端部造型。

## 2. Authoritative Input

唯一构件事实源：

`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json` / V008。

Locked Spec：

- `docs/production/zhenguo_wanfo/P3_3_STAGE1_DINGFU_MASTER_SPEC_V001.md`
- `production/zhenguo_wanfo/registry/P3_3_STAGE1_DINGFU_MASTER_SPEC_V001.json`

不得新增独立丁栿 evidence registration 文档。

## 3. Locked Evidence / Geometry Boundary

- physical instances = 8
- measured section samples = 8组
- family mean section = 331.6 × 200.9 mm
- classification = DIRECT_MEASURED_FAMILY_MEAN
- sample_to_instance_mapping = UNKNOWN
- report fen analysis = 21.7×13.1 / rounded 22×13 = REPORT_INFERRED metadata only
- historical full length = null / UNKNOWN
- canonical reference length = 1000 mm / NON_HISTORICAL_REFERENCE
- role variants = UPPER / LOWER / shared body geometry

## 4. Interface / Groove Boundary

Semantic-only interfaces：
- OUTBOARD_END = 进入山面柱头铺作
- INBOARD_END = 骑栿栱 / 与榑交构区域

Groove：
- existence = DIRECT
- geometry = DEFERRED
- Stage1 body must contain no actual groove cut

禁止把“存在槽口”升级为未经证据支持的槽宽/槽深/槽长/精确位置。

## 5. Geometry Contract

Geometry mode = BOUNDED_LONG_MEMBER_OUTER_ENVELOPE

- +X = longitudinal
- +Y = width
- +Z = thickness
- origin = longitudinal midpoint / transverse center / lower reference plane
- body = 1000 × 331.6 × 200.9 mm
- canonical transform = Location(0,0,0), Rotation(0,0,0), Scale(1,1,1)

No mortise/tenon, real groove cut, unsupported end profile, camber, damage, deformation bake, or legacy proxy geometry.

## 6. Required Engineering Outputs

1. `production/zhenguo_wanfo/component_library/masters/CMP-FRAME-DINGFU-001/CMP-FRAME-DINGFU-001_MASTER_PARAMS_V001.json`
2. `build_dingfu_master_v001.py`
3. `production/zhenguo_wanfo/scripts/dingfu_master_common_v001.py`
4. `production/zhenguo_wanfo/scripts/validate_dingfu_master_v001.py`
5. `.github/workflows/p3_3_t023_dingfu_master.yml`
6. Actions artifact:
   - canonical .blend
   - semantic snapshot
   - independent reopen evidence
   - mutation evidence
   - validation JSON
   - engineering review
   - SHA256 manifest
7. Review PNG = 6:
   - FRONT
   - SIDE
   - TOP
   - AXON
   - DIMENSION_PARAMETER_SUMMARY
   - EVIDENCE_UNCERTAINTY_SUMMARY

## 7. Validation Contract

Must machine-check at least:

- 8 physical Dingfu records
- exact instance IDs
- 8 measured samples retained
- sample_to_instance_mapping = UNKNOWN
- width = 331.6
- thickness = 200.9
- report fen values metadata only
- historical full length null
- 1000 reference length non-historical
- UPPER/LOWER share same geometry signature
- role switch does not alter body dimensions
- semantic interfaces present
- groove existence DIRECT
- groove geometry DEFERRED
- canonical body has no groove mesh cut
- X/Y/Z bbox correctness
- independent reopen
- deterministic semantic restore
- length mutation isolates X
- width mutation isolates Y
- thickness mutation isolates Z
- role mutation preserves geometry
- D-077 Dingfu-only visual waiver traceable
- no REFERENCE_LENGTH_LEAKS_INTO_BUILDING
- no SILENT_HISTORICIZATION
- no UNDECLARED_PARAMETRIC_COMPLETION
- no MASTER_WITHOUT_EVIDENCE_BINDING
- no unauthorized Stage2 interface geometry
- no .blend committed

## 8. Blender Rule

- Blender pinned to 4.5.13
- formal execution only via GitHub Actions
- .blend stored as artifact, not committed
- exact version unavailable = STOP

## 9. Git / PR Rule

ONE TASK = ONE BRANCH = ONE PR.

PR title:
`T-023｜丁栿 Master First Article V001`

Engineering completion may only reach:
`ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`.

No final Master approval and no PR merge without separate Product Owner authorization.

## 10. Protected Boundaries

T-023 must not modify/reactivate:

- T-018 / PR #3 / PR #6
- T-020
- RZ D-063
- FV D-064
- P2 frozen baseline
- approved T-021 / T-022 Master facts
- V008 facts except separately approved governance changes

D-076 remains active for later new components; D-077 applies only to Dingfu.

T-018 remains HOLD.

## 11. Authorization Boundary

D-078 locks this task contract creation only.

**Engineering execution has NOT started.**

To start T-023, Product Owner must explicitly authorize:
`开始 T-023`.
