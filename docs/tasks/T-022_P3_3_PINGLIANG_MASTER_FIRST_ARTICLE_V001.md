# 【中国古建筑3D复原｜T-022｜P3_3_PINGLIANG_MASTER_FIRST_ARTICLE_V001｜平梁 Master 首件生产】

Status: **CONTRACT ACTIVE / PRODUCT OWNER AUTHORIZED / ENGINEERING EXECUTION AUTHORIZED / D-073**  
Execution Mode: **CHATGPT_DIRECT_GITHUB_EXECUTION / GITHUB_ACTIONS_HEADLESS_BLENDER**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-20  
Branch: `codex/t022-p3-3-pingliang-master-first-article-v001`  
PR: **REQUIRED / DO NOT MERGE WITHOUT PRODUCT OWNER APPROVAL**

## 1. Objective

完成一个平梁 canonical Master family，并验证两个正式截面 Variant：

- `CMP-FRAME-PINGLIANG-001_MASTER`
- `EW_SEAM`：东缝/西缝
- `GABLE`：东山/西山

目标是服务“尽可能依据现有资料完成整殿模型”，不是宣称963年逐件完全复原。

## 2. Authoritative Input

唯一构件事实源：

`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json` / V008。

来源定位已直接写入 V008：

- SRC-ZG-WF-001
- PDF p83 / 印刷 p68
- 2.3.1.3
- 表2-40
- 图2-41

不得新增独立平梁 evidence registration 文档。

## 3. Locked Evidence / Production Boundary

### EW_SEAM

- physical instances = 平梁-东缝、平梁-西缝
- raw samples = 390×280 mm、401×281 mm
- sample_to_instance_mapping = UNKNOWN
- production section = family mean 395.5×280.5 mm
- classification = DIRECT_MEASURED_FAMILY_MEAN
- report 26分×18分 = REPORT_INFERRED metadata only

### GABLE

- physical instances = 平梁-东山、平梁-西山
- observed sample = width 346 mm / thickness UNKNOWN
- sample_to_instance_mapping = UNKNOWN
- production width = 346 mm
- production thickness = 245.4 mm
- 245.4 = 346×280.5/395.5
- classification = PARAMETRIC_COMPLETION / PROJECT_RULE / REPLACEABLE / historical_claim=false
- production width generalized to both gable instances is also explicitly replaceable
- report width 23分 = REPORT_INFERRED metadata only

禁止把245.4mm表述为实测、报告值或963年设计值。

## 4. Length Contract

- historical_full_length_mm = null / UNKNOWN
- canonical_reference_length_mm = 1000.0 / NON_HISTORICAL_REFERENCE
- canonical Master/Variant binary only uses reference length
- real building instance length must later derive from explicit assembly endpoints
- reference length leaking into building = HARD FAIL

## 5. Geometry Contract

Geometry mode = BOUNDED_LONG_MEMBER_OUTER_ENVELOPE.

- +X = member longitudinal
- +Y = section width
- +Z = vertical thickness
- origin = longitudinal midpoint / transverse center / lower reference plane
- canonical transform = Location(0,0,0), Rotation(0,0,0), Scale(1,1,1)

No mortise/tenon, notch, groove, end-profile, camber, damage, deformation bake, hidden joint, or legacy P2 proxy geometry.

## 6. Required Engineering Outputs

1. `production/zhenguo_wanfo/component_library/masters/CMP-FRAME-PINGLIANG-001/CMP-FRAME-PINGLIANG-001_MASTER_PARAMS_V001.json`
2. `build_pingliang_master_v001.py`
3. `production/zhenguo_wanfo/scripts/pingliang_master_common_v001.py`
4. `production/zhenguo_wanfo/scripts/validate_pingliang_master_v001.py`
5. `.github/workflows/p3_3_t022_pingliang_master.yml`
6. Actions artifacts:
   - canonical EW_SEAM .blend
   - canonical GABLE .blend
   - semantic snapshots
   - independent reopen evidence
   - mutation evidence
   - validation JSON
   - Stage1 catalog proposal
   - engineering review
   - SHA256 manifest
7. Review PNG = 10:
   - EW_SEAM FRONT/SIDE/TOP/AXON
   - GABLE FRONT/SIDE/TOP/AXON
   - DIMENSION_PARAMETER_SUMMARY
   - EVIDENCE_UNCERTAINTY_SUMMARY

## 7. Validation

Must machine-check at least:

- 4 physical Pingliang records in V008
- exact instance IDs
- two variants and stable IDs
- raw EW samples and UNKNOWN mapping
- EW mean 395.5×280.5
- one gable observed sample width346 / thickness null
- GABLE production width346 / thickness245.4
- 245.4 completion formula and replaceable/non-historical labels
- report-derived fen values do not drive geometry
- reference length is non-historical and does not become building length
- bbox dimensions for both variants
- independent reopen for both variants
- deterministic restore
- length mutation isolates X
- width mutation isolates Y
- thickness mutation isolates Z
- GABLE completion thickness mutation remains completion, not evidence promotion
- 10 review images complete
- no .blend committed
- V008 / P3.1 Masters / T-018 / T-020 / RZ / FV unchanged
- no silent historicization
- no undeclared parametric completion
- no legacy proxy as real component

## 8. Blender Rule

- Blender pinned to 4.5.13
- formal execution only in GitHub Actions
- .blend stored as Actions artifact, never committed
- failure to obtain exact Blender version = STOP

## 9. Git / PR Rule

ONE TASK = ONE BRANCH = ONE PR.

PR title:
`T-022｜平梁 Master First Article V001`

Engineering completion may only reach:
`ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`.

No PR merge and no final Master approval without separate Product Owner authorization.

## 10. Protected Boundaries

T-022 must not modify or reactivate:

- T-018 / PR #3 / PR #6
- T-020
- RZ D-063
- FV D-064
- P2 frozen baseline
- P3.1 approved Master binaries/assets
- V008 facts except through separately approved registry governance

T-018 remains HOLD.
