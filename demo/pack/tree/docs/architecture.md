# Taskflow architecture

## Purpose

Taskflow stores tasks in `.taskflow/tasks.json` (under the current working directory) and exposes a small CLI for add, list, mark-done, and remove operations.
This project is bundled as the Archpack `demo/pack` tree; it is not published separately.

## Layers

| Layer | Path | Responsibility |
|-------|------|----------------|
| CLI | `src/taskflow/cli.py` | argparse, stdout/stderr, exit codes |
| Domain | `src/taskflow/models.py` | `Task`, `TaskflowError` |
| Services | `src/taskflow/services/store.py` | `TaskStore` persistence API |

## Data flow

```text
CLI command → TaskStore → .taskflow/tasks.json → list[Task] → formatted table on stdout
```

## Agent guidance

Rules for AI assistants editing this repo are generated into `AGENTS.md` files.
Edit `demo/pack/agents.toml` at the Archpack repository root and regenerate; do not edit `AGENTS.md` by hand.
