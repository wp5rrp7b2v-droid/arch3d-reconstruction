# P3.3 V002 Stage 1｜丁栿 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-078**  
**日期：2026-09-20**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**视觉规则：D-077 丁栿本轮单独豁免；D-076 对后续新构件继续生效**  
**任务性质：规格设计与锁定；尚未启动 Blender 工程执行**

## 1. Master Identity

- 中文名：丁栿
- canonical component id：CMP-FRAME-DINGFU-001
- canonical master id：CMP-FRAME-DINGFU-001_MASTER
- master version：V001
- V008 physical instances：8
- source registry：P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json / V008

V001 建立一个 canonical Dingfu Master family。上丁栿 / 下丁栿当前仅作为 assembly-role 变体，不建立两个独立 geometry Master。

## 2. Authoritative Evidence

构件事实直接写入 V008 / CURRENT Registry，不新增独立 evidence registration 文档。

SRC-ZG-WF-001：
- PDF p81 / 印刷 p66：§2.3.1 构件尺度，对山面丁栿位置与结构关系的正文描述；
- PDF p83 / 印刷 p68：§2.3.1.3 平梁、丁栿、乳栿，表2-40。

直接确认：
- 丁栿总数8根；
- 东西山面前后各一道，上、下丁栿各两根；
- 外端进入山面柱头铺作；
- 内端削成骑栿栱并与榑交构；
- 上承两山承椽枋和太平梁；
- 报告明确提到丁栿入斗栱处存在槽口。

装配语义不自动等于可锁定精确榫卯/槽口几何。

## 3. Measured Section Contract

表2-40丁栿8组实测（mm）：

| # | 广 | 厚 |
|---|---:|---:|
| 1 | 346 | 208 |
| 2 | 324 | 199 |
| 3 | 335 | 205 |
| 4 | 324 | 174（含） |
| 5 | 330 | 203 |
| 6 | 330 | 195 |
| 7 | 336 | 203 |
| 8 | 328 | 193 |
| 均值 | **331.6** | **200.9** |

Canonical Master V001：
- width_mm = 331.6
- thickness_mm = 200.9

分类：
- DIRECT_MEASURED_FAMILY_MEAN
- source layer：DIRECT_PRIMARY
- sample_to_instance_mapping = UNKNOWN

不得把8组样本静默映射到8根具体实例。

报告尺度分析：
- 折合：21.7分 × 13.1分
- 取整：22分 × 13分
- classification = REPORT_INFERRED / METADATA_ONLY
- geometry_use_count = 0

不得表述为963年原始设计截面。

## 4. Length Contract

historical_full_length_mm = null / UNKNOWN

canonical_reference_length_mm = 1000.0

该1000mm仅用于独立 Master 构建、mutation、reopen 与审核：
- PROJECT_RULE
- ENGINEERING_REFERENCE
- NON_HISTORICAL_REFERENCE
- CANONICAL_REFERENCE_ONLY
- replaceable = true
- historical_claim = false

真实8根丁栿长度必须在后续 Stage 2 / Stage 4 由明确装配端点求得。

1000mm进入整殿实例触发：
REFERENCE_LENGTH_LEAKS_INTO_BUILDING

## 5. Geometry Mode

Geometry mode：BOUNDED_LONG_MEMBER_OUTER_ENVELOPE  
LOD：EVIDENCE_BOUNDED_MEDIUM_LOD  
Unit：mm

Canonical coordinate：
- +X：构件纵向
- +Y：广
- +Z：厚
- handedness：right-handed

Origin：
longitudinal_midpoint / transverse_center / lower_reference_plane

Canonical transform：
- Location = (0,0,0)
- Rotation = (0,0,0)
- Scale = (1,1,1)

V001 主体几何：
reference_length × 331.6 × 200.9

## 6. Role Variant Rule

V001 定义两个 assembly-role：
- UPPER
- LOWER

两者：
- 共享同一 canonical body geometry；
- 不因 role 自动改变截面；
- 不因 role 自动增加榫卯/槽口；
- 差异仅保留给后续装配位置、标高、接口与长度解析。

未来若直接证据证明上下丁栿本体几何存在稳定差异，再升级为 geometry variant。

## 7. End / Interface Semantics

Semantic-only：
- OUTBOARD_END：进入山面柱头铺作
- INBOARD_END：骑栿栱 / 与榑交构区域

当前仅锁定语义存在性。

精确接口坐标、榫卯轮廓、接触面尺寸：
ASSEMBLY_OWNED / DEFERRED_TO_STAGE2

## 8. Groove Boundary

报告直接确认：
丁栿入斗栱处存在槽口。

锁定为：
BRACKET_ENTRY_GROOVE = DIRECT_EXISTENCE / GEOMETRY_DEFERRED

当前未知：
- groove_width
- groove_depth
- groove_length
- exact longitudinal position
- exact contour
- whether all 8 are identical

Stage 1 canonical Master **不得切真实槽口**。

Stage 2 如装配必须使用槽口，允许以显式 PARAMETRIC_COMPLETION 建立可替换接口几何；不得回写为实测历史事实。

## 9. Geometry Prohibitions

V001 禁止：
- 推测榫卯；
- 未量化真实槽口；
- 无证据端头曲线；
- 未证明的上下丁栿造型差异；
- 实测样本与具体实例的假映射；
- 现状挠曲/损伤烘焙；
- 一般古建知识补出的“典型丁栿”细节；
- 963年原始尺寸声明。

## 10. Required Parameters

正式 params 至少包含：
- component_id
- master_id
- master_version
- physical_instance_count = 8
- role_variants = [UPPER, LOWER]
- width_mm = 331.6
- thickness_mm = 200.9
- measured_section_samples = 8组
- sample_to_instance_mapping = UNKNOWN
- historical_full_length_mm = null
- canonical_reference_length_mm = 1000.0
- report_analysis
- groove_boundary
- known_unknowns[]
- interface_contract
- placement_only_attributes[]
- generator_path
- canonical_asset_path
- review_asset_paths[]

## 11. First-Article Validation Contract

未来工程首件至少检查：

1. component/master id 唯一；
2. V008 丁栿 physical instances = 8；
3. 8个 instance id 全部存在；
4. 8组实测样本完整；
5. sample_to_instance_mapping = UNKNOWN；
6. width = 331.6；
7. thickness = 200.9；
8. 21.7/13.1 与22/13仅 metadata；
9. historical full length = null；
10. reference length = 1000且非历史；
11. UPPER/LOWER 共享同一 body geometry；
12. role 不产生静默几何差异；
13. OUTBOARD/INBOARD semantic interfaces存在；
14. groove existence = DIRECT；
15. groove geometry = DEFERRED；
16. canonical body无实际槽口/榫卯；
17. body X/Y/Z extent正确；
18. canonical origin/transform正确；
19. length mutation仅改变X；
20. width mutation仅改变Y；
21. thickness mutation仅改变Z；
22. role mutation不改变body geometry；
23. independent reopen PASS；
24. semantic restore PASS；
25. no REFERENCE_LENGTH_LEAKS_INTO_BUILDING；
26. no SILENT_HISTORICIZATION；
27. no UNDECLARED_PARAMETRIC_COMPLETION；
28. no MASTER_WITHOUT_EVIDENCE_BINDING；
29. no MODEL_BEFORE_VISUAL_REFERENCE_REVIEW violation（D-077 Dingfu-only waiver必须显式可追溯）。

## 12. Review Package

首件至少6张：
1. FRONT
2. SIDE
3. TOP
4. AXON
5. DIMENSION_PARAMETER_SUMMARY
6. EVIDENCE_UNCERTAINTY_SUMMARY

审核重点：
- 331.6×200.9比例正确；
- 1000mm明确为非历史 reference；
- UPPER/LOWER 不产生无证据造型差异；
- 槽口只在信息层显示存在，不切入几何；
- 不把简单外包络误导为“963精确复原”。

## 13. Locked Boundary

D-078 锁定本 Spec。

D-078 不授权：
- Blender执行；
- PR merge；
- Stage 2接口落位；
- 真实8根长度；
- 槽口几何；
- T-018恢复；
- P3.3 Stage 1 PASS。

下一步：建立丁栿 First Article 工程任务合同；工程执行需再按任务合同授权边界执行。
