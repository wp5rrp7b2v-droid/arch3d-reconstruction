# P3.3 Building Input and Assembly Graph V001

This T-017 package compiles a semantic, evidence-aware whole-building baseline. It does **not** create geometry or invoke Blender.

## Inputs and boundary

The compiler reads the locked P3.0 registry, P3.1 Master Library, P3.2 schema and five relationship definitions, P2.1 formal parameters/approved overrides/dependency matrix, and the P2.3 integration manifest. P2.3 is accounting/comparison input only. Its `transform.location_mm`, `transform.rotation_euler_rad`, and `transform.scale` fields are deliberately never copied or read into generated placement rules.

The P2 baseline and all P3.0/P3.1/P3.2 inputs are read-only. Their SHA-256 values are recorded in the input baseline and checked by the validator. Unknown, proxy, control, envelope, deferred, and reasonable-completion states retain their evidence boundaries.

## Commands

Run from the repository root:

```bash
python3 production/zhenguo_wanfo/scripts/build_p3_3_building_graph_v001.py
python3 production/zhenguo_wanfo/scripts/validate_p3_3_building_graph_v001.py --write-report
python3 production/zhenguo_wanfo/scripts/build_p3_3_building_graph_v001.py --check
python3 -m unittest production.zhenguo_wanfo.tests.test_p3_3_building_graph_v001
```

The builder uses sorted keys, stable instance ordering, UTF-8, two-space indentation, and a terminal newline. `--check` recompiles in memory and rejects stale or non-deterministic committed outputs. The validator rejects all five T-017 Hard Fails and writes the canonical validation report only when requested.

## Outputs

The five canonical outputs are `P3_3_BUILDING_INPUT_BASELINE_V001.json`, `P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`, `P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json`, `P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`, and `P3_3_BUILDING_GRAPH_VALIDATION_V001.json` in this directory.
