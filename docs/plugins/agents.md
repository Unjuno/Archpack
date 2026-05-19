# Agents plugin usage

## 0. Purpose

The `agents` plugin generates `AGENTS.md` files from a small `agents.toml` file.

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
```

Each `[[agents]]` block defines one output `AGENTS.md` file.

| Field | Meaning |
|---|---|
| `dir` | Output directory relative to `--out` |
| `rules` | Bullet rules to write into that directory's `AGENTS.md` |

---

## 3. Generate AGENTS.md files

Run:

```bash
archpack agents-generate examples/agents-pack --out tmp/agents-out
```

Expected output paths:

```text
tmp/agents-out/AGENTS.md
tmp/agents-out/src/AGENTS.md
```

---

## 4. Default overwrite behavior

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

## 5. Explicit overwrite

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

## 6. What this plugin does not do

This first plugin version does not:

- generate inherited effective `AGENTS.md`,
- merge parent and child rules,
- detect contradictory rules,
- monitor files,
- repair generated `AGENTS.md` automatically,
- run during `unpack` or `repair`.

Those behaviors require separate review before being added.

---

## 7. Test coverage

Current tests cover:

- loading `agents.toml`,
- generating root and subdirectory `AGENTS.md`,
- skipping existing files by default,
- overwriting only with `--overwrite`,
- CLI behavior for `agents-generate`.
