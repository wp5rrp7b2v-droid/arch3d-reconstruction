# Decision Log｜ARCH3D-001

本文件只记录已经形成正式结论、会影响后续执行的重大决策。讨论过程和未批准方案不进入本文件。

| ID | 日期 | 决策 | 状态 / 影响 |
|---|---|---|---|
| D-001 | 2026-09-10 | 项目采用 Gate 驱动，而不是 Chat 驱动。 | ACTIVE |
| D-002 | 2026-09-10 | 本地承担轻量建模与审核，Cloud承担较重计算。 | 后续由 D-009 / D-010 细化 |
| D-003 | 2026-09-10 | 采用单文件 HTML Dashboard 作为项目控制入口。 | **PARTIALLY SUPERSEDED BY D-012**：仍可作为可视化入口，但不再是 SSOT |
| D-004 | 2026-09-10 | Dashboard 前台只展示 Product Owner 当前决策所需信息。 | ACTIVE |
| D-005 | 2026-09-10 | 标准启动 wording 固化在 Dashboard。 | ACTIVE |
| D-006 | 2026-09-10 | v005 定义为 Dashboard Architecture Baseline 1.0 / LOCK。 | **SUPERSEDED BY D-012**：新可视化基线为 v006 |
| D-007 | 2026-09-10 | Codex 任务采用独立 T-### 编号；每项任务必须显式记录 Think Level。 | ACTIVE |
| D-008 | 2026-09-10 | Project Control System v1.0：Dashboard 为唯一正式状态入口，Rxxx Checkpoint 批量落档。 | **SUPERSEDED BY D-012** |
| D-009 | 2026-09-10 | P0.2 采用非对称版本架构：Local Blender 3.6.23 负责轻量维护与审核；Cloud 可使用更新的 Blender 4.x。 | ACTIVE |
| D-010 | 2026-09-10 | CP-001 APPROVED / CLOSED：Codex Cloud 因网络代理无法取得 Blender，不作为当前 Blender Executor；GitHub Actions Hosted Runner 成为替代执行节点。 | ACTIVE |
| D-011 | 2026-09-10 | P0.2 Gate PASS，分类 Class B｜ROUNDTRIP_WITH_LIMITATIONS。 | ACTIVE |
| **D-012** | **2026-09-10** | **Project Control 文件集成为项目正式事实源（SSOT）；Dashboard 改为从 Project Control 提取摘要生成的可视化快照。Dashboard 与控制文件统一放在 `docs/project_control/`。重要变化即时落档；Checkpoint 负责一致性检查、阶段压缩和 Dashboard 刷新，不再负责首次记录事实。** | **ACTIVE / GOVERNANCE BASELINE 2.0** |

## D-012 直接影响

- 正式事实不再写进 Dashboard 的历史档案区。
- Dashboard 可以删除并重新生成，不影响项目正式记录。
- 当前状态写入 `project_state.json`。
- 重大决策写入 `decision_log.md`。
- Codex 执行事实写入 `execution_log.md`。
- Gate / 验收结论写入 `acceptance_matrix.md`。
- 项目治理规则写入 `governance.md`；规则变化同时记录到 `rules_change_log.md`。
