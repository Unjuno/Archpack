# Archpack plugin model

## 0. Purpose

Archpack core should stay small.

The core is:

```text
pack directory → file tree → explicit repair
```

Plugins are reviewed extension units. They must not be required for core commands.

The current policy is:

```text
single repository → small plugin experiment → owner review → keep, revise, or remove
```

---

## 1. Core boundary

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

## 2. Plugin intake policy

Plugins may be added to the main repository after review.

The repository can contain:

- the core,
- reviewed plugin experiments,
- accepted plugins,
- plugin examples,
- plugin documentation,
- tests for plugin behavior.

A separate release repository or release fork is not required now.

The important rule is that plugins must remain reviewable and removable.

---

## 3. Plugin placement rule

A plugin works by being placed in the appropriate plugin area.

The repository-local plugin area is:

```text
src/archpack/plugins/<plugin-name>/
```

A plugin directory must contain one descriptor file:

```text
src/archpack/plugins/<plugin-name>/plugin.yml
```

Example:

```text
src/archpack/plugins/
└─ agents/
   ├─ plugin.yml
   ├─ __init__.py
   ├─ commands.py
   └─ generator.py
```

This means plugin recognition starts from repository structure plus a single plugin descriptor, not from an external package manager.

Do not introduce a registry, installer, or dependency resolver before real plugins require it.

---

## 4. Plugin descriptor rule

`plugin.yml` is the single file that describes how the plugin is recognized and used.

It should answer:

- What is the plugin ID?
- What problem does it solve?
- Is it experimental or accepted?
- Where is its usage document?
- What command exposes it?
- What input does it read?
- What files or behavior can it produce?
- How can it be tested?
- How can it be removed?

Current descriptor example:

```yaml
id: agents
name: AGENTS.md generator
status: experimental
summary: Generate AGENTS.md files from local rules declared in agents.toml.

docs:
  usage: docs/plugins/agents.md

commands:
  - name: agents-generate
    help: Generate AGENTS.md files from agents.toml.
    entrypoint: archpack.plugins.agents.commands:generate

inputs:
  files:
    - agents.toml

outputs:
  files:
    - AGENTS.md
    - "**/AGENTS.md"

remove:
  safe_to_delete:
    - src/archpack/plugins/agents/
  generated_files:
    - AGENTS.md
    - "**/AGENTS.md"
```

This descriptor is not a package manager manifest.

It is a local reviewed description of plugin behavior.

---

## 5. Plugin recognition rule

A plugin is recognizable when all are true:

1. it lives under `src/archpack/plugins/<plugin-name>/`,
2. it contains `plugin.yml`,
3. `plugin.yml` has an `id`,
4. the `id` matches `<plugin-name>`,
5. the plugin has been reviewed by the owner.

Initial recognition should be conservative.

Do not automatically execute every discovered plugin.

Recognition only means Archpack can list or wire the plugin after review.

---

## 6. Plugin usage rule

A plugin should be used through an explicit command or explicit CLI wiring.

Do not run plugins implicitly during core `unpack` or `repair`.

Current reviewed plugin command:

```text
archpack agents-generate <pack-dir> --out <dir>
```

A generic command may be considered later:

```text
archpack plugin run <plugin-name> <pack-dir> --out <dir>
```

The generic form should wait until there are several plugins.

Core commands remain independent:

```text
archpack unpack <pack-dir> --out <dir>
archpack repair <pack-dir> --out <dir>
```

---

## 7. Plugin acceptance rule

A plugin may remain in the repository only if:

- it solves a concrete problem,
- it is small enough to review,
- it has tests or clear verification steps,
- it does not make the core harder to explain,
- it does not force unrelated core format changes,
- it can be documented briefly,
- it can be disabled, ignored, or removed later.

If a plugin fails these conditions, it should be revised or removed.

---

## 8. Reviewed plugin: agents

The first reviewed plugin is the AGENTS.md generator.

Location:

```text
src/archpack/plugins/agents/
```

Descriptor:

```text
src/archpack/plugins/agents/plugin.yml
```

Usage document:

```text
docs/plugins/agents.md
```

Input:

```text
agents.toml
```

Command:

```text
archpack agents-generate <pack-dir> --out <dir>
```

Output examples:

```text
AGENTS.md
src/AGENTS.md
```

This plugin is explicit. It does not run during `unpack` or `repair`.

---

## 9. Deferred plugin extension: effective AGENTS.md

A later extension may generate effective inherited `AGENTS.md` files:

```text
parent rules + local rules = effective AGENTS.md
```

This is not part of the current agents plugin.

Open questions:

- how to detect child rules that weaken parent rules,
- whether to include inherited/local section headers,
- whether to collapse duplicate rules,
- whether effective files need a hard line limit.

---

## 10. `.archpack/` rule

`.archpack/` is deferred.

If introduced later, it should store project-local Archpack data only.

It should not store plugin implementation code.
It should not become an APT-like package directory.

Do not design a full project-local state layout before real reviewed plugins prove what state is actually needed.

---

## 11. Why not an APT-like package manager now

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

## 12. Future removal tooling

Archpack may later include tools that make plugin removal safer.

Possible future tools:

```text
archpack plugin list
archpack plugin disable <name>
archpack plugin remove <name>
archpack plugin doctor <name>
```

These are not core commands.

They should be added only after there are real reviewed plugins to manage.

---

## 13. Current decision

Current decision:

```text
Core:
  pack directory → file tree → explicit repair

Plugin intake:
  single repository
  reviewed before keeping
  removable when unnecessary or unsafe

Plugin placement:
  src/archpack/plugins/<plugin-name>/

Plugin descriptor:
  src/archpack/plugins/<plugin-name>/plugin.yml

Plugin recognition:
  placement + plugin.yml + owner review

Plugin usage:
  explicit command only
  no implicit execution during core unpack/repair

Reviewed plugin:
  agents

Deferred:
  effective AGENTS.md
  dynamic plugin loader
  .archpack state
  APT-like package manager
```
