import simplexe
import deux_phases
from fractions import Fraction


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

def saisir_fraction(msg):
    while True:
        try:
            return Fraction(input(msg))
        except ValueError:
            print("  Valeur invalide. Entrez un entier, décimal, ou fraction (ex: 3/2).")

def saisir_int(msg, mini=1):
    while True:
        try:
            v = int(input(msg))
            if v >= mini: return v
            print(f"  Entrez un entier >= {mini}.")
        except ValueError:
            print("  Valeur invalide.")

def saisir_type(msg):
    while True:
        v = input(msg).strip()
        if v in ('<=', '>=', '='): return v
        print("  Tapez  <=   >=   ou   =")

def is_optimum_admissible(b_norm):
    print("\n" + "="*55)
    print("   VÉRIFICATION ADMISSIBILITÉ DE L'ORIGINE")
    print("="*55)
    print("  → Conversion en Ax <= b et vérification x=0 (soit 0 <= b_i)\n")

    origine_admissible = True
    for i, bi in enumerate(b_norm):
        if bi < 0:
            print(f"  Contrainte (normalisée) {i+1} : 0 <= {bi}  ✘ NON satisfaite")
            origine_admissible = False
        else:
            print(f"  Contrainte (normalisée) {i+1} : 0 <= {bi}  ✔ satisfaite")
    return origine_admissible


def main():
    print("\n" + "="*55)
    print("   MÉTHODE D'OPTIMISATION LINÉAIRE")
    print("="*55 + "\n")

    n = saisir_int("Nombre de variables de décision : ")
    m = saisir_int("Nombre de contraintes          : ")

    print(f"\nFonction objectif  max Z = c1*x1 + ... + c{n}*x{n}")
    c = [saisir_fraction(f"  c{j+1} : ") for j in range(n)]

    A, b, types = [], [], []
    print("\nContraintes :")
    for i in range(m):
        print(f"\n  Contrainte {i+1} :")
        A.append([saisir_fraction(f"    a{i+1}{j+1} (coeff x{j+1}) : ") for j in range(n)])
        types.append(saisir_type(f"    Type (<=  >=  =) : "))
        b.append(saisir_fraction(f"    b{i+1} (membre droit)  : "))

    A_norm, b_norm = normaliser_contraintes(A, b, types)
    origine_admissible = is_optimum_admissible(b_norm)

    if origine_admissible:
        simplexe.run_simplexe(n, len(A_norm), c, A_norm, b_norm)
    else:
        tab_p1, base, cols = deux_phases.phase1(A_norm, b_norm)
        if tab_p1 is not None:
            tab_p2, cols_p2 = deux_phases.setup_phase2_depuis_phase1(tab_p1, base, cols, c)
            deux_phases.phase2(tab_p2, base, cols_p2)

if __name__ == "__main__":
    main()
