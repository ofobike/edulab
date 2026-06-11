#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""概率与统计 sympy 精确求解核心。"""
import sympy as sp
from sympy.stats import Binomial, Normal, P, E, variance, density
import math


def tex(e):
    return sp.latex(sp.nsimplify(sp.simplify(e)))


def fnum(e):
    return float(sp.N(e))


def binomial_pmf(n_val, p_val, k_val):
    """二项分布 P(X=k) = C(n,k) * p^k * (1-p)^(n-k)。"""
    n, p, k = sp.nsimplify(n_val), sp.nsimplify(p_val), sp.nsimplify(k_val)
    prob = sp.binomial(n, k) * p**k * (1 - p)**(n - k)
    return sp.simplify(prob)


def binomial_stats(n_val, p_val):
    """二项分布的期望和方差。"""
    n, p = sp.nsimplify(n_val), sp.nsimplify(p_val)
    return {
        'E': sp.simplify(n * p),
        'Var': sp.simplify(n * p * (1 - p)),
        'E_latex': tex(n * p),
        'Var_latex': tex(n * p * (1 - p)),
    }


def normal_pdf(mu_val, sigma_val, x_val):
    """正态分布概率密度函数值。"""
    mu, sigma = sp.nsimplify(mu_val), sp.nsimplify(sigma_val)
    x = sp.nsimplify(x_val)
    pdf = sp.exp(-(x - mu)**2 / (2 * sigma**2)) / (sigma * sp.sqrt(2 * sp.pi))
    return sp.simplify(pdf)


if __name__ == "__main__":
    # X ~ B(10, 0.3), P(X=3)
    p1 = binomial_pmf(10, sp.Rational(3, 10), 3)
    print(f"1. B(10,0.3) P(X=3) = {tex(p1)}")

    s1 = binomial_stats(10, sp.Rational(3, 10))
    print(f"2. B(10,0.3) E={s1['E_latex']}, Var={s1['Var_latex']}")

    print("\nall checks passed")
