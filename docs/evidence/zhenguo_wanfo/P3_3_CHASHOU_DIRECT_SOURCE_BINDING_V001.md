# P3.3 V002 Stage 1｜叉手 Direct Source Binding V001

**状态：LOCKED / PRODUCT OWNER APPROVED / D-108**  
**日期：2026-09-23**  
**构件：叉手**  
**Component ID：`CMP-FRAME-CHASHOU-001`**  
**资料主权：D-099 / RC-019**  
**复原方法：RC-020 / Evidence-Constrained Reconstruction**

## 1. A1｜SRC-ZG-WF-001

主定位：

- PDF p89–90
- 印刷 p74–75
- §2.3.1.8｜托脚与叉手
- 表2-45｜万佛殿托脚与叉手实测值及分析表

表中可直接辨识的叉手完整截面样本（mm）：

- 232 × 92
- 234 × 90
- 228 × 91
- 228 × 89

另存在“未及”记录；不得将未测项补造为实测值。

报告正式公布叉手平均截面：

- 广 = **230.5 mm**
- 厚 = **90.5 mm**
- 折合 = **15.07 × 5.92 分**
- 取整 = **15 × 6 分**

独立复算：

- width = (232+234+228+228)/4 = **230.5 mm**
- thickness = (92+90+91+89)/4 = **90.5 mm**

因此：

- `SOURCE_INTERNAL_NUMERIC_CONFLICT = false`
- `CANONICAL_SECTION_BASIS = DIRECT_MEASURED_REPORT_MEAN_WITH_MATCHING_RECOMPUTE`

样本到具体8根实例的逐根对应关系没有直接锁定：

- `sample_to_instance_mapping = UNKNOWN`

该 UNKNOWN 只限制“历史实测逐根对应”的声称，不阻止项目按 Registry 与装配几何完成8根叉手。

## 2. A1 Visual Corroboration

A1 梁架照片/测绘页可见平梁以上的三角斜撑体系，可作为叉手结构形态和层位的视觉交叉验证。

边界：

- 可用于确认斜向长构件、平梁以上脊部体系的总体关系；
- 不因照片目测锁定历史全长、固定角度或隐藏榫卯；
- 不要求这些未知历史量成为 Stage 1 建模前置条件。

## 3. A2｜山西文物数字博物馆·万佛殿专题

官方同建筑说明明确：

- 万佛殿为抬梁式结构；
- 平梁之上设驼峰、蜀柱、叉手。

A2 由 D-099 / RC-019 作为同建筑视觉/结构主权来源使用。

正式锁定：

- `STRUCTURAL_LAYER = ABOVE_PINGLIANG / RIDGE_SUPPORT_SYSTEM`
- `MEMBER_ROLE = DIAGONAL_RIDGE_SUPPORT_MEMBER`

A2 不单独提供精确叉手端点坐标，因此实际长度、实际倾角与端点位置由项目装配几何求解。

## 4. Canonical Registry Cross-check

当前 V008/CURRENT 已锁定 **8根**叉手：

1. 东缝 / 南侧
2. 东缝 / 北侧
3. 西缝 / 南侧
4. 西缝 / 北侧
5. 东山 / 南侧
6. 东山 / 北侧
7. 西山 / 南侧
8. 西山 / 北侧

Registry evidence：`总数8 + 每榀一对构造关系`。

角色汇总：

- `INTERIOR_FRAME = 4`
- `GABLE_FRAME = 4`

南/北、正身/山面首先属于 assembly / placement role；没有稳定本体差异证据时不建立 geometry Variant。

## 5. Evidence / Reconstruction Boundary

本记录区分两层：

### Evidence-locked
- 构件身份：叉手
- physical instance count = 8
- canonical section = 230.5 × 90.5 mm
- 平梁以上脊部支撑体系
- 四榀位置 × 每榀南北一对

### Reconstruction-designed
- 每根实际长度
- 每根安装倾角
- 精确端点坐标
- Stage 1 简化端面
- 装配所需可替换接触几何

上述 reconstruction-designed 项只要：
1. 不与 A1/A2/Registry 直接事实冲突；
2. 与整殿已锁几何关系闭合；
3. 明确标记为 reconstructed design；
4. 可被更高质量资料替换；

即可进入生产，不因缺少历史原值而阻塞。

Decision authority：**D-108 / RC-020**。
