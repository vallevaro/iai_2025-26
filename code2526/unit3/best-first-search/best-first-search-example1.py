import heapq
from objectsclass import *


def best_first_search(problem, f):
    """Best-First Search (general form).
    
    Arguments:
        problem -- instance of Problem
        f       -- evaluation function f(node) to order the frontier
    """
    # Initial node
    node = Node(problem.initial)

    # Frontier: priority queue ordered by f(node)
    frontier = [(f(node), node)]
    heapq.heapify(frontier)

    # Reached: best node found for each state
    reached = {problem.initial: node}

    while frontier:
        _, node = heapq.heappop(frontier)

        # Goal test
        if problem.is_goal(node.state):
            return node

        # Expand
        for child in expand(problem, node):
            s = child.state

            # If new or better path found
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                heapq.heappush(frontier, (f(child), child))

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
        'C': ['F']}