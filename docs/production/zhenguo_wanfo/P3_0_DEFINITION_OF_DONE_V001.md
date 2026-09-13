# P3.0 Definition of Done V001｜Component Ontology & Registry

Status: **LOCKED / PRODUCT OWNER APPROVED**  
Date: 2026-09-13  
Approved: 2026-09-13  
Decision: `D-030`  
Phase: `P3｜古建筑构件系统化与组合建模`  
Gate: `P3.0｜Component Ontology & Registry`

## 1. Gate Purpose

P3.0 的目标不是继续增加 Blender 几何，而是把 P2 已形成的工程构件架构升级为可解释、可登记、可复用、可扩展的中国古建筑构件知识与资产体系。

P3.0 必须先回答：

- 什么才算一个“历史构件 / 构件类型”；
- 什么只是工程控制对象、诊断对象或几何包络；
- 构件如何命名、分类、编号和登记；
- 构件的名称、种类、作用、参数、证据、3D资产、变体、实例和组合关系如何关联；
- P2 的 11 families / 40 variants / 365 instances 如何无损迁移到新的构件体系。

P3.0 **不得以新增视觉细节或新增模型复杂度作为完成标准**。

## 2. Frozen Input Baseline

P2 继续作为冻结工程基线，不重做、不覆盖：

- formal candidate：`P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001`；
- 11 component families；
- 40 parametric variants；
- 365 stable mesh instances；
- 33/33 automated tests PASS；
- 34/34 machine QC PASS；
- Local Blender 3.6.23 → Cloud Blender 4.5.13 → Local Blender 3.6.23 roundtrip PASS；
- P2 historical / evidence boundaries 全部 carry forward。

P3.0 对 P2 做的是 **semantic audit + registry migration**，不是几何重建。

## 3. Definition of Done｜9 Items

### DoD-01｜Component Ontology V001

建立正式构件本体层级，至少区分：

1. `HISTORICAL_COMPONENT`｜具有明确古建构件语义的构件；
2. `ASSEMBLY_UNIT`｜由多个构件组成、具有组合语义的单元，例如铺作单元；
3. `GEOMETRIC_PROXY`｜为当前证据边界或中等 LOD 使用的替代几何；
4. `CONTROL_OBJECT`｜参数化、定位、诊断使用的非历史构件对象；
5. `ENVELOPE / SURFACE`｜用于屋面或整体外形控制的连续包络；
6. `UNKNOWN / UNRESOLVED_COMPONENT`｜史料不足、暂不能确定构件身份或精确形制的对象。

必须禁止把 Blender object、mesh instance 或工程 family 自动等同于历史构件。

### DoD-02｜Canonical Naming & ID Rules

定义跨建筑可扩展的命名与 ID 规则，至少包含：

- 中文规范名称；
- 英文 / machine-readable canonical key；
- 历史原称 / 报告原称；
- 同义词 / 异名；
- 构件类别；
- 建筑专属 Variant ID；
- Instance ID；
- Assembly ID。

规则必须允许未来加入其他五代、宋、辽、金建筑，而不依赖“万佛殿专用命名”。

### DoD-03｜Component Registry Schema V001

每一种正式构件至少支持以下登记字段：

- component_id；
- canonical_name_zh；
- canonical_name_en / key；
- aliases / historical_terms；
- category / ontology_type；
- function；
- structural_role；
- typical_position；
- source_building / period；
- parameter_ids；
- evidence_by_attribute；
- source_references；
- historical_state / originality_status；
- master_3d_asset；
- variant_ids；
- instance_ids；
- assembly_relations；
- applicability / reuse_scope；
- known_unknowns / interpretation_boundary；
- version / status。

### DoD-04｜P2 Family Semantic Audit｜11 / 11

对 P2 `component_families` 的 11 个 family 完成逐项审计，不直接继承其工程名称作为历史构件名称。

当前必须审计：

- BRACKET_ARM
- BRACKET_CONTACT
- COLUMN
- FRAME_CONTROL
- FRAME_SUPPORT
- GABLE_CONTROL
- GRID_CONTROL
- PRIMARY_FRAME
- PURLIN
- RAFTER
- ROOF_ENVELOPE

每项必须给出：

- P2 engineering meaning；
- P3 ontology type；
- 是否对应真实历史构件；
- 是否需要拆分 / 合并 / 重命名；
- 是否保留为 diagnostic/control only；
- 对应史料或术语依据；
- unresolved boundary。

### DoD-05｜P2 Variant Migration｜40 / 40

对全部 40 个 P2 parametric variants 建立迁移关系：

`P2 variant → P3 component / proxy / control classification → canonical variant record`

不得出现 orphan variant；不得因为重新分类而丢失参数来源、证据等级或可替换性。

### DoD-06｜P2 Instance Migration｜365 / 365

对全部 365 个 stable instances 建立迁移关系：

`P2 instance → P3 component/assembly/proxy/control record + placement + evidence metadata`

必须满足：

- 365/365 可追踪；
- zero orphan instance；
- machine placement 不等于 historical component count；
- 同一构件类型可以对应多个 instances；
- control / envelope instances 不计入历史构件统计。

### DoD-07｜Evidence & Historical Boundary Preservation

P3 Registry 必须继承 P1/P2 evidence-aware 语义，并升级到构件 / 属性级：

- CONFIRMED / HCI / RC / UNKNOWN 不得被构件名称归一化覆盖；
- observed / report ideal / reconstructed candidate 继续分离；
- `Z-006` 保持 UNKNOWN；
- `Z-006-RC-01` 保持独立、可替换；
- `DG-114` 不得升级为统一小斗规格；
- `HIS-002` 构件原真性 unknown 继续保留；
- 45°转角、榫卯、隐角梁等 unresolved 项不得因构件登记而获得虚假精确性。

### DoD-08｜Assembly-ready Relationship Vocabulary

虽然 P3.2 才正式建立 Assembly Relationship Model，但 P3.0 Registry 必须预留统一关系词汇，至少支持：

- supports / supported_by；
- connects_to；
- inserted_into / receives；
- rests_on；
- spans_between；
- aligned_with；
- repeated_in；
- belongs_to_assembly；
- located_at / orientation。

P3.0 只定义关系数据结构和语义，不要求完成全部组合图。

### DoD-09｜Machine-readable Registry + Validation + Product Owner Review

必须形成 canonical machine-readable registry / schema，并通过最小机器校验：

- ID 唯一；
- required fields 完整；
- ontology_type 合法；
- P2 11/40/365 migration coverage 可计算；
- evidence metadata 可追踪；
- 无孤立 variant / instance；
- 不存在把 CONTROL_OBJECT / ENVELOPE 静默登记成历史构件的情况。

最终由 Product Owner 审核：

1. 构件分类是否符合项目目标；
2. 登记字段是否足以回答“名称、种类、作用、3D建模、证据、组合与复用”；
3. 体系是否适合未来扩展到第二座建筑。

## 4. Gate PASS Conditions

P3.0 PASS 必须同时满足：

- DoD 9 / 9 PASS；
- P2 family migration = 11 / 11；
- P2 variant migration = 40 / 40；
- P2 instance migration = 365 / 365；
- orphan family / variant / instance = 0；
- historical component 与 engineering/control object 已明确分离；
- evidence / uncertainty 无静默升级；
- registry schema 可扩展到下一座建筑；
- Product Owner 明确批准。

## 5. Scope Boundary

P3.0 不做：

- 新的高精度构件建模；
- 新增榫卯细节；
- 材质 / 彩画 / 风化表现；
- 整寺扩建；
- 第二座建筑生产；
- 为视觉完整性新增无证据几何。

在本 DoD 已批准并锁定后，允许创建 T-009，但 T-009 仅限 ontology / registry / migration engineering，不得新增 Blender 几何。

## 6. Expected Deliverables

P3.0 最终至少形成：

1. `P3_0_COMPONENT_ONTOLOGY_V001.json/md`；
2. `P3_0_COMPONENT_REGISTRY_SCHEMA_V001.json`；
3. `P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json/md`；
4. `P3_0_COMPONENT_REGISTRY_V001.json`；
5. `P3_0_REGISTRY_VALIDATION_REPORT_V001.md/json`；
6. `P3_0_GATE_REVIEW_YYYY-MM-DD.md`。

这些文件将成为 P3.1 构件 Master / Variant Library 的正式输入。
