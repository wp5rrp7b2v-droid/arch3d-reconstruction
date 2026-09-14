# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 最终状态 | 关键证据 / 限制 |
|---|---|---|
| P0.0 | **PASS** | Project Control 文件集可跨 Chat 作为正式 handoff；Dashboard 为派生可视化。 |
| P0.1 | **PASS** | Local Blender 3.6.23 灰模生成、保存、独立重开、Geometry Integrity、PNG 审核通过。 |
| P0.2 | **PASS / Class B** | Local3.6→GitHub Actions Blender4.5→Local3.6 roundtrip PASS；核心几何/Marker/Metadata 无关键丢失。 |
| P0.3 | **PASS** | T-004 参数驱动、独立重开与 Determinism PASS。 |

**P0 Gate Final：4 / 4 PASS。**

---

## P1｜选题取证｜CLOSED / APPROVED 2026-09-12

| Gate | 最终状态 | 关键证据 / 限制 |
|---|---|---|
| P1.0｜选题标准锁定 | **PASS** | 五项加权标准锁定。 |
| P1.1｜候选案例比较与定选 | **PASS** | 山西平遥镇国寺万佛殿正式定选。 |
| P1.2｜正式证据包建立 | **PASS** | `SRC-ZG-WF-001` 完整精细测绘报告直接核读；Gate Review 10/10 PASS。 |
| P1.3｜证据分级与可复原性 | **PASS / CONDITIONAL GO** | 85/85 参数完成分级；CG-01～CG-06 生效。 |

**P1 Gate Final：4 / 4 PASS。**

---

## P2｜正式参数化与3D复原｜CLOSED / APPROVED 2026-09-12

| Gate | 最终状态 | 关键边界 |
|---|---|---|
| P2.0｜Evidence-aware Parameter Schema | **PASS / APPROVED** | CG-01 satisfied. |
| P2.1｜Formal Production Parameter Set | **PASS / APPROVED / CLOSED** | Z-006 remains UNKNOWN；RC-01 replaceable。 |
| P2.2｜Parametric Structural Skeleton | **PASS / APPROVED / CLOSED** | 217 = machine objects，不等于历史构件数。 |
| P2.3｜Integrated Reconstruction Candidate & QC | **PASS / APPROVED / CLOSED** | 11 families / 40 variants / 365 stable mesh instances；D-028。 |

**P2 Gate Final：4 / 4 PASS / CLOSED。**

---

## P3｜古建筑构件系统化与组合建模｜ACTIVE

| Gate | 验收目标 | 当前状态 | 关键边界 |
|---|---|---|---|
| P3.0｜Component Ontology & Registry | 构件本体、Naming/ID、Registry、P2 语义迁移 | **PASS / APPROVED / CLOSED** | DoD 9/9；11/40/365 全量迁移；D-031。 |
| P3.1｜Component Master & Variant Library | 建立 evidence-qualified canonical Master / Variant / review / Registry | **PASS / APPROVED / CLOSED** | DoD 9/9；6/6 Master Approved；D-040。 |
| P3.2｜构件组合关系模型 | 建立构件资格、承托/连接/定位/重复/从属、接口、参数传递、组合单元、重建验证 | **ACTIVE / T-015 + T-016 APPROVED CLOSED / GATE REVIEW READY** | DoD V001 / D-041；T-015 / D-042；T-016 / D-045；尚未执行最终 Gate Review。 |
| P3.3｜Component-driven Building Reconstruction | 用构件库 + 构件组合关系 + 建筑参数重组万佛殿 | **LOCKED** | 等待 P3.2 正式 PASS。 |

**P3 Gate Progress：2 / 4。**

### P3.1 Gate Final｜PASS / APPROVED / CLOSED / D-040

- DoD：9 / 9 PASS。
- `MASTER_REQUIRED`：6 / 6 approved。
- Proxy 4 / Control 3 / Envelope 1 / Deferred 13 保持非历史化。
- Formal registered variants：0；参数化能力已由 mutation / rebuild 验证。
- Gate Review：`docs/production/zhenguo_wanfo/P3_1_GATE_REVIEW_2026-09-13.md`。

Carry-forward：Z-006 UNKNOWN/null；Z-006-RC-01 replaceable；DG-114 UNKNOWN；HIS-002 originality unknown；45°转角/榫卯/隐角梁 unresolved；六椽栿 historical full length UNKNOWN/null；1000 mm 仅 non-historical reference。

### P3.2 Definition of Done V001｜LOCKED / PRODUCT OWNER APPROVED / D-041

正式文件：`docs/production/zhenguo_wanfo/P3_2_DEFINITION_OF_DONE_V001.md`

9 项 DoD：

1. 组合范围与构件资格；
2. 构件关系分类体系；
3. 构件接口与定位规则；
4. 代表性组合单元与关系覆盖；
5. 尺寸与参数传递；
6. 史料依据与不确定性边界；
7. 机器验证与组合关系完整性；
8. 确定性重建与参数变更验证；
9. P3.3 整殿重建就绪性验证。

Gate Hard Fail：

- `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`
- `SILENT_HISTORICIZATION`
- `BAKED_MANUAL_ASSEMBLY`

P3.2 PASS 必须满足：9/9 DoD PASS + 0 Hard Fail + Product Owner Approval。进入 P3.3 后不得需要重新发明基础构件组合机制。

### T-015｜构件组合关系基础工程实现｜PASS / APPROVED / CLOSED / D-042

- Engineering commit：`49b0415479d811a26d4f44588d15cd863467edf4`。
- Approved Master node mapping：6/6 PASS。
- 五类基础关系：5/5（承托、连接、定位、重复、从属）。
- Interface foundation：6 个 Master / 18 个最小局部接口。
- Machine validation：31/31 PASS。
- Negative tests：21/21 expected rejection PASS。
- 三项 Gate Hard Fail 均有真实触发测试；canonical state = 0 Hard Fail。
- P2 frozen baseline / P3.1 canonical Masters：UNCHANGED。
- ChatGPT structural review：PASS；Product Owner APPROVED / CLOSED。
- Review：`docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_REVIEW_V001.md`。

### T-016｜代表性构件组合验证｜PASS / APPROVED / CLOSED / D-045

- Engineering commit：`fc01ecb4f61128faa95ecf8022d2077a36977a8c`。
- Machine validation：65/65 PASS。
- Negative tests：15/15 expected rejection PASS。
- Canonical Hard Fail：0。
- 五类关系代表性覆盖：5/5。
- A｜柱—柱头栌斗：SUPPORT / LOCATE / BELONG + interface-driven Blender rebuild / independent reopen / determinism PASS；Z-006 与 joinery evidence boundary 保持。
- B｜六椽栿梁架层位：`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED` 为预期 PASS；未生成实际全长几何；1000 mm reference leakage 可稳定拦截。
- C｜柱网重复：`PM-005=3505.7mm` 驱动同一 `CMP-COLUMN-001` 的 runtime instances；2→3→2 mutation / restore PASS；无新 component identity。
- P2 frozen baseline / 6 个 P3.1 canonical Masters：UNCHANGED。
- ChatGPT structural review：PASS。
- 正式 review PNG：4/4 已从 GitHub 直接调阅并实际逐张目视审核 PASS；遵循 RC-015。
- Product Owner：APPROVED / CLOSED。
- Review：`docs/production/zhenguo_wanfo/P3_2_REPRESENTATIVE_ASSEMBLY_REVIEW_V001.md`。

**T-015 + T-016 完成并不自动等于 P3.2 PASS。**

### P3.2 Current Boundary / Next Step

下一步是**正式 P3.2 Gate Review**。Gate Review 必须逐项核对 DoD V001 的 9 项要求及三项 Gate Hard Fail。

只有当 Gate Review 结论为：

- 9/9 DoD PASS；
- canonical Hard Fail = 0；
- 无需重新发明基础构件组合机制即可进入 P3.3；
- Product Owner 最终批准 Gate；

P3.2 才能标记为 **PASS / APPROVED / CLOSED**，P3 Gate Progress 才从 2/4 变为 3/4，并正式解锁 P3.3。

P3.3 当前继续 LOCKED。