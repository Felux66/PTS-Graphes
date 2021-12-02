from consts import *

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
                v1 = vertices[vertices.index(str(vertex))]
                v2 = vertices[vertices.index(str(neighbor))]
                edge = tuple(sorted([v1, v2]))
                edges.add(edge)
        
        return GraphGUI(vertices, edges)

    def __str__(self):
        return "Vertices: "+str(self.vertices)+"\nEdges: "+str(self.edges)


##################################

class VertexGUI():
    
    def __init__(self, x, y, name=None, color=NONE_COLOR, border=(255,255,255)):
        self.x = x
        self.y = y
        self.name = str(name)
        self.color = color
        self.border = border
    
    @property
    def pos(self):
        return (self.x, self.y)
    @pos.setter
    def pos(self, pos):
        self.x, self.y = pos

    def __lt__(self, other):
        return self.name < other.name
    def __eq__(self, other):
        if isinstance(other, str):
            return other==self.name
        if isinstance(other, GraphGUI):
            return other.name==self.name
        if isinstance(other, VertexGUI):
            return other.name==self.name
        return False  
    def __hash__(self):
        return hash(str(self.name))

    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self)
