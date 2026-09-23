# 【中国古建筑3D复原｜T-028｜P3_3_CHASHOU_MASTER_V2_V001｜叉手 Master 首件生产】

Status: **TASK CONTRACT V001 LOCKED / PRODUCT OWNER APPROVED / D-109 / ENGINEERING EXECUTION NOT AUTHORIZED**  
Think Level: **HIGH**  
Execution architecture: **MASTER V2 / MINIMAL_SUFFICIENT / ENDPOINT-DRIVEN**  
Phase/Gate: P3 / P3.3 V002  
Stage: Stage 1｜真实构件 Master 库  
Date: 2026-09-23  
Proposed branch: `codex/t028-p3-3-chashou-master-v2-v001`  
PR policy: **ONE TASK = ONE BRANCH = ONE PR / DO NOT CREATE UNTIL EXECUTION AUTHORIZED**

## 1. Objective

建立并验证一个叉手 canonical Master：

- component id: `CMP-FRAME-CHASHOU-001`
- master id: `CMP-FRAME-CHASHOU-001_MASTER`
- master version: `V001`
- physical instances: **8**
- `INTERIOR_FRAME = 4`
- `GABLE_FRAME = 4`
- geometry variant count: **0**

核心工程目标：

> Master 保存稳定构件本体；建筑实例实际长度、倾角与朝向由显式 assembly endpoints 求解。

T-028 是 RC-020 `Evidence-Constrained Reconstruction` 在 Stage 1 的第一个正式 endpoint-driven 首件。

## 2. Authoritative Inputs

### A1｜一级工程主权
`SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》`

Direct binding：
- PDF p89–90 / printed p74–75
- §2.3.1.8｜托脚与叉手
- 表2-45

Formal evidence：
`docs/evidence/zhenguo_wanfo/P3_3_CHASHOU_DIRECT_SOURCE_BINDING_V001.md`

### A2｜官方同建筑视觉/结构
山西文物数字博物馆·万佛殿专题。

结构语义：
- 平梁之上设驼峰、蜀柱、叉手；
- 叉手属于平梁以上脊部支撑体系。

### Canonical project inputs
- `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- `docs/production/zhenguo_wanfo/P3_3_STAGE1_CHASHOU_MASTER_SPEC_V001.md`
- `production/zhenguo_wanfo/registry/P3_3_STAGE1_CHASHOU_MASTER_SPEC_V001.json`

Decision chain：
- D-099 / RC-019 source authority
- D-108 / RC-020 Evidence-Constrained Reconstruction
- D-108 Chashou Master Spec V001

## 3. Locked Measurement / Registry Boundary

A1 complete visible samples, mm：
- 232 × 92
- 234 × 90
- 228 × 91
- 228 × 89

另有“未及”记录。

Report-published mean：
- width = **230.5 mm**
- thickness = **90.5 mm**

Independent recompute：
- width = **230.5 mm**
- thickness = **90.5 mm**

Locked source status：
- `SOURCE_INTERNAL_NUMERIC_CONFLICT = FALSE`
- `sample_to_instance_mapping = UNKNOWN`

Canonical section：
**230.5 × 90.5 mm**

V008/CURRENT physical instances = **8**：
- 东缝南侧 / 北侧
- 西缝南侧 / 北侧
- 东山南侧 / 北侧
- 西山南侧 / 北侧

Role partition：
- INTERIOR_FRAME = 4
- GABLE_FRAME = 4

## 4. Canonical Master Geometry

Geometry mode：
`PARAMETRIC_ENDPOINT_DRIVEN_LONG_MEMBER`

Canonical reference body：
- X = **1000 mm**
- Y = **230.5 mm**
- Z = **90.5 mm**

Axes：
- +X = longitudinal
- +Y = 广 / width
- +Z = 厚 / thickness

Origin：
- longitudinal midpoint
- transverse center
- lower reference plane

Canonical transform：
- Location=(0,0,0)
- Rotation=(0,0,0)
- Scale=(1,1,1)

1000mm classification：
- `RECONSTRUCTION_REFERENCE_LENGTH`
- non-historical
- replaceable
- Master specimen only
- **must never become building instance length by default**

## 5. Endpoint Resolver Contract

For each placement:

`V = P_upper - P_lower`

`L = ||V||`

`P_center = (P_upper + P_lower) / 2`

Local +X aligns to `V`.

Therefore：
- actual length = endpoint-derived
- actual orientation = endpoint-derived
- actual installation angle = endpoint-derived
- Master stores no fixed historical length
- Master stores no fixed installation angle

Endpoint values may be `RECONSTRUCTED_DESIGN` when derived from project geometry. Historical exact endpoint evidence is not required for production if the derived placement is source-consistent and geometrically closed.

## 6. Deterministic Endpoint Proof Fixtures

T-028 must prove the resolver with two fixtures explicitly marked：

`ENGINEERING_TEST_ONLY / NOT_BUILDING_COORDINATES`

### TEST-A
- P_lower = (0,0,0)
- P_upper = (900,0,1200)
- expected length = **1500 mm**
- expected center = **(450,0,600)**
- expected normalized direction = **(0.6,0,0.8)**

### TEST-B
- P_lower = (0,0,0)
- P_upper = (1200,0,500)
- expected length = **1300 mm**
- expected center = **(600,0,250)**
- expected normalized direction = **(12/13,0,5/13)**

Both fixtures must demonstrate：
- same Master identity
- same 230.5 × 90.5 section
- different derived length
- different derived orientation
- no 1000mm leakage
- no building-coordinate claim

These fixtures must not be written into Component Registry as physical Wanfodian coordinates.

## 7. Stage Boundary｜Why no eight real building placements in Stage 1

Stage 1 validates the Master and its assembly interface behavior.

T-028 must **not** hard-code final XYZ for the eight Wanfodian Chashou instances.

Reason：
- actual building coordinates belong to later building instance / spatial placement stages;
- early locking would recreate local-first/global-closure risk;
- RC-020 allows reconstructed design, but does not authorize Stage boundary violations.

Therefore：
- eight physical identities/roles are locked now;
- endpoint resolver capability is proven now;
- final building endpoint coordinates are resolved later under whole-building geometry authority.

## 8. End / Joinery Boundary

Stage 1 V001：
- Master reference end profile = `STRUCTURAL_SIMPLIFIED_FLAT_END`
- historical end profile = `UNRESOLVED_METADATA`
- mortise/tenon = `NOT_MODELED_AT_STAGE1`
- notch/groove = `NOT_MODELED_AT_STAGE1`

This does **not** block Stage 1 completion.

Later Assembly / Detail Stage may add replaceable reconstructed end treatment if needed for：
- collision closure
- visual closure
- newly available direct evidence

Any reconstructed end treatment must not be claimed as historical original joinery.

## 9. Variant Policy

One shared canonical Master only.

Do not create Variant for：
- 南 / 北
- mirror direction
- INTERIOR_FRAME / GABLE_FRAME
- differing derived length
- differing derived angle

A future Variant requires stable repeated body-geometry differences that cannot be represented as placement/assembly parameters.

## 10. Shared Master V2 Infrastructure Extension

Reuse：
- `production/zhenguo_wanfo/scripts/p3_3_master_v2_common.py`
- `production/zhenguo_wanfo/scripts/validate_p3_3_master_v2.py`
- `.github/workflows/p3_3_master_v2.yml`

Current shared infrastructure validates canonical body / dimension mutation / role mutation but does not yet provide a complete endpoint-driven proof contract.

T-028 may extend the shared infrastructure, but the extension must be：

- generic
- Definition-driven
- reusable by future endpoint-driven components
- not hard-coded to Chashou

Preferred Definition surface：

`endpoint_resolver_contract`

At minimum：
- enabled
- lower endpoint semantic
- upper endpoint semantic
- length rule
- center rule
- orientation rule
- deterministic proof fixtures
- fixture building-coordinate claim=false
- historical claim=false
- reconstructed-design status

Forbidden：
- Chashou-only resolver script
- Chashou-only validator
- Chashou-only workflow

## 11. Shared Regression Protection

If shared V2 infrastructure changes, complete regression is mandatory for：

- T-025｜剳牵
- T-026｜槫
- T-027｜托脚

All three must PASS before T-028 may be declared engineering complete.

No existing approved Master semantics may be weakened, silently reinterpreted, or forced into endpoint-driven mode if its locked Definition does not declare that contract.

## 12. Adaptive Review Board

Formal review output：
one adaptive `CMP-FRAME-CHASHOU-001_MASTER_REVIEW_BOARD_V001.png`.

Required panels：

1. `AXON`
2. `LONG_SIDE`
3. `END_SECTION`
4. `DIMENSION_AND_PARAMETRIC_LENGTH`
5. `PLACEMENT_AND_ENDPOINT_LOGIC`
6. `SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY`

`PLACEMENT_AND_ENDPOINT_LOGIC` must visibly show TEST-A and TEST-B with：
- same Master
- endpoint coordinates
- derived length
- derived orientation
- unchanged section

`SOURCE_AND_RECONSTRUCTION_DESIGN_BOUNDARY` must visibly separate：

Evidence locked：
- Chashou identity
- 8 instances
- 230.5 × 90.5 mm
- above-Pingliang ridge-support layer

Reconstructed design：
- endpoint placement
- derived length
- derived orientation
- simplified end treatment

Not claimed：
- exact 963 full length
- exact 963 installation angle
- historical-original joinery

## 13. Minimal-sufficient Formal Package

Expected component-specific outputs：

1. `CMP-FRAME-CHASHOU-001_MASTER_DEFINITION_V001.json`
2. `CMP-FRAME-CHASHOU-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-CHASHOU-001_MASTER_V001.blend` — Actions Artifact + local-only
4. `CMP-FRAME-CHASHOU-001_MASTER_REVIEW_BOARD_V001.png`
5. `CMP-FRAME-CHASHOU-001_MASTER_VALIDATION_V001.json`
6. this lifecycle record

Endpoint fixture results belong in Semantic / Validation; do not create a redundant standalone formal file unless execution discovers a genuine need.

Definition / Semantic / Validation remain independent.

## 14. Validation Contract

Machine validation must cover at least：

### Identity / Registry
1. task/component/master/version identity
2. V008/CURRENT authority
3. physical instances=8
4. INTERIOR_FRAME=4
5. GABLE_FRAME=4
6. all eight Registry IDs traceable
7. one shared Master / zero geometry Variant

### A1 measurement
8. four complete visible samples retained
9. source unmeasured record retained
10. report width=230.5
11. report thickness=90.5
12. recompute width=230.5
13. recompute thickness=90.5
14. source internal numeric conflict=false
15. sample-to-instance mapping remains UNKNOWN

### Canonical geometry
16. reference length=1000 / reconstruction reference
17. reference length historical claim=false
18. bbox=1000×230.5×90.5
19. canonical origin/transform
20. length mutation isolates X
21. width mutation isolates Y
22. thickness mutation isolates Z
23. role mutation preserves Master geometry signature
24. simplified flat end explicit
25. no unsupported joinery geometry

### Endpoint resolver
26. endpoint resolver contract enabled
27. TEST-A length=1500
28. TEST-A center=(450,0,600)
29. TEST-A normalized direction=(0.6,0,0.8)
30. TEST-B length=1300
31. TEST-B center=(600,0,250)
32. TEST-B normalized direction=(12/13,0,5/13)
33. TEST-A/B angles differ
34. TEST-A/B section remains 230.5×90.5
35. TEST fixtures use same Master identity
36. fixture coordinates marked NOT_BUILDING_COORDINATES
37. no fixed Master installation angle
38. no 1000mm leakage into endpoint-derived instances

### Evidence / reconstruction boundary
39. A2 structural layer retained
40. reconstructed-design fields explicitly classified
41. no reconstructed value marked DIRECT_MEASURED
42. historical unknown does not fail by itself
43. no silent historicization
44. no false Variant from placement-only differences

### Reproducibility / delivery
45. Blender 4.5.13 LTS
46. independent reopen PASS
47. deterministic restore
48. Definition↔Semantic identity
49. binary SHA recorded
50. all Definition-required Review Board panels complete
51. canonical .blend not tracked in Master directory
52. D-099 / RC-019 / D-108 / RC-020 / D-109 traceable

### Shared regression
53. T-025 regression PASS if shared infrastructure changed
54. T-026 regression PASS if shared infrastructure changed
55. T-027 regression PASS if shared infrastructure changed

Exact atomic check count may exceed 55. No required information domain may be removed merely to reduce count.

## 15. Hard Fails

- `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
- `ENDPOINT_RESOLVER_LENGTH_MISMATCH`
- `ENDPOINT_RESOLVER_ORIENTATION_MISMATCH`
- `ENDPOINT_TEST_MARKED_AS_BUILDING_COORDINATE`
- `FIXED_MASTER_INSTALLATION_ANGLE`
- `SILENT_HISTORICIZATION`
- `RECONSTRUCTED_DESIGN_MARKED_AS_DIRECT_MEASURED`
- `DIRECT_EVIDENCE_OVERRIDDEN_WITHOUT_DECISION`
- `FALSE_GEOMETRY_VARIANT_FROM_PLACEMENT_ONLY`
- `UNSUPPORTED_JOINERY_CLAIM`
- `MASTER_WITHOUT_EVIDENCE_BINDING`
- `SHARED_V2_REGRESSION_FAILURE`

`HISTORICAL_LENGTH_UNKNOWN` is explicitly **NOT** a Hard Fail.

## 16. Blender / Artifact Rule

- Blender pinned to **4.5.13 LTS**
- formal execution through GitHub Actions
- canonical .blend = Actions Artifact + local-only
- no canonical Chashou .blend committed to Git
- exact Blender version unavailable = STOP

## 17. Protected Boundaries

T-028 must not：
- reactivate T-018 / PR #3 / PR #6
- modify T-020 / RZ D-063 / FV D-064 authority
- rewrite approved T-025 / T-026 / T-027 facts
- reopen P2 frozen baseline
- treat endpoint test coordinates as Wanfodian actual coordinates
- hard-code all eight building placements in Stage 1
- create eight Masters/Variants from placement differences

T-018 remains HOLD.

## 18. Authorization Boundary｜D-109

D-109 locks this Task Contract only.

Current authorization：

- `TASK_CONTRACT_LOCKED = TRUE`
- `ENGINEERING_EXECUTION_AUTHORIZED = FALSE`
- `BLENDER_EXECUTION_AUTHORIZED = FALSE`
- `PRODUCTION_BRANCH_CREATION_AUTHORIZED = FALSE`
- `PR_CREATION_AUTHORIZED = FALSE`

To begin engineering, Product Owner must explicitly authorize：

> **开始 T-028**

Only after that authorization may：
- the locked engineering Definition be created/finalized with execution=true;
- branch `codex/t028-p3-3-chashou-master-v2-v001` be created;
- PR be opened;
- shared V2 infrastructure be extended if required;
- GitHub Actions / Blender 4.5.13 execute;
- first-article evidence be generated.

First-article acceptance and PR merge remain separate Product Owner authorization boundaries.

## 19. Engineering execution authorization / D-110

Product Owner explicitly authorized **开始 T-028** on 2026-09-23.

Authorized:
- engineering execution = true
- Blender/GitHub Actions execution = true
- production branch = `codex/t028-p3-3-chashou-master-v2-v001`
- Draft PR creation = true
- locked execution Definition creation = true
- generic Definition-driven endpoint-resolver extension to shared Master V2 infrastructure = permitted if required

Mandatory regression if shared infrastructure changes:
- T-025 剳牵
- T-026 槫
- T-027 托脚

Still requires separate Product Owner authorization:
- first-article acceptance
- formal materialization / Catalog + V008 approved binding
- PR merge
- Stage1 PASS / Stage2
- T-018 resume

## 20. First-article Run #1｜Superseded infrastructure fetch failure

Run `35816530219` failed at **Resolve locked Master Definition** before Blender installation or any geometry execution.

Root cause:
- PR base `main` advanced after branch creation because the derived Dashboard synchronized Project Control;
- the workflow then fetched the base branch with `--depth=1`;
- `git diff origin/main...HEAD` could not resolve a merge base in that shallow state;
- result: zero Definitions detected.

Classification:
- `INFRASTRUCTURE_FETCH_HISTORY_FAILURE`
- no Chashou geometry was generated;
- no endpoint resolver logic was executed;
- no validation or regression result exists from Run #1.

Patch:
- remove the two `--depth=1` base-branch fetches from the generic Master V2 workflow;
- retain full-history checkout semantics for PR diff and shared-regression comparisons.

Run #1 is **SUPERSEDED** and must not be used for engineering acceptance.

