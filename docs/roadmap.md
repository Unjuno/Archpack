# Archpack creation roadmap

## 0. Position of this document

This document defines the creation roadmap before implementation.

The goal is not to implement everything at once. The goal is to define a staged path from a minimal file-structure generator to an architecture-control tool for AI-assisted coding workflows.

Archpack starts from a simple idea:

> Read one architecture pack file and generate the file structure described by it.

After that, Archpack adds generated `AGENTS.md` files, architecture drift checks, repair, clean-up, and later reference/network monitoring.

---

## 1. Core idea

Archpack manages project architecture as a pack.

A pack should be able to describe:

- directories to create,
- files to create,
- file contents,
- which generated files are temporary,
- where `AGENTS.md` files should be placed,
- how parent and child agent instructions should be combined,
- which generated files should be audited,
- which generated files can be repaired,
- which generated files can be cleaned later.

The first implementation must stay narrow. It should not become a general project generator or an automatic code-repair tool.

---

## 2. MVP stage 1: file tree generation

### Goal

Read an arbitrary architecture pack file and generate the file structure described by that file.

### Required behavior

- Read a pack file.
- Create directories described by the pack.
- Create files described by the pack.
- Write file contents described by the pack.
- Avoid unsafe path writes.
- Avoid overwriting existing files unless explicitly allowed.

### Out of scope

- Agent instruction inheritance.
- Architecture drift detection.
- Repair.
- Clean.
- Reference monitoring.
- Network monitoring.

### Acceptance criteria

- A sample pack can generate a small project tree.
- Dangerous paths are rejected.
- Existing files are not overwritten by default.

---

## 3. MVP stage 2: generated agent instruction files

### Goal

Allow the pack to specify `AGENTS.md` files for selected directories.

`AGENTS.md` is not root-only. It can be generated in any directory specified by the pack.

Example:

```text
project/
├─ AGENTS.md
├─ src/
│  └─ AGENTS.md
└─ lab/
   └─ AGENTS.md
```

### Required behavior

- Generate `AGENTS.md` at each specified directory.
- Treat directory-level `AGENTS.md` as applying to that directory and its descendants.
- Keep each local instruction block short.
- Prefer bullet-point format.
- Prefer one rule per line.

### Instruction size rule

Each local instruction block should be at most 50 lines.

This limit exists because parent and child instructions may both be read by an agent. Long instruction files become design documents and should be moved into persistent docs instead.

---

## 4. MVP stage 3: effective AGENTS.md generation

### Goal

When nested `AGENTS.md` files exist, generate the lower-level `AGENTS.md` as an effective instruction file containing:

1. inherited parent instructions,
2. plus local child instructions.

This is an optimistic strategy: if agents are more likely to follow instructions that are explicitly present in the file they read, then lower directories should contain the effective combined instruction set.

### Example

Root local instruction:

```md
- Do not add external network calls.
- Do not edit `.github/workflows/*`.
```

`lab/` local instruction:

```md
- Edit only `lab/index.html`, `lab/style.css`, and `lab/app.js` unless explicitly instructed.
- Keep the lab static.
```

Generated `lab/AGENTS.md` should contain the inherited root rules plus the local lab rules:

```md
- Do not add external network calls.
- Do not edit `.github/workflows/*`.
- Edit only `lab/index.html`, `lab/style.css`, and `lab/app.js` unless explicitly instructed.
- Keep the lab static.
```

### Required behavior

- Process directory instructions from top to bottom.
- Pass inherited rules to child directories.
- Append child-local rules after inherited rules.
- Prevent child instructions from weakening parent constraints.
- Keep generated effective `AGENTS.md` short enough to remain useful.

### Expected size

Local blocks should be around 10 to 30 lines.

Even with several nested levels, the generated effective instruction file should stay reasonably small. A hard upper bound may be introduced later, but the design target is to keep effective instruction files compact.

### Rationale

This separates responsibility while preserving explicitness:

- parent directories define broad constraints,
- child directories define local responsibilities,
- generated lower-level `AGENTS.md` files carry the effective instruction set,
- agents do not need to infer the full inheritance chain by themselves.

---

## 5. MVP stage 4: management metadata

### Goal

Record what Archpack generated.

This enables later audit, repair, and clean operations.

### Required behavior

- Record generated files.
- Record which files are strict-managed.
- Record which files are temporary agent instructions.
- Record which files are cleanable.
- Record target paths for file-level instructions if used later.

### Candidate outputs

```text
.archpack/manifest.yml
.archpack/lock.yml
```

The exact schema is not fixed in this roadmap.

---

## 6. MVP stage 5: audit

### Goal

Check whether the generated architecture-control structure has drifted.

### Required checks

- Required generated files still exist.
- strict-managed generated files have not changed unexpectedly.
- generated `AGENTS.md` files remain within the line limit.
- generated files still have their generated marker.
- child `AGENTS.md` does not weaken parent constraints.
- cleanable files are still identifiable as generated files.

### Out of scope

- Application correctness.
- Runtime behavior.
- Semantic architecture validation.
- Import graph validation.
- Network validation.

---

## 7. MVP stage 6: repair

### Goal

Restore generated strict-managed files from the pack when they are missing or damaged.

### Required behavior

- Restore generated `AGENTS.md` files.
- Restore generated control files.
- Restore generated metadata files if possible.
- Do not repair normal application source code.
- Do not repair flexible or human-owned files.

### Boundary

Archpack repair is not code repair.

It only repairs generated architecture-control files.

---

## 8. MVP stage 7: clean

### Goal

Remove temporary agent instruction files safely.

### Required behavior

- Remove only files that Archpack generated.
- Remove only files marked as removable.
- Remove only files in the requested clean group.
- Refuse to remove handwritten files.
- Refuse to remove persistent architecture documents.

### Cleanable examples

- `AGENTS.md`
- `src/AGENTS.md`
- `lab/AGENTS.md`
- `*.agent.md`

### Non-cleanable examples

- `ARCHITECTURE.md`
- `docs/adr/*.md`
- source files
- test files
- handwritten documents

---

## 9. Post-MVP: reference monitoring

After the MVP works, Archpack may add reference monitoring.

Possible checks:

- UI layer must not import database layer directly.
- Service layer must not be bypassed.
- Forbidden dependency directions must be detected.
- Generated architecture rules should be compared against actual imports.

This is deliberately post-MVP because it requires language-specific parsing or careful static analysis.

---

## 10. Post-MVP: communication monitoring

After reference monitoring, Archpack may add communication monitoring.

Possible checks:

- Static sites must not add `fetch` or external runtime calls.
- Request-time code must not call external APIs.
- Background jobs may have a different network policy from request-time paths.
- Allowed and denied domains may be declared in the pack.

This is post-MVP because network monitoring can quickly become language-, runtime-, and CI-dependent.

---

## 11. Post-MVP: semantic architecture drift

Later, Archpack may check whether files still match their declared responsibilities.

Possible checks:

- A file has taken on responsibilities outside its declared role.
- A service boundary has been bypassed.
- A removed/deferred feature has been reintroduced.
- A file-level instruction contradicts the current implementation.

This should not be part of the first implementation.

---

## 12. Current implementation order

The implementation order should be:

1. Create repository documentation.
2. Define the minimum pack format.
3. Implement plain file-tree generation.
4. Add generated `AGENTS.md` support.
5. Add parent-to-child effective `AGENTS.md` generation.
6. Add metadata generation.
7. Add audit.
8. Add repair.
9. Add clean.
10. Add CI tests for the above.
11. Only then consider reference or communication monitoring.

---

## 13. Non-goals for the first implementation

The first implementation must not attempt to:

- rewrite application code,
- perform semantic code review,
- monitor runtime network traffic,
- parse all programming languages,
- replace human architecture review,
- become a full project scaffolding framework,
- become an AI-agent runtime.

Archpack should first prove the smallest useful loop:

```text
pack → file tree → generated agent instructions → metadata → audit → repair → clean
```

