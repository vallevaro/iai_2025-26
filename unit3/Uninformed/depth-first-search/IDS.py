import graph
sep = '  '

# The 'drawing_depth' parameter tracks the drawing depth in the call stack 
# the algorithm is currently at, for visualization purposes.
def DFS(graph, vertex, search_depth, target=None, drawing_depth=1):
    print(sep*drawing_depth + f'Exploring vertex {vertex.entity()}')
    
    result = None
    
    # Add the vertex to 'path' for the search path reconstruction.
    path.append(vertex.entity())
    
    if search_depth == 0:
        # Trivial check #1: searches for None are immediately terminated.
        if target is None:
            print(f' The vertex {target} does not exist')
            return None, False
        
        # Trivial check #2: if the entity is in the starting vertex.
        elif target == vertex.entity():
            result = vertex
            return result, True
        else:
            # Pop the vertex from 'path' - not leading to the solution.
            path.pop()
            return None, True
    elif search_depth > 0:
        any_remaining = False
        for edge in graph.adjacent_edges(vertex):
            # Gets the second endpoint.
            v_2nd_endpoint = edge.opposite(vertex)
            
            # If the vertex is not already in the vertex path...
            if v_2nd_endpoint.entity() not in path:
                # Keep searching at the lower level, from the second endpoint.
                result, remaining = DFS(graph, v_2nd_endpoint, search_depth-1, target, drawing_depth+1)
                print(sep*drawing_depth + f'Returning to vertex {vertex.entity()}')

                # If the search was successful, stop the search.
                if result is not None:
                    return result, True
                if remaining:
                    any_remaining = True
        
        # Pop the vertex from 'path' - not leading to the solution.
        path.pop()
        return None, any_remaining

def IDDFS(graph, vertex, target, search_depth_max=20):
    for search_depth in range(search_depth_max+1):
        print(f'Iteration started - search_depth = {search_depth}')
        result, remaining = DFS(graph, vertex, search_depth, target, 1)
        print('Iteration ended.', end=2*'\n')
        if result is not None:
            return result
        elif not remaining:
            return None