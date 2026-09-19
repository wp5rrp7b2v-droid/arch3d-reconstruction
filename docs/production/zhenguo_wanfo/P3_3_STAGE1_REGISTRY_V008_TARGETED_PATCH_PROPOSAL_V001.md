# P3.3 V002 Stage 1｜Component Registry V008 定点修补方案 V001

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Date：2026-09-19
- Gate：P3.3 V002
- Stage：Stage 1｜真实构件 Master 库
- Trigger：V007 Master Coverage / Disposition Matrix 一致性检查
- Status：DESIGN COMPLETE / PRODUCT OWNER APPROVAL REQUIRED
- Engineering execution：NONE
- T-018：HOLD

## 1. 为什么需要 V008

V007 的史料结论本身不需要重审。

问题发生在“序列化登记层”：

> V007 证据文档中已经明确存在、并且后续模型需要处理的若干系统/构件，没有被写进 CURRENT component registry。

如果不补，会出现：

- Master Coverage 看起来已经覆盖全部49类；
- 实际却漏掉墙体、室内地面、神台、门窗木作、屋面基层/装饰等对象；
- 后续建模又会在中途“突然发现缺件”。

因此 V008 的性质是：

> **V007 事实不变；只修正 canonical registry 的表达完整性。**

## 2. V008 不做什么

V008 不做以下事情：

- 不重新审整份测绘报告；
- 不改 V007 已锁数量；
- 不改现有472条 V007 记录；
- 不把 UNKNOWN 自动补成已知；
- 不把系统/阵列记录伪造成逐件实测构件；
- 不恢复 T-018；
- 不创建 Codex 建模任务；
- 不修改现有6个 Master 几何。

## 3. 第一组｜可直接由当前 V007 正式证据补入

### A. 围护与砌体系统

新增 registry system/family records：

1. 南墙体
2. 北墙体
3. 东墙体
4. 西墙体
5. 墙砖族 / 数量 UNKNOWN
6. 室内地面系统
7. 室内条砖族 / 数量 UNKNOWN
8. 室内方砖-约265mm型 / 数量 UNKNOWN
9. 室内方砖-约315×305mm型 / 数量 UNKNOWN
10. 神台系统

证据边界：

- 墙砖均值 277.4 × 134 × 63.1mm；
- 南墙局部厚约820–880mm，禁止推广成四面统一墙厚；
- 室内条砖均值约277.9 ×133.3mm，厚度未测；
- 方砖两类约265mm见方、约315×305mm；
- 神台四周条砖立砌压脚、表面方砖铺墁；
- 神台整体长宽高仍 UNKNOWN。

### B. 屋面基层

新增：

11. 望板系统

状态：

- 存在与层位关系可确认；
- 单板总数、标准板宽/厚、逐块位置未闭合；
- 进入模型只能是 PARAMETRIC_COMPLETION。

### C. 屋脊装饰物

新增实体记录：

12–13. 正吻 ×2  
14–17. 垂兽 ×4  
18–21. 戗兽 ×4  
22–25. 仙人 ×4

证据边界：

- 数量可以锁；
- 当前不主张精确雕塑/陶塑几何；
- Stage 1 disposition 先为 SIMPLIFIED_PROXY / replaceable ornament asset。

### D. 门窗木作视觉系统

新增：

26. 南门木作系统
27. 北门木作系统
28. 南东窗木作系统
29. 南西窗木作系统

状态统一为：

> VISUAL_MODEL + PARAMETRIC_SECTION

可用测绘立面恢复现状分格视觉关系，但：

- 木料断面 UNKNOWN；
- 榫卯 UNKNOWN；
- 门扇/窗扇完整单件尺寸 UNKNOWN。

### E. 真实存在但数量未闭合的构件族边界

新增 UNKNOWN-family records：

30. 单向长开斗族 / whole-building count UNKNOWN
31. 交互斗族 / whole-building count UNKNOWN
32. 散斗族 / whole-building count UNKNOWN
33. 替木实体族 / whole-building count UNKNOWN

这些不是“新增4件实体”，而是补登记：

> **构件族存在，但全殿真实总量/逐件位置尚未闭合。**

其中单向长开斗、交互斗已有 approved Master；V008 只补“实例数量边界”，不生成实体实例。

## 4. 第二组｜暂不进入 V008 的对象

Coverage review 还指出：

- 板瓦；
- 勾头；
- 滴水；
- 博风板；
- 悬鱼；
- 惹草；
- 生头木。

这些对象在前序审计工作中出现过，但当前 GitHub 已归档的 V007 canonical evidence 文档没有为它们保存足够完整的逐项 source binding。

因此 V008 V001 **不静默补入**。

它们转为：

> PENDING_SOURCE_BINDING

等后续需要建模这些对象时，只做局部 source-binding 补丁；不重新审整张表。

这是为了遵守：

- V007 STOP AUDIT RULE；
- MASTER_WITHOUT_EVIDENCE_BINDING Hard Fail；
- 不用聊天记忆替代 GitHub canonical evidence。

## 5. V008 预计结果

如果方案批准：

- V007 snapshot 永久保留；
- 创建 `P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json`；
- CURRENT.json 切换到 V008；
- 原472条记录保持不变；
- 追加33条 system/family/entity records；
- 预计 V008 record count = **505**；
- RC-018 自动生成：
  - CURRENT.xlsx
  - V008.xlsx
  - Sync Manifest；
- 自动验证 CURRENT=V008 snapshot、记录数、Excel行数和 SHA。

注意：

> 505 是 registry record count，不是“万佛殿共有505件构件”。

## 6. V008 record-type 规则

新增记录必须明确区分：

- PHYSICAL_INSTANCE
- SYSTEM
- FAMILY_UNKNOWN_COUNT
- PARAMETRIC_COMPLETION
- SIMPLIFIED_PROXY
- VISUAL_MODEL

禁止这些不同层级相加得出“构件总件数”。

## 7. 对 Stage 1 的影响

V008 完成后：

1. 重新生成 Master Coverage / Disposition Matrix V002；
2. 确认没有“已知但未登记”的当前核心系统；
3. 再锁首个缺失 Master：
   **四椽栿**；
4. 四椽栿 Spec 锁定后才创建实际 Codex 建模 T-###。

## 8. 当前请求

需要 Product Owner 批准：

> **按本方案建立 V008 targeted registry patch。**

批准后直接执行 canonical registry 升级 + RC-018 Excel 自动同步。
