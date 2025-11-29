# views/edit_task_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit,
    QComboBox, QListWidget, QAbstractItemView, QPushButton
)
from PySide6.QtCore import QDate
from typing import List, Dict, Any
from models.enums import TaskState
from models.task import Task, Comment
from utils.date_format import format_datetime
from datetime import datetime

ISO = "%Y-%m-%dT%H:%M:%S"

class EditTaskDialog(QDialog):
    def __init__(self, task: Task, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Modifier la tâche #{task.id}")
        self.resize(480, 520)
        self.task = task
        self._new_comments: List[Comment] = []

        layout = QVBoxLayout(self)

        # Titre
        layout.addWidget(QLabel("Titre :"))
        self.title_input = QLineEdit(task.title)
        layout.addWidget(self.title_input)

        # Description
        layout.addWidget(QLabel("Description :"))
        self.desc_input = QTextEdit(task.description)
        layout.addWidget(self.desc_input)

        # État
        layout.addWidget(QLabel("État :"))
        self.state_input = QComboBox()
        for s in TaskState:
            self.state_input.addItem(s.value)
        # positionner sur l'état courant
        self.state_input.setCurrentText(task.state.value)
        layout.addWidget(self.state_input)

        # Échéance
        layout.addWidget(QLabel("Date d’échéance (facultative) :"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if task.due_date:
            y, m, d = map(int, task.due_date[:10].split("-"))
            self.date_input.setDate(QDate(y, m, d))
        else:
            self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Commentaires existants
        layout.addWidget(QLabel("Commentaires :"))
        self.comments_list = QListWidget()
        self.comments_list.setSelectionMode(QAbstractItemView.NoSelection)
        for c in task.comments:
            self.comments_list.addItem(f"[{format_datetime(c.created_at)}] {c.content}")
        layout.addWidget(self.comments_list)

        # Ajouter un commentaire
        layout.addWidget(QLabel("Ajouter un commentaire :"))
        self.new_comment_input = QLineEdit()
        layout.addWidget(self.new_comment_input)
        btn_row = QHBoxLayout()
        self.btn_add_comment = QPushButton("Ajouter le commentaire")
        self.btn_add_comment.setObjectName("btn_add_comment")
        btn_row.addStretch()
        btn_row.addWidget(self.btn_add_comment)
        layout.addLayout(btn_row)

        # Boutons bas
        actions = QHBoxLayout()
        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.setObjectName("btn_save")
        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.setObjectName("btn_cancel")
        actions.addStretch()
        actions.addWidget(self.btn_save)
        actions.addWidget(self.btn_cancel)
        layout.addLayout(actions)

        # Signals
        self.btn_add_comment.clicked.connect(self._append_comment)
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def _append_comment(self):
        txt = self.new_comment_input.text().strip()
        if not txt:
            return
        now = datetime.now().strftime(ISO)
        c = Comment(content=txt, created_at=now)
        self._new_comments.append(c)
        self.comments_list.addItem(f"[{now}] {txt}")
        self.new_comment_input.clear()

    def get_result(self) -> Dict[str, Any]:
        # Formater la date en ISO complet : YYYY-MM-DDTHH:MM:SS
        due_date_str = self.date_input.date().toString("yyyy-MM-dd")
        due = f"{due_date_str}T00:00:00"
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "state": self.state_input.currentText(),
            "due_date": due,
            "new_comments": [c.to_dict() for c in self._new_comments],
        }
