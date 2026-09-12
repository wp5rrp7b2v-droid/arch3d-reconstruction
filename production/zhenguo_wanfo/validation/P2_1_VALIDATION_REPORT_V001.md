# P2.1 Formal Production Parameter Set｜Validation Report V001

Status: **ENGINEERING HOLD**
Date: 2026-09-12
Scope: T-006; data, dependency, and read-only Python only

## Results

| Check | Result |
|---|---|
| Python | 3.10.2 |
| jsonschema | 4.26.0 |
| Formal production parameters | 85 / 85; exact P1.3 ID set and unique `parameter_key` |
| Classification counts | CONFIRMED 46; HIGH_CONFIDENCE_INFERENCE 32; REASONABLE_COMPLETION 4; UNKNOWN 3 |
| P2.0 JSON Schema | PASS |
| P1.3 classification / production-use / time-layer / source-layer / blocking-level match | PASS, all 85 |
| P1.2 V002 candidate value and unit match | PASS, all 85; Z-007 follows explicit P1.3 HR-01B project rule |
| Geometry Dependency Matrix | 85 / 85; exact parameter ID and key match |
| Dependency roles | DIRECT_GEOMETRY_INPUT 22; DERIVED_GEOMETRY_RULE 19; VALIDATION_REFERENCE 41; METADATA_ONLY 2; NOT_USED_IN_P2_2 1 |
| UNKNOWN null / status | PASS, all 3 |
| REASONABLE_COMPLETION replaceability | PASS, 4 / 4 (`Z-005`, `Z-007`, `ROOF-010`, `ROOF-011`) |
| Three-layer preservation | PASS; `observed_as_measured`, `report_ideal_model`, and `reconstructed_963_candidate` remain distinct. No locked P1.3 row belongs to `report_ideal_model`; no row was relabelled to create one. |
| Component originality metadata policy | PASS; `historical_state_tag`, `evidence_class`, `source_layer`, `originality_status` required; unknown is the default originality status |
| Automated tests | PASS, 11 / 11 (`python3 -m unittest discover -s production/zhenguo_wanfo/tests -p 'test_p2_1_production_parameter_set_v001.py' -v`) |
| Machine validation | PASS (`python3 production/zhenguo_wanfo/scripts/validate_p2_1_parameter_set.py --json`; exit 0) |
| Production preflight | **HOLD** (`python3 production/zhenguo_wanfo/scripts/p2_1_production_preflight.py --json`; exit 1) |
| Geometry-critical unresolved blocker count | **1** |
| Blender / `bpy` / formal geometry | No Blender process, `bpy` import, or formal geometry generation used; T-006 scripts are read-only and statically checked. |

## UNKNOWN dependency decisions

| ID / parameter_key | Status | Reason | Required before P2.2 |
|---|---|---|---|
| `Z-006` / `column_height_963_design_mm` | `BLOCKS_P2_2_GEOMETRY` | P2.2 includes columns, major frame, and roof control geometry. Their absolute Z placement needs a column-height input. P1 holds 963 design column height as UNKNOWN; an observed or secondary height cannot silently supply it. Relative topology can be defined but does not resolve full structural geometry. | **Yes.** New evidence or an explicit Product Owner decision for a separate replaceable temporary candidate is needed. |
| `DG-114` / `small_dou_unified_design_rule` | `BOUNDED_NON_BLOCKING` | P2.2 requires the bracket topology skeleton, not a precise unified design size for all small dou. The previously cited main-report p107 attribution was withdrawn. | No for P2.2 skeleton; resolve before detailed component locking. |
| `HIS-002` / `component_level_963_originality` | `METADATA_ONLY_BLOCK` | Per-component originality affects historical claims, not the P2.2 structural coordinates. Every unverified component must retain `originality_status=unknown`. | No for P2.2 geometry; required for claims of fully original 963 components. |

The P1.3 conditional-go assessment permits bounded relative structure and topology work. T-006 applies the narrower P2.2 dependency test required by its contract: an unknown column height is still an unresolved input for the complete column/frame/roof geometry. No value was added or reclassified to clear that dependency.

## Engineering recommendation

**HOLD.** Data migration, matrix coverage, machine validation, and tests are complete, but the geometry-critical unresolved blocker count is 1. DoD-04's unknown-resolution condition and the zero-blocker P2.1 entry condition are not met. This report is an engineering preflight result, not a P2.1 Gate decision. No P2.2 formal geometry should be generated from this parameter set while the blocker remains.

## Files created

- `production/zhenguo_wanfo/params/P2_1_FORMAL_PRODUCTION_PARAMETER_SET_V001.json`
- `production/zhenguo_wanfo/dependency/P2_1_GEOMETRY_DEPENDENCY_MATRIX_V001.json`
- `production/zhenguo_wanfo/scripts/validate_p2_1_parameter_set.py`
- `production/zhenguo_wanfo/scripts/p2_1_production_preflight.py`
- `production/zhenguo_wanfo/tests/test_p2_1_production_parameter_set_v001.py`
- `production/zhenguo_wanfo/validation/P2_1_VALIDATION_REPORT_V001.md`

All created files are versioned V001 where applicable. The canonical Git commit SHA and push result are recorded in the T-006 final report after archive.
