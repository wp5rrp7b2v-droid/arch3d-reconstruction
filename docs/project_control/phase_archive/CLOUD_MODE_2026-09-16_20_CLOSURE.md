# Cloud Mode Closure Archive｜2026-09-16 → 2026-09-20

- Project: ARCH3D-001｜中国古建筑3D复原
- Archive status: CLOSED / HISTORICAL
- Source window: RC-014 temporary Cloud Mode
- Current authority: this file is historical only; current state remains `project_state.json`.
- Consolidation method: original source text preserved verbatim below; no semantic rewrite.
- Source files retired after consolidation:
  - `docs/project_control/CLOUD_MODE_2026-09-16_20.md`
  - `docs/project_control/CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md`
  - `docs/project_control/LOCAL_SYNC_PREP_2026-09-20.md`



---

# SOURCE SNAPSHOT｜docs/project_control/CLOUD_MODE_2026-09-16_20.md

# CLOUD MODE｜2026-09-16 → 2026-09-20

**Project:** 中国古建筑3D复原（ARCH3D-001）  
**Rule ID:** RC-014  
**Status:** APPROVED / STRICTLY TEMPORARY / AUTO-EXPIRES AFTER 2026-09-20 / PREFLIGHT VERIFIED / READY  
**Effective dates:** 2026-09-16 through 2026-09-20（含首尾两日）  
**Scope:** 仅《中国古建筑3D复原》项目，不适用于《诡舍·黑衣夫人》或其他项目。  
**Entry baseline snapshot:** Project State R082 / 2026-09-15 FINAL PRE-CLOUD SNAPSHOT  
**Current-state authority:** 本文件中的 R082 / “DoD required” 内容仅描述进入 Cloud Mode 时的起始快照，不是 2026-09-19 当前项目状态。Cloud Mode 期间的当前事实以 `project_state.json` + `CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md` 为准。当前已到 P3.3 V002 / D-066 / R127，T-018 HOLD。

## 0. 当前项目进入 Cloud Mode 前基线

截至 Project State `R082`：

- P3 总体进度：`3/4`；
- P3.0：PASS / CLOSED；
- P3.1：PASS / APPROVED / CLOSED；
- P3.2：`PASS / APPROVED / CLOSED / D-046`，Gate Review `9/9 PASS`；
- T-015：PASS / APPROVED / CLOSED；
- T-016：PASS / APPROVED / CLOSED，65/65 machine validation PASS，15/15 negative tests expected rejection PASS，4/4 review assets visual PASS；
- 当前 Gate：`P3.3｜构件驱动整殿重建`；
- P3.3 状态：`ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED`；
- Current Task：`NONE`；
- Blocker：`NONE`；
- Cloud workflow preflight：`PASS / VERIFIED`；
- Pending local engineering task：`NONE`；
- 当前唯一正式 Next Action：**先定义并由 Product Owner 批准 P3.3 Definition of Done，再创建任何 P3.3 工程 Task Contract。**

因此，Cloud Mode 的首要目标不再是继续 P3.2，而是**在不降低验收标准的前提下启动 P3.3 的定义、任务拆分与可云端执行部分**。

**2026-09-15 Final Pre-Cloud Snapshot 已完成并锁定。** 2026-09-16 开工时必须重新从 GitHub `main` 读取 Project Control，再开始任何工作。

## 1. 目的

在 Product Owner 于 2026-09-16 至 2026-09-20 暂时无法使用本地 MacBook 的期间，允许项目继续推进可由 ChatGPT App、Codex Cloud 与 GitHub 完成的工作，同时保护既有本地 Blender、二进制资产与验收基线，避免因执行环境变化造成伪验收、状态漂移或返工。

本规则是**仅覆盖 2026-09-16 至 2026-09-20 的临时运行环境覆盖层**，不修改 P3 的技术目标、DoD、Hard Fail、Evidence Boundary、Gate 审批权或既有 Governance，也不改变 2026-09-21 之后的默认项目运行模式。

## 2. 工具职责

### ChatGPT App

负责：

- 每次开工先读取 GitHub `main` 上最新 Project Control、相关 Task Contract、提交与 PR；
- P3.3 DoD、任务拆分、证据边界、Hard Fail 与执行路径设计；
- 判断某项 P3.3 工作属于 `CLOUD_EXECUTABLE`、`DESIGN_ONLY` 或 `LOCAL_MAC_REQUIRED`；
- Codex Cloud 结果审核；
- Gate / Task 状态判断；
- 根据 RC-015 直接调阅 GitHub 已提交的正式审核图，并在实际逐张目视后执行视觉审核；
- 经 Product Owner 授权后直接维护 GitHub Project Control。

### Codex Cloud

负责：

- 仅基于 GitHub 已存在且可访问的仓库内容执行工程任务；
- 代码、JSON、Registry、Schema、验证器、自动测试、文档、参数映射、关系实例与其他确定性仓库内工作；
- 按 Task Contract 自测并返回 diff / commit / PR 与验证结果；
- 遇到合同外证据冲突、资产缺失、执行环境能力不足或需要本地 Mac/Blender 的工作时 STOP 并报告，不得自行降低标准；
- 未经独立批准，不得把 Codex Cloud 中可能存在的 Blender 或替代运行环境视为本项目正式 Blender 生产基线。

### GitHub Web / App

作为：

- canonical committed state；
- 唯一跨设备事实源；
- branch / PR / commit / review / rollback 层；
- Project Control 与 Cloud 产物的正式版本记录；
- 已提交 review image 的正式视觉审核来源之一，按 RC-015 执行。

### Local Mac

在 RC-014 有效期内视为：

`TEMPORARILY UNAVAILABLE`

不得假定可访问本地 working copy、`.blend`、本地 Blender executable、未提交图片/音频/视频或其他 local-only 资产。

## 3. Cloud Mode 开工规则

每次新工作会话必须：

1. 从 GitHub `main` 读取最新 `docs/project_control/`；
2. 核对最新 Phase / Gate / Current Task / blocker / next_action；
3. 核对相关 PR、branch 与最新提交；
4. 若 P3.3 DoD 尚未批准，禁止创建或执行 P3.3 工程 T-###；
5. 不以聊天记忆替代 GitHub 当前事实；
6. GitHub 与聊天历史不一致时，以 GitHub canonical committed state 为准。

## 4. P3.3 在 Cloud Mode 中的推进顺序

### Step 1｜先完成 P3.3 DoD

当前第一优先级：

`P3.3 Definition of Done → Product Owner Approval`

这是 ChatGPT / Product Owner 的 Gate 设计工作，不占 T-###，可完全在无本地 Mac 环境下完成。

P3.3 DoD 必须明确区分：

- 建筑级关系与参数传递；
- 构件驱动整殿生成的确定性要求；
- P3.2 schema / validator 的继承边界；
- 历史证据与工程补全的分层；
- Blender / binary / render / visual review 所需证据；
- 哪些验收项可以 Cloud 完成，哪些必须本地 Mac 完成。

### Step 2｜DoD 批准后先做执行能力分类

任何 P3.3 Task Contract 建立前，先给任务标记：

- `CLOUD_EXECUTABLE`：GitHub + Codex Cloud 可完整执行和验证；
- `DESIGN_ONLY`：可在 Cloud 完成设计/脚本/输入准备，但正式执行或某项验收依赖本地环境；
- `LOCAL_MAC_REQUIRED`：核心执行或验证必须使用现有本地 Blender / local-only binary。

不得为了保持项目“持续推进”而把第三类任务强行改写为 Cloud 任务。

### Step 3｜优先执行 Cloud-native 的 P3.3 基础工程

在 DoD 批准并正式授权后，Cloud Mode 优先推进：

- 建筑级 Schema / Registry；
- 构件实例与组合关系映射；
- 参数传递规则；
- building-level validator / negative tests；
- P3.2 validators 的继承与扩展；
- deterministic input manifest；
- evidence / uncertainty mapping；
- reconstruction plan / build manifest；
- 不依赖 local-only `.blend` 的生成脚本与测试；
- GitHub 中可完整复现、审查和验证的其他工程工作。

### Step 4｜本地 Blender 相关工作按真实能力延期

若正式整殿生成、independent reopen、mutation、canonical rebuild、render 或 binary-level 验证必须依赖当前本地 Blender 3.6.23 / Intel x64，则状态只能到：

`DESIGN COMPLETE / LOCAL EXECUTION OR REVIEW PENDING`

或：

`DEFERRED / LOCAL_MAC_REQUIRED`

不得标记 PASS。

## 5. 任务分类通用规则

### A｜CLOUD_EXECUTABLE

允许正式执行并按既有标准验收：

- Markdown / Project Control / Task Contract；
- JSON / Schema / Registry；
- Python / JavaScript 等仓库内脚本；
- validator / automated tests / static checks；
- 证据映射、关系定义、参数规则、数据转换；
- 不依赖 local-only binary 的工程分析与文档；
- GitHub 内可完整复现、验证和审查的其他工作。

### B｜DESIGN_ONLY

包括：

- 依赖本地 Blender 的几何生成方案；
- 需要本地正式 `.blend` 的实现设计；
- 可以完成 Task Contract / 参数 / 算法 / generator 设计，但缺少正式执行环境的工作。

状态：

`DESIGN COMPLETE / LOCAL EXECUTION OR REVIEW PENDING`

### C｜LOCAL_MAC_REQUIRED

包括：

- 访问 local-only `.blend`；
- 调用 `/Applications/Blender.app/...` 本地 Blender；
- 本地 CLI / GUI Blender 正式生产；
- 当前 DoD 明确要求且只能由本地环境完成的 independent reopen / render / mutation / binary 验证；
- 访问未进入 GitHub 的二进制资产。

状态：

`DEFERRED / LOCAL_MAC_REQUIRED`

该状态属于 **temporary execution constraint**，默认不登记为项目技术 blocker，除非它实际阻止当前 Gate 继续产生任何有价值进展。

## 6. Cloud 工程分支规则

RC-014 有效期内默认采用：

`ONE TASK = ONE BRANCH = ONE PR`

规则：

1. Codex Cloud 从当时最新 `main` 开始；
2. 每个独立 T-### 使用独立 branch / PR，除非任务本身只是 Project Control 的轻量直接维护；
3. PR 必须包含任务范围、验证结果和已知限制；
4. ChatGPT 完成工程/结构审核后，Product Owner 仍保留正式 Gate Approval；
5. 未通过审核的 Cloud 产物不得通过“看起来完成”直接升级为 PASS；
6. 不在多个 Cloud branch 中并行修改同一 Project Control 文件；
7. merge 后再把下一 Current Task 建立在最新 `main` 上。

**本节仅属于 RC-014 的临时执行规则。2026-09-21 起不再因 RC-014 强制要求 `ONE TASK = ONE BRANCH = ONE PR`；之后按届时正常 Governance 与正式 Task Contract 执行。**

### 6.1｜2026-09-15 Workflow Preflight 解释

- `CLOUD-DRILL-002` 已验证：Codex Cloud 可从平台提供的 repository checkout 完成隔离修改，并通过 Codex UI 将结果发布为 GitHub PR。
- Codex 任务容器本身**不要求**暴露传统 `origin/main`、`gh auth` 或直接 GitHub 网络访问；不得因容器内缺少这些本地式 Git 条件而误判 Cloud checkout 无效。
- 正式 source baseline 必须由任务启动时的 checkout SHA 记录，并由 ChatGPT 在 GitHub 侧独立核对其与 canonical `main` 的关系。
- Codex 内部任务 commit SHA 与最终发布到 GitHub 的 PR head SHA 可能不同；**正式事实以 GitHub PR、GitHub commit 与 `main` 为准**。
- PR 创建后由 ChatGPT 审核实际 GitHub diff / commit / base / head；Product Owner 保留 merge 授权权。

## 7. Blender 与视觉验收边界

- 当前本地 Blender 3.6.23 / Intel x64 基线继续有效；
- Cloud Mode 不自动假定 Codex Cloud 具备等价 Blender 环境；
- 未经独立 Task Contract 验证与 Product Owner 批准，不把 Cloud Blender 或替代 renderer 视为正式生产节点；
- 需要本地 Blender executable、local-only `.blend`、binary-level reopen 或本地运行环境的 DoD 项不得在 Cloud Mode 中虚假勾选 PASS；
- **视觉审核不再一律等同于 local-Mac-required**：若正式 review images 已提交到 GitHub 且可由 ChatGPT 实际调阅和逐张目视，则按 RC-015 可直接完成视觉审核；
- 只有 review asset 仍为 local-only、GitHub 无法读取，或验收要求交互式 Blender / binary inspection 时，才必须延期到本地 Mac。

## 8. P3.2 向 P3.3 的继承边界

P3.2 已正式关闭，但以下约束必须完整带入 P3.3：

- 保留 P3.1 evidence / component identity boundary；
- `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` 继续为 Hard Fail；
- 六椽栿 `canonical_reference_length_mm=1000` 不得作为建筑实际长度进入整殿重建；
- Proxy / Control / Envelope / Deferred / UNKNOWN 不得静默历史化；
- 六椽栿完整建筑长度在获得单独批准的 building-specific 证据前继续保持 `FULL_LENGTH_GEOMETRY_BLOCKED`；
- P3.3 可以在批准的 P3.2 schema 内扩展 building-level interfaces 与 relationship instances，但不得重新定义五类基础关系，也不得绕过 P3.2 validators。

Cloud Mode 只改变执行环境，不改变上述任何证据或工程边界。

## 9. Project Control 规则

RC-014 有效期内继续遵守：

- `GitHub main = canonical committed state`；
- `Project Control = SSOT`；
- Dashboard 仍为派生可视化，不提升为事实源；
- 重大决策、Task 状态、Gate 状态、Governance 变化即时落档；
- 每日正式收尾继续执行 `DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT`；
- RC-015 Direct GitHub Visual Review 继续有效；
- 不因为无法访问本地 Mac 而修改历史验收结论或降低 DoD。

其中属于 RC-005、RC-013、RC-015 等独立长期规则的内容，在 RC-014 到期后仍按各自状态继续有效；只有 RC-014 自己新增的 Cloud-only 覆盖规则到期失效。

## 10. 返回正常模式后的恢复流程

2026-09-21 起 RC-014 自动失效。下一次恢复本地 Mac 工作时必须：

1. `git-proxy-auto pull --ff-only origin main`；
2. 核对 RC-014 有效期内所有已 merge PR / commit；
3. 核对 Project Control 与本地 working copy 一致；
4. 汇总所有 `LOCAL EXECUTION OR REVIEW PENDING` 与 `DEFERRED / LOCAL_MAC_REQUIRED` 项；
5. 按 P3.3 DoD 优先级补做本地 Blender / binary / local-only validation；
6. 不重新执行已经在 Cloud 中具备完整证据并正式 PASS 的纯仓库任务；
7. 完成一次 Project Control consistency audit 后继续按原有正常 Local + Cloud 工作模式推进。

RC-014 的结束只恢复执行模式，不回滚 2026-09-16 至 2026-09-20 已正式批准、已合并并具有完整证据的项目成果。

## 11. 生效、自动失效与禁止自动延长

- 本规则于 2026-09-14 经 Product Owner 明确批准建立；
- 同日依据 P3.2 CLOSED / P3.3 ENTERED 的最新 `R080` 项目状态完成阶段适配更新；
- 2026-09-15 完成 `CLOUD-DRILL-002`，Cloud Git workflow preflight=`PASS / VERIFIED`；
- 2026-09-15 完成 Final Pre-Cloud Snapshot=`R082 / READY` 与 Daily Closing Audit=`PASS`；
- **RC-014 只在 2026-09-16、17、18、19、20 五个自然日有效；**
- **2026-09-20 当日结束后自动失效；自 2026-09-21 起自动恢复 RC-014 生效前的正常项目治理与执行模式，无需 Product Owner 再次批准“恢复”；**
- **RC-014 不自动延长。即使 2026-09-20 后出现新的无 Mac 情况，也必须由 Product Owner 另行明确批准新的临时安排或延长，不得默认继续套用 RC-014；**
- Product Owner 可在 2026-09-20 前明确提前终止 RC-014；
- RC-014 结束后仅作为历史记录保留，不升级为长期默认 Governance；
- RC-014 到期不影响 RC-005、RC-013、RC-015 等本来就独立有效的长期规则。

## 12. CLOUD-DRILL-002｜Preflight Evidence

- Drill date：2026-09-15。
- Source `main` SHA：`ebe8599094c42274826c47b4246716a0892011ea`。
- Scope：仅新增 `docs/drills/CODEX_CLOUD_BRANCH_PR_DRILL_2026-09-15.md`；生产影响=`NONE`。
- GitHub PR：`#1`；head branch=`codex/codex-cloud-pr`；PR head SHA=`14fd97fab03345f75ac138a004273058d8efc0b8`。
- Review：ChatGPT GitHub-side diff / commit / base / head review=`PASS`。
- Merge：Product Owner 授权；merge commit=`2528221a1ad08576878fc087e5e5474631a6be75`。
- Result：**Cloud Mode Git workflow = VERIFIED**。
- 本演练不属于 P3.3 工程任务，不占 T-###，不改变 P3.3 `ENGINEERING NOT AUTHORIZED` 状态。

## 13. Final Pre-Cloud Snapshot｜2026-09-15

- Project State：`R082`。
- Dashboard：`v030 / State R082`。
- P3.3：`ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED`。
- Current Task：`NONE`。
- Blocker：`NONE`。
- Pending local engineering task：`NONE`。
- Daily Closing Project Control Consistency Audit：`PASS / known exceptions NONE`。
- 2026-09-16 开工第一动作：从 GitHub `main` 重新读取 Project Control；随后定义并由 Product Owner 批准 P3.3 DoD。


---

# SOURCE SNAPSHOT｜docs/project_control/CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md

# Cloud Mode Sync Ledger｜2026-09-16 → 2026-09-20

**Project:** ARCH3D-001｜中国古建筑3D复原  
**性质:** 临时云端变更登记 / 2026-09-20 晚间本地同步防遗漏清单  
**适用期:** 2026-09-16 ～ 2026-09-20（含）  
**目标同步日:** 2026-09-20 晚间（Product Owner 当前计划）  
**状态:** CLOUD PRODUCTION WINDOW COMPLETE / LOCAL_SYNC_VERIFICATION_PENDING  
**关联规则:** RC-014｜CLOUD_MODE_2026-09-16_20  
**事实优先级:** 如与 `project_state.json`、Decision Log、Execution Log、Acceptance Matrix 或 GitHub `main` 冲突，以正式 Project Control + GitHub `main` 为准。

---

## 1. Cloud Mode 进入基线

- Pre-Cloud Project State：`R082 / 2026-09-15 FINAL PRE-CLOUD SNAPSHOT`
- P3：ACTIVE / 3 of 4
- P3.0～P3.2：PASS / CLOSED
- P3.3：ENTERED
- Cloud workflow preflight：`CLOUD-DRILL-002 PASS / VERIFIED`
- RC-014：2026-09-16～20 临时云端生产窗口已完成；当前只保留本地同步核验义务
- Local Mac：Cloud Mode 有效期内视为 TEMPORARILY UNAVAILABLE

---

## 2. 2026-09-16｜Day 1 Closing Register

- D-047：P3.3 DoD V001 APPROVED / LOCKED。
- D-048 / RC-017：GitHub Actions headless Blender pipeline APPROVED。
- T-017 / PR #2：PASS / D-050 / MERGED；11/11 families、40/40 variants、365/365 instances。
- T-018 / PR #3：OPEN / NOT MERGED；D-051 contract locked；D-052 execution authorized；9/16 close status = RESUME READY / CORRECTIONS REQUIRED。
- T-019 / PR #4：PASS / D-055 / MERGED；7/7 PURLIN corrected to DEFERRED；merge commit `b9803fb416e375fd2f94f5d83df5fab73fe00063`。
- Latest formal decision：D-055。
- Local sync：PENDING；当前计划于 2026-09-20 晚间执行。

---

## 3. 2026-09-17｜Day 2 Closing Register

- Start canonical main SHA：`574a00831ac827d67dd58667f80fb57d1dd0c77e`
- Project State at close：`R100`
- Dashboard at close：`v044`
- New formal Decision ID：NONE；latest remains `D-055`
- Detailed daily archive：`docs/project_control/DAILY_CLOSE_2026-09-17.md`

### 3.1 T-018 status change

T-018 continued on the **same** branch / PR only:

- branch：`codex/t-018`
- PR：`#3`
- PR status：`OPEN / NOT MERGED`
- GitHub-visible head：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Merge authorization：FALSE

Round 2 result：

- 365/365 `RULE_DERIVED`
- `NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE=0`
- 12 Formal / 178 Proxy / 66 Control / 6 Envelope / 96 UNKNOWN_BLOCKED / 7 DEFERRED
- omission=0；anonymous formal mesh=0；broken identity=0
- PM-005 mutation / restore machine PASS
- visual review FAIL：non-formal representation largely generic point/octahedron markers

Round 3 result：

- differentiated engineering representation geometry by family
- generic octahedron-for-all-nonformal = 0
- view-aware projected-in-frame evidence added
- machine / representation validation PASS

### 3.2 Final Actions evidence

- Workflow：`T-018 P3.3 Deterministic Whole Building`
- Run ID：`35226626839`
- Run number：29
- Head SHA：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Conclusion：SUCCESS
- Run A / B / Render / C / D：PASS
- Artifact ID：`10499236860`
- Artifact：`P3_3_T018_HEADLESS_EVIDENCE_V001`
- Digest：`sha256:1acb510ed409e490319d62dad2232d082f163413ab81a209484f00b8b67329fa`
- Artifact expiry：2026-10-17

### 3.3 Formal visual review / roof audit

Four review PNGs (PLAN / FRONT / SIDE / AXON) were directly inspected by ChatGPT。

Final status：

`T-018 = HOLD / MACHINE PASS / FORMAL VISUAL REVIEW FAIL / UPSTREAM RULE GAP`

Root cause found by read-only audit：

- canonical PURLIN control identity topology = `N00,N01,N02,N03(shared ridge),S00,S01,S02`; no S03
- FR-007 = `[120,115,210] fen` in eave→ridge order
- MOD-002 = 15.3 mm/fen; half-run = 6808.5 mm
- existing inputs authorize the **relative** two-sided chain to one shared ridge
- existing inputs do **not** authorize the absolute shared-ridge coordinate in the T-018 whole-building coordinate frame
- Round 2/3 mixed observed/as-measured grid coordinates with reconstructed-963 roof-control sequence
- Round 3 `COLUMN_GRID_Y_MIRROR_RULE` is synthetic / unauthorized
- previous Round 2 roof-placement freeze assumption is withdrawn

At minimum, after an approved upstream datum rule exists, rederive 7 PURLIN controls, 36 RAFTER proxies, 6 ROOF_ENVELOPE, 4 GABLE_CONTROL and roof-dependent FRAME endpoints。

Root-cause classification：

`UPSTREAM ENGINEERING RULE MODELING OMISSION + T018 FAILURE TO STOP`

This is not a newly discovered historical-evidence gap。

### 3.4 Proposed T-020

`T-020｜P3.3_ROOF_SHARED_RIDGE_DATUM_RULE_V001｜屋顶共享脊基准与设计坐标层对齐规则`

Status：`PROPOSED / NOT AUTHORIZED / NO BRANCH / NO PR`

Purpose：补齐 project-level engineering datum / LOCATE semantics，不新增历史尺寸；保持 7/7 PURLIN DEFERRED；禁止 observed reference layer 静默成为 reconstructed-design placement source；P2 numeric world transforms 继续禁止。

### 3.5 Files / assets requiring 2026-09-21 awareness

Main-tracked Project Control additions/updates today：

- `docs/project_control/DAILY_CLOSE_2026-09-17.md`
- `docs/project_control/project_state.json` → R100
- `docs/project_control/dashboard.html` → v044
- `docs/project_control/acceptance_matrix.md`
- `docs/project_control/execution_log.md`
- `docs/project_control/CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md`

Open PR not in main：

- PR #3 / `codex/t-018` / head `8693c13...`

Actions artifact not brought by `git pull`：

- Artifact `10499236860` / T-018 headless evidence

LOCAL_MAC_REQUIRED / local-only follow-up：

- 2026-09-21 must verify local-only `.blend` assets separately
- do not mistake absent PR #3 content in local `main` for sync failure

Daily closing audit：`PASS`

---

## 4. 2026-09-18～20｜Daily templates

### 2026-09-18

- Start main SHA：`c1d68627cd8b34be889a3cfc10acd0a1fed6a824`
- Detailed daily archive：`docs/project_control/DAILY_CLOSE_2026-09-18.md`
- Latest formal Product Owner decision：D-064
- New execution/publication authorization at close：NONE
- T-020：PASS / CLOSED / D-058 / PR #5 MERGED
- T-018 V002 Rebaseline：D-059 LOCKED
- Stage A：initial CP-01/02 PASS classifications retained；authority coverage reopened after CP-03
- Stage B：D-061 had authorized CP-03/04/05, but CP-03 STOPPED on `FRAME_TIER_VERTICAL_AUTHORITY_GAP`; CP-04/05 NOT STARTED
- Architecture Closure Review：Outcome B / current working classification only
- Bounded completion design：D-062 / four closure specs complete
- RZ：D-063 design contract LOCKED / not published / not implemented
- FV semantic validity：source-derived claim rejected
- FV：D-064 / A = FV_PROJECT_RULE / non-historical project reconstruction convention / design contract LOCKED / not published / not implemented
- Project State final post-audit revision：R121
- Dashboard final post-audit version：v062
- T-018 final status：HOLD / NOT PASS / production direction not yet proven
- P3.3 final status：ACTIVE / NOT PASS
- CP-03：STOP / not resumed
- CP-04/05：NOT STARTED
- Stage C：LOCKED
- Blender/Actions after V002 architecture review：NONE
- New Actions artifact after V002 review：NONE
- PR #3：OPEN / SUPERSEDED / READ-ONLY / head `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750` / mergeable=false at close / DO NOT MERGE
- PR #6：OPEN / HOLD / head `65a63b011794dfe2af6a1f0be5ba497a52f23d5f` / mergeable=false at close / DO NOT PATCH / DO NOT MERGE
- Historical PR #6 Actions Run #30：FAIL / `ModuleNotFoundError: p3_3_whole_building_common_v001`
- No new local-only binary produced today
- LOCAL_MAC_REQUIRED follow-up：2026-09-21 still must verify local-only .blend/.blend1 and reconcile main + open PRs + Actions artifacts
- Daily closing audit：**PASS WITH CAUTION**
- Carry-forward rule：**do not interpret RZ/FV locks as proof the correct production direction has been established**
- Next session must first run a bounded **Pre-Publication Readiness Review** before any new publication/execution authorization.

### 2026-09-19

- Start main SHA：TBD
- End main SHA：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- Actions / artifact：TBD
- Open PRs not in main：TBD
- LOCAL_MAC_REQUIRED follow-up：TBD
- Daily closing audit：TBD

### 2026-09-20

- Start main SHA：TBD
- End-of-Cloud-Mode main SHA：TBD
- Final State Revision：TBD
- Final Dashboard Version：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- Open PRs carried into 9/21：TBD
- Actions artifacts requiring separate download：TBD
- RC-014 closure readiness：TBD
- Daily closing audit：TBD

---

## 5. 2026-09-21｜Local Mac Sync Checklist

### A. Protect local work first

1. `cd "/Users/caroline/中国古建筑3D复原"`
2. `git status --short`
3. Any unexplained tracked changes / local Project Control edits → **STOP**; do not reset / force / overwrite.
4. Confirm local-only `.blend` / `.blend1` / binary assets separately.

### B. Sync canonical main

```bash
git-proxy-auto fetch origin
git-proxy-auto pull --ff-only origin main
git rev-parse HEAD
git-proxy-auto ls-remote origin refs/heads/main
```

Requirements：fast-forward only；local HEAD == origin/main；otherwise STOP and diagnose。

### C. Verify Project Control

- `project_state.json` latest revision
- `dashboard.html` latest visualization version
- `decision_log.md` latest formal decisions
- `execution_log.md` includes Cloud Mode engineering results
- `acceptance_matrix.md` matches P3.3 state
- `CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md` present
- `DAILY_CLOSE_2026-09-17.md` present
- RC-014 expires on 2026-09-21; RC-017 remains valid unless formally changed

### D. Verify P3.3 separately

`git pull main` does **not** bring back：

- unmerged PR #3 branch content
- Actions artifact ZIP / `.blend`
- Codex internal commits
- local-only binary assets

Therefore separately check：

1. PR #3 current status / head
2. latest T-018 Actions run
3. artifact `10499236860` or any newer replacement
4. any LOCAL_MAC_REQUIRED final inspection
5. proposed/approved T-020 status if work continued after 9/17

### E. Local Sync Closure Record

- GitHub main SHA at sync：TBD
- Local HEAD after pull：TBD
- HEAD == origin/main：TBD
- Project State revision：TBD
- Dashboard version：TBD
- Open PRs carried forward：TBD
- Actions artifacts downloaded separately：TBD
- Local-only binaries present：TBD
- RC-014 expired：TBD
- Remaining work：TBD
- Final result：`LOCAL_SYNC_VERIFIED / CLOSED` or `HOLD + reason`

---

## 6. Mandatory anti-omission rules

- GitHub `main` = Cloud Mode canonical committed state。
- PR OPEN ≠ main contains it。
- Actions artifact ≠ git-tracked file。
- Codex internal SHA ≠ canonical GitHub SHA。
- Local-only binary ≠ GitHub asset。
- 2026-09-21 sync must check `main + open PR + Actions artifacts + local-only assets + Project Control` together。

- 2026-09-18：T-018 V002 Rebaseline contract approved/locked under D-059；execution not authorized；PR #3 superseded/read-only；PR #6 HOLD。


## Day 4｜2026-09-19｜IN PROGRESS

- Project State：R122
- Dashboard：v063
- T-018：HOLD / no engineering execution authorized
- New canonical evidence：
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_WHOLE_BUILDING_COMPONENT_INSTANCE_INVENTORY_V001.md`
- Main finding：existing 11/40/365 engineering baseline is retained but no longer treated as proof of whole-building real-component completeness.
- Important correction：Purlins currently confirmed as 33 total = 21 main-body + 12 gable-side.
- No new Blender run.
- No new Actions rerun.
- No PR merge authorization.
- Local Mac sync target remains 2026-09-21.


### V007 final component baseline sync

- Date：2026-09-19
- Start main SHA：`26038fa130121e6a4dcc79a71f5dc41269646767`
- Project State：R123
- Dashboard：v064
- New canonical evidence：
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_WHOLE_BUILDING_COMPONENT_INSTANCE_INVENTORY_V007.md`
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INVENTORY_V007_BUILD_BASELINE.json`
- V007：CURRENT BUILD BASELINE / FINAL HIGH-RISK AUDIT COMPLETE / AUDIT STOP RULE ACTIVE
- T-018：HOLD / no engineering execution authorized
- P3.3：ACTIVE / NOT PASS
- RZ/FV：design locks only / not published
- CP-03：STOP
- Blender/Actions：none
- PR merge authorization：none
- Local Mac 2026-09-21 sync checklist remains required.
- Day 4 status：IN PROGRESS; component-audit stream closed at V007.


### V007 detailed instance registry sync

- Date：2026-09-19
- Project State：R124
- Dashboard：v065
- Added detailed machine-readable instance registry：
  - `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`
- Purpose：preserve V007 per-instance / per-position baseline in GitHub so future sessions do not depend on the chat-generated spreadsheet binary.
- The `.xlsx` workbook remains a review artifact; GitHub canonical truth is the V007 Markdown + baseline JSON + detailed instance registry JSON + Project Control.
- T-018 remains HOLD; no engineering execution authorization.


### RC-018 Component Registry → Excel sync

- Date：2026-09-19
- Decision：D-065
- Rule：RC-018 ACTIVE
- Project State：R126
- Dashboard：v067
- Canonical source：`P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- Versioned snapshot：V007
- Registry records：472
- Auto-generator + GitHub Actions workflow：established
- Final workflow run：`35429316513` = SUCCESS
- Derived commit：`408be1829fd1b190e69eaf0e7543f4dd7f0b7f85`
- CURRENT.xlsx + V007.xlsx：generated and committed
- Excel SHA-256：`b9cd37fb940f7d91e14b11a8aeaadafbac3c6e15a6ef07ae968b6b7afa1f017d`
- Sync Manifest：SYNCED
- Governance：JSON canonical / Excel derived / no dual maintenance / fail closed
- T-018：remains HOLD / no engineering execution authorization


### P3.3 V002 real-component-driven route lock

- Date：2026-09-19
- Decision：D-066
- Project State：R127
- Dashboard：v068
- Current P3.3 plan：`docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V002.md`
- P3.3 progress：0/7 new implementation stages formally passed
- Stage 1：real Component Master library / NOT YET AUTHORIZED
- V007：current real-component fact baseline
- RC-018：JSON canonical / Excel derived / ACTIVE
- Legacy 11/40/365 + T-017 accounting：historical engineering baseline / comparison only
- T-020 / RZ / FV：retained / Stage-5 re-review
- T-018 V002：HOLD / not current execution route
- New engineering execution authorization：NONE


### P3.3 V002 Stage 1 entry

- Date：2026-09-19
- Decision：D-067
- Project State：R128
- Dashboard：v069
- Stage 1：ACTIVE
- First work：six existing approved Masters rebind/coverage review against V007
- New T-###：NONE
- T-018：HOLD
- RZ/FV/CP-03：not authorized


### P3.3 Stage 1 six-Master rebind review

- Date：2026-09-19
- Project State：R129
- Dashboard：v070
- Review status：COMPLETE
- Existing Masters reviewed：6
- Retained：6
- Immediate rebuild required：0
- Direct rebind：柱 / 柱头栌斗
- Rebind with Stage2 length bridge：下六椽栿 / 上六椽栿
- Retain unbound：单向长开斗 / 交互斗
- New T-###：NONE
- T-018：HOLD
- Next：full V007 Master Coverage / Disposition Matrix


### P3.3 Stage 1 coverage matrix / V008 proposal

- Date：2026-09-19
- Project State：R130
- Dashboard：v071
- Current V007 registry：472 records / 49 registered object types
- Coverage matrix：COMPLETE
- V008 targeted patch：DESIGN COMPLETE / APPROVAL REQUIRED
- Proposed append：33 records
- Expected V008：505 registry records
- Pending source binding：板瓦 / 勾头 / 滴水 / 博风板 / 悬鱼 / 惹草 / 生头木
- New T-###：NONE
- T-018：HOLD


### P3.3 Stage 1 V008 patch complete

- Date：2026-09-19
- Decision：D-068
- Project State：R131
- Dashboard：v072
- Registry：V008 / 505 records
- V007 preserved：472/472
- Added：33
- RC-018 run：35431569023 = SUCCESS
- Derived commit：5c9b67217cf9bb2100993ee322419481ca446ede
- Coverage Matrix：V002 FINALIZED / 66 registered object types
- Pending source binding：板瓦 / 勾头 / 滴水 / 博风板 / 悬鱼 / 惹草 / 生头木
- Next：四椽栿 Master Spec
- New T-###：NONE
- T-018：HOLD


### P3.3 Stage 1 四椽栿 Master Spec lock

- Date：2026-09-19
- Decision：D-069
- Project State：R132
- Dashboard：v073
- Component：CMP-FRAME-FOUR-CHUANFU-001
- Master：CMP-FRAME-FOUR-CHUANFU-001_MASTER
- Spec：V001 LOCKED
- Direct source：PDF p82 / printed p67 / table 2-39
- Instances：2
- Mean section：426.5×302mm
- Raw samples：413×295 / 440×309
- Sample-to-instance mapping：UNKNOWN
- Historical full length：UNKNOWN
- Canonical reference：1000mm non-historical only
- New T-###：NONE
- Codex First Article：NOT AUTHORIZED
- T-018：HOLD


### T-021 four-chuanfu Master First Article task creation

- Date：2026-09-19
- Decision：D-070
- Project State：R133
- Dashboard：v074
- Task：T-021
- Contract：LOCKED
- Target：CMP-FRAME-FOUR-CHUANFU-001_MASTER
- Branch planned：codex/t021-p3-3-four-chuanfu-master-first-article-v001
- Execution：NOT YET AUTHORIZED
- New Codex run：NONE
- Blender run：NONE
- T-018：HOLD
- Next：Product Owner explicit “开始 T-021”


### T-021 Retry 00 STOP / infrastructure

- Date：2026-09-19
- Project State：R134
- Dashboard：v075
- Task：T-021
- Result：STOP / ENVIRONMENT-INFRASTRUCTURE
- Engineering changes：NONE
- Validation：0/42
- Blender direct download in Codex sandbox：HTTP 403
- Git remote/auth：missing
- Protected assets：PASS
- Retry：T-021 Retry 01 after GitHub-connected execution path recovery
- New task：DO NOT CREATE T-022
- T-018：HOLD


### T-021 Cloud execution interpretation correction

- Date：2026-09-19
- Project State：R136
- Dashboard：v077
- Previous remote/auth STOP interpretation：SUPERSEDED
- Shell `git remote -v` / `gh auth status`：not mandatory Codex Cloud capability gates
- Correct path：Codex Cloud engineering diff → product Create PR flow → GitHub Actions Blender 4.5.13
- Blender in Codex sandbox：PROHIBITED / NOT REQUIRED
- Valid infra STOP only if：
  - Codex Cloud product-level PR creation fails, or
  - GitHub Actions cannot obtain/run Blender 4.5.13
- Engineering changes so far：NONE
- Validation：0/42
- Task：continue T-021 / no T-022
- T-018：HOLD


### T-021 executor override

- Date：2026-09-19
- Decision：D-071
- Project State：R137
- Dashboard：v078
- Task：T-021
- Engineering executor：ChatGPT direct GitHub execution
- Blender executor：GitHub Actions / Blender 4.5.13
- Codex dependency：removed for T-021 engineering file authoring
- Spec / validation / mutation / review / binary / merge boundaries：UNCHANGED
- T-022：NONE
- T-018：HOLD


### T-021 first article approval / D-072

- Date：2026-09-19
- Project State：R138
- Dashboard：v079
- Task：T-021
- Product Owner decision：D-072 / APPROVED
- Final Actions Run：35440785415 / SUCCESS
- Reviewed head：f16ba22933bb48dbae8951343b76190d2c76c1cf
- Validation：42/42 PASS
- Review PNG：6/6 PASS
- Artifact ID：10583607231
- Artifact ZIP SHA-256：2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e
- Canonical .blend SHA-256：9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997
- Semantic geometry signature：45dce8ce4e58deabd3643c57d0f6caa7ebf50a6189e8d41cf57b68e978b63322
- Correction：prior chat wording mislabeled the semantic signature as binary SHA; artifact itself was correct; no rerun required.
- PR #7：OPEN / publication closure pending / not merged by D-072 itself
- Stage 1：ACTIVE / not yet passed
- T-018：HOLD


### T-021 PR #7 publication closure

- Date：2026-09-19
- Project State：R139
- Dashboard：v080
- PR #7：MERGED
- Merge commit：2c2c3bc3dea63d7f8449271c47e58d468489c950
- Final PR head：983d1505354e38e350b5db0038d90ddc7f41a3d5
- Final head Actions Run：35445039747 / SUCCESS
- Formal delivery records：materialized on main
- T-021：COMPLETE / PRODUCT OWNER APPROVED / PUBLICATION CLOSED
- Stage 1：ACTIVE
- T-018：HOLD


### 2026-09-19 daily close

- Project State：R140
- Dashboard：v081
- Daily close：COMPLETE / CROSS-CHECK PASS
- V008：CURRENT / 505 registry records / JSON authority
- P3.3 V002：Stage 1 ACTIVE / not passed
- T-021：APPROVED D-072 / PR #7 MERGED / publication CLOSED
- Merge commit：2c2c3bc3dea63d7f8449271c47e58d468489c950
- Final head Actions Run：35445039747 / SUCCESS
- Next session：平梁 Master direct evidence review + Spec design
- New T-###：NONE
- T-018：HOLD
- T-020 / RZ / FV：Stage 5 re-review
- Pending source binding：板瓦 / 勾头 / 滴水 / 博风板 / 悬鱼 / 惹草 / 生头木

### 2026-09-20 Day 5 / Cloud production close

- Date：2026-09-20
- Status：**COMPLETE / CLOUD PRODUCTION WINDOW CLOSED / LOCAL_SYNC_VERIFICATION PENDING**
- Project State：R159
- Dashboard：v099
- P3.3 V002：Stage 1 ACTIVE / not passed
- V008：CURRENT / 505 registry records / JSON authority
- RC-018：V008 / 505 / SYNCED / latest relevant successful Run 35495608194
- Stage1 approved Master count：10
- T-022：APPROVED D-074 / PR #9 MERGED / CLOSED
- T-023：APPROVED D-080 / PR #10 MERGED / CLOSED
- T-024：APPROVED D-085 / PR #11 MERGED / CLOSED
- Latest merge decision：D-086
- Open PRs：#3 and #6 only / both T-018 / DO NOT MERGE
- Active engineering T-task：NONE
- D-076 visual-reference gate：ACTIVE for next new Master
- T-018：HOLD
- T-020 / RZ / FV：retain current boundary / Stage5 re-review
- Daily Close：`docs/project_control/DAILY_CLOSE_2026-09-20.md`
- Local sync checklist：`docs/project_control/LOCAL_SYNC_PREP_2026-09-20.md`
- Local Mac sync：NOT YET VERIFIED
- Immediate next operation：local read-only preflight + fetch; no next Master execution before local sync verification PASS

### D-087 post-close registry visibility patch

- Date：2026-09-20
- Purpose：make V008 directly readable as a Stage1 Master progress tracker
- Project State：R161（final pre-local-sync audit）
- Dashboard：v101
- V008：505 records / 66 object types
- Master scope：28 types
- Approved：10
- Pending：18
- Completion：35.7%
- Approved Master bindings：52 registry rows
- Excel generator：1.0.2
- RC-018 Run：35508113993 / SUCCESS
- Final pre-local-sync audit：PASS / binding errors 0 / active Actions 0
- Local sync prep updated：must verify “进度总览” after sync
- New engineering task：NONE
- T-018：HOLD


## Local Mac reconciliation closure｜2026-09-20

- Cloud production window：CLOSED.
- Local Git synchronization：PASS.
- Local sync checkpoint HEAD：`995a8f42be21e9f1f8c8b013424ea56d5c1b554a`.
- V008 / Excel post-sync verification：PASS.
- Approved Actions artifact reconciliation：PASS.
- T-021 四椽栿 canonical blend：SHA_MATCH.
- T-022 平梁 EW_SEAM + GABLE canonical blends：SHA_MATCH.
- T-023 丁栿 canonical blend：SHA_MATCH.
- T-024 乳栿 canonical blend：SHA_MATCH.
- Local approved Master library：10 approved Masters / 11 `.blend` files.
- Git safety：working tree clean; `.blend` ignored.
- Local-sync gate：CLOSED.
- Current engineering T-task：NONE.
- Next：return to Stage1 next-Master selection under D-076.
- T-018：HOLD.


---

# SOURCE SNAPSHOT｜docs/project_control/LOCAL_SYNC_PREP_2026-09-20.md

# Local Sync Prep｜2026-09-20｜ARCH3D-001

Status：**PREPARED / EXECUTION PENDING LOCAL MAC**

Purpose：safely reconcile the local Mac with current GitHub `main` after the 2026-09-16—20 Cloud Mode window.

## 1. Safety rule

**Do not start with `git pull`, `git reset --hard`, file deletion, branch deletion, or checkout of old T-018 branches.**

First inspect local state.

Expected project directory:

`/Users/caroline/中国古建筑3D复原`

If this path is absent, STOP and locate the actual repository before running Git commands.

## 2. Phase A｜Read-only local preflight

Run:

```bash
cd "/Users/caroline/中国古建筑3D复原"

pwd
git status --short --branch
git branch --show-current
git rev-parse HEAD
git remote -v
git log -1 --oneline --decorate
```

Expected:
- this is a Git repository;
- remote `origin` points to `wp5rrp7b2v-droid/arch3d-reconstruction`;
- preferred current branch is `main`;
- no assumption is made about whether working tree is clean until output is checked.

If any command fails：STOP.

## 3. Phase B｜Fetch only

Run:

```bash
git fetch origin --prune

git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log --oneline --decorate --graph --max-count=20 --all
```

Do **not** merge yet.

## 4. Phase C｜Decision rule

Fast-forward is allowed only if all are true:

- current branch = `main`;
- working tree has no uncommitted changes;
- no local-only commit exists ahead of `origin/main`;
- local HEAD is an ancestor of `origin/main`.

Check:

```bash
git merge-base --is-ancestor HEAD origin/main
echo $?
```

Result `0` means local HEAD is an ancestor of origin/main.

Only then run:

```bash
git pull --ff-only origin main
```

If the result is non-zero, or `git status` is not clean, **do not reset**. Preserve local state and inspect first.

## 5. Phase D｜Post-pull verification

Run:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log -1 --oneline --decorate

test -f docs/project_control/DAILY_CLOSE_2026-09-20.md && echo DAILY_CLOSE_OK
test -f docs/project_control/project_state.json && echo PROJECT_STATE_OK
test -f docs/project_control/dashboard.html && echo DASHBOARD_OK
test -f production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json && echo MASTER_CATALOG_OK
test -f docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json && echo REGISTRY_OK
```

Required logical markers after sync:
- Project State revision：R161 or later
- Dashboard：v101 or later
- Registry：V008 / 505
- Stage1 approved Master count：10
- T-024：CLOSED / PR #11 MERGED
- current engineering task：NONE
- T-018：HOLD

## 6. Phase E｜Open PR verification

GitHub open PRs expected at close:

- PR #3｜T-018｜SUPERSEDED / READ-ONLY / DO NOT MERGE
- PR #6｜T-018 replacement｜HOLD / DO NOT MERGE

There should be no open PR #9/#10/#11.

Do not checkout PR #3 or PR #6 during local sync.

## 7. Phase F｜Actions artifact reconciliation

Important：

Git does not contain approved canonical Master `.blend` binaries for T-021—T-024.

Do not substitute final-regression rebuild binaries for Product Owner-approved first-article binaries.

Approved artifact inventory:

| Task | Artifact ID | Approved binary SHA |
|---|---:|---|
| T-021 四椽栿 | 10583607231 | 9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997 |
| T-022 平梁 EW_SEAM | 10597296654 | 5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4 |
| T-022 平梁 GABLE | 10597296654 | f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a |
| T-023 丁栿 | 10599280924 | 81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737 |
| T-024 乳栿 | 10601690312 | 0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208 |

Artifact reconciliation is a separate step from Git pull.

Before putting any downloaded `.blend` into a local canonical/local-only location:
1. verify ZIP/download identity;
2. verify binary SHA-256;
3. preserve existing local-only binary assets;
4. do not commit `.blend` to normal Git;
5. document the final local path.

## 8. Existing local-only assets

Do not overwrite or delete existing local-only Blender assets merely because they are absent from Git.

Previously documented local-only examples include P0.3 baseline/variant `.blend` assets and Blender backup files.

Local binary reconciliation must be additive/verified unless a specific replacement is separately approved.

## 9. Stop conditions

STOP before modifying local data if any of these appears:

- not inside the expected Git repository;
- origin URL unexpected;
- current branch not `main`;
- uncommitted changes;
- untracked project files that might be important;
- local commits ahead of origin/main;
- divergent history;
- merge/rebase in progress;
- detached HEAD;
- existing local-only `.blend` collision;
- SHA mismatch on downloaded approved artifacts.

No `reset --hard`, `clean -fd`, force checkout, or branch deletion is part of the approved sync procedure.

## 10. What to return to ChatGPT

After Phase A + B, paste:

```text
pwd
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git remote -v
```

I will then decide whether fast-forward is safe.

After successful Phase D, paste:

```text
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log -1 --oneline --decorate
```

Do not begin the next Stage1 Master until local sync verification is closed.

## 11. V008 Master-progress verification after sync

After Git fast-forward sync, verify the derived V008 Excel:

`docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.xlsx`

Expected first sheet:
- `进度总览`

Expected values:
- 登记记录数：505
- 登记对象类型：66
- Stage1 Master范围：28
- 已批准 Master：10
- 待完成 Master：18
- Master完成度：35.7%
- 已绑定Master的登记记录：52
- binding errors：0
- PENDING_SOURCE_BINDING：7

Expected instance-table columns:
- Stage1处置
- Master状态
- Master引用

Generator version：1.0.2  
Current Excel SHA-256：
`dd0364c03f9c44c4d15f3b2aa192a1117af5261aa1705402562570a36019342c`

If these values are missing after local sync, STOP before starting the next Master and reconcile the local derived Excel.


## Completion record

Status：**PASS / COMPLETE**

- Local `main` fast-forwarded successfully.
- Local HEAD matched `origin/main` at synchronization checkpoint: `995a8f42be21e9f1f8c8b013424ea56d5c1b554a`.
- Project State / V008 / derived Excel verification passed.
- V008 Excel SHA-256 matched: `dd0364c03f9c44c4d15f3b2aa192a1117af5261aa1705402562570a36019342c`.
- T-021—T-024 approved Actions artifacts were downloaded and verified.
- Five approved canonical `.blend` binaries were restored into the local Master library with exact SHA matches.
- Final Git safety check: clean; `.blend` files remain ignored.
- Local sync gate：CLOSED.
