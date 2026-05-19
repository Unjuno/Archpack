# Archpack roadmap

## 0. Purpose

This roadmap describes what Archpack should become, step by step.

It is not an implementation spec, command reference, or finalized schema.

Archpack should first prove one small core loop:

```text
pack directory → file tree
```

Everything else should be treated as a plugin candidate until the core is stable.

---

## 1. Core MVP: file structure generator

### Goal

Prepare one pack directory and generate a project file structure from its `tree/` directory.

The pack directory should contain the files to generate as real files and folders.

Example:

```text
architecture-pack/
└─ tree/
   ├─ README.md
   ├─ docs/
   │  └─ architecture.md
   └─ src/
      └─ app.py
```

### Why

The first value is reproducible structure generation.

Instead of manually splitting one architecture document into many files, Archpack should create those files directly from a directory pack.

### Success state

A user can prepare a pack directory, run Archpack, and obtain the described file tree.

### Undecided

- Command names and arguments.
- Overwrite policy.
- Whether metadata is needed at all.
- Generated marker policy.

---

## 2. Plugin direction

Archpack should not add every useful capability into the core.

The core should stay small:

```text
read pack directory → generate file tree
```

Additional behavior should be explored as plugins or plugin-like experiments.

This keeps the release body understandable even if many experiments are created.

---

## 3. First plugin candidate: AGENTS.md generation

### Goal

Generate `AGENTS.md` files from plugin-defined local rules.

A project root `AGENTS.md` is expected.
Additional `AGENTS.md` files can be generated in selected subdirectories.

Example:

```text
project/
├─ AGENTS.md
├─ src/
│  ├─ AGENTS.md
│  └─ services/
│     ├─ AGENTS.md
│     └─ auth/
│        ├─ AGENTS.md
│        └─ password_service.py
└─ docs/
   ├─ AGENTS.md
   └─ architecture.md
```

### Why

A single root `AGENTS.md` becomes too broad.

Directory-level files separate responsibilities:

- root: project-wide constraints,
- first-level directories: major area rules,
- deeper directories: local operational rules.

### Writing policy

- Use bullet points.
- Prefer one rule per line.
- Avoid long paragraphs.
- Keep local rule blocks short.
- Use 50 lines as a rough upper limit.

---

## 4. Second plugin candidate: effective AGENTS.md

### Goal

Generate lower-level `AGENTS.md` files as effective instruction files:

```text
parent rules + local rules = effective AGENTS.md
```

This makes inherited constraints explicit where the agent is likely to read them.

### Example

Root local rules:

```md
- Do not add external network calls unless explicitly allowed.
- Do not store secrets in source files.
```

`src/` local rules:

```md
- Keep application logic inside `src/`.
```

`src/services/` local rules:

```md
- Put business rules in service modules.
```

`src/services/auth/` local rules:

```md
- Do not bypass authentication checks.
- Add tests when changing authentication behavior.
```

Generated `src/services/auth/AGENTS.md`:

```md
- Do not add external network calls unless explicitly allowed.
- Do not store secrets in source files.
- Keep application logic inside `src/`.
- Put business rules in service modules.
- Do not bypass authentication checks.
- Add tests when changing authentication behavior.
```

### Undecided

- How to detect child rules that weaken parent rules.
- Whether to include inherited/local section headers.
- Whether to collapse duplicate rules.
- Whether effective files need a separate hard line limit.

---

## 5. Development sequence

The sequence should be:

```text
1. Build core directory-pack file tree generator.
2. Validate the core with small pack directories.
3. Define a minimal plugin boundary only after the core works.
4. Try AGENTS.md generation as the first plugin.
5. Try effective AGENTS.md generation as a second plugin or extension.
6. Promote only useful, reviewable plugin behavior into the release body.
```

The core MVP must not depend on the AGENTS.md plugin.

---

## 6. Deferred candidates

These are useful but not confirmed for the core.

They should be considered only after core MVP use reveals concrete problems.

- AGENTS.md generation.
- Effective AGENTS.md generation.
- Generated-file drift check.
- Repair.
- Clean-up.
- Reference monitoring.
- Network monitoring.
- Semantic architecture drift checks.
- File-level `*.agent.md`.
- Formal schema validation.
- CI integration.

---

## 7. Discipline

Do not expand the core before the small loop works.

First prove:

```text
pack directory → file tree
```

Then test additional capabilities as plugins.

Only promote plugin behavior when it solves a concrete problem without making the core harder to explain.
