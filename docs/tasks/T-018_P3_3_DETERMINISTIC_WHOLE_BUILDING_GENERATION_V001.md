# T-018｜P3.3 整殿确定性生成与参数变更验证 V001

## Task Contract｜LOCKED / PRODUCT OWNER APPROVED / READY FOR EXECUTION / EXECUTION NOT AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.3｜构件驱动整殿重建
- Task ID：T-018
- Engineering ID：`P3_3_DETERMINISTIC_WHOLE_BUILDING_GENERATION_V001`
- 中文任务名：整殿确定性生成与参数变更验证
- Think Level：HIGH
- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`
- Primary Engineering Executor：Codex Cloud
- Blender Executor：GitHub Actions Hosted Runner
- Cloud Mode Classification：`CLOUD_EXECUTABLE / D-048 EQUIVALENT HEADLESS EXECUTION`
- Blender Requirement：`HEADLESS / SCRIPTED / DETERMINISTIC`
- Blender Version：`4.5.13 linux-x64`
- GitHub Runner：`ubuntu-latest`
- Status：**CONTRACT LOCKED / PRODUCT OWNER APPROVED / READY / NOT STARTED / EXECUTION NOT AUTHORIZED**
- Date：2026-09-16
- Gate authority：D-047 / `P3_3_DEFINITION_OF_DONE_V001`
- Execution-environment authority：D-048 / RC-017
- Foundation task：T-017 / D-050

> Product Owner 已批准并锁定本 Task Contract，但 **Task Contract 批准不等于工程执行授权**。只有 Product Owner 明确发出“开始执行 T-018”后，才允许进入 Codex Cloud 工程执行、GitHub PR 和 GitHub Actions headless Blender 运行。

---

## 1. 任务目的

T-018 是 P3.3 在 T-017 机器输入基础之后的第一项正式整殿生成工程。

T-017 已经证明：

- 正式输入边界可锁定；
- 365/365 legacy instances 可完整 accounting；
- Building Assembly Graph 可从 Registry / P3.2 / building parameters 建立；
- P2 numeric world transform 可以被禁止进入 P3.3 generative path；
- 五项 P3.3 Hard Fail 可在基础层稳定触发。

T-018 的目标是进一步证明：

> **从干净 Blender 状态开始，只依靠 T-017 正式输入体系、P3.0/P3.1 identity & Master、P3.2 relationship foundation 与正式 building parameters，即可确定性生成一份 evidence-aware 的整殿候选，并能够完成机器空间验证、参数 mutation → rebuild → validate → restore。**

本任务不追求“把未知内容补齐成完整历史几何”。

对于 `UNKNOWN_BLOCKED / DEFERRED / SEMANTIC_ONLY / Proxy / Control / Envelope`：

- 必须保留正式 runtime disposition；
- 允许生成明确标注的工程 proxy/control/envelope 或 semantic marker；
- 不得为了画面完整强行生成 historical component geometry；
- 六椽栿 historical full length 继续 `UNKNOWN / null`，`canonical_reference_length_mm=1000` 不得进入实际建筑梁长。

---

## 2. Locked Scope｜本任务覆盖的 P3.3 DoD

T-018 正式覆盖：

### DoD-05｜确定性整殿生成

建立并实际执行 clean-state whole-building generator：

`formal inputs → building graph → runtime realization → Blender scene → save → independent reopen → machine validation`

### DoD-06｜空间、几何与结构一致性｜T-018 范围

完成可脚本化和可正式审核图验证的部分：

- 柱网与主要开间/进深关系；
- 主要标高；
- 梁架层级/组织层；
- 建筑轮廓与 roof/control/envelope 关系；
- 构件重复关系；
- formal runtime identity 与 parent/organization；
- 与正式参数/approved reconstruction rule 的 machine-traceable consistency。

若出现必须手动旋转、遮挡剖切、交互式拓扑判断才能确定的正式问题，则该项转 `LOCAL_MAC_REQUIRED / PENDING`，不得在本任务中伪判 PASS。

### DoD-07｜Evidence Boundary 保持｜生成层验证

验证 evidence status 在 Blender runtime objects、manifest 与审核资产中不丢失、不升级。

### DoD-08｜机器验证、Hard Fail 与参数 Mutation｜实际执行部分

完成：

- runtime identity / omission / relation / parameter / evidence / prohibited-transform checks；
- 5 项 P3.3 Hard Fail 在整殿生成层的 synthetic negative / mutation rejection；
- 一次正式 building parameter mutation → rebuild → validation → canonical restore。

T-018 **不关闭**：

- DoD-09 最终 Gate Evidence Package；
- 最终独立 Gate Review；
- 真正需要 Local Mac 的交互式最终检查；
- P3.3 Gate PASS。

因此 T-018 即使 PASS，P3.3 仍保持 ACTIVE。

---

## 3. Authoritative Inputs｜执行前必须读取

### 3.1 Gate / Governance

1. `docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`
2. `docs/project_control/project_state.json`
3. `docs/project_control/governance.md`
4. `docs/project_control/CLOUD_MODE_2026-09-16_20.md`
5. `docs/project_control/rules_change_log.md`
6. 本合同 `docs/tasks/T-018_P3_3_DETERMINISTIC_WHOLE_BUILDING_GENERATION_V001.md`

### 3.2 T-017 P3.3 Foundation｜直接 authoritative

1. `production/zhenguo_wanfo/build/P3_3_BUILDING_INPUT_BASELINE_V001.json`
2. `production/zhenguo_wanfo/build/P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`
3. `production/zhenguo_wanfo/build/P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json`
4. `production/zhenguo_wanfo/build/P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`
5. `production/zhenguo_wanfo/build/P3_3_BUILDING_GRAPH_VALIDATION_V001.json`
6. T-017 builder / validator / tests / Hard Fail fixtures

T-018 不得另建第二套 building identity、第二套 accounting 或第二套关系语义。

### 3.3 P3.0 / P3.1 / P3.2

继续继承并保护：

- P3.0 Ontology / Registry / migration identity；
- P3.1 Component Master Library / Master Asset Contract / approved Master params & semantic snapshots；
- P3.2 Assembly Schema / Node Registry / Interface Registry / Representative Assembly / Relationship Graph / validators；
- 五类基础关系仅允许 `SUPPORT / CONNECT / LOCATE / REPEAT / BELONG`。

### 3.4 Building Parameters / Evidence

继续使用：

- `P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
- `P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
- `P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
- evidence-aware schema / source records

不得在 T-018 源码中用 naked historical constants 替代已有 parameter ids。

### 3.5 P2 Frozen Baseline｜只允许 comparison / diagnostic

允许：

- family / variant / instance coverage 对照；
- evidence metadata 对照；
- 最终 diagnostic comparison（如果明确标记 `COMPARISON_ONLY`）。

严格禁止作为生成输入：

- P2 `.blend`；
- P2 scene objects；
- P2 `transform.location_mm`；
- P2 `transform.rotation_euler_rad`；
- P2 `transform.scale`；
- 任何 pre-positioned / baked whole-building placement。

---

## 4. 正式执行环境｜RC-017 Locked

### 4.1 Codex Cloud

只负责：

- generator / validator / renderer / tests；
- GitHub Actions workflow；
- machine-readable manifests；
- 代码级 deterministic checks；
- PR 工程提交。

Codex Cloud 本身 **不是 Blender runtime**。

### 4.2 GitHub Actions

正式 runner：

`ubuntu-latest`

正式 Blender：

`Blender 4.5.13 linux-x64`

安装路线复用已验证 P0.2 / P2.3 路线：

`https://download.blender.org/release/Blender4.5/blender-4.5.13-linux-x64.tar.xz`

不得静默升级/降级 Blender 版本。

### 4.3 Clean-state rule

Workflow 必须从 task PR head 的 clean checkout 开始。

Whole-building generation 必须从空白/新建 Blender scene 构造正式 runtime objects；不得加载 P2 whole-building `.blend` 作为场景基础。

### 4.4 Branch / PR publication rule

继续遵守 RC-014：

`ONE TASK = ONE BRANCH = ONE PR`

由于 Codex Cloud 平台可能将内部 branch 映射为不同 GitHub-visible head branch：

- **ChatGPT 不预创建 T-018 GitHub branch**；
- Codex Cloud 完成首个工程 commit 后，通过 UI **Create PR** 正式发布；
- GitHub-visible PR head branch 成为该任务 canonical branch identity；
- 后续 correction 必须使用同一任务 UI 的 **Update Branch** 更新同一个 PR；
- `make_pr` 文本 handoff 不得被当成“已经 GitHub-visible”。

建议内部任务分支标签：

`codex/t018-p3-3-deterministic-whole-building-generation-v001`

但正式事实以最终 GitHub PR head 为准。

---

## 5. Whole-building Runtime Realization Rules

T-018 必须把 T-017 的 365/365 accounting 全量映射为 runtime realization outcome。

每个 accounting record 必须得到且只能得到一种明确结果，例如：

- `GENERATED_FORMAL_GEOMETRY`
- `GENERATED_PROXY`
- `GENERATED_CONTROL`
- `GENERATED_ENVELOPE`
- `SEMANTIC_ONLY`
- `DEFERRED`
- `UNKNOWN_BLOCKED`
- `COMPARISON_ONLY`

要求：

- input accounting = `365 / 365`；
- runtime outcome accounting = `365 / 365`；
- unexplained runtime omission = `0`；
- anonymous formal mesh = `0`；
- broken component identity = `0`。

正式生成对象必须至少带有机器可读 metadata：

- `runtime_instance_id`
- `legacy_instance_id`
- `component_id` / explicit non-component identity
- `graph_parent_node_id`
- `p3_3_disposition`
- `evidence status`
- `parameter / rule provenance`
- `historical_claim_boundary`

Technical camera/light/review helpers 不计入 historical component count，并须标记 technical role。

---

## 6. Unknown / Blocked Geometry Policy

T-018 不允许因为 whole-building scene 需要“看起来完整”而补造未知历史尺寸。

### 六椽栿

- historical full length：`UNKNOWN / null`
- `canonical_reference_length_mm=1000`：`NON_HISTORICAL_ENGINEERING_REFERENCE_ONLY`
- 禁止使用 1000mm 作为万佛殿实际六椽栿长度；
- 在缺少 independently approved building-specific full length 时，不生成伪历史全长六椽栿；
- 应使用 `UNKNOWN_BLOCKED / SEMANTIC_ONLY` runtime representation，或明确的非历史 diagnostic marker；
- 不得因此从 365 accounting 中消失。

### 其他边界

继续保持：

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`
- `Z-006-RC-01 = REASONABLE_COMPLETION / replaceable / D-023`
- `DG-114 = UNKNOWN`
- `HIS-002 = originality unknown`
- 45°转角 / 榫卯 / hidden-angle beam / hidden connections = unresolved / bounded

如果 generator 只有通过编造上述信息才能继续，则 STOP。

---

## 7. Required Engineering Files

### 7.1 Workflow

必须新增：

`.github/workflows/p3_3_t018_whole_building.yml`

Workflow 必须：

1. checkout 当前 task branch / PR head；
2. 安装并验证 Blender 4.5.13；
3. 从 clean state 运行 canonical whole-building generator；
4. 保存 canonical `.blend`；
5. 独立 Blender invocation reopen；
6. 运行 machine validation；
7. 渲染正式 review PNG；
8. 执行 mutation build；
9. validation；
10. canonical restore clean rebuild；
11. 再次 validation；
12. 上传 artifact；
13. 形成持久 JSON/PNG evidence。

正式执行不得在 `main` 直接写工程结果；必须在 task PR branch 内完成。

### 7.2 Generator / Validator / Renderer

至少：

- `production/zhenguo_wanfo/scripts/build_p3_3_whole_building_v001.py`
- `production/zhenguo_wanfo/scripts/validate_p3_3_whole_building_v001.py`
- `production/zhenguo_wanfo/scripts/render_p3_3_whole_building_review_v001.py`

可以合理拆分 utility，但不得形成无法追溯的手工 Blender 操作链。

### 7.3 Tests

至少：

`production/zhenguo_wanfo/tests/test_p3_3_whole_building_v001.py`

必须覆盖：

- clean-state input contract；
- 365 runtime disposition completeness；
- identity metadata；
- relation vocabulary；
- prohibited-transform scan；
- evidence boundary；
- five Hard Fails；
- mutation propagation；
- canonical restore；
- deterministic semantic snapshot。

---

## 8. Required Canonical Outputs

### O-01｜Runtime Manifest

`production/zhenguo_wanfo/build/P3_3_WHOLE_BUILDING_RUNTIME_MANIFEST_V001.json`

至少记录：

- workflow / Blender version；
- formal input hashes；
- runtime object/disposition counts；
- 365/365 mapping；
- identity / parent / parameter / evidence provenance；
- blocked/deferred/semantic-only records；
- technical helper counts；
- output `.blend` artifact identity / SHA256；
- canonical semantic snapshot hash。

### O-02｜Whole-building Validation

`production/zhenguo_wanfo/validation/P3_3_WHOLE_BUILDING_VALIDATION_V001.json`

必须机械计算：

- clean-state generation status；
- save/reopen status；
- runtime accounting；
- identity integrity；
- parameter propagation；
- spatial consistency；
- P3.2 traceability；
- evidence-boundary status；
- prohibited P2-transform usage；
- canonical Hard Fail count；
- negative-fixture results；
- deterministic semantic snapshot status。

### O-03｜Building Mutation Report

`production/zhenguo_wanfo/validation/P3_3_WHOLE_BUILDING_MUTATION_V001.json`

正式 mutation：

- parameter：`PM-005`
- canonical value：`3505.7 mm`
- test-only mutated value：`3605.7 mm`
- delta：`+100.0 mm`

Mutation 只在 runtime/test copy 中发生，不得修改 canonical parameter source file。

必须验证：

1. 所有声明依赖 PM-005 的柱网/重复关系按规则响应；
2. 非依赖对象不出现无解释漂移；
3. evidence classification 不变化；
4. 不把 mutated value 写回历史/正式 source；
5. restore 后 canonical clean rebuild 的 semantic snapshot 与 mutation 前 canonical snapshot 一致。

### O-04｜Evidence Manifest

`production/zhenguo_wanfo/review/P3_3_T018/P3_3_T018_EVIDENCE_MANIFEST_V001.json`

必须记录：

- GitHub Actions run id / run attempt；
- task PR head SHA；
- Blender version；
- artifact name/id（可取得时）；
- canonical `.blend` SHA256；
- review image paths / hashes；
- validation / mutation report hashes；
- canonical semantic snapshot hash；
- whether local-only evidence remains required。

### O-05｜Formal Review Images

至少四张：

- `P3_3_T018_PLAN_V001.png`
- `P3_3_T018_FRONT_ELEVATION_V001.png`
- `P3_3_T018_SIDE_ELEVATION_V001.png`
- `P3_3_T018_AXON_V001.png`

审核图要求：

- 摄影机/投影/裁切由脚本固定；
- 中文构件/系统名优先；
- 明确区分正式生成构件与 Proxy / Control / Envelope / UNKNOWN_BLOCKED；
- 不用材质美化掩盖结构问题；
- 必须能支持 ChatGPT RC-015 直接视觉审核。

---

## 9. GitHub Actions Artifact

Workflow 必须上传至少一个正式 artifact：

`P3_3_T018_HEADLESS_EVIDENCE_V001`

至少包含：

- canonical `.blend`
- canonical reopen validation
- canonical semantic snapshot
- mutation semantic snapshot / report
- restored canonical semantic snapshot
- Blender version record
- workflow execution logs / machine reports
- review PNG copies

`.blend` 默认作为 GitHub Actions artifact 保存，**不进入普通 Git 历史**，除非后续另有 Product Owner 批准。

Artifact retention 应设为足以完成正式审核的合理期限；不得把 artifact-only binary 当成历史事实源。

---

## 10. Spatial / Geometry Machine Checks

至少检查：

### 10.1 柱网 / 平面

- bay/depth/grid 参数到 runtime placement 的传递；
- column/control/grid organization 关系；
- repeat quantity / spacing；
- 关键平面尺寸偏差。

### 10.2 标高 / 梁架层级

- approved elevation / RC parameter 的显式来源；
- frame system 层级顺序；
- 不允许用视觉近似修正 machine mismatch。

### 10.3 Building envelope / control

- roof/gable/control/envelope 与正式 building organization 的 parent / role；
- envelope/control 不得历史化为正式 historical component。

### 10.4 Tolerance

- parameter-driven linear placement validation：默认 `<= 0.01 mm`，除非某参数的正式 schema 定义更宽 tolerance；
- rotation validation：默认 `<= 1e-6 rad`；
- scale validation：默认 `<= 1e-6`；
- semantic manifest / canonical JSON stable serialization：必须 exact deterministic；
- `.blend` binary SHA **不要求跨 clean rebuild 完全相同**；确定性判断以 normalized semantic/geometry snapshot、正式机器指标和 stable JSON 为准。

任何 tolerance override 必须来自正式 schema / approved rule，并记录 provenance。

---

## 11. P3.3 Hard Fail｜T-018 Runtime Layer

T-018 必须在 whole-building/runtime 层验证五项 Hard Fail：

### HF-01 `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`

向六椽栿 runtime actual/full-length geometry path 注入 `canonical_reference_length_mm=1000`。

Expected：REJECT。

### HF-02 `SILENT_HISTORICIZATION`

把 `UNKNOWN_BLOCKED / Proxy / Control / Envelope / Deferred / REASONABLE_COMPLETION` runtime node 静默标记为 confirmed historical geometry。

Expected：REJECT。

### HF-03 `BAKED_MANUAL_BUILDING`

向 runtime placement 注入 P2 numeric world transform / pre-positioned scene object dependency。

Expected：REJECT。

### HF-04 `SILENT_BUILDING_OMISSION`

从 365 runtime outcome mapping 中删除一个正式 accounting record，且没有 explicit disposition。

Expected：REJECT。

### HF-05 `BROKEN_COMPONENT_IDENTITY`

从一个正式 generated runtime object 移除/破坏 Registry component identity / parent / provenance。

Expected：REJECT。

要求：

- canonical Hard Fail count = `0`；
- 5/5 negative fixtures = `EXPECTED REJECTION`。

---

## 12. Deterministic Generation / Reopen / Restore

T-018 必须至少完成以下正式链路：

### Run A｜Canonical Build

clean checkout → blank Blender → canonical build → save → semantic snapshot → review render → validation

### Run B｜Independent Reopen

新的 Blender process 打开 Run A `.blend` → validation → normalized snapshot compare

### Run C｜Mutation Build

runtime/test copy `PM-005: 3505.7 → 3605.7 mm` → clean rebuild → validation → mutation report

### Run D｜Canonical Restore

丢弃 mutation runtime copy → 从正式 canonical inputs 再次 clean rebuild → validation → normalized snapshot compare with Run A

PASS 要求：

- Run A PASS；
- Run B PASS；
- Run C mutation response PASS；
- Run D restore PASS；
- Run D normalized canonical snapshot == Run A normalized canonical snapshot；
- canonical sources untouched。

---

## 13. Required Visual Review｜RC-015

T-018 engineering execution完成后，ChatGPT 必须实际打开正式四张 review PNG。

视觉审核至少判断：

1. 柱网整体是否出现明显错位/漂浮/重叠；
2. 梁架层级是否与组织规则一致；
3. 屋面/山面 control/envelope 是否与主体空间关系合理；
4. 重复构件是否出现明显 instance drift；
5. `UNKNOWN_BLOCKED / Proxy / Control / Envelope` 是否在视觉表达上被误装成历史确定构件；
6. 画面是否存在 machine validator 未捕捉的重大空间异常。

ChatGPT visual review PASS 之后，仍需 Product Owner 批准 T-018 才能关闭任务。

若 review PNG 不足以判断关键几何问题，必须 HOLD 并说明是否需要额外 scripted review view 或真正 `LOCAL_MAC_REQUIRED` 交互检查。

---

## 14. Acceptance Criteria｜T-018 PASS

T-018 工程结果必须同时满足：

1. required engineering files / outputs 全部存在；
2. GitHub Actions 使用 `ubuntu-latest + Blender 4.5.13` 成功执行；
3. clean-state canonical generation PASS；
4. independent reopen PASS；
5. runtime outcome accounting = `365 / 365`；
6. unexplained runtime omission = `0`；
7. anonymous formal mesh = `0`；
8. broken identity = `0`；
9. P2 world transform authoritative usage = `0`；
10. relation vocabulary 仍为 locked 5 types；
11. evidence boundary PASS；
12. canonical Hard Fail count = `0`；
13. runtime negative fixtures `5 / 5 EXPECTED REJECTION`；
14. spatial/parameter machine validation PASS；
15. PM-005 mutation propagation PASS；
16. canonical restore PASS；
17. normalized deterministic canonical snapshot PASS；
18. protected T-017 / P3.0 / P3.1 / P3.2 / P2 formal inputs unchanged；
19. formal review PNG `4 / 4` produced and ChatGPT actual visual review PASS；
20. Product Owner APPROVAL。

T-018 PASS **不等于** P3.3 Gate PASS。

---

## 15. Explicit Non-goals

T-018 不做：

- P3.3 final Gate Evidence Package；
- P3.3 Gate closure；
- 完全还原 963 原貌的声明；
- 历史六椽栿 full length 补值；
- 新增第六种关系；
- 证明所有榫卯/隐蔽连接真实历史做法；
- 结构力学分析；
- 高精度材质/纹理/灯光；
- 影视级渲染；
- 必须依赖 GUI 的人工逐件摆放；
- P2 whole-building `.blend` 复用；
- 把 P2 world transform 反推包装成“新规则”。

---

## 16. Protected Inputs｜禁止修改

除非 STOP 并回到 ChatGPT / Product Owner 决策，T-018 不得修改：

- P2 frozen baseline 与 P2.3 canonical outputs；
- P2.1 formal parameter sources / approved overrides；
- P3.0 canonical Ontology / Registry identities；
- P3.1 approved Master qualification / canonical params / semantic snapshots；
- P3.2 schema / five relation definitions / canonical assembly foundation；
- T-017 five canonical foundation outputs；
- P3.3 DoD V001；
- Project Control files（Codex 不直接改；由 ChatGPT维护）。

如果发现上述正式输入本身必须修改才能完成 T-018，立即 STOP。

---

## 17. STOP Conditions

出现以下任一情况，停止工程，不自行降级或绕过：

1. generator 必须读取 P2 world transform 才能建立主要整殿位置；
2. 必须使用 P2 whole-building `.blend` 才能生成；
3. 必须把六椽栿 1000mm reference 当实际 full length；
4. 必须补造 Z-006 / DG-114 / HIS-002 / hidden connection 等历史事实；
5. 必须新增第六类关系；
6. T-017 365 accounting 与 runtime generation 出现无法解释的 identity conflict；
7. approved Master generator / parameter contract 与 building-level placement rule 冲突；
8. GitHub Actions 无法固定 Blender 4.5.13 或执行环境发生未批准变化；
9. canonical restore 不能回到 normalized Run A state；
10. machine PASS 但 review images 显示重大空间异常；
11. 必须进行交互式检查才能判断正式 PASS；
12. protected input 需要修改；
13. 任何 non-obvious failure 无法由已有 contract 明确解释。

---

## 18. Completion Report｜Codex 必须返回

完成执行后必须报告：

- source `main` SHA；
- Codex internal branch / commit SHA；
- GitHub-visible PR number / URL；
- GitHub-visible head branch / SHA；
- changed-file list；
- GitHub Actions run URL / run id / attempt；
- runner / Blender exact version；
- artifact name / artifact id（如平台可返回）；
- canonical `.blend` SHA256；
- 365/365 runtime outcome summary；
- generated formal/proxy/control/envelope/semantic-only/deferred/blocked counts；
- omission / anonymous formal mesh / broken identity count；
- spatial machine validation result；
- canonical Hard Fail count；
- 5/5 negative fixture result；
- prohibited P2 transform scan；
- PM-005 mutation result；
- canonical restore result；
- deterministic normalized snapshot result；
- protected-input hash result；
- review PNG paths / hashes；
- whether any `LOCAL_MAC_REQUIRED` evidence remains；
- unresolved / STOP items；
- explicit `NO MERGE` confirmation。

PR 不得自行 merge。

---

## 19. Task Closure Authority

只有以下顺序全部完成，T-018 才可关闭：

1. Product Owner 明确授权执行 T-018；
2. Codex Cloud 完成工程并发布一个 task PR；
3. GitHub Actions headless Blender evidence chain 实际运行；
4. ChatGPT 审核 code / outputs / workflow / machine evidence；
5. ChatGPT 按 RC-015 实际打开正式 review PNG；
6. 若无必须 Local Mac 的未决 evidence，ChatGPT 给出 Task-level review conclusion；
7. Product Owner 明确批准 T-018；
8. Product Owner 单独或同一明确指令授权 merge；
9. merge 后由 ChatGPT 更新 Project Control。

在第 7 步前不得写 `T-018 PASS / CLOSED`。

---

## 20. 当前锁定结论

T-018 Task Contract 已由 Product Owner 批准并锁定。

当前状态：

`LOCKED / PRODUCT OWNER APPROVED / READY FOR EXECUTION / EXECUTION NOT AUTHORIZED`

下一动作：

> **等待 Product Owner 明确授权“开始执行 T-018”。**
