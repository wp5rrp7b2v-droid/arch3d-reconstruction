# 【中国古建筑3D复原｜T-011｜P3_1_COLUMN_MASTER_CONTRACT_PILOT_V001｜柱Master合同实现试点】

Status: **AUTHORIZED / READY_FOR_LOCAL_EXECUTION**  
Think Level: **HIGH**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13

## 1. Objective

在已锁定的 `P3.1 Canonical Master Asset Contract V001`（D-034）基础上，仅对：

> `CMP-COLUMN-001｜柱`

执行一次端到端 Contract Implementation Pilot，验证完整资产链：

> **evidence-aware params → deterministic generator → local-only canonical `.blend` → semantic QC → standard review package → Registry registration → independent reopen / mutation validation**

本任务的目的不是批量生产 P3.1 六类 Master，而是验证“一个正式 Component Master 从合同到可审核数字资产”的完整方法是否成立。

T-011 PASS 后，ChatGPT / Product Owner 再决定是否按同一模式扩展其余五类 Master。

---

## 2. Authoritative Inputs

必须完整读取并遵守：

1. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V001.md`（LOCKED / D-034）；
2. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V001.json`（LOCKED / D-034）；
3. `docs/production/zhenguo_wanfo/P3_1_DEFINITION_OF_DONE_V001.md`（LOCKED / D-032）；
4. `docs/production/zhenguo_wanfo/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md/json`；
5. `docs/production/zhenguo_wanfo/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md/json`；
6. P3.0 Ontology / Registry / Schema / Migration Audit；
7. P1 approved evidence package；
8. P2 frozen parameter / dependency / integration baseline；
9. `docs/project_control/project_state.json`、`decision_log.md`、`acceptance_matrix.md`、`governance.md`、`rules_change_log.md`；
10. D-023、D-028～D-034 与 CG-02～CG-06；
11. `RC-008｜LOCAL BLENDER EXECUTION RULE`。

如果任何执行细节与已锁定 Asset Contract 或 Governance 冲突，以 Asset Contract + Project Control 为准，不自行放宽。

---

## 3. Pilot Scope

### 唯一允许生产的历史 Component Master

`CMP-COLUMN-001｜柱`

### Pilot canonical reference realization

用于本次正式审核的参考实现：

- `diameter_mm = 460.0`
- `diameter_source_mode = OBSERVED_Z001`
- `height_mm = 3534.3`
- `height_source_mode = RC_Z006_RC_01`

语义必须明确：

- `460mm` = 当前正式证据中的 observed diameter reference；
- `3534.3mm` = D-023 批准的 `Z-006-RC-01` 可替换生产候选；
- `Z-006` 本体仍为 `UNKNOWN / null / DO_NOT_LOCK`；
- 本次 `.blend` 只是基于当前参数输入生成的 canonical reference realization，不得被描述为已证实的 963 原柱精确模型。

### Geometry mode

`PARAMETRIC_CIRCULAR_COLUMN_BODY`

只允许生成圆柱主体外轮廓。

不得添加：

- 收分；
- 卷杀 / entasis；
- 侧脚；
- 柱础；
- 柱头细部；
- 榫卯；
- 角柱生起；
- 无证据纹理、材质细节或风化。

---

## 4. Canonical Geometry Contract

必须严格满足：

- unit = mm；
- right-handed local coordinates；
- `+Z` = 柱身纵轴 / gravity up；
- origin = 柱身底面中心；
- Location = `(0,0,0)`；
- Rotation = `(0,0,0)`；
- Scale = `(1,1,1)`；
- 正式尺寸只能来自参数生成，不得通过 Object Scale 实现；
- Master 不得包含万佛殿 world position、grid / bay index、instance rotation。

推荐 root collection：

`MASTER__CMP_COLUMN_001`

推荐主体对象：

`MASTER__CMP_COLUMN_001__BODY`

允许存在用于审核/metadata 的非 mesh 辅助对象，但必须在 semantic snapshot 中明确分类，且不得污染主体 bounding box / historical geometry interpretation。

---

## 5. Required Production Assets

至少生成以下 committed source / metadata：

### A. Parameter file

`production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_PARAMS_V001.json`

必须包含 Asset Contract 规定的 common parameter fields，并显式记录：

- component_id；
- master_version；
- unit；
- coordinate / origin convention；
- diameter / height parameter；
- classification / time_layer / source_layer / production_use / source_ids / replaceable；
- `Z-006` unknown boundary；
- `Z-006-RC-01` approval / formula / replaceability；
- geometry_mode；
- known_unknowns；
- interpretation_boundary；
- originality_status；
- reuse_scope；
- variant_axes；
- placement_only_attributes；
- generator_path；
- canonical binary path；
- review paths。

### B. Deterministic Blender generator

建议：

`production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/build_column_master_v001.py`

要求：

- Blender 3.6.23 可执行；
- 参数来自 JSON；
- 禁止裸写历史尺寸常量驱动正式 geometry；
- 构建结果语义 deterministic；
- 可被 independent rebuild / reopen validation 调用。

### C. Local-only canonical Blender asset

`production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/asset/CMP-COLUMN-001_MASTER_V001.blend`

规则：

- `.blend / .blend1` local-only，不进入普通 Git；
- 必须记录 SHA256；
- 必须 independent reopen PASS；
- 必须与 semantic snapshot 对应。

### D. Semantic snapshot

`production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_SEMANTIC_V001.json`

至少包括：

- object / collection names；
- object count / mesh count；
- local transforms；
- bounding box；
- resolved parameters；
- evidence classes；
- geometry mode；
- known unknowns；
- generator version；
- input hashes；
- Blender version；
- canonical `.blend` SHA256；
- semantic geometry signature。

### E. Pilot Registry registration

建立 P3.1 Registry extension / pilot registration，至少可登记：

- component_id；
- master_id / version；
- canonical asset status；
- generator / parameter / semantic / local binary / review paths；
- geometry mode；
- reuse scope；
- evidence references；
- originality status；
- known unknowns；
- validation status；
- approval status。

推荐：

`production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`

在本 Pilot 中只登记 `CMP-COLUMN-001`，不得伪造其余五类为已完成。

---

## 6. Standard Review Package

至少生成并提交以下审核 PNG：

目录：

`production/zhenguo_wanfo/review/P3_1/masters/CMP-COLUMN-001/`

最低 6 项：

1. `FRONT`
2. `SIDE`
3. `TOP`
4. `AXON`
5. `DIMENSION_PARAMETER_SUMMARY`
6. `EVIDENCE_UNCERTAINTY_SUMMARY`

要求：

- neutral grey geometry；
- FRONT / SIDE / TOP 优先 orthographic；
- AXON 清晰展示柱体比例；
- 不使用影视材质、纹理、风化和戏剧灯光；
- 图中或 companion metadata 明确 `CMP-COLUMN-001 / MASTER V001`；
- 尺寸摘要必须同时显示 diameter 与 height；
- evidence 摘要必须明确：diameter = observed reference；height = RC-01 replaceable；Z-006 = UNKNOWN；HIS-002 = originality unknown；
- 不得把 3534.3mm 写成已证实历史柱高。

如果现有项目已有稳定 review renderer，可复用；不得为了视觉效果改变 canonical Master geometry。

---

## 7. Mutation / Variant Validation

Pilot 必须至少执行一次 synthetic parameter mutation，证明生成链是真参数驱动，不是静态复制。

建议测试：

- baseline reference：`diameter=460.0 / height=3534.3`
- synthetic mutation：改变 `height_mm` 或 `diameter_mm` 至一个明确标记为 `ENGINEERING_TEST_ONLY` 的值。

要求：

- mutation 必须导致预期 bounding box / semantic signature 变化；
- 未改变的参数语义不得漂移；
- mutation 不得覆盖 canonical reference asset；
- synthetic mutation 不进入万佛殿历史 Variant 清单；
- 不得把测试值写入正式历史 evidence parameter；
- 测试结束后 canonical reference rebuild 必须恢复并 PASS。

本任务可验证 Variant architecture，但**不要求建立正式历史 Variant Library**。

---

## 8. Machine Validation Requirements

至少验证：

1. component_id / master_id 唯一；
2. required Asset Contract fields 完整；
3. unit = mm；
4. origin / axes / transform contract PASS；
5. canonical body Scale = 1；
6. no world placement leakage；
7. no naked historical constants；
8. bounding box 与 resolved diameter / height 一致，使用合理数值容差；
9. `Z-006` 仍 UNKNOWN；
10. `Z-006-RC-01` 仍独立 replaceable RC；
11. `HIS-002` originality unknown；
12. unsupported column geometry count = 0；
13. semantic deterministic regeneration PASS；
14. independent reopen PASS；
15. synthetic mutation PASS；
16. canonical rebuild after mutation PASS；
17. committed Registry registration 无 orphan；
18. P2 frozen baseline hashes unchanged。

建议形成：

- `production/zhenguo_wanfo/validation/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json`
- `docs/production/zhenguo_wanfo/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.md`

若 validation 发现 Asset Contract 本身在真实 Blender 实现中存在无法满足或相互矛盾之处：

- 不得自行修改 LOCKED Contract；
- 标记 `REQUIRES_PROJECT_CONTROL_REVIEW`；
- T-011 状态应 HOLD / BLOCKED，由 ChatGPT / Product Owner 决定是否需要 Contract V002。

---

## 9. P2 Frozen Baseline Protection

T-011 不得修改：

- P2 canonical `.blend`；
- P2 formal production parameter set；
- P2 approved overrides；
- P2 dependency matrix；
- P2 integration manifest；
- P2 review evidence。

执行前后必须核验关键 frozen baseline hashes；任何变化均为 HARD FAIL，除非另有 Product Owner 正式决策。

---

## 10. Hard Fail Conditions

出现任一项，本任务不得报告 COMPLETE / PASS：

- 把 Z-006-RC-01 当成已证实 963 柱高；
- 静默为 Z-006 填值；
- RC/HCI 升级为 CONFIRMED；
- 添加无证据收分、卷杀、侧脚、柱础、柱头、榫卯或角柱生起；
- 通过 Object Scale 产生正式尺寸；
- Master 带入 world placement / grid position；
- generator 依赖不可追溯历史尺寸裸常量；
- `.blend` 被错误提交 Git；
- synthetic mutation 污染 canonical asset 或历史参数；
- Registry 将其他五个 Master 错记为已生产；
- P2 frozen baseline 被覆盖；
- LOCKED Asset Contract 被本任务自行修改。

---

## 11. Completion Criteria

T-011 COMPLETE 至少要求：

- `CMP-COLUMN-001` canonical parameter contract：PASS；
- deterministic generator：PASS；
- local-only canonical `.blend`：GENERATED；
- canonical `.blend` SHA256：RECORDED；
- semantic snapshot：PASS；
- standard review package：6 / 6 GENERATED；
- Asset Contract validation：PASS；
- synthetic parameter mutation：PASS；
- canonical rebuild after mutation：PASS；
- independent reopen：PASS；
- Registry pilot registration：PASS；
- evidence / historical boundary preservation：PASS；
- P2 frozen baseline：UNCHANGED；
- unexplained validation errors：0。

T-011 COMPLETE 不等于：

- `CMP-COLUMN-001` Product Owner 最终视觉批准；
- 其余五个 Master 获得生产授权；
- P3.1 PASS。

完成后必须由 ChatGPT 先审核工程结果与 review package，再由 Product Owner 决定 Pilot 是否 APPROVED，以及是否进入 remaining-five Master production。

---

## 12. Local Execution / Git Rules

执行前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git status
git pull --ff-only origin main
```

本仓库已配置 repository-local Git proxy；正常 `git pull / push` 即可。网络 443 失败先按网络/代理问题处理，不得误判为分支冲突，也不得 force/reset/overwrite。

### 12.1 Local Blender Execution｜RC-008

本任务的自动 Blender 工程**不得通过 GUI 启动链路执行**。

固定 executable：

```bash
/Applications/Blender.app/Contents/MacOS/Blender
```

正式自动执行必须优先采用：

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python <script.py>
```

强制规则：

- 禁止使用 `open -a Blender` 作为本任务的自动执行方式；
- 禁止依赖 Finder、AppleScript 或人工点击打开 Blender 后再继续自动化；
- 不自动下载安装或切换其他 Blender 版本；
- 执行前先记录 executable 实际版本，预期为 Blender 3.6.23 / Intel x64；
- 若路径不存在、版本不符或 CLI/background 失败，STOP 并报告，不静默换版本；
- GUI / LaunchServices 报错本身不构成 Blender runtime blocker；只有指定 executable 的 CLI/background 也失败时，才报告 Blender runtime blocker；
- review PNG、保存 `.blend`、independent reopen 与可自动化 QC 均应通过 background/CLI 完成；
- Product Owner 需要人工视觉检查时，再单独手动查看正式 review PNG 或打开 `.blend`，不作为 Codex 自动执行前置步骤。

若出现：

- unknown tracked changes；
- non-fast-forward；
- Project Control 同文件冲突；

立即停止并报告。

T-011 执行期间不得修改 `docs/project_control/`；Project Control 由 ChatGPT 维护。

完成后：

- 运行全部 validation；
- `git status` 确认只包含 T-011 授权的 committed text/script/JSON/review PNG；
- 确认 `.blend / .blend1` 未进入 Git；
- commit message 建议：`p3.1: implement column master contract pilot v001`；
- push `main`；
- 回传严格 Completion Report。

---

## 13. Completion Report Format

必须严格回报：

- STATUS: COMPLETE / BLOCKED / FAILED
- COMPONENT_ID: `CMP-COLUMN-001`
- MASTER_VERSION: `V001`
- BLENDER_VERSION:
- BLENDER_EXECUTION_MODE: CLI_BACKGROUND / OTHER
- BLENDER_EXECUTABLE_PATH:
- CANONICAL_PARAMS: diameter / height + source modes
- CANONICAL_BLEND_PATH:
- CANONICAL_BLEND_SHA256:
- SEMANTIC_SNAPSHOT: PASS / FAIL
- REVIEW_PACKAGE: x/6
- CONTRACT_VALIDATION: PASS / FAIL
- TRANSFORM_VALIDATION: PASS / FAIL
- EVIDENCE_BOUNDARY_VALIDATION: PASS / FAIL
- NAKED_HISTORICAL_CONSTANT_SCAN: PASS / FAIL
- DETERMINISTIC_REGENERATION: PASS / FAIL
- INDEPENDENT_REOPEN: PASS / FAIL
- SYNTHETIC_MUTATION: PASS / FAIL
- CANONICAL_REBUILD_AFTER_MUTATION: PASS / FAIL
- REGISTRY_REGISTRATION: PASS / FAIL
- P2_FROZEN_BASELINE: UNCHANGED / CHANGED
- REQUIRES_PROJECT_CONTROL_REVIEW: NONE / [items]
- FILES_CREATED / UPDATED:
- COMMIT_SHA:
- UNRESOLVED / BLOCKERS:

---

## 14. Authorization Boundary

本 Task Contract 正式授权 T-011 **仅实现 `CMP-COLUMN-001` 柱 Master Pilot**。

不得顺带生产：

- 柱头栌斗；
- 单向长开斗；
- 交互斗；
- 下六椽栿；
- 上六椽栿；
- 任意 Deferred / Proxy / Control / Envelope 对象。

Pilot 未经 ChatGPT / Product Owner 审核通过前，remaining-five batch production 继续保持未授权。
