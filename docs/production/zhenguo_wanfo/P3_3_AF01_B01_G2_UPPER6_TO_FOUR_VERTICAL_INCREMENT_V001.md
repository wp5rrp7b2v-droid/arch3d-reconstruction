# AF-01 / B01-G2｜Upper-Six → Four-Chuanfu Vertical Increment V001

- Date: **2026-09-30**
- Task: **AF01-B01-G2**
- Status: **CANDIDATE / REVIEW PATCH 01 APPLIED / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: upper-six lower support plane → four-chuanfu lower support plane only

## 1. Inherited G1 authority

Locked by D-292:

- `UPPER_SIX_SUPPORT_PLANE_Z = 5003.1 mm`
- classification = `REPORT_INFERRED / DRAWING_DERIVED / RECONSTRUCTED_DESIGN / AF01_LOCAL / REPLACEABLE`

G2 does not reopen G1.

## 2. Direct same-building structural evidence

The measured report states:

- 四椽栿位于上六椽栿之上；
- 四椽栿与其下的上六椽栿之间垫隔架单栱一组；
- 隔架单栱下不用栌斗；
- 仅由一散斗承托。

This is already locked as D-277 family semantic:

`UPPER6_TOP → SAN_DOU_ROLE → FOUR_BOTTOM`

D-277 does not provide connector geometry or world Z.

## 3. Report modular evidence for the intermediate support layer

The same report's dou analysis gives a repeated design logic:

- small/long-open dou height is around 10–11 fen;
- gong/cai guang is around 14 fen;
- because the gong beds into the dou mouth, the combined vertical layer is not the arithmetic sum of the two full bodies;
- the report explicitly concludes the dou + cai combination **“恰可凑足足材广21分”**.

For G2, the direct four-chuanfu statement is exactly one san-dou-supported single-gong intermediate layer.

Therefore AF-01 resolves the required **effective support-plane rise** as:

`INTERMEDIATE_SUPPORT_LAYER_RISE = 21 fen`

At `MOD-002 = 15.3 mm/fen`:

`21 × 15.3 = 321.3 mm`

Classification:

**REPORT_INFERRED / SAME_BUILDING_MODULAR_LOGIC / RECONSTRUCTED_DESIGN / AF01_LOCAL / REPLACEABLE**

This does NOT assert the exact hidden geometry, total body height, notch depth or historical shape of the san-dou or single gong.

## 4. Upper-six installed vertical extent

The report states that the **guang** of the upper/lower six-chuanfu is directly related to the puzuo cai module.

For the approved upper-six Master:

- observed mean `guang = 334.0 mm`;
- Master stores this as local `section_width`;
- world placement has not previously fixed the beam roll.

For AF-01 installation only:

- member longitudinal axis → north/south;
- local `section_width / 广` → **world Z**;
- local `max_thickness` → horizontal transverse section direction.

This is an **assembly rotation/orientation rule**, not a Master mutation.

Therefore:

`UPPER_SIX_TOP_Z = 5003.1 + 334.0 = 5337.1 mm`

## 5. G2 resolver

`FOUR_CHUANFU_SUPPORT_PLANE_Z`

= `UPPER_SIX_SUPPORT_PLANE_Z`
+ `UPPER_SIX_INSTALLED_VERTICAL_EXTENT`
+ `INTERMEDIATE_SUPPORT_LAYER_RISE`

= `5003.1 + 334.0 + 321.3`

= **5658.4 mm**

Equivalent bottom-to-bottom vertical increment:

`G2_DELTA_Z = 655.3 mm`

## 6. Independent modular cross-check

Report design rounding for upper-six guang:

- observed 334.0 mm = 21.8 fen;
- report rounded design reading = 22 fen.

Ideal modular check:

`22 + 21 = 43 fen = 657.9 mm`

AF-01 actual-Master placement result:

`334.0 + 321.3 = 655.3 mm`

Difference:

`657.9 - 655.3 = 2.6 mm`

Relative difference ≈ **0.40%**.

Cross-check:

**PASS / CONSISTENT / NOT PRIMARY AUTHORITY**

AF-01 uses the approved Master observed mean geometry, not the rounded 22-fen design value, so no geometry is silently resized.

## 7. Evidence boundary

G2 resolves only the effective vertical support offset.

It does not create or claim:

- a physical Registry instance for the san-dou;
- an exact san-dou shape or dimensions;
- an exact 隔架单栱 body;
- hidden mortise/tenon/notch geometry;
- exact historical contact-face machining;
- whole-puzuo topology closure;
- 963 absolute elevation truth.

D-277 connector geometry remains `UNKNOWN / NOT MATERIALIZED`.

## 8. G2 Gate

Candidate outputs:

- `UPPER_SIX_TOP_Z = 5337.1 mm`
- `INTERMEDIATE_SUPPORT_LAYER_RISE = 321.3 mm`
- `G2_DELTA_Z = 655.3 mm`
- `FOUR_CHUANFU_SUPPORT_PLANE_Z = 5658.4 mm`

No Master mutation.
No Registry mutation.
No Blender.
T-018 remains HOLD.

If Product Owner approves:

**G2 closes and B01 advances only to G3｜Four-Chuanfu → Pingliang support path.**

## 9. Review Patch 01｜2026-09-30

Joint G2/G3 review result for G2: **PASS**.

Evidence checks:
- direct Four-Chuanfu source explicitly supplies the Upper-Six → single-gong spacer → san-dou → Four-Chuanfu structural relation;
- the report's same-building dou/gong modular analysis supports a 21-fen effective supported-cai layer as a replaceable reconstructed-design rule;
- Upper-Six `广` is directly related by the report to the puzuo cai vertical module, so AF-01 may orient `广` into world Z.

Implementation guard:

After rotating the Master so local `section_width / 广` becomes world Z, a future builder MUST resolve the transformed body bottom face/bounding-plane to `UPPER_SIX_SUPPORT_PLANE_Z`. It MUST NOT simply assign the Master object origin Z to the support-plane value, because the canonical Master origin was defined in a different local orientation.

This guard changes no numeric G2 result.
