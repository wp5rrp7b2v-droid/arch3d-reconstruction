# 万佛殿｜2026-10-13 已批准局部修改原始 BLEND 归档（待 PO 审核）

## 归档性质与批准边界

本目录仅用于将 2026-10-13 已获 Product Owner **局部形制**批准的两份原始工作 BLEND 精确保存为独立可回查的工程附件。它们是含有未批准实体的完整**工作场景文件**，不是“整套82实体 Approved”、不是已证实历史榫卯或承载结构，也不自动更新正式 Master、Registry 或 Project Control。原批准判断保持不变。

这两个文件直接复用 PR #69 在 `governance/daily-close-20261013`（HEAD `8f2265933dfa56089201473d3b9a8cf4d56f666c`）中的既有 Git Blob；未重新建模、重新导出或另行修改二进制。2026-11-20 已额外从 GitHub API 以 Base64 读取 PR #69 来源与本归档的全部四份原始二进制，解码后独立计算 SHA-256；**两个源文件与两个归档文件各自均与批准记录 SHA-256 一致（4/4 PASS）**。哈希实现先经过空串、`abc`、`hello` 三组已知标准测试向量检验。未重新建模、导出或改写 BLEND。

## 原始文件与锁定来源

| 局部批准范围 | 本目录相对路径 | PR #69 原始 Git Blob SHA-1 | 字节数 | 2026-10-13 原批准记录 SHA-256 |
|---|---|---|---:|---|
| 斗形 C02 六处局部外形修改 | `dou_contour_c02/WANFO_DOU_CONTOUR_CANDIDATE_C02.blend` | `5179a9b6d5a20b9e0d425a6305e85a4d4ccf438c` | 247583 | `e7fffabdcab88a0262df773aabf9a4482351cd8c062ed335afcc0c4fb7a76fc8` |
| 上六椽栿前端 C01 局部缩榫 | `upper6_front_tenon_c01/WANFO_UPPER6_FRONT_TENON_C01.blend` | `c628bb50eea64f2e02c41a6cb6a939374abddff9` | 248585 | `baf43fc29fd9a769c89a0edc5cd4137d107133bf20239677105dde9baaa06e54` |

原 PR #69 文件路径：

- `production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-13/dou_contour_c02/WANFO_DOU_CONTOUR_CANDIDATE_C02.blend`
- `production/zhenguo_wanfo/assembly/candidate_snapshots/2026-10-13/upper6_front_tenon_c01/WANFO_UPPER6_FRONT_TENON_C01.blend`

## 批准范围与证据引用

1. **C02：** PO 于 2026-10-13 16:22:54（+08:00）批准六处局部修改；云端 Run `38381657859`、Artifact `11803840918`。原输入82实体含70个此前获批标记及12个待审，其中新增六处获批准后，仍有**六处其他待审实体**。源验证原始硬编码批准计数存在错误，已由 `CLOUD_RUN_BINDING.json` 披露更正。局部批准不得扩大为整个工作场景批准。
2. **上六椽栿前端 C01：** PO 于 2026-10-13 19:25:20（+08:00）批准**单一前端局部设计**；云端 Run `38388606922`、Artifact `11806969526`。其他81个源件的几何未被本次局部设计改变，不等于这些件或整根梁的历史形制通过；后端不在批准范围。
3. **原始证据在 PR #69 源分支：** `docs/assembly/daily_close/2026-10-13/APPROVED_ARTIFACT_AUDIT.json` 以及两个 `CLOUD_RUN_BINDING.json`、两个 `SAVE_REOPEN_*_VALIDATION.json`。原有 Git Blob 身份和审批结论是当前归档的依据，不修改原记录。

## 本次归档验证与禁止事项

- PR 级别要求：只有上述两份 BLEND 和本说明文档新增；主线其余文件、两份原始源分支及所有既有批准快照保持不变。
- **独立 SHA-256 Gate：PASS（2026-11-20）。** 从 GitHub API Base64 完整读取并解码两个源文件及两个补档文件，使用通过三组标准向量自检的 SHA-256 实现重新计算。C02 的两份结果均为 `e7fffabdcab88a0262df773aabf9a4482351cd8c062ed335afcc0c4fb7a76fc8`（每份247583字节）；上六椽栿前端 C01 两份结果均为 `baf43fc29fd9a769c89a0edc5cd4137d107133bf20239677105dde9baaa06e54`（每份248585字节）。两个 Git Blob 身份同时符合原绑定记录。
- **验证范围：** 文件字节与原审批哈希一致已独立 PASS；本轮没有重新在 Blender 中打开补档文件，也未测试完整木构装配、隐藏榫卯或结构受力。哈希 PASS 不构成额外的模型形制批准或合并授权。
- 本次只授权独立补档分支与 Draft PR；**不得据此合并 main、覆盖/改动 Master 或 Registry、修改 Project Control 或发布整模型 Approved**。
