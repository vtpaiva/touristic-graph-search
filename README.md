# touristic-graph-search

In this situation, the objective was to apply both blind search algorithms and heuristic search algorithms to a problem and place the results of the pair of implementations side by side for comparison and discussion.

The addressed problem was a variation of the traveling salesman problem, where, in a graph representing the geographical points of a city with vertices segmented as tourist spots, non-tourist spots, and the starting point, the goal was to determine a route that visited the maximum number of tourist spots within a set time limit and returned to the starting point. The problem was inspired by a theoretical tourism company that needed to find a bus route to travel through a specific city.

(The code was written in Portuguese.)

<div align = "center">
        <img src="https://i.imgur.com/LYMjZs1.png" 
                alt="Picture" 
                width="auto" 
                height="400" 
                style="display: block; margin: 0 auto" />
</div>

### Blind Search

The algorithm implemented in the code uses a blind search technique, specifically a recursive approach, to find a feasible path in a graph within a given time limit. A graph is represented by a set of nodes, where each node may have edges connecting it to other nodes. Some of these nodes are marked as "touristic points", and the objective of the search is to visit these points while adhering to certain constraints, such as a time limit.

#### Core Functions:
recursiveBlindSearch: This is the heart of the algorithm. It performs a recursive depth-first search (DFS) to explore all possible paths in the graph. Starting from a given node, it explores its neighbors (nodes connected by edges) while checking the time constraint (remaining time).

* **Base Case**: If all touristic points have been visited and the current node is the starting point, the recursion terminates and the solution (a complete cycle) is added to the list of feasible paths.
Recursive Case: For each neighboring node, the algorithm checks if the edge to the neighbor is within the remaining time. If so, it proceeds with a recursive call to explore further, adding nodes to the path and updating the count of visited touristic points.
The function also ensures that the path doesn't revisit nodes that have already been visited (except the starting point when completing a cycle).

* `blindSearch`: This function initiates the recursive search. It starts from the graph's starting point and calls the recursiveBlindSearch function with the specified time limit. After the search is complete, it selects the path that visited the most touristic points. If multiple paths visited the same number of points, the one with the shortest remaining time is preferred.

* `blindSearchTime`: This function measures the time taken to execute the blindSearch algorithm. It records the start time, runs the search, and then calculates the elapsed time.

#### How the Algorithm Works

The graph is generated with random nodes and edges, and some nodes are designated as touristic points.
The blind search begins at the starting point. From there, it explores each connected node recursively, checking the available time and whether the node is a touristic point that hasn't been visited yet.
Whenever all touristic points are visited, and the algorithm returns to the starting point, the path is considered a valid solution. The algorithm continues to search for other paths and eventually selects the path with the maximum number of visited touristic points, while also ensuring that the remaining time is maximized.

* Example Execution:
The code generates a random graph with 50 nodes and executes the blindSearch algorithm with a time limit of 20 units. The result includes the best path found, the number of touristic points visited, and the remaining time.

#### Time Complexity: 

The time complexity of the blind search algorithm is influenced by the depth of the recursion and the number of nodes and edges in the graph. Since the search explores all possible paths recursively, the worst-case time complexity is exponential in nature, particularly if the graph is dense or contains many nodes and edges.

The algorithm does not employ any heuristics or optimizations (such as pruning unpromising paths), which means that in larger graphs, the algorithm may take a long time to complete.

### A* Algorithm for Graph Search

The code provided implements the A* search algorithm, which is an informed search algorithm that combines the strengths of both greedy search and Dijkstra’s algorithm. A* uses a heuristic function to estimate the cost from the current node to the goal, guiding the search towards the most promising paths. In this particular implementation, the graph represents a set of nodes, some of which are touristic points. The objective is to find the best path through the graph, visiting as many of these points as possible while adhering to a time constraint.

### Key Components of the Algorithm

#### 1. **Euclidean Heuristic:**

The heuristic function used in this implementation is the Euclidean distance between two nodes. This provides an estimate of the shortest possible distance from a node to the destination. The Euclidean distance between two points is calculated as:

<p align="center">
$
d(A,B) = \sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}
$
</p>

This heuristic is admissible because it never overestimates the true cost to reach the goal, which is a key property for A* to guarantee finding the optimal solution.

#### 2. A* Search Algorithm (`shortestPath`):

The `shortestPath` function implements the A* algorithm. It aims to find the shortest path from a given origin node to a destination node using the following steps:

*   **Open and Closed Sets:** The open set holds nodes that are candidates for exploration, while the closed set contains nodes that have already been evaluated. Each node in the open set has an associated cost, which is the sum of two components:
    
    *   The cost from the start node to the current node (denoted as *g(n)*).
    *   The heuristic estimate of the cost from the current node to the destination (denoted as *h(n)*).
*   **Node Expansion:** The algorithm iterates by selecting the node from the open set that minimizes the total cost *f(n)=g(n)+h(n)*. It then expands the node's neighbors and adds them to the open set if they haven't been evaluated yet.
    
*   **Goal Check:** If the destination node is reached, the algorithm returns the path and the cost to reach it. If no path exists, it returns `None`.
    

#### 3. **Graph Reduction (`reduceGraph`):**

Before using A* to find the shortest path, the graph is reduced to only the touristic points (including the starting point). This simplification helps to focus the search on the key nodes, reducing the problem's size.

*   **Shortest Path Calculation:** For each pair of touristic points, the algorithm calculates the shortest path using A*. This is done by calling the `shortestPath` function for every pair of touristic nodes in the graph.
    
*   **Graph Update:** Each node's edge list is updated with the shortest path distances to other touristic nodes. Additionally, the real path (the sequence of nodes visited) is stored for later use when constructing the solution.
    

#### 4. **Maximizing Visited Points (`maxPointsPath`):**

The `maxPointsPath` function attempts to visit as many touristic points as possible within the given time limit. Starting from the starting point, it explores the neighboring nodes and greedily selects the one with the minimum cost that fits within the remaining time.

*   **Node Selection:** Among the available neighboring nodes, it chooses the one that results in the least overall cost (sum of travel time and distance to the starting point). This ensures that the search stays within the time limit while maximizing the number of visited points.
    
*   **Path Construction:** The path is built incrementally by adding nodes to the final path as they are visited. Once a node is visited, it is marked, and the algorithm proceeds to the next best candidate node.
    

#### 5. **Heuristic Search Execution Time (`heuristicSearchTime`):**

The function `heuristicSearchTime` measures the time taken to execute the heuristic-based search. It first reduces the graph to the touristic points and then runs the `maxPointsPath` function to find the best route within the time limit. The time taken to execute the search is then returned.

### Example Execution:

In the main block of the code:

1.  A random graph with 50 nodes is generated.
2.  The `maxPointsPath` function is called to find the best route through the reduced graph within a time limit of 180 units. The resulting path, including the nodes visited, is printed.
3.  The time taken for the heuristic search is printed, showing how long the algorithm took to execute.

### Time Complexity:

The time complexity of the A* algorithm is influenced by several factors:

*   **Graph Size:** The number of nodes and edges in the graph affects the number of iterations the algorithm needs to perform.
*   **Heuristic Calculation:** Each node expansion requires the calculation of the heuristic, which can be costly depending on the graph's complexity.
*   **Pathfinding in Reduced Graph:** When reducing the graph, the time complexity increases as the number of shortest path calculations grows. For each pair of touristic points, A* is run, which can be computationally expensive in large graphs.