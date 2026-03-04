# Run-RefinerAgent.ps1 - Fourth role in the agent company: Refiner.
# Reads run history and errors, updates rules and strategy so the same failures don't recur.
# Run on-demand or after a Guardian report to keep the company improving.
#
# Usage: From project root, .\Tools\Run-RefinerAgent.ps1 [-ProjectRoot <path>] [-Model <name>] [-AgentPath <path>]
#   -ProjectRoot: Project root (default: parent of Tools or HOMEWORLD_PROJECT).
#   -Model: Pass through to the agent (default "auto").
#
# See docs/AGENT_COMPANY.md and docs/AUTOMATION_REFINEMENT.md.

param(
    [string]$ProjectRoot = "",
    [string]$Model = "auto",
    [string]$AgentPath = ""
)

$ErrorActionPreference = "Stop"
if (-not $ProjectRoot) { $ProjectRoot = $env:HOMEWORLD_PROJECT }
if (-not $ProjectRoot) { $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")
$SavedDir = Join-Path $ProjectRoot "Saved"
$LogsDir = Join-Path $SavedDir "Logs"
$HistoryPath = Join-Path $LogsDir "agent_run_history.ndjson"
$ErrorsLogPath = Join-Path $LogsDir "automation_errors.log"
$ReportPath = Join-Path $LogsDir "automation_loop_breaker_report.md"
$RefinerLogPath = Join-Path $LogsDir "refiner.log"

function Write-RefinerLog {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] Run-RefinerAgent: $Message"
    Write-Host $line
    try { Add-Content -Path $RefinerLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue } catch {}
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

if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }

Write-RefinerLog "Starting Refiner agent (company role: Refiner)."

$agentExe = Get-AgentExe
if (-not $agentExe) {
    Write-RefinerLog "ERROR: Cursor Agent CLI not found. Run .\Tools\Start-AutomationSession.ps1 once or set PATH."
    exit 1
}

$historyPreview = ""
if (Test-Path -LiteralPath $HistoryPath) {
    $lines = (Get-Content -Path $HistoryPath -Tail 60 -ErrorAction SilentlyContinue)
    $historyPreview = if ($lines) { $lines -join "`n" } else { "(empty or unreadable)" }
} else {
    $historyPreview = "(agent_run_history.ndjson not found yet; run the automation loop at least once)"
}

$errorsPreview = ""
if (Test-Path -LiteralPath $ErrorsLogPath) {
    $errLines = (Get-Content -Path $ErrorsLogPath -Tail 40 -ErrorAction SilentlyContinue)
    $errorsPreview = if ($errLines) { $errLines -join "`n" } else { "(empty)" }
} else {
    $errorsPreview = "(automation_errors.log not found)"
}

$reportPreview = ""
if (Test-Path -LiteralPath $ReportPath) {
    $reportPreview = (Get-Content -Path $ReportPath -Raw -ErrorAction SilentlyContinue)
    if (-not $reportPreview) { $reportPreview = "(unreadable)" }
} else {
    $reportPreview = "(no Guardian report present)"
}

$refinerPrompt = @"
You are the **Refiner** in the agent company (see docs/AGENT_COMPANY.md). Your role is to keep the other agents accountable and improve the development process by turning run history and errors into **concrete updates to rules and strategy** so the same failures do not recur.

**Your responsibilities:**
1. Read the run history and error excerpts below (and Guardian report if present).
2. Identify repeated exit codes, repeated error patterns, and any suggested_rule_update or suggested_strategy from the history.
3. **Update** at least one of: docs/KNOWN_ERRORS.md, .cursor/rules/*.mdc, AGENTS.md, or docs/workflow/ / docs/CONVENTIONS.md with concrete changes (add an entry, add a rule, update a procedure). If the Guardian left a report, use it as a primary input.
4. Optionally note whether the Developer, Fixer, and Guardian left the expected artifacts (SESSION_LOG updates, report when unresolved); if something is missing, add a short note to SESSION_LOG or to the refinement doc so the process improves.
5. **Automation gaps:** If run history or automation_loop_breaker_report mentions an automation gap (Level Streaming/portal, State Tree, PCG no-access), recommend running the **Gap-Solver** (.\Tools\Run-GapSolverAgent.ps1 or run-gap-solver command) to implement solutions; the Gap-Solver is the role responsible for closing gaps. See docs/AGENT_COMPANY.md, docs/GAP_SOLUTIONS_RESEARCH.md, and .cursor/skills/automation-gap-solutions/SKILL.md.

Follow docs/AUTOMATION_REFINEMENT.md for how to use the run history. Your output should be actionable: either "Refiner complete. Updated X, Y, Z." or "Refiner complete. No recurring patterns yet; added note to …."

--- Last 60 lines of agent_run_history.ndjson ---
$historyPreview
--- Last 40 lines of automation_errors.log ---
$errorsPreview
--- Guardian report (if any) ---
$reportPreview
--- End of excerpts ---
"@

$agentArgs = @("-p", "-f", "--approve-mcps", "--workspace", $ProjectRoot)
if ($Model -and $Model.Trim()) { $agentArgs += "--model", $Model.Trim() }
& $agentExe @agentArgs $refinerPrompt
$exitCode = $LASTEXITCODE
Write-RefinerLog "Refiner agent finished with exit code $exitCode"
exit $exitCode
