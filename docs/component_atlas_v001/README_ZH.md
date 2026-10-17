# 万佛殿可参考可视化构件库 V001

在线入口：https://wanfo-component-atlas-v001.tartchair128.chatgpt.site

离线入口：[index.html](index.html)。HTML、CSS、脚本及图片在同一目录，离线亦可浏览，无需后端服务。

本库为派生可视化审核材料，覆盖现行 Registry 的全部名称条目、待绑定来源项目及必要变体。包含组合、测量边界与洞口的页面，不把这些概念等同独立物理木件。

每页展示资料原图、现有 Master 或模型缺口、形态差异、位置、复用范围和来源。已有局部装配视图与 Master 基准分开；C02、前端 C01 和后端 R01 的批准/退回边界不变。A1、A2、A3及官方展示之间的来源关系见 [sources.html](sources.html)。

模型来自已存在的 BLEND 或已保存的审核渲染；本轮不调用构件生成器、不修改形态、不保存改动到原 BLEND。云端渲染对输入二进制、网格和变换进行不变校验。PNG 为原始渲染，WebP 为网页显示副本。

验证结果见 [VALIDATION.json](VALIDATION.json)。静态检查覆盖所有详情页、目标名称、26个 Master、全部本地图像引用及解码、来源哈希和只读渲染结果。当前环境没有支持的浏览器插件，因此不声称完成浏览器人工观感审核。

重建页面：`python tools/component_atlas/build_atlas.py`；验证：`python tools/component_atlas/validate_atlas.py`。提取资料图需原始 A1/A2/A3 PDF：`python tools/component_atlas/extract_sources.py /path/to/pdfs`。

此 Draft PR 不合并 main，不改变工程事实源、批准 Master、Registry、正式工程结论或整殿装配。
