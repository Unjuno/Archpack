# Archpack demonstration — Taskflow

This demo deploys a **working small CLI app (Taskflow)** and **per-directory `AGENTS.md` files** with Archpack. It is not an empty skeleton: rules in `agents.toml` are written into each generated `AGENTS.md`.

## Layout

| Kind | Path | Role |
|------|------|------|
| Pack (source of truth) | `demo/pack/` | `tree/` + `agents.toml` |
| Deploy target | `demo/workspace/` | Output of unpack / agents-generate (gitignored) |
| Agent rules (edit this) | `demo/pack/agents.toml` | **Hand-edited source file** |
| Generated agent docs | `demo/workspace/**/AGENTS.md` | **Regenerate only; do not edit by hand** |

### Pack input

```text
demo/pack/
├── agents.toml              # source of truth for agent rules
└── tree/
    ├── README.md
    ├── pyproject.toml
    ├── docs/
    │   ├── architecture.md
    │   └── commands.md
    ├── src/taskflow/        # runnable CLI package
    │   ├── cli.py
    │   ├── models.py
    │   └── services/store.py
    └── tests/test_store.py
```

### After unpack + agents-generate

```text
demo/workspace/
├── AGENTS.md                         # repository-wide rules
├── docs/
│   ├── AGENTS.md                     # docs rules (parent + local)
│   ├── architecture.md
│   └── commands.md
├── src/taskflow/
│   ├── AGENTS.md                     # package rules (parent + src/taskflow)
│   ├── cli.py …
│   └── services/
│       ├── AGENTS.md                 # effective: . + src/taskflow + services
│       └── store.py
└── tests/ …
```

`src/taskflow/services/AGENTS.md` includes applicable rules from **root, src/taskflow, and services** (effective / inherited generation). The `docs/` tree is a sibling, so its rules are not included there.

---

## One-command run

From the repository root:

```powershell
.\demo\run.ps1
```

```bash
bash demo/run.sh
```

The script will:

1. Install `archpack`
2. `unpack` the Taskflow project
3. `agents-generate` **four `AGENTS.md` files**
4. `repair` a deleted file to show recovery
5. Run `pytest` and the `taskflow` CLI under `demo/workspace`

---

## Step by step (what gets deployed)

### 0. Setup

```powershell
cd C:\path\to\Archpack
python -m pip install -e ".[dev]"
```

### 1. Clean workspace

```powershell
Remove-Item -Recurse -Force demo\workspace -ErrorAction SilentlyContinue
New-Item -ItemType Directory demo\workspace | Out-Null
```

### 2. Deploy the project tree

```powershell
archpack unpack demo\pack --out demo\workspace
```

Deploys everything under `tree/` (Python package, docs, tests).

### 3. Apply AGENTS.md rules

```powershell
archpack agents-generate demo\pack --out demo\workspace
```

Deploys:

- `AGENTS.md`
- `docs/AGENTS.md`
- `src/taskflow/AGENTS.md`
- `src/taskflow/services/AGENTS.md`

### 4. Change rules and regenerate

After editing `demo/pack/agents.toml`:

```powershell
archpack agents-generate demo\pack --out demo\workspace --overwrite
```

Generated `AGENTS.md` files are instructions for tools that read directory-scoped agent docs. **The canonical source is always `agents.toml`.**

### 5. Run the app

```powershell
cd demo\workspace
python -m pip install -e ".[dev]"
python -m taskflow add "Try the Archpack demo"
python -m taskflow add "Regenerate AGENTS.md after editing agents.toml"
python -m taskflow list
python -m pytest -q
```

### 6. Verify repair

```powershell
cd C:\path\to\Archpack
Remove-Item demo\workspace\docs\commands.md
archpack repair demo\pack --out demo\workspace
```

Only the missing `docs/commands.md` is restored from the pack.

---

## agents.toml vs AGENTS.md

| `dir` in agents.toml | Generated file | Typical focus |
|----------------------|----------------|---------------|
| `.` | `AGENTS.md` | Project-wide policy, dependencies, verify commands |
| `docs` | `docs/AGENTS.md` | Keep docs aligned with the CLI |
| `src/taskflow` | `src/taskflow/AGENTS.md` | Package layout, errors, stdlib-only |
| `src/taskflow/services` | `src/taskflow/services/AGENTS.md` | Store boundary, import constraints |

---

## Cleanup

```powershell
Remove-Item -Recurse -Force demo\workspace
```

`demo/workspace/` and `.taskflow/` under it are generated artifacts and are not committed.
