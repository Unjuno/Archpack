# Agents plugin usage

## 0. Purpose

The `agents` plugin manages `AGENTS.md` files from a small `agents.toml` file.

`agents.toml` is the source of truth.
Generated `AGENTS.md` files are outputs.

It supports directory-level local rule blocks and writes **scoped** `AGENTS.md` files.

Scoped means:

```text
local rules for that directory + a short navigation hint
```

Child `AGENTS.md` files do not copy parent rules.
Agents should read guidance by walking from the repository root toward the target directory.

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

`src/AGENTS.md` contains only the local `src` rules plus a pointer to read `../AGENTS.md` first.

Do not edit generated `AGENTS.md` files directly.
Edit `agents.toml`, then run `agents-generate` again.

---

## 2. Source-of-truth rule

Manage agent instructions in one file:

```text
agents.toml
```

Generated files such as these are derived outputs:

```text
AGENTS.md
src/AGENTS.md
src/services/AGENTS.md
```

This keeps architecture instructions centralized and easier to review.

If generated files become stale, update `agents.toml` and regenerate.

Use `--overwrite` only when you intentionally want to replace existing generated `AGENTS.md` files.

---

## 3. Hierarchy notation

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

Scoped rule behavior:

| `dir` | Generated file | Included rules |
|---|---|---|
| `.` | `AGENTS.md` | `.` only |
| `src` | `src/AGENTS.md` | `src` only + parent navigation |
| `src/services` | `src/services/AGENTS.md` | `src/services` only + parent navigation |

Do not use tab-indented trees inside `agents.toml`.
Do not use absolute paths.
Do not use `..` path escapes.

---

## 4. Plugin location

The plugin lives under:

```text
src/archpack/plugins/agents/
```

The plugin descriptor is:

```text
src/archpack/plugins/agents/plugin.yml
```

---

## 5. Input file

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

## 6. Rule limits

Each `[[agents]]` block is one local rule unit.

Current limit:

```text
max 30 rules per local unit
```

Rules must be one-line strings.
Empty rules are rejected.
Duplicate `dir` blocks are rejected.

There is no inherited output size to manage because parent rules are not copied into child `AGENTS.md` files.

---

## 7. Scoped generation

Generated files include only their own local rules.

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

Scoped rule behavior:

| Output file | Included rules |
|---|---|
| `AGENTS.md` | `.` rules |
| `src/AGENTS.md` | `src` rules |
| `src/services/AGENTS.md` | `src/services` rules |

Non-root files include a short navigation hint:

```text
Read parent guidance first:

- `../AGENTS.md`
```

The root file tells agents to read each `AGENTS.md` on the path from repository root to the target directory.

---

## 8. Generate AGENTS.md files

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

## 9. Default overwrite behavior

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

## 10. Explicit overwrite

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

## 11. What this plugin does not do

This plugin does not:

- copy parent rules into child `AGENTS.md` files,
- warn on total generated `AGENTS.md` length,
- detect contradictory rules,
- decide whether child rules weaken parent rules,
- monitor files,
- repair generated `AGENTS.md` automatically,
- run during `unpack` or `repair`.

Those behaviors require separate review before being added.

---

## 12. Test coverage

Current tests cover:

- loading `agents.toml`,
- generating root and subdirectory `AGENTS.md`,
- keeping generated files scoped to local rules,
- adding parent navigation hints to non-root generated files,
- enforcing the 30-rule local unit limit,
- skipping existing files by default,
- overwriting only with `--overwrite`,
- CLI behavior for `agents-generate`.
