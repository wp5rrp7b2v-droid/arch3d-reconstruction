# P3.1 Canonical Master Asset Contract V002｜Change Proposal

Status: **APPROVED / IMPLEMENTED / D-036**  
Date: 2026-09-13  
Phase/Gate: `P3 / P3.1｜Component Master & Variant Library`  
Affected component: `CMP-LUDOU-COLUMN-001｜柱头栌斗`  
Previous locked contract: `P3_1_MASTER_ASSET_CONTRACT_V001` / D-034  
Implemented contract: `P3_1_MASTER_ASSET_CONTRACT_V002` / D-036

## 1. Reason for Change

在 D-035 批准 T-011 柱 Master Pilot 后，准备剩余五类 Master 的生产拆分时，对 V001 Contract 与 P1 直接核读证据进行了交叉核对。

发现 `CMP-LUDOU-COLUMN-001` 的四个平面尺寸字段存在**字段映射错误**。

这不是新证据，也不是历史解释变化，而是把已核实的“面阔下宽”和“进深总深”错误地写入了相反字段。

## 2. Authoritative Evidence

正式证据：

`docs/evidence/zhenguo_wanfo/P1_2_DIRECT_PAGE_REVIEW_V001.md`

D-007｜柱头栌斗，PDF p62–63 / 印刷 p47–48，表2-26、2-27：

- 面阔总宽：`475.1 mm`
- 面阔下宽：`327.1 mm`
- 进深总深：`446.3 mm`
- 进深下深：`305.5 mm`
- 总高：`293.8 mm`
- 平高：`58.75 mm`
- 欹高：`116.2 mm`

Evidence state remains:

`DIRECT_VERIFIED / observed_as_measured`

## 3. V001 Defect

V001 human-readable / machine-readable Contract 曾写成：

```text
top_width    = 475.1
top_depth    = 327.1   ← WRONG FIELD
bottom_width = 446.3   ← WRONG FIELD
bottom_depth = 305.5
```

其中：

- `327.1` 实际是 **面阔下宽 / bottom_width**；
- `446.3` 实际是 **进深总深 / top_depth**。

如果按 V001 直接生成几何，会把 X/Y 方向上下轮廓错误配对。

## 4. Approved V002 Correction

V002 将 `CMP-LUDOU-COLUMN-001.authorized_inputs_mm` 修正为：

```text
top_width     = 475.1
bottom_width  = 327.1
top_depth     = 446.3
bottom_depth  = 305.5
total_height  = 293.8
flat_height   = 58.75
sloped_height = 116.2
```

Human-readable Contract 同步表述为：

- top width / 面阔总宽 = `475.1 mm`
- bottom width / 面阔下宽 = `327.1 mm`
- top depth / 进深总深 = `446.3 mm`
- bottom depth / 进深下深 = `305.5 mm`

## 5. Explicit Non-Changes

V002 不改变：

- `CMP-LUDOU-COLUMN-001` 的 `MASTER_REQUIRED` 资格；
- evidence classification；
- total / flat / sloped heights；
- geometry mode `MEASURED_OUTER_ENVELOPE_WITH_BOUNDED_PROFILE`；
- replaceable linear interpolation rule；
- 禁止补造耳、槽、内部空腔、榫卯的边界；
- DG-114 boundary；
- 其余 5 个 Master 的任何参数或合同；
- T-011 / CMP-COLUMN-001 的任何资产、结论或 D-035 approval；
- P2 frozen baseline。

## 6. Versioning / Governance

Product Owner 已于 2026-09-13 批准本 Change Proposal（D-036）：

1. `P3_1_MASTER_ASSET_CONTRACT_V002.md` 已创建并锁定；
2. `P3_1_MASTER_ASSET_CONTRACT_V002.json` 已创建并锁定；
3. V002 继承 V001 全部规则，仅包含本 Proposal 的字段映射修正；
4. Decision Log 正式记录 D-036；
5. V001 保留历史记录，并由 Project Control 标记为被 V002 取代用于未来生产；
6. 后续 Master 生产一律以 V002 为 authoritative Contract；
7. 剩余五类恢复为 planning-ready，但仍需独立 Task Contract 授权。

## 7. Impact Assessment

- T-011 column Pilot: **NO IMPACT / remains APPROVED**
- Approved column Master V001: **NO IMPACT**
- Existing ludou Master geometry: **NONE PRODUCED**
- Asset migration required: **NONE**
- Historical claim change: **NONE**
- Evidence classification change: **NONE**
- Remaining-five production: **PLANNING READY / TASK AUTHORIZATION STILL REQUIRED**

## 8. Final Decision

**`P3.1 Canonical Master Asset Contract V002｜FIELD-MAPPING CORRECTION｜APPROVED / LOCKED / D-036`**

This is a controlled correction of an implementation contract transcription error, not a revision of the underlying historical evidence interpretation.
