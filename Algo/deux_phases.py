"""
Methode des deux phases — saisie interactive
TP Optimisation Lineaire  ING1-GIA  2025/2026
"""


# ─── Importation ──────────────────────────────────────────────────────────────
from fractions import Fraction

# ─── Affichage ────────────────────────────────────────────────────────────────

def fmt(v):
    return str(v)


def afficher_tableau(tab, base, cols):
    header = f"{'':>6}" + "".join(f"{c:>12}" for c in cols) + f"{'RHS':>12}"
    print(header)
    print("-" * len(header))
    for i, row in enumerate(tab):
        label = "Z" if i == 0 else base[i - 1]
        print(f"{label:>6}" + "".join(f"{fmt(v):>12}" for v in row[:-1]) + f"{fmt(row[-1]):>12}")
    print()


# ─── Operations du simplexe ───────────────────────────────────────────────────

def pivoter(tab, l_pivot, c_pivot, cols):
    pivot = tab[l_pivot][c_pivot]
    print(f"  Pivot = {fmt(pivot)}  (colonne {cols[c_pivot]}, ligne {l_pivot})")
    tab[l_pivot] = [v / pivot for v in tab[l_pivot]]
    print(f"  L{l_pivot} <- L{l_pivot} / {fmt(pivot)}")
    for i in range(len(tab)):
        if i != l_pivot:
            f = tab[i][c_pivot]
            if f != 0:
                signe = "-" if f > 0 else "+"
                print(f"  L{i} <- L{i} {signe} {fmt(abs(f))} * L{l_pivot}")
                tab[i] = [tab[i][k] - f * tab[l_pivot][k] for k in range(len(tab[i]))]


def choisir_entrante(z, n_cols):
    val_min = min(z[j] for j in range(n_cols))
    if val_min >= 0:
        return None
    return list(z).index(val_min)


def choisir_sortante(tab, col_e):
    ratios = []
    for i in range(1, len(tab)):
        if tab[i][col_e] > 0:
            ratios.append((tab[i][-1] / tab[i][col_e], i))
    if not ratios:
        return None
    return min(ratios)[1]


# ─── Construction du tableau Phase 1 ──────────────────────────────────────────

def construire_phase1(A, b, types):
    n = len(A[0])
    n_slack = sum(1 for t in types if t != '=')
    n_art   = sum(1 for t in types if t in ('>=', '='))

    # Nommage sequentiel des variables d'ecart et artificielles
    cols = (
        [f"x{j+1}" for j in range(n)]
        + [f"s{k+1}" for k in range(n_slack)]
        + [f"a{k+1}" for k in range(n_art)]
    )
    idx_slack, idx_art = n, n + n_slack

    base, art_cols, lignes = [], [], []
    sc = ac = 0

    for t, ai, bi in zip(types, A, b):
        bi, ai = Fraction(bi), [Fraction(v) for v in ai]
        if bi < 0:                          # normalise RHS >= 0
            ai, bi = [-v for v in ai], -bi
            t = {'<=': '>=', '>=': '<=', '=': '='}[t]

        row = ai + [Fraction(0)] * (n_slack + n_art) + [bi]

        if t == '<=':
            row[idx_slack + sc] = Fraction(1)
            base.append(f"s{sc+1}")
            sc += 1
        elif t == '>=':
            row[idx_slack + sc] = Fraction(-1)
            row[idx_art   + ac] =  Fraction(1)
            base.append(f"a{ac+1}")
            art_cols.append(idx_art + ac)
            sc += 1; ac += 1
        elif t == '=':
            row[idx_art + ac] = Fraction(1)
            base.append(f"a{ac+1}")
            art_cols.append(idx_art + ac)
            ac += 1
        lignes.append(row)

    # Ligne Z phase 1 : min W = sum(a_i)  <=>  max(-W),  z[a_i] = +1
    z = [Fraction(0)] * (n + n_slack + n_art) + [Fraction(0)]
    for ac_idx in art_cols:
        z[ac_idx] = Fraction(1)
    tableau = [z] + lignes

    # Eliminer les artificielles deja en base de la ligne Z
    for i, bv in enumerate(base):
        if bv.startswith('a'):
            k = int(bv[1:]) - 1
            coef = tableau[0][art_cols[k]]
            tableau[0] = [tableau[0][j] - coef * tableau[i+1][j]
                          for j in range(len(tableau[0]))]

    return tableau, base, cols, art_cols


# ─── Phase 1 ──────────────────────────────────────────────────────────────────

def phase1(A, b, types):
    print("\n" + "="*55)
    print("  PHASE 1 — Trouver une solution de base admissible")
    print("="*55)

    tableau, base, cols, art_cols = construire_phase1(A, b, types)
    n_cols = len(cols)

    print("\nTableau initial Phase 1 :")
    afficher_tableau(tableau, base, cols)

    it = 1
    while True:
        col_e = choisir_entrante(tableau[0], n_cols)
        if col_e is None:
            print("  => Aucun coefficient negatif en Z — Phase 1 terminee.\n")
            break

        col_s = choisir_sortante(tableau, col_e)
        if col_s is None:
            print("  Phase 1 non bornee (cas anormal).")
            return None, None, None, None

        print(f"{'─'*45}")
        print(f"  Iteration {it}")
        print(f"  Variable entrante : {cols[col_e]}   (coeff Z = {fmt(tableau[0][col_e])})")
        print(f"  Test du ratio :")
        for i in range(1, len(tableau)):
            aij = tableau[i][col_e]
            if aij > 0:
                ratio = tableau[i][-1] / aij
                arrow = "  <-- min" if i == col_s else ""
                print(f"    L{i} [{base[i-1]:>4}] : {fmt(tableau[i][-1])} / {fmt(aij)} = {fmt(ratio)}{arrow}")
            else:
                print(f"    L{i} [{base[i-1]:>4}] : aij = {fmt(aij)} <= 0, ignoree")
        print(f"  Variable sortante : {base[col_s-1]}")
        print(f"  Operations de pivot :")
        base[col_s-1] = cols[col_e]
        pivoter(tableau, col_s, col_e, cols)
        print(f"\n  Tableau apres pivot :")
        afficher_tableau(tableau, base, cols)
        it += 1

    # z_RHS = max(-W) = -W*  =>  W* = -z_RHS
    W_star = -tableau[0][-1]
    print(f"  W* = {fmt(W_star)}")
    if W_star != 0:
        print("  INFAISABLE : aucune solution admissible.\n")
        return None, None, None, None

    print(f"  W* = 0  =>  SBA trouvee — base = {base}\n")
    return tableau, base, cols, art_cols


# ─── Phase 2 ──────────────────────────────────────────────────────────────────

def phase2(tableau_p1, base_p1, cols_p1, art_cols, c):
    print("="*55)
    print("  PHASE 2 — Optimiser le probleme original")
    print("="*55)

    # Supprimer les colonnes des variables artificielles
    art_set = set(art_cols)
    keep    = [j for j in range(len(cols_p1)) if j not in art_set]
    cols    = [cols_p1[j] for j in keep]
    n2      = len(cols)

    lignes = [[tableau_p1[i][j] for j in keep] + [tableau_p1[i][-1]]
              for i in range(1, len(tableau_p1))]

    # z[j] = -c[j]  (convention : entrant = coeff le plus negatif)
    z = [Fraction(0)] * n2 + [Fraction(0)]
    for j, lbl in enumerate(cols):
        if lbl.startswith('x'):
            z[j] = -c[int(lbl[1:]) - 1]

    tableau = [z] + lignes
    base    = list(base_p1)

    # Eliminer les variables de base de la ligne Z
    for i, bv in enumerate(base):
        if bv in cols:
            bv_col = cols.index(bv)
            coef = tableau[0][bv_col]
            if coef != 0:
                tableau[0] = [tableau[0][k] - coef * tableau[i+1][k]
                              for k in range(len(tableau[0]))]

    print(f"\nTableau initial Phase 2 :")
    afficher_tableau(tableau, base, cols)

    it = 1
    while True:
        col_e = choisir_entrante(tableau[0], n2)
        if col_e is None:
            print("  => Tous les coefficients de Z >= 0 : solution OPTIMALE.\n")
            break

        col_s = choisir_sortante(tableau, col_e)
        if col_s is None:
            print("  => Probleme NON BORNE.\n")
            return

        print(f"{'─'*45}")
        print(f"  Iteration {it}")
        print(f"  Variable entrante : {cols[col_e]}   (coeff Z = {fmt(tableau[0][col_e])})")
        print(f"  Test du ratio :")
        for i in range(1, len(tableau)):
            aij = tableau[i][col_e]
            if aij > 0:
                ratio = tableau[i][-1] / aij
                arrow = "  <-- min" if i == col_s else ""
                print(f"    L{i} [{base[i-1]:>4}] : {fmt(tableau[i][-1])} / {fmt(aij)} = {fmt(ratio)}{arrow}")
            else:
                print(f"    L{i} [{base[i-1]:>4}] : aij = {fmt(aij)} <= 0, ignoree")
        print(f"  Variable sortante : {base[col_s-1]}")
        print(f"  Operations de pivot :")
        base[col_s-1] = cols[col_e]
        pivoter(tableau, col_s, col_e, cols)
        print(f"\n  Tableau apres pivot :")
        afficher_tableau(tableau, base, cols)
        it += 1

    Z_star = tableau[0][-1]
    print(f"  Z* = {fmt(Z_star)}")
    print("  Solution optimale :")
    for i, bv in enumerate(base):
        if bv.startswith('x'):
            print(f"    {bv} = {fmt(tableau[i+1][-1])}")
    for lbl in cols:
        if lbl.startswith('x') and lbl not in base:
            print(f"    {lbl} = 0")
    print()

    # Verification des solutions multiples (pour les cas d'infinite de solutions)
    for j, lbl in enumerate(cols):
        if lbl.startswith('x') and lbl not in base:
            if tableau[0][j] == 0:
                print(f"  Note : Solution OPTIMALE MULTIPLE possible car la variable hors base {lbl} a un cout reduit de 0.")
                break


# ─── Saisie utilisateur ────────────────────────────────────────────────────────

def saisir_fraction(msg):
    while True:
        try:
            return Fraction(input(msg))
        except ValueError:
            print("  Valeur invalide. Entrez un entier, decimal, ou fraction (ex: 3/2).")

def saisir_int(msg, mini=1):
    while True:
        try:
            v = int(input(msg))
            if v >= mini:
                return v
            print(f"  Entrez un entier >= {mini}.")
        except ValueError:
            print("  Valeur invalide, reessayez.")

def saisir_type(msg):
    while True:
        v = input(msg).strip()
        if v in ('<=', '>=', '='):
            return v
        print("  Tapez  <=   >=   ou   =")


def main():
    print("\n" + "="*55)
    print("   METHODE DES DEUX PHASES — Simplexe")
    print("="*55 + "\n")

    n = saisir_int("Nombre de variables de decision : ")
    m = saisir_int("Nombre de contraintes          : ")

    print(f"\nFonction objectif  max Z = c1*x1 + ... + c{n}*x{n}")
    c = [saisir_fraction(f"  c{j+1} : ") for j in range(n)]

    A, b, types = [], [], []
    print("\nContraintes :")
    for i in range(m):
        print(f"\n  Contrainte {i+1} :")
        ai = [saisir_fraction(f"    a{i+1}{j+1} (coeff x{j+1}) : ") for j in range(n)]
        A.append(ai)
        types.append(saisir_type(f"    Type (<=  >=  =) : "))
        b.append(saisir_fraction(f"    b{i+1} (membre droit)  : "))

    print("\n--- Recapitulatif ---")
    print("max Z = " + " + ".join(f"{c[j]}*x{j+1}" for j in range(n)))
    for i in range(m):
        lhs = " + ".join(f"{A[i][j]}*x{j+1}" for j in range(n))
        print(f"  {lhs}  {types[i]}  {b[i]}")
    print()

    tab, base, cols, art_cols = phase1(A, b, types)
    if tab is not None:
        phase2(tab, base, cols, art_cols, c)


if __name__ == "__main__":
    main()
