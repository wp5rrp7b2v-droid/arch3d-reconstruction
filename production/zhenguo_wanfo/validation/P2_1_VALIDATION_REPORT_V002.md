# P2.1 Formal Production Parameter Set｜Validation Report V002

Status: **ENGINEERING PASS CANDIDATE**
Date: 2026-09-12
Scope: T-006 V002; D-023 production override and read-only preflight

## Baseline and candidate checks

| Check | Result |
|---|---|
| Python | 3.10.2 |
| jsonschema | 4.26.0 |
| V001 regression | PASS, original 11 / 11 tests |
| Formal Parameter Set | 85 / 85, unchanged |
| Historical classification counts | CONFIRMED 46; HIGH_CONFIDENCE_INFERENCE 32; REASONABLE_COMPLETION 4; UNKNOWN 3. RC-01 is outside this set. |
| P2.0 Schema and V001 source-backed validation | PASS |
| Z-006 historical parameter | `UNKNOWN / null / DO_NOT_LOCK`, unchanged |
| Z-006 dependency | `BLOCKS_P2_2_GEOMETRY`, unchanged |
| Z-006-RC-01 sidecar | PASS; exactly one independent approved override; `REASONABLE_COMPLETION`, `is_replaceable=true`, `D-023`, E-018 and HR-01A cited |
| MOD-006 current value | ≈321.3 mm, read from the formal parameter set |
| Formula recomputation | `11 × MOD-006 = 11 × 321.3 = 3534.3 mm`; matches sidecar current resolved value |
| Historical geometry-critical unknown count | 1 (`Z-006`) |
| Approved candidate resolution count | 1 (`Z-006-RC-01` resolves the P2.2 production input only) |
| Geometry-critical unresolved blocker count | 0 |
| Automated tests | PASS, 21 / 21: V001 11 / 11 plus V002 10 / 10, including mutation tests |
| Approved override machine validation | PASS (`python3 production/zhenguo_wanfo/scripts/validate_p2_1_approved_override.py --json`; exit 0) |
| Production preflight | PASS (`python3 production/zhenguo_wanfo/scripts/p2_1_production_preflight.py --json`; exit 0) |
| Blender / `bpy` / formal geometry | None used or generated; validation and preflight scripts are read-only and statically checked. |

The approved candidate is a formula-driven production override for `reconstructed_963_candidate`. Its 3534.3 mm result is not an established 963 historical column height. Replacing or withdrawing RC-01 does not rewrite the historical Z-006 record or its geometry dependency. If MOD-006 changes, the old cached result fails validation until recomputed; the changed formal MOD-006 itself still requires source-backed review.

## Negative validation

Mutation tests confirm HOLD or validation failure for a missing/extra override; altered Z-006 value, classification, or production use; a nonblocking Z-006 dependency; wrong candidate identity, target, D-023 approval, classification, time layer, production use, status, or replaceability; changed formula, dependency, or multiplier; stale/non-numeric resolved value; missing evidence citation or historical-claim boundary; and accidental insertion of RC-01 into the original 85 parameters.

## Engineering recommendation

**PASS for T-006 V002 engineering preflight.** The historical UNKNOWN remains 1, while the D-023-approved replaceable candidate resolves the sole P2.2 production input blocker, leaving 0 unresolved geometry-critical blockers. This is not a P2.1 Gate decision; Gate Review and approval remain with ChatGPT and the Product Owner. No formal geometry was generated.

## Files created or modified

- Created `production/zhenguo_wanfo/params/P2_1_APPROVED_PRODUCTION_OVERRIDES_V001.json`
- Created `production/zhenguo_wanfo/scripts/validate_p2_1_approved_override.py`
- Modified `production/zhenguo_wanfo/scripts/p2_1_production_preflight.py`
- Modified `production/zhenguo_wanfo/scripts/validate_p2_1_parameter_set.py` to include the new read-only script in static checks
- Created `production/zhenguo_wanfo/tests/test_p2_1_approved_override_v002.py`
- Created `production/zhenguo_wanfo/validation/P2_1_VALIDATION_REPORT_V002.md`

The V001 formal parameter set, dependency matrix, and V001 validation report remain unchanged. The Git commit SHA and push result are recorded in the T-006 V002 final report after archiving.
