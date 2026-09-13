# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **PASS** | T-004：参数驱动、独立重开与 Determinism PASS。 |

**P0 Gate Final：4 / 4 PASS。**

---

## P1｜选题取证｜CLOSED / APPROVED 2026-09-12

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P1.0｜选题标准锁定 | 明确首个正式复原案例的筛选原则与比较维度 | **PASS** | 五项加权标准已锁定。 |
| P1.1｜候选案例比较与定选 | 对候选按统一标准比较并正式锁定案例 | **PASS** | 山西平遥镇国寺万佛殿正式定选。 |
| P1.2｜正式证据包建立 | 建立可追溯证据包并覆盖核心复原域 | **PASS** | `SRC-ZG-WF-001` 完整精细测绘报告已直接核读；Gate Review 10/10 PASS。 |
| P1.3｜证据分级与可复原性 Go / No-Go | 完成关键参数分级并判断是否可进入正式参数化与3D | **PASS / CONDITIONAL GO** | 85/85参数完成分级；CG-01～CG-06 生效。 |

**P1 Gate Final：4 / 4 PASS。**

---

## P2｜正式参数化与3D复原｜CLOSED / APPROVED 2026-09-12

| Gate | 验收标准 | 最终状态 | 关键边界 |
|---|---|---|---|
| P2.0｜Evidence-aware Parameter Schema | Evidence-aware parameter contract | **PASS / APPROVED** | CG-01 satisfied. |
| P2.1｜Formal Production Parameter Set | 85/85 formal set + dependency + preflight | **PASS / APPROVED / CLOSED** | Z-006 remains UNKNOWN; RC-01 replaceable. |
| P2.2｜Parametric Structural Skeleton | Complete medium-LOD structural skeleton | **PASS / APPROVED / CLOSED** | 217 = machine objects, not historical component count. |
| P2.3｜Integrated Reconstruction Candidate & QC | Component-library-driven integrated candidate + final engineering / visual QC | **PASS / APPROVED / CLOSED** | DoD 9/9；six-view visual/evidence review PASS；D-028。 |

**P2 Gate Final：4 / 4 PASS / CLOSED。**

P2 frozen baseline：11 families / 40 variants / 365 stable mesh instances；Local3.6→Cloud4.5→Local3.6 roundtrip PASS；历史边界继续有效。

---

## P3｜古建筑构件系统化与组合建模｜ACTIVE / ENTERED 2026-09-13

| Gate | 验收标准 | 当前状态 | 关键边界 |
|---|---|---|---|
| P3.0｜Component Ontology & Registry | 建立构件本体、命名/ID、Registry Schema，并完成 P2 11/40/365 语义审计与迁移 | **PASS / APPROVED / CLOSED** | DoD 9/9；11/40/365 全量迁移；orphan 0/0/0；D-031。 |
| P3.1｜Component Master & Variant Library | 为证据资格成立的历史构件建立 canonical 3D Master、参数化 Variant、标准审核图与资产登记 | **ACTIVE / DOD LOCKED / CONTRACT V002 LOCKED / 1 OF 6 MASTERS APPROVED** | 六类 scope 由 D-033 锁定；T-011 柱 Master 已 D-035 批准；V002 字段纠错由 D-036 锁定；剩余五类 planning-ready、尚未授权。 |
| P3.2｜Assembly Relationship Model | 建立构件之间组合、支承、连接、定位、重复和 Assembly Unit 关系 | **LOCKED** | 等待 P3.1 PASS。 |
| P3.3｜Component-driven Building Reconstruction | 验证可由构件库 + Variant + Assembly Rules 重新装配万佛殿并形成可解释成果 | **LOCKED** | 等待 P3.2 PASS。 |

**P3 Gate Progress：1 / 4。**

### P3.0 Gate Final｜APPROVED / PASS / CLOSED

- Definition of Done：9 / 9 PASS。
- Family / Variant / Instance migration：11 / 40 / 365；orphan 0/0/0。
- Historical component、GEOMETRIC_PROXY、CONTROL_OBJECT、ENVELOPE_SURFACE 已正式分离。
- T-009 engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`。
- Product Owner approval：D-031。

### P3.1 Definition of Done V001｜LOCKED / D-032

PASS 仍要求 DoD 9/9、全部 MASTER_REQUIRED 100% Master coverage、Variant/evidence/replaceability/reproducibility PASS、P2 frozen baseline unchanged、Product Owner 最终批准。

### T-010 Qualification Baseline｜APPROVED / D-033

- P3.0 Registry coverage：11/11。
- P1 minimum scope：9/9。
- Total review records：27；pending = 0。
- MASTER_REQUIRED：6；Deferred：13；Proxy：4；Control：3；Envelope：1。
- 六类正式 Master-production scope：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿。
- T-010 approval 不等于几何授权。

### P3.1 Canonical Master Asset Contract V002｜LOCKED / PRODUCT OWNER APPROVED / D-036

当前 authoritative Contract：

- `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md`
- `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`

V001（D-034）保留为历史版本，但 **V002 supersedes V001 for all future Master production**。

V002 继承原全部 Locked rules，并仅修正柱头栌斗字段映射：

- top width / 面阔总宽 = `475.1 mm`
- bottom width / 面阔下宽 = `327.1 mm`
- top depth / 进深总深 = `446.3 mm`
- bottom depth / 进深下深 = `305.5 mm`

其余核心规则继续不变：

- unit = mm；+Z = up；+X = 主水平长度/跨度；+Y = 横向深度；
- Master transform = location 0 / rotation 0 / scale 1；
- LOD = `EVIDENCE_BOUNDED_MEDIUM_LOD`；world placement 不得写入 Master；
- UNKNOWN 不得静默填值；RC/HCI 不得升级为 CONFIRMED；
- `Z-006` 保持 UNKNOWN；`Z-006-RC-01` 独立可替换；`DG-114` 不形成统一小斗规格；`HIS-002` originality unknown；
- 不建无证据榫卯、暗槽、内部空腔、耳瓣或端部细节；
- Variant 必须参数驱动，placement-only 不创建 Variant，Object Scale 不得形成正式 Variant；
- 上下六椽栿完整长度仍未被证实，只允许显式、可追溯的 length parameter；max thickness 仅作为 bounded outer envelope；
- standard review set + semantic snapshot + deterministic semantic regeneration + independent reopen + mutation validation + Registry registration 为正式资产链要求。

### T-011｜CMP-COLUMN-001 Column Master Pilot｜APPROVED / CLOSED / D-035

- Engineering：22/22 machine checks PASS。
- Blender execution：3.6.23 CLI/background / RC-008 COMPLIANT。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild / Registry registration：PASS。
- P2 frozen baseline：19 hashes unchanged。
- Review package：6/6，ChatGPT visual PASS，Product Owner APPROVED。
- `CMP-COLUMN-001` 为当前第 1 个 approved canonical Master；V002 字段纠错不影响该资产。

### P3.1 Current Boundary / Next Step

- 当前无 active Codex task。
- Master coverage：**1 / 6 approved**。
- 剩余五类已解除 Contract HOLD，但**尚未授权 Blender 生产**。
- 推荐拆分：
  1. 斗类：柱头栌斗 + 单向长开斗 + 交互斗；
  2. 梁架类：下六椽栿 + 上六椽栿。
- 下一步先定义并审核斗类 batch 的正式 Task Contract；只有明确授权后 Codex 才可执行。