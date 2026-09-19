# P3.3｜T-021 四椽栿 Master 首件｜最终验收

Date: 2026-09-19  
Decision: **D-072**  
Task: `T-021｜P3_3_FOUR_CHUANFU_MASTER_FIRST_ARTICLE_V001`  
Master: `CMP-FRAME-FOUR-CHUANFU-001_MASTER`

## 1. 最终结论

**PRODUCT OWNER APPROVED / T-021 FIRST ARTICLE PASS**

四椽栿 Master V001 已通过工程验证、ChatGPT 视觉/证据边界审核与 Product Owner 最终批准。

本批准不等于：
- P3.3 Stage 1 整体 PASS；
- PR #7 已 merge；
- Stage 2 已授权；
- T-018 已恢复。

## 2. 正式工程证据

- PR: #7
- Branch: `codex/t021-p3-3-four-chuanfu-master-first-article-v001`
- Reviewed head commit: `f16ba22933bb48dbae8951343b76190d2c76c1cf`
- GitHub Actions Run ID: `35440785415`
- Run result: **SUCCESS**
- Validation: **42/42 PASS**
- Artifact ID: `10583607231`
- Artifact name: `P3_3_T021_FOUR_CHUANFU_FIRST_ARTICLE_V001`
- Artifact ZIP SHA-256: `2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e`
- Blender: **4.5.13 LTS**
- Independent reopen: PASS
- Length mutation: PASS
- Width mutation: PASS
- Thickness mutation: PASS
- Canonical restore: PASS
- Review images: **6/6 PASS**
  - FRONT
  - SIDE
  - TOP
  - AXON
  - DIMENSION_PARAMETER_SUMMARY
  - EVIDENCE_UNCERTAINTY_SUMMARY

## 3. SHA 标识更正

此前聊天汇报曾把 semantic geometry signature 误标为 canonical `.blend` SHA-256。

正式更正如下：

- **Canonical Master binary SHA-256**  
  `9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997`

- **Semantic geometry signature**  
  `45dce8ce4e58deabd3643c57d0f6caa7ebf50a6189e8d41cf57b68e978b63322`

- **Artifact ZIP SHA-256**  
  `2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e`

本更正只修正标识标签，不改变任何 Master 几何、参数、验证结果、artifact 内容或 Actions 结果，不需要重新运行 Blender / 42项验证。

## 4. 已批准的建模边界

- 物理实例：2（东缝1 / 西缝1）
- 现状实测截面均值：**426.5 × 302 mm**
- 原始样本：413×295 mm、440×309 mm
- A/B 样本与东西缝逐一对应：**UNKNOWN**
- Historical full length：**UNKNOWN / null**
- Canonical reference length：**1000 mm / NON-HISTORICAL / PROJECT_RULE**
- Report 28分×20分：仅 design-analysis metadata，geometry_use_count=0
- Geometry：`BOUNDED_LONG_MEMBER_OUTER_ENVELOPE`
- 不包含无证据榫卯、槽口、散斗、隔架栱几何、起拱、端部细节、隐藏连接或历史化挠曲。

## 5. 后续边界

T-021 已达到首件批准条件。

下一步只允许：
1. 完成 T-021 正式 Git 跟踪交付记录闭合；
2. 单独确认 PR #7 merge 条件；
3. PR merge 仍需按项目治理单独执行。

T-018 继续 HOLD。
