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
