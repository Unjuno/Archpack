# Archpack

Archpack is a small architecture-pack project.

The core MVP is intentionally narrow:

```text
pack directory → file tree
```

The first goal is to read a pack directory and generate the file structure stored under its `tree/` directory.

Features such as `AGENTS.md` generation, effective inherited agent instructions, drift checks, repair, clean-up, reference monitoring, and network monitoring are treated as plugin candidates or later experiments, not core MVP requirements.

This repository is currently in the specification phase. Implementation is intentionally deferred until the core scope and first pack format are fixed.

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

Plugin candidates:

- generate `AGENTS.md`
- generate effective inherited `AGENTS.md`
- audit generated files
- repair generated files
- clean generated files
- monitor references
- monitor network usage
