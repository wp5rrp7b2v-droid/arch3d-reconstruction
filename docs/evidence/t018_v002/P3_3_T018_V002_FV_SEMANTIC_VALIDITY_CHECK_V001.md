# T-018 V002｜FV Semantic Validity Check V001

## Status

**COMPLETE / FV-B SOURCE-SEMANTIC SUPPORT INSUFFICIENT / DO NOT LOCK YET**

- Date：2026-09-18
- Scope：only assess whether ROOF-004/005/006 → Frame Tier cumulative Z mapping is supported by source semantics
- No Rule created
- No upstream modification
- RZ D-063 remains locked
- CP-03 remains STOP
- PR #6 remains HOLD

---

## 1. Question

Does current evidence support this mapping as more than a project convention?

```
FRAME_BASE_Z = Z-007 + Z-006-RC-01
TIER_01 = FRAME_BASE_Z + (ROOF-004 + ROOF-005 + ROOF-006) * MOD-002
TIER_02 = FRAME_BASE_Z + (ROOF-004 + ROOF-005) * MOD-002
TIER_03 = FRAME_BASE_Z + ROOF-004 * MOD-002
```

The check deliberately excludes whether the formula is numerically stable or visually plausible.
It asks only whether the **semantic correspondence** is supported.

---

## 2. Direct-source finding

Primary direct review of SRC-ZG-WF-001 records:

- ROOF-001/002/003 = measured purlin-to-purlin rise intervals A/B/C;
- ROOF-004/005/006 = report-normalized design candidates 25 / 40 / 82 fen;
- these belong to section **举折 / 屋架垂直几何**;
- after accounting for 替木, the report separately derives ROOF-007/008/009 as:
  - eave → lower purlin = 88 fen
  - lower → upper purlin = 61 fen
  - upper → ridge purlin = 82 fen.

The direct review does **not** state that ROOF-004/005/006 are Frame Tier elevations or Frame-control rises.

It also does not establish:
- Tier 01 ↔ cumulative A+B+C;
- Tier 02 ↔ cumulative A+B;
- Tier 03 ↔ A.

Therefore the exact FV-B mapping is **not directly source-supported**.

---

## 3. P1/P2 semantic classification

P1.2/P1.3 classifies ROOF-004/005/006 as:

- HIGH_CONFIDENCE_INFERENCE;
- reconstructed_design_candidate;
- REPORT_INFERRED;
- `DEFAULT_DESIGN_LOGIC`;
- semantic domain: **举折 / Z向屋架 / 槫间高差**.

This supports using them as roof-elevation design candidates.

It does not independently support reinterpreting them as Frame Tier values.

---

## 4. P3.1 finding

P3.1 `CTL-FRAME-001` is:

- `CONTROL_ONLY`;
- not a historical component;
- source context = 梁架控制坐标;
- source pages = **none directly established**.

P3.1 lists ROOF-004/005/006 among `known_geometry_inputs`, but explicitly describes these as:

> P2 engineering parameter IDs; not direct member geometry.

This list is inherited engineering provenance from P2.
It is **not an independent historical/source semantic proof** that the cumulative mapping is correct.

Using the P3.1 list to justify the same P2 formula would be circular provenance:
`P2 implementation → P3.1 inherited input list → justify P2-style implementation`.

That is not sufficient for FV authority closure.

---

## 5. P3.2 finding

P3.2 Unit B explicitly states:

- `CTL-FRAME-001__LOWER-TIER-DATUM`
- `CTL-FRAME-001__UPPER-TIER-DATUM`

are semantic engineering tier controls only.

The design explicitly says:

> used to distinguish lower/upper frame engineering tier; **does not create a concrete historical elevation**.

Therefore P3.2 validates:
- tier semantics;
- LOCATE relationship;
- non-historical control identity.

It does **not** validate:
- an exact Z formula;
- a mapping from ROOF-004/005/006 to three whole-building Frame tiers.

---

## 6. Legacy P2 finding

Legacy P2 generator used ROOF-004/005/006 cumulatively for `frame_tier_z`.

That proves only:

- the old model had a deterministic engineering convention;
- the convention produced a coherent skeleton.

It does not prove:

- the report prescribed that mapping;
- the mapping is historically correct;
- the mapping was separately authorized as a cross-system project rule.

Therefore legacy P2 remains diagnostic, not authority.

---

## 7. Semantic validity verdict

### FV-B as historical/source-derived rule

**FAIL / NOT SUPPORTED**

There is insufficient evidence to say:

> ROOF-004/005/006 are source-validated Frame Tier vertical intervals.

### FV-B as explicit project reconstruction convention

**POSSIBLE, BUT REQUIRES A NEW POLICY DECISION**

It could be adopted only if explicitly classified as:

- PROJECT_RULE;
- project reconstruction convention;
- historical_claim=false;
- replaceable=true;
- not source-derived Frame geometry;
- one-way Roof-candidate → Frame-control bridge;
- exact affected set bounded by the FV impact contract.

This would be an engineering convention created by the project, not recovered historical geometry.

---

## 8. Risk if FV-B is locked without this distinction

1. **Semantic laundering**
   - roof/purlin design values would silently become Frame authority.

2. **Circular provenance**
   - old P2 implementation would justify P3.1 input listing, which then justifies the old P2 formula.

3. **False precision**
   - 3916.8 / 4528.8 / 5783.4 mm could look like source-backed frame elevations.

4. **Future coupling**
   - replacement of a roof design candidate would move Frame tiers even though the historical linkage is not proven.

5. **Governance regression**
   - contradicts V002 principle that “computable” does not equal “authorized”.

---

## 9. Recommended disposition

**Do not lock FV-B in its current wording.**

Keep:
- FV-B mathematical candidate;
- DG-113 exclusion;
- impact/non-impact boundary;
- RZ dependency direction.

Change the decision question from:

> “Is FV-B the recovered Frame vertical rule?”

to:

> “Do we explicitly approve FV-B as a non-historical project reconstruction convention for CONTROL_ONLY geometry?”

If the Product Owner does not want a synthetic project convention, the safer alternative is to keep exact Frame Tier Z unresolved and revise CP-03 representation/acceptance for that family rather than invent source authority.

---

## 10. Current architecture classification

Outcome B is **not automatically escalated to C**.

Reason:
- identity / P3.1 / P3.2 / RZ / accounting remain intact;
- the unresolved issue is still bounded to one control-placement policy decision.

However CP-03 remains blocked until one of two bounded paths is chosen:

### Path FV-PROJECT-RULE
Explicitly approve a non-historical engineering convention.

### Path FV-SEMANTIC-ONLY
Do not assign exact tier Z; amend T-018 CP-03 scope/representation accordingly.

No third hidden formula path is allowed.
