# 万佛殿｜东缝前柱头 HUA1 接口最小预检 G0（2026-11-07）

**性质：独立只读工程复核记录，候选分支证据，不是 PO 审批、历史形制认证或装配成功报告。**

## 范围与基线
- 目标接口：东缝前柱头 **柱头栌斗—第一跳华栱（HUA1）—交互斗**。
- 目标：先判定 PR #76 视觉方向通过的第一跳华栱候选是否可以在**保持原模型轮廓朝向与未经批准接口不变**的情况下，直接刚体替换 PR #81 的旧工作件；不涉及两昂、更不扩展整殿。
- 当前正式 main 的 Project Control 为 R366；2026-10-31 R368 仅是 Draft PR #77。PR #80/#81 组装 PO FAIL；PR #76 华栱和令栱视觉方向 PASS、两昂旧版 FAIL；不以 PR #79 两昂 C01 当已批准输入。
- 结果来自 GitHub 原始 JSON 顶点的独立 min/max 逐轴复算，**没有运行新的 Blender 装配/接触/碰撞检查**。

## 固定来源（不改原始文件）
1. PR #76 候选第一跳华栱：`review/gong_ang_form_v001/geometry/JUMP_1_HUAGONG_candidate.json`，Git Blob SHA-1 `567b5336f3319a66ff292aee88c57831850bb8a6`。[审核文件](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/geometry/JUMP_1_HUAGONG_candidate.json)
2. PR #76 提取自 PR #75 的旧第一跳局部工作件：`review/gong_ang_form_v001/geometry/EAST_FRONT_HUA1_LOCAL_trial.json`，Git Blob SHA-1 `6dc9d8ed8fd162c8d5da2709c5f0698bc9eb0007`。[审核文件](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/review/gong-ang-form-v001-20261021/review/gong_ang_form_v001/geometry/EAST_FRONT_HUA1_LOCAL_trial.json)
3. PR #81 实际17对象旧网格及连接记录：[实际网格](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/assembly/east-front-connectors-c02-20261028/review/east_front_connectors_c02/output/C02_ACTUAL_MESHES.json)、[接触与碰撞](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/assembly/east-front-connectors-c02-20261028/review/east_front_connectors_c02/output/C02_INTERFACE_VALIDATION.json)。
4. [2026-10-31 审批与装配否决交接](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/governance/wanfo-status-handoff-20261027/docs/project_control/WORK_HANDOFF_2026-10-31_ZH.md)。

## 已执行的独立 G0 预检｜原始顶点范围（mm）

| 项目 | PR #76 新 HUA1 候选 | 旧东缝 HUA1 工作件 | 差值 |
|---|---:|---:|---:|
| x 向长度（轮廓主轴） | 898.800000 | 898.799988 | +0.000012 |
| y 向厚度（轮廓面挤出方向） | 214.200000 | 153.000000 | +61.200000 |
| z 向高度（轮廓面竖向） | 153.000000 | 224.200005 | -71.200005 |
| 顶点数 | 136 | 132 | 不要求相同 |
| y 向去重坐标平面数（四舍五入至0.00001 mm） | 2 | 2 | 均沿 y 挤出 |

两份网格均沿 y 轴挤出，其**可见轮廓均在 x-z 面**，所以不能靠任意把 y/z 轴交换来宣称保留了原审过的竖向卷杀轮廓；若交换会改变轮廓相对于竖向和侧厚的语义。PR #76 的 README 已指出正式 Master 与部分工作实例的截面轴表达不一致，本次以实际坐标进一步量化了该问题。

PR #81 的旧装配 HUA1 局部工作件包络为：组装坐标横向 153 mm、纵向 898.8 mm、竖向 224.2 mm，与上述旧件一致。它与栌斗旧接触面积 **24,858.6314 mm²**、与交互斗旧接触面积 **1,315.8009 mm²**；这两项是旧件的历史测试结果，**不可转移到新件**。

### 预先定义的 G0 判定
- **PASS**：不改变可见轮廓主轴及竖向语义，候选经纯刚体定位后的目标截面与旧支承接口包络相容（本预检以既有各轴截面包络精确匹配、偏差不超过0.001 mm为保守的*直接替换*条件）；然后才进入实体面接触和 Boolean 检验。
- **FAIL**：任一截面轴/数值不匹配，或必须先重作截面、槽口、支承高度，或需要改变已审批轮廓的空间语义；本轮停止，不把旧接触面积作为新件验收。
- 该0.001 mm为**本次直接替换预检门槛**，不是全项目规定的新历史精度标准或连接工程公差；不能据此判定一个允许局部调整的新方案永远不可装配。

**结果：G0 = FAIL（未经改造的刚体直接替换不合格）。** 长度轴 PASS；侧厚差 +61.2 mm、高度差 -71.2 mm，两轴 FAIL。没有执行新构件的真实接触面、间隙、穿插或完整结构测试；因此这些项应标记 **NOT_TESTED**，绝不可标 PASS。

## 这阶段实际证明了什么
- **FACT**：新旧第一跳华栱的原始网格截面方向及包络存在上述实测差异；PR #81 原有的24,858.6/1,315.8 mm²接触只属于旧网格；PR #81整套组装仍被PO否决。
- **INFERENCE**：要在该柱头位置采用新视觉候选，至少需先进行有来源的截面轴、材广、挤出方向和接口协调，可能需要重新生成仅限局部的*连接适配候选*，但不能擅自修改已认可的可见卷杀形制。
- **UNKNOWN**：A1/A2的具体构件截面投影与这两类计算轴的最终对应、可容许的工程接口调整、候选在真实斗/交互斗上的面接触/空隙与 Boolean 穿插、榫卯历史构造及受力。
- **STOP**：本轮不创建或修补实际3D网格，不启动云端Blender装配，不修改Master/Registry/main，不批准PR #79昂或PR #81失败结构。

下一项独立工作单元（尚未授权）：先核对A1/A2对该**同一真实第一跳华栱实例**的截面方向/材广与相关栌斗、交互斗的真实支承层位；明确工程允许的局部适配边界，做**一个接口面**的候选—接触—碰撞—独立重开验证。之后如PASS再扩大到上下两个接口；若FAIL继续停在该处，不迭代整套铺作。

> 复算方法：分别读取两份JSON的 `vertices` 三坐标数组，逐轴计算 `max(v[i])-min(v[i])` 与 y 轴去重平面数；本记录数据均来自真实顶点，不依赖显示图像或原始报告自动“补足”未知尺寸。
