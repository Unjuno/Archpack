# Archpack plugin model

## 0. Purpose

Archpack core should stay small.

The core MVP is:

```text
pack → file tree
```

Additional behavior should be added through plugins or plugin-like experiments.

Examples:

- `AGENTS.md` generation,
- effective inherited `AGENTS.md`,
- generated-file drift checks,
- repair,
- clean-up,
- reference monitoring,
- network monitoring.

---

## 1. Core boundary

The core should only be responsible for:

- reading a pack file,
- creating directories,
- creating files,
- writing file contents,
- applying basic safety checks.

The core should not require `AGENTS.md` generation or any AI-agent-specific behavior.

---

## 2. Local project directory

Archpack may use a project-local directory:

```text
.archpack/
```

This directory is for Archpack metadata and project-local configuration.

Possible future contents:

```text
.archpack/
├─ config.yml
├─ plugins.yml
├─ manifest.yml
└─ lock.yml
```

The exact files are not fixed yet.

---

## 3. Why not an APT-like package manager now

An APT-like package manager is too large for the MVP.

It would introduce questions that are not needed yet:

- package registry,
- dependency resolution,
- version pinning,
- trust and signatures,
- installation paths,
- upgrade and rollback behavior,
- plugin compatibility.

Those may become useful later, but they should not be part of the core MVP.

---

## 4. Recommended first model

Start with a simple project-local plugin declaration.

Example direction:

```yaml
plugins:
  - name: agents
    enabled: true
```

This does not require a package manager.

It only says which known plugin behavior should run for this project.

---

## 5. First plugin candidate: AGENTS.md generator

`AGENTS.md` generation should be treated as a plugin candidate, not core behavior.

The plugin may eventually read pack sections such as:

```yaml
agent_rules:
  - dir: .
    rules:
      - Do not add external network calls unless explicitly allowed.

  - dir: src
    rules:
      - Keep application logic inside src.
```

The plugin would generate:

```text
AGENTS.md
src/AGENTS.md
```

A later extension may generate effective inherited `AGENTS.md` files.

---

## 6. Plugin promotion rule

A plugin should be promoted only if:

- it solves a concrete user problem,
- it can be demonstrated with a small pack,
- it does not make the core harder to explain,
- it can be disabled or left unused,
- it does not force unrelated schema changes.

---

## 7. Deferred package management

A real package manager can be reconsidered only after there are multiple useful plugins.

Possible future direction:

```text
archpack plugin add agents
archpack plugin add ref-audit
archpack plugin update
```

This is intentionally deferred.

Do not build a plugin package manager before there are real plugins worth managing.
