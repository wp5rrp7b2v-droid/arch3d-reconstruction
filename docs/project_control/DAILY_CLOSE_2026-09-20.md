# Daily Close｜2026-09-20｜ARCH3D-001

## 0. Closing conclusion

**Daily Closing Audit：PASS / COMPLETE / LOCAL SYNC PREP COMPLETE**

Today closes with P3.3 V002 Stage 1 still **ACTIVE / NOT PASSED**.

The stable end-of-day condition is:

- T-022 平梁：APPROVED / PR #9 MERGED / publication CLOSED
- T-023 丁栿：APPROVED / PR #10 MERGED / publication CLOSED
- T-024 乳栿：APPROVED / PR #11 MERGED / publication CLOSED
- Stage1 approved Master count：10
- V008：CURRENT / 505 registry records / JSON canonical truth
- RC-018 derived Excel：V008 / 505 / SYNCED
- D-076 pre-model visual-reference gate：ACTIVE for all later new components
- T-018：HOLD / not current execution route
- only open PRs at close：PR #3 and PR #6, both T-018 historical/HOLD branches and both DO NOT MERGE
- no active T-022 / T-023 / T-024 PR remains
- no active engineering T-task remains
- next Stage1 Master has **not yet been selected**
- no new Blender execution is authorized after close
- local Mac Git/artifact reconciliation is prepared but **not yet performed**

This file is the primary 2026-09-20 handoff record and should be read together with the latest `project_state.json`.

---

## 1. Canonical project snapshot at close

- Project：ARCH3D-001｜中国古建筑3D复原
- Case：平遥镇国寺万佛殿
- Phase：P3｜古建筑构件系统化与组合建模
- Gate：P3.3｜构件驱动整殿重建
- P3.3 route：V002 / real-component-driven
- Stage：Stage 1｜真实构件 Master 库
- Stage status：ACTIVE / 0 of 7 P3.3 stages formally passed
- Registry：V008 / 505 records
- Registry authority：JSON
- Derived Excel role：DERIVED VIEW only
- Stage1 Component Master Catalog：10 approved Masters
- T-018：HOLD
- T-020 / RZ / FV：retain current decisions; re-review deferred to Stage 5
- Current engineering task：NONE
- Next action：local sync verification first; later select next missing Master from Stage1 coverage matrix

---

## 2. Today’s formal decisions

The following Product Owner decisions are confirmed in `decision_log.md`:

### D-073 — T-022 authorization / 平梁 production boundary

Locked:
- one Pingliang Master family;
- EW_SEAM / GABLE variants;
- EW_SEAM = 395.5 × 280.5 mm measured-family mean;
- GABLE = 346 × 245.4 mm;
- 245.4 mm is explicit PARAMETRIC_COMPLETION / replaceable / non-historical;
- historical full length UNKNOWN;
- 1000 mm canonical reference only.

### D-074 — T-022 first article approval

- Run 35483530705 = SUCCESS
- 56/56 PASS
- 10/10 review PNG PASS
- formal delivery authorized

### D-075 — PR #9 merge authorization

- PR #9 MERGED
- merge commit：`9e32324baf8257a2b1ddae0033f4797f9e9d9fd4`
- T-022 CLOSED

### D-076 — Stage1 pre-model visual-reference gate

For every later new Master:
- before creating engineering T-task / Blender execution,
- provide same-building real/site photo and/or measured/form drawing to Product Owner;
- comparative external reference must be labeled comparative;
- self-made schematic cannot substitute direct evidence;
- hard fail：`MODEL_BEFORE_VISUAL_REFERENCE_REVIEW`.

### D-077 — Dingfu-only waiver

- waived D-076 for 丁栿 only;
- did not cancel D-076 globally.

### D-078 / D-079 / D-080 / D-081 — 丁栿

- Spec V001 locked;
- T-023 execution authorized;
- first article approved;
- PR #10 merge authorized and completed.

### D-082 / D-083 / D-084 / D-085 / D-086 — 乳栿

- visual gate PASS using same-building Fig.2-42;
- Spec V001 locked;
- T-024 execution authorized;
- first article approved;
- PR #11 merge authorized and completed.

No new substantive Product Owner decision is created by this Daily Close.

---

## 3. T-022｜平梁 closure

### Approved production facts

EW_SEAM:
- section：395.5 × 280.5 mm
- classification：DIRECT_MEASURED_FAMILY_MEAN

GABLE:
- width：346 mm
- observed thickness：UNKNOWN / null
- production thickness：245.4 mm
- classification：PARAMETRIC_COMPLETION / REPLACEABLE / NON_HISTORICAL

Both:
- historical full length：UNKNOWN / null
- canonical reference length：1000 mm / non-historical Master reference only

### Acceptance / publication

- first article Run：35483530705 = SUCCESS
- validation：56/56 PASS
- review PNG：10/10 PASS
- PR #9：MERGED
- merge commit：`9e32324baf8257a2b1ddae0033f4797f9e9d9fd4`
- publication：CLOSED / MERGED_TO_MAIN
- Catalog：registered Product Owner Approved
- T-021 stale Catalog approval state discovered during T-022 audit：corrected during T-022 formal delivery
- no T-022 `.blend` committed to Git

---

## 4. T-023｜丁栿 closure

### Locked geometry boundary

- physical instances：8
- canonical section：331.6 × 200.9 mm
- classification：DIRECT_MEASURED_FAMILY_MEAN
- sample-to-instance mapping：UNKNOWN
- historical full length：UNKNOWN / null
- canonical reference length：1000 mm / non-historical only
- UPPER / LOWER：assembly roles only / same body geometry
- groove：DIRECT_EXISTENCE / GEOMETRY_DEFERRED
- Stage1 groove cut：NONE

### Acceptance / publication

- first article Run：35490552809 = SUCCESS
- validation：36/36 PASS
- review PNG：6/6 PASS
- approved canonical binary SHA-256：
  `81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737`
- semantic geometry signature：
  `2cb4b6bcae382f9a35dbca3063439aa025e0b6bba18c4175f63c1f13d089f982`
- final regression Run：35494632342 = SUCCESS
- PR #10：MERGED
- merge commit：`d6f85cd2dc9adf8080ef2a0347449b12ef94c646`
- publication：CLOSED / MERGED_TO_MAIN
- no T-023 `.blend` committed to Git

---

## 5. T-024｜乳栿 closure

### Locked evidence / geometry boundary

- physical instances：8
- Table2-40 rows：8
- complete measured samples：6
- unmeasured rows：2
- canonical section：330.5 × 187.2 mm
- sample-to-instance mapping：UNKNOWN
- historical full length：UNKNOWN / null
- exact plan angle：UNKNOWN / null
- **no silent 45-degree assumption**
- canonical reference length：1000 mm / non-historical only
- UPPER / LOWER / NE / SE / SW / NW：assembly/placement roles only
- all role geometry signatures identical
- groove：DIRECT_EXISTENCE / GEOMETRY_DEFERRED
- Stage1 groove cut：NONE

### Acceptance / publication

Approved first article:
- Run：35496581278 = SUCCESS
- validation：43/43 executed checks PASS
- conditional Catalog check #44 did not apply before initial Catalog publication
- review PNG：6/6 PASS
- approved canonical binary SHA-256：
  `0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208`
- semantic geometry signature：
  `8ae9fea45971f10c14573b8329f7ceff45f7d06dd7d6f99b8bac3ee8273d0571`
- approved artifact ID：10601690312
- approved artifact ZIP SHA-256：
  `d686825b86c3e1186682ba7b62861e18cea772242f5069f1ad6f0136f0e6f2a6`

Formal delivery:
- publication Run：35497971045 = SUCCESS
- materialization commit：`fa404ffca1fd3a49cfd70efe0a460048ef6e2f05`
- semantic / validation / engineering review / acceptance / 6 review PNG materialized
- Catalog registered Product Owner Approved
- temporary publication workflow removed

Final pre-merge regression:
- final engineering head：`d857558a1fab765fa269f76ba9217b8456c353aa`
- Run：35498221932 = SUCCESS
- validation：44/44 PASS
- Catalog check #44 executed and PASS
- semantic geometry signature unchanged
- no `.blend` committed
- PR #11：MERGED
- merge commit：`56ea76ed2bfa766991d4e3f19999dc0c704a48ea`
- publication：CLOSED / MERGED_TO_MAIN

The final regression binary byte SHA is a rebuild artifact and does not replace the D-085 approved canonical binary SHA.

---

## 6. Stage1 Master Catalog at close

Approved Master count：**10**

Existing six:
1. 柱
2. 柱头栌斗
3. 单向长开斗
4. 交互斗
5. 下六椽栿
6. 上六椽栿

Newly closed:
7. 四椽栿｜T-021
8. 平梁｜T-022
9. 丁栿｜T-023
10. 乳栿｜T-024

Important:
- Stage1 is still ACTIVE.
- 10 approved Masters does not mean Stage1 is complete.
- do not select the next Master by chat memory alone; use the current coverage matrix and registry on next startup.

---

## 7. Registry / Excel sync cross-check

Canonical registry:
- `P3_WANFO_COMPONENT_INSTANCE_REGISTRY_CURRENT.json`
- schema version：V008
- record count：505

Derived Excel manifest confirms:
- status：SYNCED
- registry version：V008
- record count：505
- source commit：`411778c2f80a0fd506e15381c06aac21433c394d`
- source JSON SHA-256：
  `32ca8de69b9f6b2878f591dccceb9beac76c7e712462f216a69d61949490233a`
- current Excel SHA-256：
  `3c8832b13ba0348a5d561e64e50bc26978c3cfdeb014955322a3066e8222ddd5`
- versioned V008 Excel SHA-256：same
- latest relevant successful RC-018 Run：35495608194

Correction made during close:
- stale Project State subrecord that still described V007 / 472 is superseded;
- V008 / 505 is current.

Canonical truth remains JSON. Manual Excel fact edits remain prohibited.

---

## 8. Open PR / branch audit

At close, only two PRs remain open:

### PR #3

- task：T-018
- branch：`codex/t-018`
- head：`8693c13bf3f04b7e7f7d7d3f24552e1aac8d5750`
- governance：SUPERSEDED / READ-ONLY / DO NOT MERGE

### PR #6

- task：T-018 replacement
- branch：`codex/-t-018`
- head：`65a63b011794dfe2af6a1f0be5ba497a52f23d5f`
- governance：HOLD / DO NOT MERGE

No T-022 / T-023 / T-024 PR remains open.

Do not treat GitHub's volatile mergeable flag as authorization.

---

## 9. Actions audit

Current accepted end states are SUCCESS.

Intermediate failed runs exist for T-022 / T-023 / T-024 and RC-018 during iterative publication or workflow transitions. They are historical engineering evidence and are superseded by the later successful accepted runs.

They must not be carried forward as active blockers.

Accepted/final runs to remember:
- T-022 first article：35483530705
- T-022 final regression：35486533628
- T-023 first article：35490552809
- T-023 final regression：35494632342
- T-024 first article：35496581278
- T-024 final regression：35498221932
- RC-018 latest relevant successful sync：35495608194

---

## 10. PENDING_SOURCE_BINDING / bounded unknowns

Still outside V008 and not silently modeled:

- 板瓦
- 勾头
- 滴水
- 博风板
- 悬鱼
- 惹草
- 生头木

Audit Stop Rule remains active:
- direct fact → lock
- explicit derivation → lock with derivation note
- parametric completion → allowed / replaceable / non-historical
- unknown → remain unknown
- full-table re-audit → STOP unless systemic source error or new evidence appears

---

## 11. T-018 boundary carried forward

T-018 remains:

**HOLD / NOT CURRENT EXECUTION ROUTE / STAGE6 REBASELINE-OR-SUPERSEDE DECISION DEFERRED**

Do not:
- patch PR #3 or #6;
- rerun T-018 Actions;
- resume CP-03;
- publish new RZ/FV implementation;
- run T-018 Blender;
- enter Stage C;
- merge PR #3 or #6.

T-020 / RZ / FV remain bounded upstream history for later Stage5 re-review.

---

## 12. Cloud Mode close

RC-014 cloud operating window 2026-09-16—2026-09-20 has completed its production work.

Day 5 close state:
- GitHub is canonical remote truth;
- all T-022/T-023/T-024 approved delivery records are on main;
- PR #9/#10/#11 are merged;
- open PRs are only T-018 #3/#6;
- local Mac synchronization has **not yet been verified**;
- Product Owner plans to open the Mac later on 2026-09-20;
- local sync target is therefore advanced from the earlier 2026-09-21 plan to **2026-09-20 evening**.

Cloud Mode is closed for production but remains **LOCAL_SYNC_VERIFICATION_PENDING** until local checks are completed.

---

## 13. Local synchronization boundary

Git synchronization will bring:
- source files;
- JSON registries;
- derived Excel;
- scripts/workflows;
- formal delivery JSON/MD;
- review PNGs.

Git synchronization will **not** bring approved canonical `.blend` files stored only as GitHub Actions artifacts.

Approved Action artifact inventory for later local reconciliation:

### T-021 四椽栿
- Artifact ID：10583607231
- ZIP SHA-256：`2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e`
- canonical blend SHA-256：`9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997`

### T-022 平梁
- Artifact ID：10597296654
- ZIP SHA-256：`31670f3654fa2f088900b06c0d7d5d7c1b8a1dbeb221dce692bb85cce4f40839`
- EW_SEAM blend SHA-256：`5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4`
- GABLE blend SHA-256：`f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a`

### T-023 丁栿
- Artifact ID：10599280924
- ZIP SHA-256：`a03ce1e3fdb4510f5cffeeec7b97fdfb215763153fab9c7c2a28690859847fe7`
- canonical blend SHA-256：`81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737`

### T-024 乳栿
- Artifact ID：10601690312
- ZIP SHA-256：`d686825b86c3e1186682ba7b62861e18cea772242f5069f1ad6f0136f0e6f2a6`
- canonical blend SHA-256：`0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208`

Do not replace approved artifact binaries with later regression byte hashes.

---

## 14. Later-today local sync startup order

When the Mac becomes available:

1. Do not immediately pull or reset.
2. Verify expected project directory.
3. Inspect local Git state read-only.
4. Fetch origin.
5. Compare local HEAD / origin/main / working tree.
6. Only if local main is clean and strictly behind origin/main, use fast-forward pull.
7. If local has uncommitted work, local commits, detached HEAD, unexpected branch, or divergent history：STOP and inspect before changing anything.
8. After Git sync, verify Project State / Dashboard / Daily Close markers.
9. Reconcile local-only approved Actions artifacts separately.
10. Only after local reconciliation is PASS should the next Stage1 Master be selected.

Exact commands are prepared in:
`docs/project_control/LOCAL_SYNC_PREP_2026-09-20.md`

---

## 15. Next-session startup rule

After local sync verification:

1. read latest GitHub/local `project_state.json`;
2. read this Daily Close;
3. confirm local HEAD equals current `origin/main`;
4. confirm PR #3/#6 remain HOLD/unmerged;
5. confirm V008 / 505 and Catalog 10 approved;
6. inspect Stage1 coverage matrix;
7. select the next missing Master;
8. apply D-076 visual-reference gate;
9. only after Product Owner visual approval → evidence review → Spec design;
10. no new T-task / Blender until Spec lock + explicit execution authorization.

---

## 16. Final close assessment

**PASS / COMPLETE**

No known unrecorded Product Owner decision, accepted Master, merge, active engineering PR, registry version, or current Stage1 task remains outside the close record.

The only intentionally unresolved items are bounded and explicit:
- Stage1 remaining Masters;
- seven PENDING_SOURCE_BINDING items;
- T-018 HOLD;
- Stage5 re-review of T-020/RZ/FV context;
- later-today local Git + Actions artifact reconciliation.

Final statement:

> **2026-09-20 closes with T-022, T-023 and T-024 fully approved, published and merged; Stage1 remains active with 10 approved Masters. The next engineering step is intentionally not started. Local synchronization is the only immediate operational task before the next modeling session.**

## 17. Post-close visibility patch｜D-087

After the initial Daily Close, Product Owner added one usability requirement:

> Opening V008 should immediately show how many objects/components are registered, how many are within Stage1 Master scope, how many Masters are complete, and how many remain.

This is now implemented without changing V008's evidence facts.

Current visibility snapshot:
- V008 registry records：505
- registered object types：66
- Stage1 Master-scope object types：28
- Product Owner approved Masters：10
- pending Master types：18
- Master completion：35.7%
- registry rows currently bound to approved Masters：52
- PENDING_SOURCE_BINDING：7

Important denominator rule:
- 505 is the **registry-record count**, not a whole-building physical-piece total;
- 66 includes physical components plus systems/topology/family-boundary objects;
- Master completion uses **28 Master-scope object types** as denominator.

V008 / CURRENT row-level additions:
- `stage1_disposition`
- `master_coverage_status`
- `master_reference` when an approved Master exists

Approval/version/SHA/publication truth remains in:
`production/zhenguo_wanfo/registry/P3_3_STAGE1_COMPONENT_MASTER_LIBRARY_V001.json`

Derived Excel:
- generator version：1.0.2
- added first sheet：`进度总览`
- added instance columns：Stage1处置 / Master状态 / Master引用
- RC-018 Run：35508113993 = SUCCESS
- Excel SHA-256：`dd0364c03f9c44c4d15f3b2aa192a1117af5261aa1705402562570a36019342c`

Governance:
Every future approved Master must update V008/CURRENT + derived Excel during formal closure; otherwise the record closure is incomplete.

This patch does not reopen T-022/T-023/T-024 engineering and does not authorize a new Master task.

## 18. Final pre-local-sync recheck

A second full consistency audit was run after D-087.

Result：**PASS**

Cross-check results:
- V008 and CURRENT JSON：equivalent at audit time
- V008 records：505
- registered object types：66
- Stage1 Master scope：28
- approved Masters：10
- pending Masters：18
- completion：35.7%
- approved-Master-bound registry rows：52
- row-level Master binding errors：0
- every V008 record has `stage1_disposition`
- every V008 record has `master_coverage_status`
- approved components have expected `master_reference`
- no unapproved component has a false approved binding
- Stage1 Catalog：10 approved / T-021—T-024 publication CLOSED
- derived Excel：SYNCED / generator 1.0.2 / Run 35508113993 SUCCESS
- open PRs：#3 / #6 only, both T-018 HOLD
- active Actions runs：0
- current engineering T-task：NONE

One stale close-metadata field was found and corrected:
- `daily_closing_audit.latest_formal_decision` was D-086;
- corrected to **D-087**;
- omission-audit range updated from D-073..D-086 to **D-073..D-087**.

Historical failed intermediate Actions runs remain visible in GitHub history. They are superseded by later successful runs and are not current blockers.

Final local-sync baseline:
- Project State：R161
- Dashboard：v101
- immediate operation：local sync verification only
- next Master：not started
- T-018：HOLD

## 19. Local sync + approved artifact reconciliation

Result：**PASS / COMPLETE**

Local Git:
- branch：`main`
- synchronized HEAD：`995a8f42be21e9f1f8c8b013424ea56d5c1b554a`
- local HEAD = origin/main at sync checkpoint
- fast-forward only：PASS
- working tree after sync：clean

Post-sync canonical checks:
- Project State：R161 at verification checkpoint
- latest decision：D-087
- current task：NONE
- V008：505 records / 66 object types
- Stage1 Master scope：28
- approved：10
- pending：18
- completion：35.7%
- Master-bound rows：52
- pending source binding：7
- V008 Excel SHA-256：`dd0364c03f9c44c4d15f3b2aa192a1117af5261aa1705402562570a36019342c`

Approved Actions artifact reconciliation:
- T-021 四椽栿：`9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997` — SHA_MATCH
- T-022 平梁 EW_SEAM：`5c077efe8d39299c8f0a0da39b02b460d3116a204888a17a203dccd189e5d8f4` — SHA_MATCH
- T-022 平梁 GABLE：`f2ecff85c6179481ba156f5f2a249cc7e060be623e3e99a6ee03d8d2ad22f59a` — SHA_MATCH
- T-023 丁栿：`81fa6c593b90c40766c6cc2098b4759c7747cf9bbc77c9c409f5320f88c7c737` — SHA_MATCH
- T-024 乳栿：`0e8095a57741d5fc28854da18670576b160b2516963789fa7d1ce1f686aa8208` — SHA_MATCH

Local Master library:
- approved Master count：10
- local `.blend` count for approved Master library：11
- reason for 11 vs 10：平梁 has two approved canonical variants, EW_SEAM and GABLE
- `.blend` remains ignored by Git
- Git safety check after installation：clean

Cloud Mode local-sync gate is now closed. No new engineering T-task was created. T-018 remains HOLD. Next work returns to Stage1 missing-Master selection under D-076 visual-reference review.
