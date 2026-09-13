# P3.1 Gate Review｜Component Master & Variant Library｜2026-09-13

Status: **PASS / APPROVED / CLOSED / D-040**  
Phase: `P3｜古建筑构件系统化与组合建模`  
Gate: `P3.1｜Component Master & Variant Library`  
Authoritative DoD: `docs/production/zhenguo_wanfo/P3_1_DEFINITION_OF_DONE_V001.md` / D-032  
Review basis: T-010 / T-011 / T-012 / T-013 / T-014 approved outputs through D-040

## 1. Executive Conclusion

P3.1 已完成最终 Gate Review，并由 Product Owner 明确批准：

> `P3.1｜Component Master & Variant Library｜PASS / APPROVED / CLOSED`

最终 Gate Score：**9 / 9 PASS**。

当前证据版本下：

- `MASTER_REQUIRED = 6`，6/6 canonical Masters 已批准；
- formal registered variants = **0**，且这不是缺失生产，而是当前没有 evidence-qualified 的 within-Master historical variant；
- Proxy / Control / Envelope / Deferred 对象继续保持非历史化边界；
- P2 frozen baseline 未被覆盖；
- T-014 已补齐 whole-library Overview，DoD-07 关闭；
- Product Owner 最终批准使 DoD-09 关闭；
- P3.2 `Assembly Relationship Model` 正式解锁，但在其 Definition of Done 被批准前不得创建工程任务。

P3.1 PASS 不代表万佛殿全部历史构件已经复原，只代表在当前正式证据边界内，所有有资格进入本版本构件库的对象已经得到一致、可复用、可验证的 Master / Variant 处理。

---

## 2. DoD Review｜9 / 9 PASS

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

Conclusion: **PASS**.

### DoD-02｜Evidence-backed Component Identity Resolution — PASS

- `BRACKET_ARM` aggregate remains proxy where individual 栱/昂 cannot be evidenced.
- `BRACKET_CONTACT` is not silently reinterpreted as 小斗; DG-114 remains UNKNOWN.
- P2 `PRIMARY_FRAME` aggregate is not reused as historical geometry; lower / upper six-chuanfu are separately evidence-qualified components.
- Purlin / rafter / bottom dou and other named members remain Deferred where geometry evidence is insufficient.
- No `EVIDENCE_REVIEW_BEFORE_MASTER` record remains unresolved.

Conclusion: **PASS**.

### DoD-03｜Canonical Component Master Asset Contract — PASS

Authoritative contract:

- `docs/production/zhenguo_wanfo/P3_1_MASTER_ASSET_CONTRACT_V002.md`
- `production/zhenguo_wanfo/registry/P3_1_MASTER_ASSET_CONTRACT_V002.json`
- approval: D-036

V002 covers all 6 Masters and locks unit / local axes / origin / transform / geometry LOD / parameter contract / evidence boundary / variant axes / placement-only distinction / prohibited geometry / review / reproducibility requirements.

Conclusion: **PASS**.

### DoD-04｜Canonical 3D Master Production — PASS

Approved Master coverage = **6/6 / 100%**:

1. `CMP-COLUMN-001｜柱` — D-035
2. `CMP-LUDOU-COLUMN-001｜柱头栌斗` — D-037
3. `CMP-DOU-SINGLE-LONGKAI-001｜单向长开斗` — D-037
4. `CMP-DOU-INTERACTIVE-001｜交互斗` — D-037
5. `CMP-FRAME-LOWER-SIX-CHUANFU-001｜下六椽栿` — D-039
6. `CMP-FRAME-UPPER-SIX-CHUANFU-001｜上六椽栿` — D-039

`CONTROL_ONLY / ENVELOPE_ONLY` historical Master count = 0; unresolved proxies are not promoted.

Conclusion: **PASS**.

### DoD-05｜Parameterized Variant Model — PASS

Current formal registered variants = **0**.

This is accepted because current evidence does not establish a qualified within-Master historical variant requiring registration:

- column observed/report/reconstructed values remain evidence-layer alternatives, not automatically distinct historical variants;
- three dou identities are distinct component types, not variants of one generic dou;
- lower / upper six-chuanfu are distinct component identities / structural roles, not variants of one generic beam;
- placement rotation / instance number does not create variants.

Parameterized behavior is proven by mutation / rebuild testing for column, dou and six-chuanfu families. Future evidence-qualified variants must obtain stable variant IDs under Contract V002 before production use.

Conclusion: **PASS / ZERO FORMAL VARIANTS IN CURRENT EVIDENCE VERSION**.

### DoD-06｜Evidence-aware Geometry & Replaceability — PASS

Boundaries retained:

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`
- `Z-006-RC-01` remains separate / replaceable
- `DG-114` remains UNKNOWN and unused as unified small-dou specification
- `HIS-002` originality remains unknown
- unsupported 45° corner / joinery / hidden-angle geometry is not promoted
- observed / report-ideal / reconstructed candidate layers remain separate
- six-chuanfu 1000 mm reference length remains explicitly non-historical / replaceable and must not leak into assembly

Conclusion: **PASS**.

### DoD-07｜Standard Component Review Package — PASS

Individual approved review coverage:

- Column: 6/6 PASS
- Dou Masters: 18/18 individual PASS
- Six-chuanfu Masters: 12/12 individual PASS
- Total individual Master review set = **36/36 PASS**

Batch overviews:

- Dou batch overview: PASS
- Six-chuanfu batch overview: PASS

T-014 closure artifact:

- `production/zhenguo_wanfo/review/P3_1/P3_1_MASTER_LIBRARY_OVERVIEW_V001.png`
- final SHA256: `4719a31c18de13b0453a64d29847381d8e45af0f145bcb37bf7fee0abf9671a7`
- validation: `production/zhenguo_wanfo/validation/P3_1_MASTER_LIBRARY_OVERVIEW_VALIDATION_V001.json`
- source components: 6/6
- formal variants shown: 0
- canonical Masters unchanged: YES
- existing individual review assets unchanged: YES
- P2 frozen baseline unchanged: YES
- P3.2 files created: NO

The six panels also show the project formal Chinese component names: 柱、柱头栌斗、单向长开斗、交互斗、下六椽栿、上六椽栿. Naming basis is `SRC-ZG-WF-001` precision survey report / project canonical naming; the overview does not claim these labels are “宋代原称” or “古籍原称”.

Visual review final result: **PASS**.

Conclusion: **PASS**.

### DoD-08｜Library Registration, Machine Validation & Reproducibility — PASS

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

Conclusion: **PASS**.

### DoD-09｜Product Owner Review + Canonical Archive + P3.2 Readiness — PASS

Product Owner explicitly approved on 2026-09-13:

> `P3.1｜Component Master & Variant Library｜PASS / APPROVED / CLOSED`

Decision: **D-040**.

P3.2 readiness answer:

**Approved P3.2 component nodes**

- 柱
- 柱头栌斗
- 单向长开斗
- 交互斗
- 下六椽栿
- 上六椽栿

**Current formal variants**

- 0 registered evidence-qualified variants in this P3.1 version.
- Parametric axes remain available under V002; future evidence can create registered variants.

**Objects remaining non-historicized**

- Proxy: 4
- Control: 3
- Envelope: 1
- Deferred insufficient evidence: 13

**Assembly carry-forward boundaries**

- six-chuanfu canonical 1000 mm reference length must not enter building assembly implicitly;
- column RC height remains replaceable / not historical fact;
- DG-114 / HIS-002 / corner / joinery boundaries remain active;
- `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY` remains a Hard Fail for later assembly work.

Conclusion: **PASS**.

---

## 3. Final Gate PASS Condition Matrix

| Condition | Final Status |
|---|---|
| DoD 9/9 | **PASS** |
| Scope Matrix coverage | PASS / 100% |
| MASTER_REQUIRED coverage | PASS / 6 of 6 / 100% |
| EVIDENCE_REVIEW_BEFORE_MASTER unresolved | PASS / 0 |
| CONTROL / ENVELOPE historicized incorrectly | PASS / 0 |
| orphan Master / Variant | PASS / 0 |
| evidence traceability | PASS |
| mutation / replaceability | PASS |
| reproducibility / independent reopen | PASS |
| P2 frozen baseline unchanged | PASS |
| Product Owner final Gate approval | **PASS / D-040** |

## 4. Final Gate Decision

**P3.1｜Component Master & Variant Library = PASS / APPROVED / CLOSED / D-040.**

P3 Gate progress becomes **2 / 4**.

P3.2 `Assembly Relationship Model` is now **UNLOCKED / ENTERED**. Before any P3.2 engineering task is created, its Definition of Done must be defined and explicitly approved by the Product Owner.
