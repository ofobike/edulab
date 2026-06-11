# edulab 高中数学扩展方案

## 现有架构

两个 skill 共享四层架构：

```
SKILL.md (技能描述 + 触发词 + 工作流)
  ↓
lib/*_kernel.py (sympy 精确计算 → 返回 {answer_latex, vals, ...})
  ↓
scripts/generate.py (build_* 组装 {lesson, steps, model/board} → render_html 注入模板)
  ↓
template/*.html (__LESSON_DATA__ JSON 数据岛 → JS 驱动可视化)
```

**可复用**：render_html 注入、is_clean 筛选、tex/fnum 工具、SKILL.md 框架、evalExpr 表达式引擎。

**需新开发**：每个板块的 kernel 数学逻辑 + 可视化模板。

---

## Phase 1 — 零模板改动，立即可做 ✅ 已完成

### 1A. 立体几何补全（edu-solid-geometry） ✅

已添加 5 个 build_* 函数 + kernel solver：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 异面直线夹角（A1C 与 AD） | `skew` | ✅ |
| 2 | 二面角（正四棱锥侧面） | `dihedral` | ✅ |
| 3 | 点到平面距离（A1→BDC1） | `distance` | ✅ |
| 4 | 正三棱锥·线面角 | `tri_pyramid` | ✅ |
| 5 | 正四面体·二面角 | `tetra` | ✅ |

### 1B. 解析几何补全（edu-analytic-geometry） ✅

已添加 5 个 build_* 函数：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 求标准方程 | `standard_equation` | ✅ |
| 2 | 定值问题（斜率之积） | `ellipse_fixed_value` | ✅ |
| 3 | 定点问题（对称点连线过定点） | `parabola_fixed_point` | ✅ |
| 4 | 轨迹方程（中点弦） | `ellipse_locus` | ✅ |
| 5 | 切线 | `ellipse_tangent` | ✅ |

---

## Phase 2 — 核心新模板：通用函数绘图 ✅ 已完成

### 2A. 新建 template/graph.html ✅

已创建 `skills/edu-function/template/graph.html`，支持：
- 函数曲线 y=f(x) 绘图（支持参数化表达式）
- 参数滑块实时改变函数形态
- 切线动态绘制（拖切点）
- 极值点、零点标注
- 实时读数（f(x)值、f'(x)值）
- 范围条、定值指示
- 轨迹追踪

### 2B. 函数与导数（edu-function） ✅

已创建 `skills/edu-function/` skill，包含：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 切线方程（三次函数） | `tangent_cubic` | ✅ |
| 2 | 单调性与极值 | `monotonicity_cubic` | ✅ |
| 3 | 零点个数讨论（含参） | `zeros_cubic` | ✅ |

模板设计：

```
board 数据结构扩展：
├── functions: [{expr, color, domain, label, dashed}]  ← 新增：函数曲线
├── conics: [...]                                       ← 保留：可叠加圆锥曲线
├── points: {...}                                       ← 复用
├── param: {...}                                        ← 复用：滑块驱动
├── derived: [...]
│   ├── tangent_at_point       ← 复用
│   ├── extremum_of_function   ← 新增：求导=0
│   ├── zero_of_function       ← 新增：f(x)=0
│   ├── intersection_functions ← 新增：两函数交点
│   ├── integral_area          ← 新增：积分面积
│   └── ...现有构造保留
├── readouts: [...]
│   ├── f_value               ← 新增：f(x₀) 的值
│   ├── derivative_value      ← 新增：f'(x₀) 的值
│   ├── integral_value        ← 新增：∫f(x)dx
│   └── ...现有类型保留
└── ...其他保留
```

核心新增 JS 逻辑：
- `sampleFunction(expr, xRange, samples=200)` — 采样 y=f(x) 为点数组
- `evalDerivative(expr, x)` — 数值导数或 sympy 预计算
- `findExtrema(expr, xRange)` — 数值求 f'(x)=0
- `findZeros(expr, xRange)` — 数值求 f(x)=0
- `drawFunction(ctx, points, color)` — 绘制函数曲线

表达式引擎：复用 board.html 的 `evalExpr()`，已支持 sin/cos/sqrt/pow 等。

### 2B. 函数与导数（edu-function）

| 序号 | 题型 | 滑块驱动 | 交互方式 | kernel 复杂度 |
|---|---|---|---|---|
| 1 | 切线方程 | 切点 x₀ | 拖切点看切线变化 | 低（求导） |
| 2 | 单调性讨论 | 含参 a | 拖 a 看极值点移动 | 中（f'=0 解含参） |
| 3 | 零点个数 | 含参 a | 拖 a 看曲线与 x 轴交点变化 | 中 |
| 4 | 不等式证明 | 辅助函数参数 | 看 f(x)≥0 恒成立 | 中（最值） |
| 5 | 含参极值 | 含参 a | 拖 a 看极值读数变化 | 高（分类讨论） |
| 6 | 双函数比较 | 切点/参数 | 两条曲线 + 交点 + 间距 | 中 |

---

## Phase 3 — 复用 graph.html 模板 ✅ 已完成

### 三角函数与解三角形（edu-trigonometry） ✅

已创建 `skills/edu-trigonometry/` skill，复用 graph.html 模板：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 图像变换 y=A·sin(ωx+φ)+k | `sine_transform` | ✅ |
| 2 | 正弦定理解三角形 | `sine_law` | ✅ |
| 3 | 余弦定理解三角形 | `cosine_law` | ✅ |

---

## Phase 4 — 复用 board.html 模板 ✅ 已完成

### 4A. 直线与圆（edu-line-circle） ✅

已创建 `skills/edu-line-circle/` skill，复用 board.html 模板：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 直线与圆的位置关系 | `line_circle_position` | ✅ |

### 4B. 平面向量（edu-vector） ✅

已创建 `skills/edu-vector/` skill，复用 board.html 模板：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 数量积与夹角 | `dot_product` | ✅ |

### 4C. 不等式 / 线性规划（edu-inequality） ✅

已创建 `skills/edu-inequality/` skill，复用 board.html 模板：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 线性规划求最值 | `linear_program` | ✅ |

---

## Phase 5 — 新模板 ✅ 已完成

### 5A. 数列（edu-sequence） ✅

已创建 `skills/edu-sequence/` skill，新建 `template/sequence.html`（柱状图模板）：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 等差数列通项与求和 | `arithmetic` | ✅ |
| 2 | 等比数列通项与求和 | `geometric` | ✅ |

### 5B. 概率与统计（edu-probability） ✅

已创建 `skills/edu-probability/` skill，复用 graph.html 模板：

| 序号 | 题型 | 注册 key | 状态 |
|---|---|---|---|
| 1 | 正态分布 | `normal_distribution` | ✅ |

---

## 实施结果总结

| Phase | 板块 | 模板 | 新增题型数 | 状态 |
|---|---|---|---|---|
| 1A | 立体几何补全 | 0（复用 lesson.html） | 5 | ✅ |
| 1B | 解析几何补全 | 0（复用 board.html） | 5 | ✅ |
| 2A | graph.html 模板 | 新建 | — | ✅ |
| 2B | 函数与导数 | 复用 graph.html | 3 | ✅ |
| 3 | 三角函数 | 复用 graph.html | 3 | ✅ |
| 4A | 直线与圆 | 复用 board.html | 1 | ✅ |
| 4B | 平面向量 | 复用 board.html | 1 | ✅ |
| 4C | 不等式 | 复用 board.html | 1 | ✅ |
| 5A | 数列 | 新建 sequence.html | 2 | ✅ |
| 5B | 概率统计 | 复用 graph.html | 1 | ✅ |
| **合计** | **8 个新 skill** | **2 个新模板** | **22** | **✅ 全部完成** |

## 依赖图

```
Phase 1A (立体几何补全) ─────────────────────→ 可独立进行
Phase 1B (解析几何补全) ─────────────────────→ 可独立进行
Phase 2A (graph.html) ──→ Phase 2B (函数导数) → Phase 3 (三角函数)
Phase 4A (直线与圆) ────────────────────────→ 可独立进行
Phase 4B (平面向量) ────────────────────────→ 可独立进行
Phase 4C (不等式) ──────────────────────────→ 可独立进行
Phase 5A (数列) ────────────────────────────→ 可独立进行
Phase 5B (概率统计) ────────────────────────→ 可独立进行
```

**关键路径**：2A → 2B → 3（graph.html 是函数导数和三角函数的前置依赖）

**可并行**：Phase 1A/1B/4A/4B/4C/5A/5B 互不依赖，可同时推进。

## 每个 skill 的目录结构

新 skill 遵循统一模式：

```
skills/edu-<topic>/
├── SKILL.md              # 触发词 + 工作流
├── lib/
│   └── <topic>_kernel.py # sympy 计算核心
├── scripts/
│   └── generate.py       # build_* + render_html + 注册表
├── template/
│   └── <template>.html   # 可视化模板（新建或复用）
├── references/
│   ├── problem-schema.md # 数据格式
│   └── conventions.md    # 解法配方
└── output/               # 开发样例
```

---

## ✅ 实施完成

所有 5 个 Phase 已完成。新增 8 个 skill、22 个题型、2 个新模板。

### 完整题型清单

**原有 skill 扩展（+10 题型）**：
- edu-solid-geometry: skew, dihedral, distance, tri_pyramid, tetra
- edu-analytic-geometry: standard_equation, ellipse_fixed_value, parabola_fixed_point, ellipse_locus, ellipse_tangent

**新建 skill（+12 题型）**：
- edu-function: tangent_cubic, monotonicity_cubic, zeros_cubic
- edu-trigonometry: sine_transform, sine_law, cosine_law
- edu-line-circle: line_circle_position
- edu-vector: dot_product
- edu-inequality: linear_program
- edu-sequence: arithmetic, geometric
- edu-probability: normal_distribution
