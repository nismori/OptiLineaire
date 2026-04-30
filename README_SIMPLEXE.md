# 📊 OptiLineaire - Simplexe Interactif

## 🎯 Description

OptiLineaire est une application interactive pour résoudre des problèmes de programmation linéaire en utilisant l'algorithme du simplexe. L'interface affiche étape par étape comment l'algorithme converge vers la solution optimale, avec mise en évidence du pivot et visualisation des variables entrantes/sortantes.

## 🚀 Installation & Lancement

### Prérequis
- Python 3.8+
- Environnement virtuel configuré: `.venv/`
- Dépendances: `customtkinter`, `tkinter`

### Lancement

```bash
source .venv/bin/activate
python main.py
```

## 📋 Fonctionnalités

### ✅ Implémentées
- **Saisie du problème**: Interface facile pour entrer le nombre de variables, contraintes, et coefficients
- **Visualisation du simplexe**: Affichage étape par étape avec historique complet
- **Variables entrantes/sortantes**: Identification claire des variables qui changent de base
- **Mise en évidence du pivot**: Le pivot est affiché en couleur (rouge/jaune)
- **Variables de base**: Affichage des variables de base et leurs valeurs à chaque étape
- **Navigation**: Boutons Précédent/Suivant pour parcourir les étapes
- **Détection d'erreurs**: Vérification de l'admissibilité de l'origine

### ⚠️ À venir (non implémenté)
- Support du mode dual (simplexe dualisé) pour cas non-admissibles
- Gestion des minimisations directes
- Support des contraintes d'égalité
- Export des résultats (PDF, CSV)

## 📝 Guide d'utilisation

### 1️⃣ Menu Principal
- **"Entrer les données"**: Accès au formulaire de saisie
- **"Charger un fichier"**: (À venir) Import depuis fichier
- **"Quitter"**: Fermeture de l'application

### 2️⃣ Formulaire de Configuration
Entrez:
- **Nombre de variables**: Nombre d'inconnues (ex: 2 pour x₁, x₂)
- **Nombre de contraintes**: Nombre de restrictions (ex: 3)

### 3️⃣ Saisie des Coefficients
Remplissez:
- **Coefficients objectif**: Pour Max/Min cx₁ + dx₂ + ...
- **Contraintes**: Coefficients et RHS (second membre)
- **Inégalités**: Choisir ≤, ≥, ou =
- **Positivité**: Contraintes de positivité (≥0, ≤0, ∈ℝ)

### 4️⃣ Résolution & Visualisation
- Cliquez **"Résoudre"**
- Utilisez **Précédent/Suivant** pour parcourir les étapes
- Chaque étape montre:
  - Tableau du simplexe
  - Variable entrante/sortante
  - Élément pivot (en évidence)
  - Variables de base et leurs valeurs

## 🔧 Architecture

### Fichiers principaux

```
├── main.py                    # Application principale, interface graphique
├── IHM/
│   └── main.py               # Composants UI (Bouton, Label, etc.)
├── Algo/
│   ├── simplexe.py           # Algorithme du simplexe
│   └── deux_phases.py        # (À implémenter) Méthode des deux phases
└── test_*.py                 # Tests et validation
```

### Classes principales

#### `SimplexeData` (simplexe.py)
Conteneur pour les résultats:
```python
data.etapes          # Liste des étapes
data.optimum         # Solution optimale
data.est_resolvable  # Booléen de faisabilité
data.message_erreur  # Message d'erreur si non résolvable
```

#### `PageResultats` (main.py)
Affichage interactif:
- `afficher_etape()`: Rendu de l'étape courante
- `afficher_tableau()`: Formatage du tableau avec mise en évidence du pivot
- Navigation avec `etape_precedente()` et `etape_suivante()`

## 📐 Exemple

### Problème d'optimisation
```
Maximiser:  10x₁ + 20x₂
Sous contraintes:
  2x₁ + x₂ ≤ 30
  x₁ + 4x₂ ≤ 64
  5x₁ + 6x₂ ≤ 110
  x₁, x₂ ≥ 0
```

### Étapes du simplexe
1. **Initialisation**: x₁=0, x₂=0, Objective=0
2. **Itération 1**: x₂ entre (coeff: 20), y₂ sort → x₂=15.5
3. **Itération 2**: x₁ entre, y₃ sort → x₁=4, x₂=15

### Solution optimale
- **x₁ = 4**
- **x₂ = 15**
- **Valeur objective = 340**

## 💡 Astuces

### Pour tester rapidement:
```bash
python test_simplexe_quick.py    # Test du simplexe
python test_validation.py         # Validation des imports
```

### Problèmes courants:
- **"L'origine n'est pas admissible"**: Vos contraintes produisent une région vide
  en (0,0). Mode dual recommandé (non implémenté pour maintenant).
  
- **Pas d'itérations affichées**: Vérifiez que les coefficients objectif sont
  positifs pour une maximisation.

## 🐛 Débogage

### Afficher les détails du simplexe:
```python
from Algo.simplexe import simplexe

data = simplexe(tableau, num_var, num_contraintes)

for i, etape in enumerate(data.etapes):
    print(f"Étape {i}: {etape['titre']}")
    if etape['var_entrante']:
        print(f"  Entrante: {etape['var_entrante']}")
        print(f"  Sortante: {etape['var_sortante']}")
```

## 📚 Ressources

- Algorithme du simplexe: https://en.wikipedia.org/wiki/Simplex_algorithm
- Programmation linéaire: https://www.coursera.org/learn/linear-programming

## 📄 Licence

Projet CivicSense - OptiLineaire

---

Dernière mise à jour: 30 Avril 2026
