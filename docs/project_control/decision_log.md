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
| D-017 | 2026-09-11 | Product Owner 批准“山西平遥镇国寺万佛殿”为首个正式复原案例。P1.1 正式 PASS；P1.2 解锁并启动。四候选按 P1.0 锁定权重比较后，镇国寺万佛殿获得最高首案适配度。该选择只代表项目首案适配性，不构成对四座建筑历史价值的排序。正式 3D 生产继续受 P1.3 Gate 约束。 | ACTIVE / CASE LOCKED / P1.1 PASS / P1.2 STARTED |
| D-018 | 2026-09-11 | Product Owner 批准 P1.2｜正式证据包建立通过。完整《精细测绘报告》已纳入主来源并完成关键原页直接核读；参数候选矩阵升级为 V002；P1.2 Gate Review 10/10 PASS。P1.2 正式 PASS，P1 Gate 进度变为 3/4；P1.3 解锁进入证据分级与可复原性 Go / No-Go。 | ACTIVE / P1.2 PASS / P1.3 ENTERED |
| D-019 | 2026-09-12 | Product Owner 正式批准 `P1.3｜CONDITIONAL GO`。P1.3 PASS，P1 Gate = 4/4 PASS，P1｜选题取证正式关闭。项目允许进入正式参数化与3D候选复原，但 CG-01～CG-06 全部成为跨阶段强制生产规则。P2 第一项强制 Gate 为 `P2.0｜Evidence-aware Parameter Schema`；P2.0 PASS 前不得启动第一项正式 Blender 几何生产。 | ACTIVE / P1 CLOSED / P2 ENTRY / CONDITIONAL GO |
| D-020 | 2026-09-12 | Product Owner 正式批准 `P2.0｜Evidence-aware Parameter Schema` PASS。T-005 V001/V002 完成并验证 Schema、UNKNOWN/DO_NOT_LOCK 机械约束、REASONABLE_COMPLETION 可替换约束及三层语义并存；P2.0 Gate Review 7/7 PASS。CG-01 前置条件正式满足。P2 后续工作可继续，但在创建第一项正式几何任务前，必须先定义并锁定 P2.1–P2.3 Gate 架构；CG-02～CG-06 继续强制生效。 | ACTIVE / P2.0 PASS / NEXT GATE ARCHITECTURE REQUIRED |
| D-021 | 2026-09-12 | Product Owner 批准 `P2.1–P2.3 Gate Architecture V001`。P2.1=`正式生产参数集锁定｜Formal Production Parameter Set`；P2.2=`参数化主体结构候选模型｜Parametric Structural Skeleton`；P2.3=`整合复原候选与质量验收｜Integrated Reconstruction Candidate & QC`。生产路径正式锁定为“参数 → 结构 → 整合候选与QC”。P2.1 不生成正式 Blender 几何；P2.1 PASS 后方可进入 P2.2 第一项正式几何生产。CG-02～CG-06 持续强制生效。 | ACTIVE / P2 GATE ARCHITECTURE LOCKED / P2.1 ENTRY READY |
| D-022 | 2026-09-12 | Product Owner 要求并批准锁定 `P2.1 Definition of Done V001`。P2.1 必须完成85/85参数迁移、证据语义保持、Schema机器验证、UNKNOWN几何阻断判定、Geometry Dependency Matrix、REASONABLE_COMPLETION可替换性、三层语义与构件原真性边界、机器preflight、版本锁定与canonical archive共9项。P2.1 PASS除9/9外还要求 `geometry-critical unresolved blocker = 0`；UNKNOWN若是P2.2必须输入，不得跳过或静默补值，只能由新证据解决或经Product Owner显式批准新的可替换REASONABLE_COMPLETION。 | ACTIVE / P2.1 DOD LOCKED |
| **D-023** | **2026-09-12** | **Product Owner 批准 `Z-006-RC-01` 作为解除 P2.2 柱高生产阻断的独立、可替换 REASONABLE_COMPLETION。Z-006 本体继续保持 `UNKNOWN / null / DO_NOT_LOCK`，不得改写为历史事实；RC-01 采用规则 `11 × MOD-006`，当前 MOD-006≈321.3mm 时解析值为 3534.3mm，仅作为 `reconstructed_963_candidate` 的生产候选。RC-01 必须独立于85项正式历史/证据参数保存并可追溯到本决策；若 MOD-006 或后续证据变化，候选必须可重新计算或替换。继续同一工程任务 T-006 V002 验证，不创建 T-007。** | **ACTIVE / Z-006 RC-01 APPROVED / T-006 V002 AUTHORIZED** |

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

## D-018 P1.2 Approval Boundary

- P1.2 的 PASS 表示“正式证据包已完整建立并具备可追溯性”，**不表示所有参数均已达到历史事实级确定性**。
- `P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md` 是 P1.3 的主输入，不是正式 Blender 生产参数。
- `DIRECT_VERIFIED` 只表示已直接核读主报告原页；若原报告本身属于推算、猜测或理想模型，该字段仍必须在 P1.3 按相应不确定性等级处理。
- P1.3 在形成 Go 结论以前，正式 3D 生产继续禁止启动。

## D-019 P1.3 Conditional Go Approval Boundary

- P1.3 PASS 的含义是：证据足以支持**受控的963候选复原**，不是“所有963历史参数已经确定”。
- CG-01：第一项正式几何生产前必须建立 Evidence-aware Parameter Schema。
- CG-02：UNKNOWN / DO_NOT_LOCK 不得静默硬编码；需要临时值时必须新增显式 REASONABLE_COMPLETION 决策。
- CG-03：REASONABLE_COMPLETION 必须独立参数化、可替换、可追踪。
- CG-04：`observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 三层长期分离。
- CG-05：转角45°精确节点、榫卯落位、隐衬角栿/隐角梁等未解决项只能进入中等LOD拓扑骨架，不得宣称历史精确复原。
- CG-06：逐构件原真性不足时，禁止“完全还原963原貌 / 全部963原构”的过度真实性声明。
- P2.0 是 CONDITIONAL GO 的第一项强制前置 Gate；在其 PASS 前不得创建第一项正式 Blender 几何生产任务。

## D-020 P2.0 Approval Boundary

- P2.0 PASS 表示 Evidence-aware Parameter Schema 已经成为正式生产数据合同，CG-01 已满足。
- P2.0 PASS 不表示所有85项参数均已 production-locked，也不改变其 P1 分类与时间层。
- UNKNOWN 继续受 `DO_NOT_LOCK` 约束；REASONABLE_COMPLETION 继续保持可替换与可追踪。
- `observed_as_measured` / `report_ideal_model` / `reconstructed_963_candidate` 三层继续强制隔离。
- CG-02～CG-06 全部继续生效。
- 下一步先定义并锁定 P2.1–P2.3 Gate 架构，再创建后续正式几何工程 T-###；不得因为 P2.0 PASS 而跳过 Gate 设计直接进入 Blender 正式建模。

## D-021 P2.1–P2.3 Gate Architecture Boundary

- P2.1｜正式生产参数集锁定：把 P1 已分类信息转成可供生产读取的正式参数集；处理 UNKNOWN 对建模的真实阻断关系；不得生成正式 Blender 几何。
- P2.2｜参数化主体结构候选模型：第一项正式 Blender 几何 Gate；验证参数驱动的柱网、柱、主要梁架、斗栱拓扑骨架、屋顶控制几何与主要空间关系。
- P2.3｜整合复原候选与质量验收：整合结构、屋面、斗栱体系与证据 metadata，完成可追溯性、确定性重建、兼容性与视觉 QC，形成正式963候选复原模型。
- P2.2 对转角45°精确节点、榫卯与隐角梁争议只允许中等LOD拓扑骨架，继续执行 CG-05。
- P2.3 PASS 表示“工程可复现、证据可追溯、不确定性透明的963候选复原模型成立”，不等于“完全还原963年原貌”。
- 下一步先明确并锁定 P2.1 Definition of Done，再创建 T-006；未经 P2.1 PASS，不进入 P2.2 正式几何生产。

## D-022 P2.1 Definition of Done Boundary

- P2.1 DoD 正式文件：`docs/production/zhenguo_wanfo/P2_1_DEFINITION_OF_DONE_V001.md`。
- PASS 必须满足 DoD-01～DoD-09 全部通过；任何一项未通过即 HOLD。
- 85项参数必须全部迁移或以明确 metadata/rule representation 保留，不能只保留直接建模参数。
- Geometry Dependency Matrix 是生产依赖分类，不改变历史证据 classification。
- UNKNOWN 必须明确判断其是否阻断 P2.2；geometry-critical UNKNOWN 未解除时 P2.1 不得 PASS。
- 若需要临时值解除 geometry blocker，必须由 Product Owner 显式批准新的 REASONABLE_COMPLETION；禁止静默赋值。
- HIS-002 的逐构件原真性边界继续进入后续 geometry metadata；无证据时 `originality_status` 默认 `unknown`。
- P2.1 允许执行纯数据、脚本、preflight 与验证；不生成正式 Blender 几何。
- DoD 锁定后下一步可定义 T-006；T-006 本身不因 DoD 锁定而自动创建或启动。

## D-023 Z-006 Replaceable Candidate Boundary

- `Z-006 / column_height_963_design_mm` **继续保持 UNKNOWN / null / DO_NOT_LOCK**；D-023 不改变其历史证据分类。
- `Z-006-RC-01` 是独立生产候选，不得覆盖或替换 Z-006 本体记录。
- 候选规则固定为 `11 × MOD-006`；当前 `MOD-006 ≈ 321.3mm` 时解析值为 **3534.3mm**。
- `Z-006-RC-01` 的 classification = `REASONABLE_COMPLETION`，time layer = `reconstructed_963_candidate`，必须 `is_replaceable=true`。
- 3534.3mm 仅表示当前参数基线下的生产解析值，不得描述成“963年柱高已证实为3534.3mm”。
- 若 MOD-006 更新，RC-01 应按公式重新计算；若获得更强柱高证据，可直接替换/撤销 RC-01，而不改写历史记录。
- T-006 V002 必须机械验证：Z-006仍未知、RC-01独立存在且获D-023批准、公式可重算、preflight的 `geometry-critical unresolved blocker count` 才可降为0。
- 在 T-006 V002 validation / preflight PASS 前，P2.1 仍不得宣布 PASS，P2.2 继续 LOCKED。
