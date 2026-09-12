# 【中国古建筑3D复原｜T-006｜P2_1_PRODUCTION_PARAMETER_SET_V002｜Z-006批准候选接入与阻断清零验证】

Status: READY_FOR_LOCAL_EXECUTION  
Think Level: HIGH  
Phase/Gate: P2 / P2.1  
Date: 2026-09-12  
Continuation of: `T-006_P2_1_PRODUCTION_PARAMETER_SET_V001.md`

## 1. Why V002

T-006 V001 已完成：

- Formal Production Parameter Set：85 / 85；
- Geometry Dependency Matrix：85 / 85；
- Machine validation：PASS；
- Automated tests：11 / 11 PASS；
- Production preflight：HOLD；
- 唯一 geometry-critical unresolved blocker：`Z-006 / column_height_963_design_mm`。

Product Owner 已通过 `D-023` 批准一个独立、可替换的生产候选：

`Z-006-RC-01 = 11 × MOD-006`

当前 `MOD-006 ≈ 321.3 mm`，因此当前解析值：

`11 × 321.3 = 3534.3 mm`

本任务目标没有改变，仍然是完成 P2.1 正式生产参数基线与 preflight，因此继续使用 **T-006**，版本升级为 **V002**，不创建 T-007。

## 2. Hard Semantic Boundary

必须同时满足以下两件事：

1. `Z-006 / column_height_963_design_mm` 继续保持：
   - `classification = UNKNOWN`
   - `value = null`
   - `production_use = DO_NOT_LOCK`
   - dependency status 继续为 `BLOCKS_P2_2_GEOMETRY`

2. `Z-006-RC-01` 作为**独立 production override / REASONABLE_COMPLETION**存在：
   - 不覆盖 Z-006；
   - 不改变原85项历史/证据参数的 ID、分类或数量；
   - 可替换、可追溯、可重新计算；
   - 仅用于 `reconstructed_963_candidate` 的 P2.2 生产输入。

严禁把 3534.3mm 写回 Z-006 本体或描述为“963年原设计柱高已证实”。

## 3. Authoritative Inputs

只以以下仓库内已批准材料为依据：

- `docs/project_control/decision_log.md` 中 `D-023`
- `docs/production/zhenguo_wanfo/P2_1_DEFINITION_OF_DONE_V001.md`
- `docs/tasks/T-006_P2_1_PRODUCTION_PARAMETER_SET_V001.md`
- `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
- `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
- `production/zhenguo_wanfo/validation/P2_1_VALIDATION_REPORT_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md` 中 E-018
- `docs/evidence/zhenguo_wanfo/P1_3_HIGH_RISK_CLASSIFICATION_V001.md` 中 HR-01A / HR-01B

不得使用外部知识重新发明柱高参数，不得自行更改 D-023 的 11×MOD-006 决策。

## 4. Scope

允许创建或修改：

- `production/zhenguo_wanfo/params/`
- `production/zhenguo_wanfo/scripts/`
- `production/zhenguo_wanfo/tests/`
- `production/zhenguo_wanfo/validation/`

必要时可只读使用：

- `production/zhenguo_wanfo/dependency/`
- P1 / P2.0 / Project Control 已批准文件

禁止修改：

- `docs/project_control/*`
- P1 evidence / classification 文件
- P2.0 Schema 及 Schema 说明
- `P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json` 中 Z-006 的 UNKNOWN/null/DO_NOT_LOCK 语义
- `P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json` 中 Z-006 的 `BLOCKS_P2_2_GEOMETRY` 历史依赖判断
- P0 POC 文件
- Blender `.blend / .blend1`
- 已知 local-only PDF 与其他 untracked 本地资产

禁止启动 Blender、导入 `bpy` 或生成任何正式建筑几何。

## 5. Required Deliverables

### A. Approved Production Override Sidecar

创建：

`production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`

该文件至少包含一个且仅包含本轮批准候选 `Z-006-RC-01`，字段至少包括：

- `candidate_id`: `Z-006-RC-01`
- `target_parameter_id`: `Z-006`
- `target_parameter_key`: `column_height_963_design_mm`
- `classification`: `REASONABLE_COMPLETION`
- `time_layer`: `reconstructed_963_candidate`
- `production_use`: `DEFAULT_REPLACEABLE_CANDIDATE`
- `formula`: `11 * MOD-006`
- `depends_on`: [`MOD-006`]
- `multiplier`: 11
- `unit`: `mm`
- `current_resolved_value`: 3534.3
- `is_replaceable`: true
- `approval_decision_id`: `D-023`
- `status`: `APPROVED_FOR_P2_2_CANDIDATE_USE`
- `evidence_basis`: 至少引用 E-018、HR-01A 与 D-023
- `historical_claim_boundary`: 明确该值不是已证实963历史事实

允许增加必要 metadata，但不得引入新的历史参数命题。

### B. Formula-driven Resolution

不得把 3534.3 当作脱离来源的裸常数使用。

验证脚本必须：

1. 从 Formal Production Parameter Set 读取 `MOD-006`；
2. 读取其当前值；
3. 按 `multiplier = 11` 计算 RC-01；
4. 验证结果与 sidecar 的 `current_resolved_value` 一致；
5. 若 MOD-006 改变，RC-01 应可重新计算并使旧 resolved value 校验失败，避免静默漂移。

### C. Preserve Z-006 Historical Unknown

V002 必须机械验证：

- Z-006 仍是 UNKNOWN；
- Z-006 `value = null`；
- Z-006 `production_use = DO_NOT_LOCK`；
- Z-006 dependency status 仍为 `BLOCKS_P2_2_GEOMETRY`；
- 不允许把 RC-01 合并进 Z-006；
- 原正式参数集仍保持85/85，classification counts仍为46/32/4/3。

注意：RC-01 是**额外的批准 production override**，不改变 P1.3 的85项分类计数。

### D. Update Production Preflight

更新：

`production/zhenguo_wanfo/scripts/p2_1_production_preflight.py`

Preflight 必须区分：

- `geometry_critical_historical_unknown_count`
- `approved_candidate_resolution_count`
- `geometry_critical_unresolved_blocker_count`

在当前批准基线下，预期：

- historical unknown = 1（Z-006仍未知）；
- approved candidate resolution = 1（Z-006-RC-01）；
- unresolved blocker = 0；
- production preflight = PASS。

只有当 approved candidate 完整、可验证、可重算且与 D-023 一致时，才能把 unresolved blocker 降为0。

### E. Machine Validation / Negative Checks

扩展验证，使以下任一情况均 FAIL / HOLD：

- Z-006 被写入任何数值；
- Z-006 不再是 UNKNOWN / DO_NOT_LOCK；
- Z-006 dependency 被改为 non-blocking；
- RC-01 缺失；
- `approval_decision_id != D-023`；
- `classification != REASONABLE_COMPLETION`；
- `is_replaceable != true`；
- formula / multiplier 不是 D-023 批准的 11×MOD-006；
- depends_on 不是 MOD-006；
- resolved value 与 MOD-006×11 不一致；
- RC-01 被算入原85项 classification counts；
- preflight 在无合法批准候选时仍返回 PASS。

### F. Automated Tests

继续使用并扩展：

`production/zhenguo_wanfo/tests/test_p2_1_production_parameter_set_v001.py`

或创建明确 V002 测试文件。

要求：

- V001 11/11 regression 全部继续 PASS；
- 增加 RC-01 正向与 mutation tests；
- 测试必须证明 preflight PASS 是由有效批准候选真实解除“unresolved”状态，而不是修改 UNKNOWN / dependency 状态获得。

### G. Validation Report V002

创建：

`production/zhenguo_wanfo/validation/P2_1_VALIDATION_REPORT_V002.md`

至少报告：

- Python / jsonschema 版本；
- V001 regression；
- Formal Parameter Set 仍为85/85；
- 原 classification counts仍为46/32/4/3；
- Z-006 UNKNOWN/null/DO_NOT_LOCK preservation；
- Z-006 dependency preservation；
- RC-01 sidecar validation；
- MOD-006 当前值；
- formula recomputation result；
- RC-01 resolved value；
- approved candidate resolution count；
- geometry-critical historical unknown count；
- geometry-critical unresolved blocker count；
- automated tests；
- production preflight；
- files created/modified；
- final engineering recommendation PASS / HOLD。

## 6. V002 Engineering PASS Logic

T-006 V002 可给出 engineering recommendation = PASS 仅当全部满足：

1. V001 全部有效成果保持通过；
2. Formal Parameter Set 仍为85/85且历史语义无漂移；
3. Z-006 仍 UNKNOWN/null/DO_NOT_LOCK；
4. Z-006 dependency 仍 `BLOCKS_P2_2_GEOMETRY`；
5. RC-01 独立存在并符合 D-023；
6. RC-01 由 MOD-006×11 动态验证，当前结果为3534.3mm；
7. RC-01 `is_replaceable=true`；
8. automated tests 全部 PASS；
9. production preflight PASS；
10. `geometry-critical unresolved blocker count = 0`；
11. 无 Blender / bpy / 正式几何生成。

即使 V002 engineering PASS，也**不要宣布 P2.1 Gate PASS**。ChatGPT + Product Owner 保留 Gate Review / Approval 权限。

## 7. Git / Archive Rules

开始前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git pull --ff-only origin main
```

若无法正常同步，停止并报告，不在旧基线执行。

完成后只 add T-006 V002 scope 内文件；不得 add 已知 local-only PDF、P0目录或 `.blend`。

建议 commit message：

`p2.1: validate approved Z-006 candidate`

只允许 normal fast-forward push；失败则报告并停止，不得 force。

## 8. Final Report Format

返回：

- STATUS: PASS / HOLD
- Python version
- jsonschema version
- V001 regression result
- Formal parameter set: n/85
- Classification counts
- Z-006 historical parameter state
- Z-006 dependency state
- RC-01 candidate validation
- MOD-006 current value
- RC-01 formula / resolved value
- Historical geometry-critical unknown count
- Approved candidate resolution count
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
