#!/usr/bin/env python3
"""Test d'import et validation de la structure"""
import sys

try:
    # Test des imports
    print("Vérification des imports...")
    
    from IHM.main import Fenetre, Titre, Label, Bouton, ChampTexte, Selection, Tableau, CaseACocher
    print("✓ Imports IHM.main OK")
    
    from main import MenuPrincipal, FormulaireSaisie, PageCoefficients, PageResultats, OptimisationLineaire
    print("✓ Imports main OK")
    
    from Algo.simplexe import simplexe, SimplexeData, getOptimum
    print("✓ Imports Algo.simplexe OK")
    
    # Test SimplexeData
    print("\nVérification de SimplexeData...")
    data = SimplexeData(2, 3)
    data.ajouter_etape(
        titre="Test",
        tableau=[[1, 2, 3], [4, 5, 6]],
        var_entrante="x1",
        var_sortante="y1",
        index_entrante=0,
        index_sortante=1,
        pivot_element=5.0
    )
    etapes = data.obtenir_etapes()
    assert len(etapes) == 1
    assert etapes[0]['titre'] == "Test"
    print("✓ SimplexeData OK")
    
    print("\n✅ Tous les tests de validation sont passés!")
    print("\nL'application est prête à être lancée.")
    print("Pour démarrer: python main.py")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
