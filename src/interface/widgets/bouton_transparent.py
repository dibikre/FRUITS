# -*- coding: utf-8 -*-
"""
Module contenant le widget de bouton transparent
"""

from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property, Qt, QSize
from PySide6.QtGui import QIcon, QColor

class BoutonTransparent(QPushButton):
    """
    Classe représentant un bouton transparent avec animations
    """
    
    def __init__(self, texte="", icone=None, parent=None):
        """
        Initialise un bouton transparent
        
        Args:
            texte (str): Texte à afficher sur le bouton
            icone (QIcon, optionnel): Icône à afficher sur le bouton
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(texte, parent)
        
        # Configuration de l'apparence
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        
        # Ajout de l'icône si fournie
        if icone:
            self.setIcon(icone)
            self.setIconSize(QSize(24, 24))
        
        # Propriétés pour les animations
        self._opacity = 0.7
        self._hover_opacity = 1.0
        
        # Effet d'opacité
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._opacity_effect.setOpacity(self._opacity)
        
        # Style transparent
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #E1E1E1;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                min-height: 30px;
                text-align: left;
            }
            
            QPushButton:hover {
                background-color: rgba(0, 122, 204, 0.2);
            }
            
            QPushButton:pressed {
                background-color: rgba(0, 122, 204, 0.3);
            }
        """)
        
        # Préparation des animations
        self._setup_animations()
    
    def _setup_animations(self):
        """Configure les animations du bouton"""
        # Animation d'opacité
        self._opacity_animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._opacity_animation.setDuration(200)
        self._opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        """Gère l'événement d'entrée de la souris"""
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self._opacity)
        self._opacity_animation.setEndValue(self._hover_opacity)
        self._opacity_animation.start()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Gère l'événement de sortie de la souris"""
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self._opacity_effect.opacity())
        self._opacity_animation.setEndValue(self._opacity)
        self._opacity_animation.start()
        
        super().leaveEvent(event)
    
    def setOpacity(self, opacity):
        """
        Définit l'opacité par défaut du bouton
        
        Args:
            opacity (float): Valeur d'opacité entre 0.0 et 1.0
        """
        self._opacity = opacity
        self._opacity_effect.setOpacity(opacity)
    
    def setHoverOpacity(self, opacity):
        """
        Définit l'opacité lors du survol du bouton
        
        Args:
            opacity (float): Valeur d'opacité entre 0.0 et 1.0
        """
        self._hover_opacity = opacity
