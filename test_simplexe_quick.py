#!/usr/bin/env python3
"""Test rapide du simplexe"""
from Algo.simplexe import simplexe

# Test simple: 
# Max 10x + 20y
# s.t. 2x + y <= 30
#      x + 4y <= 64
#      5x + 6y <= 110

num_var = 2
num_cont = 3

# Construire le tableau
# Les coefficients de l'objectif doivent être positifs pour Max
# Format: [c1, c2, ..., 0 (écarts), RHS]
tableau = [
    [10.0, 20.0, 0, 0, 0, 0],     # Objectif (positif pour Max)
    [2.0, 1.0, 1, 0, 0, 30],      # Contrainte 1
    [1.0, 4.0, 0, 1, 0, 64],      # Contrainte 2
    [5.0, 6.0, 0, 0, 1, 110]      # Contrainte 3
]

print("Tableau initial:")
for ligne in tableau:
    print([f"{x:.2f}" for x in ligne])
print()

# Lancer le simplexe
data = simplexe(tableau, num_var, num_cont)

print(f"Résolvable: {data.est_resolvable}")
if not data.est_resolvable:
    print(f"Erreur: {data.message_erreur}")
else:
    print(f"Nombre d'étapes: {len(data.etapes)}")
    
    for i, etape in enumerate(data.etapes):
        print(f"\n{i}. {etape['titre']}")
        if etape['var_entrante'] and etape['var_sortante']:
            print(f"   Entrante: {etape['var_entrante']}, Sortante: {etape['var_sortante']}")
            print(f"   Pivot: {etape['pivot_element']}")
    
    print(f"\nOptimum: {data.optimum}")
