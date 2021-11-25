import random
from consts import *
from graph import *
from pysat.solvers import Minisat22

from gui import GraphGUI

"""

ASTUCES POUR IMPLEMENTER UN NOUVEL ALGO:

    Le gui comporte un élément principal GraphGUI qui contient:
        vertices: liste des VertexGUI (sommets pour l'interface)
        edges: listes des couples (v1, v2) avec v1 et v2 les deux VertexGUI qui composent l'arête
        graph: le graph sous la forme [0: [1,3], 1: [0,2,3], ...]

    Créez un méthode principale dans la classe pour lancer l'algo qui prend en paramètre le GraphGUI
    Travaillez ensuite avec des fonctions à l'intérieur de la méthode comme dans l'exemple du SAT

    Vous pouvez identifier un VertexGUI en le comparant avec un string ou un VertexGUI, c'est le nom 
    du sommet qui sera comparé.

    Pour modifier la couleur sur l'interface, il suffit de faire vertex.color = new_color avec:
        vertex: le VertexGUI
        new_color: le nom de la couleur (ex: red, green, ...)

    Dans l'exemple du SAT, Félix a travaillé sur le graphe en liste. Il a juste fallu modifier la
    couleur en parcourant la liste des VertexGUI en les identifiant par leur nom (cf. l'algo) 

    Dans l'exemple de COLOR, j'ai travaillé directement sur le GraphGUI, cela marche tout aussi bien, quoique
    peut-être un peu plus complexe si vous n'êtes pas à l'aise avec le code


PENSEZ A AJOUTER VOTRE ALGO DANS LE DICTIONNAIRE algos A LA FIN DE LA CLASSE AVEC:
    key: le nom de l'algo qui va apparaître dans l'interface
    value: la méthode principale qui sera appelée pour lancer l'algo

IL FAUT AJOUTER UNE METHODE DANS LA CLASSE VerifAlgos AVEC LE MEME NOM QUE DANS ColoringAlgo QUI VERIFIE
SI LE GRAPH PEUT OU NON ETRE COLORIE VIA CET ALGORITHME (retourne donc un booléen)

"""

ALGO_FCTS = {
    "COLOR": "color",
    "SAT": "sat",
    "COSINE": "cosine",
}

class ColoringAlgos:
    
    coloredLimit = 0

    def verification(function):
        def other(graph):
            assert isinstance(graph, GraphGUI), "GraphGUI required, "+type(graph).__name__+" found"

            if not (graph_is_valid(graph.graph) and not graph_is_oriented(graph.graph)):
                print("Not valid")
                return

            algo = function.__name__
            if eval("VerifAlgos."+algo)(graph.graph):
                function(graph)
            else:
                print("NE PEUT PAS ETRE COLORIE AVEC")
        return other
    
    @verification
    def sat(graphGui):
        
        #fonction qui a un sommet e et à une couleur c associe un nombre
        def encode(e,c,x,y):
            # print (e)
            # print(c)
            # print(x)
            # print(y)
            ne = len(e) #7
            return 1 + e.index(x) + ne * c.index(y)

        #Fonction inverse de decode étant donné un nombre n représentant une paire(x,y), renvoie la paire.
        def decode(e,c,n):
            m=n-1
            ne = len(e)
            return (e[m % ne], c[m//ne])

        def global_sat(graph):            
            c = COLORS_ORDER # ['red','blue','green','yellow','orange','purple','pink','white','black','brown','cyan']
            e=[]
            for s in graph.keys():
                e.append(s)
            l = []
            for init,vois in graph.items():
                for vois_courant in vois:
                    l.append((init,vois_courant))

            #pour tout sommet e , il existe une couleur c, telle que les arrêtes l sont coloriés avec une couleur c.
            p1 = [[encode(e,c,x,y) for y in c] for x in e]


            #Chaque sommet a au plus une couleur
            p2 = [[-encode(e,c,x, y1), -encode(e,c,x, y2)] for x in e
                    for y1 in c
                    for y2 in c
                    if y1 < y2]

            #Deux sommet voisins ne peuvent avoir la même couleur
            psi = [[-encode(e,c,x1, y), -encode(e,c,x2, y)] for (x1, x2) in l
                    for y in c]

            ## On instancie le solver
            with Minisat22(bootstrap_with=p1+p2+psi) as m:
                if m.solve():
                    model = [decode(e,c,v) for v in m.get_model() if v > 0] # on récupère lesvariables qui sont vraies dans la solution trouvée
                    # On affiche le résultat lisiblement
                    #l = max([len(s) for s in e])
                    coloredVertices=0
                    for (x,y) in model:
                        #p = l - len(x)
                        #print(x, " "*(p+1), "-> ", y)
                        for vertex in graph.keys():
                            if vertex == x:
                                #print(x,' -> ',y)
                                if coloredVertices >= ColoringAlgos.coloredLimit:
                                    return

                                vertex.color = y  
                                coloredVertices += 1

        global_sat(graphGui.graph)

    ##############################
    ##############################
    ##############################

    @verification
    def color(graphGui):
        def rec_color(graph, current=None, visited=[]):                
            if len(visited) >= ColoringAlgos.coloredLimit:
                return

            if current == None:
                current = list(set(graph.keys())-set(visited))[0]
            
            for color in COLORS_ORDER:
                if color not in [neighbor.color for neighbor in graph[current]]:
                    current.color = color
                    break

            visited.append(current)

            for neighbor in graph[current]:
                if neighbor.color == NONE_COLOR:
                    rec_color(graph, neighbor, visited)

        rec_color(graphGui.graph)

    ##############################
    ##############################
    ##############################

    @verification
    def cosine(graphGui):
        def global_cosine(graph):
            coloredVertices = 0
            noColorVertices = [vertex for vertex in graph]
            colorIdx = 0
            while len(noColorVertices) != 0:
                if coloredVertices >= ColoringAlgos.coloredLimit:
                    return

                noNeighborC = [vertex for vertex in noColorVertices if all(neighbor.color != COLORS_ORDER[colorIdx] for neighbor in graph[vertex])]

                if len(noNeighborC) == 0:
                    colorIdx += 1

                A = [vertex for vertex in noColorVertices if any(neighbor.color == COLORS_ORDER[colorIdx] for neighbor in graph[vertex])]

                nbNeighborsInA = {vertex: len([neighbor for neighbor in graph[vertex] if neighbor in A]) for vertex in noNeighborC}
                maxVertex = noColorVertices[0] if len(A) == 0 else max(nbNeighborsInA, key=nbNeighborsInA.get)

                maxVertex.color = COLORS_ORDER[colorIdx]
                coloredVertices += 1

                noColorVertices = [vertex for vertex in graph if vertex.color == NONE_COLOR]

        global_cosine(graphGui.graph)

    ##############################
    ############################## 
    ############################## 

class VerifAlgos:

    def cosine(graph):

        cycles = get_cycles(graph)
        for cycle in cycles:
            n = len(cycle)
            if n >= 5 and n%2 != 0:
                chords = get_chords_from_cycle(graph, cycle)
                if len(chords) > 2:
                    return False
        return True

    def sat(graph):
        return True

    def color(graph):
        return True