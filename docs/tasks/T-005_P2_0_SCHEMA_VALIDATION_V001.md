# T-005｜P2.0_SCHEMA_VALIDATION_V001

Status: READY_FOR_LOCAL_EXECUTION  
Think Level: MEDIUM  
Phase/Gate: P2 / P2.0  
Date: 2026-09-12

## 1. Objective

Validate the new Evidence-aware Parameter Schema as an executable production data contract before any formal Blender geometry is generated.

This task is **data-layer validation only**. Do not create or modify formal Wanfo Hall geometry.

## 2. Inputs

- `docs/production/zhenguo_wanfo/P2_0_EVIDENCE_AWARE_PARAMETER_SCHEMA_V001.md`
- `production/zhenguo_wanfo/schema/evidence_aware_parameter_schema_v001.json`
- `production/zhenguo_wanfo/params/P2_0_MINIMAL_PARAMETER_SET_V001.json`
- `docs/evidence/zhenguo_wanfo/P1_3_FULL_CRITICAL_PARAMETER_CLASSIFICATION_V001.md`
- `docs/evidence/zhenguo_wanfo/P1_3_GATE_REVIEW_2026-09-12.md`

## 3. Task Contract

Work only under:

- `production/zhenguo_wanfo/validation/`
- `production/zhenguo_wanfo/scripts/`
- `production/zhenguo_wanfo/tests/`

Do **not** modify:

- `docs/project_control/*`
- P1 evidence/classification files
- P0 POC files
- Blender `.blend` files

Do not start formal Blender geometry.

## 4. Required Deliverables

### A. Schema validator

Create a lightweight validator, preferably Python, that:

1. loads `evidence_aware_parameter_schema_v001.json`;
2. validates a parameter-set JSON;
3. returns non-zero exit code on failure;
4. prints concise PASS/FAIL output and useful validation path/error message.

Prefer standard JSON Schema Draft 2020-12 validation. If Python package `jsonschema` is unavailable, report the dependency rather than weakening validation rules.

### B. Positive test

Validate:

`production/zhenguo_wanfo/params/P2_0_MINIMAL_PARAMETER_SET_V001.json`

Expected: PASS.

The set must demonstrate all four classes:

- CONFIRMED
- HIGH_CONFIDENCE_INFERENCE
- REASONABLE_COMPLETION
- UNKNOWN

### C. Negative test 01｜UNKNOWN hard lock

Create an invalid fixture derived from the minimal set where:

- `Z-006.classification = UNKNOWN`
- `Z-006.production_use = DO_NOT_LOCK`
- `Z-006.value` is changed from `null` to a number

Expected: FAIL.

### D. Negative test 02｜Reasonable completion not replaceable

Create an invalid fixture where:

- `Z-005.classification = REASONABLE_COMPLETION`
- `Z-005.is_replaceable = false`

Expected: FAIL.

### E. Reader smoke test

Create a read-only parameter reader that:

- loads the minimal parameter set;
- lists ID, parameter_key, value, classification, time_layer, production_use;
- does not import `bpy`;
- does not generate geometry;
- proves future Blender/Python code can consume the structured data.

### F. Validation report

Create:

`production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V001.md`

Report at minimum:

- Python version;
- validator/dependency version;
- positive test result;
- negative test 01 result;
- negative test 02 result;
- reader smoke test result;
- file list created/modified;
- blockers if any;
- final engineering recommendation: PASS / HOLD.

## 5. Acceptance Criteria

T-005 may report PASS only if all are true:

1. Schema file parses successfully as JSON Schema Draft 2020-12;
2. minimal four-class parameter set validates PASS;
3. UNKNOWN hard-lock fixture validates FAIL for the intended rule;
4. REASONABLE_COMPLETION non-replaceable fixture validates FAIL for the intended rule;
5. reader smoke test reads the parameter set without geometry generation;
6. P0 files are unchanged;
7. `docs/project_control/*` are unchanged;
8. no `.blend` is created or modified.

## 6. Git / Safety

Before work:

```bash
cd "/Users/caroline/中国古建筑3D复原"
git pull --ff-only origin main
git status
```

Do not delete or add the known local-only untracked P0/PDF/Blender assets.

At completion, report `git status --short` and list all files created/modified by T-005.

Do not update Project Control; ChatGPT will review results and perform Gate bookkeeping after the engineering evidence is available.

## 7. Expected Gate Effect

T-005 PASS does not automatically close P2.0. It provides the engineering evidence for P2.0 Gate Review. ChatGPT/Product Owner still performs the final P2.0 acceptance decision.
