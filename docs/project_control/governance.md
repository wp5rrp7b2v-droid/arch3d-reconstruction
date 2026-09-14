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
4. **Local sync**：进入本地工作前执行 `git-proxy-auto pull --ff-only origin main`，使 working copy 与 canonical committed state 对齐。
5. **Local engineering write-back**：若 Codex 的工程结果需要进入 Project Control，应在工程完成后根据明确授权更新、commit、push；若 Project Control 可由 ChatGPT 根据结果直接更新，则优先由 ChatGPT处理。
6. **冲突规则**：ChatGPT 与本地 Codex 不得并行修改同一 Project Control 文件。发生 non-fast-forward 或不明 tracked changes 时停止，不 force、不覆盖。
7. **敏感信息规则**：Project Control 不记录密码、Token、个人敏感资料或其他不应上云的信息。
8. **试运行退出条件**：如果同步成本、版本噪音、隐私风险、冲突频率或维护复杂度明显大于版本历史、备份和跨环境访问的收益，由 Product Owner 批准后调整策略。

### 4.1 GitHub 网络连接与动态代理恢复

本机可能出现“Terminal/Git 无法稳定直连 GitHub，但当前 macOS 系统代理可正常访问”的情况。该类错误属于**网络连接层问题**，不得默认解释为 Git 分支冲突或仓库状态异常。

当前统一采用 `git-proxy-auto` 动态 helper，适用于《中国古建筑3D复原》及其他采用同一 GitHub 网络环境的本地项目。

本地/Codex 执行规则：

1. **禁止持久化动态代理端口**：不得在 global 或 repository-local Git config 中长期保存类似 `127.0.0.1:15236` 的 VPN/proxy 动态端口；固定端口方案 RC-007 已由 RC-010 取代。
2. **动态检测**：每次 Git 网络操作由 helper 读取当前 `scutil --proxy`，优先使用当前有效 HTTP/HTTPS/SOCKS 系统代理；代理值仅通过本次 Git command 的 `-c http.proxy=...` 注入。
3. **协议稳定性**：经过本地 HTTP/HTTPS proxy 时默认使用 `http.version=HTTP/1.1`；push 可使用受控 `http.postBuffer` 以降低部分本地代理对 chunked POST 的兼容问题。
4. **push 结果必须验证**：若 push 正常返回成功，则结束；若发生 `unexpected disconnect`、`remote end hung up`、timeout 或等价异常，helper 应只读查询远端 branch SHA：remote SHA == local intended HEAD → `SUCCESS_WITH_ACK_LOSS`；否则 → `NETWORK_PUSH_FAILED`。
5. **不无限重试**：同一网络失败不得无上限重复 push；确认真实失败后停止并报告网络 blocker。
6. **冲突与网络严格分流**：只有 non-fast-forward、unknown tracked changes、同文件并行修改或真实 merge conflict 才进入 Git conflict STOP；普通网络异常不得触发 force/reset/rebase/overwrite。
7. **helper 路径**：`$HOME/.local/bin/git-proxy-auto`；其职责仅是网络层适配，不改变 Git 历史或项目内容。

推荐日常用法：

```bash
git-proxy-auto pull --ff-only origin main
git-proxy-auto fetch origin
git-proxy-auto push origin main
git-proxy-auto ls-remote origin refs/heads/main
```

### 4.2 本地 Blender 自动执行规则

本项目已验证本机 **Blender 3.6.23 / Intel x64** 可完成脚本化生成、保存、独立重开与审核。Codex 执行本地 Blender 工程时，默认不得依赖 macOS GUI 启动链路。

1. 默认禁止使用 `open -a Blender`、Finder 双击、AppleScript UI 控制作为正式工程链；
2. 固定调用 `/Applications/Blender.app/Contents/MacOS/Blender`；
3. 自动生成、验证、保存、重开与渲染优先使用 `--background` / CLI；
4. 未经批准不得自动安装或切换 Blender 版本；
5. executable 路径不存在或版本不符时 STOP；
6. Product Owner 人工视觉检查时才需要手动打开 `.blend` 或查看正式 review PNG；
7. GUI / LaunchServices 报错不等于 Blender engine failure，优先验证 CLI/background。

### 4.3 Lean Production Mode｜Pilot 后的精益批量生产

当某类生产已通过代表性 Pilot / First Article，且后续批次共享生成方法、资产合同与验证逻辑时，默认优先采用 `LEAN_PRODUCTION_MODE`。

1. 共享 generator utility / batch runner / validator / renderer / semantic helper；
2. 先做首件闸门，首件未 PASS 不批量扩展；
3. 每个正式资产仍须独立参数、binary/hash/semantic/Registry，并逐资产完成 regeneration、reopen、mutation、canonical rebuild、evidence/transform validation 与 review package；
4. 锁定输入优先做 hash/manifest 保护检查；
5. Codex 生成 review assets 与机器检查，视觉审核由 ChatGPT / Product Owner 完成；
6. 同一根因最多 2 次有证据修正重试；
7. Lean 不得删除 DoD、Hard Fail、Evidence Boundary、逐资产 validation 或正式视觉审核；
8. 几何方法、证据语义、资产合同或执行环境发生实质变化时回到 standalone / pilot mode。

### 4.4 Chat-first Codex-executor Mode｜试运行后持续复用 / 长期评估待定

`CHAT_FIRST_CODEX_EXECUTOR_MODE` 已在 T-013 试运行，并在 T-015、T-016 成功复用；长期是否升级为全项目默认模式仍待正式评估。

1. ChatGPT 负责证据解释、Task Contract、参数/几何语义、Hard Fail、非显然异常诊断、视觉审核与 Project Control；Codex 负责确定性工程执行、机器验证、资产生成和经授权提交；
2. 合同外证据冲突、几何方法变化、参数语义不明或非显然 validation failure 必须返回 ChatGPT；
3. 显式采用该模式的任务默认 MEDIUM，结构性问题才针对性升级 HIGH；
4. DoD、Hard Fail、逐资产 validation、mutation、independent reopen、review package 和 Product Owner approval 均不降低；
5. 长期默认化前，后续任务仍需在 Task Contract 中明确采用。

### 4.5 Chinese Component Naming in Visual Assets｜中文构件命名规则

正式面向人工审核/展示的构件、组合与证据视觉资产，只要标识具体构件身份：

1. 必须显示项目正式中文构件名；ID/英文仅作辅助；
2. 中文名称优先继承直接证据或项目 canonical naming；
3. 不得未经证据自行改名；
4. 现代测绘名、项目名与历史文献原称分层；
5. 古称声明必须有直接历史文献证据；
6. 来源不明时不为版面完整性补造古称。

### 4.6 Project Language & Terminology Layering｜项目语言与术语分层规则

本项目研究对象为中国古建筑。凡涉及建筑本体、构件名称、构件组合关系、空间与结构关系、史料解释、证据表达以及面向人工理解的复原内容，默认以中文专业术语为主表达。

1. **古建筑内容层｜中文优先**：柱、栌斗、六椽栿、承托关系、连接关系、定位关系、重复关系、从属关系、构件组合、组合单元、定位基准等优先使用中文专业术语。
2. **项目管理与工程控制层｜允许成熟英文术语**：DoD、PASS、HOLD、Hard Fail、Task Contract、Registry、Baseline、Dashboard 等可保留。
3. **机器实现层｜英文稳定字段**：JSON、脚本、Registry、验证字段可保持稳定英文 key；人类可读文档、Dashboard、审核图须映射清晰中文含义。

中文有准确专业称谓时不造新的英文主名称；工程实现动作可使用“装配、生成、实例化、验证”；Gate 可中英并列但中文为主；不因本规则强制改名既有机器字段和 ID。

### 4.7 Direct GitHub Visual Review｜GitHub 正式审核图直接调阅规则

当正式 review PNG/JPG 已进入 GitHub `main` 时，不再要求 Product Owner 重复上传到 Chat。

1. 只有实际打开并逐张目视检查后才可写 `VISUAL REVIEW PASS`；
2. 已提交 GitHub 的正式 review assets 由 ChatGPT 自行调阅；
3. local-only、未提交或 GitHub 无法读取的视觉资产仍须上传 Chat 或先提交允许入库的 review image；
4. 结构审核与视觉审核分开记录；
5. Product Owner 保留最终批准权。

## 5. Checkpoint 的职责

Checkpoint 不负责首次落档，只负责一致性核对、压缩、Phase Closure 与 Dashboard 刷新。

### 5.1 Daily Closing Project Control Consistency Audit｜每日收尾一致性审计

每天正式结束项目工作前必须执行一次，最低核对：

1. `project_state.json`；
2. `acceptance_matrix.md`；
3. `decision_log.md`；
4. `execution_log.md`；
5. `governance.md` + `rules_change_log.md`；
6. `dashboard.html`；
7. `phase_archive/`（相关时）。

审计判定：PASS / PASS WITH KNOWN EXCEPTION / HOLD。明确可纠正的不一致应当天直接修正；无法判断的差异必须登记 known exception / HOLD。

## 6. Dashboard 规则

- Dashboard 只展示 Product Owner 当前管理与决策所需信息；
- canonical 路径固定为 `docs/project_control/dashboard.html`；
- Dashboard snapshot 非 Project Control 事实本体；
- Dashboard Architecture Baseline：**v006**；Visualization Snapshot 版本独立记录；
- `Overall Gate Status` 固定显示 6 条记录并允许内部滚动；`Current Gate` 必须显示 Gate 完成度；长标签区域不得重叠。

## 7. Codex Task Contract 与权限边界

- 只有实际交给 Codex 执行的工程任务占用 T-###；
- ChatGPT 分析、项目管理、Gate Review、设计与 Project Control 判断不占 T 编号；
- 同一任务目标只递增 V###；任务目标变化才创建新 T；
- 正式命名：`【中国古建筑3D复原｜T-###｜TASK_KEY_V###｜中文任务名】`；
- 每份正式 Codex 指令必须明确 Think Level；
- Codex 默认可读取 Project Control，但不得自行改变重大决策、Gate 或 Governance；
- 只有明确授权时 Codex 才可修改 Project Control。

## 8. 决策与变更

- 用户质疑本身不自动改变正式方案；只有新证据、逻辑错误、前提变化或实验失败才触发改向；
- 重大方向变化应形成 Change Proposal 或等价明确方案，由 Product Owner 批准后进入 Decision Log；
- 被后续规则替代的决策不删除历史，而标记 `SUPERSEDED`。

## 9. 角色

- **Product Owner**：目标、重大决策、Gate Approval；
- **ChatGPT**：项目控制、方案、验证设计、审核、Change Proposal；
- **Codex**：按明确 Task Contract 做工程执行；
- **GitHub Actions / Cloud**：自动化与云执行节点；
- **GitHub private repo**：正式提交状态、版本历史、备份和跨环境访问层。

## 10. Scope / Non-goals｜当前 P3

当前正式案例仍为**平遥镇国寺万佛殿**。P3 的目标是建立可登记、可解释、可复用、可组合的古建筑构件系统，并验证构件之间的组合关系与构件驱动重建能力，不把阶段目标扩大为寺院群、城市级或无限精细化建模。

当前边界：

- P3.0、P3.1、P3.2 已关闭；P3.2 Gate Review 9/9 PASS、canonical Hard Fail=0，并由 D-046 正式批准关闭；P3 Gate Progress=3/4；
- P3.3 `构件驱动整殿重建` 已 UNLOCKED / ENTERED，但当前仅进入 **DoD 定义阶段**；P3.3 DoD 获 Product Owner 批准前不得创建 P3.3 工程 Task Contract 或启动整殿生产；
- P3.3 必须继承 P3.2 的五类基础关系、接口/定位、Assembly Unit、runtime instance、building-level parameter、Validator 与 Hard Fail，不重新发明基础组合机制；
- P1/P2/P3.1/P3.2 的 evidence boundary 持续有效，UNKNOWN、Proxy、Control、Envelope、Deferred 不得因整殿重建而静默历史化；
- 六椽栿 `canonical_reference_length_mm=1000` 仅为非历史 reference specimen；在独立 approved building-specific full length 出现前，实际全长几何继续 BLOCKED；
- Z-006 继续 UNKNOWN/null/DO_NOT_LOCK；Z-006-RC-01 保持 replaceable REASONABLE_COMPLETION；具体榫卯、隐藏连接、45°转角、隐角梁继续保持当前证据边界；
- 未经验证或未经 Task Contract 授权的 AI / Cloud / Blender 能力不得直接视为正式生产能力；
- 不以视觉完整性替代历史证据，不因构件系统可组合而宣称“完全还原963原貌”。