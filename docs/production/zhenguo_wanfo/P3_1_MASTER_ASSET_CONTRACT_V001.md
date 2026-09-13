# P3.1 Canonical Master Asset Contract V001

Status: **DRAFT / PRODUCT OWNER REVIEW REQUIRED**  
Date: 2026-09-13  
Phase/Gate: `P3 / P3.1｜Component Master & Variant Library`  
Qualification baseline: `T-010 APPROVED / D-033`  
Scope: **6 MASTER_REQUIRED components only**

## 1. Purpose

本合同定义 P3.1 当前 6 个已批准 `MASTER_REQUIRED` 构件进入正式 3D Master 生产前必须遵守的统一资产标准。

本合同解决的是：

> 一个构件 Master 在坐标、单位、参数、几何精度、证据语义、Variant、资产路径、审核和可替换性上，必须满足什么条件，才可以成为正式数字构件资产。

本合同 **不创建 Blender 几何**，也不授权任何未经后续 Task Contract 明确批准的批量建模。

正式生产范围由 D-033 锁定为：

1. `CMP-COLUMN-001`｜柱
2. `CMP-LUDOU-COLUMN-001`｜柱头栌斗
3. `CMP-DOU-SINGLE-LONGKAI-001`｜单向长开斗
4. `CMP-DOU-INTERACTIVE-001`｜交互斗
5. `CMP-FRAME-LOWER-SIX-CHUANFU-001`｜下六椽栿
6. `CMP-FRAME-UPPER-SIX-CHUANFU-001`｜上六椽栿

任何 Deferred / Proxy / Control / Envelope 对象均不得借本合同进入 Master 生产。

---

## 2. Authoritative Inputs

Master 生产必须继承且不得覆盖：

- `P3_1_DEFINITION_OF_DONE_V001.md`（D-032 LOCKED）；
- `P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md/json`；
- `P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md/json`；
- P3.0 Ontology / Registry / Migration Audit；
- P1 approved direct evidence package；
- P2 frozen engineering baseline；
- D-023、D-028～D-033；
- CG-02～CG-06；
- Evidence Visualization carry-forward rules。

历史边界继续有效：

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`；
- `Z-006-RC-01` 为独立、可替换 `REASONABLE_COMPLETION`；
- `DG-114 = UNKNOWN`，不得形成统一小斗规格；
- `HIS-002 = originality unknown`；
- 45°转角、榫卯、隐角梁及无直接证据细节继续 unresolved；
- observed / report ideal / reconstructed candidate 三层不得混合。

---

## 3. Global Asset Convention

### 3.1 Units

- Canonical unit: **millimetre (mm)**。
- Master 参数、几何导出、metadata 与 review dimension 均以 mm 为唯一标准长度单位。
- 若证据原始单位为 `fen / chi`，转换结果必须保存 source parameter / conversion provenance，不得只保留换算后的裸数值。

### 3.2 Coordinate System

统一右手局部坐标：

- `+Z`：建筑重力方向向上；
- `+X`：构件主要水平长度 / 跨度 / canonical width direction；
- `+Y`：与 +X 正交的水平深度 / transverse direction。

例外仅限柱：柱的主轴为 `+Z`，但 +X/+Y 仍定义其水平截面方向。

Master 本体禁止写入万佛殿 world coordinates、bay/grid location 或 instance rotation。

### 3.3 Origin

- 柱：柱身底面中心，`Z=0`。
- 斗类：构件底面 footprint 中心，`Z=0`。
- 梁架长构件（上下六椽栿）：纵向几何中点 `X=0`，横向中心 `Y=0`，下缘参考面 `Z=0`；理论端点为 `X=±L/2`。

Origin 必须可由机器验证；不得因建模方便临时漂移。

### 3.4 Object Transform Rule

Canonical Master：

- Location = `(0,0,0)`；
- Rotation = `(0,0,0)`；
- Scale = `(1,1,1)`；
- 几何尺寸来自参数生成，不允许通过 Object Scale 形成正式尺寸。

---

## 4. Master Identity & Naming Contract

每个 Master 必须使用 T-010 已锁定的 `component_id` 作为唯一语义主键。

建议正式资产命名：

- Master asset file: `<COMPONENT_ID>_MASTER_V001.blend`
- committed parameter file: `<COMPONENT_ID>_MASTER_PARAMS_V001.json`
- generator: `build_<machine_key>_master_v001.py`
- semantic snapshot: `<COMPONENT_ID>_MASTER_SEMANTIC_V001.json`
- Blender root collection: `MASTER__<COMPONENT_ID_NORMALIZED>`
- primary body object: `MASTER__<COMPONENT_ID_NORMALIZED>__BODY`

`component_id` 不得因建筑、位置或尺寸 Variant 改变。

---

## 5. Common Parameter Contract

每个 Master 参数记录至少包含：

- `component_id`
- `master_version`
- `unit`
- `coordinate_convention`
- `origin_convention`
- `parameters[]`
  - parameter key
  - value / null
  - unit
  - classification
  - time_layer
  - source_layer
  - production_use
  - source_ids
  - replaceable
- `geometry_mode`
- `known_unknowns[]`
- `interpretation_boundary[]`
- `historical_state`
- `originality_status`
- `reuse_scope`
- `variant_axes[]`
- `placement_only_attributes[]`
- `generator_path`
- `canonical_asset_path`
- `review_asset_paths[]`

任何 `UNKNOWN / DO_NOT_LOCK` 参数不得因 generator 需要而获得隐含默认历史值。

若工程运行必须使用 substitute / RC 值，必须作为独立 candidate 输入并记录来源、classification、replaceability 与 approval decision。

---

## 6. Geometry LOD Contract

P3.1 当前 Master 统一采用：

**`EVIDENCE_BOUNDED_MEDIUM_LOD`**

含义：

- 建立可复用的构件外部主体几何；
- 直接使用已有实测/已批准参数；
- 可使用明确标记的 engineering interpolation / replaceable completion 建立连续外轮廓；
- 不建立无证据支持的榫卯、暗槽、内部空腔、隐角结构、耳瓣细节或端部雕削；
- 不因为“看起来更像古建”而添加一般知识中的标准构造；
- 任何非直接证据几何规则必须作为 `PROJECT_RULE / REPLACEABLE` 或更低确定性记录。

Master 是 evidence-bounded digital asset，不是“963 年原构精确扫描件”。

---

## 7. Component-specific Contracts

### 7.1 CMP-COLUMN-001｜柱

**Identity:** 柱 / reusable column body  
**Geometry mode:** `PARAMETRIC_CIRCULAR_COLUMN_BODY`

Canonical axes / origin:

- +Z = 柱身纵轴；
- origin = 柱身底面中心。

Authorized geometry inputs:

- observed diameter `Z-001 ≈ 460 mm`｜CONFIRMED / observed reference；
- report design candidate `Z-002 = 459 mm`｜HCI / reconstructed candidate；
- height is explicit parameter；`Z-006` 本体继续 UNKNOWN；
- `Z-006-RC-01 = 3534.3 mm` 可作为经 D-023 批准的 replaceable building-specific candidate，但不得写成历史常量。

Required parameters:

- `diameter_mm`
- `height_mm`
- `diameter_source_mode`
- `height_source_mode`

Prohibited assumptions:

- 不添加无证据收分、卷杀、侧脚、柱础或柱头构造；
- 不把角柱生起规则固化进 Master body；
- 不把 3534.3 mm 固化为 Master 历史高度。

Variant rule:

- 直径或实际柱身高度变化属于 geometry Variant；
- 柱在柱网中的位置、旋转、是否角柱属于 instance / assembly metadata，除非后续证据证明几何本身不同。

Reuse scope: 圆柱主体型；建筑专属长度/直径由 Variant 参数提供。

### 7.2 CMP-LUDOU-COLUMN-001｜柱头栌斗

**Geometry mode:** `MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

Origin:

- 底面 footprint 中心；+Z 向上；+X=宽；+Y=深。

Authorized observed inputs:

- top width `475.1 mm`
- top depth `327.1 mm`
- bottom width `446.3 mm`
- bottom depth `305.5 mm`
- total height `293.8 mm`
- flat height `58.75 mm`
- sloped height `116.2 mm`

Contract geometry:

- 允许用上述宽/深/高建立 bounded outer envelope；
- 允许在有上下轮廓约束的区段采用明确记录的线性外轮廓 interpolation；该 interpolation 是工程规则，不是额外历史事实；
- 不建立未量化耳瓣、槽口、内部空腔或榫卯。

Variant rule:

- 证据支持的尺寸组差异可形成 Variant；
- 单纯 placement rotation 不形成 Variant。

DG-114 不得作为本 Master 或其他斗类的统一规格来源。

### 7.3 CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗

**Geometry mode:** `MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

Authorized observed inputs:

- top width `236.2 mm`
- bottom width `162.7 mm`
- top depth `256.2 mm`
- bottom depth `177.2 mm`
- total height `158.6 mm`

Origin / axes: bottom footprint center；+X=canonical width；+Y=depth；+Z=height。

Geometry rule:

- 当前只建立由 top/bottom width/depth + total height 约束的外包络；
- top/bottom 之间的连续形态若采用线性 loft，必须标记为 replaceable engineering interpolation；
- “长开”所涉及的具体槽、耳、内切形态若无直接量化，不建。

Variant rule:

- 尺寸/形制证据差异可形成 Variant；
- 构件绕 Z 轴旋转到另一方向是 placement-only，不产生新 Variant。

### 7.4 CMP-DOU-INTERACTIVE-001｜交互斗

**Geometry mode:** `MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`

Authorized observed inputs:

- top width `255.2 mm`
- top depth `240.0 mm`
- bottom width `176.2 mm`
- bottom depth `165.1 mm`
- total height `148.5 mm`

Origin / axes: bottom footprint center；+X=width；+Y=depth；+Z=height。

Geometry boundary:

- 允许建立实测上下轮廓限定的 bounded envelope；
- 线性 loft 仅作为 replaceable engineering interpolation；
- 不推导统一小斗规则；
- 不补造耳、槽、榫卯、内部空腔。

Variant rule同其他斗类：placement rotation ≠ Variant。

### 7.5 CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿

**Geometry mode:** `BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`

Canonical axes / origin:

- +X = 构件纵向跨度；
- +Y = 水平截面宽度方向；
- +Z = 垂直厚度方向；
- origin = longitudinal midpoint / transverse center / lower reference plane。

Authorized observed inputs:

- measured width `493.5 mm`
- tenon-area thickness `375 mm`
- maximum thickness `444 mm`
- frame-system identity/topology = CONFIRMED

Required parameters:

- `length_mm` = explicit free / evidence-bound parameter；当前不得作为历史固定值；
- `width_mm = 493.5` observed reference；
- `max_thickness_mm = 444` observed reference；
- `tenon_area_thickness_mm = 375` metadata/evidence parameter；其在 X 轴上的作用区间未证实时，不得据此生成局部削减位置。

Geometry boundary:

- Canonical body 可采用 `width × max_thickness × length` 的 bounded outer envelope；
- 该 envelope 表达“可建模的最大外包络”，不得声称整根构件处处厚 444 mm；
- 起拱、端部轮廓、局部厚度变化、榫卯、梁端连接均不生成，除非后续新增直接证据。

Variant rule:

- length / evidence-supported section differences = Variant；
- 支承在哪两点、世界位置、旋转 = assembly / instance；
- 不以不同 bay placement 自动复制 Master。

### 7.6 CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿

**Geometry mode:** `BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`

Axes / origin 与下六椽栿一致。

Authorized observed inputs:

- measured width `334 mm`
- tenon-area thickness `209 mm`
- maximum thickness `240.5 mm`
- frame-system identity/topology = CONFIRMED

Required parameters:

- `length_mm` = explicit free / evidence-bound parameter；
- `width_mm = 334` observed reference；
- `max_thickness_mm = 240.5` observed reference；
- `tenon_area_thickness_mm = 209` metadata/evidence parameter，作用区间未知时不得造局部端部几何。

Geometry / Variant boundary 与下六椽栿相同。

上、下六椽栿保持两个独立 Master；不得为了减少资产数量合并成一个 generic Master 后仅靠 Variant 名称区分。

---

## 8. Variant Contract

Variant 只在 **构件本体几何或证据语义发生可解释变化** 时创建。

Variant 必须有：

- stable `variant_id`；
- parent `component_id`；
- changed parameter set；
- parameter source / evidence class；
- building applicability；
- generated semantic snapshot；
- no manual object scaling。

以下不是 Variant：

- world position；
- bay / grid index；
- placement rotation；
- component instance number；
- identical geometry used at another location。

每个 Master 后续至少需要：

- canonical reference parameter set；
- 至少一次合法 parameter mutation / alternate parameter test，证明生成链可重复。

测试 Variant 不得被声称为历史建筑事实。

---

## 9. Asset Path Contract

Committed text/source assets建议固定于：

`production/zhenguo_wanfo/component_library/masters/<COMPONENT_ID>/`

包括：

- parameter JSON；
- generator script；
- semantic snapshot；
- validation output；
- committed metadata manifest。

Local-only binary：

`production/zhenguo_wanfo/component_library/masters/<COMPONENT_ID>/asset/<COMPONENT_ID>_MASTER_V001.blend`

Review assets：

`production/zhenguo_wanfo/review/P3_1/masters/<COMPONENT_ID>/`

`.blend / .blend1` 继续遵循 local-only binary policy；GitHub 保存 generator、params、semantic metadata、hash 与 review PNG，不要求提交 Blender binary。

---

## 10. Review Package Contract

每个 Master 最低审核集：

1. FRONT
2. SIDE
3. TOP（柱可为截面顶视；长构件必须能判断截面）
4. AXON
5. DIMENSION / PARAMETER SUMMARY
6. EVIDENCE / UNCERTAINTY SUMMARY

统一要求：

- neutral grey geometry；
- orthographic review views；
- 不用影视材质、纹理、风化或戏剧灯光掩盖几何；
- 标明 component_id / master version / dimensions；
- 正常几何图与 evidence visualization 分开；
- 斗类必须能看出 top/bottom footprint 差异；
- 六椽栿必须明确标注当前为 bounded outer envelope，并列出未建模端部/榫卯/起拱；
- 柱必须明确区分 observed diameter 与 replaceable height candidate。

---

## 11. Semantic / Hash / Reproducibility Contract

每个 Master 必须生成机器可读 semantic snapshot，至少含：

- object count / object names；
- local transforms；
- bounding box；
- resolved parameters；
- evidence classes；
- geometry mode；
- known unknowns；
- generator version；
- input file hashes；
- Blender version；
- canonical asset SHA256（若 binary 可读取）；
- semantic geometry signature。

PASS 要求：

- deterministic regeneration：semantic result一致；
- `.blend` 不要求 byte-identical；
- independent reopen PASS；
- no naked historical constants；
- no non-unit object scale；
- no world placement leakage；
- input mutation 能改变目标参数且不污染其他 Master；
- RC / replaceable input mutation 可重新生成；
- P2 frozen baseline hash unchanged。

---

## 12. Registration Contract

正式 Master 通过后，P3.1 Registry extension 至少登记：

- component_id
- master_id / version
- canonical asset status
- generator path
- parameter path
- local binary path
- review path
- semantic snapshot path
- variant list
- evidence references
- geometry mode
- reuse scope
- originality status
- known unknowns
- validation status
- approval status

Deferred / Proxy / Control / Envelope 不得出现 `approved master_3d_asset`。

---

## 13. Hard Fail Conditions

出现任一项即不得批准 Master：

- 使用 P2 proxy mesh 直接冒充正式历史构件；
- 将 `UNKNOWN` 静默填值；
- 把 RC/HCI 值写成 CONFIRMED；
- 斗类使用 DG-114 形成统一小斗规格；
- 建造无证据榫卯、槽口、内部空腔、端部细节并未标为非历史工程占位；
- 六椽栿把 max thickness 误写为全长已证实恒定截面；
- 柱把 Z-006-RC-01 写成 963 历史柱高；
- 通过 Object Scale 产生正式 Variant；
- world placement 写入 Master geometry；
- duplicate component_id / orphan Variant；
- P2 frozen baseline 被覆盖。

---

## 14. Contract Acceptance / Next-step Rule

本合同只有在 Product Owner 明确批准并锁定后才成为 P3.1 正式工程输入。

批准本合同：

- **不等于 P3.1 PASS**；
- **不等于 6 个 Master 已完成**；
- 只意味着后续 Codex / Blender 生产拥有稳定资产标准。

合同 LOCK 后才可创建下一项 T-task。

建议下一项工程任务按“先做可验证代表样本，再扩展到 6 个”执行：

> 先生产 1 个结构简单且证据边界清楚的 Master（建议 `CMP-COLUMN-001`）作为 Contract Implementation Pilot，验证 generator → `.blend` → semantic QC → review package → Registry registration 全链；Pilot PASS 后再批量扩展剩余 5 个。

这样可避免在资产标准尚未经真实 Blender 验证前一次性生成 6 套需要返工的 Master。
