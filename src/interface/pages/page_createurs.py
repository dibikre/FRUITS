# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
                              QGridLayout, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

import os

from ...constantes import *

class CarteAuteur(QWidget):
    """
    Widget représentant la carte d'un auteur
    """
    
    def __init__(self, nom, role, email=None, description=None, photo_path=None, parent=None):
        """
        Initialise une carte d'auteur
        
        Args:
            nom (str): Nom de l'auteur
            role (str): Rôle ou titre de l'auteur
            email (str, optionnel): Adresse email de l'auteur
            description (str, optionnel): Description ou biographie
            photo_path (str, optionnel): Chemin vers la photo de l'auteur
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        self.setMinimumWidth(300)
        self.setFixedHeight(180)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #141D2B;
                border-radius: 10px;
                border: 1px solid #2B3648;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        # Avatar et nom
        header_layout = QHBoxLayout()
        
        # Avatar (photo ou initiales si pas de photo)
        avatar_label = QLabel()
        avatar_label.setFixedSize(70, 70)
        avatar_label.setAlignment(Qt.AlignCenter)
        
        if photo_path and os.path.exists(photo_path):
            # Chargement de la photo
            pixmap = QPixmap(photo_path)
            # Redimensionnement pour qu'elle tienne dans le label
            pixmap = pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Création d'un masque circulaire
            rounded_pixmap = QPixmap(pixmap.size())
            rounded_pixmap.fill(Qt.transparent)
            
            # Application du style pour le label avec la photo
            avatar_label.setStyleSheet("""
                border-radius: 25px;
                background-color: transparent;
                border: 2px solid #2B3648;
                overflow: hidden;
            """)
            
            avatar_label.setPixmap(pixmap)
            avatar_label.setScaledContents(True)
        else:
            # Fallback avec les initiales si la photo n'existe pas
            initiales = "".join([n[0].upper() for n in nom.split() if n])
            avatar_label.setStyleSheet(f"""
                background-color: {COULEUR_PRIMAIRE};
                color: white;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            """)
            avatar_label.setText(initiales)
        
        header_layout.addWidget(avatar_label)
        
        # Nom et rôle
        info_layout = QVBoxLayout()
        
        nom_label = QLabel(nom)
        font_nom = QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL)
        font_nom.setBold(True)
        nom_label.setFont(font_nom)
        info_layout.addWidget(nom_label)
        
        role_label = QLabel(role)
        font_role = QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_PETIT)
        font_role.setItalic(True)
        role_label.setFont(font_role)
        role_label.setStyleSheet(f"color: {COULEUR_ACCENT};")
        info_layout.addWidget(role_label)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Séparateur
        separateur = QWidget()
        separateur.setFixedHeight(1)
        separateur.setStyleSheet("background-color: #2B3648; margin: 5px 0;")
        layout.addWidget(separateur)
        
        # Description
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_PETIT))
            layout.addWidget(desc_label)
        
        # Email
        if email:
            email_label = QLabel(f"Email: {email}")
            email_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_PETIT))
            email_label.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
            layout.addWidget(email_label)
        
        layout.addStretch()

class PageAuteurs(QWidget):
    """
    Page d'information sur les auteurs de l'application
    """
    
    def __init__(self, parent=None):
        """
        Initialise la page d'auteurs
        
        Args:
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Création de l'interface
        self._creer_interface()
    
    def _creer_interface(self):
        """Crée l'interface utilisateur de la page"""
        # Disposition principale
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre de la page
        titre = QLabel("À propos des auteurs")
        titre.setAlignment(Qt.AlignCenter)
        font_titre = QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE)
        font_titre.setBold(True)
        titre.setFont(font_titre)
        layout.addWidget(titre)
        
        # Description du projet
        description = QLabel(
            "Cette application de reconnaissance de fruits a été développée par une équipe "
            "passionnée d'intelligence artificielle et de traitement d'images. "
            "Notre objectif est de démontrer comment la vision par ordinateur peut être "
            "utilisée pour identifier des objets du quotidien comme les fruits."
        )
        description.setWordWrap(True)
        description.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet(f"color: {COULEUR_TEXTE};")
        layout.addWidget(description)
        
        # Grille d'auteurs
        auteurs_grid = QGridLayout()
        auteurs_grid.setSpacing(20)
        
        # Chemins vers les photos des auteurs
        base_path = os.path.dirname(os.path.abspath(__file__))
        photos_dir = os.path.join(base_path, "PHOTOS")
        
        # Données des auteurs
        auteurs = [
            {
                "nom": "DIBI Kre Michael",
                "role": "Concepteur principal",
                "email": "dibikremichael@gmail.com",
                "description": "Ayant quelques idées de spécialité en vision par ordinateur et apprentissage automatique, Dibi a conçu l'architecture du modèle de reconnaissance et amélioré l'application dans son automatisation d'interaction par rapport au design.",
                "photo": os.path.join(photos_dir, "dibi kre michael.jpg")
            }
        ]
        
        # Création des cartes d'auteurs
        for i, auteur in enumerate(auteurs):
            carte = CarteAuteur(
                nom=auteur["nom"],
                role=auteur["role"],
                email=auteur["email"],
                description=auteur["description"],
                photo_path=auteur["photo"]
            )
            
            row = i // 2
            col = i % 2
            
            auteurs_grid.addWidget(carte, row, col)
        
        layout.addLayout(auteurs_grid)
        
        # Remerciements
        remerciements_titre = QLabel("Remerciements")
        font_remerciements = QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE)
        font_remerciements.setBold(True)
        remerciements_titre.setFont(font_remerciements)
        remerciements_titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(remerciements_titre)
        
        remerciements = QLabel(
            "Nous tenons à remercier tous ceux qui ont contribué à ce projet, "
            "Notamment notre professeur Mr MBIDA pour son coup de pouce assurant le démarrage par idées, et aussi les testeurs qui ont fourni de précieux retours pour améliorer l'application. "
            "Merci également aux bibliothèques open-source TensorFlow, OpenCV et PySide6 "
            "qui ont rendu ce projet possible."
        )
        remerciements.setWordWrap(True)
        remerciements.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        remerciements.setAlignment(Qt.AlignCenter)
        remerciements.setContentsMargins(10, 30, 10, 0)
        layout.addWidget(remerciements)
        
        layout.addStretch()
        
        # Copyright
        copyright_label = QLabel("Exclusivement réservée à l'éducation")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_PETIT))
        copyright_label.setStyleSheet(f"color: {COULEUR_TEXTE_SECONDAIRE};")
        layout.addWidget(copyright_label)