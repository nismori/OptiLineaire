from fractions import Fraction

variables = 2
contraintes = 4
tab_variables = []
for i in range(variables):
    tab_variables.append(f"x{i+1}")
for i in range(contraintes):
    tab_variables.append(f"y{i+1}")

tab_contraintes= ["f"]
for i in range(contraintes):
    tab_contraintes.append(f"y{i+1}")

def getVariableX(n):
    return "x" + str(n+1)

def getVariableY(n):
    return "y" + str(n)

def getVariable(n):
    indice = 0
    if n > (variables + contraintes - 1):
        print("L'indice ne correspond pas à une variable")
        return None
    for i in range(variables):
        if indice == n:
            return getVariableX(i)
        indice += 1
    for i in range(contraintes):
        if indice == n:
            return getVariableY(i)
        indice += 1
    return None

def is_integer(x):
    return isinstance(x, int) or (isinstance(x, float) and x.is_integer())

#Récupère les lignes/colonnes sortantes et entrantes et effectue le pivot
def entranteEtsortante(tab: list[list[int]]):
    entrante = max(tab[0])
    index_entrante = tab[0].index(entrante)
    rapports = []
    pivot = 1

    for i in range(1, len(tab)):
        rapports.append(tab[i][len(tab[i])-1]/tab[i][index_entrante])
    rapports_positifs = [r for r in rapports if r > 0]
    if not rapports_positifs:
        print("Le problème est non bornée.")
        return None
    sortante = min(rapports_positifs)
    index_sortante = rapports.index(sortante) + 1

    print("On prend la plus grande valeur comme valeur entrante à savoir",tab_variables[index_entrante],":",entrante)
    print(f"On prend le plus petit rapport comme valeur sortante à savoir {tab_contraintes[index_sortante]} : {tab[index_sortante][len(tab[index_sortante])-1]}/({tab[index_sortante][index_entrante]})")
    print(f"Le pivot est {tab[index_sortante][index_entrante]}")
    tab_contraintes[index_sortante] = getVariable(index_entrante)

    if tab[index_sortante][index_entrante]!=0:
        pivot = Fraction(1) / Fraction(tab[index_sortante][index_entrante])
    for i in range(len(tab[index_sortante])):
        tab[index_sortante][i] = tab[index_sortante][i] * pivot
    facteur = 0

    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if tab[i] != tab[index_sortante]:
                if facteur == 0:
                    facteur = tab[i][index_entrante]
                tab[i][j] -= facteur * tab[index_sortante][j]
        facteur = 0
    print()

    tab_affichage = "[" + ", ".join("[" + ", ".join(str(val) for val in ligne) + "]" for ligne in tab) + "]"
    print(tab_affichage)
    return tab

#Vérifie si une ligne du tableau à toutes ces valeurs positives
def isTabPositif(tab):
    for i in range(len(tab)):
        if tab[i] > 0:
            return True
    return False

#Effectue le calcul du simplexe
def simplexe(tab: list[list[int]]):
    print(tab)
    while isTabPositif(tab[0]):
        tab = entranteEtsortante(tab)
    return tab

#Récupère les coordonnées de l'optimum
def getOptimum(tab):
    optimum = [0] * variables
    for v in range(variables):
        for i in range(len(tab)):
            if tab[i][v] == 1.0:
                optimum[v] = tab[i][-1]

    str_opt = ", ".join(str(val) for val in optimum)
    print("Optimum: (" + str_opt + ")")

# Ajoute les 0 pour la ligne d'objectif
def complete_f(tab):
    for i in range(contraintes + 1):
        tab.append(0)
    return tab

# Ajoute les 0 pour le tableau
def complete_y(tab, n):
    identity_part = [1 if i == (n-1) else 0 for i in range(contraintes)]
    return tab[:variables] + identity_part + [tab[-1]]

def main():
    f = [10,20]
    y1 = [2,1,30]
    y2 = [1,4,64]
    y3 = [5,6,110]
    y4 = [3,7,14]

    #ATTENTION : Ces fonctions ne marchent qu'avec un simple avec 3 inégalités.
    f = complete_f(f)
    y1 = complete_y(y1, 1)
    y2 = complete_y(y2, 2)
    y3 = complete_y(y3, 3)
    y4 = complete_y(y4, 4)

    tab = [f,y1,y2,y3,y4]
    tab = simplexe(tab)
    getOptimum(tab)

if __name__ == "__main__":
    main()
