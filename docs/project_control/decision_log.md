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
| D-023 | 2026-09-12 | Product Owner 批准 `Z-006-RC-01` 作为解除 P2.2 柱高生产阻断的独立、可替换 REASONABLE_COMPLETION。Z-006 本体继续保持 `UNKNOWN / null / DO_NOT_LOCK`，不得改写为历史事实；RC-01 采用规则 `11 × MOD-006`，当前 MOD-006≈321.3mm 时解析值为 3534.3mm，仅作为 `reconstructed_963_candidate` 的生产候选。RC-01 必须独立于85项正式历史/证据参数保存并可追溯到本决策；若 MOD-006 或后续证据变化，候选必须可重新计算或替换。继续同一工程任务 T-006 V002 验证，不创建 T-007。 | ACTIVE / Z-006 RC-01 APPROVED / T-006 V002 AUTHORIZED |
| D-024 | 2026-09-12 | Product Owner 正式批准 `P2.1｜Formal Production Parameter Set` PASS。Gate Review 9/9 PASS，T-006 V002 machine validation / 21/21 tests / production preflight 全部 PASS，`geometry-critical unresolved blocker = 0`。P2.1 正式 CLOSED；P2.2 `Parametric Structural Skeleton` 解锁为当前 Gate。P2.1 PASS 不改变 Z-006 的历史 UNKNOWN 状态；Z-006-RC-01 继续作为独立、可替换的生产候选。第一项正式 Blender 几何任务创建前，必须先明确并锁定 P2.2 Definition of Done。 | ACTIVE / P2.1 PASS / P2.2 ENTERED / DOD DEFINITION REQUIRED |
| D-025 | 2026-09-12 | Product Owner 正式批准并锁定 `P2.2 Definition of Done V001`。P2.2 作为第一项正式 Blender 历史候选几何 Gate，必须以 P2.1 正式参数集 + approved override + Geometry Dependency Matrix 为唯一历史/复原输入；DoD 9项覆盖 build manifest、完整主体六大范围、参数驱动与禁止 naked historical constants、机器几何验证、RC可替换、UNKNOWN/转角/原真性边界、geometry metadata traceability、deterministic rebuild + independent reopen + 人工结构审核、以及 canonical archive。P2.2 PASS 需要 9/9、完整主体、machine validation PASS、deterministic rebuild PASS、无未批准 geometry-critical input、无历史尺寸裸常量，并由 Product Owner 完成人工结构审核批准。T-007 可据此启动。 | ACTIVE / P2.2 DOD LOCKED / T-007 AUTHORIZED |
| D-026 | 2026-09-12 | Product Owner 正式批准 `P2.2｜Parametric Structural Skeleton` PASS。T-007 V001 完成 6/6 主体结构范围，machine geometry validation PASS、32/32 tests PASS、naked historical constant scan PASS、deterministic rebuild PASS、independent reopen PASS；PLAN / ELEVATION / AXON 三张结构审核图完成直接人工审核并通过。P2.2 DoD 9/9 PASS，P2.2 正式 CLOSED；P2.3 `Integrated Reconstruction Candidate & QC` 解锁为当前 Gate。P2.2 PASS 只确认中等LOD参数化主体骨架工程成立，不把217个Blender对象等同于217个历史构件，也不解除Z-006、DG-114、HIS-002及转角/榫卯/隐角梁等证据边界。P2.3第一项工程任务前必须先明确并锁定P2.3 Definition of Done。 | ACTIVE / P2.2 PASS / CLOSED / P2.3 ENTERED / DOD REQUIRED |
| D-027 | 2026-09-12 | Product Owner 正式批准并锁定 `P2.3 Definition of Done V001`。P2.3 作为 P2 最终 Gate，必须把 P2.2 approved structural baseline 升级为构件库驱动的整合复原候选，采用 `Component Library → Parametric Variant → Placement / Instance → Evidence Metadata` 架构；DoD 9项覆盖 Integration Manifest、构件族/variant/instance、完整整合几何、evidence metadata、参数驱动与可替换性、machine QC、deterministic rebuild + Local3.6↔Cloud4.5 roundtrip、六类视觉/evidence diagnostic 审核以及最终 P2 closure archive。CG-02～CG-06 持续强制生效；P2.3 PASS 不等于完全还原963原貌。T-008 获授权启动。 | ACTIVE / P2.3 DOD LOCKED / T-008 AUTHORIZED |
| D-028 | 2026-09-12 | Product Owner 正式批准 `P2.3｜PASS`。T-008 V001–V004 完成构件库驱动整合候选、33/33 tests、34/34 machine QC、Local3.6→Cloud4.5→Local3.6 roundtrip、六类视觉审核与修正版 Evidence Diagnostic；P2.3 DoD 9/9 PASS，P2 四个 Gate 4/4 PASS，P2 正式 CLOSED。同时批准 Evidence Visualization 双层 carry-forward：Risk Map 保留最高不确定性优先的 Conservative Risk Map；后续整寺级最终证据展示新增 Evidence Composition Map，按属性/子构件表达 CONFIRMED/HCI/RC/UNKNOWN 组成，正常建筑展示与证据着色分离。 | ACTIVE / P2.3 PASS / P2 CLOSED / EVIDENCE VISUALIZATION CARRY-FORWARD LOCKED |
| D-029 | 2026-09-13 | Product Owner 批准将 P3 定义为 `古建筑构件系统化与组合建模｜Component System & Assembly Architecture`，目标从“继续提高整栋模型精度”调整为“建立可登记、可解释、可复用、可组合的古建筑构件系统”。P3 Gate 架构锁定为：P3.0=`Component Ontology & Registry`；P3.1=`Component Master & Variant Library`；P3.2=`Assembly Relationship Model`；P3.3=`Component-driven Building Reconstruction`。P2 不重做，冻结为工程基线；P3.0 首先审计并迁移 P2 的 11 families / 40 variants / 365 instances，区分真实历史构件与工程 control/proxy/envelope。P3.0 DoD 批准前不得创建 T-009 或新增几何。 | ACTIVE / P3 ENTERED / P3.0 ENTERED / DOD REQUIRED |

## D-012 直接影响

- 正式事实不再写进 Dashboard 的历史档案区。
- Dashboard 可以删除并重新生成，不影响项目正式记录。
- 当前状态写入 `project_state.json`。
- 重大决策写入 `decision_log.md`。
- Codex 执行事实写入 `execution_log.md`。
- Gate / 验收结论写入 `acceptance_matrix.md`。
- 项目治理规则写入 `governance.md`；规则变化同时记录到 `rules_change_log.md`。
