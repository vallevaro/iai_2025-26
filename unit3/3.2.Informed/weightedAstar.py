# weightedAstar.py
import heapq
import math
from typing import Any, Dict, List, Tuple

def weighted_a_star_search(
    graph: Dict[Any, Dict[Any, float]],
    start: Any,
    goal: Any,
    heuristics: Dict[Any, float],
    weight: float = 1.0,
) -> Tuple[List[Any], float, Dict[str, Any]]:
    """
    Weighted A* (graph search). f(n) = g(n) + w * h(n), with w >= 1.
    Returns: (path, cost, metrics)
      metrics = {
        'expansions': int, 'generated': int, 'max_frontier': int,
        'reopened': int, 'path_len': int, 'algorithm': f'Weighted A* (w={weight})'
      }
    """
    if weight < 1.0:
        raise ValueError("weight must be >= 1.0 for Weighted A*.")

    # --- structures ---
    frontier: List[Tuple[float, int, Any]] = []  # (f, tie, node)
    came_from: Dict[Any, Any] = {}
    g: Dict[Any, float] = {start: 0.0}
    closed = set()
    tie = 0

    # --- metrics ---
    expansions = 0
    generated = 0
    max_frontier = 0
    reopened = 0

    # push start
    f0 = g[start] + weight * heuristics.get(start, 0.0)
    heapq.heappush(frontier, (f0, tie, start))
    generated += 1
    max_frontier = max(max_frontier, len(frontier))

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        _, _, node = heapq.heappop(frontier)

        if node in closed:
            continue

        closed.add(node)
        expansions += 1

        if node == goal:
            path = _reconstruct_path(came_from, node)
            return path, g[node], {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier,
                "reopened": reopened,
                "path_len": len(path),
                "algorithm": f"Weighted A* (w={weight})",
            }

        # deterministic neighbor order
        for nbr in sorted(graph.get(node, {}).keys()):
            step = graph[node][nbr]
            tentative_g = g[node] + step

            if tentative_g < g.get(nbr, math.inf):
                came_from[nbr] = node
                g[nbr] = tentative_g
                tie += 1
                f_n = tentative_g + weight * heuristics.get(nbr, 0.0)
                heapq.heappush(frontier, (f_n, tie, nbr))
                generated += 1
                if nbr in closed:
                    reopened += 1  # better path discovered after close

    # no path
    return [], float("inf"), {
        "expansions": expansions,
        "generated": generated,
        "max_frontier": max_frontier,
        "reopened": reopened,
        "path_len": 0,
        "algorithm": f"Weighted A* (w={weight})",
    }

# --- helpers ---

def _reconstruct_path(parent: Dict[Any, Any], goal: Any) -> List[Any]:
    path = [goal]
    cur = goal
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path
