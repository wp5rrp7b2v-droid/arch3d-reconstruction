# T-026｜P3.3 槫 Master V2｜Lifecycle Record V001

Status: **CLOSED / PRODUCT OWNER APPROVED / D-095 / PR #13 MERGED / D-096**  
Date: 2026-09-21  
Decisions: **D-093 / D-094 / D-095**  
Branch: `codex/t026-p3-3-purlin-master-v2-v001`  
Master: `CMP-FRAME-PURLIN-001_MASTER`

## 1. Task objective

建立 Stage1 下一只真实构件 Master：**槫**。

本任务继承 D-089 最小充分文件集规则和 T-025 已验证的共享 V2 基础设施，但不得机械复制剳牵的矩形长料几何。

## 2. Why this component is next

V008 / CURRENT 当前 Stage1 状态：

- 28 Master-scope object types
- 11 approved
- 17 pending
- 槫为当前下一项 pending Master
- physical instances = **33**

33 根展开为：

- 正身：7道 × 3段 = **21**
- 东山：2道 × 3段 = **6**
- 西山：2道 × 3段 = **6**

P3.3 Stage1 Master Coverage Matrix V002 已锁定：

> 槫｜33件｜需新建Master｜共享Master + 长度/位置变体；旧7 PURLIN不得当真实总量。

## 3. Visual-reference gate / D-093

**PASS WITH GEOMETRY BOUNDARY**

High-confidence visual/structural reference:

https://szbwgvue.chwhyun.cn/wanfodian/

该万佛殿专题页可支持：

- 撩檐槫作为柱头/转角铺作上部承托对象；
- 脊槫与其他各槫参与屋面曲线；
- 撩檐槫至脊槫的整体举折关系；
- 老角梁后尾与槫存在明确连接关系。

该来源用于构件身份、层位、结构关系和视觉 Gate，不作为 220.1×270.8 mm 尺寸权威，也不作为精确截面轮廓权威。

尺寸/数量权威继续由 V008 / SRC-ZG-WF-001 证据链承担。

## 4. Evidence boundary

Locked:

- 33 physical instances
- main body 21 / east gable 6 / west gable 6
- family statistics: 平均广 220.1 mm / 厚 270.8 mm
- one shared Master + assembly role/length variants
- current Registry uses “撩风槫”; high-confidence display uses “撩檐槫”; retain Registry IDs and record alias

UNKNOWN / must remain explicit:

- exact historical section profile
- all individual segment lengths
- exact end profiles
- hidden joinery
- exact corner-beam/purlin connection geometry
- sample-to-instance mapping
- whether any role requires a real geometry-family split

## 5. Critical geometry rule

**220.1 × 270.8 mm is currently a section-statistics envelope, not proof of a rectangular historical profile.**

Therefore Stage1 must not silently create a rectangular historical purlin.

The current design proposal is:

> `BOUNDED_SECTION_ENVELOPE / PROFILE_UNKNOWN`

The first article may use a non-historical envelope representation for validation and assembly-interface preparation, but the Review Board must state clearly that the envelope is not the historical section profile.

## 6. Identity separation from legacy PURLIN

Historical engineering ID:

`CMP-PURLIN-001`

was used in the old 7-PURLIN engineering route.

T-026 creates:

`CMP-FRAME-PURLIN-001_MASTER`

The two identities must not be silently equated.

The old 7 engineering objects remain historical engineering controls only and may not be interpreted as the real physical count of 33.

## 7. Assembly role policy

One Master currently covers all roles:

- south/north eave purlins
- south/north lower purlins
- south/north upper purlins
- ridge purlin
- east gable two lines
- west gable two lines
- three segment positions per line

Role, rotation, length and placement are assembly-owned.

Role difference alone does not create a geometry Variant.

## 8. Shengtou wood boundary

The high-confidence display states that ridge and other purlins use 生头木 to form the roof curvature.

T-026 policy:

- 生头木 is **not part of the Purlin Master body**;
- it belongs to later roof-curvature / assembly control;
- no shengtou geometry may be baked into the Stage1 purlin Master.

## 9. Adaptive Review Board

T-026 currently requires 7 panels rather than the T-025 six-panel board:

1. AXON
2. LONG_SIDE
3. END_SECTION_ENVELOPE
4. DIMENSION_PARAMETER_SUMMARY
5. INSTANCE_TOPOLOGY_33
6. ROLE_LAYER_DIAGRAM
7. EVIDENCE_UNCERTAINTY_SUMMARY

The panel count is Definition-driven and may be changed before Definition lock if a panel proves redundant or another view is genuinely required.

## 10. Current authorization boundary

D-094 now locks the T-026 Definition and explicitly authorizes first-article engineering execution.

Approved engineering representation:

- rectangular 220.1 × 270.8 mm **bounding-envelope proxy**;
- the proxy is for machine validation / assembly-interface preparation only;
- it is **not** a claim about the historical section profile;
- every Semantic / Review / Validation output must preserve `PROFILE_UNKNOWN / ENVELOPE_NOT_HISTORICAL`.

Still not authorized:

- Product Owner final Master acceptance;
- Catalog/V008 approved binding;
- PR #13 merge;
- Stage1 PASS;
- T-018 resume.

Next decision:

> **Review T-026 first-article Review Board + machine evidence and decide Product Owner acceptance.**


## 11. First-article engineering result

**PASS / PRODUCT OWNER REVIEW REQUIRED**

- GitHub Actions Run: `35584601233`
- reviewed head: `abbcfa05a2817cb04da9d917cf61377e8a379215`
- Blender: `4.5.13 LTS`
- machine validation: **41/41 PASS**
- canonical .blend SHA-256: `5b14625130f57a744c3654c060ff2e06b2520df973fee5cf2974f39b13e663f4`
- semantic geometry signature: `6ab5ea18d771d70377a693706ef669b208546d6453c7762ef4f72b8087224cd5`
- Review Board SHA-256: `073d13c7f426e2a80808e22c982df126ab64130b1c935cc88f14fc2ba28f4f4b`
- Semantic SHA-256: `ff06bec0c956a3cb5cc288c0010e58dcb6fa9e199de336a94a527666140e6448`
- Validation SHA-256: `fbd282fe7abde8128a6f5c73f061c6dcbaf1ec196bc1abf137d77fa9b6dd67b3`
- Artifact ID: `10632275014`
- Artifact ZIP SHA-256: `62a4282003644745827a1cad2697d24bf36cb3847ac98a44c7ecac8fe41b83eb`
- Artifact size: 1,813,181 bytes
- Review Board: **7 Definition-required panels**

Formal generated Artifact contains exactly four outputs:

1. `CMP-FRAME-PURLIN-001_MASTER_V001.blend`
2. `CMP-FRAME-PURLIN-001_MASTER_SEMANTIC_V001.json`
3. `CMP-FRAME-PURLIN-001_MASTER_REVIEW_BOARD_V001.png`
4. `CMP-FRAME-PURLIN-001_MASTER_VALIDATION_V001.json`

Together with Definition + this Lifecycle Record, the current T-026 component-specific package resolves to **6 formal files**, again as a result of D-089 minimal-sufficient analysis rather than a universal file-count rule.

### Critical evidence-boundary validation

Machine checks explicitly PASS:

- 33 physical instances;
- main 21 / east gable 6 / west gable 6;
- V008 section-statistics binding;
- historical full length remains null;
- 1000mm reference remains non-historical;
- legacy 7-PURLIN identity separated;
- section profile state = `UNKNOWN`;
- rectangular body = `BOUNDING_ENVELOPE_PROXY`;
- section envelope historical claim = false;
- shengtou wood baked into Master = false;
- hidden joinery/end detail = not modeled;
- Definition → Semantic → Validation independence;
- independent reopen;
- length/width/thickness mutation isolation;
- deterministic restore;
- all 7 required Review Board panels complete.

## 12. Product Owner review result

**PASS / superseded by D-095 acceptance.**

The 7-panel Review Board, bounding-envelope proxy labeling, 33-instance topology, section-statistics boundary and UNKNOWN evidence boundary were accepted without requesting geometry changes.


## 13. Product Owner acceptance / D-095

**PRODUCT OWNER APPROVED / FIRST ARTICLE ACCEPTED / FORMAL DELIVERY AUTHORIZED**

Product Owner approved the T-026 Purlin V2 first article on 2026-09-21.

Accepted evidence:
- Run: `35584601233` / SUCCESS
- validation: **41/41 PASS**
- accepted engineering head: `abbcfa05a2817cb04da9d917cf61377e8a379215`
- canonical .blend SHA-256: `5b14625130f57a744c3654c060ff2e06b2520df973fee5cf2974f39b13e663f4`
- semantic geometry signature: `6ab5ea18d771d70377a693706ef669b208546d6453c7762ef4f72b8087224cd5`
- Review Board SHA-256: `073d13c7f426e2a80808e22c982df126ab64130b1c935cc88f14fc2ba28f4f4b`
- Semantic SHA-256: `ff06bec0c956a3cb5cc288c0010e58dcb6fa9e199de336a94a527666140e6448`
- Validation SHA-256: `fbd282fe7abde8128a6f5c73f061c6dcbaf1ec196bc1abf137d77fa9b6dd67b3`
- Artifact ID: `10632275014`
- Artifact ZIP SHA-256: `62a4282003644745827a1cad2697d24bf36cb3847ac98a44c7ecac8fe41b83eb`

Accepted evidence boundary:
- 33 real purlin instances;
- 220.1 × 270.8 mm remains a section-statistics bounding envelope;
- exact historical section profile remains UNKNOWN;
- rectangular first-article body is an engineering envelope proxy only;
- historical full lengths / end profiles / hidden joinery / exact corner-beam connection geometry remain UNKNOWN;
- shengtou wood is not part of the Master body;
- legacy 7-PURLIN engineering identity remains separated.

D-095 authorizes exact materialization of the accepted Artifact's Semantic / Validation / Review Board, Stage1 Catalog registration, V008/CURRENT + derived Excel synchronization, and final regression / pre-merge cross-check.

D-095 does **not** authorize PR #13 merge, Stage1 PASS, Stage2, or T-018 resume.


## 14. Formal materialization

**PASS / EXACT D-095 APPROVED ARTIFACT MATERIALIZED**

- publication workflow run: `35589033394`
- publication job: `publish-approved-t026` = SUCCESS
- materialization commit: `3f0fb4f892b05d48ffd3afc9b285973f9edd77ef`
- source Artifact ID: `10632275014`
- source Artifact ZIP SHA-256: `62a4282003644745827a1cad2697d24bf36cb3847ac98a44c7ecac8fe41b83eb`
- exact-source verification before copy:
  - canonical .blend = `5b14625130f57a744c3654c060ff2e06b2520df973fee5cf2974f39b13e663f4`
  - Semantic = `ff06bec0c956a3cb5cc288c0010e58dcb6fa9e199de336a94a527666140e6448`
  - Validation = `fbd282fe7abde8128a6f5c73f061c6dcbaf1ec196bc1abf137d77fa9b6dd67b3`
  - Review Board = `073d13c7f426e2a80808e22c982df126ab64130b1c935cc88f14fc2ba28f4f4b`
- repository materialized files: Semantic / Validation / single adaptive Review Board
- canonical .blend remains Actions Artifact + local-only and is not tracked in the Master directory
- locked Definition remains unchanged after first-article approval

## 15. Registry / Catalog closure

**PASS / FINAL REGRESSION PENDING**

- Stage1 Catalog approved Master count: `12`
- V008/CURRENT 槫 binding: `33/33`
- Stage1 Master progress: `12/28 = 42.9%`
- approved-Master-covered Registry records: `99`
- pending Master object types: `16`
- derived Excel remains a derived view of the JSON authority and is being synchronized before merge
- temporary D-095 publication job has been removed from the shared V2 workflow

Final regression and PR #13 pre-merge cross-check are required before requesting merge authorization.


## 16. Final regression / pre-merge cross-check

**PASS / PR #13 READY FOR MERGE**

Final V2 closure regression:
- GitHub Actions Run: `35589254034` = **SUCCESS**
- regression head: `817e8dd842d765bf7a0a8cc28d2c509b64910da9`
- validation: **47 / 47 PASS**
- regenerated semantic geometry signature: `6ab5ea18d771d70377a693706ef669b208546d6453c7762ef4f72b8087224cd5`
- approved semantic geometry signature: same / MATCH
- regenerated .blend SHA-256: `ce31f75dbe0de1079fe329a66e66f2a1cad3c173134ed8bb566aefcce3686521`
- approved canonical .blend SHA-256 remains: `5b14625130f57a744c3654c060ff2e06b2520df973fee5cf2974f39b13e663f4`
- binary identity policy: Catalog remains bound to the Product Owner-approved binary; closure regression proves regenerated geometry identity rather than requiring byte-identical Blender serialization.
- regenerated Review Board SHA-256: `073d13c7f426e2a80808e22c982df126ab64130b1c935cc88f14fc2ba28f4f4b` = approved Review Board / MATCH
- regenerated Semantic SHA-256: `6e0c07709c83a1833c0059afc9023825d27ca47f077f2bf991612c251a1abaed`
- regenerated Validation SHA-256: `a6d780aff36afd6d22c45861aa2aa1517e0ce757b66e112145936d5ec1262df3`
- regression Artifact ID: `10634445266`
- regression Artifact ZIP SHA-256: `fb377ed8bc7034005a5872903620580858cda4f258921487ecea08a4b20413ec`
- section profile state: `UNKNOWN`
- section envelope historical claim: `false`
- adaptive Review Board: 7 required panels / PASS
- minimal-sufficient formal surface: PASS

Derived Registry Excel pre-merge sync:
- Run `35589254110` = **SUCCESS**
- source Registry commit: `9647e028f168c449fa86a2929181a577161faf4e`
- V008/CURRENT: 505 records
- Stage1 Catalog: 12 approved Masters
- 槫 binding: **33 / 33**
- Master progress: **12 / 28 = 42.9%**
- approved-Master-covered Registry rows: **99**
- current/versioned Excel SHA-256: `1fabd30cf851700ef9518f23d7a4ea65f8b489621636fe1a0506c32ec6669fb5`
- JSON remains canonical truth; Excel remains DERIVED_VIEW.

Static pre-merge cross-check:
- branch behind main: **0**
- PR mergeable: **true**
- changed-file scope: T-026 / shared V2 infrastructure / Catalog+V008 / derived Excel only
- D-094 locked Definition remained immutable after first-article acceptance
- approved Semantic / Validation / Review Board were exact D-095 Artifact bytes
- no canonical Purlin `.blend` is tracked in Git
- legacy `CMP-PURLIN-001` identity remains separated from the 33-instance Master
- T-018 remains HOLD
- Stage1 remains ACTIVE / not passed

No further engineering change is required before merge.

**PR #13 merge remains a separate Product Owner authorization boundary.**


## 17. Merge closure / D-096

**CLOSED / MERGED TO MAIN**

- Product Owner merge authorization: APPROVED
- PR: `#13`
- PR state: `MERGED / CLOSED`
- merge commit: `a588895004d61b0c5bc3615db4a74f1c2f4a91bc`
- main verification: PASS
- Stage1 Catalog: `12 approved Masters`
- 槫 V008/CURRENT binding: `33/33`
- Stage1 Master completion: `12/28 = 42.9%`
- approved first article: Run `35584601233` / `41/41 PASS`
- final regression: Run `35589254034` / `47/47 PASS`
- derived Excel sync: Run `35589254110` / SUCCESS
- canonical approved .blend remains Artifact/local-only with SHA-256 `5b14625130f57a744c3654c060ff2e06b2520df973fee5cf2974f39b13e663f4`
- section profile remains `UNKNOWN / BOUNDING_ENVELOPE_PROXY / NOT HISTORICAL`

T-026 is fully closed. Stage1 remains ACTIVE and does not pass as a whole. T-018 remains HOLD. Local Git synchronization is deferred to the evening batch.
