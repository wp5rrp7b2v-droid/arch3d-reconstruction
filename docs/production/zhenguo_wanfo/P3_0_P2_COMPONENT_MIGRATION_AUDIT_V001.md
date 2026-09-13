# P3.0 P2→P3 Component Migration Audit V001｜镇国寺万佛殿

Status: **11/11 COMPLETE / T-009 VALIDATED / P3.0 GATE REVIEW PENDING**

P2 input: `production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`。完整 40 个 variant 与 365 个 instance 的逐条映射见 `production/zhenguo_wanfo/registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json` 与 `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_V001.json`。

| P2 family | P2 工程语义 | P3 类型 / 当前资产 | 对应真实历史构件 | 拆分 / 命名决策 | 控制/诊断专用 | 证据 | 未决边界 | Variant / Instance |
|---|---|---|---|---|---|---|---|---|
| `BRACKET_ARM` | DG-110/111/112/113 and MOD-002; equal subdivisions are graphic topology only | `UNKNOWN_UNRESOLVED_COMPONENT` / `GEOMETRIC_PROXY` | 未决 | 保留代理；后续按实证拆分栱、昂及铺作组合，不把四跳均分网格当成构件。 | 否 | `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`, `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md` | DG-110～113 只控制总体出跳；45°构件、栱昂分件、榫卯未定。 | 8 / 88 |
| `BRACKET_CONTACT` | diagrammatic contact block from MOD-003/004/005 x MOD-002; not a DG-114 small-dou specification | `GEOMETRIC_PROXY` / `GEOMETRIC_PROXY` | 否 | 保留端点代理；不得重命名为小斗。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md` | DG-114 为 UNKNOWN / DO_NOT_LOCK；不能据此给散斗、齐心斗或交互斗统一规格。 | 1 / 88 |
| `COLUMN` | Z-002 diameter; Z-006-RC-01 height; Z-005 corner rise | `HISTORICAL_COMPONENT` / `RECONSTRUCTED_COMPONENT_CANDIDATE` | 类型概念成立；P2 实例非历史计数 | 归入柱构件概念；位置和候选尺寸只作为建筑专属变体。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md` | Z-006 963柱高 UNKNOWN；Z-006-RC-01 仅是 D-023 可替换生产候选；角柱生起为报告猜测。 | 2 / 12 |
| `FRAME_CONTROL` | retain as diagnostic-only bounded topology | `CONTROL_OBJECT` / `CONTROL_OBJECT` | 否 | 保留工程控制命名空间，不迁入历史构件目录。 | 是 | `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md` | 控制长度和位置不能解释为实体梁、枋或节点。 | 7 / 54 |
| `FRAME_SUPPORT` | separate P2.3 diagrammatic connector instances at approved P2.2 endpoints; not exact historical member or joint | `GEOMETRIC_PROXY` / `GEOMETRIC_PROXY` | 否 | 保留代理；未来按确证梁架成员替换。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md` | 端点与截面为中等 LOD；不能命名为托脚、蜀柱等具体历史构件。 | 7 / 54 |
| `GABLE_CONTROL` | diagnostic-only; roof-envelope end edge is visible | `CONTROL_OBJECT` / `CONTROL_OBJECT` | 否 | 保留诊断控制命名空间。 | 是 | `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md` | 山面控制线不能解释为博风板、角梁或其他实体构件。 | 1 / 4 |
| `GRID_CONTROL` | diagnostic-only | `CONTROL_OBJECT` / `CONTROL_OBJECT` | 否 | 保留定位控制命名空间。 | 是 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md` | 线段数不是柱数或历史构件数。 | 2 / 8 |
| `PRIMARY_FRAME` | P2.2 approved endpoints and MOD-003/004/005 section envelopes | `UNKNOWN_UNRESOLVED_COMPONENT` / `GEOMETRIC_PROXY` | 未决 | 保留集合代理；后续按证据拆分六椽栿、梁、枋等，不能把整个 family 命名为单件。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md` | 六椽栿、阑额等术语有证据，但 P2 两种网格不能逐一等同具体历史成员。 | 2 / 8 |
| `PURLIN` | FR-007, ROOF-007/008/009, OUT-003 and module section envelopes | `HISTORICAL_COMPONENT` / `RECONSTRUCTED_COMPONENT_CANDIDATE` | 类型概念成立；P2 实例非历史计数 | 以报告使用的槫为类名；具体撩风/下平/上平/脊槫分型暂不由 P2 单一 variant 锁定。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md` | 当前 P2 截面、数量和排布为 roof-control 候选，不是逐根原构清单。 | 1 / 7 |
| `RAFTER` | FR-007 and ROOF-007/008/009 endpoint segments; diagrammatic spacing | `HISTORICAL_COMPONENT` / `GEOMETRIC_PROXY` | 类型概念成立；P2 实例非历史计数 | 保留椽构件概念，P2 三种坡段仅作图示代理。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md` | P2 36 个图示段的间距、数量、翼角做法不能作为历史精确椽布置。 | 3 / 36 |
| `ROOF_ENVELOPE` | six continuous planar strips joining approved control coordinates; no thickness claim | `ENVELOPE_SURFACE` / `ENVELOPE_SURFACE` | 否 | 保留零厚度包络层，不登记为瓦、望板或实体屋面构件。 | 否 | `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`, `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md` | 六片平面条带无厚度、铺瓦及真实曲面构造主张。 | 6 / 6 |

## 迁移与边界

- 11 个 family 映射到 11 条 P3 登记记录；40 个 variant 与 365 个 instance 保留原 ID、参数、变换和证据元数据，orphan 为 0。
- `COLUMN`、`PURLIN`、`RAFTER` 的历史**类型概念**有依据；当前网格仍按各自 asset role 解释，不能把 12/7/36 个放置当历史清单。
- `BRACKET_ARM`、`PRIMARY_FRAME` 是未决集合/代理，待 P3.1 回证据拆分。`BRACKET_CONTACT` 不能解释为小斗。
- `FRAME_CONTROL`、`GABLE_CONTROL`、`GRID_CONTROL` 是控制对象；`ROOF_ENVELOPE` 是零厚度包络；均不计历史构件。
- `Z-006`、`Z-006-RC-01`、`DG-114`、`HIS-002` 和三层语义按原参数逐项保留。
