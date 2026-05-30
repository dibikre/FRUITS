# -*- coding: utf-8 -*-
"""
Module contenant les fonctions de traitement d'images
"""

import cv2
import numpy as np

class TraitementImage:
    """
    Classe contenant des méthodes statiques pour le traitement d'images
    """
    
    @staticmethod
    def redimensionner(image, dimensions):
        """
        Redimensionne une image aux dimensions spécifiées
        
        Args:
            image (ndarray): Image à redimensionner
            dimensions (tuple): Nouvelles dimensions (largeur, hauteur)
        
        Returns:
            ndarray: Image redimensionnée
        """
        if image is None:
            return None
        
        try:
            return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        except Exception as e:
            print(f"Erreur lors du redimensionnement: {e}")
            return None
    
    @staticmethod
    def normaliser(image):
        """
        Normalise les valeurs des pixels entre 0 et 1
        
        Args:
            image (ndarray): Image à normaliser
        
        Returns:
            ndarray: Image normalisée
        """
        if image is None:
            return None
        
        try:
            return image.astype(np.float32) / 255.0
        except Exception as e:
            print(f"Erreur lors de la normalisation: {e}")
            return None
    
    @staticmethod
    def pretraiter_pour_modele(image, dimensions):
        """
        Prétraite une image pour l'entrée d'un modèle
        
        Args:
            image (ndarray): Image à prétraiter (format BGR de OpenCV)
            dimensions (tuple): Dimensions requises (largeur, hauteur)
        
        Returns:
            ndarray: Image prétraitée prête pour le modèle
        """
        if image is None:
            return None
        
        try:
            # Conversion BGR -> RGB
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Redimensionnement
            resized = TraitementImage.redimensionner(rgb, dimensions)
            
            # Normalisation
            normalized = TraitementImage.normaliser(resized)
            
            # Ajout de dimension pour le batch
            return np.expand_dims(normalized, axis=0)
            
        except Exception as e:
            print(f"Erreur lors du prétraitement: {e}")
            return None
    
    @staticmethod
    def ajouter_rectangle(image, x1, y1, x2, y2, couleur=(0, 255, 0), epaisseur=2):
        """
        Ajoute un rectangle à une image
        
        Args:
            image (ndarray): Image d'origine
            x1, y1 (int): Coordonnées du coin supérieur gauche
            x2, y2 (int): Coordonnées du coin inférieur droit
            couleur (tuple): Couleur BGR du rectangle
            epaisseur (int): Épaisseur du trait
        
        Returns:
            ndarray: Image avec le rectangle
        """
        if image is None:
            return None
        
        try:
            result = image.copy()
            cv2.rectangle(result, (x1, y1), (x2, y2), couleur, epaisseur)
            return result
        except Exception as e:
            print(f"Erreur lors de l'ajout du rectangle: {e}")
            return image
    
    @staticmethod
    def ajouter_texte(image, texte, x, y, couleur=(0, 255, 0), taille=0.8, epaisseur=2):
        """
        Ajoute du texte à une image
        
        Args:
            image (ndarray): Image d'origine
            texte (str): Texte à ajouter
            x, y (int): Coordonnées du texte
            couleur (tuple): Couleur BGR du texte
            taille (float): Taille du texte
            epaisseur (int): Épaisseur du texte
        
        Returns:
            ndarray: Image avec le texte
        """
        if image is None:
            return None
        
        try:
            result = image.copy()
            cv2.putText(
                result,
                texte,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                taille,
                couleur,
                epaisseur
            )
            return result
        except Exception as e:
            print(f"Erreur lors de l'ajout du texte: {e}")
            return image
    
    @staticmethod
    def appliquer_filtres(image, flou=False, contraste=False, luminosite=False):
        """
        Applique des filtres à l'image
        
        Args:
            image (ndarray): Image d'origine
            flou (bool): Appliquer un flou gaussien
            contraste (bool): Améliorer le contraste
            luminosite (bool): Ajuster la luminosité
        
        Returns:
            ndarray: Image filtrée
        """
        if image is None:
            return None
        
        result = image.copy()
        
        try:
            # Application des filtres
            if flou:
                result = cv2.GaussianBlur(result, (5, 5), 0)
            
            if contraste or luminosite:
                # Conversion en HSV pour ajuster la luminosité et le contraste
                hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                
                if contraste:
                    # Amélioration du contraste
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    v = clahe.apply(v)
                
                if luminosite:
                    # Ajustement de la luminosité (+20)
                    v = cv2.add(v, 20)
                    v = np.clip(v, 0, 255)
                
                hsv = cv2.merge([h, s, v])
                result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            return result
            
        except Exception as e:
            print(f"Erreur lors de l'application des filtres: {e}")
            return image
