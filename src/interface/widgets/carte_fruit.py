# -*- coding: utf-8 -*-
"""
Module contenant le widget de carte de fruit
"""

import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property
from src.constantes import DOSSIER_DATASET, COULEUR_PRIMAIRE

class CarteFruit(QWidget):
    """
    Widget affichant les informations d'un fruit sous forme de carte
    """
    
    clique = Signal(str)  # Signal émis lorsque la carte est cliquée
    
    def __init__(self, nom="", description="", famille="", image_path=None, parent=None):
        """
        Initialise une carte de fruit
        
        Args:
            nom (str): Nom du fruit
            description (str): Description du fruit
            famille (str): Famille du fruit
            image_path (str, optionnel): Chemin vers l'image du fruit (provenant par ex. de votre JSON)
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Stockage des informations
        self._nom = nom
        self._description = description
        self._famille = famille
        self._image_path = image_path
        
        # Si aucune image_path explicite n'est fournie,
        # on cherche automatiquement dans dataset/{nom}/{nom}.{ext}
        if not self._image_path and self._nom:
            fruit_dir = os.path.join(DOSSIER_DATASET, self._nom)
            if os.path.isdir(fruit_dir):
                for ext in ("png", "jpg", "jpeg", "bmp", "gif"):
                    candidate = os.path.join(fruit_dir, f"{self._nom}.{ext}")
                    if os.path.exists(candidate):
                        self._image_path = candidate
                        break
        
        # Configuration de l'apparence
        self.setFixedWidth(300)
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        # Création de l'interface
        self._creer_interface()
        
        # Effet d'ombre
        self._ajouter_ombre()
        
        # Propriétés pour les animations
        self._y_offset = 0
        self._setup_animations()
        
        # Style général
        self.setStyleSheet("""
            QWidget#carte {
                background-color: #141D2B;
                border-radius: 8px;
                border: 1px solid #2B3648;
            }
            QLabel#nom {
                color: #E1E1E1;
                font-size: 16px;
                font-weight: bold;
            }
            QLabel#famille {
                color: #00BFFF;
                font-size: 12px;
                font-style: italic;
            }
            QLabel#description {
                color: #B0B0B0;
                font-size: 12px;
            }
            QPushButton#plus {
                background-color: transparent;
                color: #00BFFF;
                border: none;
                font-size: 12px;
            }
            QPushButton#plus:hover {
                color: #E1E1E1;
                text-decoration: underline;
            }
        """)
    
    def _creer_interface(self):
        """Crée les éléments de l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Conteneur principal
        self.carte_widget = QWidget()
        self.carte_widget.setObjectName("carte")
        carte_layout = QVBoxLayout(self.carte_widget)
        carte_layout.setContentsMargins(15, 15, 15, 15)
        carte_layout.setSpacing(10)
        
        # En-tête : image + textes
        header_layout = QHBoxLayout()
        
        # Chargement de l'image si disponible
        if self._image_path:
            try:
                image_path = self._image_path.replace("\\", "/")
                pixmap = QPixmap(image_path)
                if pixmap.isNull():
                    raise ValueError("Image invalide")
                self.image_label = QLabel()
                self.image_label.setFixedSize(60, 60)
                pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(pixmap)
                self.image_label.setStyleSheet("""
                    border-radius: 30px;
                    background-color: transparent;
                """)
            except Exception:
                self.image_label = QLabel()
                self.image_label.setFixedSize(60, 60)
                self.image_label.setStyleSheet(f"""
                    background-color: {COULEUR_PRIMAIRE};
                    border-radius: 30px;
                """)
        else:
            self.image_label = QLabel()
            self.image_label.setFixedSize(60, 60)
            self.image_label.setStyleSheet(f"""
                background-color: {COULEUR_PRIMAIRE};
                border-radius: 30px;
            """)
        
        header_layout.addWidget(self.image_label)
        
        # Textes : nom + famille
        text_layout = QVBoxLayout()
        self.nom_label = QLabel(self._nom)
        self.nom_label.setObjectName("nom")
        text_layout.addWidget(self.nom_label)
        self.famille_label = QLabel(f"Famille: {self._famille}")
        self.famille_label.setObjectName("famille")
        text_layout.addWidget(self.famille_label)
        text_layout.addStretch()
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        
        carte_layout.addLayout(header_layout)
        
        # Description (tronquée si nécessaire)
        desc = self._description
        if len(desc) > 120:
            desc = desc[:117] + "..."
        self.description_label = QLabel(desc)
        self.description_label.setObjectName("description")
        self.description_label.setWordWrap(True)
        carte_layout.addWidget(self.description_label)
        
        # Bouton "En savoir plus"
        bouton_layout = QHBoxLayout()
        bouton_layout.addStretch()
        self.plus_bouton = QPushButton("En savoir plus")
        self.plus_bouton.setObjectName("plus")
        self.plus_bouton.setCursor(Qt.PointingHandCursor)
        self.plus_bouton.clicked.connect(lambda: self.clique.emit(self._nom))
        bouton_layout.addWidget(self.plus_bouton)
        carte_layout.addLayout(bouton_layout)
        
        layout.addWidget(self.carte_widget)
    
    def _ajouter_ombre(self):
        """Ajoute un effet d'ombre à la carte"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.carte_widget.setGraphicsEffect(shadow)
    
    def _setup_animations(self):
        """Configure les animations de la carte"""
        self._y_animation = QPropertyAnimation(self, b"y_offset")
        self._y_animation.setDuration(150)
        self._y_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def _get_y_offset(self):
        return self._y_offset
    
    def _set_y_offset(self, offset):
        self._y_offset = offset
        shadow = self.carte_widget.graphicsEffect()
        shadow.setOffset(0, 4 - offset/2)
        shadow.setBlurRadius(15 + offset/2)
        self.carte_widget.setStyleSheet(f"""
            QWidget#carte {{
                background-color: #141D2B;
                border-radius: 8px;
                border: 1px solid #2B3648;
                margin-top: {-offset}px;
            }}
        """)
        self.update()
    
    y_offset = Property(float, _get_y_offset, _set_y_offset)
    
    def enterEvent(self, event):
        """Gère l'événement d'entrée de la souris"""
        self._y_animation.stop()
        self._y_animation.setStartValue(self._y_offset)
        self._y_animation.setEndValue(5)
        self._y_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Gère l'événement de sortie de la souris"""
        self._y_animation.stop()
        self._y_animation.setStartValue(self._y_offset)
        self._y_animation.setEndValue(0)
        self._y_animation.start()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Gère l'événement de clic de la souris"""
        self.clique.emit(self._nom)
        super().mousePressEvent(event)
