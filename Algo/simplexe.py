from fractions import Fraction
from copy import deepcopy
from typing import List, Dict, Any, Tuple

class SimplexeData:
    """Classe pour stocker les données du simplexe avec historique des étapes"""
    
    def __init__(self, num_variables: int, num_contraintes: int):
        self.num_variables = num_variables
        self.num_contraintes = num_contraintes
        self.etapes = []  # Liste des étapes
        self.tableau_final = None
        self.optimum = None
        self.est_resolvable = True
        self.message_erreur = ""
        self.variables_base = []  # Track les variables de base à chaque étape
    
    def ajouter_etape(self, titre: str, tableau: List[List], 
                     var_entrante: str = None, var_sortante: str = None,
                     index_entrante: int = None, index_sortante: int = None,
                     pivot_element: Any = None, variables_base: List[str] = None):
        """Ajouter une étape à l'historique"""
        etape = {
            'titre': titre,
            'tableau': deepcopy(tableau),
            'var_entrante': var_entrante,
            'var_sortante': var_sortante,
            'index_entrante': index_entrante,
            'index_sortante': index_sortante,
            'pivot_element': pivot_element,
            'variables_base': variables_base or []
        }
        self.etapes.append(etape)
    
    def obtenir_etapes(self) -> List[Dict]:
        return self.etapes

def getVariableX(n):
    return "x" + str(n+1)

def getVariableY(n):
    return "y" + str(n+1)

def getVariable(n, num_var: int, num_cont: int):
    """Obtenir le nom d'une variable par son indice de colonne"""
    if n < num_var:
        return getVariableX(n)
    elif n < num_var + num_cont:
        return getVariableY(n - num_var)
    return None

def is_integer(x):
    return isinstance(x, int) or (isinstance(x, float) and x.is_integer())

def fraction_to_float(x):
    """Convertir Fraction en float si nécessaire"""
    if isinstance(x, Fraction):
        return float(x)
    return x

# Vérifie si l'origine est admissible
def is_origine_admissible(tab: List[List]) -> bool:
    """Vérifie si l'origine (0,0,...) est admissible (tous les RHS positifs)"""
    for i in range(1, len(tab)):
        if tab[i][-1] < 0:
            return False
    return True

def get_variable_base_for_row(tableau: List[List], row_idx: int, num_var: int, num_cont: int) -> str:
    """Obtenir le nom de la variable en base pour une ligne donnée"""
    if row_idx == 0:
        return "Z"
    
    num_cols = len(tableau[0]) - 1  # minus RHS
    for col_idx in range(num_cols):
        # Vérifier si c'est une colonne unitaire (1 dans cette ligne, 0 ailleurs)
        is_unit_col = tableau[row_idx][col_idx] == 1
        if not is_unit_col:
            continue
        
        # Vérifier que tous les autres sont 0
        all_zero_except = True
        for other_row in range(len(tableau)):
            if other_row != row_idx and tableau[other_row][col_idx] != 0:
                all_zero_except = False
                break
        
        if all_zero_except:
            return getVariable(col_idx, num_var, num_cont)
    
    return "?"

# Récupère les lignes/colonnes sortantes et entrantes et effectue le pivot
def entranteEtsortante(tab: List[List], data: SimplexeData, num_var: int, num_cont: int, iteration: int):
    """Effectue une itération du simplexe"""
    # Trouver la variable entrante (plus grande valeur positive dans la ligne Z)
    entrante = max(tab[0][:-1])  # Exclure RHS
    
    # Si pas de valeur positive, on a optimalisé
    if entrante <= 0:
        return tab, None, None, None
    
    index_entrante = tab[0][:-1].index(entrante)  # Index de colonne
    
    # Calculer les rapports pour trouver la variable sortante
    rapports = []
    for i in range(1, len(tab)):
        if tab[i][index_entrante] > 0:
            rapport = tab[i][-1] / tab[i][index_entrante]
            rapports.append(rapport)
        else:
            rapports.append(float('inf'))
    
    rapports_positifs = [r for r in rapports if r < float('inf')]
    if not rapports_positifs:
        data.est_resolvable = False
        data.message_erreur = "Le problème est non borné."
        return None, None, None, None
    
    sortante = min(rapports_positifs)
    index_sortante = rapports.index(sortante) + 1  # Index de ligne (1-based dans tab)
    
    var_entrante = getVariable(index_entrante, num_var, num_cont)
    
    # Chercher la variable de base qui sort
    var_sortante = None
    for col_idx in range(len(tab[0]) - 1):
        if tab[index_sortante][col_idx] != 0:
            # Vérifier si c'est une colonne unitaire
            is_unit_col = True
            for row_idx in range(len(tab)):
                if row_idx != index_sortante and tab[row_idx][col_idx] != 0:
                    is_unit_col = False
                    break
            if is_unit_col and tab[index_sortante][col_idx] == 1:
                var_sortante = getVariable(col_idx, num_var, num_cont)
                break
    
    if var_sortante is None:
        var_sortante = "?"
    
    pivot_element = tab[index_sortante][index_entrante]
    
    # Effectuer le pivot
    if tab[index_sortante][index_entrante] != 0:
        pivot = Fraction(1) / Fraction(tab[index_sortante][index_entrante])
    else:
        pivot = 1
    
    for i in range(len(tab[index_sortante])):
        tab[index_sortante][i] = tab[index_sortante][i] * pivot
    
    facteur = 0
    for i in range(len(tab)):
        if i != index_sortante:
            facteur = tab[i][index_entrante]
            for j in range(len(tab[i])):
                tab[i][j] -= facteur * tab[index_sortante][j]
    
    # Calculer les variables de base après le pivot
    variables_base = []
    for row_idx in range(len(tab)):
        var = get_variable_base_for_row(tab, row_idx, num_var, num_cont)
        variables_base.append(var)
    
    # Ajouter l'étape à l'historique
    data.ajouter_etape(
        titre=f"Itération {iteration}",
        tableau=tab,
        var_entrante=var_entrante,
        var_sortante=var_sortante,
        index_entrante=index_entrante,
        index_sortante=index_sortante,
        pivot_element=pivot_element,
        variables_base=variables_base
    )
    
    return tab, index_entrante, index_sortante, variables_base

# Vérifie si une ligne du tableau à toutes ces valeurs positives
def isTabPositif(tab):
    for i in range(len(tab[0]) - 1):  # Exclure RHS
        if tab[0][i] > 0:
            return True
    return False

# Effectue le calcul du simplexe
def simplexe(tab: List[List], num_variables: int, num_contraintes: int) -> SimplexeData:
    """Effectue l'algorithme du simplexe avec enregistrement des étapes"""
    data = SimplexeData(num_variables, num_contraintes)
    
    # Vérifier l'admissibilité de l'origine
    if not is_origine_admissible(tab):
        data.est_resolvable = False
        data.message_erreur = "L'origine n'est pas admissible. Mode dual recommandé (non implémenté)."
        return data
    
    # Calculer les variables de base initiales
    variables_base = []
    for row_idx in range(len(tab)):
        var = get_variable_base_for_row(tab, row_idx, num_variables, num_contraintes)
        variables_base.append(var)
    
    # Ajouter l'étape d'initialisation
    data.ajouter_etape(titre="Initialisation", tableau=tab, variables_base=variables_base)
    
    # Boucle du simplexe
    iteration = 1
    while isTabPositif(tab):
        result = entranteEtsortante(tab, data, num_variables, num_contraintes, iteration)
        if result[0] is None:
            return data
        tab = result[0]
        iteration += 1
        
        # Limite de sécurité
        if iteration > 100:
            data.message_erreur = "Limite d'itérations dépassée"
            break
    
    # Récupérer l'optimum
    data.tableau_final = tab
    optimum = getOptimum(tab, num_variables, num_contraintes)
    data.optimum = optimum
    
    return data

# Récupère les coordonnées de l'optimum
def getOptimum(tab, num_variables: int, num_contraintes: int) -> Dict[str, float]:
    """Récupère les coordonnées de l'optimum"""
    optimum = {}
    num_cols = len(tab[0]) - 1
    
    for col_idx in range(num_cols):
        var_name = getVariable(col_idx, num_variables, num_contraintes)
        if var_name is None:
            continue
        
        # Chercher si c'est une colonne unitaire
        is_unit_col = True
        row_with_one = -1
        
        for row_idx in range(len(tab)):
            if row_idx == 0:  # Skip ligne Z
                continue
            if tab[row_idx][col_idx] == 1:
                if row_with_one == -1:
                    row_with_one = row_idx
                else:
                    is_unit_col = False
                    break
            elif tab[row_idx][col_idx] != 0:
                is_unit_col = False
                break
        
        if is_unit_col and row_with_one != -1:
            optimum[var_name] = float(tab[row_with_one][-1])
        else:
            # Variable non-basique
            optimum[var_name] = 0.0
    
    # Valeur objective (prendre la valeur absolue du RHS, car c'est -Z)
    # Si on maximise, le RHS de -Z est négatif, donc on prend le négatif pour avoir Z
    # Si on minimise, le RHS de Z est positif, donc on le prend directement
    optimum['valeur_objective'] = -float(tab[0][-1])
    return optimum

# Ajoute les 0 pour la ligne d'objectif
def complete_f(tab):
    if len(tab) == 2:
        for i in range(4):
            tab.append(0)
    else :
        print("Le tableau est incorrect")
    return tab


# Ajoute les 0 pour le tableau
def complete_y(tab, n):
    n-=1
    if len(tab) == 3:
        identity_part = [1 if i == n else 0 for i in range(3)]
        return tab[:2] + identity_part + [tab[2]]
    else:
        print("Le tableau est incorrect")
    return tab

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
