# P3.0 Component Ontology V001｜构件本体与命名规则

Status: **T-009 IMPLEMENTED / P3.0 GATE REVIEW PENDING**

P2 engineering family、Blender object 与 mesh instance 均不自动等于历史构件或历史数量。构件身份与当前资产角色分别登记；证据等级不会因命名改变。

## 本体类型

- `HISTORICAL_COMPONENT`：有证据支持的构件类型概念；当前 P2 网格精度与历史原构数量另行判断。
- `ASSEMBLY_UNIT`：多个构件的组合单元；P3.0 预留，不由 P2 family 自动生成。
- `GEOMETRIC_PROXY`：证据或 LOD 受限时的替代几何，无精确历史构件身份。
- `CONTROL_OBJECT`：参数化定位或诊断对象，不是历史构件。
- `ENVELOPE_SURFACE`：连续外形包络或曲面，不是实体古建构件。
- `UNKNOWN_UNRESOLVED_COMPONENT`：构件身份或集合拆分未获证据支持，保持未决。

## 命名与 ID

- 中文名为概念名；英文 `canonical_name_en` 使用小写下划线键，跨建筑复用。报告原称与异名分别保存在 `historical_terms`、`aliases`，不能拿别名升级证据。
- `CMP-*` 表示可辨识的历史构件**类型概念**，`PRX-*` 表示代理，`CTL-*` 表示工程控制，`ENV-*` 表示包络，`UNR-*` 表示未决集合。`ASM-*` 为未来组合单元保留。ID 不含万佛殿名。
- 建筑专属 Variant ID 保留 P2 稳定 ID；新建筑可使用 `<CASE>-<COMPONENT>-V<序号>`。Instance ID 保留 P2 稳定放置 ID；新实例可用 `<CASE>-I<序号>`。Assembly ID 使用 `<CASE>-ASM-<序号>`。均不得以 ID 推断历史身份。
- `component_id` 表示类型/代理登记；`variant_id` 表示参数化版本；`instance_id` 表示机器放置。当前没有独立 P3.1 Master，`master_3d_asset.path = null`。

## 证据与统计

- `observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate` 三层不互换。
- `Z-006` 仍 `UNKNOWN / null / DO_NOT_LOCK`；`Z-006-RC-01` 仅为 D-023 批准的独立、可替换候选。
- `DG-114` 仍 UNKNOWN，接触代理不是小斗；`HIS-002` 逐构件原真性仍 unknown。45°转角、榫卯、隐角梁仍未决。
- 所有 365 个 P2 实例仅为机器放置；控制、代理与包络从历史构件统计排除。历史类型概念的 P2 放置也不能直接算作原构数量。

## 组合关系词汇（P3.2 预留）

`supports`, `supported_by`, `connects_to`, `inserted_into`, `receives`, `rests_on`, `spans_between`, `aligned_with`, `repeated_in`, `belongs_to_assembly`, `located_at`, `orientation`。关系记录使用 `relation / target_id / evidence_status`；本版不填未经核证的具体组合边。

## 依据

- `production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`；`docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`；`docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`；`docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md`；D-023、D-028～D-030。
