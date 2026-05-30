# -*- coding: utf-8 -*-
"""
Module contenant le widget de bouton animé
"""

from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property, QSize, Qt
from PySide6.QtGui import QIcon, QColor, QPainter

class BoutonAnime(QPushButton):
    """
    Classe représentant un bouton avec des animations lors du survol et du clic
    """
    
    def __init__(self, texte="", icone=None, parent=None):
        """
        Initialise un bouton animé
        
        Args:
            texte (str): Texte à afficher sur le bouton
            icone (QIcon, optionnel): Icône à afficher sur le bouton
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(texte, parent)
        
        # Propriétés pour les animations (doivent être définies avant le style)
        self._scale = 1.0
        self._opacity = 1.0
        self._hover_color = QColor("#007ACC")
        self._default_color = QColor("#1A2332")
        self._current_color = self._default_color
        
        # Configuration de l'apparence
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        # Feuille de style de base (sans transform)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._default_color.name()};
                color: #FFFFFF;
                border: 1px solid #007ACC;
                border-radius: 4px;
                padding: 6px 12px;
                min-height: 30px;
            }}
        """
        )
        
        # Ajout de l'icône si fournie
        if icone:
            self.setIcon(icone)
            self.setIconSize(QSize(24, 24))
        
        # Effet d'opacité
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._opacity_effect.setOpacity(self._opacity)
        
        # Préparation des animations
        self._setup_animations()
    
    def _setup_animations(self):
        """Configure les animations du bouton"""
        # Animation d'échelle
        self._scale_animation = QPropertyAnimation(self, b"scale")
        self._scale_animation.setDuration(200)
        self._scale_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animation d'opacité
        self._opacity_animation = QPropertyAnimation(self, b"opacity")
        self._opacity_animation.setDuration(200)
        self._opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animation de couleur
        self._color_animation = QPropertyAnimation(self, b"color")
        self._color_animation.setDuration(200)
        self._color_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        """Gère l'événement d'entrée de la souris"""
        # Scale
        self._scale_animation.stop()
        self._scale_animation.setStartValue(self._scale)
        self._scale_animation.setEndValue(1.05)
        self._scale_animation.start()
        # Opacity
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self._opacity)
        self._opacity_animation.setEndValue(0.9)
        self._opacity_animation.start()
        # Color
        self._color_animation.stop()
        self._color_animation.setStartValue(self._current_color)
        self._color_animation.setEndValue(self._hover_color)
        self._color_animation.start()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Gère l'événement de sortie de la souris"""
        # Scale
        self._scale_animation.stop()
        self._scale_animation.setStartValue(self._scale)
        self._scale_animation.setEndValue(1.0)
        self._scale_animation.start()
        # Opacity
        self._opacity_animation.stop()
        self._opacity_animation.setStartValue(self._opacity)
        self._opacity_animation.setEndValue(1.0)
        self._opacity_animation.start()
        # Color
        self._color_animation.stop()
        self._color_animation.setStartValue(self._current_color)
        self._color_animation.setEndValue(self._default_color)
        self._color_animation.start()
        
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Gère l'événement de clic de souris"""
        self._scale_animation.stop()
        self._scale_animation.setStartValue(self._scale)
        self._scale_animation.setEndValue(0.95)
        self._scale_animation.start()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Gère l'événement de relâchement du clic"""
        self._scale_animation.stop()
        self._scale_animation.setStartValue(self._scale)
        self._scale_animation.setEndValue(1.05)
        self._scale_animation.start()
        
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """Personnalise le rendu du bouton"""
        # Applique la mise à l'échelle via QPainter
        painter = QPainter(self)
        w, h = self.width(), self.height()
        painter.translate(w/2, h/2)
        painter.scale(self._scale, self._scale)
        painter.translate(-w/2, -h/2)
        # Dessine le widget normalement
        super().paintEvent(event)
    
    # Propriétés pour les animations
    def _get_scale(self):
        return self._scale
    
    def _set_scale(self, scale):
        self._scale = scale
        self.update()
    
    def _get_opacity(self):
        return self._opacity
    
    def _set_opacity(self, opacity):
        self._opacity = opacity
        self._opacity_effect.setOpacity(opacity)
    
    def _get_color(self):
        return self._current_color
    
    def _set_color(self, color):
        self._current_color = color
        # Mise à jour de la couleur de fond
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                color: #FFFFFF;
                border: 1px solid #007ACC;
                border-radius: 4px;
                padding: 6px 12px;
                min-height: 30px;
            }}
        """
        )
        self.update()
    
    scale = Property(float, _get_scale, _set_scale)
    opacity = Property(float, _get_opacity, _set_opacity)
    color = Property(QColor, _get_color, _set_color)
