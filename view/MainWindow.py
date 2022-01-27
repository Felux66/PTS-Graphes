import math
import random

from graph import VerticesList, generate_random_graph

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from view.gui import GraphGUI, VertexGUI
from options import Options
from view.ImageWidget import ImageWidget
from view.FormWidget import FormWidget
from view.ActionWidget import ActionWidget

import usages.schedule.schedule as schedule

class MainWidget(QWidget):

    def __init__(self,surface,parent=None):
        super(MainWidget,self).__init__(parent)
        self.surface = surface

        g = generate_random_graph("NEIGHBORS_AMOUNT")

        self.graph = GraphGUI(g.vertices, g.edges)
        self.init_graph_points()
        
        self.pygameWidget = ImageWidget(self.surface, self)
        self.formWidget = FormWidget(self)
        self.actionWidget = ActionWidget(self)

        #######################################

        layout = QGridLayout()        
        layout.addWidget(self.pygameWidget, 0, 0, 1, 1)
        layout.addWidget(self.formWidget, 0, 1, 2, 1, Qt.AlignTop)
        layout.addWidget(self.actionWidget, 1, 0)       

        self.setLayout(layout)
        
    def init_graph_points(self):
        self.graph = GraphGUI.generate(self.graph, self.set_points())

    def set_points(self):
        graph = self.graph

        n = len(graph.keys())
        shift = 50
        w = self.surface.get_width()-shift*2
        h = self.surface.get_height()-shift*2

        pointSpace = (w*h)/n
        length = math.sqrt(pointSpace)
        
        points = {vertex: None for vertex in graph}

        wn = math.ceil(w/length)
        hn = math.ceil(n/wn)
        
        rand = Options.POINTS_DISTANCE_RANDOMNESS
        k=0
        for i in range(wn):
            for j in range(hn):
                x = (w-(wn-1)*length)/2+shift+i*length+((random.uniform(0,length)-length/2)*rand)
                y = (h-(hn-1)*length)/2+shift+j*length+((random.uniform(0,length)-length/2)*rand)

                try:
                    vertex = list(graph.keys())[k]
                    p = VertexGUI(x, y, vertex=vertex)
                    points[vertex] = p
                except:
                    pass

                k += 1

        def ccw(A,B,C):
            return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

        bestPos = [math.inf, {}]
        lastPos = [math.inf, {}]
        for p in range(Options.POINTS_POSITIONING_ITERATIONS):
            edges = list(set([tuple(sorted([points[vertex], points[neighbor]])) for vertex in graph for neighbor in graph[vertex]]))
            
            intersections = {vertex: 0 for vertex in graph}
            for i in range(len(edges)):
                for j in range(i+1, len(edges)):
                    A, B = edges[i][0], edges[i][1]
                    C, D = edges[j][0], edges[j][1]
                    if A not in [C, D] and B not in [C, D]:
                        if intersect(A,B,C,D):
                            intersections[A] += 1
                            intersections[B] += 1
                            intersections[C] += 1
                            intersections[D] += 1
            
            curPos = [sum(intersections.values())/4, {vertex: points[vertex].pos for vertex in graph}]
            
            if lastPos[0] < curPos[0]:
                curPos = lastPos
            else:
                lastPos = curPos
            
            if bestPos[0] > curPos[0] or bestPos[0] == -1:
                bestPos = curPos

            ordered = sorted(intersections, key=intersections.get, reverse=True)
            if intersections[ordered[0]] == 0: return points
            
            fi, se= ordered[0], random.choice([v for v in ordered if intersections[v] != 0])
            points[fi].pos, points[se].pos = points[se].pos, points[fi].pos

            if bestPos[0] == 0:
                break

        for vertex, pos in bestPos[1].items():
            points[vertex].pos = pos

        pointsV = VerticesList()
        for p in points.values():
            pointsV.add(p)

        return points

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,surface,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.surface = surface
        self.mainWidget = MainWidget(surface, self)
        self.pos

        self.setCentralWidget(self.mainWidget)