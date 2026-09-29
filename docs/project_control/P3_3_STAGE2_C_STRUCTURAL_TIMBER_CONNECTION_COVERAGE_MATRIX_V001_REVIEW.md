# P3.3 Stage2-C｜Structural Timber Connection Coverage Matrix
## Rebaseline / Patch 01 Review

- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Decision: **D-285**
- Scope authority: **D-284**

## Machine audit
- Structural Timber denominator: **33**
- Parent coverage: **33 / 33**
- Uncovered scope objects: **0**
- Parent obligations: **42**
- New rebaseline obligations: **3**
- Atomic/handoff inventory: **18**
- Locked atomic segments: **6**
- D-277/D-279 referenced records verified: **5/5**
- Parent-only objects requiring later atomic expansion: **15**
- Matrix lock allowed: **NO**

## Structural corrections achieved
1. D-284's 33-object Structural Timber Scope is the only denominator.
2. The original 39 rows are parent obligations, not 39 completed edges.
3. 襻间枋 and 隐角梁 now have explicit coverage obligations.
4. Lower foundation STOP handoff is explicit.
5. Concrete edge candidates are separated from aggregate topology tasks.
6. D-277/D-279 records are inherited without rewriting.

## Remaining before lock
Atomic expansion remains required for puzuo internal topology, primary-frame counterpart paths, ridge support, Dingfu/Rufu/Zhaqian, full purlin supporter map, hidden corner beam, and roof timber handoffs.

## Decision requested
Review this rebaseline structure. Approval would approve the matrix architecture only, not close all open edges.
