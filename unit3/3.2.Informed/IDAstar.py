# idastar.py
from __future__ import annotations
import math
from typing import Any, Dict, Iterable, List, Optional, Tuple


def ida_star(
    graph: Dict[Any, Dict[Any, float]],
    start: Any,
    goal: Any,
    heuristics: Dict[Any, float],
    *,
    weight: float = 1.0,
    max_iterations: int = 1_000_000,
) -> Tuple[List[Any], float, Dict[str, Any]]:
    """
    Iterative Deepening A* (IDA*) on a weighted adjacency dict.
    f(n) = g(n) + weight * h(n), with non-negative edge costs.

    Returns: (path, cost, metrics) where metrics includes:
      'expansions', 'generated', 'iterations', 'max_frontier' (recursion depth proxy),
      'reopened' (0), 'path_len', 'algorithm'.
    """
    if weight <= 0:
        raise ValueError("weight must be > 0")

    def h(n: Any) -> float:
        return heuristics.get(n, 0.0)

    def path_cost(path: List[Any]) -> float:
        if len(path) < 2:
            return 0.0 if path else float("inf")
        total = 0.0
        for u, v in zip(path, path[1:]):
            total += graph[u][v]
        return total

    # Metrics
    expansions_total = 0
    generated_total = 1  # count start
    iterations = 0
    max_stack = 1  # recursion depth proxy
    reopened = 0   # not meaningful in IDA*, keep 0 for schema compatibility

    # Deterministic neighbor order
    def neighbors(u: Any) -> Iterable[Tuple[Any, float]]:
        return sorted(graph.get(u, {}).items())
    
    def search(node: Any, g: float, threshold: float, path: List[Any],
               best_g: Dict[Any, float], depth: int) -> Tuple[float, Optional[List[Any]], float]:
        """
        Depth-first search limited by 'threshold' on f = g + w*h.
        Returns (f_val, solution_path_or_None, min_excess).
        If solution found: (f_solution, path, +inf sentinel not used).
        Otherwise: (f_current, None, smallest f that exceeded threshold in this subtree).
        """
        nonlocal expansions_total, generated_total, max_stack

        f = g + weight * h(node)
        if f > threshold:
            return f, None, f

        if node == goal:
            return f, path.copy(), float("inf")

        # transposition pruning within this iteration
        prev = best_g.get(node, math.inf)
        if g >= prev:
            return f, None, float("inf")
        
        best_g[node] = g

        expansions_total += 1
        min_excess = math.inf

        # Generate children
        kids = []
        for v, cost in neighbors(node):
            if cost < 0:
                raise ValueError("Negative edge cost detected.")
            if v in path:
                continue
            kids.append((v, cost))
        generated_total += len(kids)

        if not kids:
            return f, None, math.inf

        # Explore children ordered by estimated f
        # Use local monotonicity trick: f_child = max(g_child + w*h(v), f)
        for v, cost in sorted(kids, key=lambda kv: g + kv[1] + weight * h(kv[0])):
            path.append(v)
            max_stack = max(max_stack, depth + 1)
            g_child = g + cost
            f_child = max(g_child + weight * h(v), f)
            if f_child <= threshold:
                f_res, found, excess = search(v, g_child, threshold, path, best_g, depth + 1)
                path.pop()
                if found is not None:
                    return f_res, found, math.inf
                if excess < min_excess:
                    min_excess = excess
            else:
                path.pop()
                if f_child < min_excess:
                    min_excess = f_child

        return f, None, min_excess

    # Initial threshold
    threshold = weight * h(start)
    path = [start]

    while True:
        if iterations >= max_iterations:
            return [], float("inf"), {
                "expansions": expansions_total,
                "generated": generated_total,
                "iterations": iterations,
                "max_frontier": max_stack,
                "reopened": reopened,
                "path_len": 0,
                "algorithm": f"IDA* (w={weight})",
            }

        iterations += 1
        best_g_this_iter: Dict[Any, float] = {}
        f_val, found_path, min_excess = search(start, 0.0, threshold, path, best_g_this_iter, depth=1)

        if found_path is not None:
            cost = path_cost(found_path)
            return found_path, cost, {
                "expansions": expansions_total,
                "generated": generated_total,
                "iterations": iterations,
                "max_frontier": max_stack,
                "reopened": reopened,
                "path_len": len(found_path),
                "algorithm": f"IDA* (w={weight})",
            }

        if min_excess == math.inf:
            # No path
            return [], float("inf"), {
                "expansions": expansions_total,
                "generated": generated_total,
                "iterations": iterations,
                "max_frontier": max_stack,
                "reopened": reopened,
                "path_len": 0,
                "algorithm": f"IDA* (w={weight})",
            }

        threshold = min_excess  # next bound
