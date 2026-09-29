# P3.3 Stage2-A｜Coverage & Rebinding Matrix V0.1｜Review Summary

- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Entry authority: **D-272 / Stage2 design-only**
- Stage1: **CLOSED / D-271**
- Stage2 engineering execution: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Coverage result

### V008 object-type layer
- V008 registered object types: **66**
- Explicit Stage2 participation dispositions: **66 / 66**
- Breakdown:
  - MASTER_BOUND_PRODUCTION: **28**
  - PARAMETRIC_SYSTEM_OR_COMPLETION: **23**
  - TOPOLOGY_OR_ASSEMBLY_CONTAINER: **5**
  - SIMPLIFIED_PROXY: **7**
  - REFERENCE_ONLY_UNKNOWN: **3**

### Approved Master-family layer
- Approved Master families: **25**
- Explicit Stage2 rebinding status: **25 / 25**
- Existing P3.2 interface owners: **6**
- Master families requiring new Stage2 interface inventory: **19**

Existing P3.2 interface-owner Masters:
1. CMP-COLUMN-001_MASTER
2. CMP-LUDOU-COLUMN-001_MASTER
3. CMP-DOU-SINGLE-LONGKAI-001_MASTER
4. CMP-DOU-INTERACTIVE-001_MASTER
5. CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER
6. CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER

The remaining 19 approved Master families have no P3.2 interface-owner coverage and therefore require explicit Stage2 interface inventory rather than inherited assumptions.

## Rebinding principle

P3.2 is retained as a **semantic mechanism baseline**, not as current production truth.

Retain:
- SUPPORT / CONNECT / LOCATE / REPEAT / BELONG vocabulary;
- MASTER_LOCAL interface principle;
- world coordinates as derived output only;
- manual Blender placement not canonical;
- RC-024 Connection Layer kinds.

Rebind:
- Master/interface ownership;
- variant rules;
- orientation rules;
- start/end/support interfaces;
- instance length rules;
- parent/child assembly semantics;
- production attachment inventory;
- Connection Layer records and tolerances.

Do not inherit as production authority:
- legacy 11-family / 40-variant / 365-object accounting;
- P3.2 representative graph as whole-building truth;
- T-017 assembly graph;
- T-020 / RZ / FV placement authority before Stage5;
- T-018 V002;
- visual/body contact as proof of connection.

## Matrix safety policy

Candidate V0.1 deliberately uses statuses such as:
- REVIEW_REQUIRED
- DEFINE_IN_STAGE2
- REBIND_REQUIRED
- NOT_YET_STAGE2_LOCKED

These are not missing work by accident. They prevent unsupported assembly geometry from being invented during coverage enumeration.

No new historical joinery, connector dimensions, instance placement, or whole-building topology is asserted by this matrix.

## Seven PENDING_SOURCE_BINDING objects

Still outside V008 and unchanged:
- 板瓦
- 勾头
- 滴水
- 博风板
- 悬鱼
- 惹草
- 生头木

They are not silently added to Stage2 scope.

## Candidate review question

Product Owner review should decide whether the V0.1 coverage architecture is acceptable as the **Stage2-A baseline**.

If approved, the next complete step should be:

> Lock Stage2-A Coverage & Rebinding Matrix V0.1 and begin the first controlled interface/variant rule design batch.

No Stage3 or engineering execution follows automatically.
