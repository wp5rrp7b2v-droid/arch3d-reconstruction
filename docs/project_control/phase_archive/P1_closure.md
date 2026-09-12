# P1 Closure｜ARCH3D-001

Status: CLOSED / APPROVED / CONDITIONAL GO  
Date: 2026-09-12  
Phase: `P1｜选题取证`  
Formal case: 山西平遥镇国寺万佛殿

## Final Gate Result

| Gate | Result |
|---|---|
| P1.0｜选题标准锁定 | PASS |
| P1.1｜候选案例比较与定选 | PASS |
| P1.2｜正式证据包建立 | PASS |
| P1.3｜证据分级与可复原性 Go / No-Go | PASS / CONDITIONAL GO |

**P1 Gate Final：4 / 4 PASS。**

Product Owner 于 2026-09-12 正式批准 `P1.3｜CONDITIONAL GO`。

## P1 Final Conclusion

现有证据足以支持进入正式参数化与3D候选复原，但该结论只允许建立“带证据等级、可替换合理补全项、显式保留未知项”的候选复原，不代表963年全部历史参数已经确定，也不代表最终模型可宣称为“完全还原963原貌”。

P1.3 全量关键参数分类：

- CONFIRMED：46
- HIGH_CONFIDENCE_INFERENCE：32
- REASONABLE_COMPLETION：4
- UNKNOWN：3
- TOTAL：85

## Conditional Go Carry-forward Rules

以下规则跨阶段继续强制生效：

1. `CG-01`｜第一项正式几何生产前必须建立 Evidence-aware Parameter Schema；
2. `CG-02`｜UNKNOWN / DO_NOT_LOCK 不得静默硬编码；
3. `CG-03`｜REASONABLE_COMPLETION 必须独立参数化、可替换、可追踪；
4. `CG-04`｜`observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 长期分层；
5. `CG-05`｜转角45°精确节点等未知项只允许中等LOD拓扑骨架，不得声明历史精确复原；
6. `CG-06`｜逐构件原真性不足时，禁止“完全还原963原貌 / 全部963原构”等过度真实性声明。

## Unresolved but Bounded Items

- 963原设计柱高；
- 小斗统一规格设计规则；
- 逐构件963原真性；
- 转角45°精确节点与榫卯落位；
- 隐衬角栿 / 隐角梁来源冲突。

上述问题均有明确阻断范围，不构成全项目 No-Go。

## P2 Entry

P1 关闭后，项目进入 `P2｜正式参数化与3D复原`。

P2 的第一项强制 Gate：

`P2.0｜Evidence-aware Parameter Schema`

目标：把 P1 的证据分级真正转化为机器可读、可追踪、可替换的生产参数结构。**P2.0 PASS 前不得启动第一项正式 Blender 几何生产。**

后续 P2.1–P2.3 的完整 Gate 架构可在 P2.0 启动后依据生产依赖进一步锁定，不在 P1 Closure 中提前扩张范围。

## Canonical Evidence

- `docs/evidence/zhenguo_wanfo/P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`
- `docs/evidence/zhenguo_wanfo/P1_3_HIGH_RISK_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md`
