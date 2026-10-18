# 万佛殿构件形制参考展示 V001

首页：`docs/component_form_reference_v001/index.html`

12类构件、16个独立详情页：平梁分东西缝／山面，华栱分一跳／二跳，昂分头昂／二昂，驼峰分两种承托角色。六栏首页直接对照“家族｜构件｜位置｜个数｜应有形制｜当前模型”。所有图片在本目录，Chrome打开HTML即可浏览，无服务器、外部图片或运行时依赖。

## Mac Chrome 打开方式

在现有项目仓库的终端依次执行。它会建立独立审核目录，原项目不用切换分支：

```bash
git-proxy-auto fetch origin refs/heads/evidence/component-form-reference-v001:refs/remotes/origin/evidence/component-form-reference-v001
git show origin/evidence/component-form-reference-v001:docs/component_form_reference_v001/tools/open_chrome.sh > /tmp/wanfo_component_form_open.sh
bash /tmp/wanfo_component_form_open.sh
```

没有 `git-proxy-auto` 的环境可将第一行换成 `git fetch`。脚本使用系统Git；如果发现既有审核目录有未提交修改，会停止，不覆盖。已有审核目录只有在干净、身份正确时才快进到此工作分支。

也可直接用Chrome打开已有审核目录里的 `docs/component_form_reference_v001/index.html`。GitHub网页显示HTML源码，不是可浏览预览。

## 能用于什么

- 根据本殿可见原图判断梁身、柱身、栱端、斗耳、批竹昂头等基本形态；每条建议都有出处及限制。
- 区分本殿实证、时代类比、工程建议、待确认。官方数字提取件另注明匿名节点身份推断，不当作独立实测。
- 检查现有Master和局部工作件有哪些可见简化；图C均为GitHub现有渲染，核验原始像素身份后使用。
- 山面平梁、两种驼峰的完整标准形制仍不足。其他梁端、昂尾和隐藏接口也分别保留缺口；16页完成不等于16件完整外形已确认。

## 证据及可复核结果

- `sources.html`：简明来源与采用／不采用范围。
- `data.json`：16页内容、位置和数量原口径；展示数据，不是新Registry。
- `assets/PROVENANCE.json`：每张裁切图的原图、范围、SHA-256，PR72精确Git blob核验与模型原始渲染记录。
- `qa/index.html`：真实Chrome截图、机器验证及人工视觉检查范围。
- `qa/CHROME_VALIDATION.json`：实际浏览结果。实际测试Linux Google Chrome；未远程控制用户Mac。
- `qa/STATIC_VALIDATION.json`：页面、图片、必要变体、数量语义、模型身份及保护路径验证。

实际验证已完成：[Google Chrome完整运行](https://github.com/wp5rrp7b2v-droid/arch3d-reconstruction/actions/runs/39097532511)，Chrome 155.0.8059.39，Linux；19页本地文件浏览、桌面／390px窄屏、18内容页HTTP访问及图片放大通过。人工检查16个详情页首屏，并抽查完整页和窄屏，范围与限制见 `qa/VISUAL_REVIEW.json`。最终静态核对532条本地引用、165张原图及派生图解码通过。形制真实性不因浏览通过而升级。

## 边界

基于main `414be293918fea2bf4138b1a8f4345272e8764a8`，读取正式状态R366；复核PR72 `54fac54578340918c78d65e973933b54090893a1`、PR73 `c770088e04216588eb9bcae02fa16a2b54199697`。只新增本目录及两个只作用于指定工作分支的取图／浏览验证工作流。

没有修改Master、BLEND、正式Registry、Dashboard、Project Control、PR72／PR73；没有合并main。页面中的形制建议尚未批准，不改变原批准范围。
