#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""平面向量 sympy 精确求解核心。"""
import sympy as sp


def tex(e):
    return sp.latex(sp.nsimplify(sp.simplify(e)))


def fnum(e):
    return float(sp.N(e))


def dot_product(ax, ay, bx, by):
    """向量 (ax,ay)·(bx,by)。"""
    return sp.simplify(ax * bx + ay * by)


def cross_product(ax, ay, bx, by):
    """向量叉积的 z 分量（二维）。"""
    return sp.simplify(ax * by - ay * bx)


def vec_norm(ax, ay):
    """向量模长。"""
    return sp.simplify(sp.sqrt(ax**2 + ay**2))


def angle_cos(ax, ay, bx, by):
    """两向量夹角余弦。"""
    return sp.simplify(dot_product(ax, ay, bx, by) / (vec_norm(ax, ay) * vec_norm(bx, by)))


if __name__ == "__main__":
    d = dot_product(1, 2, 3, 4)
    print(f"1. (1,2)·(3,4) = {tex(d)}")
    c = angle_cos(1, 0, 0, 1)
    print(f"2. angle cos between (1,0) and (0,1) = {tex(c)}")
    print("\nall checks passed")
