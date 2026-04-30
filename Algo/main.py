def getVariableX(n):
    return "x" + str(n+1)

def getVariableY(n):
    return "y" + str(n)


#Récupère les lignes/colonnes sortantes et entrantes et effectue le pivot
def entranteEtsortante(tab: list[list[int]]):
    entrante = max(tab[0])
    index_entrante = tab[0].index(entrante)
    rapports = []
    for i in range(1, len(tab)):
        rapports.append(tab[i][len(tab[i])-1]/tab[i][index_entrante])
    rapports_positifs = [r for r in rapports if r > 0]
    sortante = min(rapports_positifs)
    index_sortante = rapports.index(sortante) + 1
    if(tab[index_sortante][index_entrante]!=0):
        pivot = 1/tab[index_sortante][index_entrante]
    for i in range(len(tab[index_sortante])):
        tab[index_sortante][i] = tab[index_sortante][i]*pivot
    facteur = 0
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if(tab[i] != tab[index_sortante]):
                if(facteur == 0):
                    facteur = tab[i][index_entrante]
                tab[i][j] -= facteur * tab[index_sortante][j]
        facteur = 0
    print(tab,"entrante : ",getVariableX(index_entrante), " ; sortante : ",getVariableY(index_sortante))
    return tab

#Vérifie si une ligne du tableau à toutes ces valeurs positives
def isTabPositif(tab):
    for i in range(len(tab)):
        if(tab[i] > 0):
            return True
    return False

#Effectue le calcul du simplexe
def simplexe(tab: list[list[int]]):
    print(tab)
    while(isTabPositif(tab[0])):
        tab = entranteEtsortante(tab)
    return tab

#Récupère les coordonnées de l'optimum
def getOptimum(tab):
    x1 = 0
    x2 = 0
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if(tab[i][1] == 1.0):
                x2 = tab[i][len(tab[i])-1]
            if(tab[i][0] == 1.0):
                x1 = tab[i][len(tab[i])-1]
    print("Optimum: (", x1,",",x2,")")

def complete_f(tab):
    if len(tab) == 2:
        for i in range(4):
            tab.append(0)
    else :
        print("Le tableau est incorrect")
    return tab


def complete_y(tab, n):
    n-=1
    if len(tab) == 3:
        identity_part = [1 if i == n else 0 for i in range(3)]
        return tab[:2] + identity_part + [tab[2]]
    else:
        print("Le tableau est incorrect")
    return tab

def main():
    f = [2,3,0]
    y1 = [1,1,3]
    y2 = [-1,1,5]
    y3 = [2,1,14]

    #ATTENTION : Ces fonctions ne marchent qu'avec un simple avec 3 inégalités.
    f = complete_f(f)
    y1 = complete_y(y1, 1)
    y2 = complete_y(y2, 2)
    y3 = complete_y(y3, 3)


    tab = [f,y1,y2]
    tab = simplexe(tab)
    getOptimum(tab)

if __name__ == "__main__":
    main()
