# Archpack roadmap

## 0. Purpose

This roadmap describes the current direction of Archpack.

It is not a command reference or a full implementation spec.

The current core loop is:

```text
pack directory → file tree → explicit repair
```

Everything beyond this core should be treated as a reviewed plugin or a later experiment.

---

## 1. Current core status

The core is implemented as a small directory-pack tool.

A pack directory contains a `tree/` directory.
Files under `tree/` are generated into an output directory.

Example pack:

```text
examples/minimal-pack/
└─ tree/
   └─ README.md
```

Implemented core commands:

```text
archpack unpack <pack-dir> --out <dir>
archpack unpack <pack-dir> --out <dir> --skip-existing
archpack repair <pack-dir> --out <dir>
archpack repair <pack-dir> --out <dir> --overwrite
```

Implemented validation:

- basic unpack,
- existing-file refusal,
- `--skip-existing`,
- default repair for missing files,
- overwrite repair,
- symlink rejection,
- CI test run through GitHub Actions.

---

## 2. Core boundary

Core includes:

- reading a pack directory,
- reading files under `tree/`,
- generating directories,
- generating files,
- writing file contents,
- skipping existing files when explicitly requested,
- explicitly repairing generated files from the pack when requested.

Core does not include:

- continuous enforcement,
- background monitoring,
- implicit auto-repair,
- plugin execution,
- `AGENTS.md` generation as special behavior,
- `.archpack/` state management,
- package management.

---

## 3. Current safety policy

The current safety policy is intentionally conservative.

- Files outside `tree/` are not generated.
- Existing files are not overwritten by default.
- `unpack` stops when it would overwrite an existing file.
- `unpack --skip-existing` keeps existing files and writes only missing files.
- `repair` restores missing files only by default.
- `repair --overwrite` overwrites existing files only when explicitly requested.
- Symlinks in the pack tree are rejected.

---

## 4. Plugin direction

Archpack should not add every useful capability into the core.

Plugins are handled in the same repository, but only after review.

The current plugin intake policy is:

```text
one problem → one experiment → one review → keep, revise, or remove
```

Plugins should be placed under:

```text
src/archpack/plugins/<plugin-name>/
```

Each plugin should have one descriptor file:

```text
src/archpack/plugins/<plugin-name>/plugin.yml
```

A plugin is recognized by placement, descriptor, and owner review.

Plugins should not run implicitly during core `unpack` or `repair`.

---

## 5. Reviewed plugin: effective AGENTS.md generation

The first reviewed plugin is effective `AGENTS.md` generation.

Location:

```text
src/archpack/plugins/agents/
```

Descriptor:

```text
src/archpack/plugins/agents/plugin.yml
```

Usage guide:

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
archpack agents-generate <pack-dir> --out <dir> --overwrite
```

Behavior:

```text
parent rules + local rules = generated AGENTS.md
```

Each local rule unit is limited to 30 rules.

Output examples:

```text
AGENTS.md
src/AGENTS.md
src/services/AGENTS.md
```

This plugin remains outside the core and only runs through explicit command invocation.

---

## 6. Open questions for agents plugin

The reviewed agents plugin now generates effective files, but some policy checks are still intentionally deferred.

Open questions:

- How should child rules that weaken parent rules be detected?
- Should duplicate rules be collapsed?
- Should generated files include stronger machine-readable markers?
- Should generated `AGENTS.md` files have a hard total line limit, separate from the 30-rule local unit limit?

---

## 7. Future candidates

These are useful but not confirmed for the core.

They should be considered only after concrete user stories justify them.

- Generated-file drift check.
- Clean-up.
- Reference monitoring.
- Network monitoring.
- Semantic architecture drift checks.
- File-level `*.agent.md`.
- Formal schema validation.
- Plugin list / disable / remove / doctor commands.
- `.archpack` config, state, and cache.
- A package-manager-like plugin system.

---

## 8. Development discipline

Do not expand the core unless the problem clearly belongs to the core.

Default decision rule:

```text
core only when necessary
plugin when optional
remove when not worth maintaining
```

The core should remain easy to explain:

```text
pack directory → file tree → explicit repair
```

New behavior must be small, reviewed, tested, documented, and removable.
