from graph import Graph, Node, plotGraphPoints, printFinalPath, randomGraph
import numpy as np, copy, matplotlib.pyplot as plt, time

# Heurística de distância euclidiana
def euclideanHeuristic(originNode, destinyNode):
    return originNode.getEuclideanDistance(destinyNode)   

# Algoriitmo do A*
def shortestPath(graph, heuristic, originNode, destinyNode):
    if originNode == destinyNode:
        return originNode, 0, 1
    
    openNodes, closedNodes = [], set()

    currentNode = (Node(originNode.nodeName, originNode.xCoord, originNode.yCoord), 0, heuristic(originNode, destinyNode))
    
    openNodes.append(currentNode)

    # Enquanto houverem nós abertos continue a busca a solução    
    while openNodes:
        closedNodes.add(currentNode[0].nodeName)
        
        # Caso o nó destino seja atingido, pare a recursão e retorne a rota
        if currentNode[0].nodeName == destinyNode.nodeName:
            return currentNode[0].pastNodes + [currentNode[0]], currentNode[1]
        
        # Escolha, dentre os nós abertos, o que possui menor função de custo
        
        currentNeighbors = graph.edges[currentNode[0].nodeName]
        
        openNodes.extend([(Node(i.nodeName, i.xCoord, i.yCoord, pastNodes = currentNode[0].pastNodes + [currentNode[0]], timeSpent = j + currentNode[0].timeSpent), 
        j + currentNode[0].timeSpent, heuristic(i, destinyNode)) for i, j in currentNeighbors.items() if i.nodeName not in closedNodes])
        
        tmpNode = min(openNodes, key = lambda x:(x[1] + x[2]))
        
        if currentNode in openNodes:
            openNodes.remove(currentNode)

        currentNode = tmpNode
        
    # Caso não exista uma rota ligando os nós, retorne None
    return None, np.inf

# Redução do Grafo a apenas pontos turísticos
def reduceGraph(originalGraph):
    touristicPointsCopy = copy.deepcopy([originalGraph.startingPoint] + originalGraph.touristicPoints)
    
    for i in touristicPointsCopy:
        shortestPathList = {node : shortPath for node in touristicPointsCopy if i != node and 
                            (shortPath := shortestPath(originalGraph, euclideanHeuristic, i, node))[1] != np.inf}
        
        i.edgeList = {a:  b[1] for a, b in shortestPathList.items()}
        i.realPath = {a : b[0][1:] for a, b in shortestPathList.items()}
                
    return Graph(*touristicPointsCopy)

# Função para encontrar melhor rota
def maxPointsPath(reducedGraph, timeLimit):
    startPoint = reducedGraph.startingPoint
    
    finalPath, currentNode = [startPoint.nodeName], startPoint
    timeSpent = pointsVisited = 0
        
    # Enquanto houverem nós que são candidatos a nós futuros, percorra o grafo
    while (avaiable := [(i, j) for i, j in currentNode.edgeList.items() if not i.isVisited and i != startPoint
                        and j + timeSpent + i.getGraphDistance(startPoint) <= timeLimit]):
        
        # Selecione o mínimo dentro os nós possíveis
        currentEdge = min(avaiable, key = lambda x: x[1])
        
        timeSpent += currentEdge[1]
        
        finalPath.extend(i.nodeName for i in currentNode.realPath.get(currentEdge[0]))
        
        currentNode = currentEdge[0]
        
        currentNode.isVisited = True
        
        pointsVisited += 1

    return (finalPath + [i.nodeName for i in currentNode.realPath.get(startPoint, [])], 
            pointsVisited, timeSpent + currentNode.getGraphDistance(startPoint))
    
# Retorna o tempo de execução do algoritmo da busca informada
def heuristicSearchTime(graph, timeLimit):
    startTime = time.time()
    
    reduced_graph = reduceGraph(graph)
    
    maxPointsPath(reduced_graph, timeLimit)
    
    return time.time() - startTime

if __name__ == "__main__":
    graph = randomGraph(50)
    printFinalPath(maxPointsPath(reduceGraph(graph), 180))
    print(heuristicSearchTime(graph, 180))
    
    pass