# T-018｜P3.3 整殿确定性生成与参数变更验证 V002

## Rebaseline Task Contract｜LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.3｜构件驱动整殿重建
- Task ID：T-018
- Engineering ID：`P3_3_DETERMINISTIC_WHOLE_BUILDING_GENERATION_V002`
- 中文任务名：整殿确定性生成与参数变更验证
- Task Goal：不变；V002 是同一 T-018 的 Rebaseline，不创建新 T 编号
- Status：LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED
- Date：2026-09-18
- Supersedes：T-018 V001 implementation design / D-051 contract
- Existing implementation history：PR #3 SUPERSEDED / PR #6 HOLD
- Merge authorization：FALSE
- Decision authority：D-059

> 本 V002 只重新设计 T-018 如何消费上游 canonical 成果，不默认重开 P3.0/P3.1/P3.2/T-017/T-019/T-020。任何上游矛盾必须 STOP 并单独处理，不得在 T-018 内静默修补。

> D-052 是 V001 的历史工程执行授权，**不自动延续到 V002**。V002 进入 Stage A 前仍需 Product Owner 单独授权。

---

## 1. Rebaseline 原因

T-018 V001 暴露的主要问题不是单一代码缺陷，而是工程边界不足：

1. T-017 已将 PM-003～007 定义为 `VALIDATION_REFERENCE`，但旧 T-018 曾直接使用 observed 值驱动 placement；
2. T-017 缺少 reconstructed-design whole-building absolute/shared-ridge datum，后由 T-020 补齐；
3. T-020 改变 T-018 的可用 authority 后，V001 合同与 mutation 假设未整体 rebaseline；
4. placement、representation、Blender generation、validator 曾重复计算同一几何，允许临时规则进入执行层；
5. compiler 与 validator 过度共享实现假设，可能出现“同错同 PASS”；
6. replacement PR #6 修正 datum 的同时发生 capability regression。

V002 的目标是切断上述错误链。

---

## 2. V002 核心架构原则

正式数据流固定为：

`Canonical Upstream Inputs → Authority Resolver → Building Control Model → Runtime Placement Manifest → Representation Specification → Blender Executor → Independent Evidence`

### 2.1 Single Authority Principle

T-018 不新建第二套 authority truth。

Authority Resolver 只读取 canonical metadata / rule：

- T-017 parameter bindings；
- T-020 reconstructed-design datum rule；
- P3.1 approved Master contracts；
- P3.2 canonical relationship vocabulary / interfaces；
- T-017 365 accounting / assembly graph。

Resolver 只能输出“解释结果/审计报告”，不得自行创造新的建筑参数值或历史事实。

### 2.2 One Geometry Calculation Principle

建筑 placement 只能在 Pure Placement / Control Compiler 中计算一次。

Blender、renderer、representation builder 不得重新推导建筑坐标，不得镜像补点，不得依据视觉需要修改 endpoint。

### 2.3 Independent Validation Principle

关键 invariant validator 不得调用 placement compiler 的几何计算函数来生成“正确答案”。

允许共享：
- JSON schema / field names；
- canonical input reader；
- stable serialization utility。

禁止共享：
- placement formula；
- roof chain derivation；
- grid coordinate derivation；
- endpoint derivation。

### 2.4 Representation ≠ Placement

“在哪里”与“画成什么”严格分离。

Representation layer 只能消费已经锁定的 placement/endpoints，不能改变其坐标或 authority。

### 2.5 No Downstream Patch-Up

后阶段发现前阶段问题时：
- STOP；
- 回到问题所属层修复；
- 从该层开始重新执行后续回归；
- 禁止在 Blender / renderer / review layer 做补偿性修正。

---

## 3. Protected Upstream Candidate Baseline

在 Stage A PASS 前，下列对象属于 **candidate protected baseline**，只读审计、不修改：

- P3.0 canonical Ontology / Registry identity；
- P3.1 approved Component Masters；
- P3.2 schema / interfaces / five relationship types；
- T-017 365/365 accounting / Building Assembly Graph / parameter bindings；
- T-019：7/7 PURLIN = DEFERRED；
- T-020：reconstructed-design coordinate datum + shared ridge authority；
- P3.3 DoD V001 / five Gate Hard Fails。

Stage A 若发现真实 canonical contradiction：
> T-018 STOP。不得通过 V002 代码绕过；必须回到上游 correction decision。

---

# 4. 四阶段管理 Gate + 九个技术检查点

## Stage A｜规则基线

**目标：先证明上游规则彼此兼容，并明确 T-018 有权使用什么。**

### CP-01｜Upstream Compatibility Audit

只读核对：

- 11 family / 365 accounting identity；
- disposition；
- P3.1 Master eligibility；
- P3.2 relationship semantics；
- T-017 parameter bindings；
- T-019 PURLIN correction；
- T-020 datum / shared ridge；
- historical/evidence boundaries。

最低强制检查：

- PM-003～007 = validation-only；
- PM-008～012 = reconstructed-design placement candidates；
- `FR-007 + MOD-002` = roof horizontal lineage；
- `ROOF-007/008/009` = roof Z chain；
- Z datum = Z-007；
- N03 = sole shared ridge；
- S03 prohibited；
- 7/7 PURLIN = DEFERRED；
- relation vocabulary exactly `SUPPORT / CONNECT / LOCATE / REPEAT / BELONG`。

**输出：**
`P3_3_T018_V002_UPSTREAM_COMPATIBILITY_AUDIT.json`

输出必须是 derived audit，不是新 authority。

**PASS：**
- no unresolved canonical contradiction；
- no missing authority required for Stage B control model；
- protected-input hashes captured。

### CP-02｜Authority Resolver

将每项可用输入按 canonical metadata 自动归类：

- `GENERATIVE_AUTHORITY`
- `VALIDATION_ONLY`
- `PROHIBITED_FOR_PLACEMENT`
- `UNRESOLVED / STOP`

不得靠 T-018 hardcode 把 observed 参数“人工列黑名单”作为唯一保护；必须优先由 canonical metadata / T-020 policy 推导。

**输出：**
`P3_3_T018_V002_AUTHORITY_RESOLUTION_REPORT.json`

**Stage A PASS 条件：**
- CP-01 PASS；
- CP-02 PASS；
- no unresolved authority；
- ChatGPT review PASS。

Stage A PASS 后，candidate protected baseline 才升级为本次 T-018 V002 的 **Protected Upstream Baseline**。

---

## Stage B｜关键骨架首件

**目标：在 365 full runtime 之前，先证明整殿控制骨架本身正确。**

### CP-03｜Pure Building Control Model

建立纯数据 control model，不依赖 Blender：

最低包含：

- X/Y/Z project-model datum；
- reconstructed-design plan grid；
- major elevation controls；
- frame tier/control authority；
- roof control chain；
- N00/N01/N02/N03/S02/S01/S00；
- ridge terminal；
- gable / roof envelope control boundaries；
- parameter/rule provenance。

所有坐标读取或推导自 Stage A 已授权 authority。

**输出：**
`P3_3_T018_V002_BUILDING_CONTROL_MODEL.json`

### CP-04｜Independent Invariant Validator

独立验证至少：

#### Plan
- grid symmetry / ordering；
- PM-008/009/010 与 MOD-001 的 design dimensions；
- PM-011 / PM-012 与分间设计的整体一致性；
- observed PM-003～007 不进入 generative provenance。

#### Roof
- north Y monotonic toward 0；
- south Y monotonic toward 0；
- N03 exactly one shared ridge；
- no S03；
- all north/south roof chains terminate on same ridge；
- roof surfaces cannot cross ridge；
- all rafter ridge endpoints converge to authorized ridge；
- FR-007 cumulative half-run exact consistency；
- roof Z rises are monotonic per authorized chain。

#### Evidence
- no historical-claim upgrade；
- no P2 transform；
- no unauthorized synthetic local rule；
- no naked building placement constant replacing canonical authority。

### CP-05｜Critical Skeleton First Article

从 control model 生成只用于工程审核的关键骨架：

- plan grid；
- major frame controls；
- roof control chain；
- representative frame/rafter topology；
- full roof envelope / gable controls。

生成固定：
- PLAN
- FRONT
- SIDE
- AXON

Blender 如被使用，只能作为 dumb renderer：坐标全部来自 control model，不允许再推导建筑规则。

**Stage B PASS 条件：**
- CP-03 PASS；
- CP-04 PASS；
- CP-05 machine review PASS；
- ChatGPT actual four-view visual review PASS；
- no structural/topological anomaly。

Stage B FAIL 时禁止进入 365 runtime。

---

## Stage C｜完整整殿

**目标：把已验证的 control model 映射为 365/365 runtime，并证明没有 identity / evidence / capability 回退。**

### CP-06｜365 Runtime Expansion

严格从 T-017 accounting 映射 365 instances。

当前 canonical family/disposition baseline：

| Family | Count | Disposition |
|---|---:|---|
| BRACKET_ARM | 88 | UNKNOWN_BLOCKED |
| COLUMN | 12 | GENERATE_FROM_FORMAL_COMPONENT |
| BRACKET_CONTACT | 88 | PROXY_ONLY |
| PRIMARY_FRAME | 8 | UNKNOWN_BLOCKED |
| FRAME_CONTROL | 54 | CONTROL_ONLY |
| GABLE_CONTROL | 4 | CONTROL_ONLY |
| GRID_CONTROL | 8 | CONTROL_ONLY |
| PURLIN | 7 | DEFERRED |
| RAFTER | 36 | PROXY_ONLY |
| ROOF_ENVELOPE | 6 | ENVELOPE_ONLY |
| FRAME_SUPPORT | 54 | PROXY_ONLY |

要求：
- 365/365；
- identity exact；
- no anonymous component；
- no silent omission；
- parent/relationship traceability；
- placement provenance；
- evidence boundary；
- protected upstream unchanged。

### CP-07｜Representation + Capability Regression Contract

Representation 只消费 CP-06 placement：

- COLUMN → approved P3.1 `CMP-COLUMN-001_MASTER`；
- BRACKET_CONTACT → non-historical technical proxy；
- BRACKET_ARM → bounded UNKNOWN engineering marker；
- PRIMARY_FRAME → UNKNOWN/semantic engineering representation；
- FRAME_CONTROL → control segment/polyline；
- FRAME_SUPPORT → proxy connector segment；
- GRID_CONTROL → control axis；
- PURLIN → DEFERRED datum/control representation；
- RAFTER → endpoint-derived proxy segment；
- ROOF_ENVELOPE → control surface；
- GABLE_CONTROL → control polyline。

禁止：
- generic cube fallback 代替 formal Master；
- point-only marker 代替要求可读的 segment/surface；
- representation layer 重算 coordinates；
- Proxy / Control / Envelope / Deferred historicalization。

建立 machine-readable **Golden Capability Contract**，来源只能是：
- current P3.3 DoD；
- T-017 canonical accounting；
- P3.1/P3.2/T-019/T-020 canonical requirements；
- 已经正式确认需要保留的 T-018 engineering capabilities。

不得把 PR #3 源码本身当 golden source。

### CP-08｜Dependency + Dual Mutation Verification

先生成 parameter → affected-runtime dependency map，再选 generative mutation。

固定 Test A：

**Observed Isolation**
- PM-005：3505.7 → 3605.7 mm
- expected：reconstructed-design placement changes = 0
- 用于证明 validation-only 参数不能污染生成。

Test B：

**Generative Propagation**
- parameter：由 dependency map 从 approved reconstructed-design generative parameters 中选择；
- 必须在执行前记录 expected affected set / unaffected set；
- mutation value 必须是 test-only；
- 选择结果在进入 Stage D 前由 Product Owner批准。

要求：
- expected dependent objects change；
- non-dependent drift = 0；
- evidence classification unchanged；
- source files unchanged；
- restore returns exact canonical semantic snapshot。

**Stage C PASS 条件：**
- CP-06 PASS；
- CP-07 PASS；
- CP-08 data-level dependency tests PASS；
- five existing P3.3 Hard Fails 5/5 EXPECTED_REJECTION；
- no capability regression；
- ChatGPT machine review PASS。

---

## Stage D｜正式执行验收

**目标：证明 Stage A-C 已锁定的系统可在正式 Blender/Actions 环境确定性重放。**

### CP-09｜Blender / Reopen / Mutation / Restore / Evidence

正式链：

**Run A**
clean checkout → blank Blender → canonical build → save → validate → snapshot

**Run B**
new Blender process → independent reopen → runtime metadata / scene coordinate validation → normalized snapshot compare

**Run C**
Observed Isolation + approved Generative Mutation test → clean rebuild → validate

**Run D**
discard test runtime → canonical clean rebuild → validate → normalized snapshot exact restore

正式环境：
- `ubuntu-latest`
- Blender 4.5.13 linux-x64

必须产生：
- canonical .blend artifact；
- validation reports；
- mutation reports；
- restore report；
- protected-input hashes；
- PR HEAD binding；
- review image hashes；
- PLAN / FRONT / SIDE / AXON；
- Evidence Manifest。

最终四视图必须再次由 ChatGPT 实际目视审核。

**Stage D PASS ≠ T-018 CLOSED。**

只有：
1. Stage A-D 全 PASS；
2. ChatGPT formal review PASS；
3. Product Owner T-018 approval；
4. Product Owner merge authorization；
5. merge + Project Control update；

之后 T-018 才可 CLOSED。

---

# 5. V002 Hard Stops

除 P3.3 五项 Gate Hard Fail 外，V002 增加以下 task-level STOP：

1. `UNAUTHORIZED_AUTHORITY_USE`  
   validation-only / prohibited input 进入 placement。

2. `UPSTREAM_CANONICAL_CONTRADICTION`  
   T-017/T-019/T-020 canonical 规则互相无法同时成立。

3. `BLENDER_REDERIVES_BUILDING_GEOMETRY`  
   Blender/renderer 自己计算建筑 placement。

4. `COMPILER_VALIDATOR_SELF_CONFIRMATION`  
   independent validator 调用 compiler 几何函数得出 expected result。

5. `CAPABILITY_REGRESSION`  
   已锁定 Golden Capability Contract 被删除或降级。

6. `UNDECLARED_BUILDING_CONSTANT`  
   用源码裸常量替代已有 canonical building authority。

7. `UPSTREAM_PROTECTED_INPUT_MUTATION`  
   T-018 修改 Protected Upstream Baseline。

8. `DOWNSTREAM_PATCHES_UPSTREAM_ERROR`  
   在 representation / Blender / renderer 层补偿 placement / authority 错误。

任一出现：STOP，不允许“为了通过 Actions”继续补丁。

---

# 6. Existing PR Policy During Rebaseline

### PR #3
- SUPERSEDED implementation history；
- read-only reference；
- DO NOT MERGE；
- 不作为 V002 源码基线。

### PR #6
- HOLD；
- 不继续 Review Patch 01；
- 不 rerun Actions；
- 不 merge。

V002 获批后先做 publication preflight：

1. 若 Codex 能从最新 canonical main 安全同步并更新 PR #6，则 PR #6 可作为同一 T-018 的 V002 active implementation PR，但其当前 T-018 implementation files 应按 V002 contract 受控重构，不采用“继续层层补丁”的策略。
2. 若平台无法安全更新 PR #6，则 STOP，由 Product Owner 批准 scoped RC-014 exception 后关闭 PR #6 为 superseded，再创建唯一 active V002 replacement PR。
3. 任一时刻只允许一个 active T-018 implementation PR。

---

# 7. Review / Authorization Model

为避免 9 个检查点造成管理负担：

- 管理层只显示 Stage A/B/C/D；
- CP-01～09 是技术检查点，不单独占 T 编号；
- Stage 内部失败由 ChatGPT归因并 STOP；
- 只有重大前提变化、上游 correction、generative mutation parameter 选择等需要 Product Owner 新决策；
- V002 contract approval 后仍需明确 engineering execution authorization；
- final T-018 approval / merge authorization 保持独立。

---

# 8. V002 Draft Acceptance Summary

T-018 V002 成功时最终必须证明：

> 同一套 canonical component identity、relationship、reconstructed-design parameter 与 evidence boundary，可以从 clean state 生成相同的 365-instance whole-building runtime；所有建筑 placement 在 Blender 之前已经确定且可独立验证；Blender 只执行而不解释建筑规则；observed data 不污染 reconstructed-design placement；generative parameter mutation 能按声明依赖传播并精确 restore；最终机器证据与四视图均通过。

这才是 T-018 的正式交付定义。

---

## 9. 当前状态

`LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED`

当前禁止：

- Codex 修改 T-018 implementation；
- PR #6 patch；
- PR #6 Actions rerun；
- PR #3 / #6 merge；
- 提前选择 generative mutation parameter。

下一动作：

> V002 已由 Product Owner 批准并锁定。下一动作：等待 Product Owner 单独授权 Stage A engineering execution。
