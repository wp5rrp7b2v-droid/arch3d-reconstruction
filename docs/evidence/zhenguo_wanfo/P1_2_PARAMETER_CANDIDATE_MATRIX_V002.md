# P1.2｜平遥镇国寺万佛殿｜正式参数候选矩阵 V002

Status: PRE-P1.3 / DIRECT-SOURCE-UPGRADED / NOT PRODUCTION-LOCKED  
Date: 2026-09-11  
Primary source: `SRC-ZG-WF-001`  
Supersedes: `P1_2_PARAMETER_CANDIDATE_MATRIX_V001.md`

## 0. V002 核心升级

V002 在完整主报告直接核读后形成。与 V001 相比：

1. 多项平面、柱、斗栱、屋架、架道、出际、举折数据升级为 `DIRECT_VERIFIED`；
2. 角柱生起由“≈50mm待核”改为“有效实测51–68mm、均值59.5mm；设计候选2寸=61.2mm”；
3. 架道、举折首次获得主报告直接表格控制；
4. 明确区分 `observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate`；
5. 撤销 V001/Batch04 中“主报告第147页”和“主报告第107页”的错误页码归属；
6. 本矩阵仍不是 Blender 正式 JSON，所有“963设计候选”需经 P1.3 分级后才能进入生产参数。

## 1. 证据状态

- `DIRECT_VERIFIED`：已直接核读主报告原页/表/图。
- `DIRECT_REPORT_INFERRED`：已直接核读主报告，但该值本身是作者推算/推荐结论。
- `A_BRIDGE_VERIFIED`：正式论文/研究转引高等级数据，但本轮未在主报告中找到相同原页定义。
- `B_SUPPORT`：机构数字展示/强佐证。
- `UNKNOWN`：证据不足。

## 2. 参数候选矩阵

### 2.1 平面 / 柱网

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| PM-001 | `bay_count_front` | topology_or_rule | 3 | DIRECT_VERIFIED | READY | 面阔三间。 |
| PM-002 | `bay_count_depth` | topology_or_rule | 3 | DIRECT_VERIFIED | READY | 进深三间六椽。 |
| PM-003 | `front_center_bay_observed_mm` | observed_as_measured | **4481.3** | DIRECT_VERIFIED | READY | 表2-4。 |
| PM-004 | `depth_center_bay_observed_mm` | observed_as_measured | **3676.8** | DIRECT_VERIFIED | READY | 表2-4。 |
| PM-005 | `side_bay_observed_mm` | observed_as_measured | **3505.7** | DIRECT_VERIFIED | READY | 面阔/进深次间均值。 |
| PM-006 | `overall_width_observed_mm` | observed_as_measured | **11492.7** | DIRECT_VERIFIED_DERIVED | READY | 4481.3+2×3505.7。 |
| PM-007 | `overall_depth_observed_mm` | observed_as_measured | **10688.2** | DIRECT_VERIFIED_DERIVED | READY | 3676.8+2×3505.7。 |
| PM-008 | `front_center_bay_design_chi` | reconstructed_design_candidate | **14.5尺** | DIRECT_REPORT_INFERRED | READY | 306mm营造尺。 |
| PM-009 | `depth_center_bay_design_chi` | reconstructed_design_candidate | **12尺** | DIRECT_REPORT_INFERRED | READY | 同上。 |
| PM-010 | `side_bay_design_chi` | reconstructed_design_candidate | **11.5尺** | DIRECT_REPORT_INFERRED | READY | 同上。 |
| PM-011 | `overall_width_design_mm` | reconstructed_design_candidate | **11475** | DIRECT_REPORT_INFERRED | READY | 37.5尺×306。 |
| PM-012 | `overall_depth_design_mm` | reconstructed_design_candidate | **10710** | DIRECT_REPORT_INFERRED | READY | 35尺×306。 |
| PM-013 | `perimeter_column_count` | topology_or_rule | **12** | DIRECT_VERIFIED | READY | 无内柱。 |
| PM-014 | `interior_column_count` | topology_or_rule | **0** | DIRECT_VERIFIED | READY | 与六椽栿通檐用两柱一致。 |

### 2.2 营造尺 / 材分

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| MOD-001 | `yingzao_chi_mm` | reconstructed_design_candidate | **306** | DIRECT_REPORT_INFERRED | READY | 报告推荐结论；不是实测物理尺。 |
| MOD-002 | `fen_mm` | reconstructed_design_candidate | **15.3** | DIRECT_REPORT_INFERRED | READY | 1尺=20分体系。 |
| MOD-003 | `single_cai_width_fen` | reconstructed_design_candidate | **14分** | DIRECT_REPORT_INFERRED | READY | 报告结论倾向14分，不按《营造法式》15分。 |
| MOD-004 | `single_cai_thickness_fen` | reconstructed_design_candidate | **10分** | DIRECT_REPORT_INFERRED | READY | 每分0.5寸。 |
| MOD-005 | `full_cai_height_fen` | reconstructed_design_candidate | **21分** | DIRECT_REPORT_INFERRED | READY | 足材。 |
| MOD-006 | `full_cai_height_mm` | reconstructed_design_candidate | **≈321.3** | DIRECT_REPORT_INFERRED | READY | 21×15.3。 |

### 2.3 柱 / Z基准

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| Z-001 | `column_diameter_observed_mm` | observed_as_measured | **≈460** | DIRECT_VERIFIED | READY | 报告现场估算调整值。 |
| Z-002 | `column_diameter_design_mm` | reconstructed_design_candidate | **459** | DIRECT_REPORT_INFERRED | READY | 1尺5寸。 |
| Z-003 | `corner_column_rise_valid_range_mm` | observed_as_measured_filtered | **51–68** | DIRECT_VERIFIED | READY | 报告筛选有效值。 |
| Z-004 | `corner_column_rise_mean_mm` | observed_as_measured_filtered | **59.5** | DIRECT_VERIFIED | READY | 有效值平均。 |
| Z-005 | `corner_column_rise_design_mm` | reconstructed_design_candidate | **61.2** | DIRECT_REPORT_INFERRED | REVIEW_HIGH_RISK | 2寸；报告仅称猜测。 |
| Z-006 | `column_height_963_design_mm` | reconstructed_design_candidate | **UNKNOWN** | UNKNOWN | HOLD_HIGH_RISK | 原始地坪/柱础关系仍不足。 |
| Z-007 | `global_z_datum` | topology_or_rule | **UNKNOWN** | UNKNOWN | HOLD_HIGH_RISK | P1.3必须明确选取基准并标注假设。 |

### 2.4 外檐斗栱 / 构件

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| DG-001 | `column_head_puzuo_type` | topology_or_rule | 七铺作、双杪双下昂 | DIRECT/B_SUPPORT | READY | 形制稳定。 |
| DG-002 | `intercolumn_puzuo_type` | topology_or_rule | 五铺作、双杪偷心 | DIRECT/B_SUPPORT | READY | 形制稳定。 |
| DG-101 | `column_ludou_top_width_mm` | observed_as_measured | **475.1** | DIRECT_VERIFIED | READY | 表2-26。 |
| DG-102 | `column_ludou_bottom_width_mm` | observed_as_measured | **327.1** | DIRECT_VERIFIED | READY | 表2-26。 |
| DG-103 | `column_ludou_top_depth_mm` | observed_as_measured | **446.3** | DIRECT_VERIFIED | READY | 表2-26。 |
| DG-104 | `column_ludou_bottom_depth_mm` | observed_as_measured | **305.5** | DIRECT_VERIFIED | READY | 表2-26。 |
| DG-105 | `bottom_long_kai_dou_top_width_mm` | observed_as_measured | **255.56** | DIRECT_VERIFIED | READY | 表2-28。 |
| DG-106 | `bottom_long_kai_dou_bottom_width_mm` | observed_as_measured | **178.56** | DIRECT_VERIFIED | READY | 表2-28。 |
| DG-107 | `single_long_kai_dou_top_width_mm` | observed_as_measured | **236.2** | DIRECT_VERIFIED | READY | 表2-28。 |
| DG-108 | `cross_dou_top_width_mm` | observed_as_measured | **255.2** | DIRECT_VERIFIED | READY | 表2-28。 |
| DG-109 | `cross_dou_top_depth_mm` | observed_as_measured | **240.0** | DIRECT_VERIFIED | READY | 表2-28。 |
| DG-110 | `first_second_jump_total_fen` | reconstructed_design_candidate | **48分** | DIRECT_REPORT_INFERRED | READY | 报告推荐结论。 |
| DG-111 | `third_fourth_jump_total_fen` | reconstructed_design_candidate | **47分** | DIRECT_REPORT_INFERRED | READY | 报告推荐结论。 |
| DG-112 | `lower_ang_run_fen` | reconstructed_design_candidate | **47分** | DIRECT_REPORT_INFERRED | READY | 下昂基准三角形。 |
| DG-113 | `lower_ang_rise_fen` | reconstructed_design_candidate | **21分** | DIRECT_REPORT_INFERRED | READY | 同上。 |
| DG-114 | `small_dou_unified_design_rule` | reconstructed_design_candidate | **HOLD** | A_BRIDGE_VERIFIED | REVIEW | “主报告p107”页码归属已撤销；待重新定位原论证或保持外部论文桥接。 |

### 2.5 主体梁架

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| RF-001 | `frame_system` | topology_or_rule | 复合式六椽栿通檐用两柱、彻上露明 | DIRECT_VERIFIED | READY | 主报告2.3。 |
| RF-002 | `lower_six_chuanfu_width_mm` | observed_as_measured | **493.5** | DIRECT_VERIFIED | READY | 表2-38均值。 |
| RF-003 | `lower_six_chuanfu_tenon_thickness_mm` | observed_as_measured | **375** | DIRECT_VERIFIED | READY | 表2-38。 |
| RF-004 | `lower_six_chuanfu_max_thickness_mm` | observed_as_measured | **444** | DIRECT_VERIFIED | READY | 表2-38。 |
| RF-005 | `upper_six_chuanfu_width_mm` | observed_as_measured | **334** | DIRECT_VERIFIED | READY | 表2-38。 |
| RF-006 | `upper_six_chuanfu_tenon_thickness_mm` | observed_as_measured | **209** | DIRECT_VERIFIED | READY | 表2-38。 |
| RF-007 | `upper_six_chuanfu_max_thickness_mm` | observed_as_measured | **240.5** | DIRECT_VERIFIED | READY | 表2-38。 |

### 2.6 架道 / 屋架水平控制

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| FR-001 | `frame_depth_1_observed_mm` | observed_as_measured | **1747.6** | DIRECT_VERIFIED | READY | 表2-51。 |
| FR-002 | `frame_depth_2_observed_mm` | observed_as_measured | **1757.2** | DIRECT_VERIFIED | READY | 表2-51。 |
| FR-003 | `frame_depth_3_observed_mm` | observed_as_measured | **1841** | DIRECT_VERIFIED | READY | 表2-51。 |
| FR-004 | `frame_depth_1_design_mm` | reconstructed_design_candidate | **1759.5** | DIRECT_REPORT_INFERRED | READY | 5.75尺。 |
| FR-005 | `frame_depth_2_design_mm` | reconstructed_design_candidate | **1759.5** | DIRECT_REPORT_INFERRED | READY | 5.75尺。 |
| FR-006 | `frame_depth_3_design_mm` | reconstructed_design_candidate | **1836** | DIRECT_REPORT_INFERRED | READY | 6尺。 |
| FR-007 | `roof_horizontal_sequence_fen` | reconstructed_design_candidate | **120 / 115 / 210** | DIRECT_REPORT_INFERRED | READY | 举折示意图。 |

### 2.7 山面出际

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| OUT-001 | `gable_projection_east_mm` | observed_as_measured | **1385** | DIRECT_VERIFIED | READY | 槫中心线→博风板内皮。 |
| OUT-002 | `gable_projection_west_mm` | observed_as_measured | **1411** | DIRECT_VERIFIED | READY | 同定义。 |
| OUT-003 | `gable_projection_design_fen` | reconstructed_design_candidate | **92分** | DIRECT_REPORT_INFERRED | READY | 约4尺6寸。 |
| OUT-004 | `rafter_head_to_column_center_mm` | observed_as_measured | **2677.5** | A_BRIDGE_VERIFIED | REVIEW | 不是主报告印刷p147；继续保留桥接状态。 |
| OUT-005 | `rafter_head_to_liaoyanfang_mm` | observed_as_measured | **1224** | A_BRIDGE_VERIFIED | REVIEW | 同上。 |
| OUT-006 | `bracket_outjump_mm` | observed_as_measured | **1453.5** | A_BRIDGE_VERIFIED | REVIEW | 同上。 |

### 2.8 举折 / Z向屋架

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| ROOF-001 | `rise_interval_A_observed_mm` | observed_as_measured | **383.5** | DIRECT_VERIFIED | READY | 表2-52。 |
| ROOF-002 | `rise_interval_B_observed_mm` | observed_as_measured | **602.3** | DIRECT_VERIFIED | READY | 表2-52。 |
| ROOF-003 | `rise_interval_C_observed_mm` | observed_as_measured | **1249.5** | DIRECT_VERIFIED | READY | 表2-52。 |
| ROOF-004 | `rise_interval_A_design_fen` | reconstructed_design_candidate | **25分** | DIRECT_REPORT_INFERRED | READY | 99.74%吻合。 |
| ROOF-005 | `rise_interval_B_design_fen` | reconstructed_design_candidate | **40分** | DIRECT_REPORT_INFERRED | READY | 98.41%吻合。 |
| ROOF-006 | `rise_interval_C_design_fen` | reconstructed_design_candidate | **82分** | DIRECT_REPORT_INFERRED | READY | 99.59%吻合。 |
| ROOF-007 | `eave_to_lower_purlin_rise_fen` | reconstructed_design_candidate | **88分** | DIRECT_REPORT_INFERRED | READY | 考虑替木。 |
| ROOF-008 | `lower_to_upper_purlin_rise_fen` | reconstructed_design_candidate | **61分** | DIRECT_REPORT_INFERRED | READY | 同上。 |
| ROOF-009 | `upper_to_ridge_purlin_rise_fen` | reconstructed_design_candidate | **82分** | DIRECT_REPORT_INFERRED | READY | 同上。 |
| ROOF-010 | `total_roof_rise_fen` | reconstructed_design_candidate | **231分** | DIRECT_REPORT_INFERRED | READY_HIGH_CAUTION | 报告明确不把举折推算提升为定论。 |
| ROOF-011 | `total_roof_rise_candidate_mm` | reconstructed_design_candidate | **≈3534.3** | DIRECT_REPORT_INFERRED_DERIVED | READY_HIGH_CAUTION | 231×15.3。 |
| ROOF-012 | `upper_purlin_drop_fen` | reconstructed_design_candidate | **20分** | DIRECT_REPORT_INFERRED | READY | 折屋解释。 |
| ROOF-013 | `lower_purlin_additional_drop_fen` | reconstructed_design_candidate | **8分** | DIRECT_REPORT_INFERRED | READY | 折屋解释。 |

### 2.9 形变 / 现状模型

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| DEF-001 | `bracket_inward_outward_vertical_mm` | observed_as_measured | **0–66** | DIRECT_VERIFIED | READY | 外檐柱头铺作。 |
| DEF-002 | `bracket_inward_outward_parallel_mm` | observed_as_measured | **0–39** | DIRECT_VERIFIED | READY | 同上。 |
| DEF-003 | `bracket_settlement_mm` | observed_as_measured | **49–126** | DIRECT_VERIFIED | READY | 令栱上替木下沉。 |
| DEF-004 | `roof_purlin_relative_settlement_mm` | observed_as_measured | **0–79** | DIRECT_VERIFIED | READY | 扣除斗栱下沉后。 |
| DEF-005 | `purlin_inward_outward_mm` | observed_as_measured | **0–34** | DIRECT_VERIFIED | READY | 进深方向。 |
| DEF-006 | `purlin_roll_mm` | observed_as_measured | **10–60** | DIRECT_VERIFIED | READY | 槫滚动。 |
| DEF-007 | `max_six_chuanfu_deflection_mm` | observed_as_measured | **56** | DIRECT_VERIFIED | READY | 西缝最大；挠跨比约1/191。 |

### 2.10 历史修缮 / 状态分层

| ID | Parameter key | 语义层 | V002候选 | Evidence | P1.3 readiness | 备注 |
|---|---|---|---|---|---|---|
| HIS-001 | `repair_events_confirmed` | evidence_rule | 1151 / 1540 / 1752前后 / 1811–1816 / 1895–1904 / 1949后局部维修 | DIRECT_VERIFIED | READY | 主报告印刷p31。 |
| HIS-002 | `component_level_963_originality` | evidence_rule | **PARTIAL / UNKNOWN BY COMPONENT** | DIRECT_VERIFIED_GAP | HOLD | P1.3按构件分级。 |

## 3. 理想模型语义锁定

主报告印刷p106明确指出：`report_ideal_model`：

- 不是“刚建成时真实状态”的自动等价物；
- 不是现状测绘模型；
- 可能包含不同历史时期改造设计的成分。

因此后续必须使用三个独立层：

1. `observed_as_measured`
2. `report_ideal_model`
3. `reconstructed_963_candidate`

禁止把第2层直接命名为“963原貌”。

## 4. V002 纠错记录

- 主报告印刷p147实际是彩画作“叠压痕迹”，撤销“p147直接支持檐部三段尺度”的说法。
- 主报告印刷p107实际是斗栱层理想模型与现状叠合图，撤销“p107直接支持小斗同规格”的页码归属。
- `2677.5 / 1224 / 1453.5mm` 继续保留 `A_BRIDGE_VERIFIED`，不升级为 DIRECT。
- `small_dou_unified_design_rule` 降为 `A_BRIDGE / REVIEW`。

## 5. V002 对 P1.3 的边界

### 已足够进入分级审核

- 年代/身份；
- 平面柱网；
- 营造尺候选；
- 主要斗栱实测；
- 主体梁架拓扑与部分构件尺寸；
- 架道；
- 山面出际；
- 举折实测与报告推定；
- 现状形变；
- 修缮时间线。

### 必须在 P1.3 显式保留的不确定性

- 963原设计柱高与统一Z基准；
- 角柱生起只能作为报告“猜测”；
- 举折231分虽然高吻合，但报告本身拒绝把它提升为定论；
- 转角45°节点精确坐标仍不足；
- 逐构件“963原构/后世替换”分层尚不完整；
- 报告理想模型不能直接等同963初建状态。

## 6. 结论

V002 已达到 **P1.3 Gate Review 输入矩阵**的要求，但仍不是正式生产参数。是否把某个候选值写入未来 Blender 参数，只能在 P1.3 完成“已证实 / 高可信推断 / 合理补全 / 未知”的正式分级后决定。
