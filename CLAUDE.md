# 纪念网站项目笔记

## 图片
- 原始 JPG 在 `图片们/`，WebP 在 `图片们/full/`(1200px) 和 `图片们/thumb/`(250px)
- 构建脚本：`python _build_images.py`（依赖 PIL，pip install 到 `D:\claude\claude-install`）
- 懒加载用 `data-src` + `loadSectionImages()`，fallback 值需在 `removeAttribute` 之前捕获

## S2 照片浮页
- 可滚动网格，`#float-container` 为独立滚动容器，标题/提示固定不动
- 网格列数：PC 4 列（123px）/ 手机 3 列（102px），行数根据 `PHOTOS.length` 动态计算
- **关键**：`position:absolute` 的 float-photo 必须显式设 `left`/`top`，否则全部堆在容器原点
- `makeFloats()` 设 `floatBox.style.height = totalH` 撑开滚动高度
- **从 S2 点入故事页后返回**：点击浮窗照片会设 `fromS2 = true`，`nxt()` 检测后直接 `go(2)` 回 S2。加图时无需改动此逻辑

## 爱心
- `drawHeartShape()` 使用心形参数方程：`x=16sin³t, y=13cost-5cos2t-2cos3t-cos4t`
- 缩放参数 `s` 等价于半宽（`scale = s / 16`），`s` 传入实际渲染尺寸即可
- 影响范围：S0 Canvas 心跳动画、背景浮动爱心、纪念卡片绘制
- S0 SVG 爱心路径在 HTML 中独立维护（与 Canvas 无关）

## 音乐
- `musicPlaying` 标志位须**同步设为 true**（在 `bgm.play()` 之前），否则 recovery 检查失效
- `<audio preload="auto">` 确保 play() 即时响应，避免异步加载导致播放失败
- S1 进入时 recovery：`if (bgm.paused) bgm.play()`

## 页面点击交互
- 全局 click-to-advance 与各页专属交互（S1 烟花、S2 浮页、故事页 reveal）会冲突
- 故事页：未 reveal 时拦截跳转，reveal 后允许跳转（检查 `storyStates[cur]`）
- S1：`.greeting` 区域触发烟花，不限跳转
- 排除规则用 `.closest('.story-stage')` 等语义选择器，不用具体元素名

## CSS 陷阱
- CSS `animation` 优先级高于 inline style。要覆盖动画中的属性必须同时设 `animation: none`

## 本地预览
- `npx http-server -p 8765 -c-1` 可正确处理中文路径 URL 编码

## 外部 CDN
- GSAP / JSZip / QRCode 来自 cdnjs，使用前检查 `typeof !== 'undefined'`
