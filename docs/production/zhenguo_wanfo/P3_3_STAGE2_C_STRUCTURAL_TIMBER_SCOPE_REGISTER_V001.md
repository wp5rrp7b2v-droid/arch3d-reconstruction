# P3.3 Stage2-C｜Structural Timber Scope Register V0.1

- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Decision: **D-283**
- V008 objects reviewed: **66/66**
- IN: **33**
- OUT: **27**
- CONTAINER: **5**
- CONDITIONAL: **1**
- Engineering: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Formal scope definition

Stage2-C Structural Timber Scope includes:

> physical timber components, indispensable timber connector roles, and timber-system handoffs required to form a continuous deterministic structural-timber assembly network.

It does **not** mean all V008 building objects, and it does **not** mean only the 25 Master families.

### Stop boundaries

- **Lower:** Column lower support → foundation support interface → **STOP**
- **Upper:** Purlin → rafter system → wangban system → **STOP**
- **Enclosure:** Structural timber frame → enclosure interface → **STOP**
- **Corner ornament:** Corner timber terminal → ornament handoff → **STOP**

## Candidate denominator

If approved, the Stage2-C connection matrix denominator becomes:

- **33 IN object types**
- plus any later-promoted CONDITIONAL item
- **5 CONTAINER items do not create physical edges**

The 33 IN objects consist of:
- 28 Master-bound object types, represented by 25 approved Master families;
- 椽系;
- 襻间枋;
- 望板系统;
- 隐角梁;
- 散斗族.

The only CONDITIONAL item is:
- **替木实体族**

## 66-object disposition

| # | Object | Stage2-A class | Scope | Role | Reason |
|---:|---|---|---|---|---|
| 01 | 北门洞 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_OPENING | Opening/enclosure scope, not structural timber skeleton. |
| 02 | 北坡筒瓦 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof covering above the wangban STOP boundary. |
| 03 | 补间铺作 | TOPOLOGY_OR_ASSEMBLY_CONTAINER | **CONTAINER** | ORGANIZATIONAL_TOPOLOGY_CONTAINER | Organizes relations/instances but is not itself a physical attachment object. |
| 04 | 补间铺作底斗 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 05 | 叉手 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 06 | 椽系 | PARAMETRIC_SYSTEM_OR_COMPLETION | **IN** | PARAMETRIC_TIMBER_SYSTEM | 主体屋架木构链必须由槫继续闭合到椽系；Stage2-C structural timber upper chain requires this handoff. |
| 07 | 窗木作系统 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ENCLOSURE_TIMBER | Timber enclosure/joinery system; intentionally deferred beyond structural timber closure. |
| 08 | 垂脊 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof ridge covering system beyond structural timber STOP boundary. |
| 09 | 垂兽 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_ORNAMENT | Roof ornament beyond structural timber scope. |
| 10 | 剳牵 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 11 | 大角梁 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 12 | 大型瓜子栱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 13 | 大型慢栱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 14 | 单向长开斗族 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 15 | 丁栿 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 16 | 东坡筒瓦 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof covering above the wangban STOP boundary. |
| 17 | 二昂 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 18 | 华栱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 19 | 交互斗族 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 20 | 角石 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_FOUNDATION_STONE | Stone/base system below the structural timber lower STOP boundary. |
| 21 | 阑额 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 22 | 令栱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 23 | 门木作系统 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ENCLOSURE_TIMBER | Timber enclosure/joinery system; intentionally deferred beyond structural timber closure. |
| 24 | 南立面窗洞 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_OPENING | Opening/enclosure scope, not structural timber skeleton. |
| 25 | 南门洞 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_OPENING | Opening/enclosure scope, not structural timber skeleton. |
| 26 | 南坡筒瓦 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof covering above the wangban STOP boundary. |
| 27 | 内槽斗栱/隔架位置 | TOPOLOGY_OR_ASSEMBLY_CONTAINER | **CONTAINER** | ORGANIZATIONAL_TOPOLOGY_CONTAINER | Organizes relations/instances but is not itself a physical attachment object. |
| 28 | 襻间枋 | PARAMETRIC_SYSTEM_OR_COMPLETION | **IN** | PARAMETRIC_TIMBER_MEMBER | Current Registry records 12 physical positions under upper/lower purlins; it is a real timber framing member in the roof-frame system. |
| 29 | 平梁 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 30 | 铺作方向单元 | TOPOLOGY_OR_ASSEMBLY_CONTAINER | **CONTAINER** | ORGANIZATIONAL_TOPOLOGY_CONTAINER | Organizes relations/instances but is not itself a physical attachment object. |
| 31 | 嵌墙石碑 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_NON_TIMBER | Wall-mounted stone element; not part of structural timber closure. |
| 32 | 戗脊 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof ridge covering system beyond structural timber STOP boundary. |
| 33 | 戗兽 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_ORNAMENT | Roof ornament beyond structural timber scope. |
| 34 | 墙体 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ENCLOSURE_NON_TIMBER | Wall/enclosure system; not part of structural timber closure. |
| 35 | 墙砖族 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ENCLOSURE_NON_TIMBER | Masonry material family; not part of structural timber closure. |
| 36 | 乳栿 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 37 | 散斗族 | REFERENCE_ONLY_UNKNOWN | **IN** | REQUIRED_CONNECTOR_ROLE | Physical timber connector role already required by locked D-277 Upper6→San-Dou→Four-Chuanfu connection; exact family geometry/count may remain bounded. |
| 38 | 上六椽栿 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 39 | 神台 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_INTERIOR_FURNISHING | Interior furnishing/platform, not structural timber skeleton. |
| 40 | 室内地面系统 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_FLOOR_SYSTEM | Interior floor system outside structural timber closure. |
| 41 | 室内方砖族 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_FLOOR_MATERIAL | Interior floor material outside structural timber closure. |
| 42 | 室内条砖族 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_FLOOR_MATERIAL | Interior floor material outside structural timber closure. |
| 43 | 蜀柱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 44 | 四椽栿 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 45 | 台基整体 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_FOUNDATION_SYSTEM | Foundation/platform system is outside Stage2-C; structural timber stops at column lower support handoff. |
| 46 | 替木测量边界 | REFERENCE_ONLY_UNKNOWN | **OUT** | EXCLUDED_REFERENCE_ONLY | Measurement/reference boundary, not a physical production object. |
| 47 | 替木实体族 | REFERENCE_ONLY_UNKNOWN | **CONDITIONAL** | CONDITIONAL_TIMBER_CONNECTOR | Physical timber family is recorded, but current project state has not yet established that it must be an independent Stage2-C production attachment object. Promotion requires explicit same-building connection-role confirmation. |
| 48 | 头昂 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 49 | 透风孔 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_OPENING | Opening/enclosure scope, not structural timber skeleton. |
| 50 | 槫 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 51 | 托脚 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 52 | 望板系统 | PARAMETRIC_SYSTEM_OR_COMPLETION | **IN** | UPPER_BOUNDARY_TIMBER_SYSTEM | Wood roof-substrate system immediately above rafters; included only through rafter→wangban attachment and used as the Stage2-C upper STOP boundary. |
| 53 | 西坡筒瓦 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof covering above the wangban STOP boundary. |
| 54 | 下六椽栿 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 55 | 仙人 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_ORNAMENT | Roof ornament beyond structural timber scope. |
| 56 | 小型瓜子栱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 57 | 小型慢栱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 58 | 隐角梁 | PARAMETRIC_SYSTEM_OR_COMPLETION | **IN** | PARAMETRIC_TIMBER_MEMBER | Current Registry records four corner instances with direct measurement/report evidence; required to close the corner timber system even without a standalone approved Master. |
| 59 | 由额 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 60 | 正脊 | PARAMETRIC_SYSTEM_OR_COMPLETION | **OUT** | EXCLUDED_ROOF_COVERING | Roof ridge covering system beyond structural timber STOP boundary. |
| 61 | 正吻 | SIMPLIFIED_PROXY | **OUT** | EXCLUDED_ORNAMENT | Roof ornament beyond structural timber scope. |
| 62 | 柱 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 63 | 柱头栌斗 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |
| 64 | 柱头铺作 | TOPOLOGY_OR_ASSEMBLY_CONTAINER | **CONTAINER** | ORGANIZATIONAL_TOPOLOGY_CONTAINER | Organizes relations/instances but is not itself a physical attachment object. |
| 65 | 转角铺作 | TOPOLOGY_OR_ASSEMBLY_CONTAINER | **CONTAINER** | ORGANIZATIONAL_TOPOLOGY_CONTAINER | Organizes relations/instances but is not itself a physical attachment object. |
| 66 | 子角梁 | MASTER_BOUND_PRODUCTION | **IN** | APPROVED_MASTER_OBJECT_TYPE | Approved Stage1 Master-bound structural timber/component object type; required for structural timber connection closure. |

## Critical interpretation

- Door/window woodwork is timber, but it is **OUT** because it belongs to enclosure, not the structural timber closure target.
- Wangban is **IN only as the upper timber-system handoff boundary**; Stage2-C stops above it.
- San-Dou is **IN as an indispensable connector role**, even though exact family geometry/count remains bounded.
- Hidden corner beam is **IN** despite lacking a standalone approved Master because the current Registry carries four real corner instances.
- Panjianfang is **IN** because the Registry has 12 located physical records under upper/lower purlins.
- Taimu physical family remains **CONDITIONAL** until its independent connection role is proven and approved.

## What this changes

This register is the proposed scope correction after D-282. It prevents Stage2-C from expanding into all walls, floors, tiles, ridge ornaments and enclosure systems while also preventing a 25-Master-only scope from omitting real structural timber members.

No Connection Coverage Matrix row is changed in this step.
