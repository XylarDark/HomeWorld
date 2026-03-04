# Update-AutomationStatusLive.ps1 - Periodically overwrites Saved/Logs/automation_status_latest.txt with Get-AutomationStatus -Short so you can tail the file for a live view.
# Run in a second terminal while the automation loop (or Watcher) is running. Exits when the loop is no longer running (no agent process and last activity > 5 min) or when agent_stop_requested exists.
#
# Usage: From project root, .\Tools\Update-AutomationStatusLive.ps1 [-IntervalSeconds 90] [-ProjectRoot <path>]
#   -IntervalSeconds: How often to refresh (default 90).
#   -ProjectRoot: Project root (default: from Common-Automation Resolve-ProjectRoot).

param(
    [int]$IntervalSeconds = 90,
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "SilentlyContinue"
$scriptRoot = $PSScriptRoot
$commonScript = Join-Path $scriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$LogsDir = Join-Path (Join-Path $ProjectRoot "Saved") "Logs"
$StatusLatestPath = Join-Path $LogsDir "automation_status_latest.txt"
$LastActivityPath = Join-Path $ProjectRoot "Saved\automation_last_activity.json"
$StopSentinelPath = Join-Path $LogsDir "agent_stop_requested"
$GetStatusScript = Join-Path $scriptRoot "Get-AutomationStatus.ps1"

if (-not (Test-Path -LiteralPath $GetStatusScript)) {
    Write-Host "Get-AutomationStatus.ps1 not found. Cannot run live updates."
    exit 1
}

function Test-LoopLikelyRunning {
    $agentProc = Get-Process -Name "agent" -ErrorAction SilentlyContinue
    if ($agentProc) { return $true }
    $nodeProcs = Get-Process -Name "node" -ErrorAction SilentlyContinue
    if ($nodeProcs -and $nodeProcs.Count -gt 0) { return $true }
    if (-not (Test-Path -LiteralPath $LastActivityPath)) { return $false }
    try {
        $last = Get-Content -Path $LastActivityPath -Raw -Encoding UTF8 | ConvertFrom-Json
        $ts = $last.timestamp
        if ($ts -match '(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})') {
            $dt = [DateTime]::ParseExact($ts, "yyyy-MM-dd HH:mm:ss", $null)
            $ageMins = ((Get-Date) - $dt).TotalMinutes
            if ($ageMins -lt 6) { return $true }
        }
    } catch {}
    return $false
}

Write-Host "Update-AutomationStatusLive: writing to $StatusLatestPath every $IntervalSeconds s. Exit with Ctrl+C or when loop is no longer running."
$count = 0
do {
    $count++
    try {
        $out = & $GetStatusScript -Short 6>&1
        if ($out) {
            $text = if ($out -is [string]) { $out } else { ($out -join "`n") }
            Set-Content -Path $StatusLatestPath -Value $text -Encoding UTF8 -ErrorAction SilentlyContinue
        }
    } catch {}
    if (Test-Path -LiteralPath $StopSentinelPath) {
        Write-Host "Stop sentinel detected; exiting."
        break
    }
    if (-not (Test-LoopLikelyRunning)) {
        Write-Host "Loop no longer running (no agent process and last activity > 5 min); exiting."
        break
    }
    Start-Sleep -Seconds $IntervalSeconds
} while ($true)

Write-Host "Update-AutomationStatusLive: stopped after $count update(s)."
