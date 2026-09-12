# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **PASS** | T-004｜PARAMETRIC_ARCHITECTURE_POC_V001：独立 JSON 参数驱动同一 Blender 3.6 Python 脚本；Baseline 3×2 开间→12 柱/21 主要对象，Variant 仅改 JSON 为 4×3 开间→20 柱/31 主要对象；尺寸与屋顶同步变化；独立重开及 Determinism PASS。 |

**P0 Gate Final：4 / 4 PASS。**

2026-09-11 Product Owner 已明确批准 P0 关闭。

## P0 Carry-forward

- Local Blender 3.6 ↔ Cloud Blender 4.5 的 Class B 兼容性限制继续生效。
- P0.3 只证明“参数 → 脚本 → 可重复模型”的技术链路成立，不证明历史参数真实性。

---

## P1｜选题取证｜CLOSED / APPROVED 2026-09-12

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P1.0｜选题标准锁定 | 明确首个正式复原案例的筛选原则与比较维度 | **PASS** | 五项加权标准已锁定。 |
| P1.1｜候选案例比较与定选 | 对候选按统一标准比较并正式锁定案例 | **PASS** | 山西平遥镇国寺万佛殿正式定选。 |
| P1.2｜正式证据包建立 | 建立可追溯证据包并覆盖核心复原域 | **PASS** | `SRC-ZG-WF-001` 完整精细测绘报告已直接核读；Gate Review 10/10 PASS。 |
| P1.3｜证据分级与可复原性 Go / No-Go | 将关键信息分为已证实 / 高可信推断 / 合理补全 / 未知，并判断是否足以进入正式参数化与3D | **PASS / CONDITIONAL GO** | Product Owner 2026-09-12 批准。85/85参数完成分级；Gate Review 6 PASS + 2 PASS WITH CONDITION + 0 FAIL。CG-01～CG-06 跨阶段强制生效。 |

**P1 Gate Final：4 / 4 PASS。**

### P1 Final Evidence

- `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`
- `docs/evidence/zhenguo_wanfo/P1_3_HIGH_RISK_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md`
- `docs/project_control/phase_archive/P1_closure.md`

### P1.3 Final Classification

- CONFIRMED：46
- HIGH_CONFIDENCE_INFERENCE：32
- REASONABLE_COMPLETION：4
- UNKNOWN：3
- TOTAL：85

`CONFIRMED` 必须结合 `time_layer` 解读，不能自动等同963年原设计事实。

### P1.3 Conditional Go｜强制边界

1. 第一项正式几何生产前建立 Evidence-aware Parameter Schema；
2. UNKNOWN / DO_NOT_LOCK 不得静默硬锁；
3. REASONABLE_COMPLETION 必须独立参数化、可替换、可追踪；
4. `observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 三层长期分离；
5. 未解决转角精确节点只允许中等LOD拓扑骨架，不得声明历史精确复原；
6. 在逐构件原真性不足时，禁止“完全还原963原貌 / 全部963原构”的过度真实性声明。

---

## P2｜正式参数化与3D复原｜ACTIVE

### P2 Entry Rule

P1.3 的 `CONDITIONAL GO` 已解锁正式参数化阶段。P2.0 已完成 CG-01 所要求的 Evidence-aware Parameter Schema 前置条件；后续正式几何工作必须继续遵守 CG-02～CG-06。

| Gate | 验收标准 | 当前状态 | 关键边界 |
|---|---|---|---|
| P2.0｜Evidence-aware Parameter Schema | 建立机器可读的正式参数 Schema，使关键参数同时保存 `value / unit / classification / time_layer / source_layer / production_use / blocking_level / source_ids / notes`；验证 UNKNOWN 不会被硬锁、REASONABLE_COMPLETION 可替换、三层语义不会串层 | **PASS / APPROVED 2026-09-12** | T-005 V001+V002 工程验证全部 PASS；Gate Review 7/7 PASS；工程证据归档至 GitHub canonical repo，commit `a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`。Product Owner 已批准 P2.0。 |
| P2.1｜正式生产参数集锁定｜Formal Production Parameter Set | 将 P1 已分类参数转为 P2.0 Schema 下的正式 production parameter set；明确 UNKNOWN 对几何生成的真实阻断关系；任何临时建模值必须形成显式、可替换、可追溯的 REASONABLE_COMPLETION | **ENTRY READY / DoD TO BE LOCKED** | **本 Gate 不生成正式 Blender 几何。P2.1 PASS 后方可进入 P2.2。** |
| P2.2｜参数化主体结构候选模型｜Parametric Structural Skeleton | 由 P2.1 正式参数集驱动生成主体结构候选模型，覆盖柱网、柱、主要梁架、斗栱拓扑骨架、屋顶控制几何及主要空间关系，并验证可重复生成与参数响应 | **LOCKED / WAITING FOR P2.1 PASS** | 第一项正式 Blender 几何 Gate；CG-05 未解决转角精确节点/榫卯/隐角梁仅允许中等LOD拓扑骨架。 |
| P2.3｜整合复原候选与质量验收｜Integrated Reconstruction Candidate & QC | 整合结构、屋面、斗栱体系与 evidence metadata，完成可追溯性、确定性重建、兼容性、可替换性与视觉 QC，形成正式963候选复原模型 | **LOCKED / WAITING FOR P2.2 PASS** | PASS 表示“工程可复现、证据可追溯、不确定性透明的963候选复原模型成立”，不等于完全还原963原貌。 |

### P2.0 Final Result

- Schema 字段完整且有明确枚举/约束：**PASS**；
- 四类 classification 实例验证：**PASS**；
- UNKNOWN 保持 `null / DO_NOT_LOCK` 且数字硬锁被机械拒绝：**PASS**；
- REASONABLE_COMPLETION 必须可替换：**PASS**；
- `observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 三层并存且不串层：**PASS**；
- 参数可由后续 Python 读取且本 Gate 不生成正式建筑几何：**PASS**；
- T-005 工程证据进入 canonical GitHub：**PASS**。

**P2.0 Gate Final：7 / 7 PASS / Product Owner APPROVED。**

### P2.0 Engineering Evidence

- `production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V001.md`
- `production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V002.md`
- `production/zhenguo_wanfo/tests/test_schema_validation_v001.py`
- `production/zhenguo_wanfo/tests/fixtures/P2_0_VALID_THREE_LAYER_COEXISTENCE_V001.json`
- canonical archive commit: `a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`

Gate Review：`docs/production/zhenguo_wanfo/P2_0_GATE_REVIEW_2026-09-12.md`  
Product Owner Approval：**P2.0 PASS / 2026-09-12**。

### P2.0 Carry-forward

- CG-01 视为已满足；
- CG-02～CG-06 继续强制生效；
- P2.0 PASS 不表示所有85项参数都已 production-locked；
- UNKNOWN、合理补全、三层语义和历史原真性边界不得在后续工程中丢失。

### P2.1–P2.3 Architecture V001｜APPROVED 2026-09-12

生产路径正式锁定为：

**P2.1 参数 → P2.2 结构 → P2.3 整合候选与QC**

下一步只展开并锁定 **P2.1 Definition of Done**。在 P2.1 DoD 明确前不创建 T-006；P2.1 PASS 前不得进入 P2.2 正式 Blender 几何生产。
