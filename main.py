from IHM.main import *


class MenuPrincipal(ctk.CTkFrame):
    """Page du menu principal"""
    
    def __init__(self, parent, application):
        super().__init__(parent)
        self.parent = parent
        self.application = application
        self.initialisation()
    
    def initialisation(self):
        """Initialiser les éléments de la page"""
        # Titre principal
        titre = Titre(self, "Optimisation Linéaire")
        titre.pack(pady=20)
        
        # Texte de description
        description = Label(self, 
                          "Bienvenue dans l'outil d'optimisation linéaire\nMéthode du Simplexe", 
                          size=16)
        description.pack(pady=10)
        
        # Boutons principaux
        bouton_donnees = Bouton(self, "Entrer les données", 
                               command=self.aller_formulaire)
        bouton_donnees.pack(pady=10)
        
        bouton_charger = Bouton(self, "Charger un fichier", 
                               command=self.charger_fichier)
        bouton_charger.pack(pady=10)
        
        bouton_quitter = Bouton(self, "Quitter", 
                               command=self.application.quitter)
        bouton_quitter.pack(pady=10)
    
    def aller_formulaire(self):
        """Aller à la page de saisie"""
        self.application.afficher_page("Formulaire")
    
    def charger_fichier(self):
        """Charger un fichier"""
        messagebox.showinfo("Charger", "Fonctionnalité à venir")


class FormulaireSaisie(ctk.CTkFrame):
    """Page de formulaire de saisie des dimensions"""
    
    def __init__(self, parent, application):
        super().__init__(parent)
        self.parent = parent
        self.application = application
        self.champ_vars = None
        self.champ_contraintes = None
        self.initialisation()
    
    def initialisation(self):
        """Initialiser les éléments de la page"""
        # Titre
        titre = Titre(self, "Configuration du Problème")
        titre.pack(pady=20)
        
        # Description
        description = Label(self, 
                          "Veuillez entrer le nombre de variables et de contraintes", 
                          size=14)
        description.pack(pady=10)
        
        # Frame pour les champs
        frame_champs = ctk.CTkFrame(self, fg_color="transparent")
        frame_champs.pack(pady=20)
        
        # Nombre de variables
        label_vars = Label(frame_champs, "Nombre de variables:", size=14)
        label_vars.pack(pady=5)
        
        self.champ_vars = ChampTexte(frame_champs)
        self.champ_vars.pack(pady=5)
        
        # Nombre de contraintes
        label_contraintes = Label(frame_champs, "Nombre de contraintes:", size=14)
        label_contraintes.pack(pady=5)
        
        self.champ_contraintes = ChampTexte(frame_champs)
        self.champ_contraintes.pack(pady=5)
        
        # Boutons d'action
        frame_boutons = ctk.CTkFrame(self, fg_color="transparent")
        frame_boutons.pack(pady=20)
        
        bouton_retour = Bouton(frame_boutons, "Retour", 
                              command=self.retourner_menu, position="left")
        bouton_retour.pack()
        
        bouton_valider = Bouton(frame_boutons, "Suivant", 
                               command=self.valider, position="left")
        bouton_valider.pack()
    
    def valider(self):
        """Valider et aller à la page suivante"""
        try:
            num_var = int(self.champ_vars.get())
            num_cont = int(self.champ_contraintes.get())
            
            if num_var <= 0 or num_cont <= 0:
                messagebox.showerror("Erreur", 
                                    "Le nombre de variables et de contraintes doit être positif")
                return
            
            # Stocker les données
            self.application.num_variables = num_var
            self.application.num_contraintes = num_cont
            
            # Aller à la page de saisie des coefficients
            self.application.afficher_page("Coefficients")
            
        except ValueError:
            messagebox.showerror("Erreur", 
                                "Veuillez entrer des nombres entiers valides")
    
    def retourner_menu(self):
        """Retourner au menu principal"""
        self.application.afficher_page("Menu")


class PageCoefficients(ctk.CTkFrame):
    """Page de saisie des coefficients"""
    
    def __init__(self, parent, application):
        super().__init__(parent)
        self.parent = parent
        self.application = application
        self.champs_objectif = []
        self.champs_contraintes = []
        self.selections_positivite = []
        self.selection_objectif = None
        self.derniere_config = None  # Track dernière configuration pour éviter recreations
    
    def doit_reinitialiser(self):
        """Vérifier si la page doit être réinitialisée"""
        config_actuelle = (self.application.num_variables, self.application.num_contraintes)
        if self.derniere_config != config_actuelle:
            self.derniere_config = config_actuelle
            return True
        return False
    
    def reinitialiser(self):
        """Réinitialiser la page seulement si la config a changé"""
        if not self.doit_reinitialiser():
            return  # Ne pas recréer si config identique
        
        # Nettoyer les anciens éléments
        for widget in self.winfo_children():
            widget.destroy()
        
        self.champs_objectif = []
        self.champs_contraintes = []
        self.selections_positivite = []
        self.selection_objectif = None
        self.initialisation()
    
    def initialisation(self):
        """Initialiser les éléments de la page avec un système de grille type formulaire web"""
        # Titre principal
        titre = Titre(self, "Saisie des Coefficients")
        titre.pack(pady=10)
        
        # Frame scrollable pour tout le contenu (vertical + horizontal)
        frame_scroll = ctk.CTkFrame(self, fg_color="transparent")
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fg_color = frame_scroll.cget("fg_color")
        if fg_color == "transparent":
            fg_color = self.cget("fg_color")
        if fg_color == "transparent":
            fg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        canvas_bg = frame_scroll._apply_appearance_mode(fg_color)
        canvas = tk.Canvas(frame_scroll, highlightthickness=0, bd=0, bg=canvas_bg)

        v_scroll = ctk.CTkScrollbar(frame_scroll, orientation="vertical", command=canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ctk.CTkScrollbar(frame_scroll, orientation="horizontal", command=canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Frame interne pour le contenu
        inner_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def on_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)

        # Créer le frame principal avec grid
        frame_grid = ctk.CTkFrame(inner_frame, fg_color="transparent")
        frame_grid.pack(fill=tk.BOTH, expand=True)
        
        # === LIGNE 1 : EN-TÊTES DES VARIABLES ===
        # Colonne 0 : vide
        label_vide = ctk.CTkLabel(frame_grid, text="", width=100, anchor="w")
        label_vide.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Colonnes pour les variables
        for i in range(self.application.num_variables):
            col = i * 2 + 1  # Pour laisser de la place aux signes +
            
            # Nom variable
            var_text = f"x₁" if i == 0 else f"x{i+1}"
            label_var = ctk.CTkLabel(frame_grid, text=var_text, font=('Arial', 12, 'bold'))
            label_var.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
            
            # Signe + (sauf après la dernière variable)
            if i < self.application.num_variables - 1:
                label_plus = ctk.CTkLabel(frame_grid, text="+", font=('Arial', 12))
                label_plus.grid(row=0, column=col + 1, padx=2, pady=5)
        
        # Colonne pour l'opérateur
        col_op = self.application.num_variables * 2
        label_op = ctk.CTkLabel(frame_grid, text="", width=50)
        label_op.grid(row=0, column=col_op, padx=5, pady=5)
        
        # Colonne pour le second membre
        col_membre = self.application.num_variables * 2 + 1
        label_membre = ctk.CTkLabel(frame_grid, text="", width=50)
        label_membre.grid(row=0, column=col_membre, padx=5, pady=5)
        
        # === LIGNE 2 : CONTRAINTES DE POSITIVITÉ ===
        for i in range(self.application.num_variables):
            col = i * 2 + 1
            
            # Sélection de positivité (directement CTkComboBox)
            combo = ctk.CTkComboBox(frame_grid, values=["≥0", "≤0", "∈ℝ"], state="readonly")
            combo.set("≥0")
            combo.grid(row=1, column=col, padx=2, pady=2, sticky="ew")
            self.selections_positivite.append(combo)
        
        # === CONTRAINTES ===
        for j in range(self.application.num_contraintes):
            row = j + 2
            
            # Étiquette de la contrainte
            label_contrainte = ctk.CTkLabel(frame_grid, 
                                           text=f"Contrainte {j+1} :", 
                                           width=100, anchor="w", font=('Arial', 10))
            label_contrainte.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
            
            ligne_champs = []
            
            # Champs pour les coefficients avec signes +
            for i in range(self.application.num_variables):
                col = i * 2 + 1
                
                # Champ pour le coefficient
                champ = ChampTexte(frame_grid)
                champ.entry.configure(width=4)
                champ.entry.grid(row=row, column=col, padx=2, pady=5, sticky="ew")
                ligne_champs.append(champ)
                
                # Signe + (sauf après la dernière variable)
                if i < self.application.num_variables - 1:
                    label_plus = ctk.CTkLabel(frame_grid, text="+", font=('Arial', 10))
                    label_plus.grid(row=row, column=col + 1, padx=2, pady=5)
            
            # Opérateur (<=, >=, =)
            selection_op = ctk.CTkComboBox(frame_grid, values=["≤", "≥", "="], state="readonly")
            selection_op.set("≤")
            selection_op.grid(row=row, column=col_op, padx=5, pady=5, sticky="ew")
            ligne_champs.append(selection_op)
            
            # Second membre
            champ_membre = ChampTexte(frame_grid)
            champ_membre.entry.configure(width=4)
            champ_membre.entry.grid(row=row, column=col_membre, padx=5, pady=5, sticky="ew")
            ligne_champs.append(champ_membre)
            
            self.champs_contraintes.append(ligne_champs)
        
        # === LIGNE OBJECTIF (vide, pour séparation) ===
        row_sep = self.application.num_contraintes + 2
        label_sep = ctk.CTkLabel(frame_grid, text="Objectif", font=('Arial', 10, 'bold'))
        label_sep.grid(row=row_sep, column=0, padx=5, pady=10, sticky="ew")
        
        # === LIGNE OBJECTIF (avec Min/Max et coefficients) ===
        row_obj = self.application.num_contraintes + 3
        
        # Sélection Min/Max
        selection_obj = ctk.CTkComboBox(frame_grid, values=["Min", "Max"], state="readonly")
        selection_obj.set("Max")
        selection_obj.grid(row=row_obj, column=0, padx=5, pady=10, sticky="ew")
        self.selection_objectif = selection_obj
        
        # Champs pour l'objectif avec signes +
        for i in range(self.application.num_variables):
            col = i * 2 + 1
            
            # Champ pour le coefficient
            champ = ChampTexte(frame_grid)
            champ.entry.configure(width=4)
            champ.entry.grid(row=row_obj, column=col, padx=2, pady=10, sticky="ew")
            self.champs_objectif.append(champ)
            
            # Signe + (sauf après la dernière variable)
            if i < self.application.num_variables - 1:
                label_plus = ctk.CTkLabel(frame_grid, text="+", font=('Arial', 10))
                label_plus.grid(row=row_obj, column=col + 1, padx=2, pady=10)
        
        # Configurer les poids des colonnes pour l'équilibre
        frame_grid.columnconfigure(0, weight=1, minsize=100)
        for i in range(1, self.application.num_variables * 2 + 2):
            if (i - 1) % 2 == 0:  # Colonnes des variables
                frame_grid.columnconfigure(i, weight=1, minsize=80)
            else:  # Colonnes des signes +
                frame_grid.columnconfigure(i, weight=0, minsize=20)
        
        # === BOUTONS ===
        frame_boutons = ctk.CTkFrame(self, fg_color="transparent")
        frame_boutons.pack(pady=10)
        
        bouton_retour = Bouton(frame_boutons, "Retour", 
                              command=self.retourner_formulaire, position="left")
        bouton_retour.pack()
        
        bouton_resoudre = Bouton(frame_boutons, "Résoudre", 
                                command=self.resoudre, position="left")
        bouton_resoudre.pack()
    
    def retourner_formulaire(self):
        """Retourner à la page de formulaire"""
        self.application.afficher_page("Formulaire")
    
    def resoudre(self):
        """Résoudre le problème"""
        messagebox.showinfo("Résoudre", 
                           "Les données seront traitées à l'étape suivante.\n" +
                           "Fonctionnalité d'optimisation en cours de développement.")
        self.application.afficher_page("Menu")


class OptimisationLineaire:
    """Application pour l'optimisation linéaire"""
    
    def __init__(self):
        self.app = Fenetre("Optimisation Linéaire", 1000, 700, theme="dark")
        self.root = self.app.get_root()
        
        # Variables pour stocker les données de l'optimisation
        self.num_variables = None
        self.num_contraintes = None
        
        # Créer les pages
        self.page_menu = MenuPrincipal(self.root, self)
        self.page_formulaire = FormulaireSaisie(self.root, self)
        self.page_coefficients = PageCoefficients(self.root, self)
        
        self.pages = {
            "Menu": self.page_menu,
            "Formulaire": self.page_formulaire,
            "Coefficients": self.page_coefficients
        }
        
        self.page_actuelle = None
        
        # Aller à la page menu
        self.afficher_page("Menu")
    
    def afficher_page(self, nom_page: str):
        """Afficher une page et masquer les autres"""
        # Masquer la page actuelle
        if self.page_actuelle:
            self.pages[self.page_actuelle].pack_forget()
        
        # Réinitialiser la page Coefficients si nécessaire
        if nom_page == "Coefficients":
            self.page_coefficients.reinitialiser()
        
        # Afficher la nouvelle page
        self.page_actuelle = nom_page
        self.pages[nom_page].pack(side="top", fill="both", expand=True)
    
    def quitter(self):
        """Quitter l'application"""
        if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter?"):
            self.app.fermer()
    
    def lancer(self):
        """Lancer l'application"""
        self.app.lancer()


if __name__ == "__main__":
    app = OptimisationLineaire()
    app.lancer()
