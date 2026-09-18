# Cloud Mode Sync Ledger｜2026-09-16 → 2026-09-20

**Project:** ARCH3D-001｜中国古建筑3D复原  
**性质:** 临时云端变更登记 / 2026-09-21 本地同步防遗漏清单  
**适用期:** 2026-09-16 ～ 2026-09-20（含）  
**目标同步日:** 2026-09-21  
**状态:** ACTIVE / TEMPORARY / LOCAL_SYNC_VERIFICATION_PENDING  
**关联规则:** RC-014｜CLOUD_MODE_2026-09-16_20  
**事实优先级:** 如与 `project_state.json`、Decision Log、Execution Log、Acceptance Matrix 或 GitHub `main` 冲突，以正式 Project Control + GitHub `main` 为准。

---

## 1. Cloud Mode 进入基线

- Pre-Cloud Project State：`R082 / 2026-09-15 FINAL PRE-CLOUD SNAPSHOT`
- P3：ACTIVE / 3 of 4
- P3.0～P3.2：PASS / CLOSED
- P3.3：ENTERED
- Cloud workflow preflight：`CLOUD-DRILL-002 PASS / VERIFIED`
- RC-014：2026-09-16～20 临时生效；2026-09-21 自动失效
- Local Mac：Cloud Mode 有效期内视为 TEMPORARILY UNAVAILABLE

---

## 2. 2026-09-16｜Day 1 Closing Register

- D-047：P3.3 DoD V001 APPROVED / LOCKED。
- D-048 / RC-017：GitHub Actions headless Blender pipeline APPROVED。
- T-017 / PR #2：PASS / D-050 / MERGED；11/11 families、40/40 variants、365/365 instances。
- T-018 / PR #3：OPEN / NOT MERGED；D-051 contract locked；D-052 execution authorized；9/16 close status = RESUME READY / CORRECTIONS REQUIRED。
- T-019 / PR #4：PASS / D-055 / MERGED；7/7 PURLIN corrected to DEFERRED；merge commit `b9803fb416e375fd2f94f5d83df5fab73fe00063`。
- Latest formal decision：D-055。
- Local sync：PENDING until 2026-09-21。

---

## 3. 2026-09-17｜Day 2 Closing Register

- Start canonical main SHA：`574a00831ac827d67dd58667f80fb57d1dd0c77e`
- Project State at close：`R100`
- Dashboard at close：`v044`
- New formal Decision ID：NONE；latest remains `D-055`
- Detailed daily archive：`docs/project_control/DAILY_CLOSE_2026-09-17.md`

### 3.1 T-018 status change

T-018 continued on the **same** branch / PR only:

- branch：`codex/t-018`
- PR：`#3`
- PR status：`OPEN / NOT MERGED`
- GitHub-visible head：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Merge authorization：FALSE

Round 2 result：

- 365/365 `RULE_DERIVED`
- `NOT_REALIZED_NO_APPROVED_PLACEMENT_RULE=0`
- 12 Formal / 178 Proxy / 66 Control / 6 Envelope / 96 UNKNOWN_BLOCKED / 7 DEFERRED
- omission=0；anonymous formal mesh=0；broken identity=0
- PM-005 mutation / restore machine PASS
- visual review FAIL：non-formal representation largely generic point/octahedron markers

Round 3 result：

- differentiated engineering representation geometry by family
- generic octahedron-for-all-nonformal = 0
- view-aware projected-in-frame evidence added
- machine / representation validation PASS

### 3.2 Final Actions evidence

- Workflow：`T-018 P3.3 Deterministic Whole Building`
- Run ID：`35226626839`
- Run number：29
- Head SHA：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- Conclusion：SUCCESS
- Run A / B / Render / C / D：PASS
- Artifact ID：`10499236860`
- Artifact：`P3_3_T018_HEADLESS_EVIDENCE_V001`
- Digest：`sha256:1acb510ed409e490319d62dad2232d082f163413ab81a209484f00b8b67329fa`
- Artifact expiry：2026-10-17

### 3.3 Formal visual review / roof audit

Four review PNGs (PLAN / FRONT / SIDE / AXON) were directly inspected by ChatGPT。

Final status：

`T-018 = HOLD / MACHINE PASS / FORMAL VISUAL REVIEW FAIL / UPSTREAM RULE GAP`

Root cause found by read-only audit：

- canonical PURLIN control identity topology = `N00,N01,N02,N03(shared ridge),S00,S01,S02`; no S03
- FR-007 = `[120,115,210] fen` in eave→ridge order
- MOD-002 = 15.3 mm/fen; half-run = 6808.5 mm
- existing inputs authorize the **relative** two-sided chain to one shared ridge
- existing inputs do **not** authorize the absolute shared-ridge coordinate in the T-018 whole-building coordinate frame
- Round 2/3 mixed observed/as-measured grid coordinates with reconstructed-963 roof-control sequence
- Round 3 `COLUMN_GRID_Y_MIRROR_RULE` is synthetic / unauthorized
- previous Round 2 roof-placement freeze assumption is withdrawn

At minimum, after an approved upstream datum rule exists, rederive 7 PURLIN controls, 36 RAFTER proxies, 6 ROOF_ENVELOPE, 4 GABLE_CONTROL and roof-dependent FRAME endpoints。

Root-cause classification：

`UPSTREAM ENGINEERING RULE MODELING OMISSION + T018 FAILURE TO STOP`

This is not a newly discovered historical-evidence gap。

### 3.4 Proposed T-020

`T-020｜P3.3_ROOF_SHARED_RIDGE_DATUM_RULE_V001｜屋顶共享脊基准与设计坐标层对齐规则`

Status：`PROPOSED / NOT AUTHORIZED / NO BRANCH / NO PR`

Purpose：补齐 project-level engineering datum / LOCATE semantics，不新增历史尺寸；保持 7/7 PURLIN DEFERRED；禁止 observed reference layer 静默成为 reconstructed-design placement source；P2 numeric world transforms 继续禁止。

### 3.5 Files / assets requiring 2026-09-21 awareness

Main-tracked Project Control additions/updates today：

- `docs/project_control/DAILY_CLOSE_2026-09-17.md`
- `docs/project_control/project_state.json` → R100
- `docs/project_control/dashboard.html` → v044
- `docs/project_control/acceptance_matrix.md`
- `docs/project_control/execution_log.md`
- `docs/project_control/CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md`

Open PR not in main：

- PR #3 / `codex/t-018` / head `8693c13...`

Actions artifact not brought by `git pull`：

- Artifact `10499236860` / T-018 headless evidence

LOCAL_MAC_REQUIRED / local-only follow-up：

- 2026-09-21 must verify local-only `.blend` assets separately
- do not mistake absent PR #3 content in local `main` for sync failure

Daily closing audit：`PASS`

---

## 4. 2026-09-18～20｜Daily templates

### 2026-09-18

- Start main SHA：`c1d68627cd8b34be889a3cfc10acd0a1fed6a824`
- Detailed daily archive：`docs/project_control/DAILY_CLOSE_2026-09-18.md`
- Latest formal Product Owner decision：D-064
- New execution/publication authorization at close：NONE
- T-020：PASS / CLOSED / D-058 / PR #5 MERGED
- T-018 V002 Rebaseline：D-059 LOCKED
- Stage A：initial CP-01/02 PASS classifications retained；authority coverage reopened after CP-03
- Stage B：D-061 had authorized CP-03/04/05, but CP-03 STOPPED on `FRAME_TIER_VERTICAL_AUTHORITY_GAP`; CP-04/05 NOT STARTED
- Architecture Closure Review：Outcome B / current working classification only
- Bounded completion design：D-062 / four closure specs complete
- RZ：D-063 design contract LOCKED / not published / not implemented
- FV semantic validity：source-derived claim rejected
- FV：D-064 / A = FV_PROJECT_RULE / non-historical project reconstruction convention / design contract LOCKED / not published / not implemented
- Project State final post-audit revision：R121
- Dashboard final post-audit version：v062
- T-018 final status：HOLD / NOT PASS / production direction not yet proven
- P3.3 final status：ACTIVE / NOT PASS
- CP-03：STOP / not resumed
- CP-04/05：NOT STARTED
- Stage C：LOCKED
- Blender/Actions after V002 architecture review：NONE
- New Actions artifact after V002 review：NONE
- PR #3：OPEN / SUPERSEDED / READ-ONLY / head `8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750` / mergeable=false at close / DO NOT MERGE
- PR #6：OPEN / HOLD / head `65a63b011794dfe2af6a1f0be5ba497a52f23d5f` / mergeable=false at close / DO NOT PATCH / DO NOT MERGE
- Historical PR #6 Actions Run #30：FAIL / `ModuleNotFoundError: p3_3_whole_building_common_v001`
- No new local-only binary produced today
- LOCAL_MAC_REQUIRED follow-up：2026-09-21 still must verify local-only .blend/.blend1 and reconcile main + open PRs + Actions artifacts
- Daily closing audit：**PASS WITH CAUTION**
- Carry-forward rule：**do not interpret RZ/FV locks as proof the correct production direction has been established**
- Next session must first run a bounded **Pre-Publication Readiness Review** before any new publication/execution authorization.

### 2026-09-19

- Start main SHA：TBD
- End main SHA：TBD
- New / changed Decision IDs：TBD
- Task status changes：TBD
- PR opened / updated / merged：TBD
- Actions / artifact：TBD
- Open PRs not in main：TBD
- LOCAL_MAC_REQUIRED follow-up：TBD
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
- Actions artifacts requiring separate download：TBD
- RC-014 closure readiness：TBD
- Daily closing audit：TBD

---

## 5. 2026-09-21｜Local Mac Sync Checklist

### A. Protect local work first

1. `cd "/Users/caroline/中国古建筑3D复原"`
2. `git status --short`
3. Any unexplained tracked changes / local Project Control edits → **STOP**; do not reset / force / overwrite.
4. Confirm local-only `.blend` / `.blend1` / binary assets separately.

### B. Sync canonical main

```bash
git-proxy-auto fetch origin
git-proxy-auto pull --ff-only origin main
git rev-parse HEAD
git-proxy-auto ls-remote origin refs/heads/main
```

Requirements：fast-forward only；local HEAD == origin/main；otherwise STOP and diagnose。

### C. Verify Project Control

- `project_state.json` latest revision
- `dashboard.html` latest visualization version
- `decision_log.md` latest formal decisions
- `execution_log.md` includes Cloud Mode engineering results
- `acceptance_matrix.md` matches P3.3 state
- `CLOUD_MODE_SYNC_LEDGER_2026-09-16_20.md` present
- `DAILY_CLOSE_2026-09-17.md` present
- RC-014 expires on 2026-09-21; RC-017 remains valid unless formally changed

### D. Verify P3.3 separately

`git pull main` does **not** bring back：

- unmerged PR #3 branch content
- Actions artifact ZIP / `.blend`
- Codex internal commits
- local-only binary assets

Therefore separately check：

1. PR #3 current status / head
2. latest T-018 Actions run
3. artifact `10499236860` or any newer replacement
4. any LOCAL_MAC_REQUIRED final inspection
5. proposed/approved T-020 status if work continued after 9/17

### E. Local Sync Closure Record

- GitHub main SHA at sync：TBD
- Local HEAD after pull：TBD
- HEAD == origin/main：TBD
- Project State revision：TBD
- Dashboard version：TBD
- Open PRs carried forward：TBD
- Actions artifacts downloaded separately：TBD
- Local-only binaries present：TBD
- RC-014 expired：TBD
- Remaining work：TBD
- Final result：`LOCAL_SYNC_VERIFIED / CLOSED` or `HOLD + reason`

---

## 6. Mandatory anti-omission rules

- GitHub `main` = Cloud Mode canonical committed state。
- PR OPEN ≠ main contains it。
- Actions artifact ≠ git-tracked file。
- Codex internal SHA ≠ canonical GitHub SHA。
- Local-only binary ≠ GitHub asset。
- 2026-09-21 sync must check `main + open PR + Actions artifacts + local-only assets + Project Control` together。

- 2026-09-18：T-018 V002 Rebaseline contract approved/locked under D-059；execution not authorized；PR #3 superseded/read-only；PR #6 HOLD。
