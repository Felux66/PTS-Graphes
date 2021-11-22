
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from consts import *
from graph import generate_random_graph, graph_is_oriented, graph_is_valid
from gui import ColoringAlgo
from options import Options

class FormWidget(QtWidgets.QWidget):   
    def __init__(self,parent=None):
        super(FormWidget,self).__init__(parent)
    
        #######################################

        self.optionsGroup = QGroupBox("Options")

            ########

        radiusEdit = QSpinBox()
        radiusEdit.setAlignment(QtCore.Qt.AlignRight)
        radiusEdit.setValue(Options.POINTS_RADIUS)
        radiusEdit.setMinimum(10)
        radiusEdit.setMaximum(60)
        def changeRadius():
            try:
                Options.POINTS_RADIUS = int(radiusEdit.value())
            except:
                Options.POINTS_RADIUS = DEFAULT_POINTS_RADIUS
            self.parent().pygameWidget.repaint()            
        radiusEdit.valueChanged.connect(changeRadius)

            ########

        distanceEdit = QSpinBox()
        distanceEdit.setAlignment(QtCore.Qt.AlignRight)
        distanceEdit.setValue(Options.POINTS_DISTANCE)
        distanceEdit.setMinimum(10)
        distanceEdit.setMaximum(200)
        def changeDistance():
            try:
                Options.POINTS_DISTANCE = int(distanceEdit.value())
            except:
                Options.POINTS_DISTANCE = DEFAULT_POINTS_DISTANCE        
        distanceEdit.valueChanged.connect(changeDistance)

            ########

        optionsLayout = QFormLayout()
        optionsLayout.addRow("Vertex radius", radiusEdit)
        optionsLayout.addRow("Vertex distance", distanceEdit)
        self.optionsGroup.setLayout(optionsLayout)

        #######################################

        self.graphGroup = QGroupBox("Graph")

            ########

        nverticesLabel = QLabel("Vertices amount: ")

        nverticesEdit = QSpinBox()
        nverticesEdit.setAlignment(QtCore.Qt.AlignRight)
        nverticesEdit.setValue(Options.N_VERTICES_RANDGRAPH)
        nverticesEdit.setMinimum(4)
        nverticesEdit.setMaximum(50)
        def changeDistance():
            try:
                Options.N_VERTICES_RANDGRAPH = int(nverticesEdit.value())
            except:
                Options.N_VERTICES_RANDGRAPH = DEFAULT_N_VERTICES_RANDGRAPH        
        nverticesEdit.valueChanged.connect(changeDistance)

            ########

        def addVertexGraph():
            self.parent().pygameWidget.action = "addVertex"
            self.parent().pygameWidget.repaint()

        buttonAddVertexGraph = QPushButton("Add vertex")
        buttonAddVertexGraph.clicked.connect(addVertexGraph)

            ########

        def addEdgeGraph():
            self.parent().pygameWidget.action = "addEdge"
            self.parent().pygameWidget.repaint()

        buttonAddEdgeGraph = QPushButton("Add edge")
        buttonAddEdgeGraph.clicked.connect(addEdgeGraph)

            ########

        def delVertexGraph():
            self.parent().pygameWidget.action = "delVertex"
            self.parent().pygameWidget.repaint()

        buttonDelVertexGraph = QPushButton("Delete vertex")
        buttonDelVertexGraph.clicked.connect(delVertexGraph)

            ########

        def delEdgeGraph():
            self.parent().pygameWidget.action = "delEdge"
            self.parent().pygameWidget.repaint()

        buttonDelEdgeGraph = QPushButton("Delete edge")
        buttonDelEdgeGraph.clicked.connect(delEdgeGraph)

            ########

        def randomGraph():
            self.parent().initialGraph = generate_random_graph(Options.N_VERTICES_RANDGRAPH)
            self.parent().graph = self.parent().init_graph()
            self.parent().pygameWidget.repaint()

        buttonRandomGraph = QPushButton("Generate random graph")
        buttonRandomGraph.clicked.connect(randomGraph)

            ########
            
        graphLayout = QGridLayout()
        graphLayout.addWidget(nverticesLabel, 0, 0)
        graphLayout.addWidget(nverticesEdit, 0, 1)
        graphLayout.addWidget(buttonAddVertexGraph, 1, 0)
        graphLayout.addWidget(buttonAddEdgeGraph, 1, 1)
        graphLayout.addWidget(buttonDelVertexGraph, 2, 0)
        graphLayout.addWidget(buttonDelEdgeGraph, 2, 1)
        graphLayout.addWidget(buttonRandomGraph, 3, 1)
        self.graphGroup.setLayout(graphLayout)

        #######################################

        def redrawGraph():
            self.parent().graph = self.parent().init_graph()
            self.parent().pygameWidget.repaint()

        self.buttonRedraw = QPushButton("Redraw")
        self.buttonRedraw.clicked.connect(redrawGraph)

        #######################################

        self.comboAlgos = QComboBox()
        for algo in ColoringAlgo.algos:
            self.comboAlgos.addItem(algo)

        def recolorGraph():
            graphGui = self.parent().graph
            
            graph = {vertex.name: [] for vertex in self.parent().graph.vertices}
            for edge in self.parent().graph.edges:
                graph[edge[0]].append(edge[1])
                graph[edge[1]].append(edge[0])
            
            if not (graph_is_valid(graph) and not graph_is_oriented(graph)):
                return

            print(self.parent().graph)
            print(graph)

            self.parent().graph.reset_colors()
            ColoringAlgo.algos[self.comboAlgos.currentText()](self.parent().graph)

            self.parent().pygameWidget.repaint()

        self.buttonColor = QPushButton("Recolor")
        self.buttonColor.clicked.connect(recolorGraph)

        #######################################

        glay = QGridLayout()

        glay.addWidget(self.optionsGroup, 0, 0, 1, 5)
        glay.addWidget(self.graphGroup, 0, 5, 1, 5)
        glay.addWidget(QLabel("Algo: "), 1, 0)
        glay.addWidget(self.comboAlgos, 1, 1, 1, 8)
        glay.addWidget(self.buttonColor, 1, 9)
        glay.addWidget(self.buttonRedraw, 2, 9)
        
        self.setLayout(glay)
        self.show()
