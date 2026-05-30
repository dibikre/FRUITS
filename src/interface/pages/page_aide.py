# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
                              QTabWidget, QPushButton)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

import os

from ..widgets.bouton_anime import BoutonAnime
from ...constantes import *

class PageAide(QWidget):
    """
    Page d'aide de l'application
    """
    
    def __init__(self, parent=None):
        """
        Initialise la page d'aide
        
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
        titre = QLabel("Aide et documentation")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Tabs d'aide
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #2B3648;
                background-color: #141D2B;
                border-radius: 8px;
            }
            
            QTabBar::tab {
                background-color: #727070 ;
                color: #E1E1E1;
                border: 1px solid #2B3648;
                padding: 10px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 120px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #000000;
                color: white;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #2B3648;
            }
        """)
        
        # Onglets d'aide
        self._creer_onglet_introduction()
        self._creer_onglet_capture()
        self._creer_onglet_entrainement()
        self._creer_onglet_reconnaissance()
        self._creer_onglet_faq()
        
        layout.addWidget(self.tabs)
    
    def _creer_onglet_introduction(self):
        """Crée l'onglet d'introduction"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Titre
        titre = QLabel("Bienvenue dans l'application de reconnaissance de fruits")
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Description
        description = QLabel(
            "Cette application vous permet de reconnaître des fruits grâce à l'intelligence artificielle. "
            "Vous pouvez capturer des images de fruits, entraîner un modèle de reconnaissance, "
            "et utiliser ce modèle pour identifier des fruits en temps réel."
        )
        description.setWordWrap(True)
        description.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(description)
        
        # Fonctionnalités principales
        fonctionnalites = QLabel("Fonctionnalités principales:")
        fonctionnalites.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(fonctionnalites)
        
        liste_fonctionnalites = QLabel(
            "• Capture d'images: Utilisez votre webcam pour capturer des images de fruits\n"
            "• Entraînement de modèle: Créez un modèle de reconnaissance personnalisé\n"
            "• Reconnaissance de fruits: Identifiez des fruits en temps réel\n"
            "• Détails sur les fruits: Consultez des informations détaillées sur les fruits\n"
        )
        liste_fonctionnalites.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        liste_fonctionnalites.setStyleSheet(f"color: {COULEUR_TEXTE};")
        layout.addWidget(liste_fonctionnalites)
        
        # Premiers pas
        premiers_pas = QLabel("Pour commencer:")
        premiers_pas.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(premiers_pas)
        
        etapes = QLabel(
            "1. Capturez des images de différents fruits\n"
            "2. Entraînez votre modèle de reconnaissance\n"
            "3. Utilisez la reconnaissance en temps réel pour identifier vos fruits\n"
        )
        etapes.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(etapes)
        
        layout.addStretch()
        self.tabs.addTab(page, "Introduction")
    
    def _creer_onglet_capture(self):
        """Crée l'onglet d'aide pour la capture d'images"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Titre
        titre = QLabel("Capture d'images")
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Description
        description = QLabel(
            "La page de capture d'images vous permet de collecter des données d'entraînement pour "
            "votre modèle de reconnaissance. Plus vous capturez d'images variées pour chaque fruit, "
            "plus votre modèle sera précis."
        )
        description.setWordWrap(True)
        description.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(description)
        
        # Comment utiliser
        utilisation = QLabel("Comment utiliser la capture d'images:")
        utilisation.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(utilisation)
        
        etapes = QLabel(
            "1. Sélectionnez le fruit que vous souhaitez capturer dans la liste déroulante\n"
            "2. Définissez le nombre d'images à capturer (au moins 30 images recommandées par fruit)\n"
            "3. Cliquez sur 'Démarrer la session de capture'\n"
            "4. Placez le fruit dans le rectangle de capture et laissez l'application prendre des photos\n"
            "5. Variez les angles et les positions du fruit pour obtenir des données diversifiées\n"
            "6. Une fois terminé, passez au fruit suivant\n"
        )
        etapes.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(etapes)
        
        # Conseils
        conseils = QLabel("Conseils pour de meilleures captures:")
        conseils.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(conseils)
        
        liste_conseils = QLabel(
            "• Assurez-vous d'avoir un bon éclairage\n"
            "• Utilisez différents arrière-plans pour une meilleure généralisation\n"
            "• Essayez différentes distances de la caméra\n"
            "• Capturez le fruit sous différents angles\n"
            "• Si possible, utilisez différents exemplaires du même fruit\n"
        )
        liste_conseils.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(liste_conseils)
        
        layout.addStretch()
        self.tabs.addTab(page, "Capture d'images")
    
    def _creer_onglet_entrainement(self):
        """Crée l'onglet d'aide pour l'entraînement du modèle"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Titre
        titre = QLabel("Entraînement du modèle")
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Description
        description = QLabel(
            "Cette page vous permet d'entraîner un modèle de deep learning qui apprendra "
            "à reconnaître les différents fruits à partir des images que vous avez capturées. "
            "L'entraînement utilise un réseau de neurones convolutifs (CNN) optimisé pour la "
            "reconnaissance d'images."
        )
        description.setWordWrap(True)
        description.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(description)
        
        # Paramètres d'entraînement
        parametres = QLabel("Paramètres d'entraînement:")
        parametres.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(parametres)
        
        liste_parametres = QLabel(
            "• Taille de l'image: Dimension des images utilisées par le modèle\n"
            "• Taille du batch: Nombre d'images traitées simultanément\n"
            "• Nombre d'époques: Nombre de fois où le modèle parcourt l'ensemble des données\n"
            "• Split de validation: Pourcentage des données réservées à la validation\n"
            "• Augmentation de données: Techniques pour augmenter artificiellement la diversité des données\n"
        )
        liste_parametres.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(liste_parametres)
        
        # Conseils
        conseils = QLabel("Conseils pour l'entraînement:")
        conseils.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(conseils)
        
        liste_conseils = QLabel(
            "• Capturez au moins 50 images par fruit pour de bons résultats\n"
            "• Utilisez l'augmentation de données pour améliorer la robustesse du modèle\n"
            "• Commencez avec 20 époques, puis augmentez si nécessaire\n"
            "• Une précision de validation supérieure à 85% est généralement acceptable\n"
            "• Si l'entraînement est trop lent, réduisez la taille des images\n"
        )
        liste_conseils.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(liste_conseils)
        
        layout.addStretch()
        self.tabs.addTab(page, "Entraînement")
    
    def _creer_onglet_reconnaissance(self):
        """Crée l'onglet d'aide pour la reconnaissance de fruits"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Titre
        titre = QLabel("Reconnaissance de fruits")
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Description
        description = QLabel(
            "La page de reconnaissance vous permet d'utiliser le modèle entraîné pour identifier "
            "des fruits en temps réel à l'aide de votre webcam. Le modèle analyse chaque image "
            "capturée et affiche le fruit détecté avec un niveau de confiance."
        )
        description.setWordWrap(True)
        description.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(description)
        
        # Comment utiliser
        utilisation = QLabel("Comment utiliser la reconnaissance:")
        utilisation.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(utilisation)
        
        etapes = QLabel(
            "1. Assurez-vous d'avoir entraîné un modèle au préalable\n"
            "2. Placez un fruit devant la caméra dans le rectangle de capture\n"
            "3. Le nom du fruit détecté s'affiche avec le niveau de confiance\n"
            "4. Ajustez le seuil de confiance si nécessaire\n"
            "5. Activez ou désactivez la synthèse vocale selon vos préférences\n"
        )
        etapes.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(etapes)
        
        # Seuil de confiance
        seuil = QLabel("Seuil de confiance:")
        seuil.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(seuil)
        
        explication_seuil = QLabel(
            "Le seuil de confiance détermine la certitude minimale requise pour "
            "que l'application considère une détection comme valide. Un seuil plus "
            "élevé réduit les fausses détections mais peut nécessiter des conditions "
            "plus optimales pour la reconnaissance."
        )
        explication_seuil.setWordWrap(True)
        explication_seuil.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(explication_seuil)
        
        # Conseils
        conseils = QLabel("Conseils pour améliorer les résultats:")
        conseils.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        layout.addWidget(conseils)
        
        liste_conseils = QLabel(
            "• Assurez-vous d'avoir un bon éclairage\n"
            "• Placez le fruit contre un fond contrasté\n"
            "• Centrez le fruit dans le rectangle de capture\n"
            "• Si la détection est instable, réduisez le seuil de confiance\n"
            "• Essayez différents angles si un fruit n'est pas reconnu\n"
        )
        liste_conseils.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(liste_conseils)
        
        layout.addStretch()
        self.tabs.addTab(page, "Reconnaissance")
    
    def _creer_onglet_faq(self):
        """Crée l'onglet de questions fréquentes"""
        page = QScrollArea()
        page.setWidgetResizable(True)
        page.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre
        titre = QLabel("Questions fréquemment posées")
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Questions et réponses
        q1 = QLabel("Q: Combien d'images sont nécessaires pour entraîner un bon modèle?")
        q1.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        q1.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
        layout.addWidget(q1)
        
        r1 = QLabel(
            "R: Il est recommandé de capturer au moins 50 images par fruit pour obtenir "
            "des résultats satisfaisants. Plus vous avez d'images variées, meilleure sera "
            "la précision du modèle. Avec l'augmentation de données, même 30 images par "
            "classe peuvent donner de bons résultats."
        )
        r1.setWordWrap(True)
        r1.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(r1)
        
        q2 = QLabel("Q: L'application peut-elle reconnaître n'importe quel fruit?")
        q2.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        q2.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
        layout.addWidget(q2)
        
        r2 = QLabel(
            "R: L'application peut reconnaître uniquement les fruits pour lesquels vous avez "
            "fourni des images d'entraînement. Si vous souhaitez ajouter un nouveau fruit, "
            "vous devrez capturer des images de ce fruit et réentraîner le modèle."
        )
        r2.setWordWrap(True)
        r2.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(r2)
        
        q3 = QLabel("Q: Combien de temps dure l'entraînement du modèle?")
        q3.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        q3.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
        layout.addWidget(q3)
        
        r3 = QLabel(
            "R: La durée de l'entraînement dépend de plusieurs facteurs: le nombre d'images, "
            "le nombre de classes (fruits différents), la taille des images et les paramètres "
            "d'entraînement choisis. En général, comptez entre 5 et 20 minutes pour un entraînement "
            "standard avec 5-10 types de fruits et 50 images par fruit."
        )
        r3.setWordWrap(True)
        r3.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(r3)
        
        q4 = QLabel("Q: Puis-je exporter mon modèle entraîné pour l'utiliser ailleurs?")
        q4.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        q4.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
        layout.addWidget(q4)
        
        r4 = QLabel(
            "R: Le modèle entraîné est automatiquement sauvegardé dans le dossier 'donnees' "
            "sous le nom 'modele_fruits.h5'. Vous pouvez copier ce fichier ainsi que le fichier "
            "'etiquettes.pkl' pour utiliser votre modèle dans d'autres applications compatibles "
            "avec TensorFlow/Keras."
        )
        r4.setWordWrap(True)
        r4.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(r4)
        
        q5 = QLabel("Q: Pourquoi mon modèle ne reconnaît-il pas correctement certains fruits?")
        q5.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_NORMAL, QFont.Bold))
        q5.setStyleSheet(f"color: {COULEUR_SECONDAIRE};")
        layout.addWidget(q5)
        
        r5 = QLabel(
            "R: Plusieurs raisons peuvent expliquer des erreurs de reconnaissance:\n"
            "• Nombre insuffisant d'images d'entraînement pour ce fruit\n"
            "• Images d'entraînement trop similaires (manque de variété)\n"
            "• Conditions d'éclairage différentes entre l'entraînement et la reconnaissance\n"
            "• Fruits visuellement similaires qui créent de la confusion\n"
            "• Angle de vue très différent de ceux présentés lors de l'entraînement\n\n"
            "Essayez de capturer plus d'images variées et de réentraîner le modèle."
        )
        r5.setWordWrap(True)
        r5.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(r5)
        
        page.setWidget(content)
        self.tabs.addTab(page, "FAQ")
