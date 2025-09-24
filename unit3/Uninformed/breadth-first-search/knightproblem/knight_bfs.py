from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import time
import os


# Functions

def knight_legal_moves(pos, N):
    x, y = pos
    
    # Generate all L-shaped moves
    deltas = []
    for dx in (1, -1):
        for dy in (2, -2):
            deltas.append((dx, dy))
            deltas.append((dy, dx))
    
    # Filter only the moves inside the board
    legal = []
    for dx, dy in deltas:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            legal.append((nx, ny))
    
    return legal

from collections import deque

def bfs(start_node, goal_node, N):
    """
    BFS with goal check.
    """
    visited = set([start_node])
    queue = deque([start_node])
    parent = {start_node: None}  # for path reconstruction

    while queue:
        current_node = queue.popleft()
        print(f"Visiting node: {current_node}")

        # Goal test
        if current_node == goal_node:
            print("Goal found!")
            # reconstruct path from start to goal
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            return list(reversed(path))

        else:
            for neighbor in knight_legal_moves(current_node, N):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_node
                    queue.append(neighbor)

    return None  # goal not found

# Visualization


def plot_knight_path_tiles(path, N, save_dir):
    board = np.zeros((N, N, 3))  # RGB image

    # Color chessboard squares (white and gray)
    for i in range(N):
        for j in range(N):
            if (i + j) % 2 == 0:
                board[i, j] = [1, 1, 1]  # white
            else:
                board[i, j] = [0.8, 0.8, 0.8]  # light gray

    # Color path tiles
    for idx, (x, y) in enumerate(path):
        if idx == 0:
            board[y, x] = [0.2, 0.8, 0.2]  # start: green
        elif idx == len(path) - 1:
            board[y, x] = [0.9, 0.2, 0.2]  # goal: red
        else:
            board[y, x] = [0.2, 0.4, 0.9]  # path: blue

    plt.figure(figsize=(6,6))
    plt.imshow(board, origin='upper')
    # Number the moves
    for idx, (x, y) in enumerate(path):
        plt.text(x, y, str(idx), color='black', fontsize=12, ha='center', va='center', weight='bold')
    plt.xticks(range(N))
    plt.yticks(range(N))
    plt.gca().set_xticks(np.arange(-.5, N, 1), minor=True)
    plt.gca().set_yticks(np.arange(-.5, N, 1), minor=True)
    plt.grid(which='minor', color='black', linewidth=1)
    plt.title("Knight's Shortest Path (Tiles Colored)")
    
    # Ensure save directory exists
    save_dir = 'unit3/breadth-first-search/knightproblem/board_imgs'
    os.makedirs(save_dir, exist_ok=True)
    # Generate unique filename with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"knight_path_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    plt.savefig(filepath)
    plt.close()
    print(f"Image saved as: {filepath}")

# Example usage:
start_time = time.time()
N=8
save_dir = '../unit3/Uninformed/breadth-first-search/knightproblem/board_solutions'
start, goal = (1,3), (0,7)

# Start the search
path = bfs(start, goal, N)
# Plot solution
plot_knight_path_tiles(path, 8, save_dir)

# Print solution
print(f"Knight moves from {start} to {goal} in {len(path)-1} moves.")
print("Path:", path)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.6f} seconds")
