# Watch-AutomationAndFix.ps1 - Runs the automation loop; on failure, starts a second "fix" agent that reads error logs and fixes issues, then optionally re-runs the loop.
# Use this so one agent runs development and another agent is triggered to fix failures automatically.
#
# Usage: From project root, .\Tools\Watch-AutomationAndFix.ps1 [-MaxFixRounds <N>] [-NoLaunchEditor] [-Verbose] [same params as Start-AutomationSession]
#   -MaxFixRounds: After the main loop fails, run up to this many fix-agent sessions (default 3). Then exit and report.
#   -NoRetryAfterFix: After a fix round, do not re-run the loop; exit and let the user re-run manually.
#   Other params are passed through to Start-AutomationSession (e.g. -NoLaunchEditor to skip auto-launching the Editor, -Verbose).
#
# Flow: Run Start-AutomationSession (main loop) -> if exit 0, done. If exit != 0, run fix agent once with prompt to read Saved/Logs/automation_errors.log and fix -> if -NoRetryAfterFix, exit; else re-run loop. Repeat until loop exits 0 or we hit MaxFixRounds.

param(
    [int]$MaxFixRounds = 3,
    [switch]$NoRetryAfterFix,
    [switch]$NoPauseOnComplete,  # when set, do not pause at success (for CI/headless); default is to pause so you can confirm the loop finished normally
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$commonScript = Join-Path $PSScriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$SavedDir = Join-Path $ProjectRoot "Saved"
$LogsDir = Join-Path $SavedDir "Logs"
if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }
$WatcherLogPath = Join-Path $LogsDir "watcher.log"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"
$LoopLogPath = Join-Path $LogsDir "automation_loop.log"
$LoopBreakerReportPath = Join-Path $LogsDir "automation_loop_breaker_report.md"
$EditorOutputFullPath = Join-Path $LogsDir "editor_output_full.txt"
$EditorOutputFilteredPath = Join-Path $LogsDir "editor_output_filtered.txt"
$HandoffPath = Join-Path $LogsDir "agent_handoff.json"
$PromptPreviewPath = Join-Path $LogsDir "automation_last_prompt_preview.txt"
$EditorLogTailLines = 3000

function Write-WatcherLog {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] Watch-AutomationAndFix: $Message"
    Write-Host $line
    try { Add-Content -Path $WatcherLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue } catch {}
}

# Capture Editor Output Log on failure: copy last N lines of HomeWorld.log to editor_output_full.txt, then filter to editor_output_filtered.txt.
function Invoke-CaptureEditorLog {
    $editorLog = Join-Path $LogsDir "HomeWorld.log"
    if (-not (Test-Path -LiteralPath $editorLog)) {
        $candidates = Get-ChildItem -Path $LogsDir -Filter "*.log" -ErrorAction SilentlyContinue | Where-Object {
            $_.Name -notmatch "^(automation_loop|automation_errors|watcher|guardian|refiner|cef3)" -and $_.Name -notmatch "\.backup\."
        } | Sort-Object LastWriteTime -Descending
        if ($candidates) { $editorLog = $candidates[0].FullName }
    }
    if (-not (Test-Path -LiteralPath $editorLog)) {
        Write-WatcherLog "No Editor log file found; skipping Editor log capture."
        return
    }
    try {
        $lines = Get-Content -Path $editorLog -Tail $EditorLogTailLines -ErrorAction Stop -Encoding UTF8
        Set-Content -Path $EditorOutputFullPath -Value $lines -Encoding UTF8 -ErrorAction Stop
        Write-WatcherLog "Captured last $($lines.Count) lines of Editor log to editor_output_full.txt"
        $filterScript = Join-Path $ProjectRoot "Content\Python\filter_editor_log.py"
        if (Test-Path -LiteralPath $filterScript) {
            $env:HOMEWORLD_PROJECT = $ProjectRoot
            & python $filterScript $EditorOutputFullPath $EditorOutputFilteredPath 2>&1 | Out-Null
            if (Test-Path -LiteralPath $EditorOutputFilteredPath) {
                Write-WatcherLog "Filtered Editor log written to editor_output_filtered.txt"
            }
        }
    } catch {
        Write-WatcherLog "Editor log capture failed: $_"
    }
}

# Write structured handoff for Fixer/Guardian (see docs/AGENT_COMPANY.md). Call after Invoke-CaptureEditorLog when starting Fixer or before invoking Guardian.
function Write-AgentHandoff {
    param(
        [int]$ExitCode,
        [int]$Round,
        [string]$RoleThatFailed,
        [string]$SuggestedNextReader,
        [string]$AgentFacingSummary = $null
    )
    $lastPromptPreview = ""
    if (Test-Path -LiteralPath $PromptPreviewPath) {
        try { $lastPromptPreview = (Get-Content -Path $PromptPreviewPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue).Trim() } catch {}
    }
    $lastErrorSummary = ""
    if (Test-Path -LiteralPath $ErrorsLogPath) {
        $lines = Get-Content -Path $ErrorsLogPath -Tail 20 -ErrorAction SilentlyContinue
        $lastErrorSummary = if ($lines) { ($lines -join " ") -replace "[\r\n]+", " " } else { "" }
        if ($lastErrorSummary.Length -gt 600) { $lastErrorSummary = $lastErrorSummary.Substring(0, 600) + "..." }
    }
    $editorLogCaptured = (Test-Path -LiteralPath $EditorOutputFullPath)
    $ts = Get-Date -Format "o"
    $handoff = @{
        ts = $ts
        exit_code = $ExitCode
        round = $Round
        role_that_failed = $RoleThatFailed
        last_prompt_preview = if ($lastPromptPreview) { $lastPromptPreview } else { $null }
        last_error_summary = if ($lastErrorSummary) { $lastErrorSummary } else { $null }
        editor_log_captured = $editorLogCaptured
        suggested_next_reader = $SuggestedNextReader
        agent_facing_summary = if ($AgentFacingSummary) { $AgentFacingSummary } else { $null }
    }
    try {
        Set-Content -Path $HandoffPath -Value ($handoff | ConvertTo-Json -Depth 3) -Encoding UTF8 -ErrorAction Stop
        Write-WatcherLog "Wrote agent_handoff.json for $RoleThatFailed handoff."
    } catch {
        Write-WatcherLog "Failed to write agent_handoff.json: $_"
    }
}

$fixRound = 0
$previousExitCode = $null
do {
    Write-WatcherLog "Starting main automation loop (fix round $fixRound / $MaxFixRounds)..."
    $sessionArgs = @{ ProjectRoot = $ProjectRoot }
    $resolvedAgent = Get-AgentExe -AgentPath $AgentPath
    if ($resolvedAgent) { $sessionArgs["AgentPath"] = $resolvedAgent }
    if ($PromptFile) { $sessionArgs["PromptFile"] = $PromptFile }
    if ($NoLaunchEditor) { $sessionArgs["NoLaunchEditor"] = $true }
    if ($Model) { $sessionArgs["Model"] = $Model }
    if ($SkipInstall) { $sessionArgs["SkipInstall"] = $true }
    if ($Verbose) { $sessionArgs["Verbose"] = $true }

    $loopScript = Join-Path $PSScriptRoot "Start-AutomationSession.ps1"
    & $loopScript @sessionArgs
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-WatcherLog "Main loop exited successfully (no pending tasks or stop requested). Done."
        if (-not $NoPauseOnComplete) {
            Write-Host ""
            Write-Host "=== Loop finished successfully ===" -ForegroundColor Green
            Write-Host "Task list has no pending/in_progress tasks (or stop was requested). Below is the final status." -ForegroundColor Gray
            Write-Host ""
            $statusScript = Join-Path $PSScriptRoot "Get-AutomationStatus.ps1"
            if (Test-Path -LiteralPath $statusScript) {
                try {
                    Push-Location $ProjectRoot | Out-Null
                    & $statusScript -Short
                } finally {
                    Pop-Location | Out-Null
                }
            }
            Write-Host ""
        }
        exit 0
    }

    # Capture Editor Output Log on failure (for Fixer and Guardian). See docs/AUTOMATION_EDITOR_LOG.md.
    Invoke-CaptureEditorLog

    # Loop detection: same failure twice in a row -> run loop-breaker (third agent) instead of fix agent
    $sameFailureAgain = ($previousExitCode -ne $null -and $previousExitCode -eq $exitCode -and $fixRound -ge 1)
    if ($sameFailureAgain) {
        Write-WatcherLog "Loop detected: same exit code $exitCode again. Invoking Guardian (Guard-AutomationLoop) instead of Fixer..."
        $failRound = 1
        $lastActivityPath = Join-Path $ProjectRoot "Saved\automation_last_activity.json"
        if (Test-Path -LiteralPath $lastActivityPath) {
            try { $la = Get-Content -Path $lastActivityPath -Raw -Encoding UTF8 | ConvertFrom-Json; if ($la.round) { $failRound = [int]$la.round } } catch {}
        }
        Write-AutomationEvent -EventType guardian_invoked -Message "Guardian started (same exit code $exitCode)"
        Write-AgentHandoff -ExitCode $exitCode -Round $failRound -RoleThatFailed "Fixer" -SuggestedNextReader "Guardian: read Saved/Logs/agent_handoff.json first, then automation_errors.log, watcher.log, editor_output_full.txt, and automation_loop_breaker_report.md if present."
        $guardScript = Join-Path $PSScriptRoot "Guard-AutomationLoop.ps1"
        if (Test-Path -LiteralPath $guardScript) {
            & $guardScript -Model $Model -AgentPath (Get-AgentExe -AgentPath $AgentPath) -ProjectRoot $ProjectRoot
            $guardExit = $LASTEXITCODE
            Write-WatcherLog "Guardian finished with exit code $guardExit"
            if (Test-Path -LiteralPath $LoopBreakerReportPath) {
                Write-WatcherLog "Guardian report written. Exiting watcher. Read Saved/Logs/automation_loop_breaker_report.md (then optionally run Refiner: .\Tools\Run-RefinerAgent.ps1 or Gap-Solver: .\Tools\Run-GapSolverAgent.ps1 if the report mentions automation gaps), fix as needed, and re-run Watch-AutomationAndFix.ps1."
                Write-Host ""
                Write-Host "========================================" -ForegroundColor Cyan
                Write-Host "  WHAT WE WERE UNABLE TO ACCOMPLISH" -ForegroundColor Cyan
                Write-Host "========================================" -ForegroundColor Cyan
                Write-Host "  * Loop failed; Guardian wrote Saved/Logs/automation_loop_breaker_report.md"
                Write-Host "  * Pending tasks and errors: see docs/workflow/CURRENT_TASK_LIST.md and Saved/Logs/automation_errors.log"
                Write-Host ""
                Write-Host "  Document deferred/blocked work in: docs/SESSION_LOG.md, docs/AUTOMATION_GAPS.md, or task docs." -ForegroundColor Yellow
                Write-Host "  The next run will include research and solution-making for these items." -ForegroundColor Yellow
                Write-Host "========================================" -ForegroundColor Cyan
                Write-Host ""
                exit 1
            }
        } else {
            Write-WatcherLog "Guard-AutomationLoop.ps1 not found; running regular fix agent."
        }
    }

    Write-WatcherLog "Main loop exited with code $exitCode. Starting fix agent..."
    $agentExe = Get-AgentExe -AgentPath $AgentPath
    if (-not $agentExe) {
        Write-WatcherLog "ERROR: agent not found. Cannot run fix agent. Run .\Tools\Start-AutomationSession.ps1 once to install, then re-run watcher."
        exit 1
    }

    $failRound = 1
    $lastActivityPath = Join-Path $ProjectRoot "Saved\automation_last_activity.json"
    if (Test-Path -LiteralPath $lastActivityPath) {
        try { $la = Get-Content -Path $lastActivityPath -Raw -Encoding UTF8 | ConvertFrom-Json; if ($la.round) { $failRound = [int]$la.round } } catch {}
    }
    Write-AutomationEvent -EventType fixer_invoked -Message "Fixer started (round $failRound, exit code $exitCode)"
    Write-AgentHandoff -ExitCode $exitCode -Round $failRound -RoleThatFailed "Developer" -SuggestedNextReader "Fixer: read Saved/Logs/agent_handoff.json first, then automation_errors.log and editor_output_filtered.txt (or editor_output_full.txt if cause unclear). See docs/AUTOMATION_EDITOR_LOG.md."

    $errorsPreview = ""
    if (Test-Path -LiteralPath $ErrorsLogPath) {
        $lines = Get-Content -Path $ErrorsLogPath -Tail 30 -ErrorAction SilentlyContinue
        $errorsPreview = if ($lines) { $lines -join "`n" } else { "" }
    }
    $loopTail = ""
    if (Test-Path -LiteralPath $LoopLogPath) {
        $lines = Get-Content -Path $LoopLogPath -Tail 40 -ErrorAction SilentlyContinue
        $loopTail = if ($lines) { $lines -join "`n" } else { "" }
    }
    $terminalCapturePath = Join-Path $LogsDir "automation_terminal_capture.log"
    $terminalCaptureTail = ""
    if (Test-Path -LiteralPath $terminalCapturePath) {
        $lines = Get-Content -Path $terminalCapturePath -Tail 80 -ErrorAction SilentlyContinue
        $terminalCaptureTail = if ($lines) { $lines -join "`n" } else { "" }
    }

    $fixPrompt = @"
You are the **Fixer** in the agent company (see docs/AGENT_COMPANY.md). The **Developer** just failed (exit code $exitCode). You are accountable for: (1) applying a concrete fix so the loop can continue, (2) documenting what you did in SESSION_LOG, (3) optionally suggesting rule/strategy changes so the same failure does not recur.

**Handoff:** Read **Saved/Logs/agent_handoff.json** first for context (exit code, round, last error summary, whether Editor log was captured). Then read the logs below.

**Your responsibilities:**
1. Read Saved/Logs/agent_handoff.json first, then Saved/Logs/automation_errors.log (last entries may be above) and the end of Saved/Logs/automation_loop.log. Also read **Saved/Logs/automation_terminal_capture.log** (last run's full terminal output including any errors that only appeared in the terminal).
2. **Editor log:** If Editor was involved (script, PIE, PCG, Blueprint), read Saved/Logs/editor_output_filtered.txt for a development-relevant excerpt. If the cause is unclear, also read Saved/Logs/editor_output_full.txt. See docs/AUTOMATION_EDITOR_LOG.md for the safety rule (when unfixable, use full log).
3. Diagnose the cause (e.g. API limit, build failure, missing dependency, script error).
4. Apply fixes: code, config, docs, or KNOWN_ERRORS.md as appropriate. If Editor-open or build-related, ensure Safe-Build or Editor-build protocol is used next time. If you block or skip the current task, update docs/workflow/CURRENT_TASK_LIST.md (set status to blocked with reason).
5. **Mandatory:** Append a short entry to docs/SESSION_LOG.md noting that the Fixer (watcher) ran a fix round and what you changed. This holds you accountable for the handoff.
6. **Optional strategy refinement:** If this failure suggests a rule or process change, write Saved/Logs/agent_feedback_this_run.json with: {"suggested_rule_update": "short text or null", "suggested_strategy": "short text or null"}. See docs/AUTOMATION_REFINEMENT.md. Omit the file if you have no suggestions.
7. When done, output clearly: "Fix round complete. Re-run .\Tools\Watch-AutomationAndFix.ps1 to continue (or .\Tools\Start-AutomationSession.ps1 to run without the watcher)."

Do not start the automation loop yourself. The Watcher will re-run the Developer after you exit. If the same failure happens again, the **Guardian** will be invoked to break the loop.
"@

    # Safety rule: when previous fix round(s) did not resolve, instruct Fixer to use unfiltered Editor log (filter may have hidden the error). See docs/AUTOMATION_EDITOR_LOG.md.
    if ($fixRound -ge 1) {
        $fixPrompt += "`n`n**Previous fix round(s) did not resolve the issue.** Read the **unfiltered** Editor log: **Saved/Logs/editor_output_full.txt**. The filtered view may have hidden the relevant error; do not rely only on editor_output_filtered.txt."
    }

    # Inject last lines into prompt so fix agent has context even if it doesn't read files first
    if ($errorsPreview) {
        $fixPrompt += "`n`n--- Last lines of automation_errors.log ---`n$errorsPreview`n---"
    }
    if ($loopTail) {
        $fixPrompt += "`n`n--- Last lines of automation_loop.log ---`n$loopTail`n---"
    }
    if ($terminalCaptureTail) {
        $fixPrompt += "`n`n--- Last lines of automation_terminal_capture.log (full terminal output) ---`n$terminalCaptureTail`n---"
    }

    $agentArgs = @("-p", "-f", "--approve-mcps", "--workspace", $ProjectRoot)
    if ($Model -and $Model.Trim()) { $agentArgs += "--model", $Model.Trim() }
    & $agentExe @agentArgs $fixPrompt
    $fixExit = $LASTEXITCODE
    Write-WatcherLog "Fix agent finished with exit code $fixExit"
    # Append fix-round record for strategy refinement (merge agent_feedback_this_run.json if present)
    $appendScript = Join-Path $PSScriptRoot "Append-AgentRunRecord.ps1"
    if (Test-Path -LiteralPath $appendScript) {
        & $appendScript -ProjectRoot $ProjectRoot -Role fix -Round $fixRound -ExitCode $fixExit -TriggerExitCode $exitCode -ErrorSummary $errorsPreview -Model $Model
    }

    if ($NoRetryAfterFix) {
        Write-WatcherLog "NoRetryAfterFix: exiting. Re-run Watch-AutomationAndFix.ps1 to continue."
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  WHAT WE WERE UNABLE TO ACCOMPLISH" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  * Loop failed; Fixer ran once (NoRetryAfterFix). See Saved/Logs/automation_errors.log and docs/workflow/CURRENT_TASK_LIST.md"
        Write-Host ""
        Write-Host "  Document deferred/blocked work in: docs/SESSION_LOG.md, docs/AUTOMATION_GAPS.md, or task docs." -ForegroundColor Yellow
        Write-Host "  The next run will include research and solution-making for these items." -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        exit $fixExit
    }

    $previousExitCode = $exitCode
    $fixRound++
    if ($fixRound -ge $MaxFixRounds) {
        Write-WatcherLog "Reached MaxFixRounds ($MaxFixRounds). Invoking loop-breaker to write report, then exiting."
        $failRound = 1
        $lastActivityPath = Join-Path $ProjectRoot "Saved\automation_last_activity.json"
        if (Test-Path -LiteralPath $lastActivityPath) {
            try { $la = Get-Content -Path $lastActivityPath -Raw -Encoding UTF8 | ConvertFrom-Json; if ($la.round) { $failRound = [int]$la.round } } catch {}
        }
        Write-AgentHandoff -ExitCode $exitCode -Round $failRound -RoleThatFailed "Developer" -SuggestedNextReader "Guardian: read Saved/Logs/agent_handoff.json first, then automation_errors.log, watcher.log, editor_output_full.txt, and write automation_loop_breaker_report.md if unresolved."
        $guardScript = Join-Path $PSScriptRoot "Guard-AutomationLoop.ps1"
        if (Test-Path -LiteralPath $guardScript) {
            & $guardScript -Model $Model -AgentPath (Get-AgentExe -AgentPath $AgentPath) -ProjectRoot $ProjectRoot | Out-Null
        }
        Write-WatcherLog "Exiting. Read Saved/Logs/automation_loop_breaker_report.md if present, then re-run Watch-AutomationAndFix.ps1."
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  WHAT WE WERE UNABLE TO ACCOMPLISH" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  * Max fix rounds ($MaxFixRounds) reached; Guardian was invoked. See Saved/Logs/automation_loop_breaker_report.md"
        Write-Host "  * Pending tasks: see docs/workflow/CURRENT_TASK_LIST.md. Errors: Saved/Logs/automation_errors.log"
        Write-Host ""
        Write-Host "  Document deferred/blocked work in: docs/SESSION_LOG.md, docs/AUTOMATION_GAPS.md, or task docs." -ForegroundColor Yellow
        Write-Host "  The next run will include research and solution-making for these items." -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        exit 1
    }

    Write-WatcherLog "Re-running main loop (fix round $fixRound of $MaxFixRounds)..."
} while ($true)
