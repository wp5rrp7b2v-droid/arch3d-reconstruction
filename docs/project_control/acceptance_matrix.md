# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **PASS** | T-004｜PARAMETRIC_ARCHITECTURE_POC_V001：独立 JSON 参数驱动同一 Blender 3.6 Python 脚本；Baseline 3×2 开间→12 柱/21主要对象，Variant 4×3 开间→20柱/31主要对象；尺寸与屋顶同步变化；独立重开及 Determinism PASS。 |

**P0 Gate Final：4 / 4 PASS。**

---

## P1｜选题取证｜CLOSED / APPROVED 2026-09-12

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P1.0｜选题标准锁定 | 明确首个正式复原案例的筛选原则与比较维度 | **PASS** | 五项加权标准已锁定。 |
| P1.1｜候选案例比较与定选 | 对候选按统一标准比较并正式锁定案例 | **PASS** | 山西平遥镇国寺万佛殿正式定选。 |
| P1.2｜正式证据包建立 | 建立可追溯证据包并覆盖核心复原域 | **PASS** | `SRC-ZG-WF-001` 完整精细测绘报告已直接核读；Gate Review 10/10 PASS。 |
| P1.3｜证据分级与可复原性 Go / No-Go | 完成关键参数分级并判断是否可进入正式参数化与3D | **PASS / CONDITIONAL GO** | 85/85参数完成分级；46 CONFIRMED / 32 HCI / 4 RC / 3 UNKNOWN；CG-01～CG-06 生效。 |

**P1 Gate Final：4 / 4 PASS。**

### P1.3 Conditional Go｜强制边界

1. Evidence-aware Parameter Schema；
2. UNKNOWN / DO_NOT_LOCK 不得静默硬锁；
3. RC 必须独立参数化、可替换、可追踪；
4. observed / report ideal / reconstructed candidate 三层分离；
5. 未解决转角仅允许 evidence-bounded medium LOD；
6. 禁止过度真实性声明。

---

## P2｜正式参数化与3D复原｜CLOSED / APPROVED 2026-09-12

| Gate | 验收标准 | 最终状态 | 关键边界 |
|---|---|---|---|
| P2.0｜Evidence-aware Parameter Schema | Evidence-aware parameter contract | **PASS / APPROVED** | CG-01 satisfied. |
| P2.1｜Formal Production Parameter Set | 85/85 formal set + dependency + preflight | **PASS / APPROVED / CLOSED** | Z-006 remains UNKNOWN; RC-01 replaceable. |
| P2.2｜Parametric Structural Skeleton | Complete medium-LOD structural skeleton | **PASS / APPROVED / CLOSED** | 217 = machine objects, not historical component count. |
| P2.3｜Integrated Reconstruction Candidate & QC | Component-library-driven integrated candidate + final engineering / visual QC | **PASS / APPROVED / CLOSED** | DoD 9/9；six-view visual/evidence review PASS；D-028。 |

**P2 Gate Final：4 / 4 PASS / CLOSED。**

### P2.1 Gate Final｜APPROVED / PASS / CLOSED

- DoD 9/9 PASS。
- `geometry-critical unresolved blocker = 0`。
- Z-006 仍 UNKNOWN；Z-006-RC-01 仍独立可替换。

### P2.2 Gate Final｜APPROVED / PASS / CLOSED

- DoD 9/9 PASS。
- 6/6 structural scope；machine validation / deterministic rebuild / reopen / Product Owner structural review 全部 PASS。
- 217 仅为 Blender 机器结构/控制对象数。

### P2.3 Definition of Done V001｜LOCKED / FINAL 9 OF 9 PASS

正式 DoD：`docs/production/zhenguo_wanfo/P2_3_DEFINITION_OF_DONE_V001.md`

1. Integration Manifest：PASS；
2. Component Library → Parametric Variant → Placement / Instance → Evidence Metadata：PASS；
3. 完整整合候选几何：PASS；
4. Evidence Metadata / historical claim boundary：PASS；
5. 参数驱动、RC可替换、无不可追溯核心手工漂移：PASS；
6. Integrated Machine QC：PASS；
7. Deterministic rebuild + independent reopen + Local 3.6 → Cloud 4.5 → Local 3.6 roundtrip QC：PASS；
8. 六类视觉 QC / Evidence Diagnostic + Product Owner review：PASS；
9. 最终归档、Known Limitations 与 P2 Closure Evidence：PASS。

### T-008 Engineering Result｜PASS / COMPLETE

- V001 candidate：11 families / 40 variants / 365 stable mesh instances。
- Local Blender 3.6 machine QC：34/34 PASS；automated tests：33/33 PASS。
- Replacement / mutation、deterministic rebuild、independent reopen、naked constant / manual drift audit：PASS。
- Historical boundaries：Z-006 UNKNOWN；RC-01 可替换；DG-114 / HIS-002 / 45° corner 等未升级。
- V001 local-only candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- GitHub Actions run `34695870243`：SUCCESS；Cloud Blender 4.5.13 input / reopen semantic QC PASS。
- Artifact `P2_3_CLOUD_ROUNDTRIP_V001`：PASS；returned blend SHA256 `d2c80c4e2e0ae278ad4b7055df6871e00bfb85ecf981fbc796ddd2f5e919efc0`。
- Local Blender 3.6 return semantic QC PASS / machine QC 34/34 PASS；core semantic diff NONE。

### P2.3 Final Visual Review｜6 / 6 PASS

- PLAN：PASS
- ELEVATION：PASS
- AXON：PASS
- EXTERIOR_3Q：PASS
- STRUCTURE_DETAIL：PASS
- EVIDENCE_DIAGNOSTIC_V002：PASS

原 Evidence Diagnostic 首轮 HOLD 后，T-008 V004 只读修正四级证据映射；canonical `.blend` SHA、11/40/365、33/33 tests、34/34 machine QC、V003 roundtrip 与其余五张审核图全部保持不变。

最终 V002 diagnostic：

- priority = `UNKNOWN / PLACEHOLDER > REASONABLE COMPLETION / APPROVED OVERRIDE > HIGH CONFIDENCE INFERENCE > CONFIRMED`；
- counts = CONFIRMED 0 / HCI 0 / RC 35 / UNKNOWN-placeholder 330；
- 0-count 类别保留 legend；
- Product Owner 直接审核 PASS。

该图正式解释为 **Conservative Risk Map**；`0 / 0 / 35 / 330` 不表示参数证据中没有 CONFIRMED / HCI。

后续 Evidence Visualization 双层规则：`docs/production/zhenguo_wanfo/EVIDENCE_VISUALIZATION_CARRY_FORWARD_V001.md`。

### P2.3 Final Gate Review｜9 / 9 PASS

Gate Review：`docs/production/zhenguo_wanfo/P2_3_GATE_REVIEW_2026-09-12.md`

Product Owner 明确批准：`P2.3｜PASS`。Decision：D-028。

P2 Closure Archive：`docs/project_control/phase_archive/P2_closure.md`。

---

## P3｜古建筑构件系统化与组合建模｜ACTIVE / ENTERED 2026-09-13

| Gate | 验收标准 | 当前状态 | 关键边界 |
|---|---|---|---|
| P3.0｜Component Ontology & Registry | 建立构件本体、命名/ID、Registry Schema，并完成 P2 11 families / 40 variants / 365 instances 的语义审计与迁移 | **ENTERED / DOD DRAFT** | 不新增几何；historical component 与 control/proxy/envelope 必须分离；T-009 未授权。 |
| P3.1｜Component Master & Variant Library | 为正式历史构件建立独立 3D Master、参数化 Variant、标准审核图与资产登记 | **LOCKED** | 等待 P3.0 PASS。 |
| P3.2｜Assembly Relationship Model | 建立构件之间组合、支承、连接、定位、重复和 Assembly Unit 关系 | **LOCKED** | 等待 P3.1 PASS。 |
| P3.3｜Component-driven Building Reconstruction | 验证可由构件库 + Variant + Assembly Rules 重新装配万佛殿并形成可解释成果 | **LOCKED** | 等待 P3.2 PASS；Evidence Visualization 双层规则继续生效。 |

**P3 Gate Progress：0 / 4。**

### P3.0 Current Boundary

- 正式 DoD Draft：`docs/production/zhenguo_wanfo/P3_0_DEFINITION_OF_DONE_V001.md`。
- P2 冻结为 Reconstruction Engineering Baseline，不重做。
- P3.0 首先审计 P2 工程 family 是否真对应历史构件。
- 现有 P2 family 中已明确混有 CONTROL / DIAGNOSTIC / ENVELOPE 类对象，因此不得直接将 11 families 解释为 11 种古建筑构件。
- P3.0 DoD 经 Product Owner 批准并锁定前，不创建 T-009、不做新增 Blender 几何。
