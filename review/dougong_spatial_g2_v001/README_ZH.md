# 数字博物馆斗栱｜空间组织关系独立分析 G2 V001

日期 2026-11-07｜用户确认“先弄清馆方斗栱如何组合，再用我们自身构件体系复原”。

## 当前基线与工作范围
- 正式项目仍以 `main/docs/project_control/project_state.json`、A1/A2为事实基线；已核 GitHub 主分支 revision R366。
- [PR #86](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/86) 的20对象原创试件被 PO 视觉审核判定 FAIL；**不延续形态修补，不向main合并**。
- [PR #85](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/85) 曾验证数字博物馆 `dougong.gltf` 含97节点、96个 `polySurface...` 匿名网格；Blender导入/三视图PASS，但栌斗与第一跳华栱身份FAIL。
- 本工作单元只查出这96件在本模型内部的**相对空间构成**（多少层、主要横向方向、候选邻接），**不创建正式建筑构件，不复制数字博物馆模型网格**。

## 证据安全与追溯
- 模型来源： https://szbwgvue.chwhyun.cn/wanfodian/3d/dougong/dougong.gltf
- 根据G1已留痕的 SHA256 精确核验 `gltf` 和 `bin`。服务器证书2026-10-15已到期，本轮仅读取固定哈希的相同数据用于临时独立分析；不声称TLS身份安全已证明。
- 原 `gltf/bin`、纹理、基于原模型直接渲染的视图均不提交公开 GitHub。临时三视图仅保留GitHub Actions Artifact 7天，公开仓库保存模型文件哈希、匿名对象统计、包络邻接候选与相对层次统计。
- A1《精细测绘报告》PDF73（印58）图2-27用于独立判断铺作/下昂的**建筑结构逻辑**。**没有对照到同一柱头的构件身份时，不得把这一参考视作一一匹配证明**。

## G2预定PASS/FAIL
- G2-1：两份源数据的SHA与G1完全一致，且Blender可独立导入96网格，否则FAIL。
- G2-2：96个网格均能提取可复现的三轴包络/方向类型；相对高度分组总数=96；可以产生至少2种不同视角的实际非空图；否则FAIL。
- G2-3：对可能“上部构件底部接触下部构件顶部”的项目列出**候选**（AABB上下端接近且水平包络有交叠）；这是INFERENCE，绝不能把候选误称为真实网格接触、榫卯、承载或历史正确性。
- G2-4：只有经过同位置A1/A2核对能够把匿名ID可靠对应“栌斗”和“第一跳华栱”，才可将单构件身份标记PASS；否则身份门槛保持FAIL/UNKNOWN。

## 本次交付
- 可复跑脚本 `review/dougong_spatial_g2_v001/analyze_blender.py` 和GitHub Actions运行日志。
- `output/G2_SPATIAL_PROOF.json`：原始SHA、匿名网格数量、方向统计、5个相对高度区间、潜在接触关联与证据级别。
- `output/G2_RELATIVE_LAYER_COUNTS.svg`：源数据统计图（不包含原模型顶点）；5等份是便于分析的可视化分段，不是建筑真实五层。
- 云端Actions Artifact：3张标色角度检视图，保存7天，源模型不再分发。

## 治理边界
- 禁止覆盖main、Master、Registry、PR83模型或将 PR86 FAIL 改判 PASS。
- 若可以证明网格空间结构关系但缺乏实体名称映射，本工作单元只能报“相对拓扑PASS/真实身份未证明”，提出**最小对象级人工视觉复核**作为下一工作单元，不直接制作V002。
