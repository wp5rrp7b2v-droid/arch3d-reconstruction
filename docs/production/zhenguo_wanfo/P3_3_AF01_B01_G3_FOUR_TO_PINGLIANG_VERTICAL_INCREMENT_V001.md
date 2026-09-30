# AF-01 / B01-G3｜Four-Chuanfu → Pingliang Vertical Increment V001

- Date: **2026-09-30**
- Task: **AF01-B01-G3**
- Status: **CANDIDATE / DEPENDS ON G2 CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Engineering generation: **NOT AUTHORIZED**
- Scope: four-chuanfu lower support plane → pingliang lower support plane only

## 1. Dependency

G3 does not reopen G1.

G3 currently depends on the unapproved G2 candidate:

- `FOUR_CHUANFU_SUPPORT_PLANE_Z = 5658.4 mm`
- G2 status = `CANDIDATE / NOT YET LOCKED`

Therefore the absolute G3 output remains provisional until G2 is approved.

## 2. Direct same-building source findings

The report confirms:

- Pingliang is a separate main-frame beam in the east/west seam;
- Pingliang sits below the Shuzhu / Chashou ridge-support system;
- the report states generally that **屋架梁栿间用隔架斗栱之垫**;
- therefore the Four-Chuanfu → Pingliang transition is not treated as an arbitrary free gap.

CCM-C05 remains unresolved only because the existing repository had not converted this same-building beam-to-beam spacer relation into a deterministic vertical resolver.

## 3. Four-Chuanfu installed vertical extent

Approved Four-Chuanfu Master:

- observed mean `guang = 426.5 mm`;
- report design reading = 27.9 fen → rounded 28 fen;
- Master local section-width/guang is an observed section dimension.

AF-01 uses the same installation-orientation rule already introduced in G2:

- beam longitudinal axis → north/south;
- `guang / section_width` → world Z;
- local `thickness` → horizontal transverse section direction.

No Master mutation is required.

Therefore:

`FOUR_CHUANFU_TOP_Z = 5658.4 + 426.5 = 6084.9 mm`

## 4. Effective spacer-layer rise

For the same Wanfo Hall report:

- small dou / gong modular analysis resolves one supported cai layer at the **足材 21-fen** order;
- the roof-frame description states that beam/fu intervals use **隔架斗栱之垫**.

For AF-01 G3, the minimum deterministic reconstruction is therefore one effective spacer/support layer:

`FOUR_TO_PINGLIANG_SPACER_RISE = 21 fen`

At `MOD-002 = 15.3 mm/fen`:

`21 × 15.3 = 321.3 mm`

Classification:

**REPORT_INFERRED / SAME_BUILDING_BEAM-SPACER_LOGIC / RECONSTRUCTED_DESIGN / AF01_LOCAL / REPLACEABLE**

This is an effective support-plane increment only. It does not assert exact hidden dou/gong composition, body count, jointing, or machining.

## 5. G3 resolver

`PINGLIANG_SUPPORT_PLANE_Z`

= `FOUR_CHUANFU_SUPPORT_PLANE_Z`
+ `FOUR_CHUANFU_INSTALLED_VERTICAL_EXTENT`
+ `FOUR_TO_PINGLIANG_SPACER_RISE`

= `5658.4 + 426.5 + 321.3`

= **6406.2 mm**

Equivalent bottom-to-bottom vertical increment:

`G3_DELTA_Z = 747.8 mm`

## 6. Independent modular cross-check

Report design reading for Four-Chuanfu guang:

- observed mean = 426.5 mm;
- report rounded design = 28 fen.

Ideal modular check:

`28 + 21 = 49 fen`

`49 × 15.3 = 749.7 mm`

AF-01 actual-Master result:

`426.5 + 321.3 = 747.8 mm`

Difference:

`749.7 - 747.8 = 1.9 mm`

Relative difference ≈ **0.25%**.

Cross-check:

**PASS / CONSISTENT / NOT PRIMARY AUTHORITY**

AF-01 preserves the actual approved Four-Chuanfu Master section rather than silently replacing it with the rounded 28-fen value.

## 7. Pingliang installed body cross-check

East/west-seam Pingliang observed family mean:

- `guang = 395.5 mm`
- report rounded design = 26 fen
- sample-to-east/west mapping remains UNKNOWN.

Using the same installation orientation only as a forward check:

`PINGLIANG_TOP_Z = 6406.2 + 395.5 = 6801.7 mm`

This value is not required to close G3. It is retained only for later Shuzhu/Chashou endpoint work and does not close B03.

## 8. Evidence boundary

G3 resolves only the effective vertical support path.

It does not claim:

- exact physical identity/count of hidden spacer dou/gong pieces;
- exact spacer joinery;
- exact 963 absolute elevation;
- current deformed/as-measured Z;
- whole-hall generalization;
- Pingliang→Shuzhu/Chashou endpoint closure.

CCM-C05 may be treated for AF-01 as a locally resolved support-path rule only after Product Owner approval.

## 9. G3 Gate

Candidate outputs:

- `FOUR_CHUANFU_TOP_Z = 6084.9 mm`
- `FOUR_TO_PINGLIANG_SPACER_RISE = 321.3 mm`
- `G3_DELTA_Z = 747.8 mm`
- `PINGLIANG_SUPPORT_PLANE_Z = 6406.2 mm`
- forward check `PINGLIANG_TOP_Z = 6801.7 mm`

No Master mutation.
No Registry mutation.
No Blender.
T-018 remains HOLD.

Because G2 is still Candidate, G3 cannot be independently locked before G2.

If Product Owner approves both the pending G2 and this G3 candidate, B01 can close with four beam support planes:

- Lower Six = 4360.5 mm
- Upper Six = 5003.1 mm
- Four-Chuanfu = 5658.4 mm
- Pingliang = 6406.2 mm
