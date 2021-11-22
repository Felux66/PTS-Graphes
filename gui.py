import pygame
from graph import generate_random_graph
import random
from math import hypot
from consts import *

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
        "COSINE": cosine,
        "Color": color,
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
        graph = {vertex: [] for edge in self.edges for vertex in edge }
        
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


##################################

class VertexGUI():
    
    def __init__(self, x, y, name=None, color=NONE_COLOR, border=(255,255,255), radius=POINTS_RADIUS):
        self.x = x
        self.y = y
        self.name = str(name)
        self.color = color
        self.border = border
        self.radius = radius
    
    @property
    def pos(self):
        return (self.x, self.y)

    def __lt__(self, other):
        return self.name < other.name
    def __eq__(self, other):
        if isinstance(other, str):
            return other==self.name
        if isinstance(other, GraphGUI):
            return other.name==self.name
        return False  
    def __hash__(self):
        return hash(str(self.name))

    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self)


##################################
##################################
##################################

class MainWindow():

    def __init__(self, graph):
        self.width, self.height = WIDTH, HEIGHT
        self.win = pygame.display.set_mode((self.width,self.height))

        self.initialGraph = graph

        self.graph = self.init_graph()

        self.run()
    
    def init_graph(self):
        graph = GraphGUI.generate(self.initialGraph, self.set_points())
        ColoringAlgo.color(graph)

        return graph

    def set_points(self, radius=POINTS_DISTANCE):
        graph = self.initialGraph

        w = self.width
        h = self.height

        points = {vertex: None for vertex in graph}
        while None in points.values():
            vertex = None
            for v in points:
                if points[v] == None:
                    vertex = v
                    break

            p = VertexGUI(random.randint(radius,w-radius), random.randint(radius,h-radius), vertex)

            placing = True
            for a in points.values():
                if a == None:
                    continue

                if hypot(p.x-a.x, p.y-a.y) <= radius:
                    points[vertex] = None
                    placing = False
                    break
            if placing:
                points[vertex] = p

        return points

    def run(self):

        while 1:

            self.win.fill(NONE_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.graph = self.init_graph()
                    if event.key == pygame.K_c:
                        self.graph.reset_colors()

                        ColoringAlgo.color(self.graph)
                        
                    if event.key == pygame.K_p:
                        for i in self.initialGraph:
                            print(f"{i}: {self.initialGraph[i]}")
                    if event.key == pygame.K_KP_0:
                        self.graph.reset_colors()

            for edge in self.graph.edges:
                pygame.draw.line(self.win, (255,255,255), edge[0].pos, edge[1].pos, 2)

            for vertex in self.graph.vertices:
                pygame.draw.circle(self.win, vertex.border, vertex.pos, vertex.radius, 0)
                pygame.draw.circle(self.win, vertex.color, vertex.pos, vertex.radius-2, 0)

                font = pygame.font.Font(None, vertex.radius)
                text = font.render(str(vertex), True, (255,255,255))
                text_rect = text.get_rect(center=vertex.pos)
                self.win.blit(text, text_rect)

            pygame.display.update()

if __name__ == '__main__':
    pygame.init()

    MainWindow(generate_random_graph(10, maxNei=4))
