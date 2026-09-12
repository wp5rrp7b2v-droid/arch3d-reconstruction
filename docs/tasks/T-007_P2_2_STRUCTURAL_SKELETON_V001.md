# 【中国古建筑3D复原｜T-007｜P2_2_STRUCTURAL_SKELETON_V001｜第一版正式主体结构候选模型】

Status: **READY_FOR_LOCAL_EXECUTION**  
Think Level: **HIGH**  
Phase/Gate: P2 / P2.2  
Date: 2026-09-12

## 1. Objective

在已批准的 P2.1 正式生产输入基线之上，建立第一版可重复构建、证据可追溯的中等 LOD Parametric Structural Skeleton Candidate，并完成 P2.2 所需的第一轮 machine geometry validation、deterministic rebuild 和结构审核图输出。

本任务是项目第一项正式 Blender 历史候选几何工程任务。

## 2. Authoritative Inputs

只允许使用：

1. `docs/production/zhenguo_wanfo/P2_2_DEFINITION_OF_DONE_V001.md`
2. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
3. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
4. `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
5. `production/zhenguo_wanfo/schema/evidence_aware_parameter_schema_v001.json`
6. P2.1 validation / Gate Review 与 D-023 / D-024 / D-025 边界

不得用外部知识、视觉估计、经验尺寸或手工 Blender 数值补足正式历史几何输入。

## 3. Scope

T-007 必须生成一个空间上连贯的完整主体结构候选，覆盖：

- grid / 柱网；
- columns / 柱；
- primary frame / 主要梁架；
- bracket topology / 中等 LOD 斗栱拓扑骨架；
- roof control geometry / 屋顶控制几何；
- 主要出檐、山面与主体空间关系。

本任务不要求：

- 材质、纹理、灯光或展示级渲染；
- 全部精细榫卯；
- 转角 45° 节点历史精确解；
- 隐衬角栿 / 隐角梁争议精确解；
- 小斗统一历史规格；
- 现状变形全量模拟；
- P2.3 级最终整合。

## 4. Required Engineering Architecture

### A. Formal Input Reader

建立只读参数读取层：

- 读取 85/85 formal parameter set；
- 读取 approved override sidecar；
- 读取 Geometry Dependency Matrix；
- 只将 `DIRECT_GEOMETRY_INPUT` / `DERIVED_GEOMETRY_RULE` 以及经批准 override 送入正式几何；
- 保留 `VALIDATION_REFERENCE / METADATA_ONLY / NOT_USED_IN_P2_2` 语义，不得混成几何输入。

### B. Build Manifest

每次正式构建生成机器可读 manifest，至少记录：

- 输入文件路径、版本、SHA256；
- Blender 版本；
- generation script 文件与 hash / Git commit；
- 实际使用的 parameter IDs；
- 每个 derived geometry rule 的 formula / source parameter IDs；
- 启用的 REASONABLE_COMPLETION / override；
- `Z-006-RC-01` 的 D-023 身份与当前解析值；
- bounded UNKNOWN / limitations；
- output `.blend` 路径与 hash；
- review image paths。

不得存在 manifest 外的历史几何输入。

### C. Generation Script

正式生成必须由脚本驱动，不接受依赖人工拖动 / 修模才能成立的结果。

优先使用 Local Blender 3.6.23 作为生产基线。脚本必须：

- 能从干净场景或明确基线重建；
- 生成稳定对象命名；
- 生成主要对象 metadata 或 manifest 映射；
- 不依赖未经批准的 Blender 4.5-only 核心功能；
- 不把历史尺寸写成无法追溯的 naked constants。

允许工程常量：容差、集合名、坐标轴约定、数学常数等非历史输入。

### D. Evidence Metadata

主要对象 / 对象族至少需具备或可由 manifest 唯一映射：

- `historical_state_tag`
- `evidence_class`
- `source_layer`
- `originality_status`
- `parameter_ids`
- override / REASONABLE_COMPLETION 标识（如适用）

无证据时 `originality_status=unknown`，不得自动升级为 `963_confirmed`。

## 5. Z-006 / RC-01 Hard Boundary

必须同时满足：

- `Z-006` 历史参数继续是 `UNKNOWN / null / DO_NOT_LOCK`；
- 其 dependency 继续是 `BLOCKS_P2_2_GEOMETRY`；
- P2.2 实际柱高输入通过独立 `Z-006-RC-01 = 11 × MOD-006` 解析；
- 当前基线下应解析为 3534.3 mm；
- 3534.3 mm 不得写回 Z-006；
- 3534.3 mm 不得作为无来源硬编码常量写入 Blender 脚本；
- manifest 必须明确 `REASONABLE_COMPLETION / D-023 / is_replaceable=true`；
- mutation / alternate override test 必须证明修改 RC-01 后重建结果随参数变化，而非手工修模。

## 6. Bounded Unknown / Precision Rules

- `DG-114`：继续 `BOUNDED_NON_BLOCKING`；P2.2 不创造统一小斗历史规格。
- `HIS-002`：继续 metadata/authenticity boundary。
- 转角 45° 节点、榫卯落位、隐角梁争议：只允许 medium-LOD topology / bounded placeholder。
- 不得因为几何完整而提升历史证据等级。

## 7. Machine Geometry Validation

至少验证：

1. grid bay count / depth bay count 与正式参数一致；
2. column count / positions 与正式参数一致；
3. column height production resolution 与 approved override 一致；
4. primary frame 主要跨度 / 层级符合正式参数与派生规则；
5. bracket topology 的 P2.2 medium-LOD 跳数 / 出跳关系符合正式输入；
6. roof control geometry 的主要控制高度 / 举折链符合正式参数；
7. eave / gable 主要控制关系符合正式参数；
8. 主要对象命名稳定、无随机 `.001/.002` 漂移作为正式接口；
9. 主要对象 metadata / manifest traceability 完整；
10. 不存在未批准历史尺寸裸常量。

构建前必须声明 machine tolerance，不得看到结果后反向放宽。

## 8. Deterministic Rebuild

在相同输入和相同 Blender 基线下至少连续执行两次干净构建，必须比较并记录：

- object name set；
- object count；
- key dimensions；
- topology summary；
- manifest geometry-input snapshot；
- output validation summary。

结果必须在定义的 deterministic tolerance 内一致。

## 9. Review Outputs

至少输出三张结构审核图：

- 平面 / plan；
- 正立面或侧立面 / elevation；
- 轴测 / axonometric。

审核图用于结构关系判断，不要求材质与展示级视觉。

建议路径：

- `production/zhenguo_wanfo/review/P2_2_STRUCTURAL_SKELETON_V001_PLAN.png`
- `production/zhenguo_wanfo/review/P2_2_STRUCTURAL_SKELETON_V001_ELEVATION.png`
- `production/zhenguo_wanfo/review/P2_2_STRUCTURAL_SKELETON_V001_AXON.png`

## 10. Required Deliverables

建议正式产物：

- `production/zhenguo_wanfo/scripts/generate_p2_2_structural_skeleton_v001.py`
- `production/zhenguo_wanfo/scripts/validate_p2_2_structural_skeleton_v001.py`
- `production/zhenguo_wanfo/tests/test_p2_2_structural_skeleton_v001.py`
- `production/zhenguo_wanfo/build/P2_2_BUILD_MANIFEST_V001.json`
- `production/zhenguo_wanfo/validation/P2_2_VALIDATION_REPORT_V001.md`
- `production/zhenguo_wanfo/review/P2_2_STRUCTURAL_SKELETON_V001_PLAN.png`
- `production/zhenguo_wanfo/review/P2_2_STRUCTURAL_SKELETON_V001_ELEVATION.png`
- `production/zhenguo_wanfo/review/P2_2_STRUCTURAL_SKELETON_V001_AXON.png`
- local-only `.blend`：建议 `production/zhenguo_wanfo/output/P2_2_STRUCTURAL_SKELETON_V001.blend`

`.blend / .blend1` 不提交普通 Git；但 validation report / manifest 必须记录绝对或项目相对路径、SHA256、Blender version。

## 11. Acceptance / HOLD Logic

Engineering recommendation PASS 仅当：

- P2.2 DoD-01～DoD-09 均有对应证据；
- 主体六大范围完整；
- machine geometry validation PASS；
- deterministic rebuild PASS；
- no unapproved geometry-critical input；
- no naked historical constants；
- RC / override replaceability 验证 PASS；
- independent reopen PASS；
- 三张 review outputs 生成；
- engineering evidence 已进入 canonical GitHub。

否则返回 HOLD，并列出精确 blocker。

Engineering PASS **不等于 P2.2 Gate PASS**。Gate Review 与最终批准仍由 ChatGPT + Product Owner 完成。

## 12. Git / Safety Boundary

开始前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git pull --ff-only origin main
```

只提交 T-007 scope 内的文本、脚本、manifest、validation、tests、review PNG 等可追踪产物。

不得提交：

- 已知 local-only PDF；
- P0 local-only directories；
- `.blend / .blend1`；
- 无关未跟踪资产。

禁止 force-push。

## 13. Final Report

Codex 完成后必须返回：

- STATUS: PASS / HOLD
- Blender version
- Python version
- formal input hashes
- build manifest path / hash
- structural scope completion: 6/6 或缺失项
- object count / key topology summary
- Z-006-RC-01 resolved value / traceability result
- machine geometry validation result
- naked historical constant scan result
- deterministic rebuild result
- independent reopen result
- review image paths
- local `.blend` path / SHA256 / file size
- automated test result
- validation report path
- Git commit SHA
- push result
- `git status --short`
- exact blocker if HOLD
- engineering recommendation

不得自行宣布 P2.2 Gate PASS。
