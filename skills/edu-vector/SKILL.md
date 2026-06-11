---
name: edu-vector
description: >-
  把一道平面向量题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态控制台
  （拖动向量端点看数量积/夹角实时变化），右侧 2D Canvas 向量画板。覆盖数量积、夹角、
  共线/垂直条件、基底表示等题型，由 sympy 精确计算驱动。
  触发词：向量, 数量积, 夹角, 共线, 垂直, 基底, 平面向量, 解这道向量题;
  vector, dot product, angle, collinear, perpendicular, basis,
  interactive vector solution page.
---

# 平面向量 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台，中栏 KaTeX 分步解析，
右侧 2D Canvas 向量画板（可拖动向量端点，实时显示数量积/夹角/投影）。

## 依赖
计算核心 `lib/vector_kernel.py` 依赖 **sympy**。模板复用 `edu-analytic-geometry` 的 board.html。

## 工作流程

### 第 1-5 步：同其他技能（spec → kernel → 组装 → 自检 → 交付）

## 目录
- `template/board.html` — 数据驱动模板（复用 edu-analytic-geometry）
- `lib/vector_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
