# P2.3｜整合复原候选与质量验收｜Gate Review｜2026-09-12

Status: **PRELIMINARY / 8 PASS + 1 HOLD — EVIDENCE DIAGNOSTIC CORRECTION REQUIRED**  
Gate: `P2.3｜Integrated Reconstruction Candidate & QC`  
Locked DoD: `docs/production/zhenguo_wanfo/P2_3_DEFINITION_OF_DONE_V001.md`

## 1. Review Conclusion

T-008 V003 已关闭 DoD-07 跨版本往返阻断，ChatGPT 对 canonical GitHub 工程证据完成独立复核，工程主链 PASS。

2026-09-12，Product Owner 上传六张正式 review 图供最终审核。ChatGPT 对六图按 DoD-08 逐项视觉复核后：

- PLAN：PASS
- ELEVATION：PASS
- AXON：PASS
- EXTERIOR_3Q：PASS
- STRUCTURE_DETAIL：PASS
- EVIDENCE_DIAGNOSTIC：**HOLD**

当前结论：

> **P2.3 engineering evidence = PASS**  
> **P2.3 visual set = 5 PASS + 1 HOLD**  
> **P2.3 Gate = NOT PASS**

HOLD 原因不是建筑几何或 Cloud QC，而是当前 Evidence Diagnostic 不能满足锁定 DoD-08 要求的 `confirmed / inference / reasonable completion / unknown-placeholder` 四级证据边界区分。

## 2. Independent Engineering Review

### DoD-01｜Integration Manifest｜PASS

- 正式输入、P2.2 baseline、component definitions、RC/override、bounded UNKNOWN、输出与 QC 环境均已进入 integration / validation evidence。
- V001 frozen candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。

### DoD-02｜Component Library / Variant / Instance Architecture｜PASS

- 正式架构：`Component Library → Parametric Variant → Placement / Instance → Evidence Metadata`。
- 11 component families / 40 variants / 365 stable mesh instances。
- 相同 variant 共享 prototype / mesh data；stable instance ID 与 metadata 映射保留。

### DoD-03｜Integrated Candidate Geometry｜PASS

六图中的 PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL 与 machine QC 共同支持：

- 柱网、主要梁架、斗栱拓扑、檩椽与屋面包络形成连续系统；
- 未发现整族漂浮、明显错向、尺度异常、重复放置或重大断链；
- P2.2 diagnostic / control-only 几何仍与 presentation layer 有明确区分；
- open elevations / gable ends 与简化屋面为已记录 evidence boundary，不作为“历史建筑缺少围护”的声明。

### DoD-04｜Evidence Metadata / Historical Claim Boundaries｜PASS

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK` 保持。
- `Z-006-RC-01` 保持 D-023 可替换候选，不升级为历史事实。
- `DG-114` 未被解释为统一小斗历史规格。
- `HIS-002` 继续限制逐构件原真性；365 instances originality status 保持 unknown。
- 45°转角、榫卯、隐角梁等继续 bounded / schematic。

### DoD-05｜Parameter-driven / Replaceability / No Manual Drift｜PASS

- replacement / mutation tests PASS。
- naked historical constant / manual drift audit PASS。
- 没有依赖不可追溯手工修模获得正式候选。

### DoD-06｜Integrated Machine QC｜PASS

- Local Blender 3.6.23 machine QC：**34 / 34 PASS / 0 errors**。
- stable IDs、family/variant counts、prototype mapping、instance metadata、presentation/diagnostic separation、P2.2 regression 全部 PASS。

### DoD-07｜Deterministic Rebuild + Local/Cloud Compatibility QC｜PASS

- deterministic rebuild / independent reopen：PASS。
- V001 regression：33/33 automated tests PASS；34/34 machine QC PASS。
- GitHub Actions run `34695870243`：SUCCESS。
- Cloud Blender 4.5.13 input / reopen semantic QC：PASS。
- Artifact `P2_3_CLOUD_ROUNDTRIP_V001`：PASS。
- returned `.blend` SHA256：`d2c80c4e2e0ae278ad4b7055df6871e00bfb85ecf981fbc796ddd2f5e919efc0`。
- Local Blender 3.6.23 return semantic QC / 34/34 machine QC：PASS。
- core semantic diff：NONE；仅保留已接受 P0.2 UI-region warning。
- temporary transport / run-trigger tags 已清理。

### DoD-08｜Visual QC / Evidence Diagnostic / Product Owner Review｜HOLD

#### 五张普通结构审核图｜PASS

1. `PLAN`：整体屋面/平面包络规则、对称关系无明显异常；作为整组六图中的平面审核视图可接受。
2. `ELEVATION`：柱—主梁—屋架—屋面关系连续，未见明显高程反转或整族错位。
3. `AXON`：整合建筑系统可读；柱、主要梁架、斗栱拓扑与屋面包络空间关系成立。
4. `EXTERIOR_3Q`：能够读出完整候选体量；未因视觉完整性擅自补入无证据墙体、门窗或装饰。
5. `STRUCTURE_DETAIL`：能够检查柱顶—斗栱/支承—梁架—屋顶的局部链条；未发现新的结构性 HOLD。

#### Evidence Diagnostic｜HOLD

锁定 DoD-08 明确要求 evidence diagnostic 能区分：

- CONFIRMED
- HIGH_CONFIDENCE_INFERENCE
- REASONABLE_COMPLETION
- UNKNOWN / PLACEHOLDER

当前 renderer 实际采用三路逻辑：

- 仅 exact `evidence_class == CONFIRMED` → confirmed color；
- 其余所有非 placeholder → 同一颜色；
- `bounded_placeholder == true` → placeholder color。

因此：

- HIGH_CONFIDENCE_INFERENCE 与 REASONABLE_COMPLETION 被合并；
- mixed evidence class 不能按不确定性等级显示；
- `override_ids`（如 `Z-006-RC-01`）未被显式纳入颜色分类；
- 当前图本身没有四级 legend；
- 图面实际主要形成 broad evidence / placeholder 分层，而不是锁定 DoD 要求的四级证据边界。

这属于 **DoD-08 合规问题**，不是美术偏好问题，因此不能在本版直接批准 P2.3。

修正任务：`docs/tasks/T-008_P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V004.md`。

### DoD-09｜Final Archive / Known Limitations / Closure Evidence｜PASS（engineering archive complete）

- component library、generator / validator / tests、integration manifest、machine QC、roundtrip evidence、validation report、known limitations 与 review images 已归档。
- local-only candidate path / SHA256 / size / Blender version 已记录。
- V004 只允许新增 corrected evidence diagnostic / QC sidecar，不得改变 canonical model。

## 3. Preliminary Gate Score

| DoD | Result |
|---|---|
| DoD-01 | PASS |
| DoD-02 | PASS |
| DoD-03 | PASS |
| DoD-04 | PASS |
| DoD-05 | PASS |
| DoD-06 | PASS |
| DoD-07 | PASS |
| DoD-08 | **HOLD — EVIDENCE DIAGNOSTIC FOUR-LEVEL MAPPING REQUIRED** |
| DoD-09 | PASS |

**Current: 8 PASS + 1 HOLD.**

## 4. Gate Recommendation

> **HOLD P2.3 ONLY FOR EVIDENCE DIAGNOSTIC CORRECTION.**

冻结全部已通过的模型与工程结果。执行 T-008 V004，只修正 Evidence Diagnostic 四级分类和 legend；新版 diagnostic 通过 ChatGPT + Product Owner 复核并由 Product Owner 明确批准后，才可形成 9/9 PASS、关闭 P2.3 与 P2。
