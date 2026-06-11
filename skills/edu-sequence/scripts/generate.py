#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数列：注入 sequence.html 产出交互网页。"""
import json, sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "template" / "sequence.html"
PLACEHOLDER = "__LESSON_DATA__"

sys.path.insert(0, str(SKILL_DIR / "lib"))
import sympy as sp
import sequence_kernel as K


def render_html(data, out):
    t = TEMPLATE.read_text(encoding="utf-8")
    out.write_text(t.replace(PLACEHOLDER, json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    return out


def f(e):
    return float(sp.N(e))


def build_arithmetic() -> dict:
    """等差数列：首项 a1=1，公差 d=2，拖 n 看前 n 项。"""
    board = {
        "sequence": {"expr": "1 + (n-1)*2"},
        "param": {"name": "N", "label": "项数 $n$", "min": 2, "max": 20,
                  "step": 1, "value": 10, "unit": "", "standard": 10,
                  "ticks": ["2", "10", "20"]},
        "readouts": [
            {"id": "n", "label": "项数 n", "type": "expr", "expr": "N", "digits": 0},
            {"id": "an", "label": "第 n 项 a_n = 1+(n-1)·2", "type": "expr", "expr": "1+(N-1)*2", "digits": 0, "highlight": True},
            {"id": "sn", "label": "前 n 项和 S_n", "type": "expr", "expr": "N*(1+1+(N-1)*2)/2", "digits": 0, "highlight": True},
        ],
    }
    lesson = {
        "language": "zh-CN", "title": "等差数列",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>等差数列 $\\{a_n\\}$，首项 $a_1=1$，公差 $d=2$。求通项公式和前 $n$ 项和。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变项数 n，观察数列柱状图和累积和曲线。）</p>"),
        "answerLabel": "通项公式",
        "answer": "$a_n=2n-1$，$S_n=n^2$",
    }
    steps = [
        {"title": "通项公式",
         "content": "<p>$a_n=a_1+(n-1)d=1+(n-1)\\cdot 2=2n-1$</p>"},
        {"title": "前 n 项和",
         "content": "<p>$S_n=\\dfrac{n(a_1+a_n)}{2}=\\dfrac{n(1+2n-1)}{2}=n^2$</p>"
                    "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    "$$ a_n=2n-1,\\quad S_n=n^2 $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


def build_geometric() -> dict:
    """等比数列：首项 a1=1，公比 r=2，拖 n 看前 n 项。"""
    board = {
        "sequence": {"expr": "1 * 2^(n-1)"},
        "param": {"name": "N", "label": "项数 $n$", "min": 2, "max": 12,
                  "step": 1, "value": 6, "unit": "", "standard": 6,
                  "ticks": ["2", "6", "12"]},
        "readouts": [
            {"id": "n", "label": "项数 n", "type": "expr", "expr": "N", "digits": 0},
            {"id": "an", "label": "第 n 项 a_n = 2^(n-1)", "type": "expr", "expr": "2^(N-1)", "digits": 0, "highlight": True},
            {"id": "sn", "label": "前 n 项和 S_n = 2^n - 1", "type": "expr", "expr": "2^N-1", "digits": 0, "highlight": True},
        ],
    }
    lesson = {
        "language": "zh-CN", "title": "等比数列",
        "problem": ("<p class='font-medium text-slate-800'>【题目】</p>"
                    "<p>等比数列 $\\{a_n\\}$，首项 $a_1=1$，公比 $q=2$。求通项公式和前 $n$ 项和。</p>"
                    "<p class='text-slate-500 text-sm'>（拖动滑块改变项数 n，观察指数增长。）</p>"),
        "answerLabel": "通项公式",
        "answer": "$a_n=2^{n-1}$，$S_n=2^n-1$",
    }
    steps = [
        {"title": "通项公式",
         "content": "<p>$a_n=a_1\\cdot q^{n-1}=1\\cdot 2^{n-1}=2^{n-1}$</p>"},
        {"title": "前 n 项和",
         "content": "<p>$S_n=\\dfrac{a_1(1-q^n)}{1-q}=\\dfrac{1-2^n}{1-2}=2^n-1$</p>"
                    "<div class='text-center py-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-900 font-bold'>"
                    "$$ a_n=2^{n-1},\\quad S_n=2^n-1 $$</div>"},
    ]
    return {"lesson": lesson, "steps": steps, "board": board}


REGISTRY = {
    "arithmetic": build_arithmetic,
    "geometric": build_geometric,
}


def main(argv):
    if not argv or argv[0] == "list":
        print("registered:"); [print("  -", k) for k in REGISTRY]; return
    if argv[0] == "all":
        out_dir = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output")
        out_dir.mkdir(parents=True, exist_ok=True)
        for k, fn in REGISTRY.items():
            render_html(fn(), out_dir / f"{k}.html")
            print("written:", out_dir / f"{k}.html")
        return
    key = argv[0]
    if key not in REGISTRY:
        print(f"unknown: {key}"); sys.exit(1)
    out = Path(argv[1]) if len(argv) > 1 else (SKILL_DIR / "output" / f"{key}.html")
    render_html(REGISTRY[key](), out)
    print("written:", out)


if __name__ == "__main__":
    main(sys.argv[1:])
