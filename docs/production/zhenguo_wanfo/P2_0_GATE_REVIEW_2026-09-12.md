# P2.0｜Evidence-aware Parameter Schema｜Gate Review

Status: HOLD / T-005 V002 REQUIRED  
Date: 2026-09-12  
Gate: `P2.0｜Evidence-aware Parameter Schema`

## 1. Inputs Reviewed

- `docs/production/zhenguo_wanfo/P2_0_EVIDENCE_AWARE_PARAMETER_SCHEMA_V001.md`
- `production/zhenguo_wanfo/schema/evidence_aware_parameter_schema_v001.json`
- `production/zhenguo_wanfo/params/P2_0_MINIMAL_PARAMETER_SET_V001.json`
- T-005 V001 uploaded engineering outputs:
  - validator
  - read-only reader
  - automated tests
  - two negative fixtures
  - validation report V001

## 2. T-005 V001 Engineering Result

Engineering result: **PASS**.

Verified:

- Python 3.10.2;
- jsonschema 4.26.0;
- Draft 2020-12 schema check PASS;
- positive four-class parameter-set validation PASS;
- UNKNOWN + DO_NOT_LOCK hard-lock negative test fails as intended;
- REASONABLE_COMPLETION with `is_replaceable=false` fails as intended;
- reader smoke test PASS;
- no `bpy` import / no geometry generation.

The two machine constraints are genuinely encoded in the GitHub Schema through JSON Schema `if/then` rules, so the negative-test results are not superficial test-only assertions.

## 3. Gate Checklist

| Check | Result | Interpretation |
|---|---|---|
| Required evidence-aware fields exist | PASS | Schema contains value/unit/classification/time/source/production/blocking/source_ids/is_replaceable/notes |
| Four evidence classifications can be represented | PASS | V001 minimal set covers all four classes |
| UNKNOWN hard-lock is mechanically rejected | PASS | numeric value rejected for UNKNOWN + DO_NOT_LOCK |
| REASONABLE_COMPLETION must remain replaceable | PASS | `is_replaceable=false` rejected |
| Parameter reader can consume data without Blender geometry | PASS | read-only JSON reader, no `bpy` |
| Three semantic layers coexist and remain distinct | **NOT YET VALIDATED** | V001 examples include `observed_as_measured` and `reconstructed_963_candidate`, but no `report_ideal_model` coexistence fixture |
| Engineering validation evidence archived in canonical GitHub repo | **NOT YET** | six V001 outputs remain local untracked |

## 4. Gate Decision

**P2.0 = HOLD.**

This is not a schema design failure. T-005 V001 proves the core schema rules work. The hold exists because P2.0 Definition of Done requires explicit preservation of the three semantic layers:

1. `observed_as_measured`
2. `report_ideal_model`
3. `reconstructed_963_candidate`

and because formal engineering evidence should be committed into the canonical repository before final Gate approval.

## 5. Required Follow-up

Continue the same engineering task as:

`【中国古建筑3D复原｜T-005｜P2_0_SCHEMA_VALIDATION_V002｜证据感知参数架构验证】`

V002 must:

- add a valid three-layer coexistence fixture;
- assert exact preservation of all three `time_layer` values;
- rerun all V001 regression tests;
- archive T-005 engineering files to Git without adding known local-only PDF/P0/.blend assets.

Task spec:

`docs/tasks/T-005_P2_0_SCHEMA_VALIDATION_V002.md`

## 6. Production Boundary

Until V002 returns PASS and P2.0 receives Product Owner approval:

- P2.0 remains open;
- first formal Blender geometry remains locked;
- no P2.1 production work should start.
