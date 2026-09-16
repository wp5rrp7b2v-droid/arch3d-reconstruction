# T-017｜P3.3 整殿输入基线与 Assembly Graph 基础工程 V001

## Task Contract｜LOCKED / READY FOR EXECUTION / NOT STARTED / EXECUTION NOT AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.3｜构件驱动整殿重建
- Task ID：T-017
- Engineering ID：`P3_3_BUILDING_INPUT_AND_ASSEMBLY_GRAPH_V001`
- 中文任务名：整殿输入基线与 Assembly Graph 基础工程
- Think Level：MEDIUM
- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`
- Executor：Codex Cloud
- Cloud Mode Classification：`CLOUD_EXECUTABLE`
- Blender Requirement：`NONE`
- Status：**CONTRACT LOCKED / READY / NOT STARTED / EXECUTION NOT AUTHORIZED**
- Date：2026-09-16
- Gate authority：D-047 / `P3_3_DEFINITION_OF_DONE_V001`
- Execution-environment authority：D-048 / RC-017

> 本合同已由 Product Owner 锁定，但“锁定 Task Contract”不等于已经授权工程执行。T-017 只有在 Product Owner 明确发出“开始执行 T-017”后才进入 Codex Cloud。正式执行时必须遵守 RC-014：`ONE TASK = ONE BRANCH = ONE PR`。

---

## 1. 任务目的

T-017 是 P3.3 的第一项基础工程。

本任务不生成整殿 Blender 几何，而是先建立一套机器可读、可验证、可追溯的整殿输入系统，使后续整殿 generator 能够回答：

1. **整座万佛殿允许读取哪些正式输入；**
2. **每个建筑级参数来自哪里、具有什么 evidence / time-layer / replaceability 状态；**
3. **P2 冻结基线中的 365 个 stable mesh instances 在 P3.3 中分别是什么身份、如何处置；**
4. **整殿的 component / proxy / control / envelope / deferred / unknown 如何进入 Building Assembly Graph；**
5. **哪些关系与位置可以从 Registry + P3.2 relationship foundation + building parameters 重新推导；**
6. **哪些内容必须保持 BLOCKED / SEMANTIC_ONLY / DEFERRED，而不能为了视觉完整性被静默补齐。**

T-017 的核心目标是切断 P3.3 对 P2 “已经摆好的 world transform”的依赖：

`P2 frozen model = comparison / accounting reference`

而不是：

`P2 frozen model = P3.3 placement source`

---

## 2. Locked Scope｜本任务只完成 DoD-01～DoD-04 基础能力

T-017 仅覆盖 P3.3 DoD V001 的以下基础范围：

- **DoD-01｜正式输入基线**
- **DoD-02｜整殿 Assembly Graph**
- **DoD-03｜建筑参数驱动与参数传递基础**
- **DoD-04｜全殿语义覆盖与对象 accounting**

同时为 DoD-07 / DoD-08 建立必要的 evidence-boundary validator 与 Hard Fail negative fixtures。

本任务明确**不完成**：

- DoD-05 的整殿 Blender 几何生成；
- DoD-06 的整殿空间/几何视觉验收；
- DoD-09 的最终 Gate Evidence Package；
- 任何 local-only `.blend`；
- 任何 GitHub Actions Blender workflow 执行。

因此 T-017 完成后，P3.3 Gate **不会自动 PASS**。

---

## 3. Authoritative Inputs｜Codex 执行前必须读取

### 3.1 Gate / Governance

1. `docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`
2. `docs/project_control/project_state.json`
3. `docs/project_control/governance.md`
4. `docs/project_control/CLOUD_MODE_2026-09-16_20.md`
5. `docs/project_control/rules_change_log.md`
6. 本合同：`docs/tasks/T-017_P3_3_BUILDING_INPUT_AND_ASSEMBLY_GRAPH_V001.md`

### 3.2 P3.0 Identity / Ontology

1. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_ONTOLOGY_V001.json`
2. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_SCHEMA_V001.json`
3. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_V001.json`
4. `production/zhenguo_wanfo/registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json`

P3.0 的 Component ID / classification / instance lineage 是 P3.3 身份层的 authoritative source；不得另建第二套 component identity。

### 3.3 P3.1 Canonical Master Layer

1. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json`
2. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json`
3. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`
4. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`
5. 六个 approved canonical Master 的 params / semantic snapshot / protected hash records

P3.1 的身份、evidence 与 Master qualification 不得因进入整殿重建而升级或改写。

### 3.4 P3.2 Assembly Foundation

1. `production/zhenguo_wanfo/assembly/P3_2_ASSEMBLY_SCHEMA_V001.json`
2. `production/zhenguo_wanfo/assembly/P3_2_ASSEMBLY_NODE_REGISTRY_V001.json`
3. `production/zhenguo_wanfo/assembly/P3_2_RELATIONSHIP_TYPES_V001.json`
4. `production/zhenguo_wanfo/assembly/P3_2_INTERFACE_REGISTRY_V001.json`
5. `production/zhenguo_wanfo/assembly/P3_2_REPRESENTATIVE_ASSEMBLY_REGISTRY_V001.json`
6. `production/zhenguo_wanfo/assembly/P3_2_REPRESENTATIVE_INTERFACE_EXTENSION_V001.json`
7. `production/zhenguo_wanfo/assembly/P3_2_REPRESENTATIVE_RELATIONSHIP_GRAPH_V001.json`
8. P3.2 validator / negative fixtures / validation reports

五类基础关系继续固定为：

- `SUPPORT`｜承托
- `CONNECT`｜连接
- `LOCATE`｜定位
- `REPEAT`｜重复
- `BELONG`｜从属

不得创建第六类平行基础关系。

### 3.5 Building Parameters / Evidence

1. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
2. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
3. `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
4. evidence-aware parameter schema / evidence source records

必须保留每个参数的：

- parameter id
- value / unit
- classification
- source layer
- time layer
- production use
- replaceability
- source ids / decision provenance

### 3.6 P2 Frozen Baseline｜只允许有限读取

正式 comparison/accounting source：

`production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`

允许读取的内容至少包括：

- `instance_id`
- `family_id`
- `variant_id`
- evidence / parameter references
- bounded-placeholder / presentation / historical-state metadata
- family / variant / instance count 与对象覆盖范围

**禁止作为 P3.3 authoritative generation input：**

- `transform.location_mm`
- `transform.rotation_euler_rad`
- `transform.scale`
- 任何从 P2 `.blend` / scene object 直接抄取的 world transform
- 任何 pre-positioned whole-building object placement

这些 transform 只能在未来作为 comparison / diagnostic evidence 使用，不能成为 T-017 Building Graph 的 placement source。

---

## 4. Required Outputs｜必须创建的五个核心机器资产

建议统一放置于：

`production/zhenguo_wanfo/build/`

### O-01｜Building Input Baseline

`P3_3_BUILDING_INPUT_BASELINE_V001.json`

至少必须将输入分类为：

- `AUTHORITATIVE_GENERATIVE`
- `ACCOUNTING_REFERENCE_ONLY`
- `COMPARISON_ONLY`
- `PROHIBITED_AS_GENERATIVE_INPUT`

每项输入必须记录 path、role、allowed fields / prohibited fields、provenance 与保护状态。

特别要求：

`P2_3_INTEGRATION_MANIFEST_V001.json` 必须明确标记为 accounting/comparison source，而其中 numeric transforms 必须进入 `PROHIBITED_AS_GENERATIVE_INPUT`。

### O-02｜Building Parameter Bindings

`P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`

建立：

`formal parameter → evidence/time layer → building role → graph node/relationship/rule dependency`

至少覆盖整殿基础拓扑、开间/进深、柱网、主要高程/模数、P3.2 已验证的 building-level parameter，以及后续 generator 必需的正式参数来源。

不得只复制 resolved number 而丢失 parameter id / evidence / provenance。

不得把 `OBSERVED_REFERENCE` 自动升级为 `reconstructed_963_candidate` 历史事实。

### O-03｜Building Scope Accounting

`P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json`

必须对 P2 frozen baseline 的 **365 / 365 stable mesh instances** 做显式 accounting。

每个 instance 至少必须记录：

- legacy `instance_id`
- source `family_id`
- source `variant_id`
- mapped P3.0 `component_id` 或明确 non-component identity
- semantic class
- P3.3 disposition
- evidence boundary
- graph inclusion status
- explanation / provenance

P3.3 disposition 至少允许：

- `GENERATE_FROM_FORMAL_COMPONENT`
- `SEMANTIC_ONLY`
- `PROXY_ONLY`
- `CONTROL_ONLY`
- `ENVELOPE_ONLY`
- `DEFERRED`
- `UNKNOWN_BLOCKED`
- `COMPARISON_ONLY`

要求：

- baseline family coverage = `11 / 11`
- baseline variant coverage = `40 / 40`
- baseline instance accounting = `365 / 365`
- unexplained omission = `0`
- orphan identity = `0`

不能为了达到 365/365，把 Proxy / Control / Envelope / Deferred / UNKNOWN 强行升级成历史正式构件。

### O-04｜Building Assembly Graph

`P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`

建立整殿机器可读语义图。

Graph 至少必须表达：

`BUILDING_ROOT → building/assembly organization → runtime/component/non-component nodes`

每个正式 graph node 必须可追溯至：

- P3.0 identity / non-component class
- P3.1 Master qualification（适用时）
- P3.2 relationship foundation
- building parameter / rule provenance
- P3.3 disposition
- evidence status / historical claim boundary

关系只能使用 P3.2 五类基础关系；可以新增 building-level **relationship instances / organizational nodes / parameter bindings**，但不能修改五类关系定义。

Graph 不要求假装所有真实历史连接已经解决。证据不足时允许并鼓励：

- `SEMANTIC_ONLY`
- `UNKNOWN_BLOCKED`
- `DEFERRED`
- explicit unresolved relationship / interface reason

### O-05｜Validation Report

`P3_3_BUILDING_GRAPH_VALIDATION_V001.json`

必须汇总：

- input baseline validation
- 365/365 accounting validation
- identity / orphan validation
- relationship-type validation
- parameter provenance validation
- prohibited-transform scan
- evidence-boundary validation
- Hard Fail canonical count
- negative fixture results
- deterministic re-run / stable serialization result

---

## 5. Required Engineering Components

除五个核心 JSON 外，Codex 必须建立或扩展：

1. T-017 builder / compiler：从 authoritative registries + formal parameters + accounting source 生成上述输出；
2. Validator：对 canonical outputs 做 schema / identity / relationship / evidence / omission / prohibited-input 检查；
3. Unit tests；
4. Synthetic negative fixtures；
5. stable serialization / deterministic rebuild test；
6. README 或工程说明，明确运行命令、输入、输出与失败条件。

可以复用 P3.0/P3.2 validator utility；不得复制形成第二套互不兼容的验证语义。

---

## 6. P3.3 Hard Fail｜T-017 必须全部建立触发验证

### HF-01｜`REFERENCE_LENGTH_LEAKS_INTO_BUILDING`

Synthetic negative：把上下六椽栿 `canonical_reference_length_mm = 1000` 注入 building actual/full-length parameter 或 building graph actual realization dimension。

Expected：REJECT。

Canonical：0。

### HF-02｜`SILENT_HISTORICIZATION`

Synthetic negative：把 Proxy / Control / Envelope / Deferred / UNKNOWN 或 PROJECT_RULE engineering object 静默标记为 historical confirmed component / construction。

Expected：REJECT。

Canonical：0。

### HF-03｜`BAKED_MANUAL_BUILDING`

Synthetic negative：把 P2 manifest 的 `transform.location_mm` / rotation / scale 或 equivalent pre-positioned world transform 作为 P3.3 authoritative placement source。

Expected：REJECT。

Canonical：0。

### HF-04｜`SILENT_BUILDING_OMISSION`

Synthetic negative：从 365 accounting 中删除一个 legacy instance，且没有 approved explicit disposition / exclusion record。

Expected：REJECT。

Canonical：0。

### HF-05｜`BROKEN_COMPONENT_IDENTITY`

Synthetic negative：让 building instance 指向不存在、错误或不符合 P3.0 Registry qualification 的 component identity。

Expected：REJECT。

Canonical：0。

---

## 7. Mandatory Evidence Boundaries｜不得突破

以下边界继续强制有效：

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`
- `Z-006-RC-01 = REASONABLE_COMPLETION / replaceable / D-023`
- `DG-114 = UNKNOWN / no unified small-dou historical specification claim`
- `HIS-002 = component originality unknown`
- 下/上六椽栿 historical full length = `UNKNOWN / null`
- `canonical_reference_length_mm = 1000` 仅为 `NON_HISTORICAL ENGINEERING_REFERENCE`
- 45°转角、榫卯、hidden-angle beam、未解连接继续 unresolved / bounded
- Proxy / Control / Envelope / Deferred / UNKNOWN 不得为“整殿完整”而历史化

若 T-017 发现 building graph 无法在不猜测的情况下建立某项关系：

**正确行为是登记 unresolved / blocked / deferred，而不是补造。**

---

## 8. Explicit Non-goals｜本任务禁止事项

T-017 禁止：

1. 生成新的整殿 `.blend`；
2. 启动 Blender / GitHub Actions Blender；
3. 修改 P2 frozen `.blend` 或 integration outputs；
4. 修改 P3.1 approved canonical Master 几何；
5. 重新定义 P3.0 Component IDs；
6. 新增第六类基础关系；
7. 将 P2 world transforms 迁移成 P3.3 placement rules；
8. 根据 P2 transform 反推并偷偷固化历史参数；
9. 为六椽栿补造 actual historical full length；
10. 宣称“整殿已重建”或“完全还原963原貌”。

---

## 9. Acceptance Criteria｜T-017 Engineering PASS 条件

T-017 工程结果必须同时达到：

- required outputs：`5 / 5` present and machine-readable
- P2 family accounting：`11 / 11`
- P2 variant accounting：`40 / 40`
- P2 instance accounting：`365 / 365`
- unexplained omission：`0`
- orphan / broken identity：`0`
- P2 numeric world transform used as authoritative generative input：`0`
- foundational relation vocabulary：仅 P3.2 锁定的 `5 / 5`
- canonical P3.3 Hard Fail count：`0`
- five Hard Fail synthetic negatives：`5 / 5 EXPECTED REJECTION`
- evidence-boundary validation：PASS
- deterministic regeneration / stable serialization：PASS
- P2 frozen baseline：UNCHANGED
- P3.1 approved Master assets：UNCHANGED
- P3.2 foundational schema / relation definitions：UNCHANGED
- Blender / `.blend` creation：`0`

Engineering PASS 仍需 ChatGPT structural review + Product Owner approval 才能关闭 T-017。

---

## 10. Cloud Execution Contract｜RC-014

T-017 分类：`CLOUD_EXECUTABLE`。

正式执行时：

- one task = one branch = one PR
- 建议 branch：`codex/t017-p3-3-building-input-assembly-graph-v001`
- Codex 必须从最新 `main` checkout 开始
- 只允许修改 T-017 scope 内工程文件
- 不允许 Codex 自行修改 `docs/project_control/`，除非 Product Owner / ChatGPT 另行明确授权
- PR 不得自动 merge
- ChatGPT 必须审核 PR changed files / machine evidence
- Product Owner 明确批准后方可 merge

由于本任务不需要 Blender，D-048 / RC-017 的 GitHub Actions Blender executor **本任务不启用**；该执行链留给后续整殿几何任务。

---

## 11. STOP Conditions｜遇到即停止并返回 ChatGPT

Codex 遇到以下任一情况必须 STOP，不得自行“合理补齐”：

- authoritative Registry 之间 identity 冲突；
- 365 baseline instance 无法映射且现有记录无法解释；
- building parameter evidence/time-layer 含义冲突；
- 需要新增第六类基础关系才能继续；
- 需要读取 P2 numeric world transform 才能完成 graph；
- 需要把 UNKNOWN / Deferred / Proxy / Control 升级为历史构件才能“补完整”；
- 需要给六椽栿 actual full length 填入 1000mm 或其他无批准长度；
- 需要改变 P3.0/P3.1/P3.2 canonical identities / schemas / Masters；
- machine test 出现非显然失败且无法从合同范围内唯一确定修复方式。

---

## 12. Completion Report｜Codex 返回格式

Codex 完成后至少报告：

- source `main` SHA
- working branch
- commit SHA
- PR number / URL（若平台提供）
- changed-file list
- 5/5 required output 状态
- 11/11 family、40/40 variant、365/365 instance accounting
- unexplained omission / orphan count
- canonical hard fail count
- 5/5 negative fixture result
- prohibited P2 transform scan result
- deterministic rebuild / stable serialization result
- protected baseline unchanged result
- explicit confirmation：`NO BLENDER / NO .BLEND CREATED`
- any STOP / unresolved items

---

## 13. Authorization Boundary｜锁定状态

**当前正式状态：**

`T-017 CONTRACT LOCKED / READY FOR EXECUTION / NOT STARTED / EXECUTION NOT AUTHORIZED`

本合同锁定后：

- 可以作为 Codex Cloud 下一项正式工程任务；
- 不需要本地 Mac；
- 不需要 Blender；
- 不自动启动 Codex；
- 不自动改变 P3.3 Gate 完成状态；
- 不自动授权 PR merge。

下一正式动作：

> Product Owner 明确发出：**“开始执行 T-017”**。
