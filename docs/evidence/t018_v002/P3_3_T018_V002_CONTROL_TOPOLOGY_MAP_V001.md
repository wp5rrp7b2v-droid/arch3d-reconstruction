# T-018 V002｜Control Topology Map V001

## Status
DESIGN COMPLETE / NOT AUTHORITY / IMPLEMENTATION FROZEN

本文件只锁定“谁连谁”的拓扑，不决定尚未获批的 Z 数值。

## 1. Roof control topology

North chain:
`N00 → N01 → N02 → N03(shared ridge)`

South chain:
`S00 → S01 → S02 → N03(shared ridge)`

Prohibited:
- `ROOF_PURLIN_S_03`
- second ridge identity
- split ridge
- local mirror-generated ridge

Y positions remain exactly T-020 canonical:
- N00 -6808.5
- N01 -4972.5
- N02 -3213.0
- N03 0
- S02 +3213.0
- S01 +4972.5
- S00 +6808.5 mm

## 2. Roof X stations

Derived from grid west/east edge plus OUT-003*MOD-002 gable projection:

- RX00 = -7145.1
- RX01 = -5737.5
- RX02 = -2218.5
- RX03 = +2218.5
- RX04 = +5737.5
- RX05 = +7145.1 mm

These six stations explain the 36 RAFTER identities:
2 roof sides × 6 X stations × 3 slope segments.

## 3. Rafter adjacency

For every X station RX00..RX05:

North:
- `ROOF_RAFTER_N_X##_S00` = N00→N01
- `ROOF_RAFTER_N_X##_S01` = N01→N02
- `ROOF_RAFTER_N_X##_S02` = N02→N03

South:
- `ROOF_RAFTER_S_X##_S00` = S00→S01
- `ROOF_RAFTER_S_X##_S01` = S01→S02
- `ROOF_RAFTER_S_X##_S02` = S02→N03

Each rafter endpoint is:
`(RX##, control_Y, control_Z)`.

No ID-string parsing is allowed inside Blender. The compiler must consume an explicit topology table equivalent to this map.

## 4. Roof Envelope topology

Each envelope is a four-corner technical surface spanning west roof edge to east roof edge.

North:
- `ROOF_SURFACE_N_00`: N00↔N01
- `ROOF_SURFACE_N_01`: N01↔N02
- `ROOF_SURFACE_N_02`: N02↔N03

South:
- `ROOF_SURFACE_S_00`: S00↔S01
- `ROOF_SURFACE_S_01`: S01↔S02
- `ROOF_SURFACE_S_02`: S02↔N03

For a pair A→B, the ordered corner set must be explicitly serialized:
1. west edge at A
2. east edge at A
3. east edge at B
4. west edge at B

The validator must check:
- no surface crosses Y=0 except the terminal segment ending at N03;
- north/south terminal edges coincide on the same ridge line;
- normal orientation is consistent;
- no duplicate or inverted surface.

## 5. Gable control topology

Each GABLE_CONTROL is a **piecewise polyline**, not a guessed straight eave-to-ridge line.

West:
- `GABLE_W_N`: W×N00 → W×N01 → W×N02 → W×N03
- `GABLE_W_S`: W×S00 → W×S01 → W×S02 → W×N03

East:
- `GABLE_E_N`: E×N00 → E×N01 → E×N02 → E×N03
- `GABLE_E_S`: E×S00 → E×S01 → E×S02 → E×N03

This preserves the same roof control chain and prevents a renderer or executor from inventing a different gable profile.

## 6. Frame-control topology

Frame tier Y stations are center-to-perimeter cumulative FR-004/005/006:

- d1 = 1759.5
- d2 = 3519.0
- d3 = 5355.0 mm

North uses -d; South uses +d.

Each `FRAME_TIER_{N|S}_{01|02|03}`:
- spans column-grid west X to east X;
- uses a single tier Z supplied only by a future approved Frame Vertical completion.

For each X00..X03 and tier k:

- `FRAME_POST_*_LOW`: `FRAME_BASE_DATUM → FRAME_TIER_k`
- `FRAME_POST_*_UP`: `FRAME_TIER_k → ROOF_PROFILE_AT(Y_k)`

Exact Z remains OPEN and is not created here.

## 7. Frame Support topology

Every `SUPPORT_FRAME_...` record is a technical proxy paired 1:1 with the corresponding FRAME_CONTROL record.

Rules:
- same endpoints as its paired control;
- no independent coordinate derivation;
- no historical connector identity claim;
- may never become an input to FRAME_CONTROL placement.

## 8. PRIMARY_FRAME handling

The 8 `PRIMARY_FRAME` records are `UNKNOWN_BLOCKED`.

This map deliberately does **not** turn them into historical beam geometry.

Allowed Stage-C representation:
- semantic/engineering marker anchored to the relevant grid/frame organizational axis;
- no derived historical member length;
- no use as authority for Frame Tier or Roof placement.

## 9. Bracket anchor topology for later Stage C

Only technical anchors are permitted:

- column-head bracket group anchor → matching perimeter column axis at approved column-top technical datum;
- intercolumn bracket group anchor → midpoint between adjacent perimeter column axes on the same façade at approved column-top technical datum.

Internal bracket marker geometry may consume bracket-system parameters, but:
- cannot move Frame;
- cannot move Roof;
- cannot redefine column height;
- remains UNKNOWN/Proxy evidence-bounded representation.

This map does not authorize exact bracket historical placement or joinery.

## 10. Hard topology failures

Immediate rejection for:
- S03 purlin/ridge creation
- any roof chain not terminating at N03
- rafter segment skipping/reversing control adjacency
- envelope using non-adjacent roof controls
- gable profile not using the same roof control sequence
- FRAME_SUPPORT coordinates differing from paired FRAME_CONTROL
- any topology inferred only inside Blender
