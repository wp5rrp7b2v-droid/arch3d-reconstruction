# 万佛殿可参考可视化构件库 V001｜审核整改 V002

浏览入口：`docs/component_atlas_v001/index.html`，使用 Chrome 直接打开，无须服务器或 ZIP。

79 个原详情页全部保留，覆盖 58 个实体构件族页面及 21 个组合、系统或边界页面，关联原有 26 个 Master 家族。首页资料图、模型图、差异卡和原图定位均以静态文件随 GitHub 分支保存。

## Mac 从 GitHub 更新并打开

在现有项目终端执行（工作目录按实际位置调整）：

```bash
cd "/Users/caroline/中国古建筑3D复原"
git-proxy-auto fetch origin visualization/wanfo-component-atlas-v001-20261017
git show FETCH_HEAD:tools/component_atlas/open_atlas_chrome.sh | bash
```

程序复用或新建相邻的“万佛殿构件图库-V001”审核目录，并用 Chrome 打开。原项目目录及 main 不切换；审核目录若有未提交修改则停止，不覆盖。

## 图片怎么读

- 图上数字指示本页讨论的可见部位；两侧数字不是已配准的同名像素。
- 绿色线只描原图可辨边缘；橙色虚框只是原图查找范围，不能作为完整外轮廓。
- 实物照片、测绘剖面、报告解释示意及官方展示提取分别标明。后两者不等于独立实测真值。
- 无法分离的单件、被遮挡的端部、身份或尺寸型未确认的个体，直接标为未知，不补成历史形状。
- Master、C02、前端C01和其他局部工作版本分别展示，批准范围不相互扩大。

## 验证与范围

实际 Chrome 截图和逐页结果：`qa/index.html`。静态资源、来源哈希和模型身份核对：`assets/v002/STATIC_VALIDATION.json`。裁切、描线、显示旋转及原图对应：`assets/v002/DERIVATION_PROVENANCE.json`。

Chrome 在 GitHub Actions 的 Linux 环境中实际测试 `file://` 入口、79个详情页、桌面和窄屏布局、图片加载、放大及标注切换。该测试不宣称用户 Mac 的浏览器版本已被远程控制，也不证明此前受限的 chatgpt.site 入口可访问。

本轮仅修改图库页面、派生标注图和验证代码；不修改 Master、批准 BLEND、Registry、正式状态或工程审批结论，不合并 main。
