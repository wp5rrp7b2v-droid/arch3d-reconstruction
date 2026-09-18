# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED

| Gate | 状态 | 关键边界 |
|---|---|---|
| P0.0 | PASS | Project Control 文件集可跨 Chat 作为正式 handoff；Dashboard 为派生可视化。 |
| P0.1 | PASS | Local Blender 3.6.23 灰模生成 / 保存 / 重开 / 几何完整性 / PNG review PASS。 |
| P0.2 | PASS / Class B | Local3.6→GitHub Actions Blender4.5→Local3.6 roundtrip PASS。 |
| P0.3 | PASS | 参数驱动、独立重开、Determinism PASS。 |

**P0 Final：4/4 PASS / CLOSED。**

---

## P1｜选题取证｜CLOSED / APPROVED

| Gate | 状态 | 关键边界 |
|---|---|---|
| P1.0 | PASS | 五项加权选题标准锁定。 |
| P1.1 | PASS | 山西平遥镇国寺万佛殿正式定选。 |
| P1.2 | PASS | `SRC-ZG-WF-001` 完整精细测绘报告纳入正式证据包。 |
| P1.3 | PASS / CONDITIONAL GO | 85/85 参数分级；CG-01～CG-06 生效。 |

**P1 Final：4/4 PASS / CLOSED。**

---

## P2｜正式参数化与3D复原｜CLOSED / APPROVED

| Gate | 状态 | 关键边界 |
|---|---|---|
| P2.0 | PASS | Evidence-aware Parameter Schema。 |
| P2.1 | PASS / CLOSED | Z-006 保持 UNKNOWN；Z-006-RC-01 replaceable。 |
| P2.2 | PASS / CLOSED | Parametric Structural Skeleton；217 machine objects 不等于历史构件数。 |
| P2.3 | PASS / CLOSED | 11 families / 40 variants / 365 stable mesh instances；D-028。 |

**P2 Final：4/4 PASS / CLOSED。**

---

## P3｜古建筑构件系统化与组合建模｜ACTIVE

| Gate | 验收目标 | 当前状态 | 关键边界 |
|---|---|---|---|
| P3.0 | Component Ontology & Registry | PASS / APPROVED / CLOSED | DoD 9/9；11/40/365 全量迁移；D-031。 |
| P3.1 | Component Master & Variant Library | PASS / APPROVED / CLOSED | DoD 9/9；6/6 Master Approved；D-040。 |
| P3.2 | 构件组合关系模型 | PASS / APPROVED / CLOSED | DoD 9/9；五类关系与接口 foundation；D-046。 |
| P3.3 | 构件驱动整殿重建 | **ACTIVE / T-018 HOLD** | T-017 / T-019 已关闭；T-018 machine PASS 但 formal visual review FAIL；缺 upstream shared-ridge datum / design-coordinate alignment rule。 |

**P3 Gate Progress：3/4。**

### P3.1 Final｜PASS / D-040

- MASTER_REQUIRED：6/6 approved。
- Proxy / Control / Envelope / Deferred 保持非历史化。
- Carry-forward：Z-006 UNKNOWN/null；DG-114 UNKNOWN；HIS-002 originality unknown；45°转角/榫卯/隐角梁 unresolved；六椽栿 historical full length UNKNOWN/null；1000mm 仅 non-historical reference。

### P3.2 Final｜PASS / D-046

- DoD：9/9 PASS。
- Canonical Hard Fail：0。
- P3.3 foundational readiness：PASS。
- P3.2 不因本次 P3.3 building-level datum rule 漏项而重新开启；本次缺口属于 P3.3 上游工程规则补全。

### P3.3 Definition of Done V001｜LOCKED / D-047

正式文件：`docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`

Gate Hard Fail：

- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `SILENT_HISTORICIZATION`
- `BAKED_MANUAL_BUILDING`
- `SILENT_BUILDING_OMISSION`
- `BROKEN_COMPONENT_IDENTITY`

### T-017｜整殿输入基线与 Assembly Graph｜PASS / CLOSED / D-050

- PR #2 merged。
- 11/11 families；40/40 variants；365/365 instances。
- P2 numeric world transforms 明确禁止作为 P3.3 generative input。
- T-019 后 7/7 PURLIN disposition 已修正为 DEFERRED。
- 2026-09-17 T-018 审核发现一个未在 T-017 正式表达的 building-level roof datum rule gap：shared ridge 如何定位到 reconstructed-design building coordinate system。

### T-019｜上游 Disposition 一致性修正｜PASS / CLOSED / D-055

- PR #4 merged；merge commit `b9803fb416e375fd2f94f5d83df5fab73fe00063`。
- 7/7 `CMP-PURLIN-001`：`DEFERRED`。
- P3.1 qualification 继续 `DEFERRED_INSUFFICIENT_EVIDENCE`；未创建 PURLIN Master；未知截面/长度/端部条件未补造。

### T-018｜整殿确定性生成与参数变更验证｜HOLD

**Current PR:** #3 / OPEN / NOT MERGED  
**Current GitHub-visible head:** `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`  
**Merge authorized:** NO

#### Round 2 machine correction

- 365/365 `RULE_DERIVED`
- `NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE = 0`
- Formal 12 / Proxy 178 / Control 66 / Envelope 6 / UNKNOWN_BLOCKED 96 / DEFERRED 7
- 7/7 PURLIN = DEFERRED
- omission=0；anonymous formal mesh=0；broken identity=0
- PM-005 mutation / restore PASS

Round 2 formal visual review：FAIL。原因是 non-formal family 仍主要表现为 generic point/octahedron marker，无法形成可读整殿工程系统。

#### Round 3 engineering representation

Round 3 将 GRID / BRACKET / FRAME / GABLE / PURLIN / RAFTER / ROOF_ENVELOPE 分别转为差异化的 engineering representation geometry，并引入 view-aware projected-in-frame evidence。

Machine / Actions evidence：

- Actions Run `35226626839` / run #29
- Head SHA `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Conclusion `SUCCESS`
- Artifact ID `10499236860`
- Artifact digest `sha256:1acb510ed409e490319d62dad2232d082f163413ab81a209484f00b8b67329fa`
- generic octahedron=0
- Run A / B / C / D PASS
- Blender reopen / validation PASS
- mutation / restore PASS

**Machine acceptance：PASS。**

#### Formal visual review｜FAIL / HOLD

ChatGPT 实际审核 PLAN / FRONT / SIDE / AXON 四张 review PNG 后，发现屋顶脊部发生交叉/重叠。

进一步只读审计确认：

- 7-PURLIN canonical identity topology = `N00,N01,N02,N03(shared ridge),S00,S01,S02`
- 不存在 S03；N03 是唯一 shared ridge terminal control
- `FR-007=[120,115,210] fen`，读取方向为 eave→ridge
- `MOD-002=15.3 mm/fen`
- eave→ridge total half-run = `6808.5 mm`
- ROOF-007 / 008 / 009 = eave→lower / lower→upper / upper→ridge rise chain
- 现有正式输入足以确定南北两坡相对单调趋近同一 shared ridge 的拓扑
- 现有正式输入**不足以**确定 shared ridge 在 T-018 whole-building coordinate space 中的绝对坐标 R

当前实现缺陷：

- Round 2/3 将 observed/as-measured column-grid coordinate frame 与 reconstructed-963 roof-control sequence 混用；
- Round 3 新增 `COLUMN_GRID_Y_MIRROR_RULE`，但该 rule 不存在于 protected authoritative inputs；
- 因此该 relation 判定为 synthetic / unauthorized；
- previous Round 2 roof-placement freeze assumption 失效。

至少以下对象需在 upstream datum rule 批准后重新推导：

- 7 PURLIN controls
- 36 RAFTER proxies
- 6 ROOF_ENVELOPE records
- 4 GABLE_CONTROL records
- roof-dependent FRAME_CONTROL / FRAME_SUPPORT endpoints

**T-018 Final Status at 2026-09-17 close：**

`HOLD / MACHINE PASS / FORMAL VISUAL REVIEW FAIL / UPSTREAM RULE GAP`

### T-020｜P3.3 Roof Shared-Ridge Datum Rule｜CONTRACT LOCKED / EXECUTION AUTHORIZED

建议任务：

`T-020｜P3.3_ROOF_SHARED_RIDGE_DATUM_RULE_V001｜屋顶共享脊基准与设计坐标层对齐规则`

当前仅为：

`ACTIVE / CONTRACT LOCKED / D-056 / EXECUTION AUTHORIZED D-057 / CODEX CLOUD READY / NO PR YET`

目标不是新增历史尺寸，而是补齐 project-level engineering datum / LOCATE semantics：

- 一个 shared ridge terminal；no S03；
- FR-007 两侧 eave→ridge；
- reconstructed-design roof 与 reconstructed-design building center datum 的坐标关系；
- observed reference layer 不得静默成为 reconstructed-design placement source；
- 7/7 PURLIN 继续 DEFERRED；historical_claim=false；replaceable project rule；
- 禁止通过 T-018-local invented `*_RULE` 填补缺口。

T-020 Task Contract 已由 Product Owner 批准并锁定（D-056），并已授权执行（D-057）。在 T-020 完成工程、ChatGPT formal review、Product Owner 批准并 merge 前，T-018 不得继续 placement correction。

---

## Current Acceptance Snapshot｜2026-09-17

- P0：CLOSED / PASS
- P1：CLOSED / PASS / CONDITIONAL GO
- P2：CLOSED / PASS
- P3：ACTIVE / 3/4
- P3.0：PASS / CLOSED
- P3.1：PASS / CLOSED
- P3.2：PASS / CLOSED
- P3.3：ACTIVE / NOT PASS
- Current Task：T-020 / EXECUTION AUTHORIZED / CODEX CLOUD READY
- Held Downstream Task：T-018 / HOLD / PR #3 OPEN
- Latest formal Decision ID：D-057
- PR #3：OPEN / NOT MERGED
- P3 phase archive：NOT APPLICABLE YET
