# T-018 V002｜Architecture Closure Review V001

## Status

**COMPLETE / OUTCOME B / IMPLEMENTATION REMAINS FROZEN**

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Task：T-018｜P3.3 整殿确定性生成与参数变更验证 V002
- Review date：2026-09-18
- Review source main：`82455c46f95e70dee20893ba5bb0ee495d4826a4`
- PR #6：OPEN / HOLD / UNTOUCHED
- Review nature：bounded architecture review only
- No upstream rule modified
- No implementation code written
- No Blender / Actions run
- No Stage B restart

---

## 1. Review Question

本次 review 不解决某一条 Frame Tier 公式，而只回答：

> 当前 T-018 从 canonical 参数 / P3.2 relationship foundation 到 whole-building control geometry 的架构是否已经闭合？如果未闭合，缺口是局部 A、有限同类 B，还是底层体系失效 C？

固定判定：

- **A**：架构闭合，仅单一局部漏项；
- **B**：存在少量同层、同性质缺口，可通过有限 authority-completion package 一次性补齐；
- **C**：底层 identity / parameter / relationship / evidence architecture 本身无法支撑 T-018，需要扩大 rebaseline。

**Final outcome：B。**

不是 A：缺口不只 Frame Tier 一项。  
不是 C：P3.0/P3.1/P3.2 identity/relationship vocabulary、T-017 accounting / parameter classification、T-019 PURLIN disposition、T-020 X/Y shared-ridge datum 均未发现需要推翻的证据。

---

## 2. What Is Structurally Sound

以下基础层继续成立，不建议重开：

1. **Identity / accounting**
   - 365 / 365 stable instances；
   - 11 / 11 families；
   - no identity omission identified in this review。

2. **P3.1 Master layer**
   - 6 approved Masters remain valid；
   - no Master geometry/evidence conflict found。

3. **P3.2 vocabulary**
   - `SUPPORT / CONNECT / LOCATE / REPEAT / BELONG` remains the only relation vocabulary；
   - representative assembly relationships remain valid as engineering semantics；
   - P3.2 Frame Tier interfaces explicitly define semantic LOWER/UPPER tier datum but do **not** claim actual whole-building elevation.

4. **Evidence separation**
   - PM-003～007 remain validation-only；
   - reconstructed-design values remain replaceable candidates；
   - no historical-claim upgrade is required by the gaps found here。

5. **T-020**
   - X=0 / Y=0 project-model center；
   - `RIDGE_Y=0`；
   - N03 sole shared ridge；
   - no `ROOF_PURLIN_S_03`；
   - 7/7 PURLIN remain DEFERRED。

因此当前问题不是“前面全部做错”，而是 **参数/语义基础与实际 whole-building placement 之间缺一层完整控制规格**。

---

## 3. 11-Family Production Closure Matrix

| Family | Count | Current closure | Review result |
|---|---:|---|---|
| GRID_CONTROL | 8 | X/Y/Z datum and design grid can be resolved from PM-008/009/010/011/012 + MOD-001 + T-020 | **CLOSED** |
| COLUMN | 12 | origin from grid; Z datum from Z-007; height from Z-006-RC-01; approved Master exists | **CLOSED** |
| PRIMARY_FRAME | 8 | semantic identity/accounting closed; exact vertical baseline is not explicitly authorized; legacy depth-frame placement referenced DG-113 while width-frame provenance does not consistently record it | **BLOCKED AT PLACEMENT** |
| FRAME_CONTROL | 54 | semantic/control identity closed; exact tier Z and LOW/UP post endpoints require cross-system vertical rule not currently closed | **BLOCKED AT PLACEMENT** |
| FRAME_SUPPORT | 54 | proxy identity closed; endpoints inherit unresolved Frame Control placement | **BLOCKED BY FRAME_CONTROL** |
| PURLIN | 7 | identity/Y chain/shared ridge closed; Z authority IDs are named by T-020, but exact eave-base/cumulative placement formula is not serialized as a complete machine authority | **PARTIAL / CLOSURE ASSERTION REQUIRED** |
| RAFTER | 36 | identity/count closed; endpoints depend on roof controls; S00/S01/S02 adjacency and X-station/gable mapping are not represented as explicit runtime placement authority | **PARTIAL** |
| ROOF_ENVELOPE | 6 | identity/count closed; six surface identities exist; exact corner/edge topology is not explicitly encoded in T-017 runtime graph | **PARTIAL** |
| GABLE_CONTROL | 4 | identity/count closed; gable projection input exists; exact control polyline/endpoints are not explicitly encoded as canonical whole-building topology | **PARTIAL** |
| BRACKET_ARM | 88 | UNKNOWN_BLOCKED identity/evidence boundary closed; deterministic engineering-marker anchoring to whole-building controls is not explicitly closed | **PARTIAL / STAGE-C RISK** |
| BRACKET_CONTACT | 88 | PROXY_ONLY identity/evidence boundary closed; deterministic proxy anchor placement is not explicitly closed | **PARTIAL / STAGE-C RISK** |

### Key observation

缺口高度集中在：

> **Building parameters + P3.2 semantics → explicit whole-building control placement / topology**

而不是分散在 identity、Master、evidence、accounting 各层。

---

## 4. Stage-B Detailed Placement Authority Closure

| Critical object/control | X | Y | Z | endpoints / surface | Result |
|---|---|---|---|---|---|
| Plan Grid | closed | closed | Z-007 | axis extents derivable | **PASS** |
| Column origin / height | closed | closed | Z-007 + Z-006-RC-01 (+ Z-005 where applicable) | Master-local axis/origin available | **PASS** |
| Primary Frame baseline | grid-derived | grid-derived | **not closed** | depends on unresolved base elevation | **STOP** |
| Frame Tier N/S 01..03 | width span derivable | FR-004/005/006 chain derivable | **not closed** | tier endpoints inherit unresolved Z | **STOP** |
| Frame Post LOW/UP | X from frame station | Y from tier station | **not closed** | upper endpoint also depends on roof surface/control | **STOP** |
| Roof control N/S 00..03 | gable/grid X extents derivable | T-020 Y chain closed | **partial** | exact base + cumulative Z formula must be explicitly closed | **HOLD** |
| Rafter segments | X stations derivable candidate | roof-control Y | roof-control Z | adjacency S00/S01/S02 not explicit authority | **HOLD** |
| Roof Envelope | X edge candidate available | roof-control Y | roof-control Z | six surface corner maps not explicit authority | **HOLD** |
| Gable Control | OUT-003 candidate X boundary | roof-control Y | roof-control Z | required polyline topology not explicit authority | **HOLD** |

This confirms CP-03's first STOP was not an isolated coding issue.

---

## 5. Cross-System Dependency Review

### 5.1 Confirmed legitimate bridges

- Building modular system (`MOD-*`) can feed multiple systems via building-level rule.
- T-020 explicitly bridges:
  - reconstructed design plan → column grid；
  - FR-007 + MOD-002 → roof shared-ridge Y chain。
- P3.2 representative interfaces allow engineering `LOCATE / CONNECT / SUPPORT / REPEAT` semantics without historical upgrade.

### 5.2 Current unresolved bridges

1. **Column / Bracket / Frame vertical bridge**
   - legacy P2 implementation used `DG-113` outside its current canonical `ORG-BRACKET-SYSTEM` target；
   - no current whole-building project rule authorizes that reuse。

2. **Roof → Frame tier bridge**
   - `ROOF-004/005/006` and `ROOF-007/008/009` belong to roof elevation authority；
   - Frame Control currently references them, but no explicit cross-system project rule defines which series controls which frame point。

3. **Column height → Roof Z bridge**
   - T-020 names Z-006-RC-01 in `z_authority`；
   - exact machine formula for eave/base elevation and cumulative purlin Z placement is not present as a complete serialized placement rule.

4. **Control topology → runtime geometry bridge**
   - T-017 graph currently has 372 relationships:
     - 370 `BELONG`
     - 2 project-level `LOCATE`
   - runtime `SUPPORT / CONNECT / LOCATE / REPEAT` topology for 365 objects is not instantiated there.
   - This is not a T-017 contract violation—T-017 was a foundation task—but T-018 cannot safely replace the missing topology with naming heuristics or old P2 transforms.

---

## 6. P3.2 Compatibility Finding

P3.2 itself does **not** need reopening.

Important distinction:

- P3.2 Unit B deliberately defines `CTL-FRAME-001__LOWER-TIER-DATUM` / `UPPER-TIER-DATUM` as **semantic ordinal only; no historical elevation**.
- Therefore the missing whole-building Frame Tier Z authority is a **P3.3 project-placement problem**, not evidence that P3.2 failed.
- P3.2 Unit C's representative `REPEAT` example references PM-005; T-020/T-018 V002 correctly prohibit using observed PM-005 as reconstructed-design whole-building placement. Representative assembly semantics must not be copied wholesale into whole-building design placement.

---

## 7. Hidden-Risk Pre-mortem

Before any restart, the following failure paths must be closed explicitly:

1. **Frame Tier fix changes Roof**
   - prohibited unless declared in affected-set contract.

2. **Roof control base Z chosen by code convention**
   - must be authority-defined before compiler implementation.

3. **Rafter / Envelope topology inferred from ID strings**
   - prohibited unless the mapping itself is a formal control-topology specification.

4. **Bracket proxy/UNKNOWN markers recover P2 transforms**
   - prohibited; anchors must derive from approved controls/interfaces.

5. **Compiler and validator share adjacency/formula implementation**
   - validator must read an independent specification/invariant set.

6. **Old PR #6 code re-enters V002**
   - PR #6 remains HOLD until a later publication decision; no code reuse by default.

7. **New completion rule mutates protected upstream**
   - additive companion specification preferred; any actual upstream amendment requires separate Product Owner decision.

---

## 8. Final A / B / C Judgment

### Outcome：**B｜有限同类缺口**

Reason:

- Not A: at least four related closure areas exist—frame vertical placement, roof-Z exact closure, roof runtime topology, later bracket anchor closure.
- Not C: all gaps sit at one architectural seam; identity, Master, evidence, parameter classification, accounting, P3.2 vocabulary, and T-020 shared-ridge X/Y architecture remain usable.

### What B means

Do **not** fix items one by one.

Before T-018 CP-03 restarts, produce one bounded **Control Placement Authority Completion Package** that closes only this seam.

The package must not redesign P3.0/P3.1/P3.2, must not alter 365 accounting, must not change PURLIN disposition, and must not add historical dimensions.

---

## 9. Maximum Allowed Completion Scope

The next design may contain only four specifications:

1. **Placement Authority Closure Matrix**
   - every Stage-B critical X/Y/Z/endpoint/surface must resolve to a source rule.

2. **Cross-System Dependency Whitelist / DAG**
   - explicit allowed direction only；
   - no cycles；
   - no hidden parameter reuse.

3. **Control Topology Map**
   - Purlin chain；
   - Rafter adjacency；
   - Roof Envelope corners；
   - Gable control polyline；
   - Frame Tier/Post linkage。

4. **Impact / Non-Impact Contract**
   - exact affected object classes；
   - exact protected/non-affected objects；
   - machine rejection if effects escape declared set。

No implementation, Blender, 365 runtime expansion, mutation, or PR #6 work is allowed while this package is only being designed.

---

## 10. Escalation Rule

After the bounded package is designed:

- if all missing closure can be expressed with existing canonical parameters / existing five P3.2 relation types / project-rule semantics, remain **Outcome B** and apply the minimum completion;
- if it requires new historical dimensions, changes P3.2 relationship vocabulary, changes component identity, or creates cyclic authority, escalate to **Outcome C** and stop before modification.

Current evidence does **not** justify Outcome C.
