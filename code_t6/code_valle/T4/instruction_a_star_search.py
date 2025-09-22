# At a high level, A* algorithm works as follows:

# Initialize open and closed list of nodes
# Set starting node as current node
# Loop until solution found:
# Consider current node’s neighbors
# Add neighbors to open list
# Set f-cost for each neighbor (g+h)
# Sort open list by lowest f-cost
# Set lowest f-cost node as current node
# Move current node to closed list
# Reconstruct path by traversing pointers backwards from goal
# Where:

# g = cost to move from starting point to current node
# h = estimated cost to move from current node to goal (heuristic)
# f = total estimated cost of path through node (f=g+h)