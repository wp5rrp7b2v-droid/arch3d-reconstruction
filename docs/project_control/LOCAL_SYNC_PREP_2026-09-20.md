# Local Sync Prep｜2026-09-20｜ARCH3D-001

Status：**PREPARED / EXECUTION PENDING LOCAL MAC**

Purpose：safely reconcile the local Mac with current GitHub `main` after the 2026-09-16—20 Cloud Mode window.

## 1. Safety rule

**Do not start with `git pull`, `git reset --hard`, file deletion, branch deletion, or checkout of old T-018 branches.**

First inspect local state.

Expected project directory:

`/Users/caroline/中国古建筑3D复原`

If this path is absent, STOP and locate the actual repository before running Git commands.

## 2. Phase A｜Read-only local preflight

Run:

```bash
cd "/Users/caroline/中国古建筑3D复原"

pwd
git status --short --branch
git branch --show-current
git rev-parse HEAD
git remote -v
git log -1 --oneline --decorate
```

Expected:
- this is a Git repository;
- remote `origin` points to `wp5rrp7b2v-droid/arch3d-reconstruction`;
- preferred current branch is `main`;
- no assumption is made about whether working tree is clean until output is checked.

If any command fails：STOP.

## 3. Phase B｜Fetch only

Run:

```bash
git fetch origin --prune

git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log --oneline --decorate --graph --max-count=20 --all
```

Do **not** merge yet.

## 4. Phase C｜Decision rule

Fast-forward is allowed only if all are true:

- current branch = `main`;
- working tree has no uncommitted changes;
- no local-only commit exists ahead of `origin/main`;
- local HEAD is an ancestor of `origin/main`.

Check:

```bash
git merge-base --is-ancestor HEAD origin/main
echo $?
```

Result `0` means local HEAD is an ancestor of origin/main.

Only then run:

```bash
git pull --ff-only origin main
```

If the result is non-zero, or `git status` is not clean, **do not reset**. Preserve local state and inspect first.

## 5. Phase D｜Post-pull verification

Run:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log -1 --oneline --decorate

test -f docs/project_control/DAILY_CLOSE_2026-09-20.md && echo DAILY_CLOSE_OK
test -f docs/project_control/project_state.json && echo PROJECT_STATE_OK
test -f docs/project_control/dashboard.html && echo DASHBOARD_OK
test -f production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json && echo MASTER_CATALOG_OK
test -f docs/evidence/zhenguo_wanfo/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json && echo REGISTRY_OK
```

Required logical markers after sync:
- Project State revision：R161 or later
- Dashboard：v101 or later
- Registry：V008 / 505
- Stage1 approved Master count：10
- T-024：CLOSED / PR #11 MERGED
- current engineering task：NONE
- T-018：HOLD

## 6. Phase E｜Open PR verification

GitHub open PRs expected at close:

- PR #3｜T-018｜SUPERSEDED / READ-ONLY / DO NOT MERGE
- PR #6｜T-018 replacement｜HOLD / DO NOT MERGE

There should be no open PR #9/#10/#11.

Do not checkout PR #3 or PR #6 during local sync.

## 7. Phase F｜Actions artifact reconciliation

Important：

Git does not contain approved canonical Master `.blend` binaries for T-021—T-024.

Do not substitute final-regression rebuild binaries for Product Owner-approved first-article binaries.

Approved artifact inventory:

| Task | Artifact ID | Approved binary SHA |
|---|---:|---|
| T-021 四椽栿 | 10583607231 | 9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997 |
| T-022 平梁 EW_SEAM | 10597296654 | 5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4 |
| T-022 平梁 GABLE | 10597296654 | f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a |
| T-023 丁栿 | 10599280924 | 81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737 |
| T-024 乳栿 | 10601690312 | 0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208 |

Artifact reconciliation is a separate step from Git pull.

Before putting any downloaded `.blend` into a local canonical/local-only location:
1. verify ZIP/download identity;
2. verify binary SHA-256;
3. preserve existing local-only binary assets;
4. do not commit `.blend` to normal Git;
5. document the final local path.

## 8. Existing local-only assets

Do not overwrite or delete existing local-only Blender assets merely because they are absent from Git.

Previously documented local-only examples include P0.3 baseline/variant `.blend` assets and Blender backup files.

Local binary reconciliation must be additive/verified unless a specific replacement is separately approved.

## 9. Stop conditions

STOP before modifying local data if any of these appears:

- not inside the expected Git repository;
- origin URL unexpected;
- current branch not `main`;
- uncommitted changes;
- untracked project files that might be important;
- local commits ahead of origin/main;
- divergent history;
- merge/rebase in progress;
- detached HEAD;
- existing local-only `.blend` collision;
- SHA mismatch on downloaded approved artifacts.

No `reset --hard`, `clean -fd`, force checkout, or branch deletion is part of the approved sync procedure.

## 10. What to return to ChatGPT

After Phase A + B, paste:

```text
pwd
git status --short --branch
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git remote -v
```

I will then decide whether fast-forward is safe.

After successful Phase D, paste:

```text
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log -1 --oneline --decorate
```

Do not begin the next Stage1 Master until local sync verification is closed.

## 11. V008 Master-progress verification after sync

After Git fast-forward sync, verify the derived V008 Excel:

`docs/evidence/zhenguo_wanfo/derived/P3_WANFO_COMPONENT_INSTANCE_REGISTRY_V008.xlsx`

Expected first sheet:
- `进度总览`

Expected values:
- 登记记录数：505
- 登记对象类型：66
- Stage1 Master范围：28
- 已批准 Master：10
- 待完成 Master：18
- Master完成度：35.7%
- 已绑定Master的登记记录：52
- binding errors：0
- PENDING_SOURCE_BINDING：7

Expected instance-table columns:
- Stage1处置
- Master状态
- Master引用

Generator version：1.0.2  
Current Excel SHA-256：
`dd0364c03f9c44c4d15f3b2aa192a1117af5261aa1705402562570a36019342c`

If these values are missing after local sync, STOP before starting the next Master and reconcile the local derived Excel.


## Completion record

Status：**PASS / COMPLETE**

- Local `main` fast-forwarded successfully.
- Local HEAD matched `origin/main` at synchronization checkpoint: `995a8f42be21e9f1f8c8b013424ea56d5c1b554a`.
- Project State / V008 / derived Excel verification passed.
- V008 Excel SHA-256 matched: `dd0364c03f9c44c4d15f3b2aa192a1117af5261aa1705402562570a36019342c`.
- T-021—T-024 approved Actions artifacts were downloaded and verified.
- Five approved canonical `.blend` binaries were restored into the local Master library with exact SHA matches.
- Final Git safety check: clean; `.blend` files remain ignored.
- Local sync gate：CLOSED.
