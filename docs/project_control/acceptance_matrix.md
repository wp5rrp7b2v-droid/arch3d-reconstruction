# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证｜CLOSED / APPROVED 2026-09-11

| Gate | 验收标准 | 最终状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **PASS** | T-004｜PARAMETRIC_ARCHITECTURE_POC_V001：独立 JSON 参数驱动同一 Blender 3.6 Python 脚本；Baseline 3×2 开间→12 柱/21 主要对象，Variant 仅改 JSON 为 4×3 开间→20 柱/31 主要对象；尺寸与屋顶同步变化；独立重开及 Determinism PASS。 |

**P0 Gate Final：4 / 4 PASS。**

2026-09-11 Product Owner 已明确批准 P0 关闭。P0 状态：**CLOSED / APPROVED**。项目进入 **P1｜选题取证**。

## P0.2 Production Rule｜Carry-forward

凡需要返回 Local Blender 3.6 继续维护的核心资产，不得默认依赖未经单独验证的 Blender 4.5-only 数据结构、节点、模拟或其他新功能。新功能进入正式生产前必须先做兼容性验证。

## P0.3 Validation Boundary｜Carry-forward

P0.3 只证明“结构化建筑参数 → 脚本 → 可重复最小结构模型”的技术链路成立；不代表历史证据已经完成参数化，也不代表正式古建筑结构、构造法式或复原精度已经被验证。这些属于 P1 及后续 Phase。

## P1 Entry

P1 已解锁并进入。P1 的正式 Gate / 验收项尚未在本文件中定义；应在 P1 启动设计完成后再写入，避免预先制造未经批准的验收标准。
