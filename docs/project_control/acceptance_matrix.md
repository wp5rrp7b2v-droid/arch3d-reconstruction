# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **PASS** | T-004｜PARAMETRIC_ARCHITECTURE_POC_V001：独立 JSON 参数驱动同一 Blender 3.6 Python 脚本；Baseline 3×2 开间→12 柱/21主要对象，Variant 4×3 开间→20柱/31主要对象；尺寸与屋顶同步变化；独立重开及 Determinism PASS。 |

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

### P1.3 Conditional Go｜强制边界

1. 第一项正式几何生产前建立 Evidence-aware Parameter Schema；
2. UNKNOWN / DO_NOT_LOCK 不得静默硬锁；
3. REASONABLE_COMPLETION 必须独立参数化、可替换、可追踪；
4. `observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 三层长期分离；
5. 未解决转角精确节点只允许中等LOD拓扑骨架，不得声明历史精确复原；
6. 在逐构件原真性不足时，禁止“完全还原963原貌 / 全部963原构”的过度真实性声明。

---

## P2｜正式参数化与3D复原｜ACTIVE

| Gate | 验收标准 | 当前状态 | 关键边界 |
|---|---|---|---|
| P2.0｜Evidence-aware Parameter Schema | Evidence-aware parameter contract | **PASS / APPROVED** | CG-01 satisfied. |
| P2.1｜Formal Production Parameter Set | 85/85 formal set + dependency + preflight | **PASS / APPROVED / CLOSED** | Z-006 remains UNKNOWN; RC-01 replaceable. |
| P2.2｜Parametric Structural Skeleton | Complete medium-LOD structural skeleton | **PASS / APPROVED / CLOSED** | 217 = machine objects, not historical component count. |
| P2.3｜Integrated Reconstruction Candidate & QC | Component-library-driven integrated candidate + final engineering QC | **IN PROGRESS / ENGINEERING HOLD / ROUNDTRIP REQUIRED** | T-008 V001 local engineering complete; DoD-07 real Cloud Blender 4.5.13 roundtrip and Local 3.6 return validation still missing. |

### P2.1 Gate Final｜APPROVED / PASS / CLOSED

- DoD 9/9 PASS。
- `geometry-critical unresolved blocker = 0`。
- Z-006 仍为 UNKNOWN；Z-006-RC-01 仍为独立可替换 production candidate。

### P2.2 Gate Final｜APPROVED / PASS / CLOSED

- DoD 9/9 PASS。
- 6/6 structural scope；machine validation / deterministic rebuild / reopen / Product Owner structural review 全部 PASS。
- 217 仅为 Blender 机器结构/控制对象数。

### P2.3 Definition of Done V001｜LOCKED

正式 DoD：`docs/production/zhenguo_wanfo/P2_3_DEFINITION_OF_DONE_V001.md`

必须完成：

1. Integration Manifest；
2. Component Library → Parametric Variant → Placement / Instance → Evidence Metadata；
3. 完整整合候选几何；
4. Evidence Metadata / historical claim boundary；
5. 参数驱动、RC可替换、无不可追溯核心手工漂移；
6. Integrated Machine QC；
7. Deterministic rebuild + independent reopen + **Local 3.6 → Cloud 4.5 → Local 3.6 roundtrip QC**；
8. 六类视觉 QC / Evidence Diagnostic + Product Owner review；
9. 最终归档、Known Limitations 与 P2 Closure Evidence。

### T-008 V001 Engineering Result｜HOLD 2026-09-12

- Component Library：**11 families / 40 variants**。
- Integrated candidate：**365 stable mesh instances**。
- Machine QC：**34/34 PASS / 0 errors**。
- Automated tests：**33/33 PASS**。
- Replacement / mutation：PASS。
- Deterministic rebuild：PASS。
- Independent reopen：PASS / PASS。
- Naked historical constant / manual drift audit：PASS。
- `Z-006` 保持 UNKNOWN；`Z-006-RC-01`、DG-114、HIS-002 与 45°转角等历史边界保持。
- 六张 review PNG 已生成；Product Owner 正式视觉审核尚未发生。
- Local-only final candidate SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`。
- Canonical engineering commit：`5bd6ca1f8300a170b74c3a9058352768800b56a6`。
- **DoD-07 = HOLD**：Cloud Blender 4.5.13 workflow 尚无真实 run；无 returned artifact；无 Local Blender 3.6 return validation。

当前 P2.3 Gate：**NOT PASS / ENGINEERING HOLD**。

### T-008 V002 Continuation｜READY FOR LOCAL EXECUTION

- 同一 T-008 目标继续，不创建 T-009。
- V001 已通过的本地整合候选与工程证据冻结；V002 仅关闭 DoD-07 blocker。
- 采用普通 Git **temporary tag → `.blend` blob** 传输；不把 `.blend` 提交到 main，不提取 Git credential，不 force-push。
- 运行 Cloud Blender 4.5.13 reopen / semantic QC / save / independent reopen。
- 下载 artifact 后以 Local Blender 3.6.23 做返回验证。
- Roundtrip evidence 入库后删除临时 transport tag。
- Task Contract：`docs/tasks/T-008_P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V002.md`。

P2.3 最终 PASS 仍需：T-008 工程 PASS + ChatGPT 独立复核 + Product Owner 对 PLAN / ELEVATION / AXON / EXTERIOR_3Q / STRUCTURE_DETAIL / EVIDENCE_DIAGNOSTIC 六图完成正式审核并明确批准。
