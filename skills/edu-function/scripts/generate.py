#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 函数与导数：注入 template/graph.html 产出交互网页。
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "graph.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp                       # noqa: E402
import function_kernel as K              # noqa: E402
from function_kernel import x            # noqa: E402


def render_html(data: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"placeholder {PLACEHOLDER} not found")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


def f(e):
    return float(sp.N(e))


def pt(px, py, color="point", label=None, emphasis=False):
    return {"xy": [f(px), f(py)], "color": color, "label": label, "emphasis": emphasis}


# =====================================================================
# 1) 切线方程：f(x)=x³-3x 在 x=t 处的切线
# =====================================================================
def build_tangent_cubic() -> dict:
    f_expr = x**3 - 3*x
    x0 = sp.Integer(1)
    t = K.tangent_line(f_expr, x0)

    board = {
        "view": {"xRange": [-3, 3], "yRange": [-4, 4]},
        "functions": [
            {"expr": "x*x*x - 3*x", "color": "curve", "label": "y = x³ − 3x"},
        ],
        "points": {
            "P": pt(x0, t['y0'], "given", f"P({x0},{f(t['y0'])})", emphasis=True),
        },
        "param": {"name": "t", "label": "切点横坐标 $t$", "min": -2.5, "max": 2.5,
                  "step": 0.01, "value": float(x0), "unit": "", "standard": float(x0),
                  "ticks": ["-2", "0", "2"]},
        "derived": [
            {"type": "tangent_at_x", "x": "@param", "color": "line"},
        ],
        "readouts": [
            {"id": "x0", "label": "切点横坐标 t", "type": "expr", "expr": "t", "digits": 2},
            {"id": "fx0", "label": "f(t)", "type": "f_value", "x": "t", "digits": 4},
            {"id": "fp", "label": "f'(t)", "type": "derivative_value", "x": "t", "digits": 4},
        ],
        "legend": [{"color": "curve", "text": "f(x) = x³ − 3x"}, {"color": "line", "text": "切线"}],
    }
    lesson = {
        "language": "zh-CN", "title": "函数的切线方程",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>已知函数 $f(x)=x^3-3x$，求曲线在 $x=1$ 处的切线方程。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变切点位置，观察切线变化。）</p>"),
        "answerLabel": "切线方程", "answer": f"${t['tangent_latex']}$",
    }
    steps = [
        {"title": "求导",
         "content": f"<p>$f'(x)={t['fp_latex']}$</p>"},
        {"title": "计算切点处的值",
         "content": (f"<p>$f({x0})={K.tex(t['y0'])}$，$f'({x0})={K.tex(t['slope'])}$。</p>")},
        {"title": "写出切线方程",
         "content": (f"<p>切线斜率 $k=f'({x0})={K.tex(t['slope'])}$。</p>"
                     f"<p>切线方程：$y - ({K.tex(t['y0'])}) = {K.tex(t['slope'])}(x - {x0})$</p>"
                     f"<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ {t['tangent_latex']} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 2) 单调性与极值：f(x)=x³-3x
# =====================================================================
def build_monotonicity_cubic() -> dict:
    f_expr = x**3 - 3*x
    m = K.monotonicity(f_expr, domain=[-3, 3])
    ext = m['extrema']

    board = {
        "view": {"xRange": [-3, 3], "yRange": [-4, 4]},
        "functions": [
            {"expr": "x*x*x - 3*x", "color": "curve", "label": "y = x³ − 3x"},
        ],
        "points": {
            "max_pt": pt(ext[0]['x'], ext[0]['y'], "ptA", f"极大({f(ext[0]['x'])},{f(ext[0]['y'])})", emphasis=True),
            "min_pt": pt(ext[1]['x'], ext[1]['y'], "ptB", f"极小({f(ext[1]['x'])},{f(ext[1]['y'])})", emphasis=True),
        },
        "param": {"name": "t", "label": "观察点 $x=t$", "min": -2.5, "max": 2.5,
                  "step": 0.01, "value": 0, "unit": "", "standard": 0,
                  "ticks": ["-2", "-1", "0", "1", "2"]},
        "derived": [
            {"type": "tangent_at_x", "x": "@param", "color": "line"},
        ],
        "readouts": [
            {"id": "t", "label": "x = t", "type": "expr", "expr": "t", "digits": 2},
            {"id": "ft", "label": "f(t)", "type": "f_value", "x": "t", "digits": 4},
            {"id": "fp", "label": "f'(t)", "type": "derivative_value", "x": "t", "digits": 4},
            {"id": "inc", "label": "单调性", "type": "status",
             "expr": "3*t*t-3", "op": ">=", "rhs": 0,
             "okText": "递增 ↑", "badText": "递减 ↓", "highlight": True},
        ],
        "legend": [{"color": "curve", "text": "f(x) = x³ − 3x"}, {"color": "line", "text": "切线"}],
    }
    lesson = {
        "language": "zh-CN", "title": "函数的单调性与极值",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>求函数 $f(x)=x^3-3x$ 的单调区间和极值。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块观察切线斜率变化：斜率>0 递增，斜率<0 递减。）</p>"),
        "answerLabel": "极值",
        "answer": f"极大值 $f(-1)={K.tex(ext[0]['y'])}$，极小值 $f(1)={K.tex(ext[1]['y'])}$",
    }
    steps = [
        {"title": "求导",
         "content": f"<p>$f'(x)={m['fp_latex']}$</p>"},
        {"title": "令 f'(x)=0 求临界点",
         "content": f"<p>$f'(x)=3x^2-3=3(x+1)(x-1)=0$，得 $x=-1$ 或 $x=1$。</p>"},
        {"title": "判断单调区间",
         "content": ("<p>当 $x<-1$ 时 $f'(x)>0$，$f$ 递增；</p>"
                     "<p>当 $-1<x<1$ 时 $f'(x)<0$，$f$ 递减；</p>"
                     "<p>当 $x>1$ 时 $f'(x)>0$，$f$ 递增。</p>")},
        {"title": "求极值",
         "content": (f"<p>$f(-1)={K.tex(ext[0]['y'])}$（极大值），$f(1)={K.tex(ext[1]['y'])}$（极小值）。</p>"
                     f"<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     f"$$ f_{{\\max}}={K.tex(ext[0]['y'])},\\quad f_{{\\min}}={K.tex(ext[1]['y'])} $$</div>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 3) 零点个数：f(x)=x³-3x+k，拖 k 看零点变化
# =====================================================================
def build_zeros_cubic() -> dict:
    # f(x)=x³-3x+k，k 为参数
    # 极大值 f(-1)=2+k，极小值 f(1)=-2+k
    # 三个零点：-2+k>0 且 2+k<0，即 -2<k<2
    # 两个零点：k=±2
    # 一个零点：k>2 或 k<-2

    board = {
        "view": {"xRange": [-3.5, 3.5], "yRange": [-5, 5]},
        "functions": [
            {"expr": "x*x*x - 3*x + k", "color": "curve", "label": "y = x³ − 3x + k"},
        ],
        "points": {
            "O": pt(0, 0, "point", "O"),
        },
        "param": {"name": "k", "label": "参数 $k$", "min": -4, "max": 4,
                  "step": 0.01, "value": 0, "unit": "", "standard": 0,
                  "ticks": ["-4", "-2", "0", "2", "4"]},
        "derived": [],
        "readouts": [
            {"id": "k", "label": "参数 k", "type": "expr", "expr": "k", "digits": 2},
            {"id": "fmax", "label": "f(-1) = 2+k", "type": "expr", "expr": "2+k", "digits": 2},
            {"id": "fmin", "label": "f(1) = -2+k", "type": "expr", "expr": "-2+k", "digits": 2},
            {"id": "zeros", "label": "零点个数", "type": "status",
             "expr": "abs(k)", "op": "<=", "rhs": 2,
             "okText": "3 个零点", "badText": "1 个零点", "highlight": True},
        ],
        "legend": [{"color": "curve", "text": "f(x) = x³ − 3x + k"}],
    }
    lesson = {
        "language": "zh-CN", "title": "函数零点个数的讨论",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>已知函数 $f(x)=x^3-3x+k$，讨论 $f(x)$ 零点的个数。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变 $k$，观察曲线与 $x$ 轴交点变化。）</p>"),
        "answerLabel": "零点个数",
        "answer": "$|k|<2$ 时 3 个，$|k|=2$ 时 2 个，$|k|>2$ 时 1 个",
    }
    steps = [
        {"title": "求导找极值",
         "content": "<p>$f'(x)=3x^2-3=3(x+1)(x-1)$。</p><p>$x=-1$ 处极大值 $f(-1)=2+k$；$x=1$ 处极小值 $f(1)=-2+k$。</p>"},
        {"title": "分类讨论",
         "content": ("<p>① 极大值 $>0$ 且极小值 $<0$：$2+k>0$ 且 $-2+k<0$，即 $-2<k<2$，有 <strong>3 个零点</strong>。</p>"
                     "<p>② 极大值 $=0$ 或极小值 $=0$：$k=\\pm 2$，有 <strong>2 个零点</strong>。</p>"
                     "<p>③ 极大值 $<0$ 或极小值 $>0$：$|k|>2$，有 <strong>1 个零点</strong>。</p>"
                     "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                     "$$ |k|<2: 3 \\text{ 个};\\quad |k|=2: 2 \\text{ 个};\\quad |k|>2: 1 \\text{ 个} $$</div>"
                     "<p class='text-slate-500 text-sm'>拖动滑块可直观看到曲线与 $x$ 轴交点个数的变化。</p>")},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {
    "tangent_cubic": build_tangent_cubic,
    "monotonicity_cubic": build_monotonicity_cubic,
    "zeros_cubic": build_zeros_cubic,
}


def main(argv):
    if not argv or argv[0] == "list":
        print("registered:")
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
        print(f"unknown type {key}; available: {', '.join(REGISTRY)}")
        sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output" / f"{key}.html")
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
