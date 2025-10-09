
import heapq
import time
import tracemalloc
from typing import Dict, Tuple, List, Optional, Any

from gbfs

def measure(func):
    """Decorator to measure time, memory (peak), and collect metrics dict from search functions."""
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # result is (path, cost, metrics)
        path, cost, metrics = result
        metrics = dict(metrics) if metrics else {}
        metrics.update({
            "time_sec": t1 - t0,
            "peak_mem_kb": peak / 1024.0,
        })
        return path, cost, metrics
    return wrapper


# ==========
# Algorithms
# ==========

@measure
def ucs(graph: Dict[Any, Dict[Any, float]], start: Any, goal: Any):
    """Uniform Cost Search (Graph search)."""
    frontier = []
    counter = 0  # tie-breaker
    heapq.heappush(frontier, (0.0, counter, start))
    parent = {start: None}
    g = {start: 0.0}
    closed = set()

    # Metrics
    expansions = 0
    generated = 1  # start is "generated"
    max_frontier = len(frontier)
    reopened = 0

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f_cost, _, node = heapq.heappop(frontier)

        if node in closed:
            # stale entry
            continue

        closed.add(node)
        expansions += 1

        if node == goal:
            path = reconstruct_path(parent, goal)
            metrics = {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier,
                "reopened": reopened,
                "path_len": len(path),
                "algorithm": "UCS",
            }
            return path, g[node], metrics

        # Expand neighbors in deterministic order
        for nbr in sorted(graph.get(node, {}).keys()):
            w = graph[node][nbr]
            tentative = g[node] + w
            if nbr not in g or tentative < g[nbr]:
                parent[nbr] = node
                g[nbr] = tentative
                counter += 1
                heapq.heappush(frontier, (tentative, counter, nbr))
                generated += 1
                if nbr in closed:
                    reopened += 1

    return [], float("inf"), {
        "expansions": expansions, "generated": generated,
        "max_frontier": max_frontier, "reopened": reopened,
        "path_len": 0, "algorithm": "UCS"
    }


@measure
def astar(graph: Dict[Any, Dict[Any, float]], h: Dict[Any, float], start: Any, goal: Any, weight: float = 1.0):
    """A* (or Weighted A* if weight != 1). Graph search with best g so far."""
    frontier = []
    counter = 0
    g = {start: 0.0}
    f0 = g[start] + weight * h.get(start, 0.0)
    heapq.heappush(frontier, (f0, counter, start))
    parent = {start: None}
    closed = set()

    expansions = 0
    generated = 1
    max_frontier = len(frontier)
    reopened = 0

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f_val, _, node = heapq.heappop(frontier)
        if node in closed:
            continue

        closed.add(node)
        expansions += 1

        if node == goal:
            path = reconstruct_path(parent, goal)
            metrics = {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier,
                "reopened": reopened,
                "path_len": len(path),
                "algorithm": f"A* (w={weight})",
            }
            return path, g[node], metrics

        for nbr in sorted(graph.get(node, {}).keys()):
            w = graph[node][nbr]
            tentative = g[node] + w
            if nbr not in g or tentative < g[nbr]:
                parent[nbr] = node
                g[nbr] = tentative
                counter += 1
                f_n = tentative + weight * h.get(nbr, 0.0)
                heapq.heappush(frontier, (f_n, counter, nbr))
                generated += 1
                if nbr in closed:
                    reopened += 1

    return [], float("inf"), {
        "expansions": expansions, "generated": generated,
        "max_frontier": max_frontier, "reopened": reopened,
        "path_len": 0, "algorithm": f"A* (w={weight})"
    }


@measure
def greedy_best_first(graph: Dict[Any, Dict[Any, float]], h: Dict[Any, float], start: Any, goal: Any):
    """Greedy Best-First Search: priority = h(n). Not guaranteed optimal."""
    frontier = []
    counter = 0
    heapq.heappush(frontier, (h.get(start, 0.0), counter, start))
    parent = {start: None}
    visited = set()

    expansions = 0
    generated = 1
    max_frontier = len(frontier)

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        _, _, node = heapq.heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        expansions += 1

        if node == goal:
            path = reconstruct_path(parent, goal)
            # compute path cost from graph (since GBFS doesn't track g)
            cost = 0.0
            for u, v in zip(path, path[1:]):
                cost += graph[u][v]
            metrics = {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier,
                "reopened": 0,
                "path_len": len(path),
                "algorithm": "Greedy Best-First",
            }
            return path, cost, metrics

        for nbr in sorted(graph.get(node, {}).keys()):
            if nbr not in visited:
                parent.setdefault(nbr, node)  # keep first parent found
                counter += 1
                heapq.heappush(frontier, (h.get(nbr, 0.0), counter, nbr))
                generated += 1

    return [], float("inf"), {
        "expansions": expansions, "generated": generated,
        "max_frontier": max_frontier, "reopened": 0,
        "path_len": 0, "algorithm": "Greedy Best-First"
    }


# ==========
# Runner and report
# ==========

def run_all(graph, h, start, goal):
    results = []
    for algo in (
        lambda: ucs(graph, start, goal),
        lambda: astar(graph, h, start, goal, weight=1.0),
        lambda: greedy_best_first(graph, h, start, goal),
    ):
        path, cost, metrics = algo()
        results.append((path, cost, metrics))
    return results


def print_report(results):
    # Tabular summary
    header = (
        f"{'ALGORITHM':<20} {'COST':>8} {'LEN':>5} "
        f"{'EXP':>6} {'GEN':>6} {'MAX_OPEN':>9} "
        f"{'TIME(s)':>9} {'PEAK(KB)':>10}"
    )
    print(header)
    print("-" * len(header))
    for path, cost, m in results:
        print(f"{m['algorithm']:<20} "
              f"{(f'{cost:.2f}' if cost != float('inf') else 'inf'):>8} "
              f"{m['path_len']:>5} "
              f"{m['expansions']:>6} {m['generated']:>6} {m['max_frontier']:>9} "
              f"{m['time_sec']:.6f:>9} {m['peak_mem_kb']:.1f:>10}")
    print("\nBest paths:")
    for path, cost, m in results:
        print(f"- {m['algorithm']}: cost={cost:.2f}  path={path}")


if __name__ == "__main__":
    results = run_all(graph, h_values, start, goal)
    print_report(results)
