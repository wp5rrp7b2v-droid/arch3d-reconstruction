# 【中国古建筑3D复原｜T-013｜P3_1_SIX_CHUANFU_MASTER_BATCH_V002｜上下六椽栿Master批次生产】

Status: **AUTHORIZED / READY_FOR_LOCAL_EXECUTION**  
Execution Mode: **CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL + LEAN_PRODUCTION_MODE_V001 / NEW_GEOMETRY_FIRST_ARTICLE**  
Codex Think Level: **MEDIUM DEFAULT / HIGH ONLY BY EXPLICIT CHATGPT ESCALATION**  
Phase/Gate: P3 / P3.1  
Date: 2026-09-13  
Authorization: **PRODUCT OWNER APPROVED / D-038**  
Supersedes for execution planning: `T-013_P3_1_SIX_CHUANFU_MASTER_BATCH_V001.md`

## 1. Objective

在 `P3_1_MASTER_ASSET_CONTRACT_V002 / D-036` 下完成最后两个 `MASTER_REQUIRED` 梁架构件的 canonical Master 生产：

1. `CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿`
2. `CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿`

目标：将 P3.1 Master coverage 从 **4/6** 推进到 **6/6 engineering + visual review ready**。

T-013 工程完成及 Product Owner 对两件 Master 最终批准后，仍需单独执行 P3.1 Gate Review；不得由 T-013 自动宣告 P3.1 PASS / CLOSED。

核心模式：

> **ChatGPT 负责分析、证据解释、规则设计、异常诊断和视觉审核；Codex 负责按锁定规则做确定性工程执行与机器验证。**

质量原则：

> **省重复推理，不省任何验收证据。**

---

## 2. Role Split｜CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL

### 2.1 ChatGPT responsibilities

由 ChatGPT 在 Codex 执行前完成：

- 证据解释与历史边界判断；
- Task Contract / geometry rule / parameter semantics；
- canonical reference-length policy；
- Hard Fail / mutation / validation 设计；
- First Article 选择；
- 非预期失败原因诊断；
- review PNG 视觉审核；
- Product Owner approval 建议；
- Project Control 维护。

### 2.2 Codex responsibilities

Codex 只负责：

- 读取最小锁定输入；
- 创建 params / generator / validator / renderer / semantic helper；
- 运行 Blender CLI/background；
- 生成独立 `.blend`、SHA256、semantic snapshot；
- deterministic regeneration / independent reopen；
- synthetic mutation / canonical rebuild；
- 机器检查 review assets；
- 更新 Registry 为 pending review；
- commit / 经授权后 push。

### 2.3 Mandatory STOP boundary

出现下列任一情况，Codex **不得自行分析扩展或修改合同**，必须 STOP，把最小失败证据交回 ChatGPT：

- 新证据与 Contract 冲突；
- 需要改变 geometry method；
- 参数语义不明确；
- validation 失败且不是显然的实现错误；
- 必须引入新的历史假设或 substitute；
- 当前 Hard Fail 规则无法判断；
- 保护性 baseline hash mismatch。

Codex STOP 回报只需：失败项、最小复现、关键日志、受影响文件、是否可判定为纯实现 bug。

ChatGPT 完成诊断后，才可给出 targeted retry / Contract amendment / Think Level escalation。

---

## 3. Think-Level Policy

T-013 Codex 默认：**MEDIUM**。

- First Article 下六椽栿：MEDIUM default；
- Batch repetition 上六椽栿：MEDIUM；
- 只有 ChatGPT 判断出现真正结构性工程问题时，才显式升级某一轮为 HIGH；
- Codex 不得自行因为“任务复杂”自动扩展到 HIGH 推理并重新解释历史资料。

Think Level 降低 **不允许** 减少 validation、mutation、reopen、review package 或 Hard Fail。

---

## 4. Why a New First-Article Gate Is Required

T-012 验证的是 Lean 执行机制，斗类 geometry mode 为 `MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`。

T-013 使用新的：

`BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`

因此必须重新建立 First Article：

`CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿`

首件未完整 PASS 前不得生成上六椽栿正式 Master。

---

## 5. Minimal Authoritative Read Set

Codex 只需优先读取：

1. 本文件；
2. `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`；
3. `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md` 中 Global Convention / LOD / 7.5 / 7.6 / Variant / Review / Registry / Hard Fail；
4. `docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md` 的 `D-009｜六椽栿实测`；
5. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json` 中两个六椽栿 record；
6. `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`；
7. T-012 已验证的 Lean orchestration / review / validation 组织方法，仅复用资产链与批处理方式；不得继承斗类几何；
8. `docs/project_control/project_state.json` 仅核对当前授权；
9. RC-008 / RC-009 / RC-010 / RC-011。

不重新全文阅读或解释全部 P1/P2/P3 历史。已锁定 P2 baseline、已批准四个 Masters、Contract V002 默认仅做 hash/manifest 保护性比较；mismatch 才 STOP。

---

## 6. Canonical Evidence Inputs

### 6.1 下六椽栿

Direct source: `P1_2_DIRECT_PAGE_REVIEW_V001 / D-009`，PDF p81 / 印刷 p66，表2-38。

- `width_mm = 493.5`
- `tenon_area_thickness_mm = 375.0`
- `max_thickness_mm = 444.0`
- `historical_full_length_mm = UNKNOWN / null`

P2 `PRIMARY_FRAME` aggregate/proxy 不作为本 Master 几何来源。

### 6.2 上六椽栿

- `width_mm = 334.0`
- `tenon_area_thickness_mm = 209.0`
- `max_thickness_mm = 240.5`
- `historical_full_length_mm = UNKNOWN / null`

上下六椽栿必须保持两个独立历史构件 Master ID。

### 6.3 Historical boundary

两者必须保持：

- present measured section data ≠ proven 963 original design；
- `HIS-002 = component originality UNKNOWN`；
- 完整历史长度 UNKNOWN；
- `max_thickness` = observed maximum bound，不是整根通长统一厚度历史事实；
- `tenon_area_thickness` = 局部实测 metadata，当前 geometry use = 0；
- 不从 P2 proxy、常识、名称或一般古建规则补造端部、榫卯、起拱或局部厚度变化。

---

## 7. Approved Canonical Reference-Length Policy｜D-038

由于历史完整长度 UNKNOWN，而 canonical `.blend` 需要一个可执行 realization，Product Owner 批准统一中性参考长度：

`canonical_reference_length_mm = 1000.0`

该值必须标记：

- classification: `PROJECT_RULE`
- source_layer: `ENGINEERING_REFERENCE`
- time_layer: `NON_HISTORICAL_REFERENCE_REALIZATION`
- production_use: `CANONICAL_REFERENCE_ONLY`
- replaceable: `true`
- historical_claim: `false`

1000 mm：

- 不是现状实测长度；
- 不是963设计候选；
- 不进入 historical evidence layer；
- 仅用于 canonical reference binary、mutation、reopen 和参数化验证；
- P3.2/P3.3 装配时必须由 building-specific evidence 或正式批准 candidate 提供实际长度，不得默认沿用；
- 必须来自 params JSON，不得作为共享 generator 裸常量。

### 7.1 Mandatory three-layer length isolation

必须明确保存并机械区分：

```text
historical_full_length_mm = null
  classification = UNKNOWN
  production_use = DO_NOT_LOCK

canonical_reference_length_mm = 1000.0
  classification = PROJECT_RULE
  source_layer = ENGINEERING_REFERENCE
  historical_claim = false

realization_length_mm = 1000.0
  role = GEOMETRY_EXECUTION_VALUE
  derives_from = canonical_reference_length_mm
```

约束：

- `historical_full_length_mm` 在 canonical build、mutation、rebuild 全流程始终保持 `null`；
- `realization_length_mm` 只能是工程执行字段，不得反写 historical layer；
- 若未来存在 building-specific approved length，必须通过显式 assembly/build input 覆盖 realization，而不是修改历史字段。

---

## 8. Canonical Geometry Rule

- unit = mm
- +X = 构件纵向
- +Y = 截面宽度
- +Z = 垂直厚度
- origin = longitudinal midpoint / transverse center / lower reference plane
- theoretical ends = `X = ±realization_length_mm / 2`
- Location `(0,0,0)` / Rotation `(0,0,0)` / Scale `(1,1,1)`

Canonical body：

> `realization_length_mm × width_mm × max_thickness_mm` centered rectangular bounded outer envelope

X = `[-L/2,+L/2]`；Y = `[-width/2,+width/2]`；Z = `[0,max_thickness]`。

Geometry semantics：

`PROJECT_RULE / BOUNDED_OUTER_ENVELOPE_REFERENCE / REPLACEABLE`

该 prism 只代表当前已知外包络上限下的 reference specimen，不是“历史整根梁通长均匀矩形截面”的声明。

`tenon_area_thickness_mm` 当前必须进入 params / semantic / review summary，但 geometry use = 0；不得生成局部薄化、榫头、榫区长度或起止位置。

禁止：camber、end profile、local thickness zones、mortise-tenon、cavity、hidden joint、无证据 bevel/decorative shaping、P2 proxy-derived geometry。

---

## 9. Shared Toolchain / Lean Rule

允许共享：

- `six_chuanfu_master_common` geometry utility
- batch runner
- validator
- review renderer
- semantic snapshot helper

最终必须独立：

- 2 component IDs
- 2 params JSON
- 2 local-only `.blend`
- 2 SHA256
- 2 semantic snapshots
- 2 review packages
- 2 Registry records

禁止 generic binary 代表上下两件；禁止 Object Scale 复制；禁止合并 ID。

---

## 10. Execution Stages

### Stage A｜Shared pipeline setup

建立一次 long-member generator / validator / renderer / semantic helper / batch orchestration。

共享代码不得出现 493.5 / 444 / 375 / 334 / 240.5 / 209 / 1000 等 component-specific 或 project-reference 裸常量；全部来自 params JSON。

### Stage B｜First Article = 下六椽栿

完整执行：params semantics、三层长度隔离、bbox/extents、origin/transform、max-thickness semantics、tenon metadata-only、unsupported geometry=0、P2 proxy non-use、deterministic regeneration、independent reopen、mutation、canonical rebuild、6/6 review assets、binary local-only。

任何合同外问题立即 STOP，交回 ChatGPT。

### Stage C｜上六椽栿

Stage B PASS 后，用相同 pipeline 参数驱动；不重新设计 generator/validator/renderer。

### Stage D｜Batch validation

完成两件独立资产、13 张 review inputs、Registry pending record 和保护性 baseline checks。

---

## 11. Mutation Strategy

每个 Master 至少两类：

### Probe A｜reference realization length mutation

临时改变 `canonical_reference_length_mm` 并令 `realization_length_mm` 显式跟随：

- 只改变 X extent；
- Y/Z 不变；
- origin 仍 X=0；
- semantic snapshot 正确反映 reference/realization mutation；
- `historical_full_length_mm` 始终保持 `null`。

随后 canonical rebuild 必须恢复 `canonical_reference_length_mm=1000.0` / `realization_length_mm=1000.0`。

### Probe B｜metadata-only tenon thickness mutation

临时改变 `tenon_area_thickness_mm`：

- params / semantic metadata 变化；
- canonical body geometry / bbox 完全不变；
- 不得出现局部削减、榫头、端部变化。

随后 rebuild 恢复正式参数。

---

## 12. Validation Matrix

每个 Master 必须 PASS：

1. unique component/master ID
2. authoritative Contract V002 / D-036
3. measured section trace to D-009
4. `historical_full_length_mm` remains UNKNOWN/null
5. `canonical_reference_length_mm=1000` only PROJECT_RULE / ENGINEERING_REFERENCE
6. `realization_length_mm` explicitly derives from canonical reference in canonical build
7. no historical/current/963 claim from reference or realization length
8. no reference/realization value written back into historical field
9. width matches params
10. Z outer bound matches max_thickness
11. max_thickness not promoted to confirmed uniform full-length section
12. tenon_area_thickness present as metadata
13. tenon_area_thickness geometry use = 0
14. origin/axes/transform correct
15. Scale=1
16. no world placement leakage
17. no naked historical/project-reference constants in shared code
18. no camber
19. no unsupported end profile
20. no local thickness zone
21. no mortise-tenon/cavity/hidden joint
22. no P2 PRIMARY_FRAME proxy geometry source
23. deterministic regeneration PASS
24. independent reopen PASS
25. reference-length mutation isolates X and preserves historical null
26. tenon metadata mutation leaves geometry unchanged
27. canonical rebuild after mutations PASS
28. `.blend/.blend1` absent from Git

Batch must PASS：

29. 2/2 params / blends / semantic snapshots / hashes
30. review 12/12 + overview 1/1
31. Registry 2 independent pending-review records
32. four approved Masters unchanged
33. P2 frozen baseline unchanged
34. Contract V002 unchanged
35. no unsupported extra Master production

---

## 13. Review Package

每个 Master 6 张：

1. FRONT
2. SIDE
3. TOP
4. AXON
5. DIMENSION_PARAMETER_SUMMARY
6. EVIDENCE_UNCERTAINTY_SUMMARY

另：`SIX_CHUANFU_MASTER_BATCH_V001_OVERVIEW.png`

共 13 张。

Overview 要求：两件同画面、同轴向、真实相对截面尺度；纵向统一使用相同 1000 mm engineering reference，并必须显著标注：

> `LENGTH NORMALIZED TO 1000 mm — NON-HISTORICAL`

> `RELATIVE SECTION SCALE IS MEANINGFUL; MEMBER LENGTH IS NOT`

避免被误读为真实或历史长度比较。

Codex 只做文件与机器检查；ChatGPT / Product Owner 做视觉与历史表达审核。

---

## 14. Registry Rule

更新 `production/zhenguo_wanfo/registry/P3_1_COMPONENT_MASTER_LIBRARY_V001.json`：

- 已批准四个 Master 保持不变；
- 新增两条独立 frame Master record；
- 初始只能为 engineering complete + `PENDING_CHATGPT_PRODUCT_OWNER_REVIEW`；
- 不得提前 Approved；
- orphan/duplicate = 0。

---

## 15. Protected Assets

前后 hash/manifest compare：

- P2 frozen baseline
- T-011 approved column
- T-012 approved dou assets/reviews/Registry semantics
- Contract V002

任一 mismatch：STOP，不自动修复。

Codex 不修改 `docs/project_control/`。

---

## 16. Hard Fail Conditions

任一不得 COMPLETE：

- historical length 被填成已知值
- 1000 mm reference / realization 被描述为 historical/current/963 length
- reference/realization length 写入 historical evidence field
- **REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY**：任何后续 assembly/building instance 在没有显式 building-specific approved length 输入时，默认继承 1000 mm canonical reference
- max_thickness 被宣称全长历史统一厚度
- tenon-area thickness 驱动无证据局部几何
- unsupported camber/end profile/local thickness/joinery/cavity
- P2 PRIMARY_FRAME proxy 被当作历史 Master 几何来源
- generic binary 或 Object Scale 复制上下两件
- mutation 污染 canonical
- Registry 提前 Approved
- approved assets/P2/Contract 被修改
- `.blend/.blend1` 进入 Git
- First Article 未 PASS 就生产第二件
- Codex 遇到合同外问题后自行改变 evidence/geometry rule 而未 STOP 回 ChatGPT

其中 `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` 本轮至少必须写入 semantic/validation contract，供 P3.2/P3.3 强制继承；T-013 本身不生成 assembly instance。

---

## 17. Retry / Cost Discipline

- 同一纯实现根因最多 2 次有证据的修正；
- 合同/证据/几何语义问题不允许 Codex 自行重试推理，第一次即 STOP；
- 不重复全文分析历史资料；
- 不重复构建两套工具链；
- 不做 Codex 视觉判断；
- 不输出长过程叙述；
- 最终保留全部正式 validation evidence。

---

## 18. Completion Criteria

T-013 engineering COMPLETE 需：

- 2/2 independent params / Masters / semantic snapshots / SHA256
- First Article PASS before second Master
- 2/2 deterministic regeneration / reopen / mutation / rebuild
- historical length UNKNOWN preserved
- 1000 mm reference correctly classified as non-historical project rule
- realization length explicitly isolated from historical length
- reference-length mutation preserves historical null
- tenon metadata-only behavior mechanically proven
- `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` carry-forward rule encoded
- unsupported geometry = 0
- review package 12+1 complete
- Registry 2 pending-review records
- P2 / Contract V002 / approved four Masters unchanged
- no `.blend` in Git
- engineering commit created and published per RC-010

之后由 ChatGPT / Product Owner 审核 13 张图并决定是否批准两件 Master。

T-013 approval 也不自动等于 P3.1 PASS；仍需独立 P3.1 Gate Review。

---

## 19. Authorization Boundary

**AUTHORIZED / READY_FOR_LOCAL_EXECUTION / D-038**。

Product Owner 已明确批准：

1. T-013 V002 scope / geometry / validation；
2. `canonical_reference_length_mm = 1000` 的非历史工程参考规则；
3. 三层长度隔离：historical null / canonical reference / realization execution value；
4. `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` Hard Fail carry-forward；
5. `CHAT_FIRST_CODEX_EXECUTOR_MODE_TRIAL`；
6. Codex `MEDIUM DEFAULT / HIGH ONLY BY EXPLICIT CHATGPT ESCALATION`。

Codex 可在完成最新 `main` 同步后开始 Stage A / Stage B。