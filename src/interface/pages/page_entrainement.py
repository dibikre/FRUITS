# -*- coding: utf-8 -*-
"""
Module contenant la page d'entraînement du modèle
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QSpinBox, QProgressBar, QMessageBox, QTextEdit,
                              QComboBox, QCheckBox, QPushButton, QFormLayout,
                              QGroupBox, QScrollArea)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, Signal, Slot, QSize, QThread, QTimer

import os
import json
import threading

from ..widgets.bouton_anime import BoutonAnime
from ...modeles.entraineur import Entraineur
from ...constantes import *

class EntainementThread(QThread):
    """Thread d'entraînement du modèle"""
    
    progression = Signal(int, str)  # Signal pour la progression (pourcentage, message)
    fin = Signal(bool, str)  # Signal de fin (succès, message)
    log = Signal(str)  # Signal pour les logs
    
    def __init__(self, entraineur, params, parent=None):
        """
        Initialise le thread d'entraînement
        
        Args:
            entraineur (Entraineur): Instance de l'entraineur
            params (dict): Paramètres d'entraînement
            parent (QObject, optionnel): Objet parent
        """
        super().__init__(parent)
        self.entraineur = entraineur
        self.params = params
    
    def run(self):
        """Méthode principale du thread"""
        try:
            # Emission du log de démarrage
            self.log.emit("Démarrage de l'entraînement...")
            self.log.emit(f"Configuration: {self.params}")
            
            # Callback de progression
            def progress_callback(epoch, total_epochs, train_loss, train_acc):
                percentage = int((epoch + 1) / total_epochs * 100)
                message = f"Epoque {epoch+1}/{total_epochs} - Perte: {train_loss:.4f} - Precision: {train_acc:.4f}"
                self.progression.emit(percentage, message)
                self.log.emit(message)
            
            # Entraînement du modèle
            success = self.entraineur.entrainer(
                taille_image=self.params["taille_image"],
                batch_size=self.params["batch_size"],
                epochs=self.params["epochs"],
                validation_split=self.params["validation_split"],
                augmentation=self.params["augmentation"],
                progress_callback=progress_callback
            )
            
            if success:
                self.fin.emit(True, "Entraînement terminé avec succès")
                self.log.emit("Modèle enregistré avec succès!")
            else:
                self.fin.emit(False, "Erreur lors de l'entraînement du modèle")
                self.log.emit("Échec de l'entraînement du modèle.")
                
        except Exception as e:
            self.fin.emit(False, f"Erreur: {str(e)}")
            self.log.emit(f"Erreur: {str(e)}")

class PageEntrainement(QWidget):
    """
    Page d'entraînement du modèle de reconnaissance
    """
    
    def __init__(self, parent=None):
        """
        Initialise la page d'entraînement
        
        Args:
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Variables de classe
        self.entraineur = Entraineur()
        self.thread_entrainement = None
        
        # Chargement de la configuration
        try:
            with open(FICHIER_CONFIG, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            self.config = {
                "modele": {
                    "taille_image": [64, 64],
                    "batch_size": 32,
                    "epochs": 20,
                    "validation_split": 0.2
                },
                "entrainement": {
                    "augmentation": {
                        "rotation_range": 20,
                        "width_shift_range": 0.2,
                        "height_shift_range": 0.2,
                        "shear_range": 0.2,
                        "zoom_range": 0.2,
                        "horizontal_flip": True
                    }
                }
            }
        
        # Création de l'interface
        self._creer_interface()
    
    def _creer_interface(self):
        """Crée l'interface utilisateur de la page"""
        # Disposition principale
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Titre de la page
        titre = QLabel("Entraînement du modèle de reconnaissance")
        titre.setAlignment(Qt.AlignCenter)
        titre.setFont(QFont(POLICE_PRINCIPALE, TAILLE_TEXTE_TITRE, QFont.Bold))
        layout.addWidget(titre)
        
        # Zone de contrôle et logs
        corps_layout = QHBoxLayout()
        
        # Panneau de configuration
        config_panel = QGroupBox("Configuration de l'entraînement")
        config_layout = QVBoxLayout(config_panel)
        
        # Formulaire de configuration
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(10, 10, 10, 10)
        
        # Taille de l'image
        self.taille_combo = QComboBox()
        self.taille_combo.addItems(["32x32", "64x64", "96x96", "128x128"])
        # Sélection de la valeur par défaut
        index = 1  # 64x64 par défaut
        if self.config["modele"]["taille_image"] == [32, 32]:
            index = 0
        elif self.config["modele"]["taille_image"] == [96, 96]:
            index = 2
        elif self.config["modele"]["taille_image"] == [128, 128]:
            index = 3
        self.taille_combo.setCurrentIndex(index)
        form_layout.addRow("Taille de l'image:", self.taille_combo)
        
        # Batch size
        self.batch_spin = QSpinBox()
        self.batch_spin.setMinimum(8)
        self.batch_spin.setMaximum(128)
        self.batch_spin.setSingleStep(8)
        self.batch_spin.setValue(self.config["modele"]["batch_size"])
        form_layout.addRow("Taille du batch:", self.batch_spin)
        
        # Nombre d'époques
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setMinimum(5)
        self.epochs_spin.setMaximum(100)
        self.epochs_spin.setValue(self.config["modele"]["epochs"])
        form_layout.addRow("Nombre d'époques:", self.epochs_spin)
        
        # Split de validation
        self.validation_combo = QComboBox()
        self.validation_combo.addItems(["10%", "20%", "30%"])
        # Sélection de la valeur par défaut
        index = 1  # 20% par défaut
        if self.config["modele"]["validation_split"] == 0.1:
            index = 0
        elif self.config["modele"]["validation_split"] == 0.3:
            index = 2
        self.validation_combo.setCurrentIndex(index)
        form_layout.addRow("Split de validation:", self.validation_combo)
        
        config_layout.addLayout(form_layout)
        
        # Augmentation de données
        augmentation_group = QGroupBox("Augmentation de données")
        augmentation_layout = QVBoxLayout(augmentation_group)
        
        self.augmentation_check = QCheckBox("Activer l'augmentation")
        self.augmentation_check.setChecked(True)
        augmentation_layout.addWidget(self.augmentation_check)
        
        # Options d'augmentation
        self.rotation_check = QCheckBox("Rotation (±20°)")
        self.rotation_check.setChecked(self.config["entrainement"]["augmentation"]["rotation_range"] > 0)
        augmentation_layout.addWidget(self.rotation_check)
        
        self.shift_check = QCheckBox("Décalage (±20%)")
        self.shift_check.setChecked(self.config["entrainement"]["augmentation"]["width_shift_range"] > 0)
        augmentation_layout.addWidget(self.shift_check)
        
        self.zoom_check = QCheckBox("Zoom (±20%)")
        self.zoom_check.setChecked(self.config["entrainement"]["augmentation"]["zoom_range"] > 0)
        augmentation_layout.addWidget(self.zoom_check)
        
        self.flip_check = QCheckBox("Retournement horizontal")
        self.flip_check.setChecked(self.config["entrainement"]["augmentation"]["horizontal_flip"])
        augmentation_layout.addWidget(self.flip_check)
        
        config_layout.addWidget(augmentation_group)
        
        # Bouton d'entraînement
        self.entrainer_btn = BoutonAnime("Démarrer l'entraînement")
        self.entrainer_btn.setIcon(QIcon(os.path.join(DOSSIER_ICONS, "entrainement.svg")))
        self.entrainer_btn.setIconSize(QSize(20, 20))
        self.entrainer_btn.clicked.connect(self._demarrer_entrainement)
        config_layout.addWidget(self.entrainer_btn)
        
        corps_layout.addWidget(config_panel)
        
        # Zone de logs et progression
        logs_panel = QGroupBox("Progression et logs")
        logs_layout = QVBoxLayout(logs_panel)
        
        # Barre de progression
        self.progression_bar = QProgressBar()
        self.progression_bar.setMinimum(0)
        self.progression_bar.setMaximum(100)
        self.progression_bar.setValue(0)
        logs_layout.addWidget(self.progression_bar)
        
        self.progression_label = QLabel("En attente de démarrage...")
        logs_layout.addWidget(self.progression_label)
        
        # Zone de logs
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet("""
            QTextEdit {
                background-color: #141D2B;
                color: #E1E1E1;
                border: 1px solid #2B3648;
                border-radius: 4px;
                font-family: Consolas, Monaco, monospace;
                font-size: 12px;
            }
        """)
        logs_layout.addWidget(self.logs_text)
        
        corps_layout.addWidget(logs_panel)
        
        layout.addLayout(corps_layout)
    
    def _demarrer_entrainement(self):
        """Démarre l'entraînement du modèle"""
        # Récupération des paramètres
        params = self._get_parameters()
        
        # Vérification des données d'entraînement
        if not self._verifier_donnees():
            QMessageBox.warning(self, "Données insuffisantes", 
                              "Pas assez de données d'entraînement. Veuillez capturer des images pour chaque fruit.")
            return
        
        # Désactivation de l'interface pendant l'entraînement
        self._toggle_interface(False)
        
        # Réinitialisation des logs et de la progression
        self.logs_text.clear()
        self.progression_bar.setValue(0)
        self.progression_label.setText("Initialisation de l'entraînement...")
        
        # Création et démarrage du thread d'entraînement
        self.thread_entrainement = EntainementThread(self.entraineur, params, self)
        self.thread_entrainement.progression.connect(self._update_progression)
        self.thread_entrainement.fin.connect(self._entrainement_termine)
        self.thread_entrainement.log.connect(self._ajouter_log)
        self.thread_entrainement.start()
    
    def _get_parameters(self):
        """
        Récupère les paramètres d'entraînement depuis l'interface
        
        Returns:
            dict: Paramètres d'entraînement
        """
        # Taille de l'image
        taille_text = self.taille_combo.currentText()
        taille = [int(taille_text.split("x")[0])] * 2
        
        # Validation split
        validation_text = self.validation_combo.currentText()
        validation_split = float(validation_text.strip("%")) / 100
        
        # Augmentation
        augmentation = None
        if self.augmentation_check.isChecked():
            augmentation = {
                "rotation_range": 20 if self.rotation_check.isChecked() else 0,
                "width_shift_range": 0.2 if self.shift_check.isChecked() else 0,
                "height_shift_range": 0.2 if self.shift_check.isChecked() else 0,
                "shear_range": 0.2,
                "zoom_range": 0.2 if self.zoom_check.isChecked() else 0,
                "horizontal_flip": self.flip_check.isChecked()
            }
        
        return {
            "taille_image": taille,
            "batch_size": self.batch_spin.value(),
            "epochs": self.epochs_spin.value(),
            "validation_split": validation_split,
            "augmentation": augmentation
        }
    
    def _verifier_donnees(self):
        """
        Vérifie si les données d'entraînement sont suffisantes
        
        Returns:
            bool: True si les données sont suffisantes, False sinon
        """
        if not os.path.exists(DOSSIER_DATASET):
            return False
        
        # Vérifier qu'il y a au moins 10 images pour au moins 2 classes
        classes_valides = 0
        for dossier in os.listdir(DOSSIER_DATASET):
            chemin_dossier = os.path.join(DOSSIER_DATASET, dossier)
            if os.path.isdir(chemin_dossier):
                fichiers = [f for f in os.listdir(chemin_dossier) if f.endswith(('.jpg', '.jpeg', '.png'))]
                if len(fichiers) >= 10:
                    classes_valides += 1
        
        return classes_valides >= 2
    
    def _toggle_interface(self, enabled):
        """
        Active ou désactive les éléments de l'interface
        
        Args:
            enabled (bool): True pour activer, False pour désactiver
        """
        self.taille_combo.setEnabled(enabled)
        self.batch_spin.setEnabled(enabled)
        self.epochs_spin.setEnabled(enabled)
        self.validation_combo.setEnabled(enabled)
        self.augmentation_check.setEnabled(enabled)
        self.rotation_check.setEnabled(enabled)
        self.shift_check.setEnabled(enabled)
        self.zoom_check.setEnabled(enabled)
        self.flip_check.setEnabled(enabled)
        self.entrainer_btn.setEnabled(enabled)
    
    @Slot(int, str)
    def _update_progression(self, percentage, message):
        """
        Met à jour la progression de l'entraînement
        
        Args:
            percentage (int): Pourcentage de progression
            message (str): Message de progression
        """
        self.progression_bar.setValue(percentage)
        self.progression_label.setText(message)
    
    @Slot(bool, str)
    def _entrainement_termine(self, success, message):
        """
        Gère la fin de l'entraînement
        
        Args:
            success (bool): True si l'entraînement a réussi, False sinon
            message (str): Message de résultat
        """
        # Réactivation de l'interface
        self._toggle_interface(True)
        
        # Affichage du résultat
        if success:
            QMessageBox.information(self, "Entraînement terminé", message)
        else:
            QMessageBox.warning(self, "Erreur d'entraînement", message)
    
    @Slot(str)
    def _ajouter_log(self, log):
        """
        Ajoute une ligne de log à la zone de logs
        
        Args:
            log (str): Message de log
        """
        self.logs_text.append(log)
        # Défilement automatique vers le bas
        scrollbar = self.logs_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
