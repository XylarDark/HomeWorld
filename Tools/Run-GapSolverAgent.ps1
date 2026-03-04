# Run-GapSolverAgent.ps1 - Gap-Solver role in the agent company.
# Implements solutions for logged automation gaps (AUTOMATION_GAPS.md). Run when a gap is found
# or after a Guardian report that mentions gaps.
#
# Usage: From project root, .\Tools\Run-GapSolverAgent.ps1 [-ProjectRoot <path>] [-Model <name>] [-AgentPath <path>]
#   -ProjectRoot: Project root (default: parent of Tools or HOMEWORLD_PROJECT).
#   -Model: Pass through to the agent (default "auto").
#
# See docs/AGENT_COMPANY.md, docs/AUTOMATION_GAPS.md, and .cursor/skills/automation-gap-solutions/SKILL.md.

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
$GapsPath = Join-Path $ProjectRoot "docs\AUTOMATION_GAPS.md"
$ResearchPath = Join-Path $ProjectRoot "docs\GAP_SOLUTIONS_RESEARCH.md"
$GapSolverLogPath = Join-Path $LogsDir "gap_solver.log"

function Write-GapSolverLog {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] Run-GapSolverAgent: $Message"
    Write-Host $line
    try { Add-Content -Path $GapSolverLogPath -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue } catch {}
}

function Get-AgentExe {
    if ($AgentPath -and (Test-Path -LiteralPath $AgentPath)) { return $AgentPath }
    $cmd = Get-Command agent -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $searchDirs = @(
        (Join-Path $env:LOCALAPPDATA "cursor-agent"),
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
        $p = Join-Path $dir "agent.ps1"
        if (Test-Path -LiteralPath $p) { return $p }
    }
    return $null
}

if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }

Write-GapSolverLog "Starting Gap-Solver agent (company role: Gap-Solver)."

$agentExe = Get-AgentExe
if (-not $agentExe) {
    Write-GapSolverLog "ERROR: Cursor Agent CLI not found. Run .\Tools\Start-AutomationSession.ps1 once or set PATH."
    exit 1
}

$gapsContent = "(file not found)"
if (Test-Path -LiteralPath $GapsPath) {
    $gapsContent = (Get-Content -Path $GapsPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue)
    if (-not $gapsContent) { $gapsContent = "(unreadable)" }
}

$researchContent = "(file not found)"
if (Test-Path -LiteralPath $ResearchPath) {
    $researchContent = (Get-Content -Path $ResearchPath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue)
    if (-not $researchContent) { $researchContent = "(unreadable)" }
}

$gapSolverPrompt = @"
You are the **Gap-Solver** in the agent company (see docs/AGENT_COMPANY.md). Your role is to **implement solutions for logged automation gaps** so that steps that could not be automated get a programmatic or GUI-automation solution and AUTOMATION_GAPS.md is updated.

**Your responsibilities:**
1. Read docs/AUTOMATION_GAPS.md and docs/GAP_SOLUTIONS_RESEARCH.md (excerpts below).
2. For each gap that does not yet have a solution implemented (or that has an open "Suggested approach" with no Research log closure): implement the solution following .cursor/rules/19-automation-gaps.mdc and the **automation-gap-solutions** skill (.cursor/skills/automation-gap-solutions/SKILL.md).
3. **Prefer programmatic first:** existing C++/Blueprint reuse (e.g. AHomeWorldDungeonEntrance for portal), Python API, or commandlet. Then GUI automation (ref-based script in Content/Python/gui_automation/). Then document outcome only if neither is viable.
4. **Portal (Gap 1):** Ensure place_portal_placeholder.py places AHomeWorldDungeonEntrance with LevelToOpen; if already done, run ensure_demo_portal.py via MCP when Editor is open with DemoMap to apply it, or document that it is applied on next ensure_demo_portal run.
5. **State Tree (Gap 2):** Stub and refs README exist; document in AUTOMATION_GAPS if needed or add any missing ref list/README. No programmatic API; GUI or one-time manual per DAY12_ROLE_PROTECTOR.md.
6. **PCG:** Ensure agents know to run pcg_apply_manual_steps.py when refs exist; no new implementation unless you add a ref or script improvement.
7. **Update** docs/AUTOMATION_GAPS.md (Research log) and/or docs/GAP_SOLUTIONS_RESEARCH.md with what you did (solution implemented, script run, or documented as GUI/manual).

Your output should be actionable: "Gap-Solver complete. Implemented X; updated Y; Z remains GUI/manual because …."

--- docs/AUTOMATION_GAPS.md ---
$gapsContent
--- docs/GAP_SOLUTIONS_RESEARCH.md ---
$researchContent
--- End of excerpts ---
"@

$agentArgs = @("-p", "-f", "--approve-mcps", "--workspace", $ProjectRoot)
if ($Model -and $Model.Trim()) { $agentArgs += "--model", $Model.Trim() }
& $agentExe @agentArgs $gapSolverPrompt
$exitCode = $LASTEXITCODE
Write-GapSolverLog "Gap-Solver agent finished with exit code $exitCode"
exit $exitCode
