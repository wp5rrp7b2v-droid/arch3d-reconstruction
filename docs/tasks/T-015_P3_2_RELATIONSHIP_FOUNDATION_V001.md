# T-015｜P3.2 构件组合关系基础工程实现 V001

## Task Contract｜AUTHORIZED FOR CODEX EXECUTION

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.2｜构件组合关系模型
- Task ID：T-015
- Engineering ID：`P3_2_RELATIONSHIP_FOUNDATION_V001`
- Think Level：MEDIUM
- Execution Mode：CHAT_FIRST_CODEX_EXECUTOR_MODE
- Executor：Codex
- Status：AUTHORIZED / READY FOR LOCAL EXECUTION
- Date：2026-09-14

## 1. 任务目的

将 ChatGPT 已锁定的 `P3_2_RELATIONSHIP_FOUNDATION_DESIGN_V001` 实现为确定性的机器可读工程基础。

本任务只实现：

1. 组合节点资格数据结构；
2. 五类基础构件关系的数据结构；
3. 组合接口与定位规则的数据结构；
4. 对上述数据结构的机器 Validator 与负向测试。

**Codex 不负责重新设计 P3.2 关系体系，不负责解释历史构造，不负责创建代表性组合几何。**

## 2. Authoritative Inputs｜必须先读取

Codex 执行前必须读取当前 `main` 同步后的以下正式输入：

1. `docs/production/zhenguo_wanfo/P3_2_DEFINITION_OF_DONE_V001.md`
2. `docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_DESIGN_V001.md`
3. P3.0 authoritative Component Registry / Schema
4. P3.1 approved Master Registry / Contract V002
5. 当前 6 个 approved canonical Master records
6. 与 Z-006、Z-006-RC-01、DG-114、HIS-002、六椽栿 historical full length、45°转角/榫卯/隐角梁有关的既有 evidence boundaries
7. 当前 P2 frozen baseline manifest / protection checks

如仓库实际 authoritative 文件名或路径与本合同概述不同，以 Registry / Project Control 中已登记的正式路径为准；**不得因找不到预想路径而新造第二套 authoritative Registry。**

## 3. Locked Design｜不得重新决策

### 3.1 正式构件节点

以下 6 个 approved canonical Masters 必须直接继承既有 `component_id`：

- `CMP-COLUMN-001`｜柱
- `CMP-LUDOU-COLUMN-001`｜柱头栌斗
- `CMP-DOU-SINGLE-LONGKAI-001`｜单向长开斗
- `CMP-DOU-INTERACTIVE-001`｜交互斗
- `CMP-FRAME-LOWER-SIX-CHUANFU-001`｜下六椽栿
- `CMP-FRAME-UPPER-SIX-CHUANFU-001`｜上六椽栿

不得创建重复 component identity。

### 3.2 非正式历史节点资格

- Proxy：工程辅助/近似/关系测试；不得历史化。
- Control：工程控制用途。
- Envelope：边界/包络/空间限制用途。
- Deferred：默认不得成为正式历史构件；明确工程引用时保持 Deferred。
- UNKNOWN：未知属性保持未知，不得自动补全或升级。

### 3.3 五类关系

只实现以下五类基础关系；Codex 不得自行增加第六类：

1. 承托 `SUPPORT`
2. 连接 `CONNECT`
3. 定位 `LOCATE`
4. 重复 `REPEAT`
5. 从属 `BELONG`

人类可读名称中文为主；机器 enum 使用上述稳定英文值。

关系语义边界：

- 承托 ≠ 连接
- 连接 ≠ 榫卯已知
- 定位 ≠ 连接
- 从属 ≠ 接触
- 重复 ≠ Blender Copy
- 视觉接触 ≠ 已确认结构关系

### 3.4 组合接口

V001 接口类型只允许：

- `POINT`｜点
- `AXIS`｜轴
- `PLANE`｜面

接口至少能够表达：接口 ID、中文名称、所属节点、接口类型、局部位置/局部基准、主方向、允许关系类型、evidence/provenance 信息。

不得将 Blender world-space coordinates 作为唯一正式定位依据。

## 4. Required Deliverables｜正式输出

Codex 应优先沿用现有仓库目录结构；若 P3.2 尚无目录，则建立最小清晰目录。最终至少生成：

1. `production/zhenguo_wanfo/assembly/P3_2_ASSEMBLY_SCHEMA_V001.json`
   - node schema
   - relationship schema
   - interface schema
   - evidence / provenance / replaceability / parameter reference constraints

2. `production/zhenguo_wanfo/assembly/P3_2_ASSEMBLY_NODE_REGISTRY_V001.json`
   - 6 个 approved Master 的正式节点记录
   - 非历史对象类型的资格规则/引用规则
   - 不要求把 365 个旧实例逐件迁入

3. `production/zhenguo_wanfo/assembly/P3_2_RELATIONSHIP_TYPES_V001.json`
   - 五类关系定义
   - 中文名 + stable enum
   - directionality
   - endpoint qualification
   - self-link / cycle policy
   - required fields

4. `production/zhenguo_wanfo/assembly/P3_2_INTERFACE_REGISTRY_V001.json`
   - 为 6 个正式 Master 建立**满足数据结构验证所需的最小接口记录**
   - 只登记能够由既有 Master 局部坐标/几何语义和现有证据安全表达的接口
   - 对证据不足的历史连接细节保持 UNKNOWN；不得猜榫卯

5. Validator script
   - 路径遵循现有 repository script convention
   - 必须可从命令行确定性执行

6. Automated tests / negative fixtures
   - 路径遵循现有 test convention
   - 必须证明非法输入能够被拒绝，而不是只验证 happy path

7. `production/zhenguo_wanfo/validation/P3_2_RELATIONSHIP_FOUNDATION_VALIDATION_V001.json`
   - machine-readable final validation report
   - 记录每项 check、PASS/FAIL、错误代码、输入版本/hash（适用时）

8. `docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_REVIEW_V001.md`
   - 人工审核摘要
   - 中文为主
   - 清楚列出：6 个节点、5 类关系、接口结构、证据边界、仍为 UNKNOWN 的内容、保护资产检查结果

## 5. Schema Minimum Contract

### 5.1 Node 最小字段

至少支持：

- `node_id`
- `component_id` 或明确非构件节点引用
- `canonical_name_zh`
- `node_class`
- `historical_role`
- `qualification_status`
- `evidence_status`
- `provenance`
- `replaceability`

不得通过 `qualification_status` 把 Proxy / Control / Envelope / Deferred 自动升级为历史构件。

### 5.2 Relationship 最小字段

至少支持：

- `relationship_id`
- `relation_type`
- `source_node`
- `target_node`
- `source_interface`（按关系需要）
- `target_interface`（按关系需要）
- `directionality`
- `evidence_status`
- `provenance`
- `replaceability`
- `parameter_refs`
- `notes`

`notes` 只能解释，不能替代机器规则。

### 5.3 Interface 最小字段

至少支持：

- `interface_id`
- `owner_node`
- `canonical_name_zh`
- `interface_type`
- local position / datum representation
- primary direction
- allowed relation types
- evidence status
- provenance

## 6. Dimension / Parameter Isolation｜强制

正式尺寸传递逻辑必须支持：

`构件身份 → 组合关系 → 建筑层级参数 → 实际实现尺寸`

禁止：

`canonical Master reference specimen → 自动成为建筑实际尺寸`

特别检查：

- `CMP-FRAME-LOWER-SIX-CHUANFU-001`
- `CMP-FRAME-UPPER-SIX-CHUANFU-001`

其 `canonical_reference_length_mm=1000` 只能保持 `PROJECT_RULE / NON_HISTORICAL / REPLACEABLE` reference specimen。

Validator 必须能够检测实际组合尺寸字段或 building-level parameter 被该 reference specimen 非法直接继承的 fixture，并返回 `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`。

## 7. Machine Validation｜最低必测

至少覆盖以下检查：

1. 6/6 approved Master 唯一存在并正确映射；
2. duplicate `component_id` / duplicate formal node identity 被拒绝；
3. Registry 外正式 component node 被拒绝；
4. Proxy / Control / Envelope / Deferred 身份保持；
5. UNKNOWN 不自动升级；
6. 五类 relation enum 完整且无额外未授权类型；
7. 非法 source / target endpoint 被拒绝；
8. 非法 self-link 被拒绝；
9. 不允许的 cycle / BELONG hierarchy cycle 被拒绝；
10. relation 引用不存在 interface 被拒绝；
11. 必填 evidence / provenance 缺失被拒绝；
12. relationship evidence 与 component evidence 不得被自动等同；
13. world-space-only placement 不能作为正式定位规则通过；
14. `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` negative fixture 必须 FAIL；
15. `SILENT_HISTORICIZATION` negative fixture 必须 FAIL；
16. 能够识别 baked/manual-only placement 表达缺乏正式规则的情形；
17. P2 frozen baseline unchanged；
18. 6 个 P3.1 canonical Master / Registry identity / protected evidence fields unchanged。

最终 machine validation 必须 **0 unexplained error**。

## 8. Required Negative Tests

至少创建并运行以下负向测试，不得只在代码中声明错误码：

- duplicate formal identity
- nonexistent component
- illegal self-link
- illegal endpoint type
- nonexistent interface
- BELONG hierarchy cycle
- missing evidence/provenance
- UNKNOWN → CONFIRMED silent upgrade
- Proxy/Control/Envelope/Deferred → historical component silent upgrade
- six-chuanfu 1000 mm reference leakage
- world-coordinate-only placement / baked manual assembly representation

每个 fixture 必须证明 Validator 实际拒绝，并输出稳定错误代码。

## 9. Hard Fail｜立即 STOP

### HF-T015-01｜SILENT_HISTORICIZATION

Proxy / Control / Envelope / Deferred / UNKNOWN 被无授权提升为历史正式构件或历史确定关系。

### HF-T015-02｜DUPLICATE_COMPONENT_IDENTITY

为既有 approved Master 创建新的重复 component identity。

### HF-T015-03｜REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY

六椽栿 1000 mm reference specimen 被作为建筑实际组合尺寸或 building-level historical dimension。

### HF-T015-04｜BAKED_MANUAL_ASSEMBLY

数据结构只能保存 Blender 最终世界坐标/人工摆放结果，不能表达可重建的关系、接口与参数来源。

### HF-T015-05｜EVIDENCE_STATUS_UPGRADE

UNKNOWN / RC / PROJECT_RULE / 工程控制信息被静默升级为历史确定事实。

### HF-T015-06｜PROTECTED_BASELINE_MUTATION

P2 frozen baseline、6 个 P3.1 canonical Master identity / protected evidence fields 被非授权修改。

任一 Hard Fail 在 canonical output 中发生：**T-015 = HOLD / STOP**，不得自行放宽 Contract。

## 10. Explicit Non-goals｜禁止扩张

T-015 不得：

- 生成整座万佛殿；
- 创建 P3.3 文件；
- 建立完整梁架组合几何；
- 创建代表性组合单元正式几何；
- 新增历史构件 Master；
- 补造榫卯、暗槽、隐藏连接细节；
- 根据视觉猜测历史连接；
- 修改 6 个 canonical Master；
- 逐件迁移 P2 的 365 个 instances；
- 为展示效果制作复杂 Blender 场景；
- 自行新增关系类型；
- 自行修改 P3.2 DoD 或 T-015A Design。

## 11. Execution Rules

1. **开始前必须同步 `origin/main`。**
2. 执行前检查 working tree；存在不明 tracked changes 或与 Project Control 同文件并发修改时 STOP。
3. 本任务默认不需要 Blender 几何生成；如仅为读取既有 `.blend` metadata 而需要 Blender，必须遵循 RC-008 CLI/background，不得通过 GUI 自动化。
4. 遵循 RC-011 Chat-first / Codex-executor：合同外证据冲突、关系语义歧义、历史解释问题必须 STOP 返回 ChatGPT。
5. Codex Think Level = MEDIUM；不得自行升级 HIGH，除非后续由 ChatGPT 明确授权。
6. `.blend/.blend1` 继续 local-only；本任务不得为了方便把 binary Master 加入普通 Git。
7. 不修改 `docs/project_control/` 作为工程任务的主要输出；工程完成后只汇报事实，由 ChatGPT 负责 Project Control 审核与正式状态更新，除非另有明确授权。

## 12. PASS Criteria

T-015 工程完成候选必须同时满足：

- Required Deliverables 全部存在；
- 6/6 approved Master node mapping PASS；
- 五类关系定义完整；
- interface / placement contract machine-readable；
- Required Negative Tests 全部按预期被拒绝；
- final machine validation PASS；
- unexplained validation error = 0；
- Gate Hard Fail = 0；
- P2 frozen baseline unchanged；
- P3.1 canonical Master identities / protected evidence fields unchanged；
- Review V001 足够支持 ChatGPT 人工结构审核。

**Codex 完成以上条件只表示 `ENGINEERING COMPLETE / REVIEW REQUIRED`，不等于 T-015 最终 APPROVED，也不等于 P3.2 PASS。**

最终批准权属于 Product Owner。

## 13. Codex Completion Report｜必须简洁返回

执行完成后只需返回：

- `STATUS`：ENGINEERING COMPLETE / HOLD / STOP
- `TASK`：T-015
- `ENGINEERING_COMMIT`
- `FILES_CREATED_OR_CHANGED`
- `MACHINE_VALIDATION`：x/x PASS
- `NEGATIVE_TESTS`：x/x EXPECTED REJECTION PASS
- `APPROVED_MASTER_MAPPING`：6/6 PASS 或异常
- `HARD_FAILS`：0 或具体错误码
- `PROTECTED_BASELINE`：PASS / FAIL
- `REVIEW_FILE`
- `NEXT_REVIEW_ACTION`：ChatGPT review / Product Owner review / STOP reason

不得用长篇解释替代上述事实字段。