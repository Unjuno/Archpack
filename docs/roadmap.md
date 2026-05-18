# Archpack creation roadmap

## 0. Position of this document

This document defines the creation roadmap before implementation.

The first roadmap must stay narrow. It should describe the path to the smallest useful Archpack prototype, not every later monitoring feature.

The starting idea is:

> Read one architecture pack file and generate the file structure described by it.

The first useful extension is:

> Generate directory-level `AGENTS.md` files from the same pack, including inherited parent instructions when needed.

Features such as generated-file drift checks, repair, clean-up, reference monitoring, and network monitoring are intentionally moved to the final future-candidates section because many details are still undecided.

---

## 1. Core idea

Archpack starts as a controlled file-structure generator.

A pack should eventually be able to describe:

- directories to create,
- files to create,
- file contents,
- where `AGENTS.md` files should be placed,
- local rules for each `AGENTS.md`,
- how parent and child agent instructions should be combined.

The first implementation must not become a full architecture governance framework. It should first prove that one file can generate a useful project structure and useful agent instructions.

---

## 2. Confirmed MVP scope

The MVP scope is limited to the following sequence:

```text
architecture-pack file
→ file tree generation
→ directory-level AGENTS.md generation
→ effective AGENTS.md generation by parent-to-child rule composition
```

This means the MVP should answer only these questions:

1. Can Archpack read a pack file?
2. Can Archpack create the described file structure?
3. Can Archpack generate `AGENTS.md` files in specified directories?
4. Can Archpack compose parent and child agent rules into lower-level effective `AGENTS.md` files?

Everything beyond this is deliberately deferred.

---

## 3. Stage 1: arbitrary file tree generation

### Goal

Read an architecture pack file and generate the file structure described by that file.

### Required behavior

- Read one pack file.
- Create directories described by the pack.
- Create files described by the pack.
- Write file contents described by the pack.
- Avoid unsafe path writes.
- Avoid overwriting existing files unless explicitly allowed.

### Acceptance criteria

- A sample pack can generate a small project tree.
- Dangerous paths are rejected.
- Existing files are not overwritten by default.

### Out of scope for this stage

- `AGENTS.md` inheritance.
- Drift checks.
- Repair.
- Clean-up.
- Reference monitoring.
- Network monitoring.

---

## 4. Stage 2: directory-level AGENTS.md generation

### Goal

Allow the pack to specify local agent instructions for selected directories.

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

- The pack can define local agent rules for a directory.
- Archpack can generate `AGENTS.md` in that directory.
- Directory-level `AGENTS.md` applies to that directory and its descendants.
- Rules should be written as bullet points.
- Prefer one rule per line.
- Keep local rule blocks short.

### Local instruction size rule

Each local instruction block should be at most 50 lines.

This is a design limit, not a target. A good local block should often be much shorter.

### Rationale

`AGENTS.md` should not become a long architecture document.

It should be a short instruction index for coding agents.

Long explanations should move to persistent documents such as `ARCHITECTURE.md`, ADRs, or other docs.

---

## 5. Stage 3: effective AGENTS.md generation

### Goal

When nested directories have local agent instructions, generate the lower-level `AGENTS.md` as an effective instruction file.

An effective `AGENTS.md` contains:

1. inherited parent rules,
2. plus local child rules.

This is an optimistic strategy:

> If agents are more likely to follow instructions that are explicitly present in the file they read, then lower directories should contain the combined effective instruction set.

---

## 6. Effective AGENTS.md example

Root local rules:

```md
- Do not add external network calls.
- Do not edit `.github/workflows/*`.
```

`lab/` local rules:

```md
- Edit only `lab/index.html`, `lab/style.css`, and `lab/app.js` unless explicitly instructed.
- Keep the lab static.
```

Generated `lab/AGENTS.md`:

```md
- Do not add external network calls.
- Do not edit `.github/workflows/*`.
- Edit only `lab/index.html`, `lab/style.css`, and `lab/app.js` unless explicitly instructed.
- Keep the lab static.
```

The generated lower-level file contains the parent constraints plus the local directory constraints.

---

## 7. Effective AGENTS.md composition rules

### Required behavior

- Process directory instructions from top to bottom.
- Pass inherited rules to child directories.
- Append child-local rules after inherited rules.
- Do not allow child rules to weaken parent rules.
- Keep generated effective `AGENTS.md` compact.

### Expected size

Local blocks should usually be around 10 to 30 lines.

The generated effective file may be longer than a local block, but it should still stay readable.

The current design assumes shallow nesting. If nesting becomes deep, the format must be revisited.

### Rationale

This separates responsibility while preserving explicitness:

- parent directories define broad constraints,
- child directories define local responsibilities,
- generated lower-level `AGENTS.md` files carry the effective instruction set,
- agents do not need to infer the full inheritance chain by themselves.

---

## 8. Stage 4: minimal implementation proof

### Goal

Build only enough implementation to prove the three confirmed capabilities:

1. file tree generation,
2. directory-level `AGENTS.md` generation,
3. effective `AGENTS.md` generation.

### Required checks

- A sample pack generates a project tree.
- A sample pack generates root `AGENTS.md`.
- A sample pack generates child `AGENTS.md`.
- A child `AGENTS.md` includes inherited parent rules.
- Local rules are appended after inherited rules.
- Unsafe paths are rejected.

### Non-goal

This stage should not implement drift checking, repair, clean-up, reference checks, or network checks.

---

## 9. Current implementation order

The implementation order should be:

1. Keep the repository documentation minimal and accurate.
2. Define the minimum pack format for file generation.
3. Implement plain file-tree generation.
4. Add local `AGENTS.md` generation.
5. Add parent-to-child effective `AGENTS.md` generation.
6. Add tests for generated output.
7. Only after this works, revisit monitoring and maintenance features.

---

## 10. Non-goals for the first implementation

The first implementation must not attempt to:

- rewrite application code,
- perform semantic code review,
- monitor runtime network traffic,
- parse all programming languages,
- repair generated files,
- clean generated files,
- detect architecture drift,
- replace human architecture review,
- become a full project scaffolding framework,
- become an AI-agent runtime.

The first implementation should prove only this loop:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

---

## 11. Deferred candidates

The following features are useful, but they are not confirmed for the first implementation.

They should be considered only after the MVP above works.

### 11.1 Generated-file drift check

Possible future checks:

- Generated files still exist.
- Generated `AGENTS.md` files still match the pack.
- Generated files still have a generated marker.
- Effective `AGENTS.md` files still contain inherited parent rules.

Unresolved questions:

- Which generated files are strict?
- Which generated files are allowed to change?
- How much metadata is needed?
- Should drift checking be line-based, hash-based, or rule-based?

### 11.2 Repair

Possible future behavior:

- Restore missing generated files.
- Restore damaged generated `AGENTS.md` files.
- Restore generated metadata files if such metadata exists.

Unresolved questions:

- What should be repaired automatically?
- What must remain human-owned?
- How should repair avoid overwriting intentional edits?

### 11.3 Clean-up

Possible future behavior:

- Remove temporary generated `AGENTS.md` files.
- Remove generated file-level agent instruction files.
- Refuse to delete handwritten files.

Unresolved questions:

- What generated marker is required?
- What metadata is required?
- What is the exact clean target group model?

### 11.4 Reference monitoring

Possible future checks:

- UI layer must not import database layer directly.
- Service layer must not be bypassed.
- Forbidden dependency directions must be detected.

Unresolved questions:

- Which languages are supported first?
- Is parsing AST required?
- Is grep-level detection acceptable initially?

### 11.5 Network monitoring

Possible future checks:

- Static sites must not add `fetch` or external runtime calls.
- Request-time code must not call external APIs.
- Background jobs may have different network policy from request-time code.

Unresolved questions:

- Is this static detection or runtime detection?
- How should allowed domains be declared?
- How should false positives be handled?

### 11.6 Semantic architecture drift

Possible future checks:

- A file has taken on responsibilities outside its declared role.
- A removed/deferred feature has been reintroduced.
- A file-level instruction contradicts the current implementation.

Unresolved questions:

- Is an LLM required?
- Can this be tested reliably in CI?
- How should false positives be reviewed?

---

## 12. Roadmap discipline

Do not promote deferred candidates into MVP until the confirmed MVP works.

The confirmed MVP is intentionally small:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

Anything beyond that must be justified by a concrete problem observed during use.
