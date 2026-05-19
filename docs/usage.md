# Archpack usage guide

## 0. MVP status

The MVP core is complete enough to use for the first validation loop:

```text
pack directory → file tree → explicit repair
```

Archpack currently works as a small directory-pack unpacker and explicit repair tool.

It does not enforce structure continuously.
It does not monitor the project in the background.
It does not implement plugins yet.

---

## 1. Install for local development

```bash
python -m pip install -e ".[dev]"
```

This installs the `archpack` command and the test dependency.

---

## 2. Pack directory layout

A pack is a directory that contains a `tree/` directory.

Example:

```text
examples/minimal-pack/
└─ tree/
   └─ README.md
```

Only files under `tree/` are generated into the output directory.

The file names and directory structure are represented by the actual filesystem.
YAML is not required for the MVP.

---

## 3. Generate a file tree

```bash
archpack unpack examples/minimal-pack --out tmp/out
```

This copies files from:

```text
examples/minimal-pack/tree/
```

to:

```text
tmp/out/
```

By default, `unpack` refuses to overwrite existing files.

---

## 4. Add only missing files

When an output directory already has some generated files, use:

```bash
archpack unpack examples/minimal-pack --out tmp/out --skip-existing
```

This mode:

- skips existing files,
- writes missing files,
- does not overwrite user edits,
- does not stop just because an existing file is found.

Use this when the pack gained new files and you want to add only the missing ones.

---

## 5. Explicit repair

```bash
archpack repair examples/minimal-pack --out tmp/out
```

Default repair behavior:

- restores missing files from the pack,
- skips existing files,
- does not overwrite changed files.

This is an explicit command.
Archpack does not repair files automatically.

---

## 6. Overwrite repair

```bash
archpack repair examples/minimal-pack --out tmp/out --overwrite
```

This overwrites existing output files with the version from the pack.

Use this only when you intentionally want to restore the pack version.

---

## 7. Behavior summary

| Command | Existing files | Missing files | Changed files |
|---|---|---|---|
| `unpack` | stop with error | write | stop before overwrite |
| `unpack --skip-existing` | skip | write | keep existing |
| `repair` | skip | write | keep existing |
| `repair --overwrite` | overwrite | write | overwrite |

---

## 8. Safety rules

Current safety behavior:

- `tree/` is required.
- Files outside `tree/` are not generated.
- Existing files are not overwritten by default.
- Symlinks in the pack tree are rejected.
- Parent-directory escape paths are rejected.
- Repair runs only when explicitly requested.

---

## 9. Run tests

```bash
pytest
```

Current test coverage includes:

- basic unpack,
- existing-file refusal,
- default repair for missing files,
- overwrite repair,
- symlink rejection,
- `unpack --skip-existing`.

---

## 10. Out of scope for MVP

The following are not part of the current MVP:

- `AGENTS.md` generation,
- effective inherited `AGENTS.md`,
- plugin execution,
- `.archpack/` state management,
- continuous enforcement,
- background monitoring,
- drift audit,
- clean-up,
- reference monitoring,
- network monitoring.
