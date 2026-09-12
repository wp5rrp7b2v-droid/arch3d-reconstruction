# 【中国古建筑3D复原｜T-005｜P2_0_SCHEMA_VALIDATION_V002｜证据感知参数架构验证】

Status: READY_FOR_LOCAL_EXECUTION  
Think Level: MEDIUM  
Phase/Gate: P2 / P2.0  
Date: 2026-09-12  
Supersedes execution instructions in: `T-005_P2_0_SCHEMA_VALIDATION_V001.md` for the remaining validation gap only.

## 1. Why V002

T-005 V001 engineering checks PASS:

- Draft 2020-12 schema validation PASS;
- four classification examples PASS;
- UNKNOWN + DO_NOT_LOCK numeric hard-lock rejected as intended;
- REASONABLE_COMPLETION + `is_replaceable=false` rejected as intended;
- read-only reader smoke test PASS;
- no Blender geometry generated.

P2.0 Gate Review found one remaining Definition-of-Done gap:

> V001 did not explicitly validate that `observed_as_measured`, `report_ideal_model`, and `reconstructed_963_candidate` can coexist in one parameter set without being merged, overwritten, or semantically re-labeled.

V001 engineering evidence files are also still local untracked and must be archived into the canonical GitHub repository before final Gate approval.

This is the same task objective, therefore it remains **T-005** and increments only to **V002**.

## 2. Scope

Work only under:

- `production/zhenguo_wanfo/scripts/`
- `production/zhenguo_wanfo/tests/`
- `production/zhenguo_wanfo/validation/`

Do not modify:

- `docs/project_control/*`
- P1 evidence/classification files
- P0 POC files
- Blender `.blend` files

Do not generate formal Blender geometry.

## 3. Required V002 Validation

### A. Three-layer coexistence fixture

Create a valid fixture containing at least one parameter in each semantic layer:

1. `observed_as_measured`
2. `report_ideal_model`
3. `reconstructed_963_candidate`

The three entries must use distinct parameter IDs and distinct semantic purposes. Do not represent the same layer by renaming another layer.

Recommended fixture path:

`production/zhenguo_wanfo/tests/fixtures/P2_0_VALID_THREE_LAYER_COEXISTENCE_V001.json`

Expected: Schema validation PASS.

### B. Three-layer reader assertion

Extend the automated suite so the reader/loader proves all three layer labels are preserved exactly after loading.

Acceptance check:

- all three expected `time_layer` values exist;
- none is silently converted to another layer;
- distinct parameter IDs remain distinct;
- no geometry generation / no `bpy` import.

### C. Preserve V001 tests

All V001 checks must continue to PASS:

- positive four-class set;
- UNKNOWN hard-lock negative test;
- REASONABLE_COMPLETION non-replaceable negative test;
- reader smoke test.

### D. Validation report V002

Create:

`production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V002.md`

Report:

- Python version;
- jsonschema version;
- all V001 test results;
- three-layer coexistence test result;
- three-layer reader preservation result;
- files created/modified;
- blocker if any;
- final engineering recommendation PASS / HOLD.

## 4. Evidence Archive Requirement

After tests PASS, add to Git only the T-005 engineering deliverables under:

- `production/zhenguo_wanfo/scripts/`
- `production/zhenguo_wanfo/tests/`
- `production/zhenguo_wanfo/validation/`

Do **not** add the known local-only PDF, P0 local directories, or `.blend` files.

Commit with a concise message such as:

`p2.0: validate evidence-aware parameter schema`

Push to `origin main` only if normal fast-forward push is available. If push is blocked, report the exact blocker and stop; do not force.

## 5. Acceptance Criteria

T-005 V002 may report PASS only if all are true:

1. all V001 automated checks still PASS;
2. three semantic layers coexist in one valid fixture;
3. reader preserves all three exact `time_layer` values;
4. no `bpy` import and no geometry generation;
5. no P0/P1/Project Control files changed;
6. T-005 engineering evidence is committed to Git;
7. known local-only untracked assets remain untouched.

## 6. Final Report Format

Return only:

- STATUS: PASS / HOLD
- Python version
- jsonschema version
- V001 regression result
- Three-layer coexistence result
- Three-layer reader preservation result
- Files created/modified
- Commit SHA
- Push result
- `git status --short`
- blocker if any
- engineering recommendation

Do not declare P2.0 Gate PASS. ChatGPT + Product Owner retain Gate authority.
