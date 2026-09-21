# T-026｜P3.3 槫 Master V2｜Lifecycle Record V001

Status: **DEFINITION LOCKED / D-094 / ENGINEERING EXECUTION AUTHORIZED / FIRST ARTICLE PENDING**  
Date: 2026-09-21  
Decisions: **D-093 / D-094**  
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
