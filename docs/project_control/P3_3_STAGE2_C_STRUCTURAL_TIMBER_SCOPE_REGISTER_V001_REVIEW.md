# P3.3 Stage2-C｜Structural Timber Scope Register V0.1 Review

- Status: **APPROVED / LOCKED D-284**
- Decision: **D-283**

## Machine checks

- V008 object types classified: **66 / 66**
- Duplicate object types: **0**
- IN: **33**
- OUT: **27**
- CONTAINER: **5**
- CONDITIONAL: **1**
- Master-bound object types in IN: **28 / 28**
- Approved Master families represented: **25**
- Non-Master IN: **椽系 / 襻间枋 / 望板系统 / 隐角梁 / 散斗族**
- CONDITIONAL: **替木实体族**
- Engineering authorized: **NO**
- Stage3 authorized: **NO**
- Batch03 resumed: **NO**

## Evidence-specific notes

- 襻间枋: current Registry has 12 located records under upper/lower purlins → candidate **IN**.
- 隐角梁: current Registry has four corner instances with direct measurement/report evidence → candidate **IN**.
- 散斗族: locked D-277 requires its connector role → candidate **IN**.
- 替木实体族: physical existence is acknowledged, but independent Stage2-C connection role is not yet closed → candidate **CONDITIONAL**.

## Lock gate

Before this register can be locked:
1. Product Owner must approve the scope definition and stop boundaries.
2. 替木实体族 must receive a final IN or OUT decision, or an explicit rule allowing CONDITIONAL to remain outside the denominator until promoted.
3. The Connection Matrix must remain unchanged until scope lock.

## Decision requested

Approve / revise the Structural Timber Scope Register V0.1.


## D-284 Product Owner Decision

**APPROVED / LOCKED**

Accepted exactly as:
- 33 IN
- 27 OUT
- 5 CONTAINER
- 1 CONDITIONAL

Special rule:
- `替木实体族` remains CONDITIONAL and **does not enter the current Connection Matrix denominator**.
- Promotion requires separate evidence review + Product Owner approval.
- If promoted later, the Connection Matrix must be patched before Stage2-C closure.

Next controlled step is **Connection Coverage Matrix Rebaseline / Patch 01 against the locked 33-object Structural Timber Scope**. That step is not authorized by this lock.
