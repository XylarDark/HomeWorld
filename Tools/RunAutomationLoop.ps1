# RunAutomationLoop.ps1 - Fully automatic loop using Cursor Agent CLI.
# Repeatedly runs the Cursor agent with the prompt from NEXT_SESSION_PROMPT.md until the current task list (CURRENT_TASK_LIST.md) has no pending or in_progress tasks, or stop is requested.
#
# Exit conditions (only these should stop the loop):
#   (1) Task list complete: no task has status pending or in_progress -> exit 0 (success; generate new task list and re-run when ready).
#   (2) User stop: Saved/Logs/agent_stop_requested exists at round start -> exit 0 (graceful stop).
#   (3) Failure (Watcher will run Fixer, then re-run loop): agent exit non-zero, agent timeout, Safe-Build failed after round, or prerequisite missing (no task list, no project root, no agent exe, Editor launch failed) -> exit non-zero.
# The loop must NOT exit 0 while CURRENT_TASK_LIST still has any task with status pending or in_progress. The agent must complete exactly one task per round and set only that task to completed; see default prompt and NEXT_SESSION_PROMPT.md.
#
# Canonical workflow (fetch task -> implement -> decide build/Editor -> validate in Editor -> debug until success -> finish -> fetch next):
#   The Developer fetches the task, implements work, and when the task requires it validates in Editor (MCP, PIE, pie_test_runner).
#   When C++ or .Build.cs files are modified after a successful round, this loop runs Safe-Build and fails the round (exit 1) if the build fails, so the Fixer runs (debug loop).
#
# Prerequisites:
#   - Cursor Agent CLI installed (see https://cursor.com/docs/cli/overview). On Windows, install per Cursor docs.
#   - Authenticated: run "agent login" once, or set CURSOR_API_KEY for headless use.
#   - For Unreal tasks that need MCP: start the Unreal Editor (and ensure Unreal MCP is available) before running this script.
#
# Usage: From project root, .\Tools\RunAutomationLoop.ps1 [-ProjectRoot <path>] [-PromptFile <path>] [-NoLaunchEditor] [-Model <name>] [-BuildBeforeFirstRound] [-AgentTimeoutMinutes <n>]
#   -ProjectRoot: Project root (default: parent of Tools, or HOMEWORLD_PROJECT env).
#   -PromptFile: Path to prompt file (default: docs/workflow/NEXT_SESSION_PROMPT.md under project root).
#   -NoLaunchEditor: Do not auto-launch the Editor; run without it (e.g. headless). By default the loop launches the Editor before the first round when UE_EDITOR is set and the Editor is not running.
#   -Model: CLI model to use (default: "auto"). The Agent CLI uses this, not Cursor in-app settings. Use "auto" to avoid Opus usage limits; run "agent models" to list names. Pass "" to use CLI default.
#   -AgentPath: Full path to agent.exe (or agent.cmd). Use if agent is not on PATH (e.g. after install, restart terminal to refresh PATH; or pass this to point to the CLI executable).
#   -Verbose: Log prompt preview and elapsed time per round; helps confirm progress and detect stalls.
#   -BuildBeforeFirstRound: Run a full build before the first round (default: false). Use for a clean baseline; the loop will still run Safe-Build after any round that modifies Source/ or *.Build.cs.
#
# Do not pipe this script's output through Select-Object -First N; that can cause agent/CLI issues (see docs/AUTOMATION_LOOP_UNTIL_DONE.md).
# Use -Verbose for extra progress lines (prompt preview, elapsed time).
#
# Note: This script parses and runs correctly under PowerShell. Some IDE linters (e.g. PowerShell extension)
# may report false positives for brace/do-loop parsing; the runtime parser handles the file correctly.

param(
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,  # when not set: auto-launch Editor before first round if UE_EDITOR set and Editor not running
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$Verbose,  # prompt preview + elapsed time per round
    [switch]$BuildBeforeFirstRound,  # when set: run Safe-Build before first round for clean baseline; default false
    [int]$AgentTimeoutMinutes = 90,  # kill agent and exit 1 (Fixer runs) if agent runs longer than this; heartbeat every 1 min so Get-AutomationStatus shows progress
    [switch]$NoStallProtection,       # when set: do not start Watch-HeartbeatStall (default is to start it so stalled agents are killed after StallThresholdMinutes with no heartbeat)
    [int]$StallThresholdMinutes = 15 # if heartbeat not updated for this many minutes, stall watcher kills agent (only when -NoStallProtection not set)
)

$ErrorActionPreference = "Stop"

# Shared helper for UE_EDITOR (avoids Test-Path -LiteralPath $null)
$commonScript = Join-Path $PSScriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }

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

# Returns $true if any modified (uncommitted) file is under Source/ or is a *.Build.cs file (build required).
# If git is unavailable or the command fails, returns $true (conservative).
function Test-CppOrBuildFilesModified {
    $root = $ProjectRoot
    if (-not $root) { return $true }
    try {
        $status = & git -C $root status --porcelain 2>$null
        if ($LASTEXITCODE -ne 0) { return $true }
        foreach ($line in $status) {
            if (-not $line) { continue }
            $path = $null
            if ($line.Length -ge 4 -and $line.Substring(0, 2) -eq "??") {
                $path = $line.Substring(3).Trim()
            } else {
                $path = $line.Substring(3).Trim()
            }
            $path = $path -replace '^"|"$', ''
            $norm = $path -replace '\\', '/'
            if ($norm -match '^Source/') { return $true }
            if ($norm -match '\.Build\.cs$') { return $true }
        }
        return $false
    } catch {
        return $true
    }
}

# Resolve project root (shared helper)
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd('\', '/')
if (-not (Test-Path $ProjectRoot)) {
    Write-Error "Project root not found: $ProjectRoot"
    exit 1
}

$TaskListPath = Join-Path $ProjectRoot "docs\workflow\CURRENT_TASK_LIST.md"
if (-not (Test-Path -LiteralPath $TaskListPath)) {
    Write-Error "Task list not found: $TaskListPath. Create it from docs/workflow/CURRENT_TASK_LIST_TEMPLATE.md or see docs/workflow/HOW_TO_GENERATE_TASK_LIST.md."
    exit 1
}

# Set up file logging (Survives terminal crash; use for "is it still running?" and error reporting)
$SavedDir = Join-Path $ProjectRoot "Saved"
$LogsDir = Join-Path $SavedDir "Logs"
if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }
$LoopLogPath = Join-Path $LogsDir "automation_loop.log"
$LastActivityPath = Join-Path $SavedDir "automation_last_activity.json"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"
$StatusLatestPath = Join-Path $LogsDir "automation_status_latest.txt"
$EventsLogPath = Join-Path $LogsDir "automation_events.log"
$script:RunHistoryPath = Join-Path $LogsDir "agent_run_history.ndjson"
$script:CurrentRound = 0
# Clear previous exit alert so the agentic chat only surfaces the most recent exit (this run will write a new one when it exits)
$prevAlertMd = Join-Path $LogsDir "automation_exit_alert.md"
$prevAlertJson = Join-Path $LogsDir "automation_exit_alert.json"
if (Test-Path -LiteralPath $prevAlertMd) { Remove-Item -LiteralPath $prevAlertMd -Force -ErrorAction SilentlyContinue }
if (Test-Path -LiteralPath $prevAlertJson) { Remove-Item -LiteralPath $prevAlertJson -Force -ErrorAction SilentlyContinue }
Write-LoopLog "RunAutomationLoop: logging to $LoopLogPath; last activity to $LastActivityPath; errors to $ErrorsLogPath; run history to $script:RunHistoryPath"

# Resolve prompt file
if (-not $PromptFile) { $PromptFile = Join-Path $ProjectRoot "docs\workflow\NEXT_SESSION_PROMPT.md" }
else { $PromptFile = Join-Path $ProjectRoot $PromptFile }

$DefaultPrompt = "Continue the automatic development cycle. Read docs/workflow/DAILY_STATE.md, docs/workflow/CURRENT_TASK_LIST.md, and docs/SESSION_LOG.md. Work only on tasks T1-T10 in CURRENT_TASK_LIST.md. Work on the first task that is pending or in_progress. Do not add new task sections (T11, T12, etc); if you discover work that deserves a new task, document it in SESSION_LOG or docs/AUTOMATION_GAPS.md for the next task-list generation. Complete exactly one task per round. When you finish a task you MUST update docs/workflow/CURRENT_TASK_LIST.md: change ONLY that task's line '- **status:** pending' or '- **status:** in_progress' to '- **status:** completed'; do not change any other task's status. Saving this file is required so the loop does not re-run the same tasks. Also update DAILY_STATE and SESSION_LOG and write the next recommended prompt into docs/workflow/NEXT_SESSION_PROMPT.md. The loop will invoke you again for the next pending task until T1-T10 are done. If you change C++ or Build.cs, the loop will run a build after this round. When the task requires in-Editor validation, run it (e.g. execute_python_script('pie_test_runner.py')) and exit non-zero if it fails so the Fixer runs."

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

# Only T1-T10 drive the loop. Do not count T11+; do not add new task sections (document in SESSION_LOG or AUTOMATION_GAPS).
# Returns: @{ PendingCount = N; FirstPendingId = "Tk" or $null; FirstPendingGoal = "short goal..." or $null; PendingIds = @("T1","T2",...); ExtraSectionsWarning = $true if file has ## T11+ }
function Get-TaskListState {
    if (-not (Test-Path -LiteralPath $TaskListPath)) {
        return @{ PendingCount = 0; FirstPendingId = $null; FirstPendingGoal = $null; PendingIds = @(); ExtraSectionsWarning = $false }
    }
    $text = Get-Content -Path $TaskListPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $text) {
        return @{ PendingCount = 0; FirstPendingId = $null; FirstPendingGoal = $null; PendingIds = @(); ExtraSectionsWarning = $false }
    }
    $pendingCount = 0
    $firstPendingId = $null
    $firstPendingGoal = $null
    $pendingIds = [System.Collections.ArrayList]@()
    $extraSections = $false
    # Use \z (end of string) not $ so we don't stop at every line end in multiline mode
    $sectionPattern = '(?m)^## T(\d+)\.\s*([\s\S]*?)(?=^## T\d+\.|\z)'
    $matches = [regex]::Matches($text, $sectionPattern)
    foreach ($m in $matches) {
        $tNum = [int]$m.Groups[1].Value
        if ($tNum -lt 1 -or $tNum -gt 10) {
            $extraSections = $true
            continue
        }
        $block = $m.Groups[2].Value
        $isPending = ($block -match 'status:.*(pending|in_progress)')
        if ($isPending) {
            $pendingCount++
            [void]$pendingIds.Add("T$tNum")
            if (-not $firstPendingId) {
                $firstPendingId = "T$tNum"
                $goalMatch = [regex]::Match($block, '-\s*\*\*goal:\*\*\s*(.+?)(?=\r?\n|$)')
                if ($goalMatch.Success) {
                    $g = $goalMatch.Groups[1].Value.Trim() -replace '\s+', ' '
                    if ($g.Length -gt 70) { $g = $g.Substring(0, 67) + "..." }
                    $firstPendingGoal = $g
                } else {
                    $firstPendingGoal = "(see CURRENT_TASK_LIST)"
                }
            }
        }
    }
    return @{ PendingCount = $pendingCount; FirstPendingId = $firstPendingId; FirstPendingGoal = $firstPendingGoal; PendingIds = $pendingIds; ExtraSectionsWarning = $extraSections }
}

function Test-HasPendingTasks {
    $state = Get-TaskListState
    return ($state.PendingCount -gt 0)
}

function Get-PendingTaskCount {
    $state = Get-TaskListState
    return $state.PendingCount
}

# Run status report and write exit-alert file when the loop is about to exit.
# The alert file is read by the agentic chat when you ask "automation update" or "check automation exit".
function Invoke-ExitStatusAlert {
    param(
        [string]$ExitReason = "Unknown",
        [int]$ExitCode = 0
    )
    $alertDir = $LogsDir
    $alertMd = Join-Path $alertDir "automation_exit_alert.md"
    $alertJson = Join-Path $alertDir "automation_exit_alert.json"
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $round = if ($null -ne $script:CurrentRound) { $script:CurrentRound } else { 0 }
    $lastMsg = '-'
    if (Test-Path -LiteralPath $LastActivityPath) {
        try {
            $last = Get-Content -Path $LastActivityPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $lastMsg = $last.message
        } catch {}
    }
    $taskState = Get-TaskListState
    $hasPending = ($taskState.PendingCount -gt 0)
    $pendingText = if ($hasPending) { 'Yes (loop would continue if restarted)' } else { 'No (task list complete or N/A)' }
    $summary = ('Loop exited: {0}. Exit code {1}. Round {2}. Pending tasks: {3}. Last message: {4}' -f $ExitReason, $ExitCode, $round, $pendingText, $lastMsg)
    $tasksComplete = ($ExitReason -eq 'No pending tasks; done')
    $tasksCompletePath = Join-Path $alertDir 'automation_tasks_complete.md'
    if ($tasksComplete) {
        $nextStep = "## Next step`n`nAll tasks in CURRENT_TASK_LIST are complete. **Generate a new task list** (see docs/workflow/HOW_TO_GENERATE_TASK_LIST.md) and run **.\Tools\Start-AllAgents.ps1** when ready. When generating the next list, read docs/workflow/TASK_LIST_REPEATS_LOG.md and ACCOMPLISHMENTS_OVERVIEW.md §4 to avoid repeating completed work."
    } else {
        if (Test-Path -LiteralPath $tasksCompletePath) { Remove-Item -LiteralPath $tasksCompletePath -Force -ErrorAction SilentlyContinue }
        $nextStep = ""
    }
    # Build "unable to accomplish" section for CLI and alert file: what still needs to be documented and addressed next run.
    $unableList = @()
    if ($taskState.PendingIds -and $taskState.PendingIds.Count -gt 0) {
        $unableList += "Tasks still not done: $($taskState.PendingIds -join ', ') (see docs/workflow/CURRENT_TASK_LIST.md)."
    }
    if ($ExitCode -ne 0) {
        $unableList += "This run ended with an error; see Saved/Logs/automation_errors.log and automation_exit_alert.md for details."
    }
    $unableBlurb = "Document any deferred or blocked work in docs/SESSION_LOG.md, docs/AUTOMATION_GAPS.md, or task docs. The next run will include research and solution-making for these items."
    $unableSection = @()
    if ($unableList.Count -gt 0) {
        $unableSection += "--- What we were unable to accomplish ---"
        foreach ($line in $unableList) { $unableSection += $line }
    }
    $unableSection += $unableBlurb
    $unableForFile = if ($unableList.Count -gt 0) {
        "`n`n## What we were unable to accomplish (document for next round)`n`n" + ($unableList -join " `n").Trim() + "`n`n**Next round:** " + $unableBlurb
    } else {
        "`n`n## What we were unable to accomplish`n`nNone this run (task list complete or N/A). " + $unableBlurb
    }
    try {
        $mdContent = (
            '# Automation exit alert',
            '',
            "**Time:** $ts  ",
            "**Exit reason:** $ExitReason  ",
            "**Exit code:** $ExitCode  ",
            "**Round:** $round  ",
            "**Pending tasks:** $pendingText  ",
            "**Last activity:** $lastMsg  ",
            '',
            '**Full terminal output (for Fixer and chat):** Saved/Logs/automation_terminal_capture.log  ',
            '',
            '## Tell the user',
            '',
            $summary,
            $nextStep,
            $unableForFile,
            '',
            'To get this update in chat, say: Give me the automation update or Check automation exit. The agent will read this file and summarize.'
        ) -join "`n"
        Set-Content -Path $alertMd -Value $mdContent -Encoding UTF8 -ErrorAction Stop
    } catch {}
    # CLI alert at end of session: what was unable to be accomplished and that it must be documented for next round.
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  WHAT WE WERE UNABLE TO ACCOMPLISH" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    if ($unableList.Count -gt 0) {
        foreach ($line in $unableList) { Write-Host "  * $line" }
    } else {
        Write-Host "  (None this run; task list complete or N/A.)"
    }
    Write-Host ""
    Write-Host "  Document deferred/blocked work in: docs/SESSION_LOG.md, docs/AUTOMATION_GAPS.md, or task docs." -ForegroundColor Yellow
    Write-Host "  The next run will include research and solution-making for these items." -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    if ($tasksComplete) {
        try {
            $completeContent = (
                '# Tasks complete - ready for new task list',
                '',
                'All tasks in **docs/workflow/CURRENT_TASK_LIST.md** are complete.',
                '',
                '**Next step:** Generate a new task list, then start the agents again.',
                '',
                '1. See **docs/workflow/HOW_TO_GENERATE_TASK_LIST.md** (template, validation, optional 30-day migration).',
                '2. Read **docs/workflow/TASK_LIST_REPEATS_LOG.md** and **ACCOMPLISHMENTS_OVERVIEW.md** §4 so the new list does not duplicate completed work.',
                '3. Update or replace **docs/workflow/CURRENT_TASK_LIST.md** with your new 10 tasks (T1-T10).',
                '4. Run **.\Tools\Start-AllAgents.ps1** from project root.',
                '',
                'The agent will alert you when this file exists so you know to create the next task list.'
            ) -join "`n"
            Set-Content -Path $tasksCompletePath -Value $completeContent -Encoding UTF8 -ErrorAction Stop
        } catch {}
    }
    try {
        $obj = @{
            timestamp = $ts
            exit_reason = $ExitReason
            exit_code = $ExitCode
            round = $round
            pending_tasks = $hasPending
            last_message = $lastMsg
            summary = $summary
            tasks_complete = $tasksComplete
        }
        $obj | ConvertTo-Json -Compress | Set-Content -Path $alertJson -Encoding UTF8 -ErrorAction Stop
    } catch {}
    # Optional: Slack/Discord webhook on exit (opt-in; no URLs in repo). See docs/AUTOMATION_LOOP_UNTIL_DONE.md.
    $webhookPath = Join-Path $alertDir 'automation_slack_webhook.txt'
    if (Test-Path -LiteralPath $webhookPath) {
        try {
            $webhookUrl = (Get-Content -Path $webhookPath -Raw -Encoding UTF8 -ErrorAction Stop).Trim()
            if ($webhookUrl -and $webhookUrl.StartsWith('http')) {
                $webhookMsg = if ($tasksComplete) { "All tasks complete. Generate a new task list (see HOW_TO_GENERATE_TASK_LIST.md) and run Start-AllAgents when ready. " + $summary } else { $summary }
                $body = @{ text = $webhookMsg; content = $webhookMsg } | ConvertTo-Json -Compress
                Invoke-RestMethod -Method Post -Uri $webhookUrl -Body $body -ContentType 'application/json; charset=utf-8' -ErrorAction Stop
            }
        } catch {}
    }
    $statusScript = Join-Path $PSScriptRoot 'Get-AutomationStatus.ps1'
    if (Test-Path -LiteralPath $statusScript) {
        Write-Host ""
        & $statusScript -Short
    }
}

function Test-EditorRunning {
    $out = & tasklist /FI "IMAGENAME eq UnrealEditor.exe" /NH 2>$null
    return ($out -match "UnrealEditor\.exe")
}

function Start-EditorAndWaitForMCP {
    if (-not (Test-UE_EDITORSet)) {
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

# Resolve agent CLI executable (shared helper)
$agentExe = Get-AgentExe -AgentPath $AgentPath
if (-not $agentExe) {
    $errMsg = 'Cursor Agent CLI (agent) not found in PATH.' + "`n`n" +
        'Install (Windows PowerShell): irm ''https://cursor.com/install?win32=true'' | Invoke-Expression' + "`n" +
        'Then close and reopen your terminal so PATH is updated, or run: .\Tools\Start-AutomationSession.ps1 (installs CLI if needed and starts the loop).' + "`n`n" +
        'See https://cursor.com/docs/cli/overview and run ''agent login'' after install.'
    Write-Error $errMsg
    exit 1
}

# Optional: build before first round for clean baseline (default: false)
if ($BuildBeforeFirstRound) {
    Write-LoopLog 'RunAutomationLoop: BuildBeforeFirstRound; running Safe-Build...'
    Push-Location $ProjectRoot
    try {
        & (Join-Path $PSScriptRoot "Safe-Build.ps1")
        if ($LASTEXITCODE -ne 0) {
            Write-LoopLog "RunAutomationLoop: Safe-Build failed (BuildBeforeFirstRound). See Build-HomeWorld.log." -IsError
            Write-AutomationEvent -EventType build_failed -Message "Safe-Build failed (BuildBeforeFirstRound). See Build-HomeWorld.log."
            if ($ErrorsLogPath) {
                Add-Content -Path $ErrorsLogPath -Value "RunAutomationLoop: Safe-Build failed (BuildBeforeFirstRound). See Build-HomeWorld.log." -Encoding UTF8 -ErrorAction SilentlyContinue
            }
            Invoke-ExitStatusAlert -ExitReason "Safe-Build failed (BuildBeforeFirstRound)" -ExitCode 1
            exit 1
        }
        Write-LoopLog "RunAutomationLoop: Safe-Build succeeded; continuing to Editor launch and first round."
        Write-AutomationEvent -EventType build_validated -Message "Safe-Build succeeded; continuing to Editor launch and first round."
    } finally {
        Pop-Location
    }
}

# Auto-launch Editor before first round when UE_EDITOR is set and Editor not running (unless -NoLaunchEditor)
if (-not $NoLaunchEditor) {
    if (Test-UE_EDITORSet) {
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

$StopSentinelPath = Join-Path $LogsDir "agent_stop_requested"
# Clear stop sentinel at start so this run is not immediately stopped (user may have created it to stop a previous run)
if (Test-Path -LiteralPath $StopSentinelPath) {
    Remove-Item -LiteralPath $StopSentinelPath -Force -ErrorAction SilentlyContinue
    Write-LoopLog "RunAutomationLoop: cleared agent_stop_requested from previous run."
}

# Stall protection: background process that kills the agent if heartbeat has not updated for StallThresholdMinutes (so the loop can exit and Fixer can run)
if (-not $NoStallProtection) {
    $stallWatcherPath = Join-Path $PSScriptRoot "Watch-HeartbeatStall.ps1"
    if (Test-Path -LiteralPath $stallWatcherPath) {
        try {
            Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $stallWatcherPath, "-ParentPID", $pid, "-ProjectRoot", $ProjectRoot, "-StallThresholdMinutes", $StallThresholdMinutes, "-CheckIntervalMinutes", "3" -WindowStyle Hidden -ErrorAction SilentlyContinue
            Write-LoopLog "RunAutomationLoop: started stall watcher (kill agent if no heartbeat for $StallThresholdMinutes min); log Saved/Logs/stall_watcher.log"
        } catch {
            Write-LoopLog "RunAutomationLoop: could not start stall watcher: $_" -IsError
        }
    }
}

$round = 0
# Single-instance guard: lock so Start-AllAgents-InNewWindow refuses to open a second loop (prevents two CLIs and task-list conflicts)
Set-AutomationLoopLock
try {
do {
    if (Test-Path -LiteralPath $StopSentinelPath) {
        Write-LoopLog "RunAutomationLoop: Stop requested (agent_stop_requested present); exiting loop."
        Write-AutomationEvent -EventType loop_exited_ok -Message "Stop requested (agent_stop_requested)."
        Invoke-ExitStatusAlert -ExitReason "Stop requested (agent_stop_requested)" -ExitCode 0
        exit 0
    }
    $round++
    $script:CurrentRound = $round
    # Cap at 10 rounds per run so we never loop forever if the task list is reset or agent keeps repopulating pending.
    if ($round -gt 10) {
        Write-LoopLog "RunAutomationLoop: max rounds (10) reached; exiting. Fix CURRENT_TASK_LIST.md if tasks were not marked completed, then restart."
        Write-AutomationEvent -EventType loop_exited_ok -Message "Max rounds (10) reached; exiting."
        Invoke-ExitStatusAlert -ExitReason "Max rounds (10) reached" -ExitCode 0
        exit 0
    }
    # Before running the agent: if there are no pending/in_progress tasks, exit 0 (task list already complete; do not run agent).
    if (-not (Test-HasPendingTasks)) {
        $n = Get-PendingTaskCount
        Write-LoopLog ('RunAutomationLoop: no pending or in_progress tasks in T1-T10 ({0} remaining); task list complete. Exiting.' -f $n)
        Write-AutomationEvent -EventType loop_exited_ok -Message "No pending tasks; task list complete."
        Invoke-ExitStatusAlert -ExitReason 'No pending tasks; done' -ExitCode 0
        exit 0
    }
    $prompt = Get-PromptText
    $taskState = Get-TaskListState
    $pendingCountAtStart = $taskState.PendingCount
    if ($taskState.ExtraSectionsWarning) {
        Write-LoopLog "RunAutomationLoop: WARNING - CURRENT_TASK_LIST has sections beyond T10; only T1-T10 drive the loop. Document new work in SESSION_LOG or docs/AUTOMATION_GAPS.md." -IsError
    }
    Write-LoopLog "RunAutomationLoop: === Round $round === ($pendingCountAtStart of 10 tasks pending or in_progress)"
    if ($taskState.FirstPendingId) {
        $currentTaskMsg = "Working on first pending task: " + $taskState.FirstPendingId + " - " + $taskState.FirstPendingGoal
        Write-LoopLog "RunAutomationLoop: $currentTaskMsg"
        Write-AutomationEvent -EventType task_started -Message $currentTaskMsg
    }
    # Live status file: one-line summary so you can tail without re-running Get-AutomationStatus (see docs/AUTOMATION_LOOP_UNTIL_DONE.md)
    $pendingYN = if (Test-HasPendingTasks) { 'Y' } else { 'N' }
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $pipe = " | "
    $statusLine = if ($taskState.FirstPendingId) {
        "[$ts] round=$round Working on $($taskState.FirstPendingId)$pipe$($taskState.FirstPendingGoal)"
    } else {
        "[$ts] round=$round Round starting$pipe pending=$pendingYN"
    }
    try {
        Set-Content -Path $StatusLatestPath -Value $statusLine -Encoding UTF8 -ErrorAction SilentlyContinue
    } catch {}
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
    $HeartbeatLogPath = Join-Path $LogsDir "automation_heartbeat.log"
    Write-LoopLog ('RunAutomationLoop: invoking agent (timeout {0}m; heartbeat every 1m with progress log at Saved/Logs/automation_heartbeat.log)...' -f $AgentTimeoutMinutes)
    $roundStart = Get-Date
    $tempExitFile = Join-Path $LogsDir "agent_exit_round_$round.txt"
    $job = Start-Job -ScriptBlock {
        param($exe, $argsArray, $promptText, $exitFile)
        & $exe @argsArray $promptText
        $LASTEXITCODE | Set-Content -Path $exitFile -Force -ErrorAction SilentlyContinue
    } -ArgumentList $agentExe, $agentArgs, $prompt, $tempExitFile
    $timeoutSec = [math]::Max(60, $AgentTimeoutMinutes * 60)
    $heartbeatSec = 60
    $deadline = (Get-Date).AddSeconds($timeoutSec)
    $lastHeartbeat = Get-Date
    # Track log line counts so each heartbeat can report "work since last heartbeat"
    $script:HeartbeatLastEventsCount = 0
    if (Test-Path -LiteralPath $EventsLogPath) { $script:HeartbeatLastEventsCount = (Get-Content -Path $EventsLogPath -Encoding UTF8 -ErrorAction SilentlyContinue | Measure-Object -Line).Lines }
    $script:HeartbeatLastLoopCount = 0
    if (Test-Path -LiteralPath $LoopLogPath) { $script:HeartbeatLastLoopCount = (Get-Content -Path $LoopLogPath -Encoding UTF8 -ErrorAction SilentlyContinue | Measure-Object -Line).Lines }
    do {
        $jobState = (Get-Job -Id $job.Id -ErrorAction SilentlyContinue).State
        if ($jobState -ne 'Running' -and $jobState -ne 'Blocked') { break }
        if ((Get-Date) -ge $deadline) {
            Stop-Job -Id $job.Id -ErrorAction SilentlyContinue
            Remove-Job -Id $job.Id -Force -ErrorAction SilentlyContinue
            Remove-Item -Path $tempExitFile -Force -ErrorAction SilentlyContinue
            Write-LoopLog "RunAutomationLoop: agent timed out after $AgentTimeoutMinutes minutes (stalled). Exiting so Fixer can run. Increase -AgentTimeoutMinutes if tasks are legitimately long." -IsError
            Write-AutomationEvent -EventType loop_exited_fail -Message "Agent timed out after $AgentTimeoutMinutes minutes (stalled). Fixer will run."
            if ($ErrorsLogPath) { Add-Content -Path $ErrorsLogPath -Value "RunAutomationLoop: agent timed out after $AgentTimeoutMinutes minutes (stalled)." -Encoding UTF8 -ErrorAction SilentlyContinue }
            Invoke-ExitStatusAlert -ExitReason "Agent timed out (stalled)" -ExitCode 1
            exit 1
        }
        if (((Get-Date) - $lastHeartbeat).TotalSeconds -ge $heartbeatSec) {
            $lastHeartbeat = Get-Date
            $elapsedM = [math]::Round(((Get-Date) - $roundStart).TotalMinutes, 1)
            $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            Write-LoopLog ('RunAutomationLoop: agent still running (heartbeat; elapsed {0}m)...' -f $elapsedM)
            try {
                # --- Work since last heartbeat (new lines in events + loop logs) ---
                $eventsLines = @()
                if (Test-Path -LiteralPath $EventsLogPath) {
                    $eventsLines = Get-Content -Path $EventsLogPath -Encoding UTF8 -ErrorAction SilentlyContinue
                }
                $loopLines = @()
                if (Test-Path -LiteralPath $LoopLogPath) {
                    $loopLines = Get-Content -Path $LoopLogPath -Encoding UTF8 -ErrorAction SilentlyContinue
                }
                $curEventsCount = $eventsLines.Count
                $curLoopCount = $loopLines.Count
                $newEvents = @()
                if ($script:HeartbeatLastEventsCount -lt $curEventsCount) {
                    $newEvents = $eventsLines[$script:HeartbeatLastEventsCount..($curEventsCount - 1)] | ForEach-Object { $_.Trim() } | Where-Object { $_ }
                }
                $newLoop = @()
                if ($script:HeartbeatLastLoopCount -lt $curLoopCount) {
                    $newLoop = $loopLines[$script:HeartbeatLastLoopCount..($curLoopCount - 1)] | ForEach-Object { $_.Trim() } | Where-Object { $_ }
                }
                $sinceParts = @()
                $joinSep = " | "
                if ($newEvents.Count -gt 0) {
                    $sinceParts += "Events: " + (($newEvents | Select-Object -Last 5) -join $joinSep)
                }
                if ($newLoop.Count -gt 0) {
                    $sinceParts += "Loop: " + (($newLoop | Select-Object -Last 5) -join $joinSep)
                }
                $sinceSummary = if ($sinceParts.Count -gt 0) { $sinceParts -join " " } else { "No new high-level events; agent still working (elapsed ${elapsedM}m)." }
                # --- What happens next ---
                $nextTask = if ($taskState.FirstPendingId) { "next pending: " + $taskState.FirstPendingId + " - " + $taskState.FirstPendingGoal } else { "no pending (T1-T10 complete)" }
                $nextSummary = "When agent exits: exit 0 -> Safe-Build if C++/Build.cs changed, then next round ($nextTask) or exit. Exit non-zero -> Fixer runs."
                # Write full heartbeat block
                $heartbeatLine = "[$ts] round=$round | elapsed=${elapsedM}m | agent running"
                $heartbeatBlock = @(
                    $heartbeatLine,
                    "--- Since last heartbeat ---",
                    $sinceSummary,
                    "--- Next ---",
                    $nextSummary
                ) -join "`n"
                Add-Content -Path $HeartbeatLogPath -Value $heartbeatBlock -Encoding UTF8 -ErrorAction SilentlyContinue
                $heartbeatMsg = "Round $round (elapsed ${elapsedM}m): $sinceSummary Next: $nextSummary"
                if ($heartbeatMsg.Length -gt 600) { $heartbeatMsg = $heartbeatMsg.Substring(0, 597) + "..." }
                Set-Content -Path $LastActivityPath -Value (@{ timestamp = $ts; message = $heartbeatMsg; round = $round } | ConvertTo-Json -Compress) -Encoding UTF8 -ErrorAction SilentlyContinue
                $statusNext = if ($taskState.FirstPendingId) { " next: $($taskState.FirstPendingId)" } else { " next: exit if done" }
                Set-Content -Path $StatusLatestPath -Value "[$ts] round=$round agent running | elapsed=${elapsedM}m$statusNext" -Encoding UTF8 -ErrorAction SilentlyContinue
                $script:HeartbeatLastEventsCount = $curEventsCount
                $script:HeartbeatLastLoopCount = $curLoopCount
            } catch {}
        }
        Start-Sleep -Seconds 15
    } while ($true)
    Receive-Job -Id $job.Id -ErrorAction SilentlyContinue | Out-Null
    Remove-Job -Id $job.Id -Force -ErrorAction SilentlyContinue
    $exitCode = 0
    if (Test-Path -LiteralPath $tempExitFile) {
        $ec = Get-Content -Path $tempExitFile -Raw -ErrorAction SilentlyContinue
        if ($ec -match '^-?\d+$') { $exitCode = [int]$ec }
        Remove-Item -Path $tempExitFile -Force -ErrorAction SilentlyContinue
    }
    $elapsed = (Get-Date) - $roundStart
    Write-LoopLog "RunAutomationLoop: agent finished in $([math]::Round($elapsed.TotalMinutes, 1))m, exit code=$exitCode"
    # Append run record for strategy refinement (actions and errors -> rules and strategy)
    $errSummary = ""
    if ($exitCode -ne 0 -and (Test-Path -LiteralPath $ErrorsLogPath)) {
        $lines = Get-Content -Path $ErrorsLogPath -Tail 10 -ErrorAction SilentlyContinue
        $errSummary = if ($lines) { ($lines -join ' ') -replace '[\r\n]+', ' ' } else { '' }
        if ($errSummary.Length -gt 800) { $errSummary = $errSummary.Substring(0, 800) }
    }
    $appendScript = Join-Path $PSScriptRoot "Append-AgentRunRecord.ps1"
    if (Test-Path -LiteralPath $appendScript) {
        & $appendScript -ProjectRoot $ProjectRoot -Role main -Round $round -ExitCode $exitCode -ErrorSummary $errSummary -Model $Model
    }
    if ($exitCode -ne 0) {
        Write-LoopLog "RunAutomationLoop: ERROR round=$round exitCode=$exitCode (paste Saved/Logs/automation_errors.log into chat to fix)" -IsError
        Write-AutomationEvent -EventType loop_exited_fail -Message "Exit code $exitCode (round $round). Fixer will run."
        if ($exitCode -eq -1073740791) {
            Write-LoopLog "RunAutomationLoop: This exit code often means API usage limit or CLI crash. Switch model, set Spend Limit, or try after cycle resets. See README-Automation.md." -IsError
        }
        # Structured handoff: write prompt preview for Watcher/Fixer (see docs/AGENT_COMPANY.md)
        $promptPreviewPath = Join-Path $LogsDir "automation_last_prompt_preview.txt"
        try {
            $preview = ($prompt -replace "[\r\n]+", " ").Trim()
            if ($preview.Length -gt 500) { $preview = $preview.Substring(0, 500) + "..." }
            Set-Content -Path $promptPreviewPath -Value $preview -Encoding UTF8 -ErrorAction SilentlyContinue
        } catch {}
        Invoke-ExitStatusAlert -ExitReason "Agent exited non-zero" -ExitCode $exitCode
        exit $exitCode
    }
    # After successful round: if C++ or Build.cs modified, run Safe-Build; on failure exit 1 so Fixer runs (debug loop)
    if (Test-CppOrBuildFilesModified) {
        Write-LoopLog "RunAutomationLoop: C++ or Build.cs modified; running Safe-Build -LaunchEditorAfter..."
        Push-Location $ProjectRoot
        try {
            & (Join-Path $PSScriptRoot "Safe-Build.ps1") -LaunchEditorAfter
            if ($LASTEXITCODE -ne 0) {
                $errMsg = "RunAutomationLoop: Safe-Build failed after round $round (C++ changed). See Build-HomeWorld.log."
                Write-LoopLog $errMsg -IsError
                Write-AutomationEvent -EventType build_failed -Message "Safe-Build failed after round $round (C++ changed). See Build-HomeWorld.log."
                if ($ErrorsLogPath) {
                    Add-Content -Path $ErrorsLogPath -Value $errMsg -Encoding UTF8 -ErrorAction SilentlyContinue
                }
                Invoke-ExitStatusAlert -ExitReason "Safe-Build failed after round (C++ changed)" -ExitCode 1
                exit 1
            }
            Write-LoopLog "RunAutomationLoop: Safe-Build succeeded; Editor relaunched for next round."
            Write-AutomationEvent -EventType build_validated -Message "Safe-Build succeeded; Editor relaunched for next round."
        } finally {
            Pop-Location
        }
    }
    # Inform the chat: write last-completion file so the in-chat agent can prepend "Round N completed" when the user returns (see 07-ai-agent-behavior.mdc).
    $lastCompletionPath = Join-Path $LogsDir "automation_last_completion.json"
    try {
        $tsRound = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $lastCompletion = @{ timestamp = $tsRound; round = $round; message = "Round $round completed successfully. CURRENT_TASK_LIST may have been updated." }
        Set-Content -Path $lastCompletionPath -Value ($lastCompletion | ConvertTo-Json -Compress) -Encoding UTF8 -ErrorAction SilentlyContinue
    } catch {}
    Write-AutomationEvent -EventType round_completed -Message "Round $round completed"
    $taskStateAfter = Get-TaskListState
    $stillPending = ($taskStateAfter.PendingCount -gt 0)
    $pendingCount = $taskStateAfter.PendingCount
    if ($stillPending) {
        $nextMsg = if ($taskStateAfter.FirstPendingId) {
            "next pending: " + $taskStateAfter.FirstPendingId + " - " + $taskStateAfter.FirstPendingGoal
        } else {
            "$pendingCount tasks pending or in_progress"
        }
        Write-LoopLog "RunAutomationLoop: pending tasks remain ($pendingCount of 10); $nextMsg; starting next round."
    } else {
        Write-LoopLog "RunAutomationLoop: no pending or in_progress tasks (T1-T10 complete); exiting."
    }
} while ($stillPending)

Write-LoopLog "RunAutomationLoop: no pending tasks; done."
Write-AutomationEvent -EventType loop_exited_ok -Message "No pending tasks; done."
Invoke-ExitStatusAlert -ExitReason 'No pending tasks; done' -ExitCode 0
exit 0
} finally {
    Remove-AutomationLoopLock
}
