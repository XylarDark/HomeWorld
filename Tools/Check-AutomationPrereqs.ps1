# Check-AutomationPrereqs.ps1 - Verify prerequisites for the 30-day automation loop.
# Run from project root: .\Tools\Check-AutomationPrereqs.ps1
# See docs/AUTOMATION_READINESS.md "Before you start" for how to fix any missing item.

param(
    [string]$ProjectRoot = ""
)

if (-not $ProjectRoot) { $ProjectRoot = $env:HOMEWORLD_PROJECT }
if (-not $ProjectRoot) { $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")

$allOk = $true

# 1. Cursor Agent CLI
$agentCmd = Get-Command agent -ErrorAction SilentlyContinue
if (-not $agentCmd) {
    Write-Host "FAIL: Cursor Agent CLI (agent) not found in PATH. Install from https://cursor.com/docs/cli/overview"
    $allOk = $false
} else {
    Write-Host "OK: Cursor Agent CLI found at $($agentCmd.Source)"
}

# 2. UE_EDITOR
if (-not $env:UE_EDITOR -or [string]::IsNullOrWhiteSpace($env:UE_EDITOR)) {
    Write-Host "FAIL: UE_EDITOR environment variable is not set. Set it to your UnrealEditor.exe path (see docs/AUTOMATION_READINESS.md)"
    $allOk = $false
} elseif (-not (Test-Path -LiteralPath $env:UE_EDITOR)) {
    Write-Host "FAIL: UE_EDITOR is set to '$env:UE_EDITOR' but that path does not exist."
    $allOk = $false
} else {
    Write-Host "OK: UE_EDITOR is set and file exists: $env:UE_EDITOR"
}

# 3. Required state files
$statusPath = Join-Path $ProjectRoot "docs\workflow\30_DAY_IMPLEMENTATION_STATUS.md"
$promptPath = Join-Path $ProjectRoot "docs\workflow\NEXT_SESSION_PROMPT.md"
if (-not (Test-Path $statusPath)) {
    Write-Host "FAIL: 30_DAY_IMPLEMENTATION_STATUS.md not found at docs/workflow/"
    $allOk = $false
} else {
    Write-Host "OK: 30_DAY_IMPLEMENTATION_STATUS.md exists"
}
if (-not (Test-Path $promptPath)) {
    Write-Host "FAIL: NEXT_SESSION_PROMPT.md not found at docs/workflow/"
    $allOk = $false
} else {
    Write-Host "OK: NEXT_SESSION_PROMPT.md exists"
}

# Auth cannot be verified without running the agent; just remind
Write-Host ""
if ($allOk) {
    Write-Host "All checks passed. Ensure you have run 'agent login' (or set CURSOR_API_KEY) before running the loop."
    Write-Host "To start the loop: .\Tools\RunAutomationLoop.ps1  (Editor auto-launches when UE_EDITOR set; use -NoLaunchEditor to skip)"
    exit 0
} else {
    Write-Host "Fix the items above, then run this script again. See docs/AUTOMATION_READINESS.md 'Before you start'."
    exit 1
}
