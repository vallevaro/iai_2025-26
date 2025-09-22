
#Input Graph
graph = {"S": ["A", "D"], "A": ["S", "B", "C"],
          "B": ["A", "C", "D", "E"], "C": ["A", "B", "G"],
          "D": ["S", "B", "E"], "E": ["B", "D", "G"], "G": ["C", "E"]}
#Input Heuristic
heuristic = {"S": 7, "A": 9, "B": 4, "C": 2, "D": 5, "E": 3, "G": 0}

def greedyBestFirstSearch(graph, start, goal, cost=100):
    """ This Function take Input Graph, Starting State, Goal State and Cost"""
    #Initializing Empty List Name Path
    path = []
    #Initializing total variable to calculate total cost
    total = 0
    #While goal is not reached
    while goal not in path:
        #If starting node not in path, add it to path.
        if start not in path:
            path.append(start)
        child = graph[start]
        #For each neighbor of starting node
        for i in child:
            #If heuristic of node is smaller than cost, then set heuristic as cost and neighbor node as starting node.
            if heuristic[i] < cost:
                cost = heuristic[i]
                start = i
        #Calculate total as sum of total and cost.
        total = total + cost
    return path,total
    
print("Path given by greedy best first serach: ",greedyBestFirstSearch(graph, "S", "G"))






