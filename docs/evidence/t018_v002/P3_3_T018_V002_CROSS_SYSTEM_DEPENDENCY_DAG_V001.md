# T-018 V002｜Cross-System Dependency Whitelist / DAG V001

## Status
DESIGN COMPLETE / NOT AUTHORITY / IMPLEMENTATION FROZEN

本文件只定义依赖方向与禁止边界，不新增任何参数值或历史事实。

## 1. Allowed dependency directions

```
PROJECT DATUM / MODULAR SYSTEM
        ↓
COLUMN GRID
   ↓        ↓
COLUMN    FRAME XY
              ↓
        FRAME CONTROL
              ↓
        FRAME SUPPORT

COLUMN HEIGHT ──→ [PROPOSED ROOF Z BASE COMPLETION]
ROOF ELEVATION PARAMETERS ──→ ROOF CONTROL Z
FR-007 + T-020 ──→ ROOF CONTROL Y

ROOF CONTROL ──→ RAFTER
ROOF CONTROL ──→ ROOF ENVELOPE
ROOF CONTROL ──→ GABLE CONTROL
ROOF CONTROL ──→ FRAME_POST_*_UP endpoint only

GRID / COLUMN TECHNICAL ANCHORS ──→ BRACKET PROXY / UNKNOWN MARKERS
```

Representation is always downstream from placement. No representation may feed back into placement.

## 2. Whitelisted edges

| From | To | Status | Boundary |
|---|---|---|---|
| MOD-001/002/003/004/005/006 | system calculations | ALLOWED | unit conversion / engineering section only |
| PM-008/009/010 + MOD-001 | COLUMN_GRID X/Y | ALLOWED | reconstructed design |
| PM-011/012 | grid extent validation / derived span | ALLOWED | reconstructed design |
| Z-007 | all project Z coordinates | ALLOWED | project datum only |
| Z-006-RC-01 | COLUMN height | ALLOWED | replaceable project rule |
| FR-004/005/006 | FRAME tier Y stations | ALLOWED | frame-system horizontal/depth chain |
| FR-007 + MOD-002 + T-020 | ROOF Y controls | ALLOWED | eave→ridge horizontal chain |
| ROOF-007/008/009 + MOD-002 | ROOF Z increments | ALLOWED | roof-system rise chain |
| T-020 roof controls | RAFTER / ENVELOPE / GABLE topology consumers | ALLOWED AFTER TOPOLOGY MAP APPROVAL | one-way |
| ROOF profile | FRAME_POST_*_UP terminal | ALLOWED AFTER FRAME VERTICAL COMPLETION | consumer only |
| FRAME_CONTROL | FRAME_SUPPORT | ALLOWED | support proxy mirrors control endpoints |
| COLUMN/GRID technical anchor | BRACKET proxy/unknown marker | ALLOWED FOR NON-HISTORICAL REPRESENTATION | must not influence building placement |

## 3. Edges requiring later explicit completion approval

These are not approved by this document:

| Candidate bridge | Why needed | Current status |
|---|---|---|
| Z-006-RC-01 → ROOF eave-base Z | T-020 names Z-006-RC-01 in roof Z authority but exact cumulative formula is not serialized | PROPOSED / NOT AUTHORITY |
| ROOF-004/005/006 → FRAME_TIER Z | legacy P2 used them as frame-rise chain, but canonical target is ORG-ROOF-SYSTEM | PROPOSED BRIDGE / DECISION REQUIRED |
| DG-113 → FRAME vertical base | legacy P2 used lower-ang rise in frame base, but canonical target is ORG-BRACKET-SYSTEM | PROPOSED BRIDGE / DECISION REQUIRED |

If either of the last two cannot be justified without new historical claims or circular authority, exact Frame Tier Z must remain unresolved rather than be invented.

## 4. Explicitly prohibited edges

- PM-003..PM-007 → any reconstructed-design placement
- P2 numeric world transform → any P3.3 placement
- DG-113 → ROOF control Z
- BRACKET geometry → FRAME or ROOF placement
- FRAME placement → ROOF control authority
- ROOF control → COLUMN_GRID or COLUMN origin
- REPRESENTATION → PLACEMENT
- BLENDER object transform → canonical runtime placement
- RENDERER camera/framing logic → geometry
- Validator expected geometry → compiler implementation
- Any locally invented mirror/origin/ridge rule not present in canonical/project-rule authority
- Any dependency that forms a cycle

## 5. Required acyclic order

1. Read protected canonical parameters / identities.
2. Resolve project datum and grid.
3. Resolve columns.
4. Resolve roof Y.
5. Resolve roof Z only after explicit closure.
6. Resolve frame Y.
7. Resolve frame Z only after explicit closure.
8. Resolve endpoints/topology.
9. Expand technical proxies / envelopes / controls.
10. Apply representation.
11. Blender executes manifest only.
12. Independent validator checks invariants without importing compiler geometry formulas.

## 6. Cycle hard-fail examples

Immediate STOP if any future implementation produces:

- FRAME_TIER_Z → ROOF_Z → FRAME_TIER_Z
- BRACKET_RISE → FRAME_Z → BRACKET_ANCHOR → BRACKET_RISE
- RENDERED_OBJECT_LOCATION → MANIFEST_LOCATION
- VALIDATOR_EXPECTED_ENDPOINTS → COMPILER_ENDPOINTS

This DAG creates no authority; it defines the only dependency shapes a later completion may be allowed to formalize.
