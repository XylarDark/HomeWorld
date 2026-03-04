# Get-AutomationStatus.ps1 - Report automation state so you always know what's happening.
# Run anytime: .\Tools\Get-AutomationStatus.ps1
# Use when the terminal disappears or you want to check if the loop is still running.

param([switch]$Short)

$ErrorActionPreference = "SilentlyContinue"
$scriptRoot = $PSScriptRoot
$commonScript = Join-Path $scriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
$projectRoot = Resolve-ProjectRoot
$projectRoot = $projectRoot.TrimEnd('\', '/')

$lastActivityPath = Join-Path $projectRoot "Saved\automation_last_activity.json"
$loopLogPath = Join-Path $projectRoot "Saved\Logs\automation_loop.log"
$heartbeatLogPath = Join-Path $projectRoot "Saved\Logs\automation_heartbeat.log"
$watcherLogPath = Join-Path $projectRoot "Saved\Logs\watcher.log"
$terminalCapturePath = Join-Path $projectRoot "Saved\Logs\automation_terminal_capture.log"
$eventsLogPath = Join-Path $projectRoot "Saved\Logs\automation_events.log"
$statusLatestPath = Join-Path $projectRoot "Saved\Logs\automation_status_latest.txt"
$taskListPath = Join-Path $projectRoot "docs\workflow\CURRENT_TASK_LIST.md"

Write-Host ""
Write-Host "=== Automation status ===" -ForegroundColor Cyan
Write-Host ""

# 1) Process check
$agentProc = Get-Process -Name "agent" -ErrorAction SilentlyContinue
$nodeProcs = Get-Process -Name "node" -ErrorAction SilentlyContinue
$likelyRunning = ($agentProc -or ($nodeProcs -and $nodeProcs.Count -gt 0))
if ($likelyRunning) {
    Write-Host "Process:  " -NoNewline
    Write-Host "Likely RUNNING (agent or node process found)" -ForegroundColor Green
} else {
    Write-Host "Process:  " -NoNewline
    Write-Host "No agent/node process (loop probably not running or finished)" -ForegroundColor Yellow
}
Write-Host ""

# 2) Current task (what this round is working on; written by RunAutomationLoop)
if (Test-Path -LiteralPath $statusLatestPath) {
    $statusLine = Get-Content -Path $statusLatestPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($statusLine) {
        Write-Host "Current task/round:  " -NoNewline
        Write-Host $statusLine.Trim() -ForegroundColor White
    }
}
Write-Host ""

# 3) Last activity
if (Test-Path -LiteralPath $lastActivityPath) {
    try {
        $last = Get-Content -Path $lastActivityPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $ts = $last.timestamp
        $msg = $last.message
        $round = if ($last.round) { $last.round } else { "?" }
        Write-Host "Last activity: $ts (round $round)" -ForegroundColor White
        Write-Host "  $msg"
        $ageMins = 0
        if ($ts -match '(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})') {
            $dt = [DateTime]::ParseExact($ts, "yyyy-MM-dd HH:mm:ss", $null)
            $ageMins = [math]::Round(((Get-Date) - $dt).TotalMinutes, 1)
        }
        if ($ageMins -gt 5 -and $likelyRunning) {
            Write-Host "  (Activity is $ageMins minutes old; if process is running, agent may be busy or stalled.)" -ForegroundColor Yellow
        } elseif ($ageMins -gt 2 -and -not $likelyRunning) {
            Write-Host "  (Loop has exited.)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "Last activity: (could not read $lastActivityPath)" -ForegroundColor Yellow
    }
} else {
    Write-Host "Last activity: (no file - loop may not have run yet)" -ForegroundColor Gray
}
Write-Host ""

if ($Short) {
    Write-Host "Run without -Short for full log tails and task list status." -ForegroundColor Gray
    Write-Host ""
    return
}

# 4) Last high-level events (round completed, build validated, Fixer/Guardian invoked, PIE validation, etc.)
if (Test-Path -LiteralPath $eventsLogPath) {
    Write-Host "--- Last 10 lines: automation_events.log (high-level event stream) ---" -ForegroundColor Cyan
    Get-Content -Path $eventsLogPath -Tail 10 -Encoding UTF8 -ErrorAction SilentlyContinue | ForEach-Object { Write-Host $_ }
    Write-Host ""
}

# 5) Heartbeat progress log (what has happened; written every 1 min while agent runs)
if (Test-Path -LiteralPath $heartbeatLogPath) {
    Write-Host "--- Last 20 lines: automation_heartbeat.log (progress) ---" -ForegroundColor Cyan
    Get-Content -Path $heartbeatLogPath -Tail 20 -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    Write-Host ""
}

# 6) Loop log tail
if (Test-Path -LiteralPath $loopLogPath) {
    Write-Host "--- Last 8 lines: automation_loop.log ---" -ForegroundColor Cyan
    Get-Content -Path $loopLogPath -Tail 8 -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    Write-Host ""
}

# 6) Watcher log tail
if (Test-Path -LiteralPath $watcherLogPath) {
    Write-Host "--- Last 5 lines: watcher.log ---" -ForegroundColor Cyan
    Get-Content -Path $watcherLogPath -Tail 5 -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    Write-Host ""
}

# 8) Terminal capture (last run's full output; errors that only appeared in the terminal)
if (Test-Path -LiteralPath $terminalCapturePath) {
    Write-Host "--- Last 25 lines: automation_terminal_capture.log (terminal output for chat/Fixer) ---" -ForegroundColor Cyan
    Get-Content -Path $terminalCapturePath -Tail 25 -Encoding UTF8 | ForEach-Object { Write-Host $_ }
    Write-Host ""
}

# 9) Pending tasks (T1–T10 only)
if (Test-Path -LiteralPath $taskListPath) {
    $text = Get-Content -Path $taskListPath -Raw -Encoding UTF8
    $hasPending = $text -match "status:\s*(pending|in_progress)"
    Write-Host "Task list:  " -NoNewline
    if ($hasPending) {
        Write-Host "Has pending or in_progress tasks (loop would continue)" -ForegroundColor Yellow
    } else {
        Write-Host "No pending/in_progress (loop exits when it sees this)" -ForegroundColor Green
    }
} else {
    Write-Host "Task list:  CURRENT_TASK_LIST.md not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== End status ===" -ForegroundColor Cyan
Write-Host ""
