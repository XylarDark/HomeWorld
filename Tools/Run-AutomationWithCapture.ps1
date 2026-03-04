# Run-AutomationWithCapture.ps1 - Run the agent company with full terminal output captured and window never auto-closed.
# All stdout/stderr is teed to Saved/Logs/automation_terminal_capture.log so chat/Fixer can read it.
# The window stays open until you press Enter (or close it yourself). Only you terminate the terminal.
#
# Usage: .\Tools\Run-AutomationWithCapture.ps1 [same params as Start-AllAgents.ps1]
# Usually invoked by Start-AllAgents-InNewWindow.ps1 or Start-AllAgents.bat.

param(
    [string]$ProjectRoot = "",
    [int]$MaxFixRounds = 3,
    [switch]$NoRetryAfterFix,
    [switch]$NoPauseOnComplete,
    [string]$PromptFile = "",
    [switch]$NoLaunchEditor,
    [string]$Model = "auto",
    [string]$AgentPath = "",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$scriptRoot = $PSScriptRoot
$commonScript = Join-Path $scriptRoot "Common-Automation.ps1"
if (Test-Path -LiteralPath $commonScript) { . $commonScript }
if (-not $ProjectRoot) { $ProjectRoot = Resolve-ProjectRoot }
$ProjectRoot = $ProjectRoot.TrimEnd("\", "/")

$LogsDir = Join-Path $ProjectRoot "Saved\Logs"
if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }
$CapturePath = Join-Path $LogsDir "automation_terminal_capture.log"

$mainScript = Join-Path $scriptRoot "Start-AllAgents.ps1"
if (-not (Test-Path -LiteralPath $mainScript)) {
    $err = "Start-AllAgents.ps1 not found at $mainScript"
    Write-Error $err
    Add-Content -Path $CapturePath -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $err" -Encoding UTF8 -ErrorAction SilentlyContinue
    Read-Host "Press Enter to close this window"
    exit 1
}

# Start-of-run header so we can find "last run" in the capture file
$runHeader = "`n=== Run started $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===`n"
Add-Content -Path $CapturePath -Value $runHeader -Encoding UTF8 -ErrorAction SilentlyContinue
Write-Host $runHeader.Trim()

# Run Start-AllAgents; tee all output (stdout + stderr) to capture file and console
$params = @{
    ProjectRoot  = $ProjectRoot
    MaxFixRounds = $MaxFixRounds
}
if ($NoRetryAfterFix) { $params['NoRetryAfterFix'] = $true }
if ($NoPauseOnComplete) { $params['NoPauseOnComplete'] = $true }
if ($PromptFile) { $params['PromptFile'] = $PromptFile }
if ($NoLaunchEditor) { $params['NoLaunchEditor'] = $true }
if ($Model) { $params['Model'] = $Model }
if ($AgentPath) { $params['AgentPath'] = $AgentPath }
if ($SkipInstall) { $params['SkipInstall'] = $true }
if ($Verbose) { $params['Verbose'] = $true }

$exitCode = 0
try {
    $output = & $mainScript @params 2>&1
    if ($null -ne $LASTEXITCODE) { $exitCode = $LASTEXITCODE }
    $output | ForEach-Object { Write-Host $_ }
    $output | Add-Content -Path $CapturePath -Encoding UTF8 -ErrorAction SilentlyContinue
} catch {
    $errText = $_ | Out-String
    Write-Host $errText
    Add-Content -Path $CapturePath -Value $errText -Encoding UTF8 -ErrorAction SilentlyContinue
    $exitCode = 1
}
$exitLine = "`n=== Run ended $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') EXIT CODE: $exitCode ===`n"
Add-Content -Path $CapturePath -Value $exitLine -Encoding UTF8 -ErrorAction SilentlyContinue
Write-Host $exitLine.Trim()

# Terminal is only closed by the user
Write-Host ""
Write-Host "Output was captured to Saved/Logs/automation_terminal_capture.log (chat and Fixer can read it)." -ForegroundColor Gray
Read-Host "Press Enter to close this window (only you can terminate the terminal)"
exit $exitCode
