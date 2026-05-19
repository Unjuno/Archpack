# Archpack format notes

## 0. Purpose

This document records the first direction for the core pack format.

It is not a final schema.
It exists to keep the MVP simple before implementation.

The core MVP remains:

```text
pack directory → file tree → explicit repair
```

---

## 1. Current decision

The core pack format should not require YAML.

The simplest authoring format is an actual directory tree.

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

Running Archpack on this pack should generate:

```text
README.md
docs/architecture.md
src/app.py
```

The same pack directory should also be usable as the source for explicit repair.

The file name and directory structure are already represented by the filesystem.
There is no need to rewrite the same structure in YAML for the core MVP.

---

## 2. Why not YAML for file names

Writing file names and file bodies inside YAML is too tedious for the main authoring format.

Rejected as canonical core MVP format:

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

## 3. Directory pack model

Preferred core pack model:

```text
architecture-pack/
└─ tree/
   └─ <files to generate or repair>
```

The `tree/` directory is copied into the output directory during generation.

The same `tree/` directory is used as the source of truth during explicit repair.

The core job is therefore simple:

```text
read source tree → validate paths → write output tree
```

For repair:

```text
read source tree → compare output tree → restore requested generated files
```

---

## 4. Repair option

Explicit repair is part of the core MVP.

Repair means:

- the user explicitly asks Archpack to repair,
- Archpack uses the pack directory as the source,
- Archpack restores output files from `tree/`,
- Archpack does not monitor continuously,
- Archpack does not decide semantic correctness.

Initial repair direction:

```text
repair missing files by default
```

Overwriting changed files should require a separate explicit option if added.

---

## 5. Metadata

Metadata is not required for the core MVP.

If metadata becomes necessary later, it can be added as a separate file.

Possible future options:

```text
architecture-pack/pack.yml
architecture-pack/pack.json
architecture-pack/pack.toml
```

Do not choose a metadata format before there is a concrete need.

Possible future metadata:

- pack name,
- pack version,
- file IDs,
- plugin settings,
- overwrite policy,
- generated markers.

---

## 6. IDs

IDs are useful for future features, but they are not required for the core MVP.

Reasons IDs may become useful later:

- validation messages,
- future manifests,
- plugin output,
- repair or drift checks,
- references from plugin sections.

But forcing IDs in the core MVP makes the first format more tedious.

Current decision:

```text
Core MVP:
  no required IDs

Future metadata/plugin layer:
  may add IDs if needed
```

---

## 7. Empty directories

The core MVP should focus on files.

Empty directories are not a priority.

If needed, users can include a placeholder file such as:

```text
.gitkeep
```

A first-class empty directory rule can be reconsidered later.

---

## 8. Tab-indented tree notation

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

## 9. Plugins

Plugin-specific format should not be added to the core format until a plugin experiment proves the need.

For example, an `AGENTS.md` plugin may later add its own metadata or config.

That belongs to the plugin layer, not the core MVP.

---

## 10. Scaffolding command

A future command may create a starter pack directory.

Possible direction:

```text
archpack init pack
```

Example generated structure:

```text
architecture-pack/
└─ tree/
   └─ README.md
```

Plugin-specific scaffolding can be added later, for example:

```text
archpack plugin scaffold agents
```

This is not required for the core MVP.

---

## 11. Summary

Current decision:

```text
Core MVP format:
  directory-based pack

Core MVP behavior:
  generate file tree
  explicitly repair generated files when requested

Canonical source of file names:
  filesystem paths under tree/

YAML:
  not required for core MVP
  possible future metadata format

IDs:
  not required for core MVP
  possible future metadata/plugin feature

Plugins:
  deferred
```
