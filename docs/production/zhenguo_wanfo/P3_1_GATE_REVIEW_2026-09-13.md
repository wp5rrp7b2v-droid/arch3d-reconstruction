# P3.1 Gate Review｜Component Master & Variant Library｜2026-09-13

Status: **HOLD / 7 OF 9 PASS / DOD-07 PARTIAL / DOD-09 PENDING**  
Phase: `P3｜古建筑构件系统化与组合建模`  
Gate: `P3.1｜Component Master & Variant Library`  
Authoritative DoD: `docs/production/zhenguo_wanfo/P3_1_DEFINITION_OF_DONE_V001.md` / D-032  
Review basis: T-010 / T-011 / T-012 / T-013 approved outputs through D-039

## 1. Executive Conclusion

P3.1 已完成核心工程与证据工作，6/6 `MASTER_REQUIRED` canonical Masters 均已通过工程、视觉与 Product Owner 审批；Scope / Identity / Contract / evidence boundary / reproducibility / Registry 均具备闭环证据。

当前 **不能直接宣告 P3.1 PASS / CLOSED**，原因不是 Master 几何或历史证据失败，而是锁定 DoD-07 明确要求：

> 同时生成至少一张 Library Overview，展示当前 P3.1 已完成的 Master / Variant 集合及其状态。

当前仓库只有：

- `DOU_MASTER_BATCH_V001_OVERVIEW.png`
- `SIX_CHUANFU_MASTER_BATCH_V001_OVERVIEW.png`

尚无一张覆盖当前 **全部 6 个 approved Masters** 的 P3.1 Library Overview。

因此：

- DoD-01～06：PASS
- DoD-07：PARTIAL / HOLD
- DoD-08：PASS
- DoD-09：PENDING（本 Gate Review 已建立，但仍需 DoD-07 closure + Product Owner final Gate approval）

当前 Gate Score：**7 PASS / 1 PARTIAL / 1 PENDING**。

---

## 2. DoD Review

### DoD-01｜Component Master Eligibility & Scope Matrix — PASS

Evidence:

- `P3_1_COMPONENT_MASTER_SCOPE_MATRIX_V001.json`
- `P3_1_SCOPE_IDENTITY_VALIDATION_REPORT_V001.json`

Results:

- P3.0 Registry coverage = `11/11`
- P1 minimum candidate scope = `9/9`
- total review records = `27`
- `MASTER_REQUIRED = 6`
- `EVIDENCE_REVIEW_BEFORE_MASTER = 0`
- `PROXY_ONLY = 4`
- `CONTROL_ONLY = 3`
- `ENVELOPE_ONLY = 1`
- `DEFERRED_INSUFFICIENT_EVIDENCE = 13`
- unexplained pending = `0`

Conclusion: coverage and unique eligibility classification satisfy DoD-01.

### DoD-02｜Evidence-backed Component Identity Resolution — PASS

Evidence:

- `P3_1_COMPONENT_IDENTITY_RESOLUTION_V001.json`
- T-010 / D-033

Key conclusions retained:

- `BRACKET_ARM` aggregate remains proxy where individual 栱/昂 cannot be evidenced.
- `BRACKET_CONTACT` is not silently reinterpreted as 小斗; DG-114 remains UNKNOWN.
- P2 `PRIMARY_FRAME` aggregate is not reused as historical geometry; lower / upper six-chuanfu are separately evidence-qualified components.
- Purlin / rafter / bottom dou and other named members remain Deferred where geometry evidence is insufficient.
- No `EVIDENCE_REVIEW_BEFORE_MASTER` record remains unresolved.

Conclusion: PASS.

### DoD-03｜Canonical Component Master Asset Contract — PASS

Evidence:

- `P3_1_MASTER_ASSET_CONTRACT_V002.json`
- D-036

Contract scope = 6 and defines unit, axes, origin, transform, geometry LOD/mode, parameter contract, variant axes, placement-only distinctions, evidence boundaries, prohibited geometry, review and reproducibility requirements.

V002 field-mapping correction is authoritative for all later production.

Conclusion: PASS.

### DoD-04｜Canonical 3D Master Production — PASS

Approved Master coverage = **6/6 / 100%**:

1. `CMP-COLUMN-001｜柱` — D-035
2. `CMP-LUDOU-COLUMN-001｜柱头栌斗` — D-037
3. `CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗` — D-037
4. `CMP-DOU-INTERACTIVE-001｜交互斗` — D-037
5. `CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿` — D-039
6. `CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿` — D-039

`CONTROL_ONLY / ENVELOPE_ONLY` historical Master count = 0; unresolved proxies are not promoted.

Conclusion: PASS.

### DoD-05｜Parameterized Variant Model — PASS WITH ZERO FORMAL VARIANTS IN CURRENT EVIDENCE VERSION

Current `variant_ids` for the six approved Masters are empty. This is **not treated as missing production**, because current evidence does not establish a qualified within-Master historical variant requiring registration:

- column observed/report/reconstructed values remain evidence-layer alternatives, not automatically distinct historical variants;
- three dou identities are distinct component types, not variants of one generic dou;
- lower / upper six-chuanfu are distinct component identities / structural roles, not variants of one generic beam;
- placement rotation / instance number does not create variants.

The locked V002 contract defines variant axes and the formal variant contract (`stable_variant_id`, parent reference, parameter evidence, no Object Scale, placement-only exclusion).

Parameter-driven behavior is mechanically proven:

- Column: synthetic height mutation PASS / canonical rebuild PASS.
- Dou batch: synthetic mutation / deterministic regeneration / rebuild PASS for 3/3.
- Six-chuanfu: length mutation and metadata-only tenon mutation / rebuild PASS for 2/2.

Gate interpretation for current evidence version:

> **Formal registered variants = 0; parametric variant capability = PASS; no evidence-qualified variant is being silently omitted.**

If future evidence supports a real dimension/form/role variant, it must obtain a stable variant ID under the V002 contract before production use.

Conclusion: PASS.

### DoD-06｜Evidence-aware Geometry & Replaceability — PASS

Verified boundaries remain active:

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`
- `Z-006-RC-01` remains separate / replaceable
- `DG-114` remains UNKNOWN and unused as unified small-dou specification
- `HIS-002` originality remains unknown
- unsupported 45° corner / joinery / hidden-angle geometry is not promoted
- observed / report-ideal / reconstructed candidate layers remain separate
- six-chuanfu 1000 mm reference length is explicitly non-historical / replaceable and cannot leak into assembly

Mutation / replaceability evidence exists for column, dou and six-chuanfu families.

Conclusion: PASS.

### DoD-07｜Standard Component Review Package — PARTIAL / HOLD

Individual approved review coverage is complete:

- Column: 6/6 PASS
- Dou Masters: 18/18 individual PASS
- Six-chuanfu Masters: 12/12 individual PASS

Total individual Master review set = **36/36 PASS**.

Batch overviews also exist and passed after correction:

- Dou batch overview: PASS
- Six-chuanfu batch overview: PASS

However the locked DoD additionally requires **at least one Library Overview showing the current P3.1 completed Master / Variant collection and status**.

No whole-library overview covering all six approved Masters exists in the current review tree.

Required closure artifact:

`production/zhenguo_wanfo/review/P3_1/P3_1_MASTER_LIBRARY_OVERVIEW_V001.png`

Minimum content:

- all 6 approved Masters visible / identifiable;
- canonical name + component ID;
- status `APPROVED`;
- formal variant count = 0 for current evidence version;
- explicit statement that zero formal variants means no evidence-qualified registered variants, not absence of parametric capability;
- no new historical geometry claims;
- existing individual review renders may be composited; no Master regeneration is required.

Conclusion: **PARTIAL / HOLD**.

### DoD-08｜Library Registration, Machine Validation & Reproducibility — PASS

Evidence chain:

- `P3_1_COMPONENT_MASTER_LIBRARY_V001.json`
- T-011 validation: 22/22 PASS
- T-012 batch validation: PASS; 3 Masters registered; protected P2 hashes PASS
- T-013 batch validation: 26/26 each / 52 total PASS

Verified:

- unique Master identity
- evidence references retained
- approved Master Registry records = 6
- orphan formal variants = 0
- canonical transform / unit / axes checks PASS
- no world-placement leakage
- deterministic semantic regeneration PASS
- independent reopen PASS
- mutation / canonical rebuild PASS
- P2 frozen baseline unchanged

Conclusion: PASS.

### DoD-09｜Product Owner Review + Canonical Archive + P3.2 Readiness — PENDING

Completed before final Gate approval:

- Scope Matrix reviewed and approved through D-033.
- All six Master assets individually Product Owner approved through D-035 / D-037 / D-039.
- Registry approval coverage = 6/6.
- Current unresolved / non-historicized objects remain explicitly classified.
- Canonical local-only binaries have hash / semantic / generator / review / registry traceability.

P3.2 readiness answer is already structurally available:

**Approved P3.2 component nodes**

- 柱
- 柱头栌斗
- 单向长开斗
- 交互斗
- 下六椽栿
- 上六椽栿

**Current formal variants**

- 0 registered evidence-qualified variants in this P3.1 version.
- Parametric axes remain available under V002 and future evidence can create registered variants.

**Objects that remain non-historicized**

- Proxy: 4
- Control: 3
- Envelope: 1
- Deferred insufficient evidence: 13

**Assembly carry-forward boundaries**

- six-chuanfu canonical 1000 mm reference length must not enter building assembly implicitly;
- column RC height remains replaceable / not historical fact;
- DG-114 / HIS-002 / corner / joinery boundaries remain active.

Remaining conditions for DoD-09 PASS:

1. close DoD-07 with whole-library overview;
2. Product Owner explicitly approve `P3.1｜PASS / CLOSED` after this Gate Review is complete.

Conclusion: **PENDING**.

---

## 3. Gate PASS Condition Matrix

| Condition | Status |
|---|---|
| DoD 9/9 | HOLD — currently 7 PASS / 1 PARTIAL / 1 PENDING |
| Scope Matrix coverage | PASS / 100% |
| MASTER_REQUIRED coverage | PASS / 6 of 6 / 100% |
| EVIDENCE_REVIEW_BEFORE_MASTER unresolved | PASS / 0 |
| CONTROL / ENVELOPE historicized incorrectly | PASS / 0 |
| orphan Master / Variant | PASS / 0 |
| evidence traceability | PASS |
| mutation / replaceability | PASS |
| reproducibility / independent reopen | PASS |
| P2 frozen baseline unchanged | PASS |
| Product Owner final Gate approval | PENDING |

## 4. Current Gate Decision

**P3.1 = HOLD FOR ONE CLOSURE ARTIFACT + FINAL PRODUCT OWNER GATE APPROVAL.**

There is no geometry/evidence failure requiring Master rework.

The only production closure artifact still required is the whole-library overview. After it passes visual review, this Gate can be re-evaluated as 8/9 technical PASS + DoD-09 ready for Product Owner final approval.

P3.2 remains LOCKED until explicit P3.1 PASS / CLOSED approval.
