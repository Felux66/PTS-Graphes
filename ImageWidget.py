from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pygame

from consts import *
from Gui import VertexGUI
from options import Options

class ImageWidget(QtWidgets.QWidget):   
    def __init__(self,surface,parent=None):
        super(ImageWidget,self).__init__(parent)
        self.surface = surface

        self.setFixedSize(surface.get_width(), surface.get_height())

        self.selected = None
        self.action = None
        self.actionParams = []
        self.actionStep = 0

    def paintEvent(self, event):
        
        self.surface.fill(NONE_COLOR)
        
        for edge in self.parent().graph.edges:
            pygame.draw.line(self.surface, (255,255,255), edge[0].pos, edge[1].pos, 2)

        for vertex in self.parent().graph.vertices:
            bordercol = (0,255,0) if vertex == self.selected else vertex.border
            if self.action == "addEdge" and vertex in self.actionParams:
                bordercol = (0,0,255)
            elif self.action == "delEdge" and vertex in self.actionParams:
                bordercol = (255,0,0)

            pygame.draw.circle(self.surface, bordercol, vertex.pos, Options.POINTS_RADIUS, 0)
            pygame.draw.circle(self.surface, vertex.color, vertex.pos, Options.POINTS_RADIUS-2, 0)

            font = pygame.font.Font(None, int(Options.POINTS_RADIUS*1.5))
            text = font.render(str(vertex), True, (255,255,255))
            text_rect = text.get_rect(center=vertex.pos)
            self.surface.blit(text, text_rect)
    
        if self.action:
            font = pygame.font.Font(None, 34)
            text = font.render(self.action+" (step "+str(self.actionStep)+")", True, (255,0,0,155))
            text_rect = text.get_rect()
            self.surface.blit(text, (10,10))
        
        w=self.surface.get_width()
        h=self.surface.get_height()
        data=self.surface.get_buffer().raw
        self.image=QtGui.QImage(data,w,h,QtGui.QImage.Format_RGB32)

        my_paint=QtGui.QPainter()  
        my_paint.begin(self)
        my_paint.drawImage(0,0,self.image)
        my_paint.end()

    def mousePressEvent(self, QMouseEvent):

        modifiers = QApplication.keyboardModifiers()
        if self.action == None:
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            for vertex in self.parent().graph.vertices:
                center_x, center_y = vertex.x, vertex.y
                if (x - center_x)**2 + (y - center_y)**2 < Options.POINTS_RADIUS**2:
                    self.selected = vertex

            self.repaint()

        elif self.action == "addVertex":
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            
            newName = "0" if len(self.parent().graph.vertices)==0 else str(max([int(v.name) for v in self.parent().graph.vertices])+1)
            newVertex = VertexGUI(x, y, newName)
            
            self.parent().graph.vertices.append(newVertex)
            self.parent().graph.graph = self.parent().graph.set_graph()

            modifiers = QApplication.keyboardModifiers()
            if not bool(modifiers == QtCore.Qt.ControlModifier):
                self.action = None
                self.actionParams = []

            self.repaint()
            
        elif self.action == "addEdge":
            if len(self.parent().graph.vertices)<2:
                self.action = None
                return 

            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            
            selVertex = None
            for vertex in self.parent().graph.vertices:
                center_x, center_y = vertex.x, vertex.y
                if (x - center_x)**2 + (y - center_y)**2 < Options.POINTS_RADIUS**2:
                    selVertex = vertex
            
            if selVertex == None:
                self.action = None
                self.actionParams = []
            elif self.actionStep == 0:
                self.actionParams.append(selVertex)
                self.actionStep = 1

                if bool(modifiers == QtCore.Qt.ControlModifier):
                    self.actionStep = 0

                elif bool(modifiers == QtCore.Qt.ShiftModifier):
                    self.actionStep = 0
                    for v1 in self.actionParams:
                        for v2 in self.actionParams:
                            if v1 == v2:
                                continue

                            edge = tuple(sorted([v1, v2]))
                            self.parent().graph.edges.add(edge)
                
                self.parent().graph.graph = self.parent().graph.set_graph()

                
            elif self.actionStep == 1:
                for v1 in self.actionParams:
                    v2 = selVertex

                    if v1 == v2:
                        continue

                    edge = tuple(sorted([v1, v2]))
                    self.parent().graph.edges.add(edge)
                
                self.parent().graph.graph = self.parent().graph.set_graph()

                if not bool(modifiers == QtCore.Qt.ControlModifier):
                    self.action = None
                    self.actionParams = []
                    self.actionStep = 0

            self.repaint()

        elif self.action == "delVertex":
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            
            selVertex = None
            for vertex in self.parent().graph.vertices:
                center_x, center_y = vertex.x, vertex.y
                if (x - center_x)**2 + (y - center_y)**2 < Options.POINTS_RADIUS**2:
                    selVertex = vertex

            if selVertex == None:
                self.action = None
                return

            self.parent().graph.vertices.remove(selVertex)
            toRem = []
            for edge in self.parent().graph.edges:
                if selVertex in edge:
                    toRem.append(edge)

            for edge in toRem:
                self.parent().graph.edges.remove(edge)
            self.parent().graph.graph = self.parent().graph.set_graph()

            if not bool(modifiers == QtCore.Qt.ControlModifier):
                self.action = None
                self.actionParams = []

            self.repaint()
            
        elif self.action == "delEdge":
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            
            selVertex = None
            for vertex in self.parent().graph.vertices:
                center_x, center_y = vertex.x, vertex.y
                if (x - center_x)**2 + (y - center_y)**2 < Options.POINTS_RADIUS**2:
                    selVertex = vertex
            
            if selVertex == None:
                self.action = None
                self.actionParams = []

            elif self.actionStep == 0:
                self.actionParams.append(selVertex)
                if not bool(modifiers == QtCore.Qt.ControlModifier):
                    self.actionStep = 1
                    
            elif self.actionStep == 1:
                for v1 in self.actionParams:
                    v2 = selVertex
                    edge = tuple(sorted([v1, v2]))
                    if edge in self.parent().graph.edges:
                        self.parent().graph.edges.remove(edge)
                
                self.parent().graph.graph = self.parent().graph.set_graph()

                modifiers = QApplication.keyboardModifiers()
                if not bool(modifiers == QtCore.Qt.ControlModifier):
                    self.action = None
                    self.actionParams = []

            self.repaint()

    def mouseMoveEvent(self, QMouseEvent) -> None:
        if self.selected:
            pos = QMouseEvent.pos()
            x, y = pos.x(), pos.y() 
            self.selected.pos = (x,y)
            self.repaint()

    def mouseReleaseEvent(self, QMouseEvent):
        self.selected = None
        self.repaint()
