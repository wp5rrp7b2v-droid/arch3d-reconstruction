# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果，只保留足以追溯结论的关键事实、证据、失败原因和最终结果；完整脚本、Workflow、Commit 与历史版本由 GitHub 保存。Checkpoint 可压缩重复或过细记录，但不得丢失正式结论与关键证据。

## T-001～T-004｜P0 技术链验证｜PASS

- T-001：项目工作区建立完成；LOW。
- T-002：Local Blender 3.6.23 灰模生成、保存、独立重开、Geometry Integrity、PNG review PASS；MEDIUM。
- T-003：Local 3.6 → GitHub Actions Blender 4.5.13 → Local 3.6 roundtrip PASS / Class B；commit `e26d5d600ed693a8e86a914e24dfbe652d718ed3`。
- T-004：JSON 参数驱动同一 Blender Python 脚本；Baseline / Variant 参数响应、独立重开、Determinism PASS；commit `63a0c506f98d843376361421cf88e1e74c807dc7`。
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
- D-023 批准独立可替换 `Z-006-RC-01 = 11 × MOD-006 = 3534.3mm`；Z-006 本体保持 UNKNOWN / null / DO_NOT_LOCK。
- 21/21 tests PASS；production preflight PASS；canonical commit `fc124922d5c0c1674548f9b99968f9848ffbb332`。

## T-007｜P2.2 Structural Skeleton｜PASS / APPROVED

- Think Level: HIGH；Blender 3.6.23。
- Structural scope 6/6；217 stable machine objects（不等于历史构件数）。
- Machine geometry validation / 32 tests / naked historical constant scan / deterministic rebuild / independent reopen PASS。
- Engineering commit：`a5a4181499c0494d16fbaf59d29337fa7d688e9d`。

## T-008｜P2.3 Integrated Reconstruction Candidate｜PASS / APPROVED

- 11 families / 40 variants / 365 stable mesh instances。
- 33/33 tests、34/34 machine QC、Local3.6→Cloud4.5→Local3.6 roundtrip PASS；core semantic diff NONE。
- Engineering commit：`93aef4803d2c0d3f7e3e3d29e9ab235c2f92d8f3`；P2 CLOSED / D-028。

## T-009｜P3.0 Component Ontology & Registry Migration｜PASS / APPROVED / CLOSED

- Component Ontology、Naming/ID、Registry Schema、P2 semantic audit / migration 完成。
- Coverage：11/11 families / 40/40 variants / 365/365 instances；orphan 0/0/0。
- Engineering commit：`3db50b94cd72e79cef419054aeaa7d2b75523ba5`；D-031。

## T-010｜P3.1 Component Master Scope & Identity｜PASS / APPROVED

- Engineering commit：`774a1469416d49268997d20970c71bb9357849aa`。
- 27 records；MASTER_REQUIRED 6 / Deferred 13 / Proxy 4 / Control 3 / Envelope 1；pending 0。
- 六类 Master scope：柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿；D-033。

## T-011｜P3.1 Column Master Pilot｜PASS / APPROVED / CLOSED

- 22/22 machine checks PASS。
- deterministic regeneration / independent reopen / synthetic mutation / canonical rebuild / Registry registration PASS。
- Review 6/6 visual PASS；Product Owner APPROVED / D-035。
- Engineering commit：`4eb79f37d31202ab2088724008b5412cba4d38b0`。

## T-012｜P3.1 Dou Master Lean Batch V002｜PASS / APPROVED / CLOSED

- First Article `CMP-LUDOU-COLUMN-001` PASS；3/3 engineering PASS。
- deterministic regeneration / reopen / mutation / rebuild：3/3 PASS。
- Review：19/19 visual PASS；Product Owner APPROVED / D-037。
- Engineering commit：`d1ae53ee368729a395623a8d9a4342f7455e2e9b`。

## T-013｜P3.1 Six-Chuanfu Master Batch V002｜PASS / APPROVED / CLOSED

- `CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL + LEAN_PRODUCTION_MODE_V001`；Codex MEDIUM。
- 两件各 26/26 machine checks PASS；52 项逐资产检查 PASS。
- deterministic regeneration / independent reopen / mutation / canonical rebuild：2/2 PASS。
- historical full length = `UNKNOWN / null`；`canonical_reference_length_mm=1000` 仅为 NON-HISTORICAL / REPLACEABLE PROJECT_RULE reference specimen。
- 最终 Review：13/13 visual PASS；Product Owner APPROVED / D-039。
- Engineering commit：`f607245444927b9853e0976b891673e387a14750`；Overview correction `cbc0a5417e56b6851778c254a8c4b5a87fc413d3`。
- P3.1 Master coverage：6/6 approved。

## T-014｜P3.1 Master Library Overview V001｜PASS / CLOSED

- whole-library Overview 覆盖 6/6 approved Masters；formal variants = 0。
- canonical Masters / individual review assets / batch overviews / P2 frozen baseline / Contract V002：UNCHANGED。
- Final Overview SHA256：`4719a31c18de13b0453a64d29847381d8e45af0f145bcb37bf7fee0abf9671a7`。
- Publication merge commit：`c15064bcd7d5cf2f3e58cdbffccc256043836413`。
- ChatGPT final visual review：PASS。

## P3.1 Gate Review｜9/9 PASS / APPROVED / CLOSED / D-040

- MASTER_REQUIRED coverage：6/6 / 100%。
- Proxy 4 / Control 3 / Envelope 1 / Deferred 13 保持非历史化。
- Registry / evidence traceability / replaceability / deterministic regeneration / independent reopen / P2 frozen baseline：PASS。
- P3.2｜构件组合关系模型解锁并进入。

## T-015｜P3.2 构件组合关系基础工程实现｜PASS / APPROVED / CLOSED / D-042

- Execution Mode：`CHAT_FIRST_CODEX_EXECUTOR_MODE`；Think Level：MEDIUM。
- Engineering commit：`49b0415479d811a26d4f44588d15cd863467edf4`。
- 正式节点 6/6；基础关系 5/5；Interface foundation PASS。
- Machine validation 31/31 PASS；Negative tests 21/21 expected rejection PASS；canonical Hard Fail=0。
- P2 frozen baseline / P3.1 canonical Masters UNCHANGED；ChatGPT structural review PASS；Product Owner D-042 APPROVED / CLOSED。

## T-016｜P3.2 代表性构件组合验证｜PASS / APPROVED / CLOSED / D-045

- Authorization D-044；Execution Mode=`CHAT_FIRST_CODEX_EXECUTOR_MODE`；Think Level=MEDIUM。
- Engineering commit：`fc01ecb4f61128faa95ecf8022d2077a36977a8c`。
- Machine validation 65/65 PASS；negative tests 15/15 expected rejection PASS；canonical Hard Fail=0；五类关系代表性覆盖 5/5。
- A｜柱—柱头栌斗：显式承托/定位接口、Blender CLI generation、independent reopen、deterministic regeneration PASS；Z-006 / RC / joinery 边界保持。
- B｜六椽栿梁架层位：Control / Proxy 不历史化；canonical=`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED`；1000 mm actual/building length injection 稳定触发 `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`。
- C｜柱网重复：PM-005=3505.7 mm 驱动同一 Master runtime instances；2→3→2 mutation/rebuild/restore、independent reopen、determinism PASS。
- P2 frozen baseline / 六个 P3.1 canonical Masters UNCHANGED；P3.3 files created=0。
- ChatGPT structural review PASS；四张正式 review PNG 按 RC-015 实际逐张打开目视审核 4/4 PASS；Product Owner D-045 APPROVED / CLOSED。

## P3.2 Gate Review｜PASS / APPROVED / CLOSED / D-046

- Gate Review file：`docs/production/zhenguo_wanfo/P3_2_GATE_REVIEW_2026-09-14.md`。
- DoD：9/9 PASS；Canonical Hard Fail：0；P3.3 foundational readiness：PASS。
- Additional engineering task required before Gate decision：NO。
- Product Owner：APPROVED / D-046。
- Carry-forward：六椽栿 historical full length UNKNOWN/null 且缺少 approved building-specific length 时继续 geometry BLOCKED；Z-006 / RC、joinery、hidden connection、45° corner 保持既有 evidence boundary；Deferred / Proxy / Control / Envelope / UNKNOWN 不得静默历史化。
- P3.2 正式 CLOSED；P3 Gate Progress 3/4；P3.3 UNLOCKED / ENTERED。

## Current Execution State｜R080｜2026-09-14

- P0：CLOSED / APPROVED。
- P1：CLOSED / 4/4 PASS / CONDITIONAL GO。
- P2：CLOSED / 4/4 PASS / PRODUCT OWNER APPROVED。
- P3：ACTIVE / **3/4 PASS**。
- P3.0：PASS / APPROVED / CLOSED。
- P3.1：PASS / APPROVED / CLOSED / D-040。
- P3.2：**PASS / APPROVED / CLOSED / D-046**。
- P3.3：**ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED**。
- Current engineering blocker：NONE。
- Current task：NONE。
- Next action：定义并由 Product Owner 批准 P3.3 Definition of Done；DoD 批准前不创建 P3.3 工程 Task Contract。

## Daily Closing Project Control Consistency Audit｜2026-09-14

- Scope：project_state / acceptance_matrix / decision_log / execution_log / governance / rules_change_log / dashboard / phase_archive applicability。
- Cross-file result：R080、D-046、P3.2 CLOSED、P3.3 ENTERED、P3 Gate Progress 3/4、Current Task NONE、Next Action=P3.3 DoD definition 在 Project Control 与 Dashboard v029 中一致。
- Governance / Rules：RC-015 已双向落档；Governance 4.6 语言分层规则通过 RC-016 补齐 Rules Change Log 镜像；Governance Current P3 已更新为 P3.3 DoD 阶段。
- Dashboard：v029 / State R080，与 project_state 当前 Phase / Gate / Progress / Current Task / Next Action 一致。
- Phase archive：P3 尚未关闭，本次无需新增 P3 closure；既有已关闭 Phase 历史档案不改写。
- Known exceptions：NONE。
- **DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT = PASS**。

## CLOUD-DRILL-002｜Codex Cloud → PR Workflow Preflight｜PASS / VERIFIED｜2026-09-15

- 性质：Cloud Mode 上线前操作链路演练；不是 P3.3 工程任务，不占用 T-###，不改变 Gate / DoD / 历史证据边界。
- Source main SHA：`ebe8599094c42274826c47b4246716a0892011ea`。
- Codex Cloud：从平台提供的 repository checkout 开始；任务容器内不要求传统 `origin/main`、`gh auth` 或直接 GitHub 网络访问。
- Drill change：仅新增 `docs/drills/CODEX_CLOUD_BRANCH_PR_DRILL_2026-09-15.md`；既有文件修改=0；`docs/project_control/` 修改=0；生产文件 / P3.3 工程文件修改=0。
- GitHub PR：`#1`；head=`codex/codex-cloud-pr`；PR head SHA=`14fd97fab03345f75ac138a004273058d8efc0b8`；target=`main`。
- ChatGPT GitHub review：PASS；变更范围与内容均符合 drill contract。
- Product Owner：授权 merge。
- Merge result：PASS；merge commit=`2528221a1ad08576878fc087e5e5474631a6be75`；`main` 已包含 drill 文件。
- 验证闭环：`GitHub main → Codex Cloud checkout → isolated modification → commit → Codex UI Create PR → ChatGPT review → Product Owner merge authorization → GitHub main`。
- Operational conclusion：**Cloud Mode Git workflow = VERIFIED**。Codex Cloud 任务容器中的内部 commit SHA 与最终发布到 GitHub 的 PR head SHA 可能不同；正式事实以 GitHub PR / commit / `main` 为准。
- Project status impact：NONE；P3.3 仍为 `ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED`；Next Action 仍为定义并批准 P3.3 DoD。

## Final Pre-Cloud Snapshot｜R082｜2026-09-15

- P3：ACTIVE / 3/4 PASS；P3.0–P3.2 均已 CLOSED；当前 Gate=P3.3。
- P3.3：`ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED`。
- Current Task：NONE；Blocker：NONE；active pending-local engineering task：NONE。
- Cloud Mode RC-014：`APPROVED / READY / PREFLIGHT VERIFIED`，有效期 2026-09-16→09-20。
- CLOUD-DRILL-002：PASS / VERIFIED；PR #1 已 merge；Cloud Git workflow 可投入临时运行模式。
- Dashboard：v030 / State R082；Final Pre-Cloud Snapshot 已可视化。
- Next Action：定义并由 Product Owner 批准 P3.3 Definition of Done；批准前不得创建 P3.3 工程 T-###。
- 本地同步：Product Owner 在本地 Mac 关闭前执行一次 `git-proxy-auto pull --ff-only origin main`，使 working copy 对齐最终 GitHub canonical state。

## Daily Closing Project Control Consistency Audit｜2026-09-15

- Scope：project_state / acceptance_matrix / decision_log / execution_log / governance / rules_change_log / dashboard / phase_archive applicability / RC-014 Cloud Mode / PR #1 merge。
- Cross-file result：P3.2=`PASS / APPROVED / CLOSED / D-046`；P3.3=`ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED`；P3 Gate=3/4；Current Task=NONE；Blocker=NONE；Next Action=P3.3 DoD；Cloud workflow preflight=PASS / VERIFIED。
- Acceptance Matrix：无需改动；Gate 状态与 project_state 一致。
- Decision Log：无需新增重大产品/技术决策；D-046 仍是最新 material Gate decision。
- Governance / Rules：RC-014 / RC-015 / RC-016 状态一致；今日无新增长期治理规则。
- Dashboard：v030 / State R082，与 Final Pre-Cloud Snapshot 一致。
- Phase archive：P3 尚未关闭，本次无新增 archive action。
- Known exceptions：NONE。
- **DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT = PASS**。

## T-017｜P3.3 整殿输入基线与 Assembly Graph 基础工程｜PASS / APPROVED / CLOSED / D-050｜2026-09-16

- Authorization：D-049；Execution Mode=`CHAT_FIRST_CODEX_EXECUTOR_MODE`；Think Level=MEDIUM；Cloud Mode=`CLOUD_EXECUTABLE`；Blender requirement=NONE。
- GitHub PR：`#2`；reviewed head=`f117cb98da713e5279174248076421caa9d9e6f4`；14 changed files；2 commits；Product Owner D-050 authorized merge。
- Merge result：PASS；merge commit=`1095440af761fc95cc18d0ce01523a097fc8ce5f`。
- 正式机器输出：5/5 present and machine-readable。
- Scope accounting：11/11 families；40/40 variants；365/365 instances；unexplained omissions=0；orphan identities=0。
- Input Baseline：四类输入分类完整；P2.3 manifest 仅 accounting/comparison；`transform.location_mm` / `rotation_euler_rad` / `scale` 明确 `PROHIBITED_AS_GENERATIVE_INPUT`。
- Parameter Bindings：formal parameter → evidence/time layer → building role → graph node / relationship / rule dependency 显式可追溯。
- Assembly Graph：`BUILDING_ROOT → ORG-BUILDING → assembly organization → runtime nodes`；P3.2 validated assembly foundation traceability PASS；基础关系仍只允许 SUPPORT / CONNECT / LOCATE / REPEAT / BELONG。
- Canonical Hard Fail=0；5/5 synthetic negative fixtures expected rejection。HF-01 真实注入六椽栿 `canonical_reference_length_mm=1000` 到 actual full-length path；HF-03 真实注入 P2 location / rotation / scale 到 authoritative placement path，均稳定拒绝。
- Mechanical validation：required outputs / input baseline / parameter provenance / building organization / P3.2 traceability / prohibited-transform scan / evidence boundary / deterministic regeneration & stable serialization / protected hashes 均由 validator 实际计算并 PASS。
- T-017 unit tests：12 tests PASS；deterministic `--check` PASS；JSON parse / compileall / `git diff --check` PASS。
- Protected inputs：P2 frozen baseline、P3.0 canonical identity、P3.1 approved Masters、P3.2 foundational definitions UNCHANGED。
- Blender invocations=0；`.blend` files created=0。
- ChatGPT first structural review：HOLD / 5 corrections required；correction publication 经 Codex UI `Update Branch` 进入同一 PR #2 后，second structural review=PASS。
- Product Owner：APPROVED / CLOSED / D-050。
- Gate impact：T-017 closure **不等于 P3.3 PASS**。T-017 已建立 DoD-01～04 基础与 DoD-07/08 验证基础；DoD-05、DoD-06、DoD-08 的 building-parameter mutation execution evidence、DoD-09 final Gate Evidence Package 仍待后续任务完成。

## Current Execution State｜R091｜2026-09-16

- P3：ACTIVE / **3/4 PASS**。
- P3.0：PASS / APPROVED / CLOSED。
- P3.1：PASS / APPROVED / CLOSED / D-040。
- P3.2：PASS / APPROVED / CLOSED / D-046。
- P3.3：ACTIVE / DOD LOCKED / T-017 PASS / NEXT TASK PLANNING。
- Current task：NONE。
- Current blocker：NONE。
- Next action：设计下一项 P3.3 Task Contract，目标为确定性整殿生成及 GitHub Actions headless Blender 证据链；未经 Product Owner 明确批准不得执行。

## T-019｜P3.3 上游 Disposition 一致性修正｜PASS / APPROVED / CLOSED / D-055｜2026-09-16

- Contract：D-053；Execution Authorization：D-054；Execution Mode=`CHAT_FIRST_CODEX_EXECUTOR_MODE`；Think Level=MEDIUM；Cloud Mode=`CLOUD_EXECUTABLE`；Blender requirement=NONE。
- GitHub PR：`#4`；reviewed head=`91723a7a2b3c3ca78473bba3cb344450e43fbb3f`；6 changed files；Product Owner D-055 authorized merge。
- Merge result：PASS；merge commit=`b9803fb416e375fd2f94f5d83df5fab73fe00063`。
- Known correction：7/7 `CMP-PURLIN-001` legacy instances in Scope Accounting and Assembly Graph changed from `GENERATE_FROM_FORMAL_COMPONENT` to `DEFERRED`。
- P3.1 qualification remains `DEFERRED_INSUFFICIENT_EVIDENCE`；no PURLIN Master created；no unknown purlin sections/lengths/end conditions invented。
- Direct-identity qualification uses explicit `candidate_id` / `source_registry_id`；family-only silent upgrade prohibited。
- Validator consistency error：`MASTER_SCOPE_DISPOSITION_CONFLICT`；not added to the five canonical P3.3 Hard Fails。
- Cross-layer direct-identity conflicts=0；new synthetic regression=`EXPECTED_REJECTION / MASTER_SCOPE_DISPOSITION_CONFLICT`。
- Accounting remains 11/11 families / 40/40 variants / 365/365 instances；unexplained omissions=0；orphan identities=0；P2 authoritative numeric-transform usage=0；five relation types unchanged；canonical Hard Fail=0；existing negatives=5/5 expected rejection。
- Deterministic regeneration / stable serialization PASS；P3.1 / P3.2 / T-018 PR #3 / Blender / `.blend` unchanged。
- Canonical `main` verification after merge：PASS；7/7 PURLIN building instances read as `DEFERRED`。
- Gate impact：T-019 closure resolves T-018 `UPSTREAM_PROTECTED_INPUT_CONFLICT` only；**does not make T-018 PASS and does not make P3.3 PASS**。

## Current Execution State｜R098｜2026-09-16

- P3：ACTIVE / **3/4 PASS**。
- P3.3：ACTIVE / DOD LOCKED。
- T-017：CLOSED / D-050 / canonical foundation corrected by T-019。
- T-019：PASS / APPROVED / CLOSED / D-055。
- Current task：T-018 / RESUME READY / CORRECTIONS REQUIRED / PR #3 OPEN。
- Previous upstream STOP：CLEARED。
- Remaining T-018 corrections：formal geometry must use approved formal generation where available；placement must derive from authoritative graph/parameters/rules；Actions evidence must bind PR head SHA；Blender 4.5.13 version check must accept valid `LTS` suffix while remaining version-locked。
- Previous Actions Run #35101537343 remains debugging-only / NOT formal evidence；Run A/B/C/D did not execute。
- Next action：return to the original T-018 Codex task, update from latest main, implement the four corrections, use Codex UI `Update Branch` to update the same PR #3, rerun GitHub Actions, then return evidence to ChatGPT；do not create a new T-018 PR and do not merge PR #3。

## Daily Closing Project Control Consistency Audit｜2026-09-16

- Scope：`project_state.json` / `acceptance_matrix.md` / `decision_log.md` / `execution_log.md` / `governance.md` / `rules_change_log.md` / `dashboard.html` / `phase_archive/` / P3.3 Task Contracts / PR #2/#3/#4 / RC-014 Cloud Mode / 9/16–20 Sync Ledger。
- Cross-file result：P3=`ACTIVE / 3/4`；P3.0–P3.2=`PASS / CLOSED`；P3.3=`ACTIVE / DOD LOCKED`；T-017=`CLOSED / D-050 / corrected foundation`；T-019=`PASS / APPROVED / CLOSED / D-055`；T-018=`RESUME READY / CORRECTIONS REQUIRED / PR #3 OPEN`。状态一致。
- Decision Log：D-047～D-055 全部已登记；D-055 为当前 latest material decision。
- Acceptance Matrix：已反映 T-017、T-019 与 T-018 resume/correction 状态；P3.3 未提前标记 PASS。
- Execution Log：T-017/T-019 的工程与 merge 事实已登记；T-018 首轮 Actions failure 明确为 debugging-only，不构成正式 evidence。
- Governance / Rules：RC-014 仍严格仅覆盖 2026-09-16→20；RC-017 scripted Blender pipeline ACTIVE；9/21 自动恢复正常模式，不自动延长 RC-014。
- Dashboard：v042 / State R098 与 Project State 一致；Current Task=T-018；PR #3 merge authorization=FALSE。
- PR audit：PR #2 MERGED；PR #4 MERGED；PR #3 OPEN / NOT MERGED。Open PR 内容不属于 canonical `main`。
- Evidence Boundary：7/7 PURLIN canonical dispositions=`DEFERRED`；PURLIN qualification=`DEFERRED_INSUFFICIENT_EVIDENCE`；六椽栿 historical full length 继续 UNKNOWN/null；1000mm reference 继续 non-historical only；P2 whole-building transforms/.blend 禁止作为 P3.3 generative input。
- Phase archive：仅 P0/P1/P2 closure；P3 尚未关闭，因此无需且不得创建 P3 closure archive。
- 9/21 防遗漏登记：已新增 `docs/project_control/CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md`，记录 9/16 Day-1 云端变化、9/17～20 每日追加模板，以及 9/21 `main + open PR + Actions artifact + local-only assets + Project Control` 五类同步核验清单。
- Known exceptions：T-018 PR #3 尚未 merge 且四项修正未完成；这是明确的 active work，不是 Project Control inconsistency。9/21 前如继续云端工作，必须每日更新 Sync Ledger。
- **DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT = PASS**。
