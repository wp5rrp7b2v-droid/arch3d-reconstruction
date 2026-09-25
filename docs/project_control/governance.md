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

### 4.8 P3.3 GitHub Actions Blender Execution｜P3.3 云端 Blender 执行规则

P3.3 中凡能够脚本化、无交互、可确定性重放的 Blender 生成与验证，默认采用以下正式链路：

`Codex Cloud writes/updates generator → GitHub Actions runs headless Blender → GitHub records outputs and validation evidence → ChatGPT reviews committed evidence → Local Mac only when interactive/final inspection is genuinely required`

1. **Codex Cloud**：负责 generator、validator、workflow 调整及机器测试，不把 Codex Cloud 本身视为 Blender runtime；
2. **GitHub Actions**：作为脚本化 Blender 的默认 headless executor，负责 clean-state generation、save/reopen、mutation、canonical rebuild、render/review asset、manifest/hash/validation 等可自动化步骤；
3. **GitHub**：保存 commit、workflow run、review PNG、机器 validation 与必要 artifact，形成可追溯证据链；
4. **ChatGPT**：按 RC-015 实际调阅已提交 review images，并审核机器结果、证据边界和 Task Contract 符合性；
5. **Local Mac**：仅保留无法被 approved headless pipeline 等价替代的交互式检查、手动旋转/遮挡/拓扑检查或最终本地兼容性复核；
6. **Cloud Mode 等价规则**：在 RC-014 有效期内，GitHub Actions 被批准作为“脚本化 Blender 生成与验证”的 equivalent execution/validation environment，因此这类工作不再因本地 Mac 暂时不可用而自动 BLOCKED；
7. **不得越权替代**：若某一 DoD/Task Contract 明确要求交互式 Blender 检查或 local-only binary evidence，仍必须标为 `LOCAL_MAC_REQUIRED / PENDING`，不得用 GitHub Actions 结果伪造本地 PASS；
8. **版本与重现性**：每个 Blender Task Contract 必须明确 runner、Blender version、formal inputs、output/evidence、mutation/rebuild 与 failure criteria；未经批准不得静默切换 Blender 版本或历史输入；
9. **审批边界**：本规则批准执行环境与职责分工，不自动授权任何具体 T-### 工程任务，也不自动改变 Gate PASS 状态。

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
- **GitHub Actions / Cloud**：自动化与云执行节点；P3.3 中 GitHub Actions 为脚本化 headless Blender 默认 executor；
- **GitHub private repo**：正式提交状态、版本历史、备份和跨环境访问层。

## 10. Scope / Non-goals｜当前 P3

当前正式案例仍为**平遥镇国寺万佛殿**。P3 的目标是建立可登记、可解释、可复用、可组合的古建筑构件系统，并验证构件之间的组合关系与构件驱动重建能力，不把阶段目标扩大为寺院群、城市级或无限精细化建模。

当前边界：

- P3.0、P3.1、P3.2 已关闭；其历史 PASS / CLOSED 状态不因 P3.3 重基线而撤销；P3 Gate Progress 仍为 3/4；
- P3.3 当前正式实施路线为 `Definition of Done / Implementation Plan V002`，由 D-066 于 2026-09-19 批准并锁定；V001 / D-047 保留为历史版本，不再作为当前实施路线；
- P3.3 V002 固定采用七阶段：①真实构件 Master 库；②构件变体与装配接口；③代表性组合验证；④整殿真实实例与拓扑；⑤整殿空间定位与标高规则；⑥确定性整殿生成；⑦整殿验收与 Gate Closure；
- 当前事实基线为 V008 Component Registry（505条 registry records；不等于505件实体构件）；V007 保留为历史快照；11类 / 40变体 / 365工程对象与 T-017 365 accounting 仅保留为历史工程基线 / comparison，不得作为真实构件完整性或真实构件数量的正式来源；
- P3.1 已批准的 Master 机制和六个既有 Master 继续保留；其 V007/V008 重新绑定与覆盖复核已完成，后续新 Master 按 P3.3 Stage 1 Task Contract 生产；
- P3.2 五类基础关系、接口 / 定位与组合机制继续保留并复用；不得重新发明基础关系语义，但旧 runtime accounting 不自动成为新整殿真实实例图；
- D-048 / RC-017 的脚本化 Blender 执行链继续有效；它只规定执行环境，不意味着旧 T-018 路线继续有效；
- T-020、RZ D-063、FV D-064 保留为已锁设计资产，但统一推迟到 Stage 5 按真实构件装配重新审查，不得在 Stage 1–4 直接作为生产 placement authority；
- T-018 V002 保持 HOLD / NOT CURRENT EXECUTION ROUTE；在 Stage 6 前由 Product Owner 再决定 rebaseline 或 supersede；PR #3 / #6 均不得 merge；
- P1/P2/P3.1/P3.2 的 evidence boundary 持续有效；UNKNOWN、Proxy、Control、Envelope、Deferred、PARAMETRIC_COMPLETION 不得因整殿重建而静默历史化；
- 六椽栿 `canonical_reference_length_mm=1000` 继续仅为非历史 reference specimen，禁止泄漏到建筑实长；历史 full length 仍 UNKNOWN，但若 V007 装配端点可确定，允许将“由装配端点推导的几何长度”作为显式项目几何使用，必须与历史实测长度严格区分；
- Z-006 继续 UNKNOWN/null/DO_NOT_LOCK；Z-006-RC-01 保持 replaceable REASONABLE_COMPLETION；具体榫卯、隐藏连接及其他无证据细节继续保持当前 evidence boundary；
- GitHub Actions 可承担脚本化、可确定性重放的 Blender 执行，但不得替代必须交互式完成的 `LOCAL_MAC_REQUIRED` 证据；
- 不以视觉完整性替代历史证据，不因构件系统可组合而宣称“完全还原963原貌”。

### 4.9 Component Registry → Excel Derived View｜构件登记到Excel派生规则

万佛殿构件数据采用与 Dashboard 相同的“正式事实源 → 可重新生成派生视图”原则。

1. **Canonical Source｜唯一事实源**：`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json` 为当前构件登记唯一正式数据入口；每个正式版本同时保留不可覆盖的 `Vxxx.json` 快照。
2. **Excel Role｜Excel职责**：Excel 仅作为构件登记的派生表格视图，不得作为独立事实源，不得通过人工编辑 Excel 直接改变项目正式构件数据。
3. **Single-write Rule｜单写入规则**：任何新增、修正、删除、证据等级变化，必须先写入版本化 JSON 并同步 CURRENT JSON；随后由自动生成链更新 Excel。
4. **Derived Outputs｜派生输出**：自动生成 `CURRENT.xlsx` 与对应 `Vxxx.xlsx`，并生成同步 Manifest，记录源 JSON、源 GitHub commit、JSON SHA-256、生成器 SHA-256、Excel SHA-256 与记录数。
5. **Fail Closed｜失败关闭**：若 CURRENT 与同版本快照不一致、Excel 行数不匹配、工作簿无法重开或哈希验证失败，则自动流程必须 FAIL；旧 Excel 保留，新登记不得宣称“Excel 已同步”。
6. **No Dual Maintenance｜禁止双维护**：禁止“GitHub JSON 改一份、Excel 再人工改一份”。Excel 中发现错误时，必须回到 canonical JSON 修正，再重新生成。
7. **Version Retention｜版本保留**：版本化 JSON/Excel 保留历史；CURRENT 始终代表当前正式登记和当前派生视图。
8. **Relation to Dashboard｜与Dashboard一致**：Dashboard 派生自 Project Control；构件 Excel 派生自 Component Registry JSON。两种派生物均可删除重建，项目事实不能依赖派生文件才能恢复。
9. **Automation｜自动化**：正式 generator 为 `scripts/generate_wanfo_component_registry_excel.py`；GitHub Actions workflow 为 `.github/workflows/wanfo-component-registry-excel.yml`。
10. **Authorization Boundary｜权限边界**：本规则只建立数据同步机制，不自动授权 T-018、Blender、Actions 生产建模、PR merge 或 Gate PASS；构件 Excel 自动生成 workflow 属于数据派生维护流程，不等于整殿工程执行。

### 4.10 Wanfodian Source Authority Priority｜万佛殿资料主权优先级

适用于 P3.3 及后续所有构件 Master / Variant / Interface、组合关系、整殿拓扑、空间定位、屋架、屋面与整体搭建的资料检索和证据锁定。

1. **A1｜一级工程主权来源**：`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`。直接测绘尺寸、原始测绘图、构件数量/位置、报告明确记载的构造关系与测量事实，以该来源原页为最高工程 authority。
2. **A2｜官方同建筑视觉/结构来源**：`山西文物数字博物馆·万佛殿专题`。用于同建筑实物视觉、官方结构说明、构件形态、层位、现场状态及官方数字展示的直接交叉验证。
3. **Mandatory First Lookup｜强制先查**：进入低等级论文、媒体、其他建筑对比例或通用知识之前，必须先核查 A1 与 A2。两者并列为“最高优先检索层”，但职责不同：A1 主导工程测绘事实；A2 主导官方同建筑视觉/结构核验。
4. **Secondary Sources｜低等级来源**：学术二级论文、媒体文章、模型网站、其他寺院或其他时代建筑的 comparison 仅能补充或交叉验证；不得因其解释更完整而静默覆盖 A1/A2。
5. **Conflict Handling｜冲突处理**：几何、尺寸、数量、测绘事实冲突时优先回到 A1 原页；若 A1 与 A2 在结构语义上存在冲突，不得自行平均、猜测或选择方便建模的一方，必须标记 `CONFLICT/UNKNOWN` 并提交 Product Owner 复核。
6. **Availability Disclosure｜可用性披露**：任一正式审核若当前无法实际访问 A1 或 A2，必须写明 `SOURCE_NOT_AVAILABLE_THIS_PASS`；不得用 secondary/comparative 来源替代后声称一级核查已完成。
7. **Visual Gate Relation｜与 D-076 的关系**：D-076 的 Pre-Model Visual Reference Gate 继续有效；A2 应作为同建筑视觉审核的首要官方入口，A1 中的测绘/式样图仍是更高工程证据。自制图仅可标记 `SOURCE_DERIVED_SCHEMATIC`，comparative 资料必须显式标注 `COMPARATIVE`。
8. **No Historical Upgrade｜禁止静默历史化**：官方同建筑展示或二级解释均不得自动升级为 963 年原状事实；时间层、修缮层和 originality 仍按既有 evidence-boundary 规则独立判断。

Decision authority: **D-099 / RC-019**.

### 4.11 Evidence-Constrained Reconstruction｜资料约束下的工程复原

Decision authority：**D-108 / RC-020**。

P3.3 的项目目标是完成一座与当前可靠资料一致、结构自洽、几何闭合、可生成并可持续迭代的万佛殿3D模型；不把“证明并复制963年全部历史原始几何”设为完成前提。

1. **Evidence First｜资料优先但不等于资料完备才可建模**：A1/A2 与 Registry 已明确的尺寸、数量、位置和结构关系必须优先采用；不得为了建模方便静默覆盖直接证据。
2. **UNKNOWN ≠ BLOCKED**：资料未给出的历史全长、角度、端点、隐藏连接等字段可以继续保留 UNKNOWN/UNRESOLVED 作为历史证据状态；只要模型完成确有需要，可同时建立显式 `RECONSTRUCTED_DESIGN` 参数继续工程。
3. **Reconstructed Design｜工程补全**：reconstructed-design 参数应优先由已锁定构件关系、整体几何、装配端点、对称/拓扑和碰撞闭合推导；必要时允许采用简化、可替换的工程几何。
4. **No Silent Historicization｜禁止静默历史化**：任何 reconstructed-design 值都不得标成 DIRECT_MEASURED、963原值或历史事实；历史证据状态与项目生产几何状态必须同时可追踪。
5. **Replaceability｜可替换性**：后续获得更高质量同建筑直接资料时，reconstructed-design 参数应可被替换，不应要求推翻整个 Master/assembly 架构。
6. **Blocking Criteria｜真正阻塞条件**：只有直接证据冲突未解决、几何无法闭合、构件身份/拓扑不明到无法定义生产对象，或设计会明确违背已锁资料时才进入 HOLD/STOP。
7. **Master / Assembly Separation｜本体与装配分离**：构件 Master 优先保存稳定本体特征；长度、倾角、镜像、具体坐标等若由装配决定，应归 assembly-owned，而不是为每个 placement 复制历史化 Variant。
8. **Detail Staging｜细节分阶段**：隐藏榫卯、端头修形等若非当前阶段实现结构闭合所必需，可先采用明确标注的简化工程表示，后续 Detail Stage 再增强。
9. **D-099 Compatibility｜与资料主权规则兼容**：RC-020 不降低 D-099/RC-019 的 A1/A2 优先级；它改变的是“资料缺口如何处理”，不是“资料冲突时可以忽略资料”。
10. **Completion Standard｜完成标准**：模型验收首先看资料一致性、结构/拓扑一致性、几何闭合、可重复生成和视觉可用性；历史原貌一致性作为独立证据维度记录，不作为所有生产步骤的绝对前置条件。



### 4.12 Minimal Sufficient Infrastructure / No Redundant Asset｜最小充分基础设施 / 禁止冗余资产

Decision authority: **D-123 / RC-021**.

1. Existing canonical assets, Registry, Evidence records, shared builders, validators and workflows must be reused before any new project infrastructure is introduced.
2. A new rule/tool/bridge/index/cache/derived/intermediate asset is allowed only when a concrete current production requirement cannot be met safely by the existing path.
3. Any retained derived asset must have an explicit purpose, authority boundary, lifecycle and regeneration path; it must not become a second source of truth.
4. Temporary troubleshooting assets must be removed after use unless an approved retained purpose is recorded.
5. “May be useful later” is not sufficient justification for permanent project infrastructure.
6. The preferred response to a narrow evidence-access or tooling problem is a narrow, reversible fix that returns the project to the existing production path.
7. Component-specific production must not create duplicate Masters, validators, workflows or caches when Definition-driven shared infrastructure can express the same requirement.
8. This rule does not permit deletion of evidence, validation, traceability, review surfaces or independent cross-checks that are required by DoD/Task Contract.

### 4.13 Execution Path Blocker Immediate Disclosure｜执行路径阻塞即时披露

Decision authority: **D-123 / RC-022**.

1. Once the approved execution path is confirmed blocked, the task status must immediately change from `EXECUTING` to `BLOCKED`; it must not continue to be described as normal execution.
2. As soon as sufficient evidence exists to identify a blocker, ChatGPT must report it to the Product Owner before prolonged troubleshooting.
3. The first blocker report must state: blocker, completed progress, effect on original task achievability, and recommended recovery path.
4. Troubleshooting, workaround validation and infrastructure repair are exception-handling work and must not be counted or represented as normal task execution time.
5. If a workaround adds engineering work, changes shared infrastructure/process, expands scope or alters approved architecture, STOP and obtain Product Owner authorization before executing it.
6. Prohibited pattern: prolonged silent troubleshooting followed by delayed disclosure after failure.
7. After recovery, explicitly record `BLOCKER CLEARED`; only then may the original task return to `EXECUTING`.
8. Before declaring a NEXT Master production-ready, perform a lightweight source-readiness check: A1/A2 accessibility, original-page/parameter provenance sufficiency, and known conflict status. This is a readiness check, not a new permanent evidence system, and it must **not** fail solely because Northern-Song/963 original dimensions, imagery, joinery, full length, angle, or other period-original data are unavailable.

### 4.14 Production Evidence Non-Blocking Precedence｜生产证据非阻塞优先规则

Decision authority: **D-137 / RC-023**.

1. **Missing historical originals are not blockers**：缺少963年/北宋原始尺寸、原始图像、精确全长、角度、隐藏榫卯、端部形态等历史原值，本身不得触发 P3.3 HOLD / STOP / Hard Fail。
2. **Current reliable sources are production authority**：A1现状/测绘资料、A2同建筑官方资料、Registry、已批准工程关系与可验证整体几何共同构成当前生产依据；不得要求“必须有北宋原始数据”才能继续。
3. **Gap handling**：资料缺口保留为 UNKNOWN / UNRESOLVED，同时可建立显式、可替换的 `RECONSTRUCTED_DESIGN` / PARAMETRIC_COMPLETION / simplified proxy 继续生产。
4. **True blockers only**：只有直接资料冲突未解决、生产对象身份/拓扑无法定义、几何/结构无法形成可验证闭合方案，或拟采用方案明确违背已锁直接证据时，才允许因 evidence issue 进入 HOLD/STOP。
5. **D-076 interpretation**：Pre-Model Visual/Form Gate 审核的是“现有资料 + 缺口边界 + 拟采用生产处置是否清楚并获批准”，不是要求资料完整。没有同建筑历史原图/北宋原值不得单独触发 `BLOCKED_ON_VISUAL_REFERENCE_REVIEW`。
6. **Precedence**：若旧 Project Control、历史 Gate 标签、`UNKNOWN_BLOCKED`、`DEFERRED_INSUFFICIENT_EVIDENCE` 等历史术语与本规则产生歧义，历史记录保留原文，但 P3.3 当前生产解释以 RC-020 + RC-023 为准。

