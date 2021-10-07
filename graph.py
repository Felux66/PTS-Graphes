import random
import itertools

def graph_is_valid(graph):
    assert isinstance(graph, dict), "graph sould be a dict"

    # Get all neighbors to avoid a missing vertex
    allNeighbors = set(vertex for neighbors in graph.values() for vertex in neighbors)    
    return all(neighbor in graph.keys() for neighbor in allNeighbors)

def graph_is_oriented(graph):
    assert isinstance(graph, dict), "graph sould be a dict"

    # Check if each vertex is a neighbor of its own neighbors
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if vertex not in graph[neighbor]:
                return False
    return True

def generate_random_graph(n, minNei=1, maxNei=None):
    assert n >= 2, "n has to be at least 2"
    
    if maxNei == None:
        maxNei = n-1

    graph = {k: [] for k in range(n)}

    adjacentMatrix = [[0 for i in range(n)] for j in range(n)]

    allVertices = []
    for i in range(maxNei):
        allVertices += list(range(n))

    i = 0
    while i < len(allVertices):
        b = random.getrandbits(1) if adjacentMatrix[allVertices[i]].count(1) >= minNei else 1
        if b:
            v1 = allVertices.pop(i)
            idx = random.randint(0, len(allVertices)-1)
            while allVertices[idx] == v1:
                idx = random.randint(0, len(allVertices)-1)
            v2 = allVertices.pop(idx)

            adjacentMatrix[v1][v2] = b
            adjacentMatrix[v2][v1] = b

            i -= 1
        i += 1

    for i in range(n):
        graph[i] = [idx for idx in range(n) if adjacentMatrix[i][idx] == 1]

    return graph
    
if __name__ == '__main__':

    graph = {
        'A': ['B', 'C', 'E'],
        'B': ['A', 'D', 'F'],
        'C': ['A', 'G'],
        'D': ['B'],
        'E': ['A', 'F'],
        'F': ['B', 'E'],
        'G': ['C']    
    }

    print(graph_is_valid(graph))
    print(graph_is_oriented(graph))

    print('{')
    for i in (g := generate_random_graph(10, maxNei=4)):
        print(f"    {i}: {g[i]}")
    print('}')