from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pygame

from consts import *
from gui import VertexGUI
from options import Options

class ActionWidget(QtWidgets.QWidget):   
    def __init__(self,surface,parent=None):
        super(ActionWidget,self).__init__(parent)

        def addVertexGraph():
            self.parent().pygameWidget.action = "addVertex"
            self.parent().pygameWidget.actionParams = []
            self.parent().pygameWidget.actionStep = 0
            self.parent().pygameWidget.repaint()

        buttonAddVertexGraph = QPushButton("Add vertex")
        buttonAddVertexGraph.clicked.connect(addVertexGraph)

            ########

        def addEdgeGraph():
            self.parent().pygameWidget.action = "addEdge"
            self.parent().pygameWidget.actionParams = []
            self.parent().pygameWidget.actionStep = 0
            self.parent().pygameWidget.repaint()

        buttonAddEdgeGraph = QPushButton("Add edge")
        buttonAddEdgeGraph.clicked.connect(addEdgeGraph)

            ########

        def delVertexGraph():
            self.parent().pygameWidget.action = "delVertex"
            self.parent().pygameWidget.actionParams = []
            self.parent().pygameWidget.actionStep = 0
            self.parent().pygameWidget.repaint()

        buttonDelVertexGraph = QPushButton("Delete vertex")
        buttonDelVertexGraph.clicked.connect(delVertexGraph)

            ########

        def delEdgeGraph():
            self.parent().pygameWidget.action = "delEdge"
            self.parent().pygameWidget.actionParams = []
            self.parent().pygameWidget.actionStep = 0
            self.parent().pygameWidget.repaint()

        buttonDelEdgeGraph = QPushButton("Delete edge")
        buttonDelEdgeGraph.clicked.connect(delEdgeGraph)

            ########
            
        gLayout = QGridLayout()
        gLayout.addWidget(buttonAddVertexGraph, 0, 0)
        gLayout.addWidget(buttonAddEdgeGraph, 0, 1)
        gLayout.addWidget(buttonDelVertexGraph, 0, 2)
        gLayout.addWidget(buttonDelEdgeGraph, 0, 3)
        self.setLayout(gLayout)
