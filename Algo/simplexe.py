from fractions import Fraction

variables = 0
contraintes = 0
tab_variables = []
tab_contraintes = []

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

    for i in range(len(tab)):
        if i != index_sortante:
            facteur = tab[i][index_entrante]
            for j in range(len(tab[i])):
                tab[i][j] -= facteur * tab[index_sortante][j]
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
    print("Optimum: (" + str_opt + ")", " ; Z =",tab[0][len(tab[0])-1]*-1)

def run_simplexe(n_vars, n_constraints, c, A, b):
    global variables, contraintes, tab_variables, tab_contraintes
    variables = n_vars
    contraintes = n_constraints

    tab_variables = []
    for i in range(variables):
        tab_variables.append(f"x{i+1}")
    for i in range(contraintes):
        tab_variables.append(f"y{i+1}")

    tab_contraintes = ["f"]
    for i in range(contraintes):
        tab_contraintes.append(f"y{i+1}")

    f = list(c)
    for i in range(contraintes + 1):
        f.append(Fraction(0))

    tab = [f]
    for i in range(contraintes):
        row = list(A[i])
        identity_part = [Fraction(1) if k == i else Fraction(0) for k in range(contraintes)]
        row = row + identity_part + [b[i]]
        tab.append(row)

    tab = simplexe(tab)
    if tab:
        getOptimum(tab)

if __name__ == "__main__":
    pass
