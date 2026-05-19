# Archpack Taskflow demo (Windows PowerShell)
# Run from repository root: .\demo\run.ps1

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

$Pack = Join-Path $RepoRoot "demo\pack"
$Out = Join-Path $RepoRoot "demo\workspace"

function Step([string]$Title) {
    Write-Host ""
    Write-Host "=== $Title ===" -ForegroundColor Cyan
}

Step "0. Install archpack"
python -m pip install -q -e ".[dev]"

Step "1. Clean demo/workspace"
if (Test-Path $Out) {
    Remove-Item -Recurse -Force $Out
}
New-Item -ItemType Directory -Path $Out | Out-Null
Remove-Item -Recurse -Force (Join-Path $Out ".taskflow") -ErrorAction SilentlyContinue

Step "2. unpack — deploy Taskflow project from pack/tree"
archpack unpack $Pack --out $Out

Step "3. agents-generate — apply agents.toml to AGENTS.md files"
archpack agents-generate $Pack --out $Out

Step "4. repair — restore deleted docs/commands.md"
Remove-Item (Join-Path $Out "docs\commands.md") -Force
archpack repair $Pack --out $Out

Step "5. Verify Taskflow app and tests in workspace"
Push-Location $Out
Remove-Item -Recurse -Force .taskflow -ErrorAction SilentlyContinue
python -m pip install -q -e ".[dev]"
python -m pytest -q
python -m taskflow add "Archpack demo task"
python -m taskflow add "Edit demo/pack/agents.toml then agents-generate --overwrite"
python -m taskflow list
Pop-Location

Step "Generated AGENTS.md locations"
@(
    "AGENTS.md",
    "docs\AGENTS.md",
    "src\taskflow\AGENTS.md",
    "src\taskflow\services\AGENTS.md"
) | ForEach-Object {
    $path = Join-Path $Out $_
    if (Test-Path $path) { Write-Host "  ok  $_" -ForegroundColor Green } else { Write-Host "  MISSING $_" -ForegroundColor Red }
}

Write-Host ""
Write-Host "Effective rules sample (src/taskflow/services/AGENTS.md):" -ForegroundColor Yellow
Get-Content (Join-Path $Out "src\taskflow\services\AGENTS.md") | Select-Object -First 22
Write-Host ""
Write-Host "Next: edit demo\pack\agents.toml, then:" -ForegroundColor Green
Write-Host "  archpack agents-generate demo\pack --out demo\workspace --overwrite"
