# P3.3 V002 Stage 1｜叉手 Master Spec V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-108**  
**日期：2026-09-23**  
**Gate：P3.3 V002｜真实构件驱动整殿重建**  
**Stage：Stage 1｜真实构件 Master 库**  
**资料主权：D-099 / RC-019**  
**复原方法：D-108 / RC-020｜Evidence-Constrained Reconstruction**  
**A1：PASS / DIRECT SECTION VERIFIED**  
**A2：PASS / SAME-BUILDING STRUCTURAL SEMANTIC VERIFIED**  
**任务性质：正式锁定规格；不等于 T-028 工程执行授权**

## 1. Project Goal Boundary

P3.3 的目标不是证明或复制“963年历史原型的全部精确几何”，而是：

> 在不违背现有可靠资料的前提下，完成结构自洽、几何闭合、可生成、可迭代的万佛殿3D模型。

因此：

- 直接资料明确的事实优先采用；
- 必要但资料未给出的几何参数允许进入 `RECONSTRUCTED_DESIGN`；
- reconstructed design 必须显式标注、可替换、不得伪装成历史实测；
- `UNKNOWN` 不再自动等于 `BLOCKED`；
- 只有与直接资料冲突、无法形成结构闭合或存在未解决的主权冲突时才阻塞生产。

## 2. Component Identity

- 中文名：叉手
- component id：`CMP-FRAME-CHASHOU-001`
- master id：`CMP-FRAME-CHASHOU-001_MASTER`
- master version：`V001`
- family：斜向脊部梁架支撑构件
- physical instances：**8**

Role：

- `INTERIOR_FRAME = 4`
- `GABLE_FRAME = 4`

锁定一个 shared canonical Master。

南/北镜像、正身/山面位置差异首先由 assembly / placement 处理，不自动建立 Geometry Variant。

## 3. Authoritative Inputs

### A1
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct locator：

- PDF p89–90
- printed p74–75
- §2.3.1.8
- Table 2-45

Formal evidence record：

`docs/evidence/zhenguo_wanfo/P3_3_CHASHOU_DIRECT_SOURCE_BINDING_V001.md`

### A2
山西文物数字博物馆·万佛殿专题。

Same-building structural semantic：

- 平梁之上设驼峰、蜀柱、叉手；
- 叉手属于平梁以上脊部梁架支撑体系。

### Canonical Registry
`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

当前锁定8根：

- 东缝南侧 / 北侧
- 西缝南侧 / 北侧
- 东山南侧 / 北侧
- 西山南侧 / 北侧

## 4. Measurement Contract

可直接辨识完整样本（mm）：

- 232 × 92
- 234 × 90
- 228 × 91
- 228 × 89

另有“未及”记录。

Report-published mean：

- width = **230.5 mm**
- thickness = **90.5 mm**

Independent recompute：

- width = **230.5 mm**
- thickness = **90.5 mm**

锁定：

- `SOURCE_INTERNAL_NUMERIC_CONFLICT = false`
- `canonical_section_mm = 230.5 × 90.5`
- `sample_to_instance_mapping = UNKNOWN`

报告折合/取整分值保留为 metadata；Stage 1 canonical section直接采用毫米实测均值。

## 5. Geometry Contract

Geometry mode：

`PARAMETRIC_ENDPOINT_DRIVEN_LONG_MEMBER`

Canonical local axes：

- +X = longitudinal axis
- +Y = 广 / width
- +Z = 厚 / thickness

Stage 1 canonical reference body：

**1000 × 230.5 × 90.5 mm**

其中：

- `canonical_reference_length_mm = 1000`
- classification = `RECONSTRUCTION_REFERENCE_LENGTH`
- historical claim = false
- building fixed length = false
- replaceable = true

1000 mm 的职责只是提供稳定 Master specimen / mutation / review / validation body，不进入整殿实例实长。

## 6. Endpoint-driven Assembly Geometry

每根叉手的实际几何由装配端点决定。

定义：

- `P_lower` = 平梁上部连接区域中的项目装配锚点
- `P_upper` = 脊部支撑连接区域中的项目装配锚点

实例纵向向量：

`V = P_upper - P_lower`

实际长度：

`L = ||V||`

实例中心：

`P_center = (P_upper + P_lower) / 2`

实例局部 +X：

沿 `V` 对齐。

因此：

- actual length = assembly-derived
- actual angle = assembly-derived
- orientation = assembly-derived
- Master 不保存固定“历史角度”
- Master 不保存固定“历史全长”

若端点本身由项目整体几何推导，则其状态为 `RECONSTRUCTED_DESIGN`，不是历史实测，但允许正式用于完成3D模型。

## 7. Placement Contract Boundary

8根实例按四榀组织：

### INTERIOR_FRAME
- 东缝 / 南侧
- 东缝 / 北侧
- 西缝 / 南侧
- 西缝 / 北侧

### GABLE_FRAME
- 东山 / 南侧
- 东山 / 北侧
- 西山 / 南侧
- 西山 / 北侧

每榀使用同一 Master 两次，通过 endpoint placement 形成南北成对斜撑。

Role / side 不改变：

- canonical section
- Master body identity
- material identity
- parameter schema

## 8. End / Joinery Design

Stage 1 不以历史榫卯完整性为完成前提。

V001 锁定：

- Master reference end profile = `STRUCTURAL_SIMPLIFIED_FLAT_END`
- historical end profile = `UNRESOLVED_METADATA`
- hidden mortise/tenon = `NOT_MODELED_AT_STAGE1`
- notch/groove = `NOT_MODELED_AT_STAGE1`

后续 Assembly / Detail Stage 允许根据：

- 实际碰撞关系
- 视觉闭合要求
- 新增直接资料

增加可替换的 reconstructed end treatment。

不得把 reconstructed end treatment 表述成历史原榫卯。

## 9. Variant Policy

V001：

- canonical Master count = 1
- Geometry Variant count = 0

不因以下因素建立 Variant：

- 南 / 北方向
- 左 / 右镜像
- INTERIOR_FRAME / GABLE_FRAME
- 装配长度不同
- 装配倾角不同

只有未来出现“稳定、重复且必须改变本体截面/轮廓/端部”的生产需求，才提出 Variant Change Proposal。

## 10. Review Board

首件 Review Board 需要6个 Definition-driven panels：

1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION`
4. `DIMENSION_AND_PARAMETRIC_LENGTH`
5. `PLACEMENT_AND_ENDPOINT_LOGIC`
6. `SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY`

第五面板必须展示：

- 同一 Master
- 至少两组不同 endpoint 示例
- 自动产生不同 length / angle
- canonical section保持不变

第六面板必须清楚区分：

- evidence-locked facts
- reconstructed-design parameters
- historical claims not made

## 11. Validation Requirements

下一工程首件至少验证：

1. component/master/version identity；
2. V008 physical instances = 8；
3. INTERIOR_FRAME = 4；
4. GABLE_FRAME = 4；
5. four complete visible samples retained；
6. unmeasured source record retained；
7. report mean = 230.5 × 90.5；
8. recomputed mean = 230.5 × 90.5；
9. source internal numeric conflict = false；
10. sample_to_instance_mapping remains UNKNOWN；
11. canonical section = 230.5 × 90.5；
12. reference length = 1000 / reconstructed reference；
13. reference length historical claim = false；
14. canonical bbox = 1000 × 230.5 × 90.5；
15. canonical axes / origin / transform；
16. length mutation isolates X；
17. width mutation isolates Y；
18. thickness mutation isolates Z；
19. side/role mutation preserves Master geometry；
20. endpoint resolver calculates length from P_lower/P_upper；
21. endpoint resolver calculates orientation from P_lower/P_upper；
22. no fixed installation angle stored in Master；
23. no 1000mm leakage to building instances；
24. eight Registry locations traceable；
25. same-building A2 structural layer retained；
26. simplified flat end explicit；
27. no unsupported historical joinery claim；
28. independent reopen PASS；
29. deterministic semantic restore；
30. Definition ↔ Semantic identity；
31. required Review Board panels complete；
32. canonical .blend not tracked in Git Master directory；
33. D-099 / RC-019 / D-108 / RC-020 traceable。

## 12. Hard Fails

- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `FIXED_MASTER_INSTALLATION_ANGLE`
- `SILENT_HISTORICIZATION`
- `RECONSTRUCTED_DESIGN_MARKED_AS_DIRECT_MEASURED`
- `DIRECT_EVIDENCE_OVERRIDDEN_WITHOUT_DECISION`
- `FALSE_GEOMETRY_VARIANT_FROM_PLACEMENT_ONLY`
- `MASTER_WITHOUT_EVIDENCE_BINDING`
- `MODEL_BEFORE_SOURCE_REVIEW`

历史数据缺失本身**不是 Hard Fail**。

## 13. Authorization Boundary

D-108 正式批准并锁定本 Master Spec V001。

允许下一步：

- 设计 `T-028｜P3_3_CHASHOU_MASTER_V2_V001` Task Contract；
- 将 endpoint-driven reconstructed-design 规则写入该合同；
- 复用 Master V2 shared builder / validator / workflow。

当前仍不授权：

- T-028 production branch / PR；
- GitHub Actions / Blender 首件执行；
- Catalog approved registration；
- V008 approved Master binding；
- Stage1 PASS；
- Stage2；
- T-018 resume。

开始工程执行仍需 Product Owner 明确授权。
