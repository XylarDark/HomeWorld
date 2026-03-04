# Check-AutomationPrereqs.ps1 - Verify prerequisites for the automation loop.
# Run from project root: .\Tools\Check-AutomationPrereqs.ps1
# See docs/AUTOMATION_READINESS.md "Before you start" for how to fix any missing item.

param(
    [string]$ProjectRoot = ""
)

$commonScript = Join-Path $PSScriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
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
if (-not (Test-UE_EDITORSet)) {
    if (-not $env:UE_EDITOR -or [string]::IsNullOrWhiteSpace($env:UE_EDITOR)) {
        Write-Host "FAIL: UE_EDITOR environment variable is not set. Set it to your UnrealEditor.exe path (see docs/AUTOMATION_READINESS.md)"
    } else {
        Write-Host "FAIL: UE_EDITOR is set to '$env:UE_EDITOR' but that path does not exist."
    }
    $allOk = $false
} else {
    Write-Host "OK: UE_EDITOR is set and file exists: $env:UE_EDITOR"
}

# 3. Required state files (current task list drives the loop)
$taskListPath = Join-Path $ProjectRoot "docs\workflow\CURRENT_TASK_LIST.md"
$promptPath = Join-Path $ProjectRoot "docs\workflow\NEXT_SESSION_PROMPT.md"
if (-not (Test-Path -LiteralPath $taskListPath)) {
    Write-Host "FAIL: CURRENT_TASK_LIST.md not found at docs/workflow/. Create from CURRENT_TASK_LIST_TEMPLATE.md or see HOW_TO_GENERATE_TASK_LIST.md"
    $allOk = $false
} else {
    Write-Host "OK: CURRENT_TASK_LIST.md exists"
    $validateScript = Join-Path $ProjectRoot "Content\Python\validate_task_list.py"
    if (Test-Path -LiteralPath $validateScript) {
        $validateResult = & python $validateScript 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "FAIL: CURRENT_TASK_LIST.md validation failed. Run: python Content/Python/validate_task_list.py"
            Write-Host $validateResult
            $allOk = $false
        } else {
            Write-Host "OK: CURRENT_TASK_LIST.md passes validate_task_list.py"
        }
    }
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
