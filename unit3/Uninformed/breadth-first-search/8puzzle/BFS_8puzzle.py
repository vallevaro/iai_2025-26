# 8-puzzle BFS

from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple, Dict
from objectsclass import Problem, Node
State = Tuple[int, ...]  # 9-tuple, 0 is the blank


@dataclass
class Node:
    state: State
    parent: Optional["Node"] = None
    action: Optional[str] = None
    path_cost: int = 0    # g(n)

# ---------- 8-puzzle domain ----------

GOAL: State = (1,2,3,4,5,6,7,8,0)

def print_board(s: State) -> None:
    def sym(x): return "·" if x == 0 else str(x)
    rows = [s[0:3], s[3:6], s[6:9]]
    for r in rows:
        print(" ".join(f"{sym(x):>2}" for x in r))
    print()

def is_solvable(s: State) -> bool:
    # For 3x3: solvable iff number of inversions (ignoring 0) is even
    arr = [x for x in s if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0

class EightPuzzle(Problem):
    def __init__(self, initial: State, goal: State = GOAL):
        super().__init__(initial, goal)

    def actions(self, state: State) -> List[str]:
        i = state.index(0)
        r, c = divmod(i, 3)
        acts = []
        if r > 0: acts.append("Up")
        if r < 2: acts.append("Down")
        if c > 0: acts.append("Left")
        if c < 2: acts.append("Right")
        return acts

    def result(self, state: State, action: str) -> State:
        i = state.index(0)
        r, c = divmod(i, 3)
        dr = {"Up": -1, "Down": 1, "Left": 0, "Right": 0}[action]
        dc = {"Up": 0, "Down": 0, "Left": -1, "Right": 1}[action]
        nr, nc = r + dr, c + dc
        j = 3 * nr + nc  # swap 0 with index j
        lst = list(state)
        lst[i], lst[j] = lst[j], lst[i]
        return tuple(lst)  # type: ignore[return-value]

# ---------- BFS (graph-search) with step-by-step trace ----------

def expand(problem: Problem, node: Node) -> Iterable[Node]:
    s = node.state
    for a in problem.actions(s):
        s2 = problem.result(s, a)
        yield Node(state=s2, parent=node, action=a, path_cost=node.path_cost + 1)

def reconstruct_path(node: Node) -> List[Node]:
    path = []
    while node:
        path.append(node)
        node = node.parent  # type: ignore[assignment]
    return list(reversed(path))

def breadth_first_search(problem: Problem, verbose: bool = True,
                         max_expansions: Optional[int] = None) -> Optional[Node]:
    root = Node(problem.initial)
    if problem.is_goal(root.state):
        if verbose:
            print("Initial state is already the goal.")
        return root

    frontier = deque([root])
    reached: Dict[State, int] = {root.state: 0}  # state -> depth
    step = 0
    expansions = 0

    if verbose:
        print("BFS started")
        print("Initial state:")
        print_board(root.state)
        print(f"Frontier size = {len(frontier)}\n")

    while frontier:
        node = frontier.popleft()
        step += 1
        expansions += 1
        if verbose:
            print(f"Step {step}: DEQUEUE (depth={node.path_cost})")
            print_board(node.state)

        if max_expansions is not None and expansions > max_expansions:
            if verbose:
                print("Max expansions limit reached → stopping.")
            return None

        for child in expand(problem, node):
            if problem.is_goal(child.state):
                if verbose:
                    print(f"  Enqueue via action '{child.action}' → **GOAL FOUND**")
                    print_board(child.state)
                    print(f"Frontier size = {len(frontier)}")
                return child
            if child.state not in reached:
                reached[child.state] = child.path_cost
                frontier.append(child)
                if verbose:
                    print(f"  Enqueue via action '{child.action}'")
        if verbose:
            print(f"Frontier size = {len(frontier)}\n")

    return None

# ---------- Demo ----------

if __name__ == "__main__":
    # Choose an example that is solvable and not too long for class demos.
    # Try one of these:
    # initial = (1,2,3,4,5,6,0,7,8)        # 2 moves
    # initial = (1,2,3,4,5,6,7,0,8)        # 1 move
    initial = (1,2,3,5,0,6,4,7,8)          # ~4 moves
    goal = GOAL

    print("Initial configuration:")
    print_board(initial)
    print("Goal configuration:")
    print_board(goal)

    if not is_solvable(initial):
        print("This instance is NOT solvable (odd inversion parity). Choose another start.")
    else:
        problem = EightPuzzle(initial, goal)
        goal_node = breadth_first_search(problem, verbose=True)

        if goal_node is None:
            print("No solution found.")
        else:
            path = reconstruct_path(goal_node)
            moves = [n.action for n in path[1:]]
            print("\n=== Solution Summary ===")
            print(f"Moves ({len(moves)}): {moves}")
            print("\nStates along the solution path:\n")
            for k, n in enumerate(path):
                print(f"Depth {k}" + ("" if n.action is None else f"  (via {n.action})"))
                print_board(n.state)
