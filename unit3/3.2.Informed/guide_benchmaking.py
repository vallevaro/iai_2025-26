


# 1Import the standard libraries you need:
# (time → measure runtime, tracemalloc → memory usage, sys/os → imports)
import time
import tracemalloc
import sys, os
from typing import Dict, Any, List, Tuple

# ------------------------------------------------------
# Make sure Python can import your other algorithm files.
# If your file structure is organized in subfolders, append the parent path:
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ------------------------------------------------------
#  Import your algorithms here (make sure function names match your files)
# from astar import a_star_search
# from gbfs import greedy_best_first_search
# from weightedAstar import weighted_a_star_search
# from IDAstar import ida_star

# ------------------------------------------------------
# Import the graph and heuristic data
# from datagraph1 import graph, h_values, start, goal


# ======================================================
# MEASUREMENT FUNCTION
# ======================================================
# This helper records execution time and peak memory for each algorithm.

def measure(func, *args, **kwargs):
    # Start memory tracking
    tracemalloc.start()
    # Start timer
    t0 = time.perf_counter()

    # Execute the algorithm
    result = func(*args, **kwargs)

    # Stop timer and memory tracking
    t1 = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Expect the function to return (path, cost, metrics)
    path, cost, metrics = result
    metrics.update({
        "time_sec": t1 - t0,
        "peak_mem_kb": peak / 1024.0
    })
    return path, cost, metrics


# ======================================================
# MAIN COMPARISON FUNCTION
# ======================================================
# Define which algorithms to compare and run them all in sequence.
# Each algorithm must return a tuple (path, cost, metrics_dict).

def run_all(graph, h, start, goal, w=1.5):
    results = []

    # Add the algorithms you want to compare here:
    algorithms = [
        ("A*", lambda: a_star_search(graph, start, goal, h)),
        ("Weighted A*", lambda: weighted_a_star_search(graph, start, goal, h, w)),
        ("Greedy Best-First", lambda: greedy_best_first_search(graph, start, goal, h)),
        ("IDA*", lambda: ida_star(graph, start, goal, h)),
    ]

    # Run each algorithm and measure its performance
    for name, thunk in algorithms:
        print(f"→ Running {name} ...")
        try:
            out = thunk()

            # Some algorithms may return only (path, cost)
            if len(out) == 2:
                path, cost = out
                metrics = {}
            else:
                path, cost, metrics = out or ([], float("inf"), {})

        except Exception as e:
            print(f"⚠️  {name} failed: {e}")
            path, cost, metrics = [], float("inf"), {"error": str(e)}

        # Store algorithm name and minimal info
        metrics.setdefault("algorithm", name)
        metrics.setdefault("path_len", len(path))
        results.append((path, cost, metrics))

    return results


# ======================================================
# REPORT FUNCTION
# ======================================================
# Print the results of all algorithms in a table format.

def print_report(results):
    # Define table header
    header = (
        f"{'ALGORITHM':<20} {'COST':>8} {'LEN':>5} "
        f"{'EXP':>6} {'GEN':>6} {'MAX_OPEN':>9} "
        f"{'TIME(s)':>9} {'PEAK(KB)':>10}"
    )
    print(header)
    print("-" * len(header))

    # Print one line per algorithm
    for path, cost, m in results:
        print(f"{m['algorithm']:<20} "
              f"{(f'{cost:.2f}' if cost != float('inf') else 'inf'):>8} "
              f"{m.get('path_len', len(path)):>5} "
              f"{m.get('expansions', '?'):>6} "
              f"{m.get('generated', '?'):>6} "
              f"{m.get('max_frontier', '?'):>9} "
              f"{m.get('time_sec', 0):.6f:>9} {m.get('peak_mem_kb', 0):.1f:>10}")

    # Print final paths
    print("\nBest paths:")
    for path, cost, m in results:
        print(f"- {m['algorithm']}: cost={cost:.2f}  path={path}")


# ======================================================
# MAIN PROGRAM
# ======================================================
# When you run this file directly, it executes all algorithms and prints results.

if __name__ == "__main__":
    # Call your run_all function using the imported graph and heuristics
    # results = run_all(graph, h_values, start, goal)
    # print_report(results)
    pass  # ← remove this line when you fill in your own calls
