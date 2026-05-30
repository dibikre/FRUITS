# -*- coding: utf-8 -*-
"""
Module contenant la page de reconnaissance de fruits
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QSlider, QPushButton, QMessageBox, QFrame)
from PySide6.QtGui import QFont, QIcon, QPixmap, QImage
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer

import os
import cv2
import numpy as np
import json

from ..widgets.lecteur_camera import LecteurCamera
from ..widgets.bouton_anime import BoutonAnime
from ...modeles.detecteur import Detecteur
from ...outils.synthese_vocale import SyntheseVocale
from ...constantes import *

class PageReconnaissance(QWidget):
    """
    Page permettant de reconnaître des fruits en temps réel
    """
    
    def __init__(self, parent=None):
        """
        Initialise la page de reconnaissance
        
        Args:
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Variables de classe
        self.detecteur = Detecteur()
        self.synthese = SyntheseVocale()
        self.fruits_info = self._charger_fruits_info()
        self.seuil_confiance = 0.7
        self.dernier_fruit = None
        self.derniere_annonce = 0
        self.delai_annonces = 3  # secondes entre les annonces
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._reset_dernier_fruit)
        
        # Création de l'interface
        self._creer_interface()
    
    def _charger_fruits_info(self):
        """
        Charge les informations sur les fruits depuis le fichier JSON
        
        Returns:
            dict: Dictionnaire contenant les informations sur les fruits
        """
        try:
            with open(FICHIER_FRUITS_INFO, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des informations sur les fruits: {e}")
            return {"fruits": []}
    
    def _creer_interface(self):
        """Crée l'interface utilisateur de la page"""
        # Disposition principale
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre de la page
        titre = QLabel("Reconnaissance de fruits en temps réel")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Zone principale (caméra + résultats)
        main_layout = QHBoxLayout()
        
        # Zone de capture vidéo
        self.camera_widget = LecteurCamera()
        self.camera_widget.image_capturee.connect(self._traiter_image)
        main_layout.addWidget(self.camera_widget, 3)  # Prend 3/5 de l'espace
        
        # Séparateur vertical
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #2B3648;")
        main_layout.addWidget(separator)
        
        # Zone de résultats
        resultats_layout = QVBoxLayout()
        
        resultats_titre = QLabel("Résultats")
        resultats_titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        resultats_layout.addWidget(resultats_titre)
        
        # Fruit détecté
        self.fruit_detecte_label = QLabel("Aucun fruit détecté")
        self.fruit_detecte_label.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE))
        self.fruit_detecte_label.setAlignment(Qt.AlignCenter)
        self.fruit_detecte_label.setStyleSheet("""
            QLabel {
                color: #E1E1E1;
                background-color: #141D2B;
                border-radius: 8px;
                border: 1px solid #2B3648;
                padding: 10px;
            }
        """)
        self.fruit_detecte_label.setMinimumHeight(60)
        resultats_layout.addWidget(self.fruit_detecte_label)
        
        # Confiance
        confiance_layout = QHBoxLayout()
        
        confiance_label = QLabel("Confiance:")
        confiance_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        confiance_layout.addWidget(confiance_label)
        
        self.confiance_value_label = QLabel("0%")
        self.confiance_value_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        confiance_layout.addWidget(self.confiance_value_label)
        
        resultats_layout.addLayout(confiance_layout)
        
        # Barre de confiance
        self.confiance_bar = QWidget()
        self.confiance_bar.setMinimumHeight(20)
        self.confiance_bar.setStyleSheet("""
            QWidget {
                background-color: #007ACC;
                border-radius: 4px;
            }
        """)
        self.confiance_bar.setFixedWidth(0)
        
        confiance_bg = QWidget()
        confiance_bg.setMinimumHeight(20)
        confiance_bg.setStyleSheet("""
            QWidget {
                background-color: #141D2B;
                border-radius: 4px;
                border: 1px solid #2B3648;
            }
        """)
        
        bar_layout = QHBoxLayout(confiance_bg)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.addWidget(self.confiance_bar)
        bar_layout.addStretch()
        
        resultats_layout.addWidget(confiance_bg)
        
        # Seuil de confiance
        seuil_layout = QHBoxLayout()
        
        seuil_label = QLabel("Seuil de confiance:")
        seuil_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        seuil_layout.addWidget(seuil_label)
        
        self.seuil_slider = QSlider(Qt.Horizontal)
        self.seuil_slider.setMinimum(30)
        self.seuil_slider.setMaximum(95)
        self.seuil_slider.setValue(int(self.seuil_confiance * 100))
        self.seuil_slider.setTickPosition(QSlider.TicksBelow)
        self.seuil_slider.setTickInterval(10)
        self.seuil_slider.valueChanged.connect(self._changer_seuil)
        seuil_layout.addWidget(self.seuil_slider)
        
        self.seuil_value_label = QLabel(f"{int(self.seuil_confiance * 100)}%")
        self.seuil_value_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        seuil_layout.addWidget(self.seuil_value_label)
        
        resultats_layout.addLayout(seuil_layout)
        
        # Synthèse vocale
        voix_layout = QHBoxLayout()
        
        voix_label = QLabel("Synthèse vocale:")
        voix_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        voix_layout.addWidget(voix_label)
        
        self.voix_btn = QPushButton("Activée")
        self.voix_btn.setCheckable(True)
        self.voix_btn.setChecked(True)
        self.voix_btn.toggled.connect(self._toggle_voix)
        voix_layout.addWidget(self.voix_btn)
        
        resultats_layout.addLayout(voix_layout)
        
        # Description du fruit
        description_titre = QLabel("Description")
        description_titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_SOUS_TITRE, QFont.Bold))
        resultats_layout.addWidget(description_titre)
        
        self.description_label = QLabel("Aucun fruit détecté")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.description_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        self.description_label.setStyleSheet("""
            QLabel {
                background-color: #141D2B;
                border-radius: 8px;
                border: 1px solid #2B3648;
                padding: 10px;
            }
        """)
        self.description_label.setMinimumHeight(150)
        resultats_layout.addWidget(self.description_label)
        
        # Famille du fruit
        self.famille_label = QLabel("")
        font = QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL)
        font.setItalic(True)
        self.famille_label.setFont(font)
        resultats_layout.addWidget(self.famille_label)
        
        # Bouton de capture
        self.capturer_btn = BoutonAnime("Capturer cette image")
        self.capturer_btn.setIcon(QIcon(os.path.join(DOSSIER_ICONS, "camera.svg")))
        self.capturer_btn.setIconSize(QSize(20, 20))
        self.capturer_btn.clicked.connect(lambda: self.camera_widget._capturer_image())
        resultats_layout.addWidget(self.capturer_btn)
        
        resultats_layout.addStretch()
        main_layout.addLayout(resultats_layout, 2)  # Prend 2/5 de l'espace
        
        layout.addLayout(main_layout)
        
        # Vérifier si le modèle est chargé
        if not self.detecteur.modele_charge:
            self.fruit_detecte_label.setText("Modèle non chargé")
            self.fruit_detecte_label.setStyleSheet("""
                QLabel {
                    color: #E91E63;
                    background-color: #141D2B;
                    border-radius: 8px;
                    border: 1px solid #2B3648;
                    padding: 10px;
                }
            """)
            
            # Désactiver les fonctionnalités qui nécessitent le modèle
            self.camera_widget.camera_btn.setEnabled(False)
            self.camera_widget.camera_btn.setToolTip("Modèle non chargé. Veuillez d'abord entraîner un modèle.")
            
            QMessageBox.warning(self, "Modèle non chargé", 
                              "Le modèle de reconnaissance n'est pas chargé. Veuillez d'abord entraîner un modèle.")
    
    def _changer_seuil(self, valeur):
        """
        Change le seuil de confiance
        
        Args:
            valeur (int): Valeur du seuil (0-100)
        """
        self.seuil_confiance = valeur / 100.0
        self.seuil_value_label.setText(f"{valeur}%")
    
    def _toggle_voix(self, active):
        """
        Active ou désactive la synthèse vocale
        
        Args:
            active (bool): True pour activer, False pour désactiver
        """
        self.voix_btn.setText("Activée" if active else "Désactivée")
        if not active:
            self.synthese.arreter()
    
    def _traiter_image(self, image):
        """
        Traite l'image capturée par la caméra
        
        Args:
            image (numpy.ndarray): Image capturée
        """
        if not self.detecteur.modele_charge:
            return
        
        # Prédiction
        fruit, confiance = self.detecteur.predire(image)
        
        # Mise à jour de l'interface
        self._update_interface(fruit, confiance)
        
        # Synthèse vocale si nécessaire
        self._handle_voix(fruit, confiance)
    
    def _update_interface(self, fruit, confiance):
        """
        Met à jour l'interface avec les résultats de la prédiction
        
        Args:
            fruit (str): Nom du fruit détecté
            confiance (float): Niveau de confiance (0-1)
        """
        confiance_percent = int(confiance * 100)
        
        # Mise à jour de la barre de confiance
        self.confiance_bar.setFixedWidth(int(confiance * 200))  # Largeur max de 200px
        self.confiance_value_label.setText(f"{confiance_percent}%")
        
        # Si la confiance est inférieure au seuil, on affiche "Aucun fruit détecté"
        if confiance < self.seuil_confiance:
            self.fruit_detecte_label.setText("Aucun fruit détecté")
            self.description_label.setText("Aucun fruit détecté")
            self.famille_label.setText("")
            return
        
        # Mise à jour du nom du fruit
        self.fruit_detecte_label.setText(fruit)
        
        # Recherche des informations sur le fruit
        for f in self.fruits_info["fruits"]:
            if f["nom"] == fruit:
                self.description_label.setText(f["description"])
                self.famille_label.setText(f"Famille: {f['famille']}")
                break
    
    def _handle_voix(self, fruit, confiance):
        """
        Gère la synthèse vocale
        
        Args:
            fruit (str): Nom du fruit détecté
            confiance (float): Niveau de confiance (0-1)
        """
        # Si la synthèse est désactivée ou la confiance trop basse, on ne fait rien
        if not self.voix_btn.isChecked() or confiance < self.seuil_confiance:
            return
        
        import time
        
        # Si c'est un nouveau fruit ou si le délai est écoulé
        maintenant = time.time()
        if (fruit != self.dernier_fruit or maintenant - self.derniere_annonce > self.delai_annonces):
            self.synthese.parler(f"C'est un {fruit}")
            self.dernier_fruit = fruit
            self.derniere_annonce = maintenant
            
            # Démarrage du timer pour réinitialiser le dernier fruit après un délai
            self.timer.start(self.delai_annonces * 1000)
    
    def _reset_dernier_fruit(self):
        """Réinitialise le dernier fruit annoncé"""
        self.dernier_fruit = None
        self.timer.stop()
    
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la page"""
        self.camera_widget.arreter()
        self.synthese.arreter()
        super().closeEvent(event)
