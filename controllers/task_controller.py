# controllers/task_controller.py
from typing import List, Optional
from models.repository_json import JsonTaskRepository
from models.task import Task, Comment
from models.enums import TaskState
from datetime import datetime

ISO = "%Y-%m-%dT%H:%M:%S"

class TaskController:
    def __init__(self, repo: Optional[JsonTaskRepository] = None):
        self.repo = repo or JsonTaskRepository()

    def list_tasks(self, state_filter: Optional[TaskState] = None) -> List[Task]:
        tasks = self.repo.all()
        if state_filter:
            return [t for t in tasks if t.state == state_filter]
        return tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.repo.get(task_id)

    def create_task(self, title: str, description: str = "", due_date: Optional[str] = None) -> Task:
        task = Task(id=0, title=title, description=description, due_date=due_date)
        return self.repo.add(task)

    def update_task(self, task: Task) -> Optional[Task]:
        return self.repo.update(task)

    def delete_task(self, task_id: int) -> bool:
        return self.repo.delete(task_id)

    def close_task(self, task_id: int) -> Optional[Task]:
        return self.repo.close(task_id)

    def add_comment(self, task_id: int, content: str) -> Optional[Task]:
        t = self.repo.get(task_id)
        if not t:
            return None
        t.comments.append(Comment(content=content, created_at=datetime.now().strftime(ISO)))
        return self.repo.update(t)
