# -*- coding: utf-8 -*-
"""
Module contenant la fenêtre principale de l'application
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve

import os
import json

from .menu_lateral import MenuLateral
from .pages import (PageCapture, PageEntrainement, PageReconnaissance,
                   PageDetails, PageAide, PageAuteurs)
from ..constantes import *

class FenetrePrincipale(QMainWindow):
    """
    Fenêtre principale de l'application
    """
    
    def __init__(self):
        """Initialise la fenêtre principale"""
        super().__init__()
        
        # Chargement de la configuration
        self._charger_config()
        
        # Configuration de la fenêtre
        self._configurer_fenetre()
        
        # Création de l'interface
        self._creer_interface()
        
        # Initialisation de la première page
        self._changer_page(0)
    
    def _charger_config(self):
        """Charge la configuration de l'application"""
        try:
            with open(FICHIER_CONFIG, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            self.config = {
                "application": {
                    "nom": "Reconnaissance de Fruits",
                    "langue": "fr_FR",
                    "theme": "bleu_noir"
                },
                "interface": {
                    "largeur": 1280,
                    "hauteur": 800
                }
            }
    
    def _configurer_fenetre(self):
        """Configure les paramètres de la fenêtre"""
        # Titre et icône
        self.setWindowTitle(self.config["application"]["nom"])
        
        # Dimensions
        largeur = self.config["interface"].get("largeur", 1280)
        hauteur = self.config["interface"].get("hauteur", 800)
        self.resize(largeur, hauteur)
        
        # Style de la fenêtre
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0D1117;
            }
        """)
    
    def _creer_interface(self):
        """Crée l'interface utilisateur"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Disposition principale
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Menu latéral
        self.menu = MenuLateral()
        self.menu.page_changee.connect(self._changer_page)
        main_layout.addWidget(self.menu)
        
        # Conteneur de pages
        self.pages_container = QStackedWidget()
        # Préparation du chemin de l'image pour qu'il soit compatible avec le CSS
        background_path = os.path.join(DOSSIER_BACKGROUNDS, "main_bg.svg").replace("\\", "/")
        
        self.pages_container.setStyleSheet(f"""
            QStackedWidget {{
                background-color: #0D1117;
                background-image: url("{background_path}");
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
        """)
        main_layout.addWidget(self.pages_container)
        
        # Création des pages
        self._creer_pages()
    
    def _creer_pages(self):
        """Crée les différentes pages de l'application"""
        # Création des instances de pages
        self.page_capture = PageCapture()
        self.page_entrainement = PageEntrainement()
        self.page_reconnaissance = PageReconnaissance()
        self.page_details = PageDetails()
        self.page_aide = PageAide()
        self.page_auteurs = PageAuteurs()
        
        # Ajout des pages au conteneur
        self.pages_container.addWidget(self.page_capture)
        self.pages_container.addWidget(self.page_entrainement)
        self.pages_container.addWidget(self.page_reconnaissance)
        self.pages_container.addWidget(self.page_details)
        self.pages_container.addWidget(self.page_aide)
        self.pages_container.addWidget(self.page_auteurs)
    
    def _changer_page(self, index):
        """
        Change la page affichée
        
        Args:
            index (int): Index de la page à afficher
        """
        # Vérification de la validité de l'index
        if 0 <= index < self.pages_container.count():
            # Animation de transition
            self._animer_transition_page(index)
    
    def _animer_transition_page(self, index):
        """
        Anime la transition vers une nouvelle page
        
        Args:
            index (int): Index de la page à afficher
        """
        # Position actuelle du widget
        widget = self.pages_container.widget(index)
        current_index = self.pages_container.currentIndex()
        
        # Si c'est la même page, pas d'animation
        if index == current_index:
            return
        
        # Changement de page
        self.pages_container.setCurrentIndex(index)
        
        # Animation d'opacité pour une transition en fondu
        # Note: nous n'utilisons pas directement cette technique car
        # elle nécessiterait de configurer des GraphicsEffects pour chaque page
        # et de les animer, ce qui serait plus complexe dans ce contexte.
        # À la place, nous utilisons simplement le changement direct avec setCurrentIndex.
    
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre"""
        # Confirmation de fermeture
        reponse = QMessageBox.question(
            self,
            "Confirmation de fermeture",
            "Êtes-vous sûr de vouloir quitter l'application ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reponse == QMessageBox.Yes:
            # Fermeture des ressources
            if hasattr(self, 'page_reconnaissance'):
                self.page_reconnaissance.camera_widget.arreter()
                self.page_reconnaissance.synthese.arreter()
            
            if hasattr(self, 'page_capture'):
                self.page_capture.camera_widget.arreter()
            
            event.accept()
        else:
            event.ignore()
