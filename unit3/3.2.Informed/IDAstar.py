from __future__ import annotations
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Tuple

Node = Hashable
NeighborsFn = Callable[[Node], Iterable[Tuple[Node, float]]]
HeuristicFn = Callable[[Node], float]


class IDAStarResult:
    def __init__(self, path: Optional[List[Node]], cost: float, iterations: int, expanded: int):
        self.path = path
        self.cost = cost
        self.iterations = iterations
        self.expanded = expanded

    def __repr__(self) -> str:
        return f"IDAStarResult(path={self.path}, cost={self.cost}, iterations={self.iterations}, expanded={self.expanded})"


def ida_star(
    start: Node,
    goal: Node,
    neighbors: NeighborsFn,
    h: HeuristicFn,
    *,
    weight: float = 1.0,
    max_iterations: int = 1_000_000,
) -> IDAStarResult:
    """
    Iterative Deepening A* (IDA*) para grafos ponderados.

    Parámetros:
        start: nodo inicial
        goal: nodo objetivo
        neighbors(u): iterable de (v, coste) para cada vecino de u
        h(n): heurística (admisible/consistente para optimalidad)
        weight: ponderación de la heurística (1.0 = A*; >1 acelera, puede perder optimalidad)
        max_iterations: tope de expansiones DFS acumuladas

    Retorna:
        IDAStarResult con (path, cost, iterations, expanded)
        Si no se encuentra camino, path=None y cost=inf.
    """
    assert weight > 0, "weight must be > 0"
    expanded_total = 0
    iterations = 0

    def search(node: Node, g: float, threshold: float, path: List[Node], best_g: Dict[Node, float]) -> Tuple[float, Optional[List[Node]], Optional[float]]:
        """
        DFS limitada por el umbral 'threshold' sobre f = g + w*h.
        Devuelve:
          (f_current, path_found, min_excess)
          - Si encuentra solución: (f_solution, path, None)
          - Si no:                (f_current, None, min_excess_over_threshold)
        """
        nonlocal expanded_total
        f = g + weight * h(node)
        if f > threshold:
            return f, None, f  # excede: candidato a próximo umbral

        if node == goal:
            return f, path.copy(), None

        min_excess = float("inf")
        expanded_total += 1

        # Registro de mejor g por nodo (transposition pruning dentro de esta iteración)
        best_prev = best_g.get(node, float("inf"))
        if g >= best_prev:
            # Ya llegamos a 'node' antes con coste menor: poda
            return f, None, min_excess
        best_g[node] = g

        for v, cost in neighbors(node):
            if cost < 0:
                raise ValueError("Negative edge cost detected; IDA* assumes non-negative costs.")
            if v in path:
                continue  # evita ciclos en el camino actual
            path.append(v)
            f_child, found_path, child_excess = search(v, g + cost, threshold, path, best_g)
            path.pop()
            if found_path is not None:
                return f_child, found_path, None
            if child_excess is not None and child_excess < min_excess:
                min_excess = child_excess

        return f, None, min_excess

    # Umbral inicial
    threshold = weight * h(start)
    path = [start]

    while True:
        if iterations > max_iterations:
            return IDAStarResult(None, float("inf"), iterations, expanded_total)
        iterations += 1
        best_g_this_iter: Dict[Node, float] = {}
        f_val, found_path, min_excess = search(start, 0.0, threshold, path, best_g_this_iter)

        if found_path is not None:
            # Calcular el coste real del camino encontrado
            total_cost = 0.0
            for a, b in zip(found_path, found_path[1:]):
                # reconstruimos el coste con neighbors (puede ser O(E) en peor caso; suficiente para scripts)
                cost_ab = None
                for nb, c in neighbors(a):
                    if nb == b:
                        cost_ab = c
                        break
                if cost_ab is None:
                    raise RuntimeError("Inconsistent neighbors function during cost reconstruction.")
                total_cost += cost_ab
            return IDAStarResult(found_path, total_cost, iterations, expanded_total)

        if min_excess == float("inf"):
            # No hay camino
            return IDAStarResult(None, float("inf"), iterations, expanded_total)

        threshold = min_excess  # siguiente umbral (menor f que excedió)



def dict_neighbors(graph: Dict[Node, Dict[Node, float]]) -> NeighborsFn:
    def _n(u: Node) -> Iterable[Tuple[Node, float]]:
        return graph.get(u, {}).items()
    return _n


if __name__ == "__main__":
    from romania_map import romania_map, h_to_bucharest 
    neighbors = dict_neighbors(romania_map)
    start, goal = "Arad", "Bucharest"
    res = ida_star(start, goal, neighbors, lambda n: h_to_bucharest.get(n, float("inf")))
    print(res)
