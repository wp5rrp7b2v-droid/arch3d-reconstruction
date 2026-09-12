# 【中国古建筑3D复原｜T-006｜P2_1_PRODUCTION_PARAMETER_SET_V001｜正式生产参数集建立与几何依赖预检】

Status: READY_FOR_LOCAL_EXECUTION  
Think Level: HIGH  
Phase/Gate: P2 / P2.1  
Date: 2026-09-12

## 1. Objective

完成 P2.1 的核心工程工作：

1. 将 P1 已锁定的 85/85 参数迁移为符合 P2.0 Evidence-aware Parameter Schema 的正式 production parameter set；
2. 为 85/85 参数建立独立的 Geometry Dependency Matrix，明确其在 P2.2 主体结构几何中的真实角色；
3. 对所有 UNKNOWN 明确阻断等级；
4. 建立机器可执行 production preflight；
5. 形成 P2.1 validation report。

本任务**不得生成任何正式 Blender 几何**。

T-006 的目标是让 P2.1 可被 Gate Review，而不是提前进入 P2.2。

## 2. Authoritative Inputs

只以仓库内已批准材料为依据，不使用外部知识补参数：

- `docs/production/zhenguo_wanfo/P2_1_DEFINITION_OF_DONE_V001.md`
- `docs/production/zhenguo_wanfo/P2_0_EVIDENCE_AWARE_PARAMETER_SCHEMA_V001.md`
- `production/zhenguo_wanfo/schema/evidence_aware_parameter_schema_v001.json`
- `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`
- `docs/evidence/zhenguo_wanfo/P1_3_HIGH_RISK_CLASSIFICATION_V001.md`
- 上述文件明确引用的正式证据来源。

若输入之间存在冲突、缺失或无法唯一映射，**不得自行调和或猜测**；记录 blocker 并返回 HOLD。

## 3. Scope

允许创建或修改：

- `production/zhenguo_wanfo/params/`
- `production/zhenguo_wanfo/dependency/`
- `production/zhenguo_wanfo/scripts/`
- `production/zhenguo_wanfo/tests/`
- `production/zhenguo_wanfo/validation/`

禁止修改：

- `docs/project_control/*`
- P1 evidence / classification 文件
- P2.0 已批准 Schema 及 Schema 说明
- P0 POC 文件
- Blender `.blend / .blend1`
- 已知 local-only PDF 与其他 untracked 本地资产

禁止启动 Blender、导入 `bpy`、生成任何正式建筑几何。

## 4. Required Deliverables

### A. Formal Production Parameter Set

创建：

`production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`

必须满足：

- 恰好 85 个唯一 `parameter_key`；
- key 集合与 P1.3 已锁定 85 项一一对应，不得遗漏、合并或新增历史参数；
- classification 计数保持：
  - CONFIRMED = 46
  - HIGH_CONFIDENCE_INFERENCE = 32
  - REASONABLE_COMPLETION = 4
  - UNKNOWN = 3
- 每项均符合 P2.0 Schema；
- 保留并正确填写 `value / unit / classification / time_layer / source_layer / production_use / blocking_level / source_ids / is_replaceable / notes`；
- 不得将 `CONFIRMED` 自动解释为“963原始设计事实”；
- 不得把 `observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate` 互相转换；
- UNKNOWN 保持 `value = null` 且不得静默 hard-lock；
- REASONABLE_COMPLETION 必须 `is_replaceable = true`；
- 不得为了让参数集“完整”而创造 P1 未支持的数值、单位、构造关系或原真性结论。

若 P1 对某项只支持文字/关系性表达，不得擅自转换成伪精确数值；只采用已锁定材料明确支持的生产表示。

### B. Geometry Dependency Matrix

创建：

`production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`

必须恰好覆盖同一 85 个 `parameter_key`，每项至少包含：

- `parameter_key`
- `geometry_dependency_role`
- `p2_2_target`
- `requires_numeric_value`
- `unknown_dependency_status`
- `blocking_reason`
- `resolution_required_before_p2_2`
- `notes`

`geometry_dependency_role` 只允许：

- `DIRECT_GEOMETRY_INPUT`
- `DERIVED_GEOMETRY_RULE`
- `VALIDATION_REFERENCE`
- `METADATA_ONLY`
- `NOT_USED_IN_P2_2`

对 UNKNOWN，`unknown_dependency_status` 必须明确为以下之一：

- `BLOCKS_P2_2_GEOMETRY`
- `BOUNDED_NON_BLOCKING`
- `METADATA_ONLY_BLOCK`

对非 UNKNOWN，不得伪造 UNKNOWN blocker 状态。

依赖判断必须以**P2.2 已批准范围**为准：柱网、柱、主要梁架、斗栱拓扑骨架、屋顶控制几何及主要空间关系。不得因为未来可能有用，就把所有参数都判为直接几何输入。

### C. UNKNOWN Hard Boundary

对所有 UNKNOWN：

- 若它是 P2.2 必须的直接/派生几何输入，且没有可合法读取的值，则必须标记 `BLOCKS_P2_2_GEOMETRY`；
- 不得跳过该参数以获得 PASS；
- 不得自行新增临时数值；
- 不得自行把 UNKNOWN 改成 REASONABLE_COMPLETION。

如确需临时建模值，T-006 只报告“需要 Product Owner 决策”；由 ChatGPT + Product Owner 形成显式决策后，再在同一 T-006 的后续版本中处理。

### D. Machine Validation

创建或扩展只读验证脚本，至少实现：

1. Formal Parameter Set 通过 P2.0 Schema；
2. 参数总数 = 85；
3. 参数 key 唯一；
4. 与锁定 key 清单一一对应；
5. classification 计数 = 46 / 32 / 4 / 3；
6. UNKNOWN 全部 `value=null`；
7. REASONABLE_COMPLETION 全部可替换；
8. 三个 `time_layer` 标签不被 merge / overwrite / relabel；
9. Geometry Dependency Matrix = 85 项且 key 集合完全相同；
10. UNKNOWN 均有合法 dependency status；
11. 若存在 `BLOCKS_P2_2_GEOMETRY`，preflight 必须返回 HOLD / 非零 blocker count；
12. 无 `bpy`，无 Blender 几何生成。

推荐脚本：

- `production/zhenguo_wanfo/scripts/validate_p2_1_parameter_set.py`
- `production/zhenguo_wanfo/scripts/p2_1_production_preflight.py`

### E. Automated Tests

创建：

`production/zhenguo_wanfo/tests/test_p2_1_production_parameter_set_v001.py`

至少验证：

- 85/85 completeness；
- exact key-set equality；
- classification counts；
- Schema PASS；
- UNKNOWN null / dependency classification；
- REASONABLE_COMPLETION replaceability；
- three-layer preservation；
- dependency matrix one-to-one coverage；
- preflight blocker logic；
- no `bpy` / no geometry generation。

测试不得通过 hard-code “PASS” 绕过真实输入检查。

### F. Validation Report

创建：

`production/zhenguo_wanfo/validation/P2_1_VALIDATION_REPORT_V001.md`

至少报告：

- Python / jsonschema 版本；
- production parameter count；
- classification counts；
- Schema validation result；
- dependency matrix coverage；
- UNKNOWN 逐项 dependency status；
- geometry-critical unresolved blocker count；
- REASONABLE_COMPLETION replaceability result；
- three-layer preservation result；
- automated test result；
- files created/modified；
- final engineering recommendation：PASS / HOLD。

## 5. P2.1 PASS Logic

T-006 可给出 engineering recommendation = PASS 仅当同时满足：

1. P2.1 Definition of Done 9/9 可被工程证据支持；
2. Formal Parameter Set = 85/85；
3. Geometry Dependency Matrix = 85/85；
4. 所有机器验证和自动化测试 PASS；
5. `geometry-critical unresolved blocker count = 0`；
6. 无静默补值、无 evidence semantics 漂移；
7. 无 Blender 几何生成。

若 blocker count > 0：

- T-006 返回 **HOLD**；
- 精确列出 blocker parameter_key 与原因；
- 不得为追求 PASS 自行填值。

T-006 的工程结论不等于 P2.1 Gate PASS。ChatGPT + Product Owner 保留 Gate Review / Approval 权限。

## 6. Git / Archive Rules

开始前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git pull --ff-only origin main
```

若无法正常同步，停止并报告，不在旧基线执行。

完成后只 add T-006 scope 内文件；不得 add 已知 local-only PDF、P0 目录或 `.blend`。

建议 commit message：

`p2.1: build formal production parameter set`

只允许 normal fast-forward push；失败则报告并停止，**不得 force**。

## 7. Final Report Format

返回：

- STATUS: PASS / HOLD
- Python version
- jsonschema version
- Formal parameter set: n/85
- Classification counts
- Dependency matrix: n/85
- UNKNOWN dependency status（逐项）
- Geometry-critical unresolved blocker count
- Automated tests result
- Production preflight result
- Files created/modified
- Commit SHA
- Push result
- `git status --short`
- blocker（如有）
- engineering recommendation

不要声明 P2.1 Gate PASS。
