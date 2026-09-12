# P2.2｜参数化主体结构候选模型｜Definition of Done V001 DRAFT

Status: **DRAFT / PRODUCT OWNER REVIEW REQUIRED**  
Date: 2026-09-12  
Gate: `P2.2｜参数化主体结构候选模型｜Parametric Structural Skeleton`

## 1. Gate Goal

在 P2.1 已批准的正式生产参数基线之上，生成万佛殿第一版**正式、参数驱动、可重复构建、证据可追溯的主体结构候选模型**。

P2.2 的目标不是完成精细古建成品，而是证明：

- 正式 P2.1 参数与 approved override 能稳定驱动 Blender 几何；
- 柱网、柱、主要梁架、斗栱拓扑骨架、屋顶控制几何和主要出檐/山面关系能够形成完整的中等 LOD 主体结构；
- 参数与几何之间可机器追溯；
- REASONABLE_COMPLETION 可替换而不破坏模型架构；
- UNKNOWN 与证据边界不会因为“已经建模”而被伪装成历史事实；
- 同一输入可确定性重建同一结构结果。

P2.2 是本项目第一项正式 Blender 历史复原几何 Gate。

## 2. Authoritative Inputs

P2.2 只能读取以下正式输入：

1. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
2. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
3. `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
4. P2.0 Evidence-aware Parameter Schema 与其已批准读取规则
5. P2.1 Gate Review / D-023 / D-024 所形成的生产边界

未经显式批准，不得把外部资料、经验尺寸、视觉估计或手工 Blender 数值直接加入正式几何。

## 3. Non-goals

P2.2 不负责：

- 完成材质、纹理、灯光、最终渲染或展示级视觉；
- 完成全部精细榫卯；
- 对转角 45° 节点、隐衬角栿/隐角梁争议给出超出证据的精确解；
- 复原每个小斗的历史精确规格；
- 证明所有构件均为 963 年原构；
- 模拟现状全部变形、沉降、挠曲与修缮痕迹；
- 宣布“完全还原 963 年原貌”。

上述内容除非直接影响主体结构成立，否则留待 P2.3 或后续更高 LOD 阶段。

## 4. Definition of Done｜9项

### DoD-01｜正式输入合同与 Build Manifest

每次正式构建必须生成机器可读的 build manifest，至少记录：

- formal parameter set 版本 / hash；
- approved override set 版本 / hash；
- Geometry Dependency Matrix 版本 / hash；
- Blender 版本；
- generation script 版本 / commit；
- 本次实际使用的 DIRECT_GEOMETRY_INPUT / DERIVED_GEOMETRY_RULE；
- 实际启用的 REASONABLE_COMPLETION / override；
- 尚未解决但允许进入 P2.2 的 UNKNOWN / bounded limitations。

禁止存在 manifest 外的历史几何输入。

### DoD-02｜主体结构范围完整

正式候选模型必须覆盖 P2.2 已批准范围：

1. 柱网 / grid；
2. 柱；
3. 主要梁架 / primary frame；
4. 斗栱拓扑骨架 / medium LOD bracket topology；
5. 屋顶控制几何 / roof control geometry；
6. 主要出檐、山面与主体空间关系。

必须形成一个空间上连贯的完整主体，不接受只完成单榀、单节点、单立面或局部样板后宣称 P2.2 完成。

### DoD-03｜参数驱动与禁止 Naked Historical Constants

所有会影响正式主体几何的历史/复原数值必须来自：

- P2.1 formal parameter set；或
- 经 Product Owner 批准的独立 override / REASONABLE_COMPLETION；或
- 由上述参数明确计算得到的派生规则。

脚本中允许存在纯工程常量，例如集合名、数值容差、数学常数、坐标轴约定；但不得出现无法追溯到 P2.1 的“历史尺寸裸常量”。

任何派生值必须能够反查其 source parameter IDs / formula。

### DoD-04｜关键几何与参数一致性机器验证

必须建立自动几何验证，至少覆盖：

- 开间 / 进深柱网数量与拓扑；
- 柱数量与柱位；
- 柱高生产解析值；
- 主要梁架层级与关键跨度；
- 斗栱跳数 / 出跳拓扑等 P2.2 medium-LOD 结构关系；
- 屋顶主要控制高度 / 举折链；
- 主要出檐 / 山面控制关系。

参数驱动的目标尺寸必须在构建前声明的 machine tolerance 内通过；不得在看到结果后反向放宽 tolerance。

OBSERVED_REFERENCE / VALIDATION_REFERENCE 与 reconstructed candidate 不要求被强行拟合成同一数值，但二者关系必须在 validation report 中明确。

### DoD-05｜Z-006-RC-01 与全部合理补全保持可替换

`Z-006-RC-01 = 11 × MOD-006` 必须以独立、可替换生产候选进入几何流程：

- 不得把 3534.3 mm 写回 Z-006；
- 不得把 3534.3 mm 烘焙为无来源常量；
- build manifest 必须显示其 `REASONABLE_COMPLETION / D-023 / replaceable` 身份；
- 改变或撤回 RC-01 后，模型必须能够通过重新构建反映变化，而不是手工修模。

现有其他 REASONABLE_COMPLETION 同样遵守这一规则。

### DoD-06｜UNKNOWN、转角与原真性边界不被几何掩盖

P2.2 必须继续执行 CG-02～CG-06：

- `DG-114` 继续作为 `BOUNDED_NON_BLOCKING`，P2.2 不借机创造统一小斗历史规格；
- `HIS-002` 继续作为 metadata / authenticity boundary；无证据构件的 `originality_status` 默认 `unknown`；
- 未解决的转角 45° 精确节点、榫卯落位、隐衬角栿/隐角梁冲突，只允许建立**中等 LOD 拓扑骨架 / bounded placeholder**；
- 不得因 Blender 中出现完整物体而把证据等级自动升级为 CONFIRMED 或 `963_confirmed`。

### DoD-07｜Geometry Metadata 与 Evidence Traceability

主体模型中的主要对象或对象族必须能够追溯到生成依据，至少具有或可由 manifest 唯一映射：

- `historical_state_tag`
- `evidence_class`
- `source_layer`
- `originality_status`
- `parameter_ids` 或等价参数引用
- 对 REASONABLE_COMPLETION / override 的显式标识

对象命名必须稳定、可机器识别，不以随机 Blender 默认名称作为正式生产接口。

### DoD-08｜确定性重建、技术完整性与人工结构审核

必须证明同一正式输入可以确定性重建主体模型：

- 从干净场景 / 明确基线执行 generation script；
- 连续两次构建的正式对象集合、对象命名、数量、关键尺寸和 topology summary 一致；
- Blender 保存后独立重开无关键几何丢失或 broken links；
- Local Blender 3.6 基线可维护，不依赖未经批准的 Blender 4.5-only 特性；
- 至少输出平面 / 正立面或侧立面 / 轴测（或等价三视图）审核图，供 Product Owner 人工检查整体结构关系。

完整 Local 3.6 ↔ Cloud 4.5 roundtrip 最终 QC 可留到 P2.3，但 P2.2 不得主动引入已知与 3.6 不兼容的核心生产依赖。

### DoD-09｜正式产物、验证报告与 Canonical Archive

P2.2 Gate Review 前必须形成并归档：

- 正式 generation script；
- build manifest；
- machine geometry validation / tests；
- deterministic rebuild evidence；
- P2.2 validation report；
- 至少三张结构审核图；
- 本地正式 `.blend` 路径、文件 hash 与 Blender 版本记录；
- GitHub canonical commit 记录脚本、manifest、validation evidence 与审核图。

`.blend / .blend1` 继续遵守项目既有规则保持 local-only，不因 P2.2 成为正式模型就强制提交普通 Git。

## 5. Gate Decision Rule

### PASS

只有同时满足以下条件才可建议 P2.2 PASS：

- DoD-01～DoD-09：**9 / 9 PASS**；
- 主体结构范围完整；
- machine geometry validation 全部 PASS；
- deterministic rebuild PASS；
- 没有新的未批准 geometry-critical input；
- 没有 naked historical constants；
- 没有把 UNKNOWN / REASONABLE_COMPLETION 静默升级为历史事实；
- Product Owner 完成人工结构审核并明确批准。

### HOLD

出现以下任一情况即 HOLD：

- 正式几何依赖未进入 build manifest；
- 主体范围有关键系统缺失；
- 模型依赖手工修模才能成立；
- 关键尺寸 / 拓扑机器验证失败；
- 存在无法追溯的历史尺寸常量；
- RC / override 被烘焙或无法替换；
- UNKNOWN 被偷偷填数或真实性等级漂移；
- 转角 / 榫卯 / 隐角梁争议被伪装成精确历史结论；
- 确定性重建失败；
- Blender 独立重开损坏；
- validation evidence 或 canonical archive 不完整。

## 6. Production Boundary

P2.2 允许第一次生成正式 Blender 历史候选几何，但必须限制在**主体结构中等 LOD**。

在 P2.2 PASS 前：

- 不进入 P2.3 最终整合复原候选；
- 不进行最终材质 / 纹理 / 灯光 / 展示渲染；
- 不把局部高精细节点完成度当作整体 Gate PASS 的替代；
- CG-02～CG-06 持续强制生效。

## 7. Proposed First Engineering Task

DoD 获 Product Owner 锁定后，下一项实际 Codex 工程任务建议创建为 **T-007**，目标是：

> 建立 P2.2 正式参数读取 / build manifest / Blender 主体结构生成器，并生成第一版可重复构建的中等 LOD Structural Skeleton Candidate。

T-007 应优先完成“完整主体 + 参数追溯 + 自动验证”，而不是优先追求斗栱雕琢、榫卯细节或视觉精修。

---

**DRAFT NOTE**：本文件尚未锁定。只有 Product Owner 明确批准后，才转为 `LOCKED / PRODUCT OWNER APPROVED`，并据此创建正式 T-007 Task Contract。