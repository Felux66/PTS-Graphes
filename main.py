#Flix
#Marianne

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pygame
import sys

from graph import generate_random_graph
import random
from math import hypot
from consts import *
from gui import GraphGUI, VertexGUI, ColoringAlgo

class Color(QtWidgets.QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)

class ImageWidget(QtWidgets.QWidget):   
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        self.surface = surface

    def paintEvent(self,event):
        
        self.surface.fill(NONE_COLOR)
        
        for edge in self.parent().graph.edges:
            pygame.draw.line(self.surface, (255,255,255), edge[0].pos, edge[1].pos, 2)

        for vertex in self.parent().graph.vertices:
            pygame.draw.circle(self.surface, vertex.border, vertex.pos, vertex.radius, 0)
            pygame.draw.circle(self.surface, vertex.color, vertex.pos, vertex.radius-2, 0)

            font = pygame.font.Font(None, vertex.radius)
            text = font.render(str(vertex), True, (255,255,255))
            text_rect = text.get_rect(center=vertex.pos)
            self.surface.blit(text, text_rect)
        
        w=self.surface.get_width()
        h=self.surface.get_height()
        data=self.surface.get_buffer().raw
        self.image=QtGui.QImage(data,w,h,QtGui.QImage.Format_RGB32)

        my_paint=QtGui.QPainter()  
        my_paint.begin(self)
        my_paint.drawImage(0,0,self.image)
        my_paint.end()

class FormWidget(QtWidgets.QWidget):   
    def __init__(self,parent=None):
        super(FormWidget,self).__init__(parent)
    
        button1 = QPushButton("Redraw")
        button1.clicked.connect(self.redrawGraph)

        combo = QComboBox(self)

        for algo in ColoringAlgo.algos:
            combo.addItem(algo)

        layout = QVBoxLayout()

        layout.addWidget(button1)
        self.setLayout(layout)
        self.show()

    def redrawGraph(self):
        self.parent().graph = self.parent().init_graph()
        self.parent().pygameWidget.repaint()

class MainWidget(QWidget):

    def __init__(self,surface,parent=None):
        super(MainWidget,self).__init__(parent)
        self.surface = surface

        self.initialGraph = generate_random_graph(10, maxNei=4)
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
        ColoringAlgo.color(graph)

        return graph

    def set_points(self, radius=POINTS_DISTANCE):
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

        self.setCentralWidget(self.mainWidget)

pygame.init()
my_surface=pygame.Surface((WIDTH, HEIGHT))
my_surface.fill((200,0,0))
 
app=QtWidgets.QApplication(sys.argv)
my_window=MainWindow(my_surface)
my_window.show()
app.exec_()