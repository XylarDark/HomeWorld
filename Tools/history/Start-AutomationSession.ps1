# Start-AutomationSession.ps1 - One-command start for the 30-day automation loop.
# Installs Cursor Agent CLI if missing, then runs RunAutomationLoop.ps1.
# Use this when you want to "start an automation session" without manually installing the CLI or restarting the terminal.
#
# Usage: From project root, .\Tools\Start-AutomationSession.ps1 [same params as RunAutomationLoop.ps1]
#   -SkipInstall: Do not run the CLI install; only start the loop (fail if agent not found).
#   -Verbose: Pass through to RunAutomationLoop for prompt preview and elapsed time per round (easier to see progress/stalls).
#   All other parameters are passed through to RunAutomationLoop.ps1.
#
# Prerequisites: After first run you may need to run "agent login" once to authenticate.

param(
    [string]$ProjectRoot = "",
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,  # pass through: run without auto-launching the Editor (default is to launch when UE_EDITOR set)
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
if (-not (Test-Path $ProjectRoot)) {
    Write-Error "Project root not found: $ProjectRoot"
    exit 1
}

function Refresh-EnvPath {
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($userPath) { $env:Path = $userPath + ";" + $env:Path }
    if ($machinePath) { $env:Path = $machinePath + ";" + $env:Path }
}

function Write-SessionLog { param([string]$Msg) Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Msg" }
$agentExe = Get-AgentExe -AgentPath $AgentPath
if ($agentExe) { Write-SessionLog "Start-AutomationSession: using agent at $agentExe" }
if (-not $agentExe) {
    Refresh-EnvPath
    $agentExe = Get-AgentExe -AgentPath $AgentPath
}

# 3) Install if missing and not -SkipInstall
if (-not $agentExe -and -not $SkipInstall) {
    Write-SessionLog "Start-AutomationSession: Cursor Agent CLI not found. Installing..."
    try {
        irm 'https://cursor.com/install?win32=true' | iex
    } catch {
        Write-Error "Install failed: $_"
        exit 1
    }
    Refresh-EnvPath
    $agentExe = Get-AgentExe -AgentPath $AgentPath
}

if (-not $agentExe) {
    Write-Error "Cursor Agent CLI (agent) not found. Install manually: irm 'https://cursor.com/install?win32=true' | iex ; then close and reopen your terminal and run this script again."
    exit 1
}

# Build args for RunAutomationLoop.ps1 (pass resolved path so loop does not depend on PATH)
$loopArgs = @{
    ProjectRoot = $ProjectRoot
    AgentPath   = $agentExe
}
if ($PromptFile) { $loopArgs["PromptFile"] = $PromptFile }
if ($NoLaunchEditor) { $loopArgs["NoLaunchEditor"] = $true }
if ($Model) { $loopArgs["Model"] = $Model }
if ($Verbose) { $loopArgs["Verbose"] = $true }

Write-SessionLog "Start-AutomationSession: launching loop script..."
$loopScript = Join-Path $PSScriptRoot "RunAutomationLoop.ps1"
& $loopScript @loopArgs
exit $LASTEXITCODE
