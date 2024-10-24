import numpy as np, math, copy, time, random, sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)

# Classe grafo com ponto inicial, arestas, nós e pontos turísticos
class Graph:
    def __init__(self, *args) -> None:
        self.startingPoint = args[0]
        self.edges = {i.nodeName:i.edgeList for i in args}
        self.nodes, self.touristicPoints = args, [i for i in args if i.isTouristic]
    
# Classe nó com nome, coordenadas e variáveis para o algoritmo A*
class Node:
    def __init__(self, nodeName, xCoord, yCoord, timeSpent = 0, isTouristic =  False, edgeList = None, pastNodes = None) -> None:
        self.nodeName = nodeName
        self.xCoord, self.yCoord = xCoord, yCoord
        self.timeSpent = timeSpent
        self.isTouristic = isTouristic
        self.isVisited = False
        self.pastNodes = pastNodes if pastNodes != None else []
        self.edgeList = edgeList if edgeList != None else {}
        self.realPath = {}
        
    def __repr__(self) -> str:
        return f"\"{self.nodeName}\" at ({self.xCoord}, {self.yCoord})"
    
    def addEdges(self, *args):
        self.edgeList.update({i[0] if isinstance(i, tuple) else 
                              i: i[1] if isinstance(i, tuple) else 1 for i in args})
        
    def getEuclideanDistance(self, other) -> float:
        return math.sqrt((self.xCoord - other.xCoord)**2 + (self.yCoord - other.yCoord)**2)
    
    def getGraphDistance(self, other) -> float:
        if self is other:
            return 0
        
        return self.edgeList.get(other, np.inf)

# Imprime o resultado final de uma busca
def printFinalPath(bestPath):
    print(" -> ".join(bestPath[0]), f"| Pontos visistados: {bestPath[1]} | Custo: {bestPath[2]}")
    
def randomGraph(n, xLowerLimit = -100.0, xUpperLimit = 100.0, yLowerLimit = -100.0, yUpperLimit = 100.0):
    nodes = [Node(f"Start", random.uniform(xLowerLimit, xUpperLimit), random.uniform(yLowerLimit, yUpperLimit))]
    
    for i in range(n):
        x = random.uniform(xLowerLimit, xUpperLimit)  # Coordenadas como números flutuantes
        y = random.uniform(yLowerLimit, yUpperLimit)
        nodes.append(Node(f"Node{i}", x, y, isTouristic = random.random() < 0.4))
        
    minEdge, maxEdge = n // 4, n // 2

    # Adicionando arestas com pesos aleatórios
    for node in nodes:
        possible_edges = [n for n in nodes if n != node and n not in [e[0] for e in node.edgeList]]
        number_of_edges = np.random.randint(minEdge, maxEdge)
        for edge_node in random.sample(possible_edges, number_of_edges):
            weight = random.uniform(1.0, node.getEuclideanDistance(edge_node) // 3)
            node.addEdges((edge_node, weight))

    return Graph(*nodes)

# Plota os pontos de um grafo.
def plotGraphPoints(graph):
    plt.figure(figsize=(10, 8))
    ax = plt.gca()

    for point in graph.nodes:
        for edgePoint in point.edgeList:
            plt.annotate(
                '', 
                xy=(edgePoint.xCoord, edgePoint.yCoord), 
                xytext=(point.xCoord, point.yCoord),
                arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', linewidth=0.7)
            )

        if point == graph.startingPoint:
            plt.plot(point.xCoord, point.yCoord, 'go', markersize=10, label='Starting Point' if point == graph.startingPoint else "")  # Verde para o ponto inicial
        else:
            plt.plot(point.xCoord, point.yCoord, 'rs' if point.isTouristic else 'ko', markersize=8, label='Touristic' if point.isTouristic else "Non-Touristic")

        ax.annotate(
            f'{point.nodeName}', 
            (point.xCoord, point.yCoord), 
            textcoords="offset points", 
            xytext=(12,-12), 
            ha='center'
        )

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.show()