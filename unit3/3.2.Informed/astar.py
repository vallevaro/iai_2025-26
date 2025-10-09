import heapq
import math

#
# STEP 2: Implement the A* Search Algorithm
#

def a_star_search(graph, start, goal, heuristics):
    """
    Finds the shortest path from start to goal using A* search.
    graph: dict[node] -> dict[neighbor] = edge_cost
    heuristics: dict[node] = h(node)
    Returns a list of nodes for the path, or None if no path.
    """
    # The set of nodes already evaluated.
    explored_set = set()

    # The priority queue of nodes to be evaluated. Stores tuples of (f_score, tie, node).
    # The tie-breaker avoids comparing nodes when f_scores are equal.
    frontier = []
    counter = 0

    # A dictionary to reconstruct the path. came_from[n] is the node immediately
    # preceding n on the cheapest path from start to n currently known.
    came_from = {}

    # g_score[n] is the cost of the cheapest path from start to n known so far.
    g_score = {start: 0}

    h_start = heuristics.get(start, 0)
    heapq.heappush(frontier, (g_score[start] + h_start, counter, start))

    while frontier:
        # Get the node in the frontier with the lowest f_score.
        # The f_score is not needed after this, so we use '_'
        _, _, current_node = heapq.heappop(frontier)

        # If we have reached the goal, reconstruct and return the path.
        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        if current_node in explored_set:
            continue
        explored_set.add(current_node)

        # Explore neighbors
        for neighbor, step_cost in graph.get(current_node, {}).items():
            if neighbor in explored_set:
                continue

            # Calculate the tentative g_score for the path through the current_node
            tentative_g = g_score[current_node] + step_cost

            # If this path to the neighbor is better than any previously known...
            if tentative_g < g_score.get(neighbor, math.inf):
                # ...record it as the new best path.
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g

                # Add/update the neighbor in the frontier for evaluation.
                h = heuristics.get(neighbor, 0)
                counter += 1
                heapq.heappush(frontier, (tentative_g + h, counter, neighbor))

    # If the frontier is empty and we haven't reached the goal, no path exists.
    return None

def reconstruct_path(came_from, current_node):
    """
    Reconstructs the path from the came_from dictionary.
    """
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    return path[::-1]  # Reverse the path to get it from start to goal

def calculate_path_cost(graph, path):
    """
    Calculates the total cost of a given path.
    """
    if not path or len(path) < 2:
        return 0
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i+1]]
    return cost

# --- Example usage ---
if __name__ == "__main__":
    # Define start and goal cities
    

    from romania_map import romania_map, h_to_bucharest 
    start, goal = "Arad", "Bucharest"
    path = a_star_search(romania_map, start, goal, h_to_bucharest)

    if path:
        print("A* Path from", start, "to", goal, ":")
        print(" → ".join(path))
        total_cost = calculate_path_cost(romania_map, path)
        print(f"\nTotal path cost: {total_cost} km")
    else:
        print(f'No path found')