# Archpack user story map

## 0. Position

This document defines how Archpack should decide work after the core MVP.

Archpack should first build the smallest useful core. After that, new behavior should be selected from concrete user stories instead of guessed features.

---

## 1. Core MVP boundary

The first MVP should stay limited to this loop:

```text
pack directory → file tree → explicit repair
```

The MVP should prove that one pack directory can:

1. store files under `tree/`,
2. generate the described project structure,
3. restore missing generated files when repair is explicitly requested.

`AGENTS.md` generation and inherited effective instructions are plugin candidates, not core MVP requirements.

---

## 2. Story map backbone

The user journey is:

```text
Prepare pack directory
→ Generate file tree
→ Inspect result
→ Damage or remove generated files
→ Explicitly repair from pack
→ Observe problems
→ Decide next plugin or core change
```

---

## 3. User activities

### 3.1 Prepare pack directory

User goal:

- Create one pack directory whose `tree/` folder contains the files to generate.

Questions:

- Is the directory pack understandable?
- Is it easier to review than a large YAML file?
- Are metadata or IDs actually needed?

### 3.2 Generate file tree

User goal:

- Generate a reproducible project structure from one pack directory.

Questions:

- Does the generated tree match expectations?
- Are unsafe paths rejected?
- Are existing files protected by default?

### 3.3 Inspect result

User goal:

- Confirm the generated files before using them in real work.

Questions:

- Is the output easy to inspect?
- Is the result too large?
- Did the pack create anything surprising?

### 3.4 Explicitly repair

User goal:

- Restore missing generated files from the pack directory when requested.

Questions:

- Does repair restore the expected files?
- Does repair avoid unexpected overwrites?
- Is repair behavior easy to understand?

### 3.5 Decide next work

User goal:

- Report concrete problems after trying the MVP.

Questions:

- Is the problem in the pack format?
- Is the problem in generation?
- Is the problem in repair?
- Is the problem outside Archpack's scope?
- Can the problem be reproduced with a small example?

---

## 4. Plugin-candidate stories

These stories are not core MVP requirements.
They should be tested as plugin candidates only after the core works.

### 4.1 Generate AGENTS.md

User goal:

- Generate root and directory-level `AGENTS.md` files from plugin-defined rules.

Questions:

- Is root `AGENTS.md` useful?
- Are directory-level rules useful?
- Are the files short enough?

### 4.2 Generate effective AGENTS.md

User goal:

- Make lower-level `AGENTS.md` include inherited parent rules plus local rules.

Questions:

- Are inherited rules visible where expected?
- Does the effective file stay readable?
- Does rule composition reduce repeated explanation?

---

## 5. Problem report format

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
Should Archpack core change, should a plugin be tested, should docs change, or should this stay out of scope?
```

---

## 6. Feature promotion rule

A post-MVP feature should be considered only when:

1. a repeated concrete problem is observed,
2. the problem belongs to Archpack,
3. the feature can be tested with a small example,
4. the feature does not break the small core loop.

---

## 7. Deferred candidates

These should remain deferred until user stories justify them:

- `AGENTS.md` generation,
- effective inherited `AGENTS.md`,
- generated-file drift checks,
- clean-up,
- reference monitoring,
- network monitoring,
- semantic architecture checks,
- file-level instruction files,
- formal schema validation,
- CI integration.

---

## 8. Discipline

Do not grow Archpack by speculation.

Build the core MVP first, then collect problems, then decide what to add as plugins or core changes.
