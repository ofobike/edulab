---
name: edu-function
description: >-
  把一道函数与导数题解成一个自包含的交互教学网页：左侧 KaTeX 分步解析 + 动态控制台
  （参数滑块驱动函数图像实时变化 + 切线/极值/零点标注 + 实时读数），右侧 2D Canvas
  函数图像画板。支持三种入口——给定文字题、随机出题、上传题目图片识别后解题。覆盖切线
  方程、单调性与极值、零点个数讨论、不等式证明、含参分类讨论等题型，统一用"求导+分析"，
  并由 sympy 精确计算驱动。其他 agent 也可调用本技能生成此类网页。
  触发词：函数, 导数, 切线, 单调性, 极值, 零点, 不等式证明, 含参讨论, 求导, 函数图像,
  解这道导数题, 随机出一道函数题; function, derivative, tangent line, monotonicity,
  extrema, zeros, inequality proof, interactive function solution page.
---

# 函数与导数解题 → 交互网页

## 这个技能产出什么
一个可直接用浏览器打开的单页 HTML：左侧题面 + 动态控制台（参数滑块驱动函数图像实时变化，
切线/极值/零点标注，f(x) 和 f'(x) 实时读数），中栏 KaTeX 分步解析，右侧 2D Canvas
函数图像画板。

## 依赖
计算核心 `lib/function_kernel.py` 依赖 **sympy**。运行前确认 `python3 -c "import sympy"`。

## 工作流程

### 第 1 步：得到 problem spec
把题目整理成结构化 spec（函数表达式、已知条件、所求类型、语言）。
- **文字题**：直接抽取。
- **图片**：视觉读图抽取，回显给用户确认后再继续。
- **随机出题**：选函数类型与参数，kernel 求解，答案不规整就重抽。

### 第 2 步：用 kernel 精确计算
调用 `lib/function_kernel.py`：求导、单调性、极值、零点等，得到精确答案和中间量。

### 第 3 步：组装数据并注入模板
写临时构建脚本，组装 `lesson` / `steps` / `board` 数据，调用 `generate.render_html(data, out)`。
输出写到用户当前工作目录（cwd）。

### 第 4 步：自检
- kernel 答案 == 答案卡 == 末步骤展示值。
- 起本地服务预览：无控制台报错、公式渲染正常、滑块实时变化正确。

### 第 5 步：交付
成品写在 cwd，命名 `solution-<题目简述>.html`。

## 目录
- `template/graph.html` — 数据驱动模板（函数绘图引擎 + 参数滑块）
- `lib/function_kernel.py` — sympy 精确计算核心
- `scripts/generate.py` — build_* + render_html + 注册表
