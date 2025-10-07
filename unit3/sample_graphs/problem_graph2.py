# problem_graph2.py

# Directed, weighted graph
graph = {
    'Arad': {'Sibiu': 140, 'Timisoara': 118},
    'Sibiu': {'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Lugoj': 111},
    'Lugoj': {'Mehadia': 70},
    'Mehadia': {'Drobeta': 75},
    'Drobeta': {'Craiova': 120},
    'Rimnicu Vilcea': {'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Bucharest': 211},
    'Pitesti': {'Bucharest': 101},
    'Craiova': {'Pitesti': 138},
    'Bucharest': {}
}

# Straight-line distance heuristic (to Bucharest)
h_values = {
    'Arad': 366,
    'Sibiu': 253,
    'Timisoara': 329,
    'Lugoj': 244,
    'Mehadia': 241,
    'Drobeta': 242,
    'Rimnicu Vilcea': 193,
    'Fagaras': 178,
    'Pitesti': 98,
    'Craiova': 160,
    'Bucharest': 0
}
