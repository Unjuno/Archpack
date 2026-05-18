# Archpack roadmap

## 0. Purpose

This roadmap describes what Archpack should become, step by step.

It is not an implementation spec, command reference, or finalized schema.

Archpack should first prove one small loop:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

Anything beyond that stays deferred until real use shows a concrete need.

---

## 1. Stage 1: generate a file tree

### Goal

Write one pack file and generate a project file structure from it.

The pack should describe:

- directories,
- files,
- file contents.

### Why

The first value is reproducible structure generation.

Instead of manually splitting one architecture document into many files, Archpack should create those files directly.

### Undecided

- Exact pack schema.
- Command names and arguments.
- Overwrite policy.
- Generated marker policy.

---

## 2. Stage 2: generate AGENTS.md in selected directories

### Goal

Generate `AGENTS.md` at the project root and selected subdirectories.

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
├─ lab/
│  ├─ AGENTS.md
│  ├─ index.html
│  ├─ style.css
│  └─ app.js
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

## 3. Stage 3: generate effective AGENTS.md

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

## 4. Stage 4: prove the smallest useful loop

### Goal

Demonstrate the loop with a small example pack:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

The example should include at least three levels, such as:

```text
project → src → services → auth
```

### Success state

A reader can inspect the pack and generated output and understand:

- what files were generated,
- where `AGENTS.md` was placed,
- how inherited rules accumulated,
- why responsibility is separated by directory.

---

## 5. Stage 5: document the first stable format

### Goal

After the smallest loop works, document only the fields that are actually used.

### Why

The schema should follow the working concept.

Writing a large schema first would create fake precision.

---

## 6. Deferred candidates

These are useful but not confirmed for the first version.

They should be considered only after MVP use reveals concrete problems.

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

Do not expand the roadmap before the small loop works.

First prove:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

Then collect user problems with the user story map and decide the next feature.
