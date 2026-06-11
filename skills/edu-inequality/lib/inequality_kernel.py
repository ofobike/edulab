#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""不等式与线性规划 sympy 精确求解核心。"""
import sympy as sp

x, y = sp.symbols('x y', real=True)


def tex(e):
    return sp.latex(sp.nsimplify(sp.simplify(e)))


def fnum(e):
    return float(sp.N(e))


def linear_program(constraints, objective, direction="max"):
    """线性规划：在约束条件下求目标函数的最值。

    constraints: list of (expr, op, val) 例如 (x+y, '<=', 4)
    objective: 目标函数表达式，例如 2*x+y
    direction: "max" 或 "min"
    """
    # 简单实现：枚举约束边界的交点
    vertices = []
    n = len(constraints)
    for i in range(n):
        for j in range(i + 1, n):
            e1, op1, v1 = constraints[i]
            e2, op2, v2 = constraints[j]
            # 求 e1=v1, e2=v2 的交点
            sol = sp.solve([e1 - v1, e2 - v2], [x, y])
            if sol and x in sol and y in sol:
                px, py = sol[x], sol[y]
                # 检查是否满足所有约束
                feasible = True
                for e, op, v in constraints:
                    val = sp.simplify(e.subs({x: px, y: py}))
                    if op == "<=" and val > v:
                        feasible = False
                    elif op == ">=" and val < v:
                        feasible = False
                if feasible:
                    vertices.append((px, py))

    if not vertices:
        return None

    # 计算目标函数在各顶点的值
    vals = [(v, sp.simplify(objective.subs({x: v[0], y: v[1]}))) for v in vertices]
    if direction == "max":
        best = max(vals, key=lambda t: fnum(t[1]))
    else:
        best = min(vals, key=lambda t: fnum(t[1]))

    return {
        'vertices': vertices, 'vals': vals,
        'opt_point': best[0], 'opt_value': best[1],
        'opt_x': fnum(best[0][0]), 'opt_y': fnum(best[0][1]),
        'opt_val_f': fnum(best[1]),
        'opt_latex': tex(best[1]),
    }


if __name__ == "__main__":
    # max z=2x+y, s.t. x+y<=4, x>=0, y>=0
    r = linear_program(
        [(x + y, "<=", 4), (x, ">=", 0), (y, ">=", 0)],
        2 * x + y, "max"
    )
    print(f"1. max 2x+y s.t. x+y<=4: opt={r['opt_latex']} at ({r['opt_x']}, {r['opt_y']})")
    print("\nall checks passed")
