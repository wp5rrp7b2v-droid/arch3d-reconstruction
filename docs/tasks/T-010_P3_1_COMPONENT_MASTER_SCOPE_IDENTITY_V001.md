# 【中国古建筑3D复原｜T-010｜P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001｜构件Master资格矩阵与证据身份解析】

Status: **READY_FOR_LOCAL_EXECUTION**  
Think Level: **HIGH**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13

## 1. Objective

在已锁定的 P3.1 Definition of Done V001 基础上，完成正式 Component Master 生产之前的资格审查与证据身份解析。

本任务只做：

> **Registry / Evidence Review → Master Eligibility Matrix → Historical Component Identity Resolution → Validation**

本任务不创建任何新的 Blender 构件几何，不建立 Component Master `.blend`，不批量生产 Variant。

T-010 的核心问题是：

> “现阶段哪些对象有足够证据成为正式 Component Master？哪些必须继续保持 Proxy / Control / Envelope / Deferred？P1 已直接核实但 P2 尚未独立表达的真实构件，哪些应新增为 P3.1 Master 候选？”

只有本任务完成并通过 ChatGPT / Product Owner 审核后，后续 P3.1 几何任务才可以按批准后的 `MASTER_REQUIRED` 清单启动。

## 2. Authoritative Inputs

必须完整读取并遵守：

1. `docs/production/zhenguo_wanfo/P3_1_DEFINITION_OF_DONE_V001.md`（LOCKED / D-032）；
2. `docs/production/zhenguo_wanfo/P3_0_COMPONENT_ONTOLOGY_V001.md`；
3. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_ONTOLOGY_V001.json`；
4. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_V001.json`；
5. `production/zhenguo_wanfo/registry/P3_0_COMPONENT_REGISTRY_SCHEMA_V001.json`；
6. `docs/production/zhenguo_wanfo/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.md`；
7. `production/zhenguo_wanfo/registry/P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001.json`；
8. P1 approved evidence package under `docs/evidence/zhenguo_wanfo/`，尤其：
   - `P1_2_DIRECT_PAGE_REVIEW_V001.md`；
   - `P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`；
   - `P1_3_GATE_REVIEW_2026-09-12.md`；
9. P2 frozen parameter / dependency / integration baseline，仅用于 provenance 与现有工程对象对照；
10. `docs/project_control/project_state.json`、`decision_log.md`、`acceptance_matrix.md`；
11. D-023、D-028～D-032 与 CG-02～CG-06。

如果历史构件身份、术语、分件关系、尺寸或形态不能由正式证据支持，必须保留 `PROXY_ONLY / DEFERRED_INSUFFICIENT_EVIDENCE / EVIDENCE_REVIEW_BEFORE_MASTER` 等证据边界，不得以一般古建知识或经验静默补齐。

## 3. Hard Boundaries

### 禁止事项

- 不新增、修改或重建 Blender 构件几何；
- 不创建 Component Master `.blend`；
- 不开始 Variant 几何生产；
- 不修改 P2 canonical `.blend` 或冻结工程基线；
- 不把 P2 engineering family 直接升级为历史构件 Master；
- 不把 P2 instance 数量解释为历史构件数量；
- 不把 `BRACKET_CONTACT` 直接解释为“小斗”；
- 不把 `BRACKET_ARM` 直接解释为单一栱、昂或铺作构件；
- 不把 `PRIMARY_FRAME` 直接当作梁、枋或六椽栿；
- 不把 `FRAME_SUPPORT` 直接当作托脚、蜀柱或具体节点构件；
- 不把 `FRAME_CONTROL / GABLE_CONTROL / GRID_CONTROL` 历史化；
- 不把 `ROOF_ENVELOPE` 当作实体屋面构件；
- 不因构件命名或拆分而升级 evidence classification；
- 不解决当前证据不足的 45° 转角、榫卯、隐角梁等问题。

### 必须保留的历史边界

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`；
- `Z-006-RC-01` 独立、可替换、D-023 traceable；
- `DG-114` 不代表统一小斗历史规格；
- `HIS-002` component originality 继续 unknown；
- observed / report ideal / reconstructed candidate 三层继续分离；
- P2 11 engineering families ≠ 11 historical component types。

## 4. Eligibility Status Vocabulary

每一个被审查对象必须且只能获得一个最终资格状态：

- `MASTER_REQUIRED`
- `EVIDENCE_REVIEW_BEFORE_MASTER`
- `PROXY_ONLY`
- `CONTROL_ONLY`
- `ENVELOPE_ONLY`
- `DEFERRED_INSUFFICIENT_EVIDENCE`

T-010 完成时，原则上不得仍有无解释的临时状态。

如果某对象在本任务中仍需继续研究才能判断，必须明确说明：

- 当前证据缺口；
- 为什么不能进入 `MASTER_REQUIRED`；
- 后续需要什么证据；
- 最终状态应落在 `DEFERRED_INSUFFICIENT_EVIDENCE`，而不是无限期保留模糊 Working 状态。

## 5. Required Scope Coverage

### A. P3.0 Registry 全量覆盖

必须审查 P3.0 Registry 的全部 11 个迁移记录：

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

覆盖要求：**11 / 11**，不得 orphan。

### B. P1 Direct-evidence Candidate Review

必须至少重新评估以下 P1 已直接核实、但未必在 P2 中作为独立 family 表达的真实构件候选：

- 柱；
- 柱头栌斗；
- 底斗；
- 单向长开斗；
- 交互斗；
- 下六椽栿；
- 上六椽栿；
- 槫类；
- 椽类。

并继续检索 P1 正式证据包中是否还存在其他已经直接核实、足以进入 Master 资格审查的历史构件类型。

不能因为某构件在 P2 没有独立 family 就忽略它。

## 6. Identity Resolution Requirements

对每个候选构件至少记录：

- candidate_id / source registry id；
- canonical_name_zh；
- canonical_name_en / machine key；
- aliases / historical_terms；
- source context / architectural position；
- historical component identity；
- whether it corresponds to a real historical component type；
- eligibility_status；
- source pages / source references；
- evidence_by_attribute；
- known geometry inputs；
- unknown / unresolved attributes；
- historical_state / originality_status；
- proxy/control/envelope relationship if migrated from P2；
- split / merge / replacement relationship to P3.0 record；
- reason for eligibility decision；
- proposed future `component_id` if a new historical component candidate is accepted；
- readiness for later Master Asset Contract。

### Proxy → Historical Component 升级

任何从 P3.0 proxy / unresolved record 中识别出的真实历史构件，都必须提供：

1. 明确构件名称；
2. 正式证据引用；
3. 至少能支持构件身份的形态 / 尺寸 /位置证据；
4. 当前仍未知的几何属性；
5. 为什么可以成为独立 Master，而不是继续作为 aggregate proxy；
6. 不得改变原 P3.0 proxy 的历史记录，应使用明确的 split / derived-from / supersession relationship。

## 7. Specific Review Rules

### COLUMN

已有历史构件类型身份，但必须区分：

- 柱构件概念；
- 万佛殿建筑专属尺寸 / Variant；
- `Z-006` 历史柱高 UNKNOWN；
- `Z-006-RC-01` 仅为可替换候选。

资格判断不得把 RC 柱高写成历史定值。

### BRACKET_CONTACT / 斗类

P3.0 的 `BRACKET_CONTACT` 继续保持 proxy。

应回到 P1 直接证据分别审查：

- 柱头栌斗；
- 底斗；
- 单向长开斗；
- 交互斗；
- 其他有明确直接证据的斗类构件。

真实斗类构件可独立获得新的 historical component candidate；不能用 P2 contact-block 几何替代其身份。

### BRACKET_ARM / 栱昂铺作

必须回到 P1 证据，识别哪些栱、昂或其他铺作构件已达到可单独命名和建模的证据门槛。

若只能确认总体铺作拓扑或出跳参数，而无法可靠分解具体构件，则相关对象保留 Proxy / Deferred。

### PRIMARY_FRAME / FRAME_SUPPORT

必须回到 P1 证据识别明确梁架成员，例如已经直接核实的上下六椽栿以及其他有充分证据的梁、枋、支承成员。

不得把 P2 aggregate mesh 或 connector proxy 自动继承为历史构件 Master。

### PURLIN / RAFTER

历史构件类型概念成立，但必须核定：

- 报告中的正式中文术语；
- 是否需要拆成多个 canonical component type，还是一个 Master + 多个 Variant；
- 哪些尺寸 / 位置差异属于 Variant；
- 哪些只是 instance placement；
- 当前哪些几何属性仍为 diagrammatic / inferred。

## 8. Required Outputs

至少生成：

1. `docs/production/zhenguo_wanfo/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md`
2. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json`
3. `docs/production/zhenguo_wanfo/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md`
4. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json`
5. `docs/production/zhenguo_wanfo/P3_1_SCOPE_IDENTITY_VALIDATION_REPORT_V001.md`
6. `production/zhenguo_wanfo/validation/P3_1_SCOPE_IDENTITY_VALIDATION_REPORT_V001.json`
7. deterministic generation / validation script(s) if needed。

本任务不得创建：

- Component Master `.blend`；
- final Master Library；
- Variant Library；
- P3.1 Gate PASS。

## 9. Validation Requirements

至少验证：

- P3.0 Registry coverage = 11/11；
- 每个被审查对象恰好一个 eligibility status；
- P1 minimum scope candidates 全部被审查；
- 新识别 historical component candidate 的 ID 唯一；
- source reference / evidence provenance 不为空；
- `CONTROL_ONLY` / `ENVELOPE_ONLY` 不会进入 Master candidate；
- proxy → historical component 的升级均有显式 evidence；
- `BRACKET_CONTACT` 未被静默命名为小斗；
- `PRIMARY_FRAME / FRAME_SUPPORT` 未被整体直接历史化；
- Z-006 / RC-01 / DG-114 / HIS-002 等边界保持；
- unresolved / deferred 对象均有明确 evidence gap；
- output 可 deterministic 重生成；
- P2 frozen baseline 未修改。

若发现正式证据与 P3.0 Registry 之间存在真实冲突，不自行覆盖 P3.0；在报告中列出 `REQUIRES_PROJECT_CONTROL_REVIEW`，由 ChatGPT / Product Owner 决定是否需要新的正式决策。

## 10. Completion Criteria for T-010

T-010 COMPLETE 至少要求：

- P3.0 Registry review = **11/11**；
- P1 minimum evidence candidate review = **100%**；
- eligibility decision coverage = **100%**；
- unexplained working / pending records = **0**；
- accidental CONTROL / ENVELOPE historicization = **0**；
- evidence provenance validation = **PASS**；
- historical-boundary validation = **PASS**；
- determinism = **PASS**。

T-010 COMPLETE 不等于 P3.1 PASS，也不自动授权批量 Master geometry。

完成后必须由 ChatGPT / Product Owner 审核 Scope Matrix 与 Identity Resolution，再决定后续 P3.1 几何任务范围。

## 11. Local Execution / Git Rules

执行前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git status

git -c http.proxy=http://127.0.0.1:15236 \
    -c https.proxy=http://127.0.0.1:15236 \
    pull --ff-only origin main
```

如果当前代理端口变化，可使用当前实际可用代理；不得因为网络问题 force / reset / overwrite。

若出现：

- 不明 tracked changes；
- non-fast-forward；
- 与 Project Control 同文件冲突；

立即停止并报告。

完成后：

- 先运行 validation；
- `git status` 确认只包含 T-010 授权范围；
- commit message 建议：`p3.1: resolve component master scope identity v001`；
- push `main`；
- 回传 commit SHA、coverage、eligibility counts、validation 和 unresolved / deferred 项。

## 12. Completion Report Format

必须严格回报：

- STATUS: COMPLETE / BLOCKED / FAILED
- P3_0_REGISTRY_COVERAGE: x/11
- P1_MINIMUM_SCOPE_COVERAGE: x/x
- TOTAL_REVIEW_RECORDS: x
- MASTER_REQUIRED: x
- EVIDENCE_REVIEW_BEFORE_MASTER: x
- PROXY_ONLY: x
- CONTROL_ONLY: x
- ENVELOPE_ONLY: x
- DEFERRED_INSUFFICIENT_EVIDENCE: x
- UNEXPLAINED_PENDING: x
- EVIDENCE_PROVENANCE_VALIDATION: PASS / FAIL
- HISTORICAL_BOUNDARY_VALIDATION: PASS / FAIL
- DETERMINISM: PASS / FAIL
- FILES_CREATED / UPDATED
- COMMIT_SHA
- REQUIRES_PROJECT_CONTROL_REVIEW
- UNRESOLVED / BLOCKERS

T-010 完成后，不自行创建下一项几何任务，不自行修改 P3.1 Gate 状态；由 ChatGPT / Product Owner 审核后决定下一步。
