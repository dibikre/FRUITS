# -*- coding: utf-8 -*-
"""
Module contenant la classe de synthèse vocale
"""

import threading
import queue
import os
import time

class SyntheseVocale:
    """
    Classe gérant la synthèse vocale
    """
    
    def __init__(self):
        """Initialise le moteur de synthèse vocale"""
        self.engine = None
        self.voix_active = True
        self.file_messages = queue.Queue()
        self.thread_actif = False
        self.thread = None
        
        # Initialisation du moteur
        self._initialiser_moteur()
        
        # Démarrage du thread de traitement
        self._demarrer_thread()
    
    def _initialiser_moteur(self):
        """Initialise le moteur de synthèse vocale"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # Configuration du moteur
            self.engine.setProperty('rate', 180)  # Vitesse de parole
            
            # Sélection d'une voix française si disponible
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if "french" in voice.id.lower() or "fr" in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
        except Exception as e:
            print(f"Erreur lors de l'initialisation du moteur de synthèse vocale: {e}")
            self.engine = None
    
    def _demarrer_thread(self):
        """Démarre le thread de traitement des messages"""
        if self.thread_actif:
            return
        
        self.thread_actif = True
        self.thread = threading.Thread(target=self._traiter_messages, daemon=True)
        self.thread.start()
    
    def _traiter_messages(self):
        """Fonction exécutée par le thread pour traiter les messages"""
        while self.thread_actif:
            try:
                # Attente d'un message (timeout pour permettre l'arrêt du thread)
                try:
                    message = self.file_messages.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                # Traitement du message si le moteur est disponible et la voix active
                if self.engine is not None and self.voix_active:
                    self.engine.say(message)
                    self.engine.runAndWait()
                
                # Marquer le message comme traité
                self.file_messages.task_done()
                
            except Exception as e:
                print(f"Erreur dans le thread de synthèse vocale: {e}")
                time.sleep(1)  # Pause pour éviter une boucle d'erreurs
    
    def parler(self, texte):
        """
        Ajoute un message à la file de traitement
        
        Args:
            texte (str): Texte à prononcer
        """
        if not self.voix_active or self.engine is None:
            return
        
        # Ajout du message à la file
        self.file_messages.put(texte)
    
    def activer(self):
        """Active la synthèse vocale"""
        self.voix_active = True
    
    def desactiver(self):
        """Désactive la synthèse vocale"""
        self.voix_active = False
        
        # Vide la file de messages
        while not self.file_messages.empty():
            try:
                self.file_messages.get_nowait()
                self.file_messages.task_done()
            except queue.Empty:
                break
    
    def arreter(self):
        """Arrête le moteur de synthèse vocale"""
        self.desactiver()
        self.thread_actif = False
        
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
        
        if self.engine:
            self.engine.stop()
