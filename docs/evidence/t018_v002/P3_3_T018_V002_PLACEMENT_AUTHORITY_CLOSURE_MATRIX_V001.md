# T-018 V002｜Placement Authority Closure Matrix V001

## Status
DESIGN COMPLETE / NOT AUTHORITY / IMPLEMENTATION FROZEN

本文件只回答：Stage B/Stage C 关键对象的 X/Y/Z/endpoint/surface 是否都有唯一合法来源。任何 `OPEN` 项在正式补全前都禁止进入 CP-03。

## 1. 已闭合的基础坐标

| Control | Formula / source | Result |
|---|---|---|
| Project X datum | T-020: X=0 reconstructed-design width center | CLOSED |
| Project Y datum | T-020: Y=0 reconstructed-design depth center | CLOSED |
| Project Z datum | Z-007: Z=0 abstract column-foot design plane | CLOSED |
| Grid X | PM-008/010 + MOD-001, checked by PM-011 | CLOSED |
| Grid Y | PM-009/010 + MOD-001, checked by PM-012 | CLOSED |
| Column height | Z-006-RC-01 = 3534.3 mm | CLOSED |
| Roof Y chain | T-020 + FR-007 + MOD-002 | CLOSED |
| Roof X edge | column-grid west/east + OUT-003*MOD-002 | CLOSED |

Derived design coordinates used only as audit values:
- grid X = [-5737.5, -2218.5, 2218.5, 5737.5] mm
- grid Y = [-5355, -1836, 1836, 5355] mm
- roof X stations = [-7145.1, -5737.5, -2218.5, 2218.5, 5737.5, 7145.1] mm
- roof Y controls:
  - N00=-6808.5, N01=-4972.5, N02=-3213, N03=0
  - S02=3213, S01=4972.5, S00=6808.5

## 2. Critical Placement Closure

| Object / control | X | Y | Z | endpoint / surface | Status |
|---|---|---|---|---|---|
| GRID_X/Y | CLOSED | CLOSED | CLOSED | axis extents CLOSED | CLOSED |
| COLUMN | CLOSED | CLOSED | CLOSED | approved Master local axis/origin | CLOSED |
| FRAME_TIER_N/S_01..03 | column-width span CLOSED | FR-004/005/006 cumulative station CLOSED | **OPEN-FV-01** | endpoints inherit tier Z | OPEN |
| FRAME_POST_*_LOW | grid-X CLOSED | tier-Y CLOSED | **OPEN-FV-02 base + tier Z** | base→tier | OPEN |
| FRAME_POST_*_UP | grid-X CLOSED | tier-Y CLOSED | **OPEN-FV-03 tier→roof profile** | tier→roof-control profile | OPEN |
| PURLIN controls | roof-X span CLOSED | T-020 Y CLOSED | **OPEN-RZ-01 exact serialized formula** | west→east control span | OPEN |
| RAFTER | roof-X station CLOSED | roof-control adjacency CLOSED by topology design | inherits RZ-01 | pair of adjacent roof controls | OPEN until RZ |
| ROOF_ENVELOPE | roof-X edge CLOSED | roof-control interval CLOSED by topology design | inherits RZ-01 | 4-corner surface map required | OPEN until RZ/topology |
| GABLE_CONTROL | fixed east/west roof edge CLOSED | roof-chain CLOSED | inherits RZ-01 | piecewise control polyline required | OPEN until RZ/topology |
| PRIMARY_FRAME | semantic family only | grid anchor available | physical Z not authorized | no historical beam placement required | CLOSED AS UNKNOWN/SEMANTIC ANCHOR ONLY |
| BRACKET_ARM | technical anchor class | grid/column anchor candidate | column-top technical datum candidate | internal marker only | DEFER TO STAGE C ANCHOR CONTRACT |
| BRACKET_CONTACT | technical anchor class | grid/column/intercolumn anchor candidate | column-top technical datum candidate | proxy only | DEFER TO STAGE C ANCHOR CONTRACT |

## 3. Roof-Z Closure Requirement

T-020 already names Z authority as:
`Z-007 + Z-006-RC-01 + ROOF-007/008/009`.

However the exact cumulative formula is not yet serialized as whole-building placement authority.

The only completion permitted by current T-020 authority envelope is a formula equivalent to:

- eave control Z0 = project Z datum + approved column-height rule
- Z1 = Z0 + ROOF-007*MOD-002
- Z2 = Z1 + ROOF-008*MOD-002
- ridge Z3 = Z2 + ROOF-009*MOD-002

Audit candidate values:
- Z0 = 3534.3
- Z1 = 4880.7
- Z2 = 5814.0
- Z3 = 7068.6 mm

**These values are design-review candidates, not new authority, until a later explicitly approved completion artifact formalizes the formula.**
DG-113 is not permitted in this roof-Z chain.

## 4. Frame-Vertical Closure Requirement

Frame Y stations are bounded by existing Frame parameters:
- d1 = FR-004 = 1759.5 mm
- d2 = FR-004+FR-005 = 3519 mm
- d3 = FR-004+FR-005+FR-006 = 5355 mm
- north uses negative sign, south positive sign.

Frame Z is **not closed**.

Legacy P2 used:
`Z-006-RC-01 + DG-113*MOD-002 + cumulative ROOF-004/005/006`

This remains DIAGNOSTIC ONLY because:
- DG-113 is currently owned by ORG-BRACKET-SYSTEM;
- ROOF-004/005/006 are currently owned by ORG-ROOF-SYSTEM;
- no P3.3 cross-system project rule authorizes using them for FRAME placement.

Therefore FV-01/FV-02/FV-03 cannot be filled by implementation code. A later completion design must either:
1. explicitly authorize a bounded one-way bridge using existing parameters, or
2. leave exact Frame Tier elevation unresolved and reduce representation accordingly.

No new historical dimension is allowed.

## 5. Entry Gate

CP-03 may restart only when:
- OPEN-RZ-01 is formally closed;
- OPEN-FV-01/02/03 are formally closed or explicitly downgraded to non-geometric semantic representation;
- topology maps for RAFTER / ROOF_ENVELOPE / GABLE are approved;
- no remaining Stage-B coordinate cell is `OPEN`.

This matrix itself creates no Rule and changes no upstream artifact.
