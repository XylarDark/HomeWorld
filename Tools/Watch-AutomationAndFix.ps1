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
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

if (-not $ProjectRoot) { $ProjectRoot = $env:HOMEWORLD_PROJECT }
if (-not $ProjectRoot) { $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$SavedDir = Join-Path $ProjectRoot "Saved"
$LogsDir = Join-Path $SavedDir "Logs"
if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }
$WatcherLogPath = Join-Path $LogsDir "watcher.log"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"
$LoopLogPath = Join-Path $LogsDir "automation_loop.log"
$LoopBreakerReportPath = Join-Path $LogsDir "automation_loop_breaker_report.md"

function Write-WatcherLog {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] Watch-AutomationAndFix: $Message"
    Write-Host $line
    try { Add-Content -Path $WatcherLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue } catch {}
}

function Get-AgentExe {
    if ($AgentPath -and (Test-Path -LiteralPath $AgentPath)) { return $AgentPath }
    $cmd = Get-Command agent -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $searchDirs = @(
        (Join-Path $env:LOCALAPPDATA "cursor-cli"),
        (Join-Path (Join-Path $env:LOCALAPPDATA "Cursor") "agent"),
        (Join-Path (Join-Path $env:USERPROFILE ".cursor") "bin"),
        (Join-Path (Join-Path $env:LOCALAPPDATA "Programs") "cursor-cli")
    )
    foreach ($dir in $searchDirs) {
        if (-not $dir -or -not (Test-Path $dir)) { continue }
        $exe = Join-Path $dir "agent.exe"
        if (Test-Path -LiteralPath $exe) { return $exe }
        $c = Join-Path $dir "agent.cmd"
        if (Test-Path -LiteralPath $c) { return $c }
    }
    return $null
}

$fixRound = 0
$previousExitCode = $null
do {
    Write-WatcherLog "Starting main automation loop (fix round $fixRound / $MaxFixRounds)..."
    $sessionArgs = @{ ProjectRoot = $ProjectRoot }
    $resolvedAgent = Get-AgentExe
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
        Write-WatcherLog "Main loop exited successfully (no pending days or normal exit). Done."
        exit 0
    }

    # Loop detection: same failure twice in a row -> run loop-breaker (third agent) instead of fix agent
    $sameFailureAgain = ($previousExitCode -ne $null -and $previousExitCode -eq $exitCode -and $fixRound -ge 1)
    if ($sameFailureAgain) {
        Write-WatcherLog "Loop detected: same exit code $exitCode again. Invoking Guardian (Guard-AutomationLoop) instead of Fixer..."
        $guardScript = Join-Path $PSScriptRoot "Guard-AutomationLoop.ps1"
        if (Test-Path -LiteralPath $guardScript) {
            & $guardScript -Model $Model -AgentPath (Get-AgentExe) -ProjectRoot $ProjectRoot
            $guardExit = $LASTEXITCODE
            Write-WatcherLog "Guardian finished with exit code $guardExit"
            if (Test-Path -LiteralPath $LoopBreakerReportPath) {
                Write-WatcherLog "Guardian report written. Exiting watcher. Read Saved/Logs/automation_loop_breaker_report.md (then optionally run Refiner: .\Tools\Run-RefinerAgent.ps1 or Gap-Solver: .\Tools\Run-GapSolverAgent.ps1 if the report mentions automation gaps), fix as needed, and re-run Watch-AutomationAndFix.ps1."
                exit 1
            }
        } else {
            Write-WatcherLog "Guard-AutomationLoop.ps1 not found; running regular fix agent."
        }
    }

    Write-WatcherLog "Main loop exited with code $exitCode. Starting fix agent..."
    $agentExe = Get-AgentExe
    if (-not $agentExe) {
        Write-WatcherLog "ERROR: agent not found. Cannot run fix agent. Run .\Tools\Start-AutomationSession.ps1 once to install, then re-run watcher."
        exit 1
    }

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

    $fixPrompt = @"
You are the **Fixer** in the agent company (see docs/AGENT_COMPANY.md). The **Developer** just failed (exit code $exitCode). You are accountable for: (1) applying a concrete fix so the loop can continue, (2) documenting what you did in SESSION_LOG, (3) optionally suggesting rule/strategy changes so the same failure does not recur.

**Your responsibilities:**
1. Read Saved/Logs/automation_errors.log (last entries may be above) and the end of Saved/Logs/automation_loop.log.
2. Diagnose the cause (e.g. API limit, build failure, missing dependency, script error).
3. Apply fixes: code, config, docs, or KNOWN_ERRORS.md as appropriate. If Editor-open or build-related, ensure Safe-Build or Editor-build protocol is used next time.
4. **Mandatory:** Append a short entry to docs/SESSION_LOG.md noting that the Fixer (watcher) ran a fix round and what you changed. This holds you accountable for the handoff.
5. **Optional strategy refinement:** If this failure suggests a rule or process change, write Saved/Logs/agent_feedback_this_run.json with: {"suggested_rule_update": "short text or null", "suggested_strategy": "short text or null"}. See docs/AUTOMATION_REFINEMENT.md. Omit the file if you have no suggestions.
6. When done, output clearly: "Fix round complete. Re-run .\Tools\Watch-AutomationAndFix.ps1 to continue (or .\Tools\Start-AutomationSession.ps1 to run without the watcher)."

Do not start the automation loop yourself. The Watcher will re-run the Developer after you exit. If the same failure happens again, the **Guardian** will be invoked to break the loop.
"@

    # Inject last lines into prompt so fix agent has context even if it doesn't read files first
    if ($errorsPreview) {
        $fixPrompt += "`n`n--- Last lines of automation_errors.log ---`n$errorsPreview`n---"
    }
    if ($loopTail) {
        $fixPrompt += "`n`n--- Last lines of automation_loop.log ---`n$loopTail`n---"
    }

    $agentArgs = @("-p", "-f", "--approve-mcps", "--workspace", $ProjectRoot)
    if ($Model -and $Model.Trim()) { $agentArgs += "--model", $Model.Trim() }
    & $agentExe @agentArgs $fixPrompt
    $fixExit = $LASTEXITCODE
    Write-WatcherLog "Fix agent finished with exit code $fixExit"
    # Append fix-round record for strategy refinement (merge agent_feedback_this_run.json if present)
    $appendScript = Join-Path $PSScriptRoot "Append-AgentRunRecord.ps1"
    if (Test-Path -LiteralPath $appendScript) {
        & $appendScript -ProjectRoot $ProjectRoot -Role fix -Round $fixRound -ExitCode $fixExit -TriggerExitCode $exitCode -ErrorSummary $errorsPreview
    }

    if ($NoRetryAfterFix) {
        Write-WatcherLog "NoRetryAfterFix: exiting. Re-run Watch-AutomationAndFix.ps1 to continue."
        exit $fixExit
    }

    $previousExitCode = $exitCode
    $fixRound++
    if ($fixRound -ge $MaxFixRounds) {
        Write-WatcherLog "Reached MaxFixRounds ($MaxFixRounds). Invoking loop-breaker to write report, then exiting."
        $guardScript = Join-Path $PSScriptRoot "Guard-AutomationLoop.ps1"
        if (Test-Path -LiteralPath $guardScript) {
            & $guardScript -Model $Model -AgentPath (Get-AgentExe) -ProjectRoot $ProjectRoot | Out-Null
        }
        Write-WatcherLog "Exiting. Read Saved/Logs/automation_loop_breaker_report.md if present, then re-run Watch-AutomationAndFix.ps1."
        exit 1
    }

    Write-WatcherLog "Re-running main loop (fix round $fixRound of $MaxFixRounds)..."
} while ($true)
