
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

        radiusEdit = QSlider(QtCore.Qt.Horizontal)
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

        distanceEdit = QSlider(QtCore.Qt.Horizontal)
        distanceEdit.setValue(Options.POINTS_DISTANCE)
        distanceEdit.setMinimum(10)
        distanceEdit.setMaximum(200)
        def changeDistance():
            try:
                Options.POINTS_DISTANCE = int(distanceEdit.value())
            except:
                Options.POINTS_DISTANCE = DEFAULT_POINTS_DISTANCE        
        distanceEdit.valueChanged.connect(changeDistance)

        optionsLayout = QFormLayout()
        optionsLayout.addRow("Vertex radius", radiusEdit)
        optionsLayout.addRow("Vertex distance", distanceEdit)
        self.optionsGroup.setLayout(optionsLayout)

        #######################################

        self.graphGroup = QGroupBox("Random graph")

            ########

        nverticesEdit = QSpinBox()
        nverticesEdit.setAlignment(QtCore.Qt.AlignRight)
        nverticesEdit.setValue(Options.N_VERTICES_RANDGRAPH)
        nverticesEdit.setMinimum(4)
        nverticesEdit.setMaximum(50)

        minEdgeEdit = QSpinBox()
        minEdgeEdit.setAlignment(QtCore.Qt.AlignRight)
        minEdgeEdit.setValue(Options.NEIGHBORS_INTERVAL[0])
        minEdgeEdit.setMinimum(Options.NEIGHBORS_INTERVAL[0])
        minEdgeEdit.setMaximum(Options.NEIGHBORS_INTERVAL[1])

        maxEdgeEdit = QSpinBox()
        maxEdgeEdit.setAlignment(QtCore.Qt.AlignRight)
        maxEdgeEdit.setValue(Options.NEIGHBORS_INTERVAL[1])
        maxEdgeEdit.setMinimum(Options.NEIGHBORS_INTERVAL[0])
        maxEdgeEdit.setMaximum(Options.NEIGHBORS_INTERVAL[1])

        def changeDistance():
            try:
                Options.N_VERTICES_RANDGRAPH = int(nverticesEdit.value())
            except:
                Options.N_VERTICES_RANDGRAPH = DEFAULT_N_VERTICES_RANDGRAPH   
            maxEdgeEdit.setMaximum(Options.N_VERTICES_RANDGRAPH)   
            if maxEdgeEdit.value() >= nverticesEdit.value():
                maxEdgeEdit.setValue(nverticesEdit.value()-1) 
        
        def changeMinEdge():
            try:
                Options.NEIGHBORS_INTERVAL[0] = int(minEdgeEdit.value())
            except:
                Options.NEIGHBORS_INTERVAL[0] = DEFAULT_NEIGHBORS_INTERVAL[0]
            maxEdgeEdit.setMinimum(Options.NEIGHBORS_INTERVAL[0])
        
        def changeMaxEdge():
            try:
                Options.NEIGHBORS_INTERVAL[1] = int(maxEdgeEdit.value())
            except:
                Options.NEIGHBORS_INTERVAL[1] = DEFAULT_NEIGHBORS_INTERVAL[1]
            minEdgeEdit.setMaximum(Options.NEIGHBORS_INTERVAL[1])     
        
        nverticesEdit.valueChanged.connect(changeDistance)   
        minEdgeEdit.valueChanged.connect(changeMinEdge)   
        maxEdgeEdit.valueChanged.connect(changeMaxEdge)

            ########

        def randomGraph():
            self.parent().initialGraph = generate_random_graph(Options.N_VERTICES_RANDGRAPH)
            self.parent().graph = self.parent().init_graph()
            self.parent().pygameWidget.repaint()

        buttonRandomGraph = QPushButton("New graph")
        buttonRandomGraph.clicked.connect(randomGraph)

            ########
            
        graphLayout = QFormLayout()
        graphLayout.addRow("Vertices amount: ", nverticesEdit)
        graphLayout.addRow("Min edge amount: ", minEdgeEdit)
        graphLayout.addRow("Max edge amount: ", maxEdgeEdit)
        graphLayout.addWidget(buttonRandomGraph)
        self.graphGroup.setLayout(graphLayout)
        self.graphGroup.setFixedSize(self.graphGroup.sizeHint())

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

        self.comboWidget = QWidget()
        fLay = QFormLayout()
        fLay.addRow("Add: ", self.comboAlgos)
        self.comboWidget.setLayout(fLay)

        def recolorGraph():            
            graph = self.parent().graph.graph

            if not (graph_is_valid(graph) and not graph_is_oriented(graph)):
                print("Not valid")
                return

            self.parent().graph.reset_colors()
            ColoringAlgo.algos[self.comboAlgos.currentText()](self.parent().graph)

            self.parent().pygameWidget.repaint()

        self.buttonColor = QPushButton("Recolor")
        self.buttonColor.clicked.connect(recolorGraph)

        #######################################

        glay = QGridLayout()

        glay.addWidget(self.optionsGroup, 0, 0, 1, 4)

        glay.addWidget(self.comboWidget, 1, 0, 1, 3)
        glay.addWidget(self.buttonColor, 1, 3)
        glay.addWidget(self.buttonRedraw, 2, 3)
        
        glay.addWidget(self.graphGroup, 3, 0, 1, 4)
        
        self.setLayout(glay)
        self.show()
