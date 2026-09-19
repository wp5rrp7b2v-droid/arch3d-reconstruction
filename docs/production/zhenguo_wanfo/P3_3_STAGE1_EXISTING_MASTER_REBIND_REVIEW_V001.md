# P3.3 V002 Stage 1｜既有6个 Component Master 对 V007 重新绑定复核 V001

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Gate：P3.3 V002｜真实构件驱动整殿重建
- Stage：Stage 1｜真实构件 Master 库
- Authorization：D-067
- Date：2026-09-19
- Nature：ChatGPT design/review；不占 T-###
- Status：REVIEW COMPLETE / 6 OF 6 RETAINED WITH BOUNDED DISPOSITIONS
- Engineering execution：NONE
- T-018 impact：NONE / HOLD

## 1. 复核目标

本轮不重新建模，也不修改既有 Master 几何。

只回答：

1. 既有6个 P3.1 已批准 Master 是否仍能服务于 V007 真实构件体系；
2. 能绑定到哪些 V007 真实实例；
3. 哪些只能保留为几何参考、不能直接进入整殿物理实例；
4. 哪些需要在 Stage 2 增加实例长度、接口或方向桥；
5. 是否存在必须废弃或立即重建的既有 Master。

## 2. 依据

- V007 canonical registry：
  `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- P3.1 Master Library：
  `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`
- P3.1 Master Contract V002：
  `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`
- 六个 Master 的参数、语义快照、review / validation 资产。

## 3. 结论总表

| 既有 Master | V007 实例/状态 | 复核结论 | 当前限制 | Stage 2动作 |
|---|---|---|---|---|
| 柱 | 12个实体实例：4角柱+8普通柱 | **RETAIN / REBIND PASS** | 现状直径约460mm；459mm仅报告设计候选；历史柱高未知，3534.3mm仍为可替换项目候选；角柱/普通柱当前只是角色差异，不证明存在几何差异 | 建立12实例→同一Master的绑定；角柱角色作为实例语义，不新增无证据几何变体 |
| 柱头栌斗 | 12枚，逐柱位置已锁 | **RETAIN / REBIND PASS** | Master 外包络尺寸与 V007 一致；耳、槽、卯口等仍无证据；方向需在装配层处理 | 建立12实例绑定；Stage 2补 orientation / support interface |
| 单向长开斗 | V007 当前无可安全闭合的逐件物理实例；全殿总量未知 | **RETAIN MASTER / INSTANCE BINDING BLOCKED** | 现有 Master 仍是有效实测外包络参考，但不得因为 Master 已存在就虚构数量和位置 | 保留 approved Master；不得进入物理实例总量；待后续新证据或明确装配规则再绑定 |
| 交互斗 | V007 当前无可安全闭合的逐件物理实例；全殿总量未知 | **RETAIN MASTER / INSTANCE BINDING BLOCKED** | 同上；DG-114 继续 UNKNOWN，不得统一化小斗规则 | 保留 approved Master；不得进入物理实例总量 |
| 下六椽栿 | 东缝、西缝共2件，截面实测锁定 | **RETAIN / REBIND PASS WITH LENGTH BRIDGE REQUIRED** | Master 的1000mm长度仅为非历史 reference specimen，绝对禁止直接进入建筑；历史全长继续 UNKNOWN | Stage 2建立“实例装配端点→building-specific geometry length”桥；必须标明 PROJECT_RULE / explicit derived geometry，不能称历史实测长度 |
| 上六椽栿 | 东缝、西缝共2件，截面实测锁定 | **RETAIN / REBIND PASS WITH LENGTH BRIDGE REQUIRED** | 与下六椽栿相同：1000mm reference 不得泄漏；历史全长 UNKNOWN | 同上 |

## 4. 逐项复核

### 4.1 柱

V007 已有12根柱的真实实例身份和位置。

现有 `CMP-COLUMN-001_MASTER`：

- 几何是恒定圆柱体；
- 现状直径参考为约460mm；
- 3534.3mm 高度明确属于 `Z-006-RC-01` 可替换候选；
- 原始963柱高 `Z-006` 仍为 UNKNOWN；
- Master 已明确禁止无证据的收分、卷杀、侧脚、柱础、柱头细节和榫卯。

因此它仍适合作为 V007 的柱体 Master。

V007 的“角柱 / 普通柱”在当前证据下先解释为**实例角色分类**，而不是两个不同几何 Master。若以后出现角柱升高、侧脚或不同截面证据，再新建正式变体。

### 4.2 柱头栌斗

V007 直接锁定12枚柱头栌斗，且尺寸口径与 P3.1 Master Contract V002 一致：

- 面阔总宽 475.1mm；
- 面阔下宽 327.1mm；
- 进深总深 446.3mm；
- 进深下深 305.5mm；
- 总高 293.8mm；
- 平高 / 斜高继续只在证据允许范围内使用。

现有 Master 可以一对一绑定12个真实位置。

转角柱上的栌斗虽然进入双向转角铺作，但这属于装配关系，不自动证明需要不同栌斗几何 Master。

### 4.3 单向长开斗

现有 `CMP-DOU-SINGLE-LONGKAI-001_MASTER` 的测量外包络仍有效：

- 顶宽236.2mm；
- 下宽162.7mm；
- 顶深256.2mm；
- 下深177.2mm；
- 总高158.6mm。

但 V007 明确没有安全闭合它的全殿真实数量与逐件位置。

因此当前状态必须是：

> **Master retained / physical-instance binding blocked**

不能因为 P3.1 已经建过这个 Master，就在 V007 中人为生成对应实例。

### 4.4 交互斗

现有 `CMP-DOU-INTERACTIVE-001_MASTER` 的测量外包络仍有效：

- 顶宽255.2mm；
- 顶深240.0mm；
- 下宽176.2mm；
- 下深165.1mm；
- 总高148.5mm。

V007 同样未闭合全殿真实总量和逐件位置。

因此保留 Master，但不进入当前物理实例 accounting。

### 4.5 下六椽栿

V007 有2件：

- 下六椽栿-东缝；
- 下六椽栿-西缝。

截面数据与现有 Master 完全同口径：

- 广493.5mm；
- 榫处厚375mm；
- 最大厚444mm。

现有 Master 的1000mm长度只为 reference specimen。

V002 当前允许在**装配端点明确后**计算 building-specific geometry length，但必须保持：

- historical full length = UNKNOWN；
- geometry length = 项目装配推导值；
- 1000mm reference 绝不进入整殿；
- 不把端点推导长度升级为历史实测尺寸。

因此 Master 本体无需重做；需要 Stage 2 的长度桥与接口合同。

### 4.6 上六椽栿

V007 有2件：

- 上六椽栿-东缝；
- 上六椽栿-西缝。

截面：

- 广334mm；
- 榫处厚209mm；
- 最大厚240.5mm。

处理方式与下六椽栿完全相同。

## 5. Stage 1 首轮结论

### 不需要推倒重做

六个既有 Master **全部保留**。

其中：

- 2类可直接绑定实体实例：
  - 柱；
  - 柱头栌斗。
- 2类可绑定实体实例，但需要 Stage 2 长度桥：
  - 下六椽栿；
  - 上六椽栿。
- 2类只保留为 approved geometry reference，当前禁止绑定实体数量：
  - 单向长开斗；
  - 交互斗。

### 本轮没有发现

- Master 尺寸与 V007 直接冲突；
- 必须立即重建的既有 Master；
- 需要重开 P3.1 Gate 的系统性错误；
- 可以把未知斗件数量补齐的新证据。

## 6. Hard Fail 防护

从本轮起：

- Master 已存在 ≠ 真实实例一定存在；
- Master 已批准 ≠ 允许自动补足其全殿数量；
- reference specimen length ≠ building-specific length；
- 角色 variant ≠ 几何 variant；
- derived geometry length ≠ historical measured length。

违反任一项将分别触发：

- `LEGACY_PROXY_AS_REAL_COMPONENT`
- `REGISTRY_LAYER_DOUBLE_COUNT`
- `MASTER_WITHOUT_EVIDENCE_BINDING`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `SILENT_HISTORICIZATION`

## 7. 下一子步骤

Stage 1 下一步：

> 建立 **V007 全构件 Master Coverage / Disposition Matrix V001**，把当前登记中的构件类型逐类分到：已有 Master / 需新建 Master / 参数化补全 / 简化 Proxy / UNKNOWN。

完成覆盖矩阵后，再正式锁定第一个缺失 Master（默认候选四椽栿）的建模规格。

此时仍不创建 T-###，不运行 Blender，不恢复 T-018。
