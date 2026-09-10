# Governance｜Project Control System 2.0

## 1. 核心原则

**Project Control 文件集是项目正式事实源；Dashboard 是派生的可视化管理工具。**

正式目录：

`/Users/caroline/中国古建筑3D复原/docs/project_control/`

当前同步试运行中，GitHub private repo `main` 上最新正式提交的 `docs/project_control/` 定义为 **canonical committed state**；本地同目录是日常 **working copy**。Dashboard 可以重新生成或替换；若 Dashboard 与 Project Control 文件冲突，以 Project Control 为准。

## 2. 文件职责

| 文件 | 唯一职责 |
|---|---|
| `project_state.json` | 当前 Phase、Gate、Baseline、Current Task、Blocker、Next Action 等机器可读当前状态 |
| `decision_log.md` | 已批准、会影响后续执行的重大决策 |
| `execution_log.md` | T-### 工程执行结果、关键失败、证据摘要 |
| `acceptance_matrix.md` | Gate / 验收标准、状态、通过依据、限制 |
| `governance.md` | 项目治理、角色、SSOT、记录机制、审批与版本规则 |
| `rules_change_log.md` | 管理机制本身的变更历史与被替代规则 |
| `phase_archive/` | Phase 关闭后的压缩总结，例如 `P0_closure.md` |
| `dashboard.html` | 从 Project Control 提取当前摘要形成的可视化驾驶舱；非正式历史档案载体 |

## 3. 即时落档机制

项目过程中只要出现以下已确认事实，ChatGPT 应判断其归属并**当下进入 Project Control**，不等待一天结束：

- 重大方向或架构决定 → `decision_log.md`
- T-### 完成、失败、阻塞或关键恢复 → `execution_log.md`
- Gate 状态、验收结论、限制变化 → `acceptance_matrix.md`
- Phase / Gate / Baseline / Current Task / Blocker / Next Action 变化 → `project_state.json`
- 项目管理机制变化 → `governance.md` + `rules_change_log.md`

普通讨论、未形成结论的推测、一次性操作细节、重复日志不进入正式档案。

## 4. Project Control Synchronization Model｜TRIAL

当前采用以下同步方式试运行：

1. **GitHub main**：保存最新正式提交状态、Git 历史、备份和跨环境访问副本。
2. **Local working copy**：`/Users/caroline/中国古建筑3D复原/docs/project_control/`，用于本地直接查看和工程配合。
3. **ChatGPT direct write**：凡属于 Project Control 的状态、决策、验收、治理和 Dashboard 更新，优先由 ChatGPT 直接更新 GitHub，避免重复生成长 Codex 管理指令。
4. **Local sync**：进入本地工作前执行 `git pull --ff-only origin main`，使 working copy 与 canonical committed state 对齐。
5. **Local engineering write-back**：若 Codex 的工程结果需要进入 Project Control，应在工程完成后根据明确授权更新、commit、push；若 Project Control 可由 ChatGPT 根据结果直接更新，则优先由 ChatGPT处理。
6. **冲突规则**：ChatGPT 与本地 Codex 不得并行修改同一 Project Control 文件。发生非 fast-forward 或不明 tracked changes 时停止，不 force、不覆盖。
7. **敏感信息规则**：Project Control 不记录密码、Token、个人敏感资料或其他不应上云的信息。
8. **试运行退出条件**：如果同步成本、版本噪音、隐私风险、冲突频率或维护复杂度明显大于版本历史、备份和跨环境访问的收益，由 Product Owner 批准后调整策略。

## 5. Checkpoint 的职责

Checkpoint **不负责首次落档**。它只负责：

1. 核对 Project Control 文件之间是否一致；
2. 合并重复或过细记录；
3. 到 Phase 结束时生成 `phase_archive/Px_closure.md`；
4. 根据最新 Project Control 重新生成 `dashboard.html`。

典型 Checkpoint：阶段 / Gate Review 完成、重大方向变更、切换 Chat、当天结束、Product Owner 明确要求刷新 Dashboard。

## 6. Dashboard 规则

- Dashboard 只展示 Product Owner 当前管理与决策所需信息。
- 不保存完整 Decision Log、Execution Log、Acceptance Matrix 或 Rules Change Log 历史。
- canonical Dashboard 路径固定为 `docs/project_control/dashboard.html`；其历史由 Git 负责，不靠文件名堆叠版本。
- Dashboard 内可包含从 `project_state.json` 派生的 compact snapshot，便于跨 Chat handoff，但该 snapshot 不是 Project Control 事实本体。
- Dashboard 可视化架构当前版本：**v006**。

## 7. Codex Task Contract 与权限边界

- 只有实际交给 Codex 执行的工程任务占用 T-###。
- ChatGPT 的分析、项目管理、Gate Review、Prompt 设计和 Project Control 判断本身不占 T 编号。
- 同一任务目标只递增 V###；只有任务目标变化才创建新 T。
- 正式命名：`【中国古建筑3D复原｜T-###｜TASK_KEY_V###｜中文任务名】`
- 每份正式 Codex 指令必须明确 Think Level：LOW / MEDIUM / HIGH / XHIGH。
- LOW：机械、确定性操作；MEDIUM：默认工程执行；HIGH：复杂调试、跨环境推理；XHIGH：仅 High 明确不足或 Product Owner 指定。
- Codex 默认可读取 Project Control，但不得自行改变重大决策、Gate 结论或 Governance。
- 只有 Task Contract / Project Control Maintenance 指令明确授权时，Codex 才可修改 Project Control。
- Product Owner 与 ChatGPT 负责决定哪些事实应进入正式 Project Control。

## 8. 决策与变更

- 用户质疑本身不自动改变正式方案；只有新证据、逻辑错误、前提变化或实验失败才触发改向。
- 重大方向变化应形成 Change Proposal 或等价的明确方案，由 Product Owner 批准后进入 Decision Log。
- 决策若被后续规则替代，不删除历史，而是在 Decision Log / Rules Change Log 中标记 `SUPERSEDED`。

## 9. 角色

- **Product Owner**：用户；负责目标、重大决策、Gate Approval。
- **ChatGPT**：项目控制、方案、验证设计、审核、Change Proposal，并优先维护 Project Control。
- **Codex**：本地工程执行；按明确 Task Contract 工作。
- **GitHub Actions / Cloud**：自动化、Cloud Blender 与工程执行节点。
- **GitHub private repo**：当前试运行中的正式提交状态、版本历史、备份和跨环境访问层。

## 10. Scope / Non-goals｜当前 P0

- P0 只验证管理与技术闭环，不追求正式古建筑成果。
- 不启动大型建筑群、城市级模型或高成本渲染。
- 未经验证的 AI / Cloud 能力不得直接视为正式生产能力。
