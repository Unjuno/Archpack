from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


class TaskflowError(Exception):
    """User-facing taskflow error."""


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    done: bool
    created_at: datetime

    @staticmethod
    def new(task_id: int, title: str) -> Task:
        title = title.strip()
        if not title:
            raise TaskflowError("Task title must not be empty")
        return Task(
            id=task_id,
            title=title,
            done=False,
            created_at=datetime.now(timezone.utc),
        )
