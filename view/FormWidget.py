
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from pygame import Color

from consts import *
from graph import generate_random_graph, get_chords_from_cycle, graph_is_oriented, graph_is_valid, get_cycles
from ColoringAlgos import ALGO_FCTS, ColoringAlgos, VerifAlgos
from options import Options

class OptionsForm(QGroupBox):

    def __init__(self, name, parent=None) -> None:
        super(OptionsForm,self).__init__(name, parent)

        self.radiusEdit = QSlider(QtCore.Qt.Horizontal)
        self.randomnessEdit = QSlider(QtCore.Qt.Horizontal)
        self.iterationsEdit = QSpinBox()

        optionsLayout = QFormLayout()
        optionsLayout.addRow(f"Vertex radius ({self.radiusEdit.value()}%)", self.radiusEdit)
        optionsLayout.addRow(f"Positioning randomness ({int(Options.POINTS_DISTANCE_RANDOMNESS*100)}%)", self.randomnessEdit)
        optionsLayout.addRow(f"Positioning iterations", self.iterationsEdit)

        ########   

        def changeRadius():
            try:
                Options.POINTS_RADIUS = int(self.radiusEdit.value())
            except:
                Options.POINTS_RADIUS = DEFAULT_POINTS_RADIUS
            self.parent().parent().pygameWidget.repaint()  

        def changeIterations():
            try:
                Options.POINTS_POSITIONING_ITERATIONS = int(self.iterationsEdit.value())
            except:
                Options.POINTS_POSITIONING_ITERATIONS = DEFAULT_POINTS_POSITIONING_ITERATIONS

        def changeDistance():
            try:
                Options.POINTS_DISTANCE_RANDOMNESS = round(self.randomnessEdit.value()/200,2)
            except:
                Options.POINTS_DISTANCE_RANDOMNESS = DEFAULT_POINTS_DISTANCE_RANDOMNESS   
            optionsLayout.labelForField(self.randomnessEdit).setText(f"Positioning randomness ({int(Options.POINTS_DISTANCE_RANDOMNESS*100)}%)")   

        ########   
               
        self.radiusEdit.valueChanged.connect(changeRadius)
        self.randomnessEdit.valueChanged.connect(changeDistance)
        self.iterationsEdit.valueChanged.connect(changeIterations)

        ########   
        
        self.randomnessEdit.setMinimum(0)
        self.randomnessEdit.setMaximum(200)
        self.randomnessEdit.setValue(Options.POINTS_DISTANCE_RANDOMNESS*200)
        
        self.iterationsEdit.setMinimum(0)
        self.iterationsEdit.setMaximum(1000)
        self.iterationsEdit.setValue(Options.POINTS_POSITIONING_ITERATIONS)

        self.radiusEdit.setValue(Options.POINTS_RADIUS)
        self.radiusEdit.setMinimum(10)
        self.radiusEdit.setMaximum(60)

        optionsLayout.labelForField(self.randomnessEdit).setFixedWidth(optionsLayout.labelForField(self.randomnessEdit).sizeHint().width()+5)
        self.setLayout(optionsLayout)

class RandomizerForm(QTabWidget):

    def __init__(self, parent=None) -> None:
        super(RandomizerForm,self).__init__(parent)

        self.nverticesNeiEdit = QSpinBox()
        self.nverticesNeiEdit.setAlignment(QtCore.Qt.AlignRight)
        self.nverticesNeiEdit.setValue(Options.N_VERTICES_RANDGRAPH)
        self.nverticesNeiEdit.setMinimum(4)
        self.nverticesNeiEdit.setMaximum(50)

        self.nverticesDelEdit = QSpinBox()
        self.nverticesDelEdit.setAlignment(QtCore.Qt.AlignRight)
        self.nverticesDelEdit.setValue(Options.N_VERTICES_RANDGRAPH)
        self.nverticesDelEdit.setMinimum(4)
        self.nverticesDelEdit.setMaximum(50)

        self.minEdgeEdit = QSpinBox()
        self.minEdgeEdit.setAlignment(QtCore.Qt.AlignRight)
        self.minEdgeEdit.setValue(Options.NEIGHBORS_INTERVAL[0])
        self.minEdgeEdit.setMinimum(Options.NEIGHBORS_INTERVAL[0])
        self.minEdgeEdit.setMaximum(Options.NEIGHBORS_INTERVAL[1])

        self.maxEdgeEdit = QSpinBox()
        self.maxEdgeEdit.setAlignment(QtCore.Qt.AlignRight)
        self.maxEdgeEdit.setValue(Options.NEIGHBORS_INTERVAL[1])
        self.maxEdgeEdit.setMinimum(2)
        self.maxEdgeEdit.setMaximum(Options.NEIGHBORS_INTERVAL[1])

        self.probaEdit = QSlider(QtCore.Qt.Horizontal)
        self.probaEdit.setValue(Options.DELETE_PROBABILITY*100)
        self.probaEdit.setMinimum(0)
        self.probaEdit.setMaximum(100)

        self.buttonRandomGraphNei = QPushButton("New graph")
        self.buttonRandomGraphDel = QPushButton("New graph")
            
        #########

        neiLayout = QFormLayout()
        neiLayout.addRow("Vertices amount: ", self.nverticesNeiEdit)
        neiLayout.addRow("Min edge amount: ", self.minEdgeEdit)
        neiLayout.addRow("Max edge amount: ", self.maxEdgeEdit)
        neiLayout.addWidget(self.buttonRandomGraphNei)
        
        delLayout = QFormLayout()
        delLayout.addRow("Vertices amount: ", self.nverticesDelEdit)
        delLayout.addRow(f"Deletion probability ({self.probaEdit.value()}%): ", self.probaEdit)
        delLayout.addWidget(self.buttonRandomGraphDel)

        #########

        def changeVerticesAmountNei():
            Options.N_VERTICES_RANDGRAPH = self.nverticesNeiEdit.value()
            self.nverticesDelEdit.setValue(self.nverticesNeiEdit.value())
            if self.maxEdgeEdit.value() >= self.nverticesNeiEdit.value():
                self.maxEdgeEdit.setValue(self.nverticesNeiEdit.value()-1) 
            self.maxEdgeEdit.setMaximum(self.nverticesNeiEdit.value()-1)

        def changeVerticesAmountDel():
            Options.N_VERTICES_RANDGRAPH = self.nverticesDelEdit.value()
            self.nverticesNeiEdit.setValue(self.nverticesDelEdit.value())
            if self.maxEdgeEdit.value() >= self.nverticesDelEdit.value():
                self.maxEdgeEdit.setValue(self.nverticesDelEdit.value()-1) 
            self.maxEdgeEdit.setMaximum(self.nverticesNeiEdit.value()-1)
        
        def changeMinEdge():
            Options.NEIGHBORS_INTERVAL[0] = self.minEdgeEdit.value()
            self.maxEdgeEdit.setMinimum(Options.NEIGHBORS_INTERVAL[0])
        
        def changeMaxEdge():
            Options.NEIGHBORS_INTERVAL[1] = self.maxEdgeEdit.value()
            self.minEdgeEdit.setMaximum(Options.NEIGHBORS_INTERVAL[1]) 

        def randomGraphNei():
            ColoringAlgos.coloredLimit = 0
            self.parent().parent().initialGraph = generate_random_graph("NEIGHBORS_AMOUNT")
            self.parent().parent().graph = self.parent().parent().init_graph()
            self.parent().parent().pygameWidget.repaint() 

        def randomGraphDel():
            ColoringAlgos.coloredLimit = 0
            self.parent().parent().initialGraph = generate_random_graph("DELETE_PROBABILITY")
            self.parent().parent().graph = self.parent().parent().init_graph()
            self.parent().parent().pygameWidget.repaint() 

        def changeProba():
            delLayout.labelForField(self.probaEdit).setText(f"Deletion probability ({self.probaEdit.value()}%): ")
            Options.DELETE_PROBABILITY = self.probaEdit.value() / 100 

        #########

        self.nverticesNeiEdit.valueChanged.connect(changeVerticesAmountNei)   
        self.nverticesDelEdit.valueChanged.connect(changeVerticesAmountDel)   
        self.minEdgeEdit.valueChanged.connect(changeMinEdge)   
        self.maxEdgeEdit.valueChanged.connect(changeMaxEdge)
        self.probaEdit.valueChanged.connect(changeProba)
        self.buttonRandomGraphNei.clicked.connect(randomGraphNei)
        self.buttonRandomGraphDel.clicked.connect(randomGraphDel)

        delLayout.labelForField(self.probaEdit).setFixedWidth(delLayout.labelForField(self.probaEdit).sizeHint().width())

        #########

        rNF = QWidget()
        rDF = QWidget()

        rNF.setLayout(neiLayout)
        rDF.setLayout(delLayout)

        self.addTab(rNF,"Neighbors")
        self.addTab(rDF,"Delete")

class FormWidget(QtWidgets.QWidget):   
    def __init__(self,parent=None):
        super(FormWidget,self).__init__(parent)
    
        #######################################

        self.optionsGroup = OptionsForm("Options", self)
        self.graphGroup = RandomizerForm(self)
        self.comboAlgos = QComboBox()
        self.buttonColor = QPushButton("Recolor")
        self.buttonRedraw = QPushButton("Redraw")
        self.buttonPreviousStep = QPushButton("<")
        self.buttonNextStep = QPushButton(">")

        #######################################

        def redrawGraph():
            self.parent().graph = self.parent().init_graph()
            self.parent().pygameWidget.repaint()

            self.buttonPreviousStep.setEnabled(False)
            self.buttonNextStep.setEnabled(True)

        def comboAlgo_onChange():
            ColoringAlgos.coloredLimit = 0
            self.parent().graph.reset_colors()
            self.parent().pygameWidget.repaint()

            self.buttonPreviousStep.setEnabled(False)
            self.buttonNextStep.setEnabled(True)

        def recolorGraph():            
            ColoringAlgos.coloredLimit = len(self.parent().graph.vertices)

            self.buttonPreviousStep.setEnabled(True)
            self.buttonNextStep.setEnabled(False)

            self.parent().graph.reset_colors()
            eval("ColoringAlgos."+ALGO_FCTS[self.comboAlgos.currentText()])(self.parent().graph)

            self.parent().pygameWidget.repaint()

        def nextStep():            
            graph = self.parent().graph.graph

            if not (graph_is_valid(graph) and not graph_is_oriented(graph)):
                print("Not valid")
                return

            if not eval("VerifAlgos."+ALGO_FCTS[self.comboAlgos.currentText()])(self.parent().graph.graph):
                print("NE PEUT PAS ETRE COLORIE AVEC")
                return

            ColoringAlgos.coloredLimit += 1
            ColoringAlgos.coloredLimit = min(len(self.parent().graph.vertices), ColoringAlgos.coloredLimit)

            if ColoringAlgos.coloredLimit >= len(self.parent().graph.vertices):
                self.buttonNextStep.setEnabled(False)
            self.buttonPreviousStep.setEnabled(True)

            self.parent().graph.reset_colors()
            eval("ColoringAlgos."+ALGO_FCTS[self.comboAlgos.currentText()])(self.parent().graph)

            self.parent().pygameWidget.repaint()

        def previousStep():            
            graph = self.parent().graph.graph

            if not (graph_is_valid(graph) and not graph_is_oriented(graph)):
                print("Not valid")
                return

            ColoringAlgos.coloredLimit -= 1
            ColoringAlgos.coloredLimit = max(0, ColoringAlgos.coloredLimit)

            if ColoringAlgos.coloredLimit <= 0:
                self.buttonPreviousStep.setEnabled(False)
            self.buttonNextStep.setEnabled(True)

            self.parent().graph.reset_colors()
            eval("ColoringAlgos."+ALGO_FCTS[self.comboAlgos.currentText()])(self.parent().graph)

            self.parent().pygameWidget.repaint()

        #######################################

        self.buttonRedraw.clicked.connect(redrawGraph)
        self.comboAlgos.currentIndexChanged.connect(comboAlgo_onChange)
        self.buttonColor.clicked.connect(recolorGraph)
        self.buttonPreviousStep.clicked.connect(previousStep)
        self.buttonNextStep.clicked.connect(nextStep)

        #######################################

        self.comboWidget = QWidget()
        for algo in ALGO_FCTS:
            self.comboAlgos.addItem(algo)
        fLay = QFormLayout()
        fLay.addRow("Algorithmes:", self.comboAlgos)
        self.comboWidget.setLayout(fLay)
        self.comboWidget.setFixedHeight(self.comboWidget.sizeHint().height())
        self.comboWidget.setFixedWidth(self.comboWidget.sizeHint().width()+20)

        self.buttonPreviousStep.setEnabled(False)
        self.buttonNextStep.setEnabled(True)

        #######################################

        glay = QGridLayout()

        glay.addWidget(self.optionsGroup, 0, 0, 1, 4)

        glay.addWidget(self.comboWidget, 1, 0, 1, 3)
        glay.addWidget(self.buttonColor, 1, 3)
        glay.addWidget(self.buttonPreviousStep, 2, 1)
        glay.addWidget(self.buttonNextStep, 2, 2)
        glay.addWidget(self.buttonRedraw, 3, 3)
        
        glay.addWidget(self.graphGroup, 4, 0, 1, 4)
        
        self.setLayout(glay)
        self.show()
