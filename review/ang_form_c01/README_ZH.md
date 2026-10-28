# 万佛殿｜头昂、二昂｜视觉参考模型 C01

**状态：候选已授权建模；待 PO 视觉审核。非官方实测成图，也非正式 Master。**

## 正式输入与界限

- PO 本轮要求：“先根据这个样子建模”，指对话中最近一张**由生成式图像工具制作**的浅色双栏《头昂与二昂官方资料约束形制参考图》。**该合成图不是山西文物数字博物馆原始三维模型，也不是 A1/A2 实测线型**。本轮以它作为**视觉造型方向**，不能将图中的木纹、隐藏接头或几何比例直接冒称官方事实。
- GitHub 基线：本分支从 [PR #78](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/78) 的只读诊断提交 `b3ab043fff5c202eb78bd9b4477d9993b594bced` 建立。保留 PR #76/#78 所有旧成果；不覆盖文件。
- 参照已批准的尺寸控制（不是推定历史全长）：头昂工作长度 **1440.62149385663 mm**，深头材广 **278.4 mm** / 单材身 **187 mm**；二昂工作长度 **1834.6484473864894 mm**，单材身 **187 mm**；两者厚均 **154 mm**。
- 真实结构控制不变：既有工程推导斜度约24.0755°；候选 GLB 存储在**自身轴向回正坐标**，尚未进行实际安装、接触检查。源图展示了昂头和斜身，但**没有提供实际端厚、削切起点、榫卯及完整昂尾**。

## 本轮可见造型要点

| 对象 | C01 视觉设计 | 证据等级 |
|---|---|---|
| 头昂 | 靠内端保留较高的深头段、以平滑过渡收为单材斜身、外端下缘逐渐向上斜削 | 方向来自 PO 选定的合成参考图；过渡长度/曲线属 INFERENCE |
| 二昂 | 独立且较长的187mm单材身，外端保留平直上缘，下缘向外渐斜削 | 同上；不按头昂整体缩放 |
| 头昂末端厚度15mm | 为生成封闭网格选择的数值 | INFERENCE，不是实测 |
| 二昂末端厚度13mm | 同上 | INFERENCE，不是实测 |
| 外端下缘开始变化的范围 | 头昂168mm / 二昂172mm（构件局部X） | INFERENCE，不是实测 |

## 成果入口（云端工作流生成）

- [两类总览](output/ANG_C01_OVERVIEW_ZH.png)
- [头昂中文审核图](output/TOU_ANG_C01_REVIEW_ZH.png)
- [二昂中文审核图](output/ER_ANG_C01_REVIEW_ZH.png)
- [头昂独立GLB](geometry/TOU_ANG_ILLUSTRATION_C01_candidate.glb)
- [二昂独立GLB](geometry/ER_ANG_ILLUSTRATION_C01_candidate.glb)
- [头昂网格JSON](geometry/TOU_ANG_ILLUSTRATION_C01_candidate.json)
- [二昂网格JSON](geometry/ER_ANG_ILLUSTRATION_C01_candidate.json)
- [本地算法网格检查](GEOMETRY_VALIDATION.json)
- [云端Blender独立进程检查](BLENDER_VALIDATION.json)

## 交付验证与审批规则

1. `build_reference_c01.py` 生成两个**独立**三角网格、GLB和中文模型审图。检查 watertight、positive volume、Euler=2、控制尺寸及GLB独立重读。
2. 云端 GitHub Actions Blender 4.5.13 LTS 从JSON**重新导出**2个GLB，并以另一个Blender进程导入检查尺寸、顶点位置、闭合和体积。
3. `PO_VISUAL=PENDING`。几何正确不证明历史形制正确，且不自动获准替换。不得修改或发布正式 Master、Registry、89实体工作模型，不得改华栱/令栱 Approved 视觉结论，也不得合并main。

审核建议重点：先确认**模型总体外观是否符合 PO 选定图**，再决定是否另行做测绘证据配准、接口核验；不要直接晋升正式 Master。
