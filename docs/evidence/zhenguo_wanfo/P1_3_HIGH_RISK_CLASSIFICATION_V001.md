# P1.3｜平遥镇国寺万佛殿｜High-Risk Evidence Classification V001

Status: COMPLETE / P1.3 STEP 1 / NOT GATE-APPROVED  
Date: 2026-09-12  
Primary input: `P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md`  
Supporting input: `P1_2_DIRECT_PAGE_REVIEW_V001.md` / `P1_2_CORE_EVIDENCE_BATCH_03.md`

## 0. 本步骤目的

本步骤只处理会直接影响 P1.3 Go / No-Go 的高风险证据，不对全部低风险参数做批量分级。

正式四级分类：

1. **已证实 / CONFIRMED**：直接证据支持该命题，并且证据的时间层、语义层与待复原命题一致。
2. **高可信推断 / HIGH_CONFIDENCE_INFERENCE**：不是直接事实，但由多项互相一致的实测、文献、构造逻辑或设计约束形成强约束；不得与来源作者的明确保留意见冲突。
3. **合理补全 / REASONABLE_COMPLETION**：模型必须补齐，但现有证据无法唯一确定；允许采用明确、可替换、可追踪的候选值或规则，且必须显式标注为非历史事实。
4. **未知 / UNKNOWN**：证据不足、存在未解决冲突，或无法唯一确定；不得静默写入生产参数。

### 核心原则

- `DIRECT_VERIFIED` 只代表“主报告原页已直接核读”，不自动等于“963年历史事实”。
- `observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate` 必须保持独立。
- 一个高风险问题可以拆成多个命题分别评级；禁止用“整体一个等级”掩盖语义差异。

---

## 1. HR-01｜963原设计柱高与统一 Z 基准

### HR-01A｜`column_height_963_design_mm`

**正式分类：UNKNOWN｜未知**

依据：

- 现有二手资料常见檐柱高约3.42m，但原始地坪、柱础和测量起止面不足以证明该值等同963设计柱高；
- V002 已明确把 `column_height_963_design_mm` 保持为 `UNKNOWN / HOLD_HIGH_RISK`；
- 当前没有足够证据将现状或二手柱高反推为963初建值。

生产规则：

- 正式生产参数中不得把3.42m或其他现状/二手高度写成“963设计柱高”；
- 该字段保持 `null / unknown`，直到后续获得直接证据或形成明确的合理补全方案；
- 可以建立相对Z向结构，但不得宣称绝对柱高已经历史锁定。

阻断性：

- **阻断最终963绝对Z锁定**；
- **不阻断平面、拓扑、相对屋架关系和参数结构继续建立**。

### HR-01B｜`global_z_datum`

**正式分类：REASONABLE_COMPLETION｜合理补全（项目坐标规则，不是历史事实）**

建议项目规则：

`Z = 0` 定义为 **abstract column-foot design plane｜抽象柱脚设计控制平面**。

说明：

- 该基准只是模型坐标约定，不声称等于963年地坪、柱础顶面或现状测绘零点；
- 一旦未来获得原始地坪/柱础关系，可整体映射或修正，不破坏其他相对几何。

禁止事项：

- 不得把工程坐标 `Z=0` 写成“963历史地坪标高”。

---

## 2. HR-02｜角柱生起

### HR-02A｜“角柱存在生起机制”

**正式分类：CONFIRMED｜已证实**

依据：主报告直接讨论角柱生起，并明确指出长期荷载、倾斜和受压形变会影响现状读数。

### HR-02B｜有效实测范围 51–68mm / 均值59.5mm

**正式分类：CONFIRMED｜已证实，但只属于 `observed_as_measured_filtered`**

不得把这一等级外推为“963原设计值已证实”。

### HR-02C｜`corner_column_rise_design_mm = 61.2`（2寸）

**正式分类：REASONABLE_COMPLETION｜合理补全**

不升为“高可信推断”的理由：

- 61.2mm 与有效实测均值59.5mm高度接近，吻合度约97.22%；
- 但主报告明确使用“初步推算/猜测”语义；
- 现状读数又受到长期结构变形影响。

生产规则：

- 61.2mm 可作为 **默认复原候选值**，但必须带 `classification=reasonable_completion`；
- 建议保留 51–68mm 为校核区间；
- 参数必须可单独修改，不应烘焙进不可逆几何。

禁止事项：

- 不得在说明文、参数表或可视化中写成“963年角柱生起确定为61.2mm”。

阻断性：**NON-BLOCKING**，前提是显式保留不确定性。

---

## 3. HR-03｜举折与总举高

### HR-03A｜实测槫间高差 A/B/C = 383.5 / 602.3 / 1249.5mm

**正式分类：CONFIRMED｜已证实，但属于现状实测层**

### HR-03B｜报告归整的设计规律（25/40/82分、88/61/82分、折屋20分+8分）

**正式分类：HIGH_CONFIDENCE_INFERENCE｜高可信推断，限“设计规律解释”语义**

依据：

- 多组实测与归整值吻合度约98.41%–99.74%；
- 水平架道与垂直归整形成相互约束的系统性解释；
- 但这仍是报告从现状推导出的设计规律，而非直接记录的963设计图。

### HR-03C｜`total_roof_rise_fen = 231` / ≈3534.3mm 作为963原设计值

**正式分类：REASONABLE_COMPLETION｜合理补全**

理由：

- 数学吻合度很高；
- 但主报告明确表示，在构件年代、替换与修改史未全面鉴定前，不把举折推算提升为定论。

生产规则：

- 231分 / ≈3534.3mm 可以作为 **963 candidate default**；
- 必须与现状实测层分开存储；
- 建议未来参数结构同时保留 `observed_rise` 与 `reconstructed_963_candidate_rise`。

禁止事项：

- 不得用“高吻合度”替代历史证据等级；
- 不得把231分写成已证实963事实。

阻断性：**NON-BLOCKING**，前提是使用候选层而非事实层。

---

## 4. HR-04｜转角铺作、45°节点与角梁

### HR-04A｜转角构件连接拓扑

包括：45°方向两跳角华栱、托双昂、由昂、令栱、里转第三跳承角梁，以及前后檐/山面柱头铺作后尾连接对象不同。

**正式分类：HIGH_CONFIDENCE_INFERENCE｜高可信推断**

理由：现有专业数字展示已形成稳定、具体、可验证的连接逻辑，足以建立拓扑 graph；但当前没有直接精确测量把所有斜向节点坐标锁死。

### HR-04B｜45°构件精确长度、标高、斜率、榫卯落位

**正式分类：UNKNOWN｜未知**

生产规则：

- 可以先建立 topology skeleton / parametric placeholders；
- 不得把自动几何推导结果标成历史实测；
- 精确节点进入生产前必须拥有独立参数和证据状态。

### HR-04C｜隐衬角栿 / 隐角梁问题

**正式分类：UNKNOWN｜未知**

理由：现有来源存在明确术语/构造判断冲突，目前不能确认是否为同一构件不同命名、不同作者判断，或历史修缮状态差异。

禁止事项：

- 不得静默选择其中一种文献说法并作为“确定结构”；
- 不得为了让模型闭合而伪造为已证实节点。

阻断性：

- **阻断高精度/榫卯级角部生产锁定**；
- **不阻断整体拓扑骨架与中等LOD复原继续进行**。

---

## 5. HR-05｜963原构 vs 后世修缮替换

### HR-05A｜修缮时间线

1151 / 1540 / 1752前后 / 1811–1816 / 1895–1904 / 1949后局部维修。

**正式分类：CONFIRMED｜已证实**

### HR-05B｜逐构件 `component_level_963_originality`

**正式分类：UNKNOWN / PARTIAL｜未知 / 部分可判**

理由：已知存在多轮修缮，且部分构件年代、磨损、替换概率可以讨论，但现有证据不足以把全部现存构件逐一认证为963原构或后世替换。

生产规则：

未来每个关键构件至少预留：

- `historical_state_tag`
- `evidence_class`
- `source_layer`
- `originality_status`

推荐 `originality_status`：

- `963_confirmed`
- `963_probable`
- `later_confirmed`
- `unknown`

未获得构件级证据时默认 `unknown`，不得默认 `963_confirmed`。

阻断性：**NON-BLOCKING for candidate reconstruction / BLOCKING for claims of complete 963 material authenticity**。

---

## 6. HR-06｜`report_ideal_model` 与 963 初建状态

### HR-06A｜“主报告理想模型不等于963真实初建状态”

**正式分类：CONFIRMED｜已证实的来源语义边界**

主报告明确说明：理想模型不是现状测绘模型，也不一定是刚建成时真实状态，其中可能包含不同历史时期的改造设计成分。

生产规则：

必须长期保留三个独立数据层：

1. `observed_as_measured`
2. `report_ideal_model`
3. `reconstructed_963_candidate`

禁止事项：

- **禁止**把 `report_ideal_model` 直接复制、重命名或描述为“963原貌”；
- 其数据只能作为963复原的证据输入之一。

阻断性：**NON-BLOCKING**，但属于强制治理规则。

---

## 7. Step 1 阻断性结论

### 当前未发现立即触发 NO-GO 的证据缺口

原因：现有高风险未知项均可以被局部隔离，而不是污染整个模型：

- 963柱高保持未知，可与相对Z关系拆开；
- Z基准可定义为工程坐标规则；
- 角柱生起、231分举折可作为显式“合理补全候选”；
- 转角拓扑可先建立，精确节点保持未知；
- 构件原真性可通过逐构件 metadata 管理；
- 理想模型语义已有明确隔离规则。

### 但 Step 1 也不构成 P1.3 PASS

仍需继续验证：

1. 全部关键参数是否都能按同一规则进入四级分类；
2. 是否还存在尚未发现的、无法隔离的关键未知项；
3. 正式参数 JSON 是否能同时保存“值 + 证据等级 + 时间层 + 来源层”；
4. 进入3D后是否可以做到所有合理补全项可替换、可追踪，而不是烘焙成事实。

### Step 1 当前方向

**PROVISIONAL DIRECTION: CONDITIONAL_GO_CANDIDATE**

这不是最终 Gate 结论，只表示：

> 目前高风险未知项尚不足以判定项目 No-Go；如果后续完整参数分级和参数结构能够保持这些不确定性边界，镇国寺万佛殿具备“带边界进入正式3D”的可能性。

---

## 8. 下一步

`P1.3 Step 2｜Full Critical Parameter Classification`

以 `P1_2_PARAMETER_CANDIDATE_MATRIX_V002.md` 为母表，把剩余关键参数批量映射为：

- CONFIRMED
- HIGH_CONFIDENCE_INFERENCE
- REASONABLE_COMPLETION
- UNKNOWN

并标记每项：

- `production_use`
- `time_layer`
- `source_layer`
- `blocking_level`

Step 2 完成后再进入最终 Go / No-Go 门槛判断。
