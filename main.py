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
    
    def collecter_donnees(self):
        """Collecter les données du formulaire"""
        try:
            # Collecter l'objectif
            directif = self.selection_objectif.get()
            coeffs_objective = []
            for champ in self.champs_objectif:
                val = float(champ.get()) if champ.get() else 0
                coeffs_objective.append(val)
            
            # IMPORTANT: Dans le tableau du simplexe, on met toujours les coefficients positifs
            # Pour Max cx, on utilise [c1, c2, ...] et on regarde le RHS
            # Pour Min cx, on utilise [c1, c2, ...] et on regarde le RHS
            # La formulation dépend de comment on setup le problème
            
            coeffs_objective.append(0)  # RHS
            
            # Collecter les contraintes
            contraintes = []
            for ligne in self.champs_contraintes:
                coeffs = []
                for i in range(self.application.num_variables):
                    val = float(ligne[i].get()) if ligne[i].get() else 0
                    coeffs.append(val)
                
                # Opérateur
                operateur = ligne[self.application.num_variables].get()
                
                # RHS
                rhs = float(ligne[self.application.num_variables + 1].get()) if ligne[self.application.num_variables + 1].get() else 0
                
                contraintes.append({
                    'coefficients': coeffs,
                    'operateur': operateur,
                    'rhs': rhs
                })
            
            # Collecter les contraintes de positivité
            positivites = [combo.get() for combo in self.selections_positivite]
            
            return {
                'directif': directif,
                'objective': coeffs_objective,
                'contraintes': contraintes,
                'positivites': positivites,
                'num_variables': self.application.num_variables,
                'num_contraintes': self.application.num_contraintes
            }
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")
            return None
    
    def resoudre(self):
        """Résoudre le problème"""
        donnees = self.collecter_donnees()
        if donnees is None:
            return
        
        # Stocker les données dans l'application
        self.application.donnees = donnees
        
        # Aller à la page de résultats
        self.application.afficher_page("Resultats")


class PageResultats(ctk.CTkFrame):
    """Page d'affichage des résultats du simplexe"""
    
    def __init__(self, parent, application):
        super().__init__(parent)
        self.parent = parent
        self.application = application
        self.etape_actuelle = 0
        self.initialisation()
    
    def initialisation(self):
        """Initialiser les éléments de la page"""
        # Titre
        titre = Titre(self, "Résultats du Simplexe")
        titre.pack(pady=10)
        
        # Frame de contrôle des étapes
        frame_controle = ctk.CTkFrame(self, fg_color="transparent")
        frame_controle.pack(pady=10, fill="x", padx=20)
        
        # Bouton précédent
        self.btn_precedent = ctk.CTkButton(frame_controle, text="← Précédent", 
                                          command=self.etape_precedente, width=120)
        self.btn_precedent.pack(side=tk.LEFT, padx=5)
        
        # Label pour le numéro d'étape
        self.label_etape = ctk.CTkLabel(frame_controle, text="", font=('Arial', 14))
        self.label_etape.pack(side=tk.LEFT, padx=20)
        
        # Bouton suivant
        self.btn_suivant = ctk.CTkButton(frame_controle, text="Suivant →", 
                                        command=self.etape_suivante, width=120)
        self.btn_suivant.pack(side=tk.LEFT, padx=5)
        
        # Frame scrollable pour le contenu (tableau et infos)
        frame_scroll = ctk.CTkFrame(self, fg_color="transparent")
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas avec scrollbar
        fg_color = frame_scroll.cget("fg_color")
        if fg_color == "transparent":
            fg_color = self.cget("fg_color")
        if fg_color == "transparent":
            fg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        canvas_bg = frame_scroll._apply_appearance_mode(fg_color)
        
        self.canvas = tk.Canvas(frame_scroll, highlightthickness=0, bd=0, bg=canvas_bg)
        scrollbar = ctk.CTkScrollbar(frame_scroll, orientation="vertical", command=self.canvas.yview)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame interne pour le contenu
        self.inner_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        def on_canvas_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        self.inner_frame.bind("<Configure>", on_canvas_configure)
        
        # Frame de boutons d'action
        frame_boutons = ctk.CTkFrame(self, fg_color="transparent")
        frame_boutons.pack(pady=10)
        
        bouton_retour = Bouton(frame_boutons, "Retour", 
                              command=self.retourner_coefficients, position="left")
        bouton_retour.pack()
        
        bouton_menu = Bouton(frame_boutons, "Menu Principal", 
                            command=self.aller_menu, position="left")
        bouton_menu.pack()
        
        # Initialiser simplex_data
        self.simplex_data = None
        
        # Afficher le message d'attente
        label_attente = ctk.CTkLabel(self.inner_frame, 
                                    text="En attente de données...\nVeuillez cliquer sur 'Résoudre' depuis la page des coefficients",
                                    font=('Arial', 14), text_color="gray")
        label_attente.pack(pady=50)
    
    def resoudre(self):
        """Résoudre le problème avec le simplexe"""
        from Algo.simplexe import simplexe, Fraction
        
        donnees = self.application.donnees
        
        # Vérifier que les données sont disponibles
        if donnees is None:
            messagebox.showerror("Erreur", "Aucune donnée disponible. Veuillez remplir le formulaire.")
            return
        
        # Construire le tableau du simplexe
        # Format: [[objectif_coeffs..., RHS], [contrainte1_coeffs..., RHS], ...]
        
        num_var = donnees['num_variables']
        num_cont = donnees['num_contraintes']
        
        # Ligne objectif avec variables d'écart
        obj = donnees['objective'][:-1]  # Enlever RHS temporaire
        # Ajouter 0 pour chaque variable d'écart
        obj = obj + [0] * num_cont + [0]  # RHS final
        
        tableau = [obj]
        
        # Lignes des contraintes
        for idx, contrainte in enumerate(donnees['contraintes']):
            ligne = contrainte['coefficients'].copy()
            
            # Ajouter les variables d'écart (identité)
            for i in range(num_cont):
                ligne.append(1 if i == idx else 0)
            
            # RHS
            ligne.append(float(contrainte['rhs']))
            tableau.append(ligne)
        
        # Convertir en floats pour le calcul
        tableau = [[float(x) for x in ligne] for ligne in tableau]
        
        # Lancer le simplexe
        try:
            self.simplex_data = simplexe(tableau, num_var, num_cont)
            self.etape_actuelle = 0
            
            # Afficher la première étape
            self.afficher_etape()
        except Exception as e:
            # Afficher l'erreur
            for widget in self.inner_frame.winfo_children():
                widget.destroy()
            label_erreur = ctk.CTkLabel(self.inner_frame, 
                                       text=f"Erreur: {str(e)}",
                                       font=('Arial', 14), text_color="red")
            label_erreur.pack(pady=20)
            print(f"Erreur lors de la résolution: {e}")
            import traceback
            traceback.print_exc()

    def on_show(self):
        """Called when the page is shown via afficher_page().
        Lance automatiquement la résolution si des données existent,
        sinon actualise l'affichage si une résolution est déjà présente."""
        # Si des données sont prêtes et qu'on n'a pas encore calculé
        if getattr(self.application, 'donnees', None) is not None and self.simplex_data is None:
            self.resoudre()
            return

        # Si on a déjà des résultats, les afficher
        if self.simplex_data is not None:
            self.afficher_etape()

    def afficher_etape(self):
        """Afficher l'étape actuelle"""
        # Nettoyer le contenu précédent
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        
        # Vérifier si des données sont disponibles
        if self.simplex_data is None:
            label_vide = ctk.CTkLabel(self.inner_frame, 
                                     text="En attente de données...\nVeuillez cliquer sur 'Résoudre' depuis la page des coefficients",
                                     font=('Arial', 14), text_color="gray")
            label_vide.pack(pady=50)
            self.label_etape.configure(text="Aucune résolution")
            self.btn_precedent.configure(state="disabled")
            self.btn_suivant.configure(state="disabled")
            return
        
        if not self.simplex_data.est_resolvable:
            label_erreur = ctk.CTkLabel(self.inner_frame, 
                                       text=f"Erreur: {self.simplex_data.message_erreur}",
                                       font=('Arial', 14), text_color="red")
            label_erreur.pack(pady=20)
            return
        
        etapes = self.simplex_data.obtenir_etapes()
        if self.etape_actuelle >= len(etapes):
            self.etape_actuelle = len(etapes) - 1
        
        etape = etapes[self.etape_actuelle]
        
        # Mettre à jour le label d'étape
        self.label_etape.configure(text=f"{etape['titre']} ({self.etape_actuelle + 1}/{len(etapes)})")
        
        # Mettre à jour les boutons
        self.btn_precedent.configure(state="normal" if self.etape_actuelle > 0 else "disabled")
        self.btn_suivant.configure(state="normal" if self.etape_actuelle < len(etapes) - 1 else "disabled")
        
        # === AFFICHER LES INFOS DE L'ÉTAPE ===
        if etape['var_entrante'] and etape['var_sortante']:
            frame_infos = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
            frame_infos.pack(pady=10, padx=10, fill="x")
            
            # Titre de l'itération
            titre_iter = ctk.CTkLabel(frame_infos, 
                                     text=f"📊 {etape['titre']}", 
                                     font=('Arial', 14, 'bold'), text_color="lightgreen")
            titre_iter.pack(side=tk.LEFT, padx=5)
            
            # Info variables
            info_text = f"Entrante: {etape['var_entrante']} | Sortante: {etape['var_sortante']} | Pivot: {etape['pivot_element'] if isinstance(etape['pivot_element'], (int, float)) else float(etape['pivot_element']):.2f}"
            label_info = ctk.CTkLabel(frame_infos, 
                                     text=info_text,
                                     font=('Arial', 12), text_color="lightyellow")
            label_info.pack(side=tk.LEFT, padx=20)
            
            # Variables de base
            if etape['variables_base']:
                vars_base_text = ", ".join([f"{var}={etape['tableau'][i][-1]:.2f}" 
                                           if var != 'Z' else 'Z'
                                           for i, var in enumerate(etape['variables_base'][1:])])
                label_base = ctk.CTkLabel(frame_infos, 
                                         text=f"Base: {vars_base_text}",
                                         font=('Arial', 10), text_color="lightcyan")
                label_base.pack(side=tk.LEFT, padx=20)
        
        # === AFFICHER LE TABLEAU ===
        self.afficher_tableau(etape['tableau'], 
                             etape['index_entrante'], 
                             etape['index_sortante'])

    
    def afficher_tableau(self, tableau, index_entrante=None, index_sortante=None):
        """Afficher le tableau du simplexe de manière ergonomique"""
        frame_tableau = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        frame_tableau.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Créer un texte affichable
        donnees = self.application.donnees
        num_var = donnees['num_variables']
        num_cont = donnees['num_contraintes']
        num_cols = num_var + num_cont + 1  # variables + écarts + RHS
        
        # Calcul des largeurs de colonnes pour l'alignement
        col_width = 12
        
        # En-têtes des colonnes
        entete = "    "
        entete += "|".join(f" {'Z':^{col_width}} ".replace(" ", ""))
        for i in range(num_var):
            entete += f"| {f'x{i+1}':^{col_width}} "
        for i in range(num_cont):
            entete += f"| {f'y{i+1}':^{col_width}} "
        entete += f"| {'RHS':^{col_width}} \n"
        
        # Barre de séparation
        barre = "=" * (len(entete) - 1) + "\n"
        
        # Afficher le tableau avec formatage speciale pour le pivot
        contenu = entete + barre
        
        labels = ["Z"] + [f"C{i}" for i in range(1, num_cont + 1)]
        
        for row_idx, ligne in enumerate(tableau):
            # Étiquette de ligne
            etiquette = f"{labels[row_idx]:>3} |"
            
            # Valeurs de la ligne
            for col_idx, val in enumerate(ligne[:-1]):
                try:
                    val_float = float(val)
                except:
                    val_float = 0
                
                # Formatage du pivot
                if row_idx == index_sortante and col_idx == index_entrante:
                    val_str = f"[{val_float:7.2f}]"  # Pivot en gras
                else:
                    val_str = f" {val_float:7.2f} "
                
                etiquette += f" {val_str:^{col_width}} |"
            
            # RHS
            try:
                rhs_float = float(ligne[-1])
            except:
                rhs_float = 0
            rhs_str = f" {rhs_float:7.2f} "
            etiquette += f" {rhs_str:^{col_width}} \n"
            
            contenu += etiquette
        
        # Afficher avec Text widget (non-modifiable)
        text_widget = tk.Text(frame_tableau, height=len(tableau) + 3, 
                             width=max(100, len(entete)), 
                             bg="#212121", fg="white", font=('Courier', 9))
        text_widget.pack(pady=10, padx=10)
        
        # Insérer le contenu avec coloration
        text_widget.insert("1.0", contenu)
        
        # Mettre en évidence le pivot
        if index_entrante is not None and index_sortante is not None:
            # Chercher et colorer le pivot (pattern: [...])
            start_search = f"{index_sortante + 1}.0"
            while True:
                pos = text_widget.search(r"\[.*\]", start_search, regexp=True, stopindex="end")
                if not pos:
                    break
                end_pos = text_widget.index(f"{pos} + 10c")
                text_widget.tag_add("pivot", pos, end_pos)
                start_search = end_pos
        
        # Configuration des tags
        text_widget.tag_config("pivot", foreground="yellow", background="red")
        text_widget.config(state="disabled")

    
    def etape_precedente(self):
        """Aller à l'étape précédente"""
        if self.simplex_data is None:
            messagebox.showwarning("Attention", "Veuillez d'abord résoudre un problème")
            return
        if self.etape_actuelle > 0:
            self.etape_actuelle -= 1
            self.afficher_etape()
    
    def etape_suivante(self):
        """Aller à l'étape suivante"""
        if self.simplex_data is None:
            messagebox.showwarning("Attention", "Veuillez d'abord résoudre un problème")
            return
        etapes = self.simplex_data.obtenir_etapes()
        if self.etape_actuelle < len(etapes) - 1:
            self.etape_actuelle += 1
            self.afficher_etape()
    
    def retourner_coefficients(self):
        """Retourner à la page de coefficients"""
        self.application.afficher_page("Coefficients")
    
    def aller_menu(self):
        """Aller au menu principal"""
        self.application.afficher_page("Menu")



class OptimisationLineaire:
    """Application pour l'optimisation linéaire"""
    
    def __init__(self):
        self.app = Fenetre("Optimisation Linéaire", 1000, 700, theme="dark")
        self.root = self.app.get_root()
        
        # Variables pour stocker les données de l'optimisation
        self.num_variables = None
        self.num_contraintes = None
        self.donnees = None
        
        # Créer les pages
        self.page_menu = MenuPrincipal(self.root, self)
        self.page_formulaire = FormulaireSaisie(self.root, self)
        self.page_coefficients = PageCoefficients(self.root, self)
        self.page_resultats = PageResultats(self.root, self)
        
        self.pages = {
            "Menu": self.page_menu,
            "Formulaire": self.page_formulaire,
            "Coefficients": self.page_coefficients,
            "Resultats": self.page_resultats
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
        page = self.pages[nom_page]
        page.pack(side="top", fill="both", expand=True)

        # Appeler un hook "on_show" si la page le fournit (utile pour rafraîchir/initialiser)
        if hasattr(page, 'on_show') and callable(getattr(page, 'on_show')):
            try:
                page.on_show()
            except Exception as e:
                print(f"Erreur dans on_show() de la page {nom_page}: {e}")
    
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
