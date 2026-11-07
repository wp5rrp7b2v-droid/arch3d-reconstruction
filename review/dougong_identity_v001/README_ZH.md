# 万佛殿数字博物馆｜柱头斗栱模型身份与双视图最小验证 V001

**范围**：仅研究山西文物数字博物馆公开展示的 `3d/dougong/dougong.gltf`，确认网格能否被独立读取、是否能够分别识别“栌斗 / 第一跳华栱”，以及能否形成不少于两幅不同视向的可核验视图。

**不是**：将数字博物馆模型拿来装配到我们的正式项目；复制或公开分发其网格；以显示模型替代 A1/A2 测绘；从通用 `polySurface...` 名字推断真实构件；修改 PR #83 当前形制。

## 输入与 SSOT

- 正式工程状态：`main/docs/project_control/project_state.json`（R366，2026-10-13；若未来仓库已变化应重新查）。
- 前置自动化研究：[Draft PR #84](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/84)；G0 成功取得 glTF 元数据（97节点、96网格，几乎全部 `polySurface` 通用名字），**精确构件身份未确认**。
- 待审单接口候选：[Draft PR #83](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/pull/83)，下接口技术几何通过，视觉审批待定。
- 关联 A1 资料：PR #76 原始报告 PDF73（印58）、PDF60（印45），见 `review/gong_ang_form_v001/sources/PR72_PAGE_PROVENANCE.json`；两页可用于辨认木构层级和位置，**不自动证明数字博物馆任意一个网格就是同一个第一跳实例**。

## 证据与权限条件

- 网站 HTTPS 证书在2026-10-15到期，PR84证据明确 `CERT_DATE_INVALID`。因此本轮仅以**不提供任何账号/密码、只访问已知公开站点的临时 GitHub Actions 沙盒**进行带不可信TLS声明的研究性读取。
- **未找到明确可公开再分发博物馆数字模型的许可**。因此源 `gltf/bin`、纹理、基于其网格渲染的三幅图片不进入公开 Git 版本历史。三幅视图只以 Actions Artifact 暂存7天，JSON保留来源URL、哈希及结论；任何更进一步的复制/再利用须明确许可。
- 项目 A1/A2 才是工程尺寸与形制的主要事实来源，数字博物馆的展示模型只能帮助核对视觉候选。
- 模型临时读取时屏蔽材质纹理，仅以未变动的几何顶点/索引生成粘土视图；无法证明个体身份，必须显示 UNKNOWN/FAIL，不得伪称“找到正确华栱”。

## 预先定义的 G1 Gate

| 验证项 | PASS 条件 | FAIL |
|---|---|---|
| G1-1 三维可读 | 成功获得 glTF 和对应二进制，记录SHA-256、节点与网格数量、云端Blender能够导入真实网格 | 读取/导入失败 |
| G1-2 双视图 | 对同一件**完整展示斗栱**自动生成至少2个不同方向、可供复核的视图，记录文件SHA-256 | 无有效两方向 |
| G1-3 构件身份 | 有证据可以分别指出真实**柱头栌斗**和**第一跳华栱**在本模型的具体对象/面或独立实体，并与A1实图位置对应 | 通用polySurface、单纯面积/高度排序、从补间模型移植同名标签、无法与A1同一实例核对 |

只有 G1-1/G1-2/G1-3 全部PASS，才能称为“满足数字博物馆同实例外形比对输入”；其后才可单独授权修形。若 G1-3 FAIL，**维持PR83视觉待审**并停止，不继续做无证据猜测或使用展示模型推导尺寸。

## 本轮存证

- 永久保存：`review/dougong_identity_v001/output/DOUGONG_IDENTITY_PROOF.json`（技术/证据结果）、本README、可复现脚本、GitHub Actions运行链接；无外部原模型二进制。
- 暂存7天：GitHub Actions Artifact 仅包含三幅无纹理的测试视图（如成功）。
- 分支以 G0 研究分支为父分支，Draft PR 不合并main，不修改正式Master、Registry、批准记录或正式GLB/BLEND。
