# Cloud Mode Sync Ledger｜2026-09-16 → 2026-09-20

**Project:** ARCH3D-001｜中国古建筑3D复原  
**性质:** 临时云端变更登记 / 2026-09-21 本地同步防遗漏清单  
**适用期:** 2026-09-16 ～ 2026-09-20（含）  
**目标同步日:** 2026-09-21  
**状态:** ACTIVE / TEMPORARY / LOCAL_SYNC_VERIFICATION_PENDING  
**关联规则:** RC-014｜CLOUD_MODE_2026-09-16_20  
**事实优先级:** 本登记是操作型补充清单；如与 `project_state.json`、Decision Log、Execution Log、Acceptance Matrix 或 GitHub `main` 冲突，以正式 Project Control + GitHub `main` 为准。

---

## 1. 为什么单独建立本登记

2026-09-16～20 期间 Product Owner 暂无本地 Mac，项目仍通过 ChatGPT App、Codex Cloud、GitHub / GitHub Actions 推进。为了避免 2026-09-21 恢复本地工作时出现以下遗漏，建立本临时登记：

- 云端期间已有 merge，但本地 working copy 尚未 pull；
- 仍 OPEN 的 PR 被误认为已经进入 `main`；
- GitHub Actions artifact 被误认为会随 `git pull` 自动进入本地；
- local-only `.blend` / 二进制资产与 Git 仓库状态混淆；
- Cloud Mode 期间新增的 Task Contract / Decision / Project Control 未在本地核验；
- 9/21 恢复正常模式时忘记关闭 RC-014 临时运行层。

本文件在 9/16～20 每日收尾时更新；9/21 完成本地同步核验后改为 `LOCAL_SYNC_VERIFIED / CLOSED`，保留作审计记录。

---

## 2. Cloud Mode 进入基线

- Pre-Cloud Project State：`R082 / 2026-09-15 FINAL PRE-CLOUD SNAPSHOT`
- P3：`ACTIVE / 3 of 4`
- P3.0～P3.2：PASS / CLOSED
- P3.3：当时为 `ENTERED / DOD REQUIRED / ENGINEERING NOT AUTHORIZED`
- Cloud workflow preflight：`CLOUD-DRILL-002 PASS / VERIFIED`
- RC-014：2026-09-16～20 临时生效，2026-09-21 自动失效
- Local Mac：Cloud Mode 有效期内视为 TEMPORARILY UNAVAILABLE

---

## 3. 2026-09-16｜Day 1 Closing Register

### 3.1 P3.3 Gate / Governance

- `D-047`：P3.3 Definition of Done V001 批准并锁定；9 项 DoD；5 项 P3.3 Hard Fail 固定。
- `D-048 / RC-017`：批准 P3.3 脚本化 Blender 执行链：Codex Cloud 编写 → GitHub Actions headless Blender → GitHub evidence → ChatGPT review → Local Mac 仅保留真正交互式/最终本地检查。
- P3 Gate 总体仍为 `3/4`；P3.3 仍 ACTIVE，未 Gate PASS。

### 3.2 T-017｜整殿输入基线与 Assembly Graph

- `D-049`：授权执行。
- GitHub PR：`#2`
- Reviewed head：`f117cb98da713e5279174248076421caa9d9e6f4`
- `D-050`：Product Owner APPROVED / CLOSED / merge authorized。
- Merge commit：`1095440af761fc95cc18d0ce01523a097fc8ce5f`
- 正式基础：11/11 families、40/40 variants、365/365 instances；P2 numeric world transforms 不得作为生成输入；五类关系保持锁定。
- 后续发现的 PURLIN disposition 冲突已由 T-019 修正，不推翻 T-017 其他基础成果。

### 3.3 T-018｜整殿确定性生成与参数变更验证

- `D-051`：Task Contract LOCKED。
- `D-052`：执行授权；该授权在 T-019 完成后继续有效。
- GitHub PR：`#3`
- 当前 GitHub-visible head（9/16 收尾时）：`ea52590daf5659074fc181aa0288ce223a3d7686`
- PR 状态：`OPEN / NOT MERGED`
- 首轮 Actions Run：`35101537343 / run #1 / FAILURE / DEBUGGING ONLY`
- 首轮 Actions 失败直接原因：Blender 实际输出 `Blender 4.5.13 LTS`，workflow 用 exact-line `Blender 4.5.13` 校验，Run A/B/C/D 尚未执行。
- 正式审核同时发现四项待修正：
  1. Formal component geometry 不得用 generic primitive cube 代替已有 approved formal generation；
  2. Placement 必须机械来源于 authoritative Assembly Graph / parameters / rules，不得使用 synthetic hard-coded family layout；
  3. GitHub Actions formal evidence 必须显式绑定 canonical PR head SHA；
  4. Blender 4.5.13 version check 必须接受合法 `LTS` suffix，同时保持版本锁定。
- 另外曾触发 upstream PURLIN protected-input STOP；该 STOP 已由 T-019/D-055 清除。
- **9/16 收尾状态：`RESUME READY / CORRECTIONS REQUIRED / SAME PR #3 ONLY`。**

### 3.4 T-019｜上游 Disposition 一致性修正

- `D-053`：Task Contract LOCKED。
- `D-054`：执行授权。
- GitHub PR：`#4`
- Reviewed head：`91723a7a2b3c3ca78473bba3cb344450e43fbb3f`
- `D-055`：Product Owner APPROVED / CLOSED / merge authorized。
- Merge commit：`b9803fb416e375fd2f94f5d83df5fab73fe00063`
- 7/7 `CMP-PURLIN-001` building instances：`GENERATE_FROM_FORMAL_COMPONENT → DEFERRED`
- P3.1 qualification 保持 `DEFERRED_INSUFFICIENT_EVIDENCE`；未创建 PURLIN Master；未补造尺寸/截面/端部条件。
- Cross-layer direct-identity conflicts：0；new regression：`MASTER_SCOPE_DISPOSITION_CONFLICT / EXPECTED_REJECTION`。
- canonical `main` 已实际验证 7/7 PURLIN = `DEFERRED`。

### 3.5 9/16 Project Control Closing State

- Project State：`R098`
- Dashboard：`v042`
- Latest material decision：`D-055`
- Current Task：`T-018 / RESUME READY / CORRECTIONS REQUIRED`
- Current blocker：仅 T-018 四项工程修正；**无上游 PURLIN protected-input blocker**
- PR #2：MERGED
- PR #3：OPEN / NOT MERGED
- PR #4：MERGED
- Pre-ledger closing `main` SHA：`5e5996080a0e983373434e36d2ce8425043b01d1`
- Local Mac sync：PENDING until 2026-09-21

---

## 4. 2026-09-17～20｜每日追加模板

后续每一天如有工作，只在对应日期追加“发生变化的事实”，不要重复整个历史。

### 2026-09-17

- Start main SHA：TBD
- End main SHA：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- GitHub Actions run / artifact：TBD
- New files requiring local sync：TBD
- Open PRs not yet in main：TBD
- LOCAL_MAC_REQUIRED / local-only follow-up：TBD
- Daily closing audit：TBD

### 2026-09-18

- Start main SHA：TBD
- End main SHA：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- GitHub Actions run / artifact：TBD
- New files requiring local sync：TBD
- Open PRs not yet in main：TBD
- LOCAL_MAC_REQUIRED / local-only follow-up：TBD
- Daily closing audit：TBD

### 2026-09-19

- Start main SHA：TBD
- End main SHA：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- GitHub Actions run / artifact：TBD
- New files requiring local sync：TBD
- Open PRs not yet in main：TBD
- LOCAL_MAC_REQUIRED / local-only follow-up：TBD
- Daily closing audit：TBD

### 2026-09-20

- Start main SHA：TBD
- End-of-Cloud-Mode main SHA：TBD
- Final State Revision：TBD
- Final Dashboard Version：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- Open PRs carried into 9/21：TBD
- GitHub Actions artifacts requiring separate download：TBD
- LOCAL_MAC_REQUIRED / local-only follow-up：TBD
- RC-014 closure readiness：TBD
- Daily closing audit：TBD

---

## 5. 2026-09-21｜Local Mac Sync Checklist｜必须逐项完成

### A. 同步前保护检查

1. 打开本地项目：`/Users/caroline/中国古建筑3D复原`
2. 先执行 `git status --short`。
3. 若存在不明 tracked changes、未提交 Project Control 修改或与云端同时修改的文件：**STOP，不 pull，不 reset，不 force，不覆盖。**
4. 本地 `.blend` / `.blend1` / 其他 local-only binary 不因 Git pull 自动上传或替换；确认这些资产仍位于预期本地路径。

### B. GitHub canonical main 同步

按 RC-010 使用：

```bash
git-proxy-auto fetch origin
git-proxy-auto pull --ff-only origin main
git rev-parse HEAD
git-proxy-auto ls-remote origin refs/heads/main
```

要求：

- pull 必须为 fast-forward；
- 本地 `HEAD` 必须等于当时 GitHub `origin/main` SHA；
- 若不相等或出现 non-fast-forward：STOP，先诊断，不 force/reset/rebase。

### C. Project Control 核验

同步后逐项确认：

- `docs/project_control/project_state.json` = GitHub 最新 State Revision；
- `docs/project_control/dashboard.html` = GitHub 最新 Dashboard Version；
- `decision_log.md` 至少包含 D-047～D-055，以及 9/17～20 新增的后续决策；
- `execution_log.md` 包含 Cloud Mode 期间所有实际 T-### 结果；
- `acceptance_matrix.md` 与 current P3.3 状态一致；
- `rules_change_log.md` 保留 RC-014 / RC-017；RC-014 在 9/21 不再作为 active execution overlay；
- 本 `CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md` 已同步到本地。

### D. P3.3 / Production 核验

至少检查：

- `docs/production/zhenguo_wanfo/P3_3_DEFINITION_OF_DONE_V001.md`
- `docs/tasks/T-017_P3_3_BUILDING_INPUT_AND_ASSEMBLY_GRAPH_V001.md`
- `docs/tasks/T-018_P3_3_DETERMINISTIC_WHOLE_BUILDING_GENERATION_V001.md`
- `docs/tasks/T-019_P3_3_UPSTREAM_DISPOSITION_CONSISTENCY_CORRECTION_V001.md`
- T-017 五项 canonical foundation outputs；
- `P3_3_BUILDING_SCOPE_ACCOUNTING_V001.json` 中 7/7 `CMP-PURLIN-001` 为 `DEFERRED`；
- T-019 validator / regression 已进入 main；
- 如 T-018 在 9/17～20 已 merge，则核对其正式 outputs / workflow / review evidence 也已进入 main；如仍未 merge，则**不要因为本地 main 没有 PR #3 的工程内容而误判同步失败**。

### E. Open PR / Actions / Artifact 单独核验

`git pull origin main` **不会**自动带回：

- 尚未 merge 的 PR branch 内容；
- GitHub Actions artifact ZIP / `.blend` artifact；
- 未提交到 Git 的 review outputs；
- Codex Cloud 任务内部 commit。

因此 9/21 必须额外检查：

1. 当时所有 OPEN PR（特别是 T-018 PR #3，如届时仍 OPEN）；
2. 最新 GitHub Actions run 状态；
3. 是否存在需要下载到本地的正式 `.blend` / evidence artifact；
4. 是否存在 `LOCAL_MAC_REQUIRED` 的交互式/final inspection；
5. Codex internal SHA 只作辅助，正式以 GitHub-visible PR/head/main 为准。

### F. RC-014 退出核验

- 2026-09-21 起 RC-014 自动失效，不得自动延长；
- 恢复正常运行模式；
- `ONE TASK = ONE BRANCH = ONE PR` 不再因 RC-014 强制，但正式 Task Contract 自身如仍要求则继续遵守；
- Local Mac 可重新作为正式本地 Blender / working-copy 执行环境；
- GitHub Actions / RC-017 作为已批准 P3.3 scripted Blender pipeline 仍继续有效，除非后续正式决策修改。

### G. Local Sync Closure Record｜9/21 填写

- GitHub main SHA at sync：TBD
- Local HEAD after pull：TBD
- `HEAD == origin/main`：TBD
- Project State revision：TBD
- Dashboard version：TBD
- Open PRs carried forward：TBD
- Actions artifacts downloaded separately：TBD
- Local-only binaries present：TBD
- Local Blender executable/version check：TBD
- RC-014 expired：TBD
- Remaining local review / execution items：TBD
- Final result：`LOCAL_SYNC_VERIFIED / CLOSED` or `HOLD + reason`

---

## 6. 强制防遗漏原则

- **GitHub `main` 是云端期间唯一 canonical committed state。**
- **PR OPEN ≠ main 已包含。**
- **Actions artifact ≠ git-tracked file。**
- **Codex internal SHA ≠ GitHub-visible canonical SHA。**
- **Local-only binary ≠ GitHub asset。**
- 9/21 同步必须同时检查：`main + open PR + Actions artifact + local-only assets + Project Control`，不能只执行一次 `git pull` 就认为同步完成。
