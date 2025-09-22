import networkx as nx
import matplotlib.pyplot as plt

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    Position nodes in a hierarchy for drawing a tree with networkx + matplotlib.
    """
    if not nx.is_tree(G):
        raise TypeError("The graph is not a tree")

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))
        else:
            root = list(G.nodes)[0]

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, 
                       xcenter=0.5, pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if parent is not None and parent in children:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc-vert_gap, xcenter=nextx, 
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def draw_tree(tree, root, target=None):
    """
    Draws a tree. Marks root in green, target in red (if given).
    """
    G = nx.DiGraph()
    for parent, children in tree.items():
        for child in children:
            G.add_edge(parent, child)

    pos = hierarchy_pos(G, root)

    # default color: lightblue
    colors = []
    for node in G.nodes():
        if node == root:
            colors.append("lightgreen")  # root
        elif node == target:
            colors.append("lightcoral")  # target
        else:
            colors.append("lightblue")

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000,
            node_color=colors, font_size=12, font_weight="bold")
    plt.show()
