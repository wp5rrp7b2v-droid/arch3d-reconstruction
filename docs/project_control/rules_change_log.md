# Rules Change Log｜ARCH3D-001

本文件只记录“项目管理规则本身”的变化，不记录普通项目进展。

| ID | 日期 | 变化 | 原因 | 状态 |
|---|---|---|---|---|
| RC-001 | 2026-09-10 | 建立 Gate 驱动机制；项目阶段推进以验收而非 Chat 数量为依据。 | 防止聊天窗口成为项目结构。 | ACTIVE |
| RC-002 | 2026-09-10 | Dashboard 曾被定义为单文件 SSOT / 正式状态入口。 | 早期追求跨 Chat 简化。 | **SUPERSEDED BY RC-004** |
| RC-003 | 2026-09-10 | 引入 Rxxx Checkpoint，避免每个细小进展都生成一个 Dashboard 版本。 | 降低 Dashboard 版本噪音。 | **PARTIALLY SUPERSEDED BY RC-004** |
| RC-004 | 2026-09-10 | Project Control 文件集成为 SSOT；Dashboard 改为派生可视化；Checkpoint 只做一致性核对、压缩、Phase Closure 与 Dashboard 刷新。 | 分离正式档案与可视化驾驶舱职责。 | ACTIVE / BASELINE 2.0 |
| **RC-005** | **2026-09-10** | **GitHub private repo `main` 的最新正式 Project Control 提交作为 canonical committed state，本地为 working copy；ChatGPT 可直接维护 Project Control；本地工程前先 pull，禁止并行修改同一控制文件。** | **保留版本历史与跨环境访问，同时减少长 Codex 管理指令。** | **ACTIVE / TRIAL** |
| **RC-006** | **2026-09-12** | **Dashboard `Overall Gate Status` 固定显示6条并允许框内滚动；`Current Gate` 必须显示完成度；长标签区域使用响应式列宽。** | **保持 Dashboard 全局观与可读性。** | **ACTIVE / DASHBOARD UI RULE** |
| **RC-007** | **2026-09-13** | **GitHub 网络失败与 Git 冲突正式分流；曾采用 repo-local 固定代理端口。** | **固定动态端口易形成 stale configuration。** | **SUPERSEDED BY RC-010** |
| **RC-008** | **2026-09-13** | **本地 Blender 自动执行统一使用固定 executable + CLI/background；GUI/LaunchServices 失败不等于 Blender engine failure。** | **把自动化与桌面 GUI 解耦，提高确定性。** | **ACTIVE / LOCAL BLENDER EXECUTION RULE** |
| **RC-009** | **2026-09-13** | **引入 `LEAN_PRODUCTION_MODE`：共享 pipeline + first-article gate + 独立逐资产验收；减少重复读取/代码/启动，不减少 DoD、Hard Fail、Evidence Boundary、validation 或正式视觉审核。** | **降低 Codex 额度和重复工程成本，不降低质量。** | **ACTIVE / LEAN PRODUCTION RULE** |
| **RC-010** | **2026-09-13** | **GitHub 网络统一采用动态 `git-proxy-auto` helper：读取当前系统代理并按命令临时注入；HTTP/1.1；异常 push 后核对 remote SHA；禁止因网络错误 force/reset/rebase/overwrite。** | **固定代理端口不稳定；动态 helper 已验证可恢复发布。** | **ACTIVE / DYNAMIC GIT CONNECTIVITY RULE** |
| **RC-011** | **2026-09-13** | **试运行 `CHAT_FIRST_CODEX_EXECUTOR_MODE`：ChatGPT 负责证据/Task Contract/语义/异常诊断/视觉审核/Project Control；Codex 负责确定性执行与机器验证；合同外问题 STOP 回 ChatGPT；默认 MEDIUM。** | **把推理额度集中在必要判断和工程执行。** | **T013 TRIAL COMPLETE / T015 + T016 SUCCESSFUL REUSE / LONG-TERM EVALUATION PENDING** |
| **RC-012** | **2026-09-13** | **正式人工审核/展示的构件、组合与证据视觉资产必须显示项目正式中文构件名；ID/英文可辅助但不得替代中文；历史原称声明需直接文献证据。** | **保证古建专业术语可读、可追溯并避免历史术语误读。** | **ACTIVE / CHINESE COMPONENT VISUAL NAMING RULE** |
| **RC-013** | **2026-09-13** | **每天正式收尾前必须执行 `DAILY_PROJECT_CONTROL_CONSISTENCY_AUDIT`，核对 project_state、acceptance_matrix、decision_log、execution_log、governance、rules_change_log、dashboard 及相关 phase_archive；明确差异当天修正，不能判断则登记 known exception / HOLD。** | **防止一天内多次更新后产生跨文件状态漂移。** | **ACTIVE / DAILY CLOSING CONSISTENCY AUDIT** |
| **RC-014** | **2026-09-14** | **建立 `CLOUD_MODE_2026-09-16_20` 临时运行规则：无本地 Mac 期间仅使用 ChatGPT App、Codex Cloud、GitHub；One Task = One Branch = One PR；local-Mac-dependent 工作不得伪造 PASS。** | **保证短期无 Mac 环境项目可继续推进且不降低验收标准。** | **APPROVED / PLANNED TEMPORARY MODE** |
| **RC-015** | **2026-09-14** | **GitHub `main` 已有正式审核图时，ChatGPT 默认直接调阅并实际打开；只有实际逐张目视后才允许 `VISUAL REVIEW PASS`；local-only 或不可读图片仍需上传 Chat。** | **消除重复上传并防止仅凭脚本/metadata 提前宣称视觉审核完成。** | **ACTIVE / DIRECT GITHUB VISUAL REVIEW RULE** |
| **RC-016** | **2026-09-14** | **补登记 Governance 4.6《Project Language & Terminology Layering｜项目语言与术语分层规则》：古建筑内容层中文优先；项目管理/工程控制层允许成熟英文术语；机器实现层保持稳定英文字段，人类可读材料需映射清晰中文。本次为既有已生效规则的 Rules Change Log 镜像补登记，不改变原规则内容。** | **Daily Closing Audit 发现 Governance 与 Rules Change Log 未双向镜像，按 RC-013 当日修正，避免规则只存在单一文件。** | **ACTIVE / LANGUAGE & TERMINOLOGY LAYERING RULE / BACKFILLED MIRROR** |

## 当前有效原则摘要

`Project Control = 正式事实与治理`

`GitHub main = canonical committed state / versioned mirror during trial`

`Local docs/project_control = working copy`

`Dashboard = Project Control 的派生可视化界面`

`ChatGPT = Project Control 优先维护者`

`Codex = 工程执行优先；未经明确授权不得自行改变重大决策、Gate 或 Governance`

`Dashboard Overall Gate Status = fixed 6 rows + internal scroll`

`Dashboard Current Gate = always show gate completion x/y`

`GitHub network failure = dynamic proxy detection + per-command injection + HTTP/1.1 + remote-SHA verification; not Git conflict`

`Local Blender automation = fixed executable + CLI/background; GUI launch is not the default execution path`

`Lean Production = shared pipeline + first-article gate + independent per-asset acceptance`

`Chat-first Codex-executor = T013 trial + T015/T016 successful reuse; long-term evaluation pending`

`Formal human-facing component/assembly/evidence visuals = Chinese canonical component name required`

`Project language layering = ancient-architecture content Chinese-first; project/engineering English allowed; machine fields stable English with human-readable Chinese mapping`

`Direct GitHub visual review = no duplicate Chat upload for committed review images; no VISUAL PASS without actual image inspection`

`Daily closing = mandatory cross-file Project Control consistency audit`

`Cloud Mode 2026-09-16→20 = ChatGPT App + Codex Cloud + GitHub only; no local-Mac-dependent PASS; One Task = One Branch = One PR`

`同步模式 = TRIAL；价值不足时可调整`