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

### 4.1 GitHub 网络连接与代理自动恢复

本项目已确认本机可能出现“无法直连 `github.com:443`，但本地系统代理可正常访问 GitHub”的网络情况。该情况属于**网络连接问题**，不得默认解释为 Git 分支冲突或仓库状态异常。

本地/Codex 执行规则：

1. 项目仓库优先使用 **repository-local Git proxy configuration**，不修改全局 Git 配置；
2. 当前已验证可用的 HTTPS/HTTP 代理端点为 `http://127.0.0.1:15236`；若未来系统代理端口变化，以当前 `scutil --proxy` / 实际可用代理为准更新仓库 local config；
3. 若普通 `git pull / fetch / push` 报 `Failed to connect to github.com port 443`、timeout 或等价网络错误，Codex 应自动检查/应用当前本地代理并重试，不把该错误上报为 merge/non-fast-forward 冲突；
4. 只有出现 **non-fast-forward、unknown tracked changes、同文件并行修改或真实 merge conflict** 时才按冲突规则 STOP；
5. 不得为解决网络错误使用 `force`、`reset --hard`、覆盖本地文件或改写历史。

推荐的一次性仓库本地配置：

```bash
git config --local http.proxy http://127.0.0.1:15236
git config --local https.proxy http://127.0.0.1:15236
```

设置后，本仓库后续普通 `git pull / fetch / push` 应自动使用代理，无需每个 T-### 重复显式添加 `-c http.proxy=...`。

### 4.2 本地 Blender 自动执行规则

本项目已验证本机 **Blender 3.6.23 / Intel x64** 可完成脚本化生成、保存、独立重开与审核。Codex 执行本地 Blender 工程时，默认不得依赖 macOS GUI 启动链路。

本地/Codex 执行规则：

1. 默认禁止使用 `open -a Blender`、Finder 双击、AppleScript UI 控制或“先打开 Blender 窗口再执行”的 GUI 自动化方式作为正式工程链；
2. 默认固定调用本机 Blender executable：`/Applications/Blender.app/Contents/MacOS/Blender`；
3. 自动生成、验证、保存、重开检查与自动渲染优先使用 `--background` / CLI，例如：

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python <script.py>
```

4. Task Contract 若未另行批准，不得自动尝试下载安装其他 Blender 版本，也不得因为 GUI 打开失败而改用不受控版本；
5. 若 executable 路径不存在或版本与任务基线不符，Codex 应 STOP 并报告实际路径/版本，不得静默替换；
6. 只有 Product Owner 需要人工视觉检查时，才需要手动打开 `.blend` 或直接查看正式 review PNG；人工检查不是自动工程执行的前置条件；
7. GUI / LaunchServices 报错不等于 Blender engine 不可用。应优先验证 executable + `--background` 是否正常；只有 CLI/background 也失败时才按 Blender runtime blocker 处理。

该规则适用于后续所有本地 Blender T-###，除非某个 Task Contract 经明确批准要求交互式 GUI 操作。

### 4.3 Lean Production Mode｜Pilot 后的精益批量生产

当某类生产已经通过代表性 Pilot 或 First Article 验证，且后续批次共享明确的生成方法、资产合同与验证逻辑时，默认优先采用 `LEAN_PRODUCTION_MODE`。

规则：

1. **共享工具链**：可共享 generator utility、batch runner、validator、renderer、semantic helper，避免为同类资产重复编写相同逻辑；
2. **首件闸门**：先选择风险最高或参数最复杂的代表资产完成完整验证，首件未 PASS 前不得批量扩展；
3. **逐资产独立验收**：每个正式资产仍必须独立 parameter set、canonical binary、SHA256、semantic snapshot、Registry record，并逐资产完成 deterministic regeneration、independent reopen、synthetic mutation、canonical rebuild、transform/evidence validation 与 review package；
4. **保护性输入用 hash check**：对已锁定且无需重新解释的 P2 baseline、approved assets、Contract 等，优先做前后 hash/manifest 比较；hash 不变则不重复通读分析，hash mismatch 才展开调查；
5. **视觉职责分离**：Codex 负责生成正式 review assets 和机器可读检查，不重复消耗额度做逐图视觉判断；视觉审核由 ChatGPT / Product Owner 完成；
6. **重试上限**：同一根因最多 2 次有证据的修正重试；仍失败则 STOP 回报，禁止无上限猜测式调试；
7. **不降低标准**：Lean 只能减少重复读取、重复代码、重复启动、重复解释和非必要中间产物，不得删除 DoD、Hard Fail、Evidence Boundary、逐资产 validation 或正式视觉审核；
8. **适用边界**：若批次之间几何方法、证据语义、资产合同或执行环境发生实质变化，必须回到 standalone / pilot mode，不得机械复用 Lean。

该模式的目标是：**共享生产工具，保留逐资产验收；降低 Codex 额度与工程冗余，而非降低工程质量。**

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
