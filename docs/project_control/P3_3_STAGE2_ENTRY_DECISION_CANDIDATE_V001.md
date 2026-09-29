# P3.3 Stage2 Entry Decision｜Candidate V0.1

- Project: ARCH3D-001｜中国古建筑3D复原
- Case: 平遥镇国寺万佛殿
- Gate: P3.3 V002
- Candidate status: **PRODUCT OWNER REVIEW REQUIRED**
- Canonical main reviewed: `8789f7b0aa796e76ed0a75be8703245e82193e1b`
- Stage 1 authority: **CLOSED / D-271**
- Stage 2 current authority: **NOT AUTHORIZED**
- T-018: **HOLD**
- This candidate does not itself authorize Stage 2.

## 1. Entry readiness conclusion

**READY_TO_ENTER_STAGE2_DESIGN_WITH_CONTROLLED_REBASELINE**

Recommended Product Owner decision:

> Authorize P3.3 Stage 2 **design / inventory / rebinding work only**.
> Do not yet authorize Stage2 Blender engineering execution, a new engineering T-task, whole-building topology generation, or T-018 restart.

## 2. Why Stage 2 may now start

Prerequisites are satisfied:

1. Stage 1 is formally CLOSED under D-271.
2. Stage1 Master scope is 28/28 object types = 100%.
3. 25 approved Master families are canonical and Registry-bound.
4. V008/CURRENT remains the canonical real-component baseline.
5. P3.2 relationship semantics already exist and remain reusable:
   - SUPPORT
   - CONNECT
   - LOCATE
   - REPEAT
   - BELONG
6. RC-024 Connection Layer rule is LOCKED / ACTIVE.
7. T-031 proved deterministic automatic two-Master placement/mutation.
8. T-032 proved complete assembly requires an explicit Connection Layer and passed the connection-aware proof.
9. No active engineering T-task or Stage1 blocker remains.

## 3. Why P3.2 cannot be reused as current Stage2 production data

P3.2 is a reusable mechanism baseline, not the current P3.3 real-component assembly truth.

Current factual gap:

- Stage1 approved Master families: **25**
- P3.2 Interface Registry owners: **6**
- P3.2 Interface Registry interfaces: **18**
- Current P3.2 representative relationship graph directly represents only **4 / 25** current approved Master references.
- P3.2 graph still contains CONTROL / PROXY constructs designed before the V008 real-component rebaseline.
- P3.3 Connection Layer schema remains **PROOF_BOUND**, not yet promoted as a complete production registry.

Therefore Stage2 must **retain semantics but rebind production data**.

## 4. Locked inheritance / rebaseline policy

### RETAIN

- P3.2 five relationship types and semantic distinctions.
- MASTER_LOCAL interface coordinate principle.
- world coordinates as derived output only.
- manual Blender placement is not canonical.
- RC-024 Connection Layer kinds:
  - PHYSICAL_CONNECTOR
  - JOINERY_FEATURE
  - CONTACT_INTERFACE
- RC-020 + RC-023 evidence rules.
- T-031 deterministic placement proof as engineering precedent.
- T-032 connection-aware complete assembly proof as engineering precedent.

### REBIND / REBUILD FOR STAGE2

- interface ownership against current 25 approved Master families;
- variant rules;
- orientation rules;
- start/end/support interfaces;
- length-determination rules;
- parent/child assembly semantics;
- production attachment inventory;
- Connection Layer records;
- validation tolerances/resolvers;
- any P3.2 proxy/control node that would otherwise leak into production truth.

### DO NOT INHERIT AS PRODUCTION AUTHORITY

- legacy 11-family / 40-variant / 365-object accounting;
- P3.2 representative graph as whole-building assembly truth;
- T-017 legacy assembly graph;
- T-020 / RZ / FV placement authority before Stage 5 review;
- T-018 V002;
- visual contact as proof of connection.

## 5. Stage2 first complete step

### Stage2-A｜Coverage & Rebinding Matrix V0.1

This is the only work authorized by the proposed entry decision.

Input scope:
- all **66 V008 registered object types**;
- all **25 approved Master families**;
- Stage1 Master Catalog;
- P3.2 relationship/interface mechanism;
- RC-024 Connection Layer contract/schema;
- Stage1 evidence boundaries.

For every V008 object type, record:
- Stage2 participation class;
- Master / parametric / proxy / topology / UNKNOWN disposition;
- production eligibility;
- owning Master family if applicable;
- variant rule requirement;
- orientation rule requirement;
- interface requirement;
- required relation types;
- length-determination authority class;
- connection-layer requirement;
- evidence boundary;
- explicit deferred/UNKNOWN items.

For every approved Master family, record at minimum:
- canonical identity;
- variant set or explicit NO_VARIANT;
- orientation set or explicit orientation rule;
- start/end/support interface inventory;
- relation-type eligibility;
- parent/child assembly role;
- length rule classification;
- connection-layer coverage status.

## 6. Stage2-A hard boundaries

Stage2-A MUST NOT:

- create whole-building topology;
- place the whole hall;
- use T-017/365 accounting as real-component truth;
- activate T-020/RZ/FV as placement authority;
- resume or patch T-018;
- create Blender geometry;
- create a new engineering T-task;
- invent historical joinery;
- silently convert the seven PENDING_SOURCE_BINDING objects into V008 records;
- treat body-to-body contact as connection closure.

The seven PENDING_SOURCE_BINDING objects remain outside V008:
板瓦 / 勾头 / 滴水 / 博风板 / 悬鱼 / 惹草 / 生头木.

## 7. Stage2-A acceptance gate

Stage2-A may close only when:

1. 66/66 V008 object types have explicit Stage2 participation disposition;
2. 25/25 approved Master families have explicit variant/orientation/interface/length-rule status;
3. all reused P3.2 interfaces are explicitly classified RETAIN / REBIND / SUPERSEDE;
4. no legacy proxy/control identity is silently promoted to real-component truth;
5. Connection Layer coverage requirements are explicit for every production attachment class identified so far;
6. UNKNOWN / RECONSTRUCTED_DESIGN / PARAMETRIC_COMPLETION boundaries remain explicit;
7. no Stage3 representative assembly work starts before Product Owner approves the Stage2 architecture baseline.

## 8. Decision options

### Option A — Recommended
**AUTHORIZE_STAGE2_DESIGN_ONLY**

- Stage2 becomes ACTIVE at governance/design level.
- Stage2-A Coverage & Rebinding Matrix V0.1 becomes the sole next step.
- Engineering execution remains NOT AUTHORIZED.
- No T-task is created yet.

### Option B
**HOLD_STAGE2_ENTRY**

Use only if Product Owner wants additional Stage1 post-close review before Stage2 design begins.

## 9. Recommended next state if Option A is approved

- P3.3: ACTIVE
- Stage1: CLOSED / D-271
- Stage2: ACTIVE / DESIGN AUTHORIZED / ENGINEERING NOT AUTHORIZED
- Current work: Stage2-A Coverage & Rebinding Matrix V0.1
- Active engineering T-task: NONE
- Stage3: NOT AUTHORIZED
- Stage5 legacy placement authorities: HOLD FOR REVIEW
- T-018: HOLD
