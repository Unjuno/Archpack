# Agents plugin usage

## 0. Purpose

The `agents` plugin generates `AGENTS.md` files from a small `agents.toml` file.

It supports directory-level local rule blocks and writes effective `AGENTS.md` files.

Effective means:

```text
parent rules + local rules = generated AGENTS.md
```

This plugin is explicit.
It does not run during core `unpack` or `repair`.

---

## 1. Quick start: write and run

Create a pack directory with `agents.toml`:

```text
my-pack/
└─ agents.toml
```

Write local rules per directory:

```toml
[[agents]]
dir = "."
rules = [
  "Keep instructions short.",
]

[[agents]]
dir = "src"
rules = [
  "Keep application code under src.",
]
```

Run the plugin:

```bash
archpack agents-generate my-pack --out tmp/out
```

Generated output:

```text
tmp/out/AGENTS.md
tmp/out/src/AGENTS.md
```

`src/AGENTS.md` includes both root rules and `src` rules.

---

## 2. Hierarchy notation

Hierarchy is written with `dir` paths.

Use `.` for the output root:

```toml
[[agents]]
dir = "."
rules = ["Root rule"]
```

Use slash-separated relative paths for child directories:

```toml
[[agents]]
dir = "src"
rules = ["Src rule"]

[[agents]]
dir = "src/services"
rules = ["Services rule"]
```

This means:

```text
.
└─ src
   └─ services
```

Generated files:

```text
AGENTS.md
src/AGENTS.md
src/services/AGENTS.md
```

Inherited rule behavior:

| `dir` | Generated file | Included rules |
|---|---|---|
| `.` | `AGENTS.md` | `.` |
| `src` | `src/AGENTS.md` | `.` + `src` |
| `src/services` | `src/services/AGENTS.md` | `.` + `src` + `src/services` |

Do not use tab-indented trees inside `agents.toml`.
Do not use absolute paths.
Do not use `..` path escapes.

---

## 3. Plugin location

The plugin lives under:

```text
src/archpack/plugins/agents/
```

The plugin descriptor is:

```text
src/archpack/plugins/agents/plugin.yml
```

---

## 4. Input file

The plugin reads:

```text
agents.toml
```

Example:

```toml
[[agents]]
dir = "."
rules = [
  "Keep instructions short.",
  "Do not add network behavior unless explicitly requested.",
]

[[agents]]
dir = "src"
rules = [
  "Keep application code under src.",
]

[[agents]]
dir = "src/services"
rules = [
  "Keep service rules in service modules.",
]
```

Each `[[agents]]` block defines local rules for one directory.

| Field | Meaning |
|---|---|
| `dir` | Output directory relative to `--out` |
| `rules` | Local bullet rules for that directory |

---

## 5. Rule limits

Each `[[agents]]` block is one local rule unit.

Current limit:

```text
max 30 rules per local unit
```

Rules must be one-line strings.
Empty rules are rejected.
Duplicate `dir` blocks are rejected.

There is no warning for the total generated `AGENTS.md` size.

Reason:

- The 30-rule limit is for each local rule unit, not for inherited output size.
- Normal project directory depth is limited by practical filesystem and path-length constraints.
- Extremely deep inheritance is not a primary case for Archpack.
- The constraint is local-unit readability, not total generated-file length.

---

## 6. Effective generation

Generated files include inherited parent rules.

Input:

```text
.
src
src/services
```

Output:

```text
AGENTS.md
src/AGENTS.md
src/services/AGENTS.md
```

Effective rule behavior:

| Output file | Included rules |
|---|---|
| `AGENTS.md` | `.` rules |
| `src/AGENTS.md` | `.` rules + `src` rules |
| `src/services/AGENTS.md` | `.` rules + `src` rules + `src/services` rules |

---

## 7. Generate AGENTS.md files

Run:

```bash
archpack agents-generate examples/agents-pack --out tmp/agents-out
```

Expected output paths:

```text
tmp/agents-out/AGENTS.md
tmp/agents-out/src/AGENTS.md
```

If the input contains deeper directories, deeper `AGENTS.md` files are generated too.

---

## 8. Default overwrite behavior

By default, existing `AGENTS.md` files are skipped.

This protects local edits.

```bash
archpack agents-generate examples/agents-pack --out tmp/agents-out
```

Behavior:

| Output file exists? | Behavior |
|---|---|
| no | write file |
| yes | skip file |

---

## 9. Explicit overwrite

Use `--overwrite` only when you intentionally want to replace existing `AGENTS.md` files.

```bash
archpack agents-generate examples/agents-pack --out tmp/agents-out --overwrite
```

Behavior:

| Output file exists? | Behavior |
|---|---|
| no | write file |
| yes | overwrite file |

---

## 10. What this plugin does not do

This plugin does not:

- warn on total generated `AGENTS.md` length,
- detect contradictory rules,
- decide whether child rules weaken parent rules,
- monitor files,
- repair generated `AGENTS.md` automatically,
- run during `unpack` or `repair`.

Those behaviors require separate review before being added.

---

## 11. Test coverage

Current tests cover:

- loading `agents.toml`,
- generating root and subdirectory `AGENTS.md`,
- inheriting parent rules into child `AGENTS.md`,
- enforcing the 30-rule local unit limit,
- skipping existing files by default,
- overwriting only with `--overwrite`,
- CLI behavior for `agents-generate`.
