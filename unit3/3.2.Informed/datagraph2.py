from typing import Dict, Hashable

Node = Hashable
Graph = Dict[Node, Dict[Node, float]]
Heur  = Dict[Node, float]

graph: Graph = {
    "A": {"B": 1, "C": 4},
    "B": {"D": 3, "E": 1},
    "C": {"F": 1},
    "D": {"G": 3},
    "E": {"G": 2},
    "F": {"G": 5},
    "G": {}
}
# heuristic to G (admissible)
h_values: Heur = {"A": 3, "B": 2, "C": 2, "D": 2, "E": 1, "F": 4, "G": 0}
