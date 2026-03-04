# Guard-AutomationLoop.ps1 - Third agent: detects if the main loop and fix agent are in a repeating failure loop,
# runs a "loop-breaker" agent to try to resolve it; if the loop-breaker cannot resolve, ensures a report is written to a file.
#
# Run manually when you suspect a loop, or run on a schedule, or the watcher can invoke the loop-breaker when it detects repeat failures.
#
# Usage: From project root, .\Tools\Guard-AutomationLoop.ps1 [-CheckOnly] [-Model <name>] [-AgentPath <path>]
#   -CheckOnly: Only check logs and report whether a loop was detected (exit 0 = no loop, 1 = loop detected); do not run the loop-breaker agent.
#   -Model: Pass through to the loop-breaker agent (default "auto").
#
# Loop detection: Same non-zero exit code 2+ times in recent automation_loop.log; or "Starting fix agent" 2+ times in watcher.log; or repeated similar errors in automation_errors.log.
# When loop detected: Run loop-breaker agent once. Then ensure Saved/Logs/automation_loop_breaker_report.md exists (create minimal report if the agent did not write one).

param(
    [switch]$CheckOnly,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "Stop"
if (-not $ProjectRoot) { $ProjectRoot = $env:HOMEWORLD_PROJECT }
if (-not $ProjectRoot) { $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$SavedDir = Join-Path $ProjectRoot "Saved"
$LogsDir = Join-Path $SavedDir "Logs"
$LoopLogPath = Join-Path $LogsDir "automation_loop.log"
$WatcherLogPath = Join-Path $LogsDir "watcher.log"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"
$GuardianLogPath = Join-Path $LogsDir "guardian.log"
$ReportPath = Join-Path $LogsDir "automation_loop_breaker_report.md"

function Write-GuardianLog {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] Guard-AutomationLoop: $Message"
    Write-Host $line
    try { Add-Content -Path $GuardianLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue } catch {}
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

# Read last N lines from a log file
function Get-LogTail {
    param([string]$Path, [int]$Lines = 80)
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    return Get-Content -Path $Path -Tail $Lines -ErrorAction SilentlyContinue
}

# Detect loop: same exit code 2+ times in loop log, or 2+ fix rounds in watcher, or repeated error pattern
function Test-LoopDetected {
    $loopLines = Get-LogTail -Path $LoopLogPath -Lines 60
    $exitCodes = @()
    foreach ($line in $loopLines) {
        if ($line -match "agent finished.*exit code=(\d+|-\d+)") {
            $code = [int]$Matches[1]
            if ($code -ne 0) { $exitCodes += $code }
        }
    }
    if ($exitCodes.Count -ge 2) {
        $last = $exitCodes[-1]
        $prev = $exitCodes[-2]
        if ($last -eq $prev) {
            Write-GuardianLog "Loop detected: same exit code $last twice in automation_loop.log"
            return $true
        }
    }

    $watcherLines = Get-LogTail -Path $WatcherLogPath -Lines 40
    $fixStarts = ($watcherLines | Select-String -Pattern "Starting fix agent").Count
    if ($fixStarts -ge 2) {
        Write-GuardianLog "Loop detected: fix agent started $fixStarts times in watcher.log"
        return $true
    }

    $errorLines = Get-LogTail -Path $ErrorsLogPath -Lines 30
    if ($errorLines.Count -ge 4) {
        $lastErr = ($errorLines -join " ") -replace "\s+", " "
        $firstHalf = ($errorLines[0..([math]::Min(14, $errorLines.Count-1))] -join " ") -replace "\s+", " "
        $secondHalf = ($errorLines[15..($errorLines.Count-1)] -join " ") -replace "\s+", " "
        if ($firstHalf.Length -gt 20 -and $secondHalf.Length -gt 20 -and $firstHalf -eq $secondHalf) {
            Write-GuardianLog "Loop detected: repeated error block in automation_errors.log"
            return $true
        }
    }
    return $false
}

if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }

Write-GuardianLog "Checking logs for loop..."
$loopDetected = Test-LoopDetected
if (-not $loopDetected) {
    Write-GuardianLog "No loop detected. Exit 0."
    exit 0
}

if ($CheckOnly) {
    Write-GuardianLog "CheckOnly: loop detected; not running loop-breaker. Exit 1."
    exit 1
}

Write-GuardianLog "Running loop-breaker agent..."
$agentExe = Get-AgentExe
if (-not $agentExe) {
    Write-GuardianLog "ERROR: agent not found. Writing minimal report and exiting."
    $report = @"
# Automation loop – guardian report (no loop-breaker run)

**Time:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Reason:** Loop was detected but the Cursor Agent CLI (agent) was not found, so the loop-breaker agent could not run.

**Recommended steps:**
1. Install or fix the agent (run `.\Tools\Start-AutomationSession.ps1` once or set PATH).
2. Re-run `.\Tools\Guard-AutomationLoop.ps1` to invoke the loop-breaker, or read the logs and fix manually.

**Logs:** Saved/Logs/automation_errors.log, Saved/Logs/watcher.log, Saved/Logs/automation_loop.log
"@
    Set-Content -Path $ReportPath -Value $report -Encoding UTF8
    exit 1
}

$loopTail = (Get-LogTail -Path $LoopLogPath -Lines 50) -join "`n"
$watcherTail = (Get-LogTail -Path $WatcherLogPath -Lines 40) -join "`n"
$errorsTail = (Get-LogTail -Path $ErrorsLogPath -Lines 35) -join "`n"

$loopBreakerPrompt = @"
You are the **Guardian** in the agent company (see docs/AGENT_COMPANY.md). The **Developer** and **Fixer** are in a **repeating failure loop** (same error or same exit code). You are accountable for either breaking the loop with a different fix or writing a full report so the user (or the **Refiner**) can continue. Development must not stop without a clear handoff.

**Your responsibilities:**
1. **Analyze** why the same failure keeps recurring (read the log excerpts below).
2. **Try a different fix** than the Fixer already tried: e.g. skip the failing day in docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md (set to blocked with reason), add a guard in code, change strategy, or log the gap in docs/AUTOMATION_GAPS.md.
3. **If you cannot resolve the loop**, you MUST write a full report to **Saved/Logs/automation_loop_breaker_report.md** with:
   - Summary of the loop (what keeps failing)
   - What the Fixer already tried (from watcher log)
   - Recommended manual steps for the user
   - **If the loop is due to or related to an automation gap** (e.g. Level Streaming/portal, State Tree, PCG no-access): recommend running the **Gap-Solver** (.\Tools\Run-GapSolverAgent.ps1 or run-gap-solver command) to implement solutions for logged gaps. See docs/AGENT_COMPANY.md (Gap-Solver role).
   - Key excerpts from the logs (last 20 lines of automation_errors.log and last 15 of watcher.log)
   If you do not write this file, the system will create a minimal report; your job is to leave a useful handoff so development can continue (e.g. via Refiner, Gap-Solver, or user).
4. **Strategy refinement:** Write **Saved/Logs/agent_feedback_this_run.json** with: {"suggested_rule_update": "one line or null", "suggested_strategy": "one line or null"}. This feed is used by the Refiner and docs to update rules and strategy. See docs/AUTOMATION_REFINEMENT.md.

Do not start the automation loop or watcher yourself. When done, output clearly: "Guardian round complete. If unresolved, see Saved/Logs/automation_loop_breaker_report.md."

--- Last 50 lines of automation_loop.log ---
$loopTail
--- Last 40 lines of watcher.log ---
$watcherTail
--- Last 35 lines of automation_errors.log ---
$errorsTail
--- End of log excerpts ---
"@

$agentArgs = @("-p", "-f", "--approve-mcps", "--workspace", $ProjectRoot)
if ($Model -and $Model.Trim()) { $agentArgs += "--model", $Model.Trim() }
& $agentExe @agentArgs $loopBreakerPrompt
$breakerExit = $LASTEXITCODE
Write-GuardianLog "Loop-breaker agent finished with exit code $breakerExit"
# Append loop-breaker record for strategy refinement (merge agent_feedback_this_run.json if present)
$appendScript = Join-Path $PSScriptRoot "Append-AgentRunRecord.ps1"
if (Test-Path -LiteralPath $appendScript) {
    $errSummary = (Get-LogTail -Path $ErrorsLogPath -Lines 15) -join " "
    & $appendScript -ProjectRoot $ProjectRoot -Role loop_breaker -Round 1 -ExitCode $breakerExit -ErrorSummary $errSummary
}

if (-not (Test-Path -LiteralPath $ReportPath)) {
    Write-GuardianLog "Loop-breaker did not write report; writing minimal report."
    $minimalReport = @"
# Automation loop – guardian report

**Time:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Status:** Loop was detected. The loop-breaker agent was run but did not create this file; the guardian created this minimal report.

**Recommended steps:**
1. Read Saved/Logs/automation_errors.log and Saved/Logs/watcher.log for the repeating failure.
2. Fix the root cause (e.g. API limit, build failure, skip the failing day, or add to AUTOMATION_GAPS.md). If the loop is due to an automation gap, run **Gap-Solver**: `.\Tools\Run-GapSolverAgent.ps1` (or run-gap-solver command).
3. Optionally run Refiner: `.\Tools\Run-RefinerAgent.ps1` to update rules from run history.
4. Re-run `.\Tools\Watch-AutomationAndFix.ps1` or `.\Tools\Start-AutomationSession.ps1` to continue.

**Logs:** automation_errors.log, watcher.log, automation_loop.log, guardian.log
"@
    Set-Content -Path $ReportPath -Value $minimalReport -Encoding UTF8
}

Write-GuardianLog "Done. Report ensured at $ReportPath. Exit 1 (loop was detected)."
exit 1
