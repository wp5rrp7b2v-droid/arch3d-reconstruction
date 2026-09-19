# T-021｜四椽栿 Master First Article｜STOP 环境复核 V001

- Date：2026-09-19
- Task：T-021｜P3_3_FOUR_CHUANFU_MASTER_FIRST_ARTICLE_V001
- Status：STOP / ENVIRONMENT-INFRASTRUCTURE
- Engineering changes：NONE
- Protected assets：PASS / unchanged
- T-018：HOLD

## 1. Codex 返回

Codex 在正式实现前停止，未创建工程提交。

已确认两类基础设施阻碍：

1. 当前 Codex 执行环境直接访问 Blender 4.5.13 Linux 官方固定下载地址返回 HTTP 403；
2. 当前 checkout 无 Git remote，且 gh 未认证，因此不能 push branch、触发 GitHub Actions、取得 run/artifact ID 或创建 PR。

当前 validation = 0/42；review / binary / artifact / PR 均未产生。

## 2. 复核结论

### Blender 版本本身没有问题

Blender 官方 4.5 LTS 当前正式版本历史中包含 4.5.13；官方 release index 也列出：

`blender-4.5.13-linux-x64.tar.xz`

因此：

> 403 应归类为当前执行环境的下载访问问题，不是“Blender 4.5.13 不存在”，也不是 D-069 / T-021 evidence 或 geometry contract 错误。

### T-021 的执行职责需按 RC-017 解释

T-021 已明确：

> Codex Cloud 写 generator / validator / workflow；GitHub Actions 执行 headless Blender。

因此 **Codex sandbox 本身无法下载 Blender，不应自动等同于 GitHub Actions 无法执行 Blender**。

只有 GitHub Actions 实际尝试 Blender 4.5.13 仍失败，才构成 Blender executor 层面的硬阻碍。

当前更直接的阻碍是：

> Codex checkout 无可推送 GitHub remote / credentials，导致 workflow 根本无法发布并触发 Actions。

## 3. 保持不变

不得因为本次 STOP：

- 改用 Blender 4.5.14；
- 放宽 Blender version pin；
- 修改四椽栿 Master Spec；
- 改 426.5×302mm；
- 改历史长度 UNKNOWN；
- 改 1000mm reference policy；
- 新建 T-022；
- 恢复 T-018。

## 4. Recovery Path

T-021 继续原任务，不新建任务号。

重试前必须先满足：

1. Codex 工作区具有可发布到 `wp5rrp7b2v-droid/arch3d-reconstruction` 的 GitHub repo connection；
2. branch/PR publication capability 可用；
3. Codex 不在本地 sandbox 执行 Blender；
4. Blender 4.5.13 只在 GitHub Actions executor 中实际安装/运行；
5. 若 Actions 对官方 4.5.13 下载也返回阻断，再 STOP 并单独设计 approved binary acquisition path。

下一轮名称：

> T-021｜Retry 01｜Execution Infrastructure Recovery

不改 D-069 Spec，不改 T-021 Task ID。
