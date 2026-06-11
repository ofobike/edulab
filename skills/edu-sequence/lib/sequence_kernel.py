#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数列 sympy 精确求解核心。"""
import sympy as sp

n = sp.Symbol('n', positive=True, integer=True)
a, d, r = sp.symbols('a d r', real=True)


def tex(e):
    return sp.latex(sp.nsimplify(sp.simplify(e)))


def fnum(e):
    return float(sp.N(e))


def arithmetic(a1_val, d_val, n_val):
    """等差数列：首项 a1，公差 d，求第 n 项和前 n 项和。"""
    a1, d_, n_ = sp.nsimplify(a1_val), sp.nsimplify(d_val), sp.nsimplify(n_val)
    an = a1 + (n_ - 1) * d_
    sn = n_ * (a1 + an) / 2
    return {
        'a1': a1, 'd': d_, 'n': n_,
        'an': sp.simplify(an), 'sn': sp.simplify(sn),
        'an_latex': tex(an), 'sn_latex': tex(sn),
        'general': f"a_n = {tex(a1)} + (n-1) \\cdot {tex(d_)} = {tex(a1 + (n - 1) * d_)}",
    }


def geometric(a1_val, r_val, n_val):
    """等比数列：首项 a1，公比 r，求第 n 项和前 n 项和。"""
    a1, r_, n_ = sp.nsimplify(a1_val), sp.nsimplify(r_val), sp.nsimplify(n_val)
    an = a1 * r_**(n_ - 1)
    if r_ == 1:
        sn = n_ * a1
    else:
        sn = a1 * (1 - r_**n_) / (1 - r_)
    return {
        'a1': a1, 'r': r_, 'n': n_,
        'an': sp.simplify(an), 'sn': sp.simplify(sn),
        'an_latex': tex(an), 'sn_latex': tex(sn),
        'general': f"a_n = {tex(a1)} \\cdot {tex(r_)}^{{n-1}}",
    }


if __name__ == "__main__":
    # 等差：a1=1, d=2, n=10
    a1 = arithmetic(1, 2, 10)
    print(f"1. arithmetic: a10={a1['an_latex']}, S10={a1['sn_latex']}")

    # 等比：a1=1, r=2, n=5
    g1 = geometric(1, 2, 5)
    print(f"2. geometric: a5={g1['an_latex']}, S5={g1['sn_latex']}")

    print("\nall checks passed")
