from consts import *
from graph import EdgesSet, Vertex, Graph, VerticesList
import pickle

class GraphGUI(Graph):
    
    def __init__(self, vertices, edges):
        super().__init__()
        
        for v in vertices:
            self.add_vertex(v if isinstance(v, VertexGUI) else VertexGUI(0,0,vertex=v))
        for e in edges:
            v1 = self.vertices[e[0].id]
            v2 = self.vertices[e[1].id]
            self.add_edge((v1,v2))
        
    def reset_colors(self):
        for v in self.vertices:
            v.color = NONE_COLOR

    def set_graph(self):
        graph = {vertex: [] for vertex in self.vertices}
        
        for edge in self.edges:
            graph[edge[0]].append(edge[1])
            graph[edge[1]].append(edge[0]) 
        
        return Graph.graph_from_dict(graph)

    def generate(graph, points):
        vertices = VerticesList()
        edges = EdgesSet()

        for v in points.values():
            vertices.add(v)
        
        for vertex, neighbors in graph.items():
            for neighbor in neighbors:
                v1 = points[points[vertex]]
                v2 = points[points[neighbor]]
        
                edge = [v1, v2]
                edges.add(edge)

        return GraphGUI(vertices, edges)

    def __str__(self):
        return "Vertices: "+str(self.vertices)+"\nEdges: "+str(self.edges)

    def save(self, filename):
        pickle.dump(self, "saves/"+filename+".ggui", pickle.HIGHEST_PROTOCOL)

    def load(filename):
        return pickle.load("saves/"+filename+".ggui")

##################################

class VertexGUI(Vertex):
    
    def __init__(self, x, y, *, vertex=None, id=0, value=None, name=None, color=NONE_COLOR, border=(255,255,255)):
        if isinstance(vertex, Vertex):
            super().__init__(vertex.id, vertex.value, vertex.name, vertex.color)
        else:
            super().__init__(id, value, name, color)
        self.x = x
        self.y = y
        self.border = border

    @property
    def pos(self):
        return (self.x, self.y)
    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos
