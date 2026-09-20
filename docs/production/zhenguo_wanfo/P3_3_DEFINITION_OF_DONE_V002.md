# P3.3｜真实构件驱动整殿重建

## Definition of Done / Implementation Plan V002｜LOCKED / PRODUCT OWNER APPROVED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Gate：P3.3｜真实构件驱动整殿重建
- Engineering subtitle：Real-component-driven Whole-building Reconstruction
- Version：V002
- Status：LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT YET AUTHORIZED
- Decision：D-066
- Visual-reference amendment：D-076 / 2026-09-20
- Approval date：2026-09-19
- Supersedes：P3.3 Definition of Done V001 / D-047 as the current P3.3 implementation plan
- Historical preservation：V001 remains retained for audit history; its five Gate Hard Fails remain inherited unless explicitly replaced below

> V002 changes the production order, not the project objective.  
> The project will no longer try to make the legacy 11-family / 40-variant / 365-engineering-object system directly become the final building.  
> The new route is: **real component registry → Component Master → variant/interface → representative assembly → whole-building instance topology → placement authority → deterministic generation → final acceptance**.

---

## 1. Why P3.3 is rebaselined

V007 whole-building component audit established that:

1. the legacy 11 / 40 / 365 system is an engineering-control/proxy baseline, not a complete inventory of the hall's real architectural components;
2. multiple real beams, bracket-set members, purlins, roof members and enclosure elements had been compressed into proxy/control objects;
3. V007 now provides a real-component-oriented evidence baseline, including component identity, instance/location, evidence status and bounded unknowns;
4. RC-018 establishes the canonical data architecture: Component Registry JSON is the fact source; Excel is only a derived view;
5. continuing directly with the old T-018 whole-building expansion would force new real-component evidence back into an old proxy-led architecture.

Therefore P3.3 V002 moves whole-building generation to the end of the gate, after the real component library and assembly topology are established.

---

## 2. Current canonical inputs

### 2.1 Real-component fact source

Current canonical component source:

`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

Current versioned snapshot:

`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`

V007 is the current build baseline.

The registry may contain:

- physical component instances;
- assembly locations;
- directional/counting units;
- measurement samples;
- parametric-completion rules;
- UNKNOWN boundaries.

These record types must not be silently summed as if all were physical components.

### 2.2 Existing approved assets retained

The following are retained, subject to V002 rebinding/review:

- P3.0 ontology / Registry governance;
- P3.1 approved Component Master mechanism;
- existing approved Masters:
  - 柱
  - 柱头栌斗
  - 单向长开斗
  - 交互斗
  - 下六椽栿
  - 上六椽栿
- P3.2 five relationship types and interface/location mechanism:
  - SUPPORT
  - CONNECT
  - LOCATE
  - REPEAT
  - BELONG
- P1/P2 evidence semantics:
  - CONFIRMED / direct evidence
  - explicit derivation
  - REASONABLE_COMPLETION / PROJECT_RULE
  - UNKNOWN / DEFERRED / PROXY boundaries.

Existing approval does not mean every retained asset is automatically suitable for the V007 real-component architecture; rebinding is required where specified below.

---

# 3. New P3.3 production architecture

## Stage 1｜真实构件 Master 库

### Goal

Establish the reusable real-component Master library required by V007.

### Work

1. rebind and review the six existing approved Masters against V007 identity, dimensions and evidence boundaries;
2. before any new component Master is authorized for engineering modeling, pass the **Stage 1 Pre-Model Visual Reference Gate** defined below;
3. build missing Masters one component family at a time;
4. for every component family in the current building scope, assign one of:
   - approved Master;
   - approved parametric Master/variant;
   - explicit simplified proxy;
   - PARAMETRIC_COMPLETION;
   - UNKNOWN / not modeled as historical geometry.

### Initial Master priority

The default order is:

1. 四椽栿
2. 平梁
3. 丁栿
4. 乳栿
5. 槫
6. 托脚
7. 叉手
8. 蜀柱
9. 大角梁 / 子角梁 / 隐角梁
10. remaining bracket-set members and variants
11. roof timber members / enclosure components as required by later assembly stages.

This order may be changed only for a documented dependency reason; it is not a historical ranking.

### Stage 1 exit criteria

- every in-scope V007 component family has an explicit modeling disposition;
- all Masters used later have:
  - canonical component identity;
  - evidence-linked dimensions;
  - local axes/orientation;
  - allowed variable parameters;
  - connection/interface points;
  - explicit UNKNOWN / simplified areas;
  - deterministic generation or controlled modeling method;
- no Master silently contains unsupported historical joinery.

**No whole-building generation is allowed in Stage 1.**

---

## Stage 1 Pre-Model Visual Reference Gate

Effective decision: **D-076 / 2026-09-20**

Before Product Owner can approve any new component Master for Blender/Codex engineering execution, ChatGPT must first present a visual reference set for that component.

Minimum requirement:

1. provide at least one same-building **real-object/site photograph** when available;
2. provide at least one same-building **survey drawing / measured drawing / structural form drawing** when available;
3. if one of the above is unavailable, provide the closest authoritative comparative reference and explicitly label it as comparative, not Wanfo direct evidence;
4. source-derived explanatory schematics are allowed only as review aids and must be labeled **SOURCE_DERIVED_SCHEMATIC / NOT DIRECT EVIDENCE**;
5. clearly distinguish what is directly visible from what remains inferred, parametric, simplified, or UNKNOWN;
6. Product Owner must explicitly review/approve the component's visual/form reference before the engineering T-task is created and before Blender generation starts.

Preferred source hierarchy:

**same-building direct photograph > same-building measured/survey drawing > authoritative comparative historic example > source-derived schematic**

A visual reference may support form understanding, but it must not silently create geometric dimensions or joinery that the evidence does not support.

**One-off waiver:** D-077 explicitly waives this visual-reference review for **丁栿 only** and authorizes direct evidence review + Master Spec design. D-077 does not repeal D-076 for later new components.

If no adequate visual/form reference can be produced, engineering modeling is **BLOCKED_ON_VISUAL_REFERENCE_REVIEW** until Product Owner explicitly accepts a bounded proxy/completion approach.


## Stage 2｜构件变体与装配接口

### Goal

Define how approved Masters vary and how they connect.

### Required outputs

For each production-eligible component:

- variant rule;
- orientation rule;
- start/end or support interfaces;
- SUPPORT / CONNECT / LOCATE / REPEAT / BELONG relations;
- parent/child assembly semantics;
- dimension authority;
- length determination rule:
  - direct measured length;
  - measured section + assembly endpoints;
  - explicit derivation;
  - replaceable parametric completion;
  - UNKNOWN.

### Stage 2 exit criteria

- no production Master depends on an undocumented attachment convention;
- component geometry and component placement remain separate;
- the same component identity can be instantiated at multiple valid locations without manual per-instance remodeling.

---

## Stage 3｜代表性组合验证

### Goal

Prove the component system can assemble correctly before whole-building topology is attempted.

### Required representative assemblies

At minimum:

1. 柱—阑额/由额—柱头斗栱 unit;
2. 正身梁架 unit;
3. 山面梁架 unit;
4. 外檐柱头/补间斗栱 unit;
5. 转角 / 翼角 representative unit, within evidence boundary;
6. 槫—椽—屋面基层 representative chain using explicit parametric-completion status where required.

### Stage 3 exit criteria

- representative assembly relationships validate;
- interface directions and attachment points are machine-readable;
- no assembly requires manual Blender placement to make the parts meet;
- unresolved historical details remain explicit.

---

## Stage 4｜整殿真实实例与拓扑

### Goal

Create the actual whole-building assembly graph from the V007 registry, not from legacy 365 accounting.

### Required behavior

Every physical building instance must map to:

- registry identity;
- Master / variant or explicit non-Master disposition;
- physical location;
- orientation;
- support/connection relationships;
- dimension authority;
- evidence state.

Non-physical records such as:

- `COUNTING_UNIT_NOT_PHYSICAL`;
- measurement sample records;
- rule-only records;
- summary/group records

must be excluded from physical-instance totals unless explicitly transformed into a separate physical record.

### Stage 4 exit criteria

- whole-building physical instance accounting is internally closed for the chosen modeling scope;
- no double-counting between group/site/directional/physical-instance layers;
- no anonymous production component;
- unresolved entries remain visible rather than omitted.

---

## Stage 5｜整殿空间定位与标高规则

### Goal

Only after real component topology is established, determine whole-building X/Y/Z placement authorities.

### Review obligations

The following old engineering controls are not automatically inherited into production:

- T-020 reconstructed-design X/Y datum / shared-ridge rule;
- RZ D-063 Roof-Z cumulative closure;
- FV D-064 Frame Vertical Placement bridge;
- T-017 legacy 365 placement/accounting assumptions.

At Stage 5 they must each be classified as:

- RETAIN;
- RETAIN WITH ADAPTATION;
- REPLACE;
- HISTORICAL ENGINEERING REFERENCE ONLY.

### Required principle

> placement rules serve the real-component assembly; real components must not be reshaped or reinterpreted merely to fit legacy proxy coordinates.

### Stage 5 exit criteria

- every production instance has one authoritative placement path;
- no observed validation-only parameter silently becomes generative;
- no duplicate coordinate authority;
- no Blender-local building placement rule;
- RZ/FV/T-020 dispositions are formally recorded.

---

## Stage 6｜确定性整殿生成

### Goal

Generate the whole hall from clean state using:

- canonical real-component registry;
- approved Masters/variants;
- assembly graph;
- placement authority;
- explicit parametric-completion rules.

### Requirements

- no pre-positioned Blender building;
- no manual per-instance transform as production authority;
- no anonymous copy losing identity;
- no legacy 365 proxy object substituted for a real component merely because it already exists;
- deterministic rebuild;
- independent validation;
- parameter mutation only after dependency mapping;
- canonical restore exact at the semantic level.

### T-018 decision point

T-018 V002 remains **HOLD / NOT CURRENT EXECUTION ROUTE** during Stages 1–5.

Before Stage 6, Product Owner must choose one of:

A. rebaseline T-018 again against the real-component architecture; or  
B. formally supersede T-018 and create a new whole-building generation task.

This decision is intentionally deferred until the Stage 4/5 architecture is proven.

---

## Stage 7｜整殿验收与 P3.3 Gate Closure

P3.3 can close only when:

1. real-component Master coverage is accepted;
2. representative assemblies PASS;
3. whole-building physical-instance accounting and topology PASS;
4. placement authority PASS;
5. deterministic clean-state generation PASS;
6. independent machine validation PASS;
7. evidence boundaries remain explicit;
8. required formal review images / visual review PASS;
9. Product Owner approves final Gate closure.

---

# 4. Legacy asset disposition under V002

| Legacy asset | V002 disposition |
|---|---|
| P3.0 ontology / identity governance | RETAIN |
| P3.1 Master mechanism | RETAIN |
| six approved existing Masters | RETAIN / REBIND TO V007 |
| P3.2 relationship vocabulary / interfaces | RETAIN |
| T-017 365 accounting / assembly graph | HISTORICAL ENGINEERING BASELINE / COMPARISON ONLY |
| 11 families / 40 variants / 365 engineering objects | RETAIN AS LEGACY ENGINEERING BASELINE / NOT REAL-COMPONENT TRUTH |
| T-019 7 PURLIN disposition | RETAIN ONLY FOR LEGACY ENGINEERING PURLIN FAMILY; must not override V007 real purlin inventory |
| T-020 shared-ridge datum | HOLD FOR STAGE-5 RE-REVIEW |
| RZ D-063 | DESIGN-LOCKED / HOLD FOR STAGE-5 RE-REVIEW |
| FV D-064 | DESIGN-LOCKED / HOLD FOR STAGE-5 RE-REVIEW |
| T-018 V002 | HOLD / NOT CURRENT EXECUTION ROUTE / REBASELINE-OR-SUPERSEDE DECISION DEFERRED |
| PR #3 | SUPERSEDED / READ-ONLY / DO NOT MERGE |
| PR #6 | HOLD / DO NOT PATCH / DO NOT MERGE |

No legacy asset is deleted merely because it is not current production authority.

---

# 5. Inherited Gate Hard Fails

The five V001 Gate Hard Fails remain active:

1. `REFERENCE_LENGTH_LEAKS_INTO_BUILDING`
2. `SILENT_HISTORICIZATION`
3. `BAKED_MANUAL_BUILDING`
4. `SILENT_BUILDING_OMISSION`
5. `BROKEN_COMPONENT_IDENTITY`

V002 adds:

6. `LEGACY_PROXY_AS_REAL_COMPONENT`  
   A legacy Proxy/Control/Envelope engineering object is presented as a real architectural component without a real-component registry identity and evidence basis.

7. `REGISTRY_LAYER_DOUBLE_COUNT`  
   physical instance, group, site, direction-counting unit or measurement-sample layers are added together as if they were one physical count.

8. `UNDECLARED_PARAMETRIC_COMPLETION`  
   missing geometry is filled by project convention without explicit PARAMETRIC_COMPLETION / PROJECT_RULE labeling.

9. `MASTER_WITHOUT_EVIDENCE_BINDING`  
   a production Master lacks traceable dimension/evidence authority or silently embeds unsupported detail.

10. `EXCEL_AS_CANONICAL_SOURCE`  
    derived Excel is used to override or diverge from the canonical Component Registry JSON.

11. `MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`  
    a new component Master is sent to engineering/Blender before the Product Owner has reviewed the required real-object / form-drawing reference set.

Any occurrence is a Gate FAIL until corrected at its owning layer.

---

# 6. Execution and authorization boundary

D-066 locks P3.3 V002 **as the current implementation plan only**.

D-066 does not authorize:

- Codex component modeling;
- a new T-### task;
- Blender generation;
- T-018 implementation;
- RZ/FV publication;
- CP-03 restart;
- PR #3 or #6 merge;
- Stage 6 whole-building generation;
- P3.3 PASS.

The next executable work, after separate Product Owner authorization, is:

> **Stage 1｜真实构件 Master 库：existing-six rebind/coverage review + first missing Master.**

ChatGPT design/review work does not itself consume a T-###.  
A T-### is created only when an actual engineering task is handed to Codex.

---

# 7. Gate status after lock

- P3.0：PASS / CLOSED
- P3.1：PASS / CLOSED as historical gate; its approved mechanisms/assets remain reusable
- P3.2：PASS / CLOSED as historical gate; its relationship mechanism remains reusable
- P3.3：ACTIVE / V002 LOCKED / 0 of 7 new implementation stages formally passed
- T-018 V002：HOLD / NOT CURRENT EXECUTION ROUTE
- Engineering execution authorization：NONE

The project has not regressed to P3.0.  
This is a controlled rebaseline of the **P3.3 implementation route** around the V007 real-component evidence baseline.

