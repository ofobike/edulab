#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直线与圆：注入 board.html 产出交互网页。"""
import json, sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "edu-analytic-geometry" / "lib"))
import sympy as sp
import conics
import line_circle_kernel as K

m_sym = sp.symbols('m', real=True)


def render_html(data, out):
    t = TEMPLATE.read_text(encoding="utf-8")
    out.write_text(t.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    return out


def f(e):
    return float(sp.N(e))


def pt(xy, color="point", label=None, emphasis=False):
    return {"xy": [f(xy[0]), f(xy[1])], "color": color, "label": label, "emphasis": emphasis}


def conic_board(c, color="curve", label=None):
    b = dict(c["board"]); b["name"] = "C"; b["color"] = color
    if label: b["label"] = label
    return b


def build_line_circle_position() -> dict:
    """直线 y=kx+1 与圆 x²+y²=4 的位置关系。拖 k 看相切→相交→相离。"""
    C = conics.circle((0, 0), 2)
    # 圆心到直线距离 d = |1|/sqrt(k²+1)
    # 相切: d=r=2 => 1/sqrt(k²+1)=2 => k²+1=1/4 => 无解（r>1 恒相交）
    # 改用 r=1: 相切 k=0, 相交 |k|>0 不对...
    # 用直线 y=kx+b，b 可变
    # 简化：固定 k=1，拖 b 看位置关系
    # d = |b|/sqrt(2), r=2
    # 相切: |b|=2sqrt(2), 相交: |b|<2sqrt(2), 相离: |b|>2sqrt(2)

    board = {
        "view": {"xRange": [-4, 4], "yRange": [-4, 4]},
        "conics": [conic_board(C, label="x² + y² = 4")],
        "points": {"O": pt((0, 0), "point", "O")},
        "param": {"name": "b", "label": "截距 $b$", "min": -4, "max": 4,
                  "step": 0.01, "value": 1, "unit": "", "standard": 1,
                  "ticks": ["-4", "-2√2", "0", "2√2", "4"]},
        "derived": [
            {"type": "line_through_slope", "name": "l", "slope": 1, "intercept": "@param", "color": "line"},
            {"type": "intersect_line_conic", "name": ["A", "B"], "line": "l", "conic": "C", "colors": ["ptA", "ptB"]},
        ],
        "readouts": [
            {"id": "b", "label": "截距 b", "type": "expr", "expr": "b", "digits": 2},
            {"id": "d", "label": "圆心到直线距离 d", "type": "expr", "expr": "abs(b)/sqrt(2)", "digits": 4},
            {"id": "r", "label": "半径 r = 2", "type": "expr", "expr": "2", "digits": 0},
            {"id": "status", "label": "位置关系", "type": "status",
             "expr": "abs(b)/sqrt(2)", "op": "<=", "rhs": 2,
             "okText": "相交 ✓", "badText": "相离 ✗", "highlight": True},
        ],
        "legend": [{"color": "line", "text": "y = x + b"}, {"color": "curve", "text": "圆 x²+y²=4"}],
    }
    lesson = {
        "language": "zh-CN", "title": "直线与圆的位置关系",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>直线 $y=x+b$ 与圆 $x^2+y^2=4$，讨论位置关系。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变截距 b，观察直线与圆的交点变化。）</p>"),
        "answerLabel": "位置关系",
        "answer": "$|b|<2\\sqrt{2}$ 相交，$|b|=2\\sqrt{2}$ 相切，$|b|>2\\sqrt{2}$ 相离",
    }
    steps = [
        {"title": "圆心到直线的距离",
         "content": "<p>圆心 $O(0,0)$ 到直线 $y=x+b$（即 $x-y+b=0$）的距离：</p>"
                    "<p>$d=\\dfrac{|b|}{\\sqrt{1^2+(-1)^2}}=\\dfrac{|b|}{\\sqrt{2}}$</p>"},
        {"title": "比较 d 与半径 r=2",
         "content": "<p>$d<r=2$ 时相交（2 个交点），$d=r$ 时相切（1 个交点），$d>r$ 时相离（无交点）。</p>"
                    "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    "$$ |b|<2\\sqrt{2}: \\text{相交};\\quad |b|=2\\sqrt{2}: \\text{相切};\\quad |b|>2\\sqrt{2}: \\text{相离} $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {"line_circle_position": build_line_circle_position}


def main(argv):
    if not argv or argv[0] == "list":
        print("registered:"); [print("  -", k) for k in REGISTRY]; return
    key = argv[0]
    if key not in REGISTRY:
        print(f"unknown: {key}"); sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output" / f"{key}.html")
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
