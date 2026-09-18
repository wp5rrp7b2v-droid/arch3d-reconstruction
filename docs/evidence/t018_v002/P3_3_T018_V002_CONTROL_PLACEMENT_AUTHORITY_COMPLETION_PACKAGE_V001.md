# T-018 V002｜Control Placement Authority Completion Package V001

## Status
DESIGN COMPLETE / PRODUCT OWNER DECISION REQUIRED / IMPLEMENTATION FROZEN

- Design authorization：D-062
- Date：2026-09-18
- Outcome from Architecture Closure Review：B｜有限同类缺口
- No Rule created by this package
- No upstream artifact modified
- No CP-03 restart
- No Blender / Actions
- PR #6 untouched

## 1. Package contents

1. `P3_3_T018_V002_PLACEMENT_AUTHORITY_CLOSURE_MATRIX_V001.md`
2. `P3_3_T018_V002_CROSS_SYSTEM_DEPENDENCY_DAG_V001.md`
3. `P3_3_T018_V002_CONTROL_TOPOLOGY_MAP_V001.md`
4. `P3_3_T018_V002_IMPACT_NON_IMPACT_CONTRACT_V001.md`

## 2. Final closure finding

The review no longer supports “one missing Frame Tier rule only”, but it also does not support a broad redesign.

The gaps are finite and concentrated at one seam:
`canonical parameters / P3.2 semantics → whole-building control placement/topology`.

After the four closure specifications, the remaining work separates into four modules:

| Module | Needs new authority? | Needs new historical dimension? | Scope |
|---|---|---|---|
| RZ｜Roof Z cumulative closure | **YES, explicit formula authority/companion required** | NO | roof Z only |
| FV｜Frame vertical placement bridge | **YES, bounded project engineering bridge required** | NO | Frame Control only |
| RT｜Control topology map | NO; machine specification | NO | rafter/envelope/gable/frame-support topology |
| BA｜Technical anchors | NO; non-historical representation contract | NO | bracket/primary-frame technical anchors |

Therefore **only two authority completions are potentially required**, not four.

## 3. RZ｜Roof Z cumulative closure

Existing authority already supplies all values:
- Z-007
- Z-006-RC-01
- ROOF-007/008/009
- MOD-002
- T-020 shared-ridge topology

No new dimension is needed.

The missing piece is an explicit machine-authoritative cumulative formula. The bounded formula envelope is:

- eave Z0 = Z datum + approved column-height rule
- Z1 = Z0 + ROOF-007*MOD-002
- Z2 = Z1 + ROOF-008*MOD-002
- ridge Z3 = Z2 + ROOF-009*MOD-002

DG-113 is excluded.

Candidate audit values:
3534.3 → 4880.7 → 5814.0 → 7068.6 mm.

This completion must not change T-020 Y coordinates or ridge identity.

## 4. FV｜Frame vertical placement bridge

This is the only materially new authority decision.

Current evidence:
- FR-004/005/006 already legitimately define Frame Y/depth stations.
- P3.2 defines LOWER/UPPER Frame Tier as semantic engineering datums but explicitly gives no historical elevation.
- ROOF-004/005/006 are formal reconstructed-design candidates for roof/purlin Z control, not currently Frame-owned.
- DG-113 is a formal reconstructed-design lower-ang rise candidate owned by the Bracket system.
- legacy P2 combined DG-113 + ROOF-004/005/006 to place frame tiers, but that combination was implementation logic, not an authorized cross-system P3.3 rule.

Additional source review confirms:
- ROOF-004/005/006 are high-confidence inferred design candidates for 槫间高差, not direct 963 records;
- DG-113 is high-confidence inferred lower-ang rise, not direct 963 record;
- both are replaceable reconstructed-design candidates.

Thus a Frame vertical completion **can remain Outcome B only if** it is formalized as:
- PROJECT_RULE / engineering placement only;
- historical_claim=false;
- replaceable=true;
- one-way dependency;
- allowed output limited to FRAME_CONTROL / FRAME_SUPPORT technical placement;
- no effect on Roof authority;
- no claim that the resulting exact tier elevations are proven 963 historical elevations.

The exact formula must be separately approved before it becomes authority. The legacy P2 formula may be used as a candidate for evaluation, never as automatic authority.

## 5. RT｜Control topology

No new authority values are needed.

The topology map already closes:
- N00→N01→N02→N03
- S00→S01→S02→N03
- all 36 rafter adjacent-control pairs
- all 6 roof envelope intervals
- all 4 gable polylines
- 1:1 FRAME_CONTROL ↔ FRAME_SUPPORT pairing

This should become a machine-readable topology artifact before CP-03 restarts.

## 6. BA｜Technical anchors

No historical placement rule is needed for UNKNOWN/Proxy representation.

Allowed:
- bracket technical markers anchored from grid/column engineering datums;
- primary-frame UNKNOWN markers anchored to organizational grid/frame axes.

Prohibited:
- using these markers to drive Frame/Roof placement;
- upgrading them to historical geometry.

This can be implemented later under Stage C, but its contract is now known and should not create a new architecture surprise.

## 7. Minimum correction architecture

If Product Owner approves future correction, the smallest safe package is:

### Authority layer
A bounded project-level completion set with at most:
1. **Roof Z Closure authority**
2. **Frame Vertical Placement authority**

### Technical specification layer
3. Control Topology Map
4. Impact / Non-Impact Contract
5. Technical Anchor Contract for Stage C

This does **not** require:
- reopening P3.0;
- reopening P3.1;
- reopening P3.2;
- changing 365 accounting;
- changing PURLIN disposition;
- changing T-020 X/Y shared-ridge topology;
- creating new historical dimensions;
- V003 at this time.

## 8. Required pre-implementation decision

Before any correction is created, Product Owner must separately approve:

1. whether to formalize the two bounded authority completions;
2. for Frame Vertical, the exact engineering formula and allowed input set;
3. whether these completions live in one minimal upstream correction task/package or another explicitly governed vehicle.

Until that approval:
- implementation remains frozen;
- CP-03 remains stopped;
- PR #6 remains HOLD;
- no Rule is created.

## 9. Escalation trigger

Outcome B remains valid only if the exact Frame Vertical formula can be expressed using existing reconstructed-design candidates without:
- new historical dimension;
- P2 world transform;
- P3.2 vocabulary change;
- identity change;
- circular dependency.

If not, STOP and reclassify Outcome C before any implementation.
