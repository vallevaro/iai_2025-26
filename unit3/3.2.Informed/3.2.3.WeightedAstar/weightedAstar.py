import heapq
import math

def weighted_a_star_search(graph, start, goal, heuristics, weight: float = 1.0):
    """
    Weighted A* search.
    Uses f(n) = g(n) + weight * h(n).  With weight >= 1:
      - w = 1.0  -> standard A*
      - w > 1.0  -> greedier, expands fewer nodes, NOT guaranteed optimal

    Parameters
    ----------
    graph : dict[node] -> dict[neighbor] = edge_cost
    start : hashable
    goal  : hashable
    heuristics : dict[node] -> h(node) >= 0
    weight : float >= 1.0

    Returns
    -------
    path : list[node] | None
        Path from start to goal (inclusive), or None if unreachable.
    """
    if weight < 1.0:
        raise ValueError("weight must be >= 1.0 for Weighted A*.")

    explored_set = set()              # closed set
    frontier = []                     # min-heap of (f_score, tie, node)
    counter = 0

    came_from = {}                    # for path reconstruction
    g_score = {start: 0.0}

    h_start = heuristics.get(start, 0.0)
    heapq.heappush(frontier, (g_score[start] + weight * h_start, counter, start))

    while frontier:
        _, _, current_node = heapq.heappop(frontier)

        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        if current_node in explored_set:
            continue
        explored_set.add(current_node)

        for neighbor, step_cost in graph.get(current_node, {}).items():
            if neighbor in explored_set:
                continue

            tentative_g = g_score[current_node] + step_cost

            # If we found a better path to 'neighbor', record it and (re)push to frontier
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g
                h = heuristics.get(neighbor, 0.0)
                counter += 1
                f = tentative_g + weight * h
                heapq.heappush(frontier, (f, counter, neighbor))

    return None  # no path

def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    return path[::-1]

def calculate_path_cost(graph, path):
    if not path or len(path) < 2:
        return 0
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i+1]]
    return cost

# -------------------------
# Example main test
# -------------------------
if __name__ == "__main__":
    
    import sys
    import os
    # Example: import the Romania graph from problem_graph2.py
    from sample_graphs.problem_graph1 import graph, h_values

    start, goal = "S", "C"
    weight = 1.0  # change to >1 for weighted A*

    path = weighted_a_star_search(graph, start, goal, h_values, weight)
    if path:
        cost = calculate_path_cost(graph, path)
        print(f"Weighted A* (w={weight}) path: {path}")
        print(f"Total path cost: {cost}")
    else:
        print("No path found.")