# T-016｜P3.2 代表性构件组合验证 V001

## Task Contract｜CREATED / READY FOR EXECUTION / NOT STARTED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.2｜构件组合关系模型
- Task ID：T-016
- Engineering ID：`P3_2_REPRESENTATIVE_ASSEMBLY_VALIDATION_V001`
- Think Level：MEDIUM
- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`
- Executor：Codex
- Status：**CONTRACT CREATED / READY / NOT STARTED**
- Date：2026-09-14
- Design authority：D-043 / `P3_2_REPRESENTATIVE_ASSEMBLY_DESIGN_V001`

> 本合同已创建，但“创建 Task Contract”不等于已经开始工程执行。正式执行须在本地同步 GitHub `main` 后，由 Product Owner / ChatGPT 明确发出“开始执行 T-016”指令。

---

## 1. 任务目的

把已锁定的 A/B/C 三个代表性组合单元从“关系设计”实现为**可计算、可验证、可重复生成、证据边界明确**的工程验证。

T-016 要证明三件不同的能力：

1. **A｜能组合**：正式 canonical Master 可以通过显式接口、定位和参数形成真实最小组合；
2. **B｜能正确不组合**：当关键建筑级参数/历史证据不足时，系统能够保留关系语义，同时主动阻断未经批准的实际几何；
3. **C｜能参数化重复**：正式 canonical Master 可由参数与规则生成多个实例，并通过 mutation/rebuild 证明不是人工复制。

本任务不完成整座万佛殿，不进入 P3.3。

---

## 2. Authoritative Inputs｜执行前必须读取

Codex 执行前必须读取当前同步后的 `main`：

1. `docs/production/zhenguo_wanfo/P3_2_DEFINITION_OF_DONE_V001.md`
2. `docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_DESIGN_V001.md`
3. `docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_REVIEW_V001.md`
4. `docs/production/zhenguo_wanfo/P3_2_REPRESENTATIVE_ASSEMBLY_DESIGN_V001.md`
5. `docs/tasks/T-015_P3_2_RELATIONSHIP_FOUNDATION_V001.md`
6. T-015 生成的：
   - `production/zhenguo_wanfo/assembly/P3_2_ASSEMBLY_SCHEMA_V001.json`
   - `production/zhenguo_wanfo/assembly/P3_2_ASSEMBLY_NODE_REGISTRY_V001.json`
   - `production/zhenguo_wanfo/assembly/P3_2_RELATIONSHIP_TYPES_V001.json`
   - `production/zhenguo_wanfo/assembly/P3_2_INTERFACE_REGISTRY_V001.json`
   - T-015 Validator / tests / validation report
7. P3.1 六个 approved canonical Master records / params / semantic snapshots / protected hashes
8. P3.0 identity / qualification Registry，特别是：
   - `CTL-FRAME-001`
   - `PRX-FRAME-CONNECTOR-001`
   - `CTL-GRID-001`
9. P2.1 formal production parameter set，特别是 `PM-005`
10. P2 frozen baseline protection manifest
11. Governance 4.2 / 4.4 / 4.6 及当前 Project Control 状态

如果仓库中的 authoritative 路径与本合同概述存在轻微路径差异，优先沿用现有正式 Registry / Project Control 路径；**不得另造第二套 authoritative identity、parameter set 或 relationship foundation。**

---

## 3. Locked Scope｜不得重新设计

### 3.1 三个正式验证单元

只实现：

- `AU-COLUMN-LUDOU-001`｜柱头承托组合单元
- `AU-FRAME-TIER-001`｜六椽栿梁架层位组合单元
- `AU-COLUMN-GRID-001`｜柱网重复组合单元

Assembly Unit 均为：

- `node_class = ASSEMBLY_UNIT`
- `evidence_status = PROJECT_RULE`
- `historical_role = ORGANIZATIONAL_UNIT`
- `historical_claim = false`

不得把 Assembly Unit 解释为历史构件。

### 3.2 五类关系仍只有五类

T-016 只能使用 T-015 已锁定的：

- `SUPPORT`｜承托
- `CONNECT`｜连接
- `LOCATE`｜定位
- `REPEAT`｜重复
- `BELONG`｜从属

不得新增第六类关系，不得为方便实现新造 `STACK`、`MOUNT`、`ATTACH`、`ARRAY` 等平行语义。

---

## 4. A｜AU-COLUMN-LUDOU-001｜柱头承托组合单元

### 4.1 正式节点

- `CMP-COLUMN-001`｜柱
- `CMP-LUDOU-COLUMN-001`｜柱头栌斗
- `AU-COLUMN-LUDOU-001`

构件身份与 evidence 继承 P3.1，不因进入组合阶段升级。

柱当前 canonical realization：

- `height_mm = 3534.3`
- classification = `REASONABLE_COMPLETION`
- source = `Z-006-RC-01 / D-023`
- replaceable = true

历史 `Z-006` 必须继续 `UNKNOWN / null / DO_NOT_LOCK`。

### 4.2 必须新增并登记的接口

#### A-I01

`CMP-COLUMN-001__TOP-SUPPORT-PLANE`

- owner：`CMP-COLUMN-001`
- type：`PLANE`
- coordinate_space：`MASTER_LOCAL`
- local z：由当前 column realization `height_mm` 参数解析
- primary direction：+Z
- allowed relation types：`SUPPORT`, `LOCATE`
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- replaceability：true

#### A-I02

`CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE`

- owner：`CMP-LUDOU-COLUMN-001`
- type：`PLANE`
- coordinate_space：`MASTER_LOCAL`
- local z：0
- basis：approved Master `bottom_footprint_center`
- primary direction：+Z
- allowed relation types：`SUPPORT`, `LOCATE`
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- replaceability：true

中心定位继续复用 T-015 已有：

- `CMP-COLUMN-001__AXIS`
- `CMP-LUDOU-COLUMN-001__AXIS`

禁止把通用 `__LOWER-PLANE` 静默改名/升级为历史接触面。

### 4.3 必须登记的关系

#### A-R01｜SUPPORT

`CMP-COLUMN-001 → CMP-LUDOU-COLUMN-001`

- source interface：`CMP-COLUMN-001__TOP-SUPPORT-PLANE`
- target interface：`CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE`
- directionality：DIRECTED
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- joinery_detail_status：`UNKNOWN`

#### A-R02｜LOCATE

`CMP-COLUMN-001 → CMP-LUDOU-COLUMN-001`

- source interface：`CMP-COLUMN-001__AXIS`
- target interface：`CMP-LUDOU-COLUMN-001__AXIS`
- evidence_status：`PROJECT_RULE`
- historical_claim：false

#### A-R03 / A-R04｜BELONG

- `CMP-COLUMN-001 → AU-COLUMN-LUDOU-001`
- `CMP-LUDOU-COLUMN-001 → AU-COLUMN-LUDOU-001`
- evidence_status：`PROJECT_RULE`

### 4.4 A 几何实现要求

A 必须生成最小 Blender 组合验证几何：

`canonical Master identity + current approved realization parameters + interface rules → derived placement`

要求：

1. 柱位置可取组合单元局部原点，但该位置必须由单元规则定义，不得依赖现有场景人工摆放；
2. 栌斗 Z 位置必须由柱 `TOP-SUPPORT-PLANE` 与栌斗 `LOWER-SUPPORT-PLANE` 接口匹配计算；
3. X/Y 定位必须由两者 AXIS 对齐计算；
4. 结果可删除后由 Registry + relationship + parameters 确定性重建；
5. 不生成任何榫卯、凹槽、暗槽、内部接触加工细节；
6. 不因视觉贴合而把 SUPPORT 升级为 CONFIRMED historical construction。

### 4.5 A 验证重点

至少验证：

- 两个 canonical component identity 未改变；
- 接口存在且 owner 正确；
- SUPPORT 与 LOCATE 均从规则计算；
- 栌斗 bottom support plane 与柱 top support plane 在组合局部坐标中对齐；
- 两主轴对齐；
- world transform 为 derived result，不是 authoritative input；
- `Z-006-RC-01` 仍标为 RC；
- `joinery_detail_status = UNKNOWN`。

---

## 5. B｜AU-FRAME-TIER-001｜六椽栿梁架层位组合单元

### 5.1 正式节点

- `CMP-FRAME-LOWER-SIX-CHUANFU-001`｜下六椽栿
- `CMP-FRAME-UPPER-SIX-CHUANFU-001`｜上六椽栿
- `CTL-FRAME-001`｜CONTROL_ONLY
- `PRX-FRAME-CONNECTOR-001`｜PROXY_ONLY
- `AU-FRAME-TIER-001`

### 5.2 Canonical 状态必须固定

`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED`

原因：

- lower historical full length = `UNKNOWN / null`
- upper historical full length = `UNKNOWN / null`
- `canonical_reference_length_mm = 1000` 只允许用于 canonical Master reference specimen
- 本任务没有批准新的 building-specific full-length 参数

### 5.3 必须新增并登记的接口

- `CTL-FRAME-001__LOWER-TIER-DATUM`
- `CTL-FRAME-001__UPPER-TIER-DATUM`
- `PRX-FRAME-CONNECTOR-001__LOWER-ENDPOINT`
- `PRX-FRAME-CONNECTOR-001__UPPER-ENDPOINT`

要求：

- evidence_status：`PROJECT_RULE`
- historical_claim：false
- Control 保持 CONTROL_ONLY
- Proxy 保持 PROXY_ONLY / NON_HISTORICAL

对于两个 tier datum 的具体 POINT / AXIS / PLANE 机器实现，Codex 只能从 T-015 schema 中选择满足最小表达的既有类型；**不得通过选择接口类型来引入未锁定的历史高程或构造含义。**

### 5.4 必须登记的关系

#### B-R01 / B-R02｜LOCATE

- `CTL-FRAME-001 → CMP-FRAME-LOWER-SIX-CHUANFU-001`
- `CTL-FRAME-001 → CMP-FRAME-UPPER-SIX-CHUANFU-001`
- evidence_status：`PROJECT_RULE`
- historical_claim：false

只表达“下层 / 上层”工程层位归属，不补造历史绝对高程。

#### B-R03 / B-R04｜CONNECT

- `CMP-FRAME-LOWER-SIX-CHUANFU-001 → PRX-FRAME-CONNECTOR-001`
- `CMP-FRAME-UPPER-SIX-CHUANFU-001 → PRX-FRAME-CONNECTOR-001`
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- joinery_detail_status：`UNKNOWN`
- historical_connector_identity：`UNKNOWN`

含义仅为：存在需表达的梁架连接关系，但真实历史中间构件与连接构造尚未解决。

#### B-R05～B-R08｜BELONG

四个成员节点分别属于 `AU-FRAME-TIER-001`。

### 5.5 B 的几何阻断验证｜核心

B **不得生成万佛殿实际全长六椽栿组合几何**。

工程实现必须做到：

1. semantic relationship graph 正常建立并通过 schema / topology / evidence validation；
2. 当 full-length geometry builder 请求下/上六椽栿实际长度时，必须查找独立 `building_specific_approved_length` 或等价正式建筑级参数来源；
3. 当前不存在该 approved 参数时，builder 必须返回稳定阻断状态，而不是 fallback 到 1000 mm；
4. canonical expected result = `FULL_LENGTH_GEOMETRY_BLOCKED`；
5. 该阻断**不是 T-016 FAIL**，而是 B 单元的预期 PASS 行为；
6. synthetic negative fixture 如果把 `canonical_reference_length_mm=1000` 直接注入 actual/building length，则必须触发 `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`。

### 5.6 B 审核资产

B 不得为了“看起来完整”偷用 1000 mm actual beam geometry。

正式人工审核资产应使用：

- 关系/层位 schematic；或
- 明确标注 `SEMANTIC ONLY / FULL-LENGTH GEOMETRY BLOCKED` 的非历史工程示意；
- 显示中文构件名、Control / Proxy 身份、CONNECT / LOCATE 关系、UNKNOWN connector identity、blocked reason。

若使用 canonical 1000 mm Master 的缩略轮廓作为图例，必须明确标记：

`NON-HISTORICAL REFERENCE SPECIMEN / NOT ACTUAL ASSEMBLY LENGTH`

不得把该图例空间尺度解释为实际梁架比例。

---

## 6. C｜AU-COLUMN-GRID-001｜柱网重复组合单元

### 6.1 正式节点

- `CTL-GRID-001`｜CONTROL_ONLY
- `CMP-COLUMN-001`｜正式 Master
- `AU-COLUMN-GRID-001`

### 6.2 Building-level parameter

唯一 canonical spacing source：

- parameter id：`PM-005`
- value：3505.7 mm
- classification：`CONFIRMED`
- time_layer：`observed_as_measured`
- source_layer：`DIRECT_PRIMARY`

数值必须通过 `parameter_ref = PM-005` 解析；关系记录可以缓存 resolved value 供 validation，但不得把 `3505.7` 作为与 PM-005 脱离的 naked authoritative constant。

### 6.3 必须新增接口

- `CTL-GRID-001__SIDEBAY-START`｜POINT
- `CTL-GRID-001__X-AXIS`｜AXIS

二者：

- evidence_status：`PROJECT_RULE`
- historical_claim：false

### 6.4 C-R01｜REPEAT

`CTL-GRID-001 → CMP-COLUMN-001`

Canonical：

- count = 2
- spacing_ref = `PM-005`
- direction = `CTL-GRID-001__X-AXIS`
- start = `CTL-GRID-001__SIDEBAY-START`
- relation evidence_status = `PROJECT_RULE`
- spacing evidence = inherited from `PM-005`
- historical_claim = false

### 6.5 BELONG

- `CTL-GRID-001 → AU-COLUMN-GRID-001`
- `CMP-COLUMN-001 → AU-COLUMN-GRID-001`
- evidence_status：`PROJECT_RULE`

### 6.6 Runtime Instance Manifest｜必须实现

T-016 必须建立最小 runtime instance manifest，至少支持：

- `instance_id`
- `source_component_id`
- `assembly_unit_id`
- `generated_by_relation_id`
- `ordinal`
- `derived_transform`
- `parameter_refs`

Canonical 至少包含：

- `INST-COLUMN-SIDEBAY-001`
- `INST-COLUMN-SIDEBAY-002`

且必须：

`source_component_id = CMP-COLUMN-001`

禁止因为实例增加创建 `CMP-COLUMN-002`、`CMP-COLUMN-003` 或其他新 component identity。

### 6.7 C Blender 几何实现

C 必须生成最小两柱 Blender 组合场景：

`CTL-GRID rule + PM-005 + CMP-COLUMN-001 → two runtime instances`

要求：

- 两柱间距由 PM-005 解析；
- 位置由 start + direction + ordinal × spacing 计算；
- world transforms 为派生结果；
- scene 中即使删除全部实例，也可以从正式输入重新生成。

### 6.8 Mutation / Restore｜必须执行

Canonical：`count = 2`

Test-only mutation：`count = 3`

禁止修改 `PM-005`。

流程：

1. canonical 2 → build → validate；
2. mutate count 3 → rebuild → validate 3 instances；
3. restore count 2 → rebuild → validate；
4. canonical semantic output / instance manifest 恢复标准状态；
5. mutation 产物不得替代 canonical output。

---

## 7. Required Engineering Outputs

Codex 应沿用现有 `production/zhenguo_wanfo/assembly/` 架构。至少生成/更新：

1. **Representative Assembly Registry**
   - A/B/C 三个 Assembly Unit
   - 正式 members / states / evidence boundary

2. **Representative Relationship Graph V001**
   - A/B/C 全部正式 relationships
   - stable relationship IDs
   - parameter refs / evidence / interfaces

3. **Interface Registry extension**
   - A/B/C 新增接口
   - 不破坏 T-015 既有接口

4. **Runtime Instance Manifest V001**
   - 至少覆盖 C canonical 2-column runtime instances

5. **Builder / Generator**
   - A 最小组合重建
   - B semantic validation + full-length geometry blocking
   - C repeat instance generation
   - 可从 CLI 确定性执行

6. **Validator extension or dedicated T-016 validator**
   - 对代表性组合结构、evidence、parameter flow、geometry blocking、runtime instances、determinism 进行机器验证

7. **Automated tests / negative fixtures**
   - 包括本合同 §11 要求

8. **Machine-readable validation report**
   - 建议：`production/zhenguo_wanfo/validation/P3_2_REPRESENTATIVE_ASSEMBLY_VALIDATION_V001.json`

9. **Human-readable engineering review summary**
   - 建议：`docs/production/zhenguo_wanfo/P3_2_REPRESENTATIVE_ASSEMBLY_REVIEW_V001.md`

10. **Review assets**
   - A｜柱—柱头栌斗承托关系图
   - B｜上下六椽栿层位 / semantic blocking 图
   - C｜柱网重复关系图
   - P3.2 Representative Assembly Overview

正式审核图必须遵循 Governance 4.5 / 4.6：中文构件名为主，ID / stable enum 可辅助显示。

11. **Local-only Blender artifacts**
   - A canonical `.blend`
   - C canonical `.blend`
   - mutation `.blend` 如为临时验证可不保留
   - `.blend/.blend1` 不进入普通 Git
   - 必须记录 canonical local path + SHA256（如实际生成）

B 不要求 actual full-length canonical `.blend`；若系统因 blocked 状态不生成 B `.blend`，这是预期行为。

---

## 8. Deterministic Reconstruction Requirements

### A

必须：

`Registry + interfaces + relationships + approved component realization params → rebuild A`

执行：

- clean generation
- save local-only `.blend`
- independent reopen
- semantic / geometry validation
- second clean regeneration
- deterministic comparison

### C

必须：

`Registry + REPEAT relation + PM-005 → rebuild C`

执行 canonical / mutation / restore；canonical restore 后再做 deterministic comparison。

### B

必须确定性得到：

`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED`

相同正式输入重复执行，blocked reason / code 必须稳定。

---

## 9. Machine Validation｜最低必测

至少覆盖：

### Foundation / identity

1. T-015 schema / node / relationship foundation 仍有效；
2. A/B/C Assembly Unit IDs 唯一；
3. 既有 component_id 未重复创建；
4. Control / Proxy 身份未升级；
5. P3.1 evidence fields 未被修改。

### A

6. A members 完整；
7. `TOP-SUPPORT-PLANE` / `LOWER-SUPPORT-PLANE` 存在且 owner/type 正确；
8. SUPPORT endpoint/interface 合法；
9. LOCATE axis 合法；
10. A geometry placement 由 interface rule 生成；
11. world-space-only/manual placement 无法通过；
12. `Z-006-RC-01` 未升级；
13. joinery remains UNKNOWN；
14. independent reopen PASS；
15. deterministic regeneration PASS。

### B

16. B members 完整；
17. CTL-FRAME 仍 CONTROL_ONLY；
18. PRX-FRAME-CONNECTOR 仍 PROXY_ONLY / NON_HISTORICAL；
19. LOCATE / CONNECT graph 合法；
20. direct lower↔upper historical connection 不存在；
21. connector historical identity = UNKNOWN；
22. joinery detail = UNKNOWN；
23. no building-specific approved full length → full-length geometry blocked；
24. canonical blocked status = expected PASS；
25. 1000 mm actual/building length fixture → `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`。

### C

26. PM-005 正确解析为 3505.7 mm；
27. PM-005 evidence 保持 CONFIRMED / observed_as_measured；
28. REPEAT relation evidence 保持 PROJECT_RULE；
29. canonical count = 2；
30. runtime instances = 2；
31. 两 instance 均引用 `CMP-COLUMN-001`；
32. derived spacing = PM-005；
33. 不产生新 component_id；
34. mutation count=3 → exactly 3 instances；
35. restore count=2 → exactly 2 instances；
36. PM-005 mutation count = 0；
37. independent reopen PASS；
38. deterministic regeneration PASS。

### Cross-unit / protection

39. SUPPORT / CONNECT / LOCATE / REPEAT / BELONG 五类均被真实代表性图使用；
40. 三项 Gate Hard Fail canonical state = 0；
41. P2 frozen baseline unchanged；
42. 6 个 P3.1 canonical Masters unchanged；
43. unrelated untracked files untouched；
44. P3.3 files created = 0。

允许实际 validation check 数大于 44；不得少于上述语义覆盖。

---

## 10. Required Review Assets

只要求 4 张核心审核图，避免过度生产。

### R-A｜柱头承托组合关系

必须清楚显示：

- 柱 / 柱头栌斗中文名；
- `component_id`；
- SUPPORT；
- LOCATE；
- top/lower support datum；
- `Z-006-RC-01 = REASONABLE_COMPLETION`；
- `joinery = UNKNOWN`。

### R-B｜六椽栿梁架层位关系与阻断

必须清楚显示：

- 上六椽栿 / 下六椽栿；
- `CTL-FRAME-001 = CONTROL_ONLY`；
- `PRX-FRAME-CONNECTOR-001 = PROXY_ONLY`；
- LOCATE / CONNECT；
- `historical full length = UNKNOWN/null`；
- `1000 mm = NON-HISTORICAL REFERENCE ONLY`；
- `FULL_LENGTH_GEOMETRY_BLOCKED = EXPECTED`。

不得用视觉构图暗示 1000 mm 是实际梁长。

### R-C｜柱网重复关系

必须清楚显示：

- 两根柱；
- 同一个 `CMP-COLUMN-001` source identity；
- `PM-005 = 3505.7 mm / CONFIRMED / observed_as_measured`；
- `REPEAT = PROJECT_RULE`；
- count=2。

### R-OVERVIEW｜P3.2 Representative Assembly Overview

同时展示 A / B / C 三类系统行为：

- A = CAN ASSEMBLE
- B = SEMANTIC VALID / GEOMETRY BLOCKED
- C = PARAMETRIC REPEAT

人类可读主标题和构件名称中文优先。

---

## 11. Required Negative Tests

至少实际运行：

1. A 缺失 top support interface → reject；
2. A 使用 world-space-only 栌斗位置且无正式 LOCATE/interface rule → `BAKED_MANUAL_ASSEMBLY`；
3. A 把 `Z-006-RC-01` 升级 CONFIRMED → reject；
4. A 把 joinery UNKNOWN 改成 confirmed mortise-tenon → reject；
5. B 使用 1000 mm 作为 actual/building full length → `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`；
6. B 将 `PRX-FRAME-CONNECTOR-001` 改为 historical component → `SILENT_HISTORICIZATION`；
7. B 将 `CTL-FRAME-001` 改成 historical member → `SILENT_HISTORICIZATION`；
8. B 创建 lower↔upper direct historical confirmed CONNECT → reject；
9. B 无 building-specific approved length 却生成 actual full-length geometry → reject；
10. C 将 3505.7 裸写并删除 PM-005 parameter_ref → reject；
11. C runtime instance 创建新 `component_id` → reject；
12. C mutation 修改 PM-005 → reject；
13. C world coordinates 代替 start/direction/spacing rule → `BAKED_MANUAL_ASSEMBLY`；
14. BELONG hierarchy cycle → reject；
15. 非法 relation/interface endpoint → reject。

每个 negative fixture 必须输出稳定错误代码或稳定 validation failure key。

---

## 12. Hard Fail｜Canonical Output 中出现即 STOP

### HF-T016-01｜REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY

六椽栿 1000 mm canonical reference 被用于实际/建筑级组合长度。

### HF-T016-02｜SILENT_HISTORICIZATION

Proxy / Control / Assembly Unit / UNKNOWN relation detail 被静默提升为历史确定对象或关系。

### HF-T016-03｜BAKED_MANUAL_ASSEMBLY

A/C 的正式结果依赖人工 Blender world position，而不能从 Registry + relationship + interfaces + parameters 重建。

### HF-T016-04｜EVIDENCE_STATUS_UPGRADE

RC / UNKNOWN / PROJECT_RULE 被未经授权升级为更高历史确定性。

### HF-T016-05｜DUPLICATE_COMPONENT_IDENTITY

重复实例或组合单元生成新的 canonical component identity。

### HF-T016-06｜BLOCK_BYPASS

B 在缺少独立 approved building-specific six-chuanfu full length 时仍生成实际全长组合几何。

### HF-T016-07｜PROTECTED_BASELINE_MUTATION

P2 frozen baseline 或 6 个 approved canonical Master 的受保护几何/身份/evidence 被非授权修改。

### HF-T016-08｜P3_3_SCOPE_LEAK

开始整殿重建、创建 P3.3 正式产物或把 A/B/C 扩大为完整万佛殿。

任一 canonical Hard Fail：`T-016 = HOLD / STOP`。

---

## 13. Explicit Non-goals｜禁止扩张

T-016 不得：

- 重建整座万佛殿；
- 创建 P3.3 文件或正式 P3.3 geometry；
- 补齐 13 个 Deferred Masters；
- 创建完整斗栱；
- 把单向长开斗 / 交互斗为了“6/6 Master 都用上”强行塞入 A/B/C；
- 补造柱头泥道栱、慢栱、华栱、昂等证据不足构件；
- 推断托脚、蜀柱等为 `PRX-FRAME-CONNECTOR-001` 的真实身份；
- 生成榫卯、暗槽、内部隐藏连接；
- 为 B 新批建筑级六椽栿 full length；
- 使用 1000 mm reference length 作为 actual assembly；
- 重建整座柱网；
- 修改 PM-005 canonical value；
- 修改 canonical Master 几何以“适配”组合；
- 创建新关系类型；
- 把 visual contact 当作 confirmed historical connection。

---

## 14. Blender / Binary Rules

A、C 需要最小 Blender 组合验证。

执行必须使用本机 Blender 3.6.23 CLI/background：

`/Applications/Blender.app/Contents/MacOS/Blender --background ...`

遵循 Governance 4.2：

- 不使用 GUI 自动化作为工程链；
- `.blend/.blend1` local-only；
- 不 add / commit binary；
- 正式 review PNG、JSON、脚本和文字文档可进入 Git；
- canonical local binary 必须记录 path + SHA256；
- independent reopen 使用 CLI/background。

B 默认不产生 actual full-length `.blend`。如果只为 review schematic 生成视觉资产，必须保证它不是伪装的 actual historical assembly geometry。

---

## 15. Git / Working Tree Rules

1. 开始前记录 `HEAD`、`origin/main`、working tree；
2. 必须满足本地已同步最新 main；
3. 既存 unrelated untracked PDF / PoC / output 不得修改、移动、删除、add、commit；
4. 不处理与 T-016 无关的 tracked changes；若出现未知 tracked changes，STOP；
5. 只提交 T-016 正式 text/code/JSON/review assets；
6. `.blend/.blend1` 不进入 Git；
7. push 后核对 `HEAD SHA == origin/main SHA`；
8. 网络异常遵循 `git-proxy-auto` 规则，不 force/reset/rebase；
9. 本任务默认不修改 `docs/project_control/`；完成后由 ChatGPT 审核并更新 Project Control。

---

## 16. Execution Mode / STOP Rules

采用 `CHAT_FIRST_CODEX_EXECUTOR_MODE`。

Codex 负责：

- 数据结构实现；
- relationship/interface/assembly unit Registry；
- A/C deterministic Blender generation；
- B geometry-blocking implementation；
- validation / tests；
- review asset generation；
- Git engineering commit/push。

Codex **不得自行决定**：

- 新历史关系；
- 新构件身份；
- 新 building-specific 六椽栿长度；
- Proxy 的真实历史名称；
- UNKNOWN 榫卯；
- evidence upgrade；
- P3.3 工作。

出现上述需要时：

`STOP_AND_RETURN_TO_CHATGPT`

Think Level：MEDIUM。只有 ChatGPT 明确授权时才可升级 HIGH。

---

## 17. PASS Criteria｜T-016 工程完成候选

必须同时满足：

1. A/B/C 三个 Assembly Unit 全部 machine-readable；
2. 五类关系 SUPPORT / CONNECT / LOCATE / REPEAT / BELONG 在代表性单元中均有真实覆盖；
3. A interface-driven geometry generation PASS；
4. A independent reopen PASS；
5. A deterministic regeneration PASS；
6. B semantic graph PASS；
7. B `FULL_LENGTH_GEOMETRY_BLOCKED` 为 expected PASS；
8. B 不存在 1000 mm reference leakage；
9. C canonical repeat 2 instances PASS；
10. C PM-005 parameter flow PASS；
11. C 2→3→2 mutation / rebuild / restore PASS；
12. C independent reopen PASS；
13. C deterministic regeneration PASS；
14. required negative tests 全部按预期拒绝；
15. canonical Hard Fail = 0；
16. P2 frozen baseline unchanged；
17. 6 个 P3.1 approved canonical Masters unchanged；
18. unrelated untracked files untouched；
19. P3.3 files created = 0；
20. 4 张核心 review assets 生成完成并可供 ChatGPT / Product Owner 人工审核；
21. engineering commit 已 push，`HEAD == origin/main`。

满足以上条件时，Codex 只可汇报：

`ENGINEERING COMPLETE / REVIEW REQUIRED`

**不得自行宣称：**

- `T-016 PRODUCT OWNER APPROVED`
- `P3.2 PASS`
- `P3.3 UNLOCKED`

这些结论必须由 ChatGPT + Product Owner 后续正式审核。

---

## 18. Final Report Contract｜Codex 必须按此汇报

完成后报告：

- `STATUS`
- `T-016`
- engineering mode / Think Level
- 实际创建/修改文件清单
- A status：interface / SUPPORT / LOCATE / Blender / reopen / determinism
- B status：semantic graph / Proxy-Control identity / geometry block / leakage check
- C status：PM-005 / repeat / runtime instances / mutation 2→3→2 / reopen / determinism
- 5/5 relationship type representative coverage
- machine validation：PASS 数 / 总数
- negative tests：expected rejection PASS 数 / 总数
- canonical Hard Fail count
- 4 review assets 路径
- A/C local-only `.blend` path + SHA256
- P2 frozen baseline：UNCHANGED / NOT
- P3.1 canonical Masters：UNCHANGED / NOT
- unrelated untracked files：UNTOUCHED / NOT
- P3.3 files created：0 / NOT
- engineering commit SHA
- `origin/main` SHA
- 是否存在需要 ChatGPT 判断的问题
- `RECOMMENDED_NEXT_ACTION`

---

## 19. Success Meaning

T-016 成功不表示万佛殿已经开始整殿重建。

它只证明：

> **A：系统知道什么时候可以按正式接口组合；**
>
> **B：系统知道什么时候证据不足，必须保留语义并拒绝伪造实际几何；**
>
> **C：系统知道如何依据正式参数重复生成构件实例。**

只有经过后续 ChatGPT / Product Owner 审核，并完成 P3.2 DoD 全面 Gate Review 后，才可能讨论 P3.2 PASS 与 P3.3 解锁。