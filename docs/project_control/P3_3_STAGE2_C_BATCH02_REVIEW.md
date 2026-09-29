# P3.3 Stage2-C｜Batch 02 Review

- Batch: **Primary Frame Attachment Classes**
- Status: **CANDIDATE / PRODUCT OWNER REVIEW REQUIRED**
- Authority: **D-278**
- Stage2-C Batch 01: **LOCKED / D-277**
- Engineering execution: **NOT AUTHORIZED**
- Stage3: **NOT AUTHORIZED**
- T-018: **HOLD**

## Materialized in this candidate

### Attachment interfaces
New interface records: **7**

1. `IF-S2C-B02-PINGLIANG-UPPER-RIDGE-SUPPORT`
2. `IF-S2C-B02-SHUZHU-LOWER`
3. `IF-S2C-B02-CHASHOU-LOWER-END`
4. `IF-S2C-B02-TUOJIAO-FOUR-END`
5. `IF-S2C-B02-FOUR-END-SUPPORT-REGION`
6. `IF-S2C-B02-TUOJIAO-PURLIN-END`
7. `IF-S2C-B02-PURLIN-TUOJIAO-SUPPORT-REGION`

All are MASTER_LOCAL / ASSEMBLY_LOCAL engineering references. None is an exact historical contact-face or joinery claim.

## Materialized Attachment Classes

### 1. Pingliang → Shuzhu
`CONN-S2C-B02-PINGLIANG-SHUZHU-FAMILY-001`

Kind: **CONTACT_INTERFACE**

Locked semantic:
蜀柱属于平梁以上脊部支撑体系，lower endpoint resolves on the Pingliang upper ridge-support region.

Still unresolved:
exact plan anchor / exact contact face / hidden joinery.

### 2. Pingliang → Chashou lower endpoint
`CONN-S2C-B02-PINGLIANG-CHASHOU-FAMILY-001`

Kind: **CONTACT_INTERFACE**

Locked semantic:
叉手下端属于平梁以上脊部支撑体系；实际长度和倾角仍由 endpoint geometry 解析。

Still unresolved:
exact plan anchor / exact contact face / exact historical angle / hidden joinery.

### 3. Tuojiao → Four-Chuanfu end support
`CONN-S2C-B02-TUOJIAO-FOUR-FAMILY-001`

Kind: **CONTACT_INTERFACE**

Locked semantic:
同建筑证据确认四椽栿两端有托脚作支撑。

Still unresolved:
具体哪一端映射到哪一根托脚 / exact contact geometry / exact angle / joinery.

### 4. Tuojiao → source-supported Purlin role
`CONN-S2C-B02-TUOJIAO-PURLIN-FAMILY-001`

Kind: **CONTACT_INTERFACE**

Locked semantic:
报告明确前后上平槫、下平槫及山面部分下平槫使用托脚。

Important boundary:
this record does **not** mean every Purlin uses Tuojiao.

Still unresolved:
exact purlin contact point / exact angle / hidden joinery / instance mapping.

## Explicitly deferred from Batch 02

- 丁栿 ↔ 斗栱槽口/交接；
- 乳栿 ↔ 斗栱槽口/交接；
- 叉手上端 ↔ 脊部支撑 counterpart；
- 蜀柱上端 ↔ 脊部支撑 counterpart；
- exact per-instance endpoint mapping；
- exact historical contact-face geometry；
- exact joinery；
- whole-building topology/world coordinates.

## Candidate machine-consistency check

- New interface records: **7**
- New Connection Layer records: **4**
- Connection kinds: **4 × CONTACT_INTERFACE**
- Required fields: **12 / 12 present on all 4 records**
- Interface references: **8 / 8 resolve**
- Duplicate interface IDs: **0**
- historical_claim: **false on all 4**
- world-coordinate authority: **false on all 4**
- instance-generation authority: **false on all 4**
- fixed historical angle claim: **none**
- exact contact geometry created: **false**
- historical joinery claimed: **false**

## Review decision requested

Approve or reject **Stage2-C Batch 02 Candidate**.

Approval would lock these four family-level attachment classes only.
It would not authorize Batch 03, Blender engineering, Stage3, instance placement or whole-building topology.
