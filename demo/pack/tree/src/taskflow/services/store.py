from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from taskflow.models import Task, TaskflowError


class TaskStore:
    """File-backed task storage for the demo application."""

    def __init__(self, data_file: Path | None = None) -> None:
        self._path = data_file or Path.cwd() / ".taskflow" / "tasks.json"
        self._tasks: list[Task] = []
        self._next_id = 1
        self._load()

    def add(self, title: str) -> Task:
        task = Task.new(self._next_id, title)
        self._next_id += 1
        self._tasks.append(task)
        self._save()
        return task

    def list(self) -> list[Task]:
        return sorted(self._tasks, key=lambda task: task.created_at)

    def get(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskflowError(f"Unknown task id: {task_id}")

    def mark_done(self, task_id: int) -> Task:
        task = self.get(task_id)
        if task.done:
            raise TaskflowError(f"Task {task_id} is already done")
        replaced = Task(
            id=task.id,
            title=task.title,
            done=True,
            created_at=task.created_at,
        )
        self._replace(replaced)
        self._save()
        return replaced

    def remove(self, task_id: int) -> None:
        before = len(self._tasks)
        self._tasks = [task for task in self._tasks if task.id != task_id]
        if len(self._tasks) == before:
            raise TaskflowError(f"Unknown task id: {task_id}")
        self._save()

    def _replace(self, updated: Task) -> None:
        self._tasks = [updated if task.id == updated.id else task for task in self._tasks]

    def _load(self) -> None:
        if not self._path.exists():
            return
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        self._next_id = int(raw["next_id"])
        self._tasks = [self._task_from_dict(item) for item in raw["tasks"]]

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "next_id": self._next_id,
            "tasks": [self._task_to_dict(task) for task in self._tasks],
        }
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @staticmethod
    def _task_to_dict(task: Task) -> dict[str, object]:
        return {
            "id": task.id,
            "title": task.title,
            "done": task.done,
            "created_at": task.created_at.isoformat(),
        }

    @staticmethod
    def _task_from_dict(data: dict[str, object]) -> Task:
        return Task(
            id=int(data["id"]),  # type: ignore[arg-type]
            title=str(data["title"]),
            done=bool(data["done"]),
            created_at=datetime.fromisoformat(str(data["created_at"])),
        )
