# T-015｜构件组合关系基础工程审核摘要 V001

- 状态：**PASS / PRODUCT OWNER APPROVED / CLOSED / D-042**。
- 权威顺序：P3.2 DoD V001 → T-015A Design V001 → T-015 Contract → 既有 Registry / Master。
- 工程边界：仅建立数据结构、资格规则、接口、Validator 与负向测试；未建立历史组合实例、Blender 组合几何或 P3.3 文件。
- Engineering commit：`49b0415479d811a26d4f44588d15cd863467edf4`。
- ChatGPT structural review：PASS。
- Product Owner approval：2026-09-14 / D-042。
- **本任务批准不等于 P3.2 Gate PASS。**

## 1. 正式节点：6/6

| 既有 component_id | 中文名称 | 身份来源 |
|---|---|---|
| `CMP-COLUMN-001` | 柱 | P3.1 approved Master |
| `CMP-LUDOU-COLUMN-001` | 柱头栌斗 | P3.1 approved Master |
| `CMP-DOU-SINGLE-LONGKAI-001` | 单向长开斗 | P3.1 approved Master |
| `CMP-DOU-INTERACTIVE-001` | 交互斗 | P3.1 approved Master |
| `CMP-FRAME-LOWER-SIX-CHUANFU-001` | 下六椽栿 | P3.1 approved Master |
| `CMP-FRAME-UPPER-SIX-CHUANFU-001` | 上六椽栿 | P3.1 approved Master |

每个正式 `node_id` 等于原有 `component_id`；未生成新 Master 身份。节点的 `evidence_status` 为 `SOURCE_ATTRIBUTE_LEVEL_ONLY`，只提示需回读各 Master 的逐属性证据，不是新的历史证据等级。Proxy、Control、Envelope、Deferred、UNKNOWN 仅按资格规则进入工程引用；它们不得被自动提升为历史正式构件。Deferred 须声明工程用途。

## 2. 关系类型：5/5

| enum | 中文主名 | 本轮机器边界 |
|---|---|---|
| `SUPPORT` | 承托 | 承托者指向被承托者；有向、无环。 |
| `CONNECT` | 连接 | 直接连接存在不推出具体榫卯已知。 |
| `LOCATE` | 定位 | 基准决定位置或方向，不推出连接；有向、无环。 |
| `REPEAT` | 重复 | 必须有数量、方向、间距、起点和参数来源。 |
| `BELONG` | 从属 | 成员指向组合单元；组织层级无环且单一父级。 |

本轮未登记任何**实际万佛殿构件关系断言**。测试中的关系均标记为合成验证数据，仅用于证明错误能被拒绝。

## 3. 接口与定位合同

6 个 Master 各有局部原点点基准、主轴基准、局部下参考面，共 18 个最小接口。这些接口由既有 Master 局部原点、轴向及外包络语义表达，证据状态为工程 `PROJECT_RULE`，不声称历史接触面或榫卯细节已知。正式定位记录必须引用接口、关系和建筑层级参数；Blender 世界坐标只能作为计算结果。六椽栿实际组合长度须有独立建筑层级参数，不能从 1000 mm canonical reference specimen 直接继承。

### 后续接口注意点（非 T-015 阻断项）

T-015 的 18 个接口足以证明 V001 接口体系和 Validator 成立，但后续建立真实代表性组合关系时，不得把统一的“局部下参考面”机械视为所有历史承托/连接界面。下一项代表性组合验证应按实际组合需要显式建立或验证上承托基准面、下承托基准面、中心/轴线定位基准等接口，并继续区分工程组合接口与有直接史料支持的历史接触关系。

## 4. 保持 UNKNOWN 的内容

- `Z-006` 历史柱高：UNKNOWN / null；`Z-006-RC-01` 仍是可替换 `REASONABLE_COMPLETION` 候选。
- `DG-114` 统一小斗规格：UNKNOWN；Proxy 接触块不是小斗。
- `HIS-002` 逐构件 963 原真性：unknown。
- 六椽栿历史全长：UNKNOWN / null；1000 mm 仅为非历史、可替换参考样件长度。
- 45° 转角、榫卯、隐藏连接与隐角梁：未补造历史解释。

## 5. 机器结果与保护资产

运行 `python3 production/zhenguo_wanfo/scripts/validate_p3_2_relationship_foundation_v001.py --report` 可重算机器报告；`--graph <JSON路径>` 可验证后续组合记录。最终结果见 `production/zhenguo_wanfo/validation/P3_2_RELATIONSHIP_FOUNDATION_VALIDATION_V001.json`：31/31 静态检查 PASS，21/21 负向测试按预期拒绝。三项 Gate Hard Fail 均有触发测试：`REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`、`SILENT_HISTORICIZATION`、`BAKED_MANUAL_ASSEMBLY`；canonical 数据中三者均为 0。

P2 冻结清单 19/19 SHA256 与原记录一致；6 个 P3.1 Master 本地二进制 SHA256 与 Registry 一致。独立 Git commit diff 核对 `2685a80 → 49b0415` 仅新增 8 个 T-015 文件，P2 / P3.1 既有 tracked 文件无修改；既存未跟踪 PDF、PoC、output 内容未被本任务处理。

## 6. Final Review Conclusion

- T-015 Engineering：**PASS**
- ChatGPT Structural Review：**PASS**
- Product Owner：**APPROVED / CLOSED / D-042**
- P3.2 Gate：**ACTIVE / NOT PASS**
- Recommended next action：设计下一项“代表性构件组合关系验证”任务，开始验证竖向承托链、横向梁架链与重复关系，但不得进入 P3.3 整殿重建。