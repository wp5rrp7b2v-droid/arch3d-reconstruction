# 【中国古建筑3D复原｜T-021｜P3_3_FOUR_CHUANFU_MASTER_FIRST_ARTICLE_V001｜四椽栿 Master 首件生产】

Status: **CONTRACT LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT YET AUTHORIZED / CODEX CLOUD READY**  
Execution Mode: **CHATGPT_DIRECT_GITHUB_EXECUTION / FIRST_ARTICLE_ONLY**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-19  
Contract approval: **PRODUCT OWNER APPROVED / D-070**  
Execution responsibility override: **D-071 / CHATGPT DIRECT GITHUB EXECUTION**  
Cloud Mode Classification: **CLOUD_EXECUTABLE**  
Primary Engineering Executor: **ChatGPT direct GitHub execution**  
Blender Executor: **GitHub Actions headless Blender / RC-017**  
Branch: codex/t021-p3-3-four-chuanfu-master-first-article-v001  
PR: **REQUIRED / DO NOT MERGE WITHOUT PRODUCT OWNER APPROVAL**

## 1. Objective

严格依据已锁定的四椽栿 Master Spec V001、直接原页 evidence binding 和 V008 Component Registry，完成一个且仅一个新路线真实构件 Master 首件：

> CMP-FRAME-FOUR-CHUANFU-001_MASTER｜四椽栿 Master V001

本任务不得批量生产平梁、丁栿、乳栿、剳牵、槫或其他新 Master。

T-021 工程完成后状态只能到 ENGINEERING COMPLETE / PENDING CHATGPT + PRODUCT OWNER REVIEW；执行方不得宣告 Master APPROVED，也不得宣告 Stage 1 PASS。

## 2. Minimal Authoritative Read Set

执行方优先只读取：

1. 本 Task Contract；
2. docs/production/zhenguo_wanfo/P3_3_STAGE1_FOUR_CHUANFU_MASTER_SPEC_V001.md；
3. production/zhenguo_wanfo/registry/P3_3_STAGE1_FOUR_CHUANFU_MASTER_SPEC_V001.json；
4. docs/evidence/zhenguo_wanfo/P3_3_FOUR_CHUANFU_DIRECT_SOURCE_BINDING_V001.md；
5. docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json，仅验证 V008 / 两个四椽栿实例；
6. 已验证的长构件工具链参考：six_chuanfu_master_common_v001.py、上下六椽栿 Master 目录、T-013 validation/review 组织方式；
7. docs/project_control/project_state.json 仅用于核对授权边界；
8. RC-014 / RC-017 / RC-018 当前规则。

禁止重新解释整份 P1/P2/P3 历史资料。锁定输入互相冲突时立即 STOP。

## 3. Locked Evidence Inputs

- component id = CMP-FRAME-FOUR-CHUANFU-001
- master id = CMP-FRAME-FOUR-CHUANFU-001_MASTER
- physical instances = 2：四椽栿-东缝、四椽栿-西缝
- source = SRC-ZG-WF-001 PDF p82 / 印刷 p67 / 表2-39
- sample A = 413 × 295 mm
- sample B = 440 × 309 mm
- observed mean width = 426.5 mm
- observed mean thickness = 302.0 mm
- sample_to_instance_mapping = UNKNOWN，禁止静默映射东西缝
- report analysis 28 fen / 20 fen = REPORT_INFERRED metadata only，geometry_use_count = 0
- historical_full_length_mm = null / UNKNOWN / DO_NOT_LOCK
- canonical_reference_length_mm = 1000.0，仅 NON-HISTORICAL ENGINEERING_REFERENCE
- realization_length_mm 在 canonical build 中显式 derives_from canonical reference。

## 4. Geometry Contract

Geometry mode = BOUNDED_LONG_MEMBER_OUTER_ENVELOPE；LOD = EVIDENCE_BOUNDED_MEDIUM_LOD；unit = mm。

- +X = 构件纵向
- +Y = 广
- +Z = 厚
- origin = longitudinal midpoint / transverse center / lower reference plane
- Location=(0,0,0), Rotation=(0,0,0), Scale=(1,1,1)

Canonical body = realization_length_mm × 426.5 × 302.0。

它只是 bounded outer envelope，不是历史通长完全规则矩形梁的声明。

## 5. Strict Geometry Prohibitions

unsupported_geometry_count 必须为 0。禁止榫头、卯口、散斗槽、隔架单栱几何、栌斗、hidden joint、local thickness zone、无证据端部轮廓、无证据 camber、历史化挠曲、破损写实化、P2 PRIMARY_FRAME proxy mesh，以及一般古建常识补出的典型细节。

## 6. Interface Boundary

本任务只建立两个 geometry endpoints：
- END_NEG_X = (-L/2, 0, thickness/2)
- END_POS_X = (+L/2, 0, thickness/2)

以下只登记 semantic，坐标保持 ASSEMBLY_OWNED / UNKNOWN：SUPPORT_FROM_SAN_DOU、RELATION_TO_UPPER_SIX_CHUANFU、SPACER_SINGLE_GONG_RELATION。Stage 2 才允许落位。

## 7. Required Engineering Outputs

创建目录 production/zhenguo_wanfo/component_library/masters/CMP-FRAME-FOUR-CHUANFU-001/，至少生成：

1. CMP-FRAME-FOUR-CHUANFU-001_MASTER_PARAMS_V001.json
2. CMP-FRAME-FOUR-CHUANFU-001_MASTER_SEMANTIC_V001.json
3. build_four_chuanfu_master_v001.py
4. 必要的 shared helper 修改/新增（仅确有需要）
5. production/zhenguo_wanfo/validation/CMP-FRAME-FOUR-CHUANFU-001_MASTER_VALIDATION_V001.json
6. docs/production/zhenguo_wanfo/P3_3_T021_FOUR_CHUANFU_ENGINEERING_REVIEW_V001.md
7. production/zhenguo_wanfo/review/P3_3/masters/CMP-FRAME-FOUR-CHUANFU-001/ 下六张 PNG：FRONT、SIDE、TOP、AXON、DIMENSION_PARAMETER_SUMMARY、EVIDENCE_UNCERTAINTY_SUMMARY。

同时创建/更新 production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json 作为 P3.3 Stage 1 当前 Master catalog：
- 引用既有6个 P3.1 approved Master，不修改其历史批准记录；
- 新增四椽栿 record；
- 四椽栿状态只能是 ENGINEERING_COMPLETE_PENDING_CHATGPT_PRODUCT_OWNER_REVIEW；
- 不得写 APPROVED；
- 不得为了新增四椽栿去修改已关闭的 P3.1 canonical Master Library。

## 8. Blender / Binary Rule

采用 D-071 task-specific execution override：ChatGPT 直接通过 GitHub 写入 generator / validator / workflow，GitHub Actions headless Blender 执行。RC-017 的 headless Blender executor、版本锁定、artifact 与验证要求全部继续有效；仅取消“必须由 Codex Cloud 编写工程文件”这一 T-021 执行前提。

- Blender version 显式 pin = 4.5.13；不得静默切换。
- ChatGPT 不在本地或沙箱中运行 Blender；正式 Blender 执行仍只能发生在 GitHub Actions。
- .blend / .blend1 不提交 Git。
- canonical .blend 由 Actions 生成并计算 SHA-256，作为 Actions artifact 保存。
- review PNG / validation JSON / semantic JSON / params / scripts / engineering report 提交 GitHub。
- binary SHA-256 必须进入 validation 和 engineering report。
- 若 Actions 无法取得 Blender 4.5.13，立即 STOP。

## 9. Execution Stages

Stage A｜Baseline protection：记录并保护 V008 CURRENT registry、四椽栿 Spec/evidence、既有6个 Master、P3.1 closed Master Library、P2 frozen baseline、T-018/RZ/FV/T-020；不得修改。

Stage B｜Params + generator：建立 params/semantic 和 generator。优先复用已验证长构件通用机制。shared code 禁止写入 426.5、302、413、295、440、309、1000 等 component-specific 裸常量，全部来自 params JSON。

Stage C｜Canonical build：Actions 生成 reference Master；验证 X=1000、Y=426.5、Z=302、canonical transform、unsupported geometry=0。

Stage D｜Independent reopen：重新打开 binary，独立读取 bbox / identity / transforms / metadata。

Stage E｜Mutation probes：
- Probe A：reference length 1000 → test → 1000，只改变 X；historical length 始终 null。
- Probe B：width 426.5 → test → 426.5，只改变 Y。
- Probe C：thickness 302 → test → 302，只改变 Z。
- 每次 mutation 后 canonical rebuild 必须精确恢复。

Stage F｜Review render：生成6张正式审核图。

Stage G｜Catalog pending record：建立 P3.3 Stage1 Master catalog record，状态只到 pending review。

## 10. Mandatory Validation Matrix

至少 PASS 42 项：
1 unique component id；2 unique master id；3 V008 instance count=2；4 source binding=p82/p67/table2-39；5 sample A=413×295；6 sample B=440×309；7 sample mapping UNKNOWN；8 mean width=426.5；9 mean thickness=302；10 report 28/20 geometry use=0；11 historical length=null；12 canonical reference classification correct；13 realization derives from reference；14 reference不回写historical；15 X extent正确；16 Y extent正确；17 Z extent正确；18 origin正确；19 rotation=0；20 scale=1；21 unsupported geometry=0；22 P2 proxy use=0；23 semantic-only interfaces无猜测坐标；24 无A/B东西缝猜配；25 deterministic regeneration PASS；26 independent reopen PASS；27 length mutation isolate X；28 width mutation isolate Y；29 thickness mutation isolate Z；30 mutation restore PASS；31 params↔semantic PASS；32 六张review齐全；33 binary SHA记录；34 Git无blend；35 P3.1 approved Masters unchanged；36 V008 registry unchanged；37 T-018/RZ/FV/T-020 unchanged；38 Stage1 catalog=pending review only；39 no REFERENCE_LENGTH_LEAKS_INTO_BUILDING；40 no SILENT_HISTORICIZATION；41 no MASTER_WITHOUT_EVIDENCE_BINDING；42 no LEGACY_PROXY_AS_REAL_COMPONENT。

## 11. Protected / Prohibited

工程执行不得修改 V008 Component Registry、V007/V008 snapshots、P3.1 approved Master assets、P3.1 historical Master Library、P2 frozen baseline、T-018 / PR #3 / PR #6、RZ/FV/T-020、四椽栿锁定 Spec 和 source-binding evidence。Project Control 仅允许由 ChatGPT 在任务状态变更时按治理规则同步更新，不得被工程脚本修改。

不得恢复整殿生成、推导真实建筑长度、进入 Stage 2、创建其他新 Master、修改 Dashboard、merge PR。

## 12. Mandatory STOP Conditions

以下任一发生即 STOP：需要改变 D-069 Spec；426.5×302 与工程输入冲突；source binding 无法确认；必须强行映射 A/B 到东西缝；需要新历史假设；需要合同外几何；protected hash mismatch；Blender 4.5.13 无法执行；validator 暴露合同层冲突；mutation 污染 canonical；必须修改 Project Control 才能继续。

STOP 只返回 failure item、minimal reproduction、relevant logs、affected files、implementation bug 或 contract/evidence issue 分类；不得自行改合同。

## 13. Git / PR Contract

ONE TASK = ONE BRANCH = ONE PR。

Branch = codex/t021-p3-3-four-chuanfu-master-first-article-v001

建议 commit：T-021: build four-chuanfu Master first article

PR title：T-021｜四椽栿 Master First Article V001

PR body 至少包含 source main SHA、task path、changed files、Actions run ID、artifact ID/SHA-256、validation summary、mutation summary、review paths、protected asset check、known limitations，并明确写 PENDING_CHATGPT_PRODUCT_OWNER_REVIEW / DO NOT MERGE。

执行方不得 merge PR；PR merge 仍需 Product Owner 单独批准。

## 14. Completion Criteria

T-021 engineering COMPLETE 需要 params/semantic/generator、canonical reference Master、Actions Blender 4.5.13、independent reopen、3类mutation+restore、42项validation、6张review PNG、blend artifact+SHA、Stage1 catalog pending record、protected inputs unchanged、branch+PR创建且未merge、Project Control未修改。

执行完成后只汇报：STATUS、branch、commit SHA、PR number/URL、Actions run ID、artifact ID、binary SHA-256、validation PASS count、review paths、protected-assets result、STOP/known issue。

## 15. Authorization Boundary

**TASK CONTRACT ACTIVE / D-070 + D-071 / CHATGPT DIRECT GITHUB EXECUTION AUTHORIZED**

Product Owner 已授权将 T-021 的工程执行责任改为 ChatGPT direct GitHub execution，并可继续执行同一 T-021。

本授权包括：T-021 工程文件的 ChatGPT direct GitHub execution 与 GitHub Actions headless Blender 执行链。仍不包括：T-021 Master 最终批准、PR merge、Stage 1 PASS、第二个新 Master、Stage 2、T-018、P3.3 PASS。

## 16. D-071｜Task-specific Executor Override

D-071 仅修改 **T-021 的工程文件作者/提交路径**：

- 原：Codex Cloud 编写工程文件 → GitHub Actions 执行 Blender；
- 新：ChatGPT direct GitHub execution 编写并提交工程文件 → GitHub Actions 执行 Blender。

以下全部不变：

- D-069 四椽栿 Master Spec；
- 42项验证；
- 3类 mutation；
- 6张 review PNG；
- Blender 4.5.13 pin；
- binary artifact / SHA-256；
- ONE TASK = ONE BRANCH = ONE PR；
- Product Owner merge approval；
- T-018 HOLD；
- evidence / historical / UNKNOWN 边界。

本 override 不创建 T-022，也不改变其他任务默认执行方式。
