import pygame
from graph import generate_random_graph
import random
from math import hypot
from consts import *
from options import Options

class ColoringAlgo:

    def cosine(graph):
        pass

    def color(graph, current=None, visited=None):
        if visited == None:
            visited = []
            
        if len(visited) == len(graph.vertices):
            return

        def set_color(vertex):
            for color in COLORS_ORDER:
                if COLORS[color] not in [neighbor.color for neighbor in graph.graph[vertex]]:
                    current.color = COLORS[color]
                    break

        if current == None:
            current = random.choice(list(set(graph.vertices)-set(visited)))
        
        set_color(current)

        visited.append(current)

        hasNone = False
        for neighbor in graph.graph[current]:
            if neighbor.color == NONE_COLOR:
                hasNone = True
                ColoringAlgo.color(graph,neighbor,visited)
        
        if not hasNone:
            ColoringAlgo.color(graph,None,visited)

    algos = {
        "COLOR": color,
        "COSINE": cosine,
    }

##################################
##################################
##################################

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
