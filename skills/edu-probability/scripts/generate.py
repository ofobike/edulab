#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""概率与统计：注入 graph.html 产出交互网页。"""
import json, sys, math
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "graph.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp
import probability_kernel as K


def render_html(data, out):
    t = TEMPLATE.read_text(encoding="utf-8")
    out.write_text(t.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    return out


def f(e):
    return float(sp.N(e))


def build_normal_distribution() -> dict:
    """正态分布 N(μ, σ²)：拖 μ/σ 看曲线变化。"""
    board = {
        "view": {"xRange": [-5, 5], "yRange": [-0.1, 1]},
        "functions": [
            {"expr": "exp(-(x-mu)*(x-mu)/(2*sigma*sigma))/(sigma*sqrt(2*PI))",
             "color": "curve", "label": "正态分布 N(μ,σ²)"},
        ],
        "points": {"O": [0, 0]},
        "param": {"name": "mu", "label": "均值 $\\mu$", "min": -3, "max": 3,
                  "step": 0.01, "value": 0, "unit": "", "standard": 0,
                  "ticks": ["-3", "0", "3"]},
        "scalars": [
            {"name": "sigma", "expr": "1"},
        ],
        "derived": [],
        "readouts": [
            {"id": "mu", "label": "均值 μ", "type": "expr", "expr": "mu", "digits": 2},
            {"id": "sigma", "label": "标准差 σ", "type": "expr", "expr": "sigma", "digits": 2},
            {"id": "peak", "label": "峰值 1/(σ√(2π))", "type": "expr", "expr": "1/(sigma*sqrt(2*PI))", "digits": 4, "highlight": True},
        ],
        "legend": [{"color": "curve", "text": "正态分布密度函数"}],
    }
    lesson = {
        "language": "zh-CN", "title": "正态分布",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>正态分布 $X\\sim N(\\mu,\\sigma^2)$ 的概率密度函数：</p>"
                    "<p>$f(x)=\\dfrac{1}{\\sigma\\sqrt{2\\pi}}e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变 μ，观察曲线平移。修改 sigma 可改变形状。）</p>"),
        "answerLabel": "性质", "answer": "$\\mu$ 控制中心位置，$\\sigma$ 控制胖瘦",
    }
    steps = [
        {"title": "均值 μ 的作用",
         "content": "<p>$\\mu$ 是分布的<strong>对称中心</strong>（期望）。$\\mu$ 增大时曲线右移，$\\mu$ 减小时曲线左移。</p>"},
        {"title": "标准差 σ 的作用",
         "content": "<p>$\\sigma$ 控制分布的<strong>离散程度</strong>。$\\sigma$ 越大曲线越矮胖（数据越分散），$\\sigma$ 越小曲线越高瘦（数据越集中）。</p>"
                    "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    "$$ P(\\mu-\\sigma < X < \\mu+\\sigma) \\approx 68.3\\% $$"
                    "$$ P(\\mu-2\\sigma < X < \\mu+2\\sigma) \\approx 95.4\\% $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {"normal_distribution": build_normal_distribution}


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
