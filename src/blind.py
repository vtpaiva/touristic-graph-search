from graph import Graph, Node, plotGraphPoints, printFinalPath, plt, randomGraph
from time import time

# Performa a busca cega recursiva.
def recursiveBlindSearch(graph, currentNode, timeLimit, finalPaths, pointsVisited):
    # Caso todos os pontos turísticos já tenham sido visitados e o nó atual é o nó inicial, pare a recursão.
    if pointsVisited == len(graph.touristicPoints) and currentNode.nodeName == graph.startingPoint.nodeName:
        finalPaths.append(([i.nodeName for  i in currentNode.pastNodes + [currentNode]], pointsVisited, timeLimit))
        return
    
    # Para cada nó ligado ao nó atual, faça uma recursão de busca de soluções.
    for node in currentNode.edgeList.keys():
        if currentNode.getGraphDistance(node) <= timeLimit:
            recursiveBlindSearch(graph, Node(node.nodeName, node.xCoord, node.yCoord, 
                                      pastNodes = currentNode.pastNodes + [currentNode], edgeList = node.edgeList), 
                                      timeLimit - currentNode.getGraphDistance(node), finalPaths,
                                      pointsVisited + 1 if node.isTouristic 
                                      and node.nodeName not in [i.nodeName for i in currentNode.pastNodes] else pointsVisited)
            
        # Caso o nó atual seja o nó inicial, foi completado um ciclo em torno do ponto inicial,
        # então adicione ao vetor de soluções factíveis.
        if currentNode.nodeName == graph.startingPoint.nodeName and currentNode.pastNodes + [currentNode] not in finalPaths:
            finalPaths.append(([i.nodeName for  i in currentNode.pastNodes + [currentNode]], pointsVisited, timeLimit))

# Realize a busca cega.
def blindSearch(graph, timeLimit):
    recursiveBlindSearch(graph, graph.startingPoint, timeLimit, finalPathsList := [], 0)

    bestPath = max(finalPathsList, key = lambda x: (x[1], x[2]))
    
    return (bestPath[0], bestPath[1], timeLimit - bestPath[2])

# Retorna o tempo de execução do algoritmo em um grafo "graph" em um limite de tempo "timeLimit".
def blindSearchTime(graph, timeLimit):
    startTime = time()
    
    blindSearch(graph, timeLimit)
    
    return time() - startTime
    
if __name__ == "__main__":
    blindGraph = randomGraph(50)
    printFinalPath(blindSearch(blindGraph, 20))
    print(blindSearchTime(blindGraph, 20))
    
    pass