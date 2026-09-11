# P1.2｜平遥镇国寺万佛殿｜正式参数候选矩阵 V001

Status: PRE-P1.3 / NOT PRODUCTION-LOCKED  
Date: 2026-09-11  
Case: 山西平遥镇国寺万佛殿  
Purpose: 将 P1.2 Batch 01–05 的证据转为结构化参数候选，供 P1.2 Gate Review 与 P1.3 证据分级使用。本文**不是 Blender 正式参数 JSON**。

## 0. 参数语义规则

### 参数层

- `observed_as_measured`：现状实测或正式论文明确转引的精测值；允许包含千年形变、修缮与测量状态。
- `reconstructed_design_candidate`：对963年设计状态的尺度/模数候选；属于推定，不等于现状实测。
- `topology_or_rule`：构件之间的连接、数量、层级、铺作类型等拓扑规则。

### 证据状态

- `DIRECT_VERIFIED`：已直接核读《精细测绘报告》原页；**当前 V001 暂无**。
- `A_BRIDGE_VERIFIED`：正式论文明确转引主报告/测量研究数据，或转载主报告图版。
- `REPORT_INFERRED`：主报告/正式研究根据实测提出的设计推定。
- `B_SUPPORT`：机构数字展示等强佐证。
- `C_SUPPORT`：二手科普/媒体，仅用于范围校验。
- `HYPOTHESIS`：后续作者的解释模型。
- `UNKNOWN`：不足以形成参数。

### 参数就绪状态

- `READY_FOR_P1.3_REVIEW`：可进入 P1.3 分级审核，但仍不等于生产锁定。
- `TOPOLOGY_READY`：拓扑可进入 P1.3；精确几何仍待补证。
- `HOLD_DIRECT_PAGE_VERIFY`：高质量桥接数据已存在，但须回主报告原页复核。
- `HOLD_HIGH_RISK`：存在关键测量基准/历史状态问题。
- `HOLD_CONFLICT_OR_DEFINITION`：数值/起止点/术语定义未统一。
- `UNKNOWN`：暂不参数化。

---

## 1. 平面与柱网

| ID | Parameter key | 层 | 候选值 / 规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| PM-001 | `bay_count_front` | topology_or_rule | 3 | A/B | READY_FOR_P1.3_REVIEW | 面阔三间，多来源一致。 |
| PM-002 | `bay_count_depth` | topology_or_rule | 3 | A/B | READY_FOR_P1.3_REVIEW | 进深三间六椽。 |
| PM-003 | `overall_width_mm` | observed_as_measured | **11492.7** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 肖旻2024表1转引《镇国寺报告》精测数据；优先于公开概述11.58m。 |
| PM-004 | `overall_depth_mm` | observed_as_measured | **10688.2** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 正式论文转引精测数据；优先于公开概述10.78m。 |
| PM-005 | `front_center_bay_mm` | observed_as_measured | **4481.3** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 精测层。 |
| PM-006 | `front_side_bay_mm` | observed_as_measured | **3505.7** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 论文表中“转角两次间”代表值，需原报告确认单侧/均值定义。 |
| PM-007 | `depth_center_bay_mm` | observed_as_measured | **3676.8** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 精测层。 |
| PM-008 | `perimeter_column_count` | topology_or_rule | **12** | B_SUPPORT + 多源一致 | READY_FOR_P1.3_REVIEW | 殿内无内柱。 |
| PM-009 | `interior_column_count` | topology_or_rule | **0** | B_SUPPORT + 多源一致 | READY_FOR_P1.3_REVIEW | 与“六椽栿通檐用两柱”体系一致。 |

### P1.3 注记

平面宏观尺度已经接近可审核状态，但 V001 仍保留 `HOLD_DIRECT_PAGE_VERIFY`，因为项目要求正式参数最好回到主报告测点定义，而不是只依赖后续论文表格。

---

## 2. 柱与垂直基准

| ID | Parameter key | 层 | 候选值 / 规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| Z-001 | `column_diameter_nominal_mm` | reconstructed_design_candidate | **≈460** | REPORT_INFERRED | HOLD_DIRECT_PAGE_VERIFY | 肖旻2024按报告数据讨论约1.5营造尺；需主报告柱径统计原表。 |
| Z-002 | `column_height_current_mm` | observed_as_measured | **≈3420** | A_BRIDGE_VERIFIED / approximate | HOLD_HIGH_RISK | 报告只称约3.42m；原始地坪、柱础未明。 |
| Z-003 | `column_height_963_design_mm` | reconstructed_design_candidate | **UNKNOWN** | UNKNOWN | UNKNOWN | 不得把3420直接当963设计柱高。 |
| Z-004 | `corner_column_rise_mm` | observed_as_measured / design candidate | **≈50（待核）** | C/B_SUPPORT | HOLD_DIRECT_PAGE_VERIFY | 二手/机构资料常见0.05m；必须核2.1.3原页测量定义。 |
| Z-005 | `column_side_slope_rule` | topology_or_rule | 檐柱存在侧脚 | B_SUPPORT + 多源一致 | TOPOLOGY_READY | 量值仍未知。 |
| Z-006 | `global_z_datum` | topology_or_rule | **UNKNOWN** | UNKNOWN | HOLD_HIGH_RISK | 必须明确台基/室内地坪/柱脚/柱头的统一起算面。 |

### P1.3 注记

Z轴是当前最大风险域。只要 `global_z_datum` 和 `column_height_963_design_mm` 未建立，正式立面比例不得锁定。

---

## 3. 营造尺 / 材分候选

| ID | Parameter key | 层 | 候选值 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| MOD-001 | `yingzao_chi_mm` | reconstructed_design_candidate | **≈306** | REPORT_INFERRED | READY_FOR_P1.3_REVIEW | 《镇国寺报告》体系/肖旻2024的设计推定，不是直接实测。 |
| MOD-002 | `fen_mm` | reconstructed_design_candidate | **≈15.3** | REPORT_INFERRED | READY_FOR_P1.3_REVIEW | 由306mm与材分关系推定。 |
| MOD-003 | `single_cai_width_mm` | reconstructed_design_candidate | **≈214** | REPORT_INFERRED | READY_FOR_P1.3_REVIEW | 14份。 |
| MOD-004 | `single_cai_thickness_mm` | reconstructed_design_candidate | **≈153** | REPORT_INFERRED | READY_FOR_P1.3_REVIEW | 10份。 |
| MOD-005 | `full_cai_height_mm` | reconstructed_design_candidate | **≈321** | REPORT_INFERRED | READY_FOR_P1.3_REVIEW | 21份足材候选。 |

### P1.3 注记

这组参数可以作为“963设计候选模型”的一条竞争解释，但 P1.3 必须明确标成 `高可信推断` 或更低等级，不能与现状精测混放。

---

## 4. 外檐铺作拓扑

| ID | Parameter key | 层 | 候选值 / 规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| DG-001 | `column_head_puzuo_type` | topology_or_rule | 七铺作、双杪双下昂 | B_SUPPORT + 学术一致 | READY_FOR_P1.3_REVIEW | 形制稳定。 |
| DG-002 | `intercolumn_puzuo_type` | topology_or_rule | 五铺作、双杪偷心 | B_SUPPORT + 学术一致 | READY_FOR_P1.3_REVIEW | 形制稳定。 |
| DG-003 | `corner_puzuo_type` | topology_or_rule | 正身七铺作双杪双下昂；45°角华栱两跳托双昂，再出由昂；里转三跳第三跳承角梁 | B_SUPPORT / 学术解释 | TOPOLOGY_READY | 精确45°尺寸仍缺。 |
| DG-004 | `small_dou_design_unified` | reconstructed_design_candidate | 散斗/齐心斗/交互斗原始设计可能同规格 | REPORT_INFERRED | READY_FOR_P1.3_REVIEW | 正式论文明确回引主报告第107页；属于设计推论。 |

---

## 5. 斗栱构件精测候选

| ID | Parameter key | 层 | 候选值 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| DG-101 | `column_ludou_top_width_mm` | observed_as_measured | **475.1** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 肖旻2024表2回注报告第47页。 |
| DG-102 | `column_ludou_top_depth_mm` | observed_as_measured | **446.3** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 同上。 |
| DG-103 | `column_ludou_bottom_width_mm` | observed_as_measured | **327.1** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 同上。 |
| DG-104 | `column_ludou_bottom_depth_mm` | observed_as_measured | **305.5** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 同上。 |
| DG-105 | `intercolumn_dou_top_width_mm` | observed_as_measured | **255.56** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 回注报告第50页。 |
| DG-106 | `intercolumn_dou_bottom_width_mm` | observed_as_measured | **178.56** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 回注报告第50页。 |
| DG-107 | `large_mangong_actual_length_mm` | observed_as_measured | **1641** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 报告第45页桥接。 |
| DG-108 | `column_nidaogong_actual_length_mm` | observed_as_measured | **1007** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 报告第44页桥接。 |
| DG-109 | `small_mangong_actual_length_mm` | observed_as_measured | **1607** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 报告第45页桥接。 |
| DG-110 | `intercolumn_nidao_guazigong_actual_length_mm` | observed_as_measured | **895** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 报告第44页桥接。 |

### 不进入现状实测层的计算值

下列值由2024论文根据斗底宽/交圈关系计算，不应与直接测值混列：大型慢栱心长1464.5mm、柱头泥道栱心长830.5mm、二跳华栱心长约1464.8mm等。可在后续 `reconstructed_design_candidate` 子表中单列，但 V001 不作为生产控制。

---

## 6. 檐部水平控制

| ID | Parameter key | 层 | 候选值 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| EAV-001 | `rafter_head_to_column_center_mm` | observed_as_measured | **2677.5** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 正式论文回引镇国寺测量研究/报告体系第147页。 |
| EAV-002 | `rafter_head_to_liaoyanfang_mm` | observed_as_measured | **1224** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 起止点明确。 |
| EAV-003 | `bracket_outjump_mm` | observed_as_measured | **1453.5** | A_BRIDGE_VERIFIED | HOLD_DIRECT_PAGE_VERIFY | 与EAV-002相加等于EAV-001。 |
| EAV-004 | `generic_eave_overhang_mm` | — | **DEPRECATED / DO NOT USE** | — | — | “檐出”必须按起止点拆分；二手2.94m不作为控制参数。 |

---

## 7. 屋架拓扑

| ID | Parameter key | 层 | 候选规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| RF-001 | `frame_system` | topology_or_rule | 复合式六椽栿通檐用两柱；彻上露明 | B_SUPPORT + 学术一致 | READY_FOR_P1.3_REVIEW | 宏观结构稳定。 |
| RF-002 | `lower_six_chuanfu_support` | topology_or_rule | 下六椽栿置于二跳华栱之上 | B_SUPPORT | TOPOLOGY_READY | 坐标/断面待主报告。 |
| RF-003 | `upper_six_chuanfu_support` | topology_or_rule | 上六椽栿置于铺作之上，并以令栱承襻间枋 | B_SUPPORT | TOPOLOGY_READY | 同上。 |
| RF-004 | `four_chuanfu_support` | topology_or_rule | 四椽栿两端有托脚；上以驼峰、令栱承平梁 | B_SUPPORT | TOPOLOGY_READY | Batch04正式再出版横剖面支持托脚不宜简化为直接顶槫。 |
| RF-005 | `ridge_support` | topology_or_rule | 平梁上驼峰、蜀柱、叉手承脊槫 | B_SUPPORT | TOPOLOGY_READY | 坐标仍缺。 |
| RF-006 | `purlin_xy_z_observed` | observed_as_measured | **UNKNOWN** | UNKNOWN | UNKNOWN | 需2.3.2/2.3.4原页。 |

---

## 8. 架道、举折与屋面

| ID | Parameter key | 层 | 候选值 / 规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| ROOF-001 | `lower_frame_depth_design` | reconstructed_design_candidate | **5.5足材 ≈ 1765.5mm** | HYPOTHESIS / report-derived input | READY_FOR_P1.3_REVIEW | 肖旻尺度规律解释，不是实测坐标。 |
| ROOF-002 | `roof_rise_mm_institutional` | observed/support | **3510** | B_SUPPORT | HOLD_CONFLICT_OR_DEFINITION | 数字展示给出举高3.51m。 |
| ROOF-003 | `roof_rise_mm_secondary` | observed/support | **≈3600** | C_SUPPORT | HOLD_CONFLICT_OR_DEFINITION | 多份二手资料；与3510相差约90mm。 |
| ROOF-004 | `liaoyanchuan_to_ridge_control_mm` | observed/support | **13620** | B_SUPPORT | HOLD_CONFLICT_OR_DEFINITION | 数字展示称“撩檐槫至脊槫13.62m”，几何定义未核。 |
| ROOF-005 | `roof_ratio_reported` | support | **1:3.88** | B_SUPPORT | HOLD_CONFLICT_OR_DEFINITION | 与13.62/3.51内部一致，但起止点未核。 |
| ROOF-006 | `purlin_step_xy_mm` | observed_as_measured | **UNKNOWN** | UNKNOWN | UNKNOWN | 需2.3.2架道原页。 |
| ROOF-007 | `purlin_step_z_mm` | observed_as_measured | **UNKNOWN** | UNKNOWN | UNKNOWN | 需2.3.4举折原页。 |
| ROOF-008 | `roof_fold_design_candidate` | reconstructed_design_candidate | **UNKNOWN** | UNKNOWN | UNKNOWN | 不采用2025预印本直接锁定。 |

---

## 9. 转角与歇山节点

| ID | Parameter key | 层 | 候选规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| COR-001 | `corner_system_type` | topology_or_rule | 递角栿型高等级殿堂体系 | 学术解释 + B_SUPPORT | READY_FOR_P1.3_REVIEW | 术语层面较稳定。 |
| COR-002 | `corner_huagong_45_topology` | topology_or_rule | 45°出两跳角华栱托双昂，再出由昂 | B_SUPPORT | TOPOLOGY_READY | 精确尺寸未知。 |
| COR-003 | `corner_inner_jump_count` | topology_or_rule | 里转三跳，第三跳承角梁 | B_SUPPORT | TOPOLOGY_READY | 精确节点未知。 |
| COR-004 | `corner_hidden_support_relation` | topology_or_rule | 隐衬角栿与“隐角梁”不能混同；存在递角栿/角梁系统 | A/B context | HOLD_DIRECT_PAGE_VERIFY | 需主报告角部图版完成构件身份校准。 |
| COR-005 | `corner_45_geometry` | observed_as_measured | **UNKNOWN** | UNKNOWN | UNKNOWN | 45°构件中心线/断面/交点缺失。 |

---

## 10. 台基、地坪、墙体与开口

| ID | Parameter key | 层 | 候选值 / 规则 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| ENV-001 | `platform_geometry` | observed_as_measured | **UNKNOWN** | UNKNOWN | UNKNOWN | 主报告3.1.2台基尚未直接读取。 |
| ENV-002 | `interior_floor_elevation` | observed_as_measured | **UNKNOWN** | UNKNOWN | HOLD_HIGH_RISK | 直接影响柱高和全局Z。 |
| ENV-003 | `walling_current_state` | topology_or_rule | 现状大量柱包入墙体 | B_SUPPORT | READY_FOR_P1.3_REVIEW | 是否属于963初建状态需修缮史分层。 |
| ENV-004 | `door_window_963_state` | reconstructed_design_candidate | **UNKNOWN** | UNKNOWN | UNKNOWN | 现状门窗/墙体不可直接回推963。 |

---

## 11. 历史状态参数

| ID | Parameter key | 层 | 当前状态 | 证据状态 | 就绪状态 | 关键说明 |
|---|---|---|---|---|---|---|
| HIST-001 | `construction_date` | metadata | **963 CE / 北汉天会七年** | A | READY_FOR_P1.3_REVIEW | 脊槫底题记支持。 |
| HIST-002 | `repair_1151` | historical layer | 已有补修题记线索 | B/A线索 | READY_FOR_P1.3_REVIEW | 需具体构件对应。 |
| HIST-003 | `repair_1540` | historical layer | 已有补修题记线索 | B/A线索 | READY_FOR_P1.3_REVIEW | 同上。 |
| HIST-004 | `repair_1796_1816` | historical layer | 嘉庆期全面修缮记录 | B | READY_FOR_P1.3_REVIEW | 对现状构件归属影响大。 |
| HIST-005 | `component_originality_map` | historical layer | **UNKNOWN / NOT BUILT** | UNKNOWN | HOLD_HIGH_RISK | P1.3前至少需形成“原构可能性”矩阵。 |

---

## 12. P1.3 前参数成熟度汇总

### A｜可以进入 P1.3 证据分级审核

- 建造年代；
- 3×3间、12外围柱、无内柱；
- 平面精测宏观尺寸（但标记A-Bridge）；
- 柱头/补间/转角铺作的基本形制；
- 主体梁架拓扑；
- 营造尺/材分作为“设计候选解释”；
- 檐部三段水平控制作为A-Bridge候选。

### B｜可以进入 P1.3，但只能作为推断/候选

- 约306mm营造尺；
- 约321mm足材；
- 5.5足材下架深；
- 小斗原设计同规格；
- 柱径约460mm。

### C｜目前禁止生产锁定

- 963原设计柱高；
- 统一Z基准；
- 角柱生起精确量；
- 各槫XY/Z；
- 架道实测统计；
- 举折分段；
- 屋顶3.51m / 3.60m差异；
- 13.62m测量定义；
- 转角45°构件尺寸和节点；
- 台基/原始地坪；
- 963墙体与门窗状态；
- 原构/后修构件映射。

---

## 13. P1.3 Gate 建议阈值

P1.2 在进入 P1.3 前，不要求所有构件都达到毫米级，但至少应满足：

1. **平面控制**：主要柱网和建筑外轮廓有可追溯实测控制；
2. **Z轴控制**：柱头、铺作层、各主要槫、脊槫之间有统一基准或可解释设计候选；
3. **屋面控制**：举折和檐部几何的起止点定义明确；
4. **转角控制**：角部骨架能明确区分“已证实拓扑”和“推断尺寸”；
5. **历史层控制**：至少能说明哪些是963复原目标、哪些为后世现状，不把现状等同初建；
6. **所有生产参数必须带 provenance**：不能出现“数值存在，但不知道从哪来”。

当前 V001 判断：

**尚未满足第2、3、4、5项的最低证据要求，因此不能进入正式3D生产；是否允许进入P1.3 Gate Review，取决于主报告关键原页是否取得并完成直接核读。**

## 14. 下一版触发条件

当获得主报告关键页后，升级为 `P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`：

- 把可核字段升级为 `DIRECT_VERIFIED`；
- 建立统一Z轴；
- 填入架道/举折/转角原始测量；
- 将“现状实测”和“963设计候选”正式拆成两组参数表；
- 为每个字段指定 P1.3 分类候选：已证实 / 高可信推断 / 合理补全 / 未知。
