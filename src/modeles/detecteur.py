# -*- coding: utf-8 -*-
"""
Module contenant la classe de détection de fruits
"""

import os
import pickle
import numpy as np
import cv2
from tensorflow.keras.models import load_model

from ..constantes import *

class Detecteur:
    """
    Classe responsable de la détection de fruits en temps réel
    """
    
    def __init__(self, chemin_modele=FICHIER_MODELE, chemin_etiquettes=FICHIER_ETIQUETTES):
        """
        Initialise le détecteur
        
        Args:
            chemin_modele (str): Chemin vers le modèle entraîné
            chemin_etiquettes (str): Chemin vers les étiquettes des classes
        """
        self.modele = None
        self.etiquettes = None
        self.taille_image = TAILLE_IMAGE
        self.modele_charge = False
        
        # Chargement du modèle et des étiquettes
        self._charger_modele(chemin_modele, chemin_etiquettes)
    
    def _charger_modele(self, chemin_modele, chemin_etiquettes):
        """
        Charge le modèle et les étiquettes
        
        Args:
            chemin_modele (str): Chemin vers le modèle entraîné
            chemin_etiquettes (str): Chemin vers les étiquettes des classes
        
        Returns:
            bool: True si le chargement a réussi, False sinon
        """
        try:
            # Vérification de l'existence des fichiers
            if not os.path.exists(chemin_modele) or not os.path.exists(chemin_etiquettes):
                print("Modèle ou étiquettes non trouvés")
                return False
            
            # Chargement du modèle
            self.modele = load_model(chemin_modele)
            
            # Chargement des étiquettes
            with open(chemin_etiquettes, 'rb') as f:
                self.etiquettes = pickle.load(f)
            
            # Extraction de la taille d'entrée du modèle
            input_shape = self.modele.input_shape
            if input_shape and len(input_shape) == 4:
                self.taille_image = (input_shape[1], input_shape[2])
            
            print(f"Modèle chargé avec succès. Classes: {self.etiquettes}")
            self.modele_charge = True
            return True
            
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            return False
    
    def predire(self, image):
        """
        Prédit la classe d'une image
        
        Args:
            image (ndarray): Image à classifier (format BGR de OpenCV)
        
        Returns:
            tuple: (nom_classe, confiance) ou (None, 0) en cas d'erreur
        """
        if not self.modele_charge:
            return "Pas de modèle", 0
        
        try:
            # Prétraitement de l'image
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_rgb, self.taille_image)
            img_normalized = img_resized / 255.0
            img_batch = np.expand_dims(img_normalized, axis=0)
            
            # Prédiction
            predictions = self.modele.predict(img_batch)[0]
            
            # Classe avec la plus haute probabilité
            classe_idx = np.argmax(predictions)
            confiance = predictions[classe_idx]
            
            # Conversion de l'index en nom de classe
            nom_classe = self.etiquettes.get(classe_idx, f"Classe_{classe_idx}")
            
            return nom_classe, confiance
            
        except Exception as e:
            print(f"Erreur lors de la prédiction: {e}")
            return "Erreur", 0
