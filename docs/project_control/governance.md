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
4. **push 结果必须验证**：若 push 正常返回成功，则结束；若发生 `unexpected disconnect`、`remote end hung up`、timeout 或等价异常，helper 应只读查询远端 branch SHA：
   - remote SHA == local intended HEAD → `SUCCESS_WITH_ACK_LOSS`；
   - remote SHA != local intended HEAD → `NETWORK_PUSH_FAILED`。
5. **不无限重试**：同一网络失败不得无上限重复 push；确认真实失败后停止并报告网络 blocker，避免无效消耗工程额度。
6. **冲突与网络严格分流**：只有 non-fast-forward、unknown tracked changes、同文件并行修改或真实 merge conflict 才进入 Git conflict STOP；普通 443 timeout / proxy disconnect 不得触发 force、reset、rebase、overwrite 或改写历史。
7. **helper 路径**：当前本机复用 helper 为 `$HOME/.local/bin/git-proxy-auto`；其职责仅是网络层适配，不改变 Git 历史或项目内容。
8. **验证记录**：T-012 发布过程中，固定代理链路出现 sideband disconnect；升级为动态 helper + HTTP/1.1 + push 保护后，提交 `d1ae53ee368729a395623a8d9a4342f7455e2e9b` 已成功发布到 `origin/main`。

推荐日常用法：

```bash
git-proxy-auto pull --ff-only origin main
git-proxy-auto fetch origin
git-proxy-auto push origin main
git-proxy-auto ls-remote origin refs/heads/main
```

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

### 4.4 Chat-first Codex-executor Mode｜T-013 试运行完成 / 评估待定

`CHAT_FIRST_CODEX_EXECUTOR_MODE` 已在 T-013 完成一次正式试运行，结果为工程链完成、逐资产验证完整，并出现一次仅影响呈现的 Overview 修正。当前状态为 **TRIAL COMPLETE / EVALUATION PENDING**，尚未自动升级为全项目长期默认模式。

在正式评估完成前：

1. **职责分离保持明确**：ChatGPT 负责证据解释、Task Contract、参数/几何语义、Hard Fail、非显然异常诊断、视觉审核与 Project Control；Codex 负责确定性工程执行、机器验证、资产生成和经授权的提交；
2. **合同外问题必须返回**：证据冲突、几何方法变化、参数语义不明、非显然 validation failure 或历史解释扩张，Codex 必须 STOP 并把最小失败证据交回 ChatGPT；
3. **Think Level**：显式采用该模式的任务中 Codex 默认 MEDIUM；只有 ChatGPT 判断存在结构性工程问题后才针对性升级 HIGH；
4. **不降低验收标准**：DoD、Hard Fail、逐资产 validation、mutation、independent reopen、review package 和 Product Owner approval 均保持；
5. **不自动继承**：在是否转为长期默认规则的评价完成前，后续任务只有在 Task Contract 明确采用时才使用该执行模式；
6. **不阻塞当前 Gate 设计**：RC-011 的长期评估不阻塞 P3.2 Definition of Done 的定义与审批。

### 4.5 Chinese Component Naming in Visual Assets｜中文构件命名规则

该规则适用于所有正式面向人工审核、项目展示或证据表达的**构件图、装配图、Library Overview、Evidence Visualization 及同类视觉资产**。只要图中标识具体构件身份，就必须遵守：

1. **中文名称必显**：必须显示项目正式中文构件名；`component_id` 可并列，英文可作为辅助，但不得只显示英文或 ID 而省略中文名称；
2. **证据优先**：中文名称优先继承当前直接证据来源中使用的古建筑专业术语；如项目已形成正式 canonical naming，则以项目 canonical 中文名作为视觉主名称，并在文档/metadata 中保留来源追溯；
3. **不得自行改名**：未经证据或正式决策，不得擅自现代化翻译、简称、俗称替换或重命名专业构件；
4. **现代术语与古籍术语分层**：现代测绘报告名称、项目 canonical naming 与历史文献原称属于不同证据层，不得混写；
5. **古称声明需直接证据**：不得未经直接历史文献核证，把现代测绘/项目术语标注成“宋代原称”“古籍原称”或《营造法式》原称；只有存在直接历史文献证据时，才能单独标注古籍原称及出处；
6. **来源不明时不臆造**：若历史原称无法核证，保持项目 canonical 中文名并明确其来源层级，不为版面完整性补造古称。

本规则从 T-014 `P3_1_MASTER_LIBRARY_OVERVIEW_V001` 的命名修订中正式抽象为跨阶段长期规则，后续 P3.2、P3.3 及其他正式人工审核视觉资产默认继承。

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
- Dashboard Architecture Baseline：**v006**；当前 Visualization Snapshot 版本单独记录在 `project_state.json` 与 `dashboard.html`，两者不得混为同一版本号。

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

## 10. Scope / Non-goals｜当前 P3

当前正式案例仍为**平遥镇国寺万佛殿**。P3 的目标是建立可登记、可解释、可复用、可组合的古建筑构件系统，并验证构件之间的装配关系与构件驱动重建能力，不把阶段目标扩大为寺院群、城市级或无限精细化建模。

当前边界：

- P3.0、P3.1 已关闭；P3.2 `Assembly Relationship Model` 已进入，但其 Definition of Done 尚未批准；
- P3.2 DoD 获 Product Owner 明确批准前，不创建 P3.2 工程任务，不提前进行装配工程实现；
- P3.3 在 P3.2 PASS 前保持 LOCKED；
- P1/P2/P3.1 的 evidence boundary 持续有效，不因进入装配阶段而把 UNKNOWN、Proxy、Control、Envelope、Deferred 对象静默历史化；
- 六椽栿 `canonical_reference_length_mm=1000` 仅为非历史 reference specimen，严禁作为建筑实际装配长度自动继承；`REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` 继续作为 Hard Fail；
- 未经验证或未经 Task Contract 授权的 AI / Cloud / Blender 能力不得直接视为正式生产能力；
- 不以视觉完整性替代历史证据，不因构件系统可组合而宣称“完全还原963原貌”。