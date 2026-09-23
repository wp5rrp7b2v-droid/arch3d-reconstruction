# T-029｜P3_3_SHUZHU_MASTER_V2_V001｜蜀柱 Master 首件生产

Status: **TASK CONTRACT LOCKED / D-116 / ENGINEERING EXECUTION AUTHORIZED**

Think Level: HIGH

## 1. Objective

Produce one reusable `CMP-FRAME-SHUZHU-001_MASTER V001` for all four V008 蜀柱 instances.

Locked facts:
- physical instances = 4
- INTERIOR_FRAME = 2
- GABLE_FRAME = 2
- geometry variants = 0
- canonical section = 218.75 × 157.5 mm
- canonical reference body = 1000 × 218.75 × 157.5 mm
- 1000 mm is non-historical reference only

## 2. Execution branch

`codex/t029-p3-3-shuzhu-master-v2-v001`

One task = one branch = one PR.

## 3. Endpoint resolver

Generic endpoint-driven placement must be reused.

Rules:
- length = norm(P_upper - P_lower)
- center = midpoint
- local longitudinal axis aligns to endpoint vector
- actual building coordinates are NOT locked in Stage1

Deterministic fixtures:

TEST-A
- lower = [0,0,0]
- upper = [0,0,1200]
- expected length = 1200 mm
- expected center = [0,0,600]
- expected direction = [0,0,1]

TEST-B
- lower = [0,0,0]
- upper = [0,0,1500]
- expected length = 1500 mm
- expected center = [0,0,750]
- expected direction = [0,0,1]

Both:
- ENGINEERING_TEST_ONLY
- NOT_BUILDING_COORDINATES
- historical_claim = false

The generic endpoint contract must support:
- lengths_must_differ = true
- directions_must_match = true
- directions_must_differ = false

Backward compatibility:
- definitions without this explicit variation policy retain the existing direction-difference default used by T-028.

## 4. Shared infrastructure rule

If shared Master V2 builder/validator/workflow changes:
- T-025 PASS
- T-026 PASS
- T-027 PASS
- T-028 PASS

No Shuzhu-only validator or workflow is allowed.

## 5. Canonical body

- straight rectangular bounding-envelope proxy
- exact historical section profile UNKNOWN
- simplified flat ends
- no hidden historical joinery claim
- length/height remains assembly-owned

## 6. Review Board

Required six panels:
1. AXON
2. LONG_SIDE
3. END_SECTION
4. DIMENSION_AND_PARAMETRIC_LENGTH
5. PLACEMENT_AND_ENDPOINT_LOGIC
6. SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY

Panel 5 must visibly prove:
- same Master
- same 218.75 × 157.5 section
- TEST-A 1200 mm
- TEST-B 1500 mm
- same vertical direction
- no 1000 mm building-height leakage

## 7. Formal package

1. `CMP-FRAME-SHUZHU-001_MASTER_DEFINITION_V001.json`
2. `CMP-FRAME-SHUZHU-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-SHUZHU-001_MASTER_V001.blend` — Actions Artifact + local-only
4. `CMP-FRAME-SHUZHU-001_MASTER_REVIEW_BOARD_V001.png`
5. `CMP-FRAME-SHUZHU-001_MASTER_VALIDATION_V001.json`
6. this lifecycle record

## 8. Hard fails

- REFERENCE_LENGTH_LEAKS_INTO_BUILDING
- ENDPOINT_RESOLVER_LENGTH_MISMATCH
- ENDPOINT_RESOLVER_ORIENTATION_MISMATCH
- ENDPOINT_TEST_MARKED_AS_BUILDING_COORDINATE
- NONVERTICAL_TEST_POLICY_MISMATCH
- SILENT_HISTORICIZATION
- RECONSTRUCTED_DESIGN_MARKED_AS_DIRECT_MEASURED
- FALSE_GEOMETRY_VARIANT_FROM_PLACEMENT_ONLY
- UNSUPPORTED_JOINERY_CLAIM
- MASTER_WITHOUT_EVIDENCE_BINDING
- SHARED_V2_REGRESSION_FAILURE

Historical height UNKNOWN by itself is not a Hard Fail.

## 9. Delegated end-to-end authorization

Product Owner instruction: **“直接一次性完成下一构件：蜀柱的建立，直到全部完成”**.

D-116 interprets this as task-specific delegated authorization to:
- create branch / PR
- execute GitHub Actions / Blender 4.5.13
- repair implementation defects within the locked spec
- conditionally accept the first article when all locked source, visual and machine gates PASS
- exact-materialize approved outputs
- bind Catalog + V008
- run derived Excel and final regression
- mark PR Ready and merge if final checks PASS
- close T-029 on main

This does not authorize:
- weakening hard gates
- changing direct source facts silently
- resuming T-018
- starting Stage2

## 10. Engineering implementation start

D-116 execution started on branch `codex/t029-p3-3-shuzhu-master-v2-v001`.

Shared infrastructure change required:
- endpoint fixture direction variation becomes Definition-driven;
- backward-compatible default remains `directions_must_differ=true`;
- T-029 declares `directions_must_match=true`;
- mandatory regressions expanded to T-025 / T-026 / T-027 / T-028.

## 11. Source transcription correction / D-117

Before first-article acceptance, cross-check against the V008 Stage1 disposition audit corrected one A1 Table 2-46 transcription:

- 东缝: 218 × 158 mm
- 东山: 220 × 未及
- 西缝: 220 × 157 mm
- 西山: 217 × 未及
- width mean = 218.75 mm
- measured thickness mean = (158 + 157) / 2 = 157.5 mm
- source numeric conflict = FALSE
- canonical section remains 218.75 × 157.5 mm

Both gable thickness rows are unmeasured. No direct 157.5 mm West-Gable thickness claim is retained.

First article Run `35845395762` started before this correction entered the Definition. Regardless of its eventual technical result, it is classified:

`SUPERSEDED_PRE_D117_SOURCE_CORRECTION`

It must not be used for first-article acceptance or formalization. A new run from the corrected Definition is mandatory.

## 12. Run #1 failure analysis + generic registry-section fix

Superseded pre-correction Run `35845395762` also exposed a shared-validator assumption at:

`10_registry_section_binding`

Root cause:
- legacy validator expected every Registry row either to contain the canonical numeric section or explicitly say it inherited measured statistics;
- Shuzhu V008 intentionally preserves measurement state instead:
  - 2 interior rows: `广厚有直接实测`
  - 2 gable rows: `广有实测；厚未及`
- forcing a numeric gable thickness into Registry would violate D-117 and the pre-existing V008 audit.

Fix:
- add generic Definition-driven `registry_section_binding_contract`;
- mode `SEMANTIC_MEASUREMENT_STATE_WITH_MASTER_MEAN` verifies 2 measured-full rows + 2 thickness-UNKNOWN rows;
- verifies that UNKNOWN remains explicit;
- verifies canonical 218.75 × 157.5 mm comes from the A1 table published/recomputed mean rather than silently filling gable measurements;
- legacy Definitions retain the old numeric/inherited binding rule.

Corrected Run `35846114260`, which started before this validator fix, is also **SUPERSEDED_FOR_KNOWN_VALIDATOR_COMPATIBILITY_GAP** and must not be accepted. A fresh run is required.

## 13. First-article Run #3｜Validator uncertainty-boundary mismatch

Run `35846386214` completed:
- Blender 4.5.13 install = PASS
- canonical Master build = PASS
- independent reopen = PASS
- length/width/thickness mutation = PASS
- INTERIOR_FRAME / GABLE_FRAME role mutation = PASS
- six-panel Review Board = PASS

It stopped at validator check `33_unknowns_preserved`.

Cause:
- the shared validator requires an explicit `sample-to-instance` uncertainty phrase;
- Shuzhu Definition already preserves the real boundary as A1 table location labels + V008 closure, but the unknowns array did not repeat that phrase.

Patch:
- add an explicit statement that sample-to-instance correspondence is position-labeled by A1/V008 closure while no additional historical identity provenance is claimed;
- no geometry, section, count, role, endpoint fixture, or source measurement value changes.

Classification:
- `VALIDATOR_UNCERTAINTY_BOUNDARY_TEXT_MISMATCH`
- Run #3 is superseded and cannot be accepted because main validation/regressions did not finish.


## 14. D-118 delegated conditional acceptance + formalization

Run 35847859509 completed all locked gates: Blender/build/reopen/mutations, 79 machine checks, six-panel Review Board, and shared T-025/T-026/T-027/T-028 regression. Under D-116 delegated conditional acceptance, exact Artifact 10744639697 is accepted.

Exact accepted identities:
- .blend SHA-256 becf3323c0ff02606abdbb04e15be550f7c5d4dd74a8d5b9f4bd9adef53c10b6 — Actions Artifact/local-only, NOT Git
- Semantic SHA-256 3327a95918d61c0ed830fb49a46042c88cb9be2b36a64b958e29918529d2cd93
- Validation SHA-256 5cfe4c5086d847e7c1f34b6ff7ea6488b20b7f9381d55e0c5fb063b5cfe6a5cb
- Review Board SHA-256 8fc89aed2ad0f0329bceb890e9a5350bac6d2aea22de2d92d34d935fa3db7d64

Run 35860705896 materialized the three formal repo outputs byte-for-byte and verified the .blend SHA without committing it. Catalog candidate = 15 approved; V008/CURRENT and versioned V008 = 4/4 蜀柱 bound; approved-master-covered Registry records = 123; Stage1 candidate = 15/28 = 53.6%. Final latest-head regression, Excel sync, pre-merge cross-check and merge remain required before closure.

## 18. Delegated first-article acceptance / D-118

Under D-116 Product Owner end-to-end delegation, the first article was accepted only after all locked gates passed.

Accepted first article:
- Run: `35847859509` — SUCCESS
- main validation: **79/79 PASS**
- shared regressions T-025/T-026/T-027/T-028: **PASS**
- minimal-sufficient surface: **PASS**
- canonical .blend SHA-256: `becf3323c0ff02606abdbb04e15be550f7c5d4dd74a8d5b9f4bd9adef53c10b6`
- semantic geometry signature: `301e5a8ecf45cdc586d701571be7415aa3eb9e3e0d02bbb8a6b82ebef3a64a40`
- Artifact: `10744639697`

D-117 source-transcription correction is included in the accepted Definition lineage.

## 19. Final closure / D-119

Formalization and publication:
- exact materialization Run `35860705896`: **SUCCESS**
- Catalog approved Masters: **15**
- V008/CURRENT Shuzhu binding: **4/4**
- approved-Master-covered Registry records: **123**
- Registry Excel Sync Run `35860792076`: **SUCCESS**

Final regression:
- Run `35860792123`: **SUCCESS**
- T-029 validation: **85/85 PASS**
- T-025/T-026/T-027/T-028 regressions: **PASS**
- minimal-sufficient surface: **PASS**
- regenerated .blend SHA-256: `09bbd5817f0e74c33f39a5a5998d1dfe05fcc56a374049a3f1292ab84be7aea0`
- geometry signature: `301e5a8ecf45cdc586d701571be7415aa3eb9e3e0d02bbb8a6b82ebef3a64a40`
- Artifact: `10752080958`
- Artifact ZIP SHA-256: `239e4c05b9b240281bc1aad61401985bb5e46276fd6b826d0fb3d9270f49e11b`

Approved canonical source remains D-118 first article:
- .blend SHA-256: `becf3323c0ff02606abdbb04e15be550f7c5d4dd74a8d5b9f4bd9adef53c10b6`
- final-regression regenerated binary is reproducibility evidence only.

Merge:
- PR #17: **MERGED**
- merge commit: `04d186bcfd0b4c898ea77f02ef0fec27f73bb08e`
- latest PR head: `bad852fab4234b3663b08b71cd16210cdb6c1401`
- delta from final-regression human head: derived Registry Excel outputs only

Final status:
- `T-029 = CLOSED / MERGED_TO_MAIN`
- Stage1 Master completion = **15/28 = 53.6%**
- current active engineering task = NONE
- T-018 remains HOLD
- Stage2 remains unauthorized

