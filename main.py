#Flix
#Marianne

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pygame
import sys

from graph import generate_random_graph
import random
from math import hypot
from consts import *
from gui import GraphGUI, VertexGUI
from options import Options
from ImageWidget import ImageWidget
from FormWidget import FormWidget

class MainWidget(QWidget):

    def __init__(self,surface,parent=None):
        super(MainWidget,self).__init__(parent)
        self.surface = surface

        self.initialGraph = generate_random_graph()
        self.graph = self.init_graph()
        
        self.pygameWidget = ImageWidget(self.surface, self)
        self.formWidget = FormWidget(self)

        layout = QGridLayout()        
        layout.addWidget(self.pygameWidget, 0, 0, 1, 5)
        layout.addWidget(self.formWidget, 0, 5, 1, 2)       

        self.w = int(surface.get_width() + (surface.get_width()*2) / 5)
        self.h = surface.get_height()

        self.setFixedSize(self.w, self.h)
        self.setLayout(layout)
        
    def init_graph(self):
        graph = GraphGUI.generate(self.initialGraph, self.set_points())

        return graph

    def set_points(self, radius=Options.POINTS_DISTANCE):
        graph = self.initialGraph

        w = self.surface.get_width()
        h = self.surface.get_height()

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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,surface,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.surface = surface
        self.mainWidget = MainWidget(surface, self)
        self.pos

        self.setCentralWidget(self.mainWidget)

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width() * 3.5
        y = 2.7 * ag.height() - sg.height() - widget.height()
        self.move(x, y)


pygame.init()
my_surface=pygame.Surface((WIDTH, HEIGHT))
my_surface.fill((200,0,0))
 
app=QtWidgets.QApplication(sys.argv)
my_window=MainWindow(my_surface)
my_window.location_on_the_screen()
my_window.show()
app.exec_()