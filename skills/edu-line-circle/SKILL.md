---
name: edu-line-circle
description: >-
  把一道直线与圆的位置关系题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态
  控制台（参数滑块驱动直线/圆变化 + 位置关系实时判定），右侧 2D Canvas 动态几何画板。
  覆盖直线与圆的位置关系（相切/相交/相离）、弦长、切线长、圆与圆的位置关系等题型。
  触发词：直线与圆, 位置关系, 弦长, 切线长, 圆与圆, 相切, 相交, 相离,
  解这道直线与圆题; line and circle, positional relationship, chord length,
  tangent length, interactive geometry solution page.
---

# 直线与圆 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台，中栏 KaTeX 分步解析，
右侧 2D Canvas 动态几何画板（圆 + 动直线 + 交点 + 位置关系判定）。

## 依赖
计算核心 `lib/line_circle_kernel.py` 依赖 **sympy**。模板复用 `edu-analytic-geometry` 的 board.html。

## 工作流程

### 第 1 步：得到 problem spec
整理题目为结构化 spec（圆的方程、直线方程、已知条件、所求类型）。

### 第 2 步：用 kernel 精确计算
调用 `lib/line_circle_kernel.py`：交点、距离、判别式等。

### 第 3 步：组装数据并注入模板
写临时构建脚本，组装数据，调用 `generate.render_html(data, out)`。输出到 cwd。

### 第 4 步：自检 + 第 5 步：交付

## 目录
- `template/board.html` — 数据驱动模板（复用 edu-analytic-geometry）
- `lib/line_circle_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
