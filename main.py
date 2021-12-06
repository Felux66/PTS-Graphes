from PyQt5 import QtWidgets
import sys
import pygame
from graph import EdgesSet
from view.MainWindow import MainWindow

from consts import *

def start_gui():
    pygame.init()
    my_surface=pygame.Surface((WIDTH, HEIGHT))
    my_surface.fill((200,0,0))
    
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    my_window=MainWindow(my_surface)
    my_window.show()
    app.exec_()

def start_schedule():
    from usages.schedule import Group, Course
    from graph import Graph, Vertex, VerticesList

    g1 = Group([1,2,3])
    g2 = Group([4,5,6])
    g3 = Group([1,5,7])
    g4 = Group([8,9,10])
    g5 = Group([11,12,13])

    c1 = Course(3.0, g1)
    c2 = Course(1.5, g2)
    c3 = Course(3.0, g4)
    c4 = Course(2.0, g2)
    c5 = Course(1.0, g5)
    c6 = Course(3.0, g4)
    c7 = Course(1.5, g4)
    c8 = Course(3.0, g3)
    c9 = Course(2.0, g3)

    courses = [c1,c2,c3,c4,c5,c6,c7,c8,c9]
    
    vertices = VerticesList()
    for i,c in enumerate(courses):
        vertices.add(Vertex(i+1, c, 'c'+str(i+1)))
    lV = list(vertices)

    edges = EdgesSet()
    for i,v1 in enumerate(lV):
        for j,v2 in enumerate(lV[i+1:]):
            if any(s in v2.value.group.students for s in v1.value.group.students):
                edges.add((v1, v2))
    
    graph = Graph(vertices, edges)
    print(graph)

    from ColoringAlgos import ColoringAlgos

    ColoringAlgos.color(graph)
    for k in graph:
        print(k.color)

if __name__ == "__main__":
    start_gui()
    # start_schedule()