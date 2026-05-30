# -*- coding: utf-8 -*-
"""
Module contenant le thème bleu-noir de l'application
"""

from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

def appliquer_theme_bleu_noir(app):
    """
    Applique le thème bleu-noir à l'application
    
    Args:
        app: L'instance de l'application QApplication
    """
    # Création de la palette de couleurs
    palette = QPalette()
    
    # Couleurs principales
    palette.setColor(QPalette.Window, QColor("#0D1117"))
    palette.setColor(QPalette.WindowText, QColor("#E1E1E1"))
    palette.setColor(QPalette.Base, QColor("#141D2B"))
    palette.setColor(QPalette.AlternateBase, QColor("#192133"))
    palette.setColor(QPalette.ToolTipBase, QColor("#0D1117"))
    palette.setColor(QPalette.ToolTipText, QColor("#E1E1E1"))
    
    # Couleurs pour les boutons
    palette.setColor(QPalette.Button, QColor("#1A2332"))
    palette.setColor(QPalette.ButtonText, QColor("#E1E1E1"))
    
    # Couleurs pour la sélection
    palette.setColor(QPalette.Highlight, QColor("#007ACC"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    
    # Couleurs pour les textes
    palette.setColor(QPalette.Text, QColor("#E1E1E1"))
    palette.setColor(QPalette.BrightText, QColor("#FFFFFF"))
    
    # Couleurs pour les liens
    palette.setColor(QPalette.Link, QColor("#00BFFF"))
    palette.setColor(QPalette.LinkVisited, QColor("#B88FFF"))
    
    # Application de la palette
    app.setPalette(palette)
    
    # Configuration de la police
    font = QFont("Montserrat", 10)
    app.setFont(font)
    
    # Applique la feuille de style personnalisée
    app.setStyleSheet("""
    QMainWindow, QDialog {
        background-color: #0D1117;
    }
    
    QWidget {
        background-color: transparent;
        color: #E1E1E1;
    }
    
    QLabel {
        color: #E1E1E1;
    }
    
    QPushButton {
        background-color: #1A2332;
        color: #E1E1E1;
        border: 1px solid #007ACC;
        border-radius: 4px;
        padding: 6px 12px;
        min-height: 30px;
    }
    
    QPushButton:hover {
        background-color: #007ACC;
        color: white;
    }
    
    QPushButton:pressed {
        background-color: #005F9E;
    }
    
    QPushButton:disabled {
        background-color: #1A2332;
        color: #7A7A7A;
        border: 1px solid #2B3648;
    }
    
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
        background-color: #141D2B;
        color: #E1E1E1;
        border: 1px solid #2B3648;
        border-radius: 4px;
        padding: 4px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #007ACC;
    }
    
    QComboBox {
        background-color: #141D2B;
        selection-background-color: #007ACC;
        selection-color: white;
    }
    
    QComboBox QAbstractItemView {
        background-color: #141D2B;
        selection-background-color: #007ACC;
    }
    
    QScrollBar:vertical {
        background-color: #141D2B;
        width: 14px;
        margin: 15px 0 15px 0;
        border-radius: 7px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #2B3648;
        min-height: 30px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #007ACC;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }
    
    QScrollBar:horizontal {
        background-color: #141D2B;
        height: 14px;
        margin: 0 15px 0 15px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #2B3648;
        min-width: 30px;
        border-radius: 7px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #007ACC;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        background: none;
    }
    
    QTabWidget::pane {
        border: 1px solid #2B3648;
        background-color: #141D2B;
    }
    
    QTabBar::tab {
        background-color: #1A2332;
        color: #E1E1E1;
        border: 1px solid #2B3648;
        padding: 6px 12px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    
    QTabBar::tab:selected {
        background-color: #007ACC;
        color: white;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #2B3648;
    }
    
    QProgressBar {
        border: 1px solid #2B3648;
        border-radius: 4px;
        background-color: #141D2B;
        text-align: center;
        color: white;
    }
    
    QProgressBar::chunk {
        background-color: #007ACC;
        border-radius: 3px;
    }
    
    QToolTip {
        background-color: #0D1117;
        color: #E1E1E1;
        border: 1px solid #007ACC;
        padding: 4px;
        opacity: 200;
    }
    
    QMenuBar {
        background-color: #0D1117;
        color: #E1E1E1;
    }
    
    QMenuBar::item:selected {
        background-color: #007ACC;
        color: white;
    }
    
    QMenu {
        background-color: #141D2B;
        color: #E1E1E1;
        border: 1px solid #2B3648;
    }
    
    QMenu::item:selected {
        background-color: #007ACC;
        color: white;
    }
    """)
