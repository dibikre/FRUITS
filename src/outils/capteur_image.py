# -*- coding: utf-8 -*-
"""
Module contenant la classe de capture d'images
"""

import os
import cv2
import numpy as np

from ..constantes import *

class CapteurImage:
    """
    Classe gérant la capture d'images pour l'entraînement
    """
    
    def __init__(self, camera_id=0):
        """
        Initialise le capteur d'images
        
        Args:
            camera_id (int): ID de la caméra à utiliser
        """
        self.camera_id = camera_id
        self.camera = None
        self.dimensions_capture = (640, 480)
        self.zone_interet = (50, 50, 550, 400)  # x1, y1, x2, y2
    
    def initialiser_camera(self):
        """
        Initialise la caméra
        
        Returns:
            bool: True si l'initialisation a réussi, False sinon
        """
        try:
            self.camera = cv2.VideoCapture(self.camera_id)
            if not self.camera.isOpened():
                print("Impossible d'accéder à la caméra")
                return False
            
            # Configuration des dimensions
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.dimensions_capture[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.dimensions_capture[1])
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la caméra: {e}")
            return False
    
    def liberer_camera(self):
        """Libère les ressources de la caméra"""
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
    
    def capturer_image(self):
        """
        Capture une image depuis la caméra
        
        Returns:
            ndarray ou None: Image capturée ou None en cas d'erreur
        """
        if self.camera is None:
            if not self.initialiser_camera():
                return None
        
        try:
            # Capture de l'image
            ret, frame = self.camera.read()
            if not ret:
                print("Erreur lors de la capture")
                return None
            
            return frame
            
        except Exception as e:
            print(f"Erreur lors de la capture d'image: {e}")
            return None
    
    def capturer_zone_interet(self):
        """
        Capture uniquement la zone d'intérêt (rectangle de capture)
        
        Returns:
            ndarray ou None: Zone d'intérêt de l'image ou None en cas d'erreur
        """
        frame = self.capturer_image()
        if frame is None:
            return None
        
        try:
            # Extraction de la zone d'intérêt
            x1, y1, x2, y2 = self.zone_interet
            roi = frame[y1:y2, x1:x2]
            return roi
            
        except Exception as e:
            print(f"Erreur lors de l'extraction de la zone d'intérêt: {e}")
            return None
    
    def enregistrer_image(self, image, dossier, nom_fichier):
        """
        Enregistre une image dans un dossier
        
        Args:
            image (ndarray): Image à enregistrer
            dossier (str): Dossier de destination
            nom_fichier (str): Nom du fichier
        
        Returns:
            bool: True si l'enregistrement a réussi, False sinon
        """
        if image is None:
            return False
        
        try:
            # Création du dossier si nécessaire
            os.makedirs(dossier, exist_ok=True)
            
            # Chemin complet du fichier
            chemin_fichier = os.path.join(dossier, nom_fichier)
            
            # Enregistrement de l'image
            cv2.imwrite(chemin_fichier, image)
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'image: {e}")
            return False
    
    def demarrer_session_capture(self, fruit, nombre_images, callback=None):
        """
        Démarre une session de capture automatique
        
        Args:
            fruit (str): Nom du fruit à capturer
            nombre_images (int): Nombre d'images à capturer
            callback (function, optionnel): Fonction appelée après chaque capture
        
        Returns:
            bool: True si la session a réussi, False sinon
        """
        if not self.initialiser_camera():
            return False
        
        dossier_fruit = os.path.join(DOSSIER_DATASET, fruit)
        os.makedirs(dossier_fruit, exist_ok=True)
        
        try:
            count = 0
            while count < nombre_images:
                # Capture de l'image
                roi = self.capturer_zone_interet()
                if roi is None:
                    continue
                
                # Enregistrement de l'image
                nom_fichier = f"{count+1}.jpg"
                if self.enregistrer_image(roi, dossier_fruit, nom_fichier):
                    count += 1
                    
                    # Appel du callback si fourni
                    if callback:
                        continuer = callback(count, nombre_images, roi)
                        if not continuer:
                            break
                
                # Pause entre les captures
                cv2.waitKey(500)  # 500ms entre chaque capture
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de la session de capture: {e}")
            return False
        
        finally:
            self.liberer_camera()
