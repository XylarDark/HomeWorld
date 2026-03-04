# RunAutomationLoop.ps1 - Fully automatic 30-day automation loop using Cursor Agent CLI.
# Repeatedly runs the Cursor agent with the prompt from NEXT_SESSION_PROMPT.md until no days are pending.
#
# Prerequisites:
#   - Cursor Agent CLI installed (see https://cursor.com/docs/cli/overview). On Windows, install per Cursor docs.
#   - Authenticated: run "agent login" once, or set CURSOR_API_KEY for headless use.
#   - For Unreal tasks that need MCP: start the Unreal Editor (and ensure Unreal MCP is available) before running this script.
#
# Usage: From project root, .\Tools\RunAutomationLoop.ps1 [-ProjectRoot <path>] [-PromptFile <path>] [-NoLaunchEditor] [-Model <name>]
#   -ProjectRoot: Project root (default: parent of Tools, or HOMEWORLD_PROJECT env).
#   -PromptFile: Path to prompt file (default: docs/workflow/NEXT_SESSION_PROMPT.md under project root).
#   -NoLaunchEditor: Do not auto-launch the Editor; run without it (e.g. headless). By default the loop launches the Editor before the first round when UE_EDITOR is set and the Editor is not running.
#   -Model: CLI model to use (default: "auto"). The Agent CLI uses this, not Cursor in-app settings. Use "auto" to avoid Opus usage limits; run "agent models" to list names. Pass "" to use CLI default.
#   -AgentPath: Full path to agent.exe (or agent.cmd). Use if agent is not on PATH (e.g. after install, restart terminal to refresh PATH; or pass this to point to the CLI executable).
#   -Verbose: Log prompt preview and elapsed time per round; helps confirm progress and detect stalls.
#
# Do not pipe this script's output through Select-Object -First N; that can cause agent/CLI issues (see docs/AUTOMATION_LOOP_UNTIL_DONE.md).
# Use -Verbose for extra progress lines (prompt preview, elapsed time).

param(
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,  # when not set: auto-launch Editor before first round if UE_EDITOR set and Editor not running
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$Verbose  # prompt preview + elapsed time per round
)

$ErrorActionPreference = "Stop"

# File logging: progress and errors so you can tell if work is still being done and report errors to chat
$SavedDir = $null   # set after ProjectRoot
$LoopLogPath = $null
$LastActivityPath = $null
$ErrorsLogPath = $null

function Write-LoopLog {
    param([string]$Message, [switch]$IsError)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $Message"
    Write-Host $line
    if ($LoopLogPath) {
        try {
            Add-Content -Path $LoopLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue
        } catch {}
    }
    if ($LastActivityPath) {
        try {
            $roundNum = if ($null -ne $script:CurrentRound) { $script:CurrentRound } else { 0 }
            Set-Content -Path $LastActivityPath -Value (@{ timestamp = $ts; message = $Message; round = $roundNum } | ConvertTo-Json -Compress) -Encoding UTF8 -ErrorAction SilentlyContinue
        } catch {}
    }
    if ($IsError -and $ErrorsLogPath) {
        try {
            Add-Content -Path $ErrorsLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue
        } catch {}
    }
}

# Resolve project root
if (-not $ProjectRoot) { $ProjectRoot = $env:HOMEWORLD_PROJECT }
if (-not $ProjectRoot) { $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
if (-not (Test-Path $ProjectRoot)) {
    Write-Error "Project root not found: $ProjectRoot"
    exit 1
}

$StatusPath = Join-Path $ProjectRoot "docs\workflow\30_DAY_IMPLEMENTATION_STATUS.md"
if (-not (Test-Path $StatusPath)) {
    Write-Error "Status file not found: $StatusPath"
    exit 1
}

# Set up file logging (Survives terminal crash; use for "is it still running?" and error reporting)
$SavedDir = Join-Path $ProjectRoot "Saved"
$LogsDir = Join-Path $SavedDir "Logs"
if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }
$LoopLogPath = Join-Path $LogsDir "automation_loop.log"
$LastActivityPath = Join-Path $SavedDir "automation_last_activity.json"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"
$script:RunHistoryPath = Join-Path $LogsDir "agent_run_history.ndjson"
$script:CurrentRound = 0
Write-LoopLog "RunAutomationLoop: logging to $LoopLogPath; last activity to $LastActivityPath; errors to $ErrorsLogPath; run history to $script:RunHistoryPath"

# Resolve prompt file
if (-not $PromptFile) { $PromptFile = Join-Path $ProjectRoot "docs\workflow\NEXT_SESSION_PROMPT.md" }
else { $PromptFile = Join-Path $ProjectRoot $PromptFile }

$DefaultPrompt = "Continue the automatic development cycle. Read docs/workflow/DAILY_STATE.md, docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md, and docs/SESSION_LOG.md. Work on the first day in 30_DAY_IMPLEMENTATION_STATUS that is still pending (or execute the plan in .cursor/plans/ if the prompt references one). When you finish a day's implementation work, set that day to done in 30_DAY_IMPLEMENTATION_STATUS and update DAILY_STATE and SESSION_LOG. Then create a short implementation plan for the next pending day (goal, key steps, task doc link, success criteria) and save it to .cursor/plans/dayN-<slug>.md (e.g. day7-resource-nodes.md), or embed the plan steps in NEXT_SESSION_PROMPT.md. Write the next recommended prompt into docs/workflow/NEXT_SESSION_PROMPT.md so the next session executes that plan (e.g. reference the plan file or include the steps)."

function Get-PromptText {
    if (-not (Test-Path $PromptFile)) { return $DefaultPrompt }
    $content = Get-Content -Path $PromptFile -Raw -Encoding UTF8
    if (-not $content) { return $DefaultPrompt }
    # Extract block between first and second "---", or everything after first "---" if only one fence
    $parts = $content -split "---", 3
    if ($parts.Count -ge 2 -and $parts[1].Trim()) {
        $candidate = $parts[1].Trim()
        if ($candidate -ne "---") { return $candidate }
    }
    # Fallback: use first non-empty paragraph (skip "---" and headers)
    $line = ($content -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -and $_ -notmatch "^\#|^\*\*" -and $_ -ne "---" } | Select-Object -First 1)
    if ($line) { return $line }
    return $DefaultPrompt
}

function Test-HasPendingDays {
    $text = Get-Content -Path $StatusPath -Raw -Encoding UTF8
    return ($text -match "\|\s*pending\s*\|")
}

function Test-EditorRunning {
    $out = & tasklist /FI "IMAGENAME eq UnrealEditor.exe" /NH 2>$null
    return ($out -match "UnrealEditor\.exe")
}

function Start-EditorAndWaitForMCP {
    if (-not $env:UE_EDITOR -or -not (Test-Path -LiteralPath $env:UE_EDITOR)) {
        Write-Error "Editor launch requires UE_EDITOR env set to UnrealEditor.exe path (e.g. C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe)."
        exit 1
    }
    $cycleScript = Join-Path $ProjectRoot "Content\Python\run_automation_cycle.py"
    if (-not (Test-Path $cycleScript)) {
        Write-Error "Orchestrator script not found: $cycleScript"
        exit 1
    }
    Write-LoopLog "RunAutomationLoop: launching Editor and waiting for MCP port 55557..."
    Push-Location $ProjectRoot
    try {
        & python $cycleScript --no-build --launch-and-wait
        $exit = $LASTEXITCODE
        if ($exit -ne 0) {
            Write-Error "Editor launch/wait failed (exit $exit). Check UE_EDITOR and run_automation_cycle.py."
            exit $exit
        }
        $readyPath = Join-Path $ProjectRoot "Saved\cycle_editor_ready.json"
        if (Test-Path $readyPath) {
            Write-LoopLog "RunAutomationLoop: Editor ready (cycle_editor_ready.json present)."
        }
    } finally {
        Pop-Location
    }
}

# Resolve agent CLI executable
$agentExe = $null
if ($AgentPath -and (Test-Path -LiteralPath $AgentPath)) {
    $agentExe = $AgentPath
} else {
    $agentCmd = Get-Command agent -ErrorAction SilentlyContinue
    if ($agentCmd) { $agentExe = $agentCmd.Source }
}
if (-not $agentExe) {
    Write-Error @"
Cursor Agent CLI (agent) not found in PATH.

Install (Windows PowerShell): irm 'https://cursor.com/install?win32=true' | iex
Then close and reopen your terminal so PATH is updated, or run: .\Tools\Start-AutomationSession.ps1 (installs CLI if needed and starts the loop).

See https://cursor.com/docs/cli/overview and run 'agent login' after install.
"@
    exit 1
}

# Auto-launch Editor before first round when UE_EDITOR is set and Editor not running (unless -NoLaunchEditor)
if (-not $NoLaunchEditor) {
    if ($env:UE_EDITOR -and (Test-Path -LiteralPath $env:UE_EDITOR)) {
        if (-not (Test-EditorRunning)) {
            Start-EditorAndWaitForMCP
        } else {
            Write-LoopLog "RunAutomationLoop: Editor already running; skipping launch."
        }
    } else {
        Write-LoopLog "RunAutomationLoop: UE_EDITOR not set or invalid; skipping Editor launch. Set UE_EDITOR to UnrealEditor.exe path for auto-launch."
    }
} else {
    Write-LoopLog "RunAutomationLoop: NoLaunchEditor; running without launching Editor."
}

$round = 0
do {
    $round++
    $script:CurrentRound = $round
    $prompt = Get-PromptText
    Write-LoopLog "RunAutomationLoop: === Round $round ==="
    Write-LoopLog "RunAutomationLoop: workspace=$ProjectRoot"
    $agentArgs = @("-p", "-f", "--approve-mcps", "--workspace", $ProjectRoot)
    if ($Model -and $Model.Trim()) {
        $agentArgs += "--model", $Model.Trim()
        Write-LoopLog "RunAutomationLoop: model=$($Model.Trim())"
    }
    if ($Verbose) {
        $preview = $prompt -replace "[\r\n]+", " "
        if ($preview.Length -gt 100) { $preview = $preview.Substring(0, 100) + "..." }
        Write-LoopLog "RunAutomationLoop: prompt preview: $preview"
    }
    Write-LoopLog "RunAutomationLoop: invoking agent (output streams below; no new lines for several minutes can mean agent is working or stalled)..."
    $roundStart = Get-Date
    & $agentExe @agentArgs $prompt
    $exitCode = $LASTEXITCODE
    $elapsed = (Get-Date) - $roundStart
    Write-LoopLog "RunAutomationLoop: agent finished in $([math]::Round($elapsed.TotalMinutes, 1))m, exit code=$exitCode"
    # Append run record for strategy refinement (actions and errors → rules and strategy)
    $errSummary = ""
    if ($exitCode -ne 0 -and (Test-Path -LiteralPath $ErrorsLogPath)) {
        $lines = Get-Content -Path $ErrorsLogPath -Tail 10 -ErrorAction SilentlyContinue
        $errSummary = if ($lines) { ($lines -join " ") -replace "[\r\n]+", " " } else { "" }
        if ($errSummary.Length -gt 800) { $errSummary = $errSummary.Substring(0, 800) }
    }
    $appendScript = Join-Path $PSScriptRoot "Append-AgentRunRecord.ps1"
    if (Test-Path -LiteralPath $appendScript) {
        & $appendScript -ProjectRoot $ProjectRoot -Role main -Round $round -ExitCode $exitCode -ErrorSummary $errSummary
    }
    if ($exitCode -ne 0) {
        Write-LoopLog "RunAutomationLoop: ERROR round=$round exitCode=$exitCode (paste Saved/Logs/automation_errors.log into chat to fix)" -IsError
        if ($exitCode -eq -1073740791) {
            Write-LoopLog "RunAutomationLoop: This exit code often means API usage limit or CLI crash. Switch model, set Spend Limit, or try after cycle resets. See README-Automation.md." -IsError
        }
        exit $exitCode
    }
    $stillPending = Test-HasPendingDays
    if ($stillPending) {
        Write-LoopLog "RunAutomationLoop: pending days remain; starting next round."
    }
} while ($stillPending)

Write-LoopLog "RunAutomationLoop: no pending days; done."
exit 0
