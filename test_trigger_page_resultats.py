#!/usr/bin/env python3
"""Test que afficher_page('Resultats') lance bien resoudre() si donnees présentes"""
from main import OptimisationLineaire

app = OptimisationLineaire()

# Simuler des données
app.donnees = {
    'num_variables': 2,
    'num_contraintes': 3,
    'directif': 'Max',
    'objective': [10, 20, 0],
    'contraintes': [
        {'coefficients': [2, 1], 'operateur': '≤', 'rhs': 30},
        {'coefficients': [1, 4], 'operateur': '≤', 'rhs': 64},
        {'coefficients': [5, 6], 'operateur': '≤', 'rhs': 110},
    ]
}

# Appeler afficher_page pour déclencher on_show
app.afficher_page('Resultats')

page = app.page_resultats
if page.simplex_data is None:
    print('ÉCHEC: simplexe non exécuté')
else:
    print('SUCCÈS: simplexe exécuté, étapes =', len(page.simplex_data.obtenir_etapes()))
    print('Optimum:', page.simplex_data.optimum)

# Ne pas lancer mainloop
