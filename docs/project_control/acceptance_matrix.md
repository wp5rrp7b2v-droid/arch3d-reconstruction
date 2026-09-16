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
|---|---|---|---|
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
| P3.2｜构件组合关系模型 | 建立构件资格、承托/连接/定位/重复/从属、接口、参数传递、组合单元、重建验证 | **PASS / APPROVED / CLOSED** | DoD 9/9；canonical Hard Fail=0；T-015 / D-042；T-016 / D-045；Gate closure D-046。 |
| P3.3｜构件驱动整殿重建 | 用构件库 + 构件组合关系 + 建筑参数重组万佛殿 | **ACTIVE / T-017 PASS / D-050 / NEXT ENGINEERING TASK REQUIRED** | T-017 已完成 DoD-01～04 的基础工程与 DoD-07/08 的部分验证基础；P3.3 尚未 Gate PASS。 |

**P3 Gate Progress：3 / 4。**

### P3.1 Gate Final｜PASS / APPROVED / CLOSED / D-040

- DoD：9 / 9 PASS。
- `MASTER_REQUIRED`：6 / 6 approved。
- Proxy 4 / Control 3 / Envelope 1 / Deferred 13 保持非历史化。
- Formal registered variants：0；参数化能力已由 mutation / rebuild 验证。
- Gate Review：`docs/production/zhenguo_wanfo/P3_1_GATE_REVIEW_2026-09-13.md`。

Carry-forward：Z-006 UNKNOWN/null；Z-006-RC-01 replaceable；DG-114 UNKNOWN；HIS-002 originality unknown；45°转角/榫卯/隐角梁 unresolved；六椽栿 historical full length UNKNOWN/null；1000 mm 仅 non-historical reference。

### P3.2 Definition of Done V001｜LOCKED / PRODUCT OWNER APPROVED / D-041

正式文件：`docs/production/zhenguo_wanfo/P3_2_DEFINITION_OF_DONE_V001.md`

9 项 DoD：组合范围与构件资格；构件关系分类体系；构件接口与定位规则；代表性组合单元与关系覆盖；尺寸与参数传递；史料依据与不确定性边界；机器验证与组合关系完整性；确定性重建与参数变更验证；P3.3 整殿重建就绪性验证。

Gate Hard Fail：`REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`、`SILENT_HISTORICIZATION`、`BAKED_MANUAL_ASSEMBLY`。

### T-015｜构件组合关系基础工程实现｜PASS / APPROVED / CLOSED / D-042

- Engineering commit：`49b0415479d811a26d4f44588d15cd863467edf4`。
- Approved Master node mapping：6/6 PASS；五类基础关系 5/5；6 个 Master / 18 个最小局部接口。
- Machine validation：31/31 PASS；Negative tests：21/21 expected rejection PASS；canonical Hard Fail=0。
- P2 frozen baseline / P3.1 canonical Masters：UNCHANGED。
- Review：`docs/production/zhenguo_wanfo/P3_2_RELATIONSHIP_FOUNDATION_REVIEW_V001.md`。

### T-016｜代表性构件组合验证｜PASS / APPROVED / CLOSED / D-045

- Engineering commit：`fc01ecb4f61128faa95ecf8022d2077a36977a8c`。
- Machine validation：65/65 PASS；Negative tests：15/15 expected rejection PASS；Canonical Hard Fail：0；五类关系代表性覆盖 5/5。
- A｜柱—柱头栌斗：interface-driven Blender rebuild / independent reopen / determinism PASS。
- B｜六椽栿梁架层位：`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED` 为预期 PASS；1000 mm reference leakage 可稳定拦截。
- C｜柱网重复：`PM-005=3505.7mm` 驱动同一 `CMP-COLUMN-001` runtime instances；2→3→2 mutation / restore PASS。
- 正式 review PNG：4/4 direct GitHub visual review PASS；P2 frozen baseline / 6 个 P3.1 canonical Masters UNCHANGED。
- Review：`docs/production/zhenguo_wanfo/P3_2_REPRESENTATIVE_ASSEMBLY_REVIEW_V001.md`。

### P3.2 Gate Final｜PASS / APPROVED / CLOSED / D-046

正式文件：`docs/production/zhenguo_wanfo/P3_2_GATE_REVIEW_2026-09-14.md`

- DoD：**9 / 9 PASS**。
- Canonical Hard Fail：**0**。
- P3.3 foundational readiness：**PASS**。
- Additional engineering task required before Gate decision：**NO**。
- Product Owner：**APPROVED / D-046**。

Carry-forward 到 P3.3：

- 六椽栿 historical full length UNKNOWN/null；未获独立批准前继续 geometry BLOCKED；
- Z-006 UNKNOWN/null/DO_NOT_LOCK；Z-006-RC-01 继续 replaceable RC；
- 具体榫卯、隐藏连接、45°转角、隐角梁等继续保持现有 evidence boundary；
- Deferred / Proxy / Control / Envelope / UNKNOWN 不得因整殿重建而静默历史化；
- P3.3 可在已批准五类关系、接口/定位、Assembly Unit、runtime instance、building-level parameter 与 validator 体系上扩展具体整殿实例，但不得重新定义基础关系体系。

### P3.3 Definition of Done V001｜LOCKED / PRODUCT OWNER APPROVED / D-047

正式文件：`docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`

9 项 DoD：正式输入基线；整殿 Assembly Graph；建筑参数驱动与参数传递；全殿语义覆盖与对象 accounting；确定性整殿生成；空间/几何/结构一致性；Evidence Boundary 保持；机器验证/Hard Fail/参数 Mutation；独立重建与最终 Gate Evidence Package。

Gate Hard Fail：

- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `SILENT_HISTORICIZATION`
- `BAKED_MANUAL_BUILDING`
- `SILENT_BUILDING_OMISSION`
- `BROKEN_COMPONENT_IDENTITY`

RC-014 Cloud Mode 中，每个后续工程任务必须先分类为 `CLOUD_EXECUTABLE`、`DESIGN_ONLY` 或 `LOCAL_MAC_REQUIRED`。

### T-017｜整殿输入基线与 Assembly Graph 基础工程｜PASS / APPROVED / CLOSED / D-050

- GitHub PR：`#2`；reviewed head：`f117cb98da713e5279174248076421caa9d9e6f4`；merge commit：`1095440af761fc95cc18d0ce01523a097fc8ce5f`。
- 五个正式机器输出：**5 / 5 PASS**。
- Scope accounting：**11 / 11 families；40 / 40 variants；365 / 365 instances**；unexplained omission=0；orphan=0。
- Input Baseline：四类输入分类完整；P2 numeric world transforms 明确为 `PROHIBITED_AS_GENERATIVE_INPUT`。
- Parameter Bindings：参数 → evidence/time layer → building role → graph node / relationship / rule dependency 显式可追溯。
- Assembly Graph：`BUILDING_ROOT → ORG-BUILDING → assembly organization → runtime nodes`；P3.2 foundation traceability PASS。
- Canonical Hard Fail：**0**；5/5 synthetic negative fixtures expected rejection；HF-01 真实注入六椽栿 1000mm reference leakage，HF-03 真实注入 P2 location/rotation/scale。
- Deterministic regeneration / stable serialization PASS；protected inputs unchanged；Blender invocations=0；`.blend` created=0。
- Product Owner：**APPROVED / D-050**；T-017 CLOSED。

T-017 的关闭只证明 P3.3 的输入、参数绑定、语义 accounting、Assembly Graph 与基础验证体系成立；**不等于 P3.3 Gate PASS**。后续仍需完成至少 DoD-05 确定性整殿生成、DoD-06 空间/几何/结构一致性、DoD-08 building-parameter mutation/rebuild 的正式执行证据，以及 DoD-09 independent rebuild / final Gate Evidence Package。