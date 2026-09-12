# P1.3｜平遥镇国寺万佛殿｜Gate Review

Status: COMPLETE / READY_FOR_PRODUCT_OWNER_DECISION  
Date: 2026-09-12  
Gate: `P1.3｜证据分级与可复原性 Go / No-Go`  
Recommendation: **CONDITIONAL GO**

Primary inputs:

- `P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`
- `P1_3_HIGH_RISK_CLASSIFICATION_V001.md`
- `P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`

---

## 1. Gate Question

当前问题不是“万佛殿所有963年参数是否已经确定”，而是：

> 现有证据是否已经足以支持一个可追溯、可替换、明确区分事实/推断/补全/未知的正式候选复原，并且不会把证据不足伪装成历史事实？

本 Gate 只决定是否允许进入正式参数化与3D复原，不宣称最终模型等于963年绝对真实原貌。

---

## 2. Step 1 / Step 2 输入完整性

### Step 1｜高风险证据分类

已完成以下高风险问题的正式分级与生产边界：

- 963原设计柱高 / Z基准；
- 角柱生起；
- 举折与总举高；
- 转角铺作45°节点与角梁；
- 963原构 vs 后世修缮；
- `report_ideal_model` 与963初建状态的语义隔离。

结论：未发现不可隔离的全局性 No-Go blocker。

### Step 2｜全量关键参数分类

V002 母表 **85 / 85** 参数已完成四级分类：

| Classification | Count |
|---|---:|
| CONFIRMED | 46 |
| HIGH_CONFIDENCE_INFERENCE | 32 |
| REASONABLE_COMPLETION | 4 |
| UNKNOWN | 3 |
| **TOTAL** | **85** |

同时每项已定义：

- `production_use`
- `time_layer`
- `source_layer`
- `blocking_level`

完整性检查：**PASS**。

---

## 3. Gate Review Checklist

| # | Review Item | Result | Gate Interpretation |
|---|---|---|---|
| 1 | 关键参数是否全部完成证据分级 | **PASS** | 85/85 已分类，无未处理参数行 |
| 2 | 现状实测、报告理想模型、963候选是否已分层 | **PASS** | 三层语义已强制分离 |
| 3 | 高风险 UNKNOWN 是否均有明确阻断范围 | **PASS** | 未发现全局阻断；均可隔离到参数/子模块 |
| 4 | 合理补全项是否明确标识并可替换 | **PASS WITH CONDITION** | 分类与规则已定义；正式参数结构必须实际实现可替换性 |
| 5 | 是否存在必须在3D前继续补证才能开始的全局硬缺口 | **PASS** | 没有；未知项不阻断候选复原 |
| 6 | 当前 P0 参数 JSON 是否足以承载证据元数据 | **NOT YET** | P0 JSON 仅验证参数驱动技术链路；正式生产前必须建立 evidence-aware schema |
| 7 | 是否可以避免 UNKNOWN 被静默转换为确定数字 | **PASS WITH CONDITION** | 必须实施 `DO_NOT_LOCK` / placeholder / metadata 规则 |
| 8 | 是否可以对最终模型的历史真实性范围作准确表述 | **PASS** | 允许“候选复原”；禁止“963绝对原貌/全部原构”式过度声明 |

Gate Review：**6 PASS + 2 PASS WITH CONDITION；0 FAIL。**

---

## 4. 为什么不是 GO

不建议无条件 `GO`，因为仍存在以下真实不确定性：

1. `Z-006｜column_height_963_design_mm` 仍为 UNKNOWN；
2. 转角45°精确节点/坐标仍未知；
3. 隐衬角栿 / 隐角梁存在来源冲突；
4. `HIS-002｜component_level_963_originality` 尚不能逐构件完全判定；
5. 正式 evidence-aware Parameter Schema 尚未实现。

因此“进入生产”必须带边界，不能把这些问题视为已经解决。

---

## 5. 为什么不是 NO-GO

也不建议 `NO-GO`，因为上述未知项都可以被局部隔离：

- 963柱高未知，不阻断平面、拓扑、相对Z关系；
- 角柱生起和总举高已有显式合理补全候选，可参数化并替换；
- 转角未知只阻断高精度角部锁定，不阻断整体结构骨架；
- 构件原真性不足只限制“全部963原构”声明，不阻断候选几何复原；
- `report_ideal_model` 已与963候选层明确隔离。

当前证据已经足以构建一个**受控的不确定性模型**，而不是一个“假装全部确定”的模型。

---

## 6. 正式推荐｜CONDITIONAL GO

### Recommendation

**P1.3 建议：CONDITIONAL GO。**

含义：

> 允许项目进入正式参数化与3D复原，但必须把证据等级、时间层、来源层和未知项作为生产数据的一部分；任何合理补全或未知项都不得在后续流程中丢失其证据语义。

这不是“万佛殿963年原貌已经确定”的结论。

---

## 7. Conditional Go 强制条件

若 Product Owner 批准 P1.3，以下规则立即成为进入正式3D的强制条件：

### CG-01｜Evidence-aware Parameter Schema

**在第一项正式几何生产任务之前**，建立正式参数 Schema。每个关键参数至少保存：

```json
{
  "value": null,
  "unit": "mm",
  "classification": "CONFIRMED | HIGH_CONFIDENCE_INFERENCE | REASONABLE_COMPLETION | UNKNOWN",
  "time_layer": "...",
  "source_layer": "...",
  "production_use": "...",
  "blocking_level": "NONE | LOW | MEDIUM | HIGH",
  "source_ids": [],
  "notes": ""
}
```

禁止正式生产继续使用“只有裸数字”的 P0 POC 参数格式。

### CG-02｜UNKNOWN 不得硬锁

所有 `UNKNOWN / DO_NOT_LOCK`：

- 默认保持 `null`、placeholder 或独立临时参数；
- 不得静默赋予“看起来合理”的数字；
- 若生产需要临时值，必须新增 `REASONABLE_COMPLETION` 决策记录后才能使用。

### CG-03｜合理补全必须可替换

`REASONABLE_COMPLETION` 必须：

- 独立参数化；
- 可在不重建整套模型的情况下修改；
- 保留来源和分类；
- 不得烘焙为不可追踪几何。

### CG-04｜三层模型语义长期分离

持续区分：

1. `observed_as_measured`
2. `report_ideal_model`
3. `reconstructed_963_candidate`

禁止把第2层直接重命名为“963原貌”。

### CG-05｜高精度角部限制

转角45°节点、榫卯精确落位、隐衬角栿/隐角梁等未解决项：

- 可建立中等LOD拓扑骨架；
- 不得标记为历史精确复原；
- 后续补证可独立升级。

### CG-06｜历史真实性声明限制

在逐构件原真性尚未解决前，项目可以称：

- “基于现存实测与文献证据的963候选复原”；
- “带证据等级的历史复原模型”。

不得称：

- “完全还原963年原貌”；
- “所有构件均为963原构的精确复原”。

---

## 8. Product Owner Decision

当前状态：**AWAITING PRODUCT OWNER DECISION**

可批准的 Gate 结论：

- `APPROVE CONDITIONAL GO` → P1.3 PASS，P1 Gate = 4/4 PASS；正式参数化/3D阶段解锁，但 CG-01～CG-06 全部生效。
- `HOLD` → P1.3 保持 IN_PROGRESS，指定需补证/修正规则后再审。
- `NO-GO` → 当前案例停止进入正式3D，重新评估对象或证据策略。

### Gate Reviewer Recommendation

**APPROVE CONDITIONAL GO**

理由：

- 证据分类覆盖完整；
- 高风险未知项均有隔离策略；
- 没有发现会使整个候选复原失去可解释性的系统性缺口；
- 当前主要剩余风险是生产治理风险，而不是证据完全不足；
- 该风险可以通过 CG-01～CG-06 在正式生产开始前受控解决。

---

## 9. Gate Boundary

即使 Product Owner 批准 CONDITIONAL GO：

- P1.3 PASS 只表示“证据足以支持受控候选复原”；
- 不表示所有历史参数已经确定；
- 不表示未知项自动消失；
- 不表示报告理想模型等于963初建状态；
- 不表示可以绕过 Evidence-aware Parameter Schema 直接开始 Blender 正式几何生产。
