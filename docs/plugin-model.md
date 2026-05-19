# Archpack plugin model

## 0. Purpose

Archpack core should stay small.

The core MVP is:

```text
pack directory → file tree → explicit repair
```

Plugins are future extension units. They must not be required for the core MVP.

A plugin does not need to live in a separate repository at this stage.

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

- the core MVP,
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

The first repository-local plugin area should be:

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
- What command exposes it?
- What pack section or input does it read?
- What files or behavior can it produce?
- How can it be tested?
- How can it be removed?

A first descriptor direction:

```yaml
id: agents
name: AGENTS.md generator
status: experimental
summary: Generate AGENTS.md files from declared local rules.

commands:
  - name: agents-generate
    help: Generate AGENTS.md files from plugin input.
    entrypoint: archpack.plugins.agents.commands:generate

inputs:
  pack_sections:
    - agent_rules

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

Good first-stage direction:

```text
archpack agents-generate <pack-dir> --out <dir>
```

or later:

```text
archpack plugin run agents <pack-dir> --out <dir>
```

The first form is simpler.
The second form should wait until there are several plugins.

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
- it does not force unrelated pack-format changes,
- it can be documented briefly,
- it can be disabled, ignored, or removed later.

If a plugin fails these conditions, it should be revised or removed.

---

## 8. Plugin shape for the first stage

Do not start with a dynamic plugin loader.

The first accepted plugins should be explicit optional modules inside the repository.

Initial plugin behavior should be invoked explicitly by core CLI wiring or a small reviewed command, not by automatic discovery.

The first priority is reviewability, not extensibility.

---

## 9. `.archpack/` rule

`.archpack/` may be introduced later, but it is not required for the core MVP.

If introduced, it should store project-local Archpack data only.

It should not store plugin implementation code.

It should not become an APT-like package directory.

---

## 10. Rejected early layout

The previous local layout idea is rejected for now:

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

- It fixes too much structure before there are real plugins.
- It mixes project configuration, generated state, plugin state, and possible plugin discovery.
- It implies every plugin needs the same `config / manifest / lock` shape.
- It makes `.archpack/` look like a package manager before Archpack needs one.

Corrected rule:

> Do not design a full project-local plugin storage layout before real reviewed plugins prove what state is actually needed.

---

## 11. Future project-local state direction

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

## 12. First plugin candidate

`AGENTS.md` generation is the first plugin candidate, not core behavior.

The candidate plugin location would be:

```text
src/archpack/plugins/agents/
```

The candidate descriptor would be:

```text
src/archpack/plugins/agents/plugin.yml
```

Possible future plugin input:

```yaml
agent_rules:
  - dir: .
    rules:
      - Keep instructions short.

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

## 13. Why not an APT-like package manager now

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

## 14. Future removal tooling

Archpack may later include tools that make plugin removal safer.

Possible future tools:

```text
archpack plugin list
archpack plugin disable <name>
archpack plugin remove <name>
archpack plugin doctor <name>
```

These are not core MVP commands.

They should be added only after there are real reviewed plugins to manage.

---

## 15. Current decision

Current decision:

```text
Core MVP:
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

Plugin implementation:
  deferred
  no dynamic plugin loader yet

.archpack/:
  not required for core MVP
  may later store config/state/cache

APT-like package manager:
  explicitly deferred
```
