# T-032｜P3.3 Connection-Layer Complete Assembly Proof V001

## Status
MACHINE + HUMAN REVIEW PASS / AWAITING PRODUCT OWNER ACCEPTANCE / COMPLETE-ASSEMBLY ARCHITECTURE PROOF

## Objective
Upgrade the prior placement-only proof into a complete assembly proof:

`上六椽栿 Master → Connection Layer / 散斗 proxy → 四椽栿 Master`

The proof must demonstrate that assembly success includes an explicit connection object and two validated interfaces, not just body-to-body contact.

## Source / authority
- Lower Master: `CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER`
- Upper Master: `CMP-FRAME-FOUR-CHUANFU-001_MASTER`
- Connection: `CONN-SAN-DOU-UPPER6-FOUR-001`
- Direct binding: `P3_3_FOUR_CHUANFU_DIRECT_SOURCE_BINDING_V001.md`
- Connection Layer contract: `P3_3_CONNECTION_LAYER_CONTRACT_V001.md`
- Rule: RC-020 + RC-023

## Evidence boundary
Direct source supports:
- 四椽栿 above 上六椽栿;
- 隔架单栱 relation exists between them;
- 四椽栿下不用栌斗;
- 四椽栿由散斗承托.

Direct source does NOT close:
- exact san-dou dimensions;
- exact historical profile;
- hidden mortise/tenon;
- full spacer-single-gong group geometry.

Therefore T-032 san-dou geometry is:
`RECONSTRUCTED_DESIGN / PHYSICAL_CONNECTOR_PROXY / ENGINEERING_TEST_ONLY`

## Test assembly
### TEST_A
- lower beam test length: 2400 mm
- upper beam test length: 2200 mm
- lower/upper canonical sections must come from their approved Master parameter files
- connector centered at X=0
- connector XY size = 0.60 × min(lower width, upper width)
- connector height = 160 mm

### TEST_B mutation
- connector height = 220 mm
- resolver must automatically move upper beam Z to preserve both connection interfaces
- no beam section or Master identity may change

## Required objects
Exactly 3 mesh objects:
1. upper-six-chuanfu lower Master realization
2. san-dou connector proxy
3. four-chuanfu upper Master realization

## PASS
1. exactly 3 mesh objects;
2. both Master identities preserved;
3. explicit unique `connection_id`;
4. connector kind = PHYSICAL_CONNECTOR;
5. connector geometry explicitly reconstructed/test-only;
6. historical_claim = false;
7. lower top ↔ connector bottom closes ≤0.1mm;
8. connector top ↔ upper bottom closes ≤0.1mm;
9. no unexplained interpenetration >0.1mm;
10. connector footprint lies inside both supported beam widths;
11. TEST_B changes connector height;
12. TEST_B automatically updates upper Master Z;
13. beam sections remain unchanged;
14. no 1000mm canonical reference length leakage;
15. no manual Blender transform;
16. TEST_A clean rebuild semantic signature exact-match;
17. Connection Layer machine schema validates;
18. all test coordinates remain ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES.

## Hard fails
- CONNECTION_LAYER_MISSING
- CONNECTOR_IDENTITY_MISSING
- CONNECTOR_HISTORICIZED
- INTERFACE_NOT_CLOSED
- CONNECTOR_INTERPENETRATION
- MANUAL_BLENDER_PLACEMENT_REQUIRED
- REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY
- TEST_COORDINATE_PROMOTED_TO_BUILDING_AUTHORITY
- MASTER_IDENTITY_CHANGED
- NON_DETERMINISTIC_REBUILD

## Boundary
PASS means the project has proven one complete connector-aware assembly architecture.

PASS does NOT claim:
- exact 963 san-dou geometry;
- exact historical joinery;
- full 隔架单栱 group completion;
- Stage 2 PASS;
- Stage 3 PASS;
- whole-building placement authority;
- T-018 authorization.


## Execution Result｜2026-09-25

- GitHub Actions Run: `36095981034`
- Blender: `4.5.13 LTS`
- Validation: **18/18 PASS**
- Artifact: `P3_3_T032_CONNECTION_LAYER_COMPLETE_ASSEMBLY_PROOF_V001`
- Artifact ID: `10846909100`
- Artifact ZIP SHA-256: `94f67748e32304639b678bec8cdd2d11169495107a123666defe8529baf64cea`
- Artifact expiry: 2026-10-25

### TEST_A
- lower Master: 上六椽栿 / section 334 × 240.5 mm
- Connection Layer: `CONN-SAN-DOU-UPPER6-FOUR-001`
- connector kind: `PHYSICAL_CONNECTOR`
- connector geometry: `RECONSTRUCTED_DESIGN / PHYSICAL_CONNECTOR_PROXY / ENGINEERING_TEST_ONLY`
- connector envelope: 200.4 × 200.4 × 160 mm
- upper Master: 四椽栿 / section 426.5 × 302 mm
- lower interface gap / penetration: 0 / 0 mm
- upper interface gap / penetration: 0 / 0 mm
- upper Master resolved bottom Z: 400.5 mm
- semantic signature: `99ceecbd3bcd1ed548e4bce165d3b34e4a1c109e0a467fdba071cb7fdc170c5e`

### TEST_B mutation
- connector height: 160 → 220 mm
- upper Master resolved bottom Z: 400.5 → 460.5 mm
- both interfaces remain 0 mm gap / 0 mm penetration
- lower/upper Master sections unchanged
- semantic signature: `8175d1f5067b2ac160178bed6167017b94e439245a28c3e1c545b2950e289de3`

### Determinism
- TEST_A restore signature:
  `99ceecbd3bcd1ed548e4bce165d3b34e4a1c109e0a467fdba071cb7fdc170c5e`
- exact match: **YES**

### Human visual review
TEST_A / TEST_B FRONT and AXON were inspected:
- lower beam, connector and upper beam are visually distinct;
- connector bridges the two Masters;
- no visible gap or gross interpenetration;
- TEST_B visibly raises the upper Master as connector height changes.

### Scope conclusion
**PASS for one connector-aware complete assembly architecture proof.**

This proves:
- Connection Layer exists as a machine-readable assembly layer;
- a physical connector can carry its own identity and evidence boundary;
- connection mutation propagates to participating Master placement;
- full assembly can rebuild deterministically without manual Blender transforms.

This does NOT prove:
- historical san-dou profile or dimensions;
- historical mortise/tenon;
- the full 隔架单栱 group;
- Stage 2 / Stage 3 completion;
- whole-building placement authority.
