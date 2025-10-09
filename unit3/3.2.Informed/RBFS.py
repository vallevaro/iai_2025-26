from __future__ import annotations
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Tuple
import math
import os, sys



Node = Hashable
NeighborsFn = Callable[[Node], Iterable[Tuple[Node, float]]]
HeuristicFn = Callable[[Node], float]


class RBFSResult:
    def __init__(self, path: Optional[List[Node]], cost: float, expanded: int):
        self.path = path
        self.cost = cost
        self.expanded = expanded

    def __repr__(self) -> str:
        return f"RBFSResult(path={self.path}, cost={self.cost}, expanded={self.expanded})"


def dict_neighbors(graph: Dict[Node, Dict[Node, float]]) -> NeighborsFn:
    def _n(u: Node) -> Iterable[Tuple[Node, float]]:
        return graph.get(u, {}).items()
    return _n


def rbfs(
    start: Node,
    goal: Node,
    neighbors: NeighborsFn,
    h: HeuristicFn,
    *,
    weight: float = 1.0,
) -> RBFSResult:
    """
    Recursive Best-First Search (Korf, 1993) con f-limit y heurística ponderada.
    Admite grafos con costes no negativos.

    Devuelve RBFSResult(path, cost, expanded). Si no hay solución: path=None, cost=inf.
    """
    assert weight > 0, "weight must be > 0"
    expanded = 0

    def reconstruct_cost(path: List[Node]) -> float:
        total = 0.0
        for a, b in zip(path, path[1:]):
            found = False
            for nb, c in neighbors(a):
                if nb == b:
                    total += c
                    found = True
                    break
            if not found:
                raise RuntimeError("Inconsistent neighbors during cost reconstruction.")
        return total

    def rbfs_rec(
        current: Node,
        g: float,
        path: List[Node],
        f_limit: float,
        best_g: Dict[Node, float],
    ) -> Tuple[Optional[List[Node]], float, float]:
        """
        Devuelve (solution_path or None, solution_f or inf, new_f_limit)
        new_f_limit es el mejor límite alternativo (el segundo mejor f) que “burbujea”.
        """
        nonlocal expanded
        f_current = g + weight * h(current)

        if f_current > f_limit:
            return None, f_current, f_current  # sobrepasa el límite

        if current == goal:
            return path.copy(), f_current, f_current

        # Poda transposicional simple por iteración de rama: si llegamos con peor g, corta.
        prev_best = best_g.get(current, math.inf)
        if g >= prev_best:
            return None, math.inf, math.inf
        best_g[current] = g

        # Genera hijos
        children: List[Tuple[Node, float, float]] = []  # (child, g_child, f_child)
        expanded += 1

        for v, cost in neighbors(current):
            if cost < 0:
                raise ValueError("Negative edge cost detected; RBFS requires non-negative costs.")
            if v in path:
                continue  # evita ciclos en el camino actual
            g_child = g + cost
            f_child = max(g_child + weight * h(v), f_current)  # mantener monotonicidad local
            children.append((v, g_child, f_child))

        if not children:
            return None, math.inf, math.inf

        # Bucle: siempre expandir el hijo con menor f, actualizando su límite al segundo mejor
        while True:
            children.sort(key=lambda x: x[2])
            best = children[0]
            best_f = best[2]
            # Si la mejor opción ya excede el límite, no hay solución bajo este límite
            if best_f > f_limit:
                return None, best_f, best_f

            # Segundo mejor f (o +inf si no hay)
            alt_f = children[1][2] if len(children) > 1 else math.inf

            v, g_child, f_child = best
            path.append(v)
            sol, sol_f, new_f = rbfs_rec(v, g_child, path, min(f_limit, alt_f), best_g)
            path.pop()

            if sol is not None:
                return sol, sol_f, new_f

            # No hubo solución por esa rama: actualiza la f del hijo con el nuevo límite 
            # y continúa con el siguiente mejor
            children[0] = (v, g_child, new_f)

    initial_limit = weight * h(start)
    solution, sol_f, _ = rbfs_rec(start, 0.0, [start], initial_limit, best_g={})

    if solution is None:
        return RBFSResult(None, float("inf"), expanded)
    return RBFSResult(solution, reconstruct_cost(solution), expanded)



if __name__ == "__main__":

    from datagraph2 import graph, h_values  
    neighbors = dict_neighbors(graph)
    start, goal = "A", "E"
    result = rbfs(start, goal, neighbors, lambda n: h_values.get(n, math.inf))
    print(result)
