from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QListWidget, QAbstractItemView, QPushButton
)
from models.task import Task
from utils.date_format import format_datetime

class DetailTaskDialog(QDialog):
    """Mini fiche en lecture seule, avec un bouton modifier..."""
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Détails - Tâche #{task.id}")
        self.resize(520,520)
        self.want_edit = False # <- sera true si l'utilisateur clique sur modifier

        layout = QVBoxLayout(self)

        #Titre
        layout.addWidget(QLabel(f"<br>Titre :</br> {task.title}"))

        #État
        layout.addWidget(QLabel(f"<br>État :</br> {task.title}"))

        # Dates
        layout.addWidget(QLabel(f"<b>Créée le :</b> {format_datetime(task.created_at)}"))
        layout.addWidget(QLabel(f"<b>Mise à jour le :</b> {format_datetime(task.updated_at)}"))
        layout.addWidget(QLabel(f"<b>Échéance :</b> {format_datetime(task.due_date)}"))
        layout.addWidget(QLabel(f"<b>Date de fin :</b> {format_datetime(task.end_date)}"))

        #Description (lecture seule)
        layout.addWidget(QLabel("<b>Description :</b>"))
        desc = QTextEdit()
        desc.setReadOnly(True)
        desc.setPlainText(task.description or "")
        layout.addWidget(desc)

        # Commentaires (lecture seule)
        layout.addWidget(QLabel("<b>Commentaires :</b>"))
        self.comments_list = QListWidget()
        self.comments_list.setSelectionMode(QAbstractItemView.NoSelection)
        for c in task.comments:
            self.comments_list.addItem(f"[{format_datetime(c.created_at)}] {c.content}")
        layout.addWidget(self.comments_list)

        # Boutons
        row = QHBoxLayout()
        self.btn_edit = QPushButton("Modifier…")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_close = QPushButton("Fermer")
        self.btn_close.setObjectName("btn_cancel")
        row.addStretch()
        row.addWidget(self.btn_edit)
        row.addWidget(self.btn_close)
        layout.addLayout(row)

        # Actions
        self.btn_edit.clicked.connect(self._edit)
        self.btn_close.clicked.connect(self.reject)

    def _edit(self):
        self.want_edit = True
        self.accept()