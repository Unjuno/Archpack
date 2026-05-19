# Archpack format notes

## 0. Purpose

This document records the first direction for the core pack format.

It is not a final schema.
It exists to keep the MVP simple before implementation.

The core MVP remains:

```text
pack → file tree
```

---

## 1. Core idea

The core pack should describe files directly.

A file entry should have:

- an `id`,
- a `path`,
- `content`.

The `path` is the file name and structure.

Archpack should not need a separate directory tree model at first. Parent directories can be inferred from file paths.

---

## 2. Minimal direction

Example:

```yaml
version: 0.1
files:
  - id: readme
    path: README.md
    content: |
      # Example project

  - id: docs_architecture
    path: docs/architecture.md
    content: |
      # Architecture

  - id: src_app
    path: src/app.py
    content: |
      print("hello")
```

Expected output:

```text
README.md
docs/architecture.md
src/app.py
```

---

## 3. Why use IDs

IDs are useful even when paths already describe structure.

The `id` can provide a stable reference for:

- later plugin output,
- validation messages,
- generated examples,
- future manifests,
- future repair or drift checks,
- references from other pack sections.

A path can change.
An ID can remain stable.

---

## 4. ID direction

The first ID rule should be simple:

- IDs are unique within the pack.
- IDs are human-readable.
- IDs use lowercase letters, numbers, and underscores.
- IDs do not encode file extensions unless useful.

Examples:

```yaml
id: readme
id: docs_architecture
id: src_app
id: test_basic_generation
```

Do not overdesign IDs before real examples exist.

---

## 5. Directories

The core format does not need a separate `directories:` section at first.

Directory creation can be derived from file paths:

```yaml
path: docs/architecture.md
```

This implies:

```text
docs/
```

A separate directory entry can be reconsidered later if there is a concrete need, such as:

- empty directories,
- directory metadata,
- directory ownership,
- plugin-specific directory rules.

---

## 6. Tab-indented tree notation

A tab-indented tree notation is attractive for humans, but it should not be the core MVP format.

Rejected core direction:

```text
README.md
src/
	app.py
	helpers.py
docs/
	architecture.md
```

Reasons:

- It creates a custom parser before the basic pack format is proven.
- Tabs and spaces become semantically dangerous.
- YAML itself should not use tab indentation.
- File content is harder to attach cleanly to each path.
- Stable `id` references become awkward unless a second mapping is added.

The core should keep this instead:

```yaml
files:
  - id: src_app
    path: src/app.py
    content: |
      print("hello")
```

A tree-like format may be useful later as an input helper or scaffolding command, but not as the first canonical format.

Possible future direction:

```text
archpack scaffold tree
```

or:

```text
archpack convert tree.txt --to architecture-pack.yml
```

This would convert a visual tree into the canonical `files[]` format.

---

## 7. Plugin sections

Plugin-specific format should not be added to the core format until a plugin experiment proves the need.

For example, an `AGENTS.md` plugin may later add something like:

```yaml
agent_rules:
  - id: root_agent_rules
    dir: .
    rules:
      - Do not add external network calls unless explicitly allowed.
```

This belongs to the plugin, not the core MVP.

---

## 8. Format scaffolding command

Plugin format can become annoying to write by hand.

Therefore, a future plugin may provide a scaffolding command that generates a starter format section.

Possible future direction:

```text
archpack plugin scaffold agents
```

or:

```text
archpack init --plugin agents
```

This should generate a small editable example, not a large magic configuration.

Example generated section:

```yaml
agent_rules:
  - id: root_agent_rules
    dir: .
    rules:
      - Keep instructions short.
```

This is deferred until the plugin model exists.

---

## 9. Current decision

Current decision:

```text
Core MVP format:
  files[] with id, path, content

Directories:
  inferred from files[].path

Tab-indented tree format:
  not canonical for core MVP
  possible future helper/convert command

Plugins:
  deferred

Plugin scaffolding command:
  useful later, not core MVP
```
