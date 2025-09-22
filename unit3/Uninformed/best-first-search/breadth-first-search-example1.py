from collections import deque
from objectsclass import *


def breadth_first_search(problem):
    """Breadth-First Search (tree/graph search)."""
    # Initial node
    node = Node(problem.initial)

    # Goal test
    if problem.is_goal(node.state):
        return node

    # Frontier: FIFO queue
    frontier = deque([node])

    # Reached: states we have seen
    reached = {problem.initial}

    while frontier:
        node = frontier.popleft()

        # Expand
        for child in expand(problem, node):
            s = child.state

            # Goal test
            if problem.is_goal(s):
                return child

            if s not in reached:
                reached.add(s)
                frontier.append(child)

    return None  # failure


def expand(problem, node):
    """Generate child nodes from node by applying all actions."""
    s = node.state
    for action in problem.actions(s):
        s_prime = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)


# --- Example Problem: simple graph search ---
class GraphProblem(Problem):
    def __init__(self, initial, goal, graph, costs=None):
        super().__init__(initial, goal)
        self.graph = graph
        self.costs = costs if costs else {}

    def actions(self, state):
        return list(self.graph.get(state, []))

    def result(self, state, action):
        return action

    def action_cost(self, s, action, s_prime):
        return self.costs.get((s, s_prime), 1)


# Example usage
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['G'],
        'F': [],
        'G': []
    }
    costs = {('A','B'):1, ('A','C'):1, ('B','D'):1, ('B','E'):1, ('C','F'):1, ('E','G'):1}

    problem = GraphProblem('A', 'G', graph, costs)

    solution = breadth_first_search(problem)

    if solution:
        # Reconstruct path
        path = []
        n = solution
        while n:
            path.append(n.state)
            n = n.parent
        print("Solution path:", list(reversed(path)))
    else:
        print("No solution found")
