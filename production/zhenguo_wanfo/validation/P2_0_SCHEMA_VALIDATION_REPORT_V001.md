# P2.0 Schema Validation Report V001

- Task: `T-005｜P2.0_SCHEMA_VALIDATION_V001`
- Date: 2026-09-12
- Scope: Evidence-aware Parameter Schema data layer only
- Python: 3.10.2
- Validator: `jsonschema` 4.26.0, `Draft202012Validator`

## Results

| Check | Expected | Result | Evidence |
|---|---:|---:|---|
| JSON Schema Draft 2020-12 parse/check | PASS | PASS | `Draft202012Validator.check_schema(...)` completed without error |
| Positive minimal four-class parameter set | PASS | PASS | Validator exit 0; all four classifications asserted by automated test |
| Negative 01: `UNKNOWN + DO_NOT_LOCK` with numeric value | FAIL | FAIL as intended | Validator exit 1 at `$.parameters.Z-006.value`: `3420 is not of type 'null'` |
| Negative 02: `REASONABLE_COMPLETION + is_replaceable=false` | FAIL | FAIL as intended | Validator exit 1 at `$.parameters.Z-005.is_replaceable`: `True was expected` |
| Read-only parameter reader smoke test | PASS | PASS | Reader exit 0; listed the six required columns for all four parameters; AST test confirms no `bpy` import |

Automated suite result: 4 tests passed (`python3 -m unittest -v production/zhenguo_wanfo/tests/test_schema_validation_v001.py`).

## Safety and scope audit

- No Blender process or API was invoked.
- The reader performs JSON input and terminal output only; it does not import `bpy` or generate geometry.
- No `.blend`, P0 POC, P1 evidence/classification, or `docs/project_control/*` file was created or modified by T-005.
- Known pre-existing untracked PDF, P0 local directories, and `.blend` files were left untouched.
- The Task Contract's pre-work `git pull --ff-only origin main` was attempted, but the managed environment rejected it because a repository-wide pull could update protected paths. Validation therefore used the current checked-out revision.

## Files created or modified by T-005

- `production/zhenguo_wanfo/scripts/validate_parameter_set.py`
- `production/zhenguo_wanfo/scripts/read_parameter_set.py`
- `production/zhenguo_wanfo/tests/test_schema_validation_v001.py`
- `production/zhenguo_wanfo/tests/fixtures/P2_0_INVALID_UNKNOWN_HARD_LOCK_V001.json`
- `production/zhenguo_wanfo/tests/fixtures/P2_0_INVALID_REASONABLE_COMPLETION_NON_REPLACEABLE_V001.json`
- `production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V001.md`

## Blockers

No blocker affects the schema-validation result. Repository synchronization could not be performed because the managed environment denied `git pull`; this is a provenance limitation, not a failed acceptance criterion.

## Engineering recommendation

**PASS** for T-005 schema data-layer validation. This recommendation supplies engineering evidence only and does not declare the P2.0 Gate PASS.
