---
name: edu-trigonometry
description: >-
  把一道三角函数或解三角形题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态
  控制台（参数滑块驱动波形实时变化 + 实时读数），右侧 2D Canvas 函数图像画板。支持三种
  入口——给定文字题、随机出题、上传题目图片识别后解题。覆盖三角函数图像变换
  （A/ω/φ 的影响）、正弦定理、余弦定理、三角形面积等题型，由 sympy 精确计算驱动。
  触发词：三角函数, 正弦定理, 余弦定理, 图像变换, 辅助角, 三角形面积, 解三角形,
  解这道三角函数题; trigonometry, sine law, cosine law, image transformation,
  auxiliary angle, triangle area, interactive trigonometry solution page.
---

# 三角函数与解三角形 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台（参数滑块驱动波形变化），
中栏 KaTeX 分步解析，右侧 2D Canvas 函数图像画板。

## 依赖
计算核心 `lib/trig_kernel.py` 依赖 **sympy**。

## 工作流程

### 第 1 步：得到 problem spec
整理题目为结构化 spec（三角函数参数、已知条件、所求类型、语言）。

### 第 2 步：用 kernel 精确计算
调用 `lib/trig_kernel.py`：三角函数变换、正弦/余弦定理等。

### 第 3 步：组装数据并注入模板
写临时构建脚本，组装数据，调用 `generate.render_html(data, out)`。输出到 cwd。

### 第 4 步：自检
- kernel 答案 == 答案卡 == 末步骤展示值。
- 预览：无控制台报错、波形变化正确。

### 第 5 步：交付
成品写在 cwd，命名 `solution-<题目简述>.html`。

## 目录
- `template/graph.html` — 数据驱动模板（复用 edu-function 的函数绘图引擎）
- `lib/trig_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
