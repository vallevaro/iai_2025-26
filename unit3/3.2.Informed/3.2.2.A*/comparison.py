import heapq


romania_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# Heuristic values: Straight-line distance to Bucharest
heuristic_distances = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

def generic_search(graph, start, goal, heuristics, f_function):
    """
    A generic search algorithm that can be configured for A*, Greedy, or UCS.
    The f_function determines the priority of nodes in the frontier.
    Returns the path and the set of explored nodes.
    """
    explored_set = set()
    frontier = [(0, start)] # Priority queue stores (priority, node)
    came_from = {}
    g_score = {city: float('inf') for city in graph}
    g_score[start] = 0
    
    while frontier:
        _, current_node = heapq.heappop(frontier)
        
        if current_node == goal:
            return reconstruct_path(came_from, current_node), explored_set
            
        explored_set.add(current_node)
        
        for neighbor, distance in graph[current_node].items():
            if neighbor in explored_set:
                continue
                
            tentative_g_score = g_score[current_node] + distance
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                
                # The key difference: calculate priority using the passed f_function
                priority = f_function(tentative_g_score, heuristics[neighbor])
                heapq.heappush(frontier, (priority, neighbor))
                
    return None, explored_set

# Helper functions (same as before)
def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    return path[::-1]

def calculate_path_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i+1]]
    return cost



if __name__ == "__main__":
    start_city = 'Arad'
    goal_city = 'Bucharest'

    print(f"Finding path from {start_city} to {goal_city}...\n")
    
    # --- A* Search ---
    # f(n) = g(n) + h(n)
    a_star_f = lambda g, h: g + h
    path_a_star, explored_a_star = generic_search(romania_map, start_city, goal_city, heuristic_distances, a_star_f)
    
    print("--- A* Search Results ---")
    if path_a_star:
        cost_a_star = calculate_path_cost(romania_map, path_a_star)
        print("Path: " + " -> ".join(path_a_star))
        print(f"Cost: {cost_a_star}")
        print(f"Nodes Explored: {len(explored_a_star)}")
    else:
        print("No path found.")

    # --- Greedy Best-First Search ---
    # f(n) = h(n)
    greedy_f = lambda g, h: h
    path_greedy, explored_greedy = generic_search(romania_map, start_city, goal_city, heuristic_distances, greedy_f)

    print("\n--- Greedy Best-First Search Results ---")
    if path_greedy:
        cost_greedy = calculate_path_cost(romania_map, path_greedy)
        print("Path: " + " -> ".join(path_greedy))
        print(f"Cost: {cost_greedy}")
        print(f"Nodes Explored: {len(explored_greedy)}")
    else:
        print("No path found.")

    # --- Uniform Cost Search (Dijkstra's) ---
    # f(n) = g(n)
    ucs_f = lambda g, h: g
    path_ucs, explored_ucs = generic_search(romania_map, start_city, goal_city, heuristic_distances, ucs_f)

    print("\n--- Uniform Cost Search Results ---")
    if path_ucs:
        cost_ucs = calculate_path_cost(romania_map, path_ucs)
        print("Path: " + " -> ".join(path_ucs))
        print(f"Cost: {cost_ucs}")
        print(f"Nodes Explored: {len(explored_ucs)}")
    else:
        print("No path found.")