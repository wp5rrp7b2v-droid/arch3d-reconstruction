# 托脚｜A1直接原页证据绑定 V001

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Component：托脚
- Source：SRC-ZG-WF-001《山西平遥镇国寺万佛殿与天王殿精细测绘报告》
- Direct pages：PDF p89–90 / 印刷 p74–75
- Section：2.3.1.8｜托脚与叉手
- Table：表2-45｜万佛殿托脚及叉手实测与分析表
- Cross-check：PDF p102 / 印刷 p87 / 表2-50
- Review date：2026-09-22
- Status：DIRECT SOURCE BINDING LOCKED / SOURCE INTERNAL NUMERIC CONFLICT RECORDED
- Source binary publication：PENDING_GITHUB_LFS_PUBLICATION；原始PDF已由Product Owner在本次审核会话中提供并直接逐页复核

## 1. 直接确认的数量与分布

报告正文直接说明：

- 万佛殿前后上平槫、下平槫共用托脚 **8根**；
- 东西山前后缝下平槫托脚 **4根**；
- 全殿托脚总数 = **12根**。

与 V008 registry 的正身8根 + 山面4根一致。

## 2. 表2-45 托脚实测记录

表2-45共列11组托脚记录，其中1组“广/厚”均为“未及”；可见10组完整数字：

| 组 | 广 mm | 厚 mm |
|---:|---:|---:|
| 1 | 249 | 152 |
| 2 | 未及 | 未及 |
| 3 | 245 | 151 |
| 4 | 245 | 152 |
| 5 | 244 | 149 |
| 6 | 250 | 151 |
| 7 | 250 | 154 |
| 8 | 214 | 151 |
| 9 | 213 | 158 |
| 10 | 212 | 150 |
| 11 | 219 | 173 |

报告正式公布统计：
- 平均广 = **237.1 mm**
- 平均厚 = **153.7 mm**
- 折合分 = **15.50 × 10.05**
- 取整分 = **15 × 10**

## 3. Source-internal numeric conflict

对表2-45中10组可见完整数字做纯算术复核：

- 可见行广均值 = **234.1 mm**
- 可见行厚均值 = **154.1 mm**

与报告正式公布的 **237.1 × 153.7 mm** 不一致。

正式分类：

`SOURCE_INTERNAL_NUMERIC_CONFLICT = TRUE`

处理规则：
- 不静默把报告改成复算值；
- 不把237.1×153.7描述成“项目重新计算均值”；
- Master canonical section 采用报告正式公布值，分类为 `REPORT_PUBLISHED_MEAN_WITH_INTERNAL_ARITHMETIC_CONFLICT`；
- 234.1×154.1仅作为 `VISIBLE_ROWS_RECOMPUTED_MEAN / AUDIT_ONLY` 保留；
- 若未来取得作者底稿、勘误或更高质量原表，可触发局部证据升级。

## 4. 分型证据边界

报告将12根托脚作为同一构件族讨论，并在同一表2-45中统计，没有直接给出：
- 正身托脚独立截面族；
- 山面托脚独立截面族；
- 二者必须采用不同本体形制的直接证据。

因此 Stage1 当前采用：
- 一个 canonical Master body；
- MAIN_FRAME × 8 与 GABLE × 4 作为 assembly/placement role；
- 不提前创建 geometry variant。

## 5. 长度、倾角、端部与榫卯

当前直接原页未锁定：
- 每根托脚历史完整长度；
- 精确安装倾角；
- 12根逐件端点坐标；
- 精确端部加工轮廓；
- 榫卯、槽口、隐藏连接的完整三维几何；
- 11组测量记录与12个具体实例的逐一映射。

以上保持 UNKNOWN / GEOMETRY_DEFERRED。

## 6. 与官方同建筑来源的交叉验证

山西文物数字博物馆·万佛殿专题明确说明“四椽栿两端有托脚作支撑”。

该信息作为 A2 官方同建筑结构语义，与A1数量/实测数据互补，但不自动生成精确接触点坐标或榫卯几何。

## 7. 报告归整值使用边界

表2-50继续将托脚归整为广15分、厚10分。

该分值属于报告分析/归整：
- METADATA_ONLY
- geometry_use_count = 0
- 不作为963年设计尺寸声明；
- 不覆盖现状实测统计。

## 8. 生产资格结论

托脚当前证据状态：

> MASTER SPEC READY / REPORT-PUBLISHED SECTION AVAILABLE / SOURCE INTERNAL NUMERIC CONFLICT RECORDED / HISTORICAL FULL LENGTH UNKNOWN / EXACT ANGLE AND JOINERY DEFERRED

