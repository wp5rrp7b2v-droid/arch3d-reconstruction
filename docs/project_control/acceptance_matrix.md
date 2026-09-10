# Acceptance Matrix｜ARCH3D-001

## P0｜技术路线验证

| Gate | 验收标准 | 当前状态 | 关键证据 / 限制 |
|---|---|---|---|
| P0.0 | 项目控制系统可跨 Chat 使用 | **PASS** | Project Control 文件集可作为正式 handoff；Dashboard 是派生可视化。 |
| P0.1 | 本地 Mac 可稳定完成轻量 Blender 灰模、保存与审核 | **PASS** | Blender 3.6.23；灰模生成、保存、独立重开、Geometry Integrity、PNG 审核全部通过。 |
| P0.2 | Local → Cloud → 修改 / 渲染 → Local，无关键资产丢失 | **PASS / Class B** | Local 3.6.23 → GitHub → GitHub Actions Blender 4.5.13 → Artifact → Local 3.6.23 全链路通过。3.6 会移除部分不支持的 4.5 UI region 数据，但核心几何、Marker 与所需 Metadata 未损失。 |
| P0.3 | 建筑参数能够驱动脚本生成一个最小结构模型 | **UNLOCKED / NEXT SESSION** | T-004｜PARAMETRIC_ARCHITECTURE_POC_V001 保持 NOT_STARTED；下一 Session 启动。 |

**P0 Gate Progress：3 / 4 PASS。**

P0.3 PASS 后进入 P0 Gate Review；只有 P0 达到 4 / 4 PASS 才能进入 P1｜选题取证。

## P0.2 Production Rule

凡需要返回 Local Blender 3.6 继续维护的核心资产，不得默认依赖未经单独验证的 Blender 4.5-only 数据结构、节点、模拟或其他新功能。新功能进入正式生产前必须先做兼容性验证。
