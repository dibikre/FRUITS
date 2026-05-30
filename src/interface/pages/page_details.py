# -*- coding: utf-8 -*-
"""
Module contenant la page de détails sur les fruits
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
                              QComboBox, QLineEdit, QPushButton, QGridLayout, QMessageBox, QDialog)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, Signal, Slot, QSize

import os
import json
import pathlib

from ..widgets.carte_fruit import CarteFruit
from ..widgets.bouton_anime import BoutonAnime
from ..widgets.dialog_ajout_fruit import DialogAjoutFruit
from ...outils.gestionnaire_donnees import GestionnaireDonnees
from ...constantes import *

class DetailsFruit(QWidget):
    """
    Widget affichant les détails complets d'un fruit
    """
    
    fermeture = Signal()  # Signal émis lors de la fermeture de la vue détaillée
    
    def __init__(self, fruit_info, parent=None):
        """
        Initialise la vue détaillée d'un fruit
        
        Args:
            fruit_info (dict): Informations sur le fruit
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        self.fruit_info = fruit_info
        
        # Conversion du chemin relatif en chemin absolu si ce n'est pas déjà fait
        if "direction" in self.fruit_info and not os.path.isabs(self.fruit_info["direction"]):
            chemin_relatif = self.fruit_info["direction"]
            # Déterminer le chemin de base du projet
            chemin_fichier_actuel = pathlib.Path(__file__)
            # Remonter de 3 niveaux (pages -> interface -> src -> racine du projet)
            base_path = chemin_fichier_actuel.parent.parent.parent.parent.absolute()
            chemin_absolu = os.path.join(base_path, chemin_relatif)
            self.fruit_info["direction"] = chemin_absolu
        
        # Configuration du widget
        self.setStyleSheet("""
            QWidget {
                background-color: #0D1117;
            }
        """)
        
        # Création de l'interface
        self._creer_interface()
    
    def _creer_interface(self):
        """Crée l'interface de la vue détaillée"""
        # Disposition principale
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Bouton de retour
        retour_layout = QHBoxLayout()
        
        retour_btn = BoutonAnime("Retour à la liste")
        retour_btn.setIcon(QIcon.fromTheme("go-previous"))
        retour_btn.clicked.connect(self.fermeture.emit)
        retour_layout.addWidget(retour_btn)
        retour_layout.addStretch()
        
        layout.addLayout(retour_layout)
        
        # Titre du fruit
        titre_layout = QHBoxLayout()
        
        # Image du fruit (si disponible)
        if "direction" in self.fruit_info and os.path.exists(self.fruit_info["direction"]):
            try:
                img_label = QLabel()
                pixmap_source = QPixmap(self.fruit_info["direction"]).scaled(120, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                pixmap_rond = QPixmap(120, 120)
                pixmap_rond.fill(Qt.transparent)
                from PySide6.QtGui import QPainter, QPainterPath
                painter = QPainter(pixmap_rond)
                painter.setRenderHint(QPainter.Antialiasing)
                path = QPainterPath()
                path.addEllipse(0, 0, 120, 120)
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, pixmap_source)
                painter.end()
                img_label.setPixmap(pixmap_rond)
                img_label.setFixedSize(120, 120)
                img_label.setAlignment(Qt.AlignCenter)
                titre_layout.addWidget(img_label)
            except Exception as e:
                print(f"Erreur lors du chargement de l'image: {e}")
        
        # Informations principales
        info_layout = QVBoxLayout()
        
        # Nom du fruit
        nom_label = QLabel(self.fruit_info["nom"])
        font_titre = QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE)
        font_titre.setBold(True)
        nom_label.setFont(font_titre)
        info_layout.addWidget(nom_label)
        
        # Famille
        famille_label = QLabel(f"Famille: {self.fruit_info.get('famille', 'Inconnue')}")
        font = QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL)
        font.setItalic(True)
        famille_label.setFont(font)
        famille_label.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
        info_layout.addWidget(famille_label)
        
        # Origine
        if "origine" in self.fruit_info:
            origine_label = QLabel(f"Origine: {self.fruit_info['origine']}")
            origine_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
            info_layout.addWidget(origine_label)
        
        # Saison
        if "saison" in self.fruit_info:
            saisons = ", ".join(self.fruit_info["saison"])
            saison_label = QLabel(f"Saison: {saisons}")
            saison_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
            info_layout.addWidget(saison_label)
        
        titre_layout.addLayout(info_layout)
        titre_layout.addStretch()
        
        layout.addLayout(titre_layout)
        
        # Description
        description_titre = QLabel("Description")
        description_titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        layout.addWidget(description_titre)
        
        description_label = QLabel(self.fruit_info["description"])
        description_label.setWordWrap(True)
        description_label.setStyleSheet("""
            QLabel {
                background-color: #141D2B;
                border-radius: 8px;
                border: 1px solid #2B3648;
                padding: 15px;
            }
        """)
        layout.addWidget(description_label)
        
        # Propriétés nutritives
        if "proprietes_nutritives" in self.fruit_info:
            nutrition_titre = QLabel("Propriétés nutritives")
            nutrition_titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
            layout.addWidget(nutrition_titre)
            
            nutrition_grid = QGridLayout()
            nutrition_grid.setSpacing(10)
            
            prop_nutritives = self.fruit_info["proprietes_nutritives"]
            for i, (cle, valeur) in enumerate(prop_nutritives.items()):
                # Formatage de la clé (premier caractère en majuscule, remplacement des underscores)
                cle_formatee = cle.replace("_", " ").capitalize()
                
                # Création des labels
                cle_label = QLabel(f"{cle_formatee}:")
                cle_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
                
                valeur_label = QLabel(str(valeur))
                font_valeur = QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL)
                font_valeur.setBold(True)
                valeur_label.setFont(font_valeur)
                valeur_label.setStyleSheet(f"color: {COULEUR_ACCENT};")
                
                # Ajout à la grille
                row = i // 2
                col = (i % 2) * 2
                
                nutrition_grid.addWidget(cle_label, row, col)
                nutrition_grid.addWidget(valeur_label, row, col+1)
            
            nutrition_widget = QWidget()
            nutrition_widget.setLayout(nutrition_grid)
            nutrition_widget.setStyleSheet("""
                QWidget {
                    background-color: #141D2B;
                    border-radius: 8px;
                    border: 1px solid #2B3648;
                    padding: 15px;
                }
            """)
            
            layout.addWidget(nutrition_widget)
        
        layout.addStretch()

class PageDetails(QWidget):
    """
    Page affichant les détails sur les fruits
    """
    
    def __init__(self, parent=None):
        """
        Initialise la page de détails
        
        Args:
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Variables de classe
        self.gestionnaire = GestionnaireDonnees()
        self.fruits_info = self.gestionnaire.charger_fruits_info()
        self.vue_detaillee = None
        
        # Convertir les chemins relatifs en chemins absolus
        self._convertir_chemins_images()
        
        # Création de l'interface
        self._creer_interface()
    
    def _convertir_chemins_images(self):
        """Convertit les chemins relatifs des images en chemins absolus"""
        # Déterminer le chemin de base du projet en remontant à la racine
        # En supposant que le fichier actuel est dans src/interface/pages/
        chemin_fichier_actuel = pathlib.Path(__file__)
        # Remonter de 3 niveaux (pages -> interface -> src -> racine du projet)
        base_path = chemin_fichier_actuel.parent.parent.parent.parent.absolute()
        
        for fruit in self.fruits_info["fruits"]:
            if "direction" in fruit:
                chemin_relatif = fruit["direction"]
                chemin_absolu = os.path.join(base_path, chemin_relatif)
                fruit["direction"] = chemin_absolu
    
    def _creer_interface(self):
        """Crée l'interface utilisateur de la page"""
        # Disposition principale
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Titre de la page
        titre = QLabel("Détails sur les fruits")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE, QFont.Bold))
        self.main_layout.addWidget(titre)
        
        # Zone de recherche
        recherche_layout = QHBoxLayout()
        
        recherche_label = QLabel("Rechercher un fruit:")
        recherche_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        recherche_layout.addWidget(recherche_label)
        
        self.recherche_input = QLineEdit()
        self.recherche_input.setPlaceholderText("Entrez le nom d'un fruit...")
        self.recherche_input.textChanged.connect(self._filtrer_fruits)
        recherche_layout.addWidget(self.recherche_input)
        
        # Bouton d'ajout
        self.ajouter_btn = BoutonAnime("Ajouter un fruit")
        self.ajouter_btn.setIcon(QIcon(os.path.join(DOSSIER_ASSETS, "icons", "entrainement.svg")))
        self.ajouter_btn.clicked.connect(self._ouvrir_dialog_ajout)
        recherche_layout.addWidget(self.ajouter_btn)
        
        self.main_layout.addLayout(recherche_layout)
        
        # Grille de cartes de fruits
        self._creer_grille_fruits()
    
    def _creer_grille_fruits(self):
        """Crée la grille affichant les cartes de fruits"""
        # Création du widget de la grille
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            
            QScrollBar:vertical {
                background-color: #141D2B;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #2B3648;
                min-height: 30px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #007ACC;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.grid_widget)
        self.main_layout.addWidget(self.scroll_area)
        
        # Remplissage de la grille
        self._remplir_grille()
    
    def _remplir_grille(self, filtre=""):
        """
        Remplit la grille avec les cartes de fruits
        
        Args:
            filtre (str, optionnel): Filtre de recherche
        """
        # Suppression des widgets existants
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Filtrage des fruits
        fruits_filtres = [
            f for f in self.fruits_info["fruits"]
            if filtre.lower() in f["nom"].lower()
        ]
        
        # Création des cartes
        col_max = 3  # Nombre maximum de colonnes
        for i, fruit in enumerate(fruits_filtres):
            row = i // col_max
            col = i % col_max
            
            carte = CarteFruit(
                nom=fruit["nom"],
                description=fruit["description"],
                famille=fruit["famille"],
                image_path=fruit.get("direction", None)
            )
            
            # Connexion du signal de clic
            carte.clique.connect(lambda nom=fruit["nom"]: self._afficher_details(nom))
            
            self.grid_layout.addWidget(carte, row, col)
        
        # Message si aucun fruit ne correspond
        if not fruits_filtres:
            aucun_resultat = QLabel("Aucun fruit ne correspond à votre recherche.")
            aucun_resultat.setAlignment(Qt.AlignCenter)
            aucun_resultat.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
            aucun_resultat.setStyleSheet(f"color: {COULEUR_TEXTE_SECONDAIRE};")
            self.grid_layout.addWidget(aucun_resultat, 0, 0, 1, col_max)
    
    def _filtrer_fruits(self):
        """Filtre les fruits selon le texte entré dans la recherche"""
        texte = self.recherche_input.text()
        self._remplir_grille(texte)
    
    def _afficher_details(self, nom_fruit):
        """
        Affiche les détails d'un fruit
        
        Args:
            nom_fruit (str): Nom du fruit à afficher
        """
        # Recherche du fruit dans la liste
        fruit = next((f for f in self.fruits_info["fruits"] if f["nom"] == nom_fruit), None)
        
        if not fruit:
            return
        
        # Création de la vue détaillée
        if self.vue_detaillee:
            self.vue_detaillee.setParent(None)
        
        self.vue_detaillee = DetailsFruit(fruit)
        self.vue_detaillee.fermeture.connect(self._fermer_details)
        
        # Remplacement de la grille par la vue détaillée
        self.scroll_area.setParent(None)
        self.main_layout.addWidget(self.vue_detaillee)
    
    def _fermer_details(self):
        """Ferme la vue détaillée et revient à la grille"""
        if self.vue_detaillee:
            self.vue_detaillee.setParent(None)
            self.vue_detaillee = None
        
        self.main_layout.addWidget(self.scroll_area)
        self._filtrer_fruits()  # Recharge la grille avec le filtre actuel

    def _ouvrir_dialog_ajout(self):
        """Ouvre le dialogue pour ajouter un nouveau fruit"""
        fruits_existants = self.gestionnaire.obtenir_liste_fruits()
        dialog = DialogAjoutFruit(fruits_existants, self)
        if dialog.exec() == QDialog.Accepted and dialog.fruit_cree:
            # Ajouter le fruit aux fruits_info
            self.fruits_info["fruits"].append(dialog.fruit_cree)
            
            # Sauvegarder les fruits_info dans le fichier JSON
            if self.gestionnaire.sauvegarder_fruits_info(self.fruits_info):
                QMessageBox.information(
                    self,
                    "Succès",
                    f"Le fruit '{dialog.fruit_cree['nom']}' a été ajouté avec succès ainsi que son dataset !"
                )
                # Convertir le chemin de l'image pour le nouveau fruit pour l'affichage immédiat
                chemin_fichier_actuel = pathlib.Path(__file__)
                base_path = chemin_fichier_actuel.parent.parent.parent.parent.absolute()
                chemin_relatif = dialog.fruit_cree["direction"]
                dialog.fruit_cree["direction"] = os.path.join(base_path, chemin_relatif)
                
                # Recharger l'affichage
                self._filtrer_fruits()
            else:
                QMessageBox.critical(
                    self,
                    "Erreur de sauvegarde",
                    "Impossible de sauvegarder les nouvelles informations sur les fruits dans le fichier JSON."
                )