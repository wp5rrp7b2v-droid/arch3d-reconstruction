# T-011｜CMP-COLUMN-001 柱 Master 合同实现试点验证 V001

**工程状态：PASS（22/22 machine checks；6/6 review PNG）**

**审核状态：待 ChatGPT / Product Owner 审核；不构成 P3.1 Gate PASS。**
Blender：3.6.23。参数、生成器、语义快照和验证结果已提交；canonical `.blend` 仅保存在本机，不进入普通 Git。

## 参考实现与证据语义

| 几何参数 | 本次解析值 | 来源模式 | 证据边界 |
|---|---:|---|---|
| `diameter_mm` | 460.0 mm | `OBSERVED_Z001` | 报告调整后的现状约值；不是已证实的 963 原设计精确柱径。 |
| `height_mm` | 3534.3 mm | `RC_Z006_RC_01` | D-023 批准的 `11 × MOD-006` 可替换生产候选；不是已证实的 963 原柱高。 |

`Z-006` 本体保持 `UNKNOWN / null / DO_NOT_LOCK`。`HIS-002` 的逐构件原真性仍为 `unknown`。Master 仅为等径圆柱主体；无收分、卷杀、侧脚、柱础、柱头细部、榫卯或角柱生起。柱底面中心为原点，+Z 向上，Location/Rotation 为零，Scale 为一；不含建筑 world placement。

## 资产与审核件

- 参数：[CMP-COLUMN-001_MASTER_PARAMS_V001.json](../../../production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_PARAMS_V001.json)
- 生成器：[build_column_master_v001.py](../../../production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/build_column_master_v001.py)
- 本机二进制：`production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/asset/CMP-COLUMN-001_MASTER_V001.blend`
- 二进制 SHA256：`98211701fcc358f6174829257ef13310baa4d1a2d5e762637c25c812a4362487`
- [语义快照](../../../production/zhenguo_wanfo/component_library/masters/CMP-COLUMN-001/CMP-COLUMN-001_MASTER_SEMANTIC_V001.json)；几何签名：`ad50176d3fb9a1125e5bcefce6ff29350997ddd0221fdc3e52e134d75151b08c`
- [审核包元数据](../../../production/zhenguo_wanfo/review/P3_1/masters/CMP-COLUMN-001/REVIEW_PACKAGE_V001.json)：`FRONT`、`SIDE`、`TOP`、`AXON`、`DIMENSION_PARAMETER_SUMMARY`、`EVIDENCE_UNCERTAINTY_SUMMARY`，共 6 张 PNG。四张几何视图为正交相机中性灰展示；渲染用相机和临时材质未写入 Master。
- [P3.1 Pilot Registry](../../../production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json)：只登记 `CMP-COLUMN-001`；approval status 保持待审核，其余五类没有登记为已完成。

## 校验结果

[机器验证 JSON](../../../production/zhenguo_wanfo/validation/P3_1_COLUMN_MASTER_PILOT_VALIDATION_V001.json) 记录全部 22 项检查、输入哈希、独立重开结果和 P2 前后哈希。重点结果：

| 检查 | 结果 |
|---|---|
| Asset Contract required fields、唯一 ID、mm 单位、坐标与原点 | PASS |
| 本体对象与 mesh 各 1；Location 0、Rotation 0、Scale 1；无 world placement | PASS |
| 包围盒 X/Y = 460.0 mm、Z ≈ 3534.30005 mm（Blender 单精度存储；容差 0.001 mm） | PASS |
| 无无证据柱构造；generator 无正式历史尺寸裸常量 | PASS |
| Z-006 UNKNOWN；RC-01 独立可替换；HIS-002 unknown | PASS |
| 独立语义重建与独立打开 `.blend` | PASS |
| 6 项 review package；Registry 单一 Master、无 orphan | PASS |
| 19 个 P2 冻结参数/依赖/集成/审核文件及本机 P2 `.blend` 前后哈希 | UNCHANGED |

Synthetic mutation 仅在临时目录中把 `height_mm` 改为 **3634.3 mm / ENGINEERING_TEST_ONLY**。包围盒高度增加 100.0 mm，几何签名改变；直径、Z-006、RC 候选记录与正式参数文件保持不变。Mutation 未写入历史 Variant 清单，也未覆盖 canonical `.blend`。测试后按正式参数重建，语义签名恢复，独立重开通过。

本报告仅确认 T-011 工程链可审核。柱 Master 的最终视觉批准、其余五类 Master 的生产授权以及 P3.1 Gate 决策仍由 ChatGPT / Product Owner 另行作出。
