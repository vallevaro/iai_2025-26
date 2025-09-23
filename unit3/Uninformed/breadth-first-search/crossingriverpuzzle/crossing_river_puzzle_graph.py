from collections import deque
from typing import List, Tuple, Optional, Dict

# ---------- State & helpers ----------
# State: (F, W, G, C) with 0=left, 1=right
LEFT, RIGHT = 0, 1
NAMES = ["F", "W", "G", "C"]

State = Tuple[int, int, int, int]

def is_legal(s: State) -> bool:
    F, W, G, C = s
    # Wolf with Goat without Farmer
    if F != W and W == G:
        return False
    # Goat with Cabbage without Farmer
    if F != C and G == C:
        return False
    return True

def neighbors(s: State) -> List[Tuple[str, State]]:
    """Generate legal moves (label, next_state)."""
    F, W, G, C = s
    side = F
    moves = []

    # Farmer alone
    t = (1 - F, W, G, C)
    if is_legal(t):
        moves.append(("F", t))

    # Farmer with Wolf
    if W == side:
        t = (1 - F, 1 - W, G, C)
        if is_legal(t):
            moves.append(("F+W", t))

    # Farmer with Goat
    if G == side:
        t = (1 - F, W, 1 - G, C)
        if is_legal(t):
            moves.append(("F+G", t))

    # Farmer with Cabbage
    if C == side:
        t = (1 - F, W, G, 1 - C)
        if is_legal(t):
            moves.append(("F+C", t))

    return moves

def pretty(s: State) -> str:
    L = "".join(n for n, side in zip(NAMES, s) if side == LEFT)
    R = "".join(n for n, side in zip(NAMES, s) if side == RIGHT)
    return f"L: {L:<4} || R: {R:<4}"

# ---------- BFS (graph-search) ----------
def bfs_farmer(start: State, goal: State) -> Optional[List[Tuple[str, State]]]:
    if not is_legal(start):
        return None
    if start == goal:
        return [("START", start)]

    q = deque([start])
    visited = {start}
    parent: Dict[State, Optional[State]] = {start: None}
    action_from: Dict[State, str] = {start: "START"}

    while q:
        s = q.popleft()
        for a, t in neighbors(s):
            if t in visited:
                continue
            visited.add(t)
            parent[t] = s
            action_from[t] = a
            if t == goal:
                return reconstruct(parent, action_from, t)
            q.append(t)

    return None

def reconstruct(parent: Dict[State, Optional[State]],
                action_from: Dict[State, str],
                goal_state: State) -> List[Tuple[str, State]]:
    path: List[Tuple[str, State]] = []
    s = goal_state
    while s is not None:
        path.append((action_from[s], s))
        s = parent[s]
    return list(reversed(path))

# ---------- demo ----------
if __name__ == "__main__":
    start = (0,0,0,0)  # all left
    goal  = (1,1,1,1)  # all right

    sol = bfs_farmer(start, goal)
    if sol is None:
        print("No solution.")
    else:
        print(f"Solution in {len(sol)-1} crossings:\n")
        for i, (move, state) in enumerate(sol):
            info = "" if move == "START" else f" via {move}"
            print(f"Step {i}{info:>10}   {pretty(state)}")
