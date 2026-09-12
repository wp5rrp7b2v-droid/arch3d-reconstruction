# P2.0 Schema Validation Report V002

- Task: `T-005｜P2_0_SCHEMA_VALIDATION_V002`
- Date: 2026-09-12
- Scope: Evidence-aware Parameter Schema data layer only
- Python: 3.10.2
- Validator: `jsonschema` 4.26.0, `Draft202012Validator`

## Results

| Check | Expected | Result | Evidence |
|---|---:|---:|---|
| V001 positive four-class parameter set | PASS | PASS | Minimal set validated; exact set of four classifications asserted |
| V001 negative 01: numeric `UNKNOWN + DO_NOT_LOCK` | FAIL | FAIL as intended | Non-zero validator result at `$.parameters.Z-006.value` |
| V001 negative 02: non-replaceable `REASONABLE_COMPLETION` | FAIL | FAIL as intended | Non-zero validator result at `$.parameters.Z-005.is_replaceable` |
| V001 read-only reader smoke test | PASS | PASS | Four parameters and six required columns read; AST assertion confirms no `bpy` import |
| V002 three-layer coexistence fixture | PASS | PASS | One valid set contains three distinct IDs and semantic purposes; validator exit 0 |
| V002 reader exact layer preservation | PASS | PASS | Loader mapping and reader output exactly preserve all three expected ID-to-layer pairs |

Automated regression suite:

```text
Ran 6 tests in 16.206s
OK
```

Exact V002 layer mapping verified:

```text
PM-TL-OBS    -> observed_as_measured
MOD-TL-IDEAL -> report_ideal_model
Z-TL-963     -> reconstructed_963_candidate
```

The assertion compares the complete ID-to-layer mapping, the exact ID set, and the exact layer-value set. A merge, overwrite, relabel, missing ID, extra ID, or silent conversion therefore fails the test.

## Safety and scope audit

- No Blender process or API was invoked.
- The reader only reads JSON and emits text; it does not generate geometry.
- Static AST validation confirms the reader does not import `bpy`.
- No P0 POC, P1 evidence/classification, `docs/project_control/*`, or `.blend` file was changed.
- Known local-only PDF, P0 directories, and `.blend` assets were left untouched and excluded from the evidence archive.

## Files created or modified

Created for V002:

- `production/zhenguo_wanfo/tests/fixtures/P2_0_VALID_THREE_LAYER_COEXISTENCE_V001.json`
- `production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V002.md`

Extended for V002:

- `production/zhenguo_wanfo/tests/test_schema_validation_v001.py`

V001 engineering evidence retained for canonical Git archival:

- `production/zhenguo_wanfo/scripts/validate_parameter_set.py`
- `production/zhenguo_wanfo/scripts/read_parameter_set.py`
- `production/zhenguo_wanfo/tests/fixtures/P2_0_INVALID_UNKNOWN_HARD_LOCK_V001.json`
- `production/zhenguo_wanfo/tests/fixtures/P2_0_INVALID_REASONABLE_COMPLETION_NON_REPLACEABLE_V001.json`
- `production/zhenguo_wanfo/validation/P2_0_SCHEMA_VALIDATION_REPORT_V001.md`

## Blockers

None affecting validation. Git commit and normal push are performed after this report is written; any push limitation is reported in the task handoff without force-pushing.

## Engineering recommendation

**PASS** for T-005 V002 engineering validation and evidence archival, subject to the required scoped Git commit completing successfully. This is not a P2.0 Gate decision.
