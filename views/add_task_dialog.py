from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit,QPushButton)
from PySide6.QtCore import QDate

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une tâche")
        self.resize(400,300)

        layout = QVBoxLayout(self)

        # titre
        layout.addWidget(QLabel("Titre :"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        # description
        layout.addWidget(QLabel("Description :"))
        self.desc_input = QTextEdit()
        layout.addWidget(self.desc_input)

        # date
        layout.addWidget(QLabel("Date d’échéance (facultative) :"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # boutons
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Enregistrer")
        self.btn_ok.setObjectName("btn_save")
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.setObjectName("btn_cancel")
        btns.addStretch()
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        # connexions
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_data(self):
        """Renvoie les valeurs saisie dans un dict."""
        # Formater la date en ISO complet : YYYY-MM-DDTHH:MM:SS
        due_date_str = self.date_input.date().toString("yyyy-MM-dd")
        due_date = f"{due_date_str}T00:00:00"
        return {
            "title" : self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "due_date": due_date
        }
    