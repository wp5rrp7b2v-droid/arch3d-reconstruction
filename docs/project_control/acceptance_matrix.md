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

### T-020｜P3.3 Roof Shared-Ridge Datum Rule｜PASS / CLOSED / D-058

- Task：`T-020｜P3_3_ROOF_SHARED_RIDGE_DATUM_RULE_V001｜屋顶共享脊基准与设计坐标层对齐规则`
- PR #5 reviewed head：`671283f4ffdf8162c4b39de88564264865b29a50`
- Formal Review 02：PASS
- Product Owner approval / merge authorization：D-058
- Merge commit：`6d83ed2f9b3b9281de364ab973edce73ac6dae02`
- Canonical rule：`P3_3_RECONSTRUCTED_DESIGN_DATUM_RULE_V001.json`
- Project rule：`historical_claim=false / historical_claim_upgrade=false / replaceable=true`
- Reconstructed-design plan datum：X=0 / Y=0；Z 继续引用 Z-007
- Shared ridge：`RIDGE_Y=0`；N03 sole terminal；no S03
- FR-007 + MOD-002 dependency lineage：PASS；half-run 6808.5mm
- PM-003～007 observed isolation：PASS
- 7/7 PURLIN：DEFERRED
- accounting：11/40/365 preserved
- P2 numeric world-transform authoritative usage：0
- P3.2 relationship vocabulary：UNCHANGED
- canonical P3.3 Hard Fail vocabulary：UNCHANGED
- 5/5 required negatives：EXPECTED_REJECTION
- Blender invocations / .blend created：0 / 0
- T-018 PR #3：UNCHANGED during T-020

T-020 已关闭。T-018 upstream datum STOP 解除；下一步必须在原 PR #3 同步最新 main 并重新推导 roof-dependent placements。
---

## Current Acceptance Snapshot｜2026-09-18

- P0：CLOSED / PASS
- P1：CLOSED / PASS / CONDITIONAL GO
- P2：CLOSED / PASS
- P3：ACTIVE / 3/4
- P3.0：PASS / CLOSED
- P3.1：PASS / CLOSED
- P3.2：PASS / CLOSED
- P3.3：ACTIVE / NOT PASS
- Current Task：T-018 / READY TO RESUME / PR #3 UPDATE BRANCH REQUIRED
- Last Completed Task：T-020 / PASS / CLOSED / D-058 / PR #5 MERGED
- Latest formal Decision ID：D-058
- PR #3：OPEN / NOT MERGED / merge not authorized
- PR #5：MERGED / T-020 CLOSED
- P3 phase archive：NOT APPLICABLE YET


---

### T-018 Replacement PR #6｜STRUCTURAL REVIEW 01 / PATCH REQUIRED

- Same Task ID：T-018；不是新 Task。
- Base main：`09d3ca4fab5ca0efb867c5e9c98bf9d2221f9ba9` / R102。
- PR #6 head：`65a63b011794dfe2af6a1f0be5ba497a52f23d5f`。
- PR #3：SUPERSEDED / OPEN / DO NOT MERGE。
- Actions Run #30 / `35308171567`：FAIL；Blender 4.5.13 install PASS；canonical Blender build failed with `ModuleNotFoundError: p3_3_whole_building_common_v001`。
- Structural Review：PATCH REQUIRED。Replacement 必须恢复 P3.1 formal Master geometry、differentiated technical representation、T-017/P3.2 traceability、protected-input checks、runtime evidence metadata、true independent reopen、robust fixed review rendering、PR-head SHA binding、完整 Run A/B/C/D evidence chain，同时保持 T-020 datum / RIDGE_Y=0 / N03 sole ridge / no S03 / 7 PURLIN DEFERRED。
- Contract issue：D-051 锁定的 PM-005 mutation 在 T-020 D-058 后只能作为 observed-boundary isolation regression，不能再单独满足 generative mutation propagation。正式 replacement generative parameter 需要 Product Owner amendment。
- T-018：NOT PASS / NO MERGE。


---

### T-018 V002 Rebaseline｜CONTRACT LOCKED / D-059 / EXECUTION NOT AUTHORIZED

- Same Task ID：T-018；Task goal unchanged；version advances V001 → V002 only after Product Owner approval.
- Management stages：A Rule Baseline / B Critical Skeleton First Article / C Full 365 Runtime / D Formal Execution Acceptance.
- Technical checkpoints：CP-01～CP-09 remain internal; no safety check is removed by the 4-stage management compression.
- Key safety changes：single canonical authority consumption；single geometry calculation before Blender；independent invariant validation；skeleton first article before 365 expansion；Golden Capability Contract；observed-isolation + generative-propagation dual mutation；Blender dumb-executor rule.
- Existing P3.3 Hard Fails remain unchanged.
- PR #3：SUPERSEDED / READ-ONLY / DO NOT MERGE。
- PR #6：HOLD / NO PATCH / NO ACTIONS RERUN / DO NOT MERGE。
- Current status：PRODUCT OWNER APPROVED / CONTRACT LOCKED / NO ENGINEERING EXECUTION。


#### Stage A｜规则基线｜REOPENED / AUTHORITY COVERAGE ISSUE

- CP-01 Upstream Compatibility Audit：PASS。
- CP-02 Authority Resolver：PASS。
- Required formal outputs：`P3_3_T018_V002_UPSTREAM_COMPATIBILITY_AUDIT.json`、`P3_3_T018_V002_AUTHORITY_RESOLUTION_REPORT.json`。
- PASS requires：no unresolved canonical contradiction；no missing Stage-B authority；protected-input hashes captured；no unauthorized observed→placement authority；ChatGPT review PASS。
- Stage A classification/isolation checks remain PASS, but authority coverage is REOPENED after CP-03 exposed a missing frame-tier vertical authority.
- Stage B：NOT AUTHORIZED / requires separate Product Owner authorization。


#### Stage B｜关键骨架首件｜STOP / HOLD / D-061

- CP-03 Building Control Model：STOP / FRAME_TIER_VERTICAL_AUTHORITY_GAP。
- CP-04 Independent Invariant Validator：NOT STARTED。
- CP-05 Critical Skeleton First Article：NOT STARTED。
- PASS requires：control model complete；independent invariants PASS；critical skeleton machine review PASS；PLAN/FRONT/SIDE/AXON actual visual review PASS；no structural/topological anomaly。
- Stage C：LOCKED until Stage B formal PASS + separate Product Owner authorization。


#### T-018 V002 Architecture Closure Review｜COMPLETE / OUTCOME B

- Review type：bounded architecture closure review；implementation frozen。
- Outcome A：REJECTED（not a single isolated gap）。
- Outcome B：SELECTED（finite same-layer closure gaps at control-placement seam）。
- Outcome C：NOT SUPPORTED BY CURRENT EVIDENCE（no need yet to reopen P3.0/P3.1/P3.2 or escalate V003）。
- Confirmed closure gaps：Frame vertical placement；exact roof-Z closure；roof runtime control topology；downstream proxy/control anchoring。
- No Rule creation / no Stage B restart / no PR #6 work until bounded completion package is designed and approved。


#### Bounded Control Placement Completion Package｜DESIGN COMPLETE / D-062

- Outcome B remains valid。
- Four closure specifications complete：Placement Authority Closure Matrix；Cross-System Dependency DAG；Control Topology Map；Impact/Non-Impact Contract。
- Proposed authority completions：RZ Roof-Z cumulative closure；FV Frame Vertical Placement bridge。
- No new historical dimensions；P3.0/P3.1/P3.2 remain protected；365 accounting unchanged；PURLIN 7/7 DEFERRED；T-020 shared-ridge X/Y unchanged。
- RT topology / BA technical anchors are specification work only and do not create new authority。
- Implementation：FROZEN。
- CP-03/04/05：NOT AUTHORIZED TO RESUME。
- PR #6：HOLD / UNTOUCHED。


#### RZ｜Roof Z Cumulative Closure｜CONTRACT LOCKED / D-063

- Design：PASS / Product Owner approved。
- Inputs：Z-007 + Z-006-RC-01 + MOD-002 + ROOF-007/008/009。
- ROOF-010/011：validation-only cross-check。
- Excluded：DG-113；ROOF-004/005/006；ROOF-001/002/003；P2 transforms；Blender-local geometry rules。
- Protected：T-020 Y positions；N03 sole ridge；7/7 PURLIN DEFERRED；365 identity/accounting；P3.2 vocabulary。
- Publication / implementation：NOT AUTHORIZED。


#### FV｜Frame Vertical Placement Bridge｜DESIGN COMPLETE / REVIEW REQUIRED

- Recommended candidate：FV-B / no DG-113。
- Inputs：Z-007 + Z-006-RC-01 + MOD-002 + ROOF-004/005/006。
- Boundary：ROOF-004/005/006 remain Roof-owned; FV is a one-way project-level engineering bridge into FRAME_CONTROL only。
- No new historical dimensions；no P3.0/P3.1/P3.2 reopen；no T-020 modification。
- Status：NOT LOCKED / implementation frozen。


#### FV Semantic Validity Check｜COMPLETE / POLICY DECISION REQUIRED

- FV-B as source-derived historical/reconstruction rule：FAIL / insufficient semantic evidence。
- FV-B as explicit PROJECT_RULE reconstruction convention：POSSIBLE / not yet approved。
- Semantic-only Frame Tier without exact Z：SAFE alternative / requires CP-03 acceptance adjustment。
- No Rule locked；implementation frozen；RZ D-063 unchanged。


#### FV｜Frame Vertical Placement Bridge｜CONTRACT LOCKED / D-064

- Policy：A / FV_PROJECT_RULE。
- Evidence status：PROJECT_RULE / historical_claim=false / replaceable=true。
- DG-113 Frame generative-use：PROHIBITED。
- ROOF-004/005/006：remain Roof-owned；consumed only through explicit one-way project bridge。
- No new historical dimensions；no P3.0/P3.1/P3.2 reopen；no T-020 modification。
- Production publication / implementation：NOT AUTHORIZED。


#### Daily Close 2026-09-18｜PASS WITH CAUTION

- P3.3：ACTIVE / NOT PASS。
- T-018 V002：HOLD / NOT PASS。
- Stage A：REOPENED / retained parameter-classification passes only；full authority closure not yet revalidated after RZ/FV。
- Stage B：STOP / CP-03 blocked；CP-04/05 not started。
- Stage C：LOCKED。
- RZ D-063：design lock only；production publication / implementation / regression pending。
- FV D-064：non-historical PROJECT_RULE design lock only；production publication / implementation / regression pending。
- Architecture Closure Outcome B：CURRENT WORKING CLASSIFICATION ONLY；not proof that no wider gap exists。
- Current evidence does not require V003；this is not a permanent prohibition on V003 escalation。
- PR #3：SUPERSEDED / DO NOT MERGE。
- PR #6：HOLD / DO NOT PATCH / DO NOT MERGE。
- Merge authorization：NONE。
- Fresh Blender/Actions evidence after V002 closure review：NONE。
- Daily close evidence：`docs/project_control/DAILY_CLOSE_2026-09-18.md`。

**Hard carry-forward condition:** next session must perform Pre-Publication Readiness Review before any RZ/FV production publication authorization or CP-03 restart。


## 2026-09-19｜整殿真实构件实例校准

- 本轮直接回到 `SRC-ZG-WF-001` 精细测绘报告，按“构件名称 / 数量 / 位置 / 样式 / 连接 / 尺寸来源 / 模型状态”重新审视整殿。
- 结论：既有 `11 families / 40 variants / 365 instances` 继续作为工程基线保留，但**不得解释为万佛殿真实建筑构件完整性已经闭合**。
- 新增正式证据：`docs/evidence/zhenguo_wanfo/P3_WANFO_WHOLE_BUILDING_COMPONENT_INSTANCE_INVENTORY_V001.md`。
- 重要数量修正：槫当前确认总数为 **33根 = 正身七道21根 + 两山12根**；旧“21根”只能指正身槫，不是整殿总数。
- 主体木构、斗栱、屋面三大系统已完成第一轮真实构件复核；若干旧 Proxy / Control 对象被确认覆盖了多个可独立管理的真实构件。
- 当前仍未闭合：丁栿/乳栿/剳牵/托脚等逐件位置；斗栱组内逐件实例；替木/襻间总数；椽系；台基/墙体/门窗等第四系统。
- 本轮不修改 P3.0 / P3.1 / P3.2 历史验收结论，也不授权 T-018 工程执行。
- **T-018 继续 HOLD；P3.3 继续 ACTIVE / NOT PASS。**


## 2026-09-19｜V007 最终高风险核实 / 当前建模基线

- 事实源：`SRC-ZG-WF-001` 正文 + 测绘图录（图纸01–26）+ 附件1-7～1-10。
- 当前正式证据：
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_WHOLE_BUILDING_COMPONENT_INSTANCE_INVENTORY_V007.md`
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INVENTORY_V007_BUILD_BASELINE.json`
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`
- V007 状态：**CURRENT BUILD BASELINE / FINAL HIGH-RISK AUDIT COMPLETE / AUDIT STOP RULE ACTIVE**。
- 主体木构数量继续锁定：柱12、上下六椽栿各2、四椽栿2、平梁4、丁栿8、乳栿8、剳牵14、槫33、阑额12、由额4、大角梁4、子角梁4、隐角梁4、托脚12、叉手8。
- 蜀柱：升级锁定为4根（东缝、东山、西缝、西山各1），证据等级为直接实测位置 + 测绘结构图闭合的明确推导。
- 外檐斗栱：
  - 24个物理铺作位置 = 4转角 + 8非角柱头 + 12补间；
  - 28个立面方向单元；
  - 头昂16、二昂16；
  - 大型瓜子栱16、小型瓜子栱28；
  - 大型慢栱16、小型慢栱28；
  - 令栱28；
  - 正身方向一、二跳华栱56仅为明确子集，不是全殿华栱总数。
- 内槽：附件1-9闭合24个内槽斗栱/隔架位置；襻间枋锁12处位置。
- 重要修正：215.0×153.6mm属于内槽栱件用材统计，**不再作为襻间枋统一截面**。
- 替木：附件1-8有23条实测记录；不得解释为全殿总件数。
- 椽系：正式转为参数化补全；真实逐根数量、标准截面、标准间距保持UNKNOWN。
- 屋脊：
  - 垂脊按每条20块垂通脊、四条80块作为明确推导；
  - 戗脊按每条5–6块通脊砖+找头、四条约20–24块+找头作为明确推导；
  - 正脊赤脚通脊17块继续为直接记录。
- 门窗：南/北立面测绘图允许建立中等精度现状视觉模型；木框断面与榫卯不得历史化。
- 南立面窗局部修正：东窗外侧墙约84cm；西窗约101cm。
- 审计停止规则生效：①直接事实锁定；②明确推导锁定并保留说明；③参数化补全必须可替换且非历史事实；④未知保持未知。
- **本轮不产生工程执行授权。**
- **T-018 V002继续HOLD；P3.3继续ACTIVE / NOT PASS。**


## 2026-09-19｜RC-018 构件登记 JSON → Excel 自动派生

- Decision：D-065 / Product Owner APPROVED。
- Governance：RC-018 ACTIVE。
- Canonical current registry：
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- Versioned snapshot：
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`
- Generator：
  - `scripts/generate_wanfo_component_registry_excel.py`
- Workflow：
  - `.github/workflows/wanfo-component-registry-excel.yml`
- Derived outputs：
  - `docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.xlsx`
  - `docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.xlsx`
  - `docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_EXCEL_SYNC_MANIFEST.json`
- Initial end-to-end workflow：run `35429316513` = **SUCCESS**。
- Validation：
  - CURRENT 与 V007 JSON 快照一致；
  - Registry records = 472；
  - Excel 可重开；
  - Excel instance rows = 472；
  - CURRENT.xlsx 与 V007.xlsx SHA-256 均为 `b9cd37fb940f7d91e14b11a8aeaadafbac3c6e15a6ef07ae968b6b7afa1f017d`；
  - Sync Manifest status = `SYNCED`。
- Rule：**JSON 是唯一事实源；Excel 只读派生，禁止双维护。**
- Failure mode：任何版本/记录数/重开/哈希验证失败必须 FAIL CLOSED。
- 本规则不改变 T-018 工程边界：T-018 继续 HOLD。


## 2026-09-19｜P3.3 V002 真实构件驱动整殿重建实施计划锁定

- Decision：D-066 / Product Owner APPROVED。
- Current plan：`docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V002.md`。
- V001：保留为历史版本，不再是当前 P3.3 实施路线。
- P3.3 当前进度：**0 / 7 new implementation stages formally passed**。
- 七阶段：①真实构件 Master 库；②构件变体与装配接口；③代表性组合验证；④整殿真实实例与拓扑；⑤整殿空间定位与标高规则；⑥确定性整殿生成；⑦整殿验收与 Gate Closure。
- Legacy 11/40/365 与 T-017 365 accounting：历史工程基线 / comparison only。
- T-020 / RZ D-063 / FV D-064：保留，Stage 5 重新审查。
- T-018 V002：**HOLD / NOT CURRENT EXECUTION ROUTE**；Stage 6 前再决定 rebaseline 或 supersede。
- 新增 Hard Fail：`LEGACY_PROXY_AS_REAL_COMPONENT`、`REGISTRY_LAYER_DOUBLE_COUNT`、`UNDECLARED_PARAMETRIC_COMPLETION`、`MASTER_WITHOUT_EVIDENCE_BINDING`、`EXCEL_AS_CANONICAL_SOURCE`。
- Existing five P3.3 Hard Fails continue active。
- 本次无工程执行授权；Stage 1 需另行授权。


## 2026-09-19｜P3.3 V002 Stage 1 进入授权

- Decision：D-067 / Product Owner AUTHORIZED。
- Stage：**Stage 1｜真实构件 Master 库 = ACTIVE**。
- 当前首项：既有6个已批准 Master 对 V007 的重新绑定 / 覆盖 / evidence boundary 复核。
- 复核对象：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿。
- Stage 1 尚未 PASS；当前仍为工作开始状态。
- ChatGPT 设计/复核不占 T-###；实际 Codex 建模任务才创建新 T-###。
- T-018 / RZ / FV / CP-03：继续 HOLD / 不授权。


## 2026-09-19｜P3.3 Stage 1 既有6个 Master 重新绑定复核

- Review：COMPLETE。
- Evidence：
  - `docs/production/zhenguo_wanfo/P3_3_STAGE1_EXISTING_MASTER_REBIND_REVIEW_V001.md`
  - `production/zhenguo_wanfo/registry/P3_3_STAGE1_EXISTING_MASTER_REBIND_MAP_V001.json`
- 6/6 existing Masters retained；0 immediate rebuild required。
- 柱 / 柱头栌斗：可直接绑定 V007 真实实例。
- 下六椽栿 / 上六椽栿：可绑定真实实例，但 Stage 2 必须增加实例装配端点→building-specific geometry length 桥；1000mm reference specimen 继续严禁进入整殿。
- 单向长开斗 / 交互斗：Master 保留，但 V007 未闭合全殿真实总量和逐件位置，当前禁止物理实例绑定。
- 本复核不改变 P3.1 历史 PASS；Stage 1 尚未整体 PASS。
- 下一步：V007 全构件 Master Coverage / Disposition Matrix。


## 2026-09-19｜P3.3 Stage 1 Master Coverage Review / V008 Patch Proposal

- V007 current registry：472 records / 49 registered object types。
- Master Coverage / Disposition Matrix：COMPLETE。
- Finding：49类登记对象并不等于整殿建模对象已完全覆盖；V007 evidence 中还有墙体、地面、神台、望板、屋脊装饰、门窗木作和若干 UNKNOWN family boundary 未序列化到 canonical registry。
- V008 targeted patch proposal：DESIGN COMPLETE / PRODUCT OWNER APPROVAL REQUIRED。
- Proposal：
  - preserve all 472 V007 records；
  - append 33 system/family/entity records；
  - expected V008 registry record count = 505；
  - 505 is registry record count, **not physical component total**。
- Pending source binding（暂不补入 V008）：板瓦、勾头、滴水、博风板、悬鱼、惹草、生头木。
- No new T-### / no Blender / T-018 remains HOLD。


## 2026-09-19｜V008 Targeted Registry Patch / Coverage Matrix V002

- Decision：D-068 / Product Owner APPROVED。
- V008 snapshot：`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json`。
- CURRENT registry：V008 / 505 records。
- Preserved V007 records：472 / 472。
- Added targeted records：33。
- RC-018 workflow run：`35431569023` = **SUCCESS**。
- Derived Excel commit：`5c9b67217cf9bb2100993ee322419481ca446ede`。
- JSON SHA-256：`e6299d8306fd4f58dac29a43230d387c2f63ca4056d002fd03803df02bb072a7`。
- CURRENT/V008 Excel SHA-256：`0174049f8b6f2b0cb86f383011a6700401ea1969c47bd132f0c0c1528cfc3adb`。
- Sync Manifest：SYNCED。
- Master Coverage / Disposition Matrix V002：FINALIZED AGAINST V008。
- V008 当前登记对象类型：66类，全部已有明确 disposition。
- Pending source binding：板瓦、勾头、滴水、博风板、悬鱼、惹草、生头木。
- 四椽栿：**READY FOR SPEC DESIGN**。
- No new T-### / no Blender / T-018 remains HOLD。


## 2026-09-19｜四椽栿 Master Spec V001

- Decision：D-069 / Product Owner APPROVED / LOCKED。
- Spec：
  - `docs/production/zhenguo_wanfo/P3_3_STAGE1_FOUR_CHUANFU_MASTER_SPEC_V001.md`
  - `production/zhenguo_wanfo/registry/P3_3_STAGE1_FOUR_CHUANFU_MASTER_SPEC_V001.json`
- Direct source binding：
  - `docs/evidence/zhenguo_wanfo/P3_3_FOUR_CHUANFU_DIRECT_SOURCE_BINDING_V001.md`
- Source：SRC-ZG-WF-001 PDF p82 / 印刷 p67 / 表2-39 / 图2-40。
- Physical instances：2（东缝1 / 西缝1）。
- Measured sections：413×295mm、440×309mm；mean=426.5×302mm。
- Sample→东/西缝映射：UNKNOWN / 不允许猜配。
- Historical full length：UNKNOWN / null。
- Canonical reference length：1000mm / PROJECT_RULE / NON-HISTORICAL / CANONICAL_REFERENCE_ONLY。
- Report 28分×20分：REPORT_INFERRED metadata only / geometry_use_count=0。
- Geometry：BOUNDED_LONG_MEMBER_OUTER_ENVELOPE / EVIDENCE_BOUNDED_MEDIUM_LOD。
- Spec validation contract：28项。
- Codex / Blender / new T-###：NOT AUTHORIZED。
- Next：separate authorization for 四椽栿 Master First Article engineering task。


## 2026-09-19｜T-021 四椽栿 Master First Article Task Contract

- Decision：D-070。
- Task：`docs/tasks/T-021_P3_3_FOUR_CHUANFU_MASTER_FIRST_ARTICLE_V001.md`。
- Scope：1个首件 Master，`CMP-FRAME-FOUR-CHUANFU-001_MASTER`。
- Contract：LOCKED / PRODUCT OWNER APPROVED。
- Execution：**NOT YET AUTHORIZED**。
- Think Level：MEDIUM DEFAULT / HIGH only by explicit ChatGPT escalation。
- Cloud Mode：CLOUD_EXECUTABLE。
- Blender：GitHub Actions headless / RC-017 / pinned 4.5.13。
- Validation：42项 + length/width/thickness 3类 mutation + independent reopen + canonical restore。
- Review：6张正式 PNG。
- Binary：Git 不提交 .blend；Actions artifact + SHA-256。
- Catalog：P3.3 Stage1 Master catalog record 只能 pending review。
- Branch：`codex/t021-p3-3-four-chuanfu-master-first-article-v001`。
- PR：required / do not merge。
- T-018 / RZ / FV / CP-03：继续 HOLD / 不授权。


## 2026-09-19｜T-021 Executor Override

- Decision：D-071 / Product Owner APPROVED。
- Task：T-021 continues under same task ID。
- Old executor：Codex Cloud writes engineering files。
- New executor：**ChatGPT direct GitHub execution**。
- Blender executor：unchanged / GitHub Actions headless / Blender 4.5.13。
- Spec：D-069 unchanged。
- Validation：42 checks unchanged。
- Mutation：3 probes unchanged。
- Review：6 PNG unchanged。
- Binary artifact/SHA：unchanged。
- Branch/PR rule：ONE TASK = ONE BRANCH = ONE PR / DO NOT MERGE without Product Owner approval。
- T-018：HOLD。
- T-022：NOT CREATED。


## 2026-09-19｜T-021 四椽栿 Master 首件正式验收

- Decision：**D-072 / Product Owner APPROVED**。
- Task：T-021。
- Master：`CMP-FRAME-FOUR-CHUANFU-001_MASTER`。
- Actions Run：`35440785415` = **SUCCESS**。
- Reviewed head：`f16ba22933bb48dbae8951343b76190d2c76c1cf`。
- Machine validation：**42/42 PASS**。
- Independent reopen：PASS。
- Mutations：Length / Width / Thickness = PASS；Canonical restore = PASS。
- Review：6/6 PNG = PASS。
- Artifact ID：`10583607231`。
- Artifact ZIP SHA-256：`2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e`。
- Canonical `.blend` SHA-256：`9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997`。
- Semantic geometry signature：`45dce8ce4e58deabd3643c57d0f6caa7ebf50a6189e8d41cf57b68e978b63322`。
- Correction：此前聊天汇报误把 semantic geometry signature 标为 binary SHA；仅标签错误，不影响工程结果，无需重跑。
- Final：**T-021 FIRST ARTICLE PRODUCT OWNER APPROVED**。
- Boundary：Stage 1 未整体 PASS；PR #7 publication closure 尚未完成；T-018 HOLD。


## 2026-09-19｜T-021 Publication Closure

- T-021 First Article：**PRODUCT OWNER APPROVED / D-072**。
- PR #7：**MERGED**。
- Merge commit：`2c2c3bc3dea63d7f8449271c47e58d468489c950`。
- Final PR head validation：Run `35445039747` = SUCCESS。
- Publication contents：4 formal text/JSON records + 6 review PNG + engineering workflow/scripts。
- Binary Master：remains Actions artifact only; no `.blend` committed to Git。
- Final：**T-021 ACCEPTANCE + PUBLICATION CLOSURE COMPLETE**。
- Boundary：Stage 1 remains ACTIVE; this does not authorize Stage 2 or resume T-018。

## 2026-09-20｜T-022 平梁 Master 首件正式验收

- Decision：**D-074 / Product Owner APPROVED**。
- Task：T-022。
- Master：`CMP-FRAME-PINGLIANG-001_MASTER`。
- Variants：`EW_SEAM` / `GABLE`。
- Actions Run：`35483530705` = **SUCCESS**。
- Reviewed head：`0ddf8290345e4087b7173e89993d3022e2ba730c`。
- Machine validation：**56/56 PASS**。
- Independent reopen：both PASS。
- Mutation / restore：PASS。
- Review：10/10 PNG = PASS。
- Artifact ID：`10597296654`；ZIP SHA-256=`31670f3654fa2f088900b06c0d7d5d7c1b8a1dbeb221dce692bb85cce4f40839`。
- EW_SEAM：395.5 × 280.5 mm / measured-family mean。
- GABLE：346 × 245.4 mm；245.4 = explicit PARAMETRIC_COMPLETION / replaceable / historical_claim=false；observed thickness remains UNKNOWN/null。
- Historical full length：UNKNOWN/null；1000 mm remains non-historical Master reference only。
- Final：**T-022 FIRST ARTICLE PRODUCT OWNER APPROVED**。
- Publication boundary：formal materialization + Stage1 Catalog correction/registration + final cross-check pending；PR #9 merge not yet authorized。
- Boundary：P3.3 Stage 1 remains ACTIVE / not passed；Stage 2 not authorized；T-018 HOLD。


## 2026-09-20｜T-022 Formal Delivery / Pre-Merge Boundary

- T-022 first article：**PRODUCT OWNER APPROVED / D-074**。
- Formal delivery materialization：**PASS**。
- Publication workflow Run：`35486003264` = SUCCESS。
- Formal delivery commit：`1f2c22f7dcc1034fca4ddb7f28bc6d23af31ed7e`。
- Stage1 Catalog：
  - T-021 = PRODUCT_OWNER_APPROVED / D-072 / publication CLOSED；
  - T-022 = PRODUCT_OWNER_APPROVED / D-074 / formal delivery materialized / PR merge pending。
- Formal T-022 delivery includes 2 semantic JSON + 1 validation JSON + engineering review + 10 review PNG + approval records。
- Binary Masters remain Actions artifact only；no T-022 .blend in Git delivery。
- Pre-merge requirement：final branch cross-check + latest applicable T-022 validation status review。
- PR #9：**DO NOT MERGE until separate Product Owner authorization**。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- T-018：HOLD。

## 2026-09-20｜T-022 Merge Closure

- Product Owner merge authorization：**D-075**。
- PR #9：**MERGED**。
- Merge commit：`9e32324baf8257a2b1ddae0033f4797f9e9d9fd4`。
- Final head：`eaee40b8fd4d50b877956e0b2292538e248b9449`。
- Final head Actions Run：`35486533628` = SUCCESS。
- T-022 publication：**CLOSED / MERGED_TO_MAIN**。
- Stage1 Master Catalog approved count：8。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Next formal work item：丁栿 Master evidence review / Spec design。
- T-018：HOLD。

## 2026-09-20｜T-023 Merge Closure

- Product Owner merge authorization：**D-081**。
- PR #10：**MERGED**。
- Merge commit：`d6f85cd2dc9adf8080ef2a0347449b12ef94c646`。
- Final head：`c07ec0819ceabd9a6d18c6b787196881849e76a6`。
- Final Actions Run：`35494632342` = SUCCESS。
- T-023 publication：**CLOSED / MERGED_TO_MAIN**。
- Stage1 Master Catalog approved count：9。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Next formal work item：乳栿 Master visual-reference review + evidence review + Spec design。
- D-076：ACTIVE for 乳栿 and later new components。
- T-018：HOLD。

## 2026-09-20｜T-024 Final Pre-Merge Acceptance State

- Product Owner first-article approval：**D-085**。
- Formal delivery：**MATERIALIZED**。
- Stage1 Catalog：乳栿 **PRODUCT_OWNER_APPROVED**。
- Approved canonical binary SHA-256：`0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208`。
- Semantic geometry signature：`8ae9fea45971f10c14573b8329f7ceff45f7d06dd7d6f99b8bac3ee8273d0571`。
- Final head：`232e9f600ec391c46e2a8240281ed3c301c09bd4`。
- Final Actions Run：`35498078597` = **SUCCESS / 44/44 PASS**。
- UPPER / LOWER / NE / SE / SW / NW：shared geometry。
- Historical full length：UNKNOWN / null。
- Exact plan angle：UNKNOWN / null / no 45-degree default。
- Groove：DIRECT_EXISTENCE / GEOMETRY_DEFERRED。
- Review PNG：6/6 retained byte-identical。
- Branch sync：ahead 14 / behind 0。
- PR #11：OPEN / mergeable / **WAITING FOR PRODUCT OWNER MERGE AUTHORIZATION**。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- T-018：HOLD。

## 2026-09-20｜T-024 Merge Closure

- Product Owner merge authorization：**D-086**。
- PR #11：**MERGED**。
- Merge commit：`56ea76ed2bfa766991d4e3f19999dc0c704a48ea`。
- Final head：`d857558a1fab765fa269f76ba9217b8456c353aa`。
- Final Actions Run：`35498221932` = SUCCESS / 44/44 PASS。
- T-024 publication：**CLOSED / MERGED_TO_MAIN**。
- Stage1 Master Catalog approved count：10。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Next formal work item：select next missing Master → D-076 visual-reference review → evidence review → Spec design。
- T-018：HOLD。

## 2026-09-20｜Daily Close State

- Overall close：**PASS / COMPLETE**。
- Latest formal Product Owner decision：D-086。
- T-022：CLOSED / PR #9 MERGED。
- T-023：CLOSED / PR #10 MERGED。
- T-024：CLOSED / PR #11 MERGED。
- Stage1 Component Master Catalog：10 approved。
- Registry：V008 / 505。
- Derived Excel：V008 / 505 / SYNCED。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Current engineering T-task：NONE。
- Next modeling Master：NOT YET SELECTED。
- Local sync verification：PENDING / prepared。
- T-018：HOLD。

## 2026-09-20｜D-087 Registry Visibility

- Status：**IMPLEMENTED / SYNC PASS**。
- V008：505 records / 66 registered object types。
- Stage1 Master scope：28 object types。
- Approved Masters：10。
- Pending Masters：18。
- Completion：35.7%。
- Approved-Master-bound rows：52。
- Derived Excel Run：35508113993 = SUCCESS。
- Authority boundary：Master Catalog controls approval/version/SHA/publication; V008 exposes linkage/progress only。
- Next Master：NOT STARTED。
