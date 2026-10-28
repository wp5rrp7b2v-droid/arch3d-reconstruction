# 镇国寺万佛殿｜四类栱昂｜独立组合试搭 C01

本轮由 Product Owner 指令“四个构件尝试组合搭建”授权。**仅为实验性四件试搭，并非整套柱头铺作、更不是已验收的历史结构。**

## 源输入与身份边界

| 试搭实体 | 已有来源 | PO状态及限制 |
|---|---|---|
| 第一跳华栱（1件） | PR #76 `JUMP_1_HUAGONG_candidate.json`，固定提交 `028517cbdada6cb266feae17f58ae0a7888c4a93` | V001形制方向视觉PASS；未证明和PR75东缝既有实例接口兼容 |
| 令栱（1件） | PR #76 `LINGGONG_candidate.json`，同提交 | 形制方向视觉PASS；PR75只给出**西缝隔架令栱**实例，不能伪称本件已有东缝合法安装实例 |
| 头昂（1件） | PR #79 `TOU_ANG_ILLUSTRATION_C01_candidate.json`，提交 `1f2690b59861b235bad0bb63fb05556178871bd7` | C01视觉PENDING；不声称官方实测 |
| 二昂（1件） | PR #79 `ER_ANG_ILLUSTRATION_C01_candidate.json`，同提交 | C01视觉PENDING；不声称官方实测 |

这里的“四个构件”按华栱、令栱、头昂、二昂**各一件**解释。**第二跳华栱未纳入**，因此既不能检验两跳华栱配置，也不具备完整双杪双下昂柱头铺作的全部结构对象。

## 空间试排逻辑

- 外檐方向按东缝PR75试搭原位的Y方向，头昂与二昂采用已有 **24.075498255°** 工程设计斜度做刚体回转。
- 华栱沿Y方向，令栱沿X方向交叉，令栱在华栱上方的高度由两件尺寸进行**试搭假设**，不宣称其实际所在铺作位置正确。
- 两昂大致使用PR75东缝前柱头相对位置中心（world bbox），但新C01形体和原试装体不同，因此此姿态只供诊断，**不是几何接口证明**。
- 所有JSON输入只读；使用原始顶点和面 + 刚性变换，无统一缩放、无删点、无加工榫卯、无隐藏的临时块支撑。源模型和89实体BLEND/GLB不变。
- 组合相对于东缝前柱头旧局部坐标，选用原试装的参考原点 `(4437.0,5355.0,-2297.831485)` mm；Blender内部以此为原点局部显示。

## 交付

由云端Blender4.5.13 LTS产生并回归GitHub的模型与验证文件：

- [组合BLEND](output/WANFO_FOUR_GONG_ANG_PILOT_C01.blend)
- [组合GLB](output/WANFO_FOUR_GONG_ANG_PILOT_C01.glb)
- [等轴透视总览](output/iso_FOUR_COMPONENTS_ZH.png)
- [侧面](output/side_FOUR_COMPONENTS_ZH.png)
- [正面](output/front_FOUR_COMPONENTS_ZH.png)
- [真实六对几何穿插检测](output/ASSEMBLY_VALIDATION.json)
- [云端二次进程GLB重读与二进制哈希](output/BINARY_REOPEN_VERIFICATION.json)
- [生成代码](cloud_build_and_verify.py)与[云端工作流](../../.github/workflows/wanfo_four_gong_ang_pilot_c01.yml)

## 验收关口

1. **FILE Gate**：至少四件原始网格只读、四个不同ID、两件Approved视觉方向不变、原有89实体及Master未触碰；组合BLEND/GLB完整。
2. **GEOMETRY Gate**：保留四件原网格、仅施刚体姿态；Blender二进制保存和独立重读 PASS；对六对网格执行交错三角面/Boolean INTERSECT检查，报告各对实际体积。不可将AABB重叠直接当真实穿插。
3. **CONTACT Gate**：先判断当前四件是否有实际支承接触，并检出冲突或离空。**即使四件都无体积穿插，也不能证明它们能独立支撑建筑**，因为还缺斗、栌斗、第二跳华栱、上梁、托脚和正式接口构件。
4. **VISUAL Gate**：仅接受四件局部空间试搭图交付 PO 审核，不将相对层位假设登记为Approved。

如发生严重穿插、离空或连接构件缺失，应**据实标 FAIL / UNSUPPORTED**、保留模型和截图供下一轮纠错，不得为了给出PASS擅自修改批准过的候选外形。

**本单元完成后停止**，不得合并main、修改Master/Registry/89实体，不得默认开始第二轮校准。
