class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial      # initial state
        self.goal = goal            # goal state(s)

    def actions(self, state):
        """Return the list of actions that can be executed from 'state'."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from applying 'action' to 'state'."""
        raise NotImplementedError

    def is_goal(self, state):
        """Return True if 'state' is a goal."""
        return state == self.goal

    def action_cost(self, state, action, state2):
        """Return the cost of performing 'action' to go from state → state2."""
        return 1   # default = unit cost

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        # Needed for priority queue comparisons
        return self.path_cost < other.path_cost