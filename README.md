# Archpack

Archpack is a small architecture-pack project.

The core MVP is intentionally narrow:

```text
pack directory → file tree → explicit repair
```

The first goal is to read a pack directory and generate the file structure stored under its `tree/` directory.

The MVP includes an explicit repair operation that restores generated files from the same pack directory when the output tree is damaged. This is not continuous enforcement or live monitoring.

Features such as `AGENTS.md` generation, effective inherited agent instructions, drift checks, clean-up, reference monitoring, and network monitoring are treated as plugin candidates or later experiments, not core MVP requirements.

## Usage

Install for local development:

```bash
python -m pip install -e ".[dev]"
```

Generate files from a pack directory:

```bash
archpack unpack examples/minimal-pack --out tmp/out
```

Repair missing generated files from the same pack directory:

```bash
archpack repair examples/minimal-pack --out tmp/out
```

Overwrite changed files only when explicitly requested:

```bash
archpack repair examples/minimal-pack --out tmp/out --overwrite
```

## Current documents

- `docs/roadmap.md` — staged project direction
- `docs/format.md` — current core pack format notes
- `docs/plugin-model.md` — core/plugin separation
- `docs/user-story-map.md` — post-MVP problem collection flow
- `docs/experiment-policy.md` — one-feature experiment and promotion policy

## Current core boundary

Core:

- read a pack directory
- read files under `tree/`
- generate directories
- generate files
- write file contents
- explicitly repair generated files from the pack when requested

Core does not:

- continuously enforce the structure
- monitor the project in the background
- auto-repair without an explicit user action

Plugin candidates:

- generate `AGENTS.md`
- generate effective inherited `AGENTS.md`
- audit generated files
- clean generated files
- monitor references
- monitor network usage
