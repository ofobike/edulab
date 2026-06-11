#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trig_kernel.py — 三角函数与解三角形 sympy 精确求解核心。
"""
import sympy as sp

x = sp.Symbol('x', real=True)
A, w, phi, k = sp.symbols('A omega phi k', real=True)


def tex(expr):
    return sp.latex(sp.nsimplify(sp.simplify(expr)))


def fnum(expr):
    return float(sp.N(expr))


# ===================== 三角函数图像变换 =====================

def sine_transform(A_val=1, omega_val=1, phi_val=0, k_val=0):
    """y = A*sin(omega*x + phi) + k。返回各参数 LaTeX 和关键量。"""
    A_, w_, p_, k_ = sp.nsimplify(A_val), sp.nsimplify(omega_val), sp.nsimplify(phi_val), sp.nsimplify(k_val)
    period = sp.simplify(2 * sp.pi / w_)
    # 五点法关键 x 值：omega*x + phi = 0, pi/2, pi, 3pi/2, 2pi
    key_xs = [(sp.Integer(0) - p_) / w_, (sp.pi / 2 - p_) / w_, (sp.pi - p_) / w_,
              (3 * sp.pi / 2 - p_) / w_, (2 * sp.pi - p_) / w_]
    key_ys = [k_, A_ + k_, k_, -A_ + k_, k_]

    return {
        'A': A_, 'omega': w_, 'phi': p_, 'k': k_,
        'period': period,
        'amplitude': sp.Abs(A_),
        'key_xs': key_xs, 'key_ys': key_ys,
        'A_latex': tex(A_), 'omega_latex': tex(w_), 'phi_latex': tex(p_), 'k_latex': tex(k_),
        'period_latex': tex(period),
        'expr_latex': f"{tex(A_)}\\sin({tex(w_)}x+{tex(p_)})+{tex(k_)}",
    }


# ===================== 正弦定理 / 余弦定理 =====================

def sine_law(a_val, A_val, B_val):
    """已知 a, A, B，用正弦定理求 b。a/sinA = b/sinB。"""
    a_, A_, B_ = sp.nsimplify(a_val), sp.nsimplify(A_val), sp.nsimplify(B_val)
    C_ = sp.pi - A_ - B_
    b_ = sp.simplify(a_ * sp.sin(B_) / sp.sin(A_))
    c_ = sp.simplify(a_ * sp.sin(C_) / sp.sin(A_))
    return {
        'a': a_, 'A': A_, 'B': B_, 'C': C_,
        'b': b_, 'c': c_,
        'a_latex': tex(a_), 'b_latex': tex(b_), 'c_latex': tex(c_),
        'A_latex': tex(A_), 'B_latex': tex(B_), 'C_latex': tex(C_),
    }


def cosine_law(a_val, b_val, C_val):
    """已知 a, b, C，用余弦定理求 c。c²=a²+b²-2ab·cosC。"""
    a_, b_, C_ = sp.nsimplify(a_val), sp.nsimplify(b_val), sp.nsimplify(C_val)
    c_sq = sp.simplify(a_**2 + b_**2 - 2 * a_ * b_ * sp.cos(C_))
    c_ = sp.simplify(sp.sqrt(c_sq))
    area = sp.simplify(sp.Rational(1, 2) * a_ * b_ * sp.sin(C_))
    return {
        'a': a_, 'b': b_, 'C': C_, 'c': c_, 'c_sq': c_sq, 'area': area,
        'a_latex': tex(a_), 'b_latex': tex(b_), 'c_latex': tex(c_),
        'C_latex': tex(C_), 'area_latex': tex(area),
    }


# ===================== 自检 =====================

if __name__ == "__main__":
    # y = 2*sin(2x + pi/6) + 1
    t1 = sine_transform(2, 2, sp.pi / 6, 1)
    print(f"1. y = {t1['expr_latex']}, period = {t1['period_latex']}")

    # 正弦定理：a=2, A=30°, B=60°
    s1 = sine_law(2, sp.pi / 6, sp.pi / 3)
    print(f"2. sine law: a={s1['a_latex']}, b={s1['b_latex']}, c={s1['c_latex']}")

    # 余弦定理：a=3, b=4, C=90°
    c1 = cosine_law(3, 4, sp.pi / 2)
    print(f"3. cosine law: c={c1['c_latex']}, area={c1['area_latex']}")

    print("\nall checks passed")
