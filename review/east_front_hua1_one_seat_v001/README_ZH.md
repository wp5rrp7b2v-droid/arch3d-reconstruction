# 万佛殿｜东缝第一跳华栱·单接口截面映射 V001

**类型：仅一处栌斗承槽→第一跳华栱下接口的独立工程实验。** 来源是 PR #76 华栱**外观方向获PO接受**的候选、PR #81 已被否决的17件旧工作连接网格中的**原栌斗**；**绝不表示 PR #81 整体组装被恢复批准。**

## 为什么要制作本候选

2026-11-07 [G0直接替换预检 PR #82](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/82) 证明：新候选局部 `x,y,z` 外包络为 `898.8×214.2×153 mm`，旧工作华栱为 `898.8×153×224.2 mm`。两者差异不允许直接用旧接触面积声称新形制通过。

### 来源层次

- **A1/A2量值的已有项目登记**：[主仓证据批次02](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/blob/main/docs/evidence/zhenguo_wanfo/P1_2_CORE_EVIDENCE_BATCH_02.md)第3节：单材广14份约214 mm、材厚10份约153 mm；依据原始测绘/2024论文桥接，不代表已经独立复核该柱头的唯一实测截面。
- **A1原页来源**：PR #76归档 A1 PDF60（印45）、PDF73（印58）及来源哈希，见 `review/gong_ang_form_v001/sources/PR72_PAGE_PROVENANCE.json`。本次使用此前已归档的来源链，**尚未进行A1/A2逐页原文重新视觉复核**，不把论文作者的模数解释当个体实测。
- **正式Master事实**：PR #76 `sources/HUAGONG_MASTER_SEMANTIC.json` 将 `width=214.2`、`thickness=153` 与原网格轴向不一致分别记录；`JUMP_1_HUAGONG_candidate.json` 的原始可见卷杀在 x-z 面、y向挤出214.2。
- **同一局部试装几何**：PR #81 `C02_ACTUAL_MESHES.json` 显示旧栌斗中央承槽平面 `z≈-297.9315mm`，槽壁横向界线为 `x=±76.5mm`；旧华栱与栌斗接触24,858.6mm²仅作为旧模型诊断资料。

## 显式适配方案（WORKING HYPOTHESIS，不等于新形制已批准）

1. **保留** PR #76 主轴 898.8mm、卷杀轮廓的归一化变化趋势，不用旧工作形制“重新生成”新模型。
2. 从PR #76 原候选的坐标重新映射：`world X = local y × (153/214.2)`，`world Y = -local x`，`world Z = 栌斗承槽底标高 + (local z − local z_min)×(214.2/153)`。即横向材厚153、竖向单材广214.2。映射是**非等比例截面修正**，卷杀纵横比随之改变，**必须重新提交PO视觉审核**，不能宣称完整保留原已批准像素轮廓。
3. 仅采用PR #81的`SOURCE_LUDOU_READONLY`源实际三角网格；不直接复制其已否决的旧第一跳华栱/昂或完整17件装配。
4. 仅对**一个承槽底面**做水平面接触面积、面法向、全部两实体Boolean穿插检查。理想接触面积>100mm²、穿插≤1mm³；其他接口包括上方交互斗均 `NOT_TESTED`。
5. GitHub Actions Blender4.5.13 LTS生成独立两实体BLEND/GLB、两张中文审图，并由第二个Blender进程重开；Python/Shapely/Trimesh独立检查与GLB导入；失败必须显式记录。

### 验收边界

- `GEOMETRY_SINGLE_LOWER_SEAT_PASS` 仅代表**实验几何证据通过**，不等于“整套铺作结构正确”、不等于古代榫卯已验证、不等于PO批准截面变更。
- `GEOMETRY_SINGLE_LOWER_SEAT_FAIL` 或 `UNKNOWN` 则停止，不把其发展为新建筑模型。
- 本PR使用 **Draft**，base为PR #81未获批准工作分支，仅提交独立实验目录和云端运行证据；**绝不合并PR #81或main、修改任何Master/Registry/已批记录**。
- 后续只有在本轮实验完成且PO认可修正后的可见形制时，才可考虑上方交互斗接口；本轮不启动第二接口。

## 资料及构件来源路径

- `review/gong_ang_form_v001/geometry/JUMP_1_HUAGONG_candidate.json`：Git Blob `567b5336f3319a66ff292aee88c57831850bb8a6`
- `review/east_front_connectors_c02/output/C02_ACTUAL_MESHES.json`：Git Blob `c5a2622065589ed3588c7099f289384686dcb3c5`
- 源89件BLEND SHA256 `5c81c836cc7ca3a229eebe5ac9cb4c62a744b9a1eeb10b0e9683cf0ccd097f13`
- 本目录所有图模必须为**新的、独立候选产物**，不能用旧验收结果替代。

