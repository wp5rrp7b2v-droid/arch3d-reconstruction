# Evidence Visualization Carry-forward V001｜镇国寺万佛殿

Status: **LOCKED / PRODUCT OWNER APPROVED CARRY-FORWARD**  
Date: 2026-09-12  
Applies after: `P2｜正式参数化与3D复原` closure

## 1. Purpose

P2.3 的 `EVIDENCE_DIAGNOSTIC_V002` 采用“最高不确定性优先”的实例级分类，用于保守识别风险边界。该图在当前 P2.3 Gate 中有效，但不应被误读为“证据丰富度图”或最终整寺证据表达方案。

后续 Evidence Visualization 正式采用双层体系。

## 2. Layer A｜Risk Map｜风险边界图

用途：内部审计、历史声明边界检查、过度确定性预警。

规则：

- 延续 `UNKNOWN / PLACEHOLDER > REASONABLE COMPLETION / APPROVED OVERRIDE > HIGH CONFIDENCE INFERENCE > CONFIRMED` 的最高不确定性优先逻辑；
- 一个实例只要命中更高不确定性类别，整实例可按该更高不确定性显示；
- 大面积 UNKNOWN / PLACEHOLDER 是允许的，不代表“整座建筑没有史料依据”；
- 必须明确标注这是 **Conservative Risk Map**；
- P2.3 `EVIDENCE_DIAGNOSTIC_V002` 即属于本层。

## 3. Layer B｜Evidence Composition Map｜证据构成图

用途：最终整寺级成果中展示“一个构件/部位内部，哪些属性由什么等级证据支持”，避免一个未知属性把整个构件视觉上全部降为 UNKNOWN。

后续设计至少应支持：

- 按属性或子构件表达证据等级，例如：`柱位 C｜柱径 C｜柱高 RC｜原真性 U`；
- 或使用分段色条、比例、属性面板等表达 CONFIRMED / HCI / RC / UNKNOWN 的组成；
- 不得把综合比例误写成历史事实概率；
- 必须能回溯到 parameter / evidence metadata，而不是只根据最终 mesh 外观推断；
- 在整寺级最终证据展示前，应先定义并验证具体视觉编码与读取规则。

## 4. Normal Presentation Model

正常复原展示与证据诊断分离：

- 正式建筑展示可使用正常木构、瓦面及后续批准的材质表达；
- 不使用 Risk Map 的证据颜色作为正常建筑材质；
- Risk Map / Evidence Composition Map 均属于 evidence visualization，不等于 presentation material system。

## 5. Interpretation Boundary

- `CONFIRMED=0 / HCI=0` 出现在 P2.3 Risk Map 中，只表示按“实例整体最高不确定性”聚合后没有完整实例落入这两类；
- 不得据此推导为 P1/P2 参数证据中没有 CONFIRMED 或 HCI；
- 参数证据等级、实例综合风险等级、构件原真性状态必须继续分开解释。

## 6. Carry-forward Requirement

进入下一阶段规划时必须保留本规则。下一阶段若涉及整寺级、精细化或最终公众展示的 Evidence Visualization，不得仅用单一“最差等级整实例着色”替代 Evidence Composition Map。
