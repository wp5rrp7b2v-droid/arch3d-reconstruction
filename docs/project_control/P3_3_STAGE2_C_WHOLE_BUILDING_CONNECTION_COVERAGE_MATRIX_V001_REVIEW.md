# P3.3 Stage2-C｜Whole-Building Connection Coverage Matrix V0.1 Review

- Status: **REVIEW COMPLETE / PATCH 01 REQUIRED / D-282 / NOT LOCKABLE**
- Decision: **D-281**
- Source main: `447f887fbb0f4b28d62d957dacf65276b85c0461`

## Machine checks
- Approved Master families: **25**
- Covered Master families: **25/25**
- Missing Master families: **0**
- Connection obligations: **39**
- ATTACHMENT_CLASS: **10**
- TOPOLOGY_RESOLUTION: **25**
- SYSTEM_HANDOFF: **4**
- Locked obligations inherited from D-277/D-279: **5**
- Duplicate requirement IDs: **0**
- World-coordinate authority introduced: **NO**
- Engineering execution: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Review focus
1. Any missing family-level physical connection domain?
2. Any row that is only adjacency and should be removed?
3. Any source-supported participant pair missing from the matrix?
4. Does every topology obligation force a deterministic resolver rather than a permanent UNKNOWN?
5. Are puzuo-internal obligations bounded enough before exact dou-role extraction?

## Decision requested
Approve or revise the matrix. Do not resume Batch 03 lock before this matrix is accepted.


## D-282 Review Result

**Result: PATCH REQUIRED. Do not lock V0.1 yet.**

### Finding F-01｜Coverage denominator is too narrow

The candidate proves **25/25 approved Master-family participation**, but Stage2-A's locked universe is **66 V008 object types**:

- MASTER_BOUND_PRODUCTION: 28 object types
- PARAMETRIC_SYSTEM_OR_COMPLETION: 23
- TOPOLOGY_OR_ASSEMBLY_CONTAINER: 5
- SIMPLIFIED_PROXY: 7
- REFERENCE_ONLY_UNKNOWN: 3

Among the non-Master rows, **30 object types** carry `REQUIRED_IF_ATTACHED_TO_OTHER_PRODUCTION_ENTITY` or `EXPLICIT_CONNECTION_REQUIRED_IF_ATTACHED`.

Therefore 25/25 Master coverage is necessary but **not sufficient** for a Whole-Building connection claim.

### Finding F-02｜39 obligations are not yet 39 atomic physical edges

Candidate V0.1 contains:

- **12** rows that already name concrete Master↔Master / Master→connector→Master participants;
- **27** rows that still contain an assembly role, member set, system role or unresolved counterpart role.

Those 27 rows are valid topology-resolution tasks, but they are **parent coverage obligations**, not a final complete edge inventory.

Examples include:
- column-head / infill puzuo root component sets;
- huagong / dou / gong / Ang stacked topology groups;
- all-purlin supporter map;
- ridge-support counterpart roles;
- roof/system handoffs.

Before lock, each aggregate row must either:
1. expand into a complete set of atomic child edges;
2. resolve to `EXPLICIT_NO_DIRECT_ATTACHMENT` with the actual intermediate path; or
3. become a locked system handoff contract.

### Finding F-03｜Whole-building system handoffs are incomplete

The current candidate includes roof handoffs, but it does not yet systematically disposition all Stage2-A non-Master production objects that may physically attach to the structural network.

Review Patch 01 must therefore add a **V008-wide attachment disposition table** before calling the matrix Whole-Building complete.

### Source review

The source pages reviewed during this audit include:
- puzuo relationship / layer drawings around PDF pp58–65;
- frame and roof-frame relation drawings around PDF pp88–94;
- ideal-model / layered structural reading around PDF pp106–114 of the loaded extract.

These drawings support using topology extraction to derive real connection edges; they do not justify treating an unresolved role-set row as a completed physical connection.

## Review Patch 01 acceptance gate

Patch 01 must pass all of the following before a lock decision:

1. **66/66 V008 object types receive an attachment disposition.**
2. 5 topology/container objects remain organizational unless evidence says otherwise.
3. 3 REFERENCE_ONLY_UNKNOWN objects remain outside production unless explicitly promoted.
4. All 30 non-Master objects with an "if attached" requirement are explicitly classified as attached or not attached.
5. Every attached non-Master object gets an explicit edge/handoff obligation.
6. Every aggregate Stage2-C parent row has a complete child-edge inventory or explicit no-direct-attachment disposition.
7. The 5 D-277/D-279 locked records remain unchanged.
8. Graph closure check returns **no unexplained open structural node**.
9. PR #49 remains HOLD.
10. PR #50 remains Draft until Patch 01 passes.

