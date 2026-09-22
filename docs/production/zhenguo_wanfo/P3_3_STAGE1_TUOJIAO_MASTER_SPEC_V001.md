# P3.3 V002 Stage 1｜托脚 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-100**  
**日期：2026-09-22**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019｜SRC-ZG-WF-001 + 山西文物数字博物馆·万佛殿专题优先**  
**视觉门：PASS WITH GEOMETRY BOUNDARY**  
**A1原页门：PASS WITH SOURCE-INTERNAL NUMERIC CONFLICT**  
**任务性质：正式锁定规格；不等于T-027工程执行授权**

## 1. Component Identity

- 中文名：托脚
- component id：`CMP-FRAME-TUOJIAO-001`
- master id：`CMP-FRAME-TUOJIAO-001_MASTER`
- master version：V001
- V008 physical instances：12
- MAIN_FRAME role：8
- GABLE role：4
- family：斜向梁架支撑构件

锁定一个 canonical 托脚 Master family。

MAIN_FRAME / GABLE 仅作为 assembly / placement role；当前没有直接证据支持拆成不同本体 geometry Variant。

## 2. A1 Direct Source Evidence

SRC-ZG-WF-001：

### PDF p89–90 / printed p74–75 / §2.3.1.8 / Table 2-45

报告直接确认：
- 前后上平槫、下平槫托脚8根；
- 东西山前后缝下平槫托脚4根；
- 全殿托脚12根；
- 托脚测量记录11组，其中1组广/厚均“未及”。

10组可见完整样本：
- 249 × 152
- 245 × 151
- 245 × 152
- 244 × 149
- 250 × 151
- 250 × 154
- 214 × 151
- 213 × 158
- 212 × 150
- 219 × 173 mm

报告正式公布：
- width = **237.1 mm**
- thickness = **153.7 mm**
- converted_fen = 15.50 × 10.05
- rounded_fen = 15 × 10

### Numeric conflict

10组可见完整行算术复算：
- width = **234.1 mm**
- thickness = **154.1 mm**

因此锁定：
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = true`
- `REPORT_PUBLISHED_MEAN = 237.1 × 153.7 mm`
- `VISIBLE_ROWS_RECOMPUTED_MEAN = 234.1 × 154.1 mm / AUDIT_ONLY`
- `SILENT_ARITHMETIC_CORRECTION = PROHIBITED`

## 3. Measurement Contract

measurement_table_row_count = 11  
complete_visible_sample_count = 10  
unmeasured_visible_row_count = 1

canonical section：
- width_mm = **237.1**
- thickness_mm = **153.7**

classification：
- `REPORT_PUBLISHED_MEAN_WITH_INTERNAL_ARITHMETIC_CONFLICT`
- source = SRC-ZG-WF-001
- observed-family statistic published by source
- historical_claim = false

sample_to_instance_mapping = **UNKNOWN**

禁止将11组记录静默对应到12根具体实例。

报告分值仅：
- REPORT_INFERRED / METADATA_ONLY
- geometry_use_count = 0

## 4. A2 Official Same-building Semantics

山西文物数字博物馆·万佛殿专题明确：

> 四椽栿两端有托脚作支撑。

该内容锁定托脚的结构语义，但不锁定：
- exact contact XYZ
- exact end contour
- exact joint geometry
- exact load-path numerical model

## 5. Length / Angle / Placement Boundary

historical_full_length_mm = null / UNKNOWN  
exact_placement_angle_deg = null / UNKNOWN

Stage1 canonical_reference_length_mm = **1000.0**

1000mm仅为：
- PROJECT_RULE
- ENGINEERING_REFERENCE
- NON_HISTORICAL_REFERENCE
- CANONICAL_REFERENCE_ONLY
- replaceable = true
- historical_claim = false

整殿真实实例：
- length later derived from explicit assembly endpoints；
- orientation later derived from explicit assembly endpoints；
- 不允许从剖面图目测角度后硬编码进 Master。

Hard fail：
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `FIXED_MASTER_ANGLE`
- `FIXED_HISTORICAL_LENGTH_WITHOUT_A1_EVIDENCE`

## 6. Geometry Mode

Geometry mode：
**BOUNDED_LONG_MEMBER_OUTER_ENVELOPE**

Canonical local coordinate：
- +X = member longitudinal axis
- +Y = width / 广
- +Z = thickness / 厚
- handedness = right-handed

Origin：
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform：
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

Stage1 canonical body：
**1000 × 237.1 × 153.7 mm**

“斜”属于 assembly placement，不烘焙为固定历史角度。

## 7. Role Policy

- role = MAIN_FRAME / GABLE
- MAIN_FRAME count = 8
- GABLE count = 4
- role 不改变 canonical body section；
- role 不自动改变端部；
- role 不自动引入榫卯；
- role 不赋予固定倾角。

若未来A1图纸/修缮档案证明两类存在稳定本体差异，再升级为 Variant。

## 8. Assembly Semantics

允许锁定：
- member_type = DIAGONAL_FRAME_SUPPORT
- official_same_building_semantic = SUPPORTS_ENDS_OF_FOUR_CHUANFU
- registry placement roles = MAIN_FRAME / GABLE
- exact endpoint/contact geometry = UNKNOWN / ASSEMBLY_ENDPOINT_TO_BE_RESOLVED

不得把旧P2 `FRAME_SUPPORT` proxy mesh直接重命名为托脚本体。

## 9. Joinery / End Geometry Boundary

当前：
- end profile = UNKNOWN
- mortise/tenon = UNKNOWN
- notch/groove = UNKNOWN
- hidden connection = UNKNOWN
- stage1 detailed cut geometry = false

《营造法式》比较栏只作为 COMPARATIVE / METADATA，不直接驱动万佛殿托脚几何。

## 10. Geometry Prohibitions

V001 不得加入：
- 依据低等级来源推测的端部；
- 依据《营造法式》直接复制的榫卯；
- 目测倾角；
- 虚构历史全长；
- MAIN_FRAME/GABLE无证据本体差异；
- 11组样本到12实例的假映射；
- 1000mm building-length leakage；
- 15分×10分直接驱动几何；
- 963原始设计尺寸声明；
- 对237.1×153.7与234.1×154.1冲突的静默消解。

## 11. First-Article Validation Requirements

下一工程首件至少验证：

1. component/master id唯一；
2. V008托脚=12；
3. MAIN_FRAME=8；
4. GABLE=4；
5. table rows=11；
6. complete visible samples=10；
7. one row unmeasured；
8. raw visible samples retained；
9. sample_to_instance_mapping=UNKNOWN；
10. report-published width=237.1；
11. report-published thickness=153.7；
12. recomputed audit width=234.1；
13. recomputed audit thickness=154.1；
14. source internal conflict=true；
15. silent arithmetic correction prohibited；
16. report fen metadata only；
17. historical length=null；
18. reference length=1000/non-historical；
19. exact angle=null；
20. MAIN_FRAME/GABLE same body geometry signature；
21. A2 four-chuanfu support semantic retained；
22. exact endpoints unresolved；
23. no joinery cut；
24. X/Y/Z bbox；
25. canonical origin/transform；
26. length mutation only X；
27. width mutation only Y；
28. thickness mutation only Z；
29. role mutation no body change；
30. independent reopen；
31. deterministic semantic restore；
32. no REFERENCE_LENGTH_LEAKS_INTO_BUILDING；
33. no FIXED_MASTER_ANGLE；
34. no SILENT_HISTORICIZATION；
35. no SILENT_ARITHMETIC_CORRECTION；
36. no UNDECLARED_PARAMETRIC_COMPLETION；
37. no MASTER_WITHOUT_EVIDENCE_BINDING；
38. D-076 + D-099 traceable。

## 12. Locked Decision

D-100 正式锁定：

> 一个 `CMP-FRAME-TUOJIAO-001_MASTER`；Stage1 canonical section使用SRC-ZG-WF-001正式公布的237.1×153.7mm，同时永久记录可见10组原始行复算234.1×154.1mm及 `SOURCE_INTERNAL_NUMERIC_CONFLICT`；MAIN_FRAME 8根与GABLE 4根只作为assembly/placement roles；历史全长、精确倾角、端点、端部加工和榫卯保持UNKNOWN/DEFERRED；1000mm仅为非历史canonical reference。

本 V001 **不授权 T-027 工程执行**。

下一步可以设计/建立 T-027 Task Contract，但在 Product Owner 明确授权“开始 T-027”之前：
- 不启动 Blender；
- 不创建 production execution branch/PR；
- 不生成首件；
- T-018 继续 HOLD。

