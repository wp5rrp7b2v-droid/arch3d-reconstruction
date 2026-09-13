# P3.1 Component Master Scope Matrix V001｜T-010

Status: **T-010 VALIDATED / PRODUCT OWNER REVIEW REQUIRED**
This is a qualification decision only; no Master or Variant geometry is authorized or produced.

P3.0 11/11 and P1 minimum 9/9 are reviewed. A `MASTER_REQUIRED` result licenses later asset-contract review, not an exact 963 geometry claim. All P3.0 records remain unchanged.

| Candidate ID | 来源 | 构件/对象 | 最终资格 | 主要理由 |
|---|---|---|---|---|
| PRX-BRACKET-JUMP-001 | BRACKET_ARM | 未定铺作出跳代理 | PROXY_ONLY | P2 equal jump subdivisions are aggregate graphic topology; DG-110–113 do not identify individual 栱 or 昂. |
| PRX-BRACKET-CONTACT-001 | BRACKET_CONTACT | 铺作端点接触代理 | PROXY_ONLY | Diagrammatic contact block is not 小斗; DG-114 unified-small-dou rule remains UNKNOWN. |
| CMP-COLUMN-001 | COLUMN | 柱 | MASTER_REQUIRED | Column type and observed diameter are verified; a reusable parametric column body is feasible while Z-006 remains unknown. |
| CTL-FRAME-001 | FRAME_CONTROL | 梁架层位控制对象 | CONTROL_ONLY | Frame-tier locator has no physical historical member identity. |
| PRX-FRAME-CONNECTOR-001 | FRAME_SUPPORT | 梁架层位连接代理 | PROXY_ONLY | P2 connector endpoints do not identify 托脚, 蜀柱 or joints. |
| CTL-GABLE-001 | GABLE_CONTROL | 山面轮廓控制对象 | CONTROL_ONLY | Gable diagnostic line is not 博风板, 角梁 or another physical member. |
| CTL-GRID-001 | GRID_CONTROL | 柱网定位控制对象 | CONTROL_ONLY | Grid locator is not a column or historical member. |
| UNR-PRIMARY-FRAME-001 | PRIMARY_FRAME | 未分解主体梁架代理 | PROXY_ONLY | Aggregate P2 frame meshes cannot be assigned to individual 六椽栿, 梁 or 枋. |
| CMP-PURLIN-001 | PURLIN | 槫类构件 | DEFERRED_INSUFFICIENT_EVIDENCE | 槫 is a verified type term, but P2 one section/variant is an engineering envelope, not a measured component profile. |
| CMP-RAFTER-001 | RAFTER | 椽类构件 | DEFERRED_INSUFFICIENT_EVIDENCE | 椽 type is real, but P2 slope segments and spacing are diagrammatic. |
| ENV-ROOF-001 | ROOF_ENVELOPE | 屋面连续形态包络 | ENVELOPE_ONLY | Zero-thickness surface strips are not tiles, boarding or solid roof members. |
| CMP-LUDOU-COLUMN-001 | BRACKET_CONTACT | 柱头栌斗 | MASTER_REQUIRED | Distinct named column-head斗 with measured width/depth/height supports a bounded reusable type; P2 contact block supplies no geometry. |
| CMP-DOU-BOTTOM-LONGKAI-001 | BRACKET_CONTACT | 底斗 | DEFERRED_INSUFFICIENT_EVIDENCE | Named and measured distinct斗 type, but missing depth prevents a qualified canonical 3D Master; DG-114 cannot fill it. |
| CMP-DOU-SINGLE-LONGKAI-001 | BRACKET_CONTACT | 单向长开斗 | MASTER_REQUIRED | Named orientation-specific斗 with distinct measured profile; future placement rotation alone does not create another type. |
| CMP-DOU-INTERACTIVE-001 | BRACKET_CONTACT | 交互斗 | MASTER_REQUIRED | Explicit measured斗 identity and profile distinguish it from a generic contact block; no unified small-dou design claim. |
| CMP-FRAME-LOWER-SIX-CHUANFU-001 | PRIMARY_FRAME | 下六椽栿 | MASTER_REQUIRED | Independent lower six-rafter beam identity and observed section support a bounded parametric member type; P2 frame mesh is not inherited. |
| CMP-FRAME-UPPER-SIX-CHUANFU-001 | PRIMARY_FRAME | 上六椽栿 | MASTER_REQUIRED | Independent upper six-rafter beam identity and distinct observed section support a bounded parametric member type; P2 frame mesh is not inherited. |
| P1-REVIEW-COLUMN-HEAD-NIDAO-GONG | BRACKET_ARM | 柱头泥道栱 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-LARGE-MAN-GONG | BRACKET_ARM | 大型慢栱 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-HUA-GONG | BRACKET_ARM | 华栱 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-INTERCOLUMN-NIDAO-GUAZI-GONG | BRACKET_ARM | 补间泥道瓜子栱 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-LOWER-ANG | BRACKET_ARM | 下昂 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-FOUR-CHUANFU | PRIMARY_FRAME | 四椽栿 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-PING-LIANG | PRIMARY_FRAME | 平梁 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-TUO-JIAO | FRAME_SUPPORT | 托脚 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-LAN-E | PRIMARY_FRAME | 阑额 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |
| P1-REVIEW-INTERCOLUMN-SEATED-DOU | BRACKET_CONTACT | 补间坐斗 | DEFERRED_INSUFFICIENT_EVIDENCE | Historical component term merits review, but source grade or member geometry does not meet Master threshold. |

## Coverage and counts

- P3.0 Registry: 11/11; P1 minimum: 9/9; total: 27.
- `MASTER_REQUIRED`: 6.
- `EVIDENCE_REVIEW_BEFORE_MASTER`: 0.
- `PROXY_ONLY`: 4.
- `CONTROL_ONLY`: 3.
- `ENVELOPE_ONLY`: 1.
- `DEFERRED_INSUFFICIENT_EVIDENCE`: 13.

## Decision boundaries

- `BRACKET_CONTACT` remains a contact proxy. The four measured斗 identities are independent P1-derived candidates; they do not inherit contact-block mesh or DG-114.
- `BRACKET_ARM`, `PRIMARY_FRAME` and `FRAME_SUPPORT` retain their P3.0 proxy identities. Named P1 members are separate records; secondary/bridge-only mentions are deferred.
- `PURLIN` uses the report term 槫, with 撩风/下平/上平/脊槫 treated as positions pending section comparison. `RAFTER` retains 椽; 檐椽/飞椽 split is not licensed. Placement alone is an instance distinction, not a Variant.
- All `MASTER_REQUIRED` geometry is bounded to observed/reference dimensions or explicit free parameters. Exact joints, component originality and 963 design dimensions remain unresolved.
- `CONTROL_ONLY` and `ENVELOPE_ONLY` are excluded from historical Master counts. P2's 365 placements are not a historical inventory.
- T-010 COMPLETE does not mark P3.1 PASS or authorize the next geometry task.
