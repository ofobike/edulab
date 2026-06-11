---
name: edu-inequality
description: >-
  把一道不等式或线性规划题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态
  控制台，右侧 2D Canvas 可行域画板（多边形 + 目标函数平移 + 最值标注）。覆盖线性规划
  求最值、均值不等式等题型，由 sympy 精确计算驱动。
  触发词：不等式, 线性规划, 可行域, 最值, 均值不等式, 解这道不等式题;
  inequality, linear programming, feasible region, optimization,
  AM-GM inequality, interactive inequality solution page.
---

# 不等式与线性规划 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台，中栏 KaTeX 分步解析，
右侧 2D Canvas 可行域画板（多边形区域 + 目标函数等值线 + 最值点标注）。

## 依赖
计算核心 `lib/inequality_kernel.py` 依赖 **sympy**。模板复用 `edu-analytic-geometry` 的 board.html。

## 工作流程

### 第 1-5 步：同其他技能（spec → kernel → 组装 → 自检 → 交付）

## 目录
- `template/board.html` — 数据驱动模板（复用 edu-analytic-geometry）
- `lib/inequality_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
