# T-016｜P3.2 代表性构件组合工程审核摘要 V001

- 状态：**ENGINEERING COMPLETE / REVIEW REQUIRED**。本文件只记录工程验证结果，不作 T-016 Product Owner 批准或 P3.2 Gate PASS 判定。
- 设计依据：D-043《P3.2 代表性构件组合验证设计 V001》；沿用 T-015 已批准的五类关系与六个正式 Master 身份。
- 起始 `main` / `origin/main`：`e3d5decd90f4ebf12235a099d3c84ce7b3e00bdd`；执行前经 `git-proxy-auto fetch` 与 `pull --ff-only` 核实最新。
- 机器报告：`production/zhenguo_wanfo/validation/P3_2_REPRESENTATIVE_ASSEMBLY_VALIDATION_V001.json`，65/65 PASS；15/15 负向用例按预期拒绝；canonical Hard Fail = 0。

## A｜柱—柱头栌斗

`AU-COLUMN-LUDOU-001` 包含 `CMP-COLUMN-001` 与 `CMP-LUDOU-COLUMN-001`。`A-R01` 以柱上承托工程基准面和栌斗下承托工程基准面表达 SUPPORT；`A-R02` 以两构件主轴表达 LOCATE；另有两条 BELONG。柱局部原点为组合原点，柱头栌斗的位置由 `CMP-COLUMN-001:height_mm` 解析为 Z=3534.3 mm，并匹配两承托基准面。Blender 文件从两个已批准 Master 二进制导入实际网格；独立重开与第二次干净重建的对象签名一致。

该柱高仍是 `Z-006-RC-01 / REASONABLE_COMPLETION / replaceable` 当前生产候选；历史 `Z-006 = UNKNOWN / null / DO_NOT_LOCK`。具体榫卯继续 `UNKNOWN`。工程基准面不声称为已证实的历史加工面。

## B｜上下六椽栿梁架层位

`AU-FRAME-TIER-001` 含上、下六椽栿正式 Master、`CTL-FRAME-001 = CONTROL_ONLY` 与 `PRX-FRAME-CONNECTOR-001 = PROXY_ONLY`。两条 LOCATE 表达工程层位，两条 CONNECT 表达通向未定身份连接代理的关系，四条 BELONG 表达单元从属。未建立上、下六椽栿直接历史连接。真实中间构件身份和榫卯均为 `UNKNOWN`。

Canonical 结果固定为 **`SEMANTIC_ASSEMBLY_VALID / FULL_LENGTH_GEOMETRY_BLOCKED`**。上下六椽栿的历史全长均 `UNKNOWN / null`，本任务没有独立批准的建筑级全长参数，因此未生成 B 的实际全长 `.blend`。1000 mm 仅为非历史 Master reference specimen；负向用例将其注入 actual/building full length 时稳定返回 `REFERENCE_LENGTH_LEAKS_INTO_ASSEMBLY`。

## C｜次间柱重复

`AU-COLUMN-GRID-001` 的 `C-R01` 以 `CTL-GRID-001__SIDEBAY-START`、`CTL-GRID-001__X-AXIS`、`PM-005` 和 count=2 生成两个 runtime instance：`INST-COLUMN-SIDEBAY-001`、`INST-COLUMN-SIDEBAY-002`，均引用 `CMP-COLUMN-001`，没有新 `component_id`。两柱派生中心距为 `PM-005 = 3505.7 mm / CONFIRMED / observed_as_measured / DIRECT_PRIMARY`；重复方法本身是 `PROJECT_RULE`。

执行 `2 → 3 → 2`：三柱测试场景和独立重开均确认恰好三个实例，恢复后两柱结果与 canonical 对象签名一致。PM-005 正式参数文件未修改。

## 审核资产与二进制

四张正式审核图位于 `production/zhenguo_wanfo/review/P3_2/representative_assembly_v001/`：

1. `A_COLUMN_LUDOU_SUPPORT.png`
2. `B_FRAME_TIER_SEMANTIC_BLOCKED.png`
3. `C_COLUMN_GRID_REPEAT.png`
4. `P3_2_REPRESENTATIVE_ASSEMBLY_OVERVIEW_V001.png`

审核图是关系与证据边界示意，非实测比例图；B 图没有实际梁长几何。A/C 的本地 `.blend` 只用于 CLI 工程验证，不进入 Git：

| 单元 | 本地路径 | SHA256 |
|---|---|---|
| A | `production/zhenguo_wanfo/assembly/local/AU-COLUMN-LUDOU-001_V001.blend` | `07c2471b6966e534cd791f86b7ffdf681d8204011d907fab5f5bdfb25482c2d1` |
| C | `production/zhenguo_wanfo/assembly/local/AU-COLUMN-GRID-001_V001.blend` | `7ada16b92c3d09d02620941c56b0aea7b5af2d7b22cdfbe883e7543d76143ce3` |

## 保护与复核

T-015 foundation 31/31 仍 PASS；P2 冻结清单 19/19 SHA256 与 6 个 P3.1 canonical Master 二进制/身份/受保护证据核对通过。既有 unrelated untracked PDF、PoC、output 未处理。未创建 P3.3 文件。三个单元合计覆盖 SUPPORT / CONNECT / LOCATE / REPEAT / BELONG 5/5。

复算命令：

```bash
python3 production/zhenguo_wanfo/scripts/validate_p3_2_relationship_foundation_v001.py
python3 -m unittest production/zhenguo_wanfo/tests/test_p3_2_representative_assembly_v001.py
python3 production/zhenguo_wanfo/scripts/validate_p3_2_representative_assembly_v001.py
```

下一步由 ChatGPT 审核结构与四张图，随后提交 Product Owner 审核。P3.3 继续 LOCKED。
