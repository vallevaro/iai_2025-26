function GreedyBestFirstSearch(start_node, goal_node, heuristic_function):
    // A priority queue to store nodes to be evaluated, ordered by heuristic value.
    // Each element could be a tuple: (heuristic_value, node).
    frontier = new PriorityQueue()
    frontier.add(start_node, heuristic_function(start_node))

    // A set to keep track of nodes that have already been expanded.
    // This prevents infinite loops in graphs with cycles.
    explored_set = new Set()

    // A map to reconstruct the path once the goal is found.
    // It stores parent pointers: came_from[child] = parent.
    came_from = new Map()
    came_from[start_node] = null

    while frontier is not empty:
        // Get the node from the frontier with the lowest heuristic value.
        current_node = frontier.pop()

        // Goal check: if the current node is the goal, we are done.
        if current_node == goal_node:
            return reconstruct_path(came_from, current_node)

        // Add the current node to the explored set so we don't visit it again.
        explored_set.add(current_node)

        // For each neighbor of the current node...
        for each neighbor in get_neighbors(current_node):
            // If we have already expanded this neighbor, skip it.
            if neighbor in explored_set:
                continue

            // If the neighbor is not already in the frontier, add it.
            // In a simple Greedy search, we don't need to check if a better
            // path to an existing frontier node is found (unlike A*).
            if neighbor not in frontier:
                came_from[neighbor] = current_node
                heuristic_value = heuristic_function(neighbor)
                frontier.add(neighbor, heuristic_value)

    // If the frontier becomes empty and the goal was not reached, no path exists.
    return failure

function reconstruct_path(came_from, current_node):
    path = []
    while current_node is not null:
        path.prepend(current_node) // Add to the beginning of the list
        current_node = came_from[current_node]
    return path




# simplified

function GreedyBestFirstSearch(start_node, goal_node, heuristic_function):
    frontier = new PriorityQueue() // Stores nodes ordered by heuristic value
    frontier.add(start_node, heuristic_function(start_node))

    explored_set = new Set()
    came_from = new Map() // For reconstructing the path

    while frontier is not empty:
        current_node = frontier.pop()

        if current_node == goal_node:
            return reconstruct_path(came_from, current_node)

        explored_set.add(current_node)

        for each neighbor in get_neighbors(current_node):
            if neighbor not in explored_set and neighbor not in frontier:
                came_from[neighbor] = current_node
                heuristic_value = heuristic_function(neighbor)
                frontier.add(neighbor, heuristic_value)

    return failure // No path found