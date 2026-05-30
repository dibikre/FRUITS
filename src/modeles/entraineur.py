# -*- coding: utf-8 -*-
"""
Module contenant la classe d'entraînement du modèle de reconnaissance
"""

import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import Callback

from ..constantes import *

class CallbackProgression(Callback):
    """
    Callback pour suivre la progression de l'entraînement
    """
    
    def __init__(self, callback_fn=None):
        """
        Initialise le callback
        
        Args:
            callback_fn (function, optionnel): Fonction de callback pour la progression
        """
        super().__init__()
        self.callback_fn = callback_fn
    
    def on_epoch_end(self, epoch, logs=None):
        """
        Appelé à la fin de chaque époque
        
        Args:
            epoch (int): Numéro de l'époque
            logs (dict, optionnel): Logs de l'époque
        """
        if self.callback_fn and logs:
            self.callback_fn(
                epoch,
                self.params['epochs'],
                logs.get('loss', 0),
                logs.get('accuracy', 0)
            )

class Entraineur:
    """
    Classe responsable de l'entraînement du modèle de reconnaissance de fruits
    """
    
    def __init__(self):
        """Initialise l'entraineur"""
        # Création des dossiers nécessaires
        os.makedirs(DIRECTION_JSON_FRUITS, exist_ok=True)
        os.makedirs(DOSSIER_DATASET, exist_ok=True)
    
    def entrainer(self, taille_image=(64, 64), batch_size=32, epochs=20, 
                 validation_split=0.2, augmentation=None, progress_callback=None):
        """
        Entraîne un modèle de reconnaissance de fruits
        
        Args:
            taille_image (tuple): Dimensions des images d'entrée
            batch_size (int): Taille du batch
            epochs (int): Nombre d'époques d'entraînement
            validation_split (float): Proportion des données pour la validation
            augmentation (dict, optionnel): Paramètres d'augmentation des données
            progress_callback (function, optionnel): Fonction de callback pour la progression
        
        Returns:
            bool: True si l'entraînement a réussi, False sinon
        """
        try:
            # Vérification des données d'entraînement
            if not os.path.exists(DOSSIER_DATASET) or not os.listdir(DOSSIER_DATASET):
                print("Aucune donnée d'entraînement trouvée")
                return False
            
            # Configuration du générateur de données
            if augmentation:
                datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=augmentation.get("rotation_range", 0),
                    width_shift_range=augmentation.get("width_shift_range", 0),
                    height_shift_range=augmentation.get("height_shift_range", 0),
                    shear_range=augmentation.get("shear_range", 0),
                    zoom_range=augmentation.get("zoom_range", 0),
                    horizontal_flip=augmentation.get("horizontal_flip", False),
                    validation_split=validation_split
                )
            else:
                datagen = ImageDataGenerator(
                    rescale=1./255,
                    validation_split=validation_split
                )
            
            # Générateur d'entraînement
            print("Chargement des données d'entraînement...")
            train_generator = datagen.flow_from_directory(
                DOSSIER_DATASET,
                target_size=taille_image,
                batch_size=batch_size,
                class_mode='categorical',
                subset='training'
            )
            
            # Générateur de validation
            validation_generator = datagen.flow_from_directory(
                DOSSIER_DATASET,
                target_size=taille_image,
                batch_size=batch_size,
                class_mode='categorical',
                subset='validation'
            )
            
            # Sauvegarde des étiquettes (mapping classe -> index)
            class_indices = train_generator.class_indices
            labels = {v: k for k, v in class_indices.items()}
            with open(FICHIER_ETIQUETTES, 'wb') as f:
                pickle.dump(labels, f)
            
            print(f"Classes détectées: {train_generator.class_indices}")
            print(f"Entraînement sur {train_generator.samples} images")
            print(f"Validation sur {validation_generator.samples} images")
            
            # Création du modèle
            model = self._creer_modele(taille_image, len(class_indices))
            
            # Callback pour suivre la progression
            callbacks = []
            if progress_callback:
                callbacks.append(CallbackProgression(progress_callback))
            
            # Entraînement du modèle
            print("Démarrage de l'entraînement...")
            model.fit(
                train_generator,
                steps_per_epoch=train_generator.samples // batch_size,
                validation_data=validation_generator,
                validation_steps=validation_generator.samples // batch_size,
                epochs=epochs,
                callbacks=callbacks
            )
            
            # Sauvegarde du modèle
            print(f"Sauvegarde du modèle dans {FICHIER_MODELE}")
            model.save(FICHIER_MODELE)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'entraînement: {e}")
            return False
    
    def _creer_modele(self, taille_image, nb_classes):
        """
        Crée un modèle CNN pour la classification d'images
        
        Args:
            taille_image (tuple): Dimensions des images d'entrée
            nb_classes (int): Nombre de classes à prédire
        
        Returns:
            Model: Modèle Keras
        """
        model = Sequential([
            # Première couche de convolution
            Conv2D(32, (3, 3), activation='relu', input_shape=(taille_image[0], taille_image[1], 3)),
            MaxPooling2D(2, 2),
            
            # Deuxième couche de convolution
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            
            # Troisième couche de convolution
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            
            # Dropout pour éviter le surapprentissage
            Dropout(0.5),
            
            # Couches denses
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(nb_classes, activation='softmax')
        ])
        
        # Compilation du modèle
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
