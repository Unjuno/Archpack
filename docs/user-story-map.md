# Archpack user story map

## 0. Position

This document defines how Archpack should decide post-MVP work.

Archpack should first build the smallest useful MVP. After that, new work should be selected from concrete user stories instead of guessed features.

---

## 1. MVP boundary

The first MVP should stay limited to this loop:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

The MVP should prove that one pack can:

1. generate a project file tree,
2. generate root and directory-level `AGENTS.md`,
3. compose parent and child rules into effective `AGENTS.md` files.

---

## 2. Story map backbone

The user journey is:

```text
Prepare pack
→ Generate files
→ Generate AGENTS.md
→ Generate effective AGENTS.md
→ Use the result in an AI-assisted coding workflow
→ Observe problems
→ Decide the next feature
```

---

## 3. User activities

### 3.1 Prepare pack

User goal:

- Write one compact architecture pack instead of manually creating many files.

Questions:

- Is the format understandable?
- Is the file easier to review than many separate instructions?
- What fields are missing?

### 3.2 Generate files

User goal:

- Generate a reproducible project structure from one pack.

Questions:

- Does the generated tree match expectations?
- Are unsafe paths rejected?
- Are existing files protected by default?

### 3.3 Generate AGENTS.md

User goal:

- Place short agent instructions in the project root and selected directories.

Questions:

- Is the root `AGENTS.md` useful?
- Are directory-level rules useful?
- Are the files short enough?

### 3.4 Generate effective AGENTS.md

User goal:

- Make lower-level `AGENTS.md` include inherited parent rules plus local rules.

Questions:

- Are inherited rules visible where expected?
- Does the effective file stay readable?
- Does rule composition reduce repeated explanation?

### 3.5 Decide next work

User goal:

- Report concrete problems after trying the MVP.

Questions:

- Is the problem in the pack format?
- Is the problem in generated output?
- Is the problem outside Archpack's scope?
- Can the problem be reproduced with a small example?

---

## 4. Problem report format

Future issues should start as problem reports, not direct feature requests.

```text
Context:
What project or example was used?

Expected result:
What should have happened?

Observed result:
What happened instead?

Impact:
Why does it matter?

Possible next step:
Should Archpack change, should docs change, or should this stay out of scope?
```

---

## 5. Feature promotion rule

A post-MVP feature should be considered only when:

1. a repeated concrete problem is observed,
2. the problem belongs to Archpack,
3. the feature can be tested with a small example,
4. the feature does not break the small MVP loop.

---

## 6. Deferred candidates

These should remain deferred until user stories justify them:

- generated-file drift checks,
- repair,
- clean-up,
- reference monitoring,
- network monitoring,
- semantic architecture checks,
- file-level instruction files,
- formal schema validation,
- CI integration.

---

## 7. Discipline

Do not grow Archpack by speculation.

Build the MVP first, then collect problems, then decide what to add.
