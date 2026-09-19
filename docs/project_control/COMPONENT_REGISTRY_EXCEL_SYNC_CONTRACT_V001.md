# Component Registry → Excel Sync Contract V001

**项目：** ARCH3D-001｜中国古建筑3D复原  
**对象：** 平遥镇国寺万佛殿  
**规则编号：** RC-018  
**决策：** D-065  
**状态：** APPROVED / ACTIVE

## 1. 核心原则

本项目的构件数据采用与 Dashboard 相同的“事实源 → 派生视图”原则：

> **构件登记 JSON = 唯一事实源**  
> **Excel = JSON 的派生表格视图**

Excel 不再作为独立维护的数据源，不允许出现“GitHub 改一份、Excel 再人工改一份”的双维护。

## 2. Canonical / Derived 分层

### Canonical

当前正式入口固定为：

`docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`

每个正式版本同时保留不可覆盖的版本快照，例如：

`P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`

正式更新时必须：

1. 形成新的版本化 JSON；
2. 将 `CURRENT.json` 更新为与该版本快照内容一致；
3. 由自动流程生成 Excel；
4. 验证同步清单和哈希；
5. Project Control 再将该版本登记为 CURRENT。

### Derived Excel

固定输出：

- `docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.xlsx`
- `docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_<VERSION>.xlsx`

Excel 必须包含：

- 登记版本；
- 数据源路径；
- 源 GitHub commit；
- JSON SHA-256；
- 生成器版本与 SHA-256；
- “派生视图 / 非独立事实源”声明。

## 3. 自动生成链

正式链路：

`CURRENT JSON → generator → CURRENT.xlsx + Vxxx.xlsx + sync manifest → GitHub commit`

生成器：

`scripts/generate_wanfo_component_registry_excel.py`

GitHub Actions：

`.github/workflows/wanfo-component-registry-excel.yml`

同步清单：

`docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_EXCEL_SYNC_MANIFEST.json`

## 4. 触发与版本规则

当以下任一文件在 `main` 变化时自动运行：

- `P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- Excel generator；
- 本 workflow。

生成器必须验证：

1. CURRENT JSON 有 `schema_version`；
2. 同版本的 `Vxxx.json` 快照存在；
3. CURRENT 与版本快照内容完全一致；
4. Excel 行数与 registry item_count 一致；
5. 生成后可重新打开；
6. manifest 保存 JSON/Excel/生成器哈希。

任一检查失败均 **FAIL CLOSED**，不得提交新 Excel。

## 5. 人工编辑规则

禁止直接修改生成后的 Excel 来改变正式构件事实。

若人工在 Excel 中发现错误：

> 回到 canonical JSON 修正 → 升级/更新正式登记 → 自动重新生成 Excel。

任何只存在于 Excel、尚未进入 JSON 的改动均视为**未正式登记**。

## 6. 失败与过期处理

自动生成失败时：

- 保留 GitHub 上上一份成功 Excel；
- workflow 必须 FAIL；
- 新 JSON 不得被宣称为“Excel 已同步”；
- Project Control 应标记 `EXCEL_SYNC_PENDING/FAILED`；
- 不允许人工覆盖 Excel 来绕过失败。

## 7. 与 Dashboard 的一致原则

Dashboard 与 Excel 均为派生物：

- Dashboard 派生自 Project Control；
- 构件 Excel 派生自 Component Registry JSON。

两者都可以重新生成；事实本体不能依赖派生文件才能恢复。

## 8. 当前V007初始化

当前初始化：

- Registry Version：V007；
- Versioned JSON：`P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V007.json`；
- CURRENT JSON：`P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`；
- Excel首次自动生成：由 RC-018 workflow 执行；
- T-018 执行边界不因本规则改变，继续 HOLD。
