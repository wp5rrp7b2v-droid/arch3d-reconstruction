# T-018 / RZ｜Roof Z Cumulative Closure V001

## Sub-contract｜LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Parent Task：T-018｜P3.3 整殿确定性生成与参数变更验证 V002
- Internal Module：RZ｜Roof Z Cumulative Closure
- Status：LOCKED / PRODUCT OWNER APPROVED / EXECUTION NOT AUTHORIZED
- Decision：D-063
- Date：2026-09-18
- Nature：bounded additive project-rule design contract
- Production publication：NOT AUTHORIZED
- Blender / Actions：NOT AUTHORIZED
- PR #6：HOLD / UNTOUCHED

> 本合同只锁定屋顶 Z 累计坐标的唯一公式，不修改 T-020，不新增历史尺寸，不改变任何 X/Y 坐标、identity、disposition 或 P3.2 vocabulary。

---

## 1. Why RZ exists

T-020 已明确屋顶 Z authority 为：

- Z-007
- Z-006-RC-01
- ROOF-007
- ROOF-008
- ROOF-009

但 T-020 有意没有重新定义 Z，也没有把这五项序列化为完整的 whole-building cumulative placement formula。

RZ 只补这个缺口：

> **把既有 Z authority 明确组合成唯一、机器可执行、可独立验证的屋顶控制 Z 链。**

RZ 不引入新的建筑事实。

---

## 2. Locked inputs

### Primary generative inputs

| ID | Role in RZ |
|---|---|
| Z-007 | project Z datum；Z0 reference plane |
| Z-006-RC-01 | approved replaceable column-height rule |
| MOD-002 | fen→mm modular conversion |
| ROOF-007 | eave→lower-purlin rise |
| ROOF-008 | lower→upper-purlin rise |
| ROOF-009 | upper→ridge rise |

### Validation-only cross-checks

| ID | Use |
|---|---|
| ROOF-010 | total roof rise = 231 fen consistency check |
| ROOF-011 | total roof rise = 3534.3 mm consistency check |

ROOF-010 / ROOF-011 **不得成为第二套 cumulative placement authority**。

### Explicitly excluded

- DG-113
- ROOF-004 / ROOF-005 / ROOF-006
- ROOF-001 / ROOF-002 / ROOF-003
- P2 whole-building transforms
- any Blender-local coordinate rule
- any locally invented eave/ridge offset

---

## 3. Locked formula

Use exact deterministic decimal arithmetic.

Let:

- `D = Z-007.datum_mm = 0`
- `H = Z-006-RC-01 = 3534.3 mm`
- `F = MOD-002 = 15.3 mm/fen`
- `R1 = ROOF-007 = 88 fen`
- `R2 = ROOF-008 = 61 fen`
- `R3 = ROOF-009 = 82 fen`

Then:

```
Z_EAVE  = D + H
Z_LOWER = Z_EAVE  + R1 * F
Z_UPPER = Z_LOWER + R2 * F
Z_RIDGE = Z_UPPER + R3 * F
```

Canonical audit values for current candidate inputs:

```
Z_EAVE  = 3534.3 mm
Z_LOWER = 4880.7 mm
Z_UPPER = 5814.0 mm
Z_RIDGE = 7068.6 mm
```

Cross-checks:

```
R1 + R2 + R3 = 231 fen = ROOF-010
231 * 15.3 = 3534.3 mm = ROOF-011
Z_RIDGE - Z_EAVE = 3534.3 mm
```

No binary-float approximation may become authority. Runtime serialization must preserve a deterministic decimal result.

---

## 4. Locked control mapping

| Roof control identity | Z authority result |
|---|---:|
| ROOF_PURLIN_N_00 | Z_EAVE |
| ROOF_PURLIN_S_00 | Z_EAVE |
| ROOF_PURLIN_N_01 | Z_LOWER |
| ROOF_PURLIN_S_01 | Z_LOWER |
| ROOF_PURLIN_N_02 | Z_UPPER |
| ROOF_PURLIN_S_02 | Z_UPPER |
| ROOF_PURLIN_N_03 | Z_RIDGE |

There is no `ROOF_PURLIN_S_03`.

North and south controls at the same level must have identical Z.

---

## 5. Dependency direction

Allowed:

```
Z-007
  + Z-006-RC-01
  + MOD-002
  + ROOF-007/008/009
            ↓
     RZ roof-control Z
            ↓
  RAFTER / ROOF_ENVELOPE / GABLE_CONTROL
            ↓
  FRAME_POST_*_UP terminal consumer
```

Prohibited:

- Frame → Roof Z
- Bracket → Roof Z
- DG-113 → Roof Z
- Representation → Roof Z
- Blender object transform → Roof Z
- Validator expected value → compiler formula

RZ is strictly one-way.

---

## 6. Direct and downstream impact

### Direct RZ outputs

Only seven technical roof-control Z values.

### Authorized downstream consumers after later execution approval

- 36 RAFTER endpoints
- 6 ROOF_ENVELOPE surface vertices
- 4 GABLE_CONTROL polyline vertices
- FRAME_POST_*_UP roof-terminal endpoints

These consumers do not gain authority of their own.

### Must remain unchanged

- all roof-control Y coordinates from T-020
- all roof X stations / gable projection
- GRID_CONTROL
- COLUMN origins and heights
- FRAME_TIER Z
- FRAME_POST_*_LOW endpoints
- 365 identities / family counts
- PURLIN disposition = 7/7 DEFERRED
- N03 sole shared ridge
- P3.2 relationship vocabulary
- PM-003..PM-007 generative-use count = 0
- historical-claim boundaries

---

## 7. Evidence boundary

RZ metadata when eventually published must remain:

- `source_layer = PROJECT_RULE`
- `historical_claim = false`
- `historical_claim_upgrade = false`
- `replaceable = true`
- reconstructed-design / engineering placement only

The exact Z coordinates are **not** to be stated as directly observed 963 historical measurements.

If any input candidate is later legitimately replaced, RZ must recompute; coordinates must not be baked.

---

## 8. Required validation

A future RZ implementation must independently reject at least:

1. DG-113 injected into roof Z formula.
2. ROOF-004/005/006 substituted for ROOF-007/008/009.
3. observed ROOF-001/002/003 used as generative placement.
4. any change to T-020 Y coordinates.
5. creation of ROOF_PURLIN_S_03 or second ridge.
6. north/south same-level Z mismatch.
7. non-monotonic eave→ridge Z.
8. total rise mismatch with ROOF-010 / ROOF-011.
9. historical_claim upgrade.
10. protected identity/disposition change.
11. baked literal coordinates replacing canonical inputs.
12. Blender-local re-derivation.

Validator must calculate expected cumulative Z independently from the implementation/compiler code path.

---

## 9. Lock boundary

D-063 locks this design contract only.

D-063 does **not** authorize:

- creation/modification of production canonical rule artifacts;
- Codex implementation;
- PR creation/update;
- CP-03 restart;
- Blender / GitHub Actions;
- Stage B PASS;
- Stage C;
- merge.

Next RZ action, if approved later:

> publish the locked RZ contract as a minimal machine-readable project-rule companion through governed engineering execution, then run independent RZ validation.

Until then implementation remains frozen.
