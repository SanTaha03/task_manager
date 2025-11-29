# models/task.py
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
from models.enums import TaskState

ISO = "%Y-%m-%dT%H:%M:%S"

@dataclass
class Comment:
    content: str
    created_at: str = datetime.now().strftime(ISO)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Comment":
        if not isinstance(d, dict):
            return Comment(content=str(d))
        return Comment(
            content=d.get("content", ""),
            created_at=d.get("created_at", datetime.now().strftime(ISO)),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    state: TaskState = TaskState.A_FAIRE
    created_at: str = datetime.now().strftime(ISO)
    updated_at: str = datetime.now().strftime(ISO)
    due_date: Optional[str] = None
    end_date: Optional[str] = None
    comments: List[Comment] = field(default_factory=list)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Task":
        if not isinstance(d, dict):
            raise ValueError("Entrée de tâche invalide (pas un dict).")

        comments_raw = d.get("comments") or []
        if isinstance(comments_raw, dict):
            comments_raw = list(comments_raw.values())
        comments = [Comment.from_dict(c) for c in comments_raw if c is not None]

        state_val = d.get("state") or TaskState.A_FAIRE.value
        try:
            state = TaskState(state_val)
        except ValueError:
            state = TaskState.A_FAIRE

        # id manquant → 0 (utile si on veut “réparer” plus tard)
        task_id = int(d.get("id", 0))

        return Task(
            id=task_id,
            title=d.get("title", ""),
            description=d.get("description", ""),
            state=state,
            created_at=d.get("created_at", datetime.now().strftime(ISO)),
            updated_at=d.get("updated_at", datetime.now().strftime(ISO)),
            due_date=d.get("due_date"),
            end_date=d.get("end_date"),
            comments=comments
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        data["comments"] = [c.to_dict() for c in self.comments]
        return data
