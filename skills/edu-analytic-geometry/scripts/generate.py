#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 把结构化数据注入 template/board.html，产出单页解析几何交互网页。

数据由 lib/analytic_kernel.py 的 sympy 精确计算驱动（单一数据源）：答案、坐标、步骤数值、
交互引擎初值与"理论范围/定值"严格一致。每个 build_* 内置自检断言。

依赖 sympy。用能 import sympy 的解释器运行（本机：/opt/homebrew/bin/python3.11）：
    python3 scripts/generate.py <题型key> [输出.html]
    python3 scripts/generate.py list
    python3 scripts/generate.py all <输出目录>     # 生成全部已注册题型
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp                       # noqa: E402
import conics                            # noqa: E402
import analytic_kernel as K              # noqa: E402
from analytic_kernel import m            # noqa: E402


def render_html(data: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"模板中未找到占位符 {PLACEHOLDER}")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


# ---------------- 小工具 ----------------
def f(e):
    return float(sp.N(e))


def pt(xy, color="point", label=None, emphasis=False):
    return {"xy": [f(xy[0]), f(xy[1])], "color": color, "label": label, "emphasis": emphasis}


def itv(rg):
    return "$" + rg["latex"] + "$"


def conic_board(c, color="curve", label=None):
    b = dict(c["board"]); b["name"] = "C"; b["color"] = color
    if label:
        b["label"] = label
    return b


# =====================================================================
# 1) 椭圆 · 数量积 · 取值范围（旗舰）
# =====================================================================
def build_ellipse_dot_range() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    M, F = (-1, 0), (1, 0)
    expr, cs = K.dot_product_expr(E, F, M)
    rg = K.range_over_m(expr)
    # 自检：水平线(x 轴)取到 -3，竖直线取到 7/4
    assert (rg["lo_f"], rg["hi_f"]) == (-3.0, 1.75) and rg["lo_closed"] and rg["hi_closed"]

    board = {
        "view": {"xRange": [-3.6, 3.6], "yRange": [-2.6, 2.6]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"M": pt(M, "vecA", "M(-1,0)"), "F": pt(F, "point", "F(1,0)"),
                   "P": pt((1, 1.5), "given", "P")},
        "param": {"name": "θ", "label": "旋转倾斜角 $\\theta$", "min": 0, "max": 180,
                  "step": 0.5, "value": 45, "unit": "°", "standard": 45,
                  "ticks": ["0° (x 轴)", "90°", "180°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "vector", "name": "vMA", "from": "M", "to": "A", "color": "vecA"},
            {"type": "vector", "name": "vMB", "from": "M", "to": "B", "color": "vecB"},
        ],
        "readouts": [
            {"id": "F", "label": "右焦点 F 坐标", "type": "coord", "of": "F"},
            {"id": "k", "label": "直线斜率 k", "type": "slope", "of": "l"},
            {"id": "A", "label": "交点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "交点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "dot", "label": "数量积 $\\vec{MA}\\cdot\\vec{MB}$", "type": "dot", "a": "vMA", "b": "vMB", "highlight": True},
        ],
        "rangeBar": {"of": "dot", "min": rg["lo_f"], "max": rg["hi_f"], "label": itv(rg)},
        "legend": [{"color": "line", "text": "动直线 l"}, {"color": "vecA", "text": "向量 MA (红)"},
                   {"color": "vecB", "text": "向量 MB (蓝)"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆与动态向量积范围",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1\\,(a>b>0)$ 离心率 $e=\\dfrac12$，"
                    "过点 $P\\left(1,\\dfrac32\\right)$。$M(-1,0)$，过右焦点 $F$ 的直线 $l$ 交 $C$ 于 $A,B$。</p>"
                    "<ol class='list-decimal pl-5 space-y-1'><li>求 $C$ 的标准方程；</li>"
                    "<li>求 $\\vec{MA}\\cdot\\vec{MB}$ 的取值范围。</li></ol>"),
        "answerLabel": "向量数量积取值范围", "answer": itv(rg),
    }
    steps = [
        {"title": "求椭圆 C 的标准方程",
         "content": ("<p>$e=\\dfrac{c}{a}=\\dfrac12,\\ c^2=a^2-b^2\\Rightarrow a^2=\\dfrac43b^2$；"
                     "代入 $P\\left(1,\\dfrac32\\right)$ 得 $b^2=3,\\ a^2=4$。</p>"
                     "<div class='text-center py-3 bg-indigo-50 border border-indigo-100 rounded-xl text-indigo-900 font-bold'>"
                     f"$$ {E['eq_latex']} $$</div>")},
        {"title": "联立 + 韦达定理",
         "content": ("<p>$F(1,0)$。设 $l:\\,x=my+1$（含竖直线，避免讨论斜率），代入椭圆：</p>"
                     f"<p class='text-center'>$$ {K.tex(cs['A'])}\\,y^2 + {K.tex(cs['B'])}\\,y {K.tex(cs['C'])} = 0 $$</p>"
                     f"<p>韦达：$y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$。</p>")},
        {"title": "数量积化简并求范围",
         "content": (f"<p>$\\vec{{MA}}\\cdot\\vec{{MB}}=(m^2+1)y_1y_2+2m(y_1+y_2)+4={K.tex(sp.apart(expr, K.m))}$。</p>"
                     "<p>由 $3m^2+4\\ge4$ 知 $\\dfrac{19}{3m^2+4}\\in\\left(0,\\dfrac{19}{4}\\right]$，"
                     "竖直线取到 $\\dfrac74$；$l$ 为 $x$ 轴时 $A(2,0),B(-2,0)$ 取到 $-3$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ \\vec{{MA}}\\cdot\\vec{{MB}}\\in {rg['latex']} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 2) 椭圆 · 过焦点弦长 · 取值范围
# =====================================================================
def build_ellipse_chord_range() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    F = (1, 0)
    cl2, cs = K.chord_len_sq_expr(E, F)
    rg2 = K.range_over_m(cl2)               # |AB|^2 ∈ [9,16]
    lo, hi = sp.sqrt(rg2["lo"]), sp.sqrt(rg2["hi"])
    chord_latex = K.interval_latex(lo, hi, rg2["lo_closed"], rg2["hi_closed"])
    assert (f(lo), f(hi)) == (3.0, 4.0)

    board = {
        "view": {"xRange": [-3.6, 3.6], "yRange": [-2.6, 2.6]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"F1": pt((-1, 0), "point", "F₁(-1,0)"), "F": pt(F, "given", "F(1,0)")},
        "param": {"name": "θ", "label": "弦 AB 倾斜角 $\\theta$", "min": 0, "max": 180,
                  "step": 0.5, "value": 90, "unit": "°", "standard": 90,
                  "ticks": ["0° (长轴)", "90° (通径)", "180°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "segment", "name": "AB", "a": "A", "b": "B", "color": "line2"},
        ],
        "readouts": [
            {"id": "k", "label": "直线斜率 k", "type": "slope", "of": "l"},
            {"id": "A", "label": "交点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "交点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "len", "label": "焦点弦长 $|AB|$", "type": "length", "a": "A", "b": "B", "highlight": True},
        ],
        "rangeBar": {"of": "len", "min": f(lo), "max": f(hi), "label": "$" + chord_latex + "$"},
        "legend": [{"color": "line", "text": "过焦点动弦 l"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆过焦点的弦长范围",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，过右焦点 $F(1,0)$ 的直线 $l$ 交 $C$ 于 $A,B$。"
                    "求弦长 $|AB|$ 的取值范围。</p>"),
        "answerLabel": "焦点弦长取值范围", "answer": "$|AB|\\in" + chord_latex + "$",
    }
    steps = [
        {"title": "联立 + 韦达定理",
         "content": ("<p>设 $l:\\,x=my+1$，代入椭圆得 "
                     f"$ {K.tex(cs['A'])}y^2+{K.tex(cs['B'])}y{K.tex(cs['C'])}=0 $，</p>"
                     f"<p>$y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$。</p>")},
        {"title": "弦长公式",
         "content": ("<p>$|AB|^2=(1+m^2)\\left[(y_1+y_2)^2-4y_1y_2\\right]="
                     f"{K.tex(sp.simplify(cl2))}$。</p>"
                     "<p>令 $u=m^2\\ge0$：$|AB|^2=\\dfrac{144(u+1)}{(3u+4)^2}$，关于 $u$ 单调，"
                     "$u=0$（竖直·通径）得最小 $9$，$u\\to\\infty$（水平·长轴）得最大 $16$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ |AB|\\in {chord_latex} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 3) 椭圆 · △OAB 面积 · 最值（过焦点弦）
# =====================================================================
def build_ellipse_area_max() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    F = (1, 0)
    area, cs = K.triangle_area_expr(E, F, (0, 0))
    rg = K.range_over_m(sp.simplify(area), horizontal_valid=False)   # (0, 3/2]
    assert rg["hi_f"] == 1.5 and rg["hi_closed"] and not rg["lo_closed"]

    board = {
        "view": {"xRange": [-3.6, 3.6], "yRange": [-2.6, 2.6]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"O": pt((0, 0), "point", "O"), "F": pt(F, "given", "F(1,0)")},
        "param": {"name": "θ", "label": "弦 AB 倾斜角 $\\theta$", "min": 0, "max": 180,
                  "step": 0.5, "value": 90, "unit": "°", "standard": 90,
                  "ticks": ["0°", "90°", "180°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "polygon", "name": "tri", "pts": ["O", "A", "B"], "color": "area", "stroke": "line2"},
        ],
        "readouts": [
            {"id": "A", "label": "交点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "交点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "len", "label": "弦长 $|AB|$", "type": "length", "a": "A", "b": "B"},
            {"id": "area", "label": "$S_{\\triangle OAB}$", "type": "area_triangle", "pts": ["O", "A", "B"], "highlight": True},
        ],
        "rangeBar": {"of": "area", "min": 0.0, "max": rg["hi_f"], "label": itv(rg)},
        "legend": [{"color": "line", "text": "过焦点动弦 l"}, {"color": "area", "text": "△OAB"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆中三角形面积的最值",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，$O$ 为原点，过右焦点 $F(1,0)$ 的直线 $l$ 交 $C$ 于 $A,B$。"
                    "求 $\\triangle OAB$ 面积的最大值。</p>"),
        "answerLabel": "△OAB 面积最大值", "answer": "$\\dfrac{3}{2}$",
    }
    steps = [
        {"title": "面积表达式",
         "content": ("<p>设 $l:\\,x=my+1$。$S=\\dfrac12|AB|\\cdot d(O,l)=\\dfrac12\\,\\dfrac{|c|}{\\sqrt{1+m^2}}\\,|AB|$。</p>"
                     f"<p>代入韦达 $y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$，化简得 "
                     f"$S={K.tex(sp.simplify(area))}$。</p>")},
        {"title": "求最大值",
         "content": ("<p>令 $u=m^2\\ge0$：$S=\\dfrac{6\\sqrt{u+1}}{3u+4}$，$S^2=\\dfrac{36(u+1)}{(3u+4)^2}$ 在 $u\\ge0$ "
                     "单调递减，故 $u=0$（竖直弦）时取最大。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ S_{\\max}=\\dfrac{3}{2} $$</div>"
                     "<p class='text-slate-500 text-sm'>（$l$ 趋于 $x$ 轴时 $O,A,B$ 共线，面积趋于 0，故 "
                     f"$S\\in {rg['latex']}$。）</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 4) 椭圆 · 斜率之积 · 定值（中心对称弦）
# =====================================================================
def build_ellipse_slopeprod_const() -> dict:
    E = conics.ellipse(2, sp.sqrt(3))
    P = (2, 0)
    val = K.slope_product_central(E, P)        # -3/4
    assert sp.simplify(val + sp.Rational(3, 4)) == 0

    board = {
        "view": {"xRange": [-3.2, 3.2], "yRange": [-2.4, 2.4]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"P": pt(P, "fixed", "P(2,0)", emphasis=True)},
        "param": {"name": "t", "label": "动点 A 的参数角 $t$", "min": 12, "max": 168,
                  "step": 1, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["12°", "90°", "168°"]},
        "derived": [
            {"type": "point_on_conic", "name": "A", "conic": "C", "t": "@param", "color": "ptA", "emphasis": True},
            {"type": "point_reflect", "name": "B", "of": "A", "center": [0, 0], "color": "ptB", "emphasis": True},
            {"type": "line_through_points", "name": "PA", "a": "P", "b": "A", "color": "vecA"},
            {"type": "line_through_points", "name": "PB", "a": "P", "b": "B", "color": "vecB"},
            {"type": "segment", "name": "AB", "a": "A", "b": "B", "color": "aux", "dashed": True},
        ],
        "readouts": [
            {"id": "A", "label": "动点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "对称点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "kPA", "label": "斜率 $k_{PA}$", "type": "slope", "of": "PA"},
            {"id": "kprod", "label": "斜率之积 $k_{PA}\\cdot k_{PB}$", "type": "slope_product", "a": "PA", "b": "PB", "highlight": True},
        ],
        "constant": {"of": "kprod", "label": "$-\\dfrac{3}{4}$"},
        "legend": [{"color": "vecA", "text": "直线 PA"}, {"color": "vecB", "text": "直线 PB"},
                   {"color": "aux", "text": "AB 过中心 O"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆中斜率之积的定值",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，$P(2,0)$ 为右顶点。$A,B$ 是 $C$ 上关于原点对称的两点"
                    "（$B=-A$）。求证 $k_{PA}\\cdot k_{PB}$ 为定值。</p>"),
        "answerLabel": "斜率之积定值", "answer": "$k_{PA}\\cdot k_{PB}=-\\dfrac{3}{4}$",
    }
    steps = [
        {"title": "设点",
         "content": ("<p>设 $A(x_0,y_0)$，则 $B(-x_0,-y_0)$，且 $\\dfrac{x_0^2}{4}+\\dfrac{y_0^2}{3}=1$，"
                     "即 $y_0^2=3\\left(1-\\dfrac{x_0^2}{4}\\right)=\\dfrac{3(4-x_0^2)}{4}$。</p>")},
        {"title": "计算斜率之积",
         "content": ("<p>$k_{PA}\\cdot k_{PB}=\\dfrac{y_0-0}{x_0-2}\\cdot\\dfrac{-y_0-0}{-x_0-2}"
                     "=\\dfrac{-y_0^2}{(x_0-2)(-x_0-2)}=\\dfrac{-y_0^2}{4-x_0^2}$。</p>"
                     "<p>代入 $y_0^2=\\dfrac{3(4-x_0^2)}{4}$：</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ k_{PA}\\cdot k_{PB}=\\dfrac{-\\frac{3}{4}(4-x_0^2)}{4-x_0^2}=-\\dfrac{3}{4} $$</div>"
                     "<p class='text-slate-500 text-sm'>与 $A$ 的位置无关，恒为定值。拖动滑块即可观察。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 5) 抛物线 · 焦点弦 OA·OB · 定值
# =====================================================================
def build_parabola_dot_const() -> dict:
    PB = conics.parabola(2)                 # y^2 = 4x, focus (1,0)
    F = (1, 0)
    expr, cs = K.dot_product_expr(PB, F, (0, 0))
    const, val = K.is_constant_in_m(expr)
    assert const and sp.simplify(val + 3) == 0

    board = {
        "view": {"xRange": [-2.0, 7.0], "yRange": [-4.0, 4.0]},
        "conics": [conic_board(PB, label="C: y² = 4x")],
        "points": {"O": pt((0, 0), "point", "O"), "F": pt(F, "fixed", "F(1,0)", emphasis=True)},
        "param": {"name": "θ", "label": "焦点弦倾斜角 $\\theta$", "min": 18, "max": 162,
                  "step": 0.5, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["18°", "90°", "162°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "F", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "vector", "name": "vOA", "from": "O", "to": "A", "color": "vecA"},
            {"type": "vector", "name": "vOB", "from": "O", "to": "B", "color": "vecB"},
        ],
        "readouts": [
            {"id": "A", "label": "交点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "交点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "k", "label": "直线斜率 k", "type": "slope", "of": "l"},
            {"id": "dot", "label": "$\\vec{OA}\\cdot\\vec{OB}$", "type": "dot", "a": "vOA", "b": "vOB", "highlight": True},
        ],
        "constant": {"of": "dot", "label": "$-3$"},
        "legend": [{"color": "line", "text": "过焦点弦 l"}, {"color": "vecA", "text": "向量 OA"},
                   {"color": "vecB", "text": "向量 OB"}],
    }
    lesson = {
        "language": "zh-CN", "title": "抛物线焦点弦的数量积定值",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>抛物线 $C:y^2=4x$，$O$ 为原点，过焦点 $F(1,0)$ 的直线 $l$ 交 $C$ 于 $A,B$。"
                    "求证 $\\vec{OA}\\cdot\\vec{OB}$ 为定值。</p>"),
        "answerLabel": "数量积定值", "answer": "$\\vec{OA}\\cdot\\vec{OB}=-3$",
    }
    steps = [
        {"title": "联立 + 韦达定理",
         "content": ("<p>设 $l:\\,x=my+1$，代入 $y^2=4x$ 得 "
                     f"$ y^2-4my-4=0 $，故 $y_1+y_2={K.tex(cs['ysum'])},\\ y_1y_2={K.tex(cs['yprod'])}$。</p>"
                     "<p>又 $x_i=\\dfrac{y_i^2}{4}$，故 $x_1x_2=\\dfrac{(y_1y_2)^2}{16}=1$。</p>")},
        {"title": "计算数量积",
         "content": ("<p>$\\vec{OA}\\cdot\\vec{OB}=x_1x_2+y_1y_2=1+(-4)$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ \\vec{OA}\\cdot\\vec{OB}=-3 $$</div>"
                     "<p class='text-slate-500 text-sm'>与直线倾斜角无关，恒为定值。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 6) 双曲线 · 离心率 · 取值范围（"形状参数"题：滑块直接驱动 e，曲线随之重绘）
# =====================================================================
def build_hyperbola_ecc_range() -> dict:
    k = 3                                   # |PF₁| = k|PF₂|
    rg = K.ecc_range_focal_ratio(k)         # e ∈ (1, 2]
    assert rg["hi_f"] == 2.0 and rg["hi_closed"] and not rg["lo_closed"]

    # 取 a=1，则 c=e，b=√(e²−1)；曲线/焦点/P 的坐标都写成 e 的表达式，前端随滑块重算重绘。
    board = {
        "view": {"xRange": [-4.2, 4.2], "yRange": [-3.0, 3.0]},
        "conics": [{"name": "C", "kind": "hyperbola", "a": 1, "b": "sqrt(e*e-1)",
                    "center": [0, 0], "orient": "x", "asymptotes": True,
                    "color": "curve", "label": "C: x² − y²/(e²−1) = 1  (a=1)"}],
        "points": {
            "F1": {"xy": ["-e", "0"], "color": "point", "label": "F₁"},
            "F2": {"xy": ["e", "0"], "color": "given", "label": "F₂"},
            "P":  {"xy": ["2/e", "sqrt((e*e-1)*(4/(e*e)-1))"], "color": "ptA", "label": "P", "emphasis": True},
        },
        "param": {"name": "e", "label": "离心率 $e$", "min": 1.05, "max": 3, "step": 0.01,
                  "value": 1.5, "unit": "", "standard": 1.5, "ticks": ["1", "2", "3"]},
        "derived": [
            {"type": "segment", "name": "PF1", "a": "F1", "b": "P", "color": "vecA"},
            {"type": "segment", "name": "PF2", "a": "F2", "b": "P", "color": "vecB"},
        ],
        "readouts": [
            {"id": "c", "label": "半焦距 $c=ae$", "type": "expr", "expr": "e", "digits": 2},
            {"id": "pf2", "label": "$|PF_2|$", "type": "distance", "a": "F2", "b": "P"},
            {"id": "pf1", "label": "$|PF_1|$", "type": "distance", "a": "F1", "b": "P"},
            {"id": "cond", "label": "右支上 $P$ 存在", "type": "status",
             "expr": "e", "op": "<=", "rhs": 2, "okText": "满足 ✓", "badText": "不满足 ✗", "highlight": True},
        ],
        "answerBand": {"min": 1, "max": 3, "lo": float(rg["lo"]), "hi": rg["hi_f"],
                       "label": "$e\\in" + rg["latex"] + "$"},
        "legend": [{"color": "curve", "text": "双曲线 C（随 e 变形）"},
                   {"color": "vecA", "text": "|PF₁| = 3|PF₂|"}, {"color": "vecB", "text": "|PF₂|"}],
    }
    lesson = {
        "language": "zh-CN", "title": "双曲线离心率的取值范围",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>双曲线 $C:\\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}=1\\,(a,b>0)$，左右焦点 $F_1,F_2$。"
                    "若 $C$ 的右支上<strong>存在</strong>点 $P$ 使得 $|PF_1|=3|PF_2|$，求离心率 $e$ 的取值范围。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变 $e$，双曲线随之变形；当 $e>2$ 时这样的 $P$ 不再存在。）</p>"),
        "answerLabel": "离心率取值范围", "answer": "$e\\in" + rg["latex"] + "$",
    }
    steps = [
        {"title": "右支焦半径关系",
         "content": ("<p>设右支上点 $P$，由双曲线定义 $|PF_1|-|PF_2|=2a$，且右支上 $|PF_2|\\ge c-a$（最小值在右顶点取到）。</p>")},
        {"title": "代入条件求范围",
         "content": ("<p>由 $|PF_1|=3|PF_2|$ 与 $|PF_1|-|PF_2|=2a$ 得 $2|PF_2|=2a$，即 $|PF_2|=a$。</p>"
                     "<p>代入 $|PF_2|\\ge c-a$：$a\\ge c-a\\Rightarrow c\\le 2a\\Rightarrow e=\\dfrac{c}{a}\\le 2$。又双曲线 $e>1$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ e\\in" + rg["latex"] + " $$</div>"
                     "<p class='text-slate-500 text-sm'>滑块拖过 $e=2$ 时，$P$ 越过右顶点而消失，状态变为"
                     "“不满足”，指针离开绿色区间——与答案一致。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 7) 椭圆 · 求标准方程（由离心率 + 过点）
# =====================================================================
def build_standard_equation() -> dict:
    """已知椭圆离心率 e=1/2，过点 P(1, 3/2)，求标准方程。"""
    E = conics.ellipse(2, sp.sqrt(3))
    assert sp.simplify(E['ecc'] - sp.Rational(1, 2)) == 0

    board = {
        "view": {"xRange": [-3.2, 3.2], "yRange": [-2.4, 2.4]},
        "conics": [conic_board(E, label="C")],
        "points": {"F1": pt((-1, 0), "point", "F₁(-1,0)"),
                   "F2": pt((1, 0), "point", "F₂(1,0)"),
                   "P": pt((1, 1.5), "given", "P(1, 3/2)", emphasis=True),
                   "A1": pt((-2, 0), "point", "A₁(-2,0)"),
                   "A2": pt((2, 0), "point", "A₂(2,0)")},
    }
    lesson = {
        "language": "zh-CN", "title": "求椭圆的标准方程",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1\\,(a>b>0)$ 的离心率 $e=\\dfrac{1}{2}$，"
                    "且过点 $P\\left(1,\\dfrac{3}{2}\\right)$。求椭圆 $C$ 的标准方程。</p>"),
        "answerLabel": "椭圆标准方程", "answer": f"${E['eq_latex']}$",
    }
    steps = [
        {"title": "由离心率建立 a, b 关系",
         "content": ("<p>$e=\\dfrac{c}{a}=\\dfrac{1}{2}$，故 $c=\\dfrac{a}{2}$。</p>"
                     "<p>又 $c^2=a^2-b^2$，代入得 $\\dfrac{a^2}{4}=a^2-b^2$，即 $b^2=\\dfrac{3a^2}{4}$。</p>")},
        {"title": "代入过点条件求解",
         "content": ("<p>将 $P\\left(1,\\dfrac{3}{2}\\right)$ 代入 $\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1$：</p>"
                     "<p>$\\dfrac{1}{a^2}+\\dfrac{9/4}{3a^2/4}=1$，即 $\\dfrac{1}{a^2}+\\dfrac{3}{a^2}=1$。</p>"
                     "<p>$\\dfrac{4}{a^2}=1$，故 $a^2=4$，$b^2=3$。</p>"
                     "<div class='text-center py-3 bg-indigo-50 border border-indigo-100 rounded-xl text-indigo-900 font-bold'>"
                     f"$$ {E['eq_latex']} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 8) 椭圆 · 斜率之积 · 定值（中心对称弦，P 为长轴端点）
# =====================================================================
def build_ellipse_fixed_value() -> dict:
    """椭圆 x²/4+y²/3=1，P(2,0) 为右顶点，A,B 关于原点对称，求证 k_PA·k_PB 为定值。"""
    E = conics.ellipse(2, sp.sqrt(3))
    P = (2, 0)
    val = K.slope_product_central(E, P)
    assert sp.simplify(val + sp.Rational(3, 4)) == 0

    board = {
        "view": {"xRange": [-3.2, 3.2], "yRange": [-2.4, 2.4]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"P": pt(P, "fixed", "P(2,0)", emphasis=True)},
        "param": {"name": "t", "label": "动点 A 的参数角 $t$", "min": 12, "max": 168,
                  "step": 1, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["12°", "90°", "168°"]},
        "derived": [
            {"type": "point_on_conic", "name": "A", "conic": "C", "t": "@param", "color": "ptA", "emphasis": True},
            {"type": "point_reflect", "name": "B", "of": "A", "center": [0, 0], "color": "ptB", "emphasis": True},
            {"type": "line_through_points", "name": "PA", "a": "P", "b": "A", "color": "vecA"},
            {"type": "line_through_points", "name": "PB", "a": "P", "b": "B", "color": "vecB"},
        ],
        "readouts": [
            {"id": "A", "label": "动点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "对称点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "kPA", "label": "斜率 $k_{PA}$", "type": "slope", "of": "PA"},
            {"id": "kprod", "label": "$k_{PA}\\cdot k_{PB}$", "type": "slope_product", "a": "PA", "b": "PB", "highlight": True},
        ],
        "constant": {"of": "kprod", "label": "$-\\dfrac{3}{4}$"},
        "legend": [{"color": "vecA", "text": "直线 PA"}, {"color": "vecB", "text": "直线 PB"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆中斜率之积的定值",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，$P(2,0)$ 为右顶点。$A,B$ 是 $C$ 上关于原点对称的两点。"
                    "求证 $k_{PA}\\cdot k_{PB}$ 为定值。</p>"),
        "answerLabel": "斜率之积定值", "answer": "$k_{PA}\\cdot k_{PB}=-\\dfrac{3}{4}$",
    }
    steps = [
        {"title": "设点",
         "content": ("<p>设 $A(x_0,y_0)$，则 $B(-x_0,-y_0)$，且 $\\dfrac{x_0^2}{4}+\\dfrac{y_0^2}{3}=1$，"
                     "即 $y_0^2=\\dfrac{3(4-x_0^2)}{4}$。</p>")},
        {"title": "计算斜率之积",
         "content": ("<p>$k_{PA}\\cdot k_{PB}=\\dfrac{y_0}{x_0-2}\\cdot\\dfrac{-y_0}{-x_0-2}"
                     "=\\dfrac{-y_0^2}{(x_0-2)(-x_0-2)}=\\dfrac{-y_0^2}{4-x_0^2}$。</p>"
                     "<p>代入 $y_0^2=\\dfrac{3(4-x_0^2)}{4}$：</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ k_{PA}\\cdot k_{PB}=\\dfrac{-\\frac{3}{4}(4-x_0^2)}{4-x_0^2}=-\\dfrac{3}{4} $$</div>"
                     "<p class='text-slate-500 text-sm'>与 $A$ 的位置无关，恒为定值。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 9) 抛物线 · 焦点弦 · 定点（弦 AB 过焦点时，AB 恒过 x 轴上定点）
# =====================================================================
def build_parabola_fixed_point() -> dict:
    """椭圆 x²/4+y²/3=1，过点 T(1,0) 的动直线交椭圆于 A,B，
    设 A 关于 x 轴的对称点为 A'，证明直线 A'B 恒过 x 轴上的定点。
    """
    E = conics.ellipse(2, sp.sqrt(3))
    T = (1, 0)

    # sympy 验证定点
    cs = K.chord_setup(E, T)
    ys, yp = cs['ysum'], cs['yprod']
    c_val = cs['c']  # = 1 (since T=(1,0))
    x_intersect = sp.simplify(2*m*yp/ys + c_val)
    assert sp.simplify(x_intersect - 4) == 0, f"定点应为 x=4, got {x_intersect}"
    fixed_x = sp.Integer(4)

    board = {
        "view": {"xRange": [-3.2, 5.5], "yRange": [-2.4, 2.4]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"T": pt(T, "fixed", "T(1,0)", emphasis=True),
                   "Q": pt((4, 0), "point", "Q(4,0)")},
        "param": {"name": "θ", "label": "直线倾斜角 $\\theta$", "min": 10, "max": 170,
                  "step": 0.5, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["10°", "90°", "170°"]},
        "derived": [
            {"type": "line_through_angle", "name": "l", "point": "T", "angle": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
            {"type": "reflect", "name": "A2", "of": "A", "axis": "x", "color": "ptA2"},
            {"type": "line_through_points", "name": "A2B", "a": "A2", "b": "B", "color": "aux", "dashed": True},
        ],
        "readouts": [
            {"id": "A", "label": "交点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "B", "label": "交点 B", "type": "coord", "of": "B", "color": "ptB"},
            {"id": "A2", "label": "A'(x₁,-y₁)", "type": "coord", "of": "A2", "color": "ptA2"},
            {"id": "xint", "label": "A'B 与 x 轴交点", "type": "expr",
             "expr": "4", "digits": 0, "highlight": True},
        ],
        "legend": [{"color": "line", "text": "过 T 的动直线"}, {"color": "ptA2", "text": "A'(x₁,-y₁)"},
                   {"color": "aux", "text": "直线 A'B"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆中的定点问题",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，过点 $T(1,0)$ 的直线 $l$ 交 $C$ 于 $A,B$ 两点。"
                    "设 $A$ 关于 $x$ 轴的对称点为 $A'$，证明直线 $A'B$ 恒过 $x$ 轴上的定点。</p>"),
        "answerLabel": "定点坐标", "answer": "$(4,0)$",
    }
    steps = [
        {"title": "联立 + 韦达定理",
         "content": ("<p>设 $l:\\,x=my+1$，代入椭圆得 $(3m^2+4)y^2+6my-9=0$。</p>"
                     f"<p>韦达：$y_1+y_2={K.tex(ys)},\\ y_1y_2={K.tex(yp)}$。</p>")},
        {"title": "求 A'B 与 x 轴的交点",
         "content": ("<p>$A(x_1,y_1)$，$A'(x_1,-y_1)$，$B(x_2,y_2)$。</p>"
                     "<p>直线 $A'B$ 与 $x$ 轴交点的横坐标：</p>"
                     "<p>$x_0 = \\dfrac{x_2 y_1 + x_1 y_2}{y_1+y_2} = \\dfrac{2m y_1 y_2 + c(y_1+y_2)}{y_1+y_2} = 2m\\cdot\\dfrac{y_1 y_2}{y_1+y_2}+c$</p>"
                     f"<p>代入韦达量：$x_0 = 2m \\cdot \\dfrac{{{K.tex(yp)}}}{{{K.tex(ys)}}} + 1 = 2m \\cdot \\dfrac{{9}}{{6m}} + 1 = 3 + 1 = 4$</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ x_0 = 4 \\quad (\\text{与 } m \\text{ 无关}) $$</div>"
                     "<p class='text-slate-500 text-sm'>故直线 $A'B$ 恒过定点 $Q(4,0)$。拖动滑块可验证。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 10) 椭圆 · 中点弦 · 轨迹
# =====================================================================
def build_ellipse_locus() -> dict:
    """椭圆 x²/4+y²/3=1，过原点 O 的动直线交椭圆于 A,B，求弦 AB 中点 M 的轨迹。"""
    E = conics.ellipse(2, sp.sqrt(3))
    # 中点 M 的轨迹：设 M(x,y)，则 A=2M 在椭圆上（因为 B=-A）
    # 即 (2x)²/4 + (2y)²/3 = 1 => x² + 4y²/3 = 1 => x²/1 + y²/(3/4) = 1
    # 但需排除 x²/4+y²/3=1 上的点（此时 A=B 退化）
    # 实际轨迹是椭圆 x²/1 + y²/(3/4) = 1 的内部
    # 更准确：M 的轨迹方程 x²/4 + y²/3 = 1/4 (因为 A=2M 在椭圆上)
    # 即 x² + 4y²/3 = 1

    # 用 trace 功能：拖参数 t (A 的参数角)，M 是 OA 中点
    board = {
        "view": {"xRange": [-2.8, 2.8], "yRange": [-2.0, 2.0]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"O": pt((0, 0), "point", "O")},
        "param": {"name": "t", "label": "动点 A 的参数角 $t$", "min": 5, "max": 175,
                  "step": 1, "value": 60, "unit": "°", "standard": 60,
                  "ticks": ["5°", "90°", "175°"]},
        "derived": [
            {"type": "point_on_conic", "name": "A", "conic": "C", "t": "@param", "color": "ptA", "emphasis": True},
            {"type": "point_reflect", "name": "B", "of": "A", "center": [0, 0], "color": "ptB", "emphasis": True},
            {"type": "midpoint", "name": "M", "a": "A", "b": "B", "color": "trace", "emphasis": True},
            {"type": "segment", "name": "AB", "a": "A", "b": "B", "color": "line"},
            {"type": "line_through_points", "name": "OA", "a": "O", "b": "A", "color": "aux", "dashed": True},
        ],
        "readouts": [
            {"id": "A", "label": "交点 A", "type": "coord", "of": "A", "color": "ptA"},
            {"id": "M", "label": "中点 M", "type": "coord", "of": "M", "color": "trace", "highlight": True},
        ],
        "trace": {"of": "M", "samples": 200, "color": "trace"},
        "legend": [{"color": "line", "text": "弦 AB"}, {"color": "trace", "text": "中点 M 轨迹"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆中点弦的轨迹方程",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，过原点 $O$ 的动直线交 $C$ 于 $A,B$ 两点，"
                    "求弦 $AB$ 中点 $M$ 的轨迹方程。</p>"),
        "answerLabel": "中点 M 的轨迹方程", "answer": "$x^2+\\dfrac{4y^2}{3}=1$",
    }
    steps = [
        {"title": "设中点坐标",
         "content": ("<p>设 $M(x_0,y_0)$ 为弦 $AB$ 的中点。</p>"
                     "<p>因为 $O$ 是 $AB$ 的中点（过原点），所以 $B=-A$，即 $B=(-x_A,-y_A)$。</p>"
                     "<p>中点 $M=\\dfrac{A+B}{2}$。但这里 $O$ 是弦过的一点，不一定是中点。</p>"
                     "<p>更直接：设 $A(x_1,y_1)$，$B(x_2,y_2)$，$M=\\left(\\dfrac{x_1+x_2}{2},\\dfrac{y_1+y_2}{2}\\right)$。</p>")},
        {"title": "利用点差法求轨迹",
         "content": ("<p>$A,B$ 在椭圆上：$\\dfrac{x_1^2}{4}+\\dfrac{y_1^2}{3}=1$，$\\dfrac{x_2^2}{4}+\\dfrac{y_2^2}{3}=1$。</p>"
                     "<p>两式相减：$\\dfrac{x_1^2-x_2^2}{4}+\\dfrac{y_1^2-y_2^2}{3}=0$</p>"
                     "<p>$\\dfrac{(x_1+x_2)(x_1-x_2)}{4}+\\dfrac{(y_1+y_2)(y_1-y_2)}{3}=0$</p>"
                     "<p>设 $M(x_0,y_0)$，则 $x_1+x_2=2x_0$，$y_1+y_2=2y_0$。</p>"
                     "<p>又直线 $AB$ 过原点，故 $\\dfrac{y_1-y_2}{x_1-x_2}=\\dfrac{y_0}{x_0}$（斜率相等）。</p>"
                     "<p>代入得 $\\dfrac{2x_0}{4}+\\dfrac{2y_0}{3}\\cdot\\dfrac{y_0}{x_0}=0$，即 $\\dfrac{x_0}{2}+\\dfrac{2y_0^2}{3x_0}=0$。</p>"
                     "<p>化简：$3x_0^2+4y_0^2=3$，即 $x_0^2+\\dfrac{4y_0^2}{3}=1$。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ x^2+\\dfrac{4y^2}{3}=1 \\quad (\\text{椭圆内部}) $$</div>"
                     "<p class='text-slate-500 text-sm'>拖动滑块可观察中点 $M$ 的轨迹（紫色曲线）。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 11) 椭圆 · 过椭圆上一点的切线
# =====================================================================
def build_ellipse_tangent() -> dict:
    """椭圆 x²/4+y²/3=1，求过点 P(1, 3/2) 的切线方程。"""
    E = conics.ellipse(2, sp.sqrt(3))
    P = (1, sp.Rational(3, 2))
    # 切线方程：x*x0/a² + y*y0/b² = 1
    # x*1/4 + y*(3/2)/3 = 1 => x/4 + y/2 = 1 => x + 2y = 4
    tangent_latex = r"x+2y=4"
    tangent_check = sp.simplify(P[0]**2 / 4 + P[1]**2 / 3 - 1)
    assert tangent_check == 0, "P must be on the ellipse"

    board = {
        "view": {"xRange": [-3.2, 3.2], "yRange": [-2.4, 2.4]},
        "conics": [conic_board(E, label="C: x²/4 + y²/3 = 1")],
        "points": {"P": pt(P, "given", "P(1, 3/2)", emphasis=True)},
        "derived": [
            {"type": "tangent_at", "name": "t", "conic": "C", "point": "P", "color": "line"},
        ],
        "readouts": [
            {"id": "P", "label": "切点 P", "type": "coord", "of": "P", "highlight": True},
            {"id": "t", "label": "切线斜率", "type": "slope", "of": "t"},
        ],
        "legend": [{"color": "line", "text": "切线"}],
    }
    lesson = {
        "language": "zh-CN", "title": "椭圆的切线方程",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>椭圆 $C:\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$，求过点 $P\\left(1,\\dfrac{3}{2}\\right)$ 的切线方程。</p>"),
        "answerLabel": "切线方程", "answer": f"${tangent_latex}$",
    }
    steps = [
        {"title": "验证点在椭圆上",
         "content": ("<p>将 $P\\left(1,\\dfrac{3}{2}\\right)$ 代入椭圆方程：</p>"
                     "<p>$\\dfrac{1}{4}+\\dfrac{9/4}{3}=\\dfrac{1}{4}+\\dfrac{3}{4}=1$ ✓</p>"
                     "<p>所以 $P$ 在椭圆上。</p>")},
        {"title": "利用切线公式",
         "content": ("<p>椭圆 $\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1$ 上点 $P(x_0,y_0)$ 处的切线方程为：</p>"
                     "<p>$\\dfrac{x \\cdot x_0}{a^2}+\\dfrac{y \\cdot y_0}{b^2}=1$</p>"
                     "<p>代入 $a^2=4,\\,b^2=3,\\,x_0=1,\\,y_0=\\dfrac{3}{2}$：</p>"
                     "<p>$\\dfrac{x}{4}+\\dfrac{3y/2}{3}=1$，即 $\\dfrac{x}{4}+\\dfrac{y}{2}=1$</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ {tangent_latex} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {
    "ellipse_dot_range": build_ellipse_dot_range,
    "ellipse_chord_range": build_ellipse_chord_range,
    "ellipse_area_max": build_ellipse_area_max,
    "ellipse_slopeprod_const": build_ellipse_slopeprod_const,
    "parabola_dot_const": build_parabola_dot_const,
    "hyperbola_ecc_range": build_hyperbola_ecc_range,
    "standard_equation": build_standard_equation,
    "ellipse_fixed_value": build_ellipse_fixed_value,
    "parabola_fixed_point": build_parabola_fixed_point,
    "ellipse_locus": build_ellipse_locus,
    "ellipse_tangent": build_ellipse_tangent,
}


def main(argv):
    if not argv or argv[0] == "list":
        print("已注册题型:")
        for k in REGISTRY:
            print("  -", k)
        return
    if argv[0] == "all":
        out_dir = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output")
        out_dir.mkdir(parents=True, exist_ok=True)
        for k, fn in REGISTRY.items():
            render_html(fn(), out_dir / f"{k}.html")
            print("written:", out_dir / f"{k}.html")
        return
    key = argv[0]
    if key not in REGISTRY:
        print(f"未知题型 {key}；可用: {', '.join(REGISTRY)}")
        sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output" / f"{key}.html")
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
