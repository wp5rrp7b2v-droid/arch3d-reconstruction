# 【中国古建筑3D复原｜T-008｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001｜构件库驱动整合复原候选与最终P2质量验收】

Status: **READY_FOR_LOCAL_EXECUTION**  
Think Level: **HIGH**  
Phase/Gate: P2 / P2.3  
Date: 2026-09-12

## 1. Objective

在已批准的 P2.1 正式生产参数与 P2.2 中等 LOD Structural Skeleton Baseline 之上，建立第一版完整、可维护、可重复重建、证据边界透明的 Integrated Reconstruction Candidate，并形成 P2.3 所需的工程验收证据。

本任务重点不是“把模型做得最精细”，而是把已经成立的参数化主体骨架升级为一个**构件库驱动、实例可追溯、整合几何连贯、可机器 QC、可跨版本往返、可供 Product Owner 审核**的正式 963 候选复原模型。

## 2. Authoritative Inputs

只允许使用：

1. `docs/production/zhenguo_wanfo/P2_3_DEFINITION_OF_DONE_V001.md`
2. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
3. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
4. `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
5. `production/zhenguo_wanfo/schema/evidence_aware_parameter_schema_v001.json`
6. `production/zhenguo_wanfo/build/P2_2_BUILD_MANIFEST_V001.json`
7. `production/zhenguo_wanfo/scripts/generate_p2_2_structural_skeleton_v001.py`
8. P2.2 approved local baseline：`production/zhenguo_wanfo/output/P2_2_STRUCTURAL_SKELETON_V001.blend`
9. P2.2 Gate Review、D-023～D-027 与 CG-02～CG-06 边界
10. P1 approved evidence package，仅作为 evidence / validation reference

未经显式批准，不得把外部资料值、经验尺寸、视觉估计或手工 Blender 数值作为新的正式历史几何输入。

## 3. Scope

T-008 必须完成以下正式工程范围：

- 建立 Component Library / Parametric Variant / Placement-Instance 数据合同；
- 保持 P2.2 已批准柱网、柱、主要梁架和屋顶控制关系；
- 将主要重复构件纳入构件族 / variant / instance 架构；
- 将斗栱从 P2.2 出跳控制骨架升级为 evidence-bounded、可读的构件族几何体系；
- 将屋顶控制线升级为连贯屋面 / 屋顶包络及主要屋面构造关系；
- 建立完整 Integration Manifest；
- 建立 P2.3 Machine QC；
- 完成 replacement / mutation、deterministic rebuild、independent reopen；
- 完成 Local Blender 3.6 → Cloud Blender 4.5 → Local Blender 3.6 roundtrip QC；
- 输出至少六类正式审核图，包括 evidence diagnostic；
- 归档 known limitations / unresolved evidence boundaries。

T-008 不要求：

- 逐瓦、逐榫、逐钉考古级微观建模；
- 解决全部 45° 转角榫卯与隐角梁争议；
- 证明逐构件 963 原真性；
- 最终影视级材质、灯光、环境或艺术渲染；
- 宣布“完全还原 963 年原貌”。

## 4. Required Production Architecture

正式采用：

> **Component Library → Parametric Variant → Placement / Instance → Evidence Metadata**

### A. Component Library

对 P2.3 中实际重复出现的主要构件族建立统一 prototype / generator definition。至少覆盖实际进入最终候选的主要：

- columns；
- primary frame member families；
- bracket-set / bracket-member families；
- purlin / rafter / roof-related repeated families（若进入本版本正式几何）；
- 其他在最终候选中重复出现且适合统一生成的构件。

不得为了满足清单而把本来构造不同的构件强行合并。

### B. Parametric Variant

同族但尺寸、方向、构造角色不同的对象使用明确 variant：

- variant 必须拥有稳定 ID；
- variant 参数来源必须来自正式参数 / approved override / 明确派生规则；
- explicit unique variant 必须登记其差异理由；
- 禁止复制后逐件手工缩放、移动或拉伸形成不可追溯差异。

### C. Placement / Instance

每个 placement / instance 必须有：

- stable instance ID；
- family / variant ID；
- transform / placement data；
- evidence metadata 映射；
- parameter / override traceability；
- originality / historical state status。

允许共享 Blender mesh data 或用统一生成规则批量生成；但相同几何不得因复制而产生未登记的局部漂移。

### D. Presentation vs Diagnostic Separation

正式整合模型至少区分：

- final candidate / presentation geometry；
- diagnostic / control geometry；
- optional evidence diagnostic collections。

P2.2 的 grid / control-only objects 不得误进入 final presentation collection 并被当成历史构件。

## 5. Historical / Evidence Hard Boundaries

必须同时满足：

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK` 不变；
- `Z-006-RC-01 = 11 × MOD-006` 继续独立、可替换、D-023 traceable；
- 3534.3mm 不得被写回历史 Z-006；
- `DG-114` 不得因建出斗栱几何而升级为统一小斗历史规格；
- `HIS-002` 继续约束 component-level originality；无证据时默认 `originality_status=unknown`；
- 45° 转角、榫卯、隐角梁冲突只能在 evidence-supported LOD 下表达，不能伪装成精确历史解；
- observed / report ideal / reconstructed 963 candidate 三层不得混合覆盖；
- 任何新增历史几何输入必须先进入 evidence classification / approval 流程。

## 6. Integration Manifest

每次正式构建必须生成 machine-readable manifest，至少包含：

- P2.1 parameter / override / dependency / schema 路径、版本、SHA256；
- P2.2 approved baseline generation script / build manifest / canonical commit / local blend SHA256；
- P2.3 component definitions / generation / integration scripts 及 hashes；
- Blender / Python / QC environment；
- component families / variants / prototype mapping；
- placement / instance counts 与 stable IDs；
- actual formal parameter IDs / derived rules；
- enabled RC / overrides；
- bounded UNKNOWN / placeholder / authenticity limitations；
- diagnostic vs presentation collection mapping；
- final `.blend` path / SHA256 / size；
- review image paths；
- roundtrip artifact / validation paths。

不得存在 manifest 外的正式历史几何输入或未登记核心手工修模。

## 7. Integration Geometry Requirements

最终候选必须：

1. 保持 P2.2 已批准 3×3 bay / perimeter column / principal-frame 基线关系；
2. 柱、主要梁架、斗栱、屋顶作为一个空间连贯系统成立；
3. 斗栱不再只是抽象出跳条段，而形成可读的构件族 / variant 体系，但不得超过证据允许的精度；
4. 屋顶不再只是 control lines / rods，而形成连贯 roof envelope / roof surfaces / main roof relationships；
5. 脊、檐、山面与主体木构空间关系连续；
6. 诊断几何与正式候选几何分层；
7. 围护、门窗、装饰等证据不足项不得为了视觉完整性静默补成“历史事实”。

## 8. Machine QC

至少自动检查：

- required family / variant / instance coverage；
- family / variant / instance counts 与 manifest 一致；
- stable IDs 唯一；
- 无意外 Blender `.001/.002` 命名漂移作为正式接口；
- 无 NaN / zero-scale / invalid transforms / broken data references；
- prototype / shared mesh / generated-family mapping 完整；
- 柱—梁架—斗栱—屋顶主要结构链连续；
- 无整族 floating / detached / mirrored wrong / duplicated placement / wrong orientation；
- P2.2 key dimensions / topology regression PASS；
- presentation collection 不包含禁止的 diagnostic-only geometry；
- evidence metadata / parameter IDs / override IDs 在实例化后仍可追溯；
- historical / reconstructed dimensions 不以 naked historical constants 进入正式脚本。

不要把中国木构正常穿插、搭接或未显式建模榫卯简单当成 collision failure。

## 9. Replacement / Mutation Tests

至少证明：

- 一个 approved RC（优先 Z-006-RC-01 / MOD-006 链）改变后，最终整合模型的所有依赖实例自动重建响应；
- 至少一个主要 component variant 参数变化后，相应实例按规则变化且其他无关 family 不发生不可解释漂移；
- mutation 只用于 test-only 输入，不得改写正式 baseline；
- historical UNKNOWN 状态不得因 test 被改变。

## 10. Deterministic Rebuild / Independent Reopen

相同正式输入下至少连续两次从干净基线构建，并比较：

- family / variant / instance ID set；
- family / variant / instance counts；
- key dimensions；
- component mapping；
- metadata summary；
- evidence / override mapping；
- validation summary。

保存后至少两次独立 reopen，核心几何、实例映射和 metadata 必须 PASS。

`.blend` byte hash 可以不同；determinism 指结构和语义结果一致。

## 11. Local / Cloud Roundtrip QC

必须对最终候选执行一次正式：

> **Local Blender 3.6 → GitHub / GitHub Actions → Cloud Blender 4.5 → Artifact → Local Blender 3.6**

要求：

- 复用 P0.2 已验证路线，必要时可新增 P2.3 专用 workflow / validation script；
- cloud 端至少 reopen / validate / save；
- 返回 Local 3.6 后再次独立验证；
- 对比核心 geometry semantic summary、family/variant/instance mapping、evidence metadata、必要相机 / review assets；
- P0.2 已知 UI-region Class B 差异可接受；
- 新的核心几何 / metadata / instance mapping 损失 = HOLD。

Cloud / artifact 产物不得替代 local canonical working model；最终 `.blend` 继续 local-only。

## 12. Review Outputs

至少输出：

1. `PLAN`
2. `ELEVATION`
3. `AXON`
4. `EXTERIOR_3Q`
5. `STRUCTURE_DETAIL`（仰视 / 剖切 / 局部结构视图之一）
6. `EVIDENCE_DIAGNOSTIC`

建议路径：

- `production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_PLAN.png`
- `production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_ELEVATION.png`
- `production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_AXON.png`
- `production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_EXTERIOR_3Q.png`
- `production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_STRUCTURE_DETAIL.png`
- `production/zhenguo_wanfo/review/P2_3_INTEGRATED_RECONSTRUCTION_V001_EVIDENCE_DIAGNOSTIC.png`

审核图允许中性材质 / system colors / evidence diagnostic colors，不要求展示级艺术渲染。

## 13. Required Deliverables

至少建议形成：

- `production/zhenguo_wanfo/components/P2_3_COMPONENT_LIBRARY_V001.json` 或等价 machine-readable component contract；
- `production/zhenguo_wanfo/scripts/generate_p2_3_integrated_reconstruction_v001.py`；
- `production/zhenguo_wanfo/scripts/validate_p2_3_integrated_reconstruction_v001.py`；
- `production/zhenguo_wanfo/tests/test_p2_3_integrated_reconstruction_v001.py`；
- `production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`；
- `production/zhenguo_wanfo/validation/P2_3_MACHINE_VALIDATION_V001.json`；
- `production/zhenguo_wanfo/validation/P2_3_VALIDATION_REPORT_V001.md`；
- `production/zhenguo_wanfo/validation/P2_3_KNOWN_LIMITATIONS_V001.md`；
- Local/Cloud roundtrip workflow / validator / QC evidence；
- 六张正式 review PNG；
- local-only `.blend`：建议 `production/zhenguo_wanfo/output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend`。

`.blend / .blend1` 不提交普通 Git；manifest / validation report 必须记录路径、SHA256、文件大小与 Blender version。

## 14. Git / Safety Boundary

开始前必须：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git pull --ff-only origin main
```

只提交 T-008 scope 内的 component definitions、脚本、workflow、manifest、tests、validation、review PNG 等可追踪产物。

不得提交：

- 已知 local-only PDF；
- P0 local-only directories；
- `.blend / .blend1`；
- 无关未跟踪资产。

禁止 force-push。

如 GitHub Actions / network 暂时不可用，T-008 必须报告 HOLD 或“工程主体完成但 DoD-07 尚未满足”；不得省略 roundtrip 后自行宣告完整 PASS。

## 15. Acceptance / HOLD Logic

Engineering recommendation PASS 仅当：

- P2.3 DoD-01～DoD-09 均有对应工程证据；
- component library / variant / instance architecture 成立；
- integrated candidate geometry 成立；
- machine QC PASS；
- replacement / mutation PASS；
- deterministic rebuild PASS；
- independent reopen PASS；
- Local 3.6 → Cloud 4.5 → Local 3.6 core roundtrip PASS；
- no unapproved geometry-critical input；
- no naked historical constants / untracked core manual edits；
- evidence boundaries preserved；
- 六张 review outputs 已生成；
- canonical GitHub evidence archive complete。

否则返回 HOLD，并列出精确 blocker。

Engineering PASS **不等于 P2.3 Gate PASS**。最终 Gate Review / Product Owner approval 由 ChatGPT + Product Owner 完成。

## 16. Final Report

Codex 完成后必须返回：

- STATUS: PASS / HOLD
- Blender local version / Python version
- Cloud Blender version / workflow run result
- formal input hashes
- P2.2 approved baseline hash / manifest reference
- component library path / hash
- component family / variant / instance summary
- integration manifest path / hash
- final candidate object / instance summary
- Z-006 / Z-006-RC-01 boundary result
- machine QC result
- naked historical constant / manual drift scan result
- replacement / mutation test result
- deterministic rebuild result
- independent reopen result
- Local 3.6 → Cloud 4.5 → Local 3.6 roundtrip result
- review image paths (6 minimum)
- evidence diagnostic result
- local final `.blend` path / SHA256 / file size
- automated test result
- validation report path
- known limitations path
- Git commit SHA
- push result
- `git status --short`
- exact blocker if HOLD
- engineering recommendation

不得自行宣布 P2.3 Gate PASS 或 P2 Phase CLOSED。