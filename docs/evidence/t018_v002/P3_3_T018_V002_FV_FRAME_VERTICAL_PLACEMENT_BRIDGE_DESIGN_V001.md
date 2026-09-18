# T-018 V002｜FV Frame Vertical Placement Bridge Design V001

## Status

**DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED / IMPLEMENTATION FROZEN**

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Parent Task：T-018｜P3.3 整殿确定性生成与参数变更验证 V002
- Internal Module：FV｜Frame Vertical Placement Bridge
- Date：2026-09-18
- RZ prerequisite：D-063 LOCKED
- No Rule created
- No upstream artifact modified
- CP-03 remains STOP
- PR #6 remains HOLD

---

## 1. Problem to solve

Current Frame Y positions are already closed by:

- FR-004 = 1759.5 mm
- FR-005 = 1759.5 mm
- FR-006 = 1836.0 mm

Therefore the three half-depth Frame stations are:

- D1 = 1759.5 mm
- D2 = 3519.0 mm
- D3 = 5355.0 mm

The unresolved problem is exact engineering Z placement for:

- FRAME_TIER_N/S_01
- FRAME_TIER_N/S_02
- FRAME_TIER_N/S_03
- FRAME_POST_*_LOW / *_UP endpoints
- paired FRAME_SUPPORT proxies

P3.2 already defines LOWER/UPPER tier datums as semantic engineering controls with `historical_claim=false`, not historical elevations.

---

## 2. Evidence boundary

### 2.1 Inputs already associated with CTL-FRAME-001

P3.1 identifies the following as known P2 engineering inputs for the Frame Control family:

- FR-004 / FR-005 / FR-006 / FR-007
- MOD-002 / MOD-003 / MOD-004
- PM-012
- ROOF-004 / ROOF-005 / ROOF-006
- ROOF-007 / ROOF-008 / ROOF-009
- Z-006-RC-01

Critically, **DG-113 is not in the CTL-FRAME-001 known-input list**.

### 2.2 Parameter ownership

Current P3.3 binding ownership remains:

- FR-004/005/006 → ORG-FRAME-SYSTEM
- ROOF-004/005/006 → ORG-ROOF-SYSTEM
- DG-113 → ORG-BRACKET-SYSTEM
- Z-006-RC-01 → ORG-COLUMN-GRID + ORG-FRAME-SYSTEM
- MOD-002 → ORG-BUILDING

FV must not rewrite these owners.

FV may only create a bounded one-way **project-level bridge** from existing reconstructed-design candidates into non-historical Frame Control placement.

---

## 3. Candidate options

### FV-A｜Legacy P2 bridge

Legacy formula:

```
FRAME_BASE = Z-007 + Z-006-RC-01 + DG-113 * MOD-002

TIER_01 = FRAME_BASE + (ROOF-004 + ROOF-005 + ROOF-006) * MOD-002
TIER_02 = FRAME_BASE + (ROOF-004 + ROOF-005) * MOD-002
TIER_03 = FRAME_BASE + ROOF-004 * MOD-002
```

Current candidate values:

- FRAME_BASE = 3855.6 mm
- TIER_01 = 6104.7 mm
- TIER_02 = 4850.1 mm
- TIER_03 = 4238.1 mm

**Assessment：REJECT**

Reasons:

1. Introduces DG-113 from ORG-BRACKET-SYSTEM into Frame placement.
2. P3.1 CTL-FRAME known-input evidence does not include DG-113.
3. Legacy P2 used the same DG-113 offset in Roof Z, which RZ D-063 has already rejected.
4. Creates unnecessary Bracket→Frame coupling.
5. Higher regression risk: future bracket candidate replacement would move the whole Frame control system.

Legacy P2 remains diagnostic evidence only.

---

### FV-B｜Bounded Roof-Elevation Bridge without DG-113

Formula:

```
FRAME_BASE = Z-007 + Z-006-RC-01

TIER_01 = FRAME_BASE + (ROOF-004 + ROOF-005 + ROOF-006) * MOD-002
TIER_02 = FRAME_BASE + (ROOF-004 + ROOF-005) * MOD-002
TIER_03 = FRAME_BASE + ROOF-004 * MOD-002
```

Current candidate values:

- FRAME_BASE = 3534.3 mm
- TIER_01 = 5783.4 mm
- TIER_02 = 4528.8 mm
- TIER_03 = 3916.8 mm

North and south use identical tier Z at the same ordinal.

RZ roof-profile cross-check at Frame Y stations:

| Frame station | |Y| mm | FV-B tier Z | RZ roof profile Z | vertical clearance |
|---|---:|---:|---:|---:|
| Tier 01 | 1759.5 | 5783.4 | 6381.557... | +598.157... |
| Tier 02 | 3519.0 | 4528.8 | 5651.687... | +1122.887... |
| Tier 03 | 5355.0 | 3916.8 | 4600.2 | +683.4 |

All tiers remain strictly below the RZ roof profile.

**Assessment：RECOMMENDED FOR LOCKING**

Why this is the minimum safe bridge:

1. No Bracket parameter enters Frame placement.
2. Uses only parameters already recorded as engineering inputs to CTL-FRAME-001 or building modular datum.
3. Does not modify Roof authority; ROOF-004/005/006 remain owned by ORG-ROOF-SYSTEM.
4. Creates only a one-way Project Rule bridge:
   `ROOF elevation candidates → non-historical Frame Control Z`.
5. No new historical dimension.
6. No new P3.2 relation type.
7. Exact tier Z remains replaceable engineering placement, not proven 963 beam elevation.
8. Current RZ roof profile leaves positive clearance at all three stations.

Important:
ROOF-004/005/006 are not being renamed as “Frame parameters”.
They remain roof-elevation design candidates whose values are consumed by an explicitly bounded Frame-control engineering bridge.

---

### FV-C｜Roof-profile interpolation / drop-rule bridge

Possible variants would derive Frame Tier Z directly from:

- RZ roof profile interpolation;
- ROOF-012 / ROOF-013 drop values;
- arbitrary roof-to-frame clearance fractions.

**Assessment：REJECT**

Reasons:

1. No canonical mapping exists from ROOF-012/013 to the three Frame Tier ordinals.
2. Would require a new hidden clearance/ratio constant.
3. Would make Frame placement directly dependent on Roof shape in a way not already established.
4. Higher risk of Frame↔Roof circular dependency.

---

### FV-D｜No exact Z / semantic-only downgrade

Keep Frame Tier as ordinal metadata only with no spatial Z.

**Assessment：SAFE FALLBACK / NOT RECOMMENDED**

Pros:
- no new authority.

Cons:
- cannot satisfy current CP-03 requirement for an explicit whole-building control model;
- would require changing the T-018 V002 representation/acceptance contract;
- would push unresolved placement into later stages rather than close it.

Use only if FV-B fails formal review.

---

## 4. Recommended locked formula envelope

If Product Owner approves FV-B, the future locked contract should define:

Let:

- `D = Z-007.datum_mm = 0`
- `H = Z-006-RC-01`
- `F = MOD-002`
- `A = ROOF-004`
- `B = ROOF-005`
- `C = ROOF-006`

Then:

```
FRAME_BASE_Z = D + H

FRAME_TIER_01_Z = FRAME_BASE_Z + (A + B + C) * F
FRAME_TIER_02_Z = FRAME_BASE_Z + (A + B) * F
FRAME_TIER_03_Z = FRAME_BASE_Z + A * F
```

Current audit values:

```
FRAME_BASE_Z    = 3534.3 mm
FRAME_TIER_01_Z = 5783.4 mm
FRAME_TIER_02_Z = 4528.8 mm
FRAME_TIER_03_Z = 3916.8 mm
```

The numbering reflects the existing Frame Y station ordering from center outward, not historical member naming.

---

## 5. Endpoint contract

For each side N/S and tier k:

### FRAME_TIER
```
A = (grid_west_X, tier_Y_k, tier_Z_k)
B = (grid_east_X, tier_Y_k, tier_Z_k)
```

### FRAME_POST_*_LOW
```
A = (X_i, tier_Y_k, FRAME_BASE_Z)
B = (X_i, tier_Y_k, tier_Z_k)
```

### FRAME_POST_*_UP
```
A = (X_i, tier_Y_k, tier_Z_k)
B = (X_i, tier_Y_k, RZ_ROOF_PROFILE_Z(tier_Y_k))
```

The upper endpoint consumes RZ as a terminal target only.
Frame placement cannot modify RZ.

FRAME_SUPPORT proxies mirror the paired FRAME_CONTROL endpoints exactly and derive no coordinates independently.

---

## 6. Allowed dependency direction

```
Z-007 + Z-006-RC-01
        ↓
   FRAME_BASE_Z

ROOF-004/005/006 + MOD-002
        ↓
PROJECT_RULE: FV bridge
        ↓
FRAME_TIER Z
        ↓
FRAME_POST LOW / FRAME_SUPPORT

RZ roof profile
        ↓
FRAME_POST UP terminal only
```

Prohibited:

- DG-113 → Frame placement
- Bracket geometry → Frame placement
- Frame → RZ Roof Z
- FRAME_SUPPORT → FRAME_CONTROL
- Blender object transform → Frame authority
- arbitrary clearance/fraction constants
- observed RF/ROOF values → reconstructed-design placement

---

## 7. Evidence and claim boundary

Future FV rule must be:

- `source_layer = PROJECT_RULE`
- `time_layer = project_model_datum / engineering_control`
- `historical_claim = false`
- `historical_claim_upgrade = false`
- `replaceable = true`

The resulting tier Z values mean:

> “current project engineering control positions derived from approved reconstructed-design candidates”

They do **not** mean:

> “verified 963 historical beam elevations”.

FRAME_CONTROL remains CONTROL_ONLY.
FRAME_SUPPORT remains PROXY_ONLY.
PRIMARY_FRAME historical member identity remains unresolved unless separately qualified.

---

## 8. Impact boundary

Allowed direct changes if FV-B is later implemented:

- 6 FRAME_TIER Z values
- 24 FRAME_POST_*_LOW segments
- 24 FRAME_POST_*_UP segments
- paired 54 FRAME_SUPPORT proxy endpoints
- only declared engineering anchors for PRIMARY_FRAME if separately enabled

Must not change:

- GRID_CONTROL
- COLUMN origin / height
- RZ roof-control coordinates
- T-020 roof Y
- RAFTER / ROOF_ENVELOPE / GABLE topology
- BRACKET internal placement
- 365 identity/accounting
- 7/7 PURLIN DEFERRED
- P3.2 vocabulary
- historical claim boundaries

---

## 9. Required validation before CP-03 restart

A future FV implementation must independently verify:

1. DG-113 generative-use count for Frame = 0.
2. observed RF/ROOF values generative-use count = 0.
3. north/south same-tier Z identical.
4. `Tier01 > Tier02 > Tier03 > FRAME_BASE`.
5. every Tier remains below RZ roof profile at the same Y station.
6. FRAME_POST_LOW has positive length.
7. FRAME_POST_UP has positive length.
8. FRAME_SUPPORT endpoints exactly equal paired FRAME_CONTROL endpoints.
9. changing FV inputs affects only the declared FV affected set.
10. RZ roof coordinates remain bit-for-bit unchanged.
11. no identity/disposition/evidence change.
12. no Blender-local placement calculation.
13. validator calculates expected tier Z independently from compiler implementation.

---

## 10. Design conclusion

**Recommended candidate：FV-B**

This is a bounded project-engineering bridge, not a historical reconstruction claim.

It removes the unjustified DG-113 dependency from legacy P2 while retaining the already-recognized ROOF-004/005/006 engineering-input relationship to CTL-FRAME-001.

No current evidence requires:

- new historical dimensions;
- P3.0/P3.1/P3.2 reopen;
- T-020 modification;
- V003;
- new relationship vocabulary.

### Current governance state

This document is **DESIGN COMPLETE / PRODUCT OWNER REVIEW REQUIRED**.

It does not create or lock the FV authority.

Next decision:

> Product Owner approves / amends / rejects FV-B.

Only after explicit approval may a locked FV sub-contract be created.
