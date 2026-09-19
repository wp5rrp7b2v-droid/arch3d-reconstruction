# P3.3｜T-021 四椽栿 Master 首件｜Product Owner Acceptance V001

Date: 2026-09-19  
Decision: **D-072**  
Task: `T-021｜P3_3_FOUR_CHUANFU_MASTER_FIRST_ARTICLE_V001`  
Master: `CMP-FRAME-FOUR-CHUANFU-001_MASTER`

## 1. Formal Decision

**PRODUCT OWNER APPROVED / FIRST ARTICLE ACCEPTED**

T-021 四椽栿 Master V001 的工程验证、视觉审核与证据边界审核均通过。该首件自 D-072 起正式获得 Product Owner 批准。

本批准不等于：
- P3.3 Stage 1 整体 PASS；
- PR #7 已合并；
- T-018 恢复；
- Stage 2 授权；
- 任何 UNKNOWN 历史事实被补全。

## 2. Accepted Evidence

- GitHub Actions Run：`35440785415` / Run #3 / **SUCCESS**
- Reviewed head commit：`f16ba22933bb48dbae8951343b76190d2c76c1cf`
- Validation：**42 / 42 PASS**
- Independent reopen：**PASS**
- Length mutation：**PASS**
- Width mutation：**PASS**
- Thickness mutation：**PASS**
- Canonical restore：**PASS**
- Review images：**6 / 6 PASS**
  - FRONT
  - SIDE
  - TOP
  - AXON
  - DIMENSION_PARAMETER_SUMMARY
  - EVIDENCE_UNCERTAINTY_SUMMARY
- Artifact ID：`10583607231`
- Artifact ZIP SHA-256：`2b5b270e43b98c2b265e487280244679661864414115bcbc2fd996237998e53e`

## 3. SHA Label Correction

正式更正此前聊天汇报中的 SHA 标签混淆：

- Canonical Master `.blend` SHA-256：
  `9f1c8531ef7d76799127d18ef97b0b0885c10a548e921ec3e119ec35a8db0997`
- Semantic geometry signature：
  `45dce8ce4e58deabd3643c57d0f6caa7ebf50a6189e8d41cf57b68e978b63322`

此前把 semantic geometry signature 误写为 Canonical `.blend` SHA-256。  
该错误属于**汇报标签错误**，不属于工程输出错误；Actions artifact 内正式字段正确，因此：

**NO ENGINEERING RERUN REQUIRED / NO GEOMETRY CHANGE / NO PARAMETER CHANGE**

## 4. Accepted Evidence Boundary

继续锁定：
- 现状实测均值截面：`426.5 × 302 mm`
- 实测样本：`413 × 295 mm`、`440 × 309 mm`
- 样本 A/B 与东/西缝对应：`UNKNOWN`
- 历史全长：`UNKNOWN / null`
- `1000 mm`：仅非历史 canonical reference
- 报告 `28分 × 20分`：仅设计分析 metadata / geometry_use_count=0
- 不添加无证据榫卯、槽口、端部、起拱、隐蔽连接或历史化变形
- P2 proxy geometry use = 0

## 5. Publication Boundary

D-072 批准的是 **T-021 首件本身**。

PR #7 当前仍保持开放；在正式交付记录物化完成前不执行 merge。  
这不影响首件批准结论，但 PR 合并仍作为后续独立 publication closure 动作处理。

## 6. Final Status

**T-021 FIRST ARTICLE = PRODUCT OWNER APPROVED / D-072**

**P3.3 Stage 1 = ACTIVE / NOT YET PASSED**

**T-018 = HOLD**
