# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **PASS** | T-004｜PARAMETRIC_ARCHITECTURE_POC_V001：独立 JSON 参数驱动同一 Blender 3.6 Python 脚本；Baseline 3×2 开间→12 柱/21 主要对象，Variant 仅改 JSON 为 4×3 开间→20 柱/31 主要对象；尺寸与屋顶同步变化；独立重开及 Determinism PASS。 |

**P0 Gate Final：4 / 4 PASS。**

2026-09-11 Product Owner 已明确批准 P0 关闭。P0 状态：**CLOSED / APPROVED**。项目进入 **P1｜选题取证**。

## P0.2 Production Rule｜Carry-forward

凡需要返回 Local Blender 3.6 继续维护的核心资产，不得默认依赖未经单独验证的 Blender 4.5-only 数据结构、节点、模拟或其他新功能。新功能进入正式生产前必须先做兼容性验证。

## P0.3 Validation Boundary｜Carry-forward

P0.3 只证明“结构化建筑参数 → 脚本 → 可重复最小结构模型”的技术链路成立；不代表历史证据已经完成参数化，也不代表正式古建筑结构、构造法式或复原精度已经被验证。这些属于 P1 及后续 Phase。

## P1｜选题取证｜ACTIVE

| Gate | 验收标准 | 当前状态 | 关键边界 |
|---|---|---|---|
| P1.0｜选题标准锁定 | 明确首个正式复原案例的筛选原则与比较维度，能够稳定排除“过于复杂 / 证据不足 / 不适合首案”的对象 | **PASS** | Product Owner 2026-09-11 批准。采用五项加权指标：证据链完整度30%；测绘/尺寸资料可获得性25%；结构规模与首案可控性20%；历史状态歧义程度15%（歧义越低得分越高）；参数化与展示价值10%。统一按1–5分评分。 |
| P1.1｜候选案例比较与定选 | 对 3–5 个候选对象按统一标准比较，并由 Product Owner 明确锁定一个正式案例 | **PASS** | 四候选按 P1.0 锁定权重比较：平遥镇国寺万佛殿 4.80；五台南禅寺大殿 4.48；五台佛光寺东大殿 4.13；宁波保国寺大殿 4.05。Product Owner 2026-09-11 批准 **平遥镇国寺万佛殿** 为首案。评分只表示首案适配度，不是历史价值排名。 |
| P1.2｜正式证据包建立 | 对锁定案例建立可追溯资料包，至少覆盖年代/身份、总体尺寸、平面柱网、立面屋顶、主体木构、关键构件及图像/测绘/考古或修缮资料 | **PASS** | Product Owner 2026-09-11 批准。`SRC-ZG-WF-001`完整精细测绘报告已直接核读；Direct Page Review V001 + Parameter Candidate Matrix V002 + Gate Review 完成；10/10 验收域通过。P1.2 的 PASS 不代表所有参数均已达到历史事实级确定性。 |
| P1.3｜证据分级与可复原性 Go / No-Go | 将关键信息分为已证实 / 高可信推断 / 合理补全 / 未知，并判断是否足以进入正式参数化与 3D 复原 | **READY FOR PO DECISION** | Step 1 + Step 2 + Final Gate Review 已完成。85/85参数已分级；Gate Review = 6 PASS + 2 PASS WITH CONDITION + 0 FAIL；Reviewer Recommendation = **CONDITIONAL GO**。等待 Product Owner 批准，批准前仍不得进入正式3D生产。 |

**P1 Gate Progress：3 / 4 PASS；P1.3 READY FOR DECISION。**

### P1.0 Locked Selection Policy

首案优先选择：**证据充分、结构规模可控、可参数化、公开资料可获得，并能够验证完整复原方法的现存或有高质量测绘资料的古代木构单体。**

不以知名度或年代最早作为首要标准；“历史状态是否清晰”是独立评价维度，不能被“资料多”替代。

### P1.1 Locked Case

**首个正式复原案例：山西平遥镇国寺万佛殿。**

锁定理由：在统一权重下获得最高首案适配度；兼具明确纪年基础、中小型单体规模、高质量精细测绘可获得性、较高参数化价值与相对可控的历史状态歧义。

### P1.2 Final Evidence

- `docs/evidence/zhenguo_wanfo/SOURCE_REGISTER.md`
- `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`
- `docs/evidence/zhenguo_wanfo/P1_2_GATE_REVIEW_2026-09-11.md`

直接核读已确认平面柱网、营造尺推定、柱径/角柱生起、斗栱主要构件、六椽栿、架道、山面出际、举折、理想模型、形变和修缮史；同时纠正了此前对主报告印刷 p107 / p147 的错误页码归属。

### P1.3 Classification Evidence

- `docs/evidence/zhenguo_wanfo/P1_3_HIGH_RISK_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md`

Step 2 完整统计：46 CONFIRMED / 32 HIGH_CONFIDENCE_INFERENCE / 4 REASONABLE_COMPLETION / 3 UNKNOWN，共85项。CONFIRMED 必须结合 `time_layer` 解读，不能自动等同963年原设计事实。

### P1.3 Final Gate Review｜2026-09-12

Gate Review 检查8项：

- 6 PASS；
- 2 PASS WITH CONDITION；
- 0 FAIL。

Reviewer Recommendation：**APPROVE CONDITIONAL GO**。

不建议无条件 GO：963原设计柱高、转角45°精确节点、隐衬角栿/隐角梁、逐构件963原真性仍存在不确定性，且正式 Evidence-aware Parameter Schema 尚未实现。

不建议 NO-GO：上述未知项都可隔离到参数或子模块，不会使整个候选复原失去可解释性。

若 Product Owner 批准 CONDITIONAL GO，则以下规则成为进入正式3D的强制条件：

1. 第一项正式几何生产前建立 Evidence-aware Parameter Schema；
2. UNKNOWN / DO_NOT_LOCK 不得静默硬锁为数字；
3. REASONABLE_COMPLETION 必须独立参数化、可替换、可追踪；
4. `observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 三层长期分离；
5. 未解决转角精确节点只允许中等LOD拓扑骨架，不得声明历史精确复原；
6. 在逐构件原真性不足时，禁止“完全还原963原貌 / 全部963原构”的过度真实性声明。

### P1.3 Decision Boundary

Product Owner 可选择：

- **APPROVE CONDITIONAL GO** → P1.3 PASS，P1 Gate = 4/4 PASS；正式参数化/3D阶段解锁，但所有 Conditional Go 条件继续强制生效；
- **HOLD** → P1.3 保持 IN_PROGRESS，补证或修改规则后重审；
- **NO-GO** → 当前案例不进入正式3D，重新评估对象或证据策略。

P1.0 / P1.1 / P1.2 / P1.3 的研究与 Gate Review 本身不创建 Codex T-###；只有出现实际工程执行任务时再创建 T 编号。
