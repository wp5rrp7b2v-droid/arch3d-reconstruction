# AF-01 / B03-R｜Ridge-Support Endpoint Resolver V001

- Date: **2026-09-30**
- Task: **AF01-B03-R**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: 蜀柱-东缝 + 叉手-东缝-北侧 + 叉手-东缝-南侧 only

## 1. Locked inputs

Inherited AF-01 authority:

- east-seam slice X = **+2218.5 mm**
- Pingliang support plane Z = **6406.2 mm**
- Pingliang EW execution guang = **395.5 mm**
- Pingliang execution top surface Z = **6801.7 mm**
- Pingliang execution ends / inner support axes = **Y ±1836.0 mm = ±120 fen**
- ridge plan axis = **Y 0**
- MOD-002 = **15.3 mm/fen**

The report's Fig. 2-73 places the paired diagonal ridge-support legs on the ±120-fen inner control lines and the shared apex on Y=0. The same figure / report roof logic gives the upper-control-to-ridge rise as **82 fen**.

ROOF-009 already records that same report-derived relative rise:

`upper_to_ridge_purlin_rise_fen = 82`

This B03-R resolver uses only the **relative 82-fen rise**. It does NOT reuse the legacy T-018 absolute roof-Z chain.

## 2. Shared ridge-support connection Z

AF-01 anchors the relative Fig. 2-73 ridge triangle to the already locked Pingliang execution upper connection plane:

`RIDGE_SUPPORT_RISE = 82 × 15.3 = 1254.6 mm`

`RIDGE_SUPPORT_CONNECTION_Z = 6801.7 + 1254.6 = 8056.3 mm`

Classification:

**REPORT_INFERRED / FIG2-73 DRAWING_DERIVED / RECONSTRUCTED_DESIGN / AF01_LOCAL / REPLACEABLE**

This is not a directly surveyed historical absolute elevation.

## 3. Shuzhu endpoint pair

Locked Stage1 contract:

- lower semantic = `PINGLIANG_UPPER_SUPPORT_REGION`
- upper semantic = `RIDGE_SUPPORT_LOWER_CONNECTION_REGION`
- vertical member
- length endpoint-derived

AF-01 execution endpoints:

- `P_lower = (+2218.5, 0.0, 6801.7) mm`
- `P_upper = (+2218.5, 0.0, 8056.3) mm`

Derived execution length:

`L = 1254.6 mm`

Important evidence boundary:

The source also depicts/references a hump/support treatment above Pingliang. AF-01 core currently has no separate hump Registry/Master. Therefore the lower endpoint above is a **simplified execution surrogate on the Pingliang upper support region**, not a claim that the historical Shuzhu physical timber itself extended continuously to the bare Pingliang top surface.

If a formal hump component is added later, this endpoint may be replaced without changing the ridge apex authority.

## 4. North Chashou endpoint pair

Locked Stage1 contract:

- lower semantic = `PINGLIANG_UPPER_CONNECTION_REGION`
- upper semantic = `RIDGE_SUPPORT_CONNECTION_REGION`
- actual length and angle endpoint-derived

AF-01 endpoints:

- `P_lower_N = (+2218.5, -1836.0, 6801.7) mm`
- `P_upper_N = (+2218.5, 0.0, 8056.3) mm`

Derived:

- horizontal run = **1836.0 mm = 120 fen**
- rise = **1254.6 mm = 82 fen**
- execution length = **2223.7 mm**
- engineering angle from horizontal ≈ **34.35°**

The angle is a calculated execution result, not a fixed historical Master angle.

## 5. South Chashou endpoint pair

Mirror of the north member in the AF-01 section plane:

- `P_lower_S = (+2218.5, +1836.0, 6801.7) mm`
- `P_upper_S = (+2218.5, 0.0, 8056.3) mm`

Derived:

- horizontal run = **1836.0 mm**
- rise = **1254.6 mm**
- execution length = **2223.7 mm**
- engineering angle from horizontal ≈ **34.35°**

No separate geometry variant is created.

## 6. Deterministic roll/orientation rule

Endpoint vectors determine longitudinal orientation but do not by themselves fix roll around the member axis.

For AF-01:

### Shuzhu
- local +X = endpoint vector = world +Z
- local thickness axis is kept normal to the east-seam frame plane
- exact sign of the rectangular-section transverse axes is non-historical / engineering-only

### Chashou
- local +X = endpoint vector
- local thickness axis remains normal to the east-seam section plane (world X direction, sign irrelevant for the symmetric bounded envelope)
- local width axis remains inside the YZ section plane

This is an engineering placement rule only; it does not claim a historical rolling angle or end-face machining.

## 7. Cross-check

The Chashou triangle uses exactly the report-method proportions:

- run = **120 fen**
- rise = **82 fen**

Therefore:

`tan(theta) = 82 / 120`

and the generated north/south pair is symmetric around the ridge axis.

Cross-check status:

**PASS / FIG2-73 METHOD-GEOMETRY CONSISTENT**

## 8. Prohibitions

B03-R does not:

- promote T-018 `Z_RIDGE=7068.6` into AF-01 absolute authority;
- claim direct historical XYZ survey coordinates;
- use 1000 mm Master reference lengths;
- fix a historical Chashou angle in the Master;
- infer historical mortise/tenon/end cuts;
- close Tuojiao endpoints;
- create a hump component.

## 9. Candidate outputs

- `RIDGE_SUPPORT_CONNECTION_Z = 8056.3 mm`
- Shuzhu execution length = **1254.6 mm**
- North Chashou execution length = **2223.7 mm**
- South Chashou execution length = **2223.7 mm**

Endpoint coordinates:

| Instance | P_lower (X,Y,Z) mm | P_upper (X,Y,Z) mm |
|---|---|---|
| 蜀柱-东缝 | (2218.5, 0, 6801.7) | (2218.5, 0, 8056.3) |
| 叉手-东缝-北侧 | (2218.5, -1836, 6801.7) | (2218.5, 0, 8056.3) |
| 叉手-东缝-南侧 | (2218.5, +1836, 6801.7) | (2218.5, 0, 8056.3) |

No Master mutation.
No Registry mutation.
No Blender.
B03-T remains open.
T-018 remains HOLD.

If Product Owner approves:

**B03-R closes; AF-01 proceeds only to B03-T｜four Tuojiao endpoint mappings.**
