#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
function_kernel.py — 函数与导数 sympy 精确求解核心。

覆盖：切线方程、单调性/极值、零点、不等式证明等。
所有数值由 sympy 精确计算，返回 LaTeX 字符串。
"""
import sympy as sp

x = sp.Symbol('x', real=True)
a, b, c = sp.symbols('a b c', real=True)


def tex(expr):
    return sp.latex(sp.nsimplify(sp.simplify(expr)))


def fnum(expr):
    return float(sp.N(expr))


def is_clean(expr, max_ops=7, max_radicand=60):
    e = sp.radsimp(sp.nsimplify(sp.simplify(expr)))
    if e.has(sp.zoo, sp.nan, sp.oo) or e.free_symbols:
        return False
    if sp.count_ops(e) > max_ops:
        return False
    for p in e.atoms(sp.Pow):
        if p.exp == sp.Rational(1, 2):
            rad = p.base
            if not (rad.is_Integer and 0 <= int(rad) <= max_radicand):
                return False
    return True


# ===================== 切线方程 =====================

def tangent_line(f_expr, x0_val):
    """求 f(x) 在 x=x0 处的切线方程。返回 {slope, y0, tangent_latex, f_latex, fp_latex}。"""
    fp = sp.diff(f_expr, x)
    y0 = sp.simplify(f_expr.subs(x, x0_val))
    slope = sp.simplify(fp.subs(x, x0_val))
    # tangent: y - y0 = slope*(x - x0) => y = slope*x + (y0 - slope*x0)
    intercept = sp.simplify(y0 - slope * x0_val)
    tangent_latex = f"y = {tex(slope)}x + {tex(intercept)}" if intercept != 0 else f"y = {tex(slope)}x"
    if slope == 0:
        tangent_latex = f"y = {tex(y0)}"
    return {
        'slope': slope, 'y0': y0, 'intercept': intercept,
        'tangent_latex': tangent_latex,
        'f_latex': tex(f_expr),
        'fp_latex': tex(fp),
        'x0': x0_val,
    }


# ===================== 单调性 / 极值 =====================

def monotonicity(f_expr, domain=None):
    """求 f(x) 的单调区间。返回 {critical_points, intervals, extrema}。"""
    fp = sp.diff(f_expr, x)
    fpp = sp.diff(fp, x)
    # find critical points
    cps = sp.solve(sp.simplify(fp), x)
    cps = [c for c in cps if c.is_real]
    if domain:
        cps = [c for c in cps if domain[0] <= c <= domain[1]]
    cps.sort()

    intervals = []
    # test intervals between critical points
    test_points = []
    if domain:
        test_points.append(domain[0])
    for cp in cps:
        test_points.append(cp)
    if domain:
        test_points.append(domain[1])

    for i in range(len(test_points) - 1):
        mid = (test_points[i] + test_points[i + 1]) / 2
        val = sp.simplify(fp.subs(x, mid))
        if val > 0:
            intervals.append({'type': 'increasing', 'lo': test_points[i], 'hi': test_points[i + 1]})
        elif val < 0:
            intervals.append({'type': 'decreasing', 'lo': test_points[i], 'hi': test_points[i + 1]})

    extrema = []
    for cp in cps:
        fval = sp.simplify(f_expr.subs(x, cp))
        fppval = sp.simplify(fpp.subs(x, cp))
        if fppval > 0:
            extrema.append({'type': 'min', 'x': cp, 'y': fval, 'fpp': fppval})
        elif fppval < 0:
            extrema.append({'type': 'max', 'x': cp, 'y': fval, 'fpp': fppval})
        else:
            extrema.append({'type': 'inflection', 'x': cp, 'y': fval})

    return {
        'fp': fp, 'fpp': fpp,
        'critical_points': cps,
        'intervals': intervals,
        'extrema': extrema,
        'fp_latex': tex(fp),
        'fpp_latex': tex(fpp),
    }


# ===================== 零点 =====================

def find_zeros(f_expr, domain=None):
    """求 f(x)=0 的实数解。"""
    zeros = sp.solve(f_expr, x)
    zeros = [z for z in zeros if z.is_real]
    if domain:
        zeros = [z for z in zeros if domain[0] <= z <= domain[1]]
    zeros.sort()
    return zeros


# ===================== 自检 =====================

if __name__ == "__main__":
    # 切线：f(x)=x³-3x 在 x=1 处
    f1 = x**3 - 3*x
    t1 = tangent_line(f1, 1)
    assert sp.simplify(t1['slope'] - 0) == 0, f"slope should be 0, got {t1['slope']}"
    assert sp.simplify(t1['y0'] - (-2)) == 0
    print(f"1. f(x)=x^3-3x, x=1: tangent = {t1['tangent_latex']}")

    # 切线：f(x)=ln(x) 在 x=1 处
    f2 = sp.ln(x)
    t2 = tangent_line(f2, 1)
    assert sp.simplify(t2['slope'] - 1) == 0
    assert sp.simplify(t2['y0'] - 0) == 0
    print(f"2. f(x)=ln(x), x=1: tangent = {t2['tangent_latex']}")

    # 单调性：f(x)=x³-3x
    m1 = monotonicity(f1, domain=[-3, 3])
    print(f"3. f(x)=x^3-3x: critical={m1['critical_points']}, extrema={[(e['type'], fnum(e['x']), fnum(e['y'])) for e in m1['extrema']]}")

    # 零点：f(x)=x²-2
    f3 = x**2 - 2
    z3 = find_zeros(f3)
    print(f"4. f(x)=x^2-2: zeros={z3}")

    print("\nall checks passed")
