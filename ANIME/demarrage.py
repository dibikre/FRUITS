#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QMovie

class FenetreChargement(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Chargement")
        self.setFixedSize(600, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # Widget central et mise en page en grille pour superposer GIF et texte
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout = QGridLayout(widget_central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Label du GIF
        self.label_gif = QLabel()
        chemin_script = os.path.dirname(os.path.abspath(__file__))
        chemin_gif = os.path.join(chemin_script, "gif", "demarrage.gif")
        self.animation = QMovie(chemin_gif)
        # Accélérer l'animation du GIF de 1.2x (120%)
        self.animation.setSpeed(150)
        self.label_gif.setMovie(self.animation)
        self.label_gif.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_gif, 0, 0)
        self.animation.start()

        # Label du texte "Chargement" superposé, légèrement vers le haut de l'image
        self.texte_chargement = QLabel("Chargement")
        self.texte_chargement.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        police = QFont()
        police.setPointSize(19)
        police.setBold(True)
        self.texte_chargement.setFont(police)
        # Décalage vertical pour placer le texte légèrement vers le top de l'image
        self.texte_chargement.setContentsMargins(0, 60, 0, 0)
        # Transparence pour laisser voir le GIF en dessous
        self.texte_chargement.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.texte_chargement, 0, 0)

        # Timer pour animer les points
        self.dot_count = 0
        self.timer_dots = QTimer(self)
        self.timer_dots.timeout.connect(self.update_dots)
        self.timer_dots.start(500)  # toutes les 500 ms

        # Timer pour fermer l'application après 6 secondes
        self.minuteur = QTimer(self)
        self.minuteur.timeout.connect(self.fermer_application)
        self.minuteur.start(6000)  # 6000 ms = 6 secondes

    def update_dots(self):
        """Met à jour le nombre de points après le texte"""
        self.dot_count = (self.dot_count + 1) % 4
        dots = '.' * self.dot_count
        self.texte_chargement.setText(f"Chargement{dots}")

    def fermer_application(self):
        """Ferme l'application après le délai défini"""
        QApplication.quit()


def demarrer_application():
    """Fonction principale pour lancer l'application"""
    app = QApplication(sys.argv)
    fenetre = FenetreChargement()
    fenetre.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    demarrer_application()
