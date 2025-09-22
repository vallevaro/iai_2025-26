from collections import deque
from objectsclass import *


def breadth_first_search(problem):
    """Breadth-First Search for tree problems (no repeated-state check)."""
    # Initial node
    node = Node(problem.initial)

    # Goal test
    if problem.is_goal(node.state):
        return node

    # Frontier: FIFO queue
    frontier = deque([node])

    while frontier:
        node = frontier.popleft()

        # Expand children
        for child in expand(problem, node):
            # Goal test
            if problem.is_goal(child.state):
                return child
            frontier.append(child)

    return None  # failure


def expand(problem, node):
    """Generate child nodes from node by applying all actions."""
    s = node.state
    for action in problem.actions(s):
        s_prime = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)


# --- Example Problem: simple binary tree ---
class BinaryTreeProblem(Problem):
    def __init__(self, initial, goal, tree):
        super().__init__(initial, goal)
        self.tree = tree  # dict mapping parent -> [children]

    def actions(self, state):
        # The "actions" are just moving to children
        return self.tree.get(state, [])

    def result(self, state, action):
        # In a tree, the result of an action is just the child
        return action

    def action_cost(self, s, action, s_prime):
        return 1  # uniform cost


# Example usage
if __name__ == "__main__":
    # A small binary tree
    tree = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': [],
        'E': [],
        'F': [],
        'G': []
    }

    problem = BinaryTreeProblem('A', 'F', tree)

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
