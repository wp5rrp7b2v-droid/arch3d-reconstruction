# P3.3 V002 Stage 1｜四椽栿 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-069**  
**日期：2026-09-19**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**任务性质：规格设计与锁定；尚未创建 Codex T-###；尚未运行 Blender**

## 1. Master Identity

- 中文名：四椽栿
- canonical component id：CMP-FRAME-FOUR-CHUANFU-001
- canonical master id：CMP-FRAME-FOUR-CHUANFU-001_MASTER
- master version：V001
- real historical component：YES
- V008 physical instances：四椽栿-东缝、四椽栿-西缝
- instance count：2
- source registry：P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json / V008

旧 P3.1 的 P1-REVIEW-FOUR-CHUANFU 保留为历史审查记录，不回写、不删除。P3.3 V002 通过新的直接原页证据绑定将四椽栿升级为可生产 Master。

## 2. Authoritative Evidence

直接原页：SRC-ZG-WF-001，PDF p82 / 印刷 p67，2.3.1.2 四椽栿，表2-39，图2-40。

正式 evidence binding：
docs/evidence/zhenguo_wanfo/P3_3_FOUR_CHUANFU_DIRECT_SOURCE_BINDING_V001.md

报告正文直接确认：
- 东缝1根；
- 西缝1根；
- 共2根；
- 四椽栿与其下的上六椽栿之间垫隔架单栱一组；
- 其下不用栌斗；
- 仅由一散斗承托。

上述装配语义属于 Stage 2 输入，不自动转化成 Master 本体上的槽口、榫卯或精确接口坐标。

## 3. Measured Section Contract

表2-39两组实测：

| 记录 | 广 | 厚 |
|---|---:|---:|
| 实测组 A | 413 mm | 295 mm |
| 实测组 B | 440 mm | 309 mm |
| 均值 | 426.5 mm | 302 mm |

Canonical Master V001 使用：
- width_mm = 426.5
- thickness_mm = 302.0

分类：
- CONFIRMED / observed_as_measured_mean
- source layer：DIRECT_PRIMARY
- production use：OBSERVED_REFERENCE_OUTER_ENVELOPE

A/B 两组值必须保存为 evidence metadata，但不得未经证据分配给东缝或西缝。因此 V001 不创建“东缝截面 Variant / 西缝截面 Variant”。

报告给出：
- 广：27.9分 → 取整28分；
- 厚：19.7分 → 取整20分。

V001 仅保存为 REPORT_INFERRED / DESIGN_ANALYSIS_METADATA，geometry_use_count = 0；不得把28分×20分当作963历史设计截面。

## 4. Length Contract

historical_full_length_mm = null

状态：
- classification：UNKNOWN
- production use：DO_NOT_LOCK
- historical claim：false

为了让 Master 本体能够独立构建、变更测试、重开与审核，延续六椽栿已经验证过的中性长构件 reference policy：

canonical_reference_length_mm = 1000.0

该值必须标记为：
- PROJECT_RULE
- ENGINEERING_REFERENCE
- NON_HISTORICAL_REFERENCE_REALIZATION
- CANONICAL_REFERENCE_ONLY
- replaceable = true
- historical_claim = false

realization_length_mm = canonical_reference_length_mm，仅用于 canonical Master reference binary。

进入真实装配时，必须由 Stage 2 / Stage 4 的明确装配端点产生 building-specific geometry length，并标记为 EXPLICIT_DERIVED_GEOMETRY / PROJECT_RULE，而不是历史实测长度或963设计长度。

1000mm 一旦泄漏进真实整殿实例，触发 REFERENCE_LENGTH_LEAKS_INTO_BUILDING。

## 5. Geometry Mode

Geometry mode：BOUNDED_LONG_MEMBER_OUTER_ENVELOPE  
LOD：EVIDENCE_BOUNDED_MEDIUM_LOD  
Unit：mm

Canonical coordinate：
- +X：构件纵向
- +Y：广 / 水平截面宽度
- +Z：厚 / 垂直截面方向
- handedness：right-handed

Origin：
longitudinal_midpoint / transverse_center / lower_reference_plane

Canonical transform：
- Location = (0,0,0)
- Rotation = (0,0,0)
- Scale = (1,1,1)

Canonical body 只建立：
realization_length × 426.5 × 302 的 bounded outer envelope。

该几何表达的是当前证据支持的构件主体外包络参考，不是整根四椽栿通长精确断面、边角、磨损或历史加工形态的声明。

## 6. Geometry Prohibitions

V001 禁止生成：
- 榫头；
- 卯口；
- 散斗槽；
- 隔架单栱几何；
- 栌斗；
- 隐藏连接；
- 未量化局部削减；
- 无证据端部轮廓；
- 无证据起拱；
- 把现状挠曲直接烘焙成原始几何；
- 木材翘曲 / 劈裂 / 腐朽 / 磨损的写实变形；
- 依据一般古建知识补出的“典型四椽栿”细节。

unsupported_geometry_count = 0。

## 7. Historical / Time-layer Boundary

必须保持 observed_as_measured、report_ideal_model、reconstructed_963_candidate 三层隔离。

当前：
- 426.5 × 302mm = 现状实测均值；
- 28分 × 20分 = 报告尺度归整分析；
- 963原始截面 = 未证明；
- HIS-002 = individual originality UNKNOWN。

## 8. Variant Rule

V001 允许的 Variant axes：
- length_mm：后续 assembly-derived geometry length；
- evidence_supported_section_set：仅在未来证据明确时开放。

以下不构成 Variant：
- 东缝 / 西缝位置；
- world coordinates；
- world rotation；
- instance number；
- “东缝/西缝”名称本身。

当前禁止把413×295或440×309强行指定给任一东西缝实例。

## 9. Interface Contract

几何端点：
- END_NEG_X：X = -L/2，Y = 0，Z = thickness/2
- END_POS_X：X = +L/2，Y = 0，Z = thickness/2

Semantic-only assembly interfaces，坐标先保持 ASSEMBLY_OWNED / UNKNOWN：
- SUPPORT_FROM_SAN_DOU
- RELATION_TO_UPPER_SIX_CHUANFU
- SPACER_SINGLE_GONG_RELATION

报告“由一散斗承托”不等于当前可锁一个精确三维支承点。Stage 2 再确定接口位置。

## 10. Reuse / Generator Policy

允许复用 T-013 已验证的长构件生成机制思想：
- 参数驱动外包络；
- canonical transform 检查；
- deterministic rebuild；
- independent reopen；
- length mutation；
- review package 组织方式。

禁止：
- 把上/下六椽栿 Master 复制后改名；
- 共用其 component id；
- 继承六椽栿截面参数；
- 继承六椽栿 building placement；
- 继承 P2 PRIMARY_FRAME proxy mesh。

建议后续实现复用/扩展通用 long_member_master_common，而不是为每个梁类复制一套不可维护代码。

## 11. Required Parameters

正式 params 至少包含：
- component_id
- master_id
- master_version
- historical_full_length_mm = null
- canonical_reference_length_mm = 1000.0
- realization_length_mm = 1000.0
- width_mm = 426.5
- thickness_mm = 302.0
- measured_section_samples：A=413×295；B=440×309
- sample_to_instance_mapping = UNKNOWN
- report_design_analysis：28 fen / 20 fen / geometry_use_count=0
- known_unknowns[]
- interpretation_boundary[]
- historical_state
- originality_status
- variant_axes[]
- placement_only_attributes[]
- interface_contract
- generator_path
- canonical_asset_path
- review_asset_paths[]

## 12. First-Article Validation Contract

未来 Codex 首件必须至少 PASS：
1. component id / master id 唯一；
2. source binding 精确指向 PDF p82 / 印刷 p67 / 表2-39；
3. V008 四椽栿物理实例 = 2；
4. width = 426.5mm；
5. thickness = 302mm；
6. 两组实测值保存为 metadata；
7. A/B 未被静默映射到东/西缝；
8. report 28/20分仅 metadata，geometry use = 0；
9. historical full length 始终 null；
10. 1000mm 只属于 canonical reference；
11. body X extent = realization length；
12. body Y extent = width；
13. body Z extent = thickness；
14. canonical origin / transform 正确；
15. unsupported geometry = 0；
16. P2 proxy geometry use count = 0；
17. length mutation 只改变 X extent；
18. width mutation 只改变 Y extent；
19. thickness mutation 只改变 Z extent；
20. mutation 后 canonical rebuild 精确恢复；
21. independent reopen PASS；
22. semantic snapshot 与 params 一致；
23. review FRONT / SIDE / TOP / AXON 完整；
24. DIMENSION_PARAMETER_SUMMARY 完整；
25. EVIDENCE_UNCERTAINTY_SUMMARY 完整；
26. no REFERENCE_LENGTH_LEAKS_INTO_BUILDING；
27. no SILENT_HISTORICIZATION；
28. no MASTER_WITHOUT_EVIDENCE_BINDING。

## 13. Review Package

首件至少生成6张审核图：
1. FRONT
2. SIDE
3. TOP
4. AXON
5. DIMENSION_PARAMETER_SUMMARY
6. EVIDENCE_UNCERTAINTY_SUMMARY

视觉审核重点：
- 梁体方向正确；
- 426.5×302 截面比例正确；
- reference length 明确标注非历史；
- 没有虚构榫卯、槽口、散斗、隔架栱；
- 不让简单外包络误导为“精确历史复原”。

## 14. Locked Production Boundary

D-069 只锁定本 Master Spec。

D-069 不授权：
- Codex 开始建模；
- 创建 Blender binary；
- 新 T-###；
- 整殿实例长度；
- Stage 2 接口落位；
- T-018；
- RZ / FV / T-020；
- CP-03；
- PR #3 / #6 merge；
- P3.3 PASS。

下一步需单独授权：
**创建四椽栿 Master First Article 的 Codex 工程任务。**
