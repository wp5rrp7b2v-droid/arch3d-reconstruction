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
| P3.1｜Component Master & Variant Library | 为证据资格成立的历史构件建立 canonical 3D Master、参数化 Variant、标准审核图与资产登记 | **ACTIVE / DOD LOCKED / T-010 APPROVED / MASTER ASSET CONTRACT REVIEW** | 六类 Master-production scope 已由 D-033 锁定；Contract V001 draft 等待 Product Owner 审核；未授权 Blender Master 几何。 |
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

### P3.1 Canonical Master Asset Contract V001｜DRAFT / PO REVIEW REQUIRED

正式草案：

- `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V001.md`
- `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V001.json`

草案统一：

- unit = mm；
- +Z = up；+X = 主水平长度/跨度；+Y = 横向深度；
- Master transform = location 0 / rotation 0 / scale 1；
- LOD = `EVIDENCE_BOUNDED_MEDIUM_LOD`；
- world placement 不得写入 Master；
- UNKNOWN 不得静默填值；RC/HCI 不得升级为 CONFIRMED；
- 不建无证据榫卯、暗槽、内部空腔、端部细节；
- Variant 必须参数驱动，placement-only 不创建 Variant；
- standard review set + semantic snapshot + independent reopen + mutation validation 必须保留。

关键限制：上下六椽栿完整长度仍未被证实，Master 只允许使用显式、可追溯的 length parameter；max thickness 只能作为 bounded outer envelope，不得声称整根构件全长恒定为该厚度。

当前建议：Contract LOCK 后先以 `CMP-COLUMN-001` 做 Contract Implementation Pilot，验证完整资产链，再扩展其余五个 Master。
