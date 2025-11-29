from PySide6.QtWidgets import QApplication
from controllers.task_controller import TaskController
from views.main_window import MainWindow
from utils.style_manager import load_modern_style

import sys

def main():
    app = QApplication(sys.argv)
    # Appliquer le style moderne
    load_modern_style(app)
    controller = TaskController()
    window = MainWindow(controller = controller)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
