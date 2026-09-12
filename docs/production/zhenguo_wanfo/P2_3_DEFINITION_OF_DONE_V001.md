# P2.3｜整合复原候选与质量验收｜Definition of Done V001

Status: **LOCKED / PRODUCT OWNER APPROVED**  
Date: 2026-09-12  
Gate: `P2.3｜整合复原候选与质量验收｜Integrated Reconstruction Candidate & QC`

## 1. Gate Goal

在 P2.1 已批准的正式生产参数基线与 P2.2 已批准的中等 LOD 主体结构基线之上，形成万佛殿第一版**完整、可维护、可重复重建、证据边界透明的整合复原候选模型**，并完成最终 P2 工程质量验收。

P2.3 的目标不是把所有未知问题“补成确定答案”，而是证明：

- P2.2 的主体结构能够被稳定升级为可理解为完整建筑候选的整合模型；
- 重复构件采用可维护的“构件族 / 参数化变体 / 放置实例”架构，而不是逐件手工复制后独立漂移；
- 斗栱、梁架、屋顶及主要外部轮廓能够在现有证据边界内形成连贯系统；
- P2.1 / P2.2 的 evidence metadata、UNKNOWN、REASONABLE_COMPLETION 与历史真实性边界在整合后仍然存在；
- 同一正式输入可以从干净基线确定性重建同一整合结果；
- Local Blender 3.6 与既有 Cloud Blender 4.5 路线对最终候选的核心几何与 metadata 兼容性得到实际 QC；
- Product Owner 能通过正式审核图判断该候选是否已达到“受控的 963 候选复原模型”标准。

P2.3 PASS 后，表示 P2｜正式参数化与3D复原 的首案工程目标完成；其含义仍是“证据可追溯、不确定性透明的 963 候选复原”，不是“完全还原 963 年原貌”。

## 2. Authoritative Inputs

P2.3 正式生产只能使用以下输入链：

1. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
2. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
3. `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
4. P2.0 Evidence-aware Parameter Schema 与正式读取规则
5. P2.2 approved structural baseline：`P2_2_STRUCTURAL_SKELETON_V001`
6. `production/zhenguo_wanfo/build/P2_2_BUILD_MANIFEST_V001.json`
7. P2.2 Gate Review、D-026 及 CG-02～CG-06 所形成的边界
8. P1 已批准 evidence package，仅作为可追溯 evidence / validation reference 使用

任何新增历史几何输入、外部资料值或经验尺寸，若要进入正式 P2.3 几何，必须先完成 evidence classification，并在需要时取得 Product Owner 显式批准；不得在 Blender 中直接“看着像”地补值。

## 3. Non-goals

P2.3 不要求：

- 解决所有 45° 转角榫卯、隐衬角栿 / 隐角梁争议；
- 证明每一构件的 963 年原真性；
- 将 `Z-006-RC-01` 升级为已证实历史柱高；
- 为 `DG-114` 创造并不存在的统一小斗历史规格；
- 逐瓦、逐钉、逐榫完成考古级微观建模，除非正式证据已足够且确有必要；
- 模拟全部现状变形、沉降、挠曲、风化与历代修缮痕迹；
- 完成最终影视级材质、纹理、灯光、环境与艺术化展示渲染；
- 宣布“完全还原 963 年原貌”或“全部构件均为 963 原构”。

P2.3 允许使用中性材质、系统色或 evidence diagnostic 色用于审核，但视觉美术精修不作为本 Gate 的主要目标。

## 4. Definition of Done｜9项

### DoD-01｜正式整合输入合同与 Integration Manifest

每次正式 P2.3 构建必须生成机器可读的 integration/build manifest，至少记录：

- P2.1 formal parameter / override / dependency / schema 的版本与 hash；
- P2.2 approved structural baseline 的 generation script / manifest / canonical commit / local `.blend` hash；
- P2.3 component library / generator / integration script 的版本与 commit；
- 实际启用的 REASONABLE_COMPLETION / override；
- bounded UNKNOWN / placeholder / unresolved authenticity items；
- 构件族、变体、实例数量与映射；
- 最终候选输出 hash、Blender 版本与 QC 环境。

禁止存在 manifest 外的正式历史几何输入或无法解释来源的手工修模结果。

### DoD-02｜构件库 / 参数化变体 / 实例架构成立

P2.3 必须正式采用以下生产架构：

> **Component Library → Parametric Variant → Placement / Instance → Evidence Metadata**

要求：

- 同一种几何逻辑的重复构件必须来自统一构件族或统一生成规则；
- 有尺寸 / 构造差异时建立命名明确的 parameterized variant，不得靠复制后逐个手改；
- 相同几何应优先共享 prototype / mesh data / generation rule，再按位置实例化或批量生成；
- 每个 placement / instance 仍必须拥有稳定 ID、位置关系与可追溯 metadata；
- 若某一构件确实需要独立几何，必须登记为 explicit unique variant，并说明差异依据；
- 禁止出现“同一构件族复制几十份后各自不可追溯地漂移”的生产方式。

该架构必须至少覆盖 P2.3 中实际重复出现的主要柱、梁架、斗栱、檩 / 椽或其他重复构件族；不要求人为把本来不同的构件强行合并为同一原型。

### DoD-03｜完整整合候选几何成立

正式候选必须从 P2.2 的“结构控制骨架”升级为可理解为完整建筑系统的整合模型，至少满足：

1. P2.2 已批准柱网、柱、主要梁架关系继续成立；
2. 斗栱从纯出跳控制段升级为**构件族驱动的可读几何体系**，精度不得超过 evidence boundary；
3. 屋顶从控制线 / 控制杆升级为连贯的**屋面 / 屋顶包络与主要屋面构造关系**；
4. 脊、檐、山面和主体木构之间形成空间连续的建筑整体；
5. P2.2 的 diagnostic grid / control-only geometry 必须与正式展示几何分层管理，不能误当成最终历史构件；
6. 对证据不足的围护、门窗、装饰或小构件，不得为了“画面看起来完整”而无依据补成历史事实；可明确省略、保留 bounded placeholder 或作为后续工作项。

P2.3 Gate 以“整体建筑候选成立”为目标，不接受仍然只有 P2.2 线框 / 控制骨架的状态。

### DoD-04｜Evidence Metadata 与历史声明边界贯穿整合模型

P2.3 不得因为模型更完整而丢失 P2.1 / P2.2 的证据语义。

主要构件族、variant 或 instance 必须能够直接或经 manifest 唯一映射到：

- `historical_state_tag`
- `classification / evidence_class`
- `time_layer`
- `source_layer`
- `originality_status`
- `parameter_ids / source parameter IDs`
- `REASONABLE_COMPLETION / override IDs`
- bounded UNKNOWN / placeholder 状态

强制边界：

- `Z-006` 继续 `UNKNOWN / null / DO_NOT_LOCK`；
- `Z-006-RC-01` 继续只是 D-023 批准的可替换生产候选；
- `DG-114` 不得被整合模型反向解释为“统一小斗规格已知”；
- `HIS-002` 继续约束逐构件原真性声明；
- 45° 转角、榫卯、隐角梁等争议项不得因视觉完成度提高而自动升级为历史精确结论。

### DoD-05｜参数驱动、可替换与禁止不可追溯手工漂移

正式 P2.3 候选必须能由批准输入和版本化构件规则重新生成。

要求：

- 影响正式历史 / 复原几何的尺寸不得以 naked historical constants 存在；
- P2.1 的 REASONABLE_COMPLETION 与 approved override 继续保持 `is_replaceable=true`；
- 修改 RC / variant 参数后，相关实例必须通过重建自动响应；
- 不允许依赖“生成后再手工挪一点 / 拉一点 / 修一点”才能得到正式 PASS 的核心几何；
- 若使用人工制作的 canonical prototype mesh，其来源、版本、hash、适用构件族与 evidence boundary 必须进入 manifest，且实例不得随后产生未登记的局部漂移。

至少要有 mutation / replacement test 证明一个已批准 RC 或主要 component variant 的改变能够传导到最终整合模型。

### DoD-06｜整合模型 Machine QC

必须建立自动化 QC，至少检查：

- required component families / variants / instance counts 与 manifest 一致；
- stable ID / naming 无意外 Blender `.001/.002` 漂移；
- 主要构件没有 NaN、零尺度、异常变换或丢失引用；
- 柱—梁架—斗栱—屋顶的主要空间链条连续；
- 不存在明显的整族漂浮、脱离、镜像错误、重复放置或错误轴向；
- P2.2 关键尺寸 / topology 控制没有被 P2.3 意外破坏；
- final presentation collection 不意外包含仅供诊断的 grid / control-only geometry；
- evidence metadata / override mapping 没有在 instancing / duplication 中丢失。

木构中合理的穿插、搭接或未显式建模榫卯不得被简单 collision scan 误判为 FAIL；QC 应针对“错误放置 / 断链 / 重复 / 丢失”而不是强制零相交。

### DoD-07｜确定性重建 + Local/Cloud Compatibility QC

P2.3 必须完成最终候选的技术可重复性和既有版本路线 QC：

- 从干净基线连续两次执行正式 integration build；
- 对象 / instance 集合、稳定 ID、family counts、关键尺寸、component variant mapping、metadata summary 与 validation summary 一致；
- 独立保存 / 重开 PASS；
- 执行一次正式 **Local Blender 3.6 → Cloud Blender 4.5 → Local Blender 3.6** 往返 QC；
- P0.2 已知 Class B UI-region 限制可以继续存在，但不得造成 P2.3 核心几何、构件映射、evidence metadata、正式相机或必要审核资产丢失；
- 若 roundtrip 出现新的核心兼容性损失，P2.3 必须 HOLD，不能仅以 P0 旧结论豁免。

`.blend` 二进制序列化不要求 byte-identical；确定性比较以声明的结构 / 实例 / 参数 / metadata 语义结果为准。

### DoD-08｜视觉 QC、Evidence Diagnostic 与 Product Owner 审核

P2.3 必须输出足够判断“整合候选是否成立”的正式审核图，至少包括：

1. 平面 / PLAN；
2. 正立面或侧立面 / ELEVATION；
3. 轴测 / AXON；
4. 一张能读出完整建筑整体的外部三分之四视角；
5. 一张能检查斗栱—梁架—屋顶整合关系的仰视、剖切或局部结构视图；
6. 一张 evidence diagnostic 视图或等价可视化，用于区分 confirmed / inference / reasonable completion / unknown-placeholder 边界。

审核重点：

- 整体比例与空间连续性；
- 重复构件是否出现明显方向 / 尺度 / 放置错误；
- 斗栱、梁架、屋顶是否作为一个系统成立；
- P2.2 diagnostic placeholder 是否被错误包装成最终历史构件；
- evidence diagnostic 是否与 manifest / metadata 一致；
- 是否出现超出证据的“视觉补全”。

Product Owner 必须完成视觉审核并明确批准后，P2.3 才可 PASS。

### DoD-09｜最终候选归档、限制清单与 P2 Closure Evidence

P2.3 Gate Review 前必须正式归档：

- component library / prototype / variant 定义；
- integration generation script；
- integration/build manifest；
- machine QC / tests；
- deterministic rebuild evidence；
- Local 3.6 ↔ Cloud 4.5 roundtrip QC evidence；
- P2.3 validation report；
- 正式审核图 / evidence diagnostic；
- local-only 最终 `.blend` 路径、SHA256、文件大小与 Blender 版本；
- canonical Git commit；
- `KNOWN_LIMITATIONS / UNRESOLVED_EVIDENCE_BOUNDARIES` 清单；
- 一段正式可复用的历史声明边界，明确该成果是“受控的 963 候选复原”，不是“完全还原 963 原貌”。

`.blend / .blend1` 继续 local-only；GitHub 保存可重建脚本、component definitions、manifest、tests、validation、QC 与审核证据。

## 5. Gate Decision Rule

### PASS

只有同时满足以下条件才可建议 P2.3 PASS：

- DoD-01～DoD-09：**9 / 9 PASS**；
- component library / variant / instance 架构通过审核；
- 完整整合候选几何成立；
- machine QC PASS；
- deterministic rebuild PASS；
- independent reopen PASS；
- Local 3.6 ↔ Cloud 4.5 ↔ Local 3.6 roundtrip 核心几何与 metadata PASS；
- 无未批准 geometry-critical input；
- 无 naked historical constants 或不可追溯核心手工修模；
- UNKNOWN / RC / authenticity boundary 无静默升级；
- Product Owner 完成视觉 / evidence diagnostic 审核并明确批准。

### HOLD

出现以下任一情况即 HOLD：

- 仍停留在 P2.2 控制骨架，未形成整合建筑候选；
- 同类构件大量复制后各自手工漂移，无法由构件族 / variant 规则重建；
- final geometry 依赖 manifest 外的历史尺寸或未登记人工修改；
- RC / override 被烘焙，替换后不能自动传播；
- component instance metadata 在复制 / instancing 后丢失；
- 主要构件族缺失、整族错位、断链或重复放置；
- P2.3 破坏 P2.2 已批准的关键结构关系；
- UNKNOWN / placeholder 被包装成已确认历史构造；
- deterministic rebuild / independent reopen 失败；
- Local/Cloud roundtrip 出现新的核心几何或 metadata 损失；
- 视觉审核发现明显结构/实例错误或无证据补全；
- validation / limitations / canonical archive 不完整。

## 6. P2.3 Production Boundary

P2.3 是 P2｜正式参数化与3D复原 的最后一个 Gate。

允许：

- 将 P2.2 控制骨架升级为整合建筑候选；
- 建立和使用正式构件库 / variants / instances；
- 在 evidence-supported LOD 内细化斗栱、主要木构与屋面；
- 使用中性材质 / system color / evidence color 辅助 QC；
- 执行最终 P2 engineering QC、roundtrip 和人工审核。

不允许：

- 为追求“像古建筑”而引入未审批历史尺寸；
- 用视觉完整性覆盖 evidence uncertainty；
- 把 P2.3 PASS 描述成所有历史细节均已解决；
- 在 Gate PASS 前进入与首案工程验收无关的大规模艺术化渲染、动画或场景扩建。

## 7. First Engineering Task

本 DoD 已由 Product Owner 批准并锁定。下一项实际工程任务为 **T-008**：

> **【中国古建筑3D复原｜T-008｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001｜构件库驱动整合复原候选与最终P2质量验收】**

优先顺序：

1. 建立 Component Library / Variant / Instance 数据合同；
2. 在不破坏 P2.2 approved baseline 的前提下整合斗栱、梁架与屋顶生产几何；
3. 建立 P2.3 machine QC / manifest；
4. 完成 replacement / deterministic rebuild / reopen；
5. 完成 Local 3.6 ↔ Cloud 4.5 ↔ Local 3.6 roundtrip QC；
6. 输出正式视觉 / evidence diagnostic 审核证据。

T-008 Engineering PASS **不等于 P2.3 Gate PASS**；最终 Gate Review 仍需 ChatGPT 独立复核以及 Product Owner 明确批准。