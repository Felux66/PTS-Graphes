import random
from consts import *
from graph import *
from pysat.solvers import Minisat22

from view.gui import GraphGUI

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
    "BIPARTITE" : "bipartite"
}

class ColoringAlgos:
    
    coloredLimit = 10000

    def verification(function):
        def other(graph):
            assert isinstance(graph, Graph), "Graph required, "+type(graph).__name__+" found"

            if not (graph_is_valid(graph) and not graph_is_oriented(graph)):
                print("Not valid")
                return

            algo = function.__name__
            if eval("VerifAlgos."+algo)(graph):
                function(graph)
            else:
                print("NE PEUT PAS ETRE COLORIE AVEC")
        return other
    
    @verification
    def sat(graph):
        
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

        global_sat(graph)

    ##############################
    ##############################
    ##############################

    @verification
    def color(graph):
        def global_color(graph):

            for vertex in graph.vertices:
                for color in COLORS_ORDER:
                    if color not in [neighbor.color for neighbor in graph[vertex]]:
                        vertex.color = color
                        break

        global_color(graph)

    ##############################
    ##############################
    ##############################

    @verification
    def cosine(graph):
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

        global_cosine(graph)

    ##############################
    ############################## 
    ############################## 

    @verification
    def dsatur(graphGui):
        
        def sort_by_degree(graph):
        
            dic={}
            for i in graph.vertices:
                dic[i]=len(graph.graph[i])
            
            #the dictionary is sorted by value and exported as a list in descending order
            output=[i[0] for i in sorted(dic.items(), key=lambda x:x[1])]
            
            return output[::-1]

        
        def global_dsatur(graph):
            #Tri des sommets par leurs degré et on choisit le sommet avec le plus grand degré
            selected_vertex=sort_by_degree(graph)[0]
        
            #initialisation du degré de saturation
            saturation_degrees=dict(zip(graph.vertices,[0]*len(graph.vertices)))
        
     
            #La limite sup du nb chromatique est égale au degré maximal du sommet +1.
            chromatic_number_upper_bound=range(len(graph.graph[selected_vertex])+1)
        
            
            #On attribue la première couleur au sommet avec le degré maximum
            color_assignments={}
            color_assignments[selected_vertex]=0
            selected_vertex.color = COLORS_ORDER[0]
            
        
            #remplir chaque sommet avec une couleur
            while len(color_assignments)<len(graph.vertices):
              
           
                #Suppression d'un sommet coloré 
                saturation_degrees.pop(selected_vertex)
        
               #Mise à jour des degrés de saturation après l'attribution des couleurs
                for node in graph.graph[selected_vertex]:
                    if node in saturation_degrees:
                        saturation_degrees[node]+=1
        
                #parmi les sommets non colorés, on choisit un sommet avec le plus grand degré de saturation
                check_vertices_degree=[node for node in saturation_degrees if saturation_degrees[node]==max(saturation_degrees.values())]
        
                #En cas égalité, on choisit celui qui a le plus grand degré.
                if len(check_vertices_degree)>1:
                    degree_distribution=[len(graph.graph[node]) for node in check_vertices_degree]
                    selected_vertex=check_vertices_degree[degree_distribution.index(max(degree_distribution))]
                else:
                    selected_vertex=check_vertices_degree[0]
        
                #Exclusion des couleurs utilisées par les voisins et attribution de la couleur la plus faible possible au sommet sélectionné
                excluded_colors=[color_assignments[node] for node in graph.graph[selected_vertex] if node in color_assignments]
                #print(excluded_colors)
                #print(selected_vertex)
                selected_color=[color for color in chromatic_number_upper_bound if color not in excluded_colors][0]
                color_assignments[selected_vertex]=selected_color
                selected_vertex.color = COLORS_ORDER[selected_color]
                
            print(color_assignments, graph.graph)
        
        
        global_dsatur(graphGui)

    ##############################
    ############################## 
    ############################## 
    @verification
    def bipartite(graph):
        def global_bipartite() :
            current, other = set(), set()
            col1, col2 = COLORS_ORDER[0:2]
            pile = set()
            pile.add(list(graph.keys())[0])
            visited = []
            while len(pile) != 0:
                newPile = set()
                for vertex in pile-(set(visited)):
                    current.update(graph[vertex])
                    newPile.update(graph[vertex])
                    visited.append(vertex)
                    vertex.color=col1

                pile = newPile.copy()
                current, other = other.copy(), current.copy()
                col1,col2 = col2,col1
        global_bipartite(graph)


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
    
    def dsatur(graph):
        return True
    def bipartite(graph):
        return graph_is_barpartite(graph)