# T-018 / FV｜Frame Vertical Placement Bridge V001

## Sub-contract｜LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Parent Task：T-018｜P3.3 整殿确定性生成与参数变更验证 V002
- Internal Module：FV｜Frame Vertical Placement Bridge
- Status：LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED
- Decision：D-064
- Date：2026-09-18
- Nature：non-historical project reconstruction convention
- Historical claim：false
- Replaceable：true
- Production publication：NOT AUTHORIZED
- Blender / Actions：NOT AUTHORIZED
- PR #6：HOLD / UNTOUCHED

> 本合同明确承认 FV 不是从史料中直接恢复出的梁架高程规则，而是为当前项目整殿控制几何建立的、显式标注且可替换的工程约定。

---

## 1. Policy decision

Product Owner chooses:

**A｜FV_PROJECT_RULE**

Therefore FV-B is approved only as:

- PROJECT_RULE
- project reconstruction convention
- historical_claim=false
- historical_claim_upgrade=false
- replaceable=true
- CONTROL_ONLY placement authority
- bounded one-way dependency
- not source-derived historical Frame elevation

It must never be described as verified 963 beam elevation.

---

## 2. Locked inputs

### Direct inputs

- Z-007
- Z-006-RC-01
- MOD-002
- ROOF-004
- ROOF-005
- ROOF-006

### Context / endpoint consumer

- RZ roof profile from D-063

### Explicitly prohibited

- DG-113
- ROOF-001 / ROOF-002 / ROOF-003
- RF observed dimensions as placement Z
- P2 world transforms
- Blender-local frame placement rules
- arbitrary clearance/fraction constants

ROOF-004/005/006 remain owned by the Roof system. FV consumes them through an explicit project-level bridge; it does not reclassify them as Frame parameters.

---

## 3. Locked formula

Let:

- `D = Z-007.datum_mm = 0`
- `H = Z-006-RC-01`
- `F = MOD-002`
- `A = ROOF-004`
- `B = ROOF-005`
- `C = ROOF-006`

Then:

```
FRAME_BASE_Z    = D + H

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

North and south use identical Z for the same tier ordinal.

The tier numbering follows the existing center-to-perimeter Frame station ordering and is an engineering control convention, not a historical member-name claim.

---

## 4. Locked Y positions

Frame Y stations remain controlled only by FR-004/005/006:

```
D1 = FR-004 = 1759.5 mm
D2 = FR-004 + FR-005 = 3519.0 mm
D3 = FR-004 + FR-005 + FR-006 = 5355.0 mm
```

North = negative Y.
South = positive Y.

FV does not redefine Frame Y.

---

## 5. Endpoint contract

For side N/S and tier k:

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

RZ is a downstream terminal target only.
FV may consume RZ roof profile for upper endpoints but may never modify RZ.

FRAME_SUPPORT proxies mirror the paired FRAME_CONTROL endpoints exactly.

---

## 6. Semantic boundary

The exact FV coordinates mean only:

> current project engineering control positions derived from existing reconstructed-design candidates.

They do not mean:

> verified original 963 Frame elevations.

The following classifications remain unchanged:

- FRAME_CONTROL = CONTROL_ONLY
- FRAME_SUPPORT = PROXY_ONLY
- PRIMARY_FRAME historical geometry remains independently evidence-bounded
- historical connector / joinery identity remains UNKNOWN where already UNKNOWN

---

## 7. Dependency direction

Allowed:

```
Z-007 + Z-006-RC-01 → FRAME_BASE_Z

ROOF-004/005/006 + MOD-002
        ↓
PROJECT_RULE: FV
        ↓
FRAME_TIER_Z
        ↓
FRAME_POST_LOW / FRAME_SUPPORT

RZ roof profile
        ↓
FRAME_POST_UP terminal only
```

Prohibited:

- DG-113 → Frame
- Bracket → Frame placement
- Frame → Roof/RZ
- FRAME_SUPPORT → FRAME_CONTROL
- Blender transform → authority
- validator output → compiler input
- any cyclic dependency

---

## 8. Impact boundary

Allowed to change under future approved FV execution:

- 6 FRAME_TIER Z values
- 24 FRAME_POST_*_LOW segments
- 24 FRAME_POST_*_UP segments
- paired FRAME_SUPPORT endpoints
- optional technical PRIMARY_FRAME anchors only if separately declared

Must remain unchanged:

- GRID_CONTROL
- COLUMN origins/heights
- RZ roof-control coordinates
- T-020 roof Y
- RAFTER topology
- ROOF_ENVELOPE topology
- GABLE_CONTROL topology
- BRACKET placement
- 365 identity/accounting
- P3.2 vocabulary
- 7/7 PURLIN DEFERRED
- historical-claim boundaries

---

## 9. Required validation

Future implementation must independently verify:

1. DG-113 Frame generative-use count = 0.
2. observed RF/ROOF values generative-use count = 0.
3. north/south same-tier Z identical.
4. `Tier01 > Tier02 > Tier03 > FRAME_BASE`.
5. every Tier is strictly below RZ roof profile at the same Y.
6. every FRAME_POST_LOW length > 0.
7. every FRAME_POST_UP length > 0.
8. FRAME_SUPPORT endpoints exactly mirror paired FRAME_CONTROL.
9. only declared FV affected IDs change under FV input mutation.
10. RZ coordinates remain bit-for-bit unchanged.
11. no identity/disposition/evidence status changes.
12. no Blender-local derivation.
13. validator computes expected FV independently from compiler code.

---

## 10. Governance boundary

D-064 locks the FV design contract only.

D-064 does **not** authorize:

- production machine-readable Rule publication;
- Codex implementation;
- PR creation/update;
- CP-03 restart;
- Blender / GitHub Actions;
- Stage B PASS;
- Stage C;
- merge.

After RZ D-063 + FV D-064 are both locked, the next governance step is a separate authorization for the **minimal authority publication package** and Stage-A closure regression.

Until that authorization, implementation remains frozen.
