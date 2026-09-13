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
| P3.1｜Component Master & Variant Library | 为证据资格成立的历史构件建立 canonical 3D Master、参数化 Variant、标准审核图与资产登记 | **PASS / APPROVED / CLOSED** | DoD 9/9；6/6 Master Approved；formal variants=0；T-014 Library Overview PASS；D-040。 |
| P3.2｜Assembly Relationship Model | 建立构件之间组合、支承、连接、定位、重复和 Assembly Unit 关系 | **ACTIVE / ENTERED / DOD REQUIRED** | 已由 D-040 解锁；P3.2 DoD 未批准前不得创建工程任务。 |
| P3.3｜Component-driven Building Reconstruction | 验证可由构件库 + Variant + Assembly Rules 重新装配万佛殿并形成可解释成果 | **LOCKED** | 等待 P3.2 PASS。 |

**P3 Gate Progress：2 / 4。**

### P3.0 Gate Final｜APPROVED / PASS / CLOSED

- Definition of Done：9 / 9 PASS。
- Family / Variant / Instance migration：11 / 40 / 365；orphan 0/0/0。
- Historical component、GEOMETRIC_PROXY、CONTROL_OBJECT、ENVELOPE_SURFACE 已正式分离。
- T-009 engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`。
- Product Owner approval：D-031。

### P3.1 Definition of Done V001｜LOCKED / D-032

PASS 要求 DoD 9/9、全部 MASTER_REQUIRED 100% Master coverage、Variant/evidence/replaceability/reproducibility PASS、P2 frozen baseline unchanged、Product Owner 最终批准。

### T-010 Qualification Baseline｜APPROVED / D-033

- P3.0 Registry coverage：11/11。
- P1 minimum scope：9/9。
- Total review records：27；pending = 0。
- MASTER_REQUIRED：6；Deferred：13；Proxy：4；Control：3；Envelope：1。
- 六类正式 Master-production scope：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿。

### P3.1 Canonical Master Asset Contract V002｜LOCKED / PRODUCT OWNER APPROVED / D-036

当前 authoritative Contract：

- `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md`
- `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`

核心规则继续有效：unit=mm；标准局部坐标与 Scale=1；`EVIDENCE_BOUNDED_MEDIUM_LOD`；UNKNOWN 不得静默填值；RC/HCI 不得升级为 CONFIRMED；不建无证据榫卯、暗槽、内部空腔、耳瓣或端部细节；Variant 必须参数驱动；standard review set + semantic snapshot + deterministic regeneration + independent reopen + mutation validation + Registry registration 为正式资产链要求。

### T-011｜CMP-COLUMN-001 Column Master Pilot｜APPROVED / CLOSED / D-035

- 22/22 machine checks PASS。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild / Registry registration：PASS。
- Review package：6/6，ChatGPT visual PASS，Product Owner APPROVED。

### T-012｜Dou Master Lean Batch V002｜APPROVED / CLOSED / D-037

- First Article `CMP-LUDOU-COLUMN-001`：PASS。
- 3/3 engineering PASS；3/3 deterministic regeneration / reopen / mutation / rebuild PASS。
- Review：18/18 individual + 1/1 batch overview = **19/19 visual PASS**。
- Approved Masters：柱头栌斗、单向长开斗、交互斗。

### T-013｜Six-Chuanfu Master Batch V002｜APPROVED / CLOSED / D-039

- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL + LEAN_PRODUCTION_MODE_V001`。
- First Article：`CMP-FRAME-LOWER-SIX-CHUANFU-001` PASS；之后 `CMP-FRAME-UPPER-SIX-CHUANFU-001` PASS。
- 两件各 26/26 machine checks PASS；deterministic regeneration / independent reopen / length mutation / tenon metadata-only mutation / canonical rebuild：2/2 PASS。
- historical full length：两件均保持 `UNKNOWN / null`。
- `canonical_reference_length_mm=1000`：仅 `PROJECT_RULE / NON_HISTORICAL / REPLACEABLE` reference specimen。
- `tenon_area_thickness`：metadata-only / geometry use = 0。
- `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`：继续作为后续 Hard Fail。
- 最终视觉审核：**13/13 PASS**。
- Product Owner：`APPROVED / CLOSED / D-039`。
- P3.1 Master coverage：**6 / 6 approved**。

### T-014｜P3.1 Master Library Overview｜PASS / CLOSED

- whole-library Overview 覆盖 6/6 approved Masters。
- 正式中文构件名：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿。
- 名称依据：`SRC-ZG-WF-001` 精细测绘报告 / project canonical naming；不宣称为宋代原称或古籍原称。
- formal variants = 0。
- canonical Masters / existing review assets / batch overviews / P2 frozen baseline / Contract V002：UNCHANGED。
- P3.2 files created = NO；new Variant records = 0。
- Final Overview SHA256：`4719a31c18de13b0453a64d29847381d8e45af0f145bcb37bf7fee0abf9671a7`。
- ChatGPT final visual review：PASS。

### P3.1 Gate Final｜PASS / APPROVED / CLOSED / D-040

Gate Review：`docs/production/zhenguo_wanfo/P3_1_GATE_REVIEW_2026-09-13.md`

| DoD | 最终结论 |
|---|---|
| DoD-01 Scope Matrix | **PASS** |
| DoD-02 Identity Resolution | **PASS** |
| DoD-03 Master Asset Contract | **PASS** |
| DoD-04 Canonical Masters | **PASS** |
| DoD-05 Parameterized Variant Model | **PASS / formal registered variants = 0** |
| DoD-06 Evidence / Replaceability | **PASS** |
| DoD-07 Standard Review Package | **PASS / T-014 whole-library Overview** |
| DoD-08 Registry / Validation / Reproducibility | **PASS** |
| DoD-09 PO Review / Archive / P3.2 Readiness | **PASS / D-040** |

**P3.1 Gate Final：9 / 9 PASS / APPROVED / CLOSED。**

Carry-forward boundaries remain active：Z-006 UNKNOWN/null；Z-006-RC-01 replaceable；DG-114 UNKNOWN；HIS-002 originality unknown；45°转角/榫卯/隐角梁 unresolved；六椽栿 historical full length UNKNOWN/null；1000 mm 仅 non-historical reference；`REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` 为 P3.2/P3.3 Hard Fail。

### P3.2 Current Boundary / Next Step

- P3.2 已解锁并进入。
- 当前无 active Codex task。
- 第一项工作不是建模，而是定义并锁定 `P3.2 Definition of Done`。
- P3.2 DoD 获 Product Owner 明确批准前，不创建新的 P3.2 工程任务。
