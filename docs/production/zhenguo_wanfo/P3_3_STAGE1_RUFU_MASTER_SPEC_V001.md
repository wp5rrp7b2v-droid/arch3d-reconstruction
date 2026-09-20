# P3.3 V002 Stage 1｜乳栿 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-083**  
**日期：2026-09-20**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**视觉门：PASS / D-082｜基于同建筑直接照片 Fig.2-42 进入证据复核与 Spec 设计**  
**任务性质：正式锁定规格；允许建立 T-024 工程任务合同，但尚未授权 Blender 执行**

## 1. Component Identity

- 中文名：乳栿
- source term：斜乳栿 / 乳栿
- proposed component id：CMP-FRAME-RUFU-001
- proposed master id：CMP-FRAME-RUFU-001_MASTER
- proposed master version：V001
- V008 physical instances：8
- family：斜向梁构件

当前建议建立一个 canonical 乳栿 Master family。

上斜乳栿 / 下斜乳栿暂时仅作为 assembly-role：
- UPPER
- LOWER

东北 / 东南 / 西南 / 西北角仅作为 placement role：
- NE
- SE
- SW
- NW

在缺少直接几何差异证据前，不为上下层或四角建立不同本体 Master。

## 2. Direct Source Evidence

SRC-ZG-WF-001：

### PDF p83 / printed p68 / §2.3.1.3 / Table 2-40

报告直接说明：
- 四角设置上、下斜乳栿，共8根；
- 组合构造中丁栿与斜乳栿间距一材一栔，垫单材栿一层；
- Table 2-40 对乳栿列出8行，其中6行有完整“广/厚”实测，2行标记“未及”；
- 6组完整截面样本：
  - 331 × 185 mm
  - 337 × 186 mm
  - 323 × 193 mm
  - 342 × 185 mm
  - 325 × 188 mm
  - 325 × 186 mm
- 表列均值：广330.5 mm；厚187.2 mm；
- 折合分：21.6 / 12.2；
- 取整分：22 / 12；
- 报告正文明确提到斜乳栿入斗栱处刻出槽口。

### PDF p84 / printed p69 / Fig.2-42

图题：**万佛殿斜乳栿与斗栱交接关系**。

该照片作为 SAME_BUILDING_DIRECT_PHOTO，直接支持：
- 斜乳栿与斗栱存在实际交接；
- 交接部位存在加工/槽口语义；
- 但照片不足以锁定槽口精确三维尺寸、端部轮廓或完整榫卯。

## 3. Measurement Contract

measurement_table_row_count = 8  
complete_measured_sample_count = 6  
unmeasured_table_row_count = 2

canonical family mean section：
- width_mm = **330.5**
- thickness_mm = **187.2**

classification：
- DIRECT_MEASURED_FAMILY_MEAN
- observed_as_measured
- not a 963 original-design claim

sample_to_instance_mapping = **UNKNOWN**

禁止把6组完整样本静默对应到8根具体实例。

报告分值：
- converted_fen = 21.6 × 12.2
- rounded_fen = 22 × 12
- REPORT_INFERRED / METADATA_ONLY
- geometry_use_count = 0

## 4. Length / Angle / Placement Boundary

historical_full_length_mm = null / UNKNOWN

Stage 1 proposed canonical_reference_length_mm = **1000.0**

该1000mm仅用于 Master 独立构建与验证：
- PROJECT_RULE
- ENGINEERING_REFERENCE
- NON_HISTORICAL_REFERENCE
- CANONICAL_REFERENCE_ONLY
- replaceable = true
- historical_claim = false

真实8根乳栿：
- exact length = UNKNOWN in Stage 1
- exact plan angle = UNKNOWN in Stage 1
- orientation / length later derive from explicit assembly endpoints
- **不得因为“四角斜向”而直接硬编码45°**

Hard fail：
- REFERENCE_LENGTH_LEAKS_INTO_BUILDING
- SILENT_45_DEGREE_ASSUMPTION

## 5. Proposed Geometry Mode

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
- Location = (0,0,0)
- Rotation = (0,0,0)
- Scale = (1,1,1)

Proposed Stage1 body：
**1000 × 330.5 × 187.2 mm**

“斜”属于后续 placement / assembly orientation，不烘焙到 canonical Master 的本体坐标。

## 6. Role Policy

Role dimensions：

- vertical_role = UPPER / LOWER
- corner_role = NE / SE / SW / NW

V0.1建议：
- UPPER / LOWER 共用同一 body geometry；
- 四角共用同一 body geometry；
- role 不改变截面；
- role 不改变端部；
- role 不自动增加槽口；
- role 不自动设置45°。

如后续直接证据证明上下乳栿或不同角位本体存在稳定几何差异，再升级为 geometry variant。

## 7. Assembly Semantics

Direct-source semantic metadata：

- member_type = DIAGONAL_FRAME_MEMBER
- bracket_end = 与斗栱交接
- opposite_end = UNKNOWN / ASSEMBLY_ENDPOINT_TO_BE_RESOLVED
- 丁栿与斜乳栿间距 = 一材一栔
- 垫单材栿一层

这些内容在 Stage 1 只作为装配语义，不用于生成未经授权的端点坐标、长度、角度或交接几何。

## 8. Groove Boundary

报告直接确认：
斜乳栿入斗栱处刻出槽口。

锁定候选：
**BRACKET_ENTRY_GROOVE = DIRECT_EXISTENCE / GEOMETRY_DEFERRED**

当前未知：
- groove_width
- groove_depth
- groove_length
- exact longitudinal position
- exact contour
- whether all 8 are identical

V0.1建议：
Stage 1 canonical Master **不切真实槽口**。

Stage 2 如装配需要，可建立显式、可替换的 PARAMETRIC_COMPLETION；必须保持：
- replaceable = true
- historical_claim = false

## 9. Geometry Prohibitions

V001 不得加入：
- 未测槽口尺寸；
- 推测榫卯；
- 无证据端头造型；
- 硬编码45°；
- 现状弯曲/损伤；
- UPPER/LOWER未经证据支持的本体差异；
- 四角未经证据支持的本体差异；
- 6组样本与具体实例的假映射；
- 1000mm building-length leakage；
- 折合分值直接驱动几何；
- 963原始设计尺寸声明。

## 10. Proposed First-Article Validation

若 V0.1 后续锁定，首件至少验证：

1. component/master id 唯一；
2. V008乳栿 physical instances = 8；
3. UPPER=4 / LOWER=4；
4. corner roles = NE/SE/SW/NW each 2；
5. Table row count=8；
6. complete samples=6；
7. unmeasured rows=2；
8. six observed samples retained；
9. sample_to_instance_mapping=UNKNOWN；
10. width=330.5；
11. thickness=187.2；
12. report fen metadata only；
13. historical length=null；
14. reference length=1000 / non-historical；
15. exact plan angle=null；
16. no silent 45-degree assumption；
17. UPPER/LOWER same geometry signature；
18. four corner roles same geometry signature；
19. bracket-end semantic exists；
20. opposite endpoint unresolved；
21. one材一栔 spacing retained as semantic metadata；
22. groove existence=DIRECT；
23. groove geometry=DEFERRED；
24. canonical body has no groove cut；
25. X/Y/Z bbox；
26. canonical origin/transform；
27. length mutation only X；
28. width mutation only Y；
29. thickness mutation only Z；
30. role mutation no body change；
31. independent reopen；
32. deterministic semantic restore；
33. no REFERENCE_LENGTH_LEAKS_INTO_BUILDING；
34. no SILENT_HISTORICIZATION；
35. no SILENT_45_DEGREE_ASSUMPTION；
36. no UNDECLARED_PARAMETRIC_COMPLETION；
37. no MASTER_WITHOUT_EVIDENCE_BINDING；
38. D-076 visual-reference gate traceable.

## 11. Proposed Review Package

建议至少6张：
- FRONT
- SIDE
- TOP
- AXON
- DIMENSION_PARAMETER_SUMMARY
- EVIDENCE_UNCERTAINTY_SUMMARY

EVIDENCE_UNCERTAINTY_SUMMARY 必须明确：
- 6 measured / 2 unmeasured；
- sample mapping UNKNOWN；
- historical length UNKNOWN；
- exact plan angle UNKNOWN；
- groove exists but geometry deferred；
- 1000mm non-historical reference only。

## 12. Locked Decision

D-083 正式锁定以下方案：

> 一个 `CMP-FRAME-RUFU-001_MASTER`；330.5×187.2mm 使用6组完整实测的构件族均值；UPPER/LOWER和四角仅作为 assembly/placement roles；斜向角度与真实长度后续由装配端点求解；不默认45°；槽口存在性直接锁定，但精确几何推迟至 Stage 2。

本 V001 不是工程执行授权。

D-083 允许建立下一项工程任务合同 T-024，但不自动授权工程执行。
在 Product Owner 明确授权开始 T-024 前：
- 不创建 T-024 execution branch/PR；
- 不运行 Blender；
- 不进行首件生产；
- T-018 继续 HOLD。
