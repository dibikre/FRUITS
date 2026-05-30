# -*- coding: utf-8 -*-
"""
Module contenant le menu latéral de l'application
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea,
                             QSizePolicy, QSpacerItem)
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtCore import Qt, QSize, Signal, QPropertyAnimation, QRect

import os

from .widgets.bouton_transparent import BoutonTransparent
from ..constantes import *

class MenuLateral(QWidget):
    """
    Widget représentant le menu latéral de l'application
    """
    
    page_changee = Signal(int)  # Signal émis lorsque la page change
    
    def __init__(self, parent=None):
        """
        Initialise le menu latéral
        
        Args:
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Configuration du widget
        self.setObjectName("menu_lateral")
        self.setFixedWidth(250)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        # Définition du style
        # Préparation du chemin de l'image pour qu'il soit compatible avec le CSS
        menu_bg_path = os.path.join(DOSSIER_BACKGROUNDS, "menu_bg.svg").replace("\\", "/")
        
        self.setStyleSheet(f"""
            QWidget#menu_lateral {{
                background-color: {COULEUR_FOND_MENU};
                background-image: url("{menu_bg_path}");
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                border-right: 1px solid #2B3648;
            }}
            
            QLabel#logo {{
                color: {COULEUR_TEXTE};
                font-family: {POLICE_PRINCIPALE};
                font-size: 20px;
                font-weight: bold;
            }}
            
            QLabel#version {{
                color: {COULEUR_TEXTE_SECONDAIRE};
                font-family: {POLICE_SECONDAIRE};
                font-size: 12px;
            }}
        """)
        
        # Création de l'interface
        self._creer_interface()
    
    def _creer_interface(self):
        """Crée l'interface du menu latéral"""
        # Disposition principale
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        
        # Entête du menu
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        # Logo et titre
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(0)
        
        logo_label = QLabel("Reconnaissance\nde Fruits")
        logo_label.setObjectName("logo")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        version_label = QLabel("Version 1.0")
        version_label.setObjectName("version")
        version_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(version_label)
        
        header_layout.addLayout(logo_layout)
        header_layout.addSpacing(20)
        
        layout.addLayout(header_layout)
        
        # Séparateur
        separateur = QWidget()
        separateur.setFixedHeight(1)
        separateur.setStyleSheet("background-color: #2B3648;")
        layout.addWidget(separateur)
        layout.addSpacing(10)
        
        # Items du menu
        self._creer_items_menu(layout)
        
        # Espacement en bas
        layout.addStretch()
        
        # Copyright
        copyright_label = QLabel("© 2023 - Tous droits réservés")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet(f"color: {COULEUR_TEXTE_SECONDAIRE}; font-size: 10px;")
        layout.addWidget(copyright_label)
    
    def _creer_items_menu(self, layout):
        """
        Crée les items du menu
        
        Args:
            layout (QVBoxLayout): Layout dans lequel ajouter les items
        """
        # Configuration des items
        items = [
            {
                "texte": "Capture d'images",
                "icone": "camera.svg",
                "index": 0
            },
            {
                "texte": "Entraînement de modèle",
                "icone": "entrainement.svg",
                "index": 1
            },
            {
                "texte": "Reconnaissance de fruits",
                "icone": "reconnaissance.svg",
                "index": 2
            },
            {
                "texte": "Détails sur les fruits",
                "icone": "details.svg",
                "index": 3
            },
            {
                "texte": "Aide",
                "icone": "aide.svg",
                "index": 4
            },
            {
                "texte": "Auteurs",
                "icone": "auteurs.svg",
                "index": 5
            }
        ]
        
        # Création des boutons
        self.boutons = []
        for item in items:
            bouton = BoutonTransparent(item["texte"])
            
            # Ajout de l'icône
            icone_path = os.path.join(DOSSIER_ICONS, item["icone"]).replace("\\", "/")
            if os.path.exists(icone_path):
                bouton.setIcon(QIcon(icone_path))
                bouton.setIconSize(QSize(24, 24))
            
            # Style et comportement
            bouton.setMinimumHeight(50)
            index = item["index"]
            bouton.clicked.connect(lambda checked=False, idx=index: self._changer_page(idx))
            
            # Ajout au layout
            layout.addWidget(bouton)
            self.boutons.append(bouton)
            
        # Marquer le premier bouton comme actif
        if self.boutons:
            self._mettre_en_surbrillance(0)
    
    def _changer_page(self, index):
        """
        Change la page active et met à jour le menu
        
        Args:
            index (int): Index de la page à afficher
        """
        # Mise en surbrillance du bouton
        self._mettre_en_surbrillance(index)
        
        # Émission du signal
        self.page_changee.emit(index)
    
    def _mettre_en_surbrillance(self, index):
        """
        Met en surbrillance le bouton correspondant à la page active
        
        Args:
            index (int): Index du bouton à mettre en surbrillance
        """
        # Réinitialisation de tous les boutons
        for i, bouton in enumerate(self.boutons):
            if i == index:
                # Bouton actif
                bouton.setStyleSheet(f"""
                    QPushButton {{
                        background-color: rgba(0, 122, 204, 0.3);
                        color: #FFFFFF;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 12px;
                        text-align: left;
                    }}
                """)
            else:
                # Boutons inactifs
                bouton.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #E1E1E1;
                        border: none;
                        border-radius: 4px;
                        padding: 6px 12px;
                        text-align: left;
                    }
                    
                    QPushButton:hover {
                        background-color: rgba(0, 122, 204, 0.2);
                    }
                """)
