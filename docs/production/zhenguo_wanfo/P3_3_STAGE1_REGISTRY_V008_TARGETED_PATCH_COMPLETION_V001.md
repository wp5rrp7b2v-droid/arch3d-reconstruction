# P3.3 V002 Stage 1｜Component Registry V008 定点修补完成记录 V001

- Date：2026-09-19
- Authorization：D-068 / Product Owner APPROVED
- Status：**COMPLETE / V008 CURRENT / RC-018 SYNC PASS**
- Base：V007 / 472 records
- Added：33 targeted records
- Current：V008 / 505 records
- T-018：HOLD

## 1. 执行结果

已按批准方案完成：

1. 保留 V007 全部472条记录；
2. 新建版本快照：
   `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.json`
3. CURRENT registry 切换至 V008：
   `docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
4. 追加33条已在V007事实边界内、但此前未序列化的 system / family / entity records；
5. 未加入仍缺正式 source binding 的7项：
   - 板瓦
   - 勾头
   - 滴水
   - 博风板
   - 悬鱼
   - 惹草
   - 生头木
6. RC-018 自动生成 Excel 并通过校验。

## 2. GitHub / RC-018 结果

- V008 snapshot commit：
  `162a6b52706e2c275b41f017137b78a0bc4ca9f7`
- CURRENT → V008 commit：
  `02856c23e5ba34b9cb6bb07bb3e25afd69c87968`
- RC-018 workflow run：
  `35431569023` = **SUCCESS**
- Derived Excel commit：
  `5c9b67217cf9bb2100993ee322419481ca446ede`
- Registry version：V008
- Registry record count：505
- Source JSON SHA-256：
  `e6299d8306fd4f58dac29a43230d387c2f63ca4056d002fd03803df02bb072a7`
- CURRENT.xlsx / V008.xlsx SHA-256：
  `0174049f8b6f2b0cb86f383011a6700401ea1969c47bd132f0c0c1528cfc3adb`
- Sync Manifest：SYNCED

## 3. 重要解释

> 505 是 registry records，不是实体构件总件数。

V008 明确混合记录：

- physical instance
- system
- family unknown-count boundary
- parametric completion
- simplified proxy
- visual-model system
- non-physical topology/counting unit

这些记录不得相加解释为“万佛殿有505件构件”。

## 4. 对史料结论的影响

V008 没有推翻 V007。

它只做：

> **V007 已锁事实 → 更完整的 canonical registry 序列化**

没有新增未经证据支持的历史尺寸或数量。

## 5. 下一步

基于 V008 重新生成 Master Coverage / Disposition Matrix V002。

若 V002 不再发现当前核心 canonical registry 缺口，则进入：

> **四椽栿 Master Spec 设计与锁定**

仍不恢复 T-018。
