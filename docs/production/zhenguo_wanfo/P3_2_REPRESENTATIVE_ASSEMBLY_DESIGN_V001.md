# P3.2｜代表性构件组合验证设计 V001

## Representative Assembly Design V001｜LOCKED / PRODUCT OWNER APPROVED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Gate：P3.2｜构件组合关系模型
- Status：LOCKED / PRODUCT OWNER APPROVED
- Decision：D-043
- Approval date：2026-09-14
- Scope：A/B/C 三个代表性组合验证单元的节点、接口、关系、参数与 evidence status 设计锁定

## 1. 总体原则

本设计用于下一项工程任务的直接实现基线，不等于 P3.2 Gate PASS，也不授权 P3.3。

三个单元承担三种不同验证：

- A：证明正式 Master 可以按显式接口规则形成真实组合；
- B：证明证据不足时系统能够保留关系语义并正确阻断未经批准的实际几何；
- C：证明正式 Master 可以由建筑级参数驱动重复生成，而不是人工复制。

不得为了形成“完整梁架”强行把六个 Master 串成未经证据支持的历史关系链。

---

## 2. A｜柱—柱头栌斗承托组合单元

### 2.1 单元身份

- Assembly Unit ID：`AU-COLUMN-LUDOU-001`
- 中文名：柱头承托组合单元
- Node class：`ASSEMBLY_UNIT`
- Evidence：`PROJECT_RULE`
- Historical role：`ORGANIZATIONAL_UNIT`
- historical_claim：false

### 2.2 节点

- `CMP-COLUMN-001`｜柱｜正式 P3.1 approved Master
- `CMP-LUDOU-COLUMN-001`｜柱头栌斗｜正式 P3.1 approved Master
- `AU-COLUMN-LUDOU-001`｜组合单元

构件身份和构件自身 evidence 均继承 P3.1，不因组合而升级。

柱当前 canonical realization 的 `height_mm=3534.3` 来自 `Z-006-RC-01 / REASONABLE_COMPLETION / D-023`，仅为可替换生产候选；历史 `Z-006` 继续 `UNKNOWN / null / DO_NOT_LOCK`。

柱头栌斗现状尺寸来自 `SRC-ZG-WF-001 / D-007` 的直接测量，但现存构件及其具体接触构造不得自动等同于 963 原始状态。

### 2.3 新增组合接口

#### A-I01｜柱上承托基准面

- interface_id：`CMP-COLUMN-001__TOP-SUPPORT-PLANE`
- owner：`CMP-COLUMN-001`
- type：`PLANE`
- coordinate_space：`MASTER_LOCAL`
- local position：`z = current realization height_mm`
- current driver：`Z-006-RC-01 = 3534.3 mm`
- primary direction：+Z
- allowed relations：`SUPPORT`, `LOCATE`
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- replaceability：true

含义：工程组合基准面，不是已证实的历史柱头加工面。

#### A-I02｜柱头栌斗下承托基准面

- interface_id：`CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE`
- owner：`CMP-LUDOU-COLUMN-001`
- type：`PLANE`
- coordinate_space：`MASTER_LOCAL`
- local position：`z=0`
- basis：现有 `bottom_footprint_center` Master 坐标体系
- primary direction：+Z
- allowed relations：`SUPPORT`, `LOCATE`
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- replaceability：true

含义：显式的工程组合接口；不得把 T-015 通用 `__LOWER-PLANE` 自动历史化为真实接触面。

中心定位继续使用：

- `CMP-COLUMN-001__AXIS`
- `CMP-LUDOU-COLUMN-001__AXIS`

### 2.4 正式关系

#### A-R01｜承托

- relation_type：`SUPPORT`
- source：`CMP-COLUMN-001`
- target：`CMP-LUDOU-COLUMN-001`
- source_interface：`CMP-COLUMN-001__TOP-SUPPORT-PLANE`
- target_interface：`CMP-LUDOU-COLUMN-001__LOWER-SUPPORT-PLANE`
- directionality：DIRECTED
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- joinery_detail_status：`UNKNOWN`

允许表达柱承托柱头栌斗这一工程组合关系；不因此确认具体榫卯、接触加工或 963 原真性。

#### A-R02｜中心定位

- relation_type：`LOCATE`
- source：`CMP-COLUMN-001`
- target：`CMP-LUDOU-COLUMN-001`
- source_interface：`CMP-COLUMN-001__AXIS`
- target_interface：`CMP-LUDOU-COLUMN-001__AXIS`
- evidence_status：`PROJECT_RULE`
- historical_claim：false

含义：代表性组合采用同轴工程定位；不声称历史实物达到数学意义绝对同轴。

#### A-R03 / A-R04｜从属

- `CMP-COLUMN-001 → AU-COLUMN-LUDOU-001`
- `CMP-LUDOU-COLUMN-001 → AU-COLUMN-LUDOU-001`
- relation_type：`BELONG`
- evidence_status：`PROJECT_RULE`

### 2.5 A 单元禁止项

- 不建立未经证据支持的 CONNECT / 榫卯关系；
- 不把 3534.3 mm 柱高升级为 CONFIRMED historical height；
- 不把工程接口宣称为历史加工面。

---

## 3. B｜上下六椽栿梁架层位关系单元

### 3.1 单元身份

- Assembly Unit ID：`AU-FRAME-TIER-001`
- 中文名：六椽栿梁架层位组合单元
- Node class：`ASSEMBLY_UNIT`
- Evidence：`PROJECT_RULE`
- Historical role：`ORGANIZATIONAL_UNIT`
- historical_claim：false

### 3.2 节点

- `CMP-FRAME-LOWER-SIX-CHUANFU-001`｜下六椽栿｜正式 Master
- `CMP-FRAME-UPPER-SIX-CHUANFU-001`｜上六椽栿｜正式 Master
- `CTL-FRAME-001`｜梁架层位控制对象｜CONTROL_ONLY
- `PRX-FRAME-CONNECTOR-001`｜梁架层位连接代理｜PROXY_ONLY
- `AU-FRAME-TIER-001`｜组合单元

`CTL-FRAME-001` 不是历史构件；`PRX-FRAME-CONNECTOR-001` 不得被解释为托脚、蜀柱、榫卯或其他具体历史连接构件。

### 3.3 核心状态

B 单元工程状态锁定为：

`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED`

原因：上下六椽栿 historical full length 均继续 `UNKNOWN / null`；`canonical_reference_length_mm=1000` 仅为 `PROJECT_RULE / NON_HISTORICAL / REPLACEABLE` reference specimen，不能作为万佛殿实际组合长度。

本设计不新增或批准任何建筑级六椽栿 full-length 参数。

### 3.4 新增接口

#### B-I01 / B-I02｜梁架层位定位基准

- `CTL-FRAME-001__LOWER-TIER-DATUM`
- `CTL-FRAME-001__UPPER-TIER-DATUM`
- type：定位基准（工程实现可选择 POINT / AXIS / PLANE 中最小适用形式）
- evidence_status：`PROJECT_RULE`
- historical_claim：false

只用于区分下六椽栿 / 上六椽栿的工程层位，不补造具体历史高程。

#### B-I03 / B-I04｜连接代理端点

- `PRX-FRAME-CONNECTOR-001__LOWER-ENDPOINT`
- `PRX-FRAME-CONNECTOR-001__UPPER-ENDPOINT`
- evidence_status：`PROJECT_RULE`
- qualification：`PROXY_ONLY / NON_HISTORICAL`
- historical_claim：false

### 3.5 正式关系

#### B-R01 / B-R02｜层位定位

- `CTL-FRAME-001 → CMP-FRAME-LOWER-SIX-CHUANFU-001`
- `CTL-FRAME-001 → CMP-FRAME-UPPER-SIX-CHUANFU-001`
- relation_type：`LOCATE`
- evidence_status：`PROJECT_RULE`
- historical_claim：false

含义：表达两类六椽栿的工程层位归属；不补造具体历史高程。

#### B-R03 / B-R04｜连接代理关系

- `CMP-FRAME-LOWER-SIX-CHUANFU-001 → PRX-FRAME-CONNECTOR-001`
- `CMP-FRAME-UPPER-SIX-CHUANFU-001 → PRX-FRAME-CONNECTOR-001`
- relation_type：`CONNECT`
- evidence_status：`PROJECT_RULE`
- historical_claim：false
- joinery_detail_status：`UNKNOWN`
- historical_connector_identity：`UNKNOWN`

含义：存在需要表达的梁架连接关系，但真实历史中间构件身份和具体连接构造尚未解决。

不得建立“上六椽栿 ↔ 下六椽栿直接历史连接”的确定关系。

#### B-R05～B-R08｜从属

四个成员节点分别 `BELONG → AU-FRAME-TIER-001`，evidence_status=`PROJECT_RULE`。

### 3.6 B 单元 PASS 逻辑

B 的正确通过条件不是“生成两根 1000 mm 六椽栿并摆好”，而是：

1. semantic relationship graph 有效；
2. Proxy / Control 身份保持非历史化；
3. 具体榫卯和真实中间构件继续 UNKNOWN；
4. 若缺少独立建筑级 approved full-length 参数，实际六椽栿 full-length geometry creation 被主动阻断；
5. 任意直接使用 `canonical_reference_length_mm=1000` 作为建筑实际长度的路径触发 `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`。

---

## 4. C｜柱网重复组合单元

### 4.1 单元身份

- Assembly Unit ID：`AU-COLUMN-GRID-001`
- 中文名：柱网重复组合单元
- Node class：`ASSEMBLY_UNIT`
- Evidence：`PROJECT_RULE`
- Historical role：`ORGANIZATIONAL_UNIT`
- historical_claim：false

### 4.2 节点

- `CTL-GRID-001`｜柱网定位控制对象｜CONTROL_ONLY
- `CMP-COLUMN-001`｜正式柱 Master
- `AU-COLUMN-GRID-001`｜组合单元

### 4.3 代表范围

不重建整座柱网。本轮只验证一个最小真实代表子集：

**两根柱 + 一个次间间距。**

建筑级 spacing 参数引用现有：

- `PM-005 / side_bay_observed_mm = 3505.7 mm`
- classification：`CONFIRMED`
- time_layer：`observed_as_measured`
- source_layer：`DIRECT_PRIMARY`

### 4.4 新增接口

#### C-I01｜次间起点

- interface_id：`CTL-GRID-001__SIDEBAY-START`
- type：`POINT`
- evidence_status：`PROJECT_RULE`
- historical_claim：false

#### C-I02｜重复方向轴

- interface_id：`CTL-GRID-001__X-AXIS`
- type：`AXIS`
- evidence_status：`PROJECT_RULE`
- historical_claim：false

### 4.5 正式重复关系

#### C-R01｜柱重复

- relation_type：`REPEAT`
- source：`CTL-GRID-001`
- target：`CMP-COLUMN-001`
- start_interface：`CTL-GRID-001__SIDEBAY-START`
- direction_interface：`CTL-GRID-001__X-AXIS`
- count：2
- spacing_ref：`PM-005`
- spacing_value_mm：3505.7（必须由参数引用取得，不得裸写为关系事实）
- relation evidence_status：`PROJECT_RULE`
- spacing evidence：继承 `PM-005 = CONFIRMED / observed_as_measured`
- historical_claim：false

必须分离：

- 3505.7 mm 作为次间现状实测参数的证据状态；
- 采用 REPEAT 规则生成实例作为工程实现规则。

### 4.6 Runtime Instance Manifest

建议下一项工程实现新增最小 runtime instance manifest，至少记录：

- `instance_id`
- `source_component_id`
- `generated_by_relation_id`
- `ordinal`
- derived transform
- parameter refs

Canonical 至少生成：

- `INST-COLUMN-SIDEBAY-001`
- `INST-COLUMN-SIDEBAY-002`

两个实例都必须保持：

`source_component_id = CMP-COLUMN-001`

禁止因为实例增加而生成新的 `component_id`。

### 4.7 Mutation 设计

C 为本轮唯一正式 mutation 对象。

Canonical：

- `count = 2`
- `spacing_ref = PM-005`

Test-only mutation：

- `count = 3`
- `PM-005` 不修改

必须执行：

`2 → rebuild → validate → 3 → rebuild → validate → restore 2 → rebuild → validate`

证明实例数量由规则和参数驱动，而非人工复制。

### 4.8 从属

- `CTL-GRID-001 → AU-COLUMN-GRID-001`
- `CMP-COLUMN-001 → AU-COLUMN-GRID-001`
- relation_type：`BELONG`
- evidence_status：`PROJECT_RULE`

---

## 5. Evidence Status 总表

| 对象 / 关系 | Evidence Status / Boundary |
|---|---|
| 正式 Master 身份 | 继承 P3.1，不升级 |
| A 柱→柱头栌斗 SUPPORT | PROJECT_RULE |
| A 同轴 LOCATE | PROJECT_RULE |
| A 新增承托接口 | PROJECT_RULE / historical_claim=false |
| A 具体榫卯 | UNKNOWN |
| 柱高 3534.3 mm | REASONABLE_COMPLETION / replaceable / not confirmed historical height |
| B 上下六椽栿身份 | 继承 P3.1；historical full length UNKNOWN/null |
| B 层位 LOCATE | PROJECT_RULE |
| B Connector Proxy CONNECT | PROJECT_RULE |
| B Connector | PROXY_ONLY / NON_HISTORICAL |
| B 真实连接构件身份 | UNKNOWN |
| B 具体榫卯 | UNKNOWN |
| C 次间 3505.7 mm | CONFIRMED / observed_as_measured / DIRECT_PRIMARY |
| C REPEAT 方法 | PROJECT_RULE |
| A/B/C Assembly Unit | PROJECT_RULE / ORGANIZATIONAL_UNIT |
| 所有 BELONG | PROJECT_RULE |

原则：**构件身份有直接证据，不代表构件关系、接口或榫卯自动升级为 CONFIRMED。**

---

## 6. Locked Prohibitions｜强制禁止

1. A 中生成未经证据支持的榫卯；
2. A 中把 3534.3 mm 柱高写成 CONFIRMED historical height；
3. A 中把工程承托接口声明为已证实历史加工面；
4. B 中使用六椽栿 1000 mm reference specimen 作为万佛殿实际梁长；
5. B 中直接建立上六椽栿与下六椽栿的确定历史直接连接；
6. B 中把 `PRX-FRAME-CONNECTOR-001` 命名或升级为托脚、蜀柱或其他具体历史构件；
7. C 中为了方便而采用统一等距柱网重建整殿；
8. C 中为重复实例创建新的 `component_id`；
9. 三个单元中均不得把当前 Blender world position 作为正式组合输入；
10. 本设计不得扩张到完整铺作、屋面、角梁、Deferred Master 补建或 P3.3 整殿重建。

---

## 7. Engineering Handoff

下一项工程任务只需实现本设计，不得重新决定古建筑关系语义。

工程目标应至少证明：

1. A：正式 Master 可以由显式接口关系确定性组合；
2. B：证据不足时能够保留关系语义并主动阻断非法实际尺寸/几何；
3. C：正式 Master 可以由参数化 REPEAT 关系生成实例并完成 mutation / restore；
4. 五类基础关系在代表性场景中得到真实使用：SUPPORT / CONNECT / LOCATE / REPEAT / BELONG；
5. 三项 P3.2 Gate Hard Fail 持续有效；
6. P2 frozen baseline 与 P3.1 canonical Masters 保持不变。

本设计批准后，T-016 Task Contract 可进入规划，但在 Contract 正式创建和 Product Owner 批准执行前，不启动工程实现。