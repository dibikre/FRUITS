# -*- coding: utf-8 -*-
"""
Module contenant le dialogue pour ajouter un nouveau fruit
"""

import os
import shutil
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout,
    QPushButton, QCheckBox, QSpinBox, QGroupBox, QLabel, QFileDialog, QMessageBox,
    QScrollArea, QWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

from ...constantes import (
    DOSSIER_DATASET, DOSSIER_ASSETS, COULEUR_PRIMAIRE, COULEUR_SECONDAIRE,
    POLICE_PRINCIPALE, POLICE_SECONDAIRE, COULEUR_TEXTE
)

class DialogAjoutFruit(QDialog):
    """
    Dialogue permettant d'ajouter un nouveau fruit à la base de données
    """
    
    def __init__(self, fruits_existants, parent=None):
        """
        Initialise le dialogue
        
        Args:
            fruits_existants (list): Liste des noms de fruits déjà présents
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        self.fruits_existants = [f.lower() for f in fruits_existants]
        self.dataset_dir_path = ""
        self.fruit_cree = None
        
        # Configuration de la fenêtre
        self.setWindowTitle("Ajouter un nouveau fruit")
        self.setMinimumSize(550, 650)
        self.resize(600, 750)
        
        # Thème sombre cohérent
        self.setStyleSheet("""
            QDialog {
                background-color: #0D1117;
            }
            QLabel {
                color: #E1E1E1;
            }
            QLineEdit, QTextEdit, QSpinBox {
                background-color: #141D2B;
                color: #E1E1E1;
                border: 1px solid #2B3648;
                border-radius: 4px;
                padding: 6px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
                border: 1px solid #007ACC;
            }
            QGroupBox {
                border: 1px solid #2B3648;
                border-radius: 6px;
                margin-top: 15px;
                padding-top: 15px;
                font-weight: bold;
                color: #00BFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QCheckBox {
                color: #E1E1E1;
                spacing: 8px;
            }
            QPushButton {
                background-color: #1A2332;
                color: #E1E1E1;
                border: 1px solid #007ACC;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007ACC;
                color: white;
            }
            QPushButton:disabled {
                background-color: #1A2332;
                color: #7A7A7A;
                border: 1px solid #2B3648;
            }
        """)
        
        # Création de l'interface
        self._creer_interface()
        
    def _creer_interface(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)
        
        # Titre
        titre = QLabel("Nouveau fruit et Dataset")
        titre.setFont(QFont(POLICE_PRINCIPALE, 16, QFont.Bold))
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("color: #FFFFFF; margin-bottom: 10px;")
        layout_principal.addWidget(titre)
        
        # Scroll Area pour le formulaire
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        form_layout = QFormLayout(scroll_content)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(0, 0, 10, 0)
        
        # --- Section 1: Informations de base ---
        # Nom du fruit
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Ex: Mangoustan")
        form_layout.addRow("Nom du fruit (obligatoire) :", self.nom_input)
        
        # Famille
        self.famille_input = QLineEdit()
        self.famille_input.setPlaceholderText("Ex: Clusiaceae")
        form_layout.addRow("Famille :", self.famille_input)
        
        # Origine
        self.origine_input = QLineEdit()
        self.origine_input.setPlaceholderText("Ex: Asie du Sud-Est")
        form_layout.addRow("Origine :", self.origine_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description détaillée du fruit...")
        self.description_input.setMaximumHeight(100)
        form_layout.addRow("Description :", self.description_input)
        
        # Saisons (multi-sélection)
        saisons_layout = QHBoxLayout()
        self.check_printemps = QCheckBox("Printemps")
        self.check_ete = QCheckBox("Été")
        self.check_automne = QCheckBox("Automne")
        self.check_hiver = QCheckBox("Hiver")
        saisons_layout.addWidget(self.check_printemps)
        saisons_layout.addWidget(self.check_ete)
        saisons_layout.addWidget(self.check_automne)
        saisons_layout.addWidget(self.check_hiver)
        form_layout.addRow("Saisons de récolte :", saisons_layout)
        
        # --- Section 2: Valeurs nutritionnelles ---
        group_nutrition = QGroupBox("Propriétés nutritionnelles (pour 100g)")
        nutrition_form = QFormLayout(group_nutrition)
        nutrition_form.setSpacing(10)
        
        self.calories_spin = QSpinBox()
        self.calories_spin.setRange(0, 1000)
        self.calories_spin.setValue(50)
        nutrition_form.addRow("Calories (kcal) :", self.calories_spin)
        
        self.fibres_input = QLineEdit()
        self.fibres_input.setPlaceholderText("Ex: 1.8g")
        nutrition_form.addRow("Fibres (g) :", self.fibres_input)
        
        self.vit_c_input = QLineEdit()
        self.vit_c_input.setPlaceholderText("Ex: 48mg")
        nutrition_form.addRow("Vitamine C (mg) :", self.vit_c_input)
        
        self.potassium_input = QLineEdit()
        self.potassium_input.setPlaceholderText("Ex: 150mg")
        nutrition_form.addRow("Potassium (mg) :", self.potassium_input)
        
        form_layout.addRow(group_nutrition)
        
        # --- Section 3: Sélection du Dataset ---
        group_dataset = QGroupBox("Données d'entraînement (Dataset)")
        dataset_layout = QVBoxLayout(group_dataset)
        dataset_layout.setSpacing(10)
        
        # Instruction/Conformité explicite
        consigne_label = QLabel(
            "<b>Consignes de conformité du dossier de dataset :</b><br/>"
            "• Le dossier doit contenir directement les images du fruit.<br/>"
            "• Formats d'images acceptés : <b>.jpg, .jpeg, .png</b>.<br/>"
            "• Les images doivent idéalement être cadrées sur le fruit.<br/>"
            "• <b>Important :</b> Les images seront copiées et renommées séquentiellement "
            "(1.jpg, 2.jpg...) dans le dossier de l'application. La première image servira d'illustration."
        )
        consigne_label.setWordWrap(True)
        consigne_label.setFont(QFont(POLICE_SECONDAIRE, 9))
        consigne_label.setStyleSheet("color: #00BFFF; background-color: rgba(0, 191, 255, 0.05); padding: 8px; border-radius: 4px; border: 1px solid rgba(0, 191, 255, 0.2);")
        dataset_layout.addWidget(consigne_label)
        
        selection_h_layout = QHBoxLayout()
        self.dataset_path_label = QLabel("Aucun dossier sélectionné")
        self.dataset_path_label.setWordWrap(True)
        self.dataset_path_label.setStyleSheet("color: #7A7A7A; font-style: italic;")
        
        btn_parcourir = QPushButton("Parcourir...")
        btn_parcourir.clicked.connect(self._parcourir_dataset)
        
        selection_h_layout.addWidget(self.dataset_path_label, 1)
        selection_h_layout.addWidget(btn_parcourir)
        dataset_layout.addLayout(selection_h_layout)
        
        form_layout.addRow(group_dataset)
        
        scroll_area.setWidget(scroll_content)
        layout_principal.addWidget(scroll_area)
        
        # Séparateur
        separateur = QWidget()
        separateur.setFixedHeight(1)
        separateur.setStyleSheet("background-color: #2B3648;")
        layout_principal.addWidget(separateur)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet("background-color: transparent; border: 1px solid #2B3648;")
        btn_annuler.clicked.connect(self.reject)
        
        self.btn_ajouter = QPushButton("Ajouter le fruit")
        self.btn_ajouter.clicked.connect(self._valider_et_ajouter)
        
        actions_layout.addStretch()
        actions_layout.addWidget(btn_annuler)
        actions_layout.addWidget(self.btn_ajouter)
        layout_principal.addLayout(actions_layout)

    def _parcourir_dataset(self):
        """Ouvre un dialogue pour sélectionner le dossier de dataset"""
        dossier = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier contenant les images du fruit",
            os.path.expanduser("~")
        )
        if dossier:
            self.dataset_dir_path = os.path.abspath(dossier)
            self.dataset_path_label.setText(self.dataset_dir_path)
            self.dataset_path_label.setStyleSheet("color: #E1E1E1; font-style: normal;")

    def _valider_et_ajouter(self):
        """Valide les saisies, copie les fichiers et génère le dictionnaire du fruit"""
        nom = self.nom_input.text().strip()
        
        # Validation du nom
        if not nom:
            QMessageBox.warning(self, "Nom manquant", "Le nom du fruit est obligatoire.")
            return
            
        if nom.lower() in self.fruits_existants:
            QMessageBox.warning(self, "Fruit doublon", f"Le fruit '{nom}' existe déjà dans la base de données.")
            return
            
        # Validation du dataset
        if not self.dataset_dir_path or not os.path.exists(self.dataset_dir_path):
            QMessageBox.warning(self, "Dataset manquant", "Veuillez sélectionner un dossier de dataset valide.")
            return
            
        # Scanner les images du dossier sélectionné
        extensions_valides = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        fichiers_images = [
            f for f in os.listdir(self.dataset_dir_path)
            if f.lower().endswith(extensions_valides) and os.path.isfile(os.path.join(self.dataset_dir_path, f))
        ]
        
        if not fichiers_images:
            QMessageBox.warning(
                self, 
                "Aucune image", 
                "Le dossier sélectionné ne contient aucune image valide (.jpg, .jpeg, .png)."
            )
            return
            
        # Si moins de 30 images, avertir mais autoriser
        if len(fichiers_images) < 30:
            reponse = QMessageBox.question(
                self,
                "Dataset réduit",
                f"Le dossier contient seulement {len(fichiers_images)} images. Il est recommandé d'avoir au moins 30 images pour l'entraînement.\n\nVoulez-vous continuer ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reponse == QMessageBox.No:
                return

        # Désactiver le bouton d'ajout pendant le traitement
        self.btn_ajouter.setEnabled(False)
        self.btn_ajouter.setText("Copie en cours...")
        
        try:
            # 1. Préparer les répertoires de destination
            nom_classe_dataset = nom.lower()
            nom_classe_assets = nom.capitalize()
            
            cible_dataset_dir = os.path.join(DOSSIER_DATASET, nom_classe_dataset)
            os.makedirs(cible_dataset_dir, exist_ok=True)
            
            cible_assets_dir = os.path.join(DOSSIER_ASSETS, "images_fruits", nom_classe_assets)
            os.makedirs(cible_assets_dir, exist_ok=True)
            
            # 2. Copier et renommer les images dans le dataset
            ext_illustration = "jpg"
            illustration_source = os.path.join(self.dataset_dir_path, fichiers_images[0])
            _, ext_illustration = os.path.splitext(fichiers_images[0])
            ext_illustration = ext_illustration.strip('.').lower()
            
            for idx, fichier in enumerate(fichiers_images, start=1):
                src_path = os.path.join(self.dataset_dir_path, fichier)
                _, ext = os.path.splitext(fichier)
                dst_path = os.path.join(cible_dataset_dir, f"{idx}{ext.lower()}")
                shutil.copy2(src_path, dst_path)
            
            # 3. Copier l'illustration
            illustration_cible = os.path.join(cible_assets_dir, f"{nom_classe_assets}.{ext_illustration}")
            shutil.copy2(illustration_source, illustration_cible)
            
            # 4. Construire la liste des saisons
            saisons = []
            if self.check_printemps.isChecked(): saisons.append("Printemps")
            if self.check_ete.isChecked(): saisons.append("Été")
            if self.check_automne.isChecked(): saisons.append("Automne")
            if self.check_hiver.isChecked(): saisons.append("Hiver")
            
            # 5. Propriétés nutritives
            proprietes = {
                "calories": self.calories_spin.value()
            }
            fibres = self.fibres_input.text().strip()
            if fibres: proprietes["fibres"] = fibres
            vit_c = self.vit_c_input.text().strip()
            if vit_c: proprietes["vitamine_c"] = vit_c
            potassium = self.potassium_input.text().strip()
            if potassium: proprietes["potassium"] = potassium
            
            # 6. Dictionnaire final pour fruits_info.json
            chemin_relatif_illu = f"assets/images_fruits/{nom_classe_assets}/{nom_classe_assets}.{ext_illustration}"
            self.fruit_cree = {
                "nom": nom,
                "type_img": ext_illustration,
                "description": self.description_input.toPlainText().strip(),
                "famille": self.famille_input.text().strip() or "Inconnue",
                "proprietes_nutritives": proprietes,
                "origine": self.origine_input.text().strip() or "Inconnue",
                "saison": saisons if saisons else ["Toute l'année"],
                "direction": chemin_relatif_illu
            }
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erreur d'importation", 
                f"Une erreur est survenue lors de la copie des fichiers :\n{str(e)}"
            )
            # Nettoyer en cas d'erreur
            try:
                if os.path.exists(cible_dataset_dir):
                    shutil.rmtree(cible_dataset_dir)
                if os.path.exists(cible_assets_dir):
                    shutil.rmtree(cible_assets_dir)
            except Exception:
                pass
                
            self.btn_ajouter.setEnabled(True)
            self.btn_ajouter.setText("Ajouter le fruit")
