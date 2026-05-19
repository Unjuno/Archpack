from __future__ import annotations

import argparse
import sys

from taskflow.models import Task, TaskflowError
from taskflow.services import TaskStore

_STORE = TaskStore()


def _format_task(task: Task) -> str:
    status = "done" if task.done else "open"
    return f"{task.id:>3}  [{status:^4}]  {task.title}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskflow", description="Local task-list CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a task")
    add_p.add_argument("title", help="Task title")

    sub.add_parser("list", help="List tasks")

    done_p = sub.add_parser("done", help="Mark a task done")
    done_p.add_argument("id", type=int, help="Task id")

    rm_p = sub.add_parser("remove", help="Remove a task")
    rm_p.add_argument("id", type=int, help="Task id")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "add":
            task = _STORE.add(args.title)
            print(f"added: {task.id} {task.title}")
        elif args.command == "list":
            tasks = _STORE.list()
            if not tasks:
                print("No tasks.")
            else:
                for task in tasks:
                    print(_format_task(task))
        elif args.command == "done":
            task = _STORE.mark_done(args.id)
            print(f"completed: {task.id} {task.title}")
        elif args.command == "remove":
            _STORE.remove(args.id)
            print(f"removed: {args.id}")
        else:
            return 2
    except TaskflowError as exc:
        print(f"taskflow: error: {exc}", file=sys.stderr)
        return 1
    return 0
