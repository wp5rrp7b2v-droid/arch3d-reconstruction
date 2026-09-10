# Rules Change Log｜ARCH3D-001

本文件只记录“项目管理规则本身”的变化，不记录普通项目进展。

| ID | 日期 | 变化 | 原因 | 状态 |
|---|---|---|---|---|
| RC-001 | 2026-09-10 | 建立 Gate 驱动机制；项目阶段推进以验收而非 Chat 数量为依据。 | 防止聊天窗口成为项目结构。 | ACTIVE |
| RC-002 | 2026-09-10 | Dashboard 曾被定义为单文件 SSOT / 正式状态入口。 | 早期追求跨 Chat 简化。 | **SUPERSEDED BY RC-004** |
| RC-003 | 2026-09-10 | 引入 Rxxx Checkpoint，避免每个细小进展都生成一个 Dashboard 版本。 | 降低 Dashboard 版本噪音。 | **PARTIALLY SUPERSEDED BY RC-004**：Checkpoint 继续存在，但不再承担首次落档。 |
| **RC-004** | **2026-09-10** | **Project Control 文件集成为 SSOT；Dashboard 改为派生可视化。重要变化即时写入对应控制文件；Checkpoint 只做一致性核对、压缩、Phase Closure 与 Dashboard 刷新。Dashboard 与控制文件同置 `docs/project_control/`，canonical 文件为 `dashboard.html`，历史由 Git 管理。** | **避免 Dashboard 随项目历史无限膨胀，并把“正式档案”与“可视化驾驶舱”职责分离。** | **ACTIVE / BASELINE 2.0** |

## 当前有效原则摘要

`Project Control = 记录事实与治理`

`Dashboard = 从 Project Control 提取摘要后的可视化界面`

`Git = 文件与工程历史版本证据`
