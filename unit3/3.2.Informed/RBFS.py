# rbfstar.py  (RBFS for benchmarking)
from __future__ import annotations
import math
from typing import Any, Dict, Iterable, List, Optional, Tuple

def recursive_best_first_search(
    graph: Dict[Any, Dict[Any, float]],
    start: Any,
    goal: Any,
    heuristics: Dict[Any, float],
    weight: float = 1.0,
) -> Tuple[List[Any], float, Dict[str, Any]]:
    """
    RBFS (Korf, 1993) with weighted heuristic: f(n) = g(n) + weight * h(n).
    Returns: (path, cost, metrics) where metrics matches the benchmarking schema.
    Requirements: non-negative edge costs.
    """

    if weight <= 0:
        raise ValueError("weight must be > 0 for RBFS.")

    # ---- metrics ----
    expansions = 0
    generated = 1   # count start
    max_stack = 1   # recursion depth proxy (memory)
    # RBFS has no explicit frontier structure; 'reopened' not meaningful here.
    reopened = 0

    def h(n: Any) -> float:
        return heuristics.get(n, 0.0)

    def reconstruct_cost(path: List[Any]) -> float:
        if len(path) < 2:
            return 0.0 if path else float("inf")
        total = 0.0
        for u, v in zip(path, path[1:]):
            total += graph[u][v]
        return total

    # Transposition guard: best g seen so far per node (within a branch)
    best_g: Dict[Any, float] = {}

    def rbfs_rec(
        current: Any,
        g_val: float,
        path: List[Any],
        f_limit: float,
    ) -> Tuple[Optional[List[Any]], float]:
        """
        Returns (solution_path or None, best_alternative_f).
        best_alternative_f is the next best f-cost bound to bubble up.
        """
        nonlocal expansions, generated, max_stack

        f_current = g_val + weight * h(current)
        if f_current > f_limit:
            return None, f_current

        if current == goal:
            return path.copy(), f_current

        # Simple transposition pruning: if we reach with worse g, cut
        prev = best_g.get(current, math.inf)
        if g_val >= prev:
            return None, math.inf
        best_g[current] = g_val

        # Generate children (deterministic order)
        children: List[Tuple[Any, float, float]] = []  # (child, g_child, f_child)
        expansions += 1
        nbrs = sorted(graph.get(current, {}).items())  # sort by neighbor id
        for v, cost in nbrs:
            if cost < 0:
                raise ValueError("Negative edge cost detected.")
            if v in path:
                continue  # avoid cycles on current path
            g_child = g_val + cost
            f_child = max(g_child + weight * h(v), f_current)  # local monotonicity
            children.append((v, g_child, f_child))

        if not children:
            return None, math.inf

        # Track generated nodes (children newly considered)
        generated += len(children)
        # Update memory proxy (recursion depth)
        max_stack = max(max_stack, len(path) + 1)

        # Main loop: expand best child under an adaptive bound
        while True:
            children.sort(key=lambda t: t[2])  # by f_child
            best_child, g_best, f_best = children[0]
            if f_best > f_limit:
                return None, f_best

            alt = children[1][2] if len(children) > 1 else math.inf

            path.append(best_child)
            sol, new_f = rbfs_rec(best_child, g_best, path, min(f_limit, alt))
            path.pop()

            if sol is not None:
                return sol, new_f

            # No solution via best child: raise its f to the returned alternative and continue
            children[0] = (best_child, g_best, new_f)

    initial_limit = weight * h(start)
    solution, _ = rbfs_rec(start, 0.0, [start], initial_limit)

    if solution is None:
        return [], float("inf"), {
            "expansions": expansions,
            "generated": generated,
            "max_frontier": max_stack,  # expose stack as frontier proxy
            "reopened": reopened,
            "path_len": 0,
            "algorithm": f"RBFS (w={weight})",
        }

    cost = reconstruct_cost(solution)
    return solution, cost, {
        "expansions": expansions,
        "generated": generated,
        "max_frontier": max_stack,
        "reopened": reopened,
        "path_len": len(solution),
        "algorithm": f"RBFS (w={weight})",
    }
