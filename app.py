#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Point d'entrée principal de l'application de reconnaissance de fruits
avec écran de chargement avant la fenêtre principale.
"""
import sys
import os
import importlib.util
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

# Répertoires de base
direction_de_base = os.path.dirname(os.path.abspath(__file__))
ANIME_DIR = os.path.join(direction_de_base, "ANIME")

# Charger dynamiquement demarrage.py depuis le répertoire ANIME

chemin_demarrage = os.path.join(ANIME_DIR, "demarrage.py")
if not os.path.exists(chemin_demarrage):
    raise FileNotFoundError(f"Le fichier de démarrage n'a pas été trouvé : {chemin_demarrage}")

spec = importlib.util.spec_from_file_location("demarrage", chemin_demarrage)
module_demarrage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_demarrage)
FenetreChargement = module_demarrage.FenetreChargement

# Import de la fenêtre principale et des thèmes
sys.path.append(direction_de_base)
from src.interface import FenetrePrincipale
from src.interface.themes import appliquer_theme_bleu_noir
from src.constantes import DOSSIER_ICONS


def main():
    """Fonction principale de l'application"""
    # Création de l'application
    app = QApplication(sys.argv)
    app.setApplicationName("Reconnaissance de Fruits")

    # Afficher l'écran de démarrage
    splash = FenetreChargement()
    # Empêcher le splash de fermer toute l'appli
    try:
        splash.minuteur.stop()
    except Exception:
        pass
    splash.show()

    # Fonction interne pour lancer la fenêtre principale
    def lancer_interface_principale():
        # Fermer le splash
        splash.close()

        # Définir l'icône de l'application
        chemin_icon = os.path.join(direction_de_base, DOSSIER_ICONS, "reconnaissance.svg")
        if os.path.exists(chemin_icon):
            app.setWindowIcon(QIcon(chemin_icon))

        # Appliquer le thème
        appliquer_theme_bleu_noir(app)

        # Créer et afficher la fenêtre principale
        main_window = FenetrePrincipale()
        # Conserver une référence pour éviter le garbage collection
        app.main_window = main_window
        main_window.show()

    # Lancer la fenêtre principale après 6 secondes
    QTimer.singleShot(6000, lancer_interface_principale)

    # Boucle événementielle
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
