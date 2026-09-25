# T-031｜P3.3 Two-piece Micro Assembly Proof V001

## Status
PLACEMENT LAYER PASS / OVERALL ASSEMBLY INCOMPLETE / SUPERSEDED AS FINAL SUCCESS CRITERION BY CONNECTION-LAYER REQUIREMENT

## Objective
Validate that two already-approved Masters can be assembled automatically from clean state without manual Blender placement:

- 四椽栿 `CMP-FRAME-FOUR-CHUANFU-001_MASTER`
- 托脚 `CMP-FRAME-TUOJIAO-001_MASTER`

This is a **Micro Assembly Proof**, not Stage 2 PASS, not Stage 3 PASS, not whole-building generation, and not authorization for T-018.

## Authority boundary
- Structural semantic: A2 / D-100 — 托脚 supports ends of 四椽栿.
- Four-chuanfu section authority: T-021 approved Master parameters.
- Tuojiao section authority: T-027 approved Master Definition.
- Missing historical length/angle/contact geometry is handled under D-108 / RC-020 + D-137 / RC-023.
- Test coordinates are `ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES`.
- No test coordinate may be written into the Wanfodian Registry or reused as a historical/building placement claim.

## Test geometry
The proof must generate exactly two mesh objects from clean state.

### Four-chuanfu
- section: locked Master section
- test assembly length: 2400 mm
- length classification: ENGINEERING_TEST_ONLY / assembly-derived proof value
- reference length 1000 mm must not leak into the assembly

### Tuojiao
- section: locked canonical section
- one lower test anchor
- one upper support target on the underside of the four-chuanfu
- length and orientation calculated automatically from the test support target
- placement must be tangent to the beam underside within tolerance, not manually translated after generation

## Mutation proof
Run at least:
- TEST_A: support target X = -900 mm
- TEST_B: support target X = -700 mm

The same two Master identities and sections must be used in both cases.

Changing the support target must:
- change Tuojiao derived length and/or direction;
- preserve Tuojiao section;
- preserve Four-chuanfu section;
- preserve support contact;
- require no manual Blender transform.

## Determinism
Rebuild TEST_A from factory-startup a second time.
Semantic geometry signature must match the first TEST_A exactly.

## PASS criteria
1. exactly 2 mesh objects;
2. correct component/master identities;
3. Four-chuanfu section = approved section;
4. Tuojiao section = approved section;
5. Four-chuanfu test length != 1000 mm;
6. Tuojiao actual length is derived, not fixed to 1000 mm;
7. support target is satisfied within 0.1 mm;
8. no positive penetration above the Four-chuanfu underside beyond 0.1 mm;
9. TEST_B changes Tuojiao geometry automatically;
10. no Master body or source authority is modified;
11. TEST_A deterministic rebuild signature MATCH;
12. all coordinates remain ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES.

## Hard fails
- MANUAL_BLENDER_PLACEMENT_REQUIRED
- REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY
- FIXED_TUOJIAO_ANGLE
- TEST_COORDINATE_PROMOTED_TO_BUILDING_AUTHORITY
- SUPPORT_CONTACT_NOT_CLOSED
- MATERIAL_INTERPENETRATION_OVER_TOLERANCE
- MASTER_IDENTITY_CHANGED
- NON_DETERMINISTIC_REBUILD

## Deliverables
Actions artifact only:
- TEST_A .blend + semantic JSON + FRONT/AXON PNG
- TEST_B .blend + semantic JSON + FRONT/AXON PNG
- TEST_A restore semantic JSON
- validation JSON

No generated .blend is committed to Git.

## Stage boundary
A PASS proves only that the current Master/assembly concept can perform one minimal automatic support-placement action.
It does **not**:
- complete Stage 1;
- enter or pass Stage 2;
- enter or pass Stage 3;
- establish whole-building XYZ;
- authorize T-018;
- establish historical joinery or historical angle/length.


## Execution Result｜2026-09-25

- GitHub Actions Run: `36094815356`
- Job: `micro-assembly-proof`
- Blender: `4.5.13 LTS`
- Result: **SUCCESS**
- Validation: **12/12 PASS**
- Artifact: `P3_3_T031_TWO_PIECE_MICRO_ASSEMBLY_PROOF_V001`
- Artifact ID: `10846594498`
- Artifact ZIP SHA-256: `35b3b669190b46c780b1d5c0dfb8af3dc626809ecd016cfa537bdbf13c43d6e2`
- Artifact expiry: 2026-10-25

### TEST_A
- Four-chuanfu test length: 2400 mm / ENGINEERING_TEST_ONLY
- Tuojiao derived length: **1387.117132 mm**
- Tuojiao direction: `[0.550881922, 0, 0.834583282]`
- support gap: **0.00012207 mm**
- penetration: **0.00012207 mm**
- tolerance: 0.1 mm
- semantic signature: `5ba3556ddaa32a4f4db9ef4e3fdf3ec9ed353a0e640cb637a4a737f8464a773f`

### TEST_B mutation
- support target X changed from -900 to -700 mm
- Tuojiao derived length changed to **1498.030102 mm**
- Tuojiao direction changed to `[0.640198708, 0, 0.768209457]`
- support gap: **0.0 mm**
- penetration: **0.0 mm**
- Four-chuanfu and Tuojiao sections unchanged
- semantic signature: `01386b4b8828143fd5140c8586fa5e2811626896d9ac40b72792577b5d07fb08`

### Determinism
- TEST_A restore signature:
  `5ba3556ddaa32a4f4db9ef4e3fdf3ec9ed353a0e640cb637a4a737f8464a773f`
- MATCH: **YES**

### Human visual review
FRONT and AXON images for TEST_A and TEST_B were actually inspected.

- no visible gross gap;
- no visible gross interpenetration;
- changing the support target visibly changes Tuojiao angle/length while retaining the same two component identities;
- the current contact is a simplified tangent support using bounded rectangular envelopes;
- this proof does **not** establish historical end profile, mortise/tenon, bearing surface, or real structural mechanics.

### Proof conclusion
**PASS for Micro Assembly architecture objective.**

What is proven:
- clean-state scripted two-piece assembly works;
- no manual Blender placement is required;
- assembly-owned target mutation automatically updates Tuojiao;
- reference length 1000 mm does not leak into assembly;
- deterministic rebuild works.

What is NOT proven:
- Stage 2 PASS;
- Stage 3 PASS;
- real Wanfodian XYZ;
- historical joinery/contact face;
- structural load-path correctness;
- whole-building placement authority.


## Product Owner refinement｜2026-09-25

T-031 is **not** accepted as a complete component-assembly success criterion.

Product Owner requires that a successful assembly proof must include an explicit **Connection Layer** between participating Masters. Therefore:

- T-031 result remains valid only as **Placement Layer PASS**;
- two bodies merely touching is insufficient for complete-assembly acceptance;
- full success requires a connector-aware proof with explicit connection identity, connection geometry/feature semantics, automatic closure, mutation propagation and deterministic rebuild;
- this refinement does not invalidate T-031's placement calculations; it narrows what T-031 proves.
