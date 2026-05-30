# -*- coding: utf-8 -*-
"""
Module contenant la classe de gestion des données
"""

import os
import json
import shutil

from ..constantes import *

class GestionnaireDonnees:
    """
    Classe gérant les données de l'application
    """
    
    def __init__(self):
        """Initialise le gestionnaire de données"""
        # Création des dossiers nécessaires
        os.makedirs(DIRECTION_JSON_FRUITS, exist_ok=True)
        os.makedirs(DOSSIER_DATASET, exist_ok=True)
    
    def charger_config(self):
        """
        Charge la configuration de l'application
        
        Returns:
            dict: Configuration de l'application
        """
        try:
            with open(FICHIER_CONFIG, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            # Configuration par défaut
            return {
                "application": {
                    "nom": "Reconnaissance de Fruits",
                    "version": "1.0.0",
                    "langue": "fr_FR",
                    "theme": "bleu_noir",
                    "port_camera": 0
                },
                "modele": {
                    "taille_image": [64, 64],
                    "batch_size": 32,
                    "epochs": 20,
                    "validation_split": 0.2,
                    "chemin_modele": "donnees/modele_fruits.h5",
                    "chemin_etiquettes": "donnees/etiquettes.pkl"
                },
                "interface": {
                    "largeur": 1280,
                    "hauteur": 800,
                    "seuil_confiance": 0.7,
                    "delai_synthese_vocale": 3
                }
            }
    
    def sauvegarder_config(self, config):
        """
        Sauvegarde la configuration de l'application
        
        Args:
            config (dict): Configuration à sauvegarder
        
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        try:
            with open(FICHIER_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False
    
    def charger_fruits_info(self):
        """
        Charge les informations sur les fruits
        
        Returns:
            dict: Informations sur les fruits
        """
        try:
            with open(FICHIER_FRUITS_INFO, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des informations sur les fruits: {e}")
            return {"fruits": []}
    
    def obtenir_liste_fruits(self):
        """
        Obtient la liste des noms de fruits
        
        Returns:
            list: Liste des noms de fruits
        """
        fruits_info = self.charger_fruits_info()
        return [fruit["nom"] for fruit in fruits_info.get("fruits", [])]
    
    def obtenir_info_fruit(self, nom):
        """
        Obtient les informations sur un fruit spécifique
        
        Args:
            nom (str): Nom du fruit
        
        Returns:
            dict ou None: Informations sur le fruit ou None si non trouvé
        """
        fruits_info = self.charger_fruits_info()
        for fruit in fruits_info.get("fruits", []):
            if fruit["nom"] == nom:
                return fruit
        return None
    
    def compter_images_entrainement(self):
        """
        Compte le nombre d'images par classe dans le dataset
        
        Returns:
            dict: Dictionnaire {nom_fruit: nombre_images}
        """
        resultats = {}
        
        try:
            # Parcours des dossiers du dataset
            for dossier in os.listdir(DOSSIER_DATASET):
                chemin_dossier = os.path.join(DOSSIER_DATASET, dossier)
                if os.path.isdir(chemin_dossier):
                    # Compte les fichiers d'images
                    images = [f for f in os.listdir(chemin_dossier) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                    resultats[dossier] = len(images)
            
            return resultats
            
        except Exception as e:
            print(f"Erreur lors du comptage des images: {e}")
            return {}
    
    def supprimer_classe(self, nom_classe):
        """
        Supprime une classe du dataset
        
        Args:
            nom_classe (str): Nom de la classe à supprimer
        
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        try:
            chemin_classe = os.path.join(DOSSIER_DATASET, nom_classe)
            if os.path.exists(chemin_classe) and os.path.isdir(chemin_classe):
                shutil.rmtree(chemin_classe)
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la suppression de la classe: {e}")
            return False
    
    def sauvegarder_image(self, image, nom_classe, nom_fichier):
        """
        Sauvegarde une image dans une classe du dataset
        
        Args:
            image (ndarray): Image à sauvegarder
            nom_classe (str): Nom de la classe
            nom_fichier (str): Nom du fichier
        
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        try:
            import cv2
            
            # Création du dossier de la classe si nécessaire
            dossier_classe = os.path.join(DOSSIER_DATASET, nom_classe)
            os.makedirs(dossier_classe, exist_ok=True)
            
            # Chemin complet du fichier
            chemin_fichier = os.path.join(dossier_classe, nom_fichier)
            
            # Sauvegarde de l'image
            return cv2.imwrite(chemin_fichier, image)
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'image: {e}")
            return False

    def sauvegarder_fruits_info(self, fruits_info):
        """
        Sauvegarde les informations sur les fruits dans le fichier JSON
        
        Args:
            fruits_info (dict): Dictionnaire contenant la liste des fruits
        
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        try:
            with open(FICHIER_FRUITS_INFO, 'w', encoding='utf-8') as f:
                json.dump(fruits_info, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des informations sur les fruits: {e}")
            return False

