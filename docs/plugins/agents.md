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

## 1. Plugin location

The plugin lives under:

```text
src/archpack/plugins/agents/
```

The plugin descriptor is:

```text
src/archpack/plugins/agents/plugin.yml
```

---

## 2. Input file

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

## 3. Rule limits

Each `[[agents]]` block is one local rule unit.

Current limit:

```text
max 30 rules per local unit
```

Rules must be one-line strings.
Empty rules are rejected.
Duplicate `dir` blocks are rejected.

---

## 4. Effective generation

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

## 5. Generate AGENTS.md files

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

## 6. Default overwrite behavior

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

## 7. Explicit overwrite

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

## 8. What this plugin does not do

This plugin does not:

- detect contradictory rules,
- decide whether child rules weaken parent rules,
- monitor files,
- repair generated `AGENTS.md` automatically,
- run during `unpack` or `repair`.

Those behaviors require separate review before being added.

---

## 9. Test coverage

Current tests cover:

- loading `agents.toml`,
- generating root and subdirectory `AGENTS.md`,
- inheriting parent rules into child `AGENTS.md`,
- enforcing the 30-rule local unit limit,
- skipping existing files by default,
- overwriting only with `--overwrite`,
- CLI behavior for `agents-generate`.
