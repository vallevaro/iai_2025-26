import heapq

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_best_first_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(start, goal), start))
    came_from = {start: None}
    visited = set()
    
    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Explore neighbors (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                    if neighbor not in came_from:
                        heapq.heappush(frontier, (manhattan_distance(neighbor, goal), neighbor))
                        came_from[neighbor] = current
    
    return "No path found"

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Example maze
maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goal = (4, 4)

result = greedy_best_first_search(maze, start, goal)
print(result)
