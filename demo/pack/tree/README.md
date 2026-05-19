# Taskflow (Archpack demo workspace)

Taskflow is a minimal task-list CLI used to demonstrate Archpack packs.

## Setup

From the Archpack repository root, deploy this tree:

```bash
archpack unpack demo/pack --out demo/workspace
archpack agents-generate demo/pack --out demo/workspace
```

Then run:

```bash
cd demo/workspace
python -m pip install -e .
python -m taskflow add "Write docs"
python -m taskflow list
```

## Agent rules

`AGENTS.md` files in this tree are generated from `demo/pack/agents.toml`.
Each directory's file includes parent rules (effective generation).

## Layout

```text
src/taskflow/       CLI and domain models
src/taskflow/services/  in-memory store
docs/               architecture and command reference
```
