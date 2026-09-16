# P3.3｜构件驱动整殿重建

## Definition of Done V001｜LOCKED / PRODUCT OWNER APPROVED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Gate：P3.3｜构件驱动整殿重建
- Engineering subtitle：Component-driven Building Reconstruction
- Version：V001
- Status：LOCKED / PRODUCT OWNER APPROVED
- Decision：D-047
- Approval date：2026-09-16

## 1. Gate 目标

P3.3 的目标不是再次手工制作一座“看起来完整”的万佛殿，也不是复制 P2 已存在的整合模型。

P3.3 必须证明：**整座万佛殿能够从正式构件身份 + P3.2 构件组合关系 + 建筑层级参数出发，被系统性、确定性地重新生成，并且全过程保持历史证据、不确定性和工程控制边界。**

P3.3 继承：

- P3.1 已批准的 Component Master / Registry / evidence boundary；
- P3.2 已批准的五类基础关系、接口/定位、Assembly Unit、runtime instance、building-level parameter 与 validator；
- P1/P2 的正式建筑参数、测绘证据、UNKNOWN / REASONABLE_COMPLETION 等证据语义；
- P2 frozen engineering baseline 仅用于对照与验证，不得作为“预摆好的整殿位置输入”绕过构件驱动重建。

## 2. Definition of Done｜9/9 required

| DoD | 验收项 | PASS 标准 | Cloud Mode 分类 |
|---|---|---|---|
| DoD-01 | 正式输入基线 | 锁定整殿重建唯一允许使用的正式 Component Registry、P3.2 Assembly Schema / relationship definitions、建筑参数、evidence 数据及 approved overrides；P2 既有对象位置、手工 transform 或已烘焙整殿结果不得作为正式生成输入。 | CLOUD_EXECUTABLE |
| DoD-02 | 整殿 Assembly Graph | 建立建筑级构件实例与组合关系图。进入正式整殿重建范围的对象必须能够追溯到构件身份、组合关系、building-level location / role 与父级关系；不得出现失去 Registry 身份的匿名正式构件。 | CLOUD_EXECUTABLE |
| DoD-03 | 建筑参数驱动与参数传递 | 柱网、开间、主要标高、梁架层位、重复数量及其他正式建筑级尺寸/位置必须通过显式参数与规则传递到构件实例。非历史 canonical reference specimen 尺寸不得直接进入建筑实际尺寸。 | CLOUD_EXECUTABLE |
| DoD-04 | 全殿语义覆盖与对象 accounting | 对整殿重建范围建立完整对象 accounting：正式构件生成、Proxy、Control、Envelope、Deferred、UNKNOWN / unresolved 等均须显式登记和解释；不得为了让整殿生成成功而静默删除、跳过或历史化对象。 | CLOUD_EXECUTABLE |
| DoD-05 | 确定性整殿生成 | 必须能够从干净状态仅依靠正式输入、构件身份、组合关系和参数生成整殿候选；不得依赖 Blender 中预先摆放位置、手工逐件 transform 或复制后失去身份的对象。正式几何生成若依赖批准的本地 Blender 基线，则 Cloud Mode 中最多到 DESIGN COMPLETE / LOCAL EXECUTION OR REVIEW PENDING。 | HYBRID / LOCAL EXECUTION MAY BE REQUIRED |
| DoD-06 | 空间、几何与结构一致性 | 重建结果在柱网、主要标高、梁架层级、建筑轮廓、构件重复关系等关键指标上与正式测绘/批准基线一致；所有超出 tolerance 的差异必须能够追溯到参数、证据状态或 approved reconstruction rule，不得以人工视觉近似替代。 | HYBRID / LOCAL REVIEW MAY BE REQUIRED |
| DoD-07 | Evidence Boundary 保持 | UNKNOWN、REASONABLE_COMPLETION、Proxy、Control、Envelope、Deferred、工程连接等状态在整殿重建后仍保持显式，不因整殿“完成”自动升级为历史事实。六椽栿 historical full length UNKNOWN/null 与其他既有 evidence boundary 必须继续有效。 | CLOUD_EXECUTABLE |
| DoD-08 | 机器验证、Hard Fail 与参数 Mutation | 建立/扩展自动验证，至少检查身份断裂、缺失/孤立实例、非法关系、参数传递错误、reference length leakage、silent omission / historicization、manual-baked dependency 等；至少完成一次建筑参数 mutation → rebuild → validation → canonical restore，证明结果具备系统响应能力。 | CLOUD_EXECUTABLE / HYBRID IF GEOMETRY RUN REQUIRED |
| DoD-09 | 独立重建与最终 Gate Evidence Package | 完成适用的 independent reopen / canonical rebuild / machine validation / formal review images / visual review，并形成可追溯 Gate Evidence Package。若 DoD 要求依赖 local-only `.blend`、本地 Blender binary 或交互式检查，必须在正式本地执行完成前保持 PENDING，不得在 Cloud Mode 中伪判 PASS。 | HYBRID / LOCAL_MAC_REQUIRED FOR LOCAL-ONLY EVIDENCE |

## 3. Gate Hard Fail

### HF-01｜REFERENCE_LENGTH_LEAKS_INTO_BUILDING

六椽栿 `canonical_reference_length_mm=1000` 以及其他 non-historical canonical reference specimen 尺寸仅用于标准化参考。若直接进入万佛殿实际建筑尺寸或实际构件长度，立即 FAIL。

### HF-02｜SILENT_HISTORICIZATION

UNKNOWN、REASONABLE_COMPLETION、Proxy、Control、Envelope、Deferred 或其他非历史确定对象/关系，不得因为进入整殿重建而被静默提升为历史事实或历史确定几何。发生即 FAIL。

### HF-03｜BAKED_MANUAL_BUILDING

如果整殿结果必须依赖 P2/Blender 中已有对象位置、现成 transform 或人工逐件摆放，不能由正式构件身份 + 组合关系 + 建筑参数从干净状态重新建立，则 FAIL。

### HF-04｜SILENT_BUILDING_OMISSION

任何属于正式整殿重建 accounting 范围的对象或未解决项，不得为了让 generator / validator 通过而被静默删除、跳过或从报告中消失。发生即 FAIL。

### HF-05｜BROKEN_COMPONENT_IDENTITY

正式构件进入整殿重建后不得变成无 Registry 身份、无来源追溯、无 parent/relationship 语义的普通 mesh / anonymous copy。发生即 FAIL。

## 4. Cloud Mode 执行边界｜RC-014

2026-09-16 至 2026-09-20 执行 RC-014：

- `CLOUD_EXECUTABLE`：可在 GitHub + Codex Cloud 中完整实现和机器验证；
- `DESIGN_ONLY`：可完成 Schema、Registry、manifest、算法、generator/validator 设计，但正式执行/某项验收依赖本地环境；
- `LOCAL_MAC_REQUIRED`：访问 local-only `.blend`、本地 Blender binary 或仅本地可完成的 binary/reopen/render/interactive inspection。

**Cloud Mode 只改变执行环境，不降低 P3.3 DoD。**

Cloud Mode 内可以优先推进 DoD-01～04、DoD-07 以及 DoD-08 的 Cloud-native 部分；DoD-05/06/09 中实际依赖本地 Blender 或 local-only binary 的部分必须保留 PENDING，不能为了推进进度提前 PASS。

## 5. P3.3 Non-goals

P3.3 不要求：

- 证明所有构件、榫卯与隐蔽连接均为北宋原始做法；
- 在缺乏证据时补齐六椽栿 historical full length；
- 消除 Z-006、DG-114、HIS-002、45°转角、隐藏连接、隐角梁等既有证据边界；
- 完成结构力学计算；
- 完成最终高精度材质、纹理、灯光或影视级渲染；
- 把 Proxy / Control / Envelope / Deferred 对象强行替换成历史构件；
- 宣称整殿模型等于“完全还原963原貌”；
- 为了达到视觉完整而放弃 Registry、关系、参数或证据追溯。

## 6. P2 / P3.1 / P3.2 / P3.3 边界

- P2：建立 evidence-aware 参数化整合复原候选与工程基线。
- P3.1：解决“构件是什么”，建立正式 Component Master / Registry。
- P3.2：解决“构件怎样组合”，建立关系、接口、定位和代表性组合机制。
- P3.3：解决“如何仅依靠正式构件系统、组合关系和建筑参数重新组成整座万佛殿”。

P3.3 PASS 的核心判断不是视觉上是否“像一座完整的殿”，而是：

> **整殿是否已经成为一个由正式构件身份、显式组合关系、建筑参数和证据状态共同驱动、可重新生成、可验证、可追溯的系统。**

## 7. Gate 判定

P3.3 关闭必须同时满足：

1. DoD 9/9 PASS；
2. Gate Hard Fail = 0；
3. 所有被标为 LOCAL_MAC_REQUIRED 的正式验收项已真实完成，不存在用 Cloud 替代环境伪验收；
4. 正式 Gate Evidence Package 完整；
5. Product Owner Approval。

在上述条件满足前，P3.3 不得标记 PASS / CLOSED。

## 8. Engineering Authorization

本 DoD 获 Product Owner 批准后：

- P3.3 工程规划与 Task Contract 创建正式解锁；
- 每个任务在 RC-014 有效期内必须先标记 `CLOUD_EXECUTABLE`、`DESIGN_ONLY` 或 `LOCAL_MAC_REQUIRED`；
- Task Contract 的建立不等于执行授权；
- 工程任务必须继续遵守 RC-014 的 `ONE TASK = ONE BRANCH = ONE PR`；
- Product Owner 保留任务执行、Task PASS 与最终 Gate PASS 的批准权。

## 9. Language Governance

本文件遵循 Governance 4.6《项目语言与术语分层规则》：古建筑内容中文优先；项目管理/工程控制可保留成熟英文术语；机器实现层保持稳定英文字段。