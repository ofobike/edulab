#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不等式与线性规划：注入 board.html 产出交互网页。"""
import json, sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp
import inequality_kernel as K
from inequality_kernel import x, y


def render_html(data, out):
    t = TEMPLATE.read_text(encoding="utf-8")
    out.write_text(t.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    return out


def f(e):
    return float(sp.N(e))


def pt(px, py, color="point", label=None, emphasis=False):
    return {"xy": [f(px), f(py)], "color": color, "label": label, "emphasis": emphasis}


def build_linear_program() -> dict:
    """线性规划：max z=2x+y，s.t. x+y<=4, x+3y<=6, x>=0, y>=0。"""
    result = K.linear_program(
        [(x + y, "<=", 4), (x + 3 * y, "<=", 6), (x, ">=", 0), (y, ">=", 0)],
        2 * x + y, "max"
    )
    verts = result['vertices']

    board = {
        "view": {"xRange": [-0.5, 5], "yRange": [-0.5, 4]},
        "points": {
            "O": pt(0, 0, "point", "O"),
            "opt": pt(result['opt_x'], result['opt_y'], "given",
                      f"最优点({result['opt_x']},{result['opt_y']})", emphasis=True),
        },
        "derived": [
            {"type": "polygon", "pts": [f"({f(v[0])},{f(v[1])})" for v in verts], "color": "area", "stroke": "line"},
        ],
        "readouts": [
            {"id": "z", "label": "目标函数 z=2x+y", "type": "expr",
             "expr": "2*4+0", "digits": 0, "highlight": True},
        ],
        "legend": [{"color": "area", "text": "可行域"}, {"color": "line", "text": "可行域边界"}],
    }
    lesson = {
        "language": "zh-CN", "title": "线性规划求最值",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>求 $z=2x+y$ 的最大值，约束条件：</p>"
                    "<p>$x+y\\le 4$，$x+3y\\le 6$，$x\\ge 0$，$y\\ge 0$。</p>"),
        "answerLabel": "最大值", "answer": f"$z_{{\\max}}={result['opt_latex']}$",
    }
    steps = [
        {"title": "画可行域",
         "content": "<p>画出约束条件围成的可行域（多边形区域）。</p>"
                    "<p>顶点：$O(0,0)$，$A(4,0)$，$B(3,1)$，$C(0,2)$。</p>"},
        {"title": "目标函数在各顶点的值",
         "content": f"<p>$z(O)=0$，$z(A)=8$，$z(B)=7$，$z(C)=2$。</p>"
                    f"<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    f"$$ z_{{\\max}}={result['opt_latex']} $$</div>"
                    f"<p class='text-slate-500 text-sm'>在点 $A(4,0)$ 处取到最大值。</p>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {"linear_program": build_linear_program}


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
