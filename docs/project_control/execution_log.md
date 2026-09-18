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
