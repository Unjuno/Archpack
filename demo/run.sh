#!/usr/bin/env bash
# Archpack Taskflow demo (macOS / Linux)
# Run from repository root: bash demo/run.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

PACK="$REPO_ROOT/demo/pack"
OUT="$REPO_ROOT/demo/workspace"

step() {
  echo ""
  echo "=== $1 ==="
}

step "0. Install archpack"
python -m pip install -q -e ".[dev]"

step "1. Clean demo/workspace"
rm -rf "$OUT"
mkdir -p "$OUT"

step "2. unpack — deploy Taskflow project from pack/tree"
archpack unpack "$PACK" --out "$OUT"

step "3. agents-generate — apply agents.toml to AGENTS.md files"
archpack agents-generate "$PACK" --out "$OUT"

step "4. repair — restore deleted docs/commands.md"
rm -f "$OUT/docs/commands.md"
archpack repair "$PACK" --out "$OUT"

step "5. Verify Taskflow app and tests in workspace"
(
  cd "$OUT"
  python -m pip install -q -e ".[dev]"
  python -m pytest -q
  python -m taskflow add "Archpack demo task"
  python -m taskflow add "Edit demo/pack/agents.toml then agents-generate --overwrite"
  python -m taskflow list
)

step "Generated AGENTS.md locations"
for rel in AGENTS.md docs/AGENTS.md src/taskflow/AGENTS.md src/taskflow/services/AGENTS.md; do
  if [[ -f "$OUT/$rel" ]]; then
    echo "  ok  $rel"
  else
    echo "  MISSING $rel"
  fi
done

echo ""
echo "Effective rules sample (src/taskflow/services/AGENTS.md):"
head -n 22 "$OUT/src/taskflow/services/AGENTS.md"
echo ""
echo "Next: edit demo/pack/agents.toml, then:"
echo "  archpack agents-generate demo/pack --out demo/workspace --overwrite"
