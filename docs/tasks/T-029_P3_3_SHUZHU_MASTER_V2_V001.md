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

