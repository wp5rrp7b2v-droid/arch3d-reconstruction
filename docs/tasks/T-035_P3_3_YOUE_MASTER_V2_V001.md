# 【中国古建筑3D复原｜T-035｜P3_3_YOUE_MASTER_V2_V001｜由额 Master】

Status: **TASK CONTRACT LOCKED / D-157 / ENGINEERING EXECUTION NOT AUTHORIZED**  
Think Level: HIGH  
Architecture: **MASTER V2 / MINIMAL_SUFFICIENT / DIRECT-SECTION-PARAMETRIC / HISTORICAL-ORIENTATION-AWARE / ASSEMBLY-ENDPOINT-DRIVEN**  
Stage: P3.3 V002 Stage 1  
Proposed branch: `codex/t035-p3-3-youe-master-v2-v001`

## 1. Objective

Build and validate one reusable canonical Master definition for:

- component id: `CMP-FRAME-YOUE-001`
- master id: `CMP-FRAME-YOUE-001_MASTER`
- master version: `V001`
- physical instances: **4**
- geometry variants: **0**

Core engineering objective:

> Preserve all four A1 direct instance sections, keep the historically flipped current orientation as semantic/history metadata rather than body geometry, prevent old mortise traces from being promoted into canonical joinery, and prove that all four instances remain one shared parametric Master whose actual building length is assembly-derived rather than copied from the 1000 mm reference specimen.

T-035 is a Stage1 Master task. It does not resolve exact 963 original top/bottom orientation, exact historical end joinery, concealed full timber length, or complete building placement.

## 2. Authoritative Inputs

### A1｜Primary engineering authority

`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct locator:
- PDF p86–88
- printed p71–73
- §2.3.1.6｜阑额、由额
- Table 2-43
- Fig. 2-46 / 2-47 / 2-49
- canonical PDF SHA-256: `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`

Formal evidence:
- `docs/evidence/zhenguo_wanfo/P3_3_YOUE_DIRECT_SOURCE_BINDING_V001.md`

### A2｜Official same-building visual / structural semantics

山西文物数字博物馆·万佛殿专题。

Allowed use:
- no 普拍枋;
- 阑额 / 由额 as intercolumn connecting members;
- same-building visual/form cross-check.

A2 is not authority for:
- exact hidden tenon/mortise geometry;
- exact full timber length;
- pre-repair original top/bottom orientation;
- per-instance 由额 section dimensions.

### Locked Spec

- `docs/production/zhenguo_wanfo/P3_3_STAGE1_YOUE_MASTER_SPEC_V001.md`
- `production/zhenguo_wanfo/registry/P3_3_STAGE1_YOUE_MASTER_SPEC_V001.json`

Decision chain:
- D-076 Pre-Model Visual Reference Gate
- D-099 / RC-019 source authority
- D-108 / RC-020 Evidence-Constrained Reconstruction
- D-137 / RC-023 historical-unknown non-blocking rule
- D-139 / RC-024 Connection Layer
- D-154 由额 Source Readiness
- D-155 由额 D-076 Visual/Form Gate
- D-156 由额 Master Spec V001
- D-157 T-035 Task Contract lock

## 3. Locked Instance Section Mapping

| Registry location | A1 label | width mm | thickness mm | classification |
|---|---|---:|---:|---|
| 南立面西次间 | 南西次间 | 255 | 105 | DIRECT_MEASURED |
| 南立面明间 | 南明间 | 245 | 105 | DIRECT_MEASURED |
| 南立面东次间 | 南东次间 | 250 | 105 | DIRECT_MEASURED |
| 北立面明间 | 北明间 | 259 | 105 | DIRECT_MEASURED |

Locked counts:
- direct width = **4 / 4**
- direct thickness = **4 / 4**
- production section completeness = **4 / 4**
- section completion = **0**

No direct instance value may be replaced by a family/reference statistic.

## 4. Reference Statistics Contract

A1 source-published:
- south-facade 由额 width mean = **250.0 mm**
- south-facade thickness = **105 mm**
- north center-bay width = **259 mm**
- north center-bay thickness = **105 mm**

Project arithmetic across all four direct widths:
- `(255 + 245 + 250 + 259) / 4 = 252.25 mm`

Mandatory classification:
- `252.25 mm = PROJECT_DERIVED_REFERENCE`
- `NOT_SOURCE_PUBLISHED_FAMILY_MEAN`

The validator must reject any representation that labels 252.25 mm as an A1-published mean.

## 5. Canonical Reference Geometry

Canonical Stage1 specimen:

**1000 × 252.25 × 105 mm**

Axes:
- +X = longitudinal
- +Y = width / 广
- +Z = thickness / 厚

Origin:
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform:
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

1000 mm:
- `NON_HISTORICAL_REFERENCE_LENGTH`
- `MASTER_SPECIMEN_ONLY`
- replaceable
- must never become a building-instance length by default.

252.25 mm:
- project-derived reference only.

105 mm:
- directly measured at all four instances.

## 6. Length / Placement Contract

No direct historical full timber length is locked.

Production rule:
- `actual_instance_length = ASSEMBLY_ENDPOINT_DERIVED`

Unknowns:
- `historical_full_timber_length_mm = null`
- hidden tenon extension = UNKNOWN
- exact end penetration into columns = UNKNOWN

The generic endpoint resolver may be reused:
- `V = P_end - P_start`
- `L = ||V||`
- `P_center = (P_start + P_end) / 2`
- local +X aligns to V

### Engineering-only fixtures

`TEST-X`
- start=(0,0,0)
- end=(1300,0,0)
- expected length=1300
- expected center=(650,0,0)
- expected direction=(1,0,0)

`TEST-Y`
- start=(0,0,0)
- end=(0,1700,0)
- expected length=1700
- expected center=(0,850,0)
- expected direction=(0,1,0)

Fixtures are:
- `ENGINEERING_TEST_ONLY`
- `NOT_BUILDING_COORDINATES`
- `NON_HISTORICAL`

They prove:
- 1000 mm does not leak;
- same Master supports multiple production spans;
- no world facade direction is baked into the body;
- assembly-derived span is not relabelled as historical concealed timber full length.

## 7. Geometry Mode

`PARAMETRIC_HORIZONTAL_LONG_MEMBER_WITH_INSTANCE_SECTION_PARAMETERS`

Stage1 body:
- straight rectangular bounded envelope;
- simplified flat ends;
- no current sag, cracking, weathering, or repair deformation baked in;
- no decorative curvature/taper;
- no unsupported historical end profile.

Variant policy:
- canonical Master count = 1
- Geometry Variant count = 0

Do not create a Variant for:
- north vs south facade;
- width difference 245/250/255/259;
- historical repair orientation metadata;
- different endpoint-derived span;
- X/Y world orientation.

## 8. Historical Orientation Contract

A1 directly establishes that current 由额 orientation reflects historical repair.

Locked semantic metadata:
- `current_orientation_state = HISTORICAL_REPAIR_FLIPPED`
- `original_963_top_bottom_orientation = UNRESOLVED`

Mandatory rule:

> Historical orientation state is semantic metadata. It must not alter canonical body identity or create a Geometry Variant while the Stage1 body remains a symmetric rectangular bounded envelope.

### Orientation metadata regression

A deterministic validation must prove:
- canonical geometry remains unchanged when orientation-history metadata is serialized/restored;
- master id remains `CMP-FRAME-YOUE-001_MASTER`;
- geometry variant count remains 0;
- the record still exposes `HISTORICAL_REPAIR_FLIPPED`;
- original 963 orientation remains unresolved.

No validator may infer `ORIGINAL_963` from the current transform.

## 9. Historical Mortise Trace Contract

A1 / Fig. 2-49 supports trace existence.

Locked:
- `mortise_trace_existence = DIRECT_EVIDENCE`
- `mortise_trace_exact_geometry = UNRESOLVED`
- `mortise_trace_current_structural_function = UNRESOLVED`
- `canonical_body_cut = false`
- classification = `HISTORICAL_REPAIR_TRACE_METADATA`

Mandatory regression:
- toggling/preserving trace metadata must not change body geometry signature;
- no mortise/slot mesh may appear in canonical Master;
- trace existence must remain visible in Semantic/Review evidence.

## 10. Connection Layer｜RC-024

Two Stage1 interfaces:

1. `LEFT_END / COLUMN_CONNECTION`
2. `RIGHT_END / COLUMN_CONNECTION`

For each:
- related family = 柱
- connection existence = KNOWN
- exact connection kind = unresolved at Stage1
- exact geometry = DEFERRED
- tenon dimensions = UNKNOWN
- mortise dimensions = UNKNOWN
- penetration depth = UNKNOWN

The vertical relationship among 阑额 / 额间板 / 由额 is assembly placement semantics, not evidence of an extra direct joinery feature.

## 11. Related-component Isolation

T-035 covers 由额 only.

Must not absorb:
- 阑额
- 额间板
- 普拍枋
- 柱
- 斗栱

Explicitly preserve:
- 万佛殿“不设普拍枋”;
- 由额 and 阑额 are distinct component identities;
- a visible 阑额 + 额间板 + 由额 stack must not become one Master.

## 12. Shared Master V2 Infrastructure

Reuse first:
- `production/zhenguo_wanfo/scripts/p3_3_master_v2_common.py`
- `production/zhenguo_wanfo/scripts/validate_p3_3_master_v2.py`
- `.github/workflows/p3_3_master_v2.yml`

Expected:
- reuse generic length/width/thickness mutation;
- reuse endpoint resolver;
- reuse adaptive Review Board generation;
- serialize historical-orientation and repair-trace metadata in Definition/Semantic without creating body variants.

If the current generic schema cannot express:
- `HISTORICAL_REPAIR_FLIPPED`
- unresolved original orientation
- non-geometric historical repair trace metadata

then a minimal generic extension may be proposed **only after engineering execution authorization**.

Any extension must be:
- reusable;
- Definition-driven;
- minimal;
- non-由额-specific;
- non-authoritative beyond locked source facts.

Forbidden:
- 由额-only permanent workflow;
- per-location builder scripts;
- a special geometry branch solely because of the repair-flip metadata;
- a parallel evidence cache.

## 13. Shared Regression Protection

If shared Master V2 infrastructure changes, mandatory regressions include:

- T-025｜剳牵
- T-026｜槫
- T-027｜托脚
- T-028｜叉手
- T-029｜蜀柱
- T-030｜大角梁
- T-033｜子角梁
- T-034｜阑额

Reason:
- T-034 introduced the current shared metadata/instance-section baseline;
- T-035 may extend semantic metadata for historical orientation/repair traces;
- no generic extension may regress prior Master semantics.

All required regressions must PASS before T-035 may be considered engineering-complete.

## 14. Required Review Board

Formal output:
`CMP-FRAME-YOUE-001_MASTER_REVIEW_BOARD_V001.png`

Required panels:
1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION`
4. `4_INSTANCE_SECTION_MAPPING`
5. `HISTORICAL_ORIENTATION_BOUNDARY`
6. `SOURCE_AND_RECONSTRUCTION_BOUNDARY`

Mandatory visible content:

### END_SECTION
- canonical reference = 252.25 × 105
- `252.25 = PROJECT_DERIVED_REFERENCE`
- reference only, not source-published family mean

### 4_INSTANCE_SECTION_MAPPING
- 南西 255×105
- 南明 245×105
- 南东 250×105
- 北明 259×105
- all four = DIRECT_MEASURED

### HISTORICAL_ORIENTATION_BOUNDARY
- current state = `HISTORICAL_REPAIR_FLIPPED`
- original 963 top/bottom = `UNRESOLVED`
- old mortise traces = observed
- exact trace geometry = unresolved / not modeled
- historical metadata does not create a Geometry Variant

### SOURCE_AND_RECONSTRUCTION_BOUNDARY
Evidence locked:
- identity / count / locations;
- four direct sections;
- current historical-repair flip;
- existence of old mortise traces;
- no 普拍枋;
- column-connection semantics.

Project/reconstruction:
- 1000 mm reference length;
- 252.25 project-derived reference width;
- endpoint fixtures;
- simplified flat ends.

Not claimed:
- exact 963 section;
- exact original top/bottom;
- exact historical full timber length;
- exact mortise/tenon geometry;
- current trace as active original joinery.

## 15. Minimal-Sufficient Formal Package

Expected component-specific outputs after execution authorization:

1. `CMP-FRAME-YOUE-001_MASTER_DEFINITION_V001.json`
2. `CMP-FRAME-YOUE-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-YOUE-001_MASTER_V001.blend` — Actions Artifact + local-only
4. `CMP-FRAME-YOUE-001_MASTER_REVIEW_BOARD_V001.png`
5. `CMP-FRAME-YOUE-001_MASTER_VALIDATION_V001.json`
6. this lifecycle record

Do not create redundant per-instance binaries, evidence caches, or duplicate authority files.

## 16. First-Article Validation Contract

Machine validation must cover at least these domains.

### Identity / Registry
1. task/component/master/version identity
2. V008/CURRENT authority
3. physical instances = 4
4. one shared Master
5. geometry variant count = 0
6. all four Registry locations traceable

### Direct section mapping
7. 南西 = 255×105
8. 南明 = 245×105
9. 南东 = 250×105
10. 北明 = 259×105
11. width direct count = 4
12. thickness direct count = 4
13. no PARAMETRIC_COMPLETION section
14. no instance section collapsed to reference value
15. 252.25 arithmetic recompute PASS
16. 252.25 classification = PROJECT_DERIVED_REFERENCE
17. 252.25 not labelled A1-published family mean
18. south A1 statistic 250.0×105 retained
19. north center A1 statistic 259×105 retained

### Canonical geometry / mutation
20. canonical length = 1000
21. canonical width = 252.25
22. canonical thickness = 105
23. canonical bbox = 1000×252.25×105
24. canonical transform/origin PASS
25. length mutation isolates local X
26. width mutation isolates local Y
27. thickness mutation isolates local Z
28. all four sections generated by same Master
29. section differences do not create Variants

### Span / orientation
30. endpoint resolver enabled/equivalent
31. TEST-X length = 1300
32. TEST-X center = (650,0,0)
33. TEST-X direction = (1,0,0)
34. TEST-Y length = 1700
35. TEST-Y center = (0,850,0)
36. TEST-Y direction = (0,1,0)
37. same Master identity in TEST-X/TEST-Y
38. fixtures marked NOT_BUILDING_COORDINATES
39. no 1000 mm leakage
40. no fixed world facade direction
41. assembly span not labelled historical full length

### Historical orientation metadata
42. current_orientation_state = HISTORICAL_REPAIR_FLIPPED
43. original_963_top_bottom_orientation = UNRESOLVED
44. current orientation not marked original 963
45. historical metadata survives deterministic restore
46. historical metadata does not change geometry signature
47. historical metadata does not create Geometry Variant

### Mortise trace boundary
48. mortise_trace_existence = DIRECT_EVIDENCE
49. mortise_trace_exact_geometry = UNRESOLVED
50. mortise_trace_current_structural_function = UNRESOLVED
51. canonical_body_cut = false
52. classification = HISTORICAL_REPAIR_TRACE_METADATA
53. no mortise/slot mesh in canonical body
54. trace metadata does not alter geometry signature

### Visual / relation / history boundary
55. D-154 Source Readiness traceable
56. D-155 Visual/Form Gate traceable
57. source binding traceable
58. 由额 separated from 阑额
59. 额间板 excluded
60. 普拍枋 not introduced
61. 柱 and 斗栱 not absorbed
62. left/right column connection semantics retained
63. exact joinery deferred
64. no unsupported mortise/tenon claim
65. no exact 963 section claim
66. no repair-state feature silently historicized

### Review Board / reproducibility
67. Blender 4.5.13 LTS
68. independent reopen PASS
69. deterministic semantic restore
70. Definition↔Semantic identity
71. binary SHA recorded
72. Review Board contains canonical Chinese name “由额”
73. all six panels complete
74. 4/4 direct sections visible
75. historical-orientation boundary visible
76. mortise-trace boundary visible
77. 252.25 classification visible
78. canonical .blend not tracked in Git Master directory
79. minimal-sufficient formal surface PASS

### Shared regression
80. T-025 PASS if shared infrastructure changes
81. T-026 PASS if shared infrastructure changes
82. T-027 PASS if shared infrastructure changes
83. T-028 PASS if shared infrastructure changes
84. T-029 PASS if shared infrastructure changes
85. T-030 PASS if shared infrastructure changes
86. T-033 PASS if shared infrastructure changes
87. T-034 PASS if shared infrastructure changes

Exact atomic count may exceed 87. No validation domain may be removed merely to reduce count.

## 17. Hard Fails

- `INSTANCE_SECTION_COLLAPSED_TO_REFERENCE_MEAN`
- `PROJECT_DERIVED_REFERENCE_MARKED_AS_SOURCE_PUBLISHED`
- `HISTORICAL_REPAIR_FLIP_IGNORED`
- `CURRENT_ORIENTATION_MARKED_AS_963_ORIGINAL`
- `ORIENTATION_METADATA_CHANGES_GEOMETRY_SIGNATURE`
- `ORIENTATION_METADATA_CREATES_GEOMETRY_VARIANT`
- `OLD_MORTISE_TRACE_MODELED_AS_CANONICAL_JOINERY`
- `MORTISE_TRACE_METADATA_CHANGES_BODY_GEOMETRY`
- `UNSUPPORTED_JOINERY_CLAIM`
- `DUPLICATE_MASTER_PER_LOCATION`
- `FALSE_GEOMETRY_VARIANT_FROM_SECTION_DIFFERENCE`
- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `ASSEMBLY_LENGTH_MARKED_AS_HISTORICAL_FULL_TIMBER_LENGTH`
- `FIXED_WORLD_FACADE_DIRECTION`
- `YOUE_LANE_IDENTITY_COLLAPSE`
- `YOUE_EJIANBAN_IDENTITY_COLLAPSE`
- `PU_PAIFANG_FALSELY_INTRODUCED`
- `SILENT_HISTORICIZATION`
- `MASTER_WITHOUT_EVIDENCE_BINDING`
- `MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`
- `SHARED_V2_REGRESSION_FAILURE`

Missing exact historical joinery, concealed timber full length, or original 963 top/bottom orientation is explicitly **NOT** a Stage1 Hard Fail when kept unresolved.

## 18. Exception / Blocker Handling

RC-021 / RC-022 apply.

If authorized execution later becomes blocked:
1. mark status BLOCKED;
2. report blocker, completed progress, impact, and recommended path;
3. troubleshooting must not silently broaden scope;
4. generic infrastructure/workflow changes require explicit Product Owner authorization if outside the locked execution contract;
5. only after blocker clearance may engineering resume.

## 19. Protected Boundaries

T-035 must not:
- reactivate T-018 / PR #3 / PR #6;
- start Stage2;
- alter T-020 / RZ / FV authority;
- reopen P2 frozen baseline;
- modify A1 evidence facts;
- claim 252.25 as A1 family mean;
- reinterpret repair-flipped current orientation as original 963 orientation;
- turn old mortise traces into canonical joinery;
- fuse 由额 with 阑额 / 额间板 / 普拍枋;
- treat endpoint span as historical full timber length;
- weaken prior Master V2 semantics.

T-018 remains HOLD.

## 20. Authorization Boundary｜D-157

Product Owner instruction **“授权设计并锁定 Task Contract”** authorizes this Task Contract design and lock only.

Locked:
- `TASK_CONTRACT_LOCKED = true`
- `ENGINEERING_EXECUTION_AUTHORIZED = false`
- `BLENDER_EXECUTION_AUTHORIZED = false`
- `PRODUCTION_BRANCH_CREATION_AUTHORIZED = false`
- `PR_CREATION_AUTHORIZED = false`

No production branch or PR is created by D-157.

To begin engineering, Product Owner must explicitly authorize:

> **开始 T-035**

Only after that separate authorization may:
- branch `codex/t035-p3-3-youe-master-v2-v001` be created;
- execution Definition be finalized;
- Draft PR be opened;
- GitHub Actions / Blender 4.5.13 execute;
- a minimal generic shared-V2 extension be introduced if demonstrably necessary;
- first-article evidence be generated.

First-article acceptance, formalization, Catalog/V008 binding, merge, Stage2, and T-018 resume remain separate authorization boundaries unless explicitly delegated later.
