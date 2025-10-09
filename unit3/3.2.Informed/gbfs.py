# gbfs.py
import heapq
from typing import Any, Dict, List, Tuple

def greedy_best_first_search(
    graph: Dict[Any, Dict[Any, float]],
    start: Any,
    goal: Any,
    heuristics: Dict[Any, float],
) -> Tuple[List[Any], float, Dict[str, Any]]:
    """
    Greedy Best-First Search (graph search).
    Priority = h(n). Not optimal in general.

    Returns: (path, cost, metrics) with:
      metrics = {
        'expansions': int, 'generated': int, 'max_frontier': int,
        'reopened': 0, 'path_len': int, 'algorithm': 'Greedy Best-First'
      }
    """

    # Priority queue: (h(n), tie, node)
    frontier: List[Tuple[float, int, Any]] = []
    tie = 0
    heapq.heappush(frontier, (heuristics.get(start, 0.0), tie, start))

    came_from: Dict[Any, Any] = {start: None}
    visited = set()

    # Metrics
    expansions = 0
    generated = 1  # start counted as generated
    max_frontier = len(frontier)

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        _, _, node = heapq.heappop(frontier)

        if node in visited:
            continue
        visited.add(node)
        expansions += 1

        if node == goal:
            path = _reconstruct_path(came_from, node)
            cost = _path_cost(graph, path)
            return path, cost, {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier,
                "reopened": 0,
                "path_len": len(path),
                "algorithm": "Greedy Best-First",
            }

        # Deterministic neighbor order
        for nbr in sorted(graph.get(node, {}).keys()):
            if nbr in visited or nbr in came_from:
                continue
            came_from[nbr] = node
            tie += 1
            heapq.heappush(frontier, (heuristics.get(nbr, 0.0), tie, nbr))
            generated += 1

    # No path
    return [], float("inf"), {
        "expansions": expansions,
        "generated": generated,
        "max_frontier": max_frontier,
        "reopened": 0,
        "path_len": 0,
        "algorithm": "Greedy Best-First",
    }

# --- helpers ---

def _reconstruct_path(parent: Dict[Any, Any], goal: Any) -> List[Any]:
    path = [goal]
    cur = goal
    while cur in parent and parent[cur] is not None:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path if path and parent.get(path[0], None) is None else path  # start included

def _path_cost(graph: Dict[Any, Dict[Any, float]], path: List[Any]) -> float:
    if len(path) < 2:
        return 0.0 if path else float("inf")
    total = 0.0
    for u, v in zip(path, path[1:]):
        total += graph[u][v]
    return total
