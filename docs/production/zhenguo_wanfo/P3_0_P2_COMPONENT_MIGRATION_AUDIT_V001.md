# P3.0 P2→P3 Component Migration Audit V001｜镇国寺万佛殿

Status: **WORKING DRAFT / SEMANTIC AUDIT STARTED**  
Date: 2026-09-13  
Input: `production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`

## 1. Purpose

本文件审计 P2 的工程 `component_families`，判断其在 P3 构件体系中究竟属于：

- 真正具有历史构件身份的构件类型；
- 当前仅用于表达证据边界的几何代理；
- 参数化 / 诊断控制对象；
- 连续几何包络；
- 尚不能确定身份的 unresolved component。

核心规则：**P2 engineering family ≠ historical component type。**

同时必须分离两个维度：

1. `ontology_identity`：它在古建筑知识体系里是什么；
2. `current_asset_role`：P2 当前这个 3D 资产是真实构件候选、近似代理、控制对象还是包络。

因此，一个 family 可以对应真实构件概念，但当前 P2 几何仍只是 `GEOMETRIC_PROXY`。

## 2. Initial 11-Family Audit

| P2 Family | P2 Engineering Meaning | P3 Ontology Candidate | Current Asset Role | Initial Decision | P3 Follow-up |
|---|---|---|---|---|---|
| `COLUMN` | perimeter column；直径由 Z-002，柱高由 Z-006-RC-01，含角柱升高 | `HISTORICAL_COMPONENT`｜柱 | `RECONSTRUCTED_COMPONENT_CANDIDATE` | **保留构件身份，但不得把 RC 柱高写成历史事实** | 建立“柱”正式 Registry；Variant 区分位置/尺寸；Z-006 继续 UNKNOWN |
| `PURLIN` | roof-control purlin；由 FR/ROOF/OUT 参数驱动 | `HISTORICAL_COMPONENT_TYPE`｜中文规范名待史料术语核定 | `RECONSTRUCTED_COMPONENT_CANDIDATE / MEDIUM_LOD` | **构件概念成立，名称与分型待证据核定** | 核对报告对槫/檩等术语；区分脊部/各架位置 Variant |
| `RAFTER` | roof slope control；端点来自 FR/ROOF，spacing 为 diagrammatic | `HISTORICAL_COMPONENT_TYPE`｜椽类 | `GEOMETRIC_PROXY` | **构件类型成立，但当前数量/间距不能视为历史精确复原** | Registry 分离“椽构件概念”与“P2 diagrammatic placement” |
| `BRACKET_ARM` | DG-110/111/112/113 aggregate jump controls；equal subdivisions 仅 graphic topology | `UNRESOLVED_COMPONENT / ASSEMBLY_SUBPROXY` | `GEOMETRIC_PROXY` | **不得直接登记成单一历史“栱/昂”构件** | 回到斗栱证据，拆解实际栱、昂及铺作构成后再建 Component Master |
| `BRACKET_CONTACT` | MOD 参数生成的 diagrammatic contact block；明确不是 DG-114 small-dou spec | `GEOMETRIC_PROXY` | `GEOMETRIC_PROXY` | **不得命名为小斗或任何确定历史斗类构件** | 保留为 P2 proxy；待证据足够时由真实斗类构件替换 |
| `PRIMARY_FRAME` | principal frame；P2.2 endpoints + section envelopes | `UNRESOLVED_COMPONENT_SET` | `GEOMETRIC_PROXY` | **当前过粗，不能作为一个历史构件类型** | 后续按梁、枋及其他明确梁架成员拆分；名称必须回到证据来源 |
| `FRAME_SUPPORT` | P2.2 frame tier/post endpoint 的 diagrammatic connector；非 exact historical member/joint | `GEOMETRIC_PROXY` | `GEOMETRIC_PROXY` | **不是正式历史构件** | 待梁架构件识别后替换或仅保留为 diagnostic proxy |
| `FRAME_CONTROL` | tier/post controls；diagnostic-only bounded topology | `CONTROL_OBJECT` | `CONTROL_OBJECT` | **从历史构件目录排除** | 保留工程控制命名空间，不进入构件数量统计 |
| `GABLE_CONTROL` | gable guide；diagnostic-only | `CONTROL_OBJECT` | `CONTROL_OBJECT` | **从历史构件目录排除** | 保留工程控制命名空间 |
| `GRID_CONTROL` | bay grid；diagnostic-only | `CONTROL_OBJECT` | `CONTROL_OBJECT` | **从历史构件目录排除** | 保留工程控制命名空间 |
| `ROOF_ENVELOPE` | six continuous planar strips；no thickness claim | `ENVELOPE / SURFACE` | `ENVELOPE_SURFACE` | **不是历史构件** | 作为屋面形态控制层保留；不得计入瓦、椽、望板等构件 |

## 3. Initial Result

P2 的 11 families 当前不能解释为“11 种古建筑构件”。

初步语义分布：

- 明确 / 基本明确具有历史构件类型身份：`COLUMN`、`PURLIN`、`RAFTER`；
- 需要进一步拆分或证据核定的构件代理：`BRACKET_ARM`、`BRACKET_CONTACT`、`PRIMARY_FRAME`、`FRAME_SUPPORT`；
- 工程控制对象：`FRAME_CONTROL`、`GABLE_CONTROL`、`GRID_CONTROL`；
- 连续几何包络：`ROOF_ENVELOPE`。

注意：上述分类是 **P3.0 初审**，不是最终构件目录。尤其 `PURLIN / RAFTER / BRACKET_ARM / PRIMARY_FRAME` 的中文规范名、历史分型和实际构成必须回到 P1 证据包与原测绘报告核定后才能 LOCK。

## 4. Migration Rule

P3 不删除 P2 engineering family。迁移采用双层映射：

`P2 engineering object`  
→ `P3 ontology identity`  
→ `P3 asset fidelity / evidence state`

例如：

`RAFTER`  
→ 历史构件类型：椽类  
→ 当前 P2 资产：diagrammatic GEOMETRIC_PROXY  
→ 后续 P3.1：若证据允许，再建立正式 Component Master / Variants。

这样既保留 P2 的工程可复现性，又避免把中等 LOD 代理误当成历史精确构件。

## 5. Next Audit Work

在 P3.0 DoD 锁定后，正式工程应继续完成：

1. 从 P1 evidence package / direct page review 提取万佛殿明确出现的构件术语；
2. 建立 canonical Chinese terminology + aliases；
3. 对 P2 40 variants 做 40/40 迁移；
4. 对 P2 365 instances 做 365/365 迁移；
5. 建立 Component Registry Schema 与 machine validation；
6. 形成真正的万佛殿 Component Registry，而不是直接沿用 11-family 工程目录。
