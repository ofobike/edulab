---
name: edu-sequence
description: >-
  把一道数列题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态控制台
  （滑块改项数 n，实时看柱状图变化 + 前 n 项和曲线），右侧 2D Canvas 数列可视化画板。
  覆盖等差数列、等比数列的通项公式与前 n 项和等题型，由 sympy 精确计算驱动。
  触发词：数列, 等差数列, 等比数列, 通项公式, 前n项和, 求和, 解这道数列题;
  sequence, arithmetic sequence, geometric sequence, general term, sum,
  interactive sequence solution page.
---

# 数列 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台（滑块改项数 n），
中栏 KaTeX 分步解析，右侧 2D Canvas 数列可视化（柱状图 + 累积和曲线）。

## 依赖
计算核心 `lib/sequence_kernel.py` 依赖 **sympy**。模板为专用的 `template/sequence.html`。

## 工作流程

### 第 1-5 步：同其他技能（spec → kernel → 组装 → 自检 → 交付）

## 目录
- `template/sequence.html` — 数据驱动模板（柱状图 + 累积和曲线）
- `lib/sequence_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
