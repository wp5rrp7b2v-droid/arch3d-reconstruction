# 【中国古建筑3D复原｜T-030｜P3_3_DAJIAOLIANG_MASTER_V2_V001｜大角梁 Master 首件生产】

Status: **TASK CONTRACT V001 LOCKED / PRODUCT OWNER APPROVED / D-125 / ENGINEERING EXECUTION AUTHORIZED / D-126**  
Think Level: **HIGH**  
Execution architecture: **MASTER V2 / MINIMAL_SUFFICIENT / INSTANCE-SECTION-PARAMETRIC / ENDPOINT-DRIVEN**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-24  
Proposed branch: `codex/t030-p3-3-dajiaoliang-master-v2-v001`  
PR policy: **ONE TASK = ONE BRANCH = ONE PR / DO NOT CREATE UNTIL EXECUTION AUTHORIZED**

## 1. Objective

建立并验证一个 reusable 大角梁 canonical Master：

- component id: `CMP-FRAME-DAJIAOLIANG-001`
- master id: `CMP-FRAME-DAJIAOLIANG-001_MASTER`
- master version: `V001`
- physical instances: **4**
- locations: 东南 / 东北 / 西南 / 西北
- geometry variant count: **0**

核心工程目标：

> 用一个 shared parametric Master 保留稳定角梁本体；四个建筑实例使用 A1 直接测得的不同截面参数；实际长度与朝向由 assembly endpoints 推导。不得用 family mean 覆盖实例实测，不得为四角复制四个 Master。

## 2. Authoritative Inputs

### A1｜一级工程主权

`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct binding:
- PDF p88–89 / printed p73–74
- §2.3.1.7｜角梁
- Fig. 2-50
- Table 2-44
- canonical PDF SHA-256 = `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Formal evidence:
`docs/evidence/zhenguo_wanfo/P3_3_DAJIAOLIANG_DIRECT_SOURCE_BINDING_V001.md`

### A2｜官方同建筑视觉/结构

山西文物数字博物馆·万佛殿专题与既有 P1 evidence records。

Allowed semantic use:
- corner-beam support/topology
- same-building visual/form cross-check

Not dimensional authority for:
- exact full length
- exact 45° node coordinates
- exact slope
- exact joinery

### Canonical project inputs

- `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- `docs/production/zhenguo_wanfo/P3_3_STAGE1_DAJIAOLIANG_MASTER_SPEC_V001.md`
- `production/zhenguo_wanfo/registry/P3_3_STAGE1_DAJIAOLIANG_MASTER_SPEC_V001.json`

Decision chain:
- D-076 Pre-Model Visual Reference Gate
- D-099 / RC-019 source authority
- D-108 / RC-020 Evidence-Constrained Reconstruction
- D-123 / RC-021 / RC-022 process correction
- D-124 大角梁 Source + Visual Gate + Master Spec V001
- D-125 T-030 Task Contract lock

## 3. Locked Measurement / Instance Mapping

A1 direct measured sections:

- 东南角 / 东南大角梁 = **240 × 210 mm**
- 东北角 / 东北大角梁 = **216 × 187 mm**
- 西南角 / 西南大角梁 = **218 × 206 mm**
- 西北角 / 西北大角梁 = **226 × 199 mm**

Report-published family mean:
- width = **225 mm**
- thickness = **200.5 mm**

Independent recompute:
- width = **225 mm**
- thickness = **200.5 mm**

Locked source status:
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = FALSE`
- `sample_to_instance_mapping = DIRECT_LOCKED`

The mean is a family statistic / reference specimen dimension. It must not replace the four direct instance sections.

## 4. Canonical Family Reference Geometry

Geometry mode:
`PARAMETRIC_ENDPOINT_DRIVEN_LONG_MEMBER_WITH_INSTANCE_SECTION_PARAMETERS`

Canonical reference body:
- X = **1000 mm**
- Y = **225 mm**
- Z = **200.5 mm**

Axes:
- +X = longitudinal
- +Y = 广 / width
- +Z = 厚 / thickness

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform:
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

1000 mm classification:
- `RECONSTRUCTION_REFERENCE_LENGTH`
- non-historical
- replaceable
- Master specimen only
- must never become building instance length by default

225 × 200.5 classification:
- `DIRECT_MEASURED_REPORT_FAMILY_MEAN`
- family reference specimen only
- must never overwrite direct instance section parameters

## 5. Instance Section Contract

The same Master definition must produce all four measured sections through parameters.

Required mapping:

| location | width mm | thickness mm |
|---|---:|---:|
| 东南角 | 240 | 210 |
| 东北角 | 216 | 187 |
| 西南角 | 218 | 206 |
| 西北角 | 226 | 199 |

Rules:
- same component_id/master_id for all four
- instance section difference is not a Master duplication
- instance section difference is not a Geometry Variant
- direct mapping is immutable without new A1 evidence or Product Owner decision
- family mean may be used for canonical specimen/review baseline only

No separate formal .blend is created for each corner.

## 6. Endpoint Resolver Contract

For each placement:

`V = P_end - P_start`  
`L = ||V||`  
`P_center = (P_start + P_end) / 2`

Local +X aligns to `V`.

Therefore:
- actual length = endpoint-derived
- actual orientation = endpoint-derived
- actual installation angle = endpoint-derived
- Master stores no fixed historical full length
- Master stores no fixed 45° installation angle

Endpoint values may later be `RECONSTRUCTED_DESIGN` when derived from whole-building geometry, but Stage1 does not lock the four final Wanfodian endpoint coordinates.

## 7. Deterministic Endpoint Proof Fixtures

Fixtures are:

`ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES / NON_HISTORICAL`

### TEST-A
- P_start = (0,0,0)
- P_end = (300,400,1200)
- expected length = **1300 mm**
- expected center = **(150,200,600)**
- expected normalized direction = **(3/13,4/13,12/13)**

### TEST-B
- P_start = (0,0,0)
- P_end = (640,480,1500)
- expected length = **1700 mm**
- expected center = **(320,240,750)**
- expected normalized direction = **(32/85,24/85,15/17)**

Both must prove:
- same Master identity
- different derived length
- different derived direction
- no fixed 45° Master angle
- no 1000 mm leakage
- coordinates are not Wanfodian physical coordinates

Section proof is independent of endpoint proof: the resolver must not overwrite the direct measured section parameters.

## 8. Stage Boundary

T-030 Stage1 validates:
- one reusable Master identity
- four direct instance-section parameter mappings
- endpoint-driven length/orientation capability
- source/reconstruction boundary
- medium-precision outer envelope

T-030 must not hard-code final building endpoint XYZ.

The four final placements belong to later whole-building spatial/assembly stages.

## 9. End / Joinery Boundary

Stage1 V001:
- `STRUCTURAL_SIMPLIFIED_FLAT_END`
- historical end profile = `UNRESOLVED_METADATA`
- mortise/tenon = `NOT_MODELED_AT_STAGE1`
- notch/groove = `NOT_MODELED_AT_STAGE1`

No direct evidence = no historical detailed cut claim.

## 10. Related Component Isolation

T-030 covers 大角梁 only.

Must not absorb:
- 子角梁
- 隐角梁
- 隐衬角栿 / 递角栿
- 翼角椽

Current Registry policy for these related identities remains unchanged.

## 11. Shared Master V2 Infrastructure Rule

Reuse first:
- `production/zhenguo_wanfo/scripts/p3_3_master_v2_common.py`
- `production/zhenguo_wanfo/scripts/validate_p3_3_master_v2.py`
- `.github/workflows/p3_3_master_v2.yml`

Default engineering expectation:
- reuse existing width/thickness mutation capability
- reuse existing endpoint resolver contract
- reuse existing adaptive Review Board pipeline

Do **not** add new shared infrastructure if the current Definition-driven pipeline can express the locked contract.

If exact instance-section mapping validation cannot be expressed by the current generic schema, a minimal generic `instance_section_binding_contract` extension is permitted only after execution authorization.

Any such extension must be:
- Definition-driven
- reusable
- minimal
- not 大角梁-specific
- not a new workflow
- not a parallel authority / cache / index

Forbidden:
- 大角梁-only validator
- 大角梁-only workflow
- four corner-specific builder scripts
- permanent derived source cache

## 12. Shared Regression Protection

If shared Master V2 infrastructure changes, mandatory regression:
- T-025｜剳牵
- T-026｜槫
- T-027｜托脚
- T-028｜叉手
- T-029｜蜀柱

All must PASS before T-030 may be engineering-complete.

If no shared infrastructure changes, T-030 must still pass its full locked validation and deterministic rebuild/reopen checks.

## 13. Adaptive Review Board

Formal review output:
`CMP-FRAME-DAJIAOLIANG-001_MASTER_REVIEW_BOARD_V001.png`

Required panels:
1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION`
4. `DIMENSION_AND_PARAMETRIC_LENGTH`
5. `PLACEMENT_AND_ENDPOINT_LOGIC`
6. `SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY`

END_SECTION must visibly show:
- 225 × 200.5 family reference specimen
- SE 240×210
- NE 216×187
- SW 218×206
- NW 226×199
- same Master / zero Geometry Variant
- family mean does not overwrite instance data

PLACEMENT_AND_ENDPOINT_LOGIC must visibly show TEST-A and TEST-B:
- endpoint coordinates
- derived length
- derived direction
- no fixed 45° claim
- no building-coordinate claim

SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY must separate:

Evidence locked:
- component identity
- 4 instances
- four location-specific measured sections
- family mean
- A1 Fig. 2-50 visual/form reference
- corner-beam structural topology

Reconstructed design:
- final endpoint placement
- final derived length
- final orientation
- simplified end treatment

Not claimed:
- exact 963 full length
- exact 963 45° node geometry
- exact historical joinery
- exact hidden-corner-beam relationship
- exact component originality

## 14. Minimal-Sufficient Formal Package

Expected component-specific outputs:

1. `CMP-FRAME-DAJIAOLIANG-001_MASTER_DEFINITION_V001.json`
2. `CMP-FRAME-DAJIAOLIANG-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-DAJIAOLIANG-001_MASTER_V001.blend` — Actions Artifact + local-only
4. `CMP-FRAME-DAJIAOLIANG-001_MASTER_REVIEW_BOARD_V001.png`
5. `CMP-FRAME-DAJIAOLIANG-001_MASTER_VALIDATION_V001.json`
6. this lifecycle record

Do not create redundant standalone source extracts, endpoint-fixture reports, section-fixture binaries, caches or indexes. Their facts belong in Definition/Semantic/Validation/Review Board.

## 15. Validation Contract

Machine validation must cover at least:

### Identity / Registry
1. task/component/master/version identity
2. V008/CURRENT authority
3. physical instances = 4
4. four Registry IDs/locations traceable
5. one shared Master
6. geometry variant count = 0

### A1 direct measurement
7. SE = 240×210
8. NE = 216×187
9. SW = 218×206
10. NW = 226×199
11. direct location mapping preserved
12. report mean width = 225
13. report mean thickness = 200.5
14. recomputed mean width = 225
15. recomputed mean thickness = 200.5
16. source internal numeric conflict = false
17. sample-to-instance mapping = DIRECT_LOCKED
18. fen values remain metadata only

### Canonical / instance geometry
19. reference length = 1000 / non-historical
20. family reference section = 225×200.5
21. family mean marked reference specimen only
22. canonical bbox = 1000×225×200.5
23. canonical origin/transform
24. same Master can build SE 240×210
25. same Master can build NE 216×187
26. same Master can build SW 218×206
27. same Master can build NW 226×199
28. section parameter mutation isolates Y/Z
29. no duplicate Master per corner
30. no false Geometry Variant from instance section differences
31. direct instance sections not collapsed to family mean

### Endpoint resolver
32. endpoint resolver enabled/reused
33. TEST-A length = 1300
34. TEST-A center = (150,200,600)
35. TEST-A direction = (3/13,4/13,12/13)
36. TEST-B length = 1700
37. TEST-B center = (320,240,750)
38. TEST-B direction = (32/85,24/85,15/17)
39. TEST-A/B directions differ
40. TEST-A/B lengths differ
41. same Master identity used
42. fixture coordinates marked NOT_BUILDING_COORDINATES
43. no fixed Master installation angle
44. no fixed historical 45° claim
45. no 1000 mm leakage into endpoint-derived instances
46. endpoint resolver does not overwrite instance section parameters

### Evidence / boundary
47. D-076 visual gate traceable
48. A1 source binding traceable
49. A2 semantic layer traceable
50. 子角梁 excluded
51. 隐角梁 excluded
52. 隐衬角栿 / 递角栿 excluded
53. simplified flat end explicit
54. no unsupported joinery
55. no silent historicization
56. reconstructed design not marked DIRECT_MEASURED

### Reproducibility / delivery
57. Blender 4.5.13 LTS
58. independent reopen PASS
59. deterministic semantic restore
60. Definition↔Semantic identity
61. binary SHA recorded
62. all Definition-required Review Board panels complete
63. canonical .blend not tracked in Git Master directory
64. minimal-sufficient formal surface PASS
65. D-099 / RC-019 / D-108 / RC-020 / D-124 / D-125 traceable

### Shared regression
66. T-025 regression PASS if shared infrastructure changed
67. T-026 regression PASS if shared infrastructure changed
68. T-027 regression PASS if shared infrastructure changed
69. T-028 regression PASS if shared infrastructure changed
70. T-029 regression PASS if shared infrastructure changed

Exact atomic check count may exceed 70. No required information domain may be removed merely to reduce count.

## 16. Hard Fails

- `INSTANCE_SECTION_COLLAPSED_TO_FAMILY_MEAN`
- `INSTANCE_SECTION_MAPPING_MISMATCH`
- `DUPLICATE_MASTER_PER_CORNER`
- `FALSE_GEOMETRY_VARIANT_FROM_INSTANCE_SECTION_ONLY`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `ENDPOINT_RESOLVER_LENGTH_MISMATCH`
- `ENDPOINT_RESOLVER_ORIENTATION_MISMATCH`
- `ENDPOINT_TEST_MARKED_AS_BUILDING_COORDINATE`
- `FIXED_MASTER_INSTALLATION_ANGLE`
- `FIXED_45_DEGREE_HISTORICAL_CLAIM`
- `SILENT_HISTORICIZATION`
- `RECONSTRUCTED_DESIGN_MARKED_AS_DIRECT_MEASURED`
- `UNSUPPORTED_JOINERY_CLAIM`
- `RELATED_COMPONENT_IDENTITY_COLLAPSE`
- `MASTER_WITHOUT_EVIDENCE_BINDING`
- `MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`
- `SHARED_V2_REGRESSION_FAILURE`

Historical full length / exact historical angle remaining UNKNOWN is explicitly **NOT** a Hard Fail.

## 17. Exception / Blocker Handling

RC-021 / RC-022 apply.

If the approved execution path becomes blocked:
1. immediately change status from EXECUTING to BLOCKED;
2. report blocker, completed progress, effect on original task, and recommended path;
3. troubleshooting is exception handling, not normal task execution time;
4. any workaround that adds infrastructure, expands scope, changes workflow or changes locked architecture requires Product Owner approval first;
5. only after explicit `BLOCKER CLEARED` may T-030 return to EXECUTING.

No silent prolonged troubleshooting.

## 18. Protected Boundaries

T-030 must not:
- reactivate T-018 / PR #3 / PR #6
- start Stage2
- alter T-020 / RZ / FV authority
- reopen P2 frozen baseline
- create final whole-building corner coordinates in Stage1
- hard-code 45° historical placement
- merge 大角梁 with 子角梁 / 隐角梁 / 隐衬角栿
- create source caches / OCR databases / parallel evidence authorities
- weaken T-025–T-029 approved semantics

T-018 remains HOLD.

## 19. Authorization Boundary｜D-125

D-125 locks this Task Contract only.

Current authorization:
- `TASK_CONTRACT_LOCKED = TRUE`
- `ENGINEERING_EXECUTION_AUTHORIZED = FALSE`
- `BLENDER_EXECUTION_AUTHORIZED = FALSE`
- `PRODUCTION_BRANCH_CREATION_AUTHORIZED = FALSE`
- `PR_CREATION_AUTHORIZED = FALSE`

To begin engineering, Product Owner must explicitly authorize:

> **开始 T-030**

Only after that authorization may:
- branch `codex/t030-p3-3-dajiaoliang-master-v2-v001` be created;
- locked execution Definition be created/finalized with execution=true;
- Draft PR be opened;
- GitHub Actions / Blender 4.5.13 execute;
- a minimal generic shared-V2 extension be introduced if demonstrably necessary;
- first-article evidence be generated.

First-article acceptance, formal materialization/Catalog+V008 binding, PR merge, Stage1 PASS, Stage2 and T-018 resume remain separate authorization boundaries unless Product Owner later grants explicit delegated end-to-end authority.

## 20. Engineering execution authorization / D-126

Product Owner explicitly authorized **开始 T-030** on 2026-09-24.

Authorized:
- engineering execution = true
- Blender/GitHub Actions execution = true
- production branch = `codex/t030-p3-3-dajiaoliang-master-v2-v001`
- Draft PR creation = true
- locked execution Definition creation = true
- minimal generic Definition-driven `instance_section_binding_contract` extension to shared Master V2 infrastructure if demonstrably necessary

Mandatory shared regression if shared infrastructure changes:
- T-025 剳牵
- T-026 槫
- T-027 托脚
- T-028 叉手
- T-029 蜀柱

Still requires separate Product Owner authorization:
- first-article acceptance
- formal materialization / Catalog + V008 approved binding
- PR merge
- Stage1 PASS / Stage2
- T-018 resume


## 21. Product Owner first-article acceptance / D-128

Product Owner reviewed the formal Review Board and explicitly approved the T-030 first article on 2026-09-24.

Accepted evidence:
- Run `35977160199` attempt 3: **SUCCESS**
- main validation: **91/91 PASS**
- shared regression T-025..T-029: **ALL PASS**
- minimal formal artifact assertion: **PASS**
- first-article Artifact ID: `10800439343`
- shared regression Artifact ID: `10801150421`
- accepted canonical .blend SHA-256: `199e1dcf7274d732e26e430e80e171f9a2a4d0c55162fb6bb100fe51b681aa91`
- semantic geometry signature: `b38684fe6adac315a53e62c5d773f36c5eabb305b744e03627b1ac9814f32dc2`
- Semantic JSON SHA-256: `ef69a45735415c618bdfe995181d545e231674b12476af119f92b8d1da610617`
- Validation JSON SHA-256: `8ef4970b6b3b353c5b58a94248a6d978f5ac89e10e03e0ad82ebc9c155911062`
- Review Board SHA-256: `2398bff3922f3a6373a7160642d787e1b797911c758c558acfc4a92e58679fff`

This acceptance does **not** authorize formal materialization, Catalog/V008 approved binding, PR #18 merge, Stage1 PASS, Stage2, or T-018 resume.

## 22. D-129 formalization / publication closure authorization

Product Owner explicitly authorized T-030 formalization, Catalog + V008 binding, and PR #18 merge subject to final PASS gates.

Exact accepted Artifact materialization:
- one-time materialization Run: `35986418607` — **SUCCESS**
- source first-article Run: `35977160199` / attempt 3
- source Artifact: `10800439343`
- canonical .blend SHA-256 verified but **NOT COMMITTED TO GIT**: `199e1dcf7274d732e26e430e80e171f9a2a4d0c55162fb6bb100fe51b681aa91`
- exact Semantic SHA-256: `ef69a45735415c618bdfe995181d545e231674b12476af119f92b8d1da610617`
- exact Validation SHA-256: `8ef4970b6b3b353c5b58a94248a6d978f5ac89e10e03e0ad82ebc9c155911062`
- exact Review Board SHA-256: `2398bff3922f3a6373a7160642d787e1b797911c758c558acfc4a92e58679fff`
- one-time workflow/helper removed in the same materialization commit.

Formalization candidate:
- Catalog approved count candidate: **16**
- V008/CURRENT 大角梁 binding: **4/4** to `CMP-FRAME-DAJIAOLIANG-001_MASTER`
- approved-Master-covered Registry records candidate: **127**
- Stage1 candidate: **16/28 = 57.1%**

Merge remains conditional on:
- Registry Excel Sync PASS
- latest-head T-030 Master V2 final validation PASS
- T-025..T-029 shared regression PASS
- minimal-sufficient surface PASS
- pre-merge cross-check PASS

Stage2 remains unauthorized and T-018 remains HOLD.

