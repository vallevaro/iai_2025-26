
import heapq
import time
import tracemalloc
from typing import Dict, Tuple, List, Optional, Any
import math  

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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, tracemalloc, heapq, sys, os
from typing import Dict, Any, List, Tuple

# === allow imports from sibling folders ===
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# === import your own algorithms ===
from astar import a_star_search
from gbfs import greedy_best_first_search
from weightedAstar import weighted_a_star_search
from IDAstar import ida_star

# === import graph and heuristics ===
from datagraph1 import graph, h_values
start, goal = 'S', 'G'

# === helper to measure time and memory ===
def measure(func, *args, **kwargs):
    tracemalloc.start()
    t0 = time.perf_counter()
    result = func(*args, **kwargs)
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    path, cost, metrics = result
    metrics.update({
        "time_sec": t1 - t0,
        "peak_mem_kb": peak / 1024.0
    })
    return path, cost, metrics


def run_all(graph, h, start, goal):
    results = []

    algorithms = [
        ("A*", a_star_search, (graph, start, goal, h)),
        ("Weighted A* w=1.5", weighted_a_star_search, (graph, start, goal, h, 1.5)),  # example weight=1.5
        ("Weighted A* w=3", weighted_a_star_search, (graph, start, goal, h, 3)),  # example weight=1.5
        ("Greedy Best-First", greedy_best_first_search, (graph, start, goal, h)),
        ("IDA*", ida_star, (graph, start, goal, h)),
    ]

    for name, func, args in algorithms:
        print(f"→ Running {name} ...")
        try:
            path, cost, metrics = measure(func, *args)
        except Exception as e:
            print(f"⚠️  {name} failed: {e}")
            path, cost, metrics = [], float("inf"), {}
        metrics.update({"algorithm": name})
        results.append((path, cost, metrics))

    return results


def print_report(results):
    header = (
        f"{'ALGORITHM':<20} {'COST':>8} {'LEN':>5} "
        f"{'EXP':>6} {'GEN':>6} {'MAX_OPEN':>9} "
        f"{'TIME(s)':>9} {'PEAK(KB)':>10}"
    )
    print(header)
    print("-" * len(header))

    for path, cost, m in results:
        algoname   = str(m.get("algorithm", "?"))
        path_len   = int(m.get("path_len", len(path) if path else 0))
        expansions = m.get("expansions", "?")
        generated  = m.get("generated", "?")
        max_open   = m.get("max_frontier", m.get("max_open", "?"))

        # Cost string
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) and math.isfinite(cost) else "inf"

        # Safe numeric defaults
        time_sec = float(m.get("time_sec", 0) or 0)
        peak_kb  = float(m.get("peak_mem_kb", 0) or 0)

        print(f"{algoname:<20} "
              f"{cost_str:>8} "
              f"{path_len:>5} "
              f"{expansions:>6} {generated:>6} {max_open:>9} "
              f"{time_sec:9.6f} {peak_kb:10.1f}")

    print("\nBest paths:")
    for path, cost, m in results:
        algoname = str(m.get("algorithm", "?"))
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) and math.isfinite(cost) else str(cost)
        print(f"- {algoname}: cost={cost_str}  path={path}")

if __name__ == "__main__":
    results = run_all(graph, h_values, start, goal)
    print_report(results)

