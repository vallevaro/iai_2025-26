
# Weighted adjacency list (same structure as romania_map)
graph = {
    "S": {"A": 1, "B": 2},
    "A": {"S": 1, "C": 2, "D": 3},
    "B": {"S": 2, "E": 2},
    "C": {"A": 2, "G": 3},
    "D": {"A": 3},
    "E": {"B": 2, "G": 1},
    "G": {"C": 3, "E": 1},  # Goal
}

# Heuristic estimates to the goal "G" (smaller = closer)
h_values = {
    "S": 5,
    "A": 4,
    "B": 3,
    "C": 2,
    "D": 6,
    "E": 1,
    "G": 0,
}
