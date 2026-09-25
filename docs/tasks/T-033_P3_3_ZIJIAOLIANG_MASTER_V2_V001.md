# 【中国古建筑3D复原｜T-033｜P3_3_ZIJIAOLIANG_MASTER_V2_V001｜子角梁 Master】

Status: **TASK CONTRACT LOCKED / D-143 / END-TO-END COMPONENT COMPLETION AUTHORIZED**  
Think Level: HIGH  
Architecture: **MASTER V2 / MINIMAL_SUFFICIENT / INSTANCE-SECTION-PARAMETRIC / ENDPOINT-DRIVEN**  
Stage: P3.3 V002 Stage 1  
Branch: `codex/t033-p3-3-zijiaoliang-master-v2-v001`

## Objective

Build one reusable:
- `CMP-FRAME-ZIJIAOLIANG-001`
- `CMP-FRAME-ZIJIAOLIANG-001_MASTER`
- V001
- 4 physical instances
- 0 geometry variants.

Preserve four direct extant-state sections and prevent the report family mean from overwriting instance measurements.

## Inputs

A1:
- SRC-ZG-WF-001
- PDF p88–89 / printed p73–74
- §2.3.1.7 / Fig.2-50 / actual Table 2-44
- source binding: `P3_3_ZIJIAOLIANG_DIRECT_SOURCE_BINDING_V001.md`

A2:
- official same-building corner-beam / 套兽 semantics.

Locked Spec:
`P3_3_STAGE1_ZIJIAOLIANG_MASTER_SPEC_V001.md`

## Measurements

- SE 220×150
- NE 190×153
- SW 213×153
- NW 125×149 mm

Published family reference:
- 216.5×152 mm
- `SOURCE_AGGREGATION_METHOD_AMBIGUOUS`
- reference only.

## Canonical geometry

- reference length 1000 mm / non-historical
- family reference section 216.5×152
- rectangular bounded envelope
- flat simplified ends
- actual building length/orientation endpoint-derived.

## Endpoint proof fixtures

Engineering-test coordinates only.

TEST-A:
- start (0,0,0)
- end (300,400,1200)
- length 1300
- center (150,200,600)
- direction (3/13,4/13,12/13)

TEST-B:
- start (0,0,0)
- end (640,480,1500)
- length 1700
- center (320,240,750)
- direction (32/85,24/85,15/17)

## RC-024 interface carry-forward

- outboard end → 套兽 attachment semantic, exact geometry deferred;
- inboard corner assembly → 大角梁/corner assembly relation known at family level, exact JOINERY_FEATURE vs CONTACT_INTERFACE deferred;
- no unsupported joint geometry may be baked into this Master.

## Shared infrastructure

Reuse:
- `p3_3_master_v2_common.py`
- `validate_p3_3_master_v2.py`
- `.github/workflows/p3_3_master_v2.yml`

No shared infrastructure change is expected.

## First-article acceptance

Must prove:
- 4 Registry instances;
- direct location mapping;
- family mean reference only;
- same Master reproduces 4 instance sections;
- replacement metadata does not create variants;
- endpoint resolver and reference-length guard;
- no fixed 45°;
- no unsupported joinery;
- D-076 traceability;
- deterministic reopen/restore;
- minimal-sufficient package.

## Completion authority

The Product Owner instruction **“继续完成子角梁”** authorizes this component to proceed end-to-end through:
- branch / PR;
- GitHub Actions / Blender first article;
- evidence review;
- if PASS, formalization;
- Catalog + V008/CURRENT binding;
- Registry Excel sync / final regression;
- Ready + merge;
- Project Control closure.

This authority does **not** authorize:
- Stage2;
- T-018;
- rewriting A1 evidence;
- exact 963 geometry claims.
