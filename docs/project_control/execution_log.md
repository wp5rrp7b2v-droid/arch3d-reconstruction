# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果，只保留足以追溯结论的关键事实、证据、失败原因和最终结果。完整脚本、Workflow、Commit 与历史版本由 GitHub 保存。Checkpoint 可压缩重复或过细记录，但不得丢失正式结论与关键证据。

## T-001～T-004｜P0 技术链验证｜PASS

- T-001：项目工作区建立完成。
- T-002：Local Blender 3.6.23 灰模生成、保存、独立重开、Geometry Integrity、PNG review PASS。
- T-003：Local 3.6 → GitHub Actions Blender 4.5.13 → Local 3.6 roundtrip PASS / Class B；commit `e26d5d600ed693a8e86a914e24dfbe652d718ed3`。
- T-004：JSON 参数驱动、Baseline/Variant 响应、独立重开、Determinism PASS；commit `63a0c506f98d843376361421cf88e1e74c807dc7`。
- P0：4/4 PASS / APPROVED / CLOSED。

## P1｜选题取证｜PASS / CLOSED

- 正式案例：山西平遥镇国寺万佛殿。
- `SRC-ZG-WF-001` 完整精细测绘报告直接核读完成。
- 85/85 关键参数完成分级；Product Owner 批准 `CONDITIONAL GO`；P1 4/4 PASS / CLOSED。

## T-005｜P2.0 Schema Validation｜PASS

- UNKNOWN/DO_NOT_LOCK、RC 可替换、observed / report-ideal / reconstructed 三层语义验证 PASS。
- Canonical evidence commit：`a938d9fe96c579c21fb3a16734f9b74efcd7d8bc`。

## T-006｜P2.1 Production Parameter Set｜PASS

- 85/85 formal parameter + dependency matrix 完成。
- D-023：`Z-006-RC-01 = 11 × MOD-006 = 3534.3mm`，replaceable；Z-006 本体保持 UNKNOWN/null/DO_NOT_LOCK。
- 21/21 tests / production preflight PASS；canonical commit `fc124922d5c0c1674548f9b99968f9848ffbb332`。

## T-007｜P2.2 Structural Skeleton｜PASS / APPROVED

- 6/6 主体结构范围；217 stable machine objects（不等于历史构件数）。
- Machine geometry validation / 32 tests / naked historical constant scan / deterministic rebuild / independent reopen PASS。
- Engineering commit `a5a4181499c0494d16fbaf59d29337fa7d688e9d`。

## T-008｜P2.3 Integrated Reconstruction Candidate｜PASS / APPROVED

- 11 families / 40 variants / 365 stable mesh instances。
- 33/33 tests、34/34 machine QC、Local3.6→Cloud4.5→Local3.6 roundtrip PASS；core semantic diff NONE。
- Engineering commit `93aef4803d2c0d3f7e3e3d29e9ab235c2f92d8f3`；P2 CLOSED / D-028。

## T-009｜P3.0 Component Ontology & Registry Migration｜PASS / APPROVED / CLOSED

- Coverage：11/11 families / 40/40 variants / 365/365 instances；orphan 0/0/0。
- Engineering commit `3db50b94cd72e79cef419054aeaa7d2b75523ba5`；D-031。

## T-010～T-014｜P3.1 Master Library｜PASS / APPROVED / CLOSED

- T-010：Master Scope & Identity；27 records；MASTER_REQUIRED 6 / Deferred 13 / Proxy 4 / Control 3 / Envelope 1；D-033。
- T-011：Column Master Pilot；22/22 checks PASS；D-035；commit `4eb79f37d31202ab2088724008b5412cba4d38b0`。
- T-012：Dou Master Lean Batch；3/3 engineering PASS；19/19 visual PASS；D-037；commit `d1ae53ee368729a395623a8d9a4342f7455e2e9b`。
- T-013：Six-Chuanfu Master Batch；historical full length UNKNOWN/null；1000mm 为 non-historical reference only；13/13 visual PASS；D-039；commit `f607245444927b9853e0976b891673e387a14750`。
- T-014：Master Library Overview；6/6 Masters covered；final overview SHA256 `4719a31c18de13b0453a64d29847381d8e45af0f145bcb37bf7fee0abf9671a7`。
- P3.1 Gate Review：9/9 PASS / APPROVED / CLOSED / D-040。

## T-015～T-016｜P3.2 构件组合关系｜PASS / APPROVED / CLOSED

- T-015：组合关系基础工程；6/6 formal nodes；5/5 relation types；31/31 checks + 21/21 negative tests PASS；D-042；commit `49b0415479d811a26d4f44588d15cd863467edf4`。
- T-016：代表性组合验证；65/65 checks + 15/15 negative tests PASS；A/B/C units validated；4/4 formal review PNG PASS；D-045；commit `fc01ecb4f61128faa95ecf8022d2077a36977a8c`。
- P3.2 Gate Review：9/9 PASS / APPROVED / CLOSED / D-046。

## P3.3 Governance｜2026-09-16

- D-047：P3.3 Definition of Done V001 LOCKED。
- D-048 / RC-017：GitHub Actions headless Blender pipeline approved。
- 5 Hard Fails：`REFERENCE_LENGTH_LEAKS_INTO_BUILDING`、`SILENT_HISTORICIZATION`、`BAKED_MANUAL_BUILDING`、`SILENT_BUILDING_OMISSION`、`BROKEN_COMPONENT_IDENTITY`。

## T-017｜P3.3 Building Input & Assembly Graph｜PASS / CLOSED / D-050

- PR #2 merged；merge commit `1095440af761fc95cc18d0ce01523a097fc8ce5f`。
- 11/11 families / 40/40 variants / 365/365 instances。
- P2 numeric world transforms prohibited as generative input。
- T-017 后续 PURLIN disposition inconsistency 由 T-019 修正；其余基础成果保留。

## T-019｜Upstream Disposition Consistency Correction｜PASS / CLOSED / D-055

- PR #4 merged；merge commit `b9803fb416e375fd2f94f5d83df5fab73fe00063`。
- 7/7 `CMP-PURLIN-001` building instances：`GENERATE_FROM_FORMAL_COMPONENT → DEFERRED`。
- P3.1 qualification 保持 `DEFERRED_INSUFFICIENT_EVIDENCE`；未创建 PURLIN Master；未知截面、长度、端部条件未补造。
- Cross-layer direct-identity conflicts=0；regression `MASTER_SCOPE_DISPOSITION_CONFLICT / EXPECTED_REJECTION`。

---

# T-018｜整殿确定性生成与参数变更验证｜2026-09-17 DAILY CLOSE

## Baseline / branch discipline

- Task Contract：D-051；execution authorization：D-052。
- Existing branch：`codex/t-018`。
- Existing PR：#3。
- No new T-018 branch / PR created。
- PR #3 at close：OPEN / NOT MERGED。
- Current GitHub-visible head：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`。
- Merge authorization：FALSE。

## Correction Round 2｜Whole-building rule consumer completion

Round 2 corrected the earlier false whole-building realization state.

Machine result：

- 365/365 runtime records = `RULE_DERIVED`
- `NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE = 0`
- Formal 12 / Proxy 178 / Control 66 / Envelope 6 / UNKNOWN_BLOCKED 96 / DEFERRED 7
- 7/7 PURLIN remain DEFERRED
- unexplained omission=0
- anonymous formal mesh=0
- broken identity=0
- PM-005 mutation / restore chain PASS

Formal visual review：FAIL。

Reason：non-formal runtime records were still largely displayed as generic point/octahedron markers; spatial data improved, but the four review views did not form a readable engineering assembly system.

## Correction Round 3｜Engineering representation geometry

Round 3 narrowed scope to representation geometry and view-aware review evidence.

Differentiated technical representations implemented for：

- GRID_CONTROL
- BRACKET_CONTACT
- BRACKET_ARM
- FRAME_CONTROL
- FRAME_SUPPORT
- PRIMARY_FRAME
- GABLE_CONTROL
- PURLIN
- RAFTER
- ROOF_ENVELOPE

Review-display constants were isolated from historical / structural dimensions。Generic octahedron-for-all-nonformal was removed。

Codex internal correction SHA：`dbd7fc30836a128914bad0daaeae869d3b9cca04`；internal SHA 仅作辅助，不是 canonical GitHub fact。

## Round 3 GitHub Actions formal evidence

- Workflow：`T-018 P3.3 Deterministic Whole Building`
- Run ID：`35226626839`
- Run number：29
- Head SHA：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Conclusion：SUCCESS
- Blender：4.5.13 linux-x64
- Run A canonical build：PASS
- Run B independent reopen / validation：PASS
- Fixed scripted review rendering：PASS
- Run C PM-005 mutation：PASS
- Run D canonical restore：PASS
- persistent hashes / evidence manifest：PASS
- artifact upload：PASS

Artifact：

- ID `10499236860`
- Name `P3_3_T018_HEADLESS_EVIDENCE_V001`
- Digest `sha256:1acb510ed409e490319d62dad2232d082f163413ab81a209484f00b8b67329fa`
- Expiry 2026-10-17

Machine / representation validation：PASS。

## Formal four-view visual review｜FAIL

ChatGPT directly inspected PLAN / FRONT_ELEVATION / SIDE_ELEVATION / AXON.

Result：

`T-018 = HOLD / MACHINE PASS / FORMAL VISUAL REVIEW FAIL`

Round 3 visual representation was materially better than Round 2, but AXON exposed a roof-control topology anomaly at the ridge：roof surfaces crossed / overlapped instead of terminating cleanly at one shared ridge datum。

## Roof-control origin audit｜READ-ONLY / B-STOP

A read-only audit followed. No project file was modified by the audit。

### Canonical seven-PURLIN control topology

- `ROOF_PURLIN_N_00` = north eave control
- `ROOF_PURLIN_N_01` = north first inward control
- `ROOF_PURLIN_N_02` = north second inward control
- `ROOF_PURLIN_N_03` = shared ridge terminal control
- `ROOF_PURLIN_S_00` = south eave control
- `ROOF_PURLIN_S_01` = south first inward control
- `ROOF_PURLIN_S_02` = south second inward control
- no `ROOF_PURLIN_S_03`; ridge terminal is shared

This semantic map does not upgrade PURLIN historical qualification. PURLIN remains 7/7 DEFERRED。

### Authorized relative chain

`FR-007 = [120,115,210] fen`，read eave→ridge。

With `MOD-002 = 15.3 mm/fen`：

- d1 = 1836.0 mm
- d2 = 1759.5 mm
- d3 = 3213.0 mm
- total half-run D = 6808.5 mm

ROOF-007 / 008 / 009 provide the eave→lower / lower→upper / upper→ridge vertical rise chain。

Existing authoritative inputs are sufficient for the relative topology：

- north：`R-D → R`
- south：`R+D → R`
- one shared terminal：`N03 = R`
- south final segment also terminates at `N03`

They are not sufficient to authorize the absolute value of `R` in T-018 whole-building coordinate space。

### Defect confirmed

Round 2/3 mixed two evidence/time layers：

- observed/as-measured column-grid coordinate frame
- reconstructed-963 candidate roof-control sequence

Round 3 also added `COLUMN_GRID_Y_MIRROR_RULE` to synthesize a missing south terminal. Repository audit found this rule is not present in protected authoritative inputs; therefore it is a synthetic / unauthorized relation。

### Root cause classification

`UPSTREAM ENGINEERING RULE MODELING OMISSION + T018 FAILURE TO STOP`

This is not a newly discovered historical-evidence gap。The missing item is a project-level engineering datum / LOCATE rule defining how the reconstructed-design roof shared ridge datum is embedded in the reconstructed-design whole-building coordinate system。

## Consequence for Round 2 freeze

The prior assumption that Round 2 roof placements were frozen-correct is withdrawn。

After an approved upstream rule exists, at minimum rederive：

- 7 PURLIN controls
- 36 RAFTER proxies
- 6 ROOF_ENVELOPE records
- 4 GABLE_CONTROL records
- any roof-dependent FRAME_CONTROL / FRAME_SUPPORT endpoints

The 365/365 machine PASS proved deterministic self-consistency of the implementation, not authorization of the roof-origin formula。

## Proposed T-020｜NOT AUTHORIZED

Proposed next task：

`T-020｜P3.3_ROOF_SHARED_RIDGE_DATUM_RULE_V001｜屋顶共享脊基准与设计坐标层对齐规则`

Status at 2026-09-17 close：

`PROPOSED / NOT AUTHORIZED / NO BRANCH / NO PR`

Intended scope：

- formalize one shared ridge datum / no S03;
- formalize the reconstructed-design roof ↔ reconstructed-design building coordinate relation;
- preserve FR-007 eave→ridge chain;
- prevent observed reference values from silently becoming reconstructed-design placement inputs;
- keep 7/7 PURLIN DEFERRED;
- historical_claim=false / replaceable project engineering rule;
- prohibit T-018-local invented `*_RULE` from filling the gap。

No T-020 engineering work has started。

## Daily Closing Audit｜2026-09-17

- P3 remains ACTIVE / 3 of 4。
- P3.0 / P3.1 / P3.2 remain PASS / CLOSED。
- P3.3 remains ACTIVE / NOT PASS。
- T-017 CLOSED / D-050；T-019 CLOSED / D-055。
- T-018 PR #3 OPEN / NOT MERGED / head `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`。
- Actions Run `35226626839` SUCCESS；artifact `10499236860` exists。
- T-018 acceptance = HOLD。
- PR #3 merge authorization = FALSE。
- Latest formal Decision ID remains D-055；no new decision ID created today。
- Proposed T-020 remains NOT AUTHORIZED。
- RC-014 Cloud Mode remains ACTIVE through 2026-09-20。
- 2026-09-21 local sync remains pending。
- P3 phase archive action = NONE。
- Detailed session archive：`docs/project_control/DAILY_CLOSE_2026-09-17.md`。

**DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT = PASS**。


---

# T-020｜屋顶共享脊基准与设计坐标层对齐规则｜2026-09-18 START

- Product Owner approved Task Contract：D-056。
- Product Owner execution authorization：D-057。
- Task Contract：`docs/tasks/T-020_P3_3_ROOF_SHARED_RIDGE_DATUM_RULE_V001.md`。
- Classification：`CLOUD_EXECUTABLE`；Blender requirement：NONE。
- Scope：minimal project-level reconstructed-design datum / shared-ridge authority patch only。
- Required preservation：single N03 shared ridge / no S03；FR-007 eave→ridge chain；7/7 PURLIN DEFERRED；observed PM-003～007 remain validation reference；P2 numeric world transforms remain prohibited；historical_claim=false / replaceable project rule。
- T-018 PR #3 remains OPEN / HOLD / NOT MERGED and is protected from T-020 changes。
- Branch / PR at authorization record：NOT YET CREATED / Codex Cloud ready。
- T-020 PASS：NOT YET ASSESSED。


## T-020｜FINAL / PASS / CLOSED / D-058

- Engineering PR：#5 / `codex/-t-020`。
- Initial head：`00d3f3510855d7c0a51a335f5dbf13d91998339a`。
- Formal Review 01：PATCH REQUIRED（self-dependency / duplicate authority / observed-leak coverage / over-broad LOCATE metadata scope）。
- Review Patch 01 GitHub-visible head：`671283f4ffdf8162c4b39de88564264865b29a50`。
- Formal Review 02：PASS。
- Product Owner approval / merge authorization：D-058。
- Merge commit：`6d83ed2f9b3b9281de364ab973edce73ac6dae02`。
- Canonical rule：reconstructed-design X/Y center datum + `RIDGE_Y=0`；Z authority remains Z-007；historical_claim=false；replaceable=true。
- Identity/topology：N03 sole shared ridge terminal；no S03；FR-007 + MOD-002 chain preserved；6808.5mm half-run。
- Evidence boundary：PM-003～007 observed validation reference only；PM-008～012 replaceable reconstructed-design candidates；7/7 PURLIN DEFERRED。
- Machine validation：PASS；canonical_failures=[]；5/5 required negatives EXPECTED_REJECTION；11/40/365 preserved；P2 numeric world-transform usage=0；P3.2 vocabulary unchanged；five P3.3 Hard Fail vocabulary unchanged。
- Blender invocations：0；.blend created：0。
- T-018 PR #3 remained unchanged through T-020 and is now eligible to resume after updating from latest main; merge remains unauthorized。


---

# T-018｜Replacement PR #6｜2026-09-18

- 原 PR #3 因 Codex UI 无法在外部更新后继续写回，保留为 SUPERSEDED / OPEN / DO NOT MERGE。
- Replacement source main：`09d3ca4fab5ca0efb867c5e9c98bf9d2221f9ba9` / R102。
- Replacement PR：#6；GitHub-visible branch `codex/-t-018`；head `65a63b011794dfe2af6a1f0be5ba497a52f23d5f`。
- Changed files：9。
- Actions Run #30 / `35308171567`：FAIL at canonical Blender build due missing script-directory import bootstrap。
- ChatGPT structural review found regression versus PR #3 Round 3 in formal Master geometry, technical representation geometry, T-017/P3.2 traceability, protected-input validation, independent reopen, review framing/evidence, PR-head binding and complete evidence chain。
- Review Patch 01 comment posted to PR #6。
- New contract conflict：PM-005 is observed-reference-only after T-020 D-058; retain as isolation regression, but formal generative mutation parameter requires Product Owner amendment。
- NO MERGE。


---

# T-018 V002 Rebaseline Design Start｜2026-09-18

- Product Owner directed T-018 to enter formal V002 Rebaseline design after repeated V001/replacement failures.
- Engineering HOLD applied: PR #3 read-only superseded; PR #6 HOLD; no further patch, Actions rerun or merge during design.
- Read-only upstream re-audit confirmed T-017 already classifies PM-003～007 as VALIDATION_REFERENCE and PM-008～012 as reconstructed-design geometry candidates; current evidence does not require reopening T-017 accounting.
- V002 draft architecture: 4 management stages + 9 technical checkpoints; authority resolution, control model, independent validator, skeleton first article, 365 runtime, representation/capability regression, dual mutation, then Blender evidence.
- Draft contract: `docs/tasks/T-018_P3_3_DETERMINISTIC_WHOLE_BUILDING_GENERATION_V002.md`.
- Status: DRAFT / PRODUCT OWNER REVIEW REQUIRED / ENGINEERING HOLD.


---

# T-018 V002 Contract Approval｜2026-09-18

- Decision：D-059。
- Product Owner approved and locked T-018 V002 Rebaseline Task Contract。
- V002 supersedes V001 implementation design for future T-018 work；Task ID remains T-018。
- D-052 remains historical V001 execution authorization only and does not authorize V002。
- PR #3：SUPERSEDED / READ-ONLY / DO NOT MERGE。
- PR #6：HOLD / NO PATCH / NO ACTIONS RERUN / DO NOT MERGE。
- Next executable scope after separate authorization：Stage A only (CP-01 + CP-02)。
- Engineering status：NOT STARTED / NOT AUTHORIZED。


---

# T-018 V002 Stage A Entry｜2026-09-18

- Decision：D-060。
- Authorized scope：CP-01 Upstream Compatibility Audit + CP-02 Authority Resolver only。
- Preliminary read-only checks：365/365 across 11 families；P3.2 relation vocabulary exact 5 types；PM-003～007 validation-only；PM-008～012 reconstructed-design candidates；T-020 RIDGE_Y=0 / N03 sole shared ridge / no S03；7/7 PURLIN DEFERRED。
- Stage A formal outputs/review：PENDING。
- Stage B：LOCKED。
- PR #3：SUPERSEDED / READ-ONLY。
- PR #6：HOLD / NO PATCH / NO ACTIONS RERUN / DO NOT MERGE。


---

# T-018 V002 Stage A PASS｜2026-09-18

- Authorization：D-060（Stage A only）。
- CP-01 Upstream Compatibility Audit：PASS。
- CP-02 Authority Resolver：PASS。
- Formal outputs：`docs/evidence/t018_v002/P3_3_T018_V002_UPSTREAM_COMPATIBILITY_AUDIT.json`；`docs/evidence/t018_v002/P3_3_T018_V002_AUTHORITY_RESOLUTION_REPORT.json`。
- 365/365 instances / 11 families；5/5 relationship vocabulary exact；7/7 PURLIN DEFERRED；T-020 RIDGE_Y=0 / N03 sole shared ridge / no ROOF_PURLIN_S_03；P2 numeric world-transform generative usage=0。
- Authority Resolution：42 GENERATIVE_AUTHORITY / 41 VALIDATION_ONLY / 4 PROHIBITED_FOR_PLACEMENT / 0 UNRESOLVED。
- Cross-checks PASS：PM-011=11475mm；PM-012=10710mm；FR-007 half-run=6808.5mm；ROOF-007+008+009=231fen=3534.3mm；Z-006-RC-01=11×MOD-006=3534.3mm。
- Non-blocking guard：ORG-COLUMN-GRID 保留一个 PM-005 node-level parameter_refs 旧关联；该关联无 placement authority，PM-005 固定为 VALIDATION_ONLY。
- Upstream canonical contradiction：0；Stage-B-critical authority gap：0。
- Protected Upstream Baseline：ESTABLISHED FOR T-018 V002。
- PR #6：未修改、未 rerun Actions。
- Stage B：NOT AUTHORIZED。


---

# T-018 V002 Stage B Entry｜2026-09-18

- Decision：D-061。
- Prerequisite：Stage A CP-01/CP-02 PASS；Protected Upstream Baseline established。
- Authorized：CP-03 Building Control Model；CP-04 Independent Invariant Validator；CP-05 Critical Skeleton First Article。
- Stage C：LOCKED。
- 365 full runtime：NOT AUTHORIZED。
- Mutation：NOT AUTHORIZED。
- PR #3：SUPERSEDED / READ-ONLY。
- PR #6：HOLD；not used as Stage B implementation baseline unless separately decided。


---

# T-018 V002 CP-03 STOP｜2026-09-18

- Stage B authorization：D-061。
- CP-03 started and performed the required authority-completeness check before emitting the Building Control Model。
- STOP code：`FRAME_TIER_VERTICAL_AUTHORITY_GAP`。
- Exact vertical placement of `FRAME_TIER_N/S_01..03` and related `FRAME_POST_*_LOW/UP` controls is not fully authorized by current canonical cross-system rules。
- Legacy P2 generator used a formula combining `Z-006-RC-01 + DG-113 + ROOF-004/005/006` and used `DG-113` as a roof-base offset；that implementation is diagnostic only and cannot be inherited because V002 resolver scopes DG-113 to ORG-BRACKET-SYSTEM and ROOF-004/005/006 to ORG-ROOF-SYSTEM, while T-020 defines roof-Z authority without DG-113。
- Continuing would trigger `UNAUTHORIZED_AUTHORITY_USE` / recreate a hidden local rule。
- CP-04：NOT STARTED；CP-05：NOT STARTED；Blender：NOT STARTED；PR #6：UNTOUCHED。
- Stage A retained results remain valid except the previous claim `stage_b_critical_authority_gaps=0`，which is superseded by this finding。
- Diagnostic：`docs/evidence/t018_v002/P3_3_T018_V002_CP03_AUTHORITY_GAP_DIAGNOSTIC.json`。


---

# T-018 V002 Architecture Closure Review｜2026-09-18

- Review scope：bounded / no implementation / no upstream mutation / PR #6 untouched。
- Formal evidence：`docs/evidence/t018_v002/T018_V002_ARCHITECTURE_CLOSURE_REVIEW_V001.md`。
- Outcome：**B｜有限同类缺口**。
- Not A：缺口不只 FRAME_TIER；还包括 exact roof-Z closure、roof runtime topology、downstream proxy/control anchoring。
- Not C：P3.0/P3.1/P3.2 identity/Master/relationship vocabulary、T-017 accounting and parameter classification、T-019 PURLIN disposition、T-020 shared-ridge X/Y authority currently remain usable。
- All identified gaps cluster at one seam：`canonical parameters + P3.2 semantics -> explicit whole-building control placement/topology`。
- Implementation remains frozen；no Rule added；CP-03 not restarted；CP-04/CP-05 not started；Blender/Actions not run；PR #6 untouched。
- Bounded next design, if Product Owner approves：Placement Authority Closure Matrix + Cross-System Dependency DAG + Control Topology Map + Impact/Non-Impact Contract。


---

# T-018 V002 Bounded Completion Package Design Complete｜2026-09-18

- Authorization：D-062 / DESIGN ONLY。
- Four design artifacts completed：Placement Authority Closure Matrix；Cross-System Dependency DAG；Control Topology Map；Impact/Non-Impact Contract。
- Package summary：`docs/evidence/t018_v002/P3_3_T018_V002_CONTROL_PLACEMENT_AUTHORITY_COMPLETION_PACKAGE_V001.md`。
- Architecture Closure outcome remains **B**。
- Minimum proposed authority completions：RZ Roof-Z cumulative closure；FV Frame Vertical Placement bridge。
- RT topology / BA technical anchors / impact contract are technical specifications, not new authority。
- No new historical dimensions introduced；no P3.0/P3.1/P3.2 reopen；no V003 required by current evidence。
- Implementation remains frozen；no Rule created；CP-03 not restarted；PR #6 untouched。


---

# T-018 RZ Contract Locked｜2026-09-18

- Decision：D-063。
- Contract：`docs/tasks/T-018_RZ_ROOF_Z_CUMULATIVE_CLOSURE_V001.md`。
- Locked formula：Z_EAVE=D+H；Z_LOWER=Z_EAVE+ROOF-007×MOD-002；Z_UPPER=Z_LOWER+ROOF-008×MOD-002；Z_RIDGE=Z_UPPER+ROOF-009×MOD-002。
- Current audit values：3534.3 / 4880.7 / 5814.0 / 7068.6 mm。
- ROOF-010/011 validation-only；DG-113 and ROOF-004/005/006 excluded。
- No new historical dimensions；T-020 Y/shared ridge unchanged；7/7 PURLIN remain DEFERRED。
- Implementation/publication：NOT AUTHORIZED。
- CP-03：STOP/HOLD；PR #6：HOLD/UNTOUCHED。


---

# T-018 FV Design Complete｜2026-09-18

- Design artifact：`docs/evidence/t018_v002/P3_3_T018_V002_FV_FRAME_VERTICAL_PLACEMENT_BRIDGE_DESIGN_V001.md`。
- Recommended：FV-B / bounded Roof-elevation bridge without DG-113。
- Rejected：FV-A legacy P2 bridge with DG-113；FV-C roof-profile/drop interpolation。
- Fallback：FV-D semantic-only downgrade。
- Candidate values：FRAME_BASE 3534.3；Tier01 5783.4；Tier02 4528.8；Tier03 3916.8 mm。
- FV-B is NOT LOCKED；implementation remains frozen；CP-03 STOP；PR #6 HOLD。


---

# T-018 FV Semantic Validity Check｜2026-09-18

- Evidence：`docs/evidence/t018_v002/P3_3_T018_V002_FV_SEMANTIC_VALIDITY_CHECK_V001.md`。
- Verdict：FV-B cannot be locked as source-derived Frame authority。
- ROOF-004/005/006 are source-supported roof/purlin elevation design candidates；the exact cumulative mapping into Frame Tier Z is not directly established by source evidence。
- P3.1 CTL-FRAME known-input list is inherited P2 engineering provenance, not independent semantic proof。
- P3.2 Frame tier datums are semantic engineering controls and explicitly do not create historical elevations。
- Allowed next paths only：FV_PROJECT_RULE non-historical project convention；or FV_SEMANTIC_ONLY no exact Z。
- Implementation frozen；CP-03 STOP；PR #6 HOLD。


---

# T-018 FV Contract Locked｜2026-09-18

- Decision：D-064。
- Contract：`docs/tasks/T-018_FV_FRAME_VERTICAL_PLACEMENT_BRIDGE_V001.md`。
- Policy：A / FV_PROJECT_RULE / non-historical project reconstruction convention。
- Locked formula：Base=Z-007+Z-006-RC-01；Tier01=Base+(ROOF-004+005+006)×MOD-002；Tier02=Base+(ROOF-004+005)×MOD-002；Tier03=Base+ROOF-004×MOD-002。
- DG-113 excluded；ROOF-004/005/006 remain Roof-owned；one-way bridge only。
- Current values：3534.3 / 5783.4 / 4528.8 / 3916.8 mm；not historical fact。
- Publication / implementation：NOT AUTHORIZED。
- CP-03：STOP/HOLD；PR #6：HOLD/UNTOUCHED。


---

# Daily Close 2026-09-18｜PASS WITH CAUTION

- Detailed archive：`docs/project_control/DAILY_CLOSE_2026-09-18.md`。
- Latest formal Product Owner decision：D-064。
- New execution/publication authorization at close：NONE。
- T-018 V002：HOLD / NOT PASS。
- P3.3：ACTIVE / NOT PASS。
- RZ D-063：DESIGN CONTRACT LOCKED / production publication not authorized / implementation not proven。
- FV D-064：PROJECT_RULE DESIGN CONTRACT LOCKED / non-historical reconstruction convention / production publication not authorized / implementation not proven。
- CP-03：STOP / not resumed。
- CP-04 / CP-05：NOT STARTED。
- Stage C：LOCKED。
- PR #3：OPEN / SUPERSEDED / READ-ONLY / DO NOT MERGE / head `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750` / mergeable=false at close。
- PR #6：OPEN / HOLD / DO NOT PATCH / DO NOT MERGE / head `65a63b011794dfe2af6a1f0be5ba497a52f23d5f` / mergeable=false at close。
- No post-closure-review Blender run；no post-review Actions artifact；no 365 runtime expansion。

## Carry-forward caution

Today materially improved problem definition but did **not** prove the final correct production architecture.

Do not reuse as current truth:

- Stage A `stage_b_critical_authority_gaps=0`;
- immediate post-T-020 `T-018 READY TO RESUME`;
- PR #3 as active implementation;
- PR #6 as V002-ready implementation;
- legacy P2 Frame Tier formula as authority;
- FV-B as source-derived Frame elevation;
- RZ/FV design lock as technical validation;
- Outcome B as proof no deeper gap exists;
- any statement that V003 is definitely unnecessary.

Current correct language:

> Outcome B is the current bounded-review classification; current evidence does not require V003, but later closure regression may still escalate.

> RZ/FV are controlled design/policy locks pending pre-publication readiness review, machine-readable publication authorization, authority-closure regression, and later CP-03 validation.

## Next-session order

1. Read latest main, `project_state.json`, and `DAILY_CLOSE_2026-09-18.md`.
2. Recheck PR #3 / #6 status and heads.
3. Perform bounded Pre-Publication Readiness Review only.
4. Do not authorize publication by default.
5. If wider ambiguity is exposed, STOP and reconsider Outcome B / V003 rather than forcing RZ/FV into production.


## 2026-09-19｜整殿真实构件实例总表 V001 落档

### 工作性质

- ChatGPT / Product Owner 侧证据复核与项目校准；
- 非 Codex 工程执行；
- 非 Blender 生产；
- 不占用新的 T-###；
- 不产生新的工程执行授权。

### 完成内容

1. 重新核读 SRC-ZG-WF-001 的主体木构、斗栱与屋面相关章节；
2. 将旧工程 family / proxy 与真实建筑构件重新分离；
3. 建立《万佛殿整殿构件实例总表 V001》第一轮底账；
4. 对能够确认的构件记录数量、位置、变体、支承/连接、尺寸来源和模型状态；
5. 明确不能确认的项目继续标记为“待逐件展开 / 待确认”，不从一般古建知识补造；
6. 建立正式证据文件：
   - `docs/evidence/zhenguo_wanfo/P3_WANFO_WHOLE_BUILDING_COMPONENT_INSTANCE_INVENTORY_V001.md`

### 关键发现

- 11/40/365 是工程基线，不是真实构件完整性证明；
- PRIMARY_FRAME / FRAME_SUPPORT / BRACKET_ARM / BRACKET_CONTACT 等代理压缩了大量报告已经能够区分的真实构件；
- 槫总数修正为33根：正身21 + 两山12；
- 当前大量主体梁架构件已具备“实测截面 + 明确装配节点 → 自动求长度”的建模条件；
- 瓦作资料较强；椽系与木基层仍是屋面主要缺口。

### 状态影响

- T-018：继续 HOLD；
- RZ / FV：仍为设计锁定，不发布；
- CP-03 / CP-04 / CP-05：不恢复；
- PR #3 / #6：不合并；
- Blender / Actions / Stage C：不执行；
- P3.3：ACTIVE / NOT PASS。

### 下一步

继续将实例组拆成逐件实例，并复核台基、墙体、围护、门窗等第四系统；在真实构件实例总表进一步闭合前，不恢复整殿工程生成。


# V007 Final High-Risk Component Audit / Build Baseline｜2026-09-19

## Work nature

- Product Owner / ChatGPT evidence audit and project-control synchronization.
- No new Codex engineering task number.
- No Blender run.
- No Actions rerun.
- No PR patch or merge.
- No T-018 execution authorization.

## Audit scope

Re-read `SRC-ZG-WF-001` with expanded scope:

- report body;
- survey drawing atlas, drawings 01–26;
- appendices 1-7 through 1-10.

Only six residual high-risk areas were audited:

1. external bracket-set per-piece counts;
2. interior panjian / timu;
3. rafters;
4. shuzhu;
5. vertical/hip ridge tile counts;
6. door/window woodwork.

## Result

- V007 becomes CURRENT BUILD BASELINE.
- Blanket full-table re-audit stops.
- Shuzhu upgraded to 4 total by explicit derivation from four measured positions + structural drawings.
- External bracket quantities further closed:
  - Tou Ang 16;
  - Er Ang 16;
  - large Guazi Gong 16;
  - small Guazi Gong 28;
  - large Man Gong 16;
  - small Man Gong 28;
  - Ling Gong 28.
- 56 straight-direction first/second-jump Huagong remains a confirmed subset, not whole-building Huagong total.
- Interior system: 24 bracket/separator positions; 12 Panjianfang positions.
- Corrected prior semantic attribution: 215.0×153.6 mm belongs to interior Gong-member material statistics, not Panjianfang section.
- Timu: 23 measured records only; whole-building total remains UNKNOWN.
- Rafters: PARAMETRIC_COMPLETION; real total/section/spacing remain UNKNOWN.
- Vertical ridge: 20 Tongji per ridge / 80 total derived.
- Hip ridge: 5–6 Tongji + Zhaotou per ridge / approximately 20–24 + Zhaotou total derived.
- Door/window: measured elevation drawings authorize medium-detail visual grid/layout; wood section and joinery remain parametric.
- South-window correction retained: east-side wall 84 cm / west-side wall 101 cm.

## Current execution boundary

- T-018 V002: HOLD / NOT PASS.
- P3.3: ACTIVE / NOT PASS.
- RZ / FV: design locks only; no publication.
- CP-03: STOP.
- CP-04 / CP-05: not resumed.
- Stage C: LOCKED.
- PR #3: SUPERSEDED / DO NOT MERGE.
- PR #6: HOLD / DO NOT PATCH / DO NOT MERGE.
- No new Blender / Actions / whole-building expansion.

## Next

Use V007 to redesign:

1. real-component Master completion order;
2. component variants and reusable parameterization;
3. whole-building assembly architecture;
4. replacement boundary for legacy 11/40/365 engineering proxies.

Do not restart T-018 by default.


## V007 Detailed Instance Registry Sync｜2026-09-19

- Added canonical detailed instance registry: `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`.
- Purpose: preserve the V007 per-instance/per-position build baseline in GitHub.
- This synchronization does not change the execution boundary: T-018 remains HOLD; no Blender/Actions/PR merge authorization.


## RC-018｜Component Registry → Excel Derived Sync｜2026-09-19

- Product Owner approved D-065: component registry JSON becomes the single canonical data source; Excel becomes a regenerated derived view, analogous to Dashboard's derived role.
- Added `P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json` and retained immutable versioned registry snapshot `V007.json`.
- Added generator `scripts/generate_wanfo_component_registry_excel.py`.
- Added workflow `.github/workflows/wanfo-component-registry-excel.yml`.
- Generator validates CURRENT=versioned snapshot, workbook sheet set, instance-row count, and SHA-256 manifest.
- During setup, intermediate workflow attempts exposed two implementation defects:
  1. untracked derived files were not detected by `git diff`;
  2. one generator patch accidentally inserted a literal `\n`, causing SyntaxError.
- Both defects were corrected before acceptance.
- Final end-to-end run `35429316513`: **SUCCESS**.
- Final derived commit: `408be1829fd1b190e69eaf0e7543f4dd7f0b7f85`.
- Registry records: 472.
- CURRENT/V007 Excel SHA-256: `b9cd37fb940f7d91e14b11a8aeaadafbac3c6e15a6ef07ae968b6b7afa1f017d`.
- Sync Manifest: `SYNCED`.
- No T-### engineering task was created; this was Project Control/data-derivation infrastructure.
- T-018 remains HOLD; no Blender/Actions modeling, CP-03 restart, PR merge, or P3.3 PASS authorization.


## P3.3 V002｜真实构件驱动整殿重建实施计划锁定｜2026-09-19

- Work nature：Project Control / implementation architecture rebaseline；非 Codex 工程执行。
- Product Owner approval：D-066。
- Current plan：`docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V002.md`。
- 新生产顺序：Master → 变体/接口 → 代表性组合 → 整殿实例/拓扑 → 空间定位 → 确定性整殿生成 → 最终验收。
- P3.0/P3.1/P3.2 历史 PASS/CLOSED 不变。
- 已有6个 Master 保留，但进入新生产前需按 V007 重新绑定/覆盖复核。
- T-018 V002：HOLD / NOT CURRENT EXECUTION ROUTE。
- T-020 / RZ / FV：保留，Stage 5 再审。
- PR #3：SUPERSEDED / DO NOT MERGE。
- PR #6：HOLD / DO NOT PATCH / DO NOT MERGE。
- No Blender run / no Actions modeling run / no new T-### / no Codex modeling authorization。
- Next executable work：需 Product Owner 单独授权 Stage 1。


## Project Control 全目录一致性复核｜2026-09-19

- Trigger：Product Owner 询问“整个 project_control 都更新了吗”。
- Result：发现 `governance.md` 的当前 P3 Scope 仍引用 P3.3 DoD V001 / D-047，且 `CLOUD_MODE_2026-09-16_20.md` 的 R082 entry snapshot 容易被误读为当前状态。
- Correction：
  - `governance.md` 已切换至 P3.3 V002 / D-066 当前路线，并明确 legacy 365、T-018、T-020/RZ/FV、六椽栿长度证据边界；
  - `CLOUD_MODE_2026-09-16_20.md` 明确 R082 仅为进入 Cloud Mode 的起始快照，当前事实以 Project State + Sync Ledger 为准。
- Intentionally unchanged：
  - `DAILY_CLOSE_2026-09-17.md` / `DAILY_CLOSE_2026-09-18.md`：历史日结快照，不回写；
  - `COMPONENT_REGISTRY_EXCEL_SYNC_CONTRACT_V001.md`：RC-018 专项合同，当前内容仍有效；
  - `rules_change_log.md`：D-066 属实施决策/DoD重基线，不是新的 governance rule，因此不新增 RC 编号；
  - `phase_archive/`：历史关闭材料，不回写。
- Current-control chain after correction：project_state / dashboard / decision_log / execution_log / acceptance_matrix / governance / Cloud Sync Ledger are mutually aligned.


## P3.3 V002 Stage 1｜进入真实构件 Master 库｜2026-09-19

- Product Owner authorization：D-067。
- Stage 1 status：ACTIVE。
- First work package：six existing approved Master rebind / coverage review against V007.
- No new T-### yet；this first step is ChatGPT design/review.
- No Blender run / no T-018 restart / no RZ/FV publication / no PR #3/#6 merge.


## P3.3 Stage 1｜既有6个 Master Rebind Review Complete｜2026-09-19

- Authorization：D-067。
- Reviewed：6 existing approved P3.1 Masters against V007 canonical registry。
- Result：6 retained / 0 immediate rebuild。
- Direct rebind：柱、柱头栌斗。
- Rebind + Stage 2 length bridge：下六椽栿、上六椽栿。
- Retain but no physical-instance binding：单向长开斗、交互斗。
- No new T-### / no Blender / no Codex modeling / T-018 remains HOLD。
- Next：build full V007 Master Coverage / Disposition Matrix。


## P3.3 Stage 1｜Master Coverage Matrix + V008 Targeted Patch Proposal｜2026-09-19

- Full current registry coverage classified across 49 registered component/object types.
- During consistency review, found canonical-registry serialization gaps relative to already locked V007 evidence.
- Designed targeted V008 patch:
  - base V007 records preserved;
  - +33 records proposed;
  - expected total 505 registry records;
  - 7 predecessor-only items held as PENDING_SOURCE_BINDING rather than silently imported.
- Proposal docs:
  - `docs/production/zhenguo_wanfo/P3_3_STAGE1_REGISTRY_V008_TARGETED_PATCH_PROPOSAL_V001.md`
  - `production/zhenguo_wanfo/registry/P3_3_STAGE1_REGISTRY_V008_TARGETED_PATCH_PROPOSAL_V001.json`
- No canonical registry update yet; Product Owner approval required.
- No new T-### / no Blender / T-018 HOLD.


## P3.3 Stage 1｜V008 Registry Patch + Coverage Matrix V002 Complete｜2026-09-19

- Product Owner approval：D-068。
- V007 472 records preserved exactly; 33 targeted records appended。
- CURRENT registry advanced to V008 / 505 records。
- RC-018 workflow run `35431569023` PASS。
- CURRENT.xlsx + V008.xlsx generated and committed。
- V008 Master Coverage / Disposition Matrix V002 finalized against 66 registered object types。
- All 66 current object types have explicit disposition。
- 7 items remain PENDING_SOURCE_BINDING: 板瓦 / 勾头 / 滴水 / 博风板 / 悬鱼 / 惹草 / 生头木。
- Next design object：四椽栿 Master Spec。
- No new T-### / no Blender / no T-018 restart。


## P3.3 Stage 1｜四椽栿 Master Spec Locked｜2026-09-19

- Product Owner instruction / approval：D-069。
- Render-first direct source inspection completed on SRC-ZG-WF-001 PDF p82 / printed p67。
- New direct source binding published for 四椽栿。
- Master Spec V001 locked for `CMP-FRAME-FOUR-CHUANFU-001_MASTER`。
- Canonical geometry authority：observed mean section 426.5×302mm。
- Two raw measured section records retained：413×295mm and 440×309mm；their east/west mapping remains UNKNOWN。
- Historical full length remains UNKNOWN/null。
- 1000mm remains non-historical canonical reference only。
- No Codex modeling / no Blender / no new T-### / T-018 remains HOLD。


## T-021｜四椽栿 Master First Article Task Created｜2026-09-19

- Product Owner instruction：create Codex task。
- Task Contract：created and locked under D-070。
- Engineering execution：NOT YET AUTHORIZED。
- Task scope：single four-chuanfu Master First Article only。
- No branch execution / no Codex run / no Blender run yet。
- Next required authorization：Product Owner explicitly says “开始 T-021”。


## T-021｜Execution Attempt STOP / Environment Infrastructure｜2026-09-19

- Codex execution attempt observed.
- STOP classification：ENVIRONMENT / EXECUTION INFRASTRUCTURE。
- Blender 4.5.13 direct download from Codex sandbox：HTTP 403。
- Git remote / GitHub auth：unavailable；cannot push / trigger Actions / create PR。
- Engineering changes：NONE。
- Validation：0/42。
- Protected assets：PASS / unchanged。
- Review artifact / blend / SHA / PR：NONE。
- Contract/evidence conflict：NONE identified。
- T-021 remains same task; next retry = Retry 01 after execution-infrastructure recovery。
- Do not create T-022; do not change Blender pin; T-018 remains HOLD。


## T-021｜Codex Cloud Execution Interpretation Correction｜2026-09-19

- Correction trigger：Product Owner notes the same Codex Cloud/GitHub workflow worked the previous day.
- Previous assumption corrected：`git remote -v` output and `gh auth status` inside the Codex sandbox are **not valid mandatory gates** for Codex Cloud repo/PR capability.
- Codex Cloud officially operates from a repository-bound cloud environment and can surface a task diff/result for Pull Request creation through the product flow; shell Git credentials do not need to be exposed to the agent.
- Therefore the prior “GitHub publish capability unavailable solely because remote/gh auth are absent” conclusion is superseded.
- Correct T-021 flow:
  1. run task in the selected `arch3d-reconstruction` Codex Cloud environment;
  2. Codex writes params/generator/validator/workflow;
  3. Codex sandbox does **not** download/run Blender;
  4. task result/diff is published through Codex Cloud/Create PR flow;
  5. GitHub Actions then executes pinned Blender 4.5.13;
  6. only product-level PR creation failure or Actions-level Blender failure is a valid infrastructure STOP.
- Engineering changes remain NONE so far; validation remains 0/42.
- T-021 remains the same task; no T-022; T-018 remains HOLD.


## T-021｜Executor Override to ChatGPT Direct GitHub｜2026-09-19

- Product Owner approval：D-071。
- Executor change：Codex Cloud → ChatGPT direct GitHub execution。
- GitHub Actions remains the only formal Blender 4.5.13 executor。
- No changes to D-069 spec, validation matrix, mutation contract, review package, binary policy, or merge boundary。
- No T-022 created。
- T-021 remains the active task。
- Engineering implementation has not yet been committed under the new executor path at this checkpoint。


## T-021｜Run #3 PASS + Product Owner Acceptance D-072｜2026-09-19

- Final Actions Run：`35440785415` / SUCCESS。
- Final engineering head：`f16ba22933bb48dbae8951343b76190d2c76c1cf`。
- Validation：42/42 PASS。
- Independent reopen：PASS。
- Length / Width / Thickness mutation：PASS。
- Canonical restore：PASS。
- Review images：6/6 PASS。
- Artifact ID：10583607231。
- Artifact ZIP SHA-256：`2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e`。
- Canonical Master binary SHA-256：`9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997`。
- Semantic geometry signature：`45dce8ce4e58deabd3643c57d0f6caa7ebf50a6189e8d41cf57b68e978b63322`。
- SHA correction：earlier chat report mislabeled semantic geometry signature as binary SHA; artifact itself was correct. No rerun required。
- Product Owner：**APPROVED / D-072**。
- T-021 first article：**CLOSED AS PRODUCT OWNER APPROVED**。
- PR #7：publication closure pending / not merged by D-072 itself。
- P3.3 Stage 1：ACTIVE / not yet passed。
- T-018：HOLD。


## 2026-09-19｜T-021 PR #7 Publication Closure

- Product Owner：D-072 APPROVED。
- Pre-merge check：PASS。
- PR #7：Draft → Ready for Review → MERGED。
- Merged PR head：`983d1505354e38e350b5db0038d90ddc7f41a3d5`。
- Merge commit on main：`2c2c3bc3dea63d7f8449271c47e58d468489c950`。
- Final head Actions Run：`35445039747` = SUCCESS。
- Formal delivery records on main：semantic JSON / validation JSON / engineering review / Stage 1 Master catalog / 6 review PNG / T-021 workflow。
- T-021 publication status：**CLOSED / MERGED TO MAIN**。
- Geometry/evidence boundary：UNCHANGED。
- P3.3 Stage 1：ACTIVE / not yet passed。
- T-018：HOLD。


## 2026-09-19｜Daily Close / Cross-check

- Daily close：**COMPLETE**。
- Canonical state：P3.3 V002 / Stage 1 ACTIVE / 0 of 7 stages passed。
- Registry：V008 / 505 registry records / JSON remains sole authority。
- T-021：Product Owner APPROVED / D-072 / PR #7 MERGED / publication CLOSED。
- PR #7 merge commit：`2c2c3bc3dea63d7f8449271c47e58d468489c950`。
- Final PR head Actions：Run `35445039747` = SUCCESS。
- Formal T-021 delivery on main：semantic JSON / validation JSON / engineering review / Stage 1 Master catalog / 6 review PNG / workflow + scripts。
- No `.blend` committed to Git；approved binary remains Actions artifact evidence。
- SHA correction is fully recorded：approved canonical binary=`9f1c8531...0997`；semantic geometry signature=`45dce8ce...63322`。
- Stage 1 next Master priority：**平梁（priority 2）**。
- 平梁 known boundary：4件；东西缝型与山面型须分证据状态；山面厚度 UNKNOWN，不得统一补写。
- Next session start：先做平梁 direct source/evidence review + Master Spec design；不先建新 T-###，不先跑 Blender。
- 7项继续 PENDING_SOURCE_BINDING：板瓦 / 勾头 / 滴水 / 博风板 / 悬鱼 / 惹草 / 生头木。
- T-018：HOLD。
- T-020 / RZ / FV：Stage 5 re-review。
- Omission audit：no open T-021 publication action remains；no unrecorded merge identified；no new engineering authorization granted。

## 2026-09-20｜T-022 平梁 Master 首件正式验收

- Product Owner：**APPROVED / D-074**。
- PR：#9 / branch `codex/t022-p3-3-pingliang-master-first-article-v001`。
- Reviewed head：`0ddf8290345e4087b7173e89993d3022e2ba730c`。
- Actions Run #2：`35483530705` = **SUCCESS**。
- Machine validation：**56/56 PASS**。
- Blender：4.5.13 LTS。
- EW_SEAM：395.5 × 280.5 mm / DIRECT_MEASURED_FAMILY_MEAN。
- GABLE：346 × 245.4 mm / PARAMETRIC_COMPLETION / replaceable / non-historical；observed thickness remains UNKNOWN/null。
- Independent reopen：EW_SEAM + GABLE = PASS。
- Mutations：Length / EW Width / EW Thickness / GABLE Completion Thickness = PASS；Canonical restore = PASS。
- Review：10/10 PNG = PASS。
- Artifact ID：`10597296654`。
- Artifact ZIP SHA-256：`31670f3654fa2f088900b06c0d7d5d7c1b8a1dbeb221dce692bb85cce4f40839`。
- EW_SEAM canonical binary SHA-256：`5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4`。
- EW_SEAM semantic geometry signature：`5805215c4aa4a18bc3f100af855c2442efdb8d4cb07d334a1aeabbf39b74fdb7`。
- GABLE canonical binary SHA-256：`f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a`。
- GABLE semantic geometry signature：`262f8493b7656f94e4112a8405be565893d89be7c099d83f63bde149d7993c40`。
- Run #1 failure was validator-only strict float equality at 245.4; no geometry/parameter decision changed. Run #2 uses millimetre tolerance and passed all checks.
- Formal delivery next：materialize approved semantic / validation / engineering review / 10 review PNG；修正 T-021 Catalog 状态；登记 T-022；final cross-check；PR #9 remains unmerged until separate merge authorization。
- T-018：HOLD。


## 2026-09-20｜T-022 Formal Delivery Materialization

- Approval authority：D-074 / Product Owner APPROVED。
- Approved source Actions Run：`35483530705` / Artifact `10597296654`。
- Publication workflow Run：`35486003264` = **SUCCESS**。
- Formal delivery commit：`1f2c22f7dcc1034fca4ddb7f28bc6d23af31ed7e`。
- Approved artifact identity verification：PASS。
- Materialized delivery：
  - EW_SEAM semantic JSON；
  - GABLE semantic JSON；
  - 56/56 validation JSON；
  - engineering review；
  - 10 review PNG；
  - Product Owner acceptance / final acceptance records。
- Stage1 Catalog correction：T-021 corrected to `PRODUCT_OWNER_APPROVED / D-072 / CLOSED / MERGED_TO_MAIN`。
- Stage1 Catalog registration：T-022 registered as `PRODUCT_OWNER_APPROVED / D-074 / FORMAL_DELIVERY_MATERIALIZED / PR_MERGE_PENDING`。
- No T-022 `.blend` added to Git；approved binaries remain Actions artifact evidence。
- Publication Run #1 false-fail was an over-broad repository-wide committed-.blend guard；materialization and catalog self-check had already passed. Guard was narrowed to the T-022 staged delivery and Run #3 passed. No model/parameter/evidence change resulted。
- PR #9：OPEN / merge not authorized。
- Next：final pre-merge cross-check, then request separate Product Owner merge authorization。
- T-018：HOLD。

## 2026-09-20｜T-022 PR #9 Merge Closure

- Product Owner merge authorization：**D-075**。
- PR：#9。
- Final validated head：`eaee40b8fd4d50b877956e0b2292538e248b9449`。
- Final head Actions Run：`35486533628` = **SUCCESS**。
- Final cross-check：PASS。
- Merge result：**MERGED**。
- Merge commit：`9e32324baf8257a2b1ddae0033f4797f9e9d9fd4`。
- Stage1 Catalog：T-022 publication status = `CLOSED / MERGED_TO_MAIN`。
- Project State：R143。
- Dashboard：v083。
- T-022：**CLOSED / PRODUCT OWNER APPROVED / PUBLICATION CLOSED**。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Next：丁栿 Master evidence review + specification design。
- T-018：HOLD。

## 2026-09-20｜T-023 PR #10 Merge Closure

- Product Owner merge authorization：**D-081**。
- PR：#10 = **MERGED**。
- Final engineering head：`c07ec0819ceabd9a6d18c6b787196881849e76a6`。
- Final regression Actions Run：`35494632342` = **SUCCESS**。
- Merge commit：`d6f85cd2dc9adf8080ef2a0347449b12ef94c646`。
- T-023 Catalog publication：`CLOSED / MERGED_TO_MAIN`。
- Approved canonical .blend SHA-256 remains `81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737`。
- Semantic geometry signature remains `2cb4b6bcae382f9a35dbca3063439aa025e0b6bba18c4175f63c1f13d089f982`。
- Project State：R149。
- Dashboard：v089。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Next：乳栿 Master；D-076 visual-reference review applies before modeling。
- T-018：HOLD。

## 2026-09-20｜T-024 Formal Delivery + Final Cross-check

- Product Owner first-article approval：**D-085**。
- Approved first-article Run：`35496581278` = SUCCESS / 43 of 43 executed checks PASS。
- Approved canonical .blend SHA-256：`0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208`。
- Semantic geometry signature：`8ae9fea45971f10c14573b8329f7ceff45f7d06dd7d6f99b8bac3ee8273d0571`。
- Formal delivery publication Run：`35497971045` = SUCCESS。
- Formal delivery materialization commit：`fa404ffca1fd3a49cfd70efe0a460048ef6e2f05`。
- Stage1 Catalog：乳栿 = PRODUCT_OWNER_APPROVED / D-085 / FORMAL_DELIVERY_MATERIALIZED。
- Temporary publication workflow：REMOVED。
- Latest branch sync：ahead 14 / behind 0 against main。
- Final head：`232e9f600ec391c46e2a8240281ed3c301c09bd4`。
- Final regression Run：`35498078597` = SUCCESS / **44/44 PASS**。
- Final regression .blend SHA-256：`7d09a7fec162a6d01f95eb914eb34324f0e17350f22377a3547caf9b22c7e208`；该字节哈希为重建产物，不替换 D-085 已批准 canonical binary SHA。
- Final regression artifact：ID `10600838637` / ZIP SHA-256 `2de17b1077473f6a66acbdcf278505e26cc19e5d1f50fedb0256d6afb33a0beb`。
- 6 review PNG：与批准首件逐字节一致。
- Git：无 .blend 提交；PR #11 OPEN / mergeable / MERGE NOT AUTHORIZED。
- T-018：HOLD。

## 2026-09-20｜T-024 PR #11 Merge Closure

- Product Owner merge authorization：**D-086**。
- PR：#11 = **MERGED**。
- Final engineering head：`d857558a1fab765fa269f76ba9217b8456c353aa`。
- Final regression Actions Run：`35498221932` = **SUCCESS / 44/44 PASS**。
- Merge commit：`56ea76ed2bfa766991d4e3f19999dc0c704a48ea`。
- T-024 Catalog publication：`CLOSED / MERGED_TO_MAIN`。
- Approved canonical .blend SHA-256 remains `0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208`。
- Semantic geometry signature remains `8ae9fea45971f10c14573b8329f7ceff45f7d06dd7d6f99b8bac3ee8273d0571`。
- Project State：R158。
- Dashboard：v098。
- P3.3 Stage 1：ACTIVE / NOT PASSED。
- Next：select next missing Master; D-076 visual-reference review applies before modeling。
- T-018：HOLD。

## 2026-09-20｜Daily Close / Local Sync Prep

- Daily Close：**PASS / COMPLETE**。
- Project State：R159。
- Dashboard：v099。
- Cloud Mode 2026-09-16—20：production window **CLOSED**；local sync verification pending。
- T-022 / T-023 / T-024：all approved, published and merged。
- Stage1 approved Master count：10。
- V008：505 records / JSON canonical truth。
- RC-018：V008 / 505 / SYNCED；latest relevant successful Run 35495608194。
- Current engineering T-task：NONE。
- Open PRs：#3 / #6 only；both T-018 HOLD / DO NOT MERGE。
- D-076：ACTIVE for next new Master。
- Local sync preparation：`docs/project_control/LOCAL_SYNC_PREP_2026-09-20.md`。
- Next immediate operation：local Mac read-only preflight + fetch; do not start next Master before local sync verification PASS。
- T-018：HOLD。

## 2026-09-20｜D-087 V008 Master Progress Visibility

- Product Owner requirement：打开 V008 即可看到整体登记规模与 Master 完成进度。
- V008 / CURRENT：已增加 `stage1_master_progress_summary`。
- Row-level：已增加 `stage1_disposition` / `master_coverage_status` / approved `master_reference`。
- Current snapshot：505 records / 66 object types / 28 Master-scope / 10 approved / 18 pending / 35.7%。
- Approved-Master-bound registry rows：52。
- PENDING_SOURCE_BINDING：7。
- Master approval authority：Stage1 Component Master Catalog remains canonical。
- Excel generator：v1.0.2。
- RC-018 Run：35508113993 = SUCCESS。
- V008 derived Excel：新增“进度总览”首页及 Master 状态列。
- Future closure rule：每个新 Master 正式闭环必须同步 V008/CURRENT + derived Excel。
- Engineering impact：NONE；no new T-task / no Blender / T-018 HOLD。


## Local Sync + Approved Artifact Reconciliation｜2026-09-20

- Operation type：local environment reconciliation; not a new engineering T-task.
- Local Git：main fast-forward PASS; working tree clean.
- Sync checkpoint：995a8f42be21e9f1f8c8b013424ea56d5c1b554a.
- Canonical checks：R161 / D-087 / V008 505 / Excel SHA matched.
- Approved artifact binaries restored and SHA-verified:
  - T-021 四椽栿：9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997
  - T-022 平梁 EW_SEAM：5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4
  - T-022 平梁 GABLE：f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a
  - T-023 丁栿：81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737
  - T-024 乳栿：0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208
- Result：PASS / local sync gate CLOSED.
- No Blender binaries committed to Git.
- No new Product Owner decision required; D-087 remains latest formal decision.
- No new T-task created.
- T-018 remains HOLD.


## 2026-09-24｜T-030 Engineering Start

- Product Owner authorization: **D-126 / 开始 T-030**.
- Task: `T-030｜P3_3_DAJIAOLIANG_MASTER_V2_V001`.
- Branch: `codex/t030-p3-3-dajiaoliang-master-v2-v001`.
- Locked instance sections: SE 240×210 / NE 216×187 / SW 218×206 / NW 226×199 mm.
- Family reference specimen: 1000×225×200.5 mm; 1000 mm non-historical only.
- Execution architecture: Master V2 / shared parametric Master / instance-section parameters / endpoint-driven placement.
- Shared infrastructure policy: reuse first; if direct instance-section mapping cannot be expressed, only a minimal generic Definition-driven extension is permitted; T-025–T-029 regression mandatory if shared infrastructure changes.
- Current boundary: first-article execution only. Acceptance/formalization/merge remain unauthorized.
- T-018: HOLD. Stage2: NOT AUTHORIZED.


## 2026-09-24｜T-030 Blocker Disclosure #1

- Status: **BLOCKED / DISCLOSED IMMEDIATELY BEFORE PR/ACTIONS**.
- Blocker: malformed YAML/shell insertion in `.github/workflows/p3_3_master_v2.yml` while implementing the D-126-authorized generic instance-section proof extension.
- Completed before blocker: T-030 branch created; locked Definition created; generic shared builder + validator instance-section support written.
- Not started: Draft PR / GitHub Actions / Blender first article.
- Impact: first article cannot safely start until workflow syntax is repaired.
- Recovery: minimal in-scope repair only; no new architecture/assets/workflow; static verify, then record `BLOCKER CLEARED` before resuming execution.


## 2026-09-24｜T-030 Blocker Cleared #1

- Status: **BLOCKER CLEARED / T-030 EXECUTION RESUMED**.
- Repair: rebuilt `.github/workflows/p3_3_master_v2.yml` from canonical main and re-applied only the D-126-authorized generic instance-section proof extension.
- Static checks: malformed marker absent; exactly one instance-section step; exactly one role-mutation step; validator instance-section argument wired; T-029 added to shared regression; T-030 Definition JSON parse PASS with 4 direct instance sections.
- No new asset class, cache, bridge, workflow or architecture introduced.
- Next: create Draft PR and allow first-article Actions to execute.


## 2026-09-24｜T-030 First Article Run #1 Started

- Draft PR: **#18**.
- Branch: `codex/t030-p3-3-dajiaoliang-master-v2-v001`.
- Head: `eb28017acb82856c01c9f5dda7ed451dc873c363`.
- Actions Run: **35963282233** / P3.3 Master V2 First Article.
- Current observed progress: checkout PASS; locked Definition resolve PASS; Blender 4.5.13 install PASS; canonical Master + review tiles IN PROGRESS.
- Shared infrastructure changed within D-126 scope, therefore mandatory regression set is T-025 / T-026 / T-027 / T-028 / T-029.
- First-article acceptance remains Product Owner-gated.


## 2026-09-24｜T-030 Blocker Disclosure #2｜Actions Timeout

- Status: **BLOCKED / FIRST ARTICLE NOT ACCEPTABLE YET**.
- Run: `35963282233` = **CANCELLED by job timeout**.
- Timeout boundary: workflow job `timeout-minutes: 35`.
- Completed before timeout:
  - T-030 locked Definition resolution PASS.
  - Blender 4.5.13 PASS.
  - canonical Master / reopen / mutation / four instance-section builds / Review Board PASS.
  - T-030 validation = **91/91 PASS**.
  - canonical .blend SHA-256 = `942472630b0998797e9ef3694294fc2ba25c461da1e3df504ee9a56397ecb846`.
  - semantic geometry signature = `b38684fe6adac315a53e62c5d773f36c5eabb305b744e03627b1ac9814f32dc2`.
  - T-025 / T-026 / T-027 / T-028 shared regressions PASS.
- Incomplete:
  - T-029 shared regression did not finish.
  - minimal-sufficient final assertion and artifact uploads were skipped because the job was cancelled.
- Root cause: adding mandatory T-029 regression increased valid regression runtime beyond the existing 35-minute job limit; this is a capacity/time-budget blocker, not a T-030 geometry or validation failure.
- Recommended minimal recovery: change only shared workflow job timeout from **35 → 50 minutes**, then rerun. This changes shared workflow infrastructure and therefore requires Product Owner approval under RC-022.


## 2026-09-24｜T-030 Blocker Disclosure #3｜GitHub Actions Pre-Step Failure

- Product Owner approved D-127 minimal timeout recovery.
- T-030 branch commit: `a8f195822a96b05bc206cd463c057885c47e2bb1`.
- Verified diff from prior runnable head: exactly one workflow line changed: `timeout-minutes: 35` → `50`.
- Recovery Run `35977160199` attempt 1: **FAILURE before any job step**; job has zero steps and no downloadable log.
- One minimal direct rerun was attempted with no code/config changes.
- Run `35977160199` attempt 2: **FAILURE before any job step** again.
- Cross-check: unrelated `Project Dashboard V2 Sync` runs on main (`35976501355`, `35977140275`, `35977387060`) also fail within seconds with zero job steps, while earlier run `35963731352` succeeded.
- Conclusion: current blocker is not T-030 geometry/validator/workflow logic; it is GitHub Actions execution availability at repository/account/service level.
- Specific GitHub-side cause is not exposed by the available connector. Possible account-side causes include Actions usage/billing/spending-limit availability; service-side scheduling is also possible. No such cause is asserted without UI/account evidence.
- T-030 previous engineering evidence remains valid but incomplete for acceptance: main validation 91/91 PASS; T-025–T-028 regressions PASS; T-029 regression/artifact closure incomplete.
- STOP: do not change T-030 architecture or workflow further until ordinary Actions jobs can start again.


## 2026-09-24｜T-030 Blocker Root Cause Confirmed｜GitHub Billing / Spending Limit

- GitHub Actions UI annotation supplied by Product Owner confirms:
  - job not started because recent account payments have failed **or**
  - account spending limit needs to be increased;
  - GitHub directs the account owner to **Billing & plans**.
- This explains both T-030 Run `35977160199` and unrelated Dashboard runs failing within seconds with zero steps.
- Classification: **EXTERNAL ACCOUNT-SIDE GITHUB ACTIONS EXECUTION GATE**.
- Not a T-030 geometry, validator, Master Definition, workflow syntax, or timeout failure.
- Do not modify T-030 code further.
- Resume condition: Billing & plans issue resolved and ordinary GitHub Actions jobs can start again.
- After unblock: rerun T-030 at existing `timeout-minutes: 50`; require T-030 PASS + T-025..T-029 regression PASS + artifact upload before first-article review.


## 2026-09-24｜T-030 First Article Run 35977160199｜SUCCESS

- Run: `35977160199` / attempt 3.
- Head: `a8f195822a96b05bc206cd463c057885c47e2bb1`.
- Result: **SUCCESS**.
- T-030 main validation: PASS.
- T-025 / T-026 / T-027 / T-028 / T-029 shared regressions: PASS.
- Minimal formal artifact assertion: PASS.
- Shared regression evidence upload: PASS.
- Formal V2 first-article artifact upload: PASS.
- First-article artifact: `P3_3_T-030_MASTER_V2_FIRST_ARTICLE_V001` / Artifact ID `10800439343`.
- Shared regression artifact: `P3_3_MASTER_V2_SHARED_REGRESSION` / Artifact ID `10801150421`.
- Current boundary: **ENGINEERING COMPLETE / PENDING PRODUCT OWNER FIRST-ARTICLE REVIEW**.
- Not yet authorized: first-article acceptance, formal materialization, Catalog/V008 approved binding, PR #18 merge, Stage1 PASS, Stage2, T-018 resume.
