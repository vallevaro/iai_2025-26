
from collections import deque
from objectsclass import Node

def expand(problem, node):
    s = node.state
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        g2 = node.path_cost + problem.action_cost(s, action, s2)
        yield Node(state=s2, parent=node, action=action, path_cost=g2)


def breadth_first_search(problem, verbose=True):
    """BFS for trees (no reached set, no duplicate detection)."""
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node

    frontier = deque([node])
    step = 0

    if verbose:
        print(f"Step {step}: init")
        print("  Frontier:", list(frontier))
        print()

    while frontier:
        step += 1
        node = frontier.popleft()
        if verbose:
            print(f"Step {step}: pop -> {node.state}")

        for child in expand(problem, node):
            if verbose:
                print(f"    generate child: {child.state}")
            if problem.is_goal(child.state):
                if verbose:
                    print("    ** GOAL FOUND ** ->", child.state)
                return child
            frontier.append(child)

        if verbose:
            print("  Frontier:", list(n.state for n in frontier))
            print()

    return None  # failure