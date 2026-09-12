# 【中国古建筑3D复原｜T-008｜P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V002｜Cloud Roundtrip 阻断清零与最终工程验收闭环】

Status: **READY_FOR_LOCAL_EXECUTION / CONTINUATION AFTER V001 HOLD**  
Think Level: **HIGH**  
Phase/Gate: P2 / P2.3  
Date: 2026-09-12

## 1. Objective

继续 T-008 原任务目标，不新增新的 T-###。

V001 已完成本地整合候选、Component Library / Variant / Instance 架构、machine QC、replacement / mutation、deterministic rebuild、independent reopen、六类 review outputs 与 canonical GitHub archive，但因 **DoD-07 所要求的 Local Blender 3.6 → Cloud Blender 4.5 → Local Blender 3.6 roundtrip 尚未实际执行**，工程结论为 HOLD。

V002 的唯一核心目标是：

> 在不改变已通过的 P2.3 本地整合候选与历史证据边界的前提下，完成安全、可追溯的临时 `.blend` 传输，执行真实 Blender 4.5.13 云端 reopen / semantic QC / save，取回 artifact，并在 Local Blender 3.6.23 中完成返回验证，从而关闭 DoD-07 blocker。

除非 roundtrip 暴露真实兼容性问题，否则不得借 V002 重新设计整合几何、扩展 LOD、增加无关构件或修改历史参数。

## 2. Authoritative Baseline

V002 必须继承并冻结以下 V001 已通过工程基线：

- `production/zhenguo_wanfo/output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend`
  - expected local SHA256: `ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512`
- `production/zhenguo_wanfo/components/P2_3_COMPONENT_LIBRARY_V001.json`
- `production/zhenguo_wanfo/build/P2_3_INTEGRATION_MANIFEST_V001.json`
- `production/zhenguo_wanfo/validation/P2_3_LOCAL_SEMANTIC_SNAPSHOT_V001.json`
- `production/zhenguo_wanfo/scripts/p2_3_roundtrip_semantic_qc_v001.py`
- `production/zhenguo_wanfo/validation/P2_3_VALIDATION_REPORT_V001.md`
- `production/zhenguo_wanfo/validation/P2_3_KNOWN_LIMITATIONS_V001.md`
- V001 canonical engineering commit: `5bd6ca1f8300a170b74c3a9058352768800b56a6`
- locked DoD: `docs/production/zhenguo_wanfo/P2_3_DEFINITION_OF_DONE_V001.md`

V001 已通过的本地工程事实不得因 V002 被重置或重新解释。

## 3. Transport Decision｜Temporary Git Tag → Blob

采用**普通 Git 协议的临时 transport tag 指向 `.blend` blob**，替代 draft-release / `gh` / browser / custom API credential extraction 路线。

原因：

- 本机普通 `git push` 已恢复可用；
- 不需要读取、导出或手工处理 Git 凭据；
- `.blend` 不进入 `main` tree，不创建普通历史 commit；
- tag 仅用于把单个 blob 临时传输至同一 private repository；
- workflow 完成并取回 artifact 后必须删除远端与本地 transport tag；
- 不得 fallback 到把 `.blend` 提交至 main、force-push 或提取 credential 调 GitHub API。

该传输是**临时 QC transport**，不改变项目 `.blend / .blend1 = local-only canonical asset` 规则。GitHub 上的 transport blob 不是 canonical model source。

## 4. Local Transport Procedure

开始前：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git pull --ff-only origin main
```

设定：

```bash
BLEND="production/zhenguo_wanfo/output/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend"
EXPECTED_SHA256="ee91e5eb2b5737174ffd0f93626ebf4f6ddaf3ae8fb427f9bfd2f66568e2f512"
TRANSPORT_TAG="p2-3-transport-v001"
```

必须先核对本地文件 hash；不一致即 HOLD，不上传。

随后使用 Git object database 写入 blob，并创建**指向该 blob 的临时 lightweight tag**：

```bash
BLOB_SHA="$(git hash-object -w "$BLEND")"
git cat-file -e "${BLOB_SHA}^{blob}"
git tag -f "$TRANSPORT_TAG" "$BLOB_SHA"
git push origin "refs/tags/$TRANSPORT_TAG:refs/tags/$TRANSPORT_TAG"
```

要求记录：

- local `.blend` SHA256；
- Git blob SHA；
- transport tag 名称；
- push 结果。

若 GitHub / Git 拒绝 blob tag、对象无法传输或 tag 无法拉取：**立即 HOLD**。不得改为 commit `.blend` 到普通分支，不得提取 token 绕过。

## 5. Workflow V002 Requirement

修改 `.github/workflows/p2_3_integrated_roundtrip.yml`，使其从临时 transport tag 读取 blob，而不是依赖 draft release。

workflow_dispatch 至少输入：

- `transport_tag`
- `expected_sha256`

Actions checkout 后显式 fetch 指定 tag，并验证它最终指向 `blob`；将 blob 导出为：

`transport/P2_3_INTEGRATED_RECONSTRUCTION_CANDIDATE_V001.blend`

推荐逻辑等价于：

```bash
git fetch --force --no-tags origin "refs/tags/${TRANSPORT_TAG}:refs/tags/${TRANSPORT_TAG}"
BLOB_SHA="$(git rev-parse "refs/tags/${TRANSPORT_TAG}")"
test "$(git cat-file -t "$BLOB_SHA")" = "blob"
git cat-file blob "$BLOB_SHA" > "$INPUT_BLEND"
echo "${EXPECTED_SHA256}  ${INPUT_BLEND}" | sha256sum --check --status
```

之后继续执行既有流程：

1. 下载并验证 Blender **4.5.13**；
2. 在 Cloud Blender 4.5.13 中 reopen V001 candidate；
3. 用 `p2_3_roundtrip_semantic_qc_v001.py` 对照正式 local semantic snapshot；
4. cloud-save 为 `P2_3_CLOUD_4_5_RETURN_V001.blend`；
5. 在 Cloud 4.5 中独立 reopen returned file 再次 compare；
6. 上传 GitHub Actions artifact，至少包含 returned `.blend`、cloud input QC、cloud reopen QC、return SHA256。

## 6. Local Return Validation

下载 workflow artifact 后，在 Local Blender **3.6.23** 对返回 `.blend` 做独立 reopen 和 semantic QC。

必须比较并记录：

- family / variant / instance stable ID set；
- instance count / family count / variant mapping；
- core geometry semantic summary；
- key transforms / bounds；
- evidence metadata；
- parameter / override mapping；
- presentation / diagnostic collection mapping；
- 正式 camera / review asset 是否仍存在；
- P2.2 key structural regression；
- known P0.2 UI-region-only difference 是否仍为唯一或等价非核心差异。

任何新的核心 geometry、metadata、instance mapping、camera / required review asset 损失 = **HOLD**。

## 7. Cleanup

只有在以下条件全部满足后才能删除 transport tag：

- workflow 已成功完成；
- artifact 已下载；
- return `.blend` 已本地保存并完成 Blender 3.6 验证；
- cloud / local QC evidence 已写入正式 validation 路径。

之后：

```bash
git push origin ":refs/tags/$TRANSPORT_TAG"
git tag -d "$TRANSPORT_TAG"
```

必须记录 remote tag cleanup result。

不得删除本地 canonical V001 candidate。

## 8. Required V002 Evidence

至少形成或更新：

- `.github/workflows/p2_3_integrated_roundtrip.yml`
- cloud workflow run ID / URL / Blender version result
- cloud input QC JSON
- cloud reopen QC JSON
- cloud return SHA256 record
- local-return Blender 3.6 QC JSON / report
- `P2_3_INTEGRATION_MANIFEST_V001.json` 的 roundtrip section
- `P2_3_VALIDATION_REPORT_V001.md` 的 DoD-07 result
- 必要时补充 `P2_3_KNOWN_LIMITATIONS_V001.md`
- canonical Git commit 归档上述文本 / JSON evidence

返回 `.blend` 与原始 `.blend` 均继续 local-only，不提交普通 Git。

## 9. Regression Requirements

V002 完成前至少重新确认：

- V001 automated tests 33/33 不回退；
- local machine QC 34/34 不回退；
- Z-006 仍 `UNKNOWN / null / DO_NOT_LOCK`；
- Z-006-RC-01 仍独立、可替换、D-023 traceable；
- DG-114 / HIS-002 / 45° corner / mortise / hidden-angle boundaries 不改变；
- Component Library 仍为 11 families / 40 variants；
- V001 formal integrated candidate 仍为 365 stable mesh instances，除非真实 roundtrip compatibility fix 经明确记录且通过同等 regression。

## 10. PASS / HOLD Logic

T-008 V002 可建议 Engineering PASS 仅当：

- temporary transport hash 验证 PASS；
- Cloud Blender 4.5.13 workflow 实际执行 PASS；
- Cloud input semantic QC PASS；
- Cloud independent reopen PASS；
- artifact 成功取回；
- Local Blender 3.6.23 返回验证 PASS；
- 没有新增核心兼容性损失；
- V001 本地工程回归不退化；
- integration manifest / validation report / roundtrip evidence 完整更新并进入 canonical GitHub；
- temporary transport tag 已清理。

否则继续 HOLD，并给出精确 blocker。

Engineering PASS **仍不等于 P2.3 Gate PASS**。P2.3 Gate 还需要 ChatGPT 独立复核以及 Product Owner 对六张正式 review / evidence diagnostic 的人工审核和明确批准。

## 11. Final Report

Codex 完成后返回：

- STATUS: PASS / HOLD
- V001 regression result
- local `.blend` SHA256 / Git blob SHA / transport tag
- transport push result
- workflow run ID / URL / status
- Cloud Blender version
- cloud input semantic QC result
- cloud reopen semantic QC result
- artifact name / download result
- cloud-return `.blend` SHA256
- Local Blender 3.6 return QC result
- core semantic diff summary
- transport tag cleanup result
- automated tests / machine QC regression
- manifest / validation report updated paths
- canonical Git commit SHA / push result
- `git status --short`
- exact blocker if HOLD
- engineering recommendation

不得自行宣布 P2.3 Gate PASS 或 P2 Phase CLOSED。
