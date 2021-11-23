import random
from consts import *

class ColoringAlgos:

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
                ColoringAlgos.color(graph,neighbor,visited)
        
        if not hasNone:
            ColoringAlgos.color(graph,None,visited)

    algos = {
        "COLOR": color,
        "COSINE": cosine,
    }
