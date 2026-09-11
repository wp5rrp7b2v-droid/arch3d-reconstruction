# P0 Closure｜ARCH3D-001

## Phase

- Phase：P0｜技术路线验证
- Status：**CLOSED / APPROVED**
- Closure Date：2026-09-11
- Product Owner Approval：YES
- Gate Result：**4 / 4 PASS**

## P0 Objective

验证《中国古建筑3D复原》项目在正式选题与历史复原开始前，是否具备最小可行的项目控制与 3D 技术闭环：跨 Chat 项目控制、本地轻量 Blender 建模、Local↔Cloud 往返，以及参数驱动最小结构生成。

## Gate Summary

| Gate | Result | Evidence Summary |
|---|---|---|
| P0.0｜Project Control 跨 Chat | PASS | Project Control 文件集成为 SSOT；Dashboard 为派生可视化；GitHub main + Local working copy 同步模式进入 TRIAL。 |
| P0.1｜Local Blender | PASS | Blender 3.6.23 macOS x64 完成灰模生成、保存、独立重开、Geometry Integrity 与 PNG 审核。 |
| P0.2｜Local→Cloud→Local | PASS / Class B | GitHub Actions + Blender 4.5.13 完成云端修改/渲染/返回；Local 3.6 可继续维护核心几何、Marker 与所需 Metadata，但会移除部分 4.5-only UI region 数据。 |
| P0.3｜参数驱动结构模型 | PASS | 独立 JSON 参数驱动同一 Blender 3.6 Python 脚本；Baseline 3×2 开间与 Variant 4×3 开间均生成、保存、重开并验证；Variant 只修改参数，不修改建模逻辑。 |

## Completed Engineering Tasks

- T-001｜PROJECT_WORKSPACE_INIT_V001｜PASS
- T-002｜LOCAL_BLENDER_POC_V002｜PASS
- T-003｜LOCAL_CLOUD_ROUNDTRIP_POC｜PASS / Class B
- T-004｜PARAMETRIC_ARCHITECTURE_POC_V001｜PASS

## P0.3 Reproducible Evidence Archive

P0.3 在 Gate 关闭后完成轻量证据归档：

- Evidence Commit：`63a0c506f98d843376361421cf88e1e74c807dc7`
- Commit Message：`p0.3: archive lightweight reproducible evidence`
- GitHub 保存：README、Baseline/Variant 两份 JSON、统一 Blender Python 生成脚本、Baseline/Variant 两张 PNG，共 6 个文件。
- Blender `.blend / .blend1` 二进制工程文件不进入普通 Git，继续保留在本地 P0.3 工作区。
- Commit 已核对，无 `.blend`、无 `.blend1`、无 P0.1 / P0.2 本地产物误提交。
- 当前阶段采用 **GitHub + Local** 的轻量资产策略；不引入第三备份位置、Git LFS、NAS 或其他复杂资产管理层。待正式资产规模、复杂度或不可重建价值明显上升时再评估。

## Validated Capabilities

1. Project Control 可以跨 Chat 作为正式 handoff 与状态事实源。
2. Local Intel Mac + Blender 3.6.23 能承担轻量模型生成、审核和维护。
3. GitHub Actions Hosted Runner + Blender 4.5.13 可承担当前 Cloud Blender 执行节点。
4. Local 3.6 → Cloud 4.5 → Local 3.6 往返可行，但属于 Class B｜ROUNDTRIP_WITH_LIMITATIONS。
5. 结构化建筑参数可以稳定驱动 Blender Python 生成可重复的最小结构模型。

## Carry-forward Rules / Limitations

### Blender Compatibility

凡需要回到 Local Blender 3.6 继续维护的核心资产，不得默认依赖未经验证的 Blender 4.5-only 数据结构、节点、模拟或其他新功能；新功能进入正式生产前应单独验证兼容性。

### Parametric Validation Boundary

P0.3 只证明：

`结构化参数 → 脚本 → 可重复最小结构模型`

技术链路成立。

P0 **没有**证明：

- 历史证据已经完成结构化参数化；
- 当前 POC 灰模具有正式历史准确性；
- 中国古建筑构造法式、斗拱、屋面、材质或比例体系已经被验证；
- 正式复原案例已经开始。

以上内容进入 P1 及后续 Phase。

## Governance Baseline at Closure

- Project Control Baseline：2.0
- Canonical committed state：GitHub private repo `main` / `docs/project_control/`
- Local working copy：`/Users/caroline/中国古建筑3D复原/docs/project_control/`
- Synchronization：TRIAL
- Dashboard Visualization：v006
- 重大同步规则：先更新 GitHub canonical Project Control，再由 Local `git pull --ff-only origin main` 拉回；ChatGPT 与 Codex 不并行修改同一 Project Control 文件。

## Material Decisions Retained

- D-009：Local Blender 3.6.23 / Cloud Blender 4.x 非对称版本架构。
- D-010：Codex Cloud 不作为当前 Blender Executor；GitHub Actions 为替代节点。
- D-011：P0.2 PASS / Class B。
- D-012：Project Control 文件集为正式 SSOT；Dashboard 为派生可视化。
- D-013：GitHub main + Local working copy 同步试运行。
- D-014：Product Owner 批准 P0 关闭并进入 P1。

## Transition

P0 已关闭，不再继续扩展技术验证范围。

**Next Phase：P1｜选题取证。**

P1 启动时首先建立首个正式复原案例的候选选择与证据获取框架；在 P1 的 Gate / 验收标准正式定义前，不预设未经批准的验收项，也不直接进入正式 3D 生产。
