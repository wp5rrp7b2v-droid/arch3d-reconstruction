# P2.0｜平遥镇国寺万佛殿｜Evidence-aware Parameter Schema V001

Status: WORKING BASELINE / P2.0 STEP 1  
Date: 2026-09-12  
Gate: `P2.0｜Evidence-aware Parameter Schema`

## 0. 目的

P2.0 将 P1 已完成的证据分级转化为机器可读、可验证、可替换、可追踪的正式生产参数结构。

本 Schema 的核心目标不是“存数字”，而是确保任何进入后续 Blender / Python 的参数都不会丢失：

- 数值本身；
- 证据等级；
- 时间/语义层；
- 来源层；
- 生产用途；
- 阻断等级；
- 来源引用；
- 是否可替换；
- 说明与边界。

P0.3 的裸数字 JSON 只保留为技术 POC，不迁移、不覆盖、不升级为正式生产参数。

---

## 1. 正式参数对象｜Required Fields

每个正式关键参数至少包含：

```json
{
  "parameter_key": "corner_column_rise_design_mm",
  "label_zh": "角柱生起设计候选",
  "value": 61.2,
  "unit": "mm",
  "classification": "REASONABLE_COMPLETION",
  "time_layer": "reconstructed_963_candidate",
  "source_layer": "REPORT_INFERRED_GUESS",
  "production_use": "DEFAULT_REPLACEABLE_CANDIDATE",
  "blocking_level": "MEDIUM",
  "source_ids": ["SRC-ZG-WF-001"],
  "is_replaceable": true,
  "notes": "主报告仅称猜测；不得表述为963年已证实事实。"
}
```

### 必填字段

| Field | Type | Rule |
|---|---|---|
| `parameter_key` | string | 稳定机器键，不随展示文案变化 |
| `label_zh` | string | 中文可读名称 |
| `value` | number/string/array/object/null | UNKNOWN + DO_NOT_LOCK 时必须为 null |
| `unit` | string/null | 无物理单位时允许 null |
| `classification` | enum | 四级证据分类 |
| `time_layer` | enum | 参数所属历史/语义层 |
| `source_layer` | enum | 证据来源性质 |
| `production_use` | enum | 允许的生产用途 |
| `blocking_level` | enum | NONE / LOW / MEDIUM / HIGH |
| `source_ids` | string[] | 至少1项；UNKNOWN 也应引用“缺口/冲突”的来源或Gate文件 |
| `is_replaceable` | boolean | REASONABLE_COMPLETION 必须为 true |
| `notes` | string | 证据边界、禁用语义、补充说明 |

---

## 2. Classification Enum

仅允许：

- `CONFIRMED`
- `HIGH_CONFIDENCE_INFERENCE`
- `REASONABLE_COMPLETION`
- `UNKNOWN`

禁止使用 `DIRECT_VERIFIED` 直接替代本字段；`DIRECT_VERIFIED` 属于来源核读状态，不等于历史事实等级。

---

## 3. Canonical time_layer

P2 起统一使用以下机器值，避免 P1 文档中的自然语言变体继续扩散：

- `observed_as_measured`
- `observed_as_measured_filtered`
- `observed_deformation`
- `observed_current_topology`
- `report_ideal_model`
- `reconstructed_design_candidate`
- `reconstructed_963_candidate`
- `project_model_datum`
- `historical_events`
- `component_history`
- `evidence_rule`
- `topology_or_rule`

### P1 → P2 规范化示例

- `observed/current topology` → `observed_current_topology`
- `observed_as_measured` → 保持不变
- `reconstructed_963_candidate` → 保持不变
- `project_model_datum` → 保持不变

任何 `report_ideal_model` 数据不得静默改写成 `reconstructed_963_candidate`。

---

## 4. source_layer Enum

正式生产最小集合：

- `DIRECT_PRIMARY`
- `DIRECT_PRIMARY_DERIVED`
- `DIRECT_PLUS_SUPPORT`
- `REPORT_INFERRED`
- `REPORT_INFERRED_GUESS`
- `REPORT_INFERRED_HIGH_CAUTION`
- `A_BRIDGE_VERIFIED`
- `A_BRIDGE_UNRESOLVED`
- `DIRECT_GAP`
- `PROJECT_RULE`
- `UNKNOWN`

原则：来源层描述“证据来自哪里/以何种方式获得”，classification 描述“我们对该命题能相信到什么程度”，二者不得混用。

---

## 5. production_use Enum

- `OBSERVED_REFERENCE`
- `OBSERVED_DEFORMATION_REFERENCE`
- `BASE_TOPOLOGY`
- `DEFAULT_963_CANDIDATE`
- `DEFAULT_DESIGN_SYSTEM`
- `DEFAULT_DESIGN_LOGIC`
- `DEFAULT_REPLACEABLE_CANDIDATE`
- `PROVISIONAL_REFERENCE`
- `DO_NOT_LOCK`
- `PROJECT_COORDINATE_RULE`
- `PER_COMPONENT_METADATA_REQUIRED`
- `HISTORICAL_TIMELINE`

---

## 6. blocking_level Enum

- `NONE`
- `LOW`
- `MEDIUM`
- `HIGH`

`HIGH` 表示阻断该参数/子问题的最终历史锁定，不自动等于整个项目 NO-GO。

---

## 7. 强制机器规则

### R-01｜UNKNOWN / DO_NOT_LOCK

若：

```text
classification = UNKNOWN
AND production_use = DO_NOT_LOCK
```

则：

```text
value = null
```

不得用 0、经验值、默认 Blender 数值或“临时看起来合理”的数字代替 null。

### R-02｜REASONABLE_COMPLETION 可替换

若：

```text
classification = REASONABLE_COMPLETION
```

则：

```text
is_replaceable = true
```

后续几何生成必须从参数读取，禁止烘焙为不可追踪固定值。

### R-03｜三层语义隔离

`observed_as_measured`、`report_ideal_model`、`reconstructed_963_candidate` 为独立语义层。

禁止：

- 从 observed 数值直接覆盖 963 candidate 而无显式判断；
- 将 report ideal 直接重命名为 963；
- 在同一字段中混存“现状值 / 963候选值”。

### R-04｜source_ids 不得为空

正式参数必须至少能追溯到：

- 主来源；或
- 支撑论文；或
- Gate / decision / gap 文件。

即使 UNKNOWN，也要能解释“为什么未知”。

### R-05｜P0 参数格式禁止进入正式生产

以下形式只能继续存在于 P0 POC：

```json
{"column_height": 3.2}
```

P2 正式参数不得只保存裸数字。

---

## 8. Root Parameter Set 结构

建议正式参数集采用：

```json
{
  "schema_version": "1.0",
  "project_id": "ARCH3D-001",
  "case_id": "ZG-WF-963-CANDIDATE",
  "case_name": "平遥镇国寺万佛殿",
  "parameter_set_version": "V001",
  "status": "P2_0_VALIDATION",
  "parameters": {
    "Z-005": { "...": "..." },
    "Z-006": { "...": "..." }
  }
}
```

参数 ID 使用 P1 已建立的 `PM / MOD / Z / DG / RF / FR / OUT / ROOF / DEF / HIS` ID，保持证据矩阵与生产参数一一映射。

---

## 9. P2.0 最小验证样例

必须至少覆盖四类：

### A｜CONFIRMED

`PM-003｜front_center_bay_observed_mm = 4481.3`

用途：现状实测参考，不得直接改称963设计值。

### B｜HIGH_CONFIDENCE_INFERENCE

`PM-008｜front_center_bay_design_chi = 14.5`

用途：963候选默认值，保留 REPORT_INFERRED 与 LOW blocking。

### C｜REASONABLE_COMPLETION

`Z-005｜corner_column_rise_design_mm = 61.2`

用途：可替换候选；`is_replaceable=true`。

### D｜UNKNOWN

`Z-006｜column_height_963_design_mm = null`

用途：`DO_NOT_LOCK`；必须保持 null，不允许默认值。

---

## 10. P2.0 Gate Acceptance Criteria

P2.0 PASS 前必须满足：

1. 正式 JSON Schema 文件存在且可被标准 JSON Schema validator 读取；
2. 四类最小样例全部通过 schema validation；
3. `UNKNOWN + DO_NOT_LOCK + non-null value` 必须验证失败；
4. `REASONABLE_COMPLETION + is_replaceable=false` 必须验证失败；
5. 至少一个未来 Blender/Python reader 能读取正式参数集而不生成正式几何；
6. P0 裸数字 JSON 与 P2 正式参数文件物理路径分离；
7. P1 参数 ID 与 P2 参数 ID 可追溯一一映射；
8. P2.0 PASS 前不得启动正式 Blender 几何生产。

---

## 11. 当前边界

本文件完成的是 P2.0 的 Schema 规则基线，不等于 P2.0 Gate PASS。

下一步：

1. 建立机器可验证的 JSON Schema；
2. 建立最小正式样例参数集；
3. 建立 validator / reader；
4. 执行正向与反向测试；
5. Gate Review。
