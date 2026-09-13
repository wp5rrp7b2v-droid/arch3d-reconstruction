# 【中国古建筑3D复原｜T-013｜P3_1_SIX_CHUANFU_MASTER_BATCH_V001｜上下六椽栿Master批次生产】

Status: **DRAFT / NOT AUTHORIZED**  
Execution Mode: **LEAN_PRODUCTION_MODE_V001 / NEW_GEOMETRY_FIRST_ARTICLE**  
Think Level: **HIGH for first-article / MEDIUM for proven batch repetition**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13  
Authorization: **PENDING PRODUCT OWNER APPROVAL**

## 1. Objective

在 `P3_1_MASTER_ASSET_CONTRACT_V002 / D-036` 下完成最后两个 `MASTER_REQUIRED` 梁架构件的 canonical Master 生产：

1. `CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿`
2. `CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿`

本任务目标是把 P3.1 Master coverage 从 **4/6** 推进到 **6/6 engineering + visual review ready**。

T-013 完成及 Product Owner 批准后，仍需单独执行 P3.1 Gate Review；不得由 T-013 自动宣告 P3.1 PASS / CLOSED。

核心原则：

> **新几何方法先做首件，首件完整 PASS 后再 Lean 批量复用；共享工具链，但两件 Master 独立验收。**

---

## 2. Why a New First-Article Gate Is Required

T-012 已验证 Lean Production Mode，但斗类采用 `MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`；本任务梁架长构件采用新的：

`BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`

因此 T-012 只证明“Lean 执行机制”成立，不证明梁架几何逻辑成立。

本任务必须重新设置 First Article：

`CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿`

原因：其截面尺度更大，且同样包含“榫厚 metadata / 最厚 bounded envelope / 长度未知”三类关键风险，适合作为共享 long-member pipeline 的代表首件。

---

## 3. Minimal Authoritative Read Set

执行前优先读取以下直接相关输入；不要无目的重新通读全部 P1/P2/P3：

1. 本文件：`docs/tasks/T-013_P3_1_SIX_CHUANFU_MASTER_BATCH_V001.md`
2. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`
3. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md` 中 Global Convention / LOD / 7.5 / 7.6 / Variant / Review / Registry / Hard Fail 相关部分
4. `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md` 中 `D-009｜六椽栿实测`
5. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json` 中两个六椽栿 record
6. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`
7. T-012 已验证的 Lean batch orchestration / review / validation 组织方法，仅用于复用资产链与批次执行模式；不得继承斗类几何逻辑
8. `docs/project_control/project_state.json` 仅核对授权状态
9. RC-008 / RC-009；Git remote publish 如需要则遵守 RC-010

P2 frozen baseline、已批准柱/三斗 Masters、Contract V002 完整内容默认仅做 hash/manifest 前后保护性比较；hash mismatch 才 STOP 并展开调查。

---

## 4. Canonical Evidence Inputs

### 4.1 CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿

Direct source: `P1_2_DIRECT_PAGE_REVIEW_V001 / D-009`，PDF p81 / 印刷 p66，表2-38。

Observed references:

- `width_mm = 493.5`
- `tenon_area_thickness_mm = 375.0`
- `max_thickness_mm = 444.0`
- `historical_full_length_mm = UNKNOWN / null`

Identity/topology：已确认其为独立下六椽栿构件类型；P2 `PRIMARY_FRAME` aggregate/proxy 不作为本 Master 几何来源。

### 4.2 CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿

Direct source 同 D-009。

Observed references:

- `width_mm = 334.0`
- `tenon_area_thickness_mm = 209.0`
- `max_thickness_mm = 240.5`
- `historical_full_length_mm = UNKNOWN / null`

Identity/topology：已确认其为独立上六椽栿构件类型；不得与下六椽栿合并为一个 generic historical Master。

### 4.3 Historical / Interpretation Boundary

两个 Master 均必须保持：

- present measured section data ≠ proven 963 original design
- `HIS-002 = component originality UNKNOWN`
- 完整历史长度当前未被直接证据锁定
- `max_thickness` 是当前实测“最厚”约束，不是“整根全长统一厚度”的历史事实
- `tenon_area_thickness` 是局部实测 metadata；其 X 轴作用区间未证实，因此当前不得驱动局部削减或榫区几何
- 不从 P2 proxy、常识、构件名称或一般古建规则补造端部、榫卯、起拱或局部厚度变化

---

## 5. Canonical Reference-Length Policy｜本任务新增项目规则

由于 V002 Contract 明确要求 `length_mm` 为显式 free / evidence-bound parameter，而历史完整长度当前为 `UNKNOWN / null`，canonical `.blend` 仍需要一个可执行的数值 realization。

本任务拟采用统一中性工程参考长度：

`canonical_reference_length_mm = 1000.0`

必须记录为：

- classification: `PROJECT_RULE`
- source_layer: `ENGINEERING_REFERENCE`
- time_layer: `NON_HISTORICAL_REFERENCE_REALIZATION`
- production_use: `CANONICAL_REFERENCE_ONLY`
- replaceable: `true`
- historical_claim: `false`

该 1000 mm：

- 不是现状实测长度；
- 不是963年设计候选；
- 不得进入 historical evidence layer；
- 仅用于建立可保存、可重开、可变体测试的 canonical reference binary；
- 后续 P3.2 / P3.3 真实装配时必须由 assembly/building-specific evidence 或经批准 candidate 提供实际 `length_mm`，不得默认沿用 1000 mm。

1000 mm 必须写入独立参数 JSON，不得写死在共享 generator 代码中。

**本条随 T-013 Task Contract 一并由 Product Owner 审批；未批准前不得执行。**

---

## 6. Canonical Geometry Rule

统一坐标：

- unit = mm
- +X = 构件纵向
- +Y = 截面宽度方向
- +Z = 垂直厚度方向
- origin = longitudinal midpoint / transverse center / lower reference plane
- theoretical ends = `X = ±length_mm / 2`
- Location `(0,0,0)` / Rotation `(0,0,0)` / Scale `(1,1,1)`

当前 canonical body 采用：

> `length_mm × width_mm × max_thickness_mm` 的 centered rectangular bounded outer envelope

其中：

- X extent = `[-L/2, +L/2]`
- Y extent = `[-width/2, +width/2]`
- Z extent = `[0, max_thickness]`

几何语义必须明确标记：

`PROJECT_RULE / BOUNDED_OUTER_ENVELOPE_REFERENCE / REPLACEABLE`

该 prism 只代表“当前已知外包络上限下的可复用参数化主体”，不得表述为“历史整根梁通长均匀矩形截面”。

### 6.1 tenon-area thickness rule

`tenon_area_thickness_mm` 当前必须存在于 params / semantic / review summary，但：

- geometry use = `0`
- 不生成局部薄化
- 不生成榫头
- 不生成榫区长度
- 不推断局部起止位置

只有后续证据明确榫区 X 范围与形状后，才能升级几何。

### 6.2 Prohibited geometry

禁止加入：

- camber / 起拱
- end profile / 端部削形
- local thickness zones / 局部厚度区
- mortise-tenon / 榫卯
- cavities / hidden joints
- bevel / decorative shaping not directly evidenced
- P2 proxy-derived end geometry

---

## 7. Shared Toolchain Rule

允许建立一次共享 long-member pipeline：

- `six_chuanfu_master_common` geometry utility
- batch runner
- validator
- review renderer
- semantic snapshot helper

最终资产必须独立：

- 2 component IDs
- 2 params JSON
- 2 local-only `.blend`
- 2 SHA256
- 2 semantic snapshots
- 2 review packages
- 2 Registry records

禁止：

- 用一个 generic `SIX_CHUANFU_MASTER` binary 同时代表上下两件
- 复制同一 binary 后仅 Object Scale 改截面
- 将上/下六椽栿合并为一个历史构件 ID

---

## 8. First-Article / Lean Execution Stages

### Stage A｜Shared pipeline setup

建立一次 long-member generator / validator / renderer / semantic helper / batch orchestration。

共享代码中不得出现 493.5 / 444 / 375 / 334 / 240.5 / 209 等 component-specific 裸常量；全部来自 params JSON。

### Stage B｜First Article = 下六椽栿

只生产 `CMP-FRAME-LOWER-SIX-CHUANFU-001`，并完整执行：

- params schema / evidence semantics
- reference-length classification check
- bbox / X-Y-Z extent
- origin / transform / Scale=1
- max-thickness bounded-envelope semantics
- tenon-area thickness metadata-only validation
- unsupported geometry = 0
- P2 proxy non-use
- deterministic regeneration
- independent reopen
- synthetic mutation probes
- canonical rebuild
- 6/6 review assets
- `.blend` local-only

任何 Hard Fail：立即 STOP，不得进入 Stage C。

### Stage C｜Batch repetition = 上六椽栿

Stage B 全部 PASS 后，以同一共享 pipeline 参数驱动生成 `CMP-FRAME-UPPER-SIX-CHUANFU-001`。

Think Level 从 HIGH 降为 MEDIUM；若出现新的结构性失败类型，再升级 HIGH，不得默默改 Contract。

### Stage D｜Batch validation

对 2 个独立资产执行完整逐资产验收、批次 overview、Registry pending record 与保护性 baseline check。

---

## 9. Mutation Strategy｜验证“参数驱动”与“metadata 不驱动几何”

每个 Master 至少执行两类 synthetic mutation：

### Probe A｜Geometry-driving length mutation

临时改变 `length_mm`，要求：

- 只改变 X extent
- Y width / Z max thickness 不变
- origin 仍为 X=0 midpoint
- semantic snapshot 正确反映 mutation

随后 canonical rebuild 必须恢复 1000 mm reference realization。

### Probe B｜Metadata-only tenon thickness mutation

临时改变 `tenon_area_thickness_mm`，要求：

- params / semantic metadata 变化
- canonical body geometry / bbox **完全不变**
- 不出现局部削减、榫头或端部变化

随后 canonical rebuild 恢复正式参数。

该 Probe 是本任务关键验收项，用于证明“榫厚当前只作证据 metadata”。

---

## 10. Retry / Token Budget Discipline

沿用 RC-009：

- 同一根因最多 2 次有证据的修正重试；
- 首件未 PASS 不生成第二件；
- 不重复全文分析 P2 / T-011 / T-012 / Contract 历史；
- 保护性资产优先 hash check；
- 不为上下两件各写一套重复 generator / validator / renderer；
- 不生成非验收需要的额外中间资产；
- Codex 不做 review PNG 的历史/视觉判断，只生成并机器检查；视觉审核由 ChatGPT / Product Owner 完成。

---

## 11. Independent Asset Requirements

每个 Component 必须生成：

- `<COMPONENT_ID>_MASTER_PARAMS_V001.json`
- 独立 wrapper / entrypoint，可调用共享 utility
- local-only `asset/<COMPONENT_ID>_MASTER_V001.blend`
- `<COMPONENT_ID>_MASTER_SEMANTIC_V001.json`
- 独立 SHA256
- 6 张正式 review PNG
- Registry 独立 record

`.blend/.blend1` 不进入普通 Git。

---

## 12. Validation Matrix

每个 Master 必须 PASS：

1. component_id / master_id unique
2. authoritative Contract = V002 / D-036
3. current measured dimensions trace to D-009
4. historical full length remains UNKNOWN / null
5. canonical `length_mm=1000` classified only as PROJECT_RULE / ENGINEERING_REFERENCE
6. no historical / 963 claim from reference length
7. width matches params
8. Z outer bound matches max_thickness params
9. max_thickness not semantically promoted to confirmed full-length uniform section
10. tenon_area_thickness present as metadata
11. tenon_area_thickness geometry use = 0
12. origin / axes / transform correct
13. body Scale = 1
14. no world placement leakage
15. no naked historical constants in code
16. no camber
17. no unsupported end profile
18. no local thickness zone
19. no mortise-tenon / cavity / hidden joint
20. P2 PRIMARY_FRAME proxy geometry not used as Master source
21. deterministic regeneration PASS
22. independent reopen PASS
23. length mutation isolates X extent
24. tenon-thickness metadata mutation leaves geometry unchanged
25. canonical rebuild after mutations PASS
26. `.blend/.blend1` absent from Git

批次级必须 PASS：

27. 2/2 params / independent blends / semantic snapshots / hashes
28. review = 12/12 + overview 1/1
29. Registry = 2 new independent pending-review records
30. existing 4 approved Masters unchanged
31. P2 frozen baseline unchanged
32. Contract V002 unchanged
33. upper/lower remain independent historical Master IDs
34. no P3.2 assembly placement or building-specific beam length silently introduced

---

## 13. Review Package

每个 Master 生成标准 6 图：

1. FRONT｜建议 X-Z longitudinal elevation
2. SIDE｜建议 Y-Z section envelope
3. TOP｜建议 X-Y plan envelope
4. AXON
5. DIMENSION_PARAMETER_SUMMARY
6. EVIDENCE_UNCERTAINTY_SUMMARY

总计 12 张。

另生成：

`production/zhenguo_wanfo/review/P3_1/batches/SIX_CHUANFU_MASTER_BATCH_V001_OVERVIEW.png`

Overview 要求：

- 两件同轴向
- 同一参考长度 1000 mm
- 真实截面相对尺度
- 清楚标识 component ID / 中文名
- 明示 `REFERENCE LENGTH = 1000 mm / ENGINEERING ONLY`
- 明示 `MAX THICKNESS = BOUNDED OUTER ENVELOPE, NOT FULL-LENGTH HISTORICAL SECTION CLAIM`

最终视觉审核输入共 **13 张**。

---

## 14. Registry Rule

更新：

`production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`

要求：

- 已批准的柱 + 三斗 4 条 record 保持不变
- 新增上下六椽栿 2 条独立 record
- 新记录初始只能是 `ENGINEERING_PASS / PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`
- 不得提前 Product Owner Approved
- originality_status = unknown
- `length_mm=1000` 必须标识为 non-historical reference realization
- orphan / duplicate = 0

---

## 15. Protected Assets / Hash-only Recheck

执行前后保护：

- P2 frozen baseline
- T-011 approved column
- T-012 approved three dou Masters
- Contract V002 md/json
- existing approved Registry records

默认只做 hash / manifest 比较。

任何 unexpected mismatch：STOP，列出文件，不自动重建/覆盖。

`docs/project_control/` 不由 Codex 修改。

---

## 16. Hard Fail Conditions

任一发生不得 COMPLETE：

- 使用 Contract V001
- P2 PRIMARY_FRAME proxy 被包装成六椽栿 historical Master
- 历史完整长度被静默填值
- 1000 mm reference length 被写成现状实测或963设计候选
- max_thickness 被声明为整根全长统一厚度的历史事实
- tenon_area_thickness 驱动局部削减/榫区几何
- 自行补造榫卯、端部、起拱、局部厚度区、空腔或隐藏连接
- 上下六椽栿合并为一个 component/master ID
- 通过 Object Scale 复制第二件
- world placement / support position 写进 Master
- First Article 未 PASS 就生产上六椽栿
- Registry 提前标 Product Owner Approved
- 已批准 4 Masters / P2 / Contract V002 被修改
- `.blend/.blend1` 进入 Git
- Codex 修改 Project Control 或自动宣告 P3.1 PASS

---

## 17. Completion Criteria

T-013 ENGINEERING COMPLETE 必须满足：

- First Article 下六椽栿完整 PASS
- shared long-member pipeline PASS
- 2/2 independent canonical Masters generated
- 2/2 semantic snapshots PASS
- 2/2 deterministic regeneration PASS
- 2/2 independent reopen PASS
- 2/2 length mutation PASS
- 2/2 metadata-only tenon-thickness mutation PASS
- 2/2 canonical rebuild PASS
- 12/12 standard review PNG + 1/1 batch overview
- 2 independent Registry pending-review records
- approved 4 Masters unchanged
- P2 frozen baseline unchanged
- Contract V002 unchanged
- no Hard Fail

工程 COMPLETE 后状态只能是：

`ENGINEERING_PASS / VISUAL_REVIEW_PENDING`

只有 ChatGPT 视觉审核 PASS + Product Owner 明确批准后，两个新 Master 才能进入 APPROVED；届时 P3.1 Master coverage = 6/6，但 P3.1 Gate 仍需单独 Final Gate Review。

---

## 18. Local Blender Execution

严格遵守 RC-008：

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background \
  --python <script.py>
```

不得以 GUI / Finder / AppleScript 作为正式自动工程链。

---

## 19. Completion Report Format

成功时只回报：

- STATUS
- TASK / EXECUTION_MODE
- FIRST_ARTICLE
- SHARED_PIPELINE
- COMPONENTS 2/2
- CONTRACT_VERSION
- BLENDER_VERSION / EXECUTION_MODE
- CANONICAL_REFERENCE_LENGTH_POLICY
- CANONICAL_BLEND_PATHS / SHA256
- SEMANTIC_SNAPSHOT
- REVIEW_PACKAGE 12/12 + OVERVIEW 1/1
- LENGTH_UNKNOWN_BOUNDARY_VALIDATION
- MAX_THICKNESS_BOUNDARY_VALIDATION
- TENON_METADATA_NON_GEOMETRY_VALIDATION
- TRANSFORM / EVIDENCE_BOUNDARY / UNSUPPORTED_DETAIL
- NAKED_CONSTANT_SCAN
- DETERMINISTIC_REGENERATION
- INDEPENDENT_REOPEN
- LENGTH_MUTATION
- TENON_METADATA_MUTATION
- CANONICAL_REBUILD
- REGISTRY_REGISTRATION
- APPROVED_MASTER_PRESERVATION
- P2_FROZEN_BASELINE
- CONTRACT_V002
- RETRY_COUNTS
- FILES_CREATED / UPDATED
- COMMIT_SHA
- UNRESOLVED / BLOCKERS

失败时只回报最小 blocker，不得扩大任务范围。

---

## 20. Authorization Boundary

当前文件仅为正式 Task Contract **DRAFT**。

Product Owner 尚未批准：

- T-013 工程执行；
- `canonical_reference_length_mm = 1000` 这一 non-historical project rule；
- 任何上下六椽栿 Blender 生产。

只有收到明确：

`T-013｜P3_1_SIX_CHUANFU_MASTER_BATCH_V001｜APPROVED / AUTHORIZE`

后，才允许进入本地 Codex 执行。