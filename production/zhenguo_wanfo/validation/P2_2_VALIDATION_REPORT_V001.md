# P2.2 T-007 Structural Skeleton Candidate — Engineering Validation V001

Date: 2026-09-12
Scope: P2.2 medium-LOD structural candidate only
Machine tolerance (declared before build): **0.01 mm**
Deterministic comparison tolerance (declared before build): **0.0001 mm**
Blender: **3.6.23**; Blender Python: **3.10.13**; host test Python: **3.10.2**

## 1. Formal input and evidence boundary

The generator reads the 85/85 formal parameter/dependency entries, the independent D-023 override sidecar, the evidence-aware schema, and the D-023/D-024/D-025 decision boundary. Geometry requests are rejected unless their dependency role is `DIRECT_GEOMETRY_INPUT` or `DERIVED_GEOMETRY_RULE`; only the approved `Z-006-RC-01` resolves the blocked historical `Z-006`. The manifest records 38 actual formal parameter IDs, 19 calculated rule outputs with formulas and source IDs, and the remaining formal derived-rule identities. These are the only formal historical/reconstruction geometry inputs.

| Input | SHA256 |
|---|---|
| `params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json` | `37bc365a50bd6a43e178c3102c19ad76cbf0cb533f4d76710a793afa318c0889` |
| `params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json` | `3436050b33508d55633d1699c9f263f976f6e4b30b534c5607f89752735116c3` |
| `dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json` | `3e77d4c03acbd3595c28e93b1d04166730ede1bd08741c9aa94b28164f3764e4` |
| `schema/evidence_aware_parameter_schema_v001.json` | `3348bddc0509e004ff6b99c48fc047c8b080bdc98bf6fd069acc6454589328ed` |
| `docs/project_control/decision_log.md` | `99050e585dcf5c6e8dd04d5eb7d5bf7fd3e00d500c04f0d34a43faa600e090a5` |

The current P2.1 production preflight and schema validation return PASS with zero unresolved geometry-critical blockers. T-007 corrected a pre-existing D-023 row-format parser mismatch in `validate_p2_1_approved_override.py`; it now accepts the decision log's ordinary table ID as well as the bold form. No P2.1 parameter, override, matrix, schema, or decision content was changed.

## 2. Structural scope and key controls

**6/6 scope families are present in one spatially connected model**, with 217 stable named mesh objects: grid 8, columns 12, primary frame 62, bracket topology 88, roof controls 43, and gable controls 4. Frame posts connecting the frame tiers to roof control lines are explicitly marked bounded medium-LOD placeholders.

| Control | Candidate result | Formal provenance |
|---|---:|---|
| Front bays / width | 3519 + 4437 + 3519 = 11475 mm; 3 bays | PM-001, PM-008, PM-010, PM-011, MOD-001 |
| Depth bays / depth | 3519 + 3672 + 3519 = 10710 mm; 3 bays | PM-002, PM-009, PM-010, PM-012, MOD-001 |
| Columns | 12 perimeter, 0 interior; diameter 459 mm | PM-013, PM-014, Z-002 |
| Column height | 3534.3 mm; corner rise +61.2 mm | D-023 Z-006-RC-01 = 11 × MOD-006; Z-005 |
| Frame half-depth spans | 1759.5, 1759.5, 1836 mm | FR-004–FR-006 |
| Bracket topology | 16 head directions × 4 jumps; 12 intercolumn sets × 2 jumps | DG-001, DG-002, DG-110–DG-113, MOD-002 |
| Roof controls | eave Z 3855.6; lower 5202.0; upper 6135.3; ridge 7389.9 mm | ROOF-007–ROOF-011, DG-113, MOD-002, RC-01 |
| Eave / gable | half roof run 6808.5 mm; 1453.5 mm beyond column line; gable projection 1407.6 mm | FR-007, PM-012, OUT-003, MOD-002 |

The two-jump and four-jump topology is represented by equal visual subdivisions of approved aggregate outjump totals. Those subdivisions, the vertical frame posts, gable outlines, and roof surface interpolation are **diagrammatic bounded placeholders**, not exact historic member sections, joint positions, 45° corner solutions, or hidden-angle-beam claims. Box sections are derived from MOD-003–MOD-005 and MOD-002 as control envelopes.

`VALIDATION_REFERENCE` remains separate from reconstructed geometry. Examples: PM-003 observed front center bay 4481.3 mm versus candidate 4437 mm; PM-004 observed depth center bay 3676.8 mm versus candidate 3672 mm; PM-006 observed overall width 11492.7 mm versus candidate 11475 mm; PM-007 observed depth 10688.2 mm versus candidate 10710 mm. No observed value was forced into the candidate layer.

## 3. Machine geometry, metadata, and unknowns

The independent validator reopened each saved Blender file and checked all 217 mesh names, required object metadata, parameter role references, manifest metadata mapping, input and output hashes, grid and column locations, column dimensions, frame endpoints and tiers, bracket projected steps and rise, roof purlin and rafter controls, gable controls, and family counts. **Both formal runs: PASS, no errors.** The final result is in `P2_2_MACHINE_VALIDATION_V001.json`.

`Z-006` stays `UNKNOWN / null / DO_NOT_LOCK`, and its dependency stays `BLOCKS_P2_2_GEOMETRY`. Only the independent `Z-006-RC-01` supplies 3534.3 mm to the candidate model, with `REASONABLE_COMPLETION`, `D-023`, and `is_replaceable=true` in the manifest. `DG-114` stays `BOUNDED_NON_BLOCKING`, with no unified small-dou specification. `HIS-002` stays metadata only. Every structural object has `originality_status=unknown`; no object is tagged `963_confirmed`.

The numeric-literal scan of the generation script found **no naked historical dimension**. Numeric literals above 10 are the approved D-023 multiplier 11, formal set cardinality 85, derived topology summary counts 12/16, cylinder tessellation 16, hash chunk size, and review-camera/render settings. Actual historical/reconstruction dimensions are obtained through the formal reader or documented formulas. The T-007 automated literal test rejects known formal dimension values embedded into the generator.

## 4. Rebuild and replacement evidence

Two consecutive builds started from `--factory-startup` under Blender 3.6.23 with identical formal inputs. Object name set, count (217), family counts, key dimensions, topology summary, geometry-input snapshot, and independently reopened output-validation summary are all **exactly equal**; both semantic-summary SHA256 values are `520b76e75478a251a6ff2ccc9c5740e536d455520bea8142eb0de938ef72162e`. The two `.blend` byte hashes differ (`e7ea201f0c26650b45d9bb4ed45d06238188fa39af1ac5a49c49b7c51e3f1d9a` and `3b61ccbaca17836bd63d9369ebc3a4c6e25fb27f0d274ea67e64f732ad3000e4`); deterministic PASS refers to the declared structural/validation comparisons, not byte-identical Blender serialization. The final `.blend` hash is the second value.

A **synthetic test-only** MOD-006 change from 321.3 to 336.6 mm, with its modular source and sidecar cache updated, rebuilt RC-01 and actual column geometry from 3534.3 to 3702.6 mm; independent reopen PASS. Z-006 remained null. A second synthetic test-only replacement changed Z-005, Z-007, ROOF-010, and ROOF-011 together with their consistent roof rule; the model rebuilt and reopened PASS, with ridge Z changing from 7389.9 to 7420.5 mm. Neither synthetic input was written into the formal files or final candidate.

## 5. Review and archive

The three 1400 × 1000 structural review PNGs were visually inspected after fixing the camera clip range and framing. Plan shows the full grid/eave footprint, side elevation shows the roof rise/gable relation, and axonometric shows the connected frame and roof control skeleton:

- `review/P2_2_STRUCTURAL_SKELETON_V001_PLAN.png`
- `review/P2_2_STRUCTURAL_SKELETON_V001_ELEVATION.png`
- `review/P2_2_STRUCTURAL_SKELETON_V001_AXON.png`

The `.blend` is local-only at `output/P2_2_STRUCTURAL_SKELETON_V001.blend` (SHA256 `3b61ccbaca17836bd63d9369ebc3a4c6e25fb27f0d274ea67e64f732ad3000e4`, 2,466,272 bytes). The tracked build manifest is `build/P2_2_BUILD_MANIFEST_V001.json`. The generation script, validator, 5 new T-007 unit tests, machine evidence, this report, and three PNGs are the canonical Git deliverables; the final task report records their GitHub commit. Full local 3.6 ↔ cloud 4.5 QC and P2.3 are outside T-007.

All 9 P2.2 DoD evidence categories have engineering evidence assembled: input/manifest, complete scope, parameter provenance, machine geometry, replacement, bounded unknowns, metadata, deterministic reopen/review images, and archive deliverables. The project's 32 automated tests pass. **Engineering recommendation: PASS after canonical push. This report does not declare P2.2 Gate PASS.** Product Owner structural review and Gate decision remain separate.
