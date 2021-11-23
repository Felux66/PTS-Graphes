import random

from pygame.version import ver
from options import Options

def graph_is_valid(graph):
    assert isinstance(graph, dict), "graph sould be a dict"

    def dfs(graph, current=None, visited=[]):
        if current == None:
            current = random.choice(list(graph.keys()))

        visited.append(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited = dfs(graph, neighbor, visited)
        
        return visited

    if any(vertex not in dfs(graph) for vertex in graph.keys()):
        return False

    # Get all neighbors to avoid a missing vertex
    allNeighbors = set(vertex for neighbors in graph.values() for vertex in neighbors)    
    return all(neighbor in graph.keys() for neighbor in allNeighbors) and all(len(neighbors)>0 for neighbors in graph.values())

def graph_is_oriented(graph):
    assert isinstance(graph, dict), "graph sould be a dict"

    # Check if each vertex is a neighbor of its own neighbors
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if vertex not in graph[neighbor]:
                return True
    return False

def get_cycles(graph):
    
    def rec_get_cycles(current, visited, maxCycle=[]):
        visited.append(current)

        for neighbor in graph[current]:

            if neighbor == visited[0] and len(visited)>=3:
                if len(visited) > len(maxCycle):
                    maxCycle = visited.copy()

            if neighbor in visited:
                continue
            
            maxCycle = rec_get_cycles(neighbor, visited.copy(), maxCycle)

        return maxCycle

    vertices = list(graph.keys())
    cycles = []
    while len(vertices) > 0:
        startVertex = vertices[0]
        cycle = rec_get_cycles(startVertex, [])
        if cycle == []:
            vertices.remove(startVertex)
            continue

        cycles.append(cycle)
        for c in cycle:
            if c in vertices:
                vertices.remove(c)

    return cycles

def get_chords_from_cycle(graph, cycle):
    chords = set()
    for vertex in cycle:
        cIdx = cycle.index(vertex)
        for neighbor in graph[vertex]:
            if neighbor in cycle:
                if neighbor not in [cycle[(cIdx+1)%len(cycle)], cycle[cIdx-1]]:
                    chords.add(tuple(sorted([vertex, neighbor])))  
    return chords
    
def generate_random_graph(n=Options.N_VERTICES_RANDGRAPH, minNei=Options.NEIGHBORS_INTERVAL[0], maxNei=Options.NEIGHBORS_INTERVAL[1]):
    assert n >= 2, "n has to be at least 2"

    graph = {k: [] for k in range(n)}

    adjacentMatrix = [[0 for i in range(n)] for j in range(n)]

    allVertices = []
    for i in range(maxNei):
        allVertices += list(range(n))
    
    i = 0
    while i < len(allVertices):
        if adjacentMatrix[allVertices[i]].count(1) >= maxNei:
            i+=1
            continue 
        b = random.getrandbits(1) if adjacentMatrix[allVertices[i]].count(1) >= minNei else 1
        if b:
            idx = random.randint(0, len(allVertices)-1)
            while allVertices[idx] == allVertices[i]:
                idx = random.randint(0, len(allVertices)-1)
                if adjacentMatrix[allVertices[idx]].count(1) >= maxNei:
                    idx = i
            v1 = allVertices.pop(max(i,idx))
            v2 = allVertices.pop(min(i,idx))

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

    """
    
    [    a b c d
       a [0,0,1,0],
       b [0,0,0,0],
       c [1,0,0,0],
       d [1,0,0,0],
    ]
    
    vertices: [1,2,3,4]
    edge: [(1,2), (2,1), (2,3), (3,2)]

    """

    print(graph_is_valid(graph))
    print(graph_is_oriented(graph))

    print('{')
    for i in (g := generate_random_graph(10, maxNei=4)):
        print(f"    {i}: {g[i]}")
    print('}')