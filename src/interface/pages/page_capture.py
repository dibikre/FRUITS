# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QComboBox, QSpinBox, QProgressBar, QMessageBox,
                              QScrollArea, QGridLayout, QPushButton)
from PySide6.QtGui import QFont, QIcon, QPixmap, QImage
from PySide6.QtCore import Qt, Signal, Slot, QSize, QTimer

import os
import cv2
import json
import numpy as np

from ..widgets.lecteur_camera import LecteurCamera
from ..widgets.bouton_anime import BoutonAnime
from ...outils.capteur_image import CapteurImage
from ...constantes import *

class PageCapture(QWidget):
    """
    Page permettant de capturer des images pour l'entraînement du modèle
    """
    
    def __init__(self, parent=None):
        """
        Initialise la page de capture
        
        Args:
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Variables de classe
        self.fruits_info = self._charger_fruits_info()
        self.fruits = [fruit["nom"] for fruit in self.fruits_info["fruits"]]
        self.current_fruit = None
        self.image_count = 0
        self.total_images = 0
        self.capteur = CapteurImage()
        
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
        titre = QLabel("Capture d'images pour l'entraînement")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Zone de contrôle
        controle_layout = QHBoxLayout()
        
        # Sélection du fruit
        selection_layout = QVBoxLayout()
        
        selection_label = QLabel("Sélectionner le fruit à capturer:")
        selection_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        selection_layout.addWidget(selection_label)
        
        self.fruit_combo = QComboBox()
        self.fruit_combo.addItems(self.fruits)
        self.fruit_combo.setCurrentIndex(0)
        self.current_fruit = self.fruits[0]
        self.fruit_combo.currentTextChanged.connect(self._changer_fruit)
        selection_layout.addWidget(self.fruit_combo)
        
        # Nombre d'images à capturer
        nombre_label = QLabel("Nombre d'images par fruit:")
        nombre_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        selection_layout.addWidget(nombre_label)
        
        self.nombre_spin = QSpinBox()
        self.nombre_spin.setMinimum(10)
        self.nombre_spin.setMaximum(100)
        self.nombre_spin.setValue(50)
        self.total_images = 50
        self.nombre_spin.valueChanged.connect(self._changer_nombre)
        selection_layout.addWidget(self.nombre_spin)
        
        # Bouton de démarrage de capture
        self.demarrer_btn = BoutonAnime("Démarrer la session de capture")
        self.demarrer_btn.setIcon(QIcon(os.path.join(DOSSIER_ICONS, "camera.svg")))
        self.demarrer_btn.setIconSize(QSize(20, 20))
        self.demarrer_btn.clicked.connect(self._demarrer_capture)
        selection_layout.addWidget(self.demarrer_btn)
        
        # Bouton d'arrêt de capture
        self.arreter_btn = BoutonAnime("Arrêter la capture")
        self.arreter_btn.setEnabled(False)
        self.arreter_btn.clicked.connect(self._arreter_capture)
        selection_layout.addWidget(self.arreter_btn)
        
        selection_layout.addStretch()
        controle_layout.addLayout(selection_layout)
        
        # Séparateur vertical
        separateur = QWidget()
        separateur.setFixedWidth(1)
        separateur.setStyleSheet("background-color: #2B3648;")
        controle_layout.addWidget(separateur)
        
        # Affichage de la caméra
        self.camera_widget = LecteurCamera()
        self.camera_widget.image_capturee.connect(self._traiter_image_capturee)
        controle_layout.addWidget(self.camera_widget, 2)
        
        layout.addLayout(controle_layout)
        
        # Progression de la capture
        progression_layout = QHBoxLayout()
        
        progression_label = QLabel("Progression:")
        progression_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        progression_layout.addWidget(progression_label)
        
        self.progression_bar = QProgressBar()
        self.progression_bar.setMinimum(0)
        self.progression_bar.setMaximum(self.total_images)
        self.progression_bar.setValue(0)
        progression_layout.addWidget(self.progression_bar)
        
        self.progression_label = QLabel("0/50")
        progression_layout.addWidget(self.progression_label)
        
        layout.addLayout(progression_layout)
        
        # Zone d'affichage des images capturées
        images_label = QLabel("Images capturées:")
        images_label.setFont(QFont(POLICE_SECONDAIRE, TAILLE_TEXTE_NORMAL))
        layout.addWidget(images_label)
        
        # Scroll area pour les images
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #141D2B;
                border: 1px solid #2B3648;
                border-radius: 4px;
            }
        """)
        
        scroll_widget = QWidget()
        self.images_grid = QGridLayout(scroll_widget)
        self.images_grid.setContentsMargins(10, 10, 10, 10)
        self.images_grid.setSpacing(10)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Cache de la session de capture
        self.capture_active = False
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self._capturer_auto)
        self.capture_intervalle = 1000  # 1 seconde entre chaque capture
    
    def _changer_fruit(self, nom_fruit):
        """
        Change le fruit actuel pour la capture
        
        Args:
            nom_fruit (str): Nom du fruit à capturer
        """
        self.current_fruit = nom_fruit
    
    def _changer_nombre(self, nombre):
        """
        Change le nombre d'images à capturer
        
        Args:
            nombre (int): Nombre d'images à capturer
        """
        self.total_images = nombre
        self.progression_bar.setMaximum(nombre)
        self.progression_label.setText(f"{self.image_count}/{nombre}")
    
    def _demarrer_capture(self):
        """Démarre une session de capture automatique"""
        # Vérification que le répertoire du dataset existe
        dataset_dir = os.path.join(DOSSIER_DATASET, self.current_fruit)
        os.makedirs(dataset_dir, exist_ok=True)
        
        # Initialisation de la capture
        self.capture_active = True
        self.image_count = 0
        self.progression_bar.setValue(0)
        self.progression_label.setText(f"0/{self.total_images}")
        
        # Nettoyage de la grille d'images
        for i in reversed(range(self.images_grid.count())):
            self.images_grid.itemAt(i).widget().setParent(None)
        
        # Configuration de l'interface
        self.demarrer_btn.setEnabled(False)
        self.arreter_btn.setEnabled(True)
        self.fruit_combo.setEnabled(False)
        self.nombre_spin.setEnabled(False)
        
        # Démarrage du timer pour la capture automatique
        self.capture_timer.start(self.capture_intervalle)
    
    def _arreter_capture(self):
        """Arrête la session de capture automatique"""
        self.capture_active = False
        self.capture_timer.stop()
        
        # Configuration de l'interface
        self.demarrer_btn.setEnabled(True)
        self.arreter_btn.setEnabled(False)
        self.fruit_combo.setEnabled(True)
        self.nombre_spin.setEnabled(True)
    
    def _capturer_auto(self):
        """Déclenche la capture automatique"""
        if self.capture_active:
            self.camera_widget._capturer_image()
    
    @Slot(np.ndarray)
    def _traiter_image_capturee(self, image):
        """
        Traite l'image capturée par la caméra
        
        Args:
            image (numpy.ndarray): Image capturée
        """
        # Suppression de l'effet miroir
        image = cv2.flip(image, 1)
        
        if not self.capture_active:
            return
        
        # Enregistrement de l'image
        try:
            dataset_dir = os.path.join(DOSSIER_DATASET, self.current_fruit)
            os.makedirs(dataset_dir, exist_ok=True)
            
            image_path = os.path.join(dataset_dir, f"{self.image_count + 1}.jpg")
            cv2.imwrite(image_path, image)
            
            # Mise à jour de l'interface
            self.image_count += 1
            self.progression_bar.setValue(self.image_count)
            self.progression_label.setText(f"{self.image_count}/{self.total_images}")
            
            # Ajout de l'image à la grille
            self._ajouter_image_grille(image)
            
            # Arrêt de la capture si le nombre d'images est atteint
            if self.image_count >= self.total_images:
                self._arreter_capture()
                QMessageBox.information(self, "Capture terminée", 
                                     f"Capture de {self.total_images} images de {self.current_fruit} terminée avec succès.")
        except Exception as e:
            print(f"Erreur lors de la capture: {e}")
            QMessageBox.warning(self, "Erreur de capture", 
                              f"Une erreur est survenue lors de la capture: {str(e)}")
    
    def _ajouter_image_grille(self, image):
        """
        Ajoute une image à la grille d'affichage
        
        Args:
            image (numpy.ndarray): Image à ajouter
        """
        # Conversion BGR -> RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Redimensionnement pour l'affichage
        h, w = rgb_image.shape[:2]
        aspect_ratio = w / h
        thumbnail_width = 120
        thumbnail_height = int(thumbnail_width / aspect_ratio)
        
        resized = cv2.resize(rgb_image, (thumbnail_width, thumbnail_height))
        
        # Conversion en QPixmap
        h, w, ch = resized.shape
        q_image = QImage(resized.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        
        # Création du label pour l'affichage
        img_label = QLabel()
        img_label.setFixedSize(thumbnail_width, thumbnail_height)
        img_label.setPixmap(pixmap)  # Utilisez le QPixmap, pas le QImage
        img_label.setStyleSheet("border: 1px solid #2B3648;")
        
        # Ajout à la grille
        row = (self.image_count - 1) // 5
        col = (self.image_count - 1) % 5
        self.images_grid.addWidget(img_label, row, col)
    
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la page"""
        self._arreter_capture()
        self.camera_widget.arreter()
        super().closeEvent(event)
