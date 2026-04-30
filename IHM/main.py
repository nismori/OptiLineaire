from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from typing import List, Callable, Any, Dict


class Bouton:
    """Classe pour créer un bouton personnalisé"""
    def __init__(self, master, text: str, command: Callable = None, position: str = "top"):
        self.button = ctk.CTkButton(master=master, text=text, command=command, font=('Arial', 18))
        self.position = position
    
    def pack(self, **kwargs):
        if self.position == "top":
            pack_kwargs = {'side': tk.TOP, 'padx': 20, 'pady': 10}
            pack_kwargs.update(kwargs)
            self.button.pack(**pack_kwargs)
        elif self.position == "left":
            pack_kwargs = {'side': tk.LEFT, 'padx': 2, 'pady': 10}
            pack_kwargs.update(kwargs)
            self.button.pack(**pack_kwargs)
        elif self.position == "right":
            pack_kwargs = {'side': tk.RIGHT, 'padx': 2, 'pady': 10}
            pack_kwargs.update(kwargs)
            self.button.pack(**pack_kwargs)
        else:
            self.button.pack(**kwargs)
        return self.button
    
    def get(self):
        return self.button


class Label:
    """Classe pour créer un label/texte personnalisé"""
    def __init__(self, master, text: str = "", size: int = 18):
        self.text_var = tk.StringVar(value=text)
        self.label = ctk.CTkLabel(master=master, textvariable=self.text_var, font=('Arial', size))
        self.size = size
    
    def pack(self, **kwargs):
        pack_kwargs = {'padx': 5, 'pady': 5}
        pack_kwargs.update(kwargs)
        self.label.pack(**pack_kwargs)
        return self.label
    
    def set_text(self, text: str):
        self.text_var.set(text)
    
    def get_text(self):
        return self.text_var.get()


class Titre(Label):
    """Classe pour créer un titre (Label avec taille plus grande)"""
    def __init__(self, master, text: str = ""):
        super().__init__(master, text, size=40)


class ChampTexte:
    """Classe pour créer un champ de texte/Entry"""
    def __init__(self, master):
        self.entry = ctk.CTkEntry(master)
    
    def pack(self, **kwargs):
        pack_kwargs = {'padx': 5, 'pady': 5}
        pack_kwargs.update(kwargs)
        self.entry.pack(**pack_kwargs)
        return self.entry
    
    def get(self):
        return self.entry.get()
    
    def set(self, value: str):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def get_widget(self):
        return self.entry


class Selection:
    """Classe pour créer une boîte de sélection (ComboBox)"""
    def __init__(self, master, titre: str = "", values: List[str] = None, default: str = ""):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        
        if titre:
            text_var = tk.StringVar(value=titre)
            label = ctk.CTkLabel(master=self.frame, textvariable=text_var, font=('Arial', 18))
            label.pack(padx=5, pady=5, side=tk.LEFT)
        
        self.combobox_var = ctk.StringVar(value=default)
        self.combobox = ctk.CTkComboBox(
            master=self.frame,
            values=values or [],
            state="readonly",
            variable=self.combobox_var
        )
        self.combobox.pack(padx=20, pady=10, side=tk.LEFT)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        return self.frame
    
    def get(self):
        return self.combobox_var.get()
    
    def set(self, value: str):
        self.combobox_var.set(value)
    
    def get_widget(self):
        return self.combobox


class CaseACocher:
    """Classe pour créer une case à cocher"""
    def __init__(self, master, titre: str = "", command: Callable = None, default: bool = False):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.check_var = tk.BooleanVar(value=default)
        self.checkbox = ctk.CTkCheckBox(
            master=self.frame,
            text=titre,
            command=command,
            variable=self.check_var
        )
        self.checkbox.pack(side=tk.LEFT)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        return self.frame
    
    def get(self):
        return self.check_var.get()
    
    def set(self, value: bool):
        self.check_var.set(value)
    
    def get_widget(self):
        return self.checkbox


class Tableau:
    """Classe pour créer un tableau avec lignes et colonnes"""
    def __init__(self, master, colonnes: List[str], hauteur: int = 20):
        self.colonnes = colonnes
        self.hauteur = hauteur
        self.donnees: List[Dict[str, Any]] = []
        
        # Frame principal avec customtkinter
        self.frame = ctk.CTkFrame(master)
        
        # Container interne avec tkinter
        container = tk.Frame(self.frame, bg="#212121")
        container.pack(fill="both", expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(container, bg="#212121", height=300, relief=tk.FLAT, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Scrollbars
        v_scroll = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        v_scroll.pack(side="right", fill="y")
        
        h_scroll = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        h_scroll.pack(side="bottom", fill="x")
        
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Frame interne pour le contenu
        self.inner_frame = tk.Frame(self.canvas, bg="#212121")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        # Treeview dans le frame interne
        self.tree = ttk.Treeview(
            self.inner_frame,
            columns=colonnes,
            show="headings",
            height=hauteur
        )
        self.tree.pack(side=tk.LEFT, expand=False)
        
        # Configurer colonnes - largeur pour forcer scroll horizontal
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        
        # Mettre à jour scrollregion
        def on_configure(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.inner_frame.bind("<Configure>", on_configure)
    
    def pack(self, **kwargs):
        pack_kwargs = {}
        pack_kwargs.update(kwargs)
        self.frame.pack(**pack_kwargs)
        return self.frame
    
    def ajouter_ligne(self, donnees: Dict[str, Any]):
        """Ajouter une ligne au tableau"""
        ligne = tuple(donnees.get(col, "") for col in self.colonnes)
        id_item = self.tree.insert("", "end", values=ligne)
        self.donnees.append(donnees)
        return id_item
    
    def ajouter_lignes(self, donnees_liste: List[Dict[str, Any]]):
        """Ajouter plusieurs lignes au tableau"""
        for donnees in donnees_liste:
            self.ajouter_ligne(donnees)
    
    def supprimer_ligne(self, index: int):
        """Supprimer une ligne par index"""
        items = self.tree.get_children()
        if 0 <= index < len(items):
            self.tree.delete(items[index])
            self.donnees.pop(index)
    
    def vider(self):
        """Vider le tableau"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.donnees.clear()
    
    def obtenir_donnees(self):
        """Obtenir toutes les données du tableau"""
        return self.donnees
    
    def obtenir_ligne_selectionnee(self):
        """Obtenir les données de la ligne sélectionnée"""
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            return self.donnees[index] if index < len(self.donnees) else None
        return None
    
    def get_widget(self):
        return self.tree


class Fenetre:
    """Classe pour créer une fenêtre principale"""
    def __init__(self, titre: str = "Application", largeur: int = 800, hauteur: int = 600, theme: str = "dark"):
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title(titre)
        self.root.geometry(f"{largeur}x{hauteur}")
    
    def ajouter_cadre(self, couleur_fond: str = "transparent"):
        """Ajouter un cadre/frame à la fenêtre"""
        frame = ctk.CTkFrame(self.root, fg_color=couleur_fond)
        return frame
    
    def lancer(self):
        """Lancer la boucle principale de la fenêtre"""
        self.root.mainloop()
    
    def fermer(self):
        """Fermer la fenêtre"""
        self.root.quit()
    
    def get_root(self):
        """Obtenir le widget root tkinter"""
        return self.root


class GestionnairePages:
    """Classe pour gérer plusieurs pages avec nettoyage automatique"""
    def __init__(self, root):
        self.root = root
        self.pages: Dict[str, ctk.CTkFrame] = {}
        self.page_actuelle: str = None
        self.callbacks: Dict[str, Callable] = {}  # Callback au changement de page
    
    def ajouter_page(self, nom: str, callback: Callable = None) -> ctk.CTkFrame:
        """Ajouter une nouvelle page"""
        frame = ctk.CTkFrame(self.root)
        self.pages[nom] = frame
        if callback:
            self.callbacks[nom] = callback
        return frame
    
    def obtenir_page(self, nom: str) -> ctk.CTkFrame:
        """Obtenir le frame d'une page"""
        return self.pages.get(nom)
    
    def nettoyer_page(self, nom: str):
        """Nettoyer tous les widgets d'une page"""
        if nom in self.pages:
            for widget in self.pages[nom].winfo_children():
                widget.destroy()
    
    def changer_page(self, nom: str, nettoyer: bool = False):
        """Changer vers une page différente"""
        if nom not in self.pages:
            raise ValueError(f"La page '{nom}' n'existe pas")
        
        # Masquer la page actuelle
        if self.page_actuelle:
            self.pages[self.page_actuelle].pack_forget()
            if nettoyer:
                self.nettoyer_page(self.page_actuelle)
        
        # Afficher la nouvelle page
        self.page_actuelle = nom
        self.pages[nom].pack(side="top", fill="both", expand=True)
        
        # Appeler le callback si défini
        if nom in self.callbacks:
            self.callbacks[nom]()
    
    def changer_page_et_reinit(self, nom: str):
        """Changer de page en nettoyant complètement l'ancienne"""
        self.changer_page(nom, nettoyer=True)
    
    def obtenir_page_actuelle(self) -> str:
        """Obtenir le nom de la page actuelle"""
        return self.page_actuelle


class Onglets:
    """Classe pour créer des onglets/pages"""
    def __init__(self, master):
        self.tabview = ctk.CTkTabview(master)
        self.onglets: Dict[str, ctk.CTkFrame] = {}
    
    def ajouter_onglet(self, nom: str) -> ctk.CTkFrame:
        """Ajouter un nouvel onglet et retourner son frame"""
        frame = self.tabview.add(nom)
        self.onglets[nom] = frame
        return frame
    
    def obtenir_onglet(self, nom: str) -> ctk.CTkFrame:
        """Obtenir le frame d'un onglet existant"""
        return self.onglets.get(nom)
    
    def supprimer_onglet(self, nom: str):
        """Supprimer un onglet"""
        if nom in self.onglets:
            self.tabview.delete(nom)
            del self.onglets[nom]
    
    def pack(self, **kwargs):
        """Afficher les onglets"""
        self.tabview.pack(fill=tk.BOTH, expand=True, **kwargs)
        return self.tabview
    
    def get_widget(self):
        """Obtenir le widget tabview"""
        return self.tabview
    
    def obtenir_onglet_actif(self) -> str:
        """Obtenir le nom de l'onglet actuellement actif"""
        return self.tabview.get()


# Exemple d'utilisation
if __name__ == "__main__":
    app = Fenetre("Application avec Gestion des Pages", 1000, 700)
    root = app.get_root()
    
    # Créer le gestionnaire de pages
    gestionnaire = GestionnairePages(root)
    
    # === PAGE 1: MENU PRINCIPAL ===
    page_menu = gestionnaire.ajouter_page("Menu")
    
    def init_menu():
        """Fonction appelée au changement vers cette page"""
        for widget in page_menu.winfo_children():
            widget.destroy()
        
        titre = Titre(page_menu, "Menu Principal")
        titre.pack()
        
        text_label = Label(page_menu, "Bienvenue dans notre application", size=18)
        text_label.pack()
        
        bouton1 = Bouton(page_menu, "Aller au Formulaire", 
                        command=lambda: gestionnaire.changer_page_et_reinit("Formulaire"))
        bouton1.pack()
        
        bouton2 = Bouton(page_menu, "Voir les Données", 
                        command=lambda: gestionnaire.changer_page("Donnees"))
        bouton2.pack()
    
    gestionnaire.callbacks["Menu"] = init_menu
    
    # === PAGE 2: FORMULAIRE ===
    page_formulaire = gestionnaire.ajouter_page("Formulaire")
    
    def init_formulaire():
        """Fonction appelée au changement vers cette page"""
        for widget in page_formulaire.winfo_children():
            widget.destroy()
        
        titre = Titre(page_formulaire, "Formulaire")
        titre.pack()
        
        label1 = Label(page_formulaire, "Entrez votre nom:", size=16)
        label1.pack()
        
        champ_nom = ChampTexte(page_formulaire)
        champ_nom.pack()
        
        label2 = Label(page_formulaire, "Sélectionnez une option:", size=16)
        label2.pack()
        
        selection = Selection(page_formulaire, "", ["Choix 1", "Choix 2", "Choix 3"], "Choix 1")
        selection.pack()
        
        label3 = Label(page_formulaire, "Accepter les conditions?", size=16)
        label3.pack()
        
        case = CaseACocher(page_formulaire, "J'accepte", default=False)
        case.pack()
        
        def retourner_au_menu():
            gestionnaire.changer_page_et_reinit("Menu")
        
        bouton_retour = Bouton(page_formulaire, "Retour au Menu", 
                              command=retourner_au_menu)
        bouton_retour.pack()
    
    gestionnaire.callbacks["Formulaire"] = init_formulaire
    
    # === PAGE 3: DONNÉES ===
    page_donnees = gestionnaire.ajouter_page("Donnees")
    
    def init_donnees():
        """Fonction appelée au changement vers cette page"""
        for widget in page_donnees.winfo_children():
            widget.destroy()
        
        titre = Titre(page_donnees, "Données")
        titre.pack()
        
        tableau = Tableau(page_donnees, ["Nom", "Âge", "Ville"], hauteur=12)
        tableau.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tableau.ajouter_lignes([
            {"Nom": "Alice", "Âge": 25, "Ville": "Paris"},
            {"Nom": "Bob", "Âge": 30, "Ville": "Lyon"},
            {"Nom": "Charlie", "Âge": 35, "Ville": "Marseille"},
            {"Nom": "Diana", "Âge": 28, "Ville": "Toulouse"},
            {"Nom": "Eve", "Âge": 32, "Ville": "Nice"},
        ])
        
        def retourner_au_menu():
            gestionnaire.changer_page_et_reinit("Menu")
        
        bouton_retour = Bouton(page_donnees, "Retour au Menu", 
                              command=retourner_au_menu)
        bouton_retour.pack()
    
    gestionnaire.callbacks["Donnees"] = init_donnees
    
    # Aller à la page menu au démarrage
    gestionnaire.changer_page("Menu")
    
    app.lancer()