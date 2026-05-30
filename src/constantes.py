# -*- coding: utf-8 -*-
"""
Fichier contenant les constantes globales utilisées dans l'application
"""

import os

# Chemins des dossiers
DOSSIER_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRECTION_JSON_FRUITS = os.path.join(DOSSIER_RACINE, "donnees")
DOSSIER_DATASET = os.path.join(DOSSIER_RACINE, "dataset")
DOSSIER_ASSETS = os.path.join(DOSSIER_RACINE, "assets")

# Chemins des fichiers
FICHIER_CONFIG = os.path.join(DIRECTION_JSON_FRUITS, "config.json")
FICHIER_FRUITS_INFO = os.path.join(DIRECTION_JSON_FRUITS, "fruits_info.json")
FICHIER_MODELE = os.path.join(DIRECTION_JSON_FRUITS, "modele_fruits.h5")
FICHIER_ETIQUETTES = os.path.join(DIRECTION_JSON_FRUITS, "etiquettes.pkl")

# Chemins des assets
DOSSIER_ICONS = os.path.join(DOSSIER_ASSETS, "icons")
DOSSIER_BACKGROUNDS = os.path.join(DOSSIER_ASSETS, "backgrounds")

# Paramètres de l'interface
COULEUR_PRIMAIRE = "#007ACC"  # Bleu vif
COULEUR_SECONDAIRE = "#00BFFF"  # Bleu ciel
COULEUR_FOND = "#0D1117"  # Fond sombre bleu-noir
COULEUR_FOND_MENU = "#001220"  # Bleu plus foncé pour le menu
COULEUR_TEXTE = "#E1E1E1"  # Blanc cassé
COULEUR_TEXTE_SECONDAIRE = "#7A7A7A"  # Gris
COULEUR_ACCENT = "#1F97EF"  # Accent bleu clair
COULEUR_ERREUR = "#E91E63"  # Rose/rouge pour les erreurs
COULEUR_SUCCES = "#4CAF50"  # Vert pour les succès

# Paramètres de la police
POLICE_PRINCIPALE = "Roboto"
POLICE_SECONDAIRE = "Montserrat"
TAILLE_TEXTE_NORMAL = 12
TAILLE_TEXTE_TITRE = 16
TAILLE_TEXTE_SOUS_TITRE = 14
TAILLE_TEXTE_PETIT = 10

# Paramètres des animations
DUREE_ANIMATION = 200  # ms
FACTEUR_ANIMATION = 1.1  # Facteur d'agrandissement
OPACITE_SURVOL = 0.8

# Paramètres du modèle
TAILLE_IMAGE = (64, 64)
BATCH_SIZE = 32
EPOCHS = 20

# Messages
MSG_AUCUNE_CAMERA = "Aucune caméra détectée. Veuillez connecter une caméra."
MSG_ERREUR_CHARGEMENT_MODELE = "Erreur lors du chargement du modèle. Veuillez entraîner un modèle."
MSG_ENTRAINEMENT_SUCCESS = "Entraînement terminé avec succès !"
MSG_ENTRAINEMENT_ERROR = "Erreur lors de l'entraînement du modèle."
MSG_CAPTURE_SUCCESS = "Capture réussie !"
MSG_CAPTURE_ERROR = "Erreur lors de la capture d'image."
