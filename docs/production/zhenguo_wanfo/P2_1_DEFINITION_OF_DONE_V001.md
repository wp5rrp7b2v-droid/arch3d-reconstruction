# P2.1｜正式生产参数集锁定｜Definition of Done V001

Status: **LOCKED / PRODUCT OWNER APPROVED**  
Date: 2026-09-12  
Gate: `P2.1｜正式生产参数集锁定｜Formal Production Parameter Set`

## 1. Gate Goal

把 P1 已完成分级的 85 项关键信息迁移为符合 P2.0 Evidence-aware Parameter Schema 的正式 production parameter set，并在进入 P2.2 第一项正式 Blender 几何前，明确每项参数尤其是 UNKNOWN 对几何生成的真实依赖与阻断关系。

P2.1 的核心不是“让所有参数都有数字”，而是建立一套：

- 85/85 可追溯；
- 证据语义不丢失；
- UNKNOWN 不被静默补值；
- 合理补全可独立替换；
- 可被后续 Python / Blender 读取；
- 能明确回答“P2.2 还缺什么”的正式生产输入。

## 2. Non-goals

P2.1 不负责：

- 生成正式 Blender 几何；
- 为未知参数凭视觉经验补数字；
- 把 `observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate` 合并成单一“正确值”；
- 解决所有转角45°节点、榫卯、隐角梁或逐构件原真性问题；
- 宣布“963年原貌已经完全确定”。

## 3. Definition of Done｜9项

### DoD-01｜85 / 85 参数完整迁移

P1.3 的 85 项参数必须全部在正式 production parameter set 或其明确的 metadata / rule representation 中得到唯一映射。

必须满足：

- 85 / 85 有唯一 P1 参数 ID 对应；
- 无遗漏；
- 无重复 ID；
- 不允许只迁移“建模方便”的子集而丢弃 deformation / history / metadata requirement 等非几何信息。

### DoD-02｜证据语义保持一致

每项参数必须保留 P2.0 Schema 所要求的证据语义，至少包括：

- `value`
- `unit`
- `classification`
- `time_layer`
- `source_layer`
- `production_use`
- `blocking_level`
- `source_ids`
- `is_replaceable`
- `notes`

从 P1 分类迁移到 production set 时，不得无记录地改变 classification、time layer、source layer 或 production use。

如确需改变，必须形成显式决策与可追溯理由，不允许静默修正。

### DoD-03｜正式参数集通过机器 Schema 验证

正式 production parameter set 必须：

- 通过 `evidence_aware_parameter_schema_v001.json`；
- 可由现有或等价的 read-only Python reader 正确读取；
- 不包含脱离 Schema 的裸数字生产输入；
- 不依赖 `bpy`；
- 本 Gate 不生成任何正式几何。

### DoD-04｜UNKNOWN 保持未知，并完成几何依赖判定

P1.3 的 UNKNOWN 项不得因进入 production set 而被“补成数字”。

每个 UNKNOWN 必须明确记录其对 P2.2 的依赖状态，至少区分：

- `BLOCKS_P2_2_GEOMETRY`：P2.2 主体结构必须使用该输入；
- `BOUNDED_NON_BLOCKING`：可以保留未知，不阻止 P2.2 中等LOD主体结构；
- `METADATA_ONLY_BLOCK`：不阻止几何生成，但限制原真性或历史声明。

若一个 UNKNOWN 被判定为 `BLOCKS_P2_2_GEOMETRY`，P2.1 **不得直接 PASS**。

解除方法只有两种：

1. 新证据把它提升为有依据的非 UNKNOWN；或
2. Product Owner 明确批准一个新的、独立、可替换、可追溯的 `REASONABLE_COMPLETION` 临时生产候选。

禁止把二手常见尺寸、视觉估计值或“看起来合理”的数字静默写入生产集。

### DoD-05｜建立正式 Geometry Dependency Matrix

必须建立一份独立于历史证据分类的几何依赖矩阵，回答“P2.2 实际会用到什么”。

矩阵至少对全部 85 项给出生产依赖角色，例如：

- `DIRECT_GEOMETRY_INPUT`
- `DERIVED_GEOMETRY_RULE`
- `VALIDATION_REFERENCE`
- `METADATA_ONLY`
- `NOT_USED_IN_P2_2`

并对所有 UNKNOWN 给出 DoD-04 所定义的 blocker 状态与理由。

注意：**几何依赖等级不改变历史证据等级。**

### DoD-06｜REASONABLE_COMPLETION 全部可独立替换

现有 4 项 REASONABLE_COMPLETION，以及 P2.1 如新增的任何临时生产候选，都必须：

- `is_replaceable = true`；
- 独立参数化；
- 保留来源与决策理由；
- 不与 CONFIRMED / HIGH_CONFIDENCE_INFERENCE 混写；
- 后续替换时不要求重写整套证据链或把值烘焙成不可追溯常量。

### DoD-07｜三层语义与构件原真性边界持续保留

必须继续保持：

- `observed_as_measured`
- `report_ideal_model`
- `reconstructed_963_candidate`

三层长期分离，不互相覆盖。

同时把 HIS-002 的逐构件原真性要求继续传递到后续几何 metadata 规则中。P2.1 至少锁定后续构件 metadata 字段/默认策略：

- `historical_state_tag`
- `evidence_class`
- `source_layer`
- `originality_status`

`originality_status` 未有证据时默认 `unknown`，不得因建模完成自动升级为 `963_confirmed`。

### DoD-08｜生产预检可机器执行

必须存在可重复执行的 P2.1 preflight / validation 流程，至少能输出：

- production set 参数总数；
- classification 计数；
- UNKNOWN 清单；
- REASONABLE_COMPLETION 清单；
- Geometry Dependency Matrix 覆盖率；
- `BLOCKS_P2_2_GEOMETRY` 数量；
- Schema validation 结果；
- 三层 time layer 保留检查。

P2.1 Gate Review 不接受只靠人工目测判断 production readiness。

### DoD-09｜版本锁定、Canonical Archive 与 P2.2 Entry Check

P2.1 最终产物必须形成明确版本并进入 GitHub canonical repo，至少包括：

- Formal Production Parameter Set；
- Geometry Dependency Matrix；
- validation / preflight 脚本或等价机器验证；
- P2.1 validation report；
- 最终文件版本与 commit / hash 记录。

P2.1 可获得 PASS 的最终条件：

> **9 / 9 DoD 全部通过，且 P2.2 所需的 geometry-critical unresolved blocker = 0。**

这并不要求所有 UNKNOWN 消失；只要求仍为 UNKNOWN 的项目被明确证明不会阻止 P2.2 受控中等LOD主体结构，或已通过显式 REASONABLE_COMPLETION 决策解除几何阻断。

## 4. Gate Decision Rule

### PASS

仅当 DoD-01～DoD-09 全部 PASS，且没有未处理的 `BLOCKS_P2_2_GEOMETRY`。

### HOLD

出现以下任一情况即 HOLD：

- 85项有遗漏或重复；
- 证据语义迁移发生未解释漂移；
- Schema 验证失败；
- UNKNOWN 被静默赋值；
- Geometry Dependency Matrix 未完成；
- 存在未处理的 geometry-critical UNKNOWN；
- 合理补全不可独立替换；
- 三层语义被覆盖；
- 缺少机器 preflight；
- 正式产物未进入 canonical repo。

## 5. Production Boundary

在 P2.1 PASS 前：

- 不进入 P2.2；
- 不生成第一项正式 Blender 历史复原几何；
- 可进行纯数据、脚本、dependency/preflight 工程验证；
- CG-02～CG-06 全部持续生效。

## 6. Next Engineering Step

DoD 锁定后，下一项实际 Codex 工程任务可创建为 **T-006**，目标应围绕：

- 85/85 formal production parameter migration；
- Geometry Dependency Matrix；
- production preflight / validation；
- P2.1 validation report。

T-006 的具体 Task Contract 另行创建；本 DoD 不等于 T-006 已经启动。
