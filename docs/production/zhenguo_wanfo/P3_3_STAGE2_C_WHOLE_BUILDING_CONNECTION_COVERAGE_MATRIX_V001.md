# P3.3 Stage2-C｜Whole-Building Connection Coverage Matrix V0.1

- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Decision: **D-281**
- Purpose: establish the complete Stage2-C connection-closure workload before any further Batch lock
- Approved Master coverage: **25/25**
- Connection/topology/handoff obligations: **39**
- Already locked from Batch 01/02: **5**
- Engineering: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Core rule

This is **not an UNKNOWN register**. Each row is a closure obligation. Before Stage2-C finishes it must become:
1. **MATERIALIZED_LOCKED**;
2. **EXPLICIT_NO_DIRECT_ATTACHMENT** with the actual intermediate path; or
3. **SYSTEM_HANDOFF_LOCKED**.

Historical joinery can remain evidence-bounded; production counterpart / endpoint / placement / orientation cannot remain permanently unresolved.

## Coverage summary

| Metric | V0.1 |
|---|---:|
| Approved Master families | 25 |
| Master families covered | 25 |
| Connection obligations | 39 |
| ATTACHMENT_CLASS | 10 |
| TOPOLOGY_RESOLUTION | 25 |
| SYSTEM_HANDOFF | 4 |
| Already locked requirements | 5 |
| Uncovered Masters | 0 |

## Whole-building connection obligations

| ID | Domain | Type | Participants | Required closure | Current status |
|---|---|---|---|---|---|
| CCM-A01 | COLUMN_LINTEL_PUZUO_BASE | ATTACHMENT_CLASS | CMP-COLUMN-001_MASTER ↔ CMP-LUDOU-COLUMN-001_MASTER | Materialize Stage2-C contact + coaxial locator; historical machining remains separately classified. | NEEDS_STAGE2C_MATERIALIZATION |
| CCM-A02 | COLUMN_LINTEL_PUZUO_BASE | ATTACHMENT_CLASS | CMP-COLUMN-001_MASTER ↔ CMP-FRAME-LANE-001_MASTER | Create left/right end contract; span derives from column-center relation; hidden tenon only explicit replaceable reconstructed design if needed. | NEEDS_CONNECTION_CONTRACT |
| CCM-A03 | COLUMN_LINTEL_PUZUO_BASE | ATTACHMENT_CLASS | CMP-COLUMN-001_MASTER ↔ CMP-FRAME-YOUE-001_MASTER | Create left/right end connection contract and deterministic span/orientation resolver. | NEEDS_CONNECTION_CONTRACT |
| CCM-A04 | COLUMN_LINTEL_PUZUO_BASE | TOPOLOGY_RESOLUTION | CMP-FRAME-LANE-001_MASTER ↔ CMP-DOU-BOTTOM-LONGKAI-001_MASTER | Verify actual bearer in same-building drawings; if Lane is bearer materialize Lane→Didou, otherwise replace participant before lock. | SOURCE_TOPOLOGY_VERIFY_THEN_MATERIALIZE |
| CCM-A05 | COLUMN_LINTEL_PUZUO_BASE | TOPOLOGY_RESOLUTION | CMP-LUDOU-COLUMN-001_MASTER ↔ COLUMN_HEAD_PUZUO_ROOT_COMPONENT_SET {CMP-GONG-HUAGONG-001_MASTER, CMP-GONG-GUAZI-001_MASTER, CMP-GONG-MANGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER, CMP-GONG-ANG-001_MASTER, CMP-GONG-LINGGONG-001_MASTER} | Resolve exact first-contact component(s) and dou roles; emit concrete Master-to-Master Connection Layer records. | ROLE_RESOLVER_REQUIRED |
| CCM-A06 | COLUMN_LINTEL_PUZUO_BASE | TOPOLOGY_RESOLUTION | CMP-DOU-BOTTOM-LONGKAI-001_MASTER ↔ BUJIAN_PUZUO_ROOT_COMPONENT_SET {CMP-GONG-HUAGONG-001_MASTER, CMP-GONG-GUAZI-001_MASTER, CMP-GONG-MANGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER, CMP-GONG-LINGGONG-001_MASTER} | Resolve exact first-contact component(s) and dou roles for infill puzuo; emit concrete pairwise records. | ROLE_RESOLVER_REQUIRED |
| CCM-B01 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [JUMP_1_TO_JUMP_2_CHAIN] {CMP-GONG-HUAGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Determine dou family at each jump transition and define lower/upper interfaces + projection resolver. | ROLE_RESOLVER_REQUIRED |
| CCM-B02 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [COLUMN_HEAD_MUDAO_GONG_STACK] {CMP-GONG-GUAZI-001_MASTER, CMP-GONG-MANGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Extract exact layer order and dou type; create concrete pairwise records. | ROLE_RESOLVER_REQUIRED |
| CCM-B03 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [COLUMN_HEAD_JUMP2_GONG_STACK] {CMP-GONG-GUAZI-001_MASTER, CMP-GONG-MANGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Extract exact second-jump layer order and dou type; materialize pairwise interfaces. | ROLE_RESOLVER_REQUIRED |
| CCM-B04 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [BUJIAN_MUDAO_GONG_STACK] {CMP-GONG-GUAZI-001_MASTER, CMP-GONG-MANGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Resolve exact infill small-gong + dou stack; do not copy column-head topology silently. | ROLE_RESOLVER_REQUIRED |
| CCM-B05 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [DOUBLE_MIAO_DOUBLE_XIA_ANG_CHAIN] {CMP-GONG-HUAGONG-001_MASTER, CMP-GONG-ANG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Resolve adjacency sequence and dou family at each Ang transition; preserve locked Ang slope/profile controls. | ROLE_RESOLVER_REQUIRED |
| CCM-B06 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [TOU_ANG_ER_ANG_RELATION] {CMP-GONG-ANG-001_MASTER} | Produce deterministic endpoint/support interfaces for both Ang variants and intervening support role(s). | ROLE_RESOLVER_REQUIRED |
| CCM-B07 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [OUTERMOST_JUMP_TERMINAL] {CMP-GONG-LINGGONG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER, CMP-GONG-HUAGONG-001_MASTER, CMP-GONG-ANG-001_MASTER} | Resolve actual supporting dou/member immediately below Linggong by unit class; materialize pairwise record(s). | ROLE_RESOLVER_REQUIRED |
| CCM-B08 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [DOU_ROLE_ASSIGNMENT_ALL_PUZUO_NODES] {CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Every bracket node must assign one allowed dou family or explicit non-dou connector; no anonymous dou placeholder at Stage2 exit. | ROLE_RESOLVER_REQUIRED |
| CCM-B09 | PUZUO_INTERNAL | TOPOLOGY_RESOLUTION | [PUZUO_UNIT_CLASS_TOPOLOGY] {CMP-GONG-HUAGONG-001_MASTER, CMP-GONG-GUAZI-001_MASTER, CMP-GONG-MANGONG-001_MASTER, CMP-GONG-LINGGONG-001_MASTER, CMP-GONG-ANG-001_MASTER, CMP-DOU-SINGLE-LONGKAI-001_MASTER, CMP-DOU-INTERACTIVE-001_MASTER} | Freeze explicit unit-class subgraphs so large/small gong and Ang presence are not inferred ad hoc per instance. | ROLE_RESOLVER_REQUIRED |
| CCM-C01 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | PUZUO_UPPER_SUPPORT ↔ CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER | Resolve real supporting component/interface replacing legacy generic proxy; bind Lower6 support interfaces. | REAL_COUNTERPART_REQUIRED |
| CCM-C02 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | PUZUO_OR_FRAME_SUPPORT ↔ CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER | Resolve actual supporter(s) from measured topology; no P3.2 control/proxy as production truth. | REAL_COUNTERPART_REQUIRED |
| CCM-C03 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER ↔ CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER | Decide direct attachment, indirect through real component(s), or EXPLICIT_NO_DIRECT_ATTACHMENT; remove ambiguity. | DISPOSITION_REQUIRED |
| CCM-C04 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER ↔ CMP-FRAME-FOUR-CHUANFU-001_MASTER → SAN_DOU_SUPPORT | Retain locked family class; later instance resolver maps real locations without promoting proxy geometry. | LOCKED_D277 |
| CCM-C05 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-FOUR-CHUANFU-001_MASTER ↔ CMP-FRAME-PINGLIANG-001_MASTER | Resolve direct vs explicit intermediate component(s); close vertical frame chain with deterministic interfaces. | REAL_COUNTERPART_OR_CONNECTOR_REQUIRED |
| CCM-C06 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-PINGLIANG-001_MASTER ↔ CMP-FRAME-SHUZHU-001_MASTER | Retain locked family attachment; plan anchor handled by deterministic resolver. | LOCKED_D279 |
| CCM-C07 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-PINGLIANG-001_MASTER ↔ CMP-FRAME-CHASHOU-001_MASTER | Retain locked lower-end attachment; upper counterpart closes separately. | LOCKED_D279 |
| CCM-C08 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-SHUZHU-001_MASTER ↔ RIDGE_SUPPORT_COUNTERPART | Identify actual counterpart; exact historic joinery may use explicit replaceable reconstructed design, but counterpart/endpoint must be deterministic. | COUNTERPART_AND_RESOLVER_REQUIRED |
| CCM-C09 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-CHASHOU-001_MASTER ↔ RIDGE_SUPPORT_COUNTERPART | Identify counterpart and solve P_upper deterministically; permanent null counterpart is not allowed. | COUNTERPART_AND_RESOLVER_REQUIRED |
| CCM-C10 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-TUOJIAO-001_MASTER ↔ CMP-FRAME-FOUR-CHUANFU-001_MASTER | Retain locked family support class; per-instance side mapping belongs later instance topology. | LOCKED_D279 |
| CCM-C11 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-TUOJIAO-001_MASTER ↔ CMP-FRAME-PURLIN-001_MASTER | Retain source-bounded purlin-role attachment; never generalize to all purlins. | LOCKED_D279 |
| CCM-C12 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-DINGFU-001_MASTER ↔ GABLE_COLUMN_HEAD_PUZUO | Create executable entry-direction, receive-region and parametric groove contract; historical claim limited by evidence. | NEEDS_DETERMINISTIC_CONNECTION_CONTRACT |
| CCM-C13 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-DINGFU-001_MASTER ↔ QIFUGONG_PURLIN_INTERSECTION_REGION | Resolve exact real counterpart(s), then materialize deterministic endpoint/connection records. | COUNTERPART_REQUIRED |
| CCM-C14 | PRIMARY_FRAME | ATTACHMENT_CLASS | CMP-FRAME-RUFU-001_MASTER ↔ BRACKET_SET_ASSEMBLY | Create endpoint orientation + receive-region + parametric groove contract; no fixed 45° assumption. | NEEDS_DETERMINISTIC_CONNECTION_CONTRACT |
| CCM-C15 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-RUFU-001_MASTER ↔ RUFU_OPPOSITE_FRAME_COUNTERPART | Resolve counterpart from source section and produce endpoint-derived length/orientation contract. | COUNTERPART_REQUIRED |
| CCM-C16 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-ZHAQIAN-001_MASTER ↔ ZHAQIAN_ENDPOINT_A_COUNTERPART | Resolve endpoint A counterpart; materialize interface and placement rule. | COUNTERPART_REQUIRED |
| CCM-C17 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-ZHAQIAN-001_MASTER ↔ ZHAQIAN_ENDPOINT_B_COUNTERPART | Resolve endpoint B counterpart and close deterministic span/orientation resolver. | COUNTERPART_REQUIRED |
| CCM-C18 | PRIMARY_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-PURLIN-001_MASTER ↔ ALL_PURLIN_SUPPORTER_MAP | Every purlin role/layer must have explicit supporter class; Tuojiao subset is locked but remaining layers must be mapped. | FULL_SUPPORT_MAP_REQUIRED |
| CCM-D01 | CORNER_FRAME | TOPOLOGY_RESOLUTION | CORNER_PUZUO_SUPPORT ↔ CMP-FRAME-DAJIAOLIANG-001_MASTER | Resolve actual corner-puzuo receiving node(s) and deterministic inboard endpoint; do not bake 45°. | COUNTERPART_AND_RESOLVER_REQUIRED |
| CCM-D02 | CORNER_FRAME | TOPOLOGY_RESOLUTION | CMP-FRAME-DAJIAOLIANG-001_MASTER ↔ CMP-FRAME-ZIJIAOLIANG-001_MASTER | Determine JOINERY_FEATURE vs CONTACT_INTERFACE and define endpoint relation + replaceable geometry. | CONNECTION_KIND_AND_RESOLVER_REQUIRED |
| CCM-D03 | CORNER_FRAME | SYSTEM_HANDOFF | CMP-FRAME-ZIJIAOLIANG-001_MASTER ↔ OUTBOARD_TERMINAL_ORNAMENT_ROLE | Define explicit terminal interface and handoff; ornament geometry stays separate scope. | HANDOFF_CONTRACT_REQUIRED |
| CCM-D04 | CORNER_FRAME | SYSTEM_HANDOFF | ↔ CORNER_RAFTER_SYSTEM {CMP-FRAME-DAJIAOLIANG-001_MASTER, CMP-FRAME-ZIJIAOLIANG-001_MASTER} | Define corner-rafter datum/orientation resolver without absorbing rafters into corner-beam geometry. | SYSTEM_HANDOFF_REQUIRED |
| CCM-E01 | ROOF_HANDOFF | SYSTEM_HANDOFF | CMP-FRAME-PURLIN-001_MASTER ↔ RAFTER_SYSTEM | Define purlin-top support interface, rafter axis/spacing/orientation handoff and deterministic resolver. | SYSTEM_HANDOFF_REQUIRED |
| CCM-E02 | ROOF_HANDOFF | SYSTEM_HANDOFF | RAFTER_SYSTEM ↔ ROOF_SHEATHING_WANGBAN_SYSTEM | Define roof-substrate support/contact handoff; tile pending-source items stay outside current Master denominator. | SYSTEM_HANDOFF_REQUIRED |

## 25-Master coverage

| Master | Requirement IDs | Coverage |
|---|---|---|
| CMP-COLUMN-001_MASTER | CCM-A01, CCM-A02, CCM-A03 | COVERED |
| CMP-LUDOU-COLUMN-001_MASTER | CCM-A01, CCM-A05 | COVERED |
| CMP-DOU-SINGLE-LONGKAI-001_MASTER | CCM-A05, CCM-A06, CCM-B01, CCM-B02, CCM-B03, CCM-B04, CCM-B05, CCM-B07, CCM-B08, CCM-B09 | COVERED |
| CMP-DOU-INTERACTIVE-001_MASTER | CCM-A05, CCM-A06, CCM-B01, CCM-B02, CCM-B03, CCM-B04, CCM-B05, CCM-B07, CCM-B08, CCM-B09 | COVERED |
| CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER | CCM-C01, CCM-C03 | COVERED |
| CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER | CCM-C02, CCM-C03, CCM-C04 | COVERED |
| CMP-FRAME-FOUR-CHUANFU-001_MASTER | CCM-C04, CCM-C05, CCM-C10 | COVERED |
| CMP-FRAME-PINGLIANG-001_MASTER | CCM-C05, CCM-C06, CCM-C07 | COVERED |
| CMP-FRAME-DINGFU-001_MASTER | CCM-C12, CCM-C13 | COVERED |
| CMP-FRAME-RUFU-001_MASTER | CCM-C14, CCM-C15 | COVERED |
| CMP-FRAME-ZHAQIAN-001_MASTER | CCM-C16, CCM-C17 | COVERED |
| CMP-FRAME-PURLIN-001_MASTER | CCM-C11, CCM-C18, CCM-E01 | COVERED |
| CMP-FRAME-TUOJIAO-001_MASTER | CCM-C10, CCM-C11 | COVERED |
| CMP-FRAME-CHASHOU-001_MASTER | CCM-C07, CCM-C09 | COVERED |
| CMP-FRAME-SHUZHU-001_MASTER | CCM-C06, CCM-C08 | COVERED |
| CMP-FRAME-DAJIAOLIANG-001_MASTER | CCM-D01, CCM-D02, CCM-D04 | COVERED |
| CMP-FRAME-ZIJIAOLIANG-001_MASTER | CCM-D02, CCM-D03, CCM-D04 | COVERED |
| CMP-FRAME-LANE-001_MASTER | CCM-A02, CCM-A04 | COVERED |
| CMP-FRAME-YOUE-001_MASTER | CCM-A03 | COVERED |
| CMP-DOU-BOTTOM-LONGKAI-001_MASTER | CCM-A04, CCM-A06 | COVERED |
| CMP-GONG-GUAZI-001_MASTER | CCM-A05, CCM-A06, CCM-B02, CCM-B03, CCM-B04, CCM-B09 | COVERED |
| CMP-GONG-MANGONG-001_MASTER | CCM-A05, CCM-A06, CCM-B02, CCM-B03, CCM-B04, CCM-B09 | COVERED |
| CMP-GONG-LINGGONG-001_MASTER | CCM-A05, CCM-A06, CCM-B07, CCM-B09 | COVERED |
| CMP-GONG-HUAGONG-001_MASTER | CCM-A05, CCM-A06, CCM-B01, CCM-B05, CCM-B07, CCM-B09 | COVERED |
| CMP-GONG-ANG-001_MASTER | CCM-A05, CCM-B05, CCM-B06, CCM-B07, CCM-B09 | COVERED |

## Evidence boundary

Primary source: `SRC-ZG-WF-001` (SHA-256 `94c2fedef64fd81ce225e04da4757d33ada34b9413b01baaf023fa72baed3472`).

Key ranges:
- PDF pp47–57: columns / lintels;
- PDF pp58–80: puzuo measurements and relationship drawings;
- PDF pp81–109: primary roof-frame measurement and structural analysis;
- PDF pp121–129: ideal model and layered structural reading.

## Governance effect

- PR #49 / D-280 is a **pre-matrix Draft** and is on HOLD. It is not eligible for lock/merge while this matrix is under review.
- No Batch 03/04/05 sequence is authoritative until this matrix is reviewed.
- After matrix lock, every future batch must be a slice of this matrix; ad-hoc connection selection is prohibited.
