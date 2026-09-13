# P3.1｜T-010 Scope / Identity Review｜2026-09-13

Status: **TECHNICAL REVIEW PASS / PRODUCT OWNER APPROVAL REQUIRED**

Task: `T-010｜P3_1_COMPONENT_MASTER_SCOPE_IDENTITY_V001｜构件Master资格矩阵与证据身份解析`
Engineering commit: `774a1469416d49268997d20970c71bb9357849aa`

## 1. Technical Review Result

T-010 engineering execution is accepted as technically complete.

- P3.0 Registry coverage: **11 / 11**
- P1 minimum scope coverage: **9 / 9**
- Total review records: **27**
- Eligibility decision coverage: **100%**
- Unexplained pending: **0**
- Evidence provenance: **PASS**
- Historical boundary preservation: **PASS**
- Determinism: **PASS**
- P2 frozen baseline: **PASS**
- Negative mutation probes: **5 / 5 REJECTED**
- Project Control conflict requiring adjudication: **none identified**

No Blender Component Master or Variant geometry was created in T-010.

## 2. Eligibility Result

Final counts:

- `MASTER_REQUIRED`: **6**
- `EVIDENCE_REVIEW_BEFORE_MASTER`: **0**
- `PROXY_ONLY`: **4**
- `CONTROL_ONLY`: **3**
- `ENVELOPE_ONLY`: **1**
- `DEFERRED_INSUFFICIENT_EVIDENCE`: **13**

### MASTER_REQUIRED｜6

1. `CMP-COLUMN-001`｜柱
2. `CMP-LUDOU-COLUMN-001`｜柱头栌斗
3. `CMP-DOU-SINGLE-LONGKAI-001`｜单向长开斗
4. `CMP-DOU-INTERACTIVE-001`｜交互斗
5. `CMP-FRAME-LOWER-SIX-CHUANFU-001`｜下六椽栿
6. `CMP-FRAME-UPPER-SIX-CHUANFU-001`｜上六椽栿

These six objects meet the current P3.1 threshold for later Master Asset Contract work, but this does **not** mean exact 963 geometry is proven.

## 3. Review of the Six MASTER_REQUIRED Decisions

### 柱

PASS. Historical component identity and observed diameter are supported. `Z-006` remains `UNKNOWN / null / DO_NOT_LOCK`; later Master must treat height as an explicit parameter. `Z-006-RC-01` remains a separate replaceable reconstruction candidate and must not be written back as historical truth.

### 柱头栌斗

PASS. Direct measured width/depth/height evidence supports an evidence-bounded Master. Exact cavity, ear/profile and mortise geometry remain outside the supported precision boundary.

### 单向长开斗

PASS. Direct measured width/depth/height evidence supports a distinct orientation-specific Master. Placement rotation is not a new historical type or Variant by itself.

### 交互斗

PASS. Direct measured width/depth/height evidence supports an independent Master. This does not revive or resolve `DG-114`; there is still no unified historical small-dou specification claim.

### 下六椽栿

PASS. Independent component identity and directly observed section dimensions support a bounded parametric Master. Full member length, camber, end profile and exact joinery remain unresolved and must stay parameterized/bounded.

### 上六椽栿

PASS. Same conclusion as lower six-chuanfu, with its own distinct measured section. P2 aggregate `PRIMARY_FRAME` meshes are not inherited as historical Master geometry.

## 4. Deferred / Excluded Decisions

The conservative decisions are accepted.

- `底斗`: deferred because approved direct review lacks sufficient depth information for a qualified 3D Master; `DG-114` cannot fill the gap.
- `槫类`: real historical type, but member-specific sections, lengths and end conditions are not sufficiently established.
- `椽类`: real historical type, but measured sections, lengths, spacing and eave/flying-rafter distinctions are insufficient.
- named 栱/昂, 四椽栿, 平梁, 托脚, 阑额, 补间坐斗: retained as deferred until attributable member-level geometry evidence is available.
- P3.0 `BRACKET_ARM / BRACKET_CONTACT / PRIMARY_FRAME / FRAME_SUPPORT`: correctly remain proxies rather than being silently historicized.
- `FRAME_CONTROL / GABLE_CONTROL / GRID_CONTROL`: correctly remain controls.
- `ROOF_ENVELOPE`: correctly remains envelope-only.

## 5. Historical Boundaries Preserved

PASS:

- `Z-006 = UNKNOWN / null / DO_NOT_LOCK`
- `Z-006-RC-01 = REASONABLE_COMPLETION / replaceable / D-023`
- `DG-114 = UNKNOWN / DO_NOT_LOCK`
- `HIS-002 = component originality unknown`
- 45° corner / mortise / hidden-angle-beam precision unresolved
- observed / report ideal / reconstructed candidate layers remain separate
- P2 365 placements are not interpreted as historical component inventory

## 6. Technical Conclusion

**T-010｜ENGINEERING PASS / COMPLETE**

The Scope Matrix and Identity Resolution are technically sound and conservative enough to become the P3.1 production qualification baseline.

However, per the locked P3.1 DoD and T-010 contract, this review does not itself authorize Component Master geometry.

## 7. Product Owner Decision Required

Product Owner should approve or reject the qualification baseline:

> `T-010 Scope Matrix & Identity Resolution｜APPROVED`

If approved, the six `MASTER_REQUIRED` records become the locked current Master-production scope for P3.1. The next task should establish the **Canonical Master Asset Contract** for those six records before batch Blender geometry production.
