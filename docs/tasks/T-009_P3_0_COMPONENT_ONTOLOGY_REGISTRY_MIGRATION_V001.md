# 【中国古建筑3D复原｜T-009｜P3_0_COMPONENT_ONTOLOGY_REGISTRY_MIGRATION_V001｜构件本体、登记体系与P2全量迁移】

Status: **READY_FOR_LOCAL_EXECUTION**  
Think Level: **HIGH**  
Phase/Gate: P3 / P3.0  
Date: 2026-09-13

## 1. Objective

在 P2 冻结工程基线之上，把现有 `11 component families / 40 variants / 365 stable instances` 从工程生产结构升级为可解释、可登记、可复用、可扩展的古建筑构件知识与资产体系。

本任务只做：

> **Component Ontology → Naming/ID → Registry Schema → P2 Semantic Audit → 11/40/365 Migration → Validation**

本任务不新增 Blender 几何，不修改 P2 canonical `.blend`，不提高模型 LOD。

## 2. Authoritative Inputs

必须读取并遵守：

1. `docs/production/zhenguo_wanfo/P3_0_DEFINITION_OF_DONE_V001.md`（LOCKED / D-030）；
2. `docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md`；
3. `production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`；
4. `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`；
5. `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`；
6. `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`；
7. `production/zhenguo_wanfo/schema/evidence_aware_parameter_schema_v001.json`；
8. P1 approved evidence package under `docs/evidence/zhenguo_wanfo/`；
9. `docs/project_control/project_state.json`、`decision_log.md`、`acceptance_matrix.md`；
10. D-023、D-028、D-029、D-030 与 CG-02～CG-06。

如果历史术语、构件身份或结构角色不能由现有正式证据支持，必须标记 `UNKNOWN / UNRESOLVED_COMPONENT` 或保留为 proxy/control，不得凭经验静默确定。

## 3. Hard Boundaries

### 禁止事项

- 不新增或修改 Blender 几何；
- 不修改 P2 canonical model；
- 不把 P2 family 名称直接当作历史构件名称；
- 不把 Blender object / mesh instance 数量解释为历史构件数量；
- 不把 `GRID_CONTROL / FRAME_CONTROL / GABLE_CONTROL` 等控制对象登记成历史构件；
- 不把 `ROOF_ENVELOPE` 当成实体古建构件；
- 不把 `BRACKET_CONTACT` 静默解释为“小斗”；
- 不因为名称归一化而升级 CONFIRMED/HCI/RC/UNKNOWN；
- 不解决当前没有证据支持的 45° 转角、榫卯、隐角梁等问题。

### 必须保留的历史边界

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`；
- `Z-006-RC-01` 独立、可替换、D-023 traceable；
- `DG-114` 不代表统一小斗历史规格；
- `HIS-002` component originality 继续 unknown；
- observed / report ideal / reconstructed candidate 三层继续分离。

## 4. Required Outputs

至少生成以下正式文件：

1. `docs/production/zhenguo_wanfo/P3_0_COMPONENT_ONTOLOGY_V001.md`
2. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_ONTOLOGY_V001.json`
3. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_SCHEMA_V001.json`
4. `docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md`（升级为完整11/11审计）
5. `production/zhenguo_wanfo/registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json`
6. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_V001.json`
7. `production/zhenguo_wanfo/validation/P3_0_REGISTRY_VALIDATION_REPORT_V001.json`
8. `docs/production/zhenguo_wanfo/P3_0_REGISTRY_VALIDATION_REPORT_V001.md`

不得自行生成 P3.0 Gate PASS 或修改 Gate 结论；Product Owner / ChatGPT 负责最终 Gate Review。

## 5. Ontology Requirements

至少支持以下 ontology_type：

- `HISTORICAL_COMPONENT`
- `ASSEMBLY_UNIT`
- `GEOMETRIC_PROXY`
- `CONTROL_OBJECT`
- `ENVELOPE_SURFACE`
- `UNKNOWN_UNRESOLVED_COMPONENT`

每一个 P2 family 必须明确归类，并说明：

- P2 engineering meaning；
- P3 ontology type；
- 是否对应真实历史构件；
- 是否需要拆分 / 合并 / 重命名；
- 是否 diagnostic/control only；
- source/evidence；
- unresolved boundary。

## 6. Registry Requirements

Component Registry 每条正式记录至少支持：

- component_id
- canonical_name_zh
- canonical_name_en / key
- aliases / historical_terms
- category / ontology_type
- function
- structural_role
- typical_position
- source_building / period
- parameter_ids
- evidence_by_attribute
- source_references
- historical_state / originality_status
- master_3d_asset
- variant_ids
- instance_ids
- assembly_relations
- applicability / reuse_scope
- known_unknowns / interpretation_boundary
- version / status

没有独立 Master 3D 的构件在 P3.0 可以明确写 `null / NOT_YET_CREATED`；P3.0 不因此创建几何。

## 7. Migration Requirements

### Family

必须完成：`11 / 11`。

P2 families：

- BRACKET_ARM
- BRACKET_CONTACT
- COLUMN
- FRAME_CONTROL
- FRAME_SUPPORT
- GABLE_CONTROL
- GRID_CONTROL
- PRIMARY_FRAME
- PURLIN
- RAFTER
- ROOF_ENVELOPE

### Variant

必须完成：`40 / 40`。

每个 P2 variant 必须映射到一个合法 P3 record，不得 orphan；必须保存参数来源、证据语义与可替换性。

### Instance

必须完成：`365 / 365`。

每个 P2 instance 必须可追踪至：

`P3 registry record + variant + placement + evidence metadata`

并明确：control/envelope/proxy 是否计入 historical component statistics。

## 8. Assembly-ready Vocabulary

Registry schema 至少预留：

- supports / supported_by
- connects_to
- inserted_into / receives
- rests_on
- spans_between
- aligned_with
- repeated_in
- belongs_to_assembly
- located_at / orientation

本任务只建立关系词汇和数据结构，不要求完成 P3.2 的完整 Assembly Graph。

## 9. Validation

编写确定性校验脚本或等价检查，至少验证：

- ontology_type 合法；
- component/variant/instance ID 唯一；
- required fields 完整；
- family coverage = 11/11；
- variant coverage = 40/40；
- instance coverage = 365/365；
- orphan family/variant/instance = 0；
- evidence metadata 保留；
- control/envelope 不会静默成为 historical component；
- registry JSON 可重复生成且 deterministic。

若发现 P2 manifest 数量或关系与已记录基线不一致，停止并报告，不自行修正 P2 基线。

## 10. Local Execution / Git Rules

执行前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git status
git pull --ff-only origin main
```

若有不明 tracked changes 或 pull 非 fast-forward：停止，不 force、不覆盖。

工程完成后：

- 先运行 validation；
- `git status` 核对只包含 T-009 授权范围；
- commit message 建议：`p3.0: build component ontology registry migration v001`；
- push `main`；
- 回传 commit SHA、11/40/365 coverage、orphan count、validation 结果、生成文件清单和任何 unresolved 项。

## 11. Completion Report Format

必须回报：

- STATUS: COMPLETE / BLOCKED / FAILED
- FAMILY_COVERAGE: x/11
- VARIANT_COVERAGE: x/40
- INSTANCE_COVERAGE: x/365
- ORPHAN_FAMILY / VARIANT / INSTANCE
- ONTOLOGY_VALIDATION
- REGISTRY_SCHEMA_VALIDATION
- EVIDENCE_BOUNDARY_VALIDATION
- DETERMINISM
- FILES_CREATED / UPDATED
- COMMIT_SHA
- UNRESOLVED / BLOCKERS

T-009 COMPLETE 不自动等于 P3.0 PASS；完成后由 ChatGPT 对照 P3.0 DoD 做 Gate Review，并由 Product Owner 最终批准。
