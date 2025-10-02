function AStarSearch(start_node, goal_node, heuristic_function, distance_function):
    // A priority queue to store nodes to be evaluated, ordered by f(n) value.
    // Each element could be a tuple: (f_value, node).
    frontier = new PriorityQueue()
    frontier.add(start_node, 0 + heuristic_function(start_node))

    // A set to keep track of nodes that have already been expanded.
    explored_set = new Set()

    // A map to reconstruct the path once the goal is found.
    came_from = new Map()
    came_from[start_node] = null

    // A map to store the cost of the cheapest path from start to n found so far.
    g_score = new Map() // Initialize all values to infinity
    g_score[start_node] = 0

    while frontier is not empty:
        // Get the node from the frontier with the lowest f(n) value.
        current_node = frontier.pop()

        // Goal check
        if current_node == goal_node:
            return reconstruct_path(came_from, current_node)

        explored_set.add(current_node)

        for each neighbor in get_neighbors(current_node):
            if neighbor in explored_set:
                continue

            // Calculate the g_score for this path to the neighbor
            tentative_g_score = g_score[current_node] + distance_function(current_node, neighbor)

            // If this path to the neighbor is better than any previous one...
            if tentative_g_score < g_score.get(neighbor, infinity):
                // Record this new, better path
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic_function(neighbor)
                
                // If neighbor is not in the frontier, add it.
                // If it is, this update will ensure its priority is correct.
                if neighbor not in frontier:
                    frontier.add(neighbor, f_score)

    // If the frontier becomes empty and the goal was not reached, no path exists.
    return failure

function reconstruct_path(came_from, current_node):
    path = []
    while current_node is not null:
        path.prepend(current_node) // Add to the beginning of the list
        current_node = came_from[current_node]
    return path



# simplified 

function AStarSearch(start_node, goal_node, heuristic_function, distance_function):
    frontier = new PriorityQueue() // Stores nodes ordered by f(n) value
    frontier.add(start_node, 0 + heuristic_function(start_node))

    explored_set = new Set()
    came_from = new Map()

    g_score = new Map() // Cost from start to a node
    g_score[start_node] = 0

    while frontier is not empty:
        current_node = frontier.pop()

        if current_node == goal_node:
            return reconstruct_path(came_from, current_node)

        explored_set.add(current_node)

        for each neighbor in get_neighbors(current_node):
            tentative_g_score = g_score[current_node] + distance_function(current_node, neighbor)

            if tentative_g_score < g_score.get(neighbor, infinity):
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic_function(neighbor)
                if neighbor not in frontier:
                    frontier.add(neighbor, f_score)
    return failure