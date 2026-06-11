#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate.py — 三角函数：注入 template/graph.html 产出交互网页。
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "graph.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp                       # noqa: E402
import trig_kernel as K                  # noqa: E402


def render_html(data: dict, out_path: Path) -> Path:
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise RuntimeError(f"placeholder {PLACEHOLDER} not found")
    out_path.write_text(template.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)),
                        encoding="utf-8")
    return out_path


def f(e):
    return float(sp.N(e))


# =====================================================================
# 1) 三角函数图像变换：y = A·sin(ωx + φ) + k
# =====================================================================
def build_sine_transform() -> dict:
    """y = A·sin(ωx + φ) + k，拖 A/ω/φ 看波形变化。"""
    board = {
        "view": {"xRange": [-7, 7], "yRange": [-4, 4]},
        "functions": [
            {"expr": "A*sin(omega*x + phi) + k", "color": "curve", "label": "y = A·sin(ωx+φ)+k"},
            {"expr": "sin(x)", "color": "aux", "label": "y = sin(x)", "lineWidth": 1, "dashed": True},
        ],
        "points": {"O": [0, 0]},
        "param": {"name": "A", "label": "振幅 $A$", "min": 0.1, "max": 3,
                  "step": 0.01, "value": 1, "unit": "", "standard": 1,
                  "ticks": ["0", "1", "2", "3"]},
        "scalars": [
            {"name": "omega", "expr": "1"},
            {"name": "phi", "expr": "0"},
            {"name": "k", "expr": "0"},
        ],
        "derived": [],
        "readouts": [
            {"id": "A", "label": "振幅 A", "type": "expr", "expr": "A", "digits": 2},
            {"id": "omega", "label": "角频率 ω", "type": "expr", "expr": "omega", "digits": 2},
            {"id": "phi", "label": "初相 φ", "type": "expr", "expr": "phi", "digits": 2},
            {"id": "T", "label": "周期 T = 2π/ω", "type": "expr", "expr": "2*PI/omega", "digits": 2},
            {"id": "max", "label": "最大值 A+k", "type": "expr", "expr": "A+k", "digits": 2, "highlight": True},
            {"id": "min", "label": "最小值 -A+k", "type": "expr", "expr": "-A+k", "digits": 2},
        ],
        "legend": [{"color": "curve", "text": "y = A·sin(ωx+φ)+k"}, {"color": "aux", "text": "y = sin(x) (参考)"}],
    }
    lesson = {
        "language": "zh-CN", "title": "三角函数图像变换",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>函数 $y=A\\sin(\\omega x+\\varphi)+k$（$A>0,\\omega>0$）。"
                    "讨论参数 $A,\\omega,\\varphi,k$ 对图像的影响。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变振幅 A，观察波形变化。"
                    "修改 scalars 中的 omega/phi/k 可切换不同参数。）</p>"),
        "answerLabel": "参数说明",
        "answer": "$A$=振幅，$\\omega$=角频率，$\\varphi$=初相，$k$=上下平移",
    }
    steps = [
        {"title": "振幅 A",
         "content": "<p>$A$ 控制波形的<strong>振幅</strong>（最高点与最低点之差的一半）。$A$ 越大，波形越高。</p>"},
        {"title": "角频率 ω",
         "content": "<p>$\\omega$ 控制<strong>周期</strong> $T=\\dfrac{2\\pi}{\\omega}$。$\\omega$ 越大，周期越短，波形越密。</p>"},
        {"title": "初相 φ",
         "content": "<p>$\\varphi$ 控制波形的<strong>左右平移</strong>。$\\varphi>0$ 时图像左移 $\\dfrac{\\varphi}{\\omega}$。</p>"},
        {"title": "平移 k",
         "content": "<p>$k$ 控制波形的<strong>上下平移</strong>。$k>0$ 时上移，$k<0$ 时下移。</p>"
                    "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    "$$ y_{\\max}=A+k,\\quad y_{\\min}=-A+k $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 2) 正弦定理：已知两边一角求第三边
# =====================================================================
def build_sine_law_problem() -> dict:
    """三角形 ABC，a=2，A=30°，B=60°，求 b 和 c。"""
    r = K.sine_law(2, sp.pi / 6, sp.pi / 3)

    board = {
        "view": {"xRange": [-1, 5], "yRange": [-1, 4]},
        "points": {
            "A": [0, 0], "B": [f(r['c']), 0],
            "C": [f(r['b'] * sp.cos(sp.pi / 6)), f(r['b'] * sp.sin(sp.pi / 6))],
        },
        "derived": [
            {"type": "segment", "a": "A", "b": "B", "color": "curve"},
            {"type": "segment", "a": "B", "b": "C", "color": "curve2"},
            {"type": "segment", "a": "C", "b": "A", "color": "curve3"},
        ],
        "readouts": [
            {"id": "a", "label": "边 a = BC", "type": "expr", "expr": "2", "digits": 2},
            {"id": "b", "label": "边 b = AC", "type": "expr", "expr": "2*sqrt(3)", "digits": 2, "highlight": True},
            {"id": "c", "label": "边 c = AB", "type": "expr", "expr": "4", "digits": 2, "highlight": True},
        ],
        "legend": [{"color": "curve", "text": "边 a"}, {"color": "curve2", "text": "边 b"}, {"color": "curve3", "text": "边 c"}],
    }
    lesson = {
        "language": "zh-CN", "title": "正弦定理解三角形",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>三角形 $ABC$ 中，$a=2$，$A=30°$，$B=60°$，求边 $b$ 和 $c$。</p>"),
        "answerLabel": "b 和 c", "answer": f"$b={r['b_latex']}$，$c={r['c_latex']}$",
    }
    steps = [
        {"title": "求角 C",
         "content": f"<p>$C=\\pi-A-B=\\pi-30°-60°=90°$。</p>"},
        {"title": "正弦定理求 b",
         "content": f"<p>$\\dfrac{{a}}{{\\sin A}}=\\dfrac{{b}}{{\\sin B}}$，"
                    f"$b=\\dfrac{{a\\sin B}}{{\\sin A}}=\\dfrac{{2\\sin 60°}}{{\\sin 30°}}={r['b_latex']}$。</p>"},
        {"title": "正弦定理求 c",
         "content": f"<p>$c=\\dfrac{{a\\sin C}}{{\\sin A}}=\\dfrac{{2\\sin 90°}}{{\\sin 30°}}={r['c_latex']}$。</p>"
                    f"<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    f"$$ b={r['b_latex']},\\quad c={r['c_latex']} $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


# =====================================================================
# 3) 余弦定理：已知两边及夹角求第三边和面积
# =====================================================================
def build_cosine_law_problem() -> dict:
    """三角形 ABC，a=3，b=4，C=60°，求 c 和面积。"""
    r = K.cosine_law(3, 4, sp.pi / 3)

    board = {
        "view": {"xRange": [-1, 6], "yRange": [-1, 5]},
        "points": {
            "A": [0, 0], "B": [4, 0],
            "C": [f(3 * sp.cos(sp.pi / 3)), f(3 * sp.sin(sp.pi / 3))],
        },
        "derived": [
            {"type": "segment", "a": "A", "b": "B", "color": "curve"},
            {"type": "segment", "a": "B", "b": "C", "color": "curve2"},
            {"type": "segment", "a": "C", "b": "A", "color": "curve3"},
        ],
        "readouts": [
            {"id": "a", "label": "边 a = BC", "type": "expr", "expr": "3", "digits": 2},
            {"id": "b", "label": "边 b = AC = 4", "type": "expr", "expr": "4", "digits": 2},
            {"id": "c", "label": "边 c = AB", "type": "expr", "expr": "sqrt(13)", "digits": 4, "highlight": True},
            {"id": "area", "label": "面积 S", "type": "expr", "expr": "3*sqrt(3)", "digits": 4, "highlight": True},
        ],
        "legend": [{"color": "curve", "text": "边 a=3"}, {"color": "curve2", "text": "边 b=4"}, {"color": "curve3", "text": "边 c"}],
    }
    lesson = {
        "language": "zh-CN", "title": "余弦定理解三角形",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>三角形 $ABC$ 中，$a=3$，$b=4$，$C=60°$，求边 $c$ 和三角形面积。</p>"),
        "answerLabel": "c 和面积", "answer": f"$c={r['c_latex']}$，$S={r['area_latex']}$",
    }
    steps = [
        {"title": "余弦定理求 c",
         "content": f"<p>$c^2=a^2+b^2-2ab\\cos C=9+16-2\\cdot3\\cdot4\\cdot\\dfrac{{1}} {{2}}={r['c_latex']}^2$。</p>"
                    f"<p>$c={r['c_latex']}$。</p>"},
        {"title": "面积公式",
         "content": f"<p>$S=\\dfrac{{1}}{{2}}ab\\sin C=\\dfrac{{1}}{{2}}\\cdot3\\cdot4\\cdot\\dfrac{{\\sqrt{{3}}}}{{2}}={r['area_latex']}$。</p>"
                    f"<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    f"$$ c={r['c_latex']},\\quad S={r['area_latex']} $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {
    "sine_transform": build_sine_transform,
    "sine_law": build_sine_law_problem,
    "cosine_law": build_cosine_law_problem,
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
