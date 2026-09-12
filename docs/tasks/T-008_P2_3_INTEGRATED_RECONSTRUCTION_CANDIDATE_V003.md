# 【中国古建筑3D复原｜T-008｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V003｜GitHub Actions 自认证 Blob 读取与 Roundtrip 阻断清零】

Status: **READY_FOR_LOCAL_EXECUTION / CONTINUATION AFTER V002 HOLD**  
Think Level: **HIGH**  
Phase/Gate: P2 / P2.3  
Date: 2026-09-12

## 1. Objective

继续同一 T-008 目标，不创建新的 T-###。

V001 已完成完整本地整合候选与本地工程 QC；V002 已成功将冻结的正式候选 `.blend` 作为 Git blob 上传至同一 private repository，并通过临时 tag `p2-3-transport-v001` 证明远端已登记 blob SHA，但本机独立 Git fetch 两次因 `Empty reply from server` 失败，因此 V002 按合同 HOLD，Cloud workflow 未启动。

V003 的唯一目标是：

> **停止依赖本机或 runner 对 transport tag 的 Git fetch；改由 GitHub Actions 使用其自身 `github.token` 通过 GitHub REST Git Blobs API 读取已存在的已知 blob SHA，完成 Blender 4.5.13 云端 QC 与返回 artifact，再在 Local Blender 3.6.23 中完成最终返回验证。**

V003 不修改 V001 正式整合候选，不改变历史参数，不扩大模型范围，不重新设计构件库。

## 2. Frozen Baseline

以下全部冻结：

- local canonical candidate：`production/zhenguo_wanfo/output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend`
- expected SHA256：`ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`
- existing Git blob SHA：`23797dbd360ba67b8195d988f2161ff9eaf37d48`
- existing transport tag：`p2-3-transport-v001`
- semantic snapshot：`production/zhenguo_wanfo/validation/P2_3_LOCAL_SEMANTIC_SNAPSHOT_V001.json`
- roundtrip validator：`production/zhenguo_wanfo/scripts/p2_3_roundtrip_semantic_qc_v001.py`
- Component Library：11 families / 40 variants
- stable mesh instances：365
- V001 automated tests：33/33 PASS
- V001 local machine QC：34/34 PASS
- Z-006 / Z-006-RC-01 / DG-114 / HIS-002 / CG-02～CG-06 boundaries unchanged

V003 不允许修改 canonical candidate `.blend`；如本地 SHA256 不等于上述值，立即 HOLD。

## 3. Why V003 Changes the Transport Mechanism

V002 已证明：

- blob 已成功 push 至 private repository；
- remote tag advertisement 返回精确 blob SHA；
- 失败发生在**本机独立 Git HTTP fetch**，错误为 `Empty reply from server`；
- Cloud Blender 尚未运行，因此尚无证据表明 GitHub-hosted runner 无法读取 blob。

因此 V003 不再把“本机独立 fetch transport tag”作为启动 Cloud QC 的必要条件。Transport integrity 由以下三层替代：

1. local canonical `.blend` SHA256 固定；
2. remote advertised blob SHA 已有 V002 证据；
3. GitHub Actions runner 内通过 authenticated GitHub REST API 读取指定 blob，并在运行前重新验证完整 SHA256。

只有第3层在 runner 中 SHA256 通过后，才允许启动 Blender 4.5.13。

## 4. Workflow V003 Architecture

修改：

`.github/workflows/p2_3_integrated_roundtrip.yml`

必须保留 `workflow_dispatch`，并新增一个**无需本机 API credential 的普通 Git trigger**。推荐：

```yaml
on:
  workflow_dispatch:
  push:
    tags:
      - 'p2-3-roundtrip-run-*'
```

注意：用于触发 workflow 的 `p2-3-roundtrip-run-*` tag 必须指向**包含 V003 workflow 的正常 main commit**，不能指向 binary blob。

workflow 必须从 canonical V002 transport evidence 文件读取：

`production/zhenguo_wanfo/validation/P2_3_V002_TRANSPORT_QC_V001.json`

取得：

- `local_canonical_blend.sha256`
- `local_canonical_blend.git_blob_sha`

不要继续执行 `git fetch refs/tags/p2-3-transport-v001` 来取得 binary。

## 5. Authenticated Blob Retrieval in GitHub Actions

GitHub Actions job 使用：

```yaml
permissions:
  contents: read
```

runner 内使用 `${{ github.token }}` 请求：

`GET https://api.github.com/repos/${GITHUB_REPOSITORY}/git/blobs/${BLOB_SHA}`

要求：

- 只使用 runner 自动提供的 `github.token`；
- 不读取、不导出、不打印任何本机 Git credential；
- 不在 repo 中保存 token；
- 不使用用户 PAT；
- API 返回必须确认 `sha == expected blob SHA`；
- base64 decode 后写入 `transport/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend`；
- 对解码文件执行 SHA256 验证，必须等于 `ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`；
- SHA256 不一致立即 FAIL / HOLD，不启动 Blender。

可采用 `curl + python3` 或等价安全实现。日志不得输出 token 或 binary base64 正文。

## 6. Trigger Procedure

完成 workflow V003 修改并 commit / push 到 `main` 后：

1. 确认 local `main` 与 `origin/main` 一致；
2. 创建一个**只用于触发 workflow 的普通 lightweight tag**，例如：

```bash
RUN_TAG="p2-3-roundtrip-run-v003-001"
git tag "$RUN_TAG" HEAD
git push origin "refs/tags/$RUN_TAG:refs/tags/$RUN_TAG"
```

该 tag 指向正常 main commit，不承载 binary。

3. 不要求本机再 fetch binary transport tag；
4. 若 tag push 成功但 workflow 没有产生 run，返回 HOLD，并报告“trigger not created / workflow not started”。

不得使用 credential extraction、custom local API upload、force-push 或把 `.blend` 提交到 main。

## 7. Cloud Blender 4.5.13 QC

Authenticated blob SHA256 验证 PASS 后，继续执行既有 V001/V002 roundtrip 流程：

1. 下载并验证 Blender 4.5.13；
2. Blender 4.5.13 reopen canonical input blend；
3. 用 `p2_3_roundtrip_semantic_qc_v001.py` 对照正式 local semantic snapshot，执行 cloud input QC；
4. cloud-save 为 `P2_3_CLOUD_4_5_RETURN_V001.blend`；
5. Blender 4.5.13 独立 reopen returned file，再次 semantic compare；
6. 记录 return SHA256；
7. 上传 artifact：`P2_3_CLOUD_ROUNDTRIP_V001`，至少包含：
   - returned `.blend`
   - cloud input QC JSON
   - cloud reopen QC JSON
   - return SHA256 TXT/JSON
   - 如有，transport retrieval QC JSON（blob SHA / decoded SHA256 / status；不得含 token）

任何核心 geometry / family / variant / instance / metadata / camera / required review asset 差异 = HOLD。

## 8. Artifact Retrieval and Local Blender 3.6 Return Validation

Cloud workflow PASS 后必须取回 artifact。

首选顺序：

1. 若本机现有工具可安全下载 Actions artifact，则自动下载；
2. 若本机缺少 `gh` 或 API 下载仍受 credential / network 限制，**允许 Product Owner 从 GitHub Actions 页面手工下载 artifact ZIP**，解压到项目指定 return 目录后继续；这不改变工程证据标准；
3. 不得为了“自动化到底”提取本机 credential 或降低安全规则。

Local Blender 3.6.23 必须对返回 `.blend` 独立 reopen + semantic QC，比较：

- stable instance IDs；
- 11 family / 40 variant mapping；
- 365 stable mesh instances；
- core geometry semantic summary；
- key transforms / bounds；
- evidence metadata；
- parameter / override mapping；
- presentation / diagnostic collections；
- cameras / required review assets；
- P2.2 structural regression。

P0.2 已知 UI-region-only 差异可接受；新增核心丢失不可接受。

## 9. Cleanup

只有当以下全部 PASS 后才能清理：

- Cloud workflow PASS；
- artifact 已下载；
- Local 3.6 return QC PASS；
- canonical validation evidence 已更新并 push。

随后删除：

- remote/local `p2-3-transport-v001`
- remote/local `p2-3-roundtrip-run-v003-001`（或实际 run tag）

记录 cleanup result。

Git object database 中历史不可立即物理擦除不作为 FAIL；治理要求是 binary 不进入 `main` tree / canonical model source，临时 refs 最终清除。

## 10. Required V003 Evidence

至少形成或更新：

- `.github/workflows/p2_3_integrated_roundtrip.yml`
- V003 workflow run ID / URL / status
- authenticated blob retrieval QC（expected blob SHA / API-returned SHA / decoded SHA256 / status）
- Cloud Blender 4.5.13 version record
- cloud input QC JSON
- cloud reopen QC JSON
- cloud return SHA256
- artifact name / retrieval result
- Local Blender 3.6 return QC JSON / report
- `P2_3_INTEGRATION_MANIFEST_V001.json` roundtrip section
- `P2_3_VALIDATION_REPORT_V001.md` DoD-07 final result
- `P2_3_KNOWN_LIMITATIONS_V001.md` if new compatibility limitation appears
- V001 regression confirmation 33/33 + 34/34
- final cleanup result
- canonical Git commit containing only text/JSON/workflow/QC evidence, not `.blend`

## 11. PASS / HOLD Logic

T-008 V003 可建议 Engineering PASS 仅当：

- V001 frozen baseline hash unchanged；
- runner authenticated blob retrieval PASS；
- decoded input SHA256 PASS；
- Cloud Blender 4.5.13 workflow 实际执行 PASS；
- cloud input semantic QC PASS；
- cloud independent reopen PASS；
- artifact 成功取得；
- Local Blender 3.6.23 return QC PASS；
- no new core compatibility loss；
- V001 regression 33/33 + 34/34 不退化；
- manifest / validation report / QC evidence canonical archived；
- temporary transport tag 与 workflow trigger tag 均清理。

否则继续 HOLD，并给出唯一/精确 blocker。

Engineering PASS **不等于 P2.3 Gate PASS**。之后仍需 ChatGPT 独立工程复核，以及 Product Owner 六张正式 review / evidence diagnostic 人工审核与明确 Gate 决策。

## 12. Final Report

Codex 完成后返回：

- STATUS: PASS / HOLD
- V001 frozen baseline regression
- local `.blend` SHA256
- existing transport blob SHA / transport tag status
- workflow V003 commit SHA
- run-trigger tag / push result
- workflow run ID / URL / status
- authenticated blob retrieval result
- decoded input SHA256 result
- Cloud Blender version
- cloud input semantic QC
- cloud reopen semantic QC
- artifact name / retrieval result
- cloud-return `.blend` SHA256
- Local Blender 3.6 return QC
- core semantic diff summary
- V001 tests 33/33 / machine QC 34/34 regression
- manifest / validation updated paths
- transport tag cleanup result
- run-trigger tag cleanup result
- canonical Git commit SHA / push result
- `git status --short`
- exact blocker if HOLD
- engineering recommendation

不得自行宣布 P2.3 Gate PASS 或 P2 Phase CLOSED。
