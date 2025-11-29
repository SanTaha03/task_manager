"""Module pour gérer les styles modernes de l'application."""

from pathlib import Path
from PySide6.QtWidgets import QApplication


def load_modern_style(app: QApplication):
    """Charge et applique le stylesheet moderne à l'application.
    
    Args:
        app: L'instance QApplication
    """
    style_path = Path(__file__).parent.parent / "styles" / "modern_style.qss"
    
    if not style_path.exists():
        print(f"Avertissement: Fichier de style non trouvé: {style_path}")
        return
    
    with open(style_path, "r", encoding="utf-8") as f:
        stylesheet = f.read()
    
    app.setStyleSheet(stylesheet)
