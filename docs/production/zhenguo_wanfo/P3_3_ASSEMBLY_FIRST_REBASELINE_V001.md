# P3.3｜Assembly-First Rebaseline V0.1

- Decision: **D-286**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Goal: **把已经建立的构件正确组合起来，搭起万佛殿**

## 1. Controlling rule

From this point onward, P3.3 is **assembly-first**.

A question is worked only when it blocks one of:

1. **where the component goes**;
2. **how it is oriented**;
3. **how its required length / scale is determined**;
4. **what supports / receives it enough to place it correctly**;
5. **what visible geometry is required to generate it**.

If none of those are blocked, the issue does not stop assembly.

## 2. What is retained

- 25 approved Master families / D-271;
- current Component Instance Registry;
- D-284 Structural Timber Scope Register;
- D-277 / D-279 connection records where directly useful;
- same-building measured report and locked source bindings.

## 3. What is no longer a prerequisite

The following are **not required before building starts**:

- whole-building atomic connection closure;
- a complete connection ontology;
- exact hidden mortise / tenon / groove reconstruction;
- closure of every D-285 parent obligation.

D-285 is retained only as **reference / diagnostic material**.

## 4. Blocker rule

### BLOCKING
- location unresolved;
- orientation unresolved;
- required length / scale unresolved;
- support/counterpart unresolved in a way that prevents placement;
- required visible geometry missing;
- direct evidence contradiction.

### NON-BLOCKING
- hidden joinery detail unknown but placement is deterministic;
- hidden groove / tenon dimensions unknown and invisible in the assembled form;
- an unrelated OUT-scope building system is unresolved;
- the global connection matrix is incomplete.

## 5. Execution flow

**Component → instance position → minimal assembly rule → first assembly → validate → repeat → whole hall**

No extra theory layer is inserted unless assembly actually fails.

## 6. Next controlled task

**AF-01｜正身梁架首榀｜Assembly Spec V0.1**

Purpose:
- select one real representative main-frame slice;
- identify its actual Registry instances;
- resolve placement / orientation / required generated lengths;
- define the minimum deterministic assembly rule.

AF-01 does **not** begin engineering generation until separately authorized.

## 7. Governance

- D-284 Scope remains locked.
- D-285 Matrix becomes **REFERENCE / NON-BLOCKING**.
- PR #49 / D-280 is **not the next step** and remains HOLD.
- T-018 remains HOLD.
- Whole-building generation remains unauthorized until representative assembly is validated.
