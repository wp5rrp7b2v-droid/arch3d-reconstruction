# P3.3 Building Input and Assembly Graph V001

This T-017 package compiles a semantic, evidence-aware whole-building baseline. It does **not** create geometry or invoke Blender.

## Inputs and boundary

The compiler inventories the locked P3.0 identity/schema layer, P3.1 qualification/contract layer and approved Master snapshots, P3.2 node/interface/representative-assembly foundation, P2.1 evidence-aware parameters, approved overrides and dependency matrix. It models all four input classifications explicitly. P2.3 is `ACCOUNTING_REFERENCE_ONLY` and `COMPARISON_ONLY`; its `transform.location_mm`, `transform.rotation_euler_rad`, and `transform.scale` fields are individually declared `PROHIBITED_AS_GENERATIVE_INPUT` and are never copied into generated placement rules.

The P2 baseline and all P3.0/P3.1/P3.2 inputs are read-only. Their SHA-256 values are recorded in the input baseline and checked by the validator. Unknown, proxy, control, envelope, deferred, and reasonable-completion states retain their evidence boundaries.

Every formal parameter retains its evidence and time layer and binds to concrete organizational nodes, locked relationship types, and named rules. The graph hierarchy is `BUILDING_ROOT → ORG-BUILDING → assembly organization → runtime node`. It traces the validated P3.2 representative assembly units without inventing unsupported building-instance `SUPPORT` or `CONNECT` edges.

## Commands

Run from the repository root:

```bash
python3 production/zhenguo_wanfo/scripts/build_p3_3_building_graph_v001.py
python3 production/zhenguo_wanfo/scripts/validate_p3_3_building_graph_v001.py --write-report
python3 production/zhenguo_wanfo/scripts/build_p3_3_building_graph_v001.py --check
python3 -m unittest production.zhenguo_wanfo.tests.test_p3_3_building_graph_v001
```

The builder uses sorted keys, stable instance ordering, UTF-8, two-space indentation, and a terminal newline. `--check` recompiles twice and rejects stale or non-deterministic committed outputs. The validator mechanically derives every reported status from the generated assets, protected hashes, committed serialization, and five T-017 Hard Fail fixtures; it writes the canonical validation report only when requested.

## Outputs

The five canonical outputs are `P3_3_BUILDING_INPUT_BASELINE_V001.json`, `P3_3_BUILDING_PARAMETER_BINDINGS_V001.json`, `P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json`, `P3_3_BUILDING_ASSEMBLY_GRAPH_V001.json`, and `P3_3_BUILDING_GRAPH_VALIDATION_V001.json` in this directory.
