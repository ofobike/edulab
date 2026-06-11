#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""平面向量：注入 board.html 产出交互网页。"""
import json, sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "board.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp
import vector_kernel as K


def render_html(data, out):
    t = TEMPLATE.read_text(encoding="utf-8")
    out.write_text(t.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    return out


def f(e):
    return float(sp.N(e))


def pt(x, y, color="point", label=None, emphasis=False):
    return {"xy": [f(x), f(y)], "color": color, "label": label, "emphasis": emphasis}


def build_dot_product() -> dict:
    """向量 OA=(1,2)，OB=(3,1)，拖 B 点看数量积变化。"""
    board = {
        "view": {"xRange": [-1, 5], "yRange": [-1, 4]},
        "points": {
            "O": pt(0, 0, "point", "O"),
            "A": pt(1, 2, "vecA", "A(1,2)", emphasis=True),
            "B": pt(3, 1, "vecB", "B(3,1)", emphasis=True),
        },
        "param": {"name": "t", "label": "B 点参数角 $t$", "min": 0, "max": 360,
                  "step": 1, "value": 18, "unit": "°", "standard": 18,
                  "ticks": ["0°", "90°", "180°", "270°"]},
        "derived": [
            {"type": "vector", "name": "vOA", "from": "O", "to": "A", "color": "vecA"},
            {"type": "vector", "name": "vOB", "from": "O", "to": "B", "color": "vecB"},
        ],
        "readouts": [
            {"id": "A", "label": "向量 OA", "type": "coord", "of": "A", "color": "vecA"},
            {"id": "B", "label": "向量 OB", "type": "coord", "of": "B", "color": "vecB"},
            {"id": "dot", "label": "OA·OB", "type": "dot", "a": "vOA", "b": "vOB", "highlight": True},
            {"id": "angle", "label": "夹角余弦", "type": "expr",
             "expr": "(1*3+2*1)/(sqrt(1+4)*sqrt(9+1))", "digits": 4},
        ],
        "legend": [{"color": "vecA", "text": "向量 OA"}, {"color": "vecB", "text": "向量 OB"}],
    }
    lesson = {
        "language": "zh-CN", "title": "向量的数量积",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>已知 $\\vec{OA}=(1,2)$，$\\vec{OB}=(3,1)$，求 $\\vec{OA}\\cdot\\vec{OB}$ 及夹角。</p>"),
        "answerLabel": "数量积", "answer": "$\\vec{OA}\\cdot\\vec{OB}=5$",
    }
    steps = [
        {"title": "数量积公式",
         "content": "<p>$\\vec{OA}\\cdot\\vec{OB}=x_1x_2+y_1y_2=1\\times3+2\\times1=5$</p>"},
        {"title": "夹角",
         "content": "<p>$\\cos\\theta=\\dfrac{\\vec{OA}\\cdot\\vec{OB}}{|\\vec{OA}|\\cdot|\\vec{OB}|}"
                    "=\\dfrac{5}{\\sqrt{5}\\cdot\\sqrt{10}}=\\dfrac{5}{\\sqrt{50}}=\\dfrac{\\sqrt{2}}{2}$</p>"
                    "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    "$$ \\theta=45° $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {"dot_product": build_dot_product}


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
