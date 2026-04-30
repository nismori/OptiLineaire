import numpy as np
from fractions import Fraction

# ─── Affichage ────────────────────────────────────────────────────────────────

def fmt(v):
    if v.denominator == 1:
        return str(v.numerator)
    return f"{v.numerator}/{v.denominator}"

def afficher_tableau(tab, base, cols):
    header = f"{'':>6}" + "".join(f"{c:>10}" for c in cols) + f"{'RHS':>10}"
    print(header)
    print("-" * len(header))
    for i, row in enumerate(tab):
        label = "f" if i == 0 else base[i - 1]
        print(f"{label:>6}" + "".join(f"{fmt(v):>10}" for v in row[:-1]) + f"{fmt(row[-1]):>10}")
    print()

# ─── Opérations du simplexe ───────────────────────────────────────────────────

def pivoter(tab, l_pivot, c_pivot):
    pivot = tab[l_pivot][c_pivot]
    # Division de la ligne du pivot
    tab[l_pivot] = [v / pivot for v in tab[l_pivot]]
    
    # Élimination dans les autres lignes (y compris la ligne de la fonction objectif f)
    for i in range(len(tab)):
        if i != l_pivot:
            facteur = tab[i][c_pivot]
            if facteur != 0:
                tab[i] = [tab[i][k] - facteur * tab[l_pivot][k] for k in range(len(tab[i]))]

def choisir_entrante(z, n_cols):
    # On cherche à MAXIMISER, donc on prend le plus grand coefficient strictement positif dans f
    max_val = 0
    col_e = None
    for j in range(n_cols):
        if z[j] > max_val:
            max_val = z[j]
            col_e = j
    return col_e # Renvoie None si tous les coeff sont <= 0 (optimum atteint)

def choisir_sortante(tab, col_e, base):
    ratios = []
    for i in range(1, len(tab)):
        if tab[i][col_e] > 0:
            ratios.append((tab[i][-1] / tab[i][col_e], i, base[i-1]))
            
    if not ratios:
        return None
        
    # Règle de choix : on prend le ratio minimum
    min_ratio = min(r[0] for r in ratios)
    candidats = [r for r in ratios if r[0] == min_ratio]
    
    # Règle de départage du cours : favoriser la sortie de δ si possible
    for r in candidats:
        if r[2] == 'δ':
            return r[1]
            
    return candidats[0][1]

# ─── Normalisation ────────────────────────────────────────────────────────────

def normaliser_contraintes(A, b, types):
    """
    Convertit toutes les contraintes sous la forme standard Ax <= b pour 
    faciliter l'évaluation de l'admissibilité de l'origine.
    """
    A_norm, b_norm = [], []
    for t, ai, bi in zip(types, A, b):
        ai_frac = [Fraction(v) for v in ai]
        bi_frac = Fraction(bi)
        
        if t == '<=':
            A_norm.append(ai_frac)
            b_norm.append(bi_frac)
        elif t == '>=':
            A_norm.append([-v for v in ai_frac])
            b_norm.append(-bi_frac)
        elif t == '=':
            A_norm.append(ai_frac)
            b_norm.append(bi_frac)
            A_norm.append([-v for v in ai_frac])
            b_norm.append(-bi_frac)
            
    return A_norm, b_norm

# ─── Phase 1 (Unique δ) ───────────────────────────────────────────────────────

def construire_phase1(A_norm, b_norm):
    n = len(A_norm[0])
    m = len(A_norm)
    
    cols = [f"x{j+1}" for j in range(n)] + ["δ"] + [f"y{i+1}" for i in range(m)]
    
    # Ligne objectif f = -δ (le coeff de δ est -1)
    f_row = [Fraction(0)] * n + [Fraction(-1)] + [Fraction(0)] * m + [Fraction(0)]
    tableau = [f_row]
    base = []
    
    for i in range(m):
        # Contrainte : A_i * x - δ + y_i = b_i
        row = A_norm[i] + [Fraction(-1)] + [Fraction(1) if k == i else Fraction(0) for k in range(m)] + [b_norm[i]]
        tableau.append(row)
        base.append(f"y{i+1}")
        
    return tableau, base, cols

def phase1(A_norm, b_norm):
    print("\n" + "="*55)
    print("  PHASE 1 — Trouver une solution de base admissible")
    print("="*55)

    tableau, base, cols = construire_phase1(A_norm, b_norm)
    n_cols = len(cols)
    
    print("\nTableau initial Phase 1 (avant pivot forcé) :")
    afficher_tableau(tableau, base, cols)

    # 1. PIVOT FORCÉ pour rendre l'origine (avec δ) admissible
    # On cherche la ligne avec le b_i le plus négatif
    b_vals = [tableau[i][-1] for i in range(1, len(tableau))]
    min_b = min(b_vals)
    l_pivot = b_vals.index(min_b) + 1
    c_pivot = cols.index("δ")
    
    print(f"  -> Pivot forcé sur δ pour rendre le tableau admissible : ligne {l_pivot}")
    pivoter(tableau, l_pivot, c_pivot)
    base[l_pivot-1] = "δ"
    
    print("\nTableau Phase 1 après pivot forcé :")
    afficher_tableau(tableau, base, cols)

    # 2. Algorithme du Simplexe standard
    it = 1
    while True:
        col_e = choisir_entrante(tableau[0], n_cols)
        if col_e is None:
            print("  => Tous les coefficients de f <= 0 : Phase 1 terminée.\n")
            break

        col_s = choisir_sortante(tableau, col_e, base)
        if col_s is None:
            print("  => Phase 1 non bornée (cas anormal).")
            return None, None, None

        print(f"  Itération {it} | Entrante : {cols[col_e]} | Sortante : {base[col_s-1]}")
        
        base[col_s-1] = cols[col_e]
        pivoter(tableau, col_s, col_e)
        afficher_tableau(tableau, base, cols)
        it += 1

    # Le RHS de la ligne f contient l'opposé de la valeur de l'objectif (-f_val)
    f_opt = -tableau[0][-1] 
    if f_opt != 0:
        print(f"  δ* = {-f_opt} != 0 => INFAISABLE : aucune solution admissible.\n")
        return None, None, None

    print(f"  δ* = 0 => Solution de base admissible trouvée !\n")
    
    # Traitement de la dégénérescence : si δ est toujours dans la base avec la valeur 0
    if "δ" in base:
        idx_row = base.index("δ") + 1
        print("  Note: δ est resté dans la base (dégénérescence). On la sort.")
        for j, c_name in enumerate(cols):
            if c_name not in base and c_name != "δ" and tableau[idx_row][j] != 0:
                pivoter(tableau, idx_row, j)
                base[idx_row - 1] = c_name
                break
        else:
            # S'il n'y a pas de pivot valide, la ligne est redondante
            tableau.pop(idx_row)
            base.pop(idx_row - 1)

    return tableau, base, cols


# ─── Phase 2 ──────────────────────────────────────────────────────────────────

def construire_phase2_direct(A_norm, b_norm, c_orig):
    n = len(A_norm[0])
    m = len(A_norm)
    cols = [f"x{j+1}" for j in range(n)] + [f"y{i+1}" for i in range(m)]
    
    tab = [[Fraction(c_orig[j]) if j < n else Fraction(0) for j in range(len(cols))] + [Fraction(0)]]
    base = []
    for i in range(m):
        row = A_norm[i] + [Fraction(1) if k == i else Fraction(0) for k in range(m)] + [b_norm[i]]
        tab.append(row)
        base.append(f"y{i+1}")
    return tab, base, cols

def setup_phase2_depuis_phase1(tab_p1, base, cols, c_orig):
    n = len(c_orig)
    idx_delta = cols.index("δ")
    
    # Suppression de la colonne δ
    cols.pop(idx_delta)
    for row in tab_p1:
        row.pop(idx_delta)
        
    # Restauration de l'objectif original dans la ligne f
    tab_p1[0] = [Fraction(c_orig[j]) if j < n else Fraction(0) for j in range(len(cols))] + [Fraction(0)]
    
    # Élimination des variables de base de la ligne f
    for i, bv in enumerate(base):
        idx_bv = cols.index(bv)
        coeff = tab_p1[0][idx_bv]
        if coeff != 0:
            for k in range(len(tab_p1[0])):
                tab_p1[0][k] -= coeff * tab_p1[i+1][k]
                
    return tab_p1, cols

def phase2(tableau, base, cols):
    print("="*55)
    print("  PHASE 2 — Optimiser le problème original")
    print("="*55 + "\n")
    
    n_cols = len(cols)
    print("Tableau initial Phase 2 :")
    afficher_tableau(tableau, base, cols)

    it = 1
    while True:
        col_e = choisir_entrante(tableau[0], n_cols)
        if col_e is None:
            print("  => Tous les coefficients de f <= 0 : solution OPTIMALE.\n")
            break

        col_s = choisir_sortante(tableau, col_e, base)
        if col_s is None:
            print("  => Problème NON BORNÉ.\n")
            return

        print(f"  Itération {it} | Entrante : {cols[col_e]} | Sortante : {base[col_s-1]}")
        
        base[col_s-1] = cols[col_e]
        pivoter(tableau, col_s, col_e)
        afficher_tableau(tableau, base, cols)
        it += 1

    Z_star = -tableau[0][-1]
    print(f"  Z* = {fmt(Z_star)}")
    print("  Solution optimale :")
    for i, bv in enumerate(base):
        if bv.startswith('x'):
            print(f"    {bv} = {fmt(tableau[i+1][-1])}")
    for lbl in cols:
        if lbl.startswith('x') and lbl not in base:
            print(f"    {lbl} = 0")
