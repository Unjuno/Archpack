# Archpack plugin model

## 0. Purpose

Archpack core should stay small.

The core MVP is:

```text
pack directory → file tree → explicit repair
```

Plugins are a future extension point. They must not be required for the core MVP.

---

## 1. Review result

The previous local layout idea was rejected:

```text
.archpack/
├─ core/
│  ├─ config.yml
│  ├─ manifest.yml
│  └─ lock.yml
└─ plugins/
   ├─ index.yml
   └─ <plugin-name>/
      ├─ config.yml
      ├─ manifest.yml
      └─ lock.yml
```

Reason:

- It still fixes too much structure before there are real plugins.
- It mixes project configuration, generated state, plugin state, and possible plugin discovery.
- It implies every plugin needs the same `config / manifest / lock` shape.
- It risks making `.archpack/` look like a package manager before Archpack needs one.

The corrected rule is:

> Do not design a full plugin storage layout before the core MVP and first plugin experiment prove what state is actually needed.

---

## 2. Core boundary

The core should only be responsible for:

- reading a pack directory,
- reading files under `tree/`,
- creating directories,
- creating files,
- writing file contents,
- applying basic safety checks,
- explicitly repairing generated files from the pack directory when requested.

The core should not require:

- `AGENTS.md` generation,
- plugin installation,
- package management,
- clean-up,
- reference monitoring,
- network monitoring.

The core should not continuously enforce or monitor the project.

---

## 3. `.archpack/` rule

`.archpack/` may be introduced later, but it is not required for the core MVP.

If introduced, it should store project-local Archpack data only.

It should not store plugin implementation code.

It should not become an APT-like package directory.

---

## 4. Better future layout direction

If project-local state becomes necessary, separate configuration, state, and cache.

Candidate direction:

```text
.archpack/
├─ config.yml
├─ state/
│  ├─ core/
│  │  ├─ manifest.yml
│  │  └─ lock.yml
│  └─ plugins/
│     └─ agents/
│        ├─ manifest.yml
│        └─ lock.yml
└─ cache/
   └─ plugins/
      └─ agents/
```

This is only a candidate.

The important separation is:

- `config.yml` = project-local settings,
- `state/` = generated state and reproducibility metadata,
- `state/core/` = core-generated state,
- `state/plugins/<plugin-name>/` = per-plugin generated state,
- `cache/` = disposable cache.

---

## 5. Plugin configuration direction

Plugin enablement should be project-level configuration, not a package installation model.

Possible future direction:

```yaml
# .archpack/config.yml
plugins:
  - id: agents
    enabled: true
```

This says only that a known plugin is enabled for this project.

It does not define where plugin code is installed.
It does not define a plugin registry.
It does not define dependency resolution.

---

## 6. First plugin candidate

`AGENTS.md` generation is the first plugin candidate, not core behavior.

Possible future pack section:

```yaml
agent_rules:
  - dir: .
    rules:
      - Do not add external network calls unless explicitly allowed.

  - dir: src
    rules:
      - Keep application logic inside src.
```

Possible output:

```text
AGENTS.md
src/AGENTS.md
```

A later plugin extension may generate effective inherited `AGENTS.md` files.

---

## 7. Why not an APT-like package manager now

An APT-like package manager is too large for the current project stage.

It would require decisions about:

- package registry,
- dependency resolution,
- version pinning,
- trust and signatures,
- installation paths,
- upgrade and rollback behavior,
- plugin compatibility.

Those decisions should wait until there are multiple real plugins worth managing.

---

## 8. Promotion rule

A plugin should be promoted only if:

- it solves a concrete user problem,
- it can be demonstrated with a small pack,
- it does not make the core harder to explain,
- it can be disabled or left unused,
- it does not force unrelated schema changes.

---

## 9. Current decision

Current decision:

```text
Core MVP:
  pack directory → file tree → explicit repair

Plugin model:
  deferred

.archpack/:
  not required for core MVP
  may later store config/state/cache

APT-like package manager:
  explicitly deferred
```
