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

This directory is for Archpack metadata, project-local settings, and future plugin state.

The directory must not be flat if plugins are expected to grow.

Flat layout is rejected:

```text
.archpack/
├─ config.yml
├─ plugins.yml
├─ manifest.yml
└─ lock.yml
```

This mixes core state and plugin state and will become unclear as plugins increase.

---

## 3. Recommended local layout

Use separated areas for core and plugins:

```text
.archpack/
├─ core/
│  ├─ config.yml
│  ├─ manifest.yml
│  └─ lock.yml
└─ plugins/
   ├─ index.yml
   ├─ agents/
   │  ├─ config.yml
   │  ├─ manifest.yml
   │  └─ lock.yml
   ├─ ref-audit/
   │  ├─ config.yml
   │  ├─ manifest.yml
   │  └─ lock.yml
   └─ network-audit/
      ├─ config.yml
      ├─ manifest.yml
      └─ lock.yml
```

The exact files are not fixed yet.

The important rule is structural separation:

- core state belongs under `.archpack/core/`,
- plugin index belongs under `.archpack/plugins/index.yml`,
- each plugin owns its own `.archpack/plugins/<plugin-name>/` directory.

---

## 4. Why this layout

A nested layout gives each plugin a clear namespace.

It avoids:

- collisions between plugin files,
- one large shared `plugins.yml`,
- unclear ownership of `manifest.yml` and `lock.yml`,
- accidental coupling between unrelated plugins,
- migration pain when plugins need their own state.

Each plugin can manage its own local state without changing the core directory structure.

---

## 5. Why not an APT-like package manager now

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

The first step is not package management.

The first step is local plugin namespacing.

---

## 6. Recommended first model

Start with local plugin declaration and local plugin state.

Example direction:

```yaml
# .archpack/plugins/index.yml
plugins:
  - name: agents
    enabled: true
    state_dir: agents
```

This does not require a package manager.

It only says which known plugin behavior should run for this project and where that plugin may store its project-local state.

---

## 7. First plugin candidate: AGENTS.md generator

`AGENTS.md` generation should be treated as a plugin candidate, not core behavior.

Possible local state:

```text
.archpack/plugins/agents/
├─ config.yml
├─ manifest.yml
└─ lock.yml
```

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

## 8. Plugin promotion rule

A plugin should be promoted only if:

- it solves a concrete user problem,
- it can be demonstrated with a small pack,
- it does not make the core harder to explain,
- it can be disabled or left unused,
- it does not force unrelated schema changes.

---

## 9. Deferred package management

A real package manager can be reconsidered only after there are multiple useful plugins.

Possible future direction:

```text
archpack plugin add agents
archpack plugin add ref-audit
archpack plugin update
```

This is intentionally deferred.

Do not build a plugin package manager before there are real plugins worth managing.
