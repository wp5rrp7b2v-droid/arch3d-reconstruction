# T-019｜P3.3 上游 Disposition 一致性修正 V001

## Task Contract｜LOCKED / PRODUCT OWNER APPROVED / READY FOR EXECUTION / EXECUTION NOT AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.3｜构件驱动整殿重建
- Task ID：T-019
- Engineering ID：`P3_3_UPSTREAM_DISPOSITION_CONSISTENCY_CORRECTION_V001`
- 中文任务名：上游 Disposition 一致性修正
- Think Level：MEDIUM
- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`
- Primary Engineering Executor：Codex Cloud
- Cloud Mode Classification：`CLOUD_EXECUTABLE`
- Blender Requirement：`NONE`
- Status：**CONTRACT LOCKED / PRODUCT OWNER APPROVED / READY / NOT STARTED / EXECUTION NOT AUTHORIZED**
- Date：2026-09-16
- Gate authority：D-047 / `P3_3_DEFINITION_OF_DONE_V001`
- Upstream baseline：T-017 / D-050
- Blocking downstream task：T-018 / PR #3 / STOP-HOLD
- Contract approval：D-053

> Product Owner 已批准并锁定本 Task Contract，但 **Task Contract 批准不等于工程执行授权**。只有 Product Owner 明确发出“开始执行 T-019”后，才允许进入 Codex Cloud 工程执行、独立 T-019 branch / PR、机器验证与 merge review。

---

## 1. 任务目的

T-019 是一个**最小上游纠错任务**，不是新的建模阶段，也不是 T-018 的替代任务。

T-018 正式审核暴露出一个 T-017 protected-input 冲突：

- P3.1 locked Master Scope 将 `CMP-PURLIN-001｜槫类构件` 定义为 `DEFERRED_INSUFFICIENT_EVIDENCE`；
- 该定义明确指出位置对应截面、构件长度、端部条件以及位置是否属于 variant / separate type 等证据不足；
- 但 T-017 canonical `P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json` 中，7 个 PURLIN legacy instances 被标为 `GENERATE_FROM_FORMAL_COMPONENT`；
- T-018 不允许自行修改 T-017 protected foundation outputs，也不得把 Deferred 构件静默升级为 formal geometry，因此触发 T-018 contract-defined STOP condition。

T-019 的唯一目标是：

> **使 T-017 P3.3 foundation disposition 与 P3.1 locked component qualification 恢复一致，并建立跨层机器回归检查，确保 Deferred / Proxy / Control / Envelope 等资格不会在后续 building accounting 中被静默升级。**

本任务不新增历史证据，不生成 Blender 几何，不重新设计 P3.1 Master Scope，也不处理 T-018 当前的 formal geometry / placement / workflow correction。

---

## 2. Known Conflict｜必须修正的已知对象

### 2.1 P3.1 canonical qualification

`CMP-PURLIN-001`：

- P3.1 eligibility：`DEFERRED_INSUFFICIENT_EVIDENCE`
- historical component type：槫类构件
- evidence gap：position-specific sections / member lengths / end conditions / variant-vs-type qualification 等仍不足
- approved Master：NONE
- 允许状态：保留 identity 与语义，但不得作为 approved formal geometry source

### 2.2 T-017 erroneous downstream disposition

T-017 当前有 **7 个 PURLIN accounting records** 被标为：

`GENERATE_FROM_FORMAL_COMPONENT`

T-019 必须将这 7 条记录的 P3.3 building disposition 改为：

`DEFERRED`

并保持：

- `component_id = CMP-PURLIN-001`
- legacy instance identity 不变
- family / variant / instance accounting 不变
- evidence gap 不被填补
- 不产生 formal geometry readiness claim
- 不把 P2 purlin envelope / transform 重新解释成历史构件几何

---

## 3. Authoritative Inputs｜执行前必须读取

### 3.1 Governance / Gate

1. `docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`
2. `docs/project_control/project_state.json`
3. `docs/project_control/governance.md`
4. `docs/project_control/CLOUD_MODE_2026-09-16_20.md`
5. 本合同 `docs/tasks/T-019_P3_3_UPSTREAM_DISPOSITION_CONSISTENCY_CORRECTION_V001.md`

### 3.2 P3.1 locked qualification｜最高资格判断来源

1. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json`
2. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json`
3. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`
4. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`
5. `production/zhenguo_wanfo/component_library/masters/**`

P3.1 qualification 在本任务中是 **READ-ONLY / CANONICAL / PROTECTED**。

### 3.3 T-017 foundation｜本任务允许修正的上游层

1. `production/zhenguo_wanfo/build/P3_3_BUILDING_INPUT_BASELINE_V001.json`
2. `production/zhenguo_wanfo/build/P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`
3. `production/zhenguo_wanfo/build/P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json`
4. `production/zhenguo_wanfo/build/P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`
5. `production/zhenguo_wanfo/build/P3_3_BUILDING_GRAPH_VALIDATION_V001.json`
6. T-017 builder / validator / tests / README / negative fixtures

### 3.4 Other protected canonical layers

必须保持不变：

- P2 frozen baseline；
- P2.1 formal parameters / approved override；
- P3.0 Registry / Ontology / migration identity；
- P3.1 Scope / Identity / Master Library / approved Masters；
- P3.2 Assembly Schema / Node Registry / Interface Registry / Relationship Types / Representative Assembly；
- P3.3 DoD；
- T-018 engineering files与 PR #3 branch。

---

## 4. Cross-layer Disposition Consistency Rule｜新增长期机器检查

T-019 必须在 T-017 validator / tests 中新增**跨层资格一致性检查**。

### 4.1 Direct-identity matching only

机器映射必须优先使用明确 identity：

- `component_id ↔ candidate_id`
- `component_id ↔ source_registry_id`
- P3.1 Identity Resolution 中的显式映射

不得仅按 `source_family` 做自动升级或降级。

特别是 P3.1 中由 P1 evidence 派生、且明确注明“不替代现有 P3.0 Proxy”的 Master candidate，不得因为 family 相同就把 legacy proxy 自动映射为该 Master。

### 4.2 Qualification → allowed P3.3 disposition

对能够直接解析到 P3.1 qualification 的 identity，至少执行以下约束：

- `MASTER_REQUIRED`：只有在 approved Master / canonical identity 条件满足时，才允许 `GENERATE_FROM_FORMAL_COMPONENT`；
- `DEFERRED_INSUFFICIENT_EVIDENCE`：不得 `GENERATE_FROM_FORMAL_COMPONENT`，building disposition 必须保持 `DEFERRED`；
- `PROXY_ONLY`：不得升级为 formal geometry，保持 `PROXY_ONLY` / equivalent explicit proxy disposition；
- `CONTROL_ONLY`：保持 `CONTROL_ONLY`；
- `ENVELOPE_ONLY`：保持 `ENVELOPE_ONLY`；
- 任何无法安全解析的资格状态：不得静默生成 formal geometry，必须显式报告。

本任务**不得新增第六项 P3.3 Hard Fail**。跨层冲突使用 T-019/T-017 validator 的 consistency error，例如 `MASTER_SCOPE_DISPOSITION_CONFLICT`；P3.3 五项 canonical Hard Fail vocabulary 保持不变。

---

## 5. Allowed Engineering Changes｜最小修改范围

### 5.1 必须更新

- T-017 builder/compiler：使 disposition 派生受 P3.1 direct-identity qualification 约束；
- T-017 validator：加入 cross-layer disposition consistency check；
- T-017 tests：加入 regression case；
- `P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json`：修正 7 个 PURLIN dispositions；
- `P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`：若 graph/runtime node 镜像 disposition，则同步修正；
- `P3_3_BUILDING_GRAPH_VALIDATION_V001.json`：重新生成正式 validation evidence。

### 5.2 原则上必须 byte/content-stable

除非发现机械上必须同步的 metadata，不应修改：

- `P3_3_BUILDING_INPUT_BASELINE_V001.json`
- `P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`

若这两项发生任何 substantive change，STOP 并回报，不得作为普通修正自行扩大范围。

### 5.3 可以新增

允许新增一个轻量 machine-readable consistency report，例如：

`production/zhenguo_wanfo/validation/P3_3_T019_DISPOSITION_CONSISTENCY_V001.json`

如新增，必须只记录 validator 结果，不形成第二套 accounting / identity system。

---

## 6. Required Regression Validation

T-019 至少必须验证：

1. 7/7 PURLIN records 均不再是 `GENERATE_FROM_FORMAL_COMPONENT`；
2. 7/7 PURLIN records 均为 `DEFERRED`；
3. `CMP-PURLIN-001` identity 保留；
4. PURLIN evidence gaps / historical boundary 未被填补或升级；
5. 全量 365 accounting 仍为 365/365；
6. 11/11 families、40/40 variants、365/365 instances coverage 不下降；
7. unexplained omission = 0；
8. orphan / broken identity = 0；
9. P2 numeric world transform authoritative usage = 0；
10. 五类 P3.2 relation vocabulary 不变；
11. canonical P3.3 Hard Fail count = 0；
12. 原 5/5 synthetic negatives 继续 expected rejection；
13. T-017 deterministic regeneration / stable serialization 继续 PASS；
14. cross-layer direct-identity disposition conflict count = 0；
15. synthetic regression：人为把 `CMP-PURLIN-001` 重新改成 `GENERATE_FROM_FORMAL_COMPONENT` 时，validator 必须拒绝并报告 `MASTER_SCOPE_DISPOSITION_CONFLICT` 或等价明确错误。

---

## 7. Acceptance Criteria｜T-019 PASS 条件

T-019 只有在以下全部成立时，才可进入 ChatGPT formal review：

- Known PURLIN correction：7/7；
- Cross-layer direct-identity conflicts：0；
- Accounting：365/365；
- Coverage：11/11 families / 40/40 variants / 365/365 instances；
- unexplained omissions：0；
- orphan / broken identities：0；
- P2 authoritative numeric-transform usage：0；
- canonical P3.3 Hard Fail：0；
- existing 5/5 hard-fail negatives：EXPECTED_REJECTION；
- new disposition-regression negative：EXPECTED_REJECTION；
- deterministic regeneration：PASS；
- stable serialization：PASS；
- P3.1 canonical files / six approved Masters：UNCHANGED；
- P3.2 canonical assembly foundation：UNCHANGED；
- P2 frozen baseline：UNCHANGED；
- T-018 files / PR #3 branch：UNCHANGED；
- Blender invocations：0；
- `.blend` files created：0。

ChatGPT structural review PASS 后，仍需 Product Owner 明确批准 T-019 并授权 merge；未经批准不得 merge。

---

## 8. Explicit Non-goals

T-019 不允许：

- 创建 PURLIN Master；
- 推测或补齐槫的实际截面、长度、端部构造；
- 修改 `CMP-PURLIN-001` 的 P3.1 eligibility；
- 修改任何六个 approved P3.1 Master；
- 修改六椽栿 historical full length 边界；
- 修改 Z-006 / Z-006-RC-01 / DG-114 / HIS-002 等既有边界；
- 修改 P3.2 relationship vocabulary；
- 新增 P3.3 Hard Fail；
- 处理 T-018 generic-cube、placement、PR-head SHA 或 Blender version-check 修正；
- 运行 Blender；
- merge PR #3。

---

## 9. STOP Conditions

出现以下任一情况，Codex 必须 STOP 并回报，不得自行扩大修正：

1. 除已知 7 个 PURLIN 外，发现新的 direct-identity qualification/disposition 冲突；
2. 修正需要修改 P3.1 Scope / Identity / Master Library / approved Master；
3. 修正需要新增历史尺寸、历史构件身份或未批准 reconstruction rule；
4. `P3_3_BUILDING_INPUT_BASELINE_V001.json` 或 `P3_3_BUILDING_PARAMETER_BINDINGS_V001.json` 需要 substantive change；
5. 365 accounting 无法在不删除记录的情况下保持；
6. 需要修改 P3.2 schema / relation vocabulary；
7. 需要修改 T-018 engineering branch / PR #3；
8. machine validator 无法区分 direct identity 与 family-level derived candidates；
9. 任何修正会造成 silent historicization。

---

## 10. Cloud / Branch / PR Rule

执行时继续遵守 RC-014：

`ONE TASK = ONE BRANCH = ONE PR`

T-019 必须使用**独立于 T-018 PR #3** 的 branch / PR。

建议内部任务分支标签：

`codex/t019-p3-3-upstream-disposition-consistency-v001`

正式 GitHub branch identity 以 Codex UI Create PR 后的 GitHub-visible head 为准。

禁止：

- 在 T-018 PR #3 上提交 T-019 correction；
- 直接向 main 提交工程修正；
- 未经 Product Owner 授权 merge。

---

## 11. T-019 完成后的 T-018 恢复条件

T-019 只有在以下流程完成后，T-018 才允许解除 STOP：

`T-019 engineering → GitHub PR → ChatGPT formal review → Product Owner approval/merge authorization → merge into main → verify corrected canonical T-017 outputs on main`

随后：

1. 回到原有 T-018 Codex Cloud task；
2. 更新到最新 canonical `main`；
3. 使用同一 T-018 task 的 Update Branch 更新原 PR #3；
4. 再修正 T-018 已发现的剩余问题：
   - formal component geometry 不得用 generic cube 代替；
   - placement 必须机械来源于 authoritative graph / parameter / rule，而不是 synthetic hard-coded family layout；
   - Actions evidence 必须显式记录 canonical PR head SHA；
   - Blender 4.5.13 version check 必须接受合法 `LTS` suffix，同时仍锁定 4.5.13；
5. 重新运行 GitHub Actions Run A/B/C/D；
6. 返回 ChatGPT 重新审核。

T-019 PASS / merge **不等于** T-018 PASS，也不等于 P3.3 Gate PASS。
