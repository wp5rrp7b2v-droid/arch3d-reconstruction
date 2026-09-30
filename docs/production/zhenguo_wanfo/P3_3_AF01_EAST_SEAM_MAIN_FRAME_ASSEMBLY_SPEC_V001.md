# P3.3｜AF-01 东缝正身梁架首榀 Assembly Spec V0.1 Candidate

- Date: **2026-09-30**
- Task: **AF-01**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Representative slice: **东缝正身梁架**
- Cross-check slice: **西缝正身梁架**
- Historical-standard-frame claim: **NO**

## 1. Purpose

AF-01 只建立一榀可执行的正身梁架装配规格。它不要求先完成整殿连接理论，也不把 UNKNOWN 榫卯补成历史事实。

东缝的选择是 engineering pilot selection；西缝保留为后续独立交叉验证。

## 2. Slice placement

Current project-model convention:

- slice role = `INNER_EAST_FRAME_AXIS`
- X = **+2218.5 mm**
- derivation = `0.5 × PM-008(14.5 chi) × MOD-001(306 mm/chi)`
- classification = **REPORT_INFERRED / RECONSTRUCTED_DESIGN / REPLACEABLE**
- this sign convention is a project-model coordinate convention, not a historical orientation-system claim.

## 3. Core Registry instance set｜11

| Role | Registry instance | Master |
|---|---|---|
| lower six-chuanfu | 下六椽栿-东缝 | CMP-FRAME-LOWER-SIX-CHUANFU-001_MASTER |
| upper six-chuanfu | 上六椽栿-东缝 | CMP-FRAME-UPPER-SIX-CHUANFU-001_MASTER |
| four-chuanfu | 四椽栿-东缝 | CMP-FRAME-FOUR-CHUANFU-001_MASTER |
| pingliang | 平梁-东缝 | CMP-FRAME-PINGLIANG-001_MASTER |
| shuzhu | 蜀柱-东缝 | CMP-FRAME-SHUZHU-001_MASTER |
| chashou north | 叉手-东缝-北侧 | CMP-FRAME-CHASHOU-001_MASTER |
| chashou south | 叉手-东缝-南侧 | CMP-FRAME-CHASHOU-001_MASTER |
| tuojiao north lower | 托脚-东缝-北下平槫 | CMP-FRAME-TUOJIAO-001_MASTER |
| tuojiao north upper | 托脚-东缝-北上平槫 | CMP-FRAME-TUOJIAO-001_MASTER |
| tuojiao south lower | 托脚-东缝-南下平槫 | CMP-FRAME-TUOJIAO-001_MASTER |
| tuojiao south upper | 托脚-东缝-南上平槫 | CMP-FRAME-TUOJIAO-001_MASTER |

## 4. Seven purlin interface targets

AF-01 does **not** create `槫-东缝-*` Registry instances. The longitudinal 槫 system intersects the east-seam slice through seven assembly interface targets.

| Role | Canonical control | Y mm | RZ planning Z mm |
|---|---|---:|---:|
| 北撩风槫 | N00 | -6808.5 | 3534.3 |
| 北下平槫 | N01 | -3595.5 | 4880.7 |
| 北上平槫 | N02 | -1836.0 | 5814.0 |
| 脊槫 | N03 | 0 | 7068.6 |
| 南上平槫 | S02 | +1836.0 | 5814.0 |
| 南下平槫 | S01 | +3595.5 | 4880.7 |
| 南撩风槫 | S00 | +6808.5 | 3534.3 |

Y is canonical from corrected T-020 / D-290+D-291.

The Z values are from the **D-063 locked RZ design contract** only. RZ production publication remains unauthorized; therefore these Z values are planning/cross-check values and may not yet be treated as a published production rule.

## 5. Resolved plan controls

| Control | Result |
|---|---:|
| outer column axes | Y = ±5355.0 mm |
| lower-purlin axes | Y = ±3595.5 mm |
| upper-purlin axes | Y = ±1836.0 mm |
| ridge axis | Y = 0 |
| lower six-chuanfu support-axis span | 10710.0 mm |
| upper six-chuanfu support-axis span | 10710.0 mm |
| four-chuanfu support-axis span | 7191.0 mm |
| pingliang support-axis span | 3672.0 mm |

**Important:** the four spans above are reconstructed-design **support-axis control spans**, not historical full member lengths and not yet approved visible body lengths.

## 6. Orientation / structural order

- 下六椽栿、上六椽栿、四椽栿、平梁：all remain in the east-seam transverse section plane and run north↔south.
- 蜀柱：vertical ridge-support member above Pingliang; endpoint-driven.
- 叉手：paired north/south diagonals from Pingliang upper connection region toward ridge-support region; no fixed historical angle.
- 托脚：four side/layer-specific diagonals according to Registry location; exact angle and endpoints endpoint-derived.

Vertical structural order retained for AF-01:

`LOWER SIX → UPPER SIX → SAN_DOU / INTERMEDIATE SUPPORT ROLE → FOUR-CHUANFU → PINGLIANG → SHUZHU + CHASHOU → RIDGE SUPPORT`

This is structural ordering only; it does not itself assign unsupported exact Z coordinates.

## 7. Reused locked connection semantics

AF-01 may directly reuse:

- D-277: Upper-six → San-dou support role → Four-chuanfu;
- D-279: Pingliang → Shuzhu;
- D-279: Pingliang → Chashou lower endpoint;
- D-279: Tuojiao → Four-chuanfu end support;
- D-279: Tuojiao → source-supported purlin role.

These records provide attachment semantics/regions only. They do not provide exact historical joinery or world XYZ points.

## 8. Blocking items before engineering generation

### AF01-B01｜Horizontal beam Z placement

Exact production Z for 下六椽栿 / 上六椽栿 / 四椽栿 / 平梁 is not currently closed by a valid production authority.

The previous T-018 FV-B numeric tier formula may **not** be reused: its later semantic-validity review explicitly rejected promoting ROOF-004/005/006 into exact Frame-tier placement authority.

### AF01-B02｜Visible body lengths / end extents

The support-axis spans are resolved, but exact visible body end extents are not.

The approved Masters explicitly prohibit reference-length leakage. Therefore 10710 / 7191 / 3672 mm must not silently become “historical full lengths.”

A later minimal rule must define reconstructed-design body extent from support axes + source-supported visible end treatment.

### AF01-B03｜Endpoint points for Shuzhu / Chashou / Tuojiao

D-279 closes the attachment regions but not the exact instance endpoints.

Endpoint-driven Masters require deterministic `P_lower / P_upper` for actual generated length and angle. The next closure must resolve only the minimum visible points needed for the east-seam pilot. Hidden historical joinery remains UNKNOWN.

## 9. Explicitly non-blocking UNKNOWN

The following do **not** block AF-01 once B01-B03 are solved:

- hidden mortise/tenon/groove shape;
- exact historical contact-face machining;
- member originality;
- report samples not individually mapped east↔west;
- exact historical San-dou geometry if beam placement is independently deterministic;
- D-285 matrix-wide atomic closure.

## 10. Excluded from AF-01 core

- physical 槫 Registry instances: represented only by seven slice interface targets;
- 剳牵: current Registry rows are not mapped to east seam;
- 襻间枋: longitudinal linkage outside the first transverse core;
- detailed dougong bodies: outside the 11-instance core unless a later placement blocker requires them.

## 11. Candidate Gate

**Candidate completeness: PASS**

AF-01 now has:

- representative slice: RESOLVED;
- 11 actual Registry instances: RESOLVED;
- plan axis and seven purlin Y targets: RESOLVED;
- basic orientation and structural order: RESOLVED;
- exact production 3D placement / visible body lengths / endpoint points: **3 bounded blockers remain**.

Therefore:

> **AF-01 Assembly Spec V0.1 Candidate is complete for Product Owner review, but Engineering Generation remains NOT READY / NOT AUTHORIZED.**

Next controlled step after approval:

**AF-01 Minimal Placement Closure｜resolve B01-B03 only.**
