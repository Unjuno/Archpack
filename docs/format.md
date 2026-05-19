# Archpack format notes

## 0. Purpose

This document records the current core pack format.

The implemented core loop is:

```text
pack directory → file tree → explicit repair
```

The core format is intentionally small. Plugin-specific input formats are documented separately.

---

## 1. Current core format

The core pack format does not require YAML.

The human-authored format is an actual directory tree.

Example:

```text
architecture-pack/
└─ tree/
   ├─ README.md
   ├─ docs/
   │  └─ architecture.md
   └─ src/
      └─ app.py
```

Running Archpack on this pack generates:

```text
README.md
docs/architecture.md
src/app.py
```

The same pack directory is also the source for explicit repair.

The file name and directory structure are represented by the filesystem.
There is no need to rewrite the same structure in YAML for the core format.

---

## 2. Core commands and behavior

Implemented core commands:

```text
archpack unpack <pack-dir> --out <dir>
archpack unpack <pack-dir> --out <dir> --skip-existing
archpack repair <pack-dir> --out <dir>
archpack repair <pack-dir> --out <dir> --overwrite
```

Behavior summary:

| Command | Existing files | Missing files | Changed files |
|---|---|---|---|
| `unpack` | stop with error | write | stop before overwrite |
| `unpack --skip-existing` | skip | write | keep existing |
| `repair` | skip | write | keep existing |
| `repair --overwrite` | overwrite | write | overwrite |

---

## 3. Why not YAML for file names

Writing file names and file bodies inside YAML is too tedious for the main authoring format.

Rejected as canonical core format:

```yaml
files:
  - id: readme
    path: README.md
    content: |
      # Example project

  - id: src_app
    path: src/app.py
    content: |
      print("hello")
```

Problems:

- It duplicates the file tree in text form.
- Large file contents become awkward.
- Editors cannot treat generated files as normal files before unpacking.
- Diffs become harder to review.
- The user must maintain both metadata and content in one place.

This may still be useful for tests, APIs, or generated examples, but not as the preferred human-authored format.

---

## 4. Directory pack model

Preferred core pack model:

```text
architecture-pack/
└─ tree/
   └─ <files to generate or repair>
```

The `tree/` directory is copied into the output directory during generation.

The same `tree/` directory is used as the source of truth during explicit repair.

Core job:

```text
read source tree → validate paths → write output tree
```

Repair job:

```text
read source tree → compare output tree → restore requested generated files
```

---

## 5. Repair policy

Explicit repair is part of the core.

Repair means:

- the user explicitly asks Archpack to repair,
- Archpack uses the pack directory as the source,
- Archpack restores output files from `tree/`,
- Archpack does not monitor continuously,
- Archpack does not decide semantic correctness.

Default repair behavior:

```text
repair missing files only
```

Overwriting changed files requires:

```text
repair --overwrite
```

---

## 6. Plugin-specific formats

Plugin-specific input is not part of the core format.

The first reviewed plugin is the AGENTS.md generator.
Its input is documented separately:

```text
docs/plugins/agents.md
```

Current agents plugin input:

```text
agents.toml
```

Core commands do not read `agents.toml`.
Only the explicit plugin command reads it:

```text
archpack agents-generate <pack-dir> --out <dir>
```

---

## 7. Metadata and IDs

Metadata is not required for the current core.

If metadata becomes necessary later, it can be added as a separate file.

Possible future options:

```text
architecture-pack/pack.yml
architecture-pack/pack.json
architecture-pack/pack.toml
```

Do not choose a metadata format before there is a concrete need.

IDs are also not required for the current core.
They may become useful later for validation messages, manifests, plugin output, repair checks, or references from plugin sections.

Current decision:

```text
Core:
  no required metadata
  no required IDs

Plugin layer:
  may define its own input files
```

---

## 8. Empty directories

The core should focus on files.

Empty directories are not a priority.

If needed, users can include a placeholder file such as:

```text
.gitkeep
```

A first-class empty directory rule can be reconsidered later.

---

## 9. Tab-indented tree notation

A tab-indented tree notation is not needed if the pack itself is a directory tree.

Rejected as canonical format:

```text
README.md
src/
	app.py
	helpers.py
docs/
	architecture.md
```

Reason:

- The actual filesystem already represents hierarchy.
- A tree text file adds a second representation of the same structure.
- Tabs and spaces become semantically dangerous.
- File contents still need to live somewhere else.

A tree text format may be useful later as a helper or converter, but not as the canonical core format.

---

## 10. Summary

Current decision:

```text
Core format:
  directory-based pack

Core source of file names:
  filesystem paths under tree/

Core metadata:
  not required

Core IDs:
  not required

Plugin formats:
  outside core
  documented per plugin

Reviewed plugin format:
  agents plugin reads agents.toml
```
