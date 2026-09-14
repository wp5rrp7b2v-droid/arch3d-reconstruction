# Rules Change Log｜ARCH3D-001

本文件只记录“项目管理规则本身”的变化，不记录普通项目进展。

| ID | 日期 | 变化 | 原因 | 状态 |
|---|---|---|---|---|
| RC-001 | 2026-09-10 | 建立 Gate 驱动机制；项目阶段推进以验收而非 Chat 数量为依据。 | 防止聊天窗口成为项目结构。 | ACTIVE |
| RC-002 | 2026-09-10 | Dashboard 曾被定义为单文件 SSOT / 正式状态入口。 | 早期追求跨 Chat 简化。 | **SUPERSEDED BY RC-004** |
| RC-003 | 2026-09-10 | 引入 Rxxx Checkpoint，避免每个细小进展都生成一个 Dashboard 版本。 | 降低 Dashboard 版本噪音。 | **PARTIALLY SUPERSEDED BY RC-004**：Checkpoint 继续存在，但不再承担首次落档。 |
| RC-004 | 2026-09-10 | Project Control 文件集成为 SSOT；Dashboard 改为派生可视化。重要变化即时写入对应控制文件；Checkpoint 只做一致性核对、压缩、Phase Closure 与 Dashboard 刷新。Dashboard 与控制文件同置 `docs/project_control/`，canonical 文件为 `dashboard.html`，历史由 Git 管理。 | 避免 Dashboard 随项目历史无限膨胀，并把“正式档案”与“可视化驾驶舱”职责分离。 | ACTIVE / BASELINE 2.0 |
| **RC-005** | **2026-09-10** | **Project Control 进入同步试运行：GitHub private repo `main` 的最新正式提交作为 canonical committed state，本地 `docs/project_control/` 为 working copy。ChatGPT 可直接维护 GitHub Project Control；Codex 默认聚焦工程执行。进入本地 Codex 工作前先 pull，且禁止 ChatGPT 与 Codex 同时修改同一控制文件。** | **减少长 Codex 管理指令与重复汇报带来的 token/操作成本，同时保留版本历史、备份和跨环境访问能力。** | **ACTIVE / TRIAL** |
| **RC-006** | **2026-09-12** | **Dashboard 显示约束：`Overall Gate Status` 固定显示 6 条记录，新增 Gate 采用框内滚动；`Current Gate` 必须显示 Gate 完成度（如 3/4）；`Final Review Set` 等长标签区域必须使用独立响应式列宽，禁止文字重叠。** | **保持 Dashboard 全局观稳定，不因 Gate 数量或长标签增加而继续拉长、破坏可读性。** | **ACTIVE / DASHBOARD UI RULE** |
| **RC-007** | **2026-09-13** | **GitHub 网络失败与 Git 冲突正式分流；曾采用 repository-local 固定代理端口方案。** | **早期本机验证固定 `127.0.0.1:15236` 可工作，但 VPN / proxy 本地端口可能变化，持久化动态端口会形成 stale configuration。** | **SUPERSEDED BY RC-010** |
| **RC-008** | **2026-09-13** | **本地 Blender 自动执行统一改为 CLI/background：Codex 默认固定调用 `/Applications/Blender.app/Contents/MacOS/Blender --background --python ...`，禁止将 `open -a Blender`、Finder/AppleScript GUI 启动作为正式自动工程链。GUI/LaunchServices 报错不视为 Blender engine failure；先验证 executable + background。只有任务明确需要交互式 GUI 时才例外。** | **本机 Blender 3.6.23 Intel 已验证可运行，但 Codex 经 GUI/LaunchServices 启动时反复报错；把自动化与桌面 GUI 解耦可减少重复故障，并使生成、验证、保存、重开和渲染更确定。** | **ACTIVE / LOCAL BLENDER EXECUTION RULE** |
| **RC-009** | **2026-09-13** | **引入 `LEAN_PRODUCTION_MODE`：在代表性 Pilot / First Article 已验证共享 pipeline 后，同类批量生产默认优先采用共享 generator utility、batch runner、validator、renderer 与首件闸门；减少重复读取、重复代码、重复启动和重复解释，但每个正式资产仍必须独立参数、独立 binary/hash/semantic/Registry，并逐资产完成 deterministic regeneration、reopen、mutation、canonical rebuild、evidence/transform validation 与正式 review package。首件失败立即停止批量扩展；同一根因最多 2 次有证据的修正重试。若几何方法、证据语义或执行环境发生实质变化，必须回到 standalone/pilot mode。** | **在不降低 DoD、Hard Fail、Evidence Boundary 或 Visual Review 的前提下，降低 Codex 额度、重复工程与调试成本，并将 Pilot→批量生产转化为可复用生产范式。** | **ACTIVE / LEAN PRODUCTION RULE** |
| **RC-010** | **2026-09-13** | **GitHub 网络连接统一采用动态 `git-proxy-auto` helper：每次 Git 网络操作读取 macOS 当前系统代理，临时注入 `http.proxy`，不在 global 或 repo-local config 持久化动态端口；通过代理时固定 HTTP/1.1；push 使用受控 POST buffer，并在异常断连后核对远端 SHA 区分真实失败与 ACK 丢失。禁止因网络问题 force/reset/rebase/overwrite，non-fast-forward、unknown tracked changes、同文件并发修改或真实冲突仍须 STOP。该 helper 可供《中国古建筑3D复原》与《诡舍·黑衣夫人》统一复用。** | **固定代理端口存在 stale configuration 风险；T-012 发布中曾出现 sideband unexpected disconnect。动态 helper 在不保存端口的前提下成功发布 `d1ae53ee...`，更适合作为跨项目长期 Git 网络层。** | **ACTIVE / DYNAMIC GIT CONNECTIVITY RULE** |
| **RC-011** | **2026-09-13** | **试运行 `CHAT_FIRST_CODEX_EXECUTOR_MODE`：ChatGPT 负责证据解释、Task Contract、几何/参数语义、Hard Fail、异常诊断、视觉审核和 Project Control；Codex 默认只读取最小锁定输入并执行确定性工程、机器验证、资产生成与提交。Codex 遇到合同外证据冲突、几何方法变化、参数语义不明或非显然实现型 validation failure 时必须 STOP，把最小失败证据交回 ChatGPT；不得自行扩展历史解释或修改 Contract。Codex Think Level 默认 MEDIUM，只有 ChatGPT 明确判断结构性工程问题后才针对性升级 HIGH。所有 DoD、逐资产 validation、mutation、reopen、review package 与 Product Owner approval 标准保持不变。** | **进一步减少 Codex 重复研究、长推理和猜测式调试，把额度集中在实际工程执行；通过“分析/决策与执行分离”降本，但不减少任何正式验收证据。先在 T-013 试运行，再依据额度、返工率与质量结果决定是否转为长期默认。** | **T013 TRIAL COMPLETE / EVALUATION PENDING** |
| **RC-012** | **2026-09-13** | **正式面向人工审核/展示的构件、装配与证据视觉资产，只要标识具体构件身份，就必须显示项目正式中文构件名；component ID 可并列，英文可作为辅助但不得替代中文。中文名称优先继承直接证据来源使用的专业术语；如项目已形成 canonical naming，则按项目正式名称显示并保留来源追溯。不得未经核证自行现代化翻译、简称、改名，也不得把现代测绘/项目术语标注为“宋代原称”“古籍原称”或《营造法式》原称。只有存在直接历史文献证据时，才可单独标注古籍原称及出处。** | **保证古建专业视觉资产对中文专业术语可读、可追溯，同时严格区分现代测绘名称、项目 canonical naming 与历史文献原称，避免视觉展示造成历史术语误读。** | **ACTIVE / CHINESE COMPONENT VISUAL NAMING RULE** |
| **RC-013** | **2026-09-13** | **每天正式收尾前必须执行 `DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT`：逐项核对 `project_state.json`、`acceptance_matrix.md`、`decision_log.md`、`execution_log.md`、`governance.md`、`rules_change_log.md`、`dashboard.html`，以及当日相关的 `phase_archive/` 索引/Closure 文件，确认 Phase、Gate、Current Task、Blocker、Next Action、Decision/Task/Rule 状态、Dashboard snapshot 与历史归档边界彼此一致。发现明确不一致应在当日修正；不能立即判断的差异必须明确登记为 known exception / HOLD，不得静默留到次日。审计本身不占 T 编号；若只做一致性维护且项目状态事实未变化，不强制递增 State Revision。** | **防止一天内多次 Project Control 更新后产生跨文件状态漂移、旧状态残留或规则只落在单一文件中；把“每天结束的一致性核对”从临时人工习惯固化为强制收尾 Gate。** | **ACTIVE / DAILY CLOSING CONSISTENCY AUDIT** |
| **RC-014** | **2026-09-14** | **建立 `CLOUD_MODE_2026-09-16_20` 临时运行规则：在 Product Owner 无本地 Mac 期间，仅使用 ChatGPT App、Codex Cloud 与 GitHub 继续项目；GitHub main 仍为 canonical committed state，ChatGPT 负责判断/审核/Project Control，Codex Cloud 负责 GitHub 仓库内可验证工程；默认采用 One Task = One Branch = One PR；任何依赖 local-only `.blend`、本地 Blender、未入库二进制或本地视觉验收的工作不得伪造 PASS，只能标记为 `DESIGN COMPLETE / LOCAL EXECUTION OR REVIEW PENDING` 或 `DEFERRED / LOCAL_MAC_REQUIRED`。该规则仅适用于《中国古建筑3D复原》，预计 2026-09-16 至 2026-09-20 生效，若 9 月 15 日继续本地开工则在进入 Cloud Mode 前更新最终 snapshot / pending list。** | **保证短期无 Mac 环境下项目仍可推进结构化工程工作，同时保持现有 DoD、Hard Fail、Evidence Boundary 与本地 Blender 基线不降级，并确保回到 Mac 后可无缝恢复。** | **APPROVED / PLANNED TEMPORARY MODE** |
| **RC-015** | **2026-09-14** | **正式审核图若已提交 GitHub `main`，ChatGPT 默认直接从 GitHub 调阅并实际打开图片完成视觉审核，不再要求 Product Owner 将同一图片重复上传 Chat。只有“实际打开并逐张目视检查”后才允许写 `VISUAL REVIEW PASS`；文件存在、生成脚本、hash、metadata、canonical 数据或结构审核均不能替代目视审核。仅 local-only、未入库或 GitHub 无法读取的图片仍需 Product Owner 上传 Chat 或先提交可入库 review image。结构审核与视觉审核必须分开记录。** | **消除已入库审核资产的重复上传步骤，同时修正仅凭脚本/文件存在就提前宣称视觉审核完成的风险，确保审核结论可验证。** | **ACTIVE / DIRECT GITHUB VISUAL REVIEW RULE** |

## 当前有效原则摘要

`Project Control = 正式事实与治理`

`GitHub main = canonical committed state / versioned mirror during trial`

`Local docs/project_control = working copy`

`Dashboard = Project Control 的派生可视化界面`

`ChatGPT = Project Control 优先维护者`

`Codex = 工程执行优先；未经明确授权不得自行改变重大决策、Gate 或 Governance`

`Dashboard Overall Gate Status = fixed 6 rows + internal scroll`

`Dashboard Current Gate = always show gate completion x/y`

`Dashboard long review labels = responsive layout / no overlap`

`GitHub network failure = dynamic proxy detection + per-command injection + HTTP/1.1 + remote-SHA verification; not Git conflict`

`No persistent dynamic Git proxy port in global or repository config`

`Local Blender automation = fixed executable + CLI/background; GUI launch is not the default execution path`

`Lean Production = shared pipeline + first-article gate + independent per-asset acceptance; reduce duplication, not quality`

`Chat-first Codex-executor = T013 trial complete / evaluation pending; ChatGPT decides/diagnoses/reviews; Codex executes/validates; contract-external ambiguity returns to ChatGPT; Codex MEDIUM by default when explicitly adopted`

`Formal human-facing component/assembly/evidence visuals = Chinese canonical component name required; English/ID may assist but not replace Chinese; historical original-name claims require direct historical-source verification`

`Direct GitHub visual review = already-committed review images are opened and inspected directly by ChatGPT; no duplicate Chat upload; no VISUAL PASS without actual image inspection`

`Daily closing = mandatory cross-file Project Control consistency audit; fix same-day inconsistencies or explicitly record known exception / HOLD`

`Cloud Mode 2026-09-16→20 = ChatGPT App + Codex Cloud + GitHub only; no local-Mac-dependent PASS; One Task = One Branch = One PR; scope limited to ARCH3D-001`

`同步模式 = TRIAL；价值不足时可调整`