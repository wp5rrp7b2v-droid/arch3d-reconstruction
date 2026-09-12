# 【中国古建筑3D复原｜T-008｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V004｜Evidence Diagnostic 四级证据映射修正与最终视觉复核】

Status: **READY_FOR_LOCAL_EXECUTION / CONTINUATION AFTER VISUAL REVIEW HOLD**  
Think Level: **MEDIUM**  
Phase/Gate: P2 / P2.3  
Date: 2026-09-12

## 1. Objective

继续 T-008 原任务目标，不创建新的 T-###。

T-008 V003 已完成全部工程 QC 与 DoD-07 跨版本往返，ChatGPT 独立工程复核通过。Product Owner 最终六图审核前，ChatGPT 对六张正式 review 图执行 DoD-08 视觉复核：PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL 均无新的结构性 HOLD；但 `EVIDENCE_DIAGNOSTIC` 不能按锁定 DoD 清晰区分 `confirmed / inference / reasonable completion / unknown-placeholder` 四类边界，因此 DoD-08 HOLD。

V004 唯一目标：

> **在完全冻结 V001 canonical `.blend`、构件库、几何、实例映射、工程 QC、DoD-07 roundtrip 证据的前提下，重新生成一个真正满足 DoD-08 的四级 Evidence Diagnostic 可视化，并完成回归核对。**

不得借本轮修改任何建筑几何、历史参数、Component Library、variant、instance placement、roundtrip 结果或已通过的五张普通结构审核图。

## 2. Frozen Baseline

必须保持：

- canonical candidate：`production/zhenguo_wanfo/output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend`
- canonical SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`
- 11 component families / 40 variants / 365 stable mesh instances
- automated tests：33/33 PASS
- machine QC：34/34 PASS
- T-008 V003 Cloud Blender 4.5.13 roundtrip：PASS
- returned Local Blender 3.6.23 QC：PASS / core semantic diff NONE
- historical boundaries：Z-006 UNKNOWN；Z-006-RC-01 replaceable；DG-114 / HIS-002 / 45° corner / mortise / hidden-angle boundaries unchanged
- PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL：不修改

不得重建或覆盖 canonical V001 `.blend`。

## 3. Exact Defect

当前 `generate_p2_3_integrated_reconstruction_v001.py` 的 diagnostic render 使用三路颜色逻辑：

- exact `evidence_class == CONFIRMED` → confirmed color
- 非 placeholder 的其他所有情况 → 同一颜色
- `bounded_placeholder == true` → placeholder color

该逻辑会把 HIGH_CONFIDENCE_INFERENCE、REASONABLE_COMPLETION、包含多种 evidence class 的实例合并；同时没有显式使用 `override_ids` 识别 `Z-006-RC-01` 等 RC 依赖。因此不能满足锁定 DoD-08 要求的四级证据边界区分。

本轮不得修改原 P2.3 geometry generator 来重新生成模型；应建立独立、只读式 review renderer / diagnostic utility，从 canonical `.blend` + Integration Manifest 生成新版 diagnostic。

## 4. Required Classification Logic

新版 evidence diagnostic 至少明确区分四类，并采用“最高不确定性优先”的保守映射：

1. **UNKNOWN / PLACEHOLDER**
   - `bounded_placeholder == true`；或 manifest 明确为 UNKNOWN / unresolved placeholder。
2. **REASONABLE_COMPLETION / APPROVED OVERRIDE**
   - `override_ids` 非空（例如 `Z-006-RC-01`）；或 evidence metadata 含 `REASONABLE_COMPLETION`。
3. **HIGH_CONFIDENCE_INFERENCE**
   - evidence metadata 含 `HIGH_CONFIDENCE_INFERENCE`，且未命中更高不确定性类别。
4. **CONFIRMED**
   - 仅在没有上述更高不确定性条件，且 evidence metadata 为 confirmed 时进入。

对于混合 evidence class，必须按：

`UNKNOWN/PLACEHOLDER > REASONABLE_COMPLETION > HIGH_CONFIDENCE_INFERENCE > CONFIRMED`

进行显示，禁止把混合类降格为 confirmed。

分类必须以 `P2_3_INTEGRATION_MANIFEST_V001.json` 的实例记录 / stable instance ID 为 authoritative mapping，避免只依赖 Blender object 上可能不完整的单一 `evidence_class` 字符串。

## 5. Visual Output Requirement

新增正式输出，建议：

`production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_EVIDENCE_DIAGNOSTIC_V002.png`

要求：

- 使用与原 diagnostic 等价或更清晰的整体视角；
- 四类必须使用明显不同、可区分的系统色；
- **图内必须包含 legend**，至少明确写出：
  - CONFIRMED
  - HIGH CONFIDENCE INFERENCE
  - REASONABLE COMPLETION
  - UNKNOWN / PLACEHOLDER
- 不允许用材质美化掩盖分类；
- diagnostic-only grid/control geometry 可以显示，但其类别必须符合 manifest / placeholder metadata；
- 不修改正式 presentation model。

## 6. Machine / Regression Checks

至少验证：

- canonical `.blend` SHA256 未变；
- component family / variant / stable instance counts 未变：11 / 40 / 365；
- 33/33 tests 不回退；
- 34/34 machine QC 不回退；
- DoD-07 roundtrip evidence 不变且无需重跑；
- 新 diagnostic 中每个被显示的 stable instance 能唯一映射到 manifest；
- 四个 legend 类别全部由代码显式支持；
- 若某一类别在当前模型中实例数为 0，也必须保留 legend，并在 sidecar summary 中记录 count=0；
- 输出 sidecar JSON，记录四类 instance count、分类优先级、输入 manifest SHA256 与 diagnostic PNG SHA256。

建议 sidecar：

`production/zhenguo_wanfo/validation/P2_3_EVIDENCE_DIAGNOSTIC_V002_QC.json`

## 7. PASS / HOLD

V004 可建议 PASS 仅当：

- 四级证据分类逻辑与 manifest 一致；
- RC / override 可被独立识别；
- placeholder / UNKNOWN 不被误显示为 inference / confirmed；
- 图内 legend 清楚；
- canonical model 与全部工程证据未发生变化；
- 回归 tests / machine QC 不退化；
- 新 diagnostic 与 sidecar evidence 进入 canonical GitHub。

任何 geometry / instance / parameter 变化，或仍无法区分四级证据边界 = HOLD。

V004 PASS 仍不等于 P2.3 Gate PASS。完成后必须重新由 ChatGPT + Product Owner 审核新版 evidence diagnostic，并由 Product Owner 明确批准 P2.3 Gate。

## 8. Final Report

返回：

- STATUS: PASS / HOLD
- canonical candidate SHA256 before / after
- family / variant / instance regression
- automated tests / machine QC regression
- new renderer / utility path
- diagnostic V002 path / SHA256
- sidecar QC path / SHA256
- four category counts
- classification precedence implementation
- legend verification
- geometry changed? YES/NO（必须 NO）
- canonical Git commit SHA / push result
- `git status --short`
- exact blocker if HOLD
- engineering recommendation

不得自行宣布 P2.3 Gate PASS 或 P2 Phase CLOSED。
