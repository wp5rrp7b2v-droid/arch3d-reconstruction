# P3.3 Stage2-B｜Interface / Variant Rule Design V0.1｜Review Summary

- Status: **LOCKED / PRODUCT OWNER APPROVED / D-275**
- Authority: **D-274 / Stage2-B design only**
- Stage2-A baseline: **LOCKED / D-273**
- Engineering execution: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Candidate coverage

- Approved Master families: **25**
- Rule coverage: **25 / 25**
- Existing P3.2 interface-owner families: **6**
- Families requiring Stage2 interface inventory: **19**

### Variant policy
- Stage1-declared geometry variant families: **5**
  - 平梁: EW_SEAM / GABLE
  - 瓜子栱: LARGE / SMALL
  - 慢栱: LARGE / SMALL
  - 华栱: JUMP_1 / JUMP_2
  - 昂: TOU_ANG / ER_ANG
- Role-label-only families: **3**
  - 柱: 角柱 / 普通柱
  - 丁栿: UPPER / LOWER
  - 乳栿: UPPER / LOWER / NE / SE / SW / NW
- No-new-geometry-variant families: **17**

Role labels do not silently create new geometry.

## Orientation rule

Stage2 orientation authority is limited to:
- MASTER_LOCAL
- ASSEMBLY_LOCAL
- assembly-role / endpoint / longitudinal-axis semantics

Whole-building world coordinates are explicitly prohibited as Stage2 authority.

No silent mirror is allowed.

## Interface profiles

Six design profiles are used:
- VERTICAL_SUPPORT
- BLOCK_BEARING
- LONG_MEMBER
- DIAGONAL_MEMBER
- CORNER_MEMBER
- BRACKET_MEMBER

Interfaces are engineering datums/references only.
They are **not** automatically historical contact planes, joinery features, or physical connectors.

## Length rule

Long members that require assembly-resolved length are explicitly assigned endpoint/span-derived rules.

Reference specimen lengths must not silently become per-instance historical exact lengths.

Bracket families retain Stage1 family/variant dimensional authority while per-instance historical full length remains bounded by the existing evidence state.

## Connection Layer

Every production attachment still requires one explicit RC-024 Connection Layer record:
- PHYSICAL_CONNECTOR
- JOINERY_FEATURE
- CONTACT_INTERFACE

Body-to-body visual contact alone remains invalid as an attachment definition.

## Preserved boundaries

- No new historical joinery claim.
- No new geometry variant beyond Stage1 locked variants.
- T-020 / RZ / FV remain Stage5 review items.
- No whole-building topology.
- No Blender engineering.
- No Stage3 execution.
- T-018 remains HOLD.

## Next gate

Product Owner review and lock of Stage2-B Rule Set V0.1.

Only after lock may attachment-specific interface records be materialized in controlled batches.


## D-275 Lock Review Result

- Product Owner review: **APPROVED**.
- Rule Set: **LOCKED**.
- Approved Master families covered: **25 / 25 PASS**.
- Stage1-declared geometry-variant families retained: **5**.
- Role-label-only families: **3**.
- No-new-geometry-variant families: **17**.
- New geometry variants introduced beyond Stage1 authority: **0**.
- World-coordinate authority introduced: **NO**.
- Unsupported historical contact/joinery claims introduced: **NO**.
- RC-024 explicit Connection Layer requirement: **PRESERVED**.
- Attachment-specific interface records materialized: **NO / NEXT CONTROLLED STEP**.
- Engineering execution: **NOT AUTHORIZED**.
- Stage3: **NOT AUTHORIZED**.
- T-018: **HOLD**.
