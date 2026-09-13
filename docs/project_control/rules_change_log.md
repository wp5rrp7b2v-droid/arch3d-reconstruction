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

`同步模式 = TRIAL；价值不足时可调整`
