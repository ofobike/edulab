#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把结构化课程数据注入 template/lesson.html，产出单页 HTML。

数据全部由 lib/geometry_kernel.py 的确定性计算驱动（方案 A）：
坐标、向量、最终答案均为 sympy 精确计算结果，3D 坐标与解题数值同源、严格一致。

依赖: sympy。用一个能 import sympy 的 python3 运行（若缺: python3 -m pip install sympy）:
    python3 scripts/generate.py [输出路径.html]
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "lesson.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import geometry_kernel as gk  # noqa: E402
import bodies  # noqa: E402


def _centroid(three_points):
    names = list(three_points)
    n = len(names)
    return [sum(three_points[k][i] for k in names) / n for i in range(3)]


def render_html(data: dict, out_path: Path) -> Path:
    """把数据以 JSON 形式注入模板占位符，写出 html。"""
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    payload = json.dumps(data, ensure_ascii=False)
    html = template.replace(PLACEHOLDER, payload)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def build_cube_data() -> dict:
    """正方体 ABCD-A1B1C1D1（棱长 1），求直线 A1C 与底面 ABCD 所成角的正弦值。

    几何体拓扑取自 bodies.cuboid，顶点坐标与答案取自 geometry_kernel（同源）。
    """
    sol = gk.solve_cube_line_plane_angle(edge=1, scale=2)
    mp = sol["math_points"]
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]

    topo = bodies.cuboid()  # spheres + 12 条棱
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [6, 5, 7],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Line_A1C": {"type": "line", "a": "A1", "b": "C", "color": "emphasis", "depthTest": False},
            "Plane_ABCD": {"type": "plane", "pts": ["A", "B", "C", "D"]},
            "Normal_Vector": {"type": "arrow", "origin": "A", "dir": [0, 1, 0], "length": 1.6, "color": "normal"},
            "Axis": {"type": "axes", "size": 2.6},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 线面角",
        "title": "正方体ABCD-A₁B₁C₁D₁中，棱长为1，求直线A₁C与底面ABCD所成角的正弦值",
        "answerLabel": "直线 A₁C 与底面 ABCD 所成角的正弦值",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>以顶点 $A$ 为原点，$AB$、$AD$、$AA_1$ 分别为 $x$、$y$、$z$ 轴建立坐标系。</p>"
                r"<p>因为棱长为 $1$，关键点坐标为：</p>"
                r"$$A" + mp["A"] + r", C" + mp["C"] + r", A_1" + mp["A1"] + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 6, "y": 5, "z": 7},
        },
        {
            "title": "求直线 A₁C 的方向向量",
            "content": (
                r"<p>直线 $A_1C$ 的方向向量为：</p>"
                r"$$\vec{A_1C} = C - A_1 = " + v["A1C"] + r"$$"
            ),
            "highlight": ["Line_A1C"],
            "cameraPos": {"x": 5, "y": 4, "z": 8},
        },
        {
            "title": "确定底面 ABCD 的法向量",
            "content": (
                r"<p>底面 $ABCD$ 在平面 $z = 0$ 上，其法向量竖直向上：</p>"
                r"$$\vec{n} = " + v["n_simpl"] + r"$$"
            ),
            "highlight": ["Line_A1C", "Plane_ABCD", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 6, "z": 5},
        },
        {
            "title": "利用向量公式求解",
            "content": (
                r"<p>设直线 $A_1C$ 与底面所成角为 $\theta$。</p>"
                r"<p>线面角公式：$\sin\theta = \dfrac{|\vec{A_1C} \cdot \vec{n}|}{|\vec{A_1C}|\,|\vec{n}|}$</p>"
                r"<p>计算数量积与模长：</p>"
                r"$$\vec{A_1C} \cdot \vec{n} = " + v["dot"] + r", \quad |\vec{A_1C}| = " + v["norm_line"] + r"$$"
                r"<p>代入公式：</p>"
                r"$$\sin\theta = " + v["sin"] + r"$$"
                r"<p>所以，直线 $A_1C$ 与底面 $ABCD$ 所成角的正弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_A1C", "Plane_ABCD", "Normal_Vector"],
            "cameraPos": {"x": 5, "y": 5, "z": 6},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_data(base_edge=2, height=1) -> dict:
    """正四棱锥 P-ABCD（E 为 PC 中点）线面角；底边、高可参数化（随机出题用）。

    数值全部来自 geometry_kernel，文字步骤只负责把这些数值组织成讲解。
    """
    sol = gk.solve_pyramid_line_plane_angle(base_edge=base_edge, height=height, scale=1.5)
    mp = sol["math_points"]   # 数学坐标的 LaTeX，例如 "(\\sqrt{2}, 0, 0)"
    v = sol["vals"]           # 各步骤中间量 LaTeX
    ans = sol["answer_latex"]
    diag_tex = gk.tex(gk.sp.sympify(base_edge) * gk.sqrt(2))
    half_tex = gk.tex(gk.sp.sympify(base_edge) * gk.sqrt(2) / 2)

    # ---- 3D 模型：顶点坐标取自 kernel（与解题同源）；拓扑/高亮在此声明 ----
    model = {
        "target": [0, 0.45, 0],
        "initialCamera": [5, 4, 5],
        "points": sol["three_points"],
        "spheres": ["O", "P", "A", "B", "C", "D", "E"],
        "edges": [
            {"a": "A", "b": "B"},
            {"a": "B", "b": "C"},
            {"a": "C", "b": "D"},
            {"a": "D", "b": "A", "dashed": True},
            {"a": "P", "b": "A"},
            {"a": "P", "b": "B"},
            {"a": "P", "b": "C"},
            {"a": "P", "b": "D"},
            {"a": "A", "b": "C", "color": "aux", "dashed": True},
            {"a": "B", "b": "D", "color": "aux", "dashed": True, "name": "Line_BD"},
        ],
        "elements": {
            "Line_BE": {"type": "line", "a": "B", "b": "E", "color": "emphasis", "depthTest": False},
            "Plane_PAC": {"type": "plane", "pts": ["P", "A", "C"]},
            "Normal_Vector": {"type": "arrow", "origin": "O", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Axis": {"type": "axes", "size": 3},
            # 线段长度标注（已知条件：底边、对角线、高）
            "Len_AB": {"type": "measure", "a": "A", "b": "B", "label": str(base_edge)},
            "Len_AC": {"type": "measure", "a": "A", "b": "C", "label": diag_tex},
            "Len_PO": {"type": "measure", "a": "P", "b": "O", "label": str(height)},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 线面角",
        "title": f"正四棱锥P-ABCD中，底面边长为{base_edge}，高为{height}，E为PC中点，求直线BE与平面PAC所成角的正弦值",
        "answerLabel": "直线 BE 与平面 PAC 所成角的正弦值",
        "answerValue": f"${ans}$",
    }

    # ---- 步骤文案：数值占位由 kernel 计算结果填入（不心算）----
    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>首先，我们需要建立一个合适的空间直角坐标系来量化几何元素。</p>"
                r"<p>取底面正方形 $ABCD$ 的中心 $O$ 为原点 $(0,0,0)$。</p>"
                r"<p>让底面对角线 $AC$ 在 $x$ 轴，$BD$ 在 $y$ 轴，顶点 $P$ 在 $z$ 轴上。</p>"
                r"<p>因为底面边长为 $" + str(base_edge) + r"$，所以两条对角线长为 $" + diag_tex + r"$，半对角线长为 $" + half_tex + r"$。于是关键点坐标为：</p>"
                r"$$A" + mp["A"] + r", C" + mp["C"] + r"$$"
                r"$$B" + mp["B"] + r", D" + mp["D"] + r"$$"
                r"$$P" + mp["P"] + r"$$"
                r"<p>这样 $AC \perp BD$ 关系更明显。</p>"
            ),
            "highlight": ["Axis", "Len_AB", "Len_AC", "Len_PO"],
            "cameraPos": {"x": 5, "y": 4, "z": 5},
        },
        {
            "title": "计算中点 E 与向量 BE",
            "content": (
                r"<p>已知 $E$ 是侧棱 $PC$ 的中点。</p>"
                r"<p>利用中点坐标公式：$E = \frac{P + C}{2}$</p>"
                r"$$P" + mp["P"] + r", C" + mp["C"] + r"$$"
                r"$$E = " + v["E"] + r"$$"
                r"<p>接下来计算直线 $BE$ 的方向向量 $\vec{BE}$：</p>"
                r"$$\vec{BE} = E - B = " + v["BE"] + r"$$"
            ),
            "highlight": ["Line_BE"],
            "cameraPos": {"x": 3, "y": 3, "z": 6},
        },
        {
            "title": "确定平面 PAC 的法向量",
            "content": (
                r"<p>我们需要求直线 $BE$ 与平面 $PAC$ 的夹角。</p>"
                r"<p>观察几何体特征：</p>"
                r"<ul>"
                r"<li>底面 $ABCD$ 是正方形，对角线互相垂直，即 $AC \perp BD$。</li>"
                r"<li>顶点 $P$ 在底面的投影是中心 $O$，所以 $PO \perp AC$。</li>"
                r"</ul>"
                r"<p>因为 $AC \perp BD$ 且 $AC \perp PO$，所以直线 $BD \perp$ 平面 $PAC$。</p>"
                r"<p>因此，平面 $PAC$ 的法向量 $\vec{n}$ 就是 $\vec{BD}$ 的方向：</p>"
                r"$$\vec{n} = " + v["n"] + r"$$"
                r"<p>简化取 $\vec{n} = " + v["n_simpl"] + r"$。</p>"
            ),
            "highlight": ["Line_BE", "Plane_PAC", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 5, "z": 2},
        },
        {
            "title": "利用向量公式求解",
            "content": (
                r"<p>设直线 $BE$ 与平面 $PAC$ 所成角为 $\theta$。</p>"
                r"<p>根据线面角公式：$\sin\theta = \dfrac{|\vec{BE} \cdot \vec{n}|}{|\vec{BE}|\,|\vec{n}|}$</p>"
                r"<p>向量数据：</p>"
                r"<ul>"
                r"<li>$\vec{BE} = " + v["BE"] + r"$</li>"
                r"<li>$\vec{n} = " + v["n_simpl"] + r"$</li>"
                r"</ul>"
                r"<p>计算数量积与模长：</p>"
                r"$$\vec{BE} \cdot \vec{n} = " + v["dot"] + r", \quad |\vec{BE}| = " + v["norm_BE"] + r"$$"
                r"<p>代入公式：</p>"
                r"$$\sin\theta = " + v["sin"] + r"$$"
                r"<p>所以，直线 $BE$ 与平面 $PAC$ 所成角的正弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_BE", "Plane_PAC", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 4.5, "z": 4},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_box_volume_data(lx=3, ly=4, lz=5) -> dict:
    """长方体 ABCD-A1B1C1D1，已知长宽高，求体积。演示非角度题型端到端出图。"""
    V = gk.volume_box(lx, ly, lz)
    pts = gk.cuboid(lx, ly, lz)
    scale = 3.0 / max(lx, ly, lz)
    tp = gk.to_three(pts, scale=scale)
    topo = bodies.cuboid()
    center = _centroid(tp)
    ans = gk.tex(V)

    model = {
        "target": center,
        "initialCamera": [center[0] + 5, center[1] + 4, center[2] + 6],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Edge_L": {"type": "line", "a": "A", "b": "B", "color": "emphasis"},
            "Edge_W": {"type": "line", "a": "A", "b": "D", "color": "emphasis"},
            "Edge_H": {"type": "line", "a": "A", "b": "A1", "color": "emphasis"},
            "Axis": {"type": "axes", "size": max(tp_span(tp), 2.5)},
        },
    }
    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 体积",
        "title": f"长方体ABCD-A₁B₁C₁D₁的长、宽、高分别为 {lx}、{ly}、{lz}，求其体积",
        "answerLabel": "长方体的体积",
        "answerValue": f"${ans}$",
    }
    steps = [
        {
            "title": "明确长、宽、高",
            "content": (
                r"<p>以顶点 $A$ 为原点建立坐标系，三条从 $A$ 出发的棱即长、宽、高：</p>"
                r"<ul>"
                r"<li>长 $AB = " + str(lx) + r"$</li>"
                r"<li>宽 $AD = " + str(ly) + r"$</li>"
                r"<li>高 $AA_1 = " + str(lz) + r"$</li>"
                r"</ul>"
            ),
            "highlight": ["Edge_L", "Edge_W", "Edge_H", "Axis"],
            "cameraPos": {"x": center[0] + 5, "y": center[1] + 4, "z": center[2] + 6},
        },
        {
            "title": "应用长方体体积公式",
            "content": (
                r"<p>长方体体积等于长 × 宽 × 高：</p>"
                r"$$V = AB \times AD \times AA_1$$"
            ),
            "highlight": ["Edge_L", "Edge_W", "Edge_H"],
            "cameraPos": {"x": center[0] + 4, "y": center[1] + 5, "z": center[2] + 5},
        },
        {
            "title": "代入求值",
            "content": (
                r"$$V = " + str(lx) + r" \times " + str(ly) + r" \times " + str(lz) + r" = " + ans + r"$$"
                r"<p>所以该长方体的体积为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Edge_L", "Edge_W", "Edge_H"],
            "cameraPos": {"x": center[0] + 5, "y": center[1] + 4, "z": center[2] + 5},
        },
    ]
    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def tp_span(three_points):
    xs = [three_points[k][i] for k in three_points for i in range(3)]
    return max(abs(x) for x in xs) + 0.5


def build_cube_skew_lines_data(edge=1) -> dict:
    """正方体 ABCD-A1B1C1D1（棱长 1），求异面直线 A1C 与 AD 所成角的余弦值。"""
    sol = gk.solve_cube_skew_lines_angle(edge=edge, scale=2)
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]
    topo = bodies.cuboid()
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [6, 5, 7],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Line_A1C": {"type": "line", "a": "A1", "b": "C", "color": "emphasis", "depthTest": False},
            "Line_AD": {"type": "line", "a": "A", "b": "D", "color": "aux", "depthTest": False},
            "Axis": {"type": "axes", "size": 2.6},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 异面直线夹角",
        "title": f"正方体ABCD-A₁B₁C₁D₁中，棱长为{edge}，求异面直线A₁C与AD所成角的余弦值",
        "answerLabel": "异面直线 A₁C 与 AD 所成角的余弦值",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>以顶点 $A$ 为原点，$AB$、$AD$、$AA_1$ 分别为 $x$、$y$、$z$ 轴建立坐标系。</p>"
                r"<p>关键点坐标：</p>"
                r"$$A_1" + v["A1C"].replace("(", "").replace(")", "").split("=")[0] + r"$$" if False else
                r"<p>棱长为 $" + str(edge) + r"$，关键点坐标：</p>"
                r"$$A(0,0,0),\; C" + gk.tex_vec(gk.cube(edge)["C"]) + r",\; A_1" + gk.tex_vec(gk.cube(edge)["A1"]) + r",\; D" + gk.tex_vec(gk.cube(edge)["D"]) + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 6, "y": 5, "z": 7},
        },
        {
            "title": "求两条直线的方向向量",
            "content": (
                r"<p>直线 $A_1C$ 的方向向量：</p>"
                r"$$\vec{A_1C} = C - A_1 = " + v["A1C"] + r"$$"
                r"<p>直线 $AD$ 的方向向量：</p>"
                r"$$\vec{AD} = D - A = " + v["AD"] + r"$$"
                r"<p>简化取方向向量：$\vec{d_1} = " + v["A1C_simpl"] + r"$，$\vec{d_2} = " + v["AD_simpl"] + r"$。</p>"
            ),
            "highlight": ["Line_A1C", "Line_AD"],
            "cameraPos": {"x": 5, "y": 4, "z": 8},
        },
        {
            "title": "利用向量公式求解",
            "content": (
                r"<p>设异面直线 $A_1C$ 与 $AD$ 所成角为 $\theta$。</p>"
                r"<p>异面直线夹角公式：$\cos\theta = \dfrac{|\vec{d_1} \cdot \vec{d_2}|}{|\vec{d_1}|\,|\vec{d_2}|}$</p>"
                r"<p>计算：</p>"
                r"$$|\vec{d_1} \cdot \vec{d_2}| = " + v["dot"] + r", \quad |\vec{d_1}| = " + v["norm_A1C"] + r", \quad |\vec{d_2}| = " + v["norm_AD"] + r"$$"
                r"<p>代入公式：</p>"
                r"$$\cos\theta = " + v["cos"] + r"$$"
                r"<p>所以，异面直线 $A_1C$ 与 $AD$ 所成角的余弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_A1C", "Line_AD"],
            "cameraPos": {"x": 5, "y": 5, "z": 6},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_pyramid_dihedral_data(base_edge=2, height=2) -> dict:
    """正四棱锥 P-ABCD，求侧面 PAB 与 PBC 所成二面角的余弦值。"""
    sol = gk.solve_pyramid_dihedral(base_edge=base_edge, height=height, scale=1.5)
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]
    topo = bodies.quad_pyramid()
    center = _centroid(tp)

    model = {
        "target": [0, 0.45, 0],
        "initialCamera": [5, 4, 5],
        "points": tp,
        "spheres": ["O", "P", "A", "B", "C", "D"],
        "edges": topo["edges"] + [
            {"a": "A", "b": "C", "color": "aux", "dashed": True},
            {"a": "B", "b": "D", "color": "aux", "dashed": True},
        ],
        "elements": {
            "Line_PB": {"type": "line", "a": "P", "b": "B", "color": "emphasis", "depthTest": False},
            "Plane_PAB": {"type": "plane", "pts": ["P", "A", "B"]},
            "Plane_PBC": {"type": "plane", "pts": ["P", "B", "C"]},
            "Normal_PAB": {"type": "arrow", "origin": "P", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Normal_PBC": {"type": "arrow", "origin": "P", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Axis": {"type": "axes", "size": 3},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 二面角",
        "title": f"正四棱锥P-ABCD中，底面边长为{base_edge}，高为{height}，求侧面PAB与PBC所成二面角的余弦值",
        "answerLabel": "侧面 PAB 与 PBC 所成二面角的余弦值",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>取底面正方形 $ABCD$ 的中心 $O$ 为原点。</p>"
                r"<p>对角线 $AC$ 在 $x$ 轴，$BD$ 在 $y$ 轴，顶点 $P$ 在 $z$ 轴上。</p>"
                r"<p>关键点坐标：</p>"
                r"$$A" + sol["math_points"]["A"] + r",\; B" + sol["math_points"]["B"] + r"$$"
                r"$$C" + sol["math_points"]["C"] + r",\; P" + sol["math_points"]["P"] + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 5, "y": 4, "z": 5},
        },
        {
            "title": "确定公共棱与两个半平面的法向量",
            "content": (
                r"<p>二面角沿公共棱 $PB$。在两个侧面内各取一个垂直于棱的向量。</p>"
                r"<p>面 $PAB$ 的法向量：</p>"
                r"$$\vec{n_1} = " + v["n1"] + r"$$"
                r"<p>面 $PBC$ 的法向量：</p>"
                r"$$\vec{n_2} = " + v["n2"] + r"$$"
                r"<p>简化：$\vec{n_1} = " + v["n1_simpl"] + r"$，$\vec{n_2} = " + v["n2_simpl"] + r"$。</p>"
            ),
            "highlight": ["Line_PB", "Plane_PAB", "Plane_PBC", "Normal_PAB", "Normal_PBC"],
            "cameraPos": {"x": 3, "y": 4, "z": 6},
        },
        {
            "title": "利用法向量求二面角",
            "content": (
                r"<p>二面角的余弦等于两半平面法向量夹角的余弦（注意判断锐钝）。</p>"
                r"$$\cos\theta = \dfrac{\vec{n_1} \cdot \vec{n_2}}{|\vec{n_1}|\,|\vec{n_2}|} = " + v["cos"] + r"$$"
                r"<p>所以，侧面 $PAB$ 与 $PBC$ 所成二面角的余弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_PB", "Plane_PAB", "Plane_PBC"],
            "cameraPos": {"x": 4, "y": 4.5, "z": 4},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_cube_point_plane_distance_data(edge=1) -> dict:
    """正方体 ABCD-A1B1C1D1（棱长 1），求顶点 A1 到对角面 BDC1 的距离。"""
    sol = gk.solve_cube_point_plane_distance(edge=edge, scale=2)
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]
    topo = bodies.cuboid()
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [6, 5, 7],
        "points": tp,
        "spheres": topo["spheres"],
        "edges": topo["edges"],
        "elements": {
            "Point_A1": {"type": "sphere", "center": "A1", "radius": 0.12, "color": "emphasis", "opacity": 0.8},
            "Plane_BDC1": {"type": "plane", "pts": ["B", "D", "C1"]},
            "Normal_Vector": {"type": "arrow", "origin": "B", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Axis": {"type": "axes", "size": 2.6},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 点到平面距离",
        "title": f"正方体ABCD-A₁B₁C₁D₁中，棱长为{edge}，求顶点A₁到对角面BDC₁的距离",
        "answerLabel": "顶点 A₁ 到对角面 BDC₁ 的距离",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>以顶点 $A$ 为原点，$AB$、$AD$、$AA_1$ 分别为 $x$、$y$、$z$ 轴建立坐标系。</p>"
                r"<p>关键点坐标：</p>"
                r"$$B" + sol["math_points"]["B"] + r",\; D" + sol["math_points"]["D"] + r",\; C_1" + sol["math_points"]["C1"] + r"$$"
                r"$$A_1" + sol["math_points"]["A1"] + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 6, "y": 5, "z": 7},
        },
        {
            "title": "求对角面 BDC₁ 的法向量",
            "content": (
                r"<p>在平面 $BDC_1$ 上取两个向量：</p>"
                r"$$\vec{BD} = " + v["BD"] + r",\quad \vec{BC_1} = " + v["BC1"] + r"$$"
                r"<p>法向量 $\vec{n} = \vec{BD} \times \vec{BC_1} = " + v["n"] + r"$</p>"
                r"<p>简化取 $\vec{n} = " + v["n_simpl"] + r"$。</p>"
            ),
            "highlight": ["Plane_BDC1", "Normal_Vector"],
            "cameraPos": {"x": 5, "y": 4, "z": 8},
        },
        {
            "title": "利用距离公式求解",
            "content": (
                r"<p>点到平面距离公式：$d = \dfrac{|(\vec{A_1} - \vec{B}) \cdot \vec{n}|}{|\vec{n}|}$</p>"
                r"$$d = " + v["dist"] + r"$$"
                r"<p>所以，顶点 $A_1$ 到对角面 $BDC_1$ 的距离为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Point_A1", "Plane_BDC1", "Normal_Vector"],
            "cameraPos": {"x": 5, "y": 5, "z": 6},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_tri_pyramid_line_plane_data(base_edge=2, height=2) -> dict:
    """正三棱锥 P-ABC，求侧棱 PA 与底面 ABC 所成角的正弦值。"""
    sol = gk.solve_tri_pyramid_line_plane_angle(base_edge=base_edge, height=height, scale=1.5)
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]
    topo = bodies.tri_pyramid()
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [5, 4, 5],
        "points": tp,
        "spheres": ["O", "P", "A", "B", "C"],
        "edges": topo["edges"],
        "elements": {
            "Line_PA": {"type": "line", "a": "P", "b": "A", "color": "emphasis", "depthTest": False},
            "Plane_ABC": {"type": "plane", "pts": ["A", "B", "C"]},
            "Normal_Vector": {"type": "arrow", "origin": "O", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Axis": {"type": "axes", "size": 3},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 线面角",
        "title": f"正三棱锥P-ABC中，底面边长为{base_edge}，高为{height}，求侧棱PA与底面ABC所成角的正弦值",
        "answerLabel": "侧棱 PA 与底面 ABC 所成角的正弦值",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>取底面正三角形 $ABC$ 的中心 $O$ 为原点，$BC$ 在 $x$ 轴上，$P$ 在 $z$ 轴上。</p>"
                r"<p>关键点坐标：</p>"
                r"$$A" + sol["math_points"]["A"] + r",\; B" + sol["math_points"]["B"] + r"$$"
                r"$$C" + sol["math_points"]["C"] + r",\; P" + sol["math_points"]["P"] + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 5, "y": 4, "z": 5},
        },
        {
            "title": "求侧棱方向向量与底面法向量",
            "content": (
                r"<p>侧棱 $PA$ 的方向向量：</p>"
                r"$$\vec{PA} = A - P = " + v["PA"] + r"$$"
                r"<p>底面 $ABC$ 的法向量：</p>"
                r"$$\vec{n} = " + v["n"] + r"$$"
                r"<p>简化取 $\vec{n} = " + v["n_simpl"] + r"$。</p>"
            ),
            "highlight": ["Line_PA", "Plane_ABC", "Normal_Vector"],
            "cameraPos": {"x": 3, "y": 3, "z": 6},
        },
        {
            "title": "利用线面角公式求解",
            "content": (
                r"<p>设侧棱 $PA$ 与底面 $ABC$ 所成角为 $\theta$。</p>"
                r"<p>线面角公式：$\sin\theta = \dfrac{|\vec{PA} \cdot \vec{n}|}{|\vec{PA}|\,|\vec{n}|}$</p>"
                r"$$\vec{PA} \cdot \vec{n} = " + v["dot"] + r", \quad |\vec{PA}| = " + v["norm_PA"] + r"$$"
                r"$$\sin\theta = " + v["sin"] + r"$$"
                r"<p>所以，侧棱 $PA$ 与底面 $ABC$ 所成角的正弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_PA", "Plane_ABC", "Normal_Vector"],
            "cameraPos": {"x": 4, "y": 4.5, "z": 4},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_tetrahedron_dihedral_data() -> dict:
    """正四面体 ABCD（棱长 2√2），求二面角的余弦值。"""
    sol = gk.solve_tetrahedron_dihedral(scale=1.5)
    v = sol["vals"]
    ans = sol["answer_latex"]
    tp = sol["three_points"]
    topo = bodies.tri_pyramid()
    center = _centroid(tp)

    model = {
        "target": center,
        "initialCamera": [5, 4, 5],
        "points": tp,
        "spheres": ["A", "B", "C", "D"],
        "edges": topo["edges"],
        "elements": {
            "Line_AB": {"type": "line", "a": "A", "b": "B", "color": "emphasis", "depthTest": False},
            "Plane_ABC": {"type": "plane", "pts": ["A", "B", "C"]},
            "Plane_ABD": {"type": "plane", "pts": ["A", "B", "D"]},
            "Normal_ABC": {"type": "arrow", "origin": "A", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Normal_ABD": {"type": "arrow", "origin": "A", "dir": [0, 0, 1], "length": 1.5, "color": "normal"},
            "Axis": {"type": "axes", "size": 3},
        },
    }

    lesson = {
        "language": "zh-CN",
        "meta": "交互解题 · 二面角",
        "title": "正四面体ABCD中，棱长为2√2，求二面角C-AB-D的余弦值",
        "answerLabel": "二面角 C-AB-D 的余弦值",
        "answerValue": f"${ans}$",
    }

    steps = [
        {
            "title": "建立空间直角坐标系",
            "content": (
                r"<p>正四面体 $ABCD$ 棱长为 $2\sqrt{2}$，取坐标：</p>"
                r"$$A" + sol["math_points"]["A"] + r",\; B" + sol["math_points"]["B"] + r"$$"
                r"$$C" + sol["math_points"]["C"] + r",\; D" + sol["math_points"]["D"] + r"$$"
            ),
            "highlight": ["Axis"],
            "cameraPos": {"x": 5, "y": 4, "z": 5},
        },
        {
            "title": "求两个半平面的法向量",
            "content": (
                r"<p>二面角沿棱 $AB$，在两个面内各取法向量。</p>"
                r"<p>面 $ABC$ 的法向量：</p>"
                r"$$\vec{n_1} = " + v["n1"] + r" \;\Rightarrow\; \vec{n_1} = " + v["n1_simpl"] + r"$$"
                r"<p>面 $ABD$ 的法向量：</p>"
                r"$$\vec{n_2} = " + v["n2"] + r" \;\Rightarrow\; \vec{n_2} = " + v["n2_simpl"] + r"$$"
            ),
            "highlight": ["Line_AB", "Plane_ABC", "Plane_ABD", "Normal_ABC", "Normal_ABD"],
            "cameraPos": {"x": 3, "y": 4, "z": 6},
        },
        {
            "title": "利用法向量求二面角",
            "content": (
                r"<p>二面角余弦：</p>"
                r"$$\cos\theta = \dfrac{\vec{n_1} \cdot \vec{n_2}}{|\vec{n_1}|\,|\vec{n_2}|} = " + v["cos"] + r"$$"
                r"<p>所以，二面角 $C$-$AB$-$D$ 的余弦值为 $" + ans + r"$。</p>"
            ),
            "highlight": ["Line_AB", "Plane_ABC", "Plane_ABD"],
            "cameraPos": {"x": 4, "y": 4.5, "z": 4},
        },
    ]

    return {"lesson": lesson, "steps": steps, "model": model, "_answer": ans}


def build_random_data(seed=0) -> dict:
    """随机出题：随机选题型与参数，求解，答案不规整就重抽，返回可渲染数据。

    覆盖：长方体体积、正四棱锥线面角、正方体异面直线角、正四棱锥二面角、
    正方体点到平面距离、正三棱锥线面角、正四面体二面角。
    """
    import random
    rng = random.Random(seed)
    kind = rng.choice([
        "box_volume", "pyramid_lpa", "cube_skew", "pyramid_dihedral",
        "cube_pp_dist", "tri_pyramid_lpa", "tetra_dihedral",
    ])

    if kind == "box_volume":
        lx, ly, lz = (rng.randint(2, 6) for _ in range(3))
        return build_box_volume_data(lx, ly, lz)

    if kind == "cube_skew":
        return build_cube_skew_lines_data()

    if kind == "pyramid_dihedral":
        for _ in range(50):
            a = rng.choice([2, 4, 6])
            h = rng.randint(1, 4)
            sol = gk.solve_pyramid_dihedral(base_edge=a, height=h)
            if gk.is_clean(sol["_exact"]["cos_theta"]):
                return build_pyramid_dihedral_data(base_edge=a, height=h)
        return build_pyramid_dihedral_data()

    if kind == "cube_pp_dist":
        return build_cube_point_plane_distance_data()

    if kind == "tri_pyramid_lpa":
        for _ in range(50):
            a = rng.choice([2, 4, 6])
            h = rng.randint(1, 4)
            sol = gk.solve_tri_pyramid_line_plane_angle(base_edge=a, height=h)
            if gk.is_clean(sol["_exact"]["sin_theta"]):
                return build_tri_pyramid_line_plane_data(base_edge=a, height=h)
        return build_tri_pyramid_line_plane_data()

    if kind == "tetra_dihedral":
        return build_tetrahedron_dihedral_data()

    # pyramid 线面角：重抽直到答案规整
    for _ in range(50):
        a = rng.choice([2, 4, 6])
        h = rng.randint(1, 4)
        sol = gk.solve_pyramid_line_plane_angle(base_edge=a, height=h)
        if gk.is_clean(sol["_exact"]["sin_theta"]):
            return build_data(base_edge=a, height=h)
    # 兜底
    return build_box_volume_data()


PROBLEMS = {
    "pyramid": build_data,
    "cube": build_cube_data,
    "box": build_box_volume_data,
    "skew": build_cube_skew_lines_data,
    "dihedral": build_pyramid_dihedral_data,
    "distance": build_cube_point_plane_distance_data,
    "tri_pyramid": build_tri_pyramid_line_plane_data,
    "tetra": build_tetrahedron_dihedral_data,
}


def main():
    args = list(sys.argv[1:])
    problem = "pyramid"
    out = None
    seed = 0
    for a in args:
        if a in PROBLEMS or a == "random":
            problem = a
        elif a.isdigit():
            seed = int(a)
        else:
            out = Path(a)
    if out is None:
        # 默认写到“用户当前工作目录”(cwd)，而不是技能自身目录
        out = Path.cwd() / f"{problem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = build_random_data(seed) if problem == "random" else PROBLEMS[problem]()

    # --- 自检：最终步骤展示的答案必须等于答案卡的答案（同为 kernel 计算结果）---
    final_step = data["steps"][-1]["content"]
    assert data["_answer"] in final_step, "最终步骤未包含计算所得答案"
    data.pop("_answer", None)

    render_html(data, out)
    print(f"已生成: {out}")


if __name__ == "__main__":
    main()
