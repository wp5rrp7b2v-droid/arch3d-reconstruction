# T-020｜P3.3 屋顶共享脊基准与设计坐标层对齐规则 V001

## Task Contract｜LOCKED / PRODUCT OWNER APPROVED / EXECUTION AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.3｜构件驱动整殿重建
- Task ID：T-020
- Engineering ID：`P3_3_ROOF_SHARED_RIDGE_DATUM_RULE_V001`
- 中文任务名：屋顶共享脊基准与设计坐标层对齐规则
- Think Level：HIGH
- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`
- Primary Engineering Executor：Codex Cloud
- Cloud Mode Classification：`CLOUD_EXECUTABLE`
- Blender Requirement：`NONE`
- Status：**CONTRACT LOCKED / PRODUCT OWNER APPROVED / EXECUTION AUTHORIZED / CODEX CLOUD READY**
- Date：2026-09-18
- Gate authority：D-047 / `P3_3_DEFINITION_OF_DONE_V001`
- Contract approval：D-056
- Execution authorization：D-057
- Blocking downstream task：T-018 / PR #3 / HOLD

> T-020 是 T-018 正式审核后新增的最小上游规则补丁。它不新增历史证据、不重开 P3.2、不替代 T-018，也不生成整殿。唯一职责是把已经存在的 reconstructed-design 参数与屋顶相对拓扑放入一个明确、可机器验证、可替换且不冒充历史事实的 project-model coordinate/datum authority 中。

---

## 1. 任务目的

T-018 Round 2/3 已证明：当前模型能够确定南北两坡相对 eave→ridge 链以及唯一 shared ridge terminal identity，但上游没有正式规则说明 reconstructed-design roof system 如何落入 reconstructed-design whole-building coordinate system。

已确认的缺口不是新的历史证据缺口，而是 project-level engineering rule modeling omission。

T-020 的唯一目标：

> **建立 reconstructed-design plan datum / coordinate-layer semantics，并正式定义唯一 shared ridge datum 与该坐标层的关系，使后续 T-018 只能消费该上游规则，而不能在生成器内部自行创造 mirror/origin/ridge 规则。**

---

## 2. 已锁定的事实与边界

### 2.1 Shared ridge identity

Canonical PURLIN control topology：

- `ROOF_PURLIN_N_00`
- `ROOF_PURLIN_N_01`
- `ROOF_PURLIN_N_02`
- `ROOF_PURLIN_N_03` = **唯一 shared ridge terminal**
- `ROOF_PURLIN_S_00`
- `ROOF_PURLIN_S_01`
- `ROOF_PURLIN_S_02`

禁止新增 `ROOF_PURLIN_S_03` 或第二个 ridge terminal。

7/7 PURLIN qualification / building disposition 继续保持：

`DEFERRED`

本任务不得创建 PURLIN Master，也不得把 control topology 升级成历史构件几何事实。

### 2.2 Authorized relative roof chain

- `MOD-002 = 15.3 mm/fen`
- `FR-007 = [120,115,210] fen`，方向固定为 eave→ridge
- 对应分段水平距离：
  - 1836.0 mm
  - 1759.5 mm
  - 3213.0 mm
- cumulative half-run = **6808.5 mm**

因此已授权的相对拓扑为：

- north：`R-D → R`
- south：`R+D → R`
- both sides terminate at the same shared ridge `N03 = R`

`ROOF-007 / ROOF-008 / ROOF-009` 继续负责 eave→lower / lower→upper / upper→ridge 的 Z 向 rise chain。

### 2.3 Layer separation

Observed / as-measured values：

- PM-003
- PM-004
- PM-005
- PM-006
- PM-007

在 P3.3 reconstructed-design placement 中只能作为：

`VALIDATION_REFERENCE / OBSERVED_REFERENCE`

不得作为 reconstructed-design plan origin、design-grid placement、ridge datum 或 roof placement 的生成输入。

Reconstructed-design candidates：

- PM-008
- PM-009
- PM-010
- PM-011
- PM-012
- MOD-002
- FR-007
- ROOF-007 / 008 / 009

可以在其既有 evidence boundary 内驱动 reconstructed-design geometry。

---

## 3. T-020 必须正式建立的 Project Coordinate Rule

### 3.1 Rule nature

新增规则必须明确：

- `source_layer = PROJECT_RULE`
- `time_layer = project_model_datum`
- `historical_claim = false`
- `historical_claim_upgrade = false`
- `replaceable = true`
- role = reconstructed-design coordinate / datum authority

它是**建模坐标约定**，不是“963 年原建筑采用此坐标系”的历史判断。

### 3.2 Reconstructed-design plan datum

建立一个独立于 observed/as-measured layer 的 reconstructed-design plan coordinate frame。

最小语义：

- `X = 0`：reconstructed-design plan width center datum
- `Y = 0`：reconstructed-design plan depth center datum
- `Z = 0`：继续引用既有 `Z-007` abstract column-foot design plane；T-020 不重新定义 Z datum
- X/Y 轴仅为 project-model convention，不形成历史方位制度主张
- north-side depth coordinates 与 south-side depth coordinates 必须位于 Y=0 两侧，并由同一 reconstructed-design design layer 派生

PM-011 / PM-012 是 reconstructed-design overall width/depth candidate；PM-008 / PM-009 / PM-010 是 reconstructed-design bay candidate。机器验证必须确保用于设计层 placement 的 width/depth/grid 不回退到 PM-003～007 observed reference。

### 3.3 Shared ridge datum

唯一 shared ridge line 的 plan-depth datum：

`RIDGE_Y = 0`

即 shared ridge 与 reconstructed-design depth center datum 共线。

这是 **replaceable project engineering placement rule**，不是历史尺寸声明。

使用 FR-007 + MOD-002 后，roof-control depth positions 必须满足：

- N00 = -6808.5 mm
- N01 = -4972.5 mm
- N02 = -3213.0 mm
- N03 = 0 mm = shared ridge
- S02 = +3213.0 mm
- S01 = +4972.5 mm
- S00 = +6808.5 mm

允许实现采用公式派生，不要求在正式数据文件中硬编码这些数值；正式 authority 必须保留 dependency lineage 到 `FR-007 + MOD-002 + shared ridge datum`。

T-020 不重新定义 ridge Z。ridge Z 继续由现有 Z datum、approved replaceable column-height rule 与 ROOF-007/008/009 等既有 vertical rules 派生。

---

## 4. Authoritative Inputs｜执行前必须读取

### Governance

1. `docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`
2. `docs/project_control/project_state.json`
3. `docs/project_control/governance.md`
4. `docs/project_control/CLOUD_MODE_2026-09-16_20.md`
5. 本合同

### Canonical model inputs

1. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
2. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
3. `production/zhenguo_wanfo/build/P3_3_BUILDING_INPUT_BASELINE_V001.json`
4. `production/zhenguo_wanfo/build/P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`
5. `production/zhenguo_wanfo/build/P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`
6. `production/zhenguo_wanfo/build/P3_3_BUILDING_GRAPH_VALIDATION_V001.json`
7. P3.2 Assembly Schema / Node Registry / Interface Registry / Relationship Types
8. T-017 builder / validator / tests
9. T-019 corrected PURLIN disposition outputs

### Read-only diagnostic source

T-018 PR #3 may be read only to confirm the failure mode. T-020 must not modify T-018 branch/files.

---

## 5. Allowed Engineering Changes｜严格最小范围

T-020 可以：

1. 新增一个 machine-readable project rule artifact，建议：
   `production/zhenguo_wanfo/build/P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_V001.json`
2. 将该 artifact 纳入 P3.3 building input authority，使下游可以明确消费；
3. 在 `P3_3_BUILDING_PARAMETER_BINDINGS_V001.json` / Building Assembly Graph 中增加**仅为引用该 project rule 所必需**的 LOCATE / datum binding；
4. 更新 T-017/P3.3 validator，使 observed-reference → reconstructed-design-placement 泄漏能够被拒绝；
5. 新增 T-020 专用 validator / tests / validation report；
6. 更新 README/engineering notes 以明确 coordinate-layer semantics。

允许新增 P3.3-specific rule id，但不得新增第六种 P3.2 relationship type；关系语义仍使用既有 `LOCATE`。

---

## 6. Required Machine Validation

至少验证：

1. project rule artifact schema/content valid；
2. `historical_claim=false`；
3. `replaceable=true`；
4. Z datum 继续引用 Z-007，不创建第二套 Z origin；
5. N03 是唯一 shared ridge terminal；
6. no S03 identity；
7. north/south roof-control chains 都精确终止于同一 `RIDGE_Y=0`；
8. FR-007 + MOD-002 dependency lineage 完整；
9. cumulative half-run = 6808.5 mm；
10. north/south segment lengths 分别保持 1836.0 / 1759.5 / 3213.0 mm；
11. PM-003～007 不得作为 reconstructed-design placement source；
12. PM-008～012 保持 reconstructed-design candidate 身份，不升级为 confirmed historical fact；
13. 7/7 PURLIN 继续 DEFERRED；
14. P2 numeric world transforms authoritative usage = 0；
15. 11/11 families / 40/40 variants / 365/365 instances accounting 不下降；
16. canonical P3.3 Hard Fail vocabulary 不变；
17. P3.2 relationship vocabulary 不变；
18. deterministic serialization / regeneration PASS。

### Required negative fixtures

至少包含：

- 将 PM-007 observed overall depth 直接用于 reconstructed-design origin/grid → EXPECTED_REJECTION；
- 创建第二个 ridge terminal / S03 → EXPECTED_REJECTION；
- north / south chains 终止于不同 ridge coordinates → EXPECTED_REJECTION；
- 在 T-018-style local rule 中发明 `COLUMN_GRID_Y_MIRROR_RULE` 而无 canonical project-rule authority → EXPECTED_REJECTION；
- 把 project coordinate rule 标记为 historical/confirmed → EXPECTED_REJECTION。

---

## 7. Acceptance Criteria｜T-020 PASS 条件

T-020 只有在以下全部成立时才可进入 ChatGPT formal review：

- project coordinate/datum artifact：PRESENT / MACHINE VALID；
- one shared ridge datum：PASS；
- no S03：PASS；
- FR-007 relative chain preserved：PASS；
- observed/reference layer isolation：PASS；
- reconstructed-design candidate layer preserved：PASS；
- PURLIN 7/7 DEFERRED：PASS；
- no P2 numeric world transform leakage：PASS；
- accounting 11/40/365 preserved：PASS；
- P3.2 relationship vocabulary unchanged：PASS；
- canonical P3.3 Hard Fail vocabulary unchanged：PASS；
- required negatives all EXPECTED_REJECTION；
- deterministic regeneration / stable serialization：PASS；
- P2 / P3.0 / P3.1 / P3.2 protected canonical layers：UNCHANGED；
- T-018 PR #3：UNCHANGED；
- Blender invocations：0；
- .blend files created：0。

ChatGPT formal structural review PASS 后，仍需 Product Owner 明确批准 T-020 并授权 merge；未经批准不得 merge。

---

## 8. Explicit Non-goals

T-020 不允许：

- 修改 P2 historical / observed measurements；
- 把 PM-003～007 改成 generative reconstructed-design values；
- 宣称 reconstructed-design center datum 是已证实的 963 年历史轴网制度；
- 新增历史尺寸；
- 创建 PURLIN Master；
- 修改 7/7 PURLIN DEFERRED qualification；
- 修改 P3.1 approved Masters；
- 修改 P3.2 relationship vocabulary；
- 重开 P3.2 Gate；
- 生成 Blender / .blend；
- 修改 T-018 generator / validator / workflow / PR #3；
- 修复 T-018 的具体 placement；该工作必须等 T-020 merge 后回到原 PR #3 执行。

---

## 9. STOP Conditions

出现以下任一情况必须 STOP：

1. 需要新增或推测历史尺寸才能确定 datum；
2. 需要把 observed/as-measured value 升级为 reconstructed-design generative authority；
3. 需要修改 P2 formal parameter values 或 evidence classification；
4. 需要修改 P3.1 Master eligibility；
5. 需要修改 P3.2 relationship vocabulary/schema foundation；
6. 需要创建第二个 ridge identity；
7. 需要改变 PURLIN DEFERRED 状态；
8. 需要修改 T-018 PR #3；
9. 需要 Blender / interactive local evidence；
10. 发现 reconstructed-design PM-008～012 自身不能在不新增历史假设的情况下形成一致 design plan grid；
11. 发现 shared ridge = design depth center 这一 project-model convention 与其他已锁定 canonical rule 发生实质冲突。

---

## 10. Cloud / Branch / PR Rule

继续遵守 RC-014：

`ONE TASK = ONE BRANCH = ONE PR`

T-020 必须使用独立于 T-018 PR #3 的 branch / PR。

建议任务标签：

`codex/t020-p3-3-roof-shared-ridge-datum-rule-v001`

禁止直接向 main 提交 T-020 工程实现；禁止未经 Product Owner 授权 merge。

---

## 11. T-020 完成后的 T-018 恢复条件

只有在以下链条完成后，T-018 才允许恢复 placement correction：

`T-020 engineering → independent PR → ChatGPT formal review → Product Owner approval/merge authorization → merge main → canonical verification`

随后回到**原 T-018 PR #3**：

1. 同步最新 main；
2. 删除/禁止 unauthorized `COLUMN_GRID_Y_MIRROR_RULE`；
3. 消费 T-020 canonical datum authority；
4. 重新推导至少 7 PURLIN controls、36 RAFTER proxies、6 ROOF_ENVELOPE、4 GABLE_CONTROL 与 roof-dependent FRAME endpoints；
5. 重跑 Actions；
6. 重新做 PLAN / FRONT / SIDE / AXON formal visual review。

T-020 PASS / merge 不等于 T-018 PASS，也不等于 P3.3 Gate PASS。
