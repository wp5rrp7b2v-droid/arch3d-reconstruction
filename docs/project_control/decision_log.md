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
| D-012 | 2026-09-10 | Project Control 文件集成为项目正式事实源（SSOT）；Dashboard 改为从 Project Control 提取摘要生成的可视化快照。Dashboard 与控制文件统一放在 `docs/project_control/`。重要变化即时落档；Checkpoint 负责一致性检查、阶段压缩和 Dashboard 刷新，不再负责首次记录事实。 | ACTIVE / GOVERNANCE BASELINE 2.0 |
| D-013 | 2026-09-10 | 批准 Project Control 同步试运行：GitHub private repo `main` 上最新正式提交的 `docs/project_control/` 作为 canonical committed state；本地同路径作为 working copy。ChatGPT 优先直接维护 Project Control 并形成 Git commit；Codex 聚焦本地工程执行。进入本地 Codex 工作前先同步 main，且不得与 ChatGPT 同时修改同一 Project Control 文件。若后续发现同步成本、版本噪音、隐私风险或维护复杂度大于价值，可由 Product Owner 调整策略。 | ACTIVE / TRIAL |
| D-014 | 2026-09-11 | Product Owner 批准 P0｜技术路线验证关闭。P0.0–P0.3 已达到 4/4 PASS；P0 正式 CLOSED，项目进入 P1｜选题取证。P0.2 的 Blender 4.5→3.6 兼容性限制继续作为生产规则；P0.3 仅证明参数驱动技术链路成立，不代表历史证据参数化或正式古建构造精度已验证。 | ACTIVE / P0 CLOSED / P1 ENTERED |
| D-015 | 2026-09-11 | Product Owner 批准 P1 Gate 架构：P1.0 选题标准锁定；P1.1 候选案例比较与定选；P1.2 正式证据包建立；P1.3 证据分级与可复原性 Go / No-Go。首案优先选择证据充分、规模可控、可参数化且公开资料可取得的古代木构单体；不以知名度作为首要标准。P1.3 PASS 前不进入正式 3D 生产。 | ACTIVE / P1 GATE APPROVED |
| D-016 | 2026-09-11 | Product Owner 批准 P1.0。首案筛选方法正式锁定为五项加权指标：证据链完整度30%、测绘/尺寸资料可获得性25%、结构规模与首案可控性20%、历史状态歧义程度15%（歧义越低得分越高）、参数化与展示价值10%；统一按1–5分评价。首案不以年代最早或知名度为优先。P1.1 解锁，候选池为平遥镇国寺万佛殿、五台佛光寺东大殿、五台南禅寺大殿、宁波保国寺大殿。 | ACTIVE / P1.0 PASS |
| **D-017** | **2026-09-11** | **Product Owner 批准“山西平遥镇国寺万佛殿”为首个正式复原案例。P1.1 正式 PASS；P1.2 解锁并启动。四候选按 P1.0 锁定权重比较后，镇国寺万佛殿获得最高首案适配度。该选择只代表项目首案适配性，不构成对四座建筑历史价值的排序。正式 3D 生产继续受 P1.3 Gate 约束。** | **ACTIVE / CASE LOCKED / P1.1 PASS / P1.2 STARTED** |

## D-012 直接影响

- 正式事实不再写进 Dashboard 的历史档案区。
- Dashboard 可以删除并重新生成，不影响项目正式记录。
- 当前状态写入 `project_state.json`。
- 重大决策写入 `decision_log.md`。
- Codex 执行事实写入 `execution_log.md`。
- Gate / 验收结论写入 `acceptance_matrix.md`。
- 项目治理规则写入 `governance.md`；规则变化同时记录到 `rules_change_log.md`。

## D-013 同步试运行边界

- GitHub 是正式提交状态、版本历史、备份和跨环境访问层；不是唯一可工作的地方。
- 本地 `docs/project_control/` 是日常 working copy，需与 `main` 保持同步。
- Project Control 不记录密码、Token、个人敏感资料或不应上云的信息。
- ChatGPT 与 Codex 不并行修改同一控制文件；本地工程工作开始前先 pull。
- 该同步方式为 TRIAL，可根据实际收益重新评估。

## D-014 P0 Closure Carry-forward

- P0 的技术目标已经完成，不再继续扩大 P0 范围。
- P0.2 的 Class B 限制继续生效：需回到 Local Blender 3.6 维护的核心资产，不得默认依赖未经验证的 Blender 4.5-only 功能。
- P0.3 的结论是“结构化参数 → 脚本 → 可重复最小结构模型”可行；历史取证、证据分层、正式古建参数体系和构造精度属于 P1 及后续 Phase。
- P1 启动时不自动创建 Codex T-###；只有出现实际工程执行任务时再编号。

## D-015 P1 Gate Boundary

- P1.0 负责锁定筛选逻辑，不直接决定最终对象。
- P1.1 必须使用统一标准比较 3–5 个候选，并由 Product Owner 明确定选。
- P1.2 只记录可追溯证据；无来源的信息不得进入“已证实”。
- P1.3 必须显式区分“已证实 / 高可信推断 / 合理补全 / 未知”，并形成进入正式参数化与 3D 复原的 Go / No-Go 结论。

## D-016 P1.0 Locked Scoring Rule

- 评分仅用于首案选择，不等同于建筑本身的历史价值排序。
- 五项权重在当前 P1.1 中保持固定，避免“先看到喜欢的对象再调整评分规则”。
- “历史状态歧义程度”单独计分；资料多不能自动抵消大修、后世改建或原状不确定性。
- 候选评分必须说明依据与不确定性，不使用无法追溯来源的精确分值作为事实。

## D-017 First Formal Case Boundary

- 正式对象固定为：**山西平遥镇国寺万佛殿**。
- P1.2 的任务不是“证明它一定能够复原”，而是建立证据包并暴露证据缺口。
- P1.2 中任何尺寸、构造、年代、修缮史或图像判断必须附来源；来源不足时只能标记为待核实或未知。
- 在 P1.3 形成 Go 结论以前，不因“已经定选”而提前进入正式参数化或 3D 生产。
