graph = {
        "S": ["A", "B"],
        "A": ["S", "C", "D"],
        "B": ["S", "E"],
        "C": ["A", "G"],
        "D": ["A"],
        "E": ["B", "G"],
        "G": ["C", "E"],  # goal
    }

# Heuristic (e.g., straight-line estimates); must be >= 0
# These numbers are just illustrative: smaller means "seems closer to G".
h_values = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 6, "E": 1, "G": 0}

