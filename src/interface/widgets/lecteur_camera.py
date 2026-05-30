# -*- coding: utf-8 -*-
"""
Module contenant le widget de capture et d'affichage de la caméra
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QImage, QPixmap, QIcon, QFont
from PySide6.QtCore import QTimer, Qt, Signal, QSize

import cv2
import numpy as np
import os

class LecteurCamera(QWidget):
    """
    Widget permettant d'afficher le flux vidéo d'une caméra
    """
    
    image_capturee = Signal(np.ndarray)  # Signal émis lorsqu'une image est capturée
    
    def __init__(self, camera_id=0, fps=30, parent=None):
        """
        Initialise le lecteur de caméra
        
        Args:
            camera_id (int): ID de la caméra à utiliser
            fps (int): Fréquence d'acquisition des images
            parent (QWidget, optionnel): Widget parent
        """
        super().__init__(parent)
        
        # Paramètres de la caméra
        self.camera_id = camera_id
        self.fps = fps
        self.camera = None
        self.timer = None
        self.current_frame = None
        self.rectangle_active = True
        self.rectangle_color = (0, 122, 204)  # Bleu
        self.rectangle_thickness = 2
        
        # État de la caméra
        self.camera_active = False
        
        # Création de l'interface
        self._creer_interface()
        
        # La caméra n'est pas démarrée automatiquement
    
    def _creer_interface(self):
        """Crée les composants de l'interface"""
        # Disposition principale
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Affichage du flux vidéo
        self.video_label = QLabel("Caméra arrêtée\nCliquez sur \"Démarrer caméra\" pour activer")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #0D1117;
                border: 1px solid #2B3648;
                border-radius: 8px;
                color: #FFFFFF;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.video_label)
        
        # Boutons de contrôle
        boutonsLayout = QHBoxLayout()
        boutonsLayout.setContentsMargins(10, 10, 10, 10)
        boutonsLayout.setSpacing(10)
        
        # Bouton pour démarrer/arrêter la caméra
        self.camera_btn = QPushButton("Démarrer caméra")
        self.camera_btn.setMinimumHeight(40)
        self.camera_btn.clicked.connect(self._toggle_camera)
        boutonsLayout.addWidget(self.camera_btn)
        
        # Bouton de capture
        self.capture_btn = QPushButton("Capturer")
        self.capture_btn.setIcon(QIcon(os.path.join("assets", "icons", "camera.svg")))
        self.capture_btn.setIconSize(QSize(20, 20))
        self.capture_btn.setMinimumHeight(40)
        self.capture_btn.clicked.connect(self._capturer_image)
        self.capture_btn.setEnabled(False)  # Désactivé tant que la caméra n'est pas démarrée
        boutonsLayout.addWidget(self.capture_btn)
        
        # Bouton pour activer/désactiver le rectangle
        self.rectangle_btn = QPushButton("Rectangle ON/OFF")
        self.rectangle_btn.setMinimumHeight(40)
        self.rectangle_btn.clicked.connect(self._toggle_rectangle)
        self.rectangle_btn.setEnabled(False)  # Désactivé tant que la caméra n'est pas démarrée
        boutonsLayout.addWidget(self.rectangle_btn)
        
        layout.addLayout(boutonsLayout)
    
    def _demarrer_camera(self):
        """Démarre la capture vidéo"""
        try:
            self.camera = cv2.VideoCapture(self.camera_id)
            if not self.camera.isOpened():
                self._afficher_erreur("Impossible d'accéder à la caméra")
                return
            
            # Définition des dimensions vidéo
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Timer pour la mise à jour du flux vidéo
            self.timer = QTimer(self)
            self.timer.timeout.connect(self._mise_a_jour_frame)
            self.timer.start(1000 // self.fps)
        except Exception as e:
            self._afficher_erreur(f"Erreur lors du démarrage de la caméra: {str(e)}")
    
    def _mise_a_jour_frame(self):
        """Met à jour l'affichage avec la dernière image de la caméra"""
        if self.camera is None or not self.camera.isOpened():
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Suppression de l'effet miroir
        frame = cv2.flip(frame, 1)
        
        # Stockage de la frame actuelle (non-miroir)
        self.current_frame = frame.copy()
        
        # Ajout d'un rectangle de capture si activé
        if self.rectangle_active:
            h, w = frame.shape[:2]
            x1, y1 = 50, 50
            x2, y2 = w - 50, h - 50
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.rectangle_color, self.rectangle_thickness)
        
        # Conversion BGR -> RGB pour Qt
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Conversion en QImage puis QPixmap
        h, w, ch = rgb_frame.shape
        img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        
        # Mise à jour de l'affichage
        self.video_label.setPixmap(pixmap)
    
    def _capturer_image(self):
        """Capture l'image actuelle et émet le signal"""
        if self.current_frame is not None:
            # Si le rectangle est actif, on ne capture que cette zone
            if self.rectangle_active:
                h, w = self.current_frame.shape[:2]
                x1, y1 = 50, 50
                x2, y2 = w - 50, h - 50
                roi = self.current_frame[y1:y2, x1:x2]
                self.image_capturee.emit(roi)
            else:
                self.image_capturee.emit(self.current_frame.copy())
    
    def _toggle_camera(self):
        """Démarre ou arrête la caméra"""
        if self.camera_active:
            # Arrêter la caméra
            self.arreter()
            self.camera_active = False
            self.camera_btn.setText("Démarrer caméra")
            self.capture_btn.setEnabled(False)
            self.rectangle_btn.setEnabled(False)
            # Afficher un message dans la zone vidéo
            self.video_label.setText("Caméra arrêtée")
            self.video_label.setStyleSheet("""
                QLabel {
                    background-color: #0D1117;
                    color: #FFFFFF;
                    border: 1px solid #2B3648;
                    border-radius: 8px;
                    font-size: 14px;
                }
            """)
        else:
            # Démarrer la caméra
            self._demarrer_camera()
            self.camera_active = True
            self.camera_btn.setText("Arrêter caméra")
            self.capture_btn.setEnabled(True)
            self.rectangle_btn.setEnabled(True)
    
    def _toggle_rectangle(self):
        """Active/désactive l'affichage du rectangle de capture"""
        self.rectangle_active = not self.rectangle_active
    
    def _afficher_erreur(self, message):
        """Affiche un message d'erreur à la place du flux vidéo"""
        self.video_label.setText(message)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: #0D1117;
                color: #E91E63;
                border: 1px solid #2B3648;
                border-radius: 8px;
                font-size: 14px;
            }
        """)
    
    def arreter(self):
        """Arrête la capture vidéo"""
        if self.timer is not None:
            self.timer.stop()
        
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
    
    def redemarrer(self):
        """Redémarre la capture vidéo"""
        self.arreter()
        self._demarrer_camera()
    
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre"""
        self.arreter()
        super().closeEvent(event)
