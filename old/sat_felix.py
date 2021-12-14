from pysat.solvers import Minisat22
import graph
from consts import *

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


def global_sat(graphe):

    c = COLORS_ORDER # ['red','blue','green','yellow','orange','purple','pink','white','black','brown','cyan']
    e=[]
    for s in graphe.keys():
        e.append(s)
    l = []
    for init,vois in graphe.items():
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
            for (x,y) in model:
                #p = l - len(x)
                #print(x, " "*(p+1), "-> ", y)
                print(x,' -> ',y)

print('{')
for i in (g := graph.generate_random_graph("NEIGHBORS_AMOUNT", 20, maxNei=8)):
    print(f"    {i}: {g[i]}")
print('}')
global_sat(g)