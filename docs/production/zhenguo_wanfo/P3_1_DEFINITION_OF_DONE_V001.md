# P3.1 Definition of Done V001｜Component Master & Variant Library

Status: **LOCKED / PRODUCT OWNER APPROVED / D-032**  
Date: 2026-09-13  
Phase: `P3｜古建筑构件系统化与组合建模`  
Gate: `P3.1｜Component Master & Variant Library`

## 1. Gate Purpose

P3.1 的目标，是把 P3.0 已建立的构件本体与 Registry 转化为一套真正可复用的 **Component Master + Parameterized Variant Library**。

本 Gate 不再以“整栋建筑看起来完整”为目标，而以“一个构件是否成为独立、可解释、可复用、证据边界透明的正式数字资产”为判断单位。

正式生产链：

> **Evidence-qualified Component Identity → Canonical Master → Parameterized Variant → Review Asset → Registry Registration**

P3.1 必须严格区分：

- `Master`：跨实例复用的标准构件资产；
- `Variant`：由参数、形制或结构角色差异形成的构件版本；
- `Instance`：构件在建筑中的具体放置，不在 P3.1 重建；
- `Proxy / Control / Envelope`：不得为了“资产完整率”被强行升级成历史构件 Master。

P3.1 **不要求重做 P2 整栋建筑，也不要求把 365 个 instance 逐件独立建模。**

---

## 2. Frozen Inputs / Authoritative Baseline

P3.1 必须继承：

1. `P3_0_COMPONENT_ONTOLOGY_V001`；
2. `P3_0_COMPONENT_REGISTRY_V001`；
3. `P3_0_COMPONENT_REGISTRY_SCHEMA_V001`；
4. `P3_0_P2_COMPONENT_MIGRATION_AUDIT_V001`；
5. P1 approved evidence package 与直接核读；
6. P2 frozen engineering baseline；
7. D-023、D-028～D-031；
8. CG-02～CG-06 与 Evidence Visualization carry-forward rules。

P3.0 已正式确认：

- `COLUMN / PURLIN / RAFTER` 具有历史构件类型概念；
- `BRACKET_ARM / BRACKET_CONTACT / PRIMARY_FRAME / FRAME_SUPPORT` 仍包含 proxy / unresolved 语义；
- `FRAME_CONTROL / GABLE_CONTROL / GRID_CONTROL` 是工程控制对象；
- `ROOF_ENVELOPE` 是几何包络。

这些边界不得在 P3.1 被静默改变。

---

## 3. Definition of Done｜9 Items

### DoD-01｜Component Master Eligibility & Scope Matrix

建立正式 `P3.1 Component Master Scope Matrix`。

所有 P3.0 Registry 记录必须被赋予且仅赋予一种 Master 资格状态：

- `MASTER_REQUIRED`：历史构件身份与几何输入足以建立正式 Master；
- `EVIDENCE_REVIEW_BEFORE_MASTER`：构件身份或分件关系需要回到证据进一步核定；
- `PROXY_ONLY`：当前只能作为几何代理，不建立历史构件 Master；
- `CONTROL_ONLY`：工程控制对象，不建立 Master；
- `ENVELOPE_ONLY`：连续包络，不建立实体构件 Master；
- `DEFERRED_INSUFFICIENT_EVIDENCE`：构件概念可能成立，但当前证据不足以形成合格 Master。

Scope Matrix 必须覆盖：

- P3.0 Registry 全部 11 个迁移记录；
- P1 证据中已经直接核实、但 P2 family 尚未独立表达的历史构件候选。

至少必须重新评估以下已在 P1 直接核读中出现的构件：

- 柱；
- 柱头栌斗；
- 底斗；
- 单向长开斗；
- 交互斗；
- 下六椽栿；
- 上六椽栿；
- 槫类（含报告已明确出现的具体位置术语）；
- 椽类。

不得用“P2 没有独立 family”为理由忽略 P1 已有证据。

### DoD-02｜Evidence-backed Component Identity Resolution

对所有 `EVIDENCE_REVIEW_BEFORE_MASTER` 对象完成证据回查。

重点包括但不限于：

- `BRACKET_ARM`：判断哪些真实栱、昂或铺作构件能够从当前证据中独立识别；
- `BRACKET_CONTACT`：不得直接解释为小斗，只有证据明确支持的斗类构件才能新建 Master；
- `PRIMARY_FRAME`：按证据识别六椽栿、梁、枋等真实构件，不能沿用“PRIMARY_FRAME”作为历史构件名；
- `FRAME_SUPPORT`：只有能够由证据支持的真实成员才能从 proxy 升级。

每一次 proxy → historical component 的升级必须记录：

- canonical component identity；
- source page / source reference；
- supporting dimensions / shape evidence；
- evidence classification；
- unresolved attributes；
- Registry 变更理由。

证据不足时，保留 `PROXY_ONLY / DEFERRED` 也视为正确结果，不允许强行解决。

### DoD-03｜Canonical Component Master Asset Contract

每一个 `MASTER_REQUIRED` 构件必须拥有正式 Master Asset Contract，至少包含：

- stable `component_id`；
- canonical Chinese / machine-readable name；
- canonical local coordinate system；
- unit = mm；
- origin / axis / forward-up convention；
- parameter contract；
- geometry-generating evidence references；
- evidence_by_attribute；
- historical_state / originality_status；
- reuse_scope；
- known_unknowns / interpretation_boundary；
- version / status；
- generator/source path；
- canonical local asset path；
- semantic/hash metadata where applicable。

Master 必须独立于建筑 placement；不得把万佛殿中的世界坐标写进构件本体几何。

### DoD-04｜Canonical 3D Master Production

所有最终判定为 `MASTER_REQUIRED` 的构件类型必须 **100% 建立正式 Canonical 3D Master**。

最低边界：

- 不允许只因为 P2 已有 mesh 就自动将其视为 Master；
- Master 必须从构件自身语义与参数定义生成 / 整理；
- 同一构件类型不得为每个建筑 instance 重复复制独立模型；
- `CONTROL_OBJECT / ENVELOPE_SURFACE` 的 Master 数量必须为 0；
- unresolved proxy 不得伪装成历史精确 Master。

P3.1 不以固定 Master 数量作为 PASS 条件；最终数量由 DoD-01 / DoD-02 的证据资格判定决定。

### DoD-05｜Parameterized Variant Model

每一个具有有效尺寸、形制、方向或结构角色差异的 Master 必须建立明确 Variant 体系。

Variant 必须满足：

- stable `variant_id`；
- 明确 parent `component_id / master_id`；
- 参数差异可解释；
- parameter source / evidence status 可追踪；
- building-specific variant 与 reusable master 分离；
- 不用复制后手工缩放形成不可追踪 variant；
- placement-only 差异不得错误创建新 variant；
- 对 RC / HCI / UNKNOWN 输入继续保留 evidence semantics。

必须通过至少一次 parameter mutation / alternate-variant test，证明 Variant 确实由参数驱动，而不是静态复制。

### DoD-06｜Evidence-aware Geometry & Replaceability

每个正式 Master / Variant 的关键几何属性必须可追溯到：

- CONFIRMED；
- HIGH_CONFIDENCE_INFERENCE；
- REASONABLE_COMPLETION；
- UNKNOWN / unresolved。

强制边界：

- `Z-006` 保持 `UNKNOWN / null / DO_NOT_LOCK`；
- `Z-006-RC-01` 仍为独立可替换候选；
- `DG-114` 不得被转化为统一小斗规格；
- `HIS-002` 原真性 unknown 继续保留；
- 45°转角、榫卯、隐角梁等无证据细节不得因 Master 建模而获得虚假精确度；
- observed / report ideal / reconstructed candidate 三层不得混合。

若一个 Master 依赖 RC 或可替换推断，必须证明替换输入后能够重新生成或更新，而不是写死在 mesh 中。

### DoD-07｜Standard Component Review Package

每一个正式 Master 至少生成标准审核资产：

1. Front / 正视；
2. Side / 侧视；
3. Top 或必要正交补充视图；
4. Axonometric / 轴测；
5. 参数 / 尺寸摘要；
6. Evidence / uncertainty 摘要。

审核图必须：

- 使用统一比例 / 方向 / 构件命名；
- 不用影视材质掩盖几何；
- 能让 Product Owner 判断构件身份、比例和差异；
- 正常几何展示与证据状态展示分离。

同时生成至少一张 Library Overview，展示当前 P3.1 已完成的 Master / Variant 集合及其状态。

### DoD-08｜Library Registration, Machine Validation & Reproducibility

所有正式 Master / Variant 必须回写 P3 Registry 或其 P3.1 扩展 Registry，并通过机器校验。

至少验证：

- Master / Variant ID 唯一；
- required fields 完整；
- `master_3d_asset` 对 `MASTER_REQUIRED` 不再为 null；
- Master ↔ Variant references 无 orphan；
- Master ↔ evidence references 可追踪；
- `CONTROL_ONLY / ENVELOPE_ONLY` 未生成历史构件 Master；
- world placement 未污染 Master geometry；
- 单位 / 原点 / 轴向约定一致；
- parameter mutation 可复现；
- independent reopen / regeneration PASS；
- generator / metadata 输出 deterministic（语义一致；`.blend` 不要求字节级相同）；
- P2 frozen baseline 未被覆盖。

### DoD-09｜Product Owner Review + Canonical Archive + P3.2 Readiness

P3.1 最终必须形成 Gate Review，并由 Product Owner 审核：

- Master Scope Matrix 是否合理；
- 哪些构件进入正式 Master Library；
- 哪些对象继续保留 proxy / unresolved；
- 每个正式 Master 的视觉身份与比例是否成立；
- Variant 差异是否合理且可解释；
- Registry / evidence / reuse boundary 是否符合项目目标。

P3.1 PASS 后必须能够明确回答：

> “万佛殿当前有哪些已经成为正式数字构件资产的类型？每一种有哪些 Variant？哪些仍然不能历史化建模？这些资产能否作为 P3.2 Assembly Relationship Model 的节点？”

只有达到该条件，P3.2 才可解锁。

---

## 4. Gate PASS Conditions

P3.1 PASS 必须同时满足：

- DoD 9 / 9 PASS；
- P3.1 Scope Matrix coverage = 100%；
- 所有 `MASTER_REQUIRED` component Master coverage = 100%；
- 所有 `EVIDENCE_REVIEW_BEFORE_MASTER` 均得到明确结论：升级为 Master / 保持 Proxy / Deferred，不得悬空；
- `CONTROL_ONLY / ENVELOPE_ONLY` 被错误历史化建模数量 = 0；
- orphan Master / Variant = 0；
- required Registry fields / evidence traceability = PASS；
- parameter mutation / replaceability = PASS；
- reproducibility / independent reopen = PASS；
- P2 frozen baseline 未修改；
- Product Owner 明确批准。

**P3.1 PASS 不等于“万佛殿全部历史构件已经复原完毕”。**

它只意味着：在现有正式证据边界内，所有有资格进入当前版本构件库的对象已经得到一致、可复用、可验证的 Master / Variant 资产处理。

---

## 5. Scope Boundary｜P3.1 不做

P3.1 不要求：

- 重建 365 个独立 instance；
- 建立完整建筑装配关系图（P3.2）；
- 用 Component Library 重新装配整座万佛殿（P3.3）；
- 强行解决所有斗栱 45° 转角、榫卯和隐角梁；
- 在证据不足时补造精确历史几何；
- 最终材质、彩画、风化、影视灯光；
- 第二座建筑的正式生产。

P3.1 可以做跨建筑复用的 engineering mutation test，但不得把测试参数声称为真实历史建筑数据。

---

## 6. Expected Deliverables

P3.1 最终建议至少形成：

1. `P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.md/json`；
2. `P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.md/json`；
3. `P3_1_MASTER_ASSET_CONTRACT_V001.json`；
4. `P3_1_COMPONENT_MASTER_LIBRARY_V001.json`；
5. `P3_1_COMPONENT_VARIANT_LIBRARY_V001.json`；
6. canonical Master generators / parameter files；
7. canonical local-only Master `.blend` assets or formally approved equivalent asset package；
8. standard component review PNGs + Library Overview；
9. `P3_1_MASTER_LIBRARY_VALIDATION_REPORT_V001.md/json`；
10. `P3_1_GATE_REVIEW_YYYY-MM-DD.md`。

上述二进制 `.blend` 若继续采用 local-only 规则，GitHub 必须保存可重建的 generator / parameters / metadata / hash / review evidence，确保资产可追溯而不是只存在于本地二进制文件中。

---

## 7. Task Authorization Rule

本 DoD 经 Product Owner 批准并锁定前：

- 不创建 T-010；
- 不开始新的 P3.1 构件几何生产。

DoD 锁定后，可以把 P3.1 拆成一个或多个 Codex 工程任务；**不强制要求整个 P3.1 由单一 T-010 一次完成**。
