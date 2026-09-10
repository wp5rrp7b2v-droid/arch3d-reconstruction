# Rules Change Log｜ARCH3D-001

本文件只记录“项目管理规则本身”的变化，不记录普通项目进展。

| ID | 日期 | 变化 | 原因 | 状态 |
|---|---|---|---|---|
| RC-001 | 2026-09-10 | 建立 Gate 驱动机制；项目阶段推进以验收而非 Chat 数量为依据。 | 防止聊天窗口成为项目结构。 | ACTIVE |
| RC-002 | 2026-09-10 | Dashboard 曾被定义为单文件 SSOT / 正式状态入口。 | 早期追求跨 Chat 简化。 | **SUPERSEDED BY RC-004** |
| RC-003 | 2026-09-10 | 引入 Rxxx Checkpoint，避免每个细小进展都生成一个 Dashboard 版本。 | 降低 Dashboard 版本噪音。 | **PARTIALLY SUPERSEDED BY RC-004**：Checkpoint 继续存在，但不再承担首次落档。 |
| RC-004 | 2026-09-10 | Project Control 文件集成为 SSOT；Dashboard 改为派生可视化。重要变化即时写入对应控制文件；Checkpoint 只做一致性核对、压缩、Phase Closure 与 Dashboard 刷新。Dashboard 与控制文件同置 `docs/project_control/`，canonical 文件为 `dashboard.html`，历史由 Git 管理。 | 避免 Dashboard 随项目历史无限膨胀，并把“正式档案”与“可视化驾驶舱”职责分离。 | ACTIVE / BASELINE 2.0 |
| **RC-005** | **2026-09-10** | **Project Control 进入同步试运行：GitHub private repo `main` 的最新正式提交作为 canonical committed state，本地 `docs/project_control/` 为 working copy。ChatGPT 可直接维护 GitHub Project Control；Codex 默认聚焦工程执行。进入本地 Codex 工作前先 pull，且禁止 ChatGPT 与 Codex 同时修改同一控制文件。** | **减少长 Codex 管理指令与重复汇报带来的 token/操作成本，同时保留版本历史、备份和跨环境访问能力。** | **ACTIVE / TRIAL** |

## 当前有效原则摘要

`Project Control = 正式事实与治理`

`GitHub main = canonical committed state / versioned mirror during trial`

`Local docs/project_control = working copy`

`Dashboard = Project Control 的派生可视化界面`

`ChatGPT = Project Control 优先维护者`

`Codex = 工程执行优先；未经明确授权不得自行改变重大决策、Gate 或 Governance`

`同步模式 = TRIAL；价值不足时可调整`
