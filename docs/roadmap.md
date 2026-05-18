# Archpack roadmap

## 0. Position of this document

This document describes what Archpack is intended to become, step by step.

It is not an implementation specification.
It is not a command reference.
It is not a finalized schema document.

The purpose of this roadmap is to keep the project direction clear before implementation begins.

---

## 1. Overall direction

Archpack starts from a small idea:

> Read one architecture pack file and generate the file structure described by it.

From there, Archpack should gradually become a tool for preparing explicit architecture context for AI-assisted coding.

The important point is that Archpack should grow in layers.
Each layer should solve one clear problem before the next layer is added.

---

## 2. Stage 1: generate a file tree from one pack

### What we want

We want to write one pack file and generate a project file structure from it.

The pack should be able to describe:

- directories,
- files,
- file contents.

### Why this matters

The first value of Archpack is not AI control.
The first value is reproducible structure generation.

Instead of manually splitting one generated architecture document into many files, Archpack should create those files directly.

### Desired state

A user can prepare one pack file, run Archpack, and obtain the described file tree.

### Still undecided

- The exact pack schema.
- The exact command name and arguments.
- The overwrite policy.
- The generated marker policy.

---

## 3. Stage 2: generate AGENTS.md in selected directories

### What we want

We want the pack to specify where `AGENTS.md` files should be placed.

`AGENTS.md` should not be root-only.
It should be possible to place it in selected directories.

Example:

```text
project/
├─ AGENTS.md
├─ src/
│  └─ AGENTS.md
└─ lab/
   └─ AGENTS.md
```

### Why this matters

Different parts of a project have different responsibilities.
A single root `AGENTS.md` can become too long and too vague.

Directory-level `AGENTS.md` files allow responsibility to be separated explicitly.

### Desired state

A user can define local agent rules for each important directory, and Archpack can generate `AGENTS.md` files at those locations.

### Writing policy

Agent instructions should be short.

- Prefer bullet points.
- Prefer one rule per line.
- Avoid long paragraphs.
- Keep each local rule block around 10 to 30 lines when possible.
- Use 50 lines as the rough upper limit for a local instruction block.

### Still undecided

- Whether the line limit is enforced immediately or treated as a warning first.
- Whether local rules are stored directly in the pack or referenced from another document.
- How much metadata each generated `AGENTS.md` should contain.

---

## 4. Stage 3: generate effective AGENTS.md by inheritance

### What we want

We want lower-level `AGENTS.md` files to include both:

1. inherited parent rules,
2. local child rules.

This means a lower directory can receive an effective `AGENTS.md` that already contains the relevant upper-level constraints.

### Why this matters

This is an optimistic design assumption:

> If an agent is more likely to follow instructions that are explicitly present in the file it reads, then lower-level `AGENTS.md` files should contain the inherited effective rules directly.

The agent should not be forced to reconstruct the full parent-child instruction chain on its own.

### Desired state

If the root has broad rules and a child directory has local rules, the generated child `AGENTS.md` contains both.

Example:

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

### Responsibility model

This gives a clear separation:

- parent directories define broad constraints,
- child directories define local responsibilities,
- generated lower-level `AGENTS.md` files carry the effective rule set.

### Still undecided

- How to detect that a child rule weakens a parent rule.
- Whether weakening detection is manual, rule-based, or postponed.
- Whether the effective file should include section headers showing inherited and local rules.
- Whether duplicate inherited rules should be collapsed.

---

## 5. Stage 4: prove the smallest useful loop

### What we want

We want to prove the smallest useful Archpack loop:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

### Why this matters

This is the point where Archpack becomes useful without becoming large.

It can already:

- generate structure,
- place agent instructions,
- separate directory responsibilities,
- make inherited constraints explicit.

### Desired state

A small example pack can demonstrate the whole loop.

The example should be simple enough that a reader can understand the result without needing the implementation internals.

### Still undecided

- The example project shape.
- Whether the example should be generic or based on an actual project pattern.
- Whether CI is added at this stage or after the first implementation exists.

---

## 6. Stage 5: document the first stable format

### What we want

After the smallest loop is proven, the pack format should be documented.

The format document should explain only the fields that are actually used.

### Why this matters

The schema should follow the working concept, not the other way around.

Writing too much schema before the first useful loop is proven will create fake precision.

### Desired state

A reader can understand:

- how to define files,
- how to define local directory rules,
- how inherited `AGENTS.md` generation works,
- what is intentionally not supported yet.

### Still undecided

- Whether schema validation is required immediately.
- Whether to publish a formal JSON Schema later.
- Whether to version the pack format from the start.

---

## 7. Deferred candidates

The following ideas are useful, but they are not part of the confirmed first roadmap.
They should stay deferred until the smallest useful loop works.

### 7.1 Generated-file drift check

Possible future direction:

- Check whether generated files still exist.
- Check whether generated `AGENTS.md` files still match the pack.
- Check whether inherited rules are still present in effective `AGENTS.md` files.

Unresolved questions:

- Which files are strict?
- Which files are allowed to change?
- Is checking hash-based, line-based, or rule-based?
- What metadata is necessary?

### 7.2 Repair

Possible future direction:

- Restore missing generated files.
- Restore damaged generated `AGENTS.md` files.
- Restore generated metadata if such metadata exists.

Unresolved questions:

- What should be repaired automatically?
- What must remain human-owned?
- How does repair avoid overwriting intentional edits?

### 7.3 Clean-up

Possible future direction:

- Remove temporary generated `AGENTS.md` files.
- Remove generated file-level agent instruction files.
- Refuse to delete handwritten files.

Unresolved questions:

- What generated marker is required?
- What metadata is required?
- What is the exact clean target group model?

### 7.4 Reference monitoring

Possible future direction:

- Detect forbidden dependency directions.
- Detect direct imports across forbidden layers.
- Compare declared architecture boundaries with actual references.

Unresolved questions:

- Which language is supported first?
- Is AST parsing required?
- Is grep-level detection acceptable initially?

### 7.5 Network monitoring

Possible future direction:

- Detect unwanted external calls.
- Separate request-time network policy from background-job network policy.
- Allow declared domains only in declared areas.

Unresolved questions:

- Is detection static or runtime-based?
- How are allowed domains declared?
- How are false positives handled?

### 7.6 Semantic architecture drift

Possible future direction:

- Detect files taking on responsibilities outside their declared role.
- Detect removed or deferred features being reintroduced.
- Detect contradictions between instructions and implementation.

Unresolved questions:

- Is an LLM required?
- Can this be tested reliably in CI?
- What review process handles false positives?

---

## 8. Roadmap discipline

Do not move deferred candidates into the active roadmap until the confirmed loop works:

```text
pack → file tree → local AGENTS.md → effective AGENTS.md
```

The first useful version should be small enough to build, inspect, and revise.

Anything beyond that must be justified by a concrete problem observed during use.
