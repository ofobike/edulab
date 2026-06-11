---
name: edu-probability
description: >-
  把一道概率与统计题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态控制台
  （参数滑块驱动分布曲线实时变化 + 实时读数），右侧 2D Canvas 分布图画板。覆盖正态
  分布、二项分布等题型，由 sympy 精确计算驱动。
  触发词：概率, 统计, 正态分布, 二项分布, 期望, 方差, 解这道概率题;
  probability, statistics, normal distribution, binomial distribution,
  expectation, variance, interactive probability solution page.
---

# 概率与统计 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台（参数滑块驱动分布曲线变化），
中栏 KaTeX 分步解析，右侧 2D Canvas 分布密度曲线画板。

## 依赖
计算核心 `lib/probability_kernel.py` 依赖 **sympy**。模板复用 `edu-function` 的 graph.html。

## 工作流程

### 第 1-5 步：同其他技能（spec → kernel → 组装 → 自检 → 交付）

## 目录
- `template/graph.html` — 数据驱动模板（复用 edu-function 的函数绘图引擎）
- `lib/probability_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
