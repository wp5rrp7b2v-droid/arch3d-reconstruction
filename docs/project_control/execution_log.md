# Execution Log｜ARCH3D-001

本文件记录实际工程执行结果。只保留足以追溯结论的关键事实、证据、失败原因和最终结果；完整脚本、Workflow、Commit 与 Artifact 由 GitHub 保存。

## T-001｜PROJECT_WORKSPACE_INIT_V001｜PASS

- Think Level: LOW
- 目标：建立本地项目工作区。
- 根目录：`/Users/caroline/中国古建筑3D复原`
- 结果：项目目录结构建立完成，无 blocker。

## T-002｜LOCAL_BLENDER_POC_V002｜PASS

- Think Level: MEDIUM
- Local Blender：3.6.23 macOS x64。
- Blender 4.2.23 macOS x64：Platform Unsupported，不作为本机基线。
- 生成并验证：`P0_1_MINIMAL_GREYBOX_V001.blend` 与 PNG。
- 灰模核心对象：`ARCH3D_BASE`、`ARCH3D_COLUMN_01`–`04`、`ARCH3D_ROOF`。
- 保存、独立重开、Geometry Integrity、PNG 审核：PASS。

## T-003｜LOCAL_CLOUD_ROUNDTRIP_POC｜PASS / CLASS B

### Part A｜Local Handoff｜PASS

- P0.2 Input SHA256：`57d987893ea96e9178908107fb34d21a032cd46c1de0b9a0e1fe05fb7fbae05e`
- Local source 与 Cloud input hash 一致。
- GitHub repo：`wp5rrp7b2v-droid/arch3d-reconstruction`
- 基线提交：`452ca00475ea57a3338005ba65aa70f66feb7bb7`
- 发现：本地 GitHub HTTPS 的 HTTP/2 连接不稳定；repo-local `HTTP/1.1` 后 push 成功。

### Codex Cloud Executor Attempts｜STOP

- 官方 Blender 下载：Cloud proxy 403。
- Ubuntu repository：索引无法取得 / 403。
- NJU Blender mirror：CONNECT 403。
- 结论：**Codex Cloud 不作为当前 Blender Executor**。这不是 Local→GitHub→Cloud 文件交接失败，而是执行环境无法取得 Blender。

### V005｜GitHub Actions Blender Bootstrap｜PASS

- Commit：`06de2095a5556f126eb89e6dfb1e975cd29f94f4`
- GitHub Actions `ubuntu-latest` 成功下载并实际启动 Blender 4.5.13 LTS Linux x64。
- `ARCH3D_BOOTSTRAP_RESULT=PASS`。

### V006｜GitHub Actions Full Roundtrip｜PASS

- Commit：`e26d5d600ed693a8e86a914e24dfbe652d718ed3`
- Input SHA256 验证：PASS。
- Blender 4.5.13 打开 Local 3.6 输入：PASS。
- Cloud Marker：PASS。
- Cycles CPU Render：PASS。
- Cloud Return `.blend`：PASS。
- Blender 4.5.13 独立重开 Cloud Return：PASS。
- Artifact：`P0_2_GHA_ROUNDTRIP_V001`
- Cloud Return SHA256：`2525c8637cfcb002b9ef77115ad984531052fd25ae87967b55497909804c47e8`

### V007｜Local Return Validation｜PASS / CLASS B

- Artifact ZIP SHA256：`959286ac83fa24a07cbb6fe0160ad2f29a3cacb342c1e6c86dfaaa84e8a26edd`｜PASS。
- Local Blender：3.6.23｜PASS。
- Cloud Return 在 3.6 打开：PASS。
- 原始六个对象：PASS。
- `ARCH3D_CLOUD_MARKER`：PASS。
- Metadata：`P0_2_V006 / 4.5.13 LTS`｜PASS。
- Geometry Integrity：PASS。
- 新增 `ARCH3D_LOCAL_RETURN_MARKER`、保存并独立重开：PASS。
- Maintained Blend：`poc/P0_2_cloud_roundtrip/local_return/V001/P0_2_LOCAL_MAINTAINED_V001.blend`
- Compatibility Warning：Blender 3.6 移除了不支持的 View3D / Image region types 14 / 15，并提示文件来自更新的 Blender binary version 405.92。
- 未发现核心几何、Cloud Marker、Local Marker 或所需 Metadata 损失。
- 最终分类：**Class B｜ROUNDTRIP_WITH_LIMITATIONS**。

## Current Execution State

- T-001：PASS
- T-002：PASS
- T-003：PASS / Class B
- T-004｜PARAMETRIC_ARCHITECTURE_POC_V001：NOT_STARTED / NEXT
