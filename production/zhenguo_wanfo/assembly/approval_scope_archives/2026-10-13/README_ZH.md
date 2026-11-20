# 万佛殿｜2026-10-13 已批准局部修改原始 BLEND 归档（待 PO 审核）

## 归档性质与批准边界

本目录仅用于将 2026-10-13 已获 Product Owner **局部形制**批准的两份原始工作 BLEND 精确保存为独立可回查的工程附件。它们是含有未批准实体的完整**工作场景文件**，不是“整套82实体 Approved”、不是已证实历史榫卯或承载结构，也不自动更新正式 Master、Registry 或 Project Control。原批准判断保持不变。

这两个文件直接复用 PR #69 在 `governance/daily-close-20261013`（HEAD `8f2265933dfa56089201473d3b9a8cf4d56f666c`）中的既有 Git Blob；未重新建模、重新导出或另行修改二进制。记录的 SHA-256 来自原公开批准绑定及云端独立保存重开验证，**并非本次新运行的 SHA-256 计算**。新归档在合并 main 之前仍需执行文件字节 SHA-256 复核。

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
- **待完成的合并前独立 SHA-256 Gate：** 在具有原始文件字节的环境运行 `sha256sum`，输出必须分别严格等于上表两个原批准 SHA-256；如不相等或无法独立核验，**不得合并 main**。
- 已能以 Git Blob SHA-1 相等确认归档引用仍是原始 Git 内容对象；这不是本次独立运行 SHA-256 的替代陈述。
- 本次只授权独立补档分支与 Draft PR；**不得据此合并 main、覆盖/改动 Master 或 Registry、修改 Project Control 或发布整模型 Approved**。
