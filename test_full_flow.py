#!/usr/bin/env python3
"""Test complet du flux Simplexe"""

from Algo.simplexe import simplexe

# Simuler le flux utilisateur
print("="*60)
print("TEST: Flux complet utilisateur")
print("="*60)

# 1. Utilisateur remplit le formulaire
print("\n1. Utilisateur configure le problème:")
print("   - 2 variables")
print("   - 3 contraintes")

# 2. Utilisateur remplit les coefficients
print("\n2. Utilisateur entre les données:")
donnees = {
    'num_variables': 2,
    'num_contraintes': 3,
    'directif': 'Max',
    'objective': [10, 20, 0],  # 10x1 + 20x2 + 0 (placeholder)
    'contraintes': [
        {'coefficients': [2, 1], 'operateur': '≤', 'rhs': 30},
        {'coefficients': [1, 4], 'operateur': '≤', 'rhs': 64},
        {'coefficients': [5, 6], 'operateur': '≤', 'rhs': 110},
    ]
}
print(f"   Objectif: {donnees['directif']} {donnees['objective'][0]}x1 + {donnees['objective'][1]}x2")
for i, c in enumerate(donnees['contraintes']):
    print(f"   Contrainte {i+1}: {c['coefficients'][0]}x1 + {c['coefficients'][1]}x2 {c['operateur']} {c['rhs']}")

# 3. Utilisateur clique "Résoudre"
print("\n3. Utilisateur clique 'Résoudre'...")

# Construire le tableau
num_var = donnees['num_variables']
num_cont = donnees['num_contraintes']

obj = donnees['objective'][:-1]
obj = obj + [0] * num_cont + [0]

tableau = [obj]
for idx, contrainte in enumerate(donnees['contraintes']):
    ligne = contrainte['coefficients'].copy()
    for i in range(num_cont):
        ligne.append(1 if i == idx else 0)
    ligne.append(float(contrainte['rhs']))
    tableau.append(ligne)

tableau = [[float(x) for x in ligne] for ligne in tableau]

print(f"   Tableau construit: {len(tableau)} lignes x {len(tableau[0])} colonnes")

try:
    # Lancer le simplexe
    data = simplexe(tableau, num_var, num_cont)
    
    print("\n4. Résultats:")
    print(f"   ✓ Résolvable: {data.est_resolvable}")
    print(f"   ✓ Nombre d'étapes: {len(data.etapes)}")
    
    if data.est_resolvable:
        print(f"\n5. Affichage des étapes (comme dans l'interface):")
        for i, etape in enumerate(data.etapes):
            print(f"\n   Étape {i+1}: {etape['titre']}")
            if etape['var_entrante']:
                print(f"     - Entrante: {etape['var_entrante']}")
                print(f"     - Sortante: {etape['var_sortante']}")
                print(f"     - Pivot: {etape['pivot_element']}")
                if etape['variables_base']:
                    print(f"     - Base: {etape['variables_base']}")
        
        print(f"\n6. Solution finale:")
        for var, val in data.optimum.items():
            if var != 'valeur_objective':
                print(f"   {var} = {val:.2f}")
        print(f"   Valeur objective = {data.optimum['valeur_objective']:.2f}")
    else:
        print(f"   Erreur: {data.message_erreur}")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLÉTÉ AVEC SUCCÈS")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
