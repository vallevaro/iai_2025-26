from collections import deque
from typing import Tuple, List, Optional

State = Tuple[int, ...]  # 9-tuple; 0 is the blank
GOAL: State = (1,2,3,4,5,6,7,8,0)

# ---------- utilities ----------
def is_solvable(s: State) -> bool:
    arr = [x for x in s if x != 0]
    inv = sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i+1, len(arr)))
    return inv % 2 == 0

def pretty(s: State) -> str:
    sym = lambda x: "·" if x == 0 else str(x)
    return "\n".join(" ".join(sym(x) for x in s[i:i+3]) for i in (0,3,6))

def neighbors(s: State) -> List[Tuple[str, State]]:
    i = s.index(0)
    r, c = divmod(i, 3)
    moves = []
    for label, (dr, dc) in {"Up":(-1,0), "Down":(1,0), "Left":(0,-1), "Right":(0,1)}.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = 3*nr + nc
            lst = list(s)
            lst[i], lst[j] = lst[j], lst[i]
            moves.append((label, tuple(lst)))
    return moves

# ---------- BFS (graph-search) ----------
def bfs_8puzzle(start: State, goal: State = GOAL, verbose: bool = False) -> Optional[List[Tuple[str, State]]]:
    if start == goal:
        return [("START", start)]
    if not is_solvable(start):
        return None

    q = deque([start])
    visited = {start}
    parent = {start: None}        # state -> parent state
    action_from = {start: "START"}# state -> action used to reach it

    while q:
        s = q.popleft()
        if verbose:
            print(f"Dequeue (depth≈{depth(parent, s)}):\n{pretty(s)}\n")

        for a, t in neighbors(s):
            if t in visited:
                continue
            visited.add(t)
            parent[t] = s
            action_from[t] = a
            if t == goal:
                return reconstruct(parent, action_from, t)
            q.append(t)

    return None  # not found

def depth(parent, s):
    d = 0
    while parent[s] is not None:
        s = parent[s]
        d += 1
    return d

def reconstruct(parent, action_from, goal_state) -> List[Tuple[str, State]]:
    path = []
    s = goal_state
    while s is not None:
        path.append((action_from[s], s))
        s = parent[s]
    return list(reversed(path))

# ---------- demo ----------
if __name__ == "__main__":
    # easy examples:
    # start = (1,2,3,4,5,6,7,0,8)          # 1 move (Right)
    # start = (1,2,3,4,5,6,0,7,8)          # 2 moves
    start = (1,2,3,5,0,6,4,7,8)            # ~4 moves

    print("Start:\n" + pretty(start))
    print("\nGoal:\n" + pretty(GOAL))

    sol = bfs_8puzzle(start, GOAL, verbose=False)
    if sol is None:
        print("\nNo solution (unsolvable or not found).")
    else:
        print(f"\nSolved in {len(sol)-1} moves:")
        for k, (a, s) in enumerate(sol):
            print(f"\nStep {k}: {a}\n{pretty(s)}")
