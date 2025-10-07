import heapq
from typing import Dict, Iterable, Callable, Hashable, List, Optional, Tuple, Any

Node = Hashable
Graph = Dict[Node, Iterable[Node]]

def greedy_best_first_search(
    graph: Graph,
    start: Node,
    goal: Node,
    h: Callable[[Node], float],
) -> Tuple[Optional[List[Node]], List[Node]]:
    """
    Greedy Best-First Search (graph search).
    Expands the node with smallest heuristic h(n). Does NOT optimize path cost.

    Parameters
    ----------
    graph : dict node -> iterable of neighboring nodes
        (If you have weights, they are ignored by GBFS.)
    start : start node
    goal  : goal node
    h     : heuristic function h(n) >= 0

    Returns
    -------
    path : list of nodes from start to goal (inclusive), or None if no path found
    expanded_order : list of nodes in the order they were expanded
    """
    # Priority queue of (h(n), tie, node)
    # 'tie' ensures deterministic behavior when h(n) ties occur.
    frontier: List[Tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (h(start), counter, start))
    counter += 1

    came_from: Dict[Node, Optional[Node]] = {start: None}
    visited: set[Node] = set()
    expanded_order: List[Node] = []

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)
        expanded_order.append(current)

        if current == goal:
            # Reconstruct path
            path = []
            n: Optional[Node] = current
            while n is not None:
                path.append(n)
                n = came_from[n]
            path.reverse()
            return path, expanded_order

        # Push neighbors prioritized purely by h(n)
        for neigh in graph.get(current, []):
            if neigh not in visited and neigh not in came_from:
                came_from[neigh] = current
                heapq.heappush(frontier, (h(neigh), counter, neigh))
                counter += 1

    return None, expanded_order


# --- Example usage ---
if __name__ == "__main__":
    
    # Simple unweighted graph (edges are undirected here for convenience)
    from problem_graph2 import graph, h_values
    import sys, os
    sys.path.append(os.path.dirname(__file__))
    
    h = lambda n: h_values[n]
    
    start_node= 'S'
    goal_node= 'G'
    
    path, expanded = greedy_best_first_search(graph, start=start_node, goal=goal_node, h=h)
    
    print("Path:", path)           # e.g., ['S', 'B', 'E', 'G']
    print("Expanded:", expanded)   # expansion order under GBFS
