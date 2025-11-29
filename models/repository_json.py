import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from models.task import Task
from models.enums import TaskState

ISO = "%Y-%m-%dT%H:%M:%S"

class JsonTaskRepository:
    def __init__(self, path: str = "data/tasks.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"tasks": []})

    # --- Internes
    def _read(self) -> dict:
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _next_id(self, tasks: List[Task]) -> int:
        return (max((t.id for t in tasks), default=0) + 1)

    # --- API
    def all(self) -> List[Task]:
        raw = self._read()
        items = raw.get("tasks", []) or []
        # Si c'est un dict (mauvais format), on prend ses valeurs
        if isinstance(items, dict):
            print("[WARN] 'tasks' est un dict, conversion en liste de valeurs.")
            items = list(items.values())
        if not isinstance(items, list):
            print("[WARN] 'tasks' n'est pas une liste, réinitialisé.")
            items = []
        tasks: List[Task] = []
        for i, it in enumerate(items):
            if not isinstance(it, dict):
                print(f"[WARN] Entrée #{i} ignorée (non-dict): {it!r}")
                continue
            try:
                tasks.append(Task.from_dict(it))
            except Exception as e:
                print(f"[WARN] Entrée #{i} ignorée (parse): {e} ; data={it!r}")
        return tasks
        
    def get(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.all() if t.id == task_id), None)

    def add(self, task: Task) -> Task:
        tasks = self.all()
        if task.id == 0:
            task.id = self._next_id(tasks)
        now = datetime.now().strftime(ISO)
        task.created_at = now
        task.updated_at = now
        tasks.append(task)
        self._write({"tasks": [t.to_dict() for t in tasks]})
        return task

    def update(self, task: Task) -> Optional[Task]:
        tasks = self.all()
        for i, t in enumerate(tasks):
            if t.id == task.id:
                task.updated_at = datetime.now().strftime(ISO)
                tasks[i] = task
                self._write({"tasks": [x.to_dict() for x in tasks]})
                return task
        return None

    def delete(self, task_id: int) -> bool:
        tasks = self.all()
        new_tasks = [t for t in tasks if t.id != task_id]
        if len(new_tasks) == len(tasks):
            return False
        self._write({"tasks": [t.to_dict() for t in new_tasks]})
        return True

    def close(self, task_id: int) -> Optional[Task]:
        t = self.get(task_id)
        if not t:
            return None
        t.state = TaskState.REALISE
        t.end_date = datetime.now().strftime(ISO)
        return self.update(t)
