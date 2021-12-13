from consts import *
from graph import Vertex

class GraphGUI():
    
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        
        self.graph = self.set_graph()

    def reset_colors(self):
        for v in self.vertices:
            v.color = NONE_COLOR

    def set_graph(self):
        graph = {vertex: [] for vertex in self.vertices}
        
        for edge in self.edges:
            graph[edge[0]].append(edge[1])
            graph[edge[1]].append(edge[0]) 
        
        return graph

    def generate(graph, points):
        vertices = list(points.values())
        edges = set()
        
        for vertex, neighbors in graph.items():
            for neighbor in neighbors:
                v1 = vertices[vertices.index(vertex)]
                v2 = vertices[vertices.index(neighbor)]
                edge = tuple(sorted([v1, v2]))
                edges.add(edge)
        
        return GraphGUI(vertices, edges)

    def __str__(self):
        return "Vertices: "+str(self.vertices)+"\nEdges: "+str(self.edges)

##################################

class VertexGUI(Vertex):
    
    def __init__(self, x, y, id, value=None, name=None, color=NONE_COLOR, border=(255,255,255)):
        super().__init__(self, id, value, name, color)
        self.x = x
        self.y = y
        self.border = border

    def __init__(self, x, y, vertex, border=(255,255,255)):
        super().__init__(vertex.id, vertex.value, vertex.name, vertex.color)
        self.x = x
        self.y = y
        self.border = border
    
    @property
    def pos(self):
        return (self.x, self.y)
    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos
