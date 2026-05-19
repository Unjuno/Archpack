# Taskflow commands

All commands run from `demo/workspace` after `pip install -e .`.

| Command | Description |
|---------|-------------|
| `taskflow add <title>` | Create an open task |
| `taskflow list` | Show all tasks with id, status, title |
| `taskflow done <id>` | Mark a task completed |
| `taskflow remove <id>` | Delete a task |

## Examples

```bash
python -m taskflow add "Draft architecture doc"
python -m taskflow add "Review agents.toml rules"
python -m taskflow list
python -m taskflow done 1
python -m taskflow remove 2
```

## Errors

Unknown task ids and empty titles raise `TaskflowError`; the CLI prints the message to stderr and exits with code 1.
