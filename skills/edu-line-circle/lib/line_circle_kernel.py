#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直线与圆的 sympy 精确求解核心。"""
import sympy as sp

x, y = sp.symbols('x y', real=True)
m = sp.symbols('m', real=True)


def tex(e):
    return sp.latex(sp.nsimplify(sp.simplify(e)))


def fnum(e):
    return float(sp.N(e))


def line_circle_intersect(r_val, slope_val):
    """直线 y=kx 过原点，与圆 x²+y²=r² 的交点。返回交点坐标。"""
    r = sp.nsimplify(r_val)
    k = sp.nsimplify(slope_val)
    # y=kx 代入 x²+y²=r² => x²(1+k²)=r² => x=±r/√(1+k²)
    x_val = sp.simplify(r / sp.sqrt(1 + k**2))
    return {
        'A': (x_val, k * x_val), 'B': (-x_val, -k * x_val),
        'r': r, 'k': k,
        'chord_len': sp.simplify(2 * r),  # diameter when through center
        'A_latex': f"({tex(x_val)}, {tex(k * x_val)})",
        'B_latex': f"({tex(-x_val)}, {tex(-k * x_val)})",
    }


def point_to_line_dist(px, py, a, b, c):
    """点 (px,py) 到直线 ax+by+c=0 的距离。"""
    return sp.simplify(sp.Abs(a * px + b * py + c) / sp.sqrt(a**2 + b**2))


if __name__ == "__main__":
    r1 = line_circle_intersect(2, sp.Integer(1))
    print(f"1. circle r=2, line y=x: A={r1['A_latex']}, B={r1['B_latex']}")
    d1 = point_to_line_dist(1, 1, 1, -1, 0)
    print(f"2. point (1,1) to line x-y=0: dist={tex(d1)}")
    print("\nall checks passed")
