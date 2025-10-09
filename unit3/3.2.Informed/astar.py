# astar.py
import heapq
import math
from typing import Any, Dict, List, Tuple

def a_star_search(graph: Dict[Any, Dict[Any, float]],
                  start: Any,
                  goal: Any,
                  heuristics: Dict[Any, float]) -> Tuple[List[Any], float, Dict[str, Any]]:
    """
    A* graph search with benchmarking-friendly return.
    Returns: (path, cost, metrics)
      - path: list of nodes from start to goal (empty if no path)
      - cost: total path cost (float('inf') if no path)
      - metrics: {
            'expansions': int,
            'generated': int,
            'max_frontier': int,
            'reopened': int,
            'path_len': int,
            'algorithm': 'A*'
        }
    """

    # --- Data structures ---
    frontier: List[Tuple[float, int, Any]] = []  # (f, tie, node)
    came_from: Dict[Any, Any] = {}               # best parent
    g: Dict[Any, float] = {start: 0.0}           # best g so far
    closed: set = set()                          # expanded nodes
    counter = 0                                   # tie-breaker

    # --- Metrics ---
    expansions = 0
    generated = 0
    max_frontier = 0
    reopened = 0

    # push start
    h0 = heuristics.get(start, 0.0)
    heapq.heappush(frontier, (g[start] + h0, counter, start))
    generated += 1
    max_frontier = max(max_frontier, len(frontier))

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f_val, _, node = heapq.heappop(frontier)

        if node in closed:
            # stale entry
            continue

        # expand
        closed.add(node)
        expansions += 1

        if node == goal:
            path = _reconstruct_path(came_from, node)
            cost = g[node]
            return path, cost, {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier,
                "reopened": reopened,
                "path_len": len(path),
                "algorithm": "A*",
            }

        # deterministic neighbor order
        for nbr in sorted(graph.get(node, {}).keys()):
            step = graph[node][nbr]
            tentative_g = g[node] + step

            # found a better path to nbr
            if tentative_g < g.get(nbr, math.inf):
                came_from[nbr] = node
                g[nbr] = tentative_g
                counter += 1
                f_n = tentative_g + heuristics.get(nbr, 0.0)
                heapq.heappush(frontier, (f_n, counter, nbr))
                generated += 1

                # if we had already closed nbr, we are effectively reopening it
                if nbr in closed:
                    reopened += 1
                    # allow reconsideration by leaving the stale closed mark;
                    # we'll skip stale pops but accept the new better entry

    # no path
    return [], float("inf"), {
        "expansions": expansions,
        "generated": generated,
        "max_frontier": max_frontier,
        "reopened": reopened,
        "path_len": 0,
        "algorithm": "A*",
    }


# ---------- helpers ----------

def _reconstruct_path(parent: Dict[Any, Any], goal: Any) -> List[Any]:
    path = [goal]
    cur = goal
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path
