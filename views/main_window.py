from PySide6.QtWidgets import (QMainWindow, QMessageBox,QWidget, QAbstractItemView, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, QPushButton,QTableWidgetItem)
from PySide6.QtCore import Qt
from models.enums import TaskState
from controllers.task_controller import TaskController
from views.add_task_dialog import AddTaskDialog
from views.edit_task_dialog import EditTaskDialog
from views.detail_task_dialog import DetailTaskDialog
from utils.date_format import format_datetime
from datetime import datetime
from typing import Optional


class MainWindow(QMainWindow):
    def __init__(self, controller: TaskController):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Gestionnaire de Tâches")
        self.resize(900, 520)

        # -- Widgets principaux --
        central = QWidget(self)
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        
        # Barre de filtres (par état)
        filter_bar = QHBoxLayout()
        filter_bar.addWidget(QLabel("Filtrer par état :"))
        self.state_filter = QComboBox()
        self.state_filter.addItem("Tous")
        for state in TaskState:
            self.state_filter.addItem(state.value)
        filter_bar.addWidget(self.state_filter)
        filter_bar.addStretch()
        layout.addLayout(filter_bar)

        # Tableau des tâches (liste)
        self.table = QTableWidget(0, 5, self)
        self.table.setHorizontalHeaderLabels(["ID","Titre", "État", "Date d'échéance", "Date de fin"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        

        # Barre d'actions CRUD
        actions = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.clicked.connect(self.open_add_dialog)

        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_close = QPushButton("Clôturer la tâche")
        self.btn_close.setObjectName("btn_close")
        actions.addWidget(self.btn_add)
        actions.addWidget(self.btn_edit)
        actions.addWidget(self.btn_delete)
        actions.addStretch()
        actions.addWidget(self.btn_close)
        layout.addLayout(actions)

        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_close.setEnabled(False)

        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self.btn_delete.clicked.connect(self.on_delete_clicked)
        self.btn_close.clicked.connect(self.on_close_clicked)
        self.btn_edit.clicked.connect(self.on_edit_clicked)

        #Signals
        self.state_filter.currentTextChanged.connect(self.refresh)

        self.refresh()

    # -- Helpers --
    def open_add_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():  
            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(self, "Erreur", "Le titre ne peut pas être vide.")
                return
        task = self.controller.create_task(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"]
        )
        QMessageBox.information(self, "Succès", f"Tâche '{task.title}' ajoutée.")
        self.refresh()

    def _selected_task_id(self) -> Optional[int]:
        sel = self.table.selectedItems()
        if not sel:
            return None
        # Colonne 0 = ID (assure-toi de ne pas réordonner les colonnes)
        try:
            return int(self.table.item(self.table.currentRow(), 0).text())
        except Exception:
            return None

    def _on_selection_changed(self, *_):
        has = self._selected_task_id() is not None
        self.btn_edit.setEnabled(has)
        self.btn_delete.setEnabled(has)
        self.btn_close.setEnabled(has)


    def on_delete_clicked(self):
        task_id = self._selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Info", "Sélectionne une tâche d’abord.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            "Es-tu sûr de vouloir supprimer cette tâche ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        ok = self.controller.delete_task(task_id)
        if ok:
            QMessageBox.information(self, "Supprimé", "La tâche a été supprimée.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de supprimer la tâche (introuvable).")

    def on_close_clicked(self):
        task_id = self._selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Info", "Sélectionne une tâche d’abord.")
            return

        reply = QMessageBox.question(
            self,
            "Clôturer la tâche",
            "Marquer cette tâche comme 'Réalisé' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        updated = self.controller.close_task(task_id)
        if updated:
            QMessageBox.information(self, "Clôturée", "La tâche est maintenant 'Réalisé'.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de clôturer la tâche (introuvable).")

    def on_edit_clicked(self):
        task_id = self._selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Info", "Sélectionne une tâche d’abord.")
            return

        task = self.controller.get_task(task_id)
        if not task:
            QMessageBox.warning(self, "Erreur", "Tâche introuvable.")
            return

        dlg = EditTaskDialog(task, self)
        if not dlg.exec():
            return

        data = dlg.get_result()
        if not data["title"]:
            QMessageBox.warning(self, "Erreur", "Le titre ne peut pas être vide.")
            return

        # Appliquer les champs modifiés
        task.title = data["title"]
        task.description = data["description"]

        # État
        # (le QComboBox renvoie la valeur texte, on retransforme en Enum)
        for s in TaskState:
            if s.value == data["state"]:
                task.state = s
                break

        # Échéance
        task.due_date = data["due_date"]

        # Logique end_date :
        # - si on passe à "Réalisé" et qu'il n'y a pas d'end_date => la fixer maintenant
        # - si on passe à un autre état => on peut vider end_date (pour "ré-ouvrir" une tâche)
        if task.state == TaskState.REALISE and not task.end_date:
            task.end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        elif task.state != TaskState.REALISE:
            task.end_date = None

        # Ajouter les nouveaux commentaires saisis dans le dialog
        for cdict in data["new_comments"]:
            # on passe par le modèle pour robustesse
            from models.task import Comment
            task.comments.append(Comment.from_dict(cdict))

        updated = self.controller.update_task(task)
        if updated:
            QMessageBox.information(self, "Modifié", "La tâche a été mise à jour.")
            self.refresh()
        else:
            QMessageBox.warning(self, "Erreur", "La mise à jour a échoué.")

    def on_row_double_clicked(self, _row: int, _col: int):
        task_id = self._selected_task_id()
        if task_id is None:
            return
        task = self.controller.get_task(task_id)
        if not task:
            QMessageBox.warning(self, "Erreur", "Tâche introuvable.")
            return
        
        #ouvre la fiche détail
        dlg = DetailTaskDialog(task, self)
        if dlg.exec() and dlg.want_edit:
            # L'utilisateur a cliqué "Modifier..."
            self.on_edit_clicked()
    
    def _current_filter(self) ->Optional[TaskState]:
        text = self.state_filter.currentText()
        if text == "Tous":
            return None
        for s in TaskState:
            if s.value == text:
                return s
        return None
    
    def refresh(self):
        state_filter = self._current_filter()
        tasks = self.controller.list_tasks(state_filter)
        self.table.setRowCount(len(tasks))

        for r, t in enumerate(tasks):
            self.table.setItem(r, 0, QTableWidgetItem(str(t.id)))
            self.table.setItem(r, 1, QTableWidgetItem(t.title))
            self.table.setItem(r, 2, QTableWidgetItem(t.state.value))
            self.table.setItem(r, 3, QTableWidgetItem(format_datetime(t.due_date) or ""))
            self.table.setItem(r, 4, QTableWidgetItem(format_datetime(t.end_date) or ""))
        self._on_selection_changed()